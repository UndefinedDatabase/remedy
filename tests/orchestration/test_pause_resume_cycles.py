"""F025 R3 — the pause brought to the cycle executor, `run_cycles` (E1 to E7).

One test per row of the block's semantics table: a job pause at the loop's own
safe point parks with zero task steps; a job pause requested mid-cycle lets
the running step finish and withholds the rest of the batch; the task mask
withholds a paused branch's downstream on the diamond DAG while independent
branches keep running; a release and a relaunch resume exactly where things
stood; a stop beats a pause; an awaiting decision and a paused branch coexist;
a corrupt `paused_tasks` entry blocks loudly (E5); the wall clock keeps
counting through a pause; a relaunch that is still withheld stays parked; and
`paused_by_operator` writes no final report (E6).

Reuses `test_long_run_executor.py`'s fixtures and fakes exactly, the way
`test_pause_resume.py` reuses `test_job_stop_integration.py`'s: the same
`isolate_data_root`/`control_root` fixtures, the same `FakeProvider`/
`FakeClock`, the same `SteeredStep`/diamond job for DAG withholding, and the
same `make_job`/`never_called_step`/`no_save`/`passing_verify` for the linear
cases.
"""
from __future__ import annotations

from pathlib import Path

import packages.orchestration.long_run_executor as lre
from packages.core.models import JobBudgets, RunState
from packages.orchestration import pause_control as pc
from packages.orchestration.builder_models import TaskExecutionContext
from packages.orchestration.long_run_executor import (
    TERMINAL_ALL_GREEN,
    TERMINAL_BLOCKED,
    TERMINAL_PAUSED_BY_OPERATOR,
    CycleLimits,
    TaskAttempt,
    run_cycles,
)
from packages.orchestration.pingpong_job import JOB_PAUSED, load_job_plan, save_job_plan
from packages.orchestration.safe_points import job_control_dir

# Reused exactly, per the block: the fixtures and fakes the terminal-status
# matrix is already driven through.
from tests.orchestration.test_long_run_executor import (  # noqa: F401
    T0,
    FakeClock,
    FakeProvider,
    SteeredStep,
    completing_step,
    control_root,
    isolate_data_root,
    make_diamond_job,
    make_job,
    never_called_step,
    no_save,
    passing_verify,
    planned_id_of,
    task_by_planned_id,
)


def _events(data_root: Path, job_id: str, event: str) -> list[dict]:
    """Mirrors `test_job_stop_integration._events`: every ledger event of this
    name for this job, across every run-log file `RunLogWriter` produced."""
    import json

    runs = data_root / "job_logs" / job_id
    out: list[dict] = []
    for f in sorted(runs.glob("*.jsonl")) if runs.is_dir() else []:
        for line in f.read_text().splitlines():
            if line.strip():
                raw = json.loads(line)
                if raw.get("event") == event:
                    out.append(raw)
    return out


class DecisionOrCompleteStep:
    """A step that raises `needs_decision` for one named planned id and
    completes every other ready task normally — c6's "awaiting beside
    paused" branch needs a decision on demand, not a hard-coded failure."""

    def __init__(self, decision_planned_id: str) -> None:
        self.decision_planned_id = decision_planned_id
        self.executed: list[str] = []

    def __call__(self, job, provider_call, task_id=None) -> TaskAttempt:
        if task_id is not None:
            task = next((t for t in job.tasks if t.task_id == task_id), None)
        else:
            task = next((t for t in job.tasks if t.status == RunState.PENDING), None)
        if task is None:
            return TaskAttempt()
        planned_id = task.inputs["plan"]["planned_id"]
        if planned_id == self.decision_planned_id:
            return TaskAttempt(task_id=task.task_id, needs_decision=True,
                               question="continue on this branch?",
                               options=("yes", "no"), safe_default="")
        provider_call(TaskExecutionContext(
            job_id=str(job.job_id), job_prompt=job.user_prompt,
            task_id=str(task.task_id), task_type=task.inputs.get("task_type", "unknown"),
            task_description=task.title,
        ))
        self.executed.append(planned_id)
        task.status = RunState.COMPLETED
        if all(t.status == RunState.COMPLETED for t in job.tasks):
            job.state = RunState.COMPLETED
        return TaskAttempt(task_id=task.task_id, executed=True, verified=True)


class TestC1JobPausePendingAtFirstSafePoint:
    def test_parks_with_zero_task_steps(self, isolate_data_root, control_root):
        job = make_job(2)
        pc.request_pause(str(job.job_id), "operator pause", "cli",
                         control_root_path=control_root)

        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )

        assert result.terminal_status == TERMINAL_PAUSED_BY_OPERATOR
        assert result.job_status == JOB_PAUSED
        assert result.cycles_run == 0
        assert job.state == RunState.PAUSED
        assert job.pause.get("scope") == "job"
        assert len(_events(isolate_data_root, str(job.job_id), "job_paused")) == 1
        assert pc.pause_requested(str(job.job_id), control_root_path=control_root) is None
        archive_dir = job_control_dir(str(job.job_id), control_root) / pc.PAUSE_ARCHIVE_DIRNAME
        archived = list(archive_dir.glob("*.json"))
        assert len(archived) == 1
        import json as _json
        assert _json.loads(archived[0].read_text())["outcome"] == "served"


class TestC2AJobPauseDuringTheFirstTaskStep:
    def test_the_running_step_finishes_and_task_two_is_never_picked(
            self, isolate_data_root, control_root):
        job = make_job(2)
        calls = {"n": 0}

        def pausing_step(j, provider_call):
            calls["n"] += 1
            if calls["n"] == 1:
                pc.request_pause(str(j.job_id), "mid-batch pause", "cli",
                                 control_root_path=control_root)
            return completing_step(j, provider_call)

        result = run_cycles(
            job, CycleLimits(max_cycles=5, batch_size=2), FakeProvider(),
            task_step=pausing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )

        assert calls["n"] == 1                       # task 2 never dispatched
        assert job.tasks[0].status == RunState.COMPLETED
        assert job.tasks[1].status == RunState.PENDING
        assert result.terminal_status == TERMINAL_PAUSED_BY_OPERATOR
        assert result.cycles_run == 1
        assert result.cycles[0].tasks_completed == 1


class TestC3TheDiamondWithBPaused:
    def test_a_and_c_run_d_is_withheld_and_the_park_names_b(
            self, isolate_data_root, control_root):
        job = make_diamond_job()
        b_task = task_by_planned_id(job, "B")
        d_task = task_by_planned_id(job, "D")
        pc.request_task_pause(str(job.job_id), str(b_task.task_id),
                              "second branch needs a human", "cli",
                              control_root_path=control_root)
        step = SteeredStep()

        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )

        assert set(step.executed) == {"A", "C"}
        assert result.terminal_status == TERMINAL_PAUSED_BY_OPERATOR
        assert result.stop_reason == f"paused_tasks={b_task.task_id}"
        assert job.pause.get("scope") == "task"
        assert job.pause.get("paused_task_ids") == [str(b_task.task_id)]
        assert str(d_task.task_id) in (job.pause.get("withheld_task_ids") or [])
        last = result.cycles[-1]
        assert last.paused_task_ids == (str(b_task.task_id),)
        assert last.paused_downstream_task_ids == (str(d_task.task_id),)


class TestC4AfterReleaseTheRelaunchResumes:
    def test_writes_one_job_resumed_runs_b_then_d_and_ends_all_green(
            self, isolate_data_root, control_root):
        job = make_diamond_job()
        b_task = task_by_planned_id(job, "B")
        pc.request_task_pause(str(job.job_id), str(b_task.task_id),
                              "second branch needs a human", "cli",
                              control_root_path=control_root)
        step = SteeredStep()
        parked = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )
        assert parked.terminal_status == TERMINAL_PAUSED_BY_OPERATOR

        pc.release_task_pause(str(job.job_id), str(b_task.task_id),
                              control_root_path=control_root)

        resumed = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )

        assert resumed.terminal_status == TERMINAL_ALL_GREEN
        assert set(step.executed) == {"A", "C", "B", "D"}
        assert job.pause == {}
        assert len(_events(isolate_data_root, str(job.job_id), "job_resumed")) == 1


class TestC5AStopAndAJobPauseBothPending:
    def test_the_stop_wins_and_the_pause_is_superseded(
            self, isolate_data_root, control_root):
        from packages.orchestration.safe_points import request_stop

        job = make_job(2)
        request_stop(str(job.job_id), "operator stop", "cli",
                    control_root_path=control_root)
        pending_pause = pc.request_pause(str(job.job_id), "operator pause", "cli",
                                         control_root_path=control_root)

        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )

        assert result.terminal_status == lre.TERMINAL_STOPPED_BY_OPERATOR
        assert len(_events(isolate_data_root, str(job.job_id), "job_paused")) == 0
        archive_path = (job_control_dir(str(job.job_id), control_root)
                        / pc.PAUSE_ARCHIVE_DIRNAME / f"{pending_pause.request_id}.json")
        assert archive_path.is_file()
        import json as _json
        assert _json.loads(archive_path.read_text())["outcome"] == "superseded_by_stop"
        assert pc.pause_requested(str(job.job_id), control_root_path=control_root) is None


class TestC6AnAwaitingBranchBesideAPausedBranch:
    def test_ends_with_the_awaiting_terminal_and_names_both(
            self, isolate_data_root, control_root):
        job = make_diamond_job()
        c_task = task_by_planned_id(job, "C")
        d_task = task_by_planned_id(job, "D")
        pc.request_task_pause(str(job.job_id), str(c_task.task_id),
                              "third branch needs a human", "cli",
                              control_root_path=control_root)
        step = DecisionOrCompleteStep("B")

        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )

        assert step.executed == ["A"]
        assert result.terminal_status == TERMINAL_BLOCKED   # the awaiting terminal
        assert "awaiting_decision" in result.stop_reason
        last = result.cycles[-1]
        b_task = task_by_planned_id(job, "B")
        assert str(b_task.task_id) in last.awaiting_task_ids
        assert str(c_task.task_id) in last.paused_task_ids
        assert str(d_task.task_id) in last.paused_downstream_task_ids


class TestC7ACorruptPausedTasksEntry:
    def test_blocks_with_pause_control_error_and_zero_task_steps(
            self, isolate_data_root, control_root):
        job = make_job(2)
        pc.request_task_pause(str(job.job_id), "some-other-task", "reason", "cli",
                              control_root_path=control_root)
        paused_dir = job_control_dir(str(job.job_id), control_root) / pc.PAUSED_TASKS_DIRNAME
        entry = next(paused_dir.iterdir())
        entry.write_bytes(b"{not valid json")

        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )

        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.stop_reason.startswith("pause_control_error:")
        assert result.cycles_run == 0


class TestC8TheDeadlineKeepsCountingThroughAPause:
    def test_a_parked_relaunch_with_an_exhausted_wall_clock_stops_at_zero_calls(
            self, isolate_data_root, control_root):
        job = make_job(1)
        pc.request_pause(str(job.job_id), "operator pause", "cli",
                         control_root_path=control_root)
        parked = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=save_job_plan, control_root_path=control_root,
        )
        assert parked.terminal_status == TERMINAL_PAUSED_BY_OPERATOR
        assert job.state == RunState.PAUSED

        reloaded = load_job_plan(str(job.job_id))
        assert reloaded is not None
        from datetime import timedelta
        moved = T0 - timedelta(days=1)
        moved_iso = moved.isoformat()
        reloaded.first_running_at = moved_iso
        reloaded.budget_actuals = {
            "schema_version": "1.0.0",
            "provider_call_count": 0,
            "actual_call_count": 0,
            "unmeasured_call_count": 0,
            "total_tokens": 0,
            "actual_sources": [],
            "started_at": moved_iso,
        }
        save_job_plan(reloaded)

        budgets = JobBudgets(deadline=moved + timedelta(hours=1))
        result = run_cycles(
            reloaded, CycleLimits(max_cycles=5, budgets=budgets), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=save_job_plan, control_root_path=control_root,
        )

        assert result.terminal_status == lre.TERMINAL_DEADLINE_REACHED
        assert result.cycles_run == 0


class TestC9ARelaunchWhileStillPaused:
    def test_stays_parked_with_zero_steps_and_no_new_event(
            self, isolate_data_root, control_root):
        job = make_diamond_job()
        b_task = task_by_planned_id(job, "B")
        pc.request_task_pause(str(job.job_id), str(b_task.task_id),
                              "second branch needs a human", "cli",
                              control_root_path=control_root)
        step = SteeredStep()
        parked = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )
        assert parked.terminal_status == TERMINAL_PAUSED_BY_OPERATOR
        before = len(_events(isolate_data_root, str(job.job_id), "job_paused"))
        assert before == 1

        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )

        assert result.terminal_status == TERMINAL_PAUSED_BY_OPERATOR
        assert result.cycles_run == 0
        assert len(_events(isolate_data_root, str(job.job_id), "job_paused")) == before
        assert _events(isolate_data_root, str(job.job_id), "job_resumed") == []


class TestC10PausedByOperatorWritesNoFinalReport:
    def test_write_final_report_is_never_called(
            self, isolate_data_root, control_root, monkeypatch):
        import packages.orchestration.run_report as run_report_mod

        calls: list[object] = []
        monkeypatch.setattr(run_report_mod, "write_final_report",
                            lambda *a, **k: calls.append(True))

        job = make_job(1)
        pc.request_pause(str(job.job_id), "operator pause", "cli",
                         control_root_path=control_root)

        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )

        assert result.terminal_status == TERMINAL_PAUSED_BY_OPERATOR
        assert calls == []
