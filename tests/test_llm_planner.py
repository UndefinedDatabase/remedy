"""
Tests for plan_job_with_llm() and planner output transformation.

All tests use a mock call_planner callable — no live Ollama server required.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.job_runner import PlanJobResult
from packages.orchestration.llm_planner import plan_job_with_llm
from packages.orchestration.planner_models import PlannerOutput, ProposedTask


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_output(**kwargs) -> PlannerOutput:
    defaults: dict = dict(
        summary="Implement a CLI tool.",
        proposed_tasks=[
            ProposedTask(task_type="analyse_requirements", description="Understand the requirements."),
            ProposedTask(task_type="implement_feature", description="Write the implementation."),
            ProposedTask(task_type="write_tests", description="Add test coverage."),
        ],
    )
    defaults.update(kwargs)
    return PlannerOutput(**defaults)


def _stub_planner(output: PlannerOutput):
    """Return a callable that always returns the given output."""
    return lambda _prompt: output


# ---------------------------------------------------------------------------
# Basic transformation
# ---------------------------------------------------------------------------

def test_plan_job_with_llm_produces_tasks():
    job = Job(name="test", user_prompt="build a CLI")
    result = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert len(result.job.tasks) == 3


def test_plan_job_with_llm_task_types_match():
    output = _make_output()
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(output))
    task_types = [t.inputs.get("task_type") for t in result.job.tasks]
    assert task_types == ["analyse_requirements", "implement_feature", "write_tests"]


def test_plan_job_with_llm_task_descriptions_match():
    output = _make_output()
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(output))
    assert result.job.tasks[0].description == "Understand the requirements."


def test_plan_job_with_llm_produces_artifact():
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert len(result.job.artifacts) == 1
    assert result.job.artifacts[0].name == "planning_output"


def test_plan_job_with_llm_artifact_contains_summary():
    output = _make_output(summary="My unique summary text.")
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(output))
    assert "My unique summary text." in result.job.artifacts[0].content


def test_plan_job_with_llm_artifact_task_id_is_none():
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert result.job.artifacts[0].task_id is None


def test_plan_job_with_llm_artifact_metadata_planner():
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert result.job.artifacts[0].metadata.get("planner") == "llm"


# ---------------------------------------------------------------------------
# Optional fields in artifact content
# ---------------------------------------------------------------------------

def test_acceptance_checks_in_artifact_content():
    output = _make_output(acceptance_checks=["all tests pass", "no lint errors"])
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(output))
    content = result.job.artifacts[0].content
    assert "all tests pass" in content
    assert "no lint errors" in content


def test_notes_in_artifact_content():
    output = _make_output(notes=["assumes Python 3.10+"])
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(output))
    assert "assumes Python 3.10+" in result.job.artifacts[0].content


def test_empty_optional_fields_no_section_in_content():
    output = _make_output(acceptance_checks=[], notes=[])
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(output))
    content = result.job.artifacts[0].content
    assert "Acceptance Checks:" not in content
    assert "Notes:" not in content


# ---------------------------------------------------------------------------
# State transitions
# ---------------------------------------------------------------------------

def test_plan_job_with_llm_state_is_planned():
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert result.job.state == RunState.PLANNED


def test_plan_job_with_llm_changed_true():
    job = Job(name="test")
    result = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert result.changed is True


# ---------------------------------------------------------------------------
# Idempotency / no-op
# ---------------------------------------------------------------------------

def test_plan_job_with_llm_no_op_if_already_planned():
    job = Job(name="test")
    plan_job_with_llm(job, _stub_planner(_make_output()))  # first call
    first_task_ids = [t.id for t in job.tasks]

    result2 = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert result2.changed is False
    assert [t.id for t in result2.job.tasks] == first_task_ids


def test_plan_job_with_llm_no_op_if_has_tasks():
    job = Job(name="test")
    job.tasks = [Task(description="pre-existing")]
    result = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert result.changed is False
    assert len(result.job.tasks) == 1


def test_plan_job_with_llm_no_op_if_has_artifacts():
    job = Job(name="test")
    job.artifacts = [Artifact(name="pre-existing", content="x")]
    result = plan_job_with_llm(job, _stub_planner(_make_output()))
    assert result.changed is False
    assert len(result.job.artifacts) == 1


# ---------------------------------------------------------------------------
# Validation failure propagation
# ---------------------------------------------------------------------------

def test_plan_job_with_llm_propagates_validation_error():
    """If call_planner raises ValidationError, plan_job_with_llm propagates it."""
    def bad_planner(_prompt):
        # Simulate a provider that returns invalid data
        PlannerOutput.model_validate({"summary": 123, "proposed_tasks": "not-a-list"})

    job = Job(name="test")
    with pytest.raises(ValidationError):
        plan_job_with_llm(job, bad_planner)


def test_plan_job_with_llm_propagates_provider_exceptions():
    """If call_planner raises any exception, plan_job_with_llm propagates it."""
    def failing_planner(_prompt):
        raise RuntimeError("Ollama server unreachable")

    job = Job(name="test")
    with pytest.raises(RuntimeError, match="Ollama server unreachable"):
        plan_job_with_llm(job, failing_planner)


# ---------------------------------------------------------------------------
# PlannerOutput model validation
# ---------------------------------------------------------------------------

def test_planner_output_requires_summary():
    with pytest.raises(ValidationError):
        PlannerOutput(proposed_tasks=[])  # type: ignore[call-arg]


def test_planner_output_requires_proposed_tasks():
    with pytest.raises(ValidationError):
        PlannerOutput(summary="ok")  # type: ignore[call-arg]


def test_planner_output_optional_fields_default_empty():
    output = PlannerOutput(summary="ok", proposed_tasks=[])
    assert output.acceptance_checks == []
    assert output.notes == []
