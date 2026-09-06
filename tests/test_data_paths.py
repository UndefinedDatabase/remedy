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


# DECISION F260 D1: the set of modules that OWN part of a job's evidence
# directory and have been migrated onto ``data_paths.job_evidence_dir``. The set
# is defined SEMANTICALLY — membership is "F260 moved this module's hand-built
# ``jobs_dir() / <id> / 'evidence'`` onto the one spelling" — so a later reader
# knows what earns a place here rather than guessing from the list.
#
# ``packages/orchestration/checkpoints.py`` and ``packages/orchestration/
# storage.py`` are DELIBERATELY EXCLUDED and correctly keep their ``jobs_dir``
# calls. They name the CLASSIC job store, ``<data_root>/jobs/<uuid>.json``,
# which is one FILE per job and a different concept from a job's evidence
# DIRECTORY; that store is deleted in F260 T004, not here. The reason is written
# down because an exclusion a later reader cannot justify is one a later reader
# deletes — or, worse, "fixes" by migrating the classic store onto an evidence
# path it was never meant to share.
_JOB_EVIDENCE_OWNING_MODULES = (
    "packages.orchestration.pingpong_job",
    "packages.orchestration.job_evidence",
    "packages.orchestration.repair_attest",
    "apps.cli.commands.do_cmd",
)


class TestJobAndRunLayout:
    """DECISION F260 D1: ONE root per job, and ONE spelling of that layout.

    The record lives at ``<root>/jobs/<job_id>/job.json``, that job's evidence at
    ``<root>/jobs/<job_id>/evidence/``, and a run's log under
    ``<root>/runs/<run_id>/`` — keyed by RUN id, not by job id. These tests read
    the SHIPPED functions; the layout is never re-spelled here, because a test
    that rebuilds the path by hand pins its own copy of the rule and nothing else.
    """

    def _layout(self):
        from packages.orchestration.data_paths import (
            job_dir,
            job_evidence_dir,
            job_record_path,
            run_dir,
        )
        return job_dir, job_record_path, job_evidence_dir, run_dir

    def test_the_record_and_the_evidence_share_one_root(self, monkeypatch, tmp_path):
        """D1's whole point: a job's record and its evidence hang off ONE directory."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job_dir, job_record_path, job_evidence_dir, _ = self._layout()
        jid = "0123456789abcdef"
        assert job_record_path(jid).parent == job_dir(jid)
        assert job_evidence_dir(jid).parent == job_dir(jid)
        assert job_record_path(jid).parent == job_evidence_dir(jid).parent

    def test_job_dir_is_jobs_dir_keyed_by_the_job_id(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import jobs_dir
        job_dir, _, _, _ = self._layout()
        jid = "0123456789abcdef"
        assert job_dir(jid) == jobs_dir() / jid

    def test_the_record_is_named_job_json(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        _, job_record_path, _, _ = self._layout()
        assert job_record_path("0123456789abcdef").name == "job.json"

    def test_a_run_hangs_under_runs_dir_and_never_under_jobs_dir(self, monkeypatch, tmp_path):
        """The copy-paste this layout invites is keying a RUN under ``jobs/``.

        D1 changes what ``<data_root>/runs/`` is keyed by — run id, not job id —
        and a run filed under ``jobs/`` is unreadable by every run-log reader.
        """
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import jobs_dir, runs_dir
        _, _, _, run_dir = self._layout()
        rid = "fedcba9876543210"
        assert run_dir(rid) == runs_dir() / rid
        assert run_dir(rid).parent == runs_dir()
        assert jobs_dir() not in run_dir(rid).parents

    def test_the_root_override_is_honoured_by_all_four(self, monkeypatch, tmp_path):
        """Each function takes ``root`` exactly as ``jobs_dir`` and ``runs_dir`` do.

        Set the env root to a DIFFERENT directory, so a function that quietly
        ignores its ``root`` argument returns the env path and is caught here
        rather than passing by coincidence.
        """
        env_root = tmp_path / "env"
        arg_root = tmp_path / "arg"
        monkeypatch.setenv("REMEDY_DATA_DIR", str(env_root))
        job_dir, job_record_path, job_evidence_dir, run_dir = self._layout()
        jid = "0123456789abcdef"
        rid = "fedcba9876543210"
        assert job_dir(jid, arg_root) == arg_root / "jobs" / jid
        assert job_record_path(jid, arg_root) == arg_root / "jobs" / jid / "job.json"
        assert job_evidence_dir(jid, arg_root) == arg_root / "jobs" / jid / "evidence"
        assert run_dir(rid, arg_root) == arg_root / "runs" / rid
        for p in (job_dir(jid, arg_root), job_record_path(jid, arg_root),
                  job_evidence_dir(jid, arg_root), run_dir(rid, arg_root)):
            assert env_root not in p.parents, f"{p} ignored its root argument"

    def test_pingpong_job_evidence_paths_equal_the_data_paths_ones(self, monkeypatch, tmp_path):
        """No behaviour change: both call sites return exactly what they returned before."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration import data_paths, pingpong_job
        jid = "0123456789abcdef"
        assert pingpong_job.job_evidence_dir(jid) == data_paths.job_evidence_dir(jid)
        assert pingpong_job._task_stream_dir(jid, "t1") == \
            data_paths.job_evidence_dir(jid) / "task_runs" / "t1"

    def _jobs_dir_references(self, module):
        """Every AST reference in ``module`` resolving to exactly ``jobs_dir``.

        Read via ``ast`` rather than as a substring, so a comment or a docstring
        naming the old layout cannot trip the guard and an ``import ... as``
        alias cannot dodge it. ``_jobs_dir`` and ``task_jobs_dir`` are DIFFERENT
        names that merely contain the same substring; matching on the resolved
        name is exactly what keeps them correctly invisible here.
        """
        import ast

        tree = ast.parse(Path(module.__file__).read_text())
        return [
            node for node in ast.walk(tree)
            if (isinstance(node, ast.Name) and node.id == "jobs_dir")
            or (isinstance(node, ast.Attribute) and node.attr == "jobs_dir")
            or (isinstance(node, ast.alias)
                and (node.asname or node.name) == "jobs_dir")
        ]

    @pytest.mark.parametrize("modname", _JOB_EVIDENCE_OWNING_MODULES)
    def test_no_module_that_owns_job_evidence_spells_the_path_itself(self, modname):
        """The VALUE readings above cannot see a regression to the hand-built path.

        ``jobs_dir() / job_id / "evidence"`` is EQUAL to what ``data_paths`` now
        returns, so an equality test stays green while the second spelling comes
        back. Only reading the module itself sees it, which is why BOTH readings
        ship rather than either one alone.

        ``checkpoints.py`` and ``storage.py`` are not in this set on purpose:
        they name the CLASSIC store ``<data_root>/jobs/<uuid>.json``, a file per
        job rather than a job's evidence directory, and F260 T004 deletes it.
        """
        import importlib

        module = importlib.import_module(modname)
        hits = self._jobs_dir_references(module)
        assert hits == [], (
            f"{modname} references data_paths.jobs_dir at lines "
            f"{[getattr(n, 'lineno', '?') for n in hits]}; DECISION F260 D1 puts "
            "the job evidence layout in data_paths and nowhere else"
        )

    def test_the_job_evidence_owning_module_set_is_real(self):
        """Non-vacuity: a guard over an empty set would pass while measuring nothing.

        The absence assertion above is only as strong as the set it ranges over,
        so the set is checked to be non-empty, free of duplicates, and made
        entirely of modules that actually import and have a readable source file.
        """
        import importlib

        assert _JOB_EVIDENCE_OWNING_MODULES, (
            "the evidence-owning module set is EMPTY; the absence guard above "
            "would then range over nothing and pass without reading any module"
        )
        assert len(set(_JOB_EVIDENCE_OWNING_MODULES)) == \
            len(_JOB_EVIDENCE_OWNING_MODULES), "duplicate module in the set"
        for modname in _JOB_EVIDENCE_OWNING_MODULES:
            module = importlib.import_module(modname)
            assert Path(module.__file__).is_file(), f"{modname} has no source file"

    def test_the_classic_store_modules_still_call_jobs_dir(self):
        """The excluded pair must keep naming the classic store, not lose it quietly.

        This is the other half of the non-vacuity reading: if ``jobs_dir`` had
        simply been deleted everywhere, the absence guard above would pass for
        the wrong reason. ``checkpoints.py`` and ``storage.py`` are the modules
        that legitimately still call it, until F260 T004 deletes that store.
        """
        from packages.orchestration import checkpoints, storage

        for module in (checkpoints, storage):
            hits = self._jobs_dir_references(module)
            assert hits, (
                f"{module.__name__} no longer references jobs_dir; the classic "
                "store is still live until F260 T004 deletes it, so this is "
                "either a real regression or a sign this guard now measures "
                "nothing"
            )
