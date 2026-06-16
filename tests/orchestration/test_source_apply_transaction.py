"""Tests for source_apply transactionality and diff hunk validation.

v2: FileSnapshot and _rollback removed (durable snapshot replaces in-memory rollback).
Transactional tests use apply_structured_patch public API.
"""
from __future__ import annotations

from uuid import uuid4

from packages.core.models import Job
from packages.orchestration.source_apply import (
    _apply_hunks,
    apply_structured_patch,
)


class TestTransactionRollback:
    """All-or-nothing: if op N fails, ops 1..N-1 are rolled back via durable snapshot."""

    def _make_approved_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Artifact
        from packages.orchestration.approval_queue import (
            APPROVAL_APPROVED,
            make_intent_id,
            set_approval_state,
        )
        from packages.orchestration.permissions import Capability, set_permission
        from packages.orchestration.storage import save_job

        job = Job(name="txn-test")
        set_permission(job, Capability.repo_generated_write, allow=True)

        artifact = Artifact(task_id=uuid4(), name="test-patch", content="")
        artifact.metadata = {"patch_intent_explanations": [
            {"file": "test", "action": "modify", "risk": "low",
             "reason": "test", "summary": "test patch"}
        ]}
        job.artifacts.append(artifact)
        save_job(job)

        intent_id = make_intent_id(artifact.id, 0)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        return job, intent_id

    def test_file_ops_rollback_on_second_failure(self, tmp_path, monkeypatch):
        """If second file_op fails, first file_op is rolled back via durable snapshot."""
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "a.py").write_text("original-a")

        job, intent_id = self._make_approved_job(tmp_path, monkeypatch)

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=[
                FileOp(path="a.py", action="modify", content="modified-a"),
                FileOp(path="b.py", action="modify", content="x"),  # b.py doesn't exist
            ],
        )

        result = apply_structured_patch(patch, repo, job=job, intent_id=intent_id)
        assert not result.success
        assert "b.py" in result.errors[-1]
        # a.py should be rolled back to original via durable snapshot
        assert (repo / "a.py").read_text() == "original-a"

    def test_unified_diff_rollback_on_second_failure(self, tmp_path, monkeypatch):
        """If second unified diff fails, first is rolled back via durable snapshot."""
        from packages.orchestration.structured_patch import StructuredPatch, UnifiedDiff

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "a.py").write_text("line1\nline2\n")

        job, intent_id = self._make_approved_job(tmp_path, monkeypatch)

        patch = StructuredPatch(
            intent_kind="unified_diff",
            unified_diffs=[
                UnifiedDiff(path="a.py", diff="@@ -1,2 +1,2 @@\n-line1\n+LINE1\n line2\n"),
                UnifiedDiff(path="missing.py", diff="@@ -1 +1 @@\n-x\n+y\n"),
            ],
        )

        result = apply_structured_patch(patch, repo, job=job, intent_id=intent_id)
        assert not result.success
        # a.py should be rolled back
        assert (repo / "a.py").read_text() == "line1\nline2\n"

    def test_apply_result_has_snapshot_id_on_success(self, tmp_path, monkeypatch):
        """Successful apply populates snapshot_id + snapshot_verified on ApplyResult."""
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "a.py").write_text("original")

        job, intent_id = self._make_approved_job(tmp_path, monkeypatch)

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=[FileOp(path="a.py", action="modify", content="updated")],
        )

        result = apply_structured_patch(patch, repo, job=job, intent_id=intent_id)
        assert result.success
        assert result.snapshot_id
        assert result.snapshot_verified

    def test_apply_result_no_content_field(self, tmp_path, monkeypatch):
        """ApplyResult must not expose raw content."""
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "a.py").write_text("SECRET_VALUE")

        job, intent_id = self._make_approved_job(tmp_path, monkeypatch)

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=[FileOp(path="a.py", action="modify", content="new content")],
        )

        result = apply_structured_patch(patch, repo, job=job, intent_id=intent_id)
        assert not hasattr(result, "snapshots")
        result_str = str(result)
        assert "SECRET_VALUE" not in result_str


class TestHunkValidation:
    """Context and removal lines must match actual file content."""

    def test_correct_context_applies(self):
        original = "alpha\nbeta\ngamma\n"
        diff = "@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n"
        result = _apply_hunks(original, diff)
        assert result is not None
        assert "BETA" in result

    def test_wrong_context_line_rejects(self):
        original = "alpha\nbeta\ngamma\n"
        diff = "@@ -1,3 +1,3 @@\n WRONG\n-beta\n+BETA\n gamma\n"
        result = _apply_hunks(original, diff)
        assert result is None

    def test_wrong_removal_line_rejects(self):
        original = "alpha\nbeta\ngamma\n"
        diff = "@@ -1,3 +1,3 @@\n alpha\n-WRONG\n+BETA\n gamma\n"
        result = _apply_hunks(original, diff)
        assert result is None

    def test_context_out_of_range_rejects(self):
        original = "one\n"
        diff = "@@ -1,3 +1,3 @@\n one\n two\n three\n"
        result = _apply_hunks(original, diff)
        assert result is None

    def test_removal_out_of_range_rejects(self):
        original = "one\n"
        diff = "@@ -1,2 +1,1 @@\n one\n-two\n"
        result = _apply_hunks(original, diff)
        assert result is None

    def test_empty_diff_is_noop(self):
        original = "alpha\nbeta\n"
        diff = ""
        result = _apply_hunks(original, diff)
        assert result == original
