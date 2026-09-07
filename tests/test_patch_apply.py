"""
Tests for packages/orchestration/patch_apply.py — Step 30: Approved Patch Apply v0.

Test categories:
  1. Safety / path validation
  2. Approval / risk validation
  3. Permission checks
  4. Apply behavior (create / modify / idempotency)
  5. Apply record persistence
  6. Run log events
  7. CLI (apply-patch-intent)
  8. Trust report integration
  9. Timeline integration
 10. Brain integration (patch_apply node / edge / detail / viewer)
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from uuid import UUID, uuid4

import pytest

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------
from packages.core.models import Artifact, ArtifactKind, Job
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    APPROVAL_REJECTED,
    make_intent_id,
    set_approval_state,
)
from packages.orchestration.markdown_output_safety import (
    neutralize_markdown_html_comment_start as _neutralize_markdown_html_comment_start,
)
from packages.orchestration.patch_apply import (
    _build_create_content,
    _build_modify_section,
    apply_patch_intent,
    format_apply_result,
)
from packages.orchestration.patch_intent import RISK_HIGH, RISK_LOW, RISK_MEDIUM, RISK_UNKNOWN
from packages.orchestration.permissions import Capability, set_permission


def _make_job(*, with_repo: bool = True, tmp_repo: Path | None = None) -> tuple[Job, Path | None]:
    """Create a minimal job, optionally with a target_repo attached."""
    job = Job(name="test apply job")
    repo: Path | None = None
    if with_repo:
        repo = tmp_repo or Path(tempfile.mkdtemp())
        job.metadata["target_repo"] = str(repo)
    return job, repo


def _add_artifact(
    job: Job,
    *,
    action: str = "modify",
    risk: str = RISK_LOW,
    target_path: str = "README.md",
    proposed: list[str] | None = None,
) -> str:
    """Add an artifact with a patch intent explanation; return intent_id."""
    proposed = proposed or ["Update summary", "Add details"]
    proposed_block = "\n".join(f"  - {ln}" for ln in proposed)
    content = (
        f"Summary:\n  Generated output\nProposed Changes:\n{proposed_block}\nNotes:\n  none\n"
    )
    artifact = Artifact(
        name="test artifact",
        content=content,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=uuid4(),
        metadata={
            "patch_intent_explanations": [
                {
                    "file": target_path,
                    "action": action,
                    "risk": risk,
                    "reason": "task type 'test'",
                    "summary": "test intent",
                }
            ]
        },
    )
    job.artifacts.append(artifact)
    return make_intent_id(artifact.id, 0)


def _approve(job: Job, intent_id: str) -> None:
    set_approval_state(job, intent_id, APPROVAL_APPROVED)


def _grant_repo_write(job: Job) -> None:
    set_permission(job, Capability.repo_generated_write, allow=True)


# ---------------------------------------------------------------------------
# 1. Safety / path validation
# ---------------------------------------------------------------------------


class TestPathSafety:
    def test_rejects_absolute_path(self, tmp_path):
        job, repo = _make_job(tmp_repo=tmp_path)
        _add_artifact(job, target_path="/etc/passwd", action="create")
        intent_id = _add_artifact(job, target_path="/etc/passwd", action="create")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "absolute" in result.blocked_reason or "path" in result.blocked_reason.lower()

    def test_rejects_traversal_path(self, tmp_path):
        job, repo = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, target_path="../escape.md", action="create")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "traversal" in result.blocked_reason or "path" in result.blocked_reason.lower()

    def test_rejects_null_byte_path(self, tmp_path):
        job, repo = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, target_path="docs/\x00evil.md", action="create")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "null" in result.blocked_reason or "path" in result.blocked_reason.lower()

    def test_rejects_non_md_extension(self, tmp_path):
        job, repo = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, target_path="README.py", action="create")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "file_type" in result.blocked_reason or "unsupported" in result.blocked_reason

    def test_resolved_target_must_stay_in_repo_root(self, tmp_path):
        # Traversal via ".." components — blocked by _validate_target_path
        job, repo = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, target_path="a/../../outside.md", action="create")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"

    def test_symlink_escape_blocked(self, tmp_path):
        """A symlink inside repo_root pointing outside must be blocked.

        This exercises the resolved_target.is_relative_to(resolved_root) guard
        (section 6 of apply_patch_intent), not the '..' component guard in
        _validate_target_path.  The path 'escape/file.md' contains no '..', so
        _validate_target_path passes — but resolution of the symlink moves
        outside the repo, which the boundary guard catches.
        """
        # Create repo and an external directory that a symlink will point at
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        external_dir = tmp_path / "external"
        external_dir.mkdir()

        # Create the symlink inside the repo pointing outside it
        symlink = repo_dir / "escape"
        try:
            symlink.symlink_to(external_dir)
        except (OSError, NotImplementedError):
            pytest.skip("symlink creation not available on this platform")

        job = __import__("packages.core.models", fromlist=["Job"]).Job(name="symlink test")
        job.metadata["target_repo"] = str(repo_dir)

        # Build an intent pointing at escape/file.md — passes path component checks
        # but resolves to external_dir/file.md (outside repo_dir)
        from uuid import uuid4

        from packages.core.models import Artifact, ArtifactKind
        from packages.orchestration.approval_queue import APPROVAL_APPROVED, make_intent_id, set_approval_state
        from packages.orchestration.permissions import Capability, set_permission
        artifact = Artifact(
            name="symlink test artifact",
            content="Summary:\n  test\nProposed Changes:\n  - bullet\n",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={
                "patch_intent_explanations": [{
                    "file": "escape/file.md",
                    "action": "create",
                    "risk": "low",
                    "reason": "test",
                    "summary": "test",
                }]
            },
        )
        job.artifacts.append(artifact)
        intent_id = make_intent_id(artifact.id, 0)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        set_permission(job, Capability.repo_generated_write, allow=True)

        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)

        # Must be blocked — boundary guard fires
        assert result.state == "blocked", f"expected blocked, got {result.state!r}"
        assert result.blocked_reason == "unsafe_path", (
            f"expected unsafe_path but got {result.blocked_reason!r}"
        )
        # External file must not have been created
        assert not (external_dir / "file.md").exists()
        # Run log event must still be emitted (structurally)
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = []
        if runs_dir.exists():
            for jsonl in sorted(runs_dir.glob("*.jsonl")):
                for line in jsonl.read_text().splitlines():
                    if line.strip():
                        import json as _json
                        ev = _json.loads(line)
                        if ev.get("event") == "patch_intent_applied":
                            events.append(ev)
        assert events, "expected patch_intent_applied run-log event even on blocked result"
        assert events[0]["metadata"]["outcome"] == "blocked"

    def test_valid_relative_md_path_accepted(self, tmp_path):
        job, repo = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, target_path="docs/README.md", action="create", risk=RISK_LOW
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"

    def test_subdirectory_path_created(self, tmp_path):
        job, repo = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, target_path="docs/sub/page.md", action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        assert (tmp_path / "docs" / "sub" / "page.md").exists()


# ---------------------------------------------------------------------------
# 2. Approval / risk validation
# ---------------------------------------------------------------------------


class TestApprovalAndRisk:
    def test_rejects_pending_intent(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "not_approved" in result.blocked_reason

    def test_rejects_rejected_intent(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_REJECTED)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "not_approved" in result.blocked_reason

    def test_applies_approved_low_risk_create(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"

    def test_applies_approved_medium_risk_modify(self, tmp_path):
        job, repo = _make_job(tmp_repo=tmp_path)
        (tmp_path / "README.md").write_text("# Existing\n")
        intent_id = _add_artifact(job, action="modify", risk=RISK_MEDIUM, target_path="README.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"

    def test_rejects_high_risk(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_HIGH)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "unsupported_risk" in result.blocked_reason

    def test_rejects_unknown_risk(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_UNKNOWN)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "unsupported_risk" in result.blocked_reason

    def test_does_not_use_repo_overwrite_permission(self, tmp_path):
        """repo_overwrite must remain reserved — applying must not require it."""
        from packages.orchestration.permissions import Capability
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        # Explicitly deny repo_overwrite — must not affect apply
        set_permission(job, Capability.repo_overwrite, allow=False)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"

    def test_unknown_intent_returns_blocked(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        result = apply_patch_intent(job, "nonexistent-0", data_dir=tmp_path)
        assert result.state == "blocked"
        assert "intent_not_found" in result.blocked_reason


# ---------------------------------------------------------------------------
# 3. Permission checks
# ---------------------------------------------------------------------------


class TestPermissions:
    def test_rejects_without_repo_generated_write(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        # repo_generated_write NOT granted (default deny)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert result.blocked_reason == "permission_denied"

    def test_applies_with_repo_generated_write(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"

    def test_shell_exec_not_touched(self, tmp_path):
        """shell_exec capability must not be involved in apply."""
        from packages.orchestration.permissions import Capability, is_allowed
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        # shell_exec must remain deny (default)
        assert not is_allowed(job, Capability.shell_exec)

    def test_blocked_when_repo_missing(self, tmp_path):
        job, _ = _make_job(with_repo=False)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "repo_missing" in result.blocked_reason

    def test_blocked_when_repo_not_directory(self, tmp_path):
        fake = tmp_path / "notadir.txt"
        fake.write_text("not a dir")
        job = Job(name="test")
        job.metadata["target_repo"] = str(fake)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "repo_missing" in result.blocked_reason


# ---------------------------------------------------------------------------
# 4. Apply behavior
# ---------------------------------------------------------------------------


class TestApplyBehavior:
    def test_create_writes_new_markdown_file(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW, target_path="NEW.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        assert (tmp_path / "NEW.md").exists()

    def test_create_blocks_if_target_exists(self, tmp_path):
        (tmp_path / "EXISTING.md").write_text("pre-existing")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW, target_path="EXISTING.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "target_exists" in result.blocked_reason

    def test_modify_appends_section_to_existing_file(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello\n\nOriginal content.\n")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM, target_path="README.md"
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        content_after = (tmp_path / "README.md").read_text()
        assert "Original content." in content_after
        assert "## Proposed Update" in content_after
        assert "<!-- remedy:patch-intent" not in content_after
        assert intent_id not in content_after

    def test_modify_blocks_if_target_missing(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM, target_path="MISSING.md"
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert "target_missing" in result.blocked_reason

    def test_second_create_apply_is_noop(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW, target_path="NEW.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        r1 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r1.state == "applied"
        r2 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r2.state == "noop"
        assert r2.outcome == "already_applied"

    def test_second_modify_apply_is_noop(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello\n")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM, target_path="README.md"
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        r1 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r1.state == "applied"
        r2 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r2.state == "noop"
        assert r2.outcome == "already_applied"

    def test_existing_content_preserved_before_appended_section(self, tmp_path):
        original = "# Hello\n\nOriginal text must survive.\n"
        (tmp_path / "README.md").write_text(original)
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM, target_path="README.md"
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        content_after = (tmp_path / "README.md").read_text()
        assert content_after.startswith(original)

    def test_create_content_contains_proposed_lines(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="create", risk=RISK_LOW,
            target_path="NEW.md", proposed=["First bullet", "Second bullet"]
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        content = (tmp_path / "NEW.md").read_text()
        assert "First bullet" in content
        assert "Second bullet" in content

    def test_modify_section_contains_proposed_lines(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello\n")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM,
            target_path="README.md", proposed=["Alpha item", "Beta item"]
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        content = (tmp_path / "README.md").read_text()
        assert "Alpha item" in content
        assert "Beta item" in content

    def test_bytes_written_positive_on_apply(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.bytes_written > 0

    def test_line_count_positive_on_apply(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.line_count > 0

    def test_noop_bytes_written_is_zero(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        r2 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r2.bytes_written == 0
        assert r2.line_count == 0

    def test_modify_file_has_no_control_markers(self, tmp_path):
        """Modified files must contain no raw HTML comments, control markers, or intent IDs."""
        (tmp_path / "README.md").write_text("# Hello\n")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM,
            target_path="README.md", proposed=["Alpha", "Beta"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        content = (tmp_path / "README.md").read_text()
        assert "<!--" not in content
        assert "remedy:patch-intent" not in content
        assert intent_id not in content
        assert "Generated by Remedy" not in content
        assert "## Proposed Update" in content
        assert "Alpha" in content
        assert "Beta" in content

    def test_create_file_has_no_control_markers(self, tmp_path):
        """Created files must contain no raw HTML comments, control markers, or intent IDs."""
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="create", risk=RISK_LOW,
            target_path="NEW.md", proposed=["Gamma", "Delta"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert (tmp_path / "NEW.md").exists()
        content = (tmp_path / "NEW.md").read_text()
        assert "<!--" not in content
        assert "remedy:patch-intent" not in content
        assert intent_id not in content
        assert "Generated by Remedy" not in content
        assert "## Proposed Update" in content
        assert "Gamma" in content
        assert "Delta" in content

    def test_modify_control_marker_in_proposed_line_is_neutralized(self, tmp_path):
        """A proposed modify line containing a control marker prefix is neutralized.

        The apply must succeed, the active HTML comment must not appear verbatim,
        and the inert HTML-entity form must be present instead.
        """
        (tmp_path / "README.md").write_text("# Hello\n")
        job, _ = _make_job(tmp_repo=tmp_path)
        malicious_line = "<!-- remedy:patch-intent FAKEID begin -->"
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM,
            target_path="README.md",
            proposed=[malicious_line, "normal line"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        content = (tmp_path / "README.md").read_text()
        assert "<!--" not in content
        assert malicious_line not in content
        assert "&lt;!-- remedy:patch-intent" in content
        # Repeat apply is noop via metadata
        r2 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r2.state == "noop"

    def test_create_control_marker_in_proposed_line_is_neutralized(self, tmp_path):
        """A proposed create line containing a control marker prefix is neutralized.

        Exercises _build_create_content.  Active HTML comment must not appear.
        """
        job, _ = _make_job(tmp_repo=tmp_path)
        malicious_line = "<!-- remedy:patch-intent FAKEID begin -->"
        intent_id = _add_artifact(
            job, action="create", risk=RISK_LOW,
            target_path="NEW.md",
            proposed=[malicious_line, "safe line"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        assert (tmp_path / "NEW.md").exists()
        content = (tmp_path / "NEW.md").read_text()
        assert "<!--" not in content
        assert malicious_line not in content
        assert "&lt;!-- remedy:patch-intent" in content
        # Repeat apply is noop via metadata
        r2 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r2.state == "noop"

    def test_metadata_idempotency_still_works_without_file_markers(self, tmp_path):
        """Idempotency is metadata-only — file content is never consulted.

        After the first apply, clear the file so it contains no marker-like text.
        The second apply must be a noop (metadata record is authoritative) and
        must not append a duplicate section.
        """
        (tmp_path / "README.md").write_text("# Hello\n")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM,
            target_path="README.md", proposed=["Content"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        r1 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r1.state == "applied"
        # Overwrite the file to remove everything (simulates content replacement)
        (tmp_path / "README.md").write_text("# Cleared\n")
        # Second apply must be noop — metadata record is authoritative
        r2 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert r2.state == "noop"
        assert r2.outcome == "already_applied"
        # File must not have received a duplicate section
        final_content = (tmp_path / "README.md").read_text()
        assert final_content == "# Cleared\n"

    # -- Newline contract ----------------------------------------------------

    def test_build_modify_section_ends_with_exactly_one_newline(self):
        section = _build_modify_section(["line A", "line B"])
        assert section.endswith("\n"), "section must end with a newline"
        assert not section.endswith("\n\n"), "section must not end with double newline"

    def test_build_create_content_ends_with_exactly_one_newline(self):
        content = _build_create_content("my_doc.md", ["line A", "line B"])
        assert content.endswith("\n"), "create content must end with a newline"
        assert not content.endswith("\n\n"), "create content must not end with double newline"

    def test_modify_appended_text_ends_with_exactly_one_newline(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello\n")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM,
            target_path="README.md", proposed=["Alpha"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        content = (tmp_path / "README.md").read_text()
        assert content.endswith("\n"), "applied modify file must end with a newline"
        assert not content.endswith("\n\n"), "applied modify file must not end with double newline"

    def test_create_applied_file_ends_with_exactly_one_newline(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="create", risk=RISK_LOW,
            target_path="NEW.md", proposed=["Gamma"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        content = (tmp_path / "NEW.md").read_text()
        assert content.endswith("\n"), "created file must end with a newline"
        assert not content.endswith("\n\n"), "created file must not end with double newline"

    # -- Generalized HTML comment neutralization ----------------------------

    def test_neutralize_markdown_html_comment_start_remedy_marker(self):
        result = _neutralize_markdown_html_comment_start("<!-- remedy:patch-intent FAKE begin -->")
        assert result == "&lt;!-- remedy:patch-intent FAKE begin -->"

    def test_neutralize_markdown_html_comment_start_generic_comment(self):
        result = _neutralize_markdown_html_comment_start("<!-- generic comment -->")
        assert result == "&lt;!-- generic comment -->"

    def test_neutralize_markdown_html_comment_start_leaves_safe_form_unchanged(self):
        already_safe = "&lt;!-- already neutralized -->"
        result = _neutralize_markdown_html_comment_start(already_safe)
        assert result == already_safe

    def test_modify_generic_html_comment_in_proposed_line_is_neutralized(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello\n")
        job, _ = _make_job(tmp_repo=tmp_path)
        comment_line = "<!-- generic comment -->"
        intent_id = _add_artifact(
            job, action="modify", risk=RISK_MEDIUM,
            target_path="README.md",
            proposed=[comment_line, "normal line"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        content = (tmp_path / "README.md").read_text()
        assert "<!--" not in content
        assert comment_line not in content
        assert "&lt;!-- generic comment -->" in content

    def test_create_generic_html_comment_in_proposed_line_is_neutralized(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        comment_line = "<!-- generic comment -->"
        intent_id = _add_artifact(
            job, action="create", risk=RISK_LOW,
            target_path="NOTES.md",
            proposed=[comment_line, "safe line"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        content = (tmp_path / "NOTES.md").read_text()
        assert "<!--" not in content
        assert comment_line not in content
        assert "&lt;!-- generic comment -->" in content

    def test_create_title_derived_from_path_never_contains_raw_html_comment(self, tmp_path):
        """The create-file title derived from target_path never contains raw '<!--'.

        A path stem like 'test<!--doc' has its hyphens replaced with spaces by the
        title builder (so '<!--' becomes '<! '), which already prevents raw HTML
        comment starts in the title.  _neutralize is applied as a belt-and-suspenders
        output-boundary guard.  Either way the written file must be free of raw '<!--'.
        """
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="create", risk=RISK_LOW,
            target_path="test<!--doc.md",
            proposed=["normal line"],
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        content = (tmp_path / "test<!--doc.md").read_text()
        assert "<!--" not in content

    def test_build_create_content_title_never_contains_raw_html_comment(self):
        """_build_create_content output never contains raw '<!--' in the title.

        The '-' → ' ' replacement in the builder already breaks '<!--' in path-derived
        stems before _neutralize runs.  The invariant that matters: raw '<!--' must
        never appear in the returned content regardless of how it was prevented.
        """
        # "docs/readme<!--comment.md" — stem is "readme<!--comment"
        # After replace("-", " "): "readme<!  comment" — no "<!--" survives
        content = _build_create_content("docs/readme<!--comment.md", ["line"])
        assert "<!--" not in content


# ---------------------------------------------------------------------------
# 5. Apply record persistence
# ---------------------------------------------------------------------------


class TestApplyRecord:
    def _get_record(self, job: Job, intent_id: str) -> dict | None:
        for art in job.artifacts:
            records = art.metadata.get("patch_intent_apply_records", {})
            if intent_id in records:
                return records[intent_id]
        return None

    def test_apply_record_stored_after_apply(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        record = self._get_record(job, intent_id)
        assert record is not None
        assert record["state"] == "applied"

    def test_apply_record_has_required_keys(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        record = self._get_record(job, intent_id)
        for key in ("state", "applied_at", "target_path", "action", "bytes_written", "line_count", "reason"):
            assert key in record, f"missing key: {key}"

    def test_no_raw_artifact_content_in_record(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW,
                                   proposed=["SECRET_CONTENT_XYZ"])
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        record = self._get_record(job, intent_id)
        record_str = json.dumps(record)
        assert "SECRET_CONTENT_XYZ" not in record_str

    def test_no_approval_reason_in_record(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason="TOP_SECRET_REASON")
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        record = self._get_record(job, intent_id)
        record_str = json.dumps(record)
        assert "TOP_SECRET_REASON" not in record_str

    def test_no_diff_preview_in_record(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        record = self._get_record(job, intent_id)
        # record should only have schema-defined keys (proof is a nested dict, not raw content)
        allowed_keys = {"state", "applied_at", "target_path", "action",
                        "bytes_written", "line_count", "reason", "proof",
                        "snapshot_id", "snapshot_verified", "scope"}
        unexpected = set(record.keys()) - allowed_keys
        assert not unexpected, f"unexpected keys in record: {unexpected}"
        # proof must not contain raw file content, only structural hashes and counts
        proof = record.get("proof", {})
        if proof:
            raw_content_keys = {"content", "diff_preview", "approval_reason", "command_output"}
            assert not (set(proof.keys()) & raw_content_keys), \
                f"proof contains raw content keys: {set(proof.keys()) & raw_content_keys}"

    def test_apply_state_visible_after_reload(self, tmp_path):
        from packages.orchestration.storage import load_job
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied"
        # Reload and check record
        job2 = load_job(job.id, tmp_path)
        record = None
        for art in job2.artifacts:
            records = art.metadata.get("patch_intent_apply_records", {})
            if intent_id in records:
                record = records[intent_id]
        assert record is not None
        assert record["state"] == "applied"


# ---------------------------------------------------------------------------
# 6. Run log events
# ---------------------------------------------------------------------------


class TestRunLog:
    def _find_apply_event(self, tmp_path: Path, job_id: str) -> dict | None:
        runs_dir = tmp_path / "job_logs" / job_id
        if not runs_dir.exists():
            return None
        for jsonl in sorted(runs_dir.glob("*.jsonl")):
            for line in jsonl.read_text().splitlines():
                if line.strip():
                    ev = json.loads(line)
                    if ev.get("event") == "patch_intent_applied":
                        return ev
        return None

    def test_patch_intent_applied_event_emitted(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        ev = self._find_apply_event(tmp_path, str(job.id))
        assert ev is not None

    def test_run_log_exact_metadata_keys(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        ev = self._find_apply_event(tmp_path, str(job.id))
        meta = ev["metadata"]
        expected = {
            "intent_id",
            "target_path",
            "action",
            "outcome",
            "bytes_written",
            "line_count",
        }
        assert set(meta.keys()) == expected, (
            f"metadata keys mismatch — got {set(meta.keys())}, expected {expected}"
        )

    def test_run_log_outcome_applied(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        ev = self._find_apply_event(tmp_path, str(job.id))
        assert ev["metadata"]["outcome"] == "applied"

    def test_run_log_noop_emitted(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        # Second event should have outcome=noop
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = []
        for jsonl in sorted(runs_dir.glob("*.jsonl")):
            for line in jsonl.read_text().splitlines():
                if line.strip():
                    ev = json.loads(line)
                    if ev.get("event") == "patch_intent_applied":
                        events.append(ev)
        assert any(e["metadata"]["outcome"] == "noop" for e in events)

    def test_run_log_blocked_emitted(self, tmp_path):
        job, _ = _make_job(with_repo=False)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = []
        if runs_dir.exists():
            for jsonl in sorted(runs_dir.glob("*.jsonl")):
                for line in jsonl.read_text().splitlines():
                    if line.strip():
                        ev = json.loads(line)
                        if ev.get("event") == "patch_intent_applied":
                            events.append(ev)
        assert any(e["metadata"]["outcome"] == "blocked" for e in events)

    def test_no_raw_content_in_run_log(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW,
                                   proposed=["RUNLOG_SECRET_XYZ"])
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        ev = self._find_apply_event(tmp_path, str(job.id))
        ev_str = json.dumps(ev)
        assert "RUNLOG_SECRET_XYZ" not in ev_str

    def test_no_approval_reason_in_run_log(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason="MY_PRIVATE_REASON")
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        ev = self._find_apply_event(tmp_path, str(job.id))
        ev_str = json.dumps(ev)
        assert "MY_PRIVATE_REASON" not in ev_str

    def test_no_diff_preview_in_run_log(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        ev = self._find_apply_event(tmp_path, str(job.id))
        meta = ev["metadata"]
        # metadata must not contain diff_preview or patch content
        assert "diff_preview" not in meta
        assert "content" not in meta


# ---------------------------------------------------------------------------
# 7. CLI
# ---------------------------------------------------------------------------


class TestCLI:
    def _run_cli(self, *args):
        from unittest.mock import patch as mock_patch
        with mock_patch.object(sys, "argv", ["remedy", *[str(a) for a in args]]):
            from apps.cli.main import main
            try:
                main()
                return 0, "", ""
            except SystemExit as exc:
                return (exc.code or 0), "", ""

    def test_invalid_uuid_exits_1(self, tmp_path, capsys):
        code, _, _ = self._run_cli("patch", "apply", "not-a-uuid", "abc-0")
        assert code == 1

    def test_unknown_job_exits_1(self, tmp_path, capsys):
        code, _, _ = self._run_cli("patch", "apply", str(uuid4()), "abc-0")
        assert code == 1

    def test_pending_intent_exits_1(self, tmp_path):
        from packages.orchestration.storage import save_job
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _grant_repo_write(job)
        save_job(job)
        from unittest.mock import patch as mock_patch
        with mock_patch.object(sys, "argv", ["remedy", "patch", "apply", str(job.id), intent_id]):
            from apps.cli.main import main
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_approved_intent_applies(self, tmp_path, capsys):
        from packages.orchestration.storage import save_job
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        save_job(job)
        from unittest.mock import patch as mock_patch
        with mock_patch.object(sys, "argv", ["remedy", "patch", "apply", str(job.id), intent_id]):
            from apps.cli.main import main
            try:
                main()
            except SystemExit as e:
                if e.code and e.code != 0:
                    raise
        captured = capsys.readouterr()
        assert "Applied" in captured.out

    def test_no_traceback_on_failures(self, tmp_path, capsys):
        from unittest.mock import patch as mock_patch
        with mock_patch.object(sys, "argv", ["remedy", "patch", "apply", str(uuid4()), "abc-0"]):
            from apps.cli.main import main
            with pytest.raises(SystemExit):
                main()
        captured = capsys.readouterr()
        assert "Traceback" not in captured.err
        assert "Traceback" not in captured.out

    def test_stdout_does_not_echo_raw_content(self, tmp_path, capsys):
        from packages.orchestration.storage import save_job
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(
            job, action="create", risk=RISK_LOW, proposed=["STDOUT_SECRET_ZYX"]
        )
        _approve(job, intent_id)
        _grant_repo_write(job)
        save_job(job)
        from unittest.mock import patch as mock_patch
        with mock_patch.object(sys, "argv", ["remedy", "patch", "apply", str(job.id), intent_id]):
            from apps.cli.main import main
            try:
                main()
            except SystemExit:
                pass
        captured = capsys.readouterr()
        assert "STDOUT_SECRET_ZYX" not in captured.out

    def test_json_flag_produces_json(self, tmp_path, capsys):
        from packages.orchestration.storage import save_job
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        save_job(job)
        from unittest.mock import patch as mock_patch
        with mock_patch.object(sys, "argv", ["remedy", "patch", "apply", str(job.id), intent_id, "--json"]):
            from apps.cli.main import main
            try:
                main()
            except SystemExit:
                pass
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["state"] == "applied"
        assert "intent_id" in data


# ---------------------------------------------------------------------------
# 8. Trust report integration
# ---------------------------------------------------------------------------


class TestTrustReport:
    def test_applied_status_appears_structurally(self, tmp_path):
        from packages.orchestration.trust_report import summarize_trust_report
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = summarize_trust_report(job, [])
        assert "applied" in out.lower()

    def test_applied_outcome_shown_in_report(self, tmp_path):
        from packages.orchestration.trust_report import summarize_trust_report
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = summarize_trust_report(job, [])
        assert "outcome=applied" in out

    def test_no_content_in_trust_report(self, tmp_path):
        from packages.orchestration.trust_report import summarize_trust_report
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW,
                                   proposed=["TRUST_SECRET_ABC"])
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = summarize_trust_report(job, [])
        assert "TRUST_SECRET_ABC" not in out

    def test_no_approval_reason_in_trust_report(self, tmp_path):
        from packages.orchestration.trust_report import summarize_trust_report
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason="TRUST_PRIVATE_REASON")
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = summarize_trust_report(job, [])
        assert "TRUST_PRIVATE_REASON" not in out

    def test_apply_command_shown_when_unapplied(self, tmp_path):
        from packages.orchestration.trust_report import summarize_trust_report
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        out = summarize_trust_report(job, [])
        assert "patch apply" in out


# ---------------------------------------------------------------------------
# 9. Timeline integration
# ---------------------------------------------------------------------------


class TestTimeline:
    def _load_events(self, tmp_path: Path, job_id: str) -> list[dict]:
        from packages.orchestration.timeline import load_run_events
        return load_run_events(tmp_path, UUID(job_id))

    def test_patch_intent_applied_appears_in_timeline(self, tmp_path):
        from packages.orchestration.timeline import summarize_timeline
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._load_events(tmp_path, str(job.id))
        out = summarize_timeline(job, events)
        assert "patch intent applied" in out

    def test_timeline_shows_outcome_applied(self, tmp_path):
        from packages.orchestration.timeline import summarize_timeline
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._load_events(tmp_path, str(job.id))
        out = summarize_timeline(job, events)
        assert "outcome=applied" in out

    def test_timeline_shows_intent_id(self, tmp_path):
        from packages.orchestration.timeline import summarize_timeline
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._load_events(tmp_path, str(job.id))
        out = summarize_timeline(job, events)
        assert intent_id[:8] in out


# ---------------------------------------------------------------------------
# 10. Brain integration
# ---------------------------------------------------------------------------


class TestBrainIntegration:
    def _build_brain(self, job):
        from packages.orchestration.project_brain import build_project_brain
        return build_project_brain(job, [])

    def test_patch_apply_node_appears_after_apply(self, tmp_path):
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        types = [n.type for n in graph.nodes]
        assert NT_PATCH_APPLY in types

    def test_patch_apply_node_absent_without_apply(self):
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(with_repo=False)
        _add_artifact(job, action="create", risk=RISK_LOW)
        graph = self._build_brain(job)
        types = [n.type for n in graph.nodes]
        assert NT_PATCH_APPLY not in types

    def test_edge_applied_by_exists_after_apply(self, tmp_path):
        from packages.orchestration.project_brain import ET_APPLIED_BY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        edge_types = [e.type for e in graph.edges]
        assert ET_APPLIED_BY in edge_types

    def test_applied_by_edge_correct_source_target(self, tmp_path):
        from packages.orchestration.project_brain import ET_APPLIED_BY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_edges = [e for e in graph.edges if e.type == ET_APPLIED_BY]
        assert len(apply_edges) == 1
        assert apply_edges[0].source == f"pi:{intent_id}"
        assert apply_edges[0].target == f"apply:{intent_id}"

    def test_brain_node_detail_works_for_patch_apply(self, tmp_path):
        from packages.orchestration.brain_detail import (
            build_brain_node_detail,
            summarize_brain_node_detail,
        )
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_node = next(n for n in graph.nodes if n.type == NT_PATCH_APPLY)
        detail = build_brain_node_detail(job, graph, apply_node.id, [])
        assert detail.node_type == NT_PATCH_APPLY
        out = summarize_brain_node_detail(detail)
        assert "patch apply" in out.lower() or "apply" in out.lower()

    def test_brain_node_detail_no_patch_content(self, tmp_path):
        """Brain node detail for patch_apply must not render any of:
        artifact content, diff_preview, approval_reason, command_output,
        or raw exception text.
        """
        from packages.orchestration.brain_detail import (
            build_brain_node_detail,
            export_brain_node_detail_json,
            summarize_brain_node_detail,
        )
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW,
                                   proposed=["BRAIN_SECRET_789"])
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason="BRAIN_APPROVAL_REASON")
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_node = next(n for n in graph.nodes if n.type == NT_PATCH_APPLY)
        detail = build_brain_node_detail(job, graph, apply_node.id, [])
        text_out = summarize_brain_node_detail(detail)
        json_out = json.dumps(export_brain_node_detail_json(detail))
        for sentinel in ("BRAIN_SECRET_789", "BRAIN_APPROVAL_REASON",
                         "diff_preview", "command_output", "Traceback"):
            assert sentinel not in text_out, f"sentinel {sentinel!r} found in text output"
            assert sentinel not in json_out, f"sentinel {sentinel!r} found in JSON output"

    def test_brain_viewer_data_includes_patch_apply_node(self, tmp_path):
        from packages.orchestration.brain_viewer import build_brain_viewer_data
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        data = build_brain_viewer_data(job, graph, [])
        node_types = [n["type"] for n in data.graph["nodes"]]
        assert "patch_apply" in node_types

    def test_brain_viewer_json_no_sentinel_content(self, tmp_path):
        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data,
            export_brain_viewer_json,
        )
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW,
                                   proposed=["VIEWER_SECRET_999"])
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        data = build_brain_viewer_data(job, graph, [])
        exported = json.dumps(export_brain_viewer_json(data))
        assert "VIEWER_SECRET_999" not in exported

    def test_patch_apply_node_status_is_applied(self, tmp_path):
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_node = next(n for n in graph.nodes if n.type == NT_PATCH_APPLY)
        assert apply_node.status == "applied"


# ---------------------------------------------------------------------------
# PatchApplyResult shape
# ---------------------------------------------------------------------------


class TestPatchApplyResultShape:
    def test_result_is_frozen(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        with pytest.raises((AttributeError, TypeError)):
            result.state = "tampered"  # type: ignore[misc]

    def test_format_apply_result_applied(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW, target_path="NEW.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = format_apply_result(result)
        assert "Applied" in out
        assert "NEW.md" in out
        assert "v0" in out.lower() or "Markdown" in out

    def test_format_apply_result_noop(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        r2 = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = format_apply_result(r2)
        assert "No-op" in out or "noop" in out.lower()

    def test_format_apply_result_blocked_no_traceback(self, tmp_path):
        job, _ = _make_job(with_repo=False)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = format_apply_result(result)
        assert "Traceback" not in out


# ---------------------------------------------------------------------------
# 11. Apply Snapshot + Diff Proof (Step 31)
# ---------------------------------------------------------------------------


class TestApplyProof:
    """Tests for the proof snapshot stored in patch_intent_apply_records."""

    def _get_proof(self, job, intent_id: str) -> dict:
        for art in job.artifacts:
            record = art.metadata.get("patch_intent_apply_records", {}).get(intent_id, {})
            if record and "proof" in record:
                return record["proof"]
        return {}

    def test_proof_stored_in_apply_record_create(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        assert proof, "proof dict must be present in apply record after create"

    def test_proof_stored_in_apply_record_modify(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        (tmp_path / "README.md").write_text("# Existing\n", encoding="utf-8")
        intent_id = _add_artifact(job, action="modify", risk=RISK_LOW, target_path="README.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        assert proof, "proof dict must be present in apply record after modify"

    def test_proof_create_before_sha_is_empty_string(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        assert proof["before_sha256"] == "", (
            "before_sha256 must be empty string for create (file did not exist)"
        )

    def test_proof_after_sha_is_64_char_hex_create(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        sha = proof["after_sha256"]
        assert len(sha) == 64, f"after_sha256 must be 64-char hex, got {sha!r}"
        assert all(c in "0123456789abcdef" for c in sha), "after_sha256 must be lowercase hex"

    def test_proof_after_sha_is_64_char_hex_modify(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        (tmp_path / "README.md").write_text("# Existing\n", encoding="utf-8")
        intent_id = _add_artifact(job, action="modify", risk=RISK_LOW, target_path="README.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        sha = proof["after_sha256"]
        assert len(sha) == 64, f"after_sha256 must be 64-char hex, got {sha!r}"

    def test_proof_before_bytes_zero_for_create(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        assert proof["before_bytes"] == 0

    def test_proof_after_bytes_positive(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        assert proof["after_bytes"] > 0

    def test_proof_bytes_delta_positive_for_modify(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        (tmp_path / "README.md").write_text("# Existing\n", encoding="utf-8")
        intent_id = _add_artifact(job, action="modify", risk=RISK_LOW, target_path="README.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        assert proof["bytes_delta"] > 0, "bytes_delta must be positive after modify"

    def test_proof_before_sha_differs_from_after_sha_for_modify(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        (tmp_path / "README.md").write_text("# Existing\n", encoding="utf-8")
        intent_id = _add_artifact(job, action="modify", risk=RISK_LOW, target_path="README.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        assert proof["before_sha256"] != proof["after_sha256"], (
            "before and after SHA-256 must differ after modify"
        )

    def test_proof_all_expected_keys_present(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        expected_keys = {
            "before_sha256", "after_sha256",
            "before_bytes", "after_bytes", "bytes_delta",
            "before_line_count", "after_line_count", "line_delta",
        }
        assert expected_keys <= set(proof.keys()), (
            f"proof missing keys: {expected_keys - set(proof.keys())}"
        )

    def test_proof_not_stored_for_blocked_apply(self, tmp_path):
        job, _ = _make_job(with_repo=False)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        proof = self._get_proof(job, intent_id)
        assert proof == {}, "proof must not be stored for a blocked apply"


class TestRunLogProof:
    """Tests for the patch_apply_proof_recorded run-log event (Step 31)."""

    def _find_events_by_name(self, tmp_path: Path, job_id: str, ev_name: str) -> list[dict]:
        runs_dir = tmp_path / "job_logs" / job_id
        found = []
        if not runs_dir.exists():
            return found
        for jsonl in sorted(runs_dir.glob("*.jsonl")):
            for line in jsonl.read_text().splitlines():
                if line.strip():
                    ev = json.loads(line)
                    if ev.get("event") == ev_name:
                        found.append(ev)
        return found

    def test_proof_event_emitted_after_create(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._find_events_by_name(tmp_path, str(job.id), "patch_apply_proof_recorded")
        assert len(events) == 1, "exactly one proof event must be emitted after create"

    def test_proof_event_emitted_after_modify(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        (tmp_path / "README.md").write_text("# Existing\n", encoding="utf-8")
        intent_id = _add_artifact(job, action="modify", risk=RISK_LOW, target_path="README.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._find_events_by_name(tmp_path, str(job.id), "patch_apply_proof_recorded")
        assert len(events) == 1

    def test_proof_event_exact_metadata_keys(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._find_events_by_name(tmp_path, str(job.id), "patch_apply_proof_recorded")
        meta = events[0]["metadata"]
        expected = {
            "intent_id", "target_path", "action", "outcome",
            "before_sha256", "after_sha256",
            "before_bytes", "after_bytes", "bytes_delta",
            "before_line_count", "after_line_count", "line_delta",
            "applied_at",
        }
        assert set(meta.keys()) == expected, (
            f"proof event metadata keys mismatch — got {set(meta.keys())}, expected {expected}"
        )

    def test_proof_event_not_emitted_on_blocked(self, tmp_path):
        job, _ = _make_job(with_repo=False)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._find_events_by_name(tmp_path, str(job.id), "patch_apply_proof_recorded")
        assert len(events) == 0, "proof event must not be emitted for blocked apply"

    def test_proof_event_not_emitted_on_noop(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)  # noop
        events = self._find_events_by_name(tmp_path, str(job.id), "patch_apply_proof_recorded")
        assert len(events) == 1, "proof event must not be emitted on noop (second apply)"

    def test_proof_event_after_sha_is_valid_hex(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._find_events_by_name(tmp_path, str(job.id), "patch_apply_proof_recorded")
        sha = events[0]["metadata"]["after_sha256"]
        assert len(sha) == 64
        assert all(c in "0123456789abcdef" for c in sha)

    def test_proof_event_no_raw_content(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW,
                                   proposed=["PROOF_SECRET_XYZ"])
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._find_events_by_name(tmp_path, str(job.id), "patch_apply_proof_recorded")
        ev_str = json.dumps(events[0])
        assert "PROOF_SECRET_XYZ" not in ev_str


class TestBrainProof:
    """Tests for proof fields in the patch_apply Brain node (Step 31)."""

    def _build_brain(self, job):
        from packages.orchestration.project_brain import build_project_brain
        return build_project_brain(job, [])

    def test_patch_apply_node_has_after_sha256(self, tmp_path):
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_node = next(n for n in graph.nodes if n.type == NT_PATCH_APPLY)
        assert "after_sha256" in apply_node.metadata
        assert len(apply_node.metadata["after_sha256"]) == 64

    def test_patch_apply_node_has_before_sha256(self, tmp_path):
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_node = next(n for n in graph.nodes if n.type == NT_PATCH_APPLY)
        assert "before_sha256" in apply_node.metadata
        # For create, before_sha256 should be empty string
        assert apply_node.metadata["before_sha256"] == ""

    def test_patch_apply_node_bytes_delta_positive_for_create(self, tmp_path):
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_node = next(n for n in graph.nodes if n.type == NT_PATCH_APPLY)
        assert apply_node.metadata.get("bytes_delta", 0) > 0

    def test_brain_detail_shows_proof_hashes(self, tmp_path):
        from packages.orchestration.brain_detail import (
            build_brain_node_detail,
            summarize_brain_node_detail,
        )
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_node = next(n for n in graph.nodes if n.type == NT_PATCH_APPLY)
        detail = build_brain_node_detail(job, graph, apply_node.id, [])
        out = summarize_brain_node_detail(detail)
        assert "after_sha256" in out

    def test_brain_detail_proof_no_raw_file_content(self, tmp_path):
        from packages.orchestration.brain_detail import (
            build_brain_node_detail,
            export_brain_node_detail_json,
            summarize_brain_node_detail,
        )
        from packages.orchestration.project_brain import NT_PATCH_APPLY
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW,
                                   proposed=["BRAIN_PROOF_SECRET_ABC"])
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        graph = self._build_brain(job)
        apply_node = next(n for n in graph.nodes if n.type == NT_PATCH_APPLY)
        detail = build_brain_node_detail(job, graph, apply_node.id, [])
        text_out = summarize_brain_node_detail(detail)
        json_out = json.dumps(export_brain_node_detail_json(detail))
        assert "BRAIN_PROOF_SECRET_ABC" not in text_out
        assert "BRAIN_PROOF_SECRET_ABC" not in json_out


class TestTrustReportProof:
    """Tests for proof display in the Trust Report (Step 31)."""

    def test_trust_report_shows_proof_hashes_after_apply(self, tmp_path):
        from packages.orchestration.trust_report import summarize_trust_report
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = summarize_trust_report(job, [])
        assert "proof:" in out, "trust report must include proof line after apply"
        assert "after=" in out or "after_sha" in out or "after=" in out

    def test_trust_report_proof_no_raw_content(self, tmp_path):
        from packages.orchestration.trust_report import summarize_trust_report
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW,
                                   proposed=["TRUST_PROOF_SECRET_DEF"])
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        out = summarize_trust_report(job, [])
        assert "TRUST_PROOF_SECRET_DEF" not in out


class TestTimelineProof:
    """Tests for proof event rendering in the Timeline (Step 31)."""

    def _load_events(self, tmp_path: Path, job_id: str) -> list[dict]:
        from packages.orchestration.timeline import load_run_events
        return load_run_events(tmp_path, UUID(job_id))

    def test_proof_event_appears_in_timeline(self, tmp_path):
        from packages.orchestration.timeline import summarize_timeline
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._load_events(tmp_path, str(job.id))
        out = summarize_timeline(job, events)
        assert "patch apply proof" in out

    def test_proof_timeline_shows_sha(self, tmp_path):
        from packages.orchestration.timeline import summarize_timeline
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._load_events(tmp_path, str(job.id))
        out = summarize_timeline(job, events)
        assert "after_sha=" in out

    def test_proof_timeline_shows_deltas(self, tmp_path):
        from packages.orchestration.timeline import summarize_timeline
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        events = self._load_events(tmp_path, str(job.id))
        out = summarize_timeline(job, events)
        assert "Δbytes=" in out or "bytes=" in out


# ---------------------------------------------------------------------------
# Part A — Proof dict identity (Step 32 polish)
# ---------------------------------------------------------------------------


class TestProofDictIdentity:
    """Verify metadata proof and run-log proof are identical in value (Step 32).

    The proof dict is constructed once in apply_patch_intent and reused for
    both the artifact metadata 'proof' sub-key and the proof run-log event.
    These tests confirm the two sources report the same values.
    """

    def _get_metadata_proof(self, job, intent_id: str) -> dict:
        for art in job.artifacts:
            record = art.metadata.get("patch_intent_apply_records", {}).get(intent_id, {})
            if "proof" in record:
                return record["proof"]
        return {}

    def _get_runlog_proof(self, tmp_path: Path, job, intent_id: str) -> dict:
        runs_dir = tmp_path / "job_logs" / str(job.id)
        if not runs_dir.exists():
            return {}
        for jsonl in sorted(runs_dir.glob("*.jsonl")):
            for line in jsonl.read_text().splitlines():
                if not line.strip():
                    continue
                ev = json.loads(line)
                if (
                    ev.get("event") == "patch_apply_proof_recorded"
                    and ev.get("metadata", {}).get("intent_id") == intent_id
                ):
                    m = ev["metadata"]
                    return {
                        "before_sha256":     m["before_sha256"],
                        "after_sha256":      m["after_sha256"],
                        "before_bytes":      m["before_bytes"],
                        "after_bytes":       m["after_bytes"],
                        "bytes_delta":       m["bytes_delta"],
                        "before_line_count": m["before_line_count"],
                        "after_line_count":  m["after_line_count"],
                        "line_delta":        m["line_delta"],
                    }
        return {}

    def test_create_metadata_and_runlog_before_sha_identical(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        mp = self._get_metadata_proof(job, intent_id)
        rp = self._get_runlog_proof(tmp_path, job, intent_id)
        assert mp["before_sha256"] == rp["before_sha256"]

    def test_create_metadata_and_runlog_after_sha_identical(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        mp = self._get_metadata_proof(job, intent_id)
        rp = self._get_runlog_proof(tmp_path, job, intent_id)
        assert mp["after_sha256"] == rp["after_sha256"]

    def test_create_metadata_and_runlog_bytes_delta_identical(self, tmp_path):
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="create", risk=RISK_LOW)
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        mp = self._get_metadata_proof(job, intent_id)
        rp = self._get_runlog_proof(tmp_path, job, intent_id)
        assert mp["bytes_delta"] == rp["bytes_delta"]

    def test_modify_metadata_and_runlog_line_delta_identical(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello\n", encoding="utf-8")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="modify", risk=RISK_LOW, target_path="README.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        mp = self._get_metadata_proof(job, intent_id)
        rp = self._get_runlog_proof(tmp_path, job, intent_id)
        assert mp["line_delta"] == rp["line_delta"]

    def test_modify_metadata_before_sha_matches_runlog_before_sha(self, tmp_path):
        (tmp_path / "README.md").write_text("# Before content\n", encoding="utf-8")
        job, _ = _make_job(tmp_repo=tmp_path)
        intent_id = _add_artifact(job, action="modify", risk=RISK_LOW, target_path="README.md")
        _approve(job, intent_id)
        _grant_repo_write(job)
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        mp = self._get_metadata_proof(job, intent_id)
        rp = self._get_runlog_proof(tmp_path, job, intent_id)
        assert mp["before_sha256"] == rp["before_sha256"]
        # For modify the before_sha must be non-empty (file existed)
        assert mp["before_sha256"] != ""
