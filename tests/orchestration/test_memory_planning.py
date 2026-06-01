"""Tests: approved memory feeds into planning safely."""
from __future__ import annotations

from uuid import uuid4

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.llm_planner import plan_job_with_llm
from packages.orchestration.planner_models import PlannerOutput, ProposedTask


def _fake_planner(prompt: str) -> PlannerOutput:
    """Capture prompt and return minimal valid output."""
    _fake_planner.last_prompt = prompt
    return PlannerOutput(
        summary="Test plan",
        proposed_tasks=[ProposedTask(task_type="test_task", description="Test")],
    )


_fake_planner.last_prompt = ""


class TestPlannerWithNoMemory:
    def test_no_memory_behaves_as_before(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test-job", user_prompt="Fix the bug")
        result = plan_job_with_llm(job, _fake_planner)
        assert result.changed is True
        assert job.state == RunState.PLANNED
        assert "Fix the bug" in _fake_planner.last_prompt

    def test_no_memory_no_memory_section_in_prompt(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test-job", user_prompt="Fix the bug")
        plan_job_with_llm(job, _fake_planner)
        assert "Project Memory" not in _fake_planner.last_prompt


class TestPlannerWithApprovedMemory:
    def test_approved_memory_injected_into_prompt(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        store_memory(
            key="test-pattern",
            value="Always run pytest with -x flag",
            project_id="proj1",
            approved=True,
            tags=["testing"],
        )
        job = Job(name="test-job", user_prompt="Fix the tests")
        job.metadata["project_id"] = "proj1"
        result = plan_job_with_llm(job, _fake_planner)
        assert result.changed is True
        assert "Project Memory" in _fake_planner.last_prompt
        assert "test-pattern" in _fake_planner.last_prompt

    def test_unapproved_memory_excluded(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        store_memory(
            key="secret-plan",
            value="Unapproved idea",
            project_id="proj1",
            approved=False,
        )
        job = Job(name="test-job", user_prompt="Fix")
        job.metadata["project_id"] = "proj1"
        plan_job_with_llm(job, _fake_planner)
        assert "secret-plan" not in _fake_planner.last_prompt


class TestPlannerMemoryMetadata:
    def test_planning_artifact_has_memory_metadata(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        store_memory(key="pattern", value="Info", project_id="proj1", approved=True)
        job = Job(name="test-job", user_prompt="Plan")
        job.metadata["project_id"] = "proj1"
        plan_job_with_llm(job, _fake_planner)

        artifact = job.artifacts[0]
        assert artifact.metadata.get("memory_item_count") == 1
        assert "memory_context_hash" in artifact.metadata
        assert artifact.metadata.get("memory_truncated") is False

    def test_no_memory_metadata_when_empty(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test-job", user_prompt="Plan")
        plan_job_with_llm(job, _fake_planner)

        artifact = job.artifacts[0]
        assert artifact.metadata.get("memory_item_count", 0) == 0

    def test_no_raw_memory_text_in_artifact_content(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        store_memory(key="rule", value="Sensitive details here", project_id="proj1", approved=True)
        job = Job(name="test-job", user_prompt="Plan")
        job.metadata["project_id"] = "proj1"
        plan_job_with_llm(job, _fake_planner)

        artifact = job.artifacts[0]
        # Artifact content should not contain raw memory value
        assert "Sensitive details here" not in artifact.content


class TestPlannerMemoryBudget:
    def test_over_budget_memory_truncated(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        # Each item key ~100 chars → ~25+ tokens per item. 50 items → >500 budget
        for i in range(50):
            store_memory(
                key=f"pattern-observation-about-project-configuration-{i:03d}-{'x' * 50}",
                value="x" * 200,
                project_id="proj1", approved=True,
            )
        job = Job(name="test-job", user_prompt="Plan")
        job.metadata["project_id"] = "proj1"
        plan_job_with_llm(job, _fake_planner)

        artifact = job.artifacts[0]
        assert artifact.metadata.get("memory_truncated") is True
