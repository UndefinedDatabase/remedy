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

import json
import re
from pathlib import Path
from uuid import uuid4

import pytest


@pytest.fixture(autouse=True)
def _hermetic_config_cache():
    """Isolate these tests from the process-global config cache.

    ``resolve_data_root()`` falls back to ``get_config().get("data_dir")``,
    and ``get_config()`` caches a ``RemedyConfig`` built from the
    cwd-relative ``remedy.toml`` (``_DEFAULT_PROJECT_PATH``). Any earlier
    test in the same xdist worker that chdir'd into a temp directory
    holding a ``remedy.toml`` leaves that ``data_dir`` in the cache, so the
    default-root assertions here saw another test's value and failed
    depending on execution order. Reset on both sides so this module never
    inherits — and never exports — a poisoned cache.
    """
    from packages.orchestration.config import reset_config
    reset_config()
    yield
    reset_config()


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


class TestResolveJobId:
    """Test the central short-ID resolver."""

    def _make_job_file(self, jobs_path: Path, job_id: str) -> None:
        jobs_path.mkdir(parents=True, exist_ok=True)
        (jobs_path / f"{job_id}.json").write_text(json.dumps({"id": job_id}))

    def test_full_uuid_returns_uuid(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import resolve_job_id
        uid = uuid4()
        self._make_job_file(tmp_path / "jobs", str(uid))
        assert resolve_job_id(str(uid)) == uid

    def test_short_prefix_resolves(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import resolve_job_id
        uid = uuid4()
        self._make_job_file(tmp_path / "jobs", str(uid))
        short = str(uid)[:8]
        assert resolve_job_id(short) == uid

    def test_ambiguous_prefix_exits_2(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import resolve_job_id
        uid1 = "aaaa1111-0000-0000-0000-000000000001"
        uid2 = "aaaa1111-0000-0000-0000-000000000002"
        self._make_job_file(tmp_path / "jobs", uid1)
        self._make_job_file(tmp_path / "jobs", uid2)
        import pytest
        with pytest.raises(SystemExit) as exc_info:
            resolve_job_id("aaaa1111")
        assert exc_info.value.code == 2

    def test_no_match_exits_1(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import resolve_job_id
        (tmp_path / "jobs").mkdir(parents=True)
        import pytest
        with pytest.raises(SystemExit) as exc_info:
            resolve_job_id("deadbeef")
        assert exc_info.value.code == 1

    def test_invalid_string_exits_1(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import pytest

        from packages.orchestration.data_paths import resolve_job_id
        with pytest.raises(SystemExit) as exc_info:
            resolve_job_id("not-a-hex")
        assert exc_info.value.code == 1

    def test_full_uuid_works_without_job_file(self, monkeypatch, tmp_path):
        """Full UUID parses even if no job file exists (load_job handles NotFound)."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import resolve_job_id
        uid = uuid4()
        result = resolve_job_id(str(uid))
        assert result == uid


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


class TestMintIds:
    """DECISION F260 D2: one 16-hex id shape, one minting function per KIND of id.

    Every test here CALLS the shipped function. Re-implementing ``uuid4().hex[:16]``
    in the test would pin the test's own copy of the rule and nothing else.
    """

    def _minters(self) -> list:
        from packages.orchestration.data_paths import mint_episode_id, mint_job_id, mint_run_id
        return [mint_job_id, mint_run_id, mint_episode_id]

    def test_each_mints_sixteen_lowercase_hex_chars(self):
        for mint in self._minters():
            value = mint()
            assert isinstance(value, str), f"{mint.__name__} returned {value!r}"
            assert len(value) == 16, f"{mint.__name__} returned {value!r} of length {len(value)}"
            assert set(value) <= set("0123456789abcdef"), f"{mint.__name__} returned {value!r}"

    def test_successive_calls_differ(self):
        """The id is MINTED, not a constant the module computed once at import."""
        for mint in self._minters():
            assert mint() != mint(), f"{mint.__name__} returns the same id twice"

    def test_the_three_names_are_three_distinct_functions(self):
        """D2's "one shape is not one function" clause: an alias fails right here."""
        from packages.orchestration.data_paths import mint_episode_id, mint_job_id, mint_run_id
        assert mint_job_id is not mint_run_id
        assert mint_job_id is not mint_episode_id
        assert mint_run_id is not mint_episode_id

    def test_minted_ids_match_the_short_hex_pattern(self):
        """What lets the existing prefix resolvers accept a minted id at all."""
        from packages.orchestration import data_paths
        for mint in self._minters():
            value = mint()
            assert data_paths._SHORT_HEX_RE.fullmatch(value) is not None, \
                f"{mint.__name__} minted {value!r}, which _SHORT_HEX_RE rejects"

    def test_a_minted_job_id_is_not_a_uuid(self):
        """Round 2's inventory recorded this as why ``resolve_job_id`` cannot resolve a
        ping-pong job id. Pinned so a later round cannot quietly widen the shape back
        into a UUID without this test saying what that breaks.
        """
        from uuid import UUID

        from packages.orchestration.data_paths import mint_job_id
        with pytest.raises(ValueError):
            UUID(mint_job_id())
