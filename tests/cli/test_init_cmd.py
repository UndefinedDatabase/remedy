"""Tests for ``remedy init`` (F081 T001 + T002)."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

import pytest

_CLI = [sys.executable, "-m", "apps.cli.grouped"]


def _make_env(tmp_path):
    """Build subprocess env with REMEDY_DATA_DIR isolated to tmp_path."""
    return {
        **os.environ,
        "PYTHONPATH": os.getcwd(),
        "REMEDY_DATA_DIR": str(tmp_path / "data"),
    }


def _make_git_repo(tmp_path):
    """Create a bare git repo in tmp_path and return the path."""
    subprocess.run(
        ["git", "init", "-q", str(tmp_path)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return tmp_path


def _snapshot_mtimes(projects_dir):
    """Return {filename: mtime} for all files in projects_dir."""
    if not os.path.isdir(projects_dir):
        return {}
    return {f: os.path.getmtime(os.path.join(projects_dir, f))
            for f in os.listdir(projects_dir)}


def _run_init(repo, env, extra_args=None):
    return subprocess.run(
        [*_CLI, "init", *(extra_args or [])],
        capture_output=True, text=True, timeout=30,
        cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
    )


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# T001: Preflight + Registry + Idempotency
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestInitCmd:

    def test_fresh_repo_creates_project(self, tmp_path):
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r = _run_init(repo, env)
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

    def test_second_run_idempotent(self, tmp_path):
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r1 = _run_init(repo, env)
        assert r1.returncode == 0

        projects = str(tmp_path / "data" / "projects")
        mtime_before = _snapshot_mtimes(projects)
        assert mtime_before, "first run should have created project files"

        r2 = _run_init(repo, env)
        assert r2.returncode == 0, f"stderr: {r2.stderr}"
        assert "[exists] project " in r2.stdout
        for line in r2.stdout.strip().splitlines():
            assert line.strip().startswith("[exists]"), f"unexpected line: {line}"

        mtime_after = _snapshot_mtimes(projects)
        assert mtime_before == mtime_after, (
            f"second run modified project files: before={mtime_before}, after={mtime_after}"
        )

    def test_non_git_exit_4(self, tmp_path):
        plain_dir = tmp_path / "notgit"
        plain_dir.mkdir()
        env = _make_env(tmp_path)
        r = _run_init(plain_dir, env)
        assert r.returncode == 4, f"expected exit 4, got {r.returncode}"
        assert "remedy init requires a git repository" in r.stderr
        contents = os.listdir(str(plain_dir))
        assert contents == [], f"non-git dir should be untouched, found: {contents}"

    def test_project_name_flag(self, tmp_path):
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r = _run_init(repo, env, ["--project-name", "my-custom-name"])
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

    def test_subdirectory_targets_repo_root(self, tmp_path):
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        subdir = repo / "deep" / "nested"
        subdir.mkdir(parents=True)
        r = _run_init(subdir, env)
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

        r2 = _run_init(repo, env)
        assert r2.returncode == 0
        assert "[exists] project " in r2.stdout


# ---------------------------------------------------------------------------
# T002: Config template + Runtime detection
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestInitConfig:

    def test_no_marker_repo_skips_runtime(self, tmp_path):
        """No framework markers → [runtime] commented out + skip line."""
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r = _run_init(repo, env)
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] config remedy.toml" in r.stdout
        assert "[skipped] skipped runtime autodetect" in r.stdout

        cfg = (repo / "remedy.toml").read_text(encoding="utf-8")
        assert "[remedy]" in cfg
        assert "# [runtime]" in cfg
        assert "\n[runtime]\n" not in cfg

    def test_vite_marker_fills_runtime(self, tmp_path):
        """Vite in package.json → [runtime] filled with detected cmd/port."""
        repo = _make_git_repo(tmp_path / "repo")
        (repo / "package.json").write_text(
            json.dumps({"devDependencies": {"vite": "^5"}, "scripts": {"dev": "vite"}}),
            encoding="utf-8",
        )
        env = _make_env(tmp_path)
        r = _run_init(repo, env)
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] config remedy.toml" in r.stdout
        assert "[skipped]" not in r.stdout

        cfg = (repo / "remedy.toml").read_text(encoding="utf-8")
        assert "[runtime]\n" in cfg
        assert "# [runtime]" not in cfg
        assert "5173" in cfg

    def test_uvicorn_marker_fills_runtime(self, tmp_path):
        """uvicorn in requirements + app/main.py → [runtime] filled."""
        repo = _make_git_repo(tmp_path / "repo")
        (repo / "requirements.txt").write_text("uvicorn\nfastapi\n", encoding="utf-8")
        app_dir = repo / "app"
        app_dir.mkdir()
        (app_dir / "main.py").write_text("app = None\n", encoding="utf-8")
        env = _make_env(tmp_path)
        r = _run_init(repo, env)
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] config remedy.toml" in r.stdout
        assert "[skipped]" not in r.stdout

        cfg = (repo / "remedy.toml").read_text(encoding="utf-8")
        assert "[runtime]\n" in cfg
        assert "uvicorn" in cfg
        assert "8000" in cfg

    def test_existing_config_untouched(self, tmp_path):
        """Handwritten remedy.toml is never overwritten."""
        repo = _make_git_repo(tmp_path / "repo")
        cfg_path = repo / "remedy.toml"
        handwritten = "# my custom config\n[remedy]\ndata_dir = \"/tmp/custom\"\n"
        cfg_path.write_text(handwritten, encoding="utf-8")
        hash_before = _sha256(cfg_path)

        env = _make_env(tmp_path)
        r = _run_init(repo, env)
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[exists] config remedy.toml" in r.stdout
        assert "[created] project " in r.stdout

        hash_after = _sha256(cfg_path)
        assert hash_before == hash_after, "existing remedy.toml was modified"

    def test_config_parses_through_loader(self, tmp_path):
        """Generated remedy.toml is valid for config.load_config."""
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r = _run_init(repo, env)
        assert r.returncode == 0, f"stderr: {r.stderr}"

        from packages.orchestration.config import load_config
        cfg = load_config(project_path=repo / "remedy.toml")
        assert cfg.load_report.project_loaded

    def test_config_written_before_registry(self, tmp_path):
        """Config file exists even if registry would fail — verified by
        checking both are created in a single run."""
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r = _run_init(repo, env)
        assert r.returncode == 0, f"stderr: {r.stderr}"
        lines = r.stdout.strip().splitlines()
        config_idx = next(i for i, l in enumerate(lines) if "config" in l)
        project_idx = next(i for i, l in enumerate(lines) if "project" in l)
        assert config_idx < project_idx, (
            f"config should be reported before project: {lines}"
        )
