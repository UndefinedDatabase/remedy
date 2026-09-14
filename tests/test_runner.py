"""
Tests for plan_job() orchestration runner.
"""

from __future__ import annotations

from packages.core.models import Artifact, RunState
from packages.orchestration.pingpong_job import JobPlan, TaskEntry
from packages.orchestration.job_runner import plan_job

# ---------------------------------------------------------------------------
# plan_job: basic behavior
# ---------------------------------------------------------------------------

def test_plan_job_adds_three_tasks():
    job = JobPlan(job_title="test", user_prompt="build something")
    result = plan_job(job)
    assert len(result.job.tasks) == 3


def test_plan_job_adds_one_artifact():
    job = JobPlan(job_title="test", user_prompt="build something")
    result = plan_job(job)
    assert len(result.job.artifacts) == 1


def test_plan_job_artifact_name():
    job = JobPlan(job_title="test")
    result = plan_job(job)
    assert result.job.artifacts[0].name == "planning_output"


def test_plan_job_artifact_contains_job_id():
    job = JobPlan(job_title="test", user_prompt="do the thing")
    result = plan_job(job)
    assert str(job.job_id) in result.job.artifacts[0].content


def test_plan_job_tasks_are_pending():
    job = JobPlan(job_title="test")
    result = plan_job(job)
    assert all(t.status == RunState.PENDING for t in result.job.tasks)


def test_plan_job_task_types_present():
    job = JobPlan(job_title="test")
    result = plan_job(job)
    task_types = {t.inputs.get("task_type") for t in result.job.tasks}
    assert "analyze_requirements" in task_types
    assert "define_acceptance_checks" in task_types
    assert "prepare_implementation_plan" in task_types


# ---------------------------------------------------------------------------
# plan_job: PLANNED state
# ---------------------------------------------------------------------------

def test_plan_job_state_is_planned_after_planning():
    job = JobPlan(job_title="test")
    assert job.state == RunState.PENDING
    result = plan_job(job)
    assert result.job.state == RunState.PLANNED


def test_planned_state_value():
    assert RunState.PLANNED == "planned"


# ---------------------------------------------------------------------------
# plan_job: PlanJobResult.changed
# ---------------------------------------------------------------------------

def test_plan_job_returns_changed_true_on_first_plan():
    job = JobPlan(job_title="test")
    result = plan_job(job)
    assert result.changed is True


def test_plan_job_returns_changed_false_when_already_planned():
    job = JobPlan(job_title="test")
    plan_job(job)  # first call mutates job in place
    result2 = plan_job(job)
    assert result2.changed is False


# ---------------------------------------------------------------------------
# plan_job: orchestration-owned artifact (task_id=None)
# ---------------------------------------------------------------------------

def test_plan_job_artifact_task_id_is_none():
    """Planning artifacts are orchestration-owned: task_id must be None."""
    job = JobPlan(job_title="test")
    result = plan_job(job)
    assert result.job.artifacts[0].task_id is None


# ---------------------------------------------------------------------------
# plan_job: idempotency
# ---------------------------------------------------------------------------

def test_plan_job_is_idempotent_tasks():
    job = JobPlan(job_title="test")
    plan_job(job)
    task_ids_first = [t.task_id for t in job.tasks]

    plan_job(job)
    task_ids_second = [t.task_id for t in job.tasks]

    assert task_ids_first == task_ids_second
    assert len(job.tasks) == 3


def test_plan_job_is_idempotent_artifacts():
    job = JobPlan(job_title="test")
    plan_job(job)
    artifact_ids_first = [a.id for a in job.artifacts]

    plan_job(job)
    artifact_ids_second = [a.id for a in job.artifacts]

    assert artifact_ids_first == artifact_ids_second
    assert len(job.artifacts) == 1


def test_plan_job_returns_unchanged_if_already_has_tasks():
    job = JobPlan(job_title="test")
    existing_task = TaskEntry(title="pre-existing")
    job.tasks = [existing_task]

    result = plan_job(job)

    assert result.changed is False
    assert len(result.job.tasks) == 1
    assert result.job.tasks[0].task_id == existing_task.task_id


def test_plan_job_returns_unchanged_if_already_has_artifacts():
    job = JobPlan(job_title="test")
    existing = Artifact(name="pre-existing", content="x")
    job.artifacts = [existing]

    result = plan_job(job)

    assert result.changed is False
    assert len(result.job.artifacts) == 1
    assert result.job.artifacts[0].id == existing.id
