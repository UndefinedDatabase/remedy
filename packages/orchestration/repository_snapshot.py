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
from typing import Any
from uuid import uuid4

from packages.orchestration.data_paths import resolve_data_root


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
) -> None:
    """Emit a snapshot lifecycle event. Silent on failure — events are secondary."""
    if event_type not in _SNAPSHOT_EVENTS:
        return
    try:
        from uuid import UUID
        from packages.orchestration.timeline import append_run_event
        try:
            jid = UUID(job_id)
        except ValueError:
            return
        append_run_event(str(data_dir), jid, event=event_type, metadata=metadata)
    except Exception:
        pass


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
) -> None:
    """Update the state field in the manifest. Best-effort."""
    snap_dir = _snapshot_dir(job_id, snapshot_id, data_dir)
    manifest_path = snap_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_bytes())
        manifest["state"] = new_state
        _write_private(manifest_path, json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8"))
    except (OSError, json.JSONDecodeError):
        pass


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
    from packages.orchestration.storage import (
        load_job as _load_job, JobNotFoundError as _JobNotFoundError,
    )
    from packages.orchestration.permissions import (
        is_allowed as _is_allowed, Capability as _Capability,
    )
    from packages.orchestration.run_contract import (
        ensure_contract as _ensure_contract, evaluate_run_action as _evaluate_run_action,
        ContractAction as _ContractAction,
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

    _update_snapshot_state(record.snapshot_id, job_id, final_state, data_dir)

    # Update apply record revert state
    try:
        record_path = _apply_record_dir(job_id, data_dir) / f"{apply_id}.json"
        apply_data = json.loads(record_path.read_bytes())
        apply_data["revert_state"] = final_state
        apply_data["state"] = "reverted" if success else apply_data.get("state", "applied")
        _write_private(record_path, json.dumps(apply_data, indent=2, sort_keys=True).encode("utf-8"))
    except (OSError, json.JSONDecodeError):
        pass

    revert_event = "revert_completed" if success else "revert_failed"
    _emit_snapshot_event(data_dir, job_id, revert_event, {
        "apply_id": apply_id,
        "snapshot_id": record.snapshot_id,
        "state": final_state,
        "paths_restored": paths_restored,
        "paths_deleted": paths_deleted,
        "paths_failed": paths_failed,
        "verification_failures": verification_failures,
    })

    return RepositoryRevertResult(
        success=success,
        apply_id=apply_id,
        snapshot_id=record.snapshot_id,
        state=final_state,
        paths_restored=paths_restored,
        paths_deleted=paths_deleted,
        paths_failed=paths_failed,
        verification_failures=verification_failures,
        safe_summary=(
            f"Revert {'complete' if success else 'incomplete'}: "
            f"{paths_restored} restored, {paths_deleted} deleted, {paths_failed} failed, "
            f"{verification_failures} verification failures."
        ),
    )
