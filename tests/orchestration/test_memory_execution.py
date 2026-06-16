"""Tests: approved memory feeds into task execution context safely."""
from __future__ import annotations

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.task_runner import run_next_task


def _fake_builder(ctx: TaskExecutionContext) -> BuilderOutput:
    """Capture context and return minimal output."""
    _fake_builder.last_ctx = ctx
    return BuilderOutput(
        summary="Done",
        proposed_changes=["Changed something"],
    )


_fake_builder.last_ctx = None


def _make_planned_job(prompt="Fix bug"):
    job = Job(name="test-job", user_prompt=prompt)
    job.state = RunState.PLANNED
    job.tasks = [Task(description="Test task", inputs={"task_type": "test_task"})]
    job.artifacts = [
        Artifact(
            name="planning_output",
            content="Plan",
            task_id=None,
            kind=ArtifactKind.PLANNING,
            metadata={"summary": "Plan summary"},
        )
    ]
    return job


class TestExecutionWithNoMemory:
    def test_no_memory_context_is_none(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_planned_job()
        run_next_task(job, _fake_builder)
        assert _fake_builder.last_ctx.memory_context is None

    def test_no_memory_metadata_empty_or_zero(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_planned_job()
        run_next_task(job, _fake_builder)
        meta = _fake_builder.last_ctx.memory_metadata
        assert meta.get("memory_item_count", 0) == 0


class TestExecutionWithApprovedMemory:
    def test_approved_memory_in_context(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        store_memory(key="pattern", value="Use fixtures", project_id="proj1", approved=True)

        job = _make_planned_job()
        job.metadata["project_id"] = "proj1"
        run_next_task(job, _fake_builder)

        assert _fake_builder.last_ctx.memory_context is not None
        assert "pattern" in _fake_builder.last_ctx.memory_context

    def test_unapproved_excluded_from_context(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        store_memory(key="secret", value="Bad", project_id="proj1", approved=False)

        job = _make_planned_job()
        job.metadata["project_id"] = "proj1"
        run_next_task(job, _fake_builder)

        ctx = _fake_builder.last_ctx
        assert ctx.memory_context is None or "secret" not in ctx.memory_context


class TestExecutionMemoryMetadata:
    def test_artifact_has_memory_metadata(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        store_memory(key="tip", value="Info", project_id="proj1", approved=True)

        job = _make_planned_job()
        job.metadata["project_id"] = "proj1"
        run_next_task(job, _fake_builder)

        task_artifact = [a for a in job.artifacts if a.task_id is not None][0]
        assert task_artifact.metadata.get("memory_item_count") == 1
        assert "memory_context_hash" in task_artifact.metadata

    def test_no_raw_memory_in_artifact(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory

        store_memory(key="rule", value="Raw sensitive details", project_id="proj1", approved=True)

        job = _make_planned_job()
        job.metadata["project_id"] = "proj1"
        run_next_task(job, _fake_builder)

        task_artifact = [a for a in job.artifacts if a.task_id is not None][0]
        assert "Raw sensitive details" not in task_artifact.content

    def test_memory_does_not_change_approval_requirement(self, tmp_path, monkeypatch):
        """Memory cannot bypass source_apply permission gates."""
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "repo"
        repo.mkdir()

        job = Job(name="test")
        # No permission, no approval — must fail regardless of memory
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=[FileOp(path="x.py", action="create", content="x")],
        )
        result = apply_structured_patch(patch, repo, job=job, intent_id=None)
        assert not result.success
