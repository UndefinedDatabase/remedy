"""F027 R2 — the linear runner's fold of a veto (DECISION F027 D2).

The fold before the task loop and at every pre-task safe point, the vetoed attempt's
workspace restored to its start tree, the unreachable set never dispatched, the tasks a
block skipped going back to pending unless unreachable, the terminal that names both the
vetoed and the unreachable sets, and `vetoed` in the run manifest's vocabulary.

Planned jobs are built as ``tests/orchestration/test_task_edit_runtime.py``'s own
``_save_job`` builds them (an approved plan, a plain directory as the repository for a
copy job); vetoes are recorded through ``task_veto.veto_task_command`` against the control
root ``safe_points.control_root()`` resolves under ``REMEDY_DATA_DIR``; runs go through the
real ``run_job`` with ``pingpong_provider.FakeProvider`` or a small custom fake.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import pingpong_job as pj
from packages.orchestration import safe_points
from packages.orchestration import task_veto as tv
from packages.orchestration import worktrees as W
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PAUSED,
    job_evidence_dir,
    load_job_plan,
    parse_job_file,
    run_job,
    save_job_plan,
)
from packages.orchestration.pingpong_provider import BuilderOutput, FakeProvider, ReviewerOutput
from packages.orchestration.run_manifest import (
    MODE_PUBLISHED_REFERENCE,
    load_episode_manifest_verified,
    validate_run_manifest,
)
from tests.orchestration.test_task_edit_runtime import _by_planned, _save_job, _task, _task_id_of


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
    return data


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A plain (non-git) directory: the copy-mode job's target."""
    r = tmp_path / "repo"
    r.mkdir()
    (r / "docs").mkdir()
    (r / "docs" / "README.md").write_text("# Docs\n")
    return r


def _control():
    return safe_points.control_root()


def _pass_provider() -> FakeProvider:
    return FakeProvider(pass_on_round=1, fail_on_round=99)


def _veto_filename(task_id: str) -> str:
    """Mirrors ``task_veto._veto_filename`` exactly — the veto file is named by a digest
    of the task id, never by the id itself."""
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:32]
    return f"{digest}.json"


class _RefusingProvider:
    """A provider that must never be called: `build`/`review` fail the test outright."""

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return False

    def build(self, prompt, **kw):
        raise AssertionError("the builder must not run: nothing should be dispatched")

    def review(self, prompt, **kw):
        raise AssertionError("the reviewer must not run: nothing should be dispatched")


class _AlwaysBlockedProvider:
    """Builds once, then the reviewer answers `blocked` — a deterministic first-round
    completion-gate failure, mirroring `test_job_worktree_integration.py`'s `_Blocking`."""

    def __init__(self, files=("docs/README.md",)):
        self._files = list(files)
        self.build_calls = 0

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return False

    def build(self, prompt, **kw):
        self.build_calls += 1
        return BuilderOutput(summary="attempt", files_changed=list(self._files),
                             provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="blocked", confidence="high", summary="no",
                              provider="fake")


# ---------------------------------------------------------------------------
# The diamond: B vetoed before the run
# ---------------------------------------------------------------------------


class TestDiamondVetoBeforeTheRun:
    def test_b_vetoed_before_the_run(self, root, repo):
        tasks = [_task("A", []), _task("B", ["A"]), _task("C", ["A"]), _task("D", ["B", "C"])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        job = load_job_plan(job_id, root)
        b_id = _task_id_of(root, job_id, "B")
        d_id = _task_id_of(root, job_id, "D")

        veto = tv.veto_task_command(job, task_id=b_id, reason="known-bad approach for B",
                                    actor="alice", control_root_path=_control())
        assert veto["outcome"] == "vetoed"
        assert veto["unreachable"] == [d_id]

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_BLOCKED
        a = _by_planned(done, "A")[1]
        b = _by_planned(done, "B")[1]
        c = _by_planned(done, "C")[1]
        d = _by_planned(done, "D")[1]
        assert a.status == pj.TASK_APPLIED
        assert c.status == pj.TASK_APPLIED
        assert b.status == pj.TASK_VETOED
        assert d.status == pj.TASK_SKIPPED
        assert not b.run_id
        assert not d.run_id
        assert done.error == f"all_remaining_work_vetoed: vetoed {b_id}; unreachable {d_id}"
        assert done.metadata["veto_terminal"] == {"vetoed": [b_id], "unreachable": [d_id]}

        entry = done.metadata["task_vetoes"][b_id]
        assert entry["reason"] == "known-bad approach for B"
        assert entry["unreachable_task_ids"] == [d_id]
        assert entry["restored"] is False


# ---------------------------------------------------------------------------
# Every task vetoed
# ---------------------------------------------------------------------------


class TestEveryTaskVetoed:
    def test_nothing_is_dispatched_and_the_error_names_them_all(self, root, repo):
        tasks = [_task("A", []), _task("B", ["A"])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        job = load_job_plan(job_id, root)
        a_id = _task_id_of(root, job_id, "A")
        b_id = _task_id_of(root, job_id, "B")
        for tid in (a_id, b_id):
            result = tv.veto_task_command(job, task_id=tid, reason="stop everything",
                                          actor="alice", control_root_path=_control())
            assert result["outcome"] == "vetoed"

        done = run_job(job_id, builder_provider=_RefusingProvider(),
                       reviewer_provider=_RefusingProvider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_BLOCKED
        assert done.error == f"all_remaining_work_vetoed: vetoed {a_id}, {b_id}; unreachable none"
        a = _by_planned(done, "A")[1]
        b = _by_planned(done, "B")[1]
        assert a.status == pj.TASK_VETOED and not a.run_id
        assert b.status == pj.TASK_VETOED and not b.run_id


# ---------------------------------------------------------------------------
# A job file's tasks without plan metadata (the legacy-linear rule)
# ---------------------------------------------------------------------------

_THREE_TASK_LEGACY_JOB = """# Legacy job

## Task 1
First task.

## Task 2
Second task.

## Task 3
Third task.
"""


class TestLegacyJobFileVeto:
    def test_the_second_of_three_vetoed(self, root, repo):
        job = parse_job_file(_THREE_TASK_LEGACY_JOB, str(repo))
        job_id = job.job_id
        t2_id = job.tasks[1].task_id

        result = tv.veto_task_command(job, task_id=t2_id, reason="skip this approach",
                                      actor="alice", control_root_path=_control())
        assert result["outcome"] == "vetoed"

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert done.tasks[0].status == pj.TASK_APPLIED
        assert done.tasks[1].status == pj.TASK_VETOED
        assert done.tasks[2].status == pj.TASK_SKIPPED
        assert done.state == JOB_BLOCKED


# ---------------------------------------------------------------------------
# A veto recorded DURING the run
# ---------------------------------------------------------------------------


class _VetoingBuilder:
    """Vetoes ``c_task_id`` the first time it is asked to build — i.e. while A runs."""

    def __init__(self, job_id: str, c_task_id: str):
        self._job_id = job_id
        self._c_task_id = c_task_id
        self.build_calls = 0

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return False

    def build(self, prompt, **kw):
        self.build_calls += 1
        if self.build_calls == 1:
            job = load_job_plan(self._job_id)
            result = tv.veto_task_command(
                job, task_id=self._c_task_id, reason="stop C while A runs", actor="ci",
                control_root_path=_control())
            assert result["outcome"] == "vetoed"
        return BuilderOutput(summary="ok", files_changed=["docs/README.md"], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


class TestVetoDuringTheRun:
    def test_a_veto_recorded_while_the_prior_task_runs_stops_the_next_one(self, root, repo):
        tasks = [_task("A", []), _task("C", [])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        c_id = _task_id_of(root, job_id, "C")
        builder = _VetoingBuilder(job_id, c_id)

        done = run_job(job_id, builder_provider=builder, reviewer_provider=builder,
                       max_rounds=1, repair_rounds=0)

        a = _by_planned(done, "A")[1]
        c = _by_planned(done, "C")[1]
        assert a.status == pj.TASK_APPLIED
        assert c.status == pj.TASK_VETOED
        assert not c.run_id
        assert builder.build_calls == 1                # C's build was never reached
        assert done.state == JOB_BLOCKED


