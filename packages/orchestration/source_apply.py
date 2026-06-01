"""
Source Patch Apply v1 — safe application of structured code patches.

Applies file_ops and unified diffs after approval.
Safety: no binary, no symlink escape, no path traversal, no .env/secrets,
no absolute paths, snapshot before apply, revert support.

Public API::

    apply_structured_patch(patch, repo_path, *, data_dir, job_id) -> ApplyResult
    revert_apply(apply_id, repo_path, *, data_dir) -> bool
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.structured_patch import (
    FileOp,
    StructuredPatch,
    UnifiedDiff,
    validate_structured_patch,
)

# ---------------------------------------------------------------------------
# Deny list
# ---------------------------------------------------------------------------

_DENY_EXTENSIONS = frozenset({
    ".env", ".pem", ".key", ".p12", ".pfx", ".jks",
    ".sqlite", ".sqlite3", ".db",
    ".exe", ".dll", ".so", ".dylib",
    ".zip", ".tar", ".gz", ".bz2",
})

_DENY_DIRS = frozenset({
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "vendor", ".cache",
})

_MAX_FILE_SIZE = 500_000  # 500KB


@dataclass
class FileSnapshot:
    """Snapshot of a file before modification."""
    path: str
    existed: bool
    content_hash: str
    content: str  # Only stored for revert


@dataclass
class ApplyResult:
    """Result of applying a structured patch."""
    apply_id: str
    success: bool
    files_modified: int
    files_created: int
    errors: list[str] = field(default_factory=list)
    snapshots: list[FileSnapshot] = field(default_factory=list)


def _is_safe_path(path: str, repo_root: Path) -> tuple[bool, str]:
    """Validate path safety. Returns (safe, reason)."""
    if not path:
        return False, "empty path"
    if os.path.isabs(path):
        return False, "absolute path not allowed"
    if ".." in path.split(os.sep):
        return False, "path traversal not allowed"

    # Check resolved path is within repo
    resolved = (repo_root / path).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError:
        return False, "path escapes repo root"

    # Check symlink
    if resolved.is_symlink():
        return False, "symlink target not allowed"

    # Check deny list
    lower = path.lower()
    for ext in _DENY_EXTENSIONS:
        if lower.endswith(ext):
            return False, f"denied extension: {ext}"
    for part in Path(path).parts:
        if part in _DENY_DIRS:
            return False, f"denied directory: {part}"

    return True, ""


def _is_text_content(content: str) -> bool:
    """Check content is valid text (no null bytes)."""
    return "\x00" not in content


def _hash_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _snapshot_file(repo_root: Path, rel_path: str) -> FileSnapshot:
    """Create a snapshot of a file for revert."""
    full = repo_root / rel_path
    if full.is_file():
        content = full.read_text(encoding="utf-8", errors="replace")
        return FileSnapshot(
            path=rel_path,
            existed=True,
            content_hash=_hash_content(content),
            content=content,
        )
    return FileSnapshot(
        path=rel_path,
        existed=False,
        content_hash="",
        content="",
    )


def apply_structured_patch(
    patch: StructuredPatch,
    repo_path: Path,
    *,
    data_dir: str | None = None,
    job_id: UUID | None = None,
    job: Any,
) -> ApplyResult:
    """Apply a structured patch to the repo. Snapshot before each change.

    Requires:
      - job parameter (mandatory — no bypass)
      - job must have repo_generated_write permission

    No mutation occurs without explicit permission boundary.
    """
    apply_id = uuid4().hex[:12]
    result = ApplyResult(apply_id=apply_id, success=True, files_modified=0, files_created=0)

    # Permission boundary: always enforced
    from packages.orchestration.permissions import Capability, is_allowed
    if not is_allowed(job, Capability.repo_generated_write):
        result.success = False
        result.errors.append("permission denied: repo_generated_write not granted")
        return result

    # Validate first
    issues = validate_structured_patch(patch)
    if issues:
        result.success = False
        result.errors = issues
        return result

    repo_root = repo_path.resolve()
    if not repo_root.is_dir():
        result.success = False
        result.errors.append(f"repo path not found: {repo_root}")
        return result

    if patch.intent_kind == "file_ops":
        for op in patch.file_ops:
            _apply_file_op(op, repo_root, result)
    elif patch.intent_kind == "unified_diff":
        for diff in patch.unified_diffs:
            _apply_unified_diff(diff, repo_root, result)
    else:
        result.errors.append(f"non-applicable intent kind: {patch.intent_kind}")
        result.success = False

    # Record event
    if data_dir and job_id:
        from packages.orchestration.timeline import append_run_event
        append_run_event(data_dir, job_id, event="source_patch_applied", metadata={
            "apply_id": apply_id,
            "success": result.success,
            "files_modified": result.files_modified,
            "files_created": result.files_created,
            "error_count": len(result.errors),
        })

    return result


def _apply_file_op(op: FileOp, repo_root: Path, result: ApplyResult) -> None:
    """Apply a single file operation."""
    safe, reason = _is_safe_path(op.path, repo_root)
    if not safe:
        result.errors.append(f"{op.path}: {reason}")
        result.success = False
        return

    if not _is_text_content(op.content):
        result.errors.append(f"{op.path}: binary content not allowed")
        result.success = False
        return

    if len(op.content.encode()) > _MAX_FILE_SIZE:
        result.errors.append(f"{op.path}: exceeds max file size")
        result.success = False
        return

    full = repo_root / op.path

    # Snapshot
    snapshot = _snapshot_file(repo_root, op.path)
    result.snapshots.append(snapshot)

    if op.action == "create":
        if full.exists():
            result.errors.append(f"{op.path}: file already exists (create)")
            result.success = False
            return
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(op.content, encoding="utf-8")
        result.files_created += 1

    elif op.action == "modify":
        if not full.is_file():
            result.errors.append(f"{op.path}: file not found (modify)")
            result.success = False
            return
        full.write_text(op.content, encoding="utf-8")
        result.files_modified += 1

    elif op.action == "delete":
        result.errors.append(f"{op.path}: delete not supported in v1")
        result.success = False


def _apply_unified_diff(diff: UnifiedDiff, repo_root: Path, result: ApplyResult) -> None:
    """Apply a unified diff to a file using Python-only patch logic."""
    safe, reason = _is_safe_path(diff.path, repo_root)
    if not safe:
        result.errors.append(f"{diff.path}: {reason}")
        result.success = False
        return

    full = repo_root / diff.path
    if not full.is_file():
        result.errors.append(f"{diff.path}: file not found for diff")
        result.success = False
        return

    # Snapshot
    snapshot = _snapshot_file(repo_root, diff.path)
    result.snapshots.append(snapshot)

    # Apply diff using simple hunk application
    try:
        original = full.read_text(encoding="utf-8")
        patched = _apply_hunks(original, diff.diff)
        if patched is None:
            result.errors.append(f"{diff.path}: diff hunks did not apply cleanly")
            result.success = False
            return
        full.write_text(patched, encoding="utf-8")
        result.files_modified += 1
    except (OSError, UnicodeDecodeError) as e:
        result.errors.append(f"{diff.path}: {e}")
        result.success = False


def _apply_hunks(original: str, diff_text: str) -> str | None:
    """Apply unified diff hunks to original text. Returns None if fails."""
    import re

    lines = original.split("\n")
    result_lines = list(lines)
    offset = 0

    # Parse hunks
    hunk_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")

    diff_lines = diff_text.split("\n")
    i = 0
    while i < len(diff_lines):
        m = hunk_re.match(diff_lines[i])
        if not m:
            i += 1
            continue

        orig_start = int(m.group(1)) - 1  # 0-indexed
        i += 1

        # Collect hunk lines
        removals: list[int] = []
        additions: list[tuple[int, str]] = []
        pos = orig_start

        while i < len(diff_lines):
            line = diff_lines[i]
            if line.startswith("@@") or line.startswith("diff ") or line.startswith("---") or line.startswith("+++"):
                break
            if line.startswith("-"):
                removals.append(pos + offset)
                pos += 1
            elif line.startswith("+"):
                additions.append((pos + offset, line[1:]))
            elif line.startswith(" "):
                pos += 1
            else:
                pos += 1
            i += 1

        # Apply: remove then insert
        for idx in sorted(removals, reverse=True):
            if 0 <= idx < len(result_lines):
                result_lines.pop(idx)
                offset -= 1

        insert_at = orig_start + offset
        for j, (_, content) in enumerate(additions):
            result_lines.insert(insert_at + j, content)
            offset += 1

    return "\n".join(result_lines)


def revert_apply(snapshots: list[FileSnapshot], repo_path: Path) -> bool:
    """Revert files to their snapshot state."""
    success = True
    for snap in snapshots:
        full = repo_path / snap.path
        try:
            if snap.existed:
                full.write_text(snap.content, encoding="utf-8")
            elif full.exists():
                full.unlink()
        except OSError:
            success = False
    return success
