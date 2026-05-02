"""
Tests for verifier.py: TaskContract, VerificationResult, verify_task_output.

All tests are deterministic — no live Ollama, no real builder.
Workspace files are written to tmp_path where disk access is needed.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.task_runner import (
    annotate_task_result,
    finalize_task,
    materialize_task_output,
    run_next_task,
)
from packages.orchestration.verifier import (
    TaskContract,
    VerificationResult,
    verify_task_output,
)
from packages.orchestration.workspace import LocalWorkspaceRuntime


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


def _full_run(job: Job, tmp_path, builder=None) -> tuple:
    """Run build → annotate → materialize → verify → finalize for one task.

    Returns (result, mf, vr) after finalize_task has been called.
    """
    if builder is None:
        builder = _stub_builder
    import os
    os.environ["REMEDY_DATA_DIR"] = str(tmp_path)
    result = run_next_task(job, builder)
    annotate_task_result(
        result, provider="stub", role="builder", model="stub-model", elapsed_ms=1.0
    )
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    vr = verify_task_output(result.job, result.task_id)
    finalize_task(result, vr)
    return result, mf, vr


# ---------------------------------------------------------------------------
# Happy path: all checks pass
# ---------------------------------------------------------------------------


def test_verify_passes_on_valid_task_output(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result, mf, vr = _full_run(job, tmp_path)

    assert vr.passed is True
    assert vr.failures == []
    assert job.tasks[0].status == RunState.COMPLETED


def test_verify_all_checks_present_on_pass(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result, mf, vr = _full_run(job, tmp_path)

    check_names = [c.check for c in vr.checks]
    assert "has_output_artifact" in check_names
    assert "artifact_exists" in check_names
    assert "artifact_task_id_matches" in check_names
    assert "workspace_file_in_metadata" in check_names
    assert "workspace_file_exists" in check_names
    assert "workspace_file_not_empty" in check_names
    assert "has_proposed_change" in check_names


# ---------------------------------------------------------------------------
# Task not in job (impossible state guard)
# ---------------------------------------------------------------------------


def test_verify_fails_when_task_not_in_job():
    job = _make_planned_job()
    orphan_id = uuid4()
    vr = verify_task_output(job, orphan_id)
    assert vr.passed is False
    assert any(c.check == "task_exists" for c in vr.checks)


# ---------------------------------------------------------------------------
# Check: has_output_artifact
# ---------------------------------------------------------------------------


def test_verify_fails_when_no_output_artifact_ids():
    """Task with no output_artifact_ids fails the first check."""
    job = _make_planned_job()
    task = job.tasks[0]
    # task.output_artifact_ids is empty (no build was run)
    vr = verify_task_output(job, task.id)
    assert vr.passed is False
    assert any(c.check == "has_output_artifact" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# Check: artifact_exists
# ---------------------------------------------------------------------------


def test_verify_fails_when_artifact_id_not_in_job_artifacts():
    """output_artifact_ids references a UUID not in job.artifacts."""
    job = _make_planned_job()
    task = job.tasks[0]
    task.output_artifact_ids.append(uuid4())  # dangling reference
    vr = verify_task_output(job, task.id)
    assert vr.passed is False
    assert any(c.check == "artifact_exists" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# Check: artifact_task_id_matches
# ---------------------------------------------------------------------------


def test_verify_fails_when_artifact_task_id_does_not_match():
    """Artifact exists but artifact.task_id != task.id."""
    job = _make_planned_job()
    task = job.tasks[0]
    wrong_artifact = Artifact(
        name="task_output_write_code",
        content="some content",
        mime_type="text/plain",
        task_id=uuid4(),  # wrong task_id — not task.id
        metadata={},
    )
    job.artifacts.append(wrong_artifact)
    task.output_artifact_ids.append(wrong_artifact.id)

    vr = verify_task_output(job, task.id)
    assert vr.passed is False
    assert any(c.check == "artifact_task_id_matches" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# Check: workspace_file_in_metadata
# ---------------------------------------------------------------------------


def test_verify_fails_when_workspace_file_key_missing():
    """Artifact has correct task_id but no 'workspace_file' in metadata."""
    job = _make_planned_job()
    task = job.tasks[0]
    artifact = Artifact(
        name="task_output_write_code",
        content="Builder Execution Output\n\nProposed Changes:\n  - Add foo()\n",
        mime_type="text/plain",
        task_id=task.id,
        metadata={"task_type": "write_code", "summary": "done"},
        # no 'workspace_file' key
    )
    job.artifacts.append(artifact)
    task.output_artifact_ids.append(artifact.id)

    vr = verify_task_output(job, task.id)
    assert vr.passed is False
    assert any(c.check == "workspace_file_in_metadata" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# Check: workspace_file_exists
# ---------------------------------------------------------------------------


def test_verify_fails_when_workspace_file_does_not_exist(tmp_path):
    """workspace_file key is present but points to a non-existent file."""
    job = _make_planned_job()
    task = job.tasks[0]
    nonexistent = tmp_path / "ghost.txt"
    artifact = Artifact(
        name="task_output_write_code",
        content="...",
        mime_type="text/plain",
        task_id=task.id,
        metadata={
            "task_type": "write_code",
            "summary": "done",
            "workspace_file": str(nonexistent),
        },
    )
    job.artifacts.append(artifact)
    task.output_artifact_ids.append(artifact.id)

    vr = verify_task_output(job, task.id)
    assert vr.passed is False
    assert any(c.check == "workspace_file_exists" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# Check: workspace_file_not_empty
# ---------------------------------------------------------------------------


def test_verify_fails_when_workspace_file_is_empty(tmp_path):
    """workspace file exists but is 0 bytes."""
    job = _make_planned_job()
    task = job.tasks[0]
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    artifact = Artifact(
        name="task_output_write_code",
        content="...",
        mime_type="text/plain",
        task_id=task.id,
        metadata={
            "task_type": "write_code",
            "summary": "done",
            "workspace_file": str(empty_file),
        },
    )
    job.artifacts.append(artifact)
    task.output_artifact_ids.append(artifact.id)

    vr = verify_task_output(job, task.id)
    assert vr.passed is False
    assert any(c.check == "workspace_file_not_empty" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# Check: has_proposed_change
# ---------------------------------------------------------------------------


def test_verify_fails_when_no_proposed_change_lines(tmp_path):
    """workspace file has content but no lines starting with '  - '."""
    job = _make_planned_job()
    task = job.tasks[0]
    file = tmp_path / "no_changes.txt"
    file.write_text("Task Type: write_code\nSummary: done\n\nProposed Changes:\n")

    artifact = Artifact(
        name="task_output_write_code",
        content="...",
        mime_type="text/plain",
        task_id=task.id,
        metadata={
            "task_type": "write_code",
            "summary": "done",
            "workspace_file": str(file),
        },
    )
    job.artifacts.append(artifact)
    task.output_artifact_ids.append(artifact.id)

    vr = verify_task_output(job, task.id)
    assert vr.passed is False
    assert any(c.check == "has_proposed_change" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# Integration: task only COMPLETED after verification passes
# ---------------------------------------------------------------------------


def test_task_not_completed_until_verification_passes(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)

    # Task is RUNNING immediately after builder — not COMPLETED
    assert job.tasks[0].status == RunState.RUNNING

    annotate_task_result(
        result, provider="stub", role="builder", model="m", elapsed_ms=1.0
    )
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    materialize_task_output(result, runtime)

    vr = verify_task_output(result.job, result.task_id)
    assert vr.passed is True

    finalize_task(result, vr)
    assert job.tasks[0].status == RunState.COMPLETED


def test_failed_verification_leaves_task_pending(tmp_path, monkeypatch):
    """If verification fails, task is rolled back to PENDING — not stranded RUNNING."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)
    assert job.tasks[0].status == RunState.RUNNING

    # Force verification to fail by pointing workspace_file at a non-existent path
    artifact = next(a for a in job.artifacts if a.task_id == result.task_id)
    artifact.metadata["workspace_file"] = str(tmp_path / "ghost.txt")

    vr = verify_task_output(result.job, result.task_id)
    assert vr.passed is False

    finalize_task(result, vr)
    # Task rolled back to PENDING — not stranded in RUNNING
    assert job.tasks[0].status == RunState.PENDING


def test_failed_verification_records_failures_in_artifact_metadata(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)

    artifact = next(a for a in job.artifacts if a.task_id == result.task_id)
    artifact.metadata["workspace_file"] = str(tmp_path / "ghost.txt")

    vr = verify_task_output(result.job, result.task_id)
    finalize_task(result, vr)

    assert artifact.metadata["verification_passed"] is False
    assert isinstance(artifact.metadata["verification_failures"], list)
    assert len(artifact.metadata["verification_failures"]) > 0


def test_failed_verification_clears_output_artifact_ids(tmp_path, monkeypatch):
    """Retry safety: finalize_task clears output_artifact_ids on failure."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()
    result = run_next_task(job, _stub_builder)
    assert len(job.tasks[0].output_artifact_ids) == 1

    artifact = next(a for a in job.artifacts if a.task_id == result.task_id)
    artifact.metadata["workspace_file"] = str(tmp_path / "ghost.txt")

    vr = verify_task_output(result.job, result.task_id)
    finalize_task(result, vr)

    assert job.tasks[0].output_artifact_ids == []


def test_retry_verify_uses_new_artifact_not_stale(tmp_path, monkeypatch):
    """Full retry cycle: second build produces a new artifact; verify sees only it."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = _make_planned_job()

    # First attempt: verification fails (point workspace_file at non-existent path)
    result1 = run_next_task(job, _stub_builder)
    stale_artifact_id = job.tasks[0].output_artifact_ids[0]
    artifact1 = next(a for a in job.artifacts if a.task_id == result1.task_id)
    artifact1.metadata["workspace_file"] = str(tmp_path / "ghost.txt")
    vr1 = verify_task_output(result1.job, result1.task_id)
    assert vr1.passed is False
    finalize_task(result1, vr1)
    assert job.tasks[0].status == RunState.PENDING
    assert job.tasks[0].output_artifact_ids == []

    # Second attempt: builder runs again; materialize produces a real file
    result2 = run_next_task(job, _stub_builder)
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    annotate_task_result(
        result2, provider="stub", role="builder", model="m", elapsed_ms=1.0
    )
    materialize_task_output(result2, runtime)

    # The task now references only the new artifact
    assert len(job.tasks[0].output_artifact_ids) == 1
    new_artifact_id = job.tasks[0].output_artifact_ids[0]
    assert new_artifact_id != stale_artifact_id

    # Verification on retry passes (real file was materialized)
    vr2 = verify_task_output(result2.job, result2.task_id)
    assert vr2.passed is True
    finalize_task(result2, vr2)
    assert job.tasks[0].status == RunState.COMPLETED


# ---------------------------------------------------------------------------
# Verifier Profiles v1
#
# Profile checks run inside verify_task_output after workspace file checks pass.
# They read artifact.content, not the workspace file.
# ---------------------------------------------------------------------------

_BUILDER_CONTENT_TEMPLATE = """\
Builder Execution Output
Task:  {task_id}
Type:  {task_type}
Desc:  test description

Summary: {summary}

Proposed Changes:
{changes}{risks_block}"""


def _make_artifact_content(
    task_id,
    task_type: str = "write_code",
    summary: str = "Done.",
    changes: list[str] | None = None,
    risks: list[str] | None = None,
) -> str:
    if changes is None:
        changes = ["Add function foo()", "Add unit test"]
    changes_text = "\n".join(f"  - {c}" for c in changes)
    risks_block = ""
    if risks:
        risks_text = "\n".join(f"  - {r}" for r in risks)
        risks_block = f"\n\nRisks:\n{risks_text}"
    return _BUILDER_CONTENT_TEMPLATE.format(
        task_id=task_id,
        task_type=task_type,
        summary=summary,
        changes=changes_text,
        risks_block=risks_block,
    )


def _setup_artifact_with_content(
    job: Job,
    content: str,
    task_type: str,
    ws_file_path,
) -> Artifact:
    """Create an artifact with given content and a valid workspace file."""
    task = job.tasks[0]
    ws_file_path.write_text("Task Type: test\nSummary: done\n\nProposed Changes:\n  - x\n")
    artifact = Artifact(
        name=f"task_output_{task_type}",
        content=content,
        mime_type="text/plain",
        task_id=task.id,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        metadata={
            "task_type": task_type,
            "summary": "done",
            "workspace_file": str(ws_file_path),
        },
    )
    job.artifacts.append(artifact)
    task.output_artifact_ids.append(artifact.id)
    return artifact


# ---------------------------------------------------------------------------
# generic profile — baseline
# ---------------------------------------------------------------------------


class TestGenericProfileVerification:
    def test_generic_happy_path_passes(self, tmp_path):
        """Unknown task_type uses generic profile; standard content passes."""
        job = _make_planned_job("write_code")
        task = job.tasks[0]
        content = _make_artifact_content(task.id, "write_code")
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_code", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is True

    def test_generic_profile_check_names_present(self, tmp_path):
        job = _make_planned_job("write_code")
        task = job.tasks[0]
        content = _make_artifact_content(task.id, "write_code")
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_code", ws)
        vr = verify_task_output(job, task.id)
        check_names = [c.check for c in vr.checks]
        assert "required_section:Summary:" in check_names
        assert "required_section:Proposed Changes:" in check_names
        assert "min_proposed_changes" in check_names

    def test_profile_checks_run_without_workspace_file(self):
        """Profile checks are independent of TaskContract.require_workspace_file.

        Passing TaskContract(require_workspace_file=False) skips workspace checks
        but must NOT skip profile content checks.
        """
        from packages.orchestration.verifier import TaskContract

        job = _make_planned_job("write_readme")  # repo_doc profile → forbids TODO/TBD
        task = job.tasks[0]
        # Artifact content with a TODO — should fail repo_doc forbidden_phrase:TODO
        content = _make_artifact_content(
            task.id, "write_readme", summary="TODO: fill in later"
        )
        # No workspace_file in metadata; contract skips workspace checks entirely.
        artifact = Artifact(
            name="task_output_write_readme",
            content=content,
            mime_type="text/plain",
            task_id=task.id,
            kind=ArtifactKind.BUILDER_PROPOSAL,
            metadata={"task_type": "write_readme", "summary": "done"},
        )
        job.artifacts.append(artifact)
        task.output_artifact_ids.append(artifact.id)

        vr = verify_task_output(
            job, task.id, contract=TaskContract(require_workspace_file=False)
        )
        # Profile check should still fire and fail on TODO
        check_names = [c.check for c in vr.checks]
        assert "forbidden_phrase:TODO" in check_names
        assert any(c.check == "forbidden_phrase:TODO" and not c.passed for c in vr.checks)
        # No workspace checks present (they were skipped by contract)
        assert "workspace_file_in_metadata" not in check_names


# ---------------------------------------------------------------------------
# repo_doc profile — forbidden phrases (TODO, TBD)
# ---------------------------------------------------------------------------


class TestRepoDocProfileVerification:
    def test_repo_doc_passes_with_clean_content(self, tmp_path):
        """write_readme → repo_doc; content without TODO/TBD passes."""
        job = _make_planned_job("write_readme")
        task = job.tasks[0]
        content = _make_artifact_content(task.id, "write_readme")
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_readme", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is True

    def test_repo_doc_fails_on_TODO_in_content(self, tmp_path):
        """repo_doc profile rejects 'TODO' anywhere in artifact content."""
        job = _make_planned_job("write_readme")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "write_readme", summary="TODO: finish this"
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_readme", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is False
        assert any(c.check == "forbidden_phrase:TODO" and not c.passed for c in vr.checks)

    def test_repo_doc_fails_on_TBD_in_content(self, tmp_path):
        job = _make_planned_job("write_readme")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "write_readme", changes=["Update section TBD later"]
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_readme", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is False
        assert any(c.check == "forbidden_phrase:TBD" and not c.passed for c in vr.checks)

    def test_forbidden_phrase_check_is_case_insensitive(self, tmp_path):
        """'todo' (lowercase) must also be caught by repo_doc forbidden_phrase:TODO."""
        job = _make_planned_job("write_readme")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "write_readme", summary="todo: figure out later"
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_readme", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is False
        assert any(c.check == "forbidden_phrase:TODO" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# analysis_doc profile — min 2 proposed changes, forbidden phrases
# ---------------------------------------------------------------------------


class TestAnalysisDocProfileVerification:
    def test_analysis_doc_passes_with_two_changes(self, tmp_path):
        job = _make_planned_job("write_spec")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "write_spec",
            changes=["Add section A", "Add section B"],
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_spec", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is True

    def test_analysis_doc_fails_with_one_change(self, tmp_path):
        """analysis_doc requires >= 2 proposed changes; 1 is not enough."""
        job = _make_planned_job("write_spec")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "write_spec", changes=["Only one change"]
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_spec", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is False
        assert any(c.check == "min_proposed_changes" and not c.passed for c in vr.checks)

    def test_analysis_doc_fails_on_maybe(self, tmp_path):
        job = _make_planned_job("write_analysis")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "write_analysis",
            summary="maybe this is correct",
            changes=["Change A", "Change B"],
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "write_analysis", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is False
        assert any(c.check == "forbidden_phrase:maybe" and not c.passed for c in vr.checks)


# ---------------------------------------------------------------------------
# implementation_plan profile — requires Risks: section, min 2 changes
# ---------------------------------------------------------------------------


class TestImplementationPlanProfileVerification:
    def test_implementation_plan_passes_with_risks(self, tmp_path):
        job = _make_planned_job("create_plan")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "create_plan",
            changes=["Step A", "Step B"],
            risks=["Breaking change to API"],
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "create_plan", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is True

    def test_implementation_plan_fails_without_risks_section(self, tmp_path):
        """implementation_plan requires 'Risks:' in artifact content."""
        job = _make_planned_job("create_plan")
        task = job.tasks[0]
        # No risks= argument → no Risks: section
        content = _make_artifact_content(
            task.id, "create_plan", changes=["Step A", "Step B"]
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "create_plan", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is False
        assert any(
            c.check == "required_section:Risks:" and not c.passed for c in vr.checks
        )

    def test_implementation_plan_fails_with_one_change(self, tmp_path):
        job = _make_planned_job("create_plan")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "create_plan",
            changes=["Only one step"],
            risks=["Some risk"],
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "create_plan", ws)
        vr = verify_task_output(job, task.id)
        assert vr.passed is False
        assert any(c.check == "min_proposed_changes" and not c.passed for c in vr.checks)

    def test_failure_result_has_clear_check_name(self, tmp_path):
        """Check names include the section string for easy diagnosis."""
        job = _make_planned_job("create_plan")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "create_plan", changes=["Step A", "Step B"]
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "create_plan", ws)
        vr = verify_task_output(job, task.id)
        check_names = [c.check for c in vr.checks]
        assert "required_section:Risks:" in check_names

    def test_implementation_plan_does_not_forbid_TODO(self, tmp_path):
        """implementation_plan allows TODO — plans may reference follow-up work."""
        job = _make_planned_job("create_plan")
        task = job.tasks[0]
        content = _make_artifact_content(
            task.id, "create_plan",
            summary="TODO: decide on API surface",
            changes=["Step A", "Step B"],
            risks=["API may break consumers"],
        )
        ws = tmp_path / "out.txt"
        _setup_artifact_with_content(job, content, "create_plan", ws)
        vr = verify_task_output(job, task.id)
        # No forbidden_phrase:TODO check should appear (or if it does, it must pass)
        todo_checks = [c for c in vr.checks if c.check == "forbidden_phrase:TODO"]
        assert all(c.passed for c in todo_checks), (
            "implementation_plan should not forbid TODO but check failed"
        )
        # Verify TODO did not cause overall failure
        assert vr.passed is True
