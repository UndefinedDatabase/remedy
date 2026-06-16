"""
Repository Snapshot / Rollback Service v1 — Steps 1118-1127.

Provides mandatory, verified snapshot-backed revert for repository mutations.
No apply may begin without a verified snapshot.
No revert may overwrite post-apply changes (drift detection).

Public API::

    create_snapshot(job_id, intent_id, path_set, repo_root, data_dir) -> SnapshotCreateResult
    verify_snapshot(snapshot_id, job_id, data_dir) -> SnapshotVerification
    revert_repository_apply(job_id, apply_id, data_dir) -> RepositoryRevertResult
    build_snapshot_path_set(patch) -> list[str]
    load_snapshot(snapshot_id, job_id, data_dir) -> RepositorySnapshot | None
    save_durable_apply_record(record, job_id, data_dir) -> bool
    load_durable_apply_record(apply_id, job_id, data_dir) -> DurableApplyRecord | None

Design invariants:
  - No raw content in public models, events, or return values.
  - Snapshot contents are private recovery material — never returned to callers.
  - No symlink following during snapshot or restore.
  - No absolute paths stored or accepted.
  - No path traversal.
  - Bounded snapshot size (10 MiB total; 500 KB per file).
  - Apply MUST be blocked if snapshot creation or verification fails.
  - Revert MUST be blocked if current file state diverges from post-apply hashes.
  - Restore MUST verify each path matches before-state hash.
  - Existing snapshots never overwritten.
  - No Git reset/checkout/clean.
  - No automatic revert — caller must invoke explicitly.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from packages.orchestration.data_paths import resolve_data_root

if TYPE_CHECKING:
    from packages.orchestration.event_persistence import EventPersistenceResult

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_MAX_FILE_BYTES: int = 500_000       # 500 KB per file
_MAX_TOTAL_BYTES: int = 10_485_760   # 10 MiB total snapshot
_SNAPSHOT_DIR_NAME: str = "repository_snapshots"
_APPLY_RECORDS_DIR_NAME: str = "apply_records"

_BLOB_PREFIX: str = "blob_"

# Path safety
_DENY_EXTENSIONS: frozenset[str] = frozenset({
    ".env", ".pem", ".key", ".p12", ".pfx", ".jks",
    ".sqlite", ".sqlite3", ".db",
    ".exe", ".dll", ".so", ".dylib",
    ".zip", ".tar", ".gz", ".bz2",
    ".whl", ".rpm", ".deb",
})

_DENY_DIRS: frozenset[str] = frozenset({
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "vendor", ".cache",
})


# ---------------------------------------------------------------------------
# Models (Step 1118) — no raw content fields
# ---------------------------------------------------------------------------


@dataclass
class SnapshotEntry:
    """Metadata for one file in a snapshot. No raw content."""
    rel_path: str
    existed_before: bool
    file_type: str          # "text" | "binary" | "absent"
    before_sha256: str      # empty if not existed_before
    before_bytes: int       # 0 if not existed_before
    recovery_blob_ref: str  # basename of private blob (not a path); empty if not existed_before


@dataclass
class RepositorySnapshot:
    """Metadata for a repository snapshot. No raw recovery content."""
    snapshot_id: str
    job_id: str
    intent_id: str
    apply_id: str
    repository_identity_hash: str   # SHA-256 of canonical repo path; not the path itself
    created_at: str
    state: str          # "creating" | "verified" | "failed" | "reverted" | "revert_failed" | "partial_revert"
    path_count: int
    total_bytes: int
    entries: list[SnapshotEntry]
    manifest_hash: str  # SHA-256 of manifest.json bytes
    verified: bool


@dataclass
class SnapshotCreateResult:
    """Result of create_snapshot(). No raw content."""
    success: bool
    snapshot_id: str
    intent_id: str
    state: str
    path_count: int
    total_bytes: int
    verified: bool
    error_reason: str = ""
    safe_error_kind: str = ""   # "path_unsafe" | "file_too_large" | "total_too_large" | "io_error" | "unexpected"
    warnings: list[str] = field(default_factory=list)


@dataclass
class SnapshotVerification:
    """Result of verify_snapshot(). Safe metadata only."""
    verified: bool
    snapshot_id: str
    state: str
    path_count: int
    blobs_present: int
    blobs_missing: int
    hash_mismatches: int
    failure_reason: str = ""


@dataclass
class DurableApplyRecord:
    """Durable record of a repository apply. Safe metadata — no raw source/diff."""
    apply_id: str
    job_id: str
    intent_id: str
    snapshot_id: str
    state: str          # "pending" | "applied" | "reverted" | "revert_failed" | "partial_revert"
    target_paths: list[str]
    applied_at: str
    before_proof: dict[str, Any]    # {rel_path: {sha256, bytes, existed}} — no content
    after_proof: dict[str, Any]     # {rel_path: {sha256, bytes, existed}} — no content
    snapshot_verified: bool
    revert_state: str = ""          # "clean" | "drifted" | "reverted" | "failed" | ""
    test_run_id: str = ""


@dataclass
class SnapshotTruth:
    """Authoritative, read-only snapshot/apply truth (Step 1156).

    Single shared source for Proof Chain, File Provenance, Readiness,
    Review Bundle, and `do --continue`. Loaded from durable RepositorySnapshot
    + DurableApplyRecord and verified against current manifest/blobs.

    Never trusts events or artifact metadata as authority. Unknown is explicit:
    apply_state / revert_state are "unknown" when no durable record exists.
    No raw paths, blob refs, source, or diff content.
    """
    job_id: str
    snapshot_id: str
    apply_id: str
    intent_id: str
    snapshot_exists: bool
    manifest_exists: bool
    recovery_material_available: bool
    snapshot_verified_now: bool
    apply_state: str            # DurableApplyRecord.state or "unknown"
    revert_state: str           # "" | clean | drifted | reverted | partial_revert | revert_failed | unknown
    restore_verified: bool
    drift_blocked: bool
    evidence_status: str        # "complete" | "degraded" | "unknown"
    blockers: list[str] = field(default_factory=list)


@dataclass
class RepositoryRevertResult:
    """Result of revert_repository_apply(). Safe metadata only."""
    success: bool
    apply_id: str
    snapshot_id: str
    state: str          # "reverted" | "revert_failed" | "partial_revert" | "blocked"
    paths_restored: int
    paths_deleted: int
    paths_failed: int
    block_reason: str = ""          # "no_apply_record" | "no_snapshot" | "post_apply_drift" | "permission_denied" | "contract_denied" | "verify_failed"
    drift_path_count: int = 0
    verification_failures: int = 0
    safe_summary: str = ""
    # Evidence durability (Step 1161) — no silent persistence loss.
    apply_record_persisted: bool = True
    snapshot_state_persisted: bool = True
    event_evidence_status: str = "complete"   # "complete" | "partial" | "failed"
    evidence_warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Path safety (shared with source_apply.py logic)
# ---------------------------------------------------------------------------


def _is_safe_path(rel_path: str, repo_root: Path) -> tuple[bool, str]:
    """Validate a relative path for snapshot/restore safety."""
    if not rel_path:
        return False, "empty_path"
    if os.path.isabs(rel_path):
        return False, "absolute_path"

    # Normalize separators
    rel_path = rel_path.replace("\\", "/")
    parts = Path(rel_path).parts
    if ".." in parts:
        return False, "path_traversal"

    resolved = (repo_root / rel_path).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError:
        return False, "escapes_repo_root"

    # No symlinks
    if resolved.is_symlink():
        return False, "symlink_target"

    lower = rel_path.lower()
    for ext in _DENY_EXTENSIONS:
        if lower.endswith(ext):
            return False, f"denied_extension:{ext}"
    for part in parts:
        if part in _DENY_DIRS:
            return False, f"denied_directory:{part}"

    return True, ""


def _normalize_path_set(paths: list[str]) -> list[str]:
    """Deduplicate and normalize a path set."""
    seen: set[str] = set()
    result: list[str] = []
    for p in paths:
        normalized = p.replace("\\", "/").strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


# ---------------------------------------------------------------------------
# Storage helpers (Step 1119)
# ---------------------------------------------------------------------------


def _snapshot_dir(job_id: str, snapshot_id: str, data_dir: Path) -> Path:
    """Private snapshot directory. Contents never returned publicly."""
    return data_dir / "workspaces" / job_id / _SNAPSHOT_DIR_NAME / snapshot_id


def _apply_record_dir(job_id: str, data_dir: Path) -> Path:
    return data_dir / "workspaces" / job_id / _APPLY_RECORDS_DIR_NAME


def _file_sha256(path: Path) -> str:
    """SHA-256 hex digest of file bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _repo_identity_hash(repo_root: Path) -> str:
    """Non-reversible hash of canonical repo path. Not the path itself."""
    return hashlib.sha256(str(repo_root.resolve()).encode("utf-8")).hexdigest()


def _write_private(path: Path, data: bytes) -> None:
    """Write file with restrictive permissions (owner-read-write only)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0o600
    except OSError:
        pass  # permissions best-effort on platforms that don't support it


def _set_dir_private(path: Path) -> None:
    """Set directory permissions to owner-only where supported."""
    try:
        os.chmod(path, stat.S_IRWXU)  # 0o700
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Event emission (Step 1128)
# ---------------------------------------------------------------------------

# 10 event types. Metadata: safe fields only — no content, no paths, no blobs.
_SNAPSHOT_EVENTS: frozenset[str] = frozenset({
    "snapshot_create_started",
    "snapshot_create_completed",
    "snapshot_create_failed",
    "snapshot_verified",
    "snapshot_verify_failed",
    "apply_record_saved",
    "revert_started",
    "revert_blocked",
    "revert_completed",
    "revert_failed",
})


def _emit_snapshot_event(
    data_dir: Path,
    job_id: str,
    event_type: str,
    metadata: dict,
) -> EventPersistenceResult:
    """Emit a snapshot lifecycle event, returning a structured persistence result.

    Failures are no longer swallowed silently (R-0057, Step 1162): the returned
    EventPersistenceResult carries a status code instead of raising or discarding.

    Authority note (R-0067): snapshot/apply truth is derived from on-disk
    manifest, blobs, and the DurableApplyRecord (see build_snapshot_truth), NOT
    from these events. The create/verify/apply_record_saved emit sites therefore
    treat events as non-authoritative best-effort history and intentionally do
    not gate evidence on the return value — losing a lifecycle event cannot
    corrupt authoritative state. The revert path, where event evidence is
    surfaced to callers, does capture and propagate the status.
    """
    from packages.orchestration.event_persistence import emit_important_event
    return emit_important_event(
        data_dir, job_id, event_type, metadata, eligible=_SNAPSHOT_EVENTS
    )


# ---------------------------------------------------------------------------
# Snapshot path derivation (Step 1120)
# ---------------------------------------------------------------------------


def build_snapshot_path_set(patch: Any) -> list[str]:
    """Derive the exact set of paths to snapshot from a StructuredPatch.

    Includes:
    - FileOp targets (create/modify/delete)
    - UnifiedDiff targets
    No broad whole-repository copy. Safe paths only.

    Returns deduplicated, normalized relative paths.
    """
    paths: list[str] = []

    # FileOp targets
    for op in getattr(patch, "file_ops", []) or []:
        p = getattr(op, "path", "") or ""
        if p:
            paths.append(p)

    # UnifiedDiff targets
    for diff in getattr(patch, "unified_diffs", []) or []:
        p = getattr(diff, "path", "") or ""
        if p:
            paths.append(p)

    return _normalize_path_set(paths)


def build_snapshot_path_set_from_intent(intent: dict) -> list[str]:
    """Derive snapshot path set from a Markdown patch intent dict."""
    target = intent.get("target_path", "")
    if target:
        return _normalize_path_set([target])
    return []


# ---------------------------------------------------------------------------
# Snapshot creation (Steps 1118-1119)
# ---------------------------------------------------------------------------


def create_snapshot(
    job_id: str,
    intent_id: str,
    path_set: list[str],
    repo_root: Path,
    data_dir: Path | None = None,
    *,
    apply_id: str = "",
) -> SnapshotCreateResult:
    """Create a durable, verified snapshot of the given path set.

    Must be called before any repository mutation.
    Returns SnapshotCreateResult with verified=True on success.
    Apply must be blocked if success is False or verified is False.

    Recovery blobs are stored in a private workspace directory.
    Raw content is never returned.
    """
    data_dir = data_dir or resolve_data_root()
    repo_root = repo_root.resolve()
    snapshot_id = uuid4().hex

    normalized_paths = _normalize_path_set(path_set)
    if not normalized_paths:
        return SnapshotCreateResult(
            success=False,
            snapshot_id="",
            intent_id=intent_id,
            state="failed",
            path_count=0,
            total_bytes=0,
            verified=False,
            error_reason="empty_path_set",
            safe_error_kind="path_unsafe",
        )

    snap_dir = _snapshot_dir(job_id, snapshot_id, data_dir)
    try:
        snap_dir.mkdir(parents=True, exist_ok=False)
        _set_dir_private(snap_dir)
    except FileExistsError:
        return SnapshotCreateResult(
            success=False,
            snapshot_id=snapshot_id,
            intent_id=intent_id,
            state="failed",
            path_count=0,
            total_bytes=0,
            verified=False,
            error_reason="snapshot_dir_exists",
            safe_error_kind="io_error",
        )
    except OSError:
        return SnapshotCreateResult(
            success=False,
            snapshot_id=snapshot_id,
            intent_id=intent_id,
            state="failed",
            path_count=0,
            total_bytes=0,
            verified=False,
            error_reason="cannot_create_snapshot_dir",
            safe_error_kind="io_error",
        )

    entries: list[SnapshotEntry] = []
    total_bytes = 0
    warnings: list[str] = []

    for rel_path in normalized_paths:
        safe, reason = _is_safe_path(rel_path, repo_root)
        if not safe:
            # Clean up and fail
            try:
                import shutil
                shutil.rmtree(snap_dir, ignore_errors=True)
            except Exception:
                pass
            return SnapshotCreateResult(
                success=False,
                snapshot_id=snapshot_id,
                intent_id=intent_id,
                state="failed",
                path_count=0,
                total_bytes=0,
                verified=False,
                error_reason=f"unsafe_path:{reason}",
                safe_error_kind="path_unsafe",
            )

        full_path = repo_root / rel_path

        if not full_path.exists():
            # Create target — existed_before=False, no blob needed
            entries.append(SnapshotEntry(
                rel_path=rel_path,
                existed_before=False,
                file_type="absent",
                before_sha256="",
                before_bytes=0,
                recovery_blob_ref="",
            ))
            continue

        if full_path.is_symlink():
            warnings.append(f"skipped_symlink:{rel_path}")
            continue

        try:
            raw = full_path.read_bytes()
        except OSError:
            # Clean up and fail
            try:
                import shutil
                shutil.rmtree(snap_dir, ignore_errors=True)
            except Exception:
                pass
            return SnapshotCreateResult(
                success=False,
                snapshot_id=snapshot_id,
                intent_id=intent_id,
                state="failed",
                path_count=0,
                total_bytes=0,
                verified=False,
                error_reason="cannot_read_file",
                safe_error_kind="io_error",
            )

        file_bytes = len(raw)
        if file_bytes > _MAX_FILE_BYTES:
            # Clean up and fail
            try:
                import shutil
                shutil.rmtree(snap_dir, ignore_errors=True)
            except Exception:
                pass
            return SnapshotCreateResult(
                success=False,
                snapshot_id=snapshot_id,
                intent_id=intent_id,
                state="failed",
                path_count=0,
                total_bytes=0,
                verified=False,
                error_reason="file_too_large",
                safe_error_kind="file_too_large",
            )

        if total_bytes + file_bytes > _MAX_TOTAL_BYTES:
            # Clean up and fail
            try:
                import shutil
                shutil.rmtree(snap_dir, ignore_errors=True)
            except Exception:
                pass
            return SnapshotCreateResult(
                success=False,
                snapshot_id=snapshot_id,
                intent_id=intent_id,
                state="failed",
                path_count=0,
                total_bytes=total_bytes,
                verified=False,
                error_reason="total_snapshot_too_large",
                safe_error_kind="total_too_large",
            )

        before_sha256 = _bytes_sha256(raw)
        # Blob filename is hash-based — not the original path
        blob_name = f"{_BLOB_PREFIX}{before_sha256[:32]}.bin"
        blob_path = snap_dir / blob_name

        try:
            _write_private(blob_path, raw)
        except OSError:
            try:
                import shutil
                shutil.rmtree(snap_dir, ignore_errors=True)
            except Exception:
                pass
            return SnapshotCreateResult(
                success=False,
                snapshot_id=snapshot_id,
                intent_id=intent_id,
                state="failed",
                path_count=0,
                total_bytes=total_bytes,
                verified=False,
                error_reason="cannot_write_blob",
                safe_error_kind="io_error",
            )

        # Detect file type (no binary content in metadata)
        try:
            raw.decode("utf-8")
            file_type = "text"
        except UnicodeDecodeError:
            file_type = "binary"

        total_bytes += file_bytes
        entries.append(SnapshotEntry(
            rel_path=rel_path,
            existed_before=True,
            file_type=file_type,
            before_sha256=before_sha256,
            before_bytes=file_bytes,
            recovery_blob_ref=blob_name,  # basename only, never an absolute path
        ))

    # Write manifest
    repo_id_hash = _repo_identity_hash(repo_root)
    manifest_data: dict[str, Any] = {
        "snapshot_id": snapshot_id,
        "job_id": job_id,
        "intent_id": intent_id,
        "apply_id": apply_id,
        "repository_identity_hash": repo_id_hash,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "state": "creating",
        "path_count": len(entries),
        "total_bytes": total_bytes,
        "entries": [
            {
                "rel_path": e.rel_path,
                "existed_before": e.existed_before,
                "file_type": e.file_type,
                "before_sha256": e.before_sha256,
                "before_bytes": e.before_bytes,
                "recovery_blob_ref": e.recovery_blob_ref,
            }
            for e in entries
        ],
        "warnings": warnings,
    }
    manifest_bytes = json.dumps(manifest_data, indent=2, sort_keys=True).encode("utf-8")
    manifest_hash = _bytes_sha256(manifest_bytes)
    manifest_data["manifest_hash"] = manifest_hash
    manifest_bytes = json.dumps(manifest_data, indent=2, sort_keys=True).encode("utf-8")

    manifest_path = snap_dir / "manifest.json"
    try:
        _write_private(manifest_path, manifest_bytes)
    except OSError:
        try:
            import shutil
            shutil.rmtree(snap_dir, ignore_errors=True)
        except Exception:
            pass
        return SnapshotCreateResult(
            success=False,
            snapshot_id=snapshot_id,
            intent_id=intent_id,
            state="failed",
            path_count=len(entries),
            total_bytes=total_bytes,
            verified=False,
            error_reason="cannot_write_manifest",
            safe_error_kind="io_error",
        )

    create_result = SnapshotCreateResult(
        success=True,
        snapshot_id=snapshot_id,
        intent_id=intent_id,
        state="creating",
        path_count=len(entries),
        total_bytes=total_bytes,
        verified=False,
        warnings=warnings,
    )
    _emit_snapshot_event(data_dir, job_id, "snapshot_create_completed", {
        "snapshot_id": snapshot_id,
        "intent_id": intent_id,
        "apply_id": apply_id,
        "path_count": len(entries),
        "total_bytes": total_bytes,
    })
    return create_result


# ---------------------------------------------------------------------------
# Snapshot verification (Step 1121)
# ---------------------------------------------------------------------------


def verify_snapshot(
    snapshot_id: str,
    job_id: str,
    data_dir: Path | None = None,
) -> SnapshotVerification:
    """Verify a snapshot is complete and consistent.

    Checks:
    - manifest.json exists and is readable
    - manifest hash matches content
    - every required path has an entry
    - every recovery_blob_ref that is non-empty has a matching blob file
    - each blob hash matches entry before_sha256

    Returns SnapshotVerification with verified=True only on full success.
    On success, updates manifest state to "verified".
    """
    data_dir = data_dir or resolve_data_root()
    snap_dir = _snapshot_dir(job_id, snapshot_id, data_dir)
    manifest_path = snap_dir / "manifest.json"

    if not manifest_path.exists():
        return SnapshotVerification(
            verified=False, snapshot_id=snapshot_id, state="failed",
            path_count=0, blobs_present=0, blobs_missing=0, hash_mismatches=0,
            failure_reason="manifest_missing",
        )

    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest: dict = json.loads(manifest_bytes)
    except (OSError, json.JSONDecodeError):
        return SnapshotVerification(
            verified=False, snapshot_id=snapshot_id, state="failed",
            path_count=0, blobs_present=0, blobs_missing=0, hash_mismatches=0,
            failure_reason="manifest_unreadable",
        )

    # Verify manifest hash
    stored_hash = manifest.get("manifest_hash", "")
    manifest_without_hash = {k: v for k, v in manifest.items() if k != "manifest_hash"}
    recomputed = _bytes_sha256(json.dumps(manifest_without_hash, indent=2, sort_keys=True).encode("utf-8"))
    if stored_hash != recomputed:
        return SnapshotVerification(
            verified=False, snapshot_id=snapshot_id, state="failed",
            path_count=0, blobs_present=0, blobs_missing=0, hash_mismatches=1,
            failure_reason="manifest_hash_mismatch",
        )

    entries = manifest.get("entries", [])
    blobs_present = 0
    blobs_missing = 0
    hash_mismatches = 0

    for entry in entries:
        blob_ref = entry.get("recovery_blob_ref", "")
        if not blob_ref:
            # Create target — no blob expected
            continue
        blob_path = snap_dir / blob_ref
        if not blob_path.exists():
            blobs_missing += 1
            continue
        # Verify blob hash
        try:
            actual_hash = _file_sha256(blob_path)
        except OSError:
            blobs_missing += 1
            continue
        expected_hash = entry.get("before_sha256", "")
        if actual_hash != expected_hash:
            hash_mismatches += 1
        else:
            blobs_present += 1

    if blobs_missing > 0 or hash_mismatches > 0:
        return SnapshotVerification(
            verified=False, snapshot_id=snapshot_id, state="failed",
            path_count=len(entries),
            blobs_present=blobs_present,
            blobs_missing=blobs_missing,
            hash_mismatches=hash_mismatches,
            failure_reason="blob_verification_failed",
        )

    # Update manifest state to "verified" and recompute hash
    try:
        manifest["state"] = "verified"
        manifest_without_hash = {k: v for k, v in manifest.items() if k != "manifest_hash"}
        new_hash = _bytes_sha256(
            json.dumps(manifest_without_hash, indent=2, sort_keys=True).encode("utf-8")
        )
        manifest["manifest_hash"] = new_hash
        manifest_bytes = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8")
        _write_private(manifest_path, manifest_bytes)
    except OSError:
        pass  # state update best-effort; verification itself succeeded

    verif_ok = SnapshotVerification(
        verified=True,
        snapshot_id=snapshot_id,
        state="verified",
        path_count=len(entries),
        blobs_present=blobs_present,
        blobs_missing=0,
        hash_mismatches=0,
    )
    _emit_snapshot_event(data_dir, job_id, "snapshot_verified", {
        "snapshot_id": snapshot_id,
        "path_count": len(entries),
        "blobs_present": blobs_present,
    })
    return verif_ok


# ---------------------------------------------------------------------------
# Snapshot loading
# ---------------------------------------------------------------------------


def load_snapshot(
    snapshot_id: str,
    job_id: str,
    data_dir: Path | None = None,
) -> RepositorySnapshot | None:
    """Load snapshot metadata. Returns None if not found or unreadable."""
    data_dir = data_dir or resolve_data_root()
    snap_dir = _snapshot_dir(job_id, snapshot_id, data_dir)
    manifest_path = snap_dir / "manifest.json"

    if not manifest_path.exists():
        return None
    try:
        manifest = json.loads(manifest_path.read_bytes())
    except (OSError, json.JSONDecodeError):
        return None

    entries = [
        SnapshotEntry(
            rel_path=e["rel_path"],
            existed_before=e["existed_before"],
            file_type=e.get("file_type", "text"),
            before_sha256=e.get("before_sha256", ""),
            before_bytes=e.get("before_bytes", 0),
            recovery_blob_ref=e.get("recovery_blob_ref", ""),
        )
        for e in manifest.get("entries", [])
    ]

    return RepositorySnapshot(
        snapshot_id=manifest.get("snapshot_id", snapshot_id),
        job_id=manifest.get("job_id", job_id),
        intent_id=manifest.get("intent_id", ""),
        apply_id=manifest.get("apply_id", ""),
        repository_identity_hash=manifest.get("repository_identity_hash", ""),
        created_at=manifest.get("created_at", ""),
        state=manifest.get("state", "unknown"),
        path_count=manifest.get("path_count", len(entries)),
        total_bytes=manifest.get("total_bytes", 0),
        entries=entries,
        manifest_hash=manifest.get("manifest_hash", ""),
        verified=manifest.get("state") == "verified",
    )


def _update_snapshot_state(
    snapshot_id: str,
    job_id: str,
    new_state: str,
    data_dir: Path,
) -> bool:
    """Update the state field in the manifest. Returns True if persisted.

    Failure is reported (not silently swallowed) so callers can surface degraded
    evidence (Step 1161). No raw exception text is propagated.
    """
    snap_dir = _snapshot_dir(job_id, snapshot_id, data_dir)
    manifest_path = snap_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_bytes())
        manifest["state"] = new_state
        # Recompute manifest_hash so the manifest stays internally consistent
        # and tamper-evident across legitimate state transitions (Step 1156).
        without_hash = {k: v for k, v in manifest.items() if k != "manifest_hash"}
        manifest["manifest_hash"] = _bytes_sha256(
            json.dumps(without_hash, indent=2, sort_keys=True).encode("utf-8")
        )
        _write_private(manifest_path, json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8"))
        return True
    except (OSError, json.JSONDecodeError):
        return False


# ---------------------------------------------------------------------------
# Durable apply record (Step 1124)
# ---------------------------------------------------------------------------


def save_durable_apply_record(
    record: DurableApplyRecord,
    job_id: str,
    data_dir: Path | None = None,
) -> bool:
    """Persist a durable apply record to private workspace storage."""
    data_dir = data_dir or resolve_data_root()
    records_dir = _apply_record_dir(job_id, data_dir)
    try:
        records_dir.mkdir(parents=True, exist_ok=True)
        _set_dir_private(records_dir)
        record_path = records_dir / f"{record.apply_id}.json"
        record_bytes = json.dumps(asdict(record), indent=2, sort_keys=True).encode("utf-8")
        _write_private(record_path, record_bytes)
        _emit_snapshot_event(data_dir, job_id, "apply_record_saved", {
            "apply_id": record.apply_id,
            "snapshot_id": record.snapshot_id,
            "intent_id": record.intent_id,
            "state": record.state,
            "path_count": len(record.target_paths),
        })
        return True
    except OSError:
        return False


def list_durable_apply_ids(
    job_id: str,
    data_dir: Path | None = None,
) -> list[str]:
    """List apply_ids that have a durable apply record for *job_id*. Sorted."""
    data_dir = Path(data_dir) if data_dir is not None else resolve_data_root()
    records_dir = _apply_record_dir(job_id, data_dir)
    if not records_dir.exists():
        return []
    try:
        return sorted(p.stem for p in records_dir.glob("*.json"))
    except OSError:
        return []


def load_durable_apply_record(
    apply_id: str,
    job_id: str,
    data_dir: Path | None = None,
) -> DurableApplyRecord | None:
    """Load a durable apply record. Returns None if not found or unreadable."""
    data_dir = data_dir or resolve_data_root()
    record_path = _apply_record_dir(job_id, data_dir) / f"{apply_id}.json"
    if not record_path.exists():
        return None
    try:
        data = json.loads(record_path.read_bytes())
        return DurableApplyRecord(
            apply_id=data.get("apply_id", apply_id),
            job_id=data.get("job_id", job_id),
            intent_id=data.get("intent_id", ""),
            snapshot_id=data.get("snapshot_id", ""),
            state=data.get("state", "pending"),
            target_paths=data.get("target_paths", []),
            applied_at=data.get("applied_at", ""),
            before_proof=data.get("before_proof", {}),
            after_proof=data.get("after_proof", {}),
            snapshot_verified=data.get("snapshot_verified", False),
            revert_state=data.get("revert_state", ""),
            test_run_id=data.get("test_run_id", ""),
        )
    except (OSError, json.JSONDecodeError, KeyError):
        return None


# ---------------------------------------------------------------------------
# Canonical apply-record state machine (Step 1163)
# ---------------------------------------------------------------------------

# All legal DurableApplyRecord states.
APPLY_STATES: frozenset[str] = frozenset({
    "pending",
    "applied",
    "test_pending",
    "tested_passed",
    "tested_failed",
    "revert_blocked",
    "reverted",
    "partial_revert",
    "revert_failed",
    "evidence_degraded",
})

# Legal forward transitions. Self-transition is always allowed (idempotent).
# "evidence_degraded" is reachable from any active state and recoverable to any.
_LEGAL_TRANSITIONS: dict[str, frozenset[str]] = {
    "pending": frozenset({"applied", "evidence_degraded"}),
    "applied": frozenset({
        "test_pending", "tested_passed", "tested_failed",
        "revert_blocked", "reverted", "partial_revert", "revert_failed",
        "evidence_degraded",
    }),
    "test_pending": frozenset({"tested_passed", "tested_failed", "evidence_degraded"}),
    "tested_passed": frozenset({
        "revert_blocked", "reverted", "partial_revert", "revert_failed",
        "evidence_degraded",
    }),
    "tested_failed": frozenset({
        "test_pending", "revert_blocked", "reverted", "partial_revert",
        "revert_failed", "evidence_degraded",
    }),
    "revert_blocked": frozenset({
        "applied", "reverted", "partial_revert", "revert_failed", "evidence_degraded",
    }),
    "reverted": frozenset(),  # terminal
    "partial_revert": frozenset({"reverted", "revert_failed", "evidence_degraded"}),
    "revert_failed": frozenset({"reverted", "partial_revert", "evidence_degraded"}),
    # Degraded evidence can be re-derived back to any active/terminal state.
    "evidence_degraded": frozenset(APPLY_STATES),
}


def is_legal_apply_transition(current: str, new: str) -> bool:
    """True if current → new is a legal apply-record state transition."""
    if new not in APPLY_STATES:
        return False
    if new == current:
        return True  # idempotent
    return new in _LEGAL_TRANSITIONS.get(current, frozenset())


def update_apply_record_state(
    job_id: str,
    apply_id: str,
    new_state: str,
    data_dir: Path | None = None,
    *,
    revert_state: str | None = None,
    test_run_id: str | None = None,
) -> bool:
    """Canonically update a DurableApplyRecord's state (Step 1163).

    - Atomic write (temp file + os.replace) — no torn records.
    - Legal transitions only; impossible transitions are rejected without
      mutating the record. Repeated transitions are idempotent.
    - State history is recorded as safe (state, timestamp) codes — no content.

    Returns True if the record now reflects *new_state* (including idempotent
    no-ops); False if the record is missing/unreadable or the transition is
    illegal. No raw exception text is exposed.
    """
    data_dir = Path(data_dir) if data_dir is not None else resolve_data_root()
    if new_state not in APPLY_STATES:
        return False

    record_path = _apply_record_dir(job_id, data_dir) / f"{apply_id}.json"
    if not record_path.exists():
        return False
    try:
        data = json.loads(record_path.read_bytes())
    except (OSError, json.JSONDecodeError):
        return False

    current = data.get("state", "pending")
    if not is_legal_apply_transition(current, new_state):
        return False

    data["state"] = new_state
    if revert_state is not None:
        data["revert_state"] = revert_state
    if test_run_id is not None:
        data["test_run_id"] = test_run_id

    history = data.get("state_history")
    if not isinstance(history, list):
        history = []
    if current != new_state or not history:
        history.append({
            "state": new_state,
            "at": datetime.now(timezone.utc).isoformat(),
        })
    data["state_history"] = history[-50:]  # bounded

    tmp_path = record_path.with_suffix(".json.tmp")
    try:
        tmp_path.write_bytes(
            json.dumps(data, indent=2, sort_keys=True).encode("utf-8")
        )
        try:
            os.chmod(tmp_path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
        os.replace(tmp_path, record_path)
        return True
    except OSError:
        try:
            tmp_path.unlink()
        except OSError:
            pass
        return False


# ---------------------------------------------------------------------------
# Authoritative snapshot truth (Step 1156)
# ---------------------------------------------------------------------------


def _check_snapshot_integrity(snap_dir: Path) -> dict[str, Any]:
    """Read-only integrity check of a snapshot directory.

    Does NOT mutate the manifest (unlike verify_snapshot, which rewrites state).
    Safe to call against reverted/blocked snapshots without corrupting state.

    Returns a dict with: manifest_exists, manifest_ok, blobs_expected,
    blobs_present, blobs_missing, hash_mismatches, recovery_available, verified.
    """
    manifest_path = snap_dir / "manifest.json"
    result: dict[str, Any] = {
        "manifest_exists": False,
        "manifest_ok": False,
        "blobs_expected": 0,
        "blobs_present": 0,
        "blobs_missing": 0,
        "hash_mismatches": 0,
        "recovery_available": False,
        "verified": False,
    }
    if not manifest_path.exists():
        return result
    result["manifest_exists"] = True

    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
    except (OSError, json.JSONDecodeError):
        return result

    stored_hash = manifest.get("manifest_hash", "")
    without_hash = {k: v for k, v in manifest.items() if k != "manifest_hash"}
    recomputed = _bytes_sha256(
        json.dumps(without_hash, indent=2, sort_keys=True).encode("utf-8")
    )
    result["manifest_ok"] = bool(stored_hash) and stored_hash == recomputed

    entries = manifest.get("entries", [])
    for entry in entries:
        blob_ref = entry.get("recovery_blob_ref", "")
        if not blob_ref:
            continue
        result["blobs_expected"] += 1
        blob_path = snap_dir / blob_ref
        if not blob_path.exists():
            result["blobs_missing"] += 1
            continue
        try:
            actual = _file_sha256(blob_path)
        except OSError:
            result["blobs_missing"] += 1
            continue
        if actual != entry.get("before_sha256", ""):
            result["hash_mismatches"] += 1
        else:
            result["blobs_present"] += 1

    result["recovery_available"] = (
        result["blobs_missing"] == 0 and result["hash_mismatches"] == 0
    )
    result["verified"] = (
        result["manifest_ok"]
        and result["blobs_missing"] == 0
        and result["hash_mismatches"] == 0
    )
    return result


def _find_apply_record(
    job_id: str,
    apply_id: str | None,
    intent_id: str | None,
    data_dir: Path,
) -> tuple[DurableApplyRecord | None, bool]:
    """Locate the durable apply record for a snapshot-truth query.

    Resolution order:
      1. exact apply_id, if given (never ambiguous)
      2. records matching an explicit intent_id (ambiguous if >1 match)
      3. latest applied_at across all records for the job (job-wide default —
         the most recent apply is the canonical "current" one, not ambiguous)

    Returns (record, ambiguous). ambiguous=True only when an explicit intent_id
    resolves to more than one apply — the caller must surface that rather than
    silently pick a winner (R-0065). Returns (None, False) when no record exists.
    """
    if apply_id:
        return load_durable_apply_record(apply_id, job_id, data_dir), False

    records_dir = _apply_record_dir(job_id, data_dir)
    if not records_dir.exists():
        return None, False

    candidates: list[DurableApplyRecord] = []
    try:
        files = sorted(records_dir.glob("*.json"))
    except OSError:
        return None, False
    for rec_path in files:
        rec = load_durable_apply_record(rec_path.stem, job_id, data_dir)
        if rec is None:
            continue
        if intent_id and rec.intent_id != intent_id:
            continue
        candidates.append(rec)

    if not candidates:
        return None, False
    # Latest by applied_at (ISO timestamps sort lexically); fall back to apply_id.
    candidates.sort(key=lambda r: (r.applied_at or "", r.apply_id))
    # Explicit intent with multiple matching applies is genuinely ambiguous.
    ambiguous = bool(intent_id) and len(candidates) > 1
    return candidates[-1], ambiguous


def build_snapshot_truth(
    job_id: str,
    apply_id: str | None = None,
    intent_id: str | None = None,
    data_dir: Path | None = None,
) -> SnapshotTruth:
    """Build the authoritative snapshot/apply truth (Step 1156).

    Loads the DurableApplyRecord and RepositorySnapshot, verifies the current
    manifest and recovery blobs (read-only), and returns a single safe truth
    object. Never relies on events or artifact metadata as authority.

    Shared source for Proof Chain, File Provenance, Readiness, Review Bundle,
    and `do --continue`. No raw paths or blob refs are exposed.
    """
    data_dir = Path(data_dir) if data_dir is not None else resolve_data_root()

    record, ambiguous = _find_apply_record(job_id, apply_id, intent_id, data_dir)
    blockers: list[str] = []

    if record is None:
        # No durable linkage — everything unknown, explicitly.
        return SnapshotTruth(
            job_id=job_id,
            snapshot_id="",
            apply_id=apply_id or "",
            intent_id=intent_id or "",
            snapshot_exists=False,
            manifest_exists=False,
            recovery_material_available=False,
            snapshot_verified_now=False,
            apply_state="unknown",
            revert_state="unknown",
            restore_verified=False,
            drift_blocked=False,
            evidence_status="unknown",
            blockers=["no_apply_record"],
        )

    resolved_apply_id = record.apply_id
    resolved_intent_id = record.intent_id or (intent_id or "")
    snapshot_id = record.snapshot_id

    snapshot = load_snapshot(snapshot_id, job_id, data_dir) if snapshot_id else None
    snap_dir = _snapshot_dir(job_id, snapshot_id, data_dir) if snapshot_id else None
    snapshot_dir_exists = bool(snap_dir and snap_dir.exists())

    if snapshot is None:
        blockers.append("no_snapshot")
        return SnapshotTruth(
            job_id=job_id,
            snapshot_id=snapshot_id,
            apply_id=resolved_apply_id,
            intent_id=resolved_intent_id,
            snapshot_exists=snapshot_dir_exists,
            manifest_exists=False,
            recovery_material_available=False,
            snapshot_verified_now=False,
            apply_state=record.state or "unknown",
            revert_state=record.revert_state or "unknown",
            restore_verified=False,
            drift_blocked=record.revert_state == "drifted",
            evidence_status="degraded",
            blockers=blockers,
        )

    integrity = _check_snapshot_integrity(snap_dir)  # type: ignore[arg-type]
    manifest_exists = bool(integrity["manifest_exists"])
    recovery_material_available = bool(integrity["recovery_available"])
    snapshot_verified_now = bool(integrity["verified"])

    if not manifest_exists:
        blockers.append("manifest_missing")
    elif not integrity["manifest_ok"]:
        blockers.append("manifest_tampered")
    if integrity["blobs_missing"] > 0:
        blockers.append("recovery_material_missing")
    if integrity["hash_mismatches"] > 0:
        blockers.append("recovery_material_corrupt")

    # Derive revert/drift/restore truth from durable state (authoritative).
    snap_state = snapshot.state or ""
    apply_state = record.state or "unknown"
    revert_state = record.revert_state or ""
    if not revert_state:
        if snap_state in ("reverted", "partial_revert", "revert_failed"):
            revert_state = snap_state
        elif snap_state == "blocked_drift":
            revert_state = "drifted"

    drift_blocked = revert_state == "drifted" or snap_state == "blocked_drift"
    restore_verified = (
        snap_state == "reverted" or record.state == "reverted"
    ) and revert_state in ("reverted", "clean", "")

    if revert_state == "partial_revert" or snap_state == "partial_revert":
        blockers.append("partial_revert")
    if revert_state == "revert_failed" or snap_state == "revert_failed":
        blockers.append("revert_failed")
    if drift_blocked:
        blockers.append("post_apply_drift")
    if not snapshot_verified_now and revert_state not in (
        "reverted",
        "partial_revert",
        "revert_failed",
    ):
        # Active apply must have a verifiable snapshot; reverted ones legitimately
        # change state, so missing live verification there is not a fresh blocker.
        blockers.append("snapshot_not_verified")
    if ambiguous:
        # Explicit intent resolved to >1 apply — surface, never silently pick (R-0065).
        blockers.append("ambiguous_intent_apply")

    # Evidence status reflects durable-material consistency only — independent of
    # advisory blockers (drift, ambiguity). Complete when the manifest is intact,
    # all recovery blobs verify, and any revert that occurred fully succeeded.
    material_ok = (
        bool(integrity["manifest_ok"])
        and integrity["blobs_missing"] == 0
        and integrity["hash_mismatches"] == 0
    )
    if not material_ok or revert_state in ("partial_revert", "revert_failed"):
        evidence_status = "degraded"
    else:
        evidence_status = "complete"

    return SnapshotTruth(
        job_id=job_id,
        snapshot_id=snapshot_id,
        apply_id=resolved_apply_id,
        intent_id=resolved_intent_id,
        snapshot_exists=snapshot_dir_exists,
        manifest_exists=manifest_exists,
        recovery_material_available=recovery_material_available,
        snapshot_verified_now=snapshot_verified_now,
        apply_state=apply_state,
        revert_state=revert_state or ("clean" if apply_state == "applied" else ""),
        restore_verified=restore_verified,
        drift_blocked=drift_blocked,
        evidence_status=evidence_status,
        blockers=blockers,
    )


# ---------------------------------------------------------------------------
# Revert service (Steps 1125-1127)
# ---------------------------------------------------------------------------


def revert_repository_apply(
    job_id: str,
    apply_id: str,
    repo_root: Path,
    data_dir: Path | None = None,
) -> RepositoryRevertResult:
    """Revert a repository apply by restoring pre-apply snapshot state.

    Explicit call only. Not automatic.

    Gates (in order):
    1. Load apply record
    2. Load snapshot
    3a. Load job from storage (job_not_found → permission_denied)
    3b. Verify Capability.repo_revert is allowed for the job
    3c. Load persisted RunContract and evaluate ContractAction.REVERT
    4. Verify snapshot integrity again
    5. Check post-apply drift (Step 1126)
    6. Restore files from private blobs
    7. Verify restored state (Step 1127)
    8. Update apply record + snapshot state

    No Git reset/checkout/clean. No symlink traversal.
    No revert if files changed after apply (drift detection).
    No caller-supplied permission booleans (Step 1137).
    """
    from uuid import UUID as _UUID

    from packages.orchestration.permissions import (
        Capability as _Capability,
    )
    from packages.orchestration.permissions import (
        is_allowed as _is_allowed,
    )
    from packages.orchestration.run_contract import (
        ContractAction as _ContractAction,
    )
    from packages.orchestration.run_contract import (
        ensure_contract as _ensure_contract,
    )
    from packages.orchestration.run_contract import (
        evaluate_run_action as _evaluate_run_action,
    )
    from packages.orchestration.storage import (
        JobNotFoundError as _JobNotFoundError,
    )
    from packages.orchestration.storage import (
        load_job as _load_job,
    )

    data_dir = data_dir or resolve_data_root()
    repo_root = repo_root.resolve()

    _emit_snapshot_event(data_dir, job_id, "revert_started", {
        "apply_id": apply_id, "job_id": job_id,
    })

    # Gate 1: Load apply record
    record = load_durable_apply_record(apply_id, job_id, data_dir)
    if record is None:
        return RepositoryRevertResult(
            success=False, apply_id=apply_id, snapshot_id="",
            state="blocked", paths_restored=0, paths_deleted=0, paths_failed=0,
            block_reason="no_apply_record",
            safe_summary="No apply record found for this apply_id.",
        )

    # Gate 2: Load snapshot
    snapshot = load_snapshot(record.snapshot_id, job_id, data_dir)
    if snapshot is None:
        return RepositoryRevertResult(
            success=False, apply_id=apply_id, snapshot_id=record.snapshot_id,
            state="blocked", paths_restored=0, paths_deleted=0, paths_failed=0,
            block_reason="no_snapshot",
            safe_summary="No snapshot found — cannot revert.",
        )

    # Gate 3a: Load job from storage — no bypass booleans (Step 1137)
    try:
        _job_uuid = _UUID(job_id)
        _job = _load_job(_job_uuid, data_dir)
    except (ValueError, _JobNotFoundError):
        _emit_snapshot_event(data_dir, job_id, "revert_blocked", {
            "apply_id": apply_id, "block_reason": "permission_denied",
        })
        return RepositoryRevertResult(
            success=False, apply_id=apply_id, snapshot_id=record.snapshot_id,
            state="blocked", paths_restored=0, paths_deleted=0, paths_failed=0,
            block_reason="permission_denied",
            safe_summary="Job not found — cannot verify revert permission.",
        )

    # Gate 3b: Permission check — Capability.repo_revert must be allowed
    if not _is_allowed(_job, _Capability.repo_revert):
        _emit_snapshot_event(data_dir, job_id, "revert_blocked", {
            "apply_id": apply_id, "block_reason": "permission_denied",
        })
        return RepositoryRevertResult(
            success=False, apply_id=apply_id, snapshot_id=record.snapshot_id,
            state="blocked", paths_restored=0, paths_deleted=0, paths_failed=0,
            block_reason="permission_denied",
            safe_summary="Permission denied: repo_revert capability not granted for this job.",
        )

    # Gate 3c: Contract check — ContractAction.REVERT must be allowed
    _contract = _ensure_contract(_job)
    _decision = _evaluate_run_action(_contract, _ContractAction.REVERT)
    if not _decision.allowed:
        _emit_snapshot_event(data_dir, job_id, "revert_blocked", {
            "apply_id": apply_id, "block_reason": "contract_denied",
        })
        return RepositoryRevertResult(
            success=False, apply_id=apply_id, snapshot_id=record.snapshot_id,
            state="blocked", paths_restored=0, paths_deleted=0, paths_failed=0,
            block_reason="contract_denied",
            safe_summary="Run contract does not permit revert action.",
        )

    # Gate 4: Verify snapshot integrity
    verification = verify_snapshot(record.snapshot_id, job_id, data_dir)
    if not verification.verified:
        return RepositoryRevertResult(
            success=False, apply_id=apply_id, snapshot_id=record.snapshot_id,
            state="blocked", paths_restored=0, paths_deleted=0, paths_failed=0,
            block_reason="verify_failed",
            safe_summary="Snapshot verification failed — cannot safely revert.",
        )

    # Gate 5: Post-apply drift detection (Step 1126)
    after_proof = record.after_proof
    drift_paths: list[str] = []
    for entry in snapshot.entries:
        rel_path = entry.rel_path
        expected_after = after_proof.get(rel_path, {})
        if not expected_after:
            continue
        current_path = repo_root / rel_path
        expected_sha = expected_after.get("sha256", "")
        expected_existed = expected_after.get("existed", True)

        if not expected_sha:
            continue

        if not current_path.exists():
            if expected_existed:
                drift_paths.append(rel_path)
        else:
            try:
                current_sha = _file_sha256(current_path)
                if current_sha != expected_sha:
                    drift_paths.append(rel_path)
            except OSError:
                drift_paths.append(rel_path)

    if drift_paths:
        _update_snapshot_state(record.snapshot_id, job_id, "blocked_drift", data_dir)
        return RepositoryRevertResult(
            success=False, apply_id=apply_id, snapshot_id=record.snapshot_id,
            state="blocked", paths_restored=0, paths_deleted=0, paths_failed=0,
            block_reason="post_apply_drift",
            drift_path_count=len(drift_paths),
            safe_summary=(
                f"Revert blocked: {len(drift_paths)} file(s) changed after apply. "
                "Manual review required before revert."
            ),
        )

    # Gate 6: Restore files from private blobs
    snap_dir = _snapshot_dir(job_id, record.snapshot_id, data_dir)
    paths_restored = 0
    paths_deleted = 0
    paths_failed = 0

    for entry in snapshot.entries:
        rel_path = entry.rel_path
        target = repo_root / rel_path

        if not entry.existed_before:
            # File was created by the apply — delete it now
            if target.exists():
                try:
                    target.unlink()
                    paths_deleted += 1
                except OSError:
                    paths_failed += 1
            continue

        # File existed before — restore from blob
        blob_path = snap_dir / entry.recovery_blob_ref
        if not blob_path.exists():
            paths_failed += 1
            continue

        try:
            raw = blob_path.read_bytes()
        except OSError:
            paths_failed += 1
            continue

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            paths_restored += 1
        except OSError:
            paths_failed += 1

    # Gate 7: Verify restored state (Step 1127)
    verification_failures = 0
    for entry in snapshot.entries:
        rel_path = entry.rel_path
        target = repo_root / rel_path

        if not entry.existed_before:
            # Should not exist now
            if target.exists():
                verification_failures += 1
        else:
            # Should exist with matching hash
            if not target.exists():
                verification_failures += 1
            else:
                try:
                    actual_sha = _file_sha256(target)
                    if actual_sha != entry.before_sha256:
                        verification_failures += 1
                except OSError:
                    verification_failures += 1

    # Gate 8: Update states
    if paths_failed == 0 and verification_failures == 0:
        final_state = "reverted"
        success = True
    elif paths_failed > 0 or verification_failures > 0:
        if paths_restored > 0 or paths_deleted > 0:
            final_state = "partial_revert"
        else:
            final_state = "revert_failed"
        success = False
    else:
        final_state = "reverted"
        success = True

    # Persist durable state — failures are reported, never silently swallowed
    # (Step 1161). The actual file-restore outcome above remains truthful.
    evidence_warnings: list[str] = []
    snapshot_state_persisted = _update_snapshot_state(
        record.snapshot_id, job_id, final_state, data_dir
    )
    if not snapshot_state_persisted:
        evidence_warnings.append("snapshot_state_persist_failed")

    apply_record_persisted = _persist_apply_record_revert_state(
        job_id, apply_id, final_state, success, data_dir
    )
    if not apply_record_persisted:
        evidence_warnings.append("apply_record_persist_failed")

    revert_event = "revert_completed" if success else "revert_failed"
    event_result = _emit_snapshot_event(data_dir, job_id, revert_event, {
        "apply_id": apply_id,
        "snapshot_id": record.snapshot_id,
        "state": final_state,
        "paths_restored": paths_restored,
        "paths_deleted": paths_deleted,
        "paths_failed": paths_failed,
        "verification_failures": verification_failures,
        "evidence_degraded": bool(evidence_warnings),
    })
    if event_result.status != "complete":
        evidence_warnings.append(f"event_{event_result.status}")

    # Evidence status: even when file restore succeeded, a durable-record write
    # failure degrades evidence so readiness/proof cannot claim fully verified.
    if not apply_record_persisted or not snapshot_state_persisted:
        event_evidence_status = "failed"
    elif event_result.status != "complete":
        event_evidence_status = "partial"
    else:
        event_evidence_status = "complete"

    summary = (
        f"Revert {'complete' if success else 'incomplete'}: "
        f"{paths_restored} restored, {paths_deleted} deleted, {paths_failed} failed, "
        f"{verification_failures} verification failures."
    )
    if evidence_warnings:
        summary += " Evidence degraded — durable record/event persistence incomplete."

    return RepositoryRevertResult(
        success=success,
        apply_id=apply_id,
        snapshot_id=record.snapshot_id,
        state=final_state,
        paths_restored=paths_restored,
        paths_deleted=paths_deleted,
        paths_failed=paths_failed,
        verification_failures=verification_failures,
        safe_summary=summary,
        apply_record_persisted=apply_record_persisted,
        snapshot_state_persisted=snapshot_state_persisted,
        event_evidence_status=event_evidence_status,
        evidence_warnings=evidence_warnings,
    )


def _persist_apply_record_revert_state(
    job_id: str,
    apply_id: str,
    final_state: str,
    success: bool,
    data_dir: Path,
) -> bool:
    """Persist the post-revert apply-record state. Returns True if written.

    Reports failure to the caller (no silent `except: pass`, Step 1161). No raw
    exception text is exposed. Routes through the canonical state updater.
    """
    new_apply_state = "reverted" if success else final_state
    return update_apply_record_state(
        job_id, apply_id, new_apply_state, data_dir, revert_state=final_state
    )
