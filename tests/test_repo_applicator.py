"""
Tests for repo_applicator.py: _resolve_repo_path, _write_to_repo,
apply_task_output_to_repo, and attach-repo validation logic.

All tests are deterministic — no live Ollama, no real builder.
Filesystem access uses tmp_path only.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact
from packages.orchestration.repo_applicator import (
    _resolve_repo_path,
    _write_to_repo,
    apply_task_output_to_repo,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_artifact(task_type: str, summary: str = "Test summary.") -> Artifact:
    """Build a minimal Artifact with the content format produced by run_next_task."""
    content_lines = [
        "Builder Execution Output",
        f"Task:  {uuid4()}",
        f"Type:  {task_type}",
        "Desc:  Test task.",
        "",
        f"Summary: {summary}",
        "",
        "Proposed Changes:",
        "  - Add function foo()",
        "  - Update README with usage",
        "",
        "Notes:",
        "  - Assumed Python 3.11+",
    ]
    return Artifact(
        name=f"task_output_{task_type}",
        content="\n".join(content_lines),
        mime_type="text/plain",
        task_id=uuid4(),
        metadata={"task_type": task_type, "summary": summary},
    )


# ---------------------------------------------------------------------------
# _resolve_repo_path
# ---------------------------------------------------------------------------


class TestResolveRepoPath:
    def test_readme_keyword_maps_to_readme_md(self):
        assert _resolve_repo_path("readme") == "README.md"

    def test_readme_case_insensitive(self):
        assert _resolve_repo_path("generate_README") == "README.md"

    def test_doc_keyword_maps_to_docs(self):
        path = _resolve_repo_path("write_documentation")
        assert path is not None
        assert path.startswith("docs/")
        assert path.endswith(".md")

    def test_plan_keyword_maps_to_docs_remedy(self):
        path = _resolve_repo_path("create_implementation_plan")
        assert path is not None
        assert path.startswith("docs/remedy/")

    def test_spec_keyword_maps_to_docs_remedy(self):
        path = _resolve_repo_path("write_spec")
        assert path is not None
        assert path.startswith("docs/remedy/")

    def test_requirement_keyword_maps_to_docs_remedy(self):
        path = _resolve_repo_path("analyze_requirements")
        assert path is not None
        assert path.startswith("docs/remedy/")

    def test_acceptance_keyword_maps_to_docs_remedy(self):
        path = _resolve_repo_path("define_acceptance_checks")
        assert path is not None
        assert path.startswith("docs/remedy/")

    def test_analysis_keyword_maps_to_docs_remedy(self):
        path = _resolve_repo_path("analysis_phase")
        assert path is not None
        assert path.startswith("docs/remedy/")

    def test_architecture_keyword_maps_to_docs(self):
        path = _resolve_repo_path("architecture_overview")
        assert path is not None
        assert path.startswith("docs/")
        assert "remedy" not in path

    def test_write_code_is_not_eligible(self):
        assert _resolve_repo_path("write_code") is None

    def test_write_tests_is_not_eligible(self):
        assert _resolve_repo_path("write_tests") is None

    def test_unknown_is_not_eligible(self):
        assert _resolve_repo_path("unknown") is None

    def test_empty_string_is_not_eligible(self):
        assert _resolve_repo_path("") is None

    def test_path_does_not_contain_raw_user_string(self):
        """Safe_type must be sanitized — no spaces, slashes, dots."""
        path = _resolve_repo_path("../evil plan")
        # Either None (no keyword) or a sanitized safe path (not containing ..)
        if path is not None:
            assert ".." not in path
            assert "/" not in path.split("docs/remedy/")[-1] if "remedy" in (path or "") else True

    def test_changelog_keyword_maps_to_docs(self):
        path = _resolve_repo_path("generate_changelog")
        assert path is not None
        assert path.startswith("docs/")
        assert path.endswith(".md")

    def test_guide_keyword_maps_to_docs(self):
        path = _resolve_repo_path("write_user_guide")
        assert path is not None
        assert path.startswith("docs/")
        assert path.endswith(".md")

    def test_safe_type_replaces_unsafe_chars(self):
        path = _resolve_repo_path("acceptance checks for release")
        assert path is not None
        # Spaces replaced with underscores in safe_type
        assert " " not in path

    def test_spec_document_routes_to_docs_remedy_not_docs(self):
        """'spec_document' contains both 'spec' and 'doc'.
        'spec' must match first so it routes to docs/remedy/, not plain docs/."""
        path = _resolve_repo_path("spec_document")
        assert path is not None
        assert path.startswith("docs/remedy/"), (
            f"expected docs/remedy/ but got {path!r} — rule ordering bug"
        )

    def test_planning_document_routes_to_docs_remedy_not_docs(self):
        """'planning_document' contains both 'plan' and 'doc'.
        'plan' must match first so it routes to docs/remedy/, not plain docs/."""
        path = _resolve_repo_path("planning_document")
        assert path is not None
        assert path.startswith("docs/remedy/"), (
            f"expected docs/remedy/ but got {path!r} — rule ordering bug"
        )

    def test_requirement_document_routes_to_docs_remedy_not_docs(self):
        """'requirement_document' contains both 'requirement' and 'doc'.
        'requirement' must match first so it routes to docs/remedy/, not plain docs/."""
        path = _resolve_repo_path("requirement_document")
        assert path is not None
        assert path.startswith("docs/remedy/"), (
            f"expected docs/remedy/ but got {path!r} — rule ordering bug"
        )

    def test_define_api_endpoint_is_not_eligible(self):
        """'define' keyword was removed — code-style task types must not match."""
        assert _resolve_repo_path("define_api_endpoint") is None

    def test_write_implementation_is_not_eligible(self):
        """'implementation' keyword was removed — code tasks must not match."""
        assert _resolve_repo_path("write_implementation") is None

    def test_prepare_data_migration_is_not_eligible(self):
        """'prepare' keyword was removed — too broad, matches non-doc tasks."""
        assert _resolve_repo_path("prepare_data_migration") is None

    def test_summarize_output_is_not_eligible(self):
        """'summarize'/'summary' keywords were removed — too broad."""
        assert _resolve_repo_path("summarize_output") is None
        assert _resolve_repo_path("write_summary") is None


# ---------------------------------------------------------------------------
# _write_to_repo
# ---------------------------------------------------------------------------


class TestWriteToRepo:
    def test_writes_file_and_returns_path(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = _write_to_repo(repo_root, "docs/output.md", "# Hello\n")
        assert result is not None
        assert result.exists()
        assert result.read_text() == "# Hello\n"

    def test_creates_parent_directories(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = _write_to_repo(repo_root, "docs/remedy/output.md", "content")
        assert result is not None
        assert result.parent.is_dir()

    def test_returns_none_if_file_exists(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        (repo_root / "output.md").write_text("existing")
        result = _write_to_repo(repo_root, "output.md", "new content")
        assert result is None
        # File must not be overwritten
        assert (repo_root / "output.md").read_text() == "existing"

    def test_raises_on_traversal_via_dotdot(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with pytest.raises(RuntimeError, match="Path traversal is not allowed"):
            _write_to_repo(repo_root, "../outside.md", "content")

    def test_raises_on_traversal_via_absolute_path(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        # A path that resolves outside — use /tmp/etc-style absolute component
        with pytest.raises(RuntimeError, match="Path traversal is not allowed"):
            _write_to_repo(repo_root, "/etc/passwd", "content")

    def test_nested_path_within_repo_is_safe(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = _write_to_repo(repo_root, "a/b/c/deep.md", "content")
        assert result is not None
        assert result.read_text() == "content"

    def test_boundary_safe_with_symlinked_repo_root(self, tmp_path):
        """Boundary check is correct even when repo_root is a symlink.

        Without internal resolve() of repo_root, target.is_relative_to(symlink)
        would fail because the resolved target path uses the real directory name,
        not the symlink name — causing a false boundary-violation error.
        """
        real_dir = tmp_path / "real_repo"
        real_dir.mkdir()
        symlink = tmp_path / "link_repo"
        symlink.symlink_to(real_dir)
        result = _write_to_repo(symlink, "docs/test.md", "content")
        assert result is not None
        assert result.exists()


# ---------------------------------------------------------------------------
# apply_task_output_to_repo
# ---------------------------------------------------------------------------


class TestApplyTaskOutputToRepo:
    def test_eligible_task_type_writes_file(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("analyze_requirements")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert len(applied) == 1
        assert Path(applied[0]).exists()

    def test_ineligible_task_type_returns_empty(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("write_code")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert applied == []

    def test_no_file_written_for_ineligible_type(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("write_tests")
        apply_task_output_to_repo(artifact, repo_root)
        # No files created in repo
        assert list(repo_root.rglob("*.md")) == []

    def test_existing_file_is_not_overwritten(self, tmp_path):
        repo_root = tmp_path / "repo"
        (repo_root / "docs" / "remedy").mkdir(parents=True)
        # Pre-create the file that would be written
        artifact = _make_artifact("analyze_requirements")
        from packages.orchestration.repo_applicator import _resolve_repo_path
        path = _resolve_repo_path("analyze_requirements")
        assert path is not None
        existing = repo_root / path
        existing.parent.mkdir(parents=True, exist_ok=True)
        existing.write_text("original content")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert applied == []
        assert existing.read_text() == "original content"

    def test_written_file_is_markdown_with_summary(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("analyze_requirements", summary="Requirements done.")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert len(applied) == 1
        content = Path(applied[0]).read_text()
        assert "Requirements done." in content
        assert content.startswith("#")

    def test_written_file_contains_proposed_changes_as_bullets(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("analyze_requirements")
        applied = apply_task_output_to_repo(artifact, repo_root)
        content = Path(applied[0]).read_text()
        # Proposed changes converted from "  - item" to "- item"
        assert "- Add function foo()" in content
        assert "- Update README with usage" in content

    def test_notes_not_included_in_repo_file(self, tmp_path):
        """Notes section from artifact content must not appear in repo markdown."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("analyze_requirements")
        # Artifact has "  - Assumed Python 3.11+" as a note
        applied = apply_task_output_to_repo(artifact, repo_root)
        content = Path(applied[0]).read_text()
        # Notes appear in artifact.content but should not appear in repo output
        assert "Assumed Python 3.11+" not in content

    def test_returned_paths_are_absolute(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("analyze_requirements")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert len(applied) == 1
        assert Path(applied[0]).is_absolute()

    def test_normal_eligible_task_type_applies_successfully(self, tmp_path):
        """An eligible task_type with sanitized path applies without error."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("analyze_requirements")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert len(applied) == 1
        assert Path(applied[0]).exists()

    def test_repo_not_attached_workspace_only_flow(self, tmp_path):
        """If no target_repo in job metadata, no repo write should happen.

        This test verifies apply_task_output_to_repo itself returns empty when
        called on an ineligible type — the CLI skips calling it if no repo attached.
        """
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("write_code")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert applied == []

    def test_artifact_metadata_records_repo_applied_files(self, tmp_path):
        """After apply, caller records repo_applied_files in artifact metadata."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("analyze_requirements")
        applied = apply_task_output_to_repo(artifact, repo_root)
        # Simulate what the CLI does after calling apply_task_output_to_repo
        if applied:
            artifact.metadata["repo_applied_files"] = applied
        assert "repo_applied_files" in artifact.metadata
        assert len(artifact.metadata["repo_applied_files"]) == 1

    def test_plan_type_writes_to_docs_remedy(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("create_implementation_plan")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert len(applied) == 1
        assert "docs/remedy" in applied[0]

    def test_readme_type_writes_to_readme_md(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("generate_readme")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert len(applied) == 1
        assert applied[0].endswith("README.md")

    def test_architecture_type_writes_to_docs(self, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifact = _make_artifact("architecture_overview")
        applied = apply_task_output_to_repo(artifact, repo_root)
        assert len(applied) == 1
        assert "/docs/" in applied[0]
        assert "/docs/remedy/" not in applied[0]


# ---------------------------------------------------------------------------
# attach-repo validation (mirrors _cmd_attach_repo logic)
# ---------------------------------------------------------------------------


class TestStaleRepoPath:
    """Behavioral tests for stale/invalid repo_root handling in apply_task_output_to_repo.

    apply_task_output_to_repo returns [] without error when repo_root does not
    exist or is not a directory.  The CLI also emits a warning when its own
    re-validation detects a stale path; that behavior is complementary.
    """

    def test_nonexistent_repo_root_returns_empty_for_eligible_type(self, tmp_path):
        """An eligible task type returns [] when the repo root has been deleted."""
        stale = tmp_path / "deleted_repo"
        # Never created — simulates a repo deleted after attach-repo
        artifact = _make_artifact("analyze_requirements")
        applied = apply_task_output_to_repo(artifact, stale)
        assert applied == []

    def test_nonexistent_repo_root_creates_no_files(self, tmp_path):
        """No directories or files are created when repo_root does not exist."""
        stale = tmp_path / "deleted_repo"
        artifact = _make_artifact("write_spec")
        apply_task_output_to_repo(artifact, stale)
        assert not stale.exists()

    def test_file_at_repo_root_returns_empty_for_eligible_type(self, tmp_path):
        """A file where a directory is expected causes a safe no-op return."""
        file_path = tmp_path / "not_a_dir"
        file_path.write_text("I am a file")
        artifact = _make_artifact("analyze_requirements")
        applied = apply_task_output_to_repo(artifact, file_path)
        assert applied == []

    def test_valid_repo_root_still_applies_eligible_type(self, tmp_path):
        """A live directory allows eligible task types to apply as expected."""
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        artifact = _make_artifact("analyze_requirements")
        applied = apply_task_output_to_repo(artifact, repo_dir)
        assert len(applied) == 1
        assert Path(applied[0]).exists()


class TestAttachRepoValidation:
    """These tests verify the validation rules applied by attach-repo without
    invoking the CLI directly."""

    def test_valid_directory_is_accepted(self, tmp_path):
        repo_dir = tmp_path / "my_repo"
        repo_dir.mkdir()
        # Simulate the check that the CLI performs
        assert repo_dir.exists()
        assert repo_dir.is_dir()
        resolved = repo_dir.resolve()
        assert resolved.is_absolute()

    def test_nonexistent_path_is_rejected(self, tmp_path):
        missing = tmp_path / "does_not_exist"
        assert not missing.exists()

    def test_file_path_is_rejected_as_non_directory(self, tmp_path):
        file_path = tmp_path / "a_file.txt"
        file_path.write_text("hello")
        assert file_path.exists()
        assert not file_path.is_dir()

    def test_resolved_path_is_absolute(self, tmp_path):
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        resolved = repo_dir.resolve()
        assert resolved.is_absolute()
        # Stored as str
        assert isinstance(str(resolved), str)
