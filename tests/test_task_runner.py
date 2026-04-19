"""
Tests for run_next_task() and annotate_task_result().

All tests use a stub builder callable — no live Ollama server required.
"""

from __future__ import annotations

from uuid import UUID

import pytest

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput
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


def _stub_builder(prompt: str) -> BuilderOutput:
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
# Error propagation
# ---------------------------------------------------------------------------

def test_builder_error_propagates():
    job = _make_job(1)

    def bad_builder(prompt: str) -> BuilderOutput:
        raise RuntimeError("builder failed")

    with pytest.raises(RuntimeError, match="builder failed"):
        run_next_task(job, bad_builder)


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
    # The task artifact (at index 1) must have been annotated
    task_artifact = next(a for a in job.artifacts if a.task_id == result.task_id)
    assert task_artifact.metadata["provider"] == "ollama"
