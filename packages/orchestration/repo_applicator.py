"""
Repository attachment and safe generated-file application.

Provides apply_task_output_to_repo() — the only public entry point — which
writes eligible task output as a markdown file into a user-attached target
repository.

Design constraints:
  - No arbitrary LLM paths: task_type is matched against a static keyword
    mapping (_REPO_PATH_RULES). If no keyword matches, no file is written.
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

import re
from pathlib import Path

from packages.core.models import Artifact

# ---------------------------------------------------------------------------
# Path sanitization
# Mirrors _sanitize_path_component in task_runner.py; kept local to avoid
# importing a private helper across modules.
# ---------------------------------------------------------------------------

_SAFE_PATH_RE = re.compile(r"[^a-zA-Z0-9_-]")
_MAX_PATH_COMPONENT_LENGTH = 48


def _sanitize_path_component(value: str) -> str:
    """Replace unsafe characters and truncate for safe use in a path component."""
    sanitized = _SAFE_PATH_RE.sub("_", value)
    sanitized = sanitized[:_MAX_PATH_COMPONENT_LENGTH].strip("_")
    return sanitized or "unknown"


# ---------------------------------------------------------------------------
# Repo path mapping
#
# Conservative, inspectable mapping from task_type keyword → repo-relative
# path template.  Each entry: (keyword, path_template).  The first matching
# keyword wins (case-insensitive substring match).  Order matters — more
# specific keywords appear first.
#
# Allowed targets:
#   README.md             — readme-type output
#   docs/<type>.md        — documentation, architecture, design, changelog, guide output
#   docs/remedy/<type>.md — planning, spec, requirement, acceptance, analysis output
#
# Source code paths, test paths, and arbitrary paths are intentionally absent.
#
# Intentionally excluded keywords (too broad — would match code/implementation tasks):
#   implementation, prepare, define, summarize, summary
# ---------------------------------------------------------------------------

_REPO_PATH_RULES: list[tuple[str, str]] = [
    ("readme",          "README.md"),
    ("changelog",       "docs/{safe_type}.md"),
    ("architecture",    "docs/{safe_type}.md"),
    ("design",          "docs/{safe_type}.md"),
    ("guide",           "docs/{safe_type}.md"),
    ("documentation",   "docs/{safe_type}.md"),
    ("doc",             "docs/{safe_type}.md"),
    ("plan",            "docs/remedy/{safe_type}.md"),
    ("spec",            "docs/remedy/{safe_type}.md"),
    ("requirement",     "docs/remedy/{safe_type}.md"),
    ("acceptance",      "docs/remedy/{safe_type}.md"),
    ("analysis",        "docs/remedy/{safe_type}.md"),
]


def _resolve_repo_path(task_type: str) -> str | None:
    """Return the repo-relative path template for a task_type, or None.

    Matches task_type (case-insensitive) against each keyword in
    _REPO_PATH_RULES.  Returns the path for the first matching keyword,
    with {safe_type} substituted.  Returns None if no keyword matches.
    """
    lower = task_type.lower()
    safe_type = _sanitize_path_component(task_type)
    for keyword, template in _REPO_PATH_RULES:
        if keyword in lower:
            return template.format(safe_type=safe_type)
    return None


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

    Creates parent directories as needed.
    """
    target = (repo_root / relative_path).resolve()
    if not target.is_relative_to(repo_root):
        raise RuntimeError(
            f"_write_to_repo: resolved path {target!r} is outside "
            f"repo root {repo_root!r}. Path traversal is not allowed."
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
    title = task_type.replace("_", " ").title()
    lines: list[str] = [
        f"# {title}",
        "",
        "> Generated by Remedy",
        "",
        f"**Summary:** {summary}",
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
            # Strip leading spaces to convert "  - item" → "- item"
            lines.append(line.lstrip())
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def apply_task_output_to_repo(
    artifact: Artifact,
    repo_root: Path,
) -> list[str]:
    """Apply eligible task output to the attached target repository.

    Checks whether the artifact's task_type matches any keyword in
    _REPO_PATH_RULES.  If it does:
      1. Generates a markdown file from the artifact's summary and proposed
         changes.
      2. Writes it to the determined repo-relative path (only if it does not
         already exist — no overwriting).
      3. Returns a list containing the absolute path string of the written file.

    Returns an empty list if:
      - task_type is not eligible (no keyword match)
      - target file already exists (no overwrite)

    Raises RuntimeError if the resolved target path falls outside repo_root.

    This function does not mutate the artifact or the job.  The caller is
    responsible for recording the returned paths in artifact metadata as
    'repo_applied_files' before persisting.
    """
    task_type = artifact.metadata.get("task_type", "unknown")
    summary = artifact.metadata.get("summary", "")

    relative_path = _resolve_repo_path(task_type)
    if relative_path is None:
        return []

    content = _build_repo_file_content(task_type, summary, artifact.content)

    target = _write_to_repo(repo_root, relative_path, content)
    if target is None:
        return []

    return [str(target)]
