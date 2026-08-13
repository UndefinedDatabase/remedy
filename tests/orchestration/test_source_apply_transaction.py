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
        # Full string, not a substring: a substring check cannot see the added
        # line landing in the wrong place (finding R-0311).
        assert result == "alpha\nBETA\ngamma\n"

    def test_addition_in_middle_of_hunk_lands_between_neighbours(self):
        """An added line lands at its own position, not at the hunk start."""
        original = "a\nb\nc\nd\n"
        diff = "@@ -1,3 +1,4 @@\n a\n b\n+NEW\n c\n"
        result = _apply_hunks(original, diff)
        assert result == "a\nb\nNEW\nc\nd\n"

    def test_addition_at_end_of_hunk_lands_last(self):
        """An added line at the end of a hunk lands last, not first."""
        original = "a\nb\nc\n"
        diff = "@@ -1,2 +1,3 @@\n a\n b\n+NEW\n"
        result = _apply_hunks(original, diff)
        assert result == "a\nb\nNEW\nc\n"

    def test_two_hunks_both_land_correctly(self):
        """The running offset stays right after a splice that changes length."""
        original = "a\nb\nc\nd\ne\nf\n"
        diff = (
            "@@ -1,2 +1,3 @@\n a\n+X\n b\n"
            "@@ -5,2 +6,3 @@\n e\n+Y\n f\n"
        )
        result = _apply_hunks(original, diff)
        assert result == "a\nX\nb\nc\nd\ne\nY\nf\n"

    def test_pure_deletion_hunk_removes_only_its_line(self):
        original = "a\nb\nc\n"
        diff = "@@ -2,1 +2,0 @@\n-b\n"
        result = _apply_hunks(original, diff)
        assert result == "a\nc\n"

    def test_no_newline_marker_does_not_swallow_following_line(self):
        """`\\ No newline at end of file` consumes no original line."""
        original = "a\nb\nc\n"
        diff = (
            "@@ -1,3 +1,3 @@\n"
            " a\n"
            "-b\n"
            "+B\n"
            "\\ No newline at end of file\n"
            " c\n"
        )
        result = _apply_hunks(original, diff)
        assert result == "a\nB\nc\n"

    def test_zero_count_hunk_inserts_after_its_header_line(self):
        """`@@ -1,0 +2 @@` is git's own header for inserting between a and b."""
        original = "a\nb\nc\n"
        diff = "@@ -1,0 +2 @@\n+X\n"
        result = _apply_hunks(original, diff)
        assert result == "a\nX\nb\nc\n"

    def test_zero_count_hunk_at_line_zero_prepends(self):
        """`@@ -0,0 +1 @@` is a PREPEND that silently became an APPEND.

        `orig_start` was -1, so `result_lines[-1:-1]` spliced before the
        trailing element and the line landed at the end of the file (R-0312).
        """
        original = "a\nb\nc\n"
        diff = "@@ -0,0 +1 @@\n+X\n"
        result = _apply_hunks(original, diff)
        assert result == "X\na\nb\nc\n"

    def test_zero_count_hunk_past_last_line_appends(self):
        original = "a\nb\nc\n"
        diff = "@@ -3,0 +4 @@\n+X\n"
        result = _apply_hunks(original, diff)
        assert result == "a\nb\nc\nX\n"

    def test_two_zero_count_hunks_both_land_correctly(self):
        """The running offset survives a splice that consumes no original line."""
        original = "a\nb\nc\n"
        diff = "@@ -1,0 +2 @@\n+X\n@@ -2,0 +4 @@\n+Y\n"
        result = _apply_hunks(original, diff)
        assert result == "a\nX\nb\nY\nc\n"

    def test_zero_count_header_with_consuming_body_rejects(self):
        """A header contradicting its own body is rejected, not guessed at.

        The repeated `a` makes the context line MATCH at the shifted index, so
        this proves the old-count rejection and not the context validation.
        """
        original = "a\na\nb\n"
        diff = "@@ -1,0 +2 @@\n a\n+X\n"
        result = _apply_hunks(original, diff)
        assert result is None

    def test_negative_splice_index_rejects(self):
        """`@@ -0,1 @@` names line 0 with a non-zero old count: index -1."""
        original = "a\nb\n"
        diff = "@@ -0,1 +0,2 @@\n+X\n"
        result = _apply_hunks(original, diff)
        assert result is None

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
