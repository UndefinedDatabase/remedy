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

# The modules that reached the live ping-pong store through
# ``pingpong_job._jobs_dir`` until F260 T002 DELETED that helper. They now spell
# it as ``data_paths.job_dir`` / ``job_record_path`` and nothing else.
# ``packages.orchestration.storage`` is NOT in this set and must never be added:
# its ``_resolve_jobs_dir`` is a different symbol naming the CLASSIC store that
# F260 T004 deletes, and it merely shares a substring with the deleted name.
_MIGRATED_OFF_JOBS_DIR_MODULES = (
    "packages.orchestration.pingpong_job",
    "packages.orchestration.job_evidence",
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

    def test_a_persisted_pingpong_job_writes_its_record_under_its_own_job_dir(
        self, monkeypatch, tmp_path,
    ):
        """F260 T002: the WRITER, not only the accessor, files the record under ``jobs/``.

        Every reading above proves ``job_record_path`` SPELLS the D1 layout. This
        one runs the SHIPPED writer and reads the bytes it left, which is the
        remaining fix condition of finding R-0814: a job's record and that job's
        evidence share ONE root. Until T002 ``_persist_job`` wrote to
        ``<data_root>/task_jobs/<16hex>/job.json`` while every equality test here
        stayed green, because an accessor nobody calls is a spelling and not a
        layout.
        """
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration import data_paths, pingpong_job

        job = pingpong_job.JobPlan()
        written = pingpong_job.save_job_plan(job)

        assert written == data_paths.job_record_path(job.job_id)
        assert written.is_file(), f"the writer returned {written} but wrote nothing there"
        assert json.loads(written.read_text())["job_id"] == job.job_id
        assert pingpong_job.job_evidence_dir(job.job_id).parent == \
            data_paths.job_dir(job.job_id)
        assert written.parent == pingpong_job.job_evidence_dir(job.job_id).parent, (
            "the record and the evidence no longer share one root"
        )
        assert "task_jobs" not in written.parts, (
            f"the record is still filed under a task_jobs component: {written}"
        )

    def test_a_pingpong_record_in_the_jobs_dir_is_still_resolvable_beside_a_classic_one(
        self, monkeypatch, tmp_path,
    ):
        """Both stores share ``jobs/`` now, and neither shadows the other.

        This is why the T002 move is ONE commit: the writer moved and its reader
        moved with it. ``_classic_job_id_matches`` globs ``*.json`` and cannot
        see a directory; ``_task_job_id_matches`` reads directories holding a
        ``job.json`` and cannot see a classic file. So one directory carrying
        both shapes yields exactly one match per id and never a false ambiguity —
        and a directory without a ``job.json`` is not a job at all.
        """
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import jobs_dir, resolve_any_job_id

        classic_id = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
        pingpong_id = "0123456789abcdef"
        bare_id = "fedcba9876543210"

        jobs_dir().mkdir(parents=True)
        (jobs_dir() / f"{classic_id}.json").write_text(
            json.dumps({"job_id": classic_id}), encoding="utf-8")
        (jobs_dir() / pingpong_id).mkdir()
        (jobs_dir() / pingpong_id / "job.json").write_text(
            json.dumps({"job_id": pingpong_id}), encoding="utf-8")
        (jobs_dir() / bare_id).mkdir()

        assert resolve_any_job_id(pingpong_id) == pingpong_id
        assert resolve_any_job_id(pingpong_id[:8]) == pingpong_id
        assert resolve_any_job_id(classic_id) == classic_id
        assert resolve_any_job_id(classic_id[:8]) == classic_id

        with pytest.raises(SystemExit) as exc:
            resolve_any_job_id(bare_id)
        assert exc.value.code == 1, (
            f"a directory with no job.json resolved to something (exit {exc.value.code})"
        )

    def _references_to(self, module, name):
        """Every AST reference in ``module`` resolving to exactly ``name``.

        Read via ``ast`` rather than as a substring, so a comment or a docstring
        naming the old layout cannot trip the guard and an ``import ... as``
        alias cannot dodge it. ``jobs_dir``, ``_jobs_dir`` and
        ``_resolve_jobs_dir`` are THREE DIFFERENT names that merely share a
        substring; matching on the resolved name is exactly what keeps each of
        them correctly invisible to a reading aimed at another.
        """
        import ast

        tree = ast.parse(Path(module.__file__).read_text())
        return [
            node for node in ast.walk(tree)
            if (isinstance(node, ast.Name) and node.id == name)
            or (isinstance(node, ast.Attribute) and node.attr == name)
            or (isinstance(node, ast.alias)
                and (node.asname or node.name) == name)
        ]

    def _jobs_dir_references(self, module):
        """Every AST reference in ``module`` resolving to exactly ``jobs_dir``."""
        return self._references_to(module, "jobs_dir")

    def _names_of(self, module, name):
        """Every AST node in ``module`` that NAMES ``name`` — reference OR definition.

        ``_references_to`` above reads USES, and a use is all the round-7 guard
        needed: ``jobs_dir`` is defined in ``data_paths`` and the modules it
        ranges over can only ever call it. A DELETED helper is different. A bare
        ``def _jobs_dir(): ...`` that nothing calls yet is exactly how a deleted
        helper comes back — and it is invisible to a reference reading, because
        a ``FunctionDef`` is not a ``Name``. Measured: reviving the helper as an
        uncalled ``def`` leaves the reference reading GREEN and is caught only
        by the ``hasattr`` test. So this reading adds the binding forms, and the
        two guards below fail for genuinely different reasons.
        """
        import ast

        tree = ast.parse(Path(module.__file__).read_text())
        bindings = [
            node for node in ast.walk(tree)
            if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and node.name == name)
        ]
        return self._references_to(module, name) + bindings

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

    def test_pingpong_job_has_no_jobs_dir_attribute_at_all(self):
        """``pingpong_job._jobs_dir`` is GONE, not merely unused.

        Read by ``hasattr`` on the IMPORTED module rather than from its text, so
        a helper reintroduced by any route — a def, an assignment, a re-export —
        is caught. The AST guard below reads the source instead; the two fail
        for different reasons and both ship.
        """
        from packages.orchestration import pingpong_job

        assert not hasattr(pingpong_job, "_jobs_dir"), (
            "pingpong_job._jobs_dir is back; F260 T002 deleted it so the live "
            "ping-pong store has ONE spelling, data_paths.job_dir"
        )
        assert hasattr(pingpong_job, "_persist_job"), (
            "hasattr found nothing at all on pingpong_job; the absence above "
            "would then be measuring an import failure, not a deleted helper"
        )

    @pytest.mark.parametrize("modname", _MIGRATED_OFF_JOBS_DIR_MODULES)
    def test_no_migrated_module_names_the_deleted_jobs_dir_helper(self, modname):
        """The VALUE readings above cannot see the deleted spelling come back.

        ``_jobs_dir() / job_id`` was EQUAL to what ``job_dir`` returns, so
        an equality test stays green while the second spelling returns. Only
        reading the module itself sees it.

        ``storage.py`` is out of scope on purpose: its ``_resolve_jobs_dir`` is
        a DIFFERENT symbol that merely contains the same substring, and it names
        the CLASSIC store ``<data_root>/jobs/<uuid>.json`` that F260 T004
        deletes. It is not a survivor of this migration and never referenced the
        deleted helper.
        """
        import importlib

        module = importlib.import_module(modname)
        hits = self._names_of(module, "_jobs_dir")
        assert hits == [], (
            f"{modname} names _jobs_dir at lines "
            f"{[getattr(n, 'lineno', '?') for n in hits]}; F260 T002 deleted "
            "that helper and data_paths.job_dir replaced it"
        )

    def test_the_deleted_name_guard_is_not_vacuous(self):
        """Non-vacuity, in both directions the absence guard above can be empty in.

        The set could be empty, and the AST reading could be structurally unable
        to see an underscore-prefixed private helper — in which case the guard
        would pass while measuring nothing. ``storage._resolve_jobs_dir`` is the
        control: a private, underscore-prefixed, module-local helper of exactly
        the shape ``_jobs_dir`` had, defined AND called in the same file, which
        the same reading DOES find.

        The last assertion is the one that matters most. A helper comes back as
        an uncalled ``def`` before it comes back as a call, so the reading must
        see a DEFINITION and not only a use. If ``_names_of`` ever collapses
        back to ``_references_to``, the guard above stops catching the revival
        it exists for, and this is where that shows up.
        """
        import importlib

        from packages.orchestration import storage

        assert _MIGRATED_OFF_JOBS_DIR_MODULES, (
            "the migrated module set is EMPTY; the absence guard above would "
            "then range over nothing and pass without reading any module"
        )
        assert len(set(_MIGRATED_OFF_JOBS_DIR_MODULES)) == \
            len(_MIGRATED_OFF_JOBS_DIR_MODULES), "duplicate module in the set"
        for modname in _MIGRATED_OFF_JOBS_DIR_MODULES:
            module = importlib.import_module(modname)
            assert Path(module.__file__).is_file(), f"{modname} has no source file"
        assert self._names_of(storage, "_resolve_jobs_dir"), (
            "the AST reading cannot find storage._resolve_jobs_dir, a private "
            "helper of exactly the shape _jobs_dir had; the absence assertions "
            "above are therefore measuring nothing"
        )
        assert self._names_of(storage, "_jobs_dir") == [], (
            "storage.py names _jobs_dir; it never did, so either the reading "
            "now matches on a substring or storage.py grew a dependency on a "
            "helper that no longer exists"
        )
        assert len(self._names_of(storage, "_resolve_jobs_dir")) > \
            len(self._references_to(storage, "_resolve_jobs_dir")), (
            "_names_of found no more than _references_to did, so its DEFINITION "
            "arm is dead; a helper revived as an uncalled def would then slip "
            "past the absence guard above"
        )
