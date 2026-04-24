"""
Tests for run_next_task() and annotate_task_result().

All tests use a stub builder callable — no live Ollama server required.
"""

from __future__ import annotations

from uuid import UUID

import pytest

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.task_runner import (
    RunTaskResult,
    annotate_task_result,
    finalize_task,
    run_next_task,
)
from packages.orchestration.verifier import VerificationCheckResult, VerificationResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_job(n_tasks: int = 3, state: RunState = RunState.PLANNED) -> Job:
    tasks = [
        Task(description=f"Task {i}", inputs={"task_type": f"type_{i}"})
        for i in range(n_tasks)
    ]
    return Job(name="test-job", tasks=tasks, state=state)


def _stub_builder(context: TaskExecutionContext) -> BuilderOutput:
    return BuilderOutput(
        summary="Stub output.",
        proposed_changes=["change A", "change B"],
        notes=["note 1"],
        risks=[],
    )


# ---------------------------------------------------------------------------
# Selecting the next pending task
# ---------------------------------------------------------------------------

def test_run_next_task_changed_true():
    job = _make_job(2)
    result = run_next_task(job, _stub_builder)
    assert result.changed is True


def test_run_next_task_executes_first_pending():
    job = _make_job(3)
    first_id = job.tasks[0].id
    result = run_next_task(job, _stub_builder)
    assert result.task_id == first_id


def test_run_next_task_skips_non_pending():
    """If first task is already completed, second task is picked."""
    job = _make_job(3)
    job.tasks[0].status = RunState.COMPLETED
    result = run_next_task(job, _stub_builder)
    assert result.task_id == job.tasks[1].id


# ---------------------------------------------------------------------------
# Execution context passed to provider
# ---------------------------------------------------------------------------

def test_provider_receives_task_execution_context():
    """Builder callable receives a TaskExecutionContext, not a raw string."""
    received: list[TaskExecutionContext] = []

    def capturing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        received.append(ctx)
        return BuilderOutput(summary="ok", proposed_changes=["x"])

    job = _make_job(1)
    job.user_prompt = "build something"
    run_next_task(job, capturing_builder)

    assert len(received) == 1
    ctx = received[0]
    assert isinstance(ctx, TaskExecutionContext)


def test_context_fields_populated_correctly():
    """Context fields match the job and task from which they were built."""
    received: list[TaskExecutionContext] = []

    def capturing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        received.append(ctx)
        return BuilderOutput(summary="ok", proposed_changes=["x"])

    job = _make_job(1)
    job.user_prompt = "do something cool"
    task = job.tasks[0]

    run_next_task(job, capturing_builder)
    ctx = received[0]

    assert ctx.job_id == job.id
    assert ctx.job_prompt == "do something cool"
    assert ctx.task_id == task.id
    assert ctx.task_type == "type_0"
    assert ctx.task_description == "Task 0"


def test_context_includes_planning_summary():
    """planning_summary is extracted from the orchestration-owned planning artifact."""
    received: list[TaskExecutionContext] = []

    def capturing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        received.append(ctx)
        return BuilderOutput(summary="ok", proposed_changes=["x"])

    job = _make_job(1)
    planning_artifact = Artifact(
        name="planning_output",
        content="plan text",
        task_id=None,
        metadata={"summary": "Overall plan summary"},
    )
    job.artifacts.append(planning_artifact)

    run_next_task(job, capturing_builder)
    assert received[0].planning_summary == "Overall plan summary"


def test_context_includes_prior_task_summaries():
    """prior_task_summaries collected from already-completed tasks in order.

    Tasks must reach COMPLETED (via finalize_task) before they appear as prior
    summaries — this matches the Step 7 verifier-gate semantics. The test
    manually sets up completed state to isolate _build_execution_context.
    """
    received: list[TaskExecutionContext] = []

    def capturing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        received.append(ctx)
        return BuilderOutput(summary="done task", proposed_changes=["x"])

    job = _make_job(3)

    # Manually mark tasks 0 and 1 as COMPLETED with artifacts — simulates what
    # finalize_task() would do after a successful build+verify cycle.
    for i in range(2):
        t = job.tasks[i]
        t.status = RunState.COMPLETED
        art = Artifact(
            name=f"task_output_type_{i}",
            content="...",
            task_id=t.id,
            metadata={"task_type": f"type_{i}", "summary": f"done task {i + 1}"},
        )
        job.artifacts.append(art)
        t.output_artifact_ids.append(art.id)

    run_next_task(job, capturing_builder)  # task 2 — receives summaries from 0 and 1

    ctx_task2 = received[0]
    assert len(ctx_task2.prior_task_summaries) == 2
    assert "done task 1" in ctx_task2.prior_task_summaries
    assert "done task 2" in ctx_task2.prior_task_summaries


def test_context_no_planning_summary_when_absent():
    """planning_summary is None when no planning_output artifact exists."""
    received: list[TaskExecutionContext] = []

    def capturing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        received.append(ctx)
        return BuilderOutput(summary="ok", proposed_changes=["x"])

    job = _make_job(1)
    run_next_task(job, capturing_builder)
    assert received[0].planning_summary is None


# ---------------------------------------------------------------------------
# Artifact provenance
# ---------------------------------------------------------------------------

def test_artifact_task_id_matches_executed_task():
    job = _make_job(1)
    task_id = job.tasks[0].id
    run_next_task(job, _stub_builder)
    task_artifacts = [a for a in job.artifacts if a.task_id is not None]
    assert len(task_artifacts) == 1
    assert task_artifacts[0].task_id == task_id


def test_output_artifact_ids_updated():
    job = _make_job(1)
    run_next_task(job, _stub_builder)
    task = job.tasks[0]
    assert len(task.output_artifact_ids) == 1
    assert task.output_artifact_ids[0] == job.artifacts[-1].id


def test_artifact_name_contains_task_type():
    job = _make_job(1)
    run_next_task(job, _stub_builder)
    assert "type_0" in job.artifacts[-1].name


def test_artifact_content_contains_summary():
    job = _make_job(1)
    run_next_task(job, _stub_builder)
    assert "Stub output." in job.artifacts[-1].content


def test_artifact_metadata_has_no_legacy_builder_key():
    """The removed 'builder':'llm' key must not appear in artifact metadata."""
    job = _make_job(1)
    run_next_task(job, _stub_builder)
    artifact = next(a for a in job.artifacts if a.task_id is not None)
    assert "builder" not in artifact.metadata


def test_artifact_metadata_has_task_type_and_summary():
    """Artifact metadata contains task_type and summary before annotation."""
    job = _make_job(1)
    run_next_task(job, _stub_builder)
    artifact = next(a for a in job.artifacts if a.task_id is not None)
    assert artifact.metadata["task_type"] == "type_0"
    assert artifact.metadata["summary"] == "Stub output."


# ---------------------------------------------------------------------------
# State transitions (Step 7: task stays RUNNING until finalize_task)
# ---------------------------------------------------------------------------

def test_task_running_after_run_next_task():
    """Task is RUNNING (not COMPLETED) immediately after run_next_task.

    COMPLETED only arrives after finalize_task() with a passing VerificationResult.
    """
    job = _make_job(3)
    run_next_task(job, _stub_builder)
    assert job.tasks[0].status == RunState.RUNNING
    assert job.tasks[1].status == RunState.PENDING
    assert job.tasks[2].status == RunState.PENDING


def test_job_running_while_tasks_remain():
    job = _make_job(3)
    run_next_task(job, _stub_builder)
    assert job.state == RunState.RUNNING


def test_job_not_completed_until_finalize_task_called():
    """Even if only one task exists, job is not COMPLETED until finalize_task passes."""
    job = _make_job(1)
    run_next_task(job, _stub_builder)
    assert job.state == RunState.RUNNING


def test_sequential_execution_advances_through_tasks():
    """run_next_task always picks the next PENDING task regardless of RUNNING tasks."""
    job = _make_job(3)
    r1 = run_next_task(job, _stub_builder)
    assert r1.task_id == job.tasks[0].id
    r2 = run_next_task(job, _stub_builder)
    assert r2.task_id == job.tasks[1].id
    r3 = run_next_task(job, _stub_builder)
    assert r3.task_id == job.tasks[2].id
    # All three tasks are RUNNING (not COMPLETED); job is RUNNING.
    # finalize_task() must be called on each to advance to COMPLETED.
    assert job.state == RunState.RUNNING


# ---------------------------------------------------------------------------
# Failure rollback
# ---------------------------------------------------------------------------

def test_builder_failure_rolls_task_back_to_pending():
    """On builder failure task must be PENDING, not RUNNING."""
    job = _make_job(1)

    def failing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        raise RuntimeError("provider unavailable")

    with pytest.raises(RuntimeError):
        run_next_task(job, failing_builder)

    assert job.tasks[0].status == RunState.PENDING


def test_builder_failure_restores_job_state():
    """On builder failure job.state is restored to its pre-call value."""
    job = _make_job(2, state=RunState.PLANNED)

    def failing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        raise RuntimeError("provider unavailable")

    with pytest.raises(RuntimeError):
        run_next_task(job, failing_builder)

    assert job.state == RunState.PLANNED


def test_builder_failure_on_partially_executed_job_preserves_running():
    """If job was already RUNNING (some tasks done), state stays RUNNING on failure."""
    job = _make_job(3)
    run_next_task(job, _stub_builder)   # task 0 succeeds; job now RUNNING

    def failing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        raise RuntimeError("transient error")

    with pytest.raises(RuntimeError):
        run_next_task(job, failing_builder)  # task 1 fails

    assert job.state == RunState.RUNNING
    assert job.tasks[1].status == RunState.PENDING


def test_builder_error_propagates():
    job = _make_job(1)

    def bad_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        raise RuntimeError("builder failed")

    with pytest.raises(RuntimeError, match="builder failed"):
        run_next_task(job, bad_builder)


# ---------------------------------------------------------------------------
# No-op when no pending tasks
# ---------------------------------------------------------------------------

def test_no_op_when_no_tasks():
    job = _make_job(0)
    result = run_next_task(job, _stub_builder)
    assert result.changed is False
    assert result.task_id is None


def test_no_op_when_all_completed():
    job = _make_job(2)
    for t in job.tasks:
        t.status = RunState.COMPLETED
    result = run_next_task(job, _stub_builder)
    assert result.changed is False
    assert result.task_id is None


def test_no_op_does_not_add_artifacts():
    job = _make_job(0)
    run_next_task(job, _stub_builder)
    assert len(job.artifacts) == 0


# ---------------------------------------------------------------------------
# annotate_task_result
# ---------------------------------------------------------------------------

def test_annotate_task_result_adds_metadata():
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    annotate_task_result(result, provider="ollama", role="builder", model="m1", elapsed_ms=750.0)
    artifact = next(a for a in job.artifacts if a.task_id == result.task_id)
    assert artifact.metadata["provider"] == "ollama"
    assert artifact.metadata["role"] == "builder"
    assert artifact.metadata["model"] == "m1"
    assert artifact.metadata["elapsed_ms"] == 750


def test_annotate_task_result_no_op_when_not_changed():
    job = _make_job(0)
    result = run_next_task(job, _stub_builder)
    # Should not raise even when task_id is None
    annotate_task_result(result, provider="ollama", role="builder", model="m1", elapsed_ms=100.0)


def test_annotate_task_result_raises_if_changed_but_no_artifact():
    """annotate_task_result must raise RuntimeError if changed=True but artifact is missing."""
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    # Forcibly remove the artifact to simulate the bug condition
    job.artifacts.clear()

    with pytest.raises(RuntimeError, match="no artifact found"):
        annotate_task_result(result, provider="ollama", role="builder", model="m1", elapsed_ms=50.0)


def test_annotate_task_result_finds_by_task_id_not_index():
    """If a planning artifact sits at index 0, annotation still targets the task artifact."""
    job = _make_job(1)
    # Add a fake orchestration-owned artifact at index 0 BEFORE running the task
    orchestration_artifact = Artifact(
        name="planning_output",
        content="plan",
        task_id=None,
        metadata={},
    )
    job.artifacts.insert(0, orchestration_artifact)

    result = run_next_task(job, _stub_builder)
    annotate_task_result(result, provider="ollama", role="builder", model="m1", elapsed_ms=200.0)

    # The orchestration artifact at index 0 must NOT have been annotated
    assert "provider" not in job.artifacts[0].metadata
    # The task artifact must have been annotated
    task_artifact = next(a for a in job.artifacts if a.task_id == result.task_id)
    assert task_artifact.metadata["provider"] == "ollama"


# ---------------------------------------------------------------------------
# finalize_task — Step 7 state finalization
# ---------------------------------------------------------------------------

def _passing_vr(task_id: UUID) -> VerificationResult:
    """Minimal passing VerificationResult for a given task_id."""
    return VerificationResult(
        task_id=task_id,
        passed=True,
        checks=[VerificationCheckResult(check="stub", passed=True, message="OK")],
    )


def _failing_vr(task_id: UUID, reason: str = "stub check") -> VerificationResult:
    """Minimal failing VerificationResult for a given task_id."""
    return VerificationResult(
        task_id=task_id,
        passed=False,
        checks=[VerificationCheckResult(check="stub", passed=False, message=reason)],
    )


def test_finalize_task_marks_completed_when_verified():
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    assert job.tasks[0].status == RunState.RUNNING

    finalize_task(result, _passing_vr(result.task_id))

    assert job.tasks[0].status == RunState.COMPLETED


def test_finalize_task_advances_job_to_completed():
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    assert job.state == RunState.RUNNING

    finalize_task(result, _passing_vr(result.task_id))

    assert job.state == RunState.COMPLETED


def test_finalize_task_does_not_complete_job_while_tasks_remain():
    """Job stays RUNNING if other tasks are still PENDING after finalization."""
    job = _make_job(3)
    result = run_next_task(job, _stub_builder)
    finalize_task(result, _passing_vr(result.task_id))

    assert job.tasks[0].status == RunState.COMPLETED
    assert job.tasks[1].status == RunState.PENDING
    assert job.state == RunState.RUNNING


def test_finalize_task_rolls_back_to_pending_on_failure():
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    assert job.tasks[0].status == RunState.RUNNING

    finalize_task(result, _failing_vr(result.task_id, "workspace_file missing"))

    assert job.tasks[0].status == RunState.PENDING


def test_finalize_task_clears_output_artifact_ids_on_failure():
    """Retry safety: failed artifact ID must not remain in task.output_artifact_ids."""
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    assert len(job.tasks[0].output_artifact_ids) == 1

    finalize_task(result, _failing_vr(result.task_id, "workspace file missing"))

    assert job.tasks[0].output_artifact_ids == []


def test_finalize_task_failed_artifact_remains_in_job_artifacts():
    """Failed artifact is kept in job.artifacts for diagnostics — only the task ref is cleared."""
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    failed_artifact_id = job.tasks[0].output_artifact_ids[0]

    finalize_task(result, _failing_vr(result.task_id, "workspace file missing"))

    # Artifact stays in job.artifacts even though task no longer references it
    assert any(a.id == failed_artifact_id for a in job.artifacts)


def test_finalize_task_records_failure_in_artifact_metadata():
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    finalize_task(result, _failing_vr(result.task_id, "workspace_file missing"))

    artifact = next(a for a in job.artifacts if a.task_id == result.task_id)
    assert artifact.metadata["verification_passed"] is False
    assert any(
        "workspace_file missing" in f for f in artifact.metadata["verification_failures"]
    )


def test_retry_after_failure_uses_new_artifact_not_stale():
    """After a failed verification, the next run_next_task creates a fresh artifact.

    The verifier must check that new artifact, not the stale failed one.
    """
    job = _make_job(1)

    # First attempt: fails verification
    result1 = run_next_task(job, _stub_builder)
    stale_artifact_id = job.tasks[0].output_artifact_ids[0]
    finalize_task(result1, _failing_vr(result1.task_id, "workspace file missing"))

    # Task is PENDING again; output_artifact_ids is empty
    assert job.tasks[0].status == RunState.PENDING
    assert job.tasks[0].output_artifact_ids == []

    # Second attempt: builder runs again
    result2 = run_next_task(job, _stub_builder)
    new_artifact_id = job.tasks[0].output_artifact_ids[0]

    # The new artifact is different from the stale one
    assert new_artifact_id != stale_artifact_id
    # The task now references only the new artifact
    assert len(job.tasks[0].output_artifact_ids) == 1
    assert job.tasks[0].output_artifact_ids[0] == new_artifact_id


def test_consecutive_failures_annotate_each_artifact_separately():
    """Second failure metadata is written to the second artifact, not the first.

    This is the Step 7.6 regression: before the fix, finalize_task scanned by task_id
    after clearing output_artifact_ids and found the first (stale) artifact instead of
    the current attempt's artifact.
    """
    job = _make_job(1)

    # First attempt fails
    result1 = run_next_task(job, _stub_builder)
    artifact1_id = job.tasks[0].output_artifact_ids[0]
    finalize_task(result1, _failing_vr(result1.task_id, "first failure reason"))

    # Second attempt fails
    result2 = run_next_task(job, _stub_builder)
    artifact2_id = job.tasks[0].output_artifact_ids[0]
    assert artifact2_id != artifact1_id
    finalize_task(result2, _failing_vr(result2.task_id, "second failure reason"))

    # artifact1: has metadata from FIRST failure
    artifact1 = next(a for a in job.artifacts if a.id == artifact1_id)
    assert artifact1.metadata["verification_passed"] is False
    assert any("first failure reason" in f for f in artifact1.metadata["verification_failures"])
    # artifact1 must NOT have been overwritten with second failure data
    assert not any("second failure reason" in f for f in artifact1.metadata["verification_failures"])

    # artifact2: has metadata from SECOND failure
    artifact2 = next(a for a in job.artifacts if a.id == artifact2_id)
    assert artifact2.metadata["verification_passed"] is False
    assert any("second failure reason" in f for f in artifact2.metadata["verification_failures"])


def test_consecutive_failures_each_clear_output_artifact_ids():
    """output_artifact_ids is cleared after every failure, not just the first."""
    job = _make_job(1)

    result1 = run_next_task(job, _stub_builder)
    finalize_task(result1, _failing_vr(result1.task_id, "fail 1"))
    assert job.tasks[0].output_artifact_ids == []

    result2 = run_next_task(job, _stub_builder)
    finalize_task(result2, _failing_vr(result2.task_id, "fail 2"))
    assert job.tasks[0].output_artifact_ids == []


def test_consecutive_failures_both_artifacts_preserved_in_job():
    """Both failed artifacts remain in job.artifacts for diagnostics."""
    job = _make_job(1)

    result1 = run_next_task(job, _stub_builder)
    artifact1_id = job.tasks[0].output_artifact_ids[0]
    finalize_task(result1, _failing_vr(result1.task_id, "fail 1"))

    result2 = run_next_task(job, _stub_builder)
    artifact2_id = job.tasks[0].output_artifact_ids[0]
    finalize_task(result2, _failing_vr(result2.task_id, "fail 2"))

    artifact_ids_in_job = {a.id for a in job.artifacts}
    assert artifact1_id in artifact_ids_in_job
    assert artifact2_id in artifact_ids_in_job


def test_finalize_task_no_op_when_not_changed():
    job = _make_job(0)
    result = run_next_task(job, _stub_builder)
    assert result.changed is False
    # Must not raise
    finalize_task(result, _passing_vr(result.task_id or job.id))


def test_finalize_task_raises_if_task_not_in_job():
    """finalize_task raises RuntimeError if result.task_id not found in job.tasks."""
    from uuid import uuid4 as _uuid4

    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    orphan_id = _uuid4()
    vr = _passing_vr(orphan_id)

    # Patch result.task_id to an orphan UUID to trigger the bug guard
    object.__setattr__(result, "task_id", orphan_id)
    with pytest.raises(RuntimeError, match="not found in job.tasks"):
        finalize_task(result, vr)


# ---------------------------------------------------------------------------
# Carry-in: RuntimeError guards for missing artifact state on failure
# ---------------------------------------------------------------------------


def test_finalize_task_raises_if_no_output_artifact_ids_on_failure():
    """Verification failure with empty output_artifact_ids is a bug — must raise."""
    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    # Manually clear output_artifact_ids to simulate the invariant violation
    job.tasks[0].output_artifact_ids.clear()
    with pytest.raises(RuntimeError, match="has no output_artifact_ids"):
        finalize_task(result, _failing_vr(result.task_id, "some failure"))


def test_finalize_task_raises_if_artifact_not_found_in_job_artifacts():
    """Verification failure where artifact ID not in job.artifacts — must raise."""
    from uuid import uuid4 as _uuid4

    job = _make_job(1)
    result = run_next_task(job, _stub_builder)
    # Replace artifact ID in task with a dangling UUID so the lookup fails
    phantom_id = _uuid4()
    job.tasks[0].output_artifact_ids[0] = phantom_id
    with pytest.raises(RuntimeError, match="not found in job.artifacts"):
        finalize_task(result, _failing_vr(result.task_id, "some failure"))
