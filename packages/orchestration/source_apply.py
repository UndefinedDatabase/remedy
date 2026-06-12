"""
Source Patch Apply v2 — safe application of structured code patches.

Applies file_ops and unified diffs after approval.
Safety: no binary, no symlink escape, no path traversal, no .env/secrets,
no absolute paths, mandatory durable snapshot before apply, revert support.

v2 changes from v1:
  - FileSnapshot removed — no raw content in public models.
  - Durable snapshot created and verified before any mutation.
  - Apply BLOCKED if snapshot creation or verification fails.
  - Transactional rollback reads from private snapshot blobs (not memory).
  - DurableApplyRecord saved after successful apply for post-apply revert.
  - revert_apply() delegates to revert_repository_apply().

Public API::

    apply_structured_patch(patch, repo_path, *, data_dir, job_id, job, intent_id) -> ApplyResult
    revert_apply(apply_id, repo_path, *, job_id, data_dir=None) -> bool
"""

from __future__ import annotations

import hashlib
import json
import os
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
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.repository_snapshot import (
    DurableApplyRecord,
    SnapshotEntry,
    build_snapshot_path_set,
    create_snapshot,
    load_snapshot,
    revert_repository_apply,
    save_durable_apply_record,
    verify_snapshot,
    _snapshot_dir,
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
class ApplyResult:
    """Result of applying a structured patch. No raw content."""
    apply_id: str
    success: bool
    files_modified: int
    files_created: int
    errors: list[str] = field(default_factory=list)
    snapshot_id: str = ""
    snapshot_verified: bool = False


def _is_safe_path(path: str, repo_root: Path) -> tuple[bool, str]:
    """Validate path safety. Returns (safe, reason)."""
    if not path:
        return False, "empty path"
    if os.path.isabs(path):
        return False, "absolute path not allowed"
    if ".." in path.split(os.sep):
        return False, "path traversal not allowed"

    resolved = (repo_root / path).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError:
        return False, "path escapes repo root"

    if resolved.is_symlink():
        return False, "symlink target not allowed"

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


def _rollback_from_snapshot(
    snapshot_id: str,
    job_id_str: str,
    data_dir: Path,
    repo_root: Path,
    result: ApplyResult,
) -> None:
    """Restore files from durable snapshot blobs after mid-apply failure."""
    snap = load_snapshot(snapshot_id, job_id_str, data_dir)
    if snap is None:
        result.errors.append("rollback_failed:snapshot_not_found")
        return

    failures: list[str] = []
    snap_dir = _snapshot_dir(job_id_str, snapshot_id, data_dir)

    for entry in reversed(snap.entries):
        target = repo_root / entry.rel_path
        if not entry.existed_before:
            if target.exists():
                try:
                    target.unlink()
                except OSError:
                    failures.append(entry.rel_path)
        else:
            blob_path = snap_dir / entry.recovery_blob_ref
            try:
                raw = blob_path.read_bytes()
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
            except OSError:
                failures.append(entry.rel_path)

    if failures:
        result.errors.append(
            f"rollback_incomplete ({len(failures)} file(s)): " + "; ".join(failures)
        )


def _collect_after_proof(
    entries: list[SnapshotEntry], repo_root: Path
) -> dict[str, Any]:
    """Collect post-apply file state. No raw content — hashes only."""
    proof: dict[str, Any] = {}
    for entry in entries:
        full = repo_root / entry.rel_path
        if full.exists() and not full.is_symlink():
            try:
                raw = full.read_bytes()
                proof[entry.rel_path] = {
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "bytes": len(raw),
                    "existed": True,
                }
            except OSError:
                proof[entry.rel_path] = {"sha256": "", "bytes": 0, "existed": True}
        else:
            proof[entry.rel_path] = {"sha256": "", "bytes": 0, "existed": False}
    return proof


def apply_structured_patch(
    patch: StructuredPatch,
    repo_path: Path,
    *,
    data_dir: str | None = None,
    job_id: UUID | None = None,
    job: Any,
    intent_id: str | None = None,
) -> ApplyResult:
    """Apply a structured patch to the repo.

    Mandatory durable snapshot created and verified before any mutation.
    Apply BLOCKED if snapshot creation or verification fails.

    Requires:
      - job parameter (mandatory — no bypass)
      - job must have repo_generated_write permission
      - intent_id must reference an approved patch intent

    No mutation occurs without permission + approval + verified snapshot.
    No raw content in ApplyResult.
    """
    apply_id = uuid4().hex[:12]
    result = ApplyResult(apply_id=apply_id, success=True, files_modified=0, files_created=0)

    # Permission boundary: always enforced
    from packages.orchestration.permissions import Capability, is_allowed
    if not is_allowed(job, Capability.repo_generated_write):
        result.success = False
        result.errors.append("permission denied: repo_generated_write not granted")
        return result

    # Approval gate: intent_id required, must be approved
    if intent_id is None:
        result.success = False
        result.errors.append("approval required: intent_id not provided")
        return result

    from packages.orchestration.approval_queue import get_patch_intent, APPROVAL_APPROVED
    intent = get_patch_intent(job, intent_id)
    if intent is None:
        result.success = False
        result.errors.append(f"approval required: intent {intent_id!r} not found")
        return result
    if intent["state"] != APPROVAL_APPROVED:
        result.success = False
        result.errors.append(
            f"approval required: intent {intent_id!r} state is "
            f"{intent['state']!r}, not 'approved'"
        )
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

    data_dir_path = Path(data_dir) if data_dir else resolve_data_root()
    job_id_str = str(getattr(job, "id", None) or job_id or "unknown")

    # Mandatory snapshot: derive path set, create, verify — block if any step fails
    path_set = build_snapshot_path_set(patch)
    if path_set:
        snap_result = create_snapshot(
            job_id_str,
            intent_id or apply_id,
            path_set,
            repo_root,
            data_dir_path,
            apply_id=apply_id,
        )
        if not snap_result.success:
            result.success = False
            result.errors.append(f"snapshot_blocked:{snap_result.safe_error_kind}")
            return result

        snap_verif = verify_snapshot(snap_result.snapshot_id, job_id_str, data_dir_path)
        if not snap_verif.verified:
            result.success = False
            result.errors.append(f"snapshot_verify_failed:{snap_verif.failure_reason}")
            return result

        result.snapshot_id = snap_result.snapshot_id
        result.snapshot_verified = True
    else:
        # No target paths — apply trivially no-ops (validate_structured_patch already passed)
        result.snapshot_id = ""
        result.snapshot_verified = False

    # Transactional apply: apply all ops; rollback from snapshot on any failure
    if patch.intent_kind == "file_ops":
        for op in patch.file_ops:
            _apply_file_op(op, repo_root, result)
            if not result.success:
                if result.snapshot_id:
                    _rollback_from_snapshot(result.snapshot_id, job_id_str, data_dir_path, repo_root, result)
                break
    elif patch.intent_kind == "unified_diff":
        for diff in patch.unified_diffs:
            _apply_unified_diff(diff, repo_root, result)
            if not result.success:
                if result.snapshot_id:
                    _rollback_from_snapshot(result.snapshot_id, job_id_str, data_dir_path, repo_root, result)
                break
    else:
        result.errors.append(f"non-applicable intent kind: {patch.intent_kind}")
        result.success = False

    # Save durable apply record on success
    if result.success and result.snapshot_id:
        snap = load_snapshot(result.snapshot_id, job_id_str, data_dir_path)
        before_proof: dict[str, Any] = {}
        after_proof: dict[str, Any] = {}
        if snap:
            for entry in snap.entries:
                before_proof[entry.rel_path] = {
                    "sha256": entry.before_sha256,
                    "bytes": entry.before_bytes,
                    "existed": entry.existed_before,
                }
            after_proof = _collect_after_proof(snap.entries, repo_root)

        apply_record = DurableApplyRecord(
            apply_id=apply_id,
            job_id=job_id_str,
            intent_id=intent_id or "",
            snapshot_id=result.snapshot_id,
            state="applied",
            target_paths=path_set,
            applied_at=datetime.now(timezone.utc).isoformat(),
            before_proof=before_proof,
            after_proof=after_proof,
            snapshot_verified=True,
        )
        save_durable_apply_record(apply_record, job_id_str, data_dir_path)

    # Record event
    if data_dir and job_id:
        try:
            from packages.orchestration.timeline import append_run_event
            append_run_event(data_dir, job_id, event="source_patch_applied", metadata={
                "apply_id": apply_id,
                "snapshot_id": result.snapshot_id,
                "snapshot_verified": result.snapshot_verified,
                "success": result.success,
                "files_modified": result.files_modified,
                "files_created": result.files_created,
                "error_count": len(result.errors),
            })
        except Exception:
            pass

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
        result.errors.append(f"{diff.path}: {type(e).__name__}")
        result.success = False


def _apply_hunks(original: str, diff_text: str) -> str | None:
    """Apply unified diff hunks to original text.

    Validates context and removal lines against actual file content.
    Returns None if any hunk fails to apply.
    """
    import re

    lines = original.split("\n")
    result_lines = list(lines)
    offset = 0

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

        removals: list[int] = []
        additions: list[tuple[int, str]] = []
        pos = orig_start

        while i < len(diff_lines):
            line = diff_lines[i]
            if line.startswith("@@") or line.startswith("diff ") or line.startswith("---") or line.startswith("+++"):
                break
            if line.startswith("-"):
                actual_idx = pos
                if actual_idx < 0 or actual_idx >= len(lines):
                    return None
                if lines[actual_idx] != line[1:]:
                    return None
                removals.append(pos + offset)
                pos += 1
            elif line.startswith("+"):
                additions.append((pos + offset, line[1:]))
            elif line.startswith(" "):
                actual_idx = pos
                if actual_idx < 0 or actual_idx >= len(lines):
                    return None
                if lines[actual_idx] != line[1:]:
                    return None
                pos += 1
            else:
                pos += 1
            i += 1

        for idx in sorted(removals, reverse=True):
            if 0 <= idx < len(result_lines):
                result_lines.pop(idx)
                offset -= 1

        insert_at = orig_start + offset
        for j, (_, content) in enumerate(additions):
            result_lines.insert(insert_at + j, content)
            offset += 1

    return "\n".join(result_lines)


def revert_apply(
    apply_id: str,
    repo_path: Path,
    *,
    job_id: str,
    data_dir: Path | None = None,
    permitted: bool = True,
    contract_allows_revert: bool = True,
) -> bool:
    """Revert files to their pre-apply state using the durable snapshot.

    Delegates to revert_repository_apply() in repository_snapshot.py.
    Returns True if revert fully succeeded.
    """
    data_dir = data_dir or resolve_data_root()
    revert_result = revert_repository_apply(
        job_id,
        apply_id,
        repo_path,
        data_dir,
        permitted=permitted,
        contract_allows_revert=contract_allows_revert,
    )
    return revert_result.success
