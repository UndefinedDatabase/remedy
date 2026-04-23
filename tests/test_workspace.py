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
from packages.orchestration.task_runner import (
    _extract_proposed_changes,
    _sanitize_path_component,
    materialize_task_output,
    run_next_task,
)
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
    # Filename format: <index>_<safe_type>_<short_id>.txt
    assert "generate_tests" in mf.path.name
    assert mf.path.name.endswith(".txt")
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


# ---------------------------------------------------------------------------
# Step 6.5: _sanitize_path_component
# ---------------------------------------------------------------------------


def test_sanitize_safe_snake_case_passthrough():
    assert _sanitize_path_component("write_code") == "write_code"


def test_sanitize_safe_hyphen_passthrough():
    assert _sanitize_path_component("write-code") == "write-code"


def test_sanitize_replaces_slash():
    result = _sanitize_path_component("foo/bar")
    assert "/" not in result
    assert "foo" in result
    assert "bar" in result


def test_sanitize_neutralizes_traversal():
    result = _sanitize_path_component("../../etc/passwd")
    assert ".." not in result
    assert "/" not in result


def test_sanitize_replaces_dot():
    assert "." not in _sanitize_path_component("foo.bar")


def test_sanitize_replaces_space():
    assert " " not in _sanitize_path_component("foo bar")


def test_sanitize_truncates_long_value():
    result = _sanitize_path_component("a" * 100)
    assert len(result) <= 48


def test_sanitize_empty_string_returns_unknown():
    assert _sanitize_path_component("") == "unknown"


def test_sanitize_all_dots_returns_unknown():
    # "..." → "___" → strip → "" → "unknown"
    assert _sanitize_path_component("...") == "unknown"


def test_sanitize_all_slashes_returns_unknown():
    assert _sanitize_path_component("///") == "unknown"


# ---------------------------------------------------------------------------
# Step 6.5: _extract_proposed_changes — section-aware extraction
# ---------------------------------------------------------------------------


def _make_artifact_content(
    proposed: list[str],
    notes: list[str] | None = None,
    risks: list[str] | None = None,
) -> str:
    """Build a minimal artifact content string matching the run_next_task format."""
    lines = [
        "Builder Execution Output",
        "Task:  fake-task-id",
        "Type:  do_work",
        "Desc:  Some task.",
        "",
        "Summary: Did stuff.",
        "",
        "Proposed Changes:",
    ]
    for p in proposed:
        lines.append(f"  - {p}")
    if notes:
        lines.append("")
        lines.append("Notes:")
        for n in notes:
            lines.append(f"  - {n}")
    if risks:
        lines.append("")
        lines.append("Risks:")
        for r in risks:
            lines.append(f"  - {r}")
    return "\n".join(lines)


def test_extract_returns_proposed_changes():
    content = _make_artifact_content(proposed=["Change A", "Change B"])
    result = _extract_proposed_changes(content)
    assert result == ["  - Change A", "  - Change B"]


def test_extract_excludes_notes():
    content = _make_artifact_content(
        proposed=["Change A"],
        notes=["A note here"],
    )
    result = _extract_proposed_changes(content)
    assert all("note" not in line.lower() for line in result)
    assert result == ["  - Change A"]


def test_extract_excludes_risks():
    content = _make_artifact_content(
        proposed=["Change A"],
        risks=["A risk here"],
    )
    result = _extract_proposed_changes(content)
    assert all("risk" not in line.lower() for line in result)
    assert result == ["  - Change A"]


def test_extract_excludes_notes_and_risks():
    content = _make_artifact_content(
        proposed=["Real change"],
        notes=["Note text"],
        risks=["Risk text"],
    )
    result = _extract_proposed_changes(content)
    assert result == ["  - Real change"]


def test_extract_empty_proposed_section():
    content = _make_artifact_content(proposed=[], notes=["Only a note"])
    result = _extract_proposed_changes(content)
    assert result == []


def test_extract_no_notes_or_risks():
    content = _make_artifact_content(proposed=["Only change"])
    result = _extract_proposed_changes(content)
    assert result == ["  - Only change"]


# ---------------------------------------------------------------------------
# Step 6.5: materialize — section-aware (notes/risks excluded from file)
# ---------------------------------------------------------------------------


def _stub_builder_with_notes_and_risks(context: TaskExecutionContext) -> BuilderOutput:
    return BuilderOutput(
        summary="Done.",
        proposed_changes=["Add foo()", "Add bar()"],
        notes=["Assumed Python 3.11+"],
        risks=["May break existing tests"],
    )


def test_materialize_notes_not_in_proposed_section(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder_with_notes_and_risks)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    # Find the "Proposed Changes:" section in the file and check no note text appears there
    lines = mf.content.splitlines()
    in_proposed = False
    for line in lines:
        if line == "Proposed Changes:":
            in_proposed = True
        elif line in ("Notes:", "Risks:"):
            in_proposed = False
        elif in_proposed:
            assert "Assumed Python 3.11+" not in line


def test_materialize_risks_not_in_proposed_section(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder_with_notes_and_risks)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    lines = mf.content.splitlines()
    in_proposed = False
    for line in lines:
        if line == "Proposed Changes:":
            in_proposed = True
        elif line in ("Notes:", "Risks:"):
            in_proposed = False
        elif in_proposed:
            assert "May break existing tests" not in line


def test_materialize_proposed_changes_all_present(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder_with_notes_and_risks)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    assert "Add foo()" in mf.content
    assert "Add bar()" in mf.content


# ---------------------------------------------------------------------------
# Step 6.5: collision-safe filenames
# ---------------------------------------------------------------------------


def test_materialize_filename_includes_index(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job(task_type="write_code")
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    # First task in job.tasks → index 0 → "000_..."
    assert mf.path.name.startswith("000_")


def test_materialize_filename_includes_short_task_id(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job(task_type="write_code")
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    task = next(t for t in result.job.tasks if t.id == result.task_id)
    short_id = task.id.hex[:8]
    assert short_id in mf.path.name


def test_duplicate_task_type_no_filename_collision(tmp_path, monkeypatch):
    """Two tasks with the same task_type must produce different workspace files."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    task1 = Task(description="First.", inputs={"task_type": "do_work"})
    task2 = Task(description="Second.", inputs={"task_type": "do_work"})
    job = Job(name="test", tasks=[task1, task2], state=RunState.PLANNED)

    result1 = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf1 = materialize_task_output(result1, runtime)

    result2 = run_next_task(result1.job, _stub_builder)
    mf2 = materialize_task_output(result2, runtime)

    assert mf1 is not None and mf2 is not None
    assert mf1.path != mf2.path
    assert mf1.path.exists() and mf2.path.exists()


def test_second_task_filename_index_is_one(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    task1 = Task(description="First.", inputs={"task_type": "step_a"})
    task2 = Task(description="Second.", inputs={"task_type": "step_b"})
    job = Job(name="test", tasks=[task1, task2], state=RunState.PLANNED)

    result1 = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    materialize_task_output(result1, runtime)

    result2 = run_next_task(result1.job, _stub_builder)
    mf2 = materialize_task_output(result2, runtime)

    assert mf2 is not None
    assert mf2.path.name.startswith("001_")


# ---------------------------------------------------------------------------
# Step 6.5: path sanitization in materialize
# ---------------------------------------------------------------------------


def test_materialize_sanitizes_unsafe_task_type(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job(task_type="../../../etc/passwd")
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    # File must be inside the workspace root — no traversal succeeded
    assert mf.path.is_relative_to(runtime.workspace.root)
    # No traversal sequences in the filename
    assert ".." not in mf.path.name
    assert "/" not in mf.path.name
    assert mf.path.exists()


def test_materialize_sanitizes_spaces_in_task_type(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job(task_type="write some code")
    result = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    assert mf is not None
    assert " " not in mf.path.name
    assert mf.path.exists()
