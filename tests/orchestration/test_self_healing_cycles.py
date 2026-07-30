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
from packages.orchestration.config import get_key_spec
from packages.orchestration.long_run_executor import (
    DEFAULT_REPAIR_ROUNDS,
    VERIFY_CONFIG_ERROR,
    VERIFY_FAILED,
    VERIFY_NOT_RUN,
    VERIFY_PASSED,
    VERIFY_UNKNOWN_ERROR,
    CycleLimits,
    RepairOutcome,
    RepairPhase,
    TaskAttempt,
    VerifyOutcome,
    as_verify_outcome,
    build_cycle_repair_findings,
    cycle_verify_failure_class,
    limits_from_config,
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


# ---------------------------------------------------------------------------
# What a repair round is given, and how many it may have
# ---------------------------------------------------------------------------


class TestRepairFindingsPayload:
    def test_the_payload_carries_ids_tail_and_changed_files(self):
        job = make_job(1)
        outcome = VerifyOutcome(
            result=VERIFY_FAILED, output="E   assert 4 == 5",
            failing_test_ids=("tests/test_calc.py::test_add",),
            changed_files=("calc.py",),
        )
        findings = build_cycle_repair_findings(job, 3, outcome, round_number=2)

        assert findings["failing_test_ids"] == ["tests/test_calc.py::test_add"]
        assert findings["failure_tail"] == "E   assert 4 == 5"
        assert findings["changed_files"] == ["calc.py"]
        assert findings["cycle_index"] == 3
        assert findings["repair_round"] == 2
        assert findings["source"] == "cycle_verify"

    def test_the_payload_is_the_existing_repair_context_shape(self):
        """Not a second findings vocabulary — the one the repair loop consumes."""
        job = make_job(1)
        findings = build_cycle_repair_findings(
            job, 1, VerifyOutcome(result=VERIFY_FAILED))
        assert findings["version"] == 1
        assert findings["job_id"] == str(job.id)
        assert findings["failure_kind"] == "assertion"
        assert findings["status"] == "failed"
        assert "safe_summary" in findings

    def test_executed_task_ids_are_the_hint_when_the_step_named_no_files(self):
        job = make_job(1)
        findings = build_cycle_repair_findings(
            job, 1, VerifyOutcome(result=VERIFY_FAILED),
            executed_task_ids=("task-1",))
        assert findings["changed_files"] == ["task-1"]


class TestRepairOutcome:
    def test_a_round_defaults_to_not_having_run(self):
        """Nothing is claimed about a round nobody reported."""
        assert RepairOutcome().ran is False
        assert RepairOutcome().changed_files == ()


class TestRepairPhaseSummary:
    def test_no_rounds_says_nothing_at_all(self):
        assert RepairPhase(outcome=VerifyOutcome(result=VERIFY_FAILED)).summary == ""

    def test_one_round_that_healed(self):
        phase = RepairPhase(outcome=VerifyOutcome(result=VERIFY_PASSED),
                            rounds_used=1, healed=True)
        assert phase.summary == "healed after 1 repair round"

    def test_two_rounds_that_did_not_heal(self):
        phase = RepairPhase(outcome=VerifyOutcome(result=VERIFY_FAILED),
                            rounds_used=2)
        assert phase.summary == "not healed after 2 repair rounds"

    def test_a_heal_that_changed_nothing_is_a_flake_suspect(self):
        """A9: a test that starts passing on its own has to be visible."""
        phase = RepairPhase(outcome=VerifyOutcome(result=VERIFY_PASSED),
                            rounds_used=1, healed=True,
                            healed_without_changes=True)
        assert phase.summary == "healed without changes (flaky?) after 1 repair round"


class TestRepairRoundCap:
    def test_the_config_key_exists_with_default_two(self):
        spec = get_key_spec("cycles.repair_rounds")
        assert spec is not None
        assert spec.default == 2
        assert spec.value_type is int
        assert DEFAULT_REPAIR_ROUNDS == 2

    def test_limits_read_the_cap_from_config(self):
        class Cfg:
            def get(self, key):
                return {"cycles.max_cycles": 1, "cycles.batch_size": 1,
                        "cycles.verify_command": None,
                        "cycles.repair_rounds": 5}.get(key)

        limits, _ = limits_from_config(Cfg())
        assert limits.repair_rounds == 5

    def test_a_missing_config_value_falls_back_to_the_default(self):
        class Cfg:
            def get(self, key):
                return {"cycles.max_cycles": 1, "cycles.batch_size": 1}.get(key)

        limits, _ = limits_from_config(Cfg())
        assert limits.repair_rounds == DEFAULT_REPAIR_ROUNDS

    def test_hand_built_limits_do_not_self_heal_by_accident(self):
        """A caller that named its own bounds never spends calls it did not ask for."""
        assert CycleLimits().repair_rounds == 0

    def test_a_negative_cap_is_refused(self):
        with pytest.raises(ValueError, match="repair_rounds must be >= 0"):
            CycleLimits(repair_rounds=-1)


class TestRepairSummaryIsRendered:
    def test_the_rendered_line_names_the_repair_phase(self):
        record = lre.CycleRecord(
            cycle_index=1, tasks_attempted=1, tasks_completed=1, tasks_failed=0,
            verify_result=VERIFY_PASSED, tokens_so_far=0, started_at="",
            ended_at="", repair_rounds_used=1, healed_after_repair=True,
            repair_summary="healed after 1 repair round",
        )
        line = render_cycle_summary_line(record)
        assert "healed after 1 repair round" in line
        assert "cycle 1" in line

    def test_the_record_serializes_the_repair_phase(self):
        payload = lre.CycleRecord(
            cycle_index=1, tasks_attempted=1, tasks_completed=1, tasks_failed=0,
            verify_result=VERIFY_PASSED, tokens_so_far=0, started_at="",
            ended_at="", repair_rounds_used=2, healed_after_repair=True,
            healed_without_changes=True,
            repair_summary="healed without changes (flaky?) after 2 repair rounds",
        ).to_json()
        assert payload["repair_rounds_used"] == 2
        assert payload["healed_after_repair"] is True
        assert payload["healed_without_changes"] is True
        assert "flaky?" in payload["repair_summary"]
