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
import json
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


def _events(root: Path, job_id: str, event: str) -> list[dict]:
    """Mirrors `test_job_stop_integration._events`: every ledger event of this
    name for this job, across every run-log file `RunLogWriter` produced."""
    runs = root / "job_logs" / job_id
    out: list[dict] = []
    for f in sorted(runs.glob("*.jsonl")) if runs.is_dir() else []:
        for line in f.read_text().splitlines():
            if line.strip():
                raw = json.loads(line)
                if raw.get("event") == event:
                    out.append(raw)
    return out


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


# ---------------------------------------------------------------------------
# A block, a veto and a relaunch: the skipped set unwinds except what stays unreachable
# ---------------------------------------------------------------------------


class TestBlockThenVetoThenRelaunch:
    def test_the_independent_task_returns_to_pending_and_runs(self, root, repo):
        tasks = [_task("A", []), _task("D", ["A"]), _task("E", [])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        a_id = _task_id_of(root, job_id, "A")

        failing = _AlwaysBlockedProvider()
        blocked = run_job(job_id, builder_provider=failing, reviewer_provider=failing,
                          max_rounds=1, repair_rounds=0)
        assert blocked.state == JOB_BLOCKED
        a0 = _by_planned(blocked, "A")[1]
        d0 = _by_planned(blocked, "D")[1]
        e0 = _by_planned(blocked, "E")[1]
        assert a0.status == pj.TASK_BLOCKED
        assert d0.status == pj.TASK_SKIPPED
        assert e0.status == pj.TASK_SKIPPED

        job = load_job_plan(job_id, root)
        veto = tv.veto_task_command(job, task_id=a_id, reason="A's approach was wrong",
                                    actor="alice", control_root_path=_control())
        assert veto["outcome"] == "vetoed"

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        a = _by_planned(done, "A")[1]
        d = _by_planned(done, "D")[1]
        e = _by_planned(done, "E")[1]
        assert a.status == pj.TASK_VETOED
        assert d.status == pj.TASK_SKIPPED           # A's dependent stays skipped: unreachable
        assert e.status == pj.TASK_APPLIED            # independent: back to pending, then ran
        assert e.run_id
        assert done.state == JOB_BLOCKED
        assert done.error.startswith("all_remaining_work_vetoed:")


class TestFoldSkipResetIsExact:
    """Direct coverage of ``_fold_task_vetoes``'s own skip-reset rule (D2 (2)): the
    runner's per-task unreachable filter (S4) would independently withhold D from
    dispatch even if the fold reset it too, so a scenario driven through the whole
    ``run_job`` loop cannot tell 'reset nothing' apart from 'reset everything' — this
    calls the fold directly and reads its immediate effect, before the loop ever runs.
    """

    def test_only_the_reachable_skipped_task_returns_to_pending(self, root, repo):
        tasks = [_task("A", []), _task("D", ["A"]), _task("E", [])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        a_id = _task_id_of(root, job_id, "A")

        job = load_job_plan(job_id, root)
        a = _by_planned(job, "A")[1]
        d = _by_planned(job, "D")[1]
        e = _by_planned(job, "E")[1]
        a.status = pj.TASK_BLOCKED
        d.status = pj.TASK_SKIPPED
        e.status = pj.TASK_SKIPPED
        save_job_plan(job, root)

        tv.record_task_veto(job_id, a_id, "A was wrong", "alice", pj.TASK_BLOCKED,
                            control_root_path=_control())

        reloaded = load_job_plan(job_id, root)
        blocked = pj._fold_task_vetoes(reloaded, None, _control())
        assert blocked is False

        a2 = _by_planned(reloaded, "A")[1]
        d2 = _by_planned(reloaded, "D")[1]
        e2 = _by_planned(reloaded, "E")[1]
        assert a2.status == pj.TASK_VETOED
        assert d2.status == pj.TASK_SKIPPED       # unreachable behind A's veto: stays skipped
        assert e2.status == pj.TASK_PENDING        # independent: goes back to pending


# ---------------------------------------------------------------------------
# The task cap parks after a veto folded; the paused manifest validates
# ---------------------------------------------------------------------------


_THREE_TASK_CAP_JOB = """# Task-cap job

## Task 1
First task.

## Task 2
Second task.

## Task 3
Third task.
"""


class TestTaskCapAfterAVeto:
    def test_the_paused_manifest_reads_the_vetoed_task_as_skipped(self, root, repo):
        # A legacy (markdown) job so `job_file_sha256` is real — a Task-Plan job never
        # carries one, which fails manifest validation for a reason unrelated to the veto.
        # T3 (the chain's tail) is vetoed before the run: nothing depends on it, so T2
        # stays reachable and pending when the cap parks the run one task in.
        job = parse_job_file(_THREE_TASK_CAP_JOB, str(repo))
        job_id = job.job_id
        t3_id = job.tasks[2].task_id

        veto = tv.veto_task_command(job, task_id=t3_id, reason="stop the tail task",
                                    actor="alice", control_root_path=_control())
        assert veto["outcome"] == "vetoed"

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0,
                       max_tasks=1)

        assert done.state == JOB_PAUSED
        t1, t2, t3 = done.tasks
        assert t1.status == pj.TASK_APPLIED
        assert t2.status == pj.TASK_PENDING
        assert t3.status == pj.TASK_VETOED

        ev = job_evidence_dir(done.job_id)
        manifest = load_episode_manifest_verified(
            ev, done.active_episode_id, expected_job_id=done.job_id)
        assert manifest.status == "paused"
        assert validate_run_manifest(manifest, mode=MODE_PUBLISHED_REFERENCE) == []
        te = next(t for t in manifest.call_expectation.tasks if t.task_id == t3_id)
        assert te.expectation == "skipped"
        assert te.task_status_at_finalization == "vetoed"


# ---------------------------------------------------------------------------
# An inert veto of an applied task
# ---------------------------------------------------------------------------


class TestInertVeto:
    def test_a_veto_of_an_already_applied_task_changes_nothing(self, root, repo):
        tasks = [_task("A", [])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        a_id = _task_id_of(root, job_id, "A")

        job = load_job_plan(job_id, root)
        a = _by_planned(job, "A")[1]
        a.status = pj.TASK_APPLIED
        save_job_plan(job, root)

        tv.record_task_veto(job_id, a_id, "too late now", "alice", pj.TASK_APPLIED,
                            control_root_path=_control())

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_COMPLETED
        a_done = _by_planned(done, "A")[1]
        assert a_done.status == pj.TASK_APPLIED
        entry = done.metadata["task_vetoes"][a_id]
        assert entry["inert"] == pj.TASK_APPLIED
        assert "folded_at" not in entry


# ---------------------------------------------------------------------------
# A corrupt veto file blocks the job
# ---------------------------------------------------------------------------


class TestCorruptVetoFile:
    def test_blocks_with_task_veto_control_error_and_dispatches_nothing(self, root, repo):
        tasks = [_task("A", [])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        a_id = _task_id_of(root, job_id, "A")

        vdir = _control() / "jobs" / job_id / "vetoed_tasks"
        vdir.mkdir(parents=True)
        (vdir / _veto_filename(a_id)).write_text("not json")

        done = run_job(job_id, builder_provider=_RefusingProvider(),
                       reviewer_provider=_RefusingProvider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_BLOCKED
        assert done.error.startswith("task_veto_control_error:")
        a = _by_planned(done, "A")[1]
        assert a.status == pj.TASK_PENDING
        assert not a.run_id


# ---------------------------------------------------------------------------
# A GIT job: the veto restores the workspace before the next task starts
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True,
                          check=True).stdout


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    r = tmp_path / "gitrepo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    (r / "base.txt").write_text("base\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


_ONE_TASK_JOB_TEXT = """# One task

## Task 1 — write partial work

Write partial.txt, then never pass review.
"""


class TestGitWorktreeVetoRestoresTheWorkspace:
    def test_a_veto_and_relaunch_removes_the_blocked_attempts_file(
            self, root, git_repo, monkeypatch):
        job = parse_job_file(_ONE_TASK_JOB_TEXT, str(git_repo))
        job_id = job.job_id

        holder: dict = {}
        real_create = W.create

        def spy(jid, r):
            h = real_create(jid, r)
            holder["path"] = h.path
            return h

        monkeypatch.setattr(W, "create", spy)

        class _WritesThenBlocks:
            @property
            def name(self) -> str:
                return "fake"

            @property
            def supports_resume(self) -> bool:
                return False

            def build(self, prompt, **kw):
                (Path(holder["path"]) / "partial.txt").write_text("work in progress\n")
                return BuilderOutput(summary="partial work", files_changed=["partial.txt"],
                                     provider="fake")

            def review(self, prompt, **kw):
                return ReviewerOutput(verdict="blocked", confidence="high", summary="no",
                                      provider="fake")

        prov = _WritesThenBlocks()
        blocked = run_job(job_id, builder_provider=prov, reviewer_provider=prov,
                          max_rounds=1, repair_rounds=0)
        assert blocked.state == JOB_BLOCKED
        t1 = blocked.tasks[0]
        assert t1.status == pj.TASK_BLOCKED
        ws = Path(holder["path"])
        assert (ws / "partial.txt").exists()

        veto = tv.veto_task_command(blocked, task_id=t1.task_id, reason="wrong approach",
                                    actor="alice", control_root_path=_control())
        assert veto["outcome"] == "vetoed"

        done = run_job(job_id, builder_provider=_RefusingProvider(),
                       reviewer_provider=_RefusingProvider(), max_rounds=1, repair_rounds=0)

        assert not (ws / "partial.txt").exists()
        assert done.state == JOB_BLOCKED
        assert done.error.startswith("all_remaining_work_vetoed:")


# ---------------------------------------------------------------------------
# F027 R3 — a veto of the IN-FLIGHT task (DECISION F027 D3 (1)-(2))
# ---------------------------------------------------------------------------


class _SelfVetoingBuilder:
    """During B's OWN build call — the second task this job dispatches — records a
    veto of B itself. The in-task safe point catches it at the NEXT safe point,
    which is before B's reviewer call, so B's build finishes but its review never
    runs (D3 (1): the call already running finishes; nothing is killed mid-call)."""

    def __init__(self, job_id: str, b_task_id: str):
        self._job_id = job_id
        self._b_task_id = b_task_id
        self.build_calls = 0
        self.review_calls = 0

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return False

    def build(self, prompt, **kw):
        self.build_calls += 1
        if self.build_calls == 2:                      # B's own first (only) build call
            job = load_job_plan(self._job_id)
            result = tv.veto_task_command(
                job, task_id=self._b_task_id, reason="stop B mid-flight", actor="ci",
                control_root_path=_control())
            assert result["outcome"] == "vetoed"
        return BuilderOutput(summary="ok", files_changed=["docs/README.md"], provider="fake")

    def review(self, prompt, **kw):
        self.review_calls += 1
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


class TestInFlightVetoOfTheRunningTask:
    def test_bs_build_finishes_its_review_never_runs_and_the_run_continues(
            self, root, repo):
        tasks = [_task("A", []), _task("B", ["A"]), _task("C", ["A"]), _task("D", ["B", "C"])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        b_id = _task_id_of(root, job_id, "B")
        d_id = _task_id_of(root, job_id, "D")
        builder = _SelfVetoingBuilder(job_id, b_id)

        done = run_job(job_id, builder_provider=builder, reviewer_provider=builder,
                       max_rounds=1, repair_rounds=0)

        assert done.state == JOB_BLOCKED
        a = _by_planned(done, "A")[1]
        b = _by_planned(done, "B")[1]
        c = _by_planned(done, "C")[1]
        d = _by_planned(done, "D")[1]
        assert a.status == pj.TASK_APPLIED
        assert c.status == pj.TASK_APPLIED
        assert b.status == pj.TASK_VETOED
        assert d.status == pj.TASK_SKIPPED
        assert b.run_id                              # D3 (2): the run fields are KEPT
        assert builder.build_calls == 3               # A, B, C — D is never dispatched
        assert builder.review_calls == 2               # A, C — B's reviewer never ran
        assert done.error == f"all_remaining_work_vetoed: vetoed {b_id}; unreachable {d_id}"

        failed = _events(root, job_id, "task_run_failed")
        b_failed = [e for e in failed if e.get("task_id") == b_id]
        assert len(b_failed) == 1
        assert b_failed[0]["outcome"] == "vetoed"
        assert _events(root, job_id, "job_stopped") == []


class _WritesThenSelfVetoes:
    """A GIT job's single-task builder: writes a file, then vetoes its OWN task
    while its own build call is still running."""

    def __init__(self, job_id: str, workspace: dict):
        self._job_id = job_id
        self._workspace = workspace
        self.build_calls = 0

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return False

    def build(self, prompt, **kw):
        self.build_calls += 1
        (Path(self._workspace["path"]) / "partial.txt").write_text("work in progress\n")
        job = load_job_plan(self._job_id)
        t1_id = job.tasks[0].task_id
        result = tv.veto_task_command(
            job, task_id=t1_id, reason="wrong approach mid-flight", actor="alice",
            control_root_path=_control())
        assert result["outcome"] == "vetoed"
        return BuilderOutput(summary="partial work", files_changed=["partial.txt"],
                             provider="fake")

    def review(self, prompt, **kw):
        raise AssertionError("the reviewer must not run: the in-flight veto halts before it")


class TestGitInFlightVetoRestoresTheWorkspace:
    def test_the_partial_file_is_gone_and_restored_is_true(
            self, root, git_repo, monkeypatch):
        job = parse_job_file(_ONE_TASK_JOB_TEXT, str(git_repo))
        job_id = job.job_id

        holder: dict = {}
        real_create = W.create

        def spy(jid, r):
            h = real_create(jid, r)
            holder["path"] = h.path
            return h

        monkeypatch.setattr(W, "create", spy)

        prov = _WritesThenSelfVetoes(job_id, holder)
        done = run_job(job_id, builder_provider=prov, reviewer_provider=prov,
                       max_rounds=1, repair_rounds=0)

        ws = Path(holder["path"])
        assert not (ws / "partial.txt").exists()
        assert done.state == JOB_BLOCKED
        t1 = done.tasks[0]
        assert t1.status == pj.TASK_VETOED
        assert t1.run_id
        entry = done.metadata["task_vetoes"][t1.task_id]
        assert entry["restored"] is True


class _BuildsThenCorruptsTheVetoArea:
    """Builds normally, then corrupts the veto control area during its own
    build call — the NEXT safe point (before review) reads it and blocks."""

    def __init__(self, job_id: str):
        self._job_id = job_id

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return False

    def build(self, prompt, **kw):
        vdir = _control() / "jobs" / self._job_id / "vetoed_tasks"
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / _veto_filename("bogus")).write_text("not json")
        return BuilderOutput(summary="ok", files_changed=["docs/README.md"], provider="fake")

    def review(self, prompt, **kw):
        raise AssertionError("the reviewer must not run: the control error halts before it")


class TestInFlightVetoControlAreaUnreadable:
    def test_blocks_with_task_veto_control_error(self, root, repo):
        tasks = [_task("A", [])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        prov = _BuildsThenCorruptsTheVetoArea(job_id)

        done = run_job(job_id, builder_provider=prov, reviewer_provider=prov,
                       max_rounds=1, repair_rounds=0)

        assert done.state == JOB_BLOCKED
        assert done.error.startswith("task_veto_control_error:")
        a = done.tasks[0]
        assert a.status == pj.TASK_RUNNING             # the fold never reached it
        assert a.run_id
