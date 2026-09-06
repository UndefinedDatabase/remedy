"""
Patch Revert v0 — snapshot-backed revert for approved applied Markdown patch intents.

Before applying a patch, a private pre-apply snapshot is stored in workspace.
This module implements the revert command: restore file to pre-apply state.

Markdown-only v0. No shell, no Git, no LLM, no network.

Snapshot storage:
  .data/workspaces/<job_id>/patch_snapshots/<intent_id>/
  - before_content.md or before_content.txt (raw file bytes, private recovery material)
  - metadata.json (safe structured metadata)

Snapshot content MUST NEVER appear in run logs, Brain, Viewer, Trust, Timeline,
Project Brain, or Context Pack. It is private workspace recovery material only.

Public API::

    store_pre_apply_snapshot(job, intent_id, target_path, action, repo_root) -> bool
    revert_patch_intent(job, intent_id) -> PatchRevertResult
    format_revert_result(result) -> str
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from packages.orchestration.data_paths import resolve_data_root

if TYPE_CHECKING:
    from packages.core.models import Job


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PatchRevertResult:
    """Immutable outcome of a patch revert operation."""

    state: str  # "reverted" | "noop" | "blocked"
    intent_id: str
    target_path: str
    action: str
    outcome: str
    existed_before: bool
    bytes_written: int
    line_count: int
    before_sha256: str
    after_sha256: str
    blocked_reason: str | None


# ---------------------------------------------------------------------------
# Snapshot helpers
# ---------------------------------------------------------------------------


def _snapshot_dir(job_id: str, intent_id: str, data_dir: Path | None = None) -> Path:
    root = data_dir or resolve_data_root()
    return root / "workspaces" / job_id / "patch_snapshots" / intent_id


def _file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def store_pre_apply_snapshot(
    job: Job,
    intent_id: str,
    target_path: str,
    action: str,
    repo_root: Path,
    *,
    data_dir: Path | None = None,
) -> bool:
    """Store a pre-apply snapshot before applying a patch.

    Returns True if snapshot was stored, False if already exists (no overwrite).
    """
    snap_dir = _snapshot_dir(str(job.id), intent_id, data_dir)
    meta_path = snap_dir / "metadata.json"

    # Don't overwrite existing snapshot (idempotent)
    if meta_path.exists():
        return False

    resolved = (repo_root / target_path).resolve()
    existed = resolved.exists()
    before_bytes = b""
    before_sha256 = ""
    before_byte_count = 0

    if existed:
        before_bytes = resolved.read_bytes()
        before_sha256 = _file_hash(before_bytes)
        before_byte_count = len(before_bytes)

    snap_dir.mkdir(parents=True, exist_ok=True)

    # Store raw content for recovery (private workspace only)
    if existed:
        ext = ".md" if target_path.lower().endswith(".md") else ".txt"
        (snap_dir / f"before_content{ext}").write_bytes(before_bytes)

    # Store safe metadata
    meta = {
        "intent_id": intent_id,
        "target_path": target_path,
        "action": action,
        "existed_before": existed,
        "before_sha256": before_sha256,
        "before_bytes": before_byte_count,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def revert_patch_intent(
    job: Job,
    intent_id: str,
    *,
    data_dir: Path | None = None,
) -> PatchRevertResult:
    """Revert a previously applied patch intent using stored snapshot.

    Explicit CLI-only. No automatic revert. Markdown-only v0.
    No shell, no Git, no LLM, no network.
    """
    from packages.orchestration.approval_queue import get_patch_intent
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.storage import save_job

    def _blocked(reason: str, target_path: str = "", action: str = "") -> PatchRevertResult:
        return PatchRevertResult(
            state="blocked", intent_id=intent_id,
            target_path=target_path, action=action,
            outcome=reason, existed_before=False,
            bytes_written=0, line_count=0,
            before_sha256="", after_sha256="",
            blocked_reason=reason,
        )

    # Validate job and intent
    intent = get_patch_intent(job, intent_id)
    if intent is None:
        return _blocked("intent_not_found")

    target_path: str = intent["target_path"]
    action: str = intent["action"]

    # Check target repo
    target_repo_str = job.metadata.get("target_repo", "")
    if not target_repo_str:
        return _blocked("repo_missing", target_path, action)
    repo_root = Path(target_repo_str)
    if not repo_root.exists():
        return _blocked("repo_missing", target_path, action)

    # Path safety
    from packages.orchestration.patch_apply import _validate_target_path
    path_err = _validate_target_path(target_path)
    if path_err:
        return _blocked(path_err, target_path, action)
    resolved_target = (repo_root / target_path).resolve()
    if not resolved_target.is_relative_to(repo_root.resolve()):
        return _blocked("unsafe_path", target_path, action)

    # Check snapshot exists
    snap_dir = _snapshot_dir(str(job.id), intent_id, data_dir)
    meta_path = snap_dir / "metadata.json"
    if not meta_path.exists():
        return _blocked("snapshot_missing", target_path, action)

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    existed_before = meta.get("existed_before", False)

    # Check if already reverted
    artifact = next(
        (a for a in job.artifacts if str(a.id) == intent["artifact_id"]), None
    )
    if artifact is not None:
        records = artifact.metadata.get("patch_intent_apply_records", {})
        record = records.get(intent_id, {})
        if record.get("state") == "reverted":
            return PatchRevertResult(
                state="noop", intent_id=intent_id,
                target_path=target_path, action=action,
                outcome="already_reverted", existed_before=existed_before,
                bytes_written=0, line_count=0,
                before_sha256="", after_sha256="",
                blocked_reason=None,
            )

    # Perform revert
    if existed_before:
        # Restore previous content
        ext = ".md" if target_path.lower().endswith(".md") else ".txt"
        content_path = snap_dir / f"before_content{ext}"
        if not content_path.exists():
            return _blocked("snapshot_content_missing", target_path, action)
        restored_bytes = content_path.read_bytes()
        resolved_target.parent.mkdir(parents=True, exist_ok=True)
        resolved_target.write_bytes(restored_bytes)
        bytes_written = len(restored_bytes)
        line_count = restored_bytes.count(b"\n")
    else:
        # File was created by apply — delete it
        if resolved_target.exists():
            resolved_target.unlink()
        bytes_written = 0
        line_count = 0

    before_sha256 = meta.get("before_sha256", "")
    after_data = resolved_target.read_bytes() if resolved_target.exists() else b""
    after_sha256 = _file_hash(after_data) if after_data else ""

    # Update apply record
    if artifact is not None:
        if "patch_intent_apply_records" not in artifact.metadata:
            artifact.metadata["patch_intent_apply_records"] = {}
        artifact.metadata["patch_intent_apply_records"][intent_id] = {
            "state": "reverted",
            "reverted_at": datetime.now(timezone.utc).isoformat(),
            "target_path": target_path,
            "action": action,
        }
        save_job(job)

    # Emit run-log event
    actual_data_dir = data_dir or resolve_data_root()
    log = RunLogWriter(job_id=job.id, data_root=actual_data_dir)
    from packages.orchestration.run_log import RunEvent
    log.append(RunEvent(
        event="patch_intent_reverted",
        job_id=str(job.id),
        run_id=log.run_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        outcome="reverted",
        metadata={
            "intent_id": intent_id,
            "target_path": target_path,
            "action": action,
            "outcome": "reverted",
            "existed_before": existed_before,
            "bytes_written": bytes_written,
            "line_count": line_count,
            "before_sha256": before_sha256,
            "after_sha256": after_sha256,
        },
    ))

    return PatchRevertResult(
        state="reverted", intent_id=intent_id,
        target_path=target_path, action=action,
        outcome="reverted", existed_before=existed_before,
        bytes_written=bytes_written, line_count=line_count,
        before_sha256=before_sha256, after_sha256=after_sha256,
        blocked_reason=None,
    )


def format_revert_result(result: PatchRevertResult) -> str:
    """Format a PatchRevertResult for CLI output. No raw content."""
    if result.state == "reverted":
        lines = [
            f"Reverted: {result.intent_id} ({result.target_path})",
            f"  action: {result.action}",
            f"  existed_before: {result.existed_before}",
            f"  bytes_written: {result.bytes_written}",
            f"  before_sha256: {result.before_sha256[:16]}..." if result.before_sha256 else "  before_sha256: (none)",
            f"  after_sha256: {result.after_sha256[:16]}..." if result.after_sha256 else "  after_sha256: (none)",
        ]
        return "\n".join(lines)
    if result.state == "noop":
        return f"No-op: {result.intent_id} ({result.target_path}) — {result.outcome}"
    return f"Error: {result.blocked_reason or result.outcome}"
