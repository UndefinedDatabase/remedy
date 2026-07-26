"""F046 T001 — multi-cycle loop conductor.

One test per row of the terminal-status matrix, an ordering test proving a
cycle never starts after should_stop says stop, and a five-cycle fixture that
reaches every stop cause with a fake provider.  Nothing here sleeps: wall
clock and deadlines go through an injected clock.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.core.models import Job, JobBudgets, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.long_run_executor import (
    TERMINAL_ALL_GREEN,
    TERMINAL_BLOCKED,
    TERMINAL_BUDGET_EXHAUSTED,
    TERMINAL_DEADLINE_REACHED,
    TERMINAL_JOB_STATUS,
    TERMINAL_MAX_CYCLES_REACHED,
    TERMINAL_RUN_STATE,
    TERMINAL_STOPPED_BY_OPERATOR,
    VERIFY_FAILED,
    VERIFY_NOT_RUN,
    VERIFY_PASSED,
    CycleLimits,
    TaskAttempt,
    default_task_step,
    ready_tasks,
    run_cycles,
)
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_RUNNING,
    JOB_STOPPED,
)
from packages.orchestration.safe_points import request_stop

UTC = timezone.utc
T0 = datetime(2026, 7, 26, 12, 0, 0, tzinfo=UTC)


# ---------------------------------------------------------------------------
# Fixtures and fakes
# ---------------------------------------------------------------------------


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def control_root(tmp_path: Path) -> Path:
    root = tmp_path / "control"
    root.mkdir()
    return root


def make_job(task_count: int = 1, *, name: str = "cycle-job") -> Job:
    return Job(
        name=name,
        user_prompt="build the thing",
        tasks=[
            Task(description=f"task {i}", inputs={"task_type": "documentation"})
            for i in range(task_count)
        ],
        state=RunState.PLANNED,
    )


class FakeProvider:
    """A builder that always returns verifiable output and counts its calls."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, context: TaskExecutionContext) -> BuilderOutput:
        self.calls += 1
        return BuilderOutput(
            summary=f"did {context.task_description}",
            proposed_changes=[f"write docs for {context.task_description}"],
        )


class FakeClock:
    """A clock that advances only when the test says so."""

    def __init__(self, start: datetime = T0, step: timedelta = timedelta(seconds=1)) -> None:
        self.now = start
        self.step = step
        self.reads = 0

    def __call__(self) -> datetime:
        self.reads += 1
        current = self.now
        self.now = self.now + self.step
        return current


def completing_step(job: Job, provider_call) -> TaskAttempt:
    """A task step that completes the first PENDING task, calling the provider."""
    task = next((t for t in job.tasks if t.status == RunState.PENDING), None)
    if task is None:
        return TaskAttempt()
    provider_call(
        TaskExecutionContext(
            job_id=job.id,
            job_prompt=job.user_prompt,
            task_id=task.id,
            task_type=task.inputs.get("task_type", "unknown"),
            task_description=task.description,
        )
    )
    task.status = RunState.COMPLETED
    if all(t.status == RunState.COMPLETED for t in job.tasks):
        job.state = RunState.COMPLETED
    return TaskAttempt(task_id=task.id, executed=True, verified=True)


def never_called_step(job: Job, provider_call) -> TaskAttempt:
    raise AssertionError("a cycle started after should_stop said stop")


def passing_verify(job: Job, cycle_index: int, verify_command) -> str:
    return VERIFY_PASSED


def failing_verify(job: Job, cycle_index: int, verify_command) -> str:
    return VERIFY_FAILED


def no_save(job: Job) -> None:
    """Persistence is exercised separately; most matrix tests stay in memory."""
    return None


class RecordingLog:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict]] = []

    def log(self, event: str, **meta) -> None:
        self.events.append((event, meta))


# ---------------------------------------------------------------------------
# Terminal-status matrix — one test per row
# ---------------------------------------------------------------------------


class TestTerminalStatusMatrix:
    def test_all_green(self, control_root):
        job = make_job(2)
        provider = FakeProvider()
        result = run_cycles(
            job, CycleLimits(max_cycles=5), provider,
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_ALL_GREEN
        assert result.job_status == JOB_COMPLETED
        assert job.state == RunState.COMPLETED
        assert result.cycles_run == 2
        assert provider.calls == 2

    def test_stopped_by_operator(self, control_root):
        job = make_job(3)
        request_stop(str(job.id), reason="operator asked", control_root_path=control_root)
        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_STOPPED_BY_OPERATOR
        assert result.job_status == JOB_STOPPED
        assert job.state == RunState.PAUSED
        assert "operator_stop" in result.stop_reason
        assert result.cycles_run == 0

    def test_budget_exhausted(self, control_root):
        job = make_job(4)
        result = run_cycles(
            job, CycleLimits(max_cycles=5, budgets=JobBudgets(max_provider_calls=2)),
            FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_BUDGET_EXHAUSTED
        assert result.job_status == JOB_STOPPED
        assert job.state == RunState.PAUSED
        assert result.stop_reason == "budget_exhausted:max_provider_calls"
        # Two cycles ran (one provider call each), the third safe point stopped.
        assert result.cycles_run == 2

    def test_deadline_reached(self, control_root):
        job = make_job(4)
        clock = FakeClock(step=timedelta(minutes=10))
        budgets = JobBudgets(deadline=T0 + timedelta(minutes=15))
        result = run_cycles(
            job, CycleLimits(max_cycles=5, budgets=budgets), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=clock, save=no_save, control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_DEADLINE_REACHED
        assert result.job_status == JOB_STOPPED
        assert job.state == RunState.PAUSED
        assert result.stop_reason == "budget_exhausted:deadline"
        assert result.cycles_run >= 1

    def test_blocked_zero_ready_tasks_not_green(self, control_root):
        job = make_job(2)
        # Neither PENDING (not ready) nor COMPLETED (not green): awaiting a decision.
        job.tasks[0].status = RunState.COMPLETED
        job.tasks[1].status = RunState.RUNNING
        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.job_status == JOB_BLOCKED
        assert job.state == RunState.PAUSED
        assert result.cycles_run == 0

    def test_max_cycles_reached_leaves_job_running(self, control_root):
        job = make_job(3)
        job.state = RunState.RUNNING
        result = run_cycles(
            job, CycleLimits(max_cycles=1), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_MAX_CYCLES_REACHED
        assert result.job_status == JOB_RUNNING
        assert job.state == RunState.RUNNING       # untouched by the conductor
        assert result.cycles_run == 1


class TestStatusMapping:
    def test_every_terminal_status_maps_to_a_job_status_and_run_state(self):
        assert set(TERMINAL_JOB_STATUS) == set(TERMINAL_RUN_STATE)
        assert TERMINAL_JOB_STATUS[TERMINAL_ALL_GREEN] == JOB_COMPLETED
        assert TERMINAL_JOB_STATUS[TERMINAL_STOPPED_BY_OPERATOR] == JOB_STOPPED
        assert TERMINAL_JOB_STATUS[TERMINAL_BUDGET_EXHAUSTED] == JOB_STOPPED
        assert TERMINAL_JOB_STATUS[TERMINAL_DEADLINE_REACHED] == JOB_STOPPED
        assert TERMINAL_JOB_STATUS[TERMINAL_BLOCKED] == JOB_BLOCKED
        assert TERMINAL_JOB_STATUS[TERMINAL_MAX_CYCLES_REACHED] == JOB_RUNNING
        assert TERMINAL_RUN_STATE[TERMINAL_MAX_CYCLES_REACHED] is None

    def test_terminal_status_recorded_on_the_job(self, control_root):
        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=3), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert job.metadata["cycle_terminal_status"] == result.terminal_status
        assert job.metadata["cycle_job_status"] == result.job_status
        assert "cycle_stop_reason" not in job.metadata


# ---------------------------------------------------------------------------
# Ordering — a cycle never starts after should_stop says stop
# ---------------------------------------------------------------------------


class TestOrdering:
    def test_no_cycle_starts_after_stop_is_requested(self, control_root):
        """The stop lands after cycle 1; cycle 2 must never begin."""
        job = make_job(4)
        order: list[str] = []

        def stopping_step(j: Job, provider_call) -> TaskAttempt:
            order.append("cycle")
            if len(order) == 1:
                request_stop(str(j.id), reason="mid-run", control_root_path=control_root)
            return completing_step(j, provider_call)

        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=stopping_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert order == ["cycle"]
        assert result.cycles_run == 1
        assert result.terminal_status == TERMINAL_STOPPED_BY_OPERATOR

    def test_stop_before_the_first_cycle_runs_nothing(self, control_root):
        job = make_job(2)
        request_stop(str(job.id), reason="before start", control_root_path=control_root)
        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, clock=FakeClock(), save=no_save,
            control_root_path=control_root,
        )
        assert result.cycles == ()
        assert all(t.status == RunState.PENDING for t in job.tasks)

    def test_max_cycles_zero_runs_nothing(self, control_root):
        job = make_job(2)
        result = run_cycles(
            job, CycleLimits(max_cycles=0), FakeProvider(),
            task_step=never_called_step, clock=FakeClock(), save=no_save,
            control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_MAX_CYCLES_REACHED
        assert result.cycles_run == 0


# ---------------------------------------------------------------------------
# Five-cycle fixture — every stop cause, one loop each, fake provider
# ---------------------------------------------------------------------------


class TestFiveCycleFixture:
    """Five loops over the same five-task shape, one per stop cause."""

    def _run(self, control_root, **kwargs):
        job = kwargs.pop("job", None) or make_job(5)
        provider = FakeProvider()
        limits = kwargs.pop("limits", CycleLimits(max_cycles=5))
        result = run_cycles(
            job, limits, provider,
            task_step=kwargs.pop("task_step", completing_step),
            verify=kwargs.pop("verify", passing_verify),
            clock=kwargs.pop("clock", FakeClock()),
            save=no_save, control_root_path=control_root, **kwargs,
        )
        return job, provider, result

    def test_five_cycles_reach_all_green(self, control_root):
        job, provider, result = self._run(control_root)
        assert result.cycles_run == 5
        assert provider.calls == 5
        assert result.terminal_status == TERMINAL_ALL_GREEN
        assert [c.cycle_index for c in result.cycles] == [1, 2, 3, 4, 5]

    def test_operator_stop_in_the_middle_of_five(self, control_root):
        job = make_job(5)
        seen: list[int] = []

        def step(j: Job, provider_call) -> TaskAttempt:
            seen.append(len(seen) + 1)
            if len(seen) == 3:
                request_stop(str(j.id), reason="stop at three",
                             control_root_path=control_root)
            return completing_step(j, provider_call)

        _, provider, result = self._run(control_root, job=job, task_step=step)
        assert result.terminal_status == TERMINAL_STOPPED_BY_OPERATOR
        assert result.cycles_run == 3
        assert provider.calls == 3

    def test_budget_stops_before_the_fifth_cycle(self, control_root):
        _, provider, result = self._run(
            control_root,
            limits=CycleLimits(max_cycles=5, budgets=JobBudgets(max_provider_calls=4)),
        )
        assert result.terminal_status == TERMINAL_BUDGET_EXHAUSTED
        assert result.cycles_run == 4
        assert provider.calls == 4

    def test_deadline_stops_before_the_fifth_cycle(self, control_root):
        clock = FakeClock(step=timedelta(minutes=1))
        # Each cycle reads the clock twice (safe point + cycle end), so the
        # deadline lands during the loop without anything ever sleeping.
        _, _, result = self._run(
            control_root, clock=clock,
            limits=CycleLimits(max_cycles=5,
                               budgets=JobBudgets(deadline=T0 + timedelta(minutes=5))),
        )
        assert result.terminal_status == TERMINAL_DEADLINE_REACHED
        assert 1 <= result.cycles_run < 5

    def test_blocked_when_a_task_awaits_a_decision(self, control_root):
        job = make_job(5)
        job.tasks[2].status = RunState.RUNNING          # awaiting a decision
        job.tasks[3].status = RunState.RUNNING
        job.tasks[4].status = RunState.RUNNING
        _, provider, result = self._run(control_root, job=job)
        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.cycles_run == 2                   # only the two PENDING ones
        assert provider.calls == 2
        assert "no_ready_tasks" in result.stop_reason


# ---------------------------------------------------------------------------
# Verify step
# ---------------------------------------------------------------------------


class TestVerifyStep:
    def test_failed_verify_ends_the_cycle_and_is_recorded(self, control_root):
        job = make_job(2)
        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=completing_step, verify=failing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.cycles[0].verify_result == VERIFY_FAILED
        assert "verify_failed" in result.cycles[0].errors

    def test_failed_verify_denies_all_green(self, control_root):
        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=3), FakeProvider(),
            task_step=completing_step, verify=failing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert all(t.status == RunState.COMPLETED for t in job.tasks)
        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.job_status == JOB_BLOCKED

    def test_no_verify_configured_is_recorded_as_not_run(self, control_root):
        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=3), FakeProvider(),
            task_step=completing_step, clock=FakeClock(), save=no_save,
            control_root_path=control_root,
        )
        assert result.cycles[0].verify_result == VERIFY_NOT_RUN
        assert result.terminal_status == TERMINAL_ALL_GREEN


# ---------------------------------------------------------------------------
# Ready batch, limits, persistence, ledger
# ---------------------------------------------------------------------------


class TestReadyBatch:
    def test_linear_order_capped_at_batch_size(self):
        job = make_job(4)
        assert len(ready_tasks(job, 2)) == 2
        assert ready_tasks(job, 2) == [job.tasks[0].id, job.tasks[1].id]

    def test_batch_larger_than_remaining_tasks_is_fine(self, control_root):
        job = make_job(2)
        result = run_cycles(
            job, CycleLimits(max_cycles=5, batch_size=10), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.cycles_run == 1
        assert result.cycles[0].tasks_attempted == 2
        assert result.terminal_status == TERMINAL_ALL_GREEN

    def test_invalid_limits_are_refused(self):
        with pytest.raises(ValueError):
            CycleLimits(max_cycles=-1)
        with pytest.raises(ValueError):
            CycleLimits(batch_size=0)


class TestPersistenceAndLedger:
    def test_job_is_persisted_after_every_cycle_and_at_the_end(self, control_root):
        job = make_job(3)
        saves: list[str] = []
        run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=lambda j: saves.append(j.state.value),
            control_root_path=control_root,
        )
        assert len(saves) == 4                       # 3 cycles + the terminal write

    def test_ledger_events_agree_with_the_result(self, control_root):
        job = make_job(2)
        log = RecordingLog()
        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, log=log,
            control_root_path=control_root,
        )
        names = [e for e, _ in log.events]
        assert names == ["cycle_completed", "cycle_completed", "cycle_loop_terminal"]
        terminal_meta = log.events[-1][1]
        assert terminal_meta["terminal_status"] == result.terminal_status
        assert terminal_meta["job_status"] == result.job_status
        assert terminal_meta["cycles_run"] == result.cycles_run

    def test_a_broken_ledger_writer_never_breaks_the_loop(self, control_root):
        class Exploding:
            def log(self, event, **meta):
                raise RuntimeError("ledger is down")

        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=2), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, log=Exploding(),
            control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_ALL_GREEN


# ---------------------------------------------------------------------------
# The default task step — the real single-task path with a fake provider
# ---------------------------------------------------------------------------


class TestDefaultTaskStep:
    def test_default_step_runs_the_real_single_task_path(
        self, isolate_data_root, control_root
    ):
        job = make_job(2)
        provider = FakeProvider()
        result = run_cycles(
            job, CycleLimits(max_cycles=5), provider,
            task_step=default_task_step, verify=passing_verify,
            clock=FakeClock(), control_root_path=control_root,
        )
        assert provider.calls == 2
        assert result.terminal_status == TERMINAL_ALL_GREEN
        assert all(t.status == RunState.COMPLETED for t in job.tasks)
        assert (isolate_data_root / "jobs" / f"{job.id}.json").is_file()

    def test_provider_failure_is_recorded_and_the_task_stays_pending(
        self, isolate_data_root, control_root
    ):
        def exploding_provider(context: TaskExecutionContext) -> BuilderOutput:
            raise RuntimeError("provider is down")

        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=1), exploding_provider,
            task_step=default_task_step, verify=passing_verify,
            clock=FakeClock(), control_root_path=control_root,
        )
        assert result.cycles[0].tasks_failed == 1
        assert "RuntimeError" in result.cycles[0].errors[0]
        assert job.tasks[0].status == RunState.PENDING   # rolled back by the runner
