"""
Tests for workspace.py (Workspace, MaterializedFile, LocalWorkspaceRuntime)
and materialize_task_output() in task_runner.py.

No live filesystem mocking is used for LocalWorkspaceRuntime — tests use
a tmp_path fixture so they write to a real temp directory and clean up
automatically.
"""

from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.task_runner import materialize_task_output, run_next_task
from packages.orchestration.workspace import LocalWorkspaceRuntime, MaterializedFile, Workspace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_planned_job(task_type: str = "write_code") -> Job:
    task = Task(description="Do some work.", inputs={"task_type": task_type})
    return Job(name="test-job", tasks=[task], state=RunState.PLANNED)


def _stub_builder(context: TaskExecutionContext) -> BuilderOutput:
    return BuilderOutput(
        summary="Implemented the feature.",
        proposed_changes=["Add function foo()", "Add unit test for foo"],
        notes=["Assumed Python 3.11+"],
        risks=[],
    )


# ---------------------------------------------------------------------------
# LocalWorkspaceRuntime — workspace creation
# ---------------------------------------------------------------------------


def test_runtime_creates_workspace_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job_id = uuid4()
    runtime = LocalWorkspaceRuntime(job_id=job_id)
    expected = tmp_path / "workspaces" / str(job_id)
    assert expected.is_dir()


def test_runtime_workspace_job_id(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job_id = uuid4()
    runtime = LocalWorkspaceRuntime(job_id=job_id)
    assert runtime.workspace.job_id == job_id


def test_runtime_workspace_root_matches_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job_id = uuid4()
    runtime = LocalWorkspaceRuntime(job_id=job_id)
    assert runtime.workspace.root == tmp_path / "workspaces" / str(job_id)


def test_runtime_workspace_starts_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    assert runtime.workspace.materialized_files == []


# ---------------------------------------------------------------------------
# LocalWorkspaceRuntime — write()
# ---------------------------------------------------------------------------


def test_runtime_write_creates_file(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    runtime.write("output/hello.txt", "hello world\n")
    assert (runtime.workspace.root / "output" / "hello.txt").exists()


def test_runtime_write_content_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    content = "line one\nline two\n"
    runtime.write("notes.txt", content)
    assert (runtime.workspace.root / "notes.txt").read_text() == content


def test_runtime_write_returns_materialized_file(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    mf = runtime.write("a/b.txt", "data")
    assert isinstance(mf, MaterializedFile)


def test_runtime_write_materialized_file_path(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    mf = runtime.write("sub/file.txt", "x")
    assert mf.path == runtime.workspace.root / "sub" / "file.txt"


def test_runtime_write_materialized_file_content(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    content = "hello"
    mf = runtime.write("f.txt", content)
    assert mf.content == content


def test_runtime_write_materialized_file_size(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    content = "abc"
    mf = runtime.write("f.txt", content)
    assert mf.size == len(content.encode("utf-8"))


def test_runtime_write_appended_to_workspace(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    runtime.write("a.txt", "a")
    runtime.write("b.txt", "b")
    assert len(runtime.workspace.materialized_files) == 2


def test_runtime_write_creates_nested_dirs(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    runtime = LocalWorkspaceRuntime(job_id=uuid4())
    runtime.write("deep/nested/path/file.txt", "content")
    assert (runtime.workspace.root / "deep" / "nested" / "path" / "file.txt").exists()


# ---------------------------------------------------------------------------
# materialize_task_output — basic behaviour
# ---------------------------------------------------------------------------


def test_materialize_noop_when_not_changed(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    # Simulate no-op result (no pending tasks)
    from packages.orchestration.task_runner import RunTaskResult
    result = RunTaskResult(job=job, task_id=None, changed=False)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is None


def test_materialize_returns_materialized_file(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert isinstance(mf, MaterializedFile)


def test_materialize_file_exists_on_disk(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job(task_type="write_code")
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    assert mf.path.exists()


def test_materialize_file_path_uses_task_type(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job(task_type="generate_tests")
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    assert mf.path.name == "generate_tests.txt"
    assert mf.path.parent.name == "task_output"


def test_materialize_file_content_contains_summary(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    assert "Implemented the feature." in mf.content


def test_materialize_file_content_contains_proposed_changes(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    assert "Add function foo()" in mf.content
    assert "Add unit test for foo" in mf.content


# ---------------------------------------------------------------------------
# materialize_task_output — artifact metadata
# ---------------------------------------------------------------------------


def test_materialize_sets_workspace_file_in_artifact_metadata(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    artifact = next(a for a in result.job.artifacts if a.task_id == result.task_id)
    assert "workspace_file" in artifact.metadata
    assert artifact.metadata["workspace_file"] == str(mf.path)


def test_materialize_workspace_file_path_is_absolute(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    materialize_task_output(result, runtime)
    artifact = next(a for a in result.job.artifacts if a.task_id == result.task_id)
    assert Path(artifact.metadata["workspace_file"]).is_absolute()
