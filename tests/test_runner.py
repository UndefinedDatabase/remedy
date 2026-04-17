"""
Tests for plan_job() orchestration runner.
"""

from __future__ import annotations

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.job_runner import plan_job


# ---------------------------------------------------------------------------
# plan_job: basic behavior
# ---------------------------------------------------------------------------

def test_plan_job_adds_three_tasks():
    job = Job(name="test", user_prompt="build something")
    result = plan_job(job)
    assert len(result.tasks) == 3


def test_plan_job_adds_one_artifact():
    job = Job(name="test", user_prompt="build something")
    result = plan_job(job)
    assert len(result.artifacts) == 1


def test_plan_job_artifact_name():
    job = Job(name="test")
    result = plan_job(job)
    assert result.artifacts[0].name == "planning_output"


def test_plan_job_artifact_contains_job_id():
    job = Job(name="test", user_prompt="do the thing")
    result = plan_job(job)
    assert str(job.id) in result.artifacts[0].content


def test_plan_job_tasks_are_pending():
    job = Job(name="test")
    result = plan_job(job)
    assert all(t.status == RunState.PENDING for t in result.tasks)


def test_plan_job_task_types_present():
    job = Job(name="test")
    result = plan_job(job)
    task_types = {t.inputs.get("task_type") for t in result.tasks}
    assert "analyze_requirements" in task_types
    assert "define_acceptance_checks" in task_types
    assert "prepare_implementation_plan" in task_types


def test_plan_job_state_after_planning():
    job = Job(name="test")
    assert job.state == RunState.PENDING
    result = plan_job(job)
    # After planning, job is PENDING (tasks ready, not yet executing)
    assert result.state == RunState.PENDING


# ---------------------------------------------------------------------------
# plan_job: idempotency
# ---------------------------------------------------------------------------

def test_plan_job_is_idempotent_tasks():
    job = Job(name="test")
    plan_job(job)
    task_ids_first = [t.id for t in job.tasks]

    plan_job(job)
    task_ids_second = [t.id for t in job.tasks]

    assert task_ids_first == task_ids_second
    assert len(job.tasks) == 3


def test_plan_job_is_idempotent_artifacts():
    job = Job(name="test")
    plan_job(job)
    artifact_ids_first = [a.id for a in job.artifacts]

    plan_job(job)
    artifact_ids_second = [a.id for a in job.artifacts]

    assert artifact_ids_first == artifact_ids_second
    assert len(job.artifacts) == 1


def test_plan_job_returns_unchanged_if_already_has_tasks():
    job = Job(name="test")
    existing_task = Task(description="pre-existing")
    job.tasks = [existing_task]

    result = plan_job(job)

    assert len(result.tasks) == 1
    assert result.tasks[0].id == existing_task.id


def test_plan_job_returns_unchanged_if_already_has_artifacts():
    job = Job(name="test")
    existing = Artifact(name="pre-existing", content="x")
    job.artifacts = [existing]

    result = plan_job(job)

    assert len(result.artifacts) == 1
    assert result.artifacts[0].id == existing.id
