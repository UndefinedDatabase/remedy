"""
Tests for run_next_task() and annotate_task_result().

All tests use a stub builder callable — no live Ollama server required.
"""

from __future__ import annotations

from uuid import UUID

import pytest

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.task_runner import RunTaskResult, annotate_task_result, run_next_task


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
    """prior_task_summaries collected from already-completed tasks in order."""
    received: list[TaskExecutionContext] = []
    call_count = 0

    def capturing_builder(ctx: TaskExecutionContext) -> BuilderOutput:
        received.append(ctx)
        nonlocal call_count
        call_count += 1
        return BuilderOutput(summary=f"done task {call_count}", proposed_changes=["x"])

    job = _make_job(3)
    # Execute task 0 and task 1; capture context on task 2
    run_next_task(job, capturing_builder)  # task 0
    run_next_task(job, capturing_builder)  # task 1
    run_next_task(job, capturing_builder)  # task 2 — receives summaries from 0 and 1

    ctx_task2 = received[2]
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
# State transitions
# ---------------------------------------------------------------------------

def test_task_marked_completed():
    job = _make_job(3)
    run_next_task(job, _stub_builder)
    assert job.tasks[0].status == RunState.COMPLETED
    assert job.tasks[1].status == RunState.PENDING
    assert job.tasks[2].status == RunState.PENDING


def test_job_running_while_tasks_remain():
    job = _make_job(3)
    run_next_task(job, _stub_builder)
    assert job.state == RunState.RUNNING


def test_job_completed_when_all_tasks_done():
    job = _make_job(1)
    run_next_task(job, _stub_builder)
    assert job.state == RunState.COMPLETED


def test_sequential_execution_advances_through_tasks():
    job = _make_job(3)
    r1 = run_next_task(job, _stub_builder)
    assert r1.task_id == job.tasks[0].id
    r2 = run_next_task(job, _stub_builder)
    assert r2.task_id == job.tasks[1].id
    r3 = run_next_task(job, _stub_builder)
    assert r3.task_id == job.tasks[2].id
    assert job.state == RunState.COMPLETED


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
