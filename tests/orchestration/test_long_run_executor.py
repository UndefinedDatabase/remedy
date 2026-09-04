"""F046 — multi-cycle loop conductor (T001) and its evidence, config and
single-pass regression (T002).

One test per row of the terminal-status matrix, an ordering test proving a
cycle never starts after should_stop says stop, and a five-cycle fixture that
reaches every stop cause with a fake provider.  Nothing here sleeps: wall
clock and deadlines go through an injected clock.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import packages.orchestration.long_run_executor as lre
from packages.core.models import Job, JobBudgets, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.config import get_key_spec
from packages.orchestration.long_run_executor import (
    CYCLE_SAFETY_CAP,
    DEFAULT_BATCH_SIZE,
    DEFAULT_MAX_CYCLES,
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
    cycle_evidence_dir,
    default_task_step,
    limits_from_config,
    read_cycle_records,
    ready_tasks,
    resolve_max_cycles,
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


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Autouse: every cycle writes an evidence record, so no test may ever
    reach the repository's real data root."""
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
    def test_legacy_plan_releases_one_task_at_a_time(self):
        """F050 replaced the linear batch with the DAG ready set.

        ``make_job`` builds tasks without Flight Plan metadata, so the legacy
        rule applies: each task depends on its predecessor.  The ready set is
        therefore one task deep until that predecessor completes — where this
        used to return the first ``batch_size`` PENDING tasks.  Loop behavior
        for such plans is unchanged (see the linear-regression tests below and
        ``test_batch_larger_than_remaining_tasks_is_fine``): the batch is a cap
        on how many tasks a cycle runs, and the set is recomputed after each.
        """
        job = make_job(4)
        assert ready_tasks(job, 2) == [job.tasks[0].id]

        job.tasks[0].status = RunState.COMPLETED
        assert ready_tasks(job, 2) == [job.tasks[1].id]

    def test_independent_tasks_fill_the_batch_up_to_its_cap(self):
        job = make_job(4)
        # Flight metadata declaring no dependencies: all four are ready, and
        # the cap is what limits the batch.
        for index, task in enumerate(job.tasks):
            task.inputs["flight"] = {"planned_id": f"T{index}", "depends_on": []}
        assert ready_tasks(job, 2) == [job.tasks[0].id, job.tasks[1].id]
        assert len(ready_tasks(job, 10)) == 4

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


# ---------------------------------------------------------------------------
# T002 — cycle evidence records
# ---------------------------------------------------------------------------


class TestCycleEvidence:
    def test_n_cycles_produce_exactly_n_monotonic_records(self, control_root):
        job = make_job(4)
        result = run_cycles(
            job, CycleLimits(max_cycles=4), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        records = read_cycle_records(str(job.id))
        assert result.cycles_run == 4
        assert len(records) == 4
        assert [r["cycle_index"] for r in records] == [1, 2, 3, 4]

    def test_record_carries_the_cycle_summary(self, control_root):
        job = make_job(1)
        run_cycles(
            job, CycleLimits(max_cycles=1, verify_command="pytest -q"),
            FakeProvider(), task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        record = read_cycle_records(str(job.id))[0]
        assert record["job_id"] == str(job.id)
        assert record["tasks_attempted"] == 1
        assert record["tasks_completed"] == 1
        assert record["tasks_failed"] == 0
        assert record["verify_result"] == VERIFY_PASSED
        assert record["verify_command"] == "pytest -q"
        assert record["tokens_so_far"] == 0        # nothing measured, nothing claimed
        assert record["started_at"] and record["ended_at"]

    def test_records_live_in_the_job_evidence_area(self, isolate_data_root, control_root):
        job = make_job(1)
        run_cycles(
            job, CycleLimits(max_cycles=1), FakeProvider(),
            task_step=completing_step, clock=FakeClock(), save=no_save,
            control_root_path=control_root,
        )
        expected = isolate_data_root / "jobs" / str(job.id) / "evidence" / "cycles"
        assert cycle_evidence_dir(str(job.id)) == expected
        assert (expected / "cycle_0001.json").is_file()

    def test_evidence_can_be_switched_off(self, control_root):
        job = make_job(2)
        run_cycles(
            job, CycleLimits(max_cycles=2), FakeProvider(),
            task_step=completing_step, clock=FakeClock(), save=no_save,
            control_root_path=control_root, record_evidence=False,
        )
        assert read_cycle_records(str(job.id)) == []

    def test_no_records_when_no_cycle_ran(self, control_root):
        job = make_job(2)
        request_stop(str(job.id), reason="stop first", control_root_path=control_root)
        run_cycles(
            job, CycleLimits(max_cycles=3), FakeProvider(),
            task_step=never_called_step, clock=FakeClock(), save=no_save,
            control_root_path=control_root,
        )
        assert read_cycle_records(str(job.id)) == []


# ---------------------------------------------------------------------------
# T002 — config keys and the rollout cap
# ---------------------------------------------------------------------------


class FakeConfig:
    def __init__(self, **values) -> None:
        self._values = values

    def get(self, key: str):
        return self._values.get(key)


class TestCycleConfig:
    def test_config_keys_are_registered_with_the_rollout_default(self):
        assert get_key_spec("cycles.max_cycles").default == DEFAULT_MAX_CYCLES == 1
        assert get_key_spec("cycles.batch_size").default == DEFAULT_BATCH_SIZE
        assert get_key_spec("cycles.verify_command").default is None
        assert get_key_spec("cycles.max_cycles").env_var == "REMEDY_CYCLES_MAX_CYCLES"

    def test_default_when_nothing_is_set(self):
        r = resolve_max_cycles()
        assert (r.max_cycles, r.source, r.capped) == (1, "default", False)

    def test_flag_beats_config(self, monkeypatch):
        monkeypatch.setattr(lre, "CYCLE_SAFETY_CAP", 10)
        r = resolve_max_cycles(flag=4, config_value=7)
        assert (r.max_cycles, r.source, r.requested) == (4, "flag", 4)

    def test_config_used_when_no_flag(self, monkeypatch):
        monkeypatch.setattr(lre, "CYCLE_SAFETY_CAP", 10)
        r = resolve_max_cycles(config_value=6)
        assert (r.max_cycles, r.source) == (6, "config")

    def test_the_rollout_cap_is_eight_since_adr_0001_was_applied(self):
        """ADR-0001 (docs/adr/0001-raise-cycle-safety-cap.md) raised
        CYCLE_SAFETY_CAP from 1 to 8 on the F075 10/10 evidence — 8 is the
        largest cycle budget that campaign granted and completed under.  The
        ADR is ACCEPTED & APPLIED; this pin fails the moment the constant
        moves again, so any further change needs its own record.  The shipped
        DEFAULT_MAX_CYCLES stays 1: the ceiling rose, the default did not.
        """
        assert CYCLE_SAFETY_CAP == 8
        assert DEFAULT_MAX_CYCLES == 1

    def test_the_cap_trims_both_flag_and_config(self):
        flagged = resolve_max_cycles(flag=25)
        configured = resolve_max_cycles(config_value=25)
        assert flagged.max_cycles == configured.max_cycles == CYCLE_SAFETY_CAP == 8
        assert flagged.capped is True and flagged.requested == 25
        assert configured.capped is True

    def test_zero_or_negative_is_refused(self):
        with pytest.raises(ValueError):
            resolve_max_cycles(flag=0)
        with pytest.raises(ValueError):
            resolve_max_cycles(config_value=-3)

    def test_limits_from_config(self, monkeypatch):
        monkeypatch.setattr(lre, "CYCLE_SAFETY_CAP", 10)
        limits, resolved = limits_from_config(
            FakeConfig(**{"cycles.max_cycles": 3, "cycles.batch_size": 5,
                          "cycles.verify_command": "make test"}),
        )
        assert limits.max_cycles == 3
        assert limits.batch_size == 5
        assert limits.verify_command == "make test"
        assert resolved.source == "config"

    def test_limits_from_config_falls_back_to_the_defaults(self):
        limits, resolved = limits_from_config(FakeConfig())
        assert limits.max_cycles == DEFAULT_MAX_CYCLES
        assert limits.batch_size == DEFAULT_BATCH_SIZE
        assert limits.verify_command is None
        assert resolved.source == "default"


# ---------------------------------------------------------------------------
# T002 — single-pass regression
# ---------------------------------------------------------------------------


def _single_pass(job: Job, provider) -> None:
    """Today's single pass, exactly as `remedy job run-next` performs it."""
    from packages.orchestration.storage import save_job
    from packages.orchestration.task_runner import (
        finalize_task,
        materialize_task_output,
        run_next_task,
    )
    from packages.orchestration.verifier import verify_task_output
    from packages.orchestration.workspace import LocalWorkspaceRuntime

    result = run_next_task(job, provider)
    if not result.changed:
        return
    materialize_task_output(result, LocalWorkspaceRuntime(job_id=job.id))
    vr = verify_task_output(result.job, result.task_id)
    finalize_task(result, vr)
    save_job(result.job)


def _normalize(job: Job) -> dict:
    """Job JSON with the randomly generated artifact ids replaced by ordinals."""
    payload = json.loads(job.model_dump_json())
    mapping: dict[str, str] = {}
    for i, artifact in enumerate(payload.get("artifacts", [])):
        mapping[artifact["id"]] = f"artifact-{i}"
    text = json.dumps(payload, sort_keys=True)
    for real, placeholder in mapping.items():
        text = text.replace(real, placeholder)
    return json.loads(text)


class TestSinglePassRegression:
    def test_defaults_reproduce_the_single_pass_exactly(
        self, isolate_data_root, control_root
    ):
        job = make_job(3)
        single = job.model_copy(deep=True)
        cycled = job.model_copy(deep=True)

        _single_pass(single, FakeProvider())
        single_workspace = sorted(
            p.name for p in (isolate_data_root / "workspaces" / str(job.id)).rglob("*")
            if p.is_file()
        )

        run_cycles(cycled, CycleLimits(), FakeProvider(),
                   task_step=default_task_step, clock=FakeClock(),
                   control_root_path=control_root)
        cycled_workspace = sorted(
            p.name for p in (isolate_data_root / "workspaces" / str(job.id)).rglob("*")
            if p.is_file()
        )

        assert cycled_workspace == single_workspace
        expected = _normalize(single)
        actual = _normalize(cycled)
        # The ONLY difference is the loop's own additive trace.
        added = set(actual["metadata"]) - set(expected["metadata"])
        assert added == {"cycle_terminal_status", "cycle_job_status"}
        for key in added:
            actual["metadata"].pop(key)
        assert actual == expected

    def test_defaults_run_exactly_one_cycle_and_leave_the_rest_pending(
        self, isolate_data_root, control_root
    ):
        job = make_job(3)
        result = run_cycles(job, CycleLimits(), FakeProvider(),
                            task_step=default_task_step, clock=FakeClock(),
                            control_root_path=control_root)
        assert result.cycles_run == 1
        assert result.terminal_status == TERMINAL_MAX_CYCLES_REACHED
        assert [t.status for t in job.tasks] == [
            RunState.COMPLETED, RunState.PENDING, RunState.PENDING,
        ]

    def test_default_limits_are_the_rollout_defaults(self):
        limits = CycleLimits()
        assert limits.max_cycles == 1
        assert limits.batch_size == 1
        assert limits.budgets is None
        assert limits.verify_command is None



# ---------------------------------------------------------------------------
# T002 — `remedy job run <id> [--cycles N]`
# ---------------------------------------------------------------------------


class FakeBuilder:
    model = "fake-model"

    def build(self, context: TaskExecutionContext) -> BuilderOutput:
        return BuilderOutput(
            summary=f"did {context.task_description}",
            proposed_changes=[f"write docs for {context.task_description}"],
        )


class TestJobRunCommand:
    def test_registered_in_the_catalog_with_a_handler(self):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.commands.job import COMMAND_HANDLERS

        entry = next(c for c in CATALOG if c.command_id == "job.run")
        assert entry.subcommand == "run"
        assert "--cycles" in [a.name for a in entry.args]
        assert "job.run" in COMMAND_HANDLERS

    def test_one_cycle_delegates_to_the_existing_single_pass(self, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd

        seen: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", seen.append)
        job_cmd._cmd_job_run_cycles("abc12345", yes=True)
        assert seen == ["abc12345"]

    def test_the_flag_is_capped_and_the_operator_is_told(self, monkeypatch, capsys):
        """ADR-0001 moved the ceiling to 8, so a capped run is no longer the
        single pass — it is a real loop run.  What is pinned is unchanged: the
        flag is trimmed to the cap and the operator is told so."""
        from apps.cli.commands import job as job_cmd
        from packages.orchestration.storage import save_job
        from packages.providers.ollama_builder import provider as provider_mod

        monkeypatch.setattr(provider_mod, "OllamaBuilder", FakeBuilder)

        job = make_job(2)
        save_job(job)
        job_cmd._cmd_job_run_cycles(str(job.id), cycles=99, yes=True)

        err = capsys.readouterr().err
        assert "capped to 8" in err and "F075" in err

    def test_zero_cycles_is_refused(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        with pytest.raises(SystemExit) as exc:
            job_cmd._cmd_job_run_cycles("abc12345", cycles=0)
        assert exc.value.code == 2

    def test_multi_cycle_path_runs_the_loop_after_the_gate(self, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd
        from packages.orchestration.storage import save_job
        from packages.providers.ollama_builder import provider as provider_mod

        monkeypatch.setattr(lre, "CYCLE_SAFETY_CAP", 5)
        monkeypatch.setattr(provider_mod, "OllamaBuilder", FakeBuilder)

        job = make_job(2)
        save_job(job)
        job_cmd._cmd_job_run_cycles(str(job.id), cycles=3, yes=True)

        out = capsys.readouterr().out
        assert "cycles=2/3" in out
        assert f"terminal={TERMINAL_ALL_GREEN}" in out
        assert len(read_cycle_records(str(job.id))) == 2

    def test_a_capped_config_value_names_the_config_key(self, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd

        from packages.orchestration.storage import save_job
        from packages.providers.ollama_builder import provider as provider_mod

        monkeypatch.setattr(provider_mod, "OllamaBuilder", FakeBuilder)
        monkeypatch.setenv("REMEDY_CYCLES_MAX_CYCLES", "20")
        from packages.orchestration.config import reset_config
        reset_config()
        job = make_job(2)
        save_job(job)
        try:
            job_cmd._cmd_job_run_cycles(str(job.id), yes=True)
        finally:
            reset_config()
        err = capsys.readouterr().err
        assert "cycles.max_cycles 20 capped to 8" in err

    def test_declining_the_cost_preview_returns_without_running(self, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr(
            "apps.cli.cost_preview_confirm.confirm_cost_preview", lambda *a, **k: False)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)
        job_cmd._cmd_job_run_cycles("abc12345")
        assert ran == []
        assert "Cancelled" in capsys.readouterr().out

    def test_the_gate_sees_an_unavailable_estimate_and_yes_or_unattended(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        seen: dict = {}

        def fake_confirm(estimate, *, confirm_above_usd, yes, command_name):
            seen["estimate"] = estimate
            seen["yes"] = yes
            seen["command_name"] = command_name
            return True

        monkeypatch.setattr("apps.cli.cost_preview_confirm.confirm_cost_preview", fake_confirm)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)
        job_cmd._cmd_job_run_cycles("abc12345", unattended=True)
        assert seen["estimate"].band_usd_high is None
        assert seen["yes"] is True
        assert seen["command_name"] == "job.run"
        assert ran == ["abc12345"]


# ---------------------------------------------------------------------------
# F050 — DAG scheduling in the loop (T002)
# ---------------------------------------------------------------------------


def make_diamond_job(name: str = "diamond-job") -> Job:
    """A -> (B, C) -> D, expressed the way ``map_flight_plan_to_tasks`` does.

    Plan order puts B before C, so a scheduler that just took the first PENDING
    task would pick the blocked branch and never reach C — which is exactly the
    behavior F050 replaces.
    """
    def task(planned_id: str, *depends_on: str) -> Task:
        return Task(
            description=f"task {planned_id}",
            inputs={
                "task_type": "documentation",
                "flight": {"planned_id": planned_id,
                           "title": planned_id,
                           "depends_on": list(depends_on)},
            },
        )

    return Job(
        name=name,
        user_prompt="build the thing",
        tasks=[task("A"), task("B", "A"), task("C", "A"), task("D", "B", "C")],
        state=RunState.PLANNED,
    )


def planned_id_of(job: Job, task_id) -> str:
    for task in job.tasks:
        if str(task.id) == str(task_id):
            return task.inputs["flight"]["planned_id"]
    raise AssertionError(f"no task {task_id} in this job")


def task_by_planned_id(job: Job, planned_id: str) -> Task:
    for task in job.tasks:
        if task.inputs.get("flight", {}).get("planned_id") == planned_id:
            return task
    raise AssertionError(f"no task {planned_id} in this job")


class SteeredStep:
    """A step that runs the task the ready set selected, failing named ones.

    Declaring ``task_id`` is what makes the conductor offer the target; a step
    without it keeps the pre-F050 "first PENDING" behavior.  A forced failure
    mirrors the real task runner: the task is rolled back to PENDING.
    """

    def __init__(self, *fail_planned_ids: str) -> None:
        self.fail = set(fail_planned_ids)
        self.executed: list[str] = []

    def __call__(self, job: Job, provider_call, task_id=None) -> TaskAttempt:
        if task_id is not None:
            task = next((t for t in job.tasks if t.id == task_id), None)
        else:
            task = next((t for t in job.tasks
                         if t.status == RunState.PENDING), None)
        if task is None:
            return TaskAttempt()

        planned_id = task.inputs["flight"]["planned_id"]
        provider_call(
            TaskExecutionContext(
                job_id=job.id,
                job_prompt=job.user_prompt,
                task_id=task.id,
                task_type=task.inputs.get("task_type", "unknown"),
                task_description=task.description,
            )
        )
        self.executed.append(planned_id)
        if planned_id in self.fail:
            task.status = RunState.PENDING          # the runner's rollback
            return TaskAttempt(task_id=task.id, executed=True, verified=False,
                               error=f"verification_failed: {planned_id}")
        task.status = RunState.COMPLETED
        if all(t.status == RunState.COMPLETED for t in job.tasks):
            job.state = RunState.COMPLETED
        return TaskAttempt(task_id=task.id, executed=True, verified=True)


def run_diamond(control_root: Path, *fail: str, batch_size: int = 1):
    job = make_diamond_job()
    step = SteeredStep(*fail)
    result = run_cycles(
        job, CycleLimits(max_cycles=10, batch_size=batch_size), FakeProvider(),
        task_step=step, verify=passing_verify, clock=FakeClock(),
        save=no_save, control_root_path=control_root,
    )
    return job, step, result


class TestDagScheduling:
    def test_both_branches_open_once_the_root_completes(self, control_root):
        job, step, result = run_diamond(control_root, batch_size=1)
        assert result.terminal_status == TERMINAL_ALL_GREEN
        # A first, then the two branches in plan order, then the join.
        assert step.executed == ["A", "B", "C", "D"]
        assert all(t.status == RunState.COMPLETED for t in job.tasks)

    def test_a_blocked_branch_does_not_block_the_independent_one(self, control_root):
        job, step, result = run_diamond(control_root, "B", batch_size=1)

        # B failed; C is independent of B and must still complete.
        assert step.executed == ["A", "B", "C"]
        assert task_by_planned_id(job, "C").status == RunState.COMPLETED
        # D depends on B, so it is never attempted at all.
        assert "D" not in step.executed
        assert task_by_planned_id(job, "D").status == RunState.PENDING
        assert result.terminal_status == TERMINAL_BLOCKED

    def test_the_skipped_downstream_is_named_in_the_cycle_evidence(self, control_root):
        job, _, result = run_diamond(control_root, "B", batch_size=1)

        last = result.cycles[-1]
        skipped = [planned_id_of(job, t) for t in last.skipped_blocked_task_ids]
        # Exactly the join — not C, which ran, and not B, which is blocked for
        # its own reason rather than skipped.
        assert skipped == ["D"]
        assert last.to_json()["skipped_blocked_task_ids"] == list(
            last.skipped_blocked_task_ids)

    def test_the_terminal_reason_says_nothing_was_ready(self, control_root):
        _, _, result = run_diamond(control_root, "B", batch_size=1)
        assert result.terminal_status == TERMINAL_BLOCKED
        assert "no_ready_tasks" in result.stop_reason

    def test_a_blocked_leaf_blocks_nothing(self, control_root):
        job, step, result = run_diamond(control_root, "D", batch_size=1)
        # Everything upstream of the failed join still completes.
        assert step.executed == ["A", "B", "C", "D"]
        for planned_id in ("A", "B", "C"):
            assert task_by_planned_id(job, planned_id).status == RunState.COMPLETED
        assert result.cycles[-1].skipped_blocked_task_ids == ()
        assert result.terminal_status == TERMINAL_BLOCKED

    def test_the_ready_set_is_recomputed_after_every_task_end(self, control_root):
        # batch_size 4 with a diamond: only A is ready when the cycle starts.
        # B, C and D can only run in this same cycle if the ready set is
        # recomputed after each task end rather than once per batch.
        job, step, result = run_diamond(control_root, batch_size=4)
        assert result.cycles_run == 1
        assert step.executed == ["A", "B", "C", "D"]
        assert result.cycles[0].tasks_attempted == 4
        assert result.terminal_status == TERMINAL_ALL_GREEN

    def test_recomputation_is_visible_to_a_counting_stub(self, control_root,
                                                         monkeypatch):
        calls: list[int] = []
        real_ready_tasks = lre.ready_tasks

        def counting_ready_tasks(job, batch_size, **kwargs):
            calls.append(len(calls))
            return real_ready_tasks(job, batch_size, **kwargs)

        monkeypatch.setattr(lre, "ready_tasks", counting_ready_tasks)
        _, step, result = run_diamond(control_root, batch_size=4)

        assert step.executed == ["A", "B", "C", "D"]
        # One batch-boundary call, then one per task end inside the cycle: the
        # selection point is consulted more often than once per cycle.
        assert len(calls) > result.cycles_run

    def test_two_runs_of_the_same_fixture_schedule_identically(self, control_root):
        first_job, first_step, first = run_diamond(control_root, "B", batch_size=1)
        second_job, second_step, second = run_diamond(control_root, "B", batch_size=1)

        assert first_step.executed == second_step.executed
        assert first.terminal_status == second.terminal_status
        assert first.cycles_run == second.cycles_run
        as_planned = lambda job, record: [                      # noqa: E731
            planned_id_of(job, t) for t in record.executed_task_ids]
        assert [as_planned(first_job, r) for r in first.cycles] == \
               [as_planned(second_job, r) for r in second.cycles]
        assert [[planned_id_of(first_job, t) for t in r.skipped_blocked_task_ids]
                for r in first.cycles] == \
               [[planned_id_of(second_job, t) for t in r.skipped_blocked_task_ids]
                for r in second.cycles]

    def test_a_step_without_a_target_parameter_still_works(self, control_root):
        # The pre-F050 seam: ``completing_step`` takes (job, provider_call) and
        # picks the first PENDING task itself.  It must keep running unchanged.
        job = make_diamond_job()
        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.terminal_status == TERMINAL_ALL_GREEN
        assert all(t.status == RunState.COMPLETED for t in job.tasks)


class TestLinearPlansAreUnchanged:
    def test_a_legacy_plan_runs_one_task_per_cycle_at_batch_size_one(
            self, control_root):
        job = make_job(3)
        result = run_cycles(
            job, CycleLimits(max_cycles=5, batch_size=1), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.cycles_run == 3
        assert result.terminal_status == TERMINAL_ALL_GREEN
        assert [r.tasks_attempted for r in result.cycles] == [1, 1, 1]

    def test_a_legacy_plan_fills_one_cycle_when_the_batch_allows(self, control_root):
        job = make_job(3)
        result = run_cycles(
            job, CycleLimits(max_cycles=5, batch_size=3), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.cycles_run == 1
        assert result.cycles[0].tasks_attempted == 3
        assert result.terminal_status == TERMINAL_ALL_GREEN

    def test_a_legacy_plan_never_reports_a_skipped_downstream(self, control_root):
        job = make_job(3)
        result = run_cycles(
            job, CycleLimits(max_cycles=5, batch_size=1), FakeProvider(),
            task_step=completing_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert all(r.skipped_blocked_task_ids == () for r in result.cycles)

    def test_a_failed_legacy_task_blocks_its_successors(self, control_root):
        job = make_job(3)
        failing_ids = {job.tasks[1].id}

        def step(job_: Job, provider_call) -> TaskAttempt:
            task = next((t for t in job_.tasks
                         if t.status == RunState.PENDING), None)
            if task is None:
                return TaskAttempt()
            if task.id in failing_ids:
                return TaskAttempt(task_id=task.id, executed=True,
                                   verified=False, error="boom")
            task.status = RunState.COMPLETED
            return TaskAttempt(task_id=task.id, executed=True, verified=True)

        result = run_cycles(
            job, CycleLimits(max_cycles=5, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )
        # Task 2 failed, so task 3 (its successor in the legacy chain) is
        # skipped-blocked rather than run out of order.
        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.cycles[-1].skipped_blocked_task_ids == (str(job.tasks[2].id),)
        assert job.tasks[2].status == RunState.PENDING


# ---------------------------------------------------------------------------
# F075 R-0187 — the cycles experiment vehicle
# ---------------------------------------------------------------------------
#
# The F075 gate cannot demonstrate ten flawless multi-cycle missions while
# every job is wedged at one cycle, and raising the DEFAULT is the job of the
# human-applied ADR a passing 10/10 produces. So the campaign gets an explicit,
# loudly-named override and the shipped F046 safety is left exactly as it is.
# Both directions are pinned here: what the override may do, and what config
# and flag still may NOT do.


class TestTheCyclesExperimentOverride:

    def test_a_flag_over_the_cap_is_still_clamped(self):
        from packages.orchestration.long_run_executor import (
            CYCLE_SAFETY_CAP,
            resolve_max_cycles,
        )
        resolved = resolve_max_cycles(99)
        assert resolved.max_cycles == CYCLE_SAFETY_CAP
        assert resolved.capped is True
        assert resolved.source == "flag"

    def test_a_config_value_over_the_cap_is_still_clamped(self):
        from packages.orchestration.long_run_executor import (
            CYCLE_SAFETY_CAP,
            resolve_max_cycles,
        )
        resolved = resolve_max_cycles(None, 99)
        assert resolved.max_cycles == CYCLE_SAFETY_CAP
        assert resolved.capped is True
        assert resolved.source == "config"

    def test_the_override_may_exceed_the_cap(self):
        from packages.orchestration.long_run_executor import resolve_max_cycles

        resolved = resolve_max_cycles(experiment_max_cycles=12)
        assert resolved.max_cycles == 12
        assert resolved.source == "experiment"
        assert resolved.capped is False

    def test_the_override_beats_a_flag_and_a_config_value(self):
        from packages.orchestration.long_run_executor import resolve_max_cycles

        resolved = resolve_max_cycles(3, 4, experiment_max_cycles=6)
        assert (resolved.max_cycles, resolved.source) == (6, "experiment")

    def test_without_the_override_nothing_changes(self):
        from packages.orchestration.long_run_executor import (
            DEFAULT_MAX_CYCLES,
            resolve_max_cycles,
        )
        resolved = resolve_max_cycles()
        assert resolved.max_cycles == DEFAULT_MAX_CYCLES
        assert resolved.source == "default"
        assert resolved.capped is False

    def test_the_override_still_refuses_a_nonsense_value(self):
        from packages.orchestration.long_run_executor import resolve_max_cycles

        with pytest.raises(ValueError, match="max_cycles must be >= 1"):
            resolve_max_cycles(experiment_max_cycles=0)

    def test_an_over_cap_run_is_recorded_as_over_cap(self):
        """No run may exceed the rollout cap silently — it is a fact on disk."""
        from packages.orchestration.long_run_executor import resolve_max_cycles

        body = resolve_max_cycles(experiment_max_cycles=12).to_json()
        assert body["over_cap"] is True
        assert body["source"] == "experiment"
        assert body["cap"] == 8 and body["max_cycles"] == 12

    def test_a_capped_run_is_not_recorded_as_over_cap(self):
        from packages.orchestration.long_run_executor import resolve_max_cycles

        body = resolve_max_cycles(99).to_json()
        assert body["over_cap"] is False
        assert body["capped"] is True and body["requested"] == 99

    def test_limits_from_config_passes_the_override_through(self):
        from packages.orchestration.long_run_executor import limits_from_config

        class _Config:
            def get(self, key):
                return None

        limits, resolved = limits_from_config(_Config(), experiment_max_cycles=5)
        assert limits.max_cycles == 5
        assert resolved.source == "experiment"

    def test_limits_from_config_without_the_override_still_clamps(self):
        from packages.orchestration.long_run_executor import (
            CYCLE_SAFETY_CAP,
            CONFIG_KEY_MAX_CYCLES,
            limits_from_config,
        )

        class _Config:
            def get(self, key):
                return 99 if key == CONFIG_KEY_MAX_CYCLES else None

        limits, resolved = limits_from_config(_Config())
        assert limits.max_cycles == CYCLE_SAFETY_CAP
        assert resolved.capped is True
