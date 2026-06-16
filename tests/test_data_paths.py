"""
Tests for packages/orchestration/data_paths.py — Step 32: Repository Structure Foundation.

Verifies:
- env var override returns the env-specified root
- default root ends with ".data"
- directory helpers append the correct subdirectory names
- directory helpers accept an explicit root argument
- data_paths.py is the only production Python file reading REMEDY_DATA_DIR
"""

from __future__ import annotations

import re
from pathlib import Path


class TestResolveDataRoot:
    def test_env_var_override(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration import data_paths
        # Reimport to bypass cached calls (function reads env at call time)
        result = data_paths.resolve_data_root()
        assert result == tmp_path

    def test_default_ends_with_data(self, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        from packages.orchestration import data_paths
        result = data_paths.resolve_data_root()
        assert result.name == ".data"

    def test_default_is_inside_repo(self, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        from packages.orchestration import data_paths
        result = data_paths.resolve_data_root()
        # .data should be at the repo root, not inside packages/
        assert "packages" not in result.parts

    def test_env_var_none_uses_file_based_root(self, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        from packages.orchestration import data_paths
        r1 = data_paths.resolve_data_root()
        r2 = data_paths.resolve_data_root()
        assert r1 == r2


class TestDirectoryHelpers:
    def test_jobs_dir_default(self, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        from packages.orchestration.data_paths import jobs_dir, resolve_data_root
        assert jobs_dir() == resolve_data_root() / "jobs"

    def test_runs_dir_default(self, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        from packages.orchestration.data_paths import resolve_data_root, runs_dir
        assert runs_dir() == resolve_data_root() / "runs"

    def test_projects_dir_default(self, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        from packages.orchestration.data_paths import projects_dir, resolve_data_root
        assert projects_dir() == resolve_data_root() / "projects"

    def test_workspaces_dir_default(self, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        from packages.orchestration.data_paths import resolve_data_root, workspaces_dir
        assert workspaces_dir() == resolve_data_root() / "workspaces"

    def test_viewers_dir_default(self, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        from packages.orchestration.data_paths import resolve_data_root, viewers_dir
        assert viewers_dir() == resolve_data_root() / "viewers"

    def test_jobs_dir_explicit_root(self, tmp_path):
        from packages.orchestration.data_paths import jobs_dir
        assert jobs_dir(tmp_path) == tmp_path / "jobs"

    def test_runs_dir_explicit_root(self, tmp_path):
        from packages.orchestration.data_paths import runs_dir
        assert runs_dir(tmp_path) == tmp_path / "runs"

    def test_projects_dir_explicit_root(self, tmp_path):
        from packages.orchestration.data_paths import projects_dir
        assert projects_dir(tmp_path) == tmp_path / "projects"

    def test_workspaces_dir_explicit_root(self, tmp_path):
        from packages.orchestration.data_paths import workspaces_dir
        assert workspaces_dir(tmp_path) == tmp_path / "workspaces"

    def test_viewers_dir_explicit_root(self, tmp_path):
        from packages.orchestration.data_paths import viewers_dir
        assert viewers_dir(tmp_path) == tmp_path / "viewers"

    def test_env_override_propagates_to_helpers(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import jobs_dir, projects_dir, runs_dir
        assert jobs_dir() == tmp_path / "jobs"
        assert runs_dir() == tmp_path / "runs"
        assert projects_dir() == tmp_path / "projects"


class TestSingleReaderInvariant:
    """Verify data_paths.py is the only production Python file reading REMEDY_DATA_DIR."""

    def _find_repo_root(self) -> Path:
        from packages.orchestration import data_paths
        # data_paths.py is at packages/orchestration/data_paths.py → repo root 3 up
        return Path(data_paths.__file__).resolve().parents[2]

    def test_no_inline_env_read_in_apps(self):
        repo = self._find_repo_root()
        env_re = re.compile(r'os\.environ\.get\(["\']REMEDY_DATA_DIR["\']')
        violations = []
        for p in (repo / "apps").rglob("*.py"):
            if "test_" in p.name:
                continue
            text = p.read_text()
            if env_re.search(text):
                violations.append(str(p.relative_to(repo)))
        assert violations == [], f"Production apps/ files directly read REMEDY_DATA_DIR: {violations}"

    def test_no_inline_env_read_in_packages(self):
        repo = self._find_repo_root()
        env_re = re.compile(r'os\.environ\.get\(["\']REMEDY_DATA_DIR["\']')
        violations = []
        for p in (repo / "packages").rglob("*.py"):
            if p.name == "data_paths.py":
                continue
            if "test_" in p.name:
                continue
            text = p.read_text()
            if env_re.search(text):
                violations.append(str(p.relative_to(repo)))
        assert violations == [], f"Production packages/ files directly read REMEDY_DATA_DIR: {violations}"
