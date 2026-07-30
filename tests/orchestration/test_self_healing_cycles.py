"""F052 — self-healing test rounds.

A cycle whose verify step fails spends up to ``cycles.repair_rounds`` bounded
repair rounds through the EXISTING repair loop before the cycle keeps its
failure.  This file pins that contract.

First, the part every later step stands on: a failed verify has to say WHAT
failed.  A bare ``"failed"`` cannot be repaired (there is nothing to hand a
repair round) and cannot be reported honestly (a missing test command and a
broken assertion read identically).  So the verify seam may return a
``VerifyOutcome``, the failure is classified through the EXISTING classifier,
and the cycle renders that class where a human sees it.

Nothing here sleeps and nothing here calls a provider.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import packages.orchestration.long_run_executor as lre
from packages.core.models import Job, RunState, Task
from packages.orchestration.builder_models import TaskExecutionContext
from packages.orchestration.long_run_executor import (
    VERIFY_CONFIG_ERROR,
    VERIFY_FAILED,
    VERIFY_NOT_RUN,
    VERIFY_PASSED,
    VERIFY_UNKNOWN_ERROR,
    CycleLimits,
    TaskAttempt,
    VerifyOutcome,
    as_verify_outcome,
    cycle_verify_failure_class,
    read_cycle_records,
    render_cycle_summary_line,
    run_cycles,
)

UTC = timezone.utc
T0 = datetime(2026, 7, 30, 9, 0, 0, tzinfo=UTC)


# ---------------------------------------------------------------------------
# Fixtures and fakes
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Every cycle writes evidence — no test may reach the real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def control_root(tmp_path: Path) -> Path:
    root = tmp_path / "control"
    root.mkdir()
    return root


def make_job(task_count: int = 1) -> Job:
    return Job(
        name="healing-job",
        user_prompt="build the thing",
        tasks=[
            Task(description=f"task {i}", inputs={"task_type": "documentation"})
            for i in range(task_count)
        ],
        state=RunState.PLANNED,
    )


class FakeClock:
    def __init__(self, start: datetime = T0,
                 step: timedelta = timedelta(seconds=1)) -> None:
        self.now = start
        self.step = step

    def __call__(self) -> datetime:
        current = self.now
        self.now = self.now + self.step
        return current


def completing_step(job: Job, provider_call) -> TaskAttempt:
    """Completes the first PENDING task, through the provider seam."""
    task = next((t for t in job.tasks if t.status == RunState.PENDING), None)
    if task is None:
        return TaskAttempt()
    provider_call(TaskExecutionContext(
        job_id=job.id,
        job_prompt=job.user_prompt,
        task_id=task.id,
        task_type=task.inputs.get("task_type", "unknown"),
        task_description=task.description,
    ))
    task.status = RunState.COMPLETED
    if all(t.status == RunState.COMPLETED for t in job.tasks):
        job.state = RunState.COMPLETED
    return TaskAttempt(task_id=task.id, executed=True, verified=True)


def no_save(job: Job) -> None:
    return None


# ---------------------------------------------------------------------------
# The verify seam may say more than pass/fail
# ---------------------------------------------------------------------------


class TestVerifyOutcome:
    def test_a_bare_string_normalizes_to_an_outcome(self):
        outcome = as_verify_outcome(VERIFY_FAILED)
        assert outcome.result == VERIFY_FAILED
        assert outcome.output == ""
        assert outcome.failing_test_ids == ()
        assert outcome.changed_files == ()

    def test_an_outcome_passes_through_unchanged(self):
        original = VerifyOutcome(result=VERIFY_FAILED, output="E   assert 4 == 5",
                                 failing_test_ids=("tests/test_calc.py::test_add",))
        assert as_verify_outcome(original) is original

    def test_a_pre_f052_verify_step_still_drives_the_loop(self, control_root):
        """Every verify step written before F052 returns a plain string."""
        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=1), lambda _ctx: None,
            task_step=completing_step, verify=lambda j, i, c: VERIFY_FAILED,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.cycles[0].verify_result == VERIFY_FAILED
        assert "verify_failed" in result.cycles[0].errors

    def test_a_rich_verify_step_drives_the_loop_the_same_way(self, control_root):
        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=1), lambda _ctx: None,
            task_step=completing_step,
            verify=lambda j, i, c: VerifyOutcome(
                result=VERIFY_FAILED, output="E   assert 4 == 5",
                failing_test_ids=("tests/test_calc.py::test_add",)),
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.cycles[0].verify_result == VERIFY_FAILED
        assert "verify_failed" in result.cycles[0].errors


# ---------------------------------------------------------------------------
# A failed verify is classified, not just flagged
# ---------------------------------------------------------------------------


class TestVerifyFailureClassification:
    def test_a_failing_test_is_the_classifier_s_test_failed(self):
        assert cycle_verify_failure_class(VERIFY_FAILED) == "test_failed"

    def test_a_harness_problem_is_config_not_a_test_failure(self):
        """A9: a missing command or a bad config is not something a patch fixes."""
        assert cycle_verify_failure_class(VERIFY_CONFIG_ERROR) == "config"

    def test_an_unrecognized_outcome_is_honestly_unknown(self):
        assert cycle_verify_failure_class(VERIFY_UNKNOWN_ERROR) == "unknown"
        assert cycle_verify_failure_class("something nobody mapped") == "unknown"

    def test_a_passing_or_never_run_verify_has_no_failure_class(self):
        assert cycle_verify_failure_class(VERIFY_PASSED) == ""
        assert cycle_verify_failure_class(VERIFY_NOT_RUN) == ""
        assert cycle_verify_failure_class("") == ""

    def test_the_harness_outcomes_deny_the_job_all_green(self):
        assert lre._is_green(make_job(0), VERIFY_CONFIG_ERROR) is False
        job = make_job(1)
        job.tasks[0].status = RunState.COMPLETED
        assert lre._is_green(job, VERIFY_CONFIG_ERROR) is False
        assert lre._is_green(job, VERIFY_UNKNOWN_ERROR) is False
        assert lre._is_green(job, VERIFY_PASSED) is True

    def test_the_cycle_record_carries_the_class(self, control_root):
        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=1), lambda _ctx: None,
            task_step=completing_step,
            verify=lambda j, i, c: VERIFY_CONFIG_ERROR,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
            record_checkpoint=False,
        )
        assert result.cycles[0].verify_failure_class == "config"
        assert read_cycle_records(str(job.id))[0]["verify_failure_class"] == "config"

    def test_a_green_cycle_records_no_class(self, control_root):
        job = make_job(1)
        result = run_cycles(
            job, CycleLimits(max_cycles=1), lambda _ctx: None,
            task_step=completing_step, verify=lambda j, i, c: VERIFY_PASSED,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )
        assert result.cycles[0].verify_failure_class == ""


# ---------------------------------------------------------------------------
# What a human sees
# ---------------------------------------------------------------------------


class TestCycleSummaryRendering:
    def _record(self, **kw) -> lre.CycleRecord:
        base = dict(cycle_index=1, tasks_attempted=1, tasks_completed=1,
                    tasks_failed=0, verify_result=VERIFY_PASSED, tokens_so_far=0,
                    started_at="", ended_at="")
        base.update(kw)
        return lre.CycleRecord(**base)

    def test_a_green_cycle_renders_without_a_failure_class(self):
        line = render_cycle_summary_line(self._record())
        assert line == "cycle 1: verify=passed tasks=1/1"

    def test_a_harness_failure_names_its_class_on_the_line(self):
        line = render_cycle_summary_line(self._record(
            verify_result=VERIFY_CONFIG_ERROR, verify_failure_class="config",
            tasks_completed=0))
        assert "verify=config" in line
        assert "failure_class=config" in line

    def test_a_test_failure_names_its_class_on_the_line(self):
        line = render_cycle_summary_line(self._record(
            verify_result=VERIFY_FAILED, verify_failure_class="test_failed"))
        assert "failure_class=test_failed" in line
