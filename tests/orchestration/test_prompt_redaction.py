"""Tests: planning artifact does not contain raw prompt or memory content."""
from __future__ import annotations

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.llm_planner import plan_job_with_llm
from packages.orchestration.planner_models import PlannerOutput, ProposedTask


def _fake_planner(prompt: str) -> PlannerOutput:
    _fake_planner.last_prompt = prompt
    return PlannerOutput(
        summary="Test plan",
        proposed_tasks=[ProposedTask(task_type="test_task", description="Test")],
    )


_fake_planner.last_prompt = ""


class TestPlanningArtifactRedaction:
    def test_no_raw_prompt_in_artifact_content(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", user_prompt="Fix the auth vulnerability in login.py")
        plan_job_with_llm(job, _fake_planner)
        content = job.artifacts[0].content
        assert "Fix the auth vulnerability" not in content
        assert "[redacted]" in content

    def test_no_memory_section_in_artifact_content(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        store_memory(key="pattern-tip", value="Use bcrypt", project_id="proj1", approved=True)

        job = Job(name="test", user_prompt="Fix auth")
        job.metadata["project_id"] = "proj1"
        plan_job_with_llm(job, _fake_planner)
        content = job.artifacts[0].content
        assert "pattern-tip" not in content
        assert "Project Memory" not in content

    def test_prompt_hash_in_metadata(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", user_prompt="Fix bug")
        plan_job_with_llm(job, _fake_planner)
        meta = job.artifacts[0].metadata
        assert meta["prompt_present"] is True
        assert len(meta["prompt_hash"]) == 16
        assert meta["prompt_length"] == len("Fix bug")

    def test_memory_metadata_in_artifact(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        store_memory(key="tip", value="info", project_id="proj1", approved=True)

        job = Job(name="test", user_prompt="Plan")
        job.metadata["project_id"] = "proj1"
        plan_job_with_llm(job, _fake_planner)
        meta = job.artifacts[0].metadata
        assert meta.get("memory_item_count") == 1
        assert "memory_context_hash" in meta

    def test_planner_still_receives_full_prompt(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", user_prompt="Fix the login bug")
        plan_job_with_llm(job, _fake_planner)
        # Provider still gets full prompt
        assert "Fix the login bug" in _fake_planner.last_prompt

    def test_missing_data_dir_no_crash(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        store_memory(key="tip", value="info", project_id="proj1", approved=True)

        job = Job(name="test", user_prompt="Plan")
        job.metadata["project_id"] = "proj1"
        # No data_dir in job metadata — event emission should not crash
        result = plan_job_with_llm(job, _fake_planner)
        assert result.changed is True
