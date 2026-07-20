"""
Repository attachment and safe generated-file application.

Provides apply_task_output_to_repo() — the only public entry point — which
writes eligible task output as a markdown file into a user-attached target
repository.

Design constraints:
  - No arbitrary LLM paths: task_type is matched against the task registry
    (packages/orchestration/task_registry.py).  If the registry returns
    repo_route=None, no file is written.
  - No source code edits: only new markdown files under docs/ or README.md.
  - No overwriting: if the target path already exists, the write is skipped
    silently and an empty list is returned.
  - No shell execution, no Git operations, no patch application.
  - Repo writes are boundary-safe: the resolved target must remain inside
    repo_root. Boundary violations raise RuntimeError regardless of how the
    caller constructed the relative path.

Repo file format:
  Each eligible task produces one markdown file whose content is derived from
  the artifact's metadata (task_type, summary) and content (proposed changes
  in "  - item" format, converted to "- item" markdown bullets).

Relationship to workspace:
  The workspace is Remedy-owned (under .data/workspaces/<job_id>/). The target
  repository is user-owned. These are separate; this module bridges the two
  only for eligible, safely mapped task output. workspace_file and
  repo_applied_files are recorded as separate metadata keys on the artifact.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from packages.core.models import Artifact
from packages.orchestration.markdown_output_safety import (
    neutralize_markdown_html_comment_start as _neutralize,
)
from packages.orchestration.task_registry import get_task_type_spec

if TYPE_CHECKING:
    from packages.core.models import Job


def _resolve_repo_path(task_type: str) -> str | None:
    """Return the fully-resolved repo-relative path for task_type, or None.

    Delegates to get_task_type_spec() — the task registry is the single source
    of routing truth.  Returns None if the spec has no repo_route (unknown or
    non-doc task types).
    """
    return get_task_type_spec(task_type).repo_route


# ---------------------------------------------------------------------------
# Boundary-safe repo write
# ---------------------------------------------------------------------------


def _write_to_repo(repo_root: Path, relative_path: str, content: str) -> Path | None:
    """Write content to a path inside repo_root with boundary enforcement.

    Returns:
      Path of written file on success.
      None if the target already exists (no overwrite).

    Raises RuntimeError if the resolved target falls outside repo_root
    (path traversal attempt).  This check runs inside the function so it
    cannot be bypassed by callers that skip sanitization.

    repo_root is resolved internally so the boundary check is correct even
    when the caller passes an unresolved or symlinked path.

    Creates parent directories as needed.
    """
    resolved_root = repo_root.resolve()
    target = (repo_root / relative_path).resolve()
    if not target.is_relative_to(resolved_root):
        raise RuntimeError(
            f"_write_to_repo: resolved path {target!r} is outside "
            f"repo root {resolved_root!r}. Path traversal is not allowed."
        )
    if target.exists():
        return None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


# ---------------------------------------------------------------------------
# Markdown content generation
# ---------------------------------------------------------------------------

# Known section headers in the builder artifact content.
# Used by _build_repo_file_content to exclude Notes and Risks from the output.
_ARTIFACT_SECTION_HEADERS = frozenset({"Proposed Changes:", "Notes:", "Risks:"})


def _build_repo_file_content(task_type: str, summary: str, artifact_content: str) -> str:
    """Build the markdown file content for the target repo.

    Extracts only the Proposed Changes section from artifact_content
    (section-aware: Notes and Risks are excluded even though they share the
    "  - " prefix). Converts "  - item" workspace format to "- item" bullets.
    """
    title = _neutralize(task_type.replace("_", " ").title())
    safe_summary = _neutralize(summary)
    lines: list[str] = [
        f"# {title}",
        "",
        f"**Summary:** {safe_summary}",
        "",
        "## Proposed Changes",
        "",
    ]
    in_proposed = False
    for line in artifact_content.splitlines():
        if line == "Proposed Changes:":
            in_proposed = True
        elif line in _ARTIFACT_SECTION_HEADERS:
            in_proposed = False
        elif in_proposed and line.startswith("  - "):
            # Strip "  - " prefix, neutralize HTML comment starts, emit as bullet.
            lines.append("- " + _neutralize(line[4:]))
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def apply_task_output_to_repo(
    artifact: Artifact,
    repo_root: Path,
    *,
    job_fences: dict | None = None,
) -> list[str]:
    """Apply eligible task output to the attached target repository.

    Checks whether the artifact's task_type maps to a repo_route via the
    task registry.  If it does:
      1. Generates a markdown file from the artifact's summary and proposed
         changes.
      2. Writes it to the determined repo-relative path (only if it does not
         already exist — no overwriting).
      3. Returns a list containing the absolute path string of the written file.

    Returns an empty list if:
      - repo_root does not exist or is not a directory (stale/invalid path)
      - task_type is not eligible (no keyword match)
      - target file already exists (no overwrite)

    Raises FenceViolationError if the target path violates scope fences.
    Raises RuntimeError if the resolved target path falls outside repo_root.

    This function does not mutate the artifact or the job.  The caller is
    responsible for recording the returned paths in artifact metadata as
    'repo_applied_files' before persisting.
    """
    if not repo_root.exists() or not repo_root.is_dir():
        return []

    task_type = str(artifact.metadata.get("task_type") or "unknown")
    summary   = str(artifact.metadata.get("summary")   or "")

    relative_path = _resolve_repo_path(task_type)
    if relative_path is None:
        return []

    # F017: fence preflight via shared enforcement boundary
    from packages.orchestration.scope_fences import TouchedPath, enforce_change_set

    enforce_change_set(
        repo_root,
        [TouchedPath(path=relative_path, operation="create", role="target")],
        applicator="repo_applicator",
        job_fences=job_fences,
    )

    content = _build_repo_file_content(task_type, summary, artifact.content)

    target = _write_to_repo(repo_root, relative_path, content)
    if target is None:
        return []

    return [str(target)]


# ---------------------------------------------------------------------------
# Permission-gated application
# ---------------------------------------------------------------------------


def check_and_apply_to_repo(
    job: Job,
    artifact: Artifact,
    repo_root: Path,
) -> list[str]:
    """Apply task output to the target repo after checking repo_generated_write permission.

    If repo_generated_write is not allowed:
      - records repo_application_skipped_reason="permission_denied" in artifact.metadata
      - returns []

    If allowed, delegates to apply_task_output_to_repo (which handles stale paths,
    keyword eligibility, no-overwrite, and boundary safety).

    Mutates artifact.metadata on permission denial.  The caller is responsible for
    persisting the updated artifact (via save_job).
    """
    from packages.orchestration.permissions import Capability, is_allowed

    if not is_allowed(job, Capability.repo_generated_write):
        artifact.metadata["repo_application_skipped_reason"] = "permission_denied"
        return []

    _job_fences = None
    if hasattr(job, "fences") and job.fences is not None:
        _job_fences = {"allow": job.fences.allow, "deny": job.fences.deny}
    return apply_task_output_to_repo(artifact, repo_root, job_fences=_job_fences)
