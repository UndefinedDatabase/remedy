"""Snapshot group command handlers — Step 1129."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _cmd_snapshot_inspect(job_id_str: str, snapshot_id: str, *, as_json: bool = False) -> None:
    """Show snapshot metadata. Safe fields only — no recovery content, no blob data."""
    from uuid import UUID

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.repository_snapshot import load_snapshot
    from packages.orchestration.storage import JobNotFoundError, load_job

    try:
        job_id = UUID(job_id_str)
    except ValueError:
        if as_json:
            print(_json.dumps({"error": "invalid_job_id", "job_id": job_id_str}))
        else:
            print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)

    try:
        load_job(job_id)
    except JobNotFoundError:
        if as_json:
            print(_json.dumps({"error": "job_not_found", "job_id": job_id_str}))
        else:
            print(f"Error: job {job_id_str!r} not found.", file=sys.stderr)
        sys.exit(1)

    data_dir = resolve_data_root()
    snap = load_snapshot(snapshot_id, job_id_str, data_dir)
    if snap is None:
        if as_json:
            print(_json.dumps({"error": "snapshot_not_found", "snapshot_id": snapshot_id}))
        else:
            print(f"Error: snapshot {snapshot_id!r} not found.", file=sys.stderr)
        sys.exit(1)

    # Safe metadata — no recovery_blob_ref, no raw content
    entry_meta = [
        {
            "rel_path": e.rel_path,
            "existed_before": e.existed_before,
            "file_type": e.file_type,
            "before_bytes": e.before_bytes,
        }
        for e in snap.entries
    ]

    out = {
        "snapshot_id": snap.snapshot_id,
        "job_id": snap.job_id,
        "intent_id": snap.intent_id,
        "apply_id": snap.apply_id,
        "repository_identity_hash": snap.repository_identity_hash,
        "created_at": snap.created_at,
        "state": snap.state,
        "verified": snap.verified,
        "path_count": snap.path_count,
        "total_bytes": snap.total_bytes,
        "entries": entry_meta,
    }

    if as_json:
        print(_json.dumps(out))
        return

    print(f"Snapshot {snap.snapshot_id}")
    print(f"  job_id:    {snap.job_id}")
    print(f"  intent_id: {snap.intent_id}")
    if snap.apply_id:
        print(f"  apply_id:  {snap.apply_id}")
    print(f"  created:   {snap.created_at}")
    print(f"  state:     {snap.state}  verified={snap.verified}")
    print(f"  paths:     {snap.path_count}  total_bytes={snap.total_bytes}")
    for e in snap.entries:
        status = "existed" if e.existed_before else "absent"
        print(f"    {e.rel_path}  [{status}  {e.file_type}  {e.before_bytes}B]")


def _cmd_snapshot_list_applies(job_id_str: str, *, as_json: bool = False) -> None:
    """List durable apply records for a job. Safe fields only."""
    from uuid import UUID

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.repository_snapshot import load_durable_apply_record
    from packages.orchestration.storage import JobNotFoundError, load_job

    try:
        job_id = UUID(job_id_str)
    except ValueError:
        if as_json:
            print(_json.dumps({"error": "invalid_job_id", "job_id": job_id_str}))
        else:
            print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)

    try:
        load_job(job_id)
    except JobNotFoundError:
        if as_json:
            print(_json.dumps({"error": "job_not_found", "job_id": job_id_str}))
        else:
            print(f"Error: job {job_id_str!r} not found.", file=sys.stderr)
        sys.exit(1)

    data_dir = resolve_data_root()
    records_dir = data_dir / "workspaces" / job_id_str / "apply_records"

    apply_ids: list[str] = []
    if records_dir.exists():
        apply_ids = [p.stem for p in records_dir.glob("*.json")]

    records_out = []
    for aid in sorted(apply_ids):
        rec = load_durable_apply_record(aid, job_id_str, data_dir)
        if rec is None:
            continue
        records_out.append({
            "apply_id": rec.apply_id,
            "intent_id": rec.intent_id,
            "snapshot_id": rec.snapshot_id,
            "state": rec.state,
            "revert_state": rec.revert_state,
            "applied_at": rec.applied_at,
            "path_count": len(rec.target_paths),
            "snapshot_verified": rec.snapshot_verified,
        })

    out = {"job_id": job_id_str, "apply_records": records_out}

    if as_json:
        print(_json.dumps(out))
        return

    if not records_out:
        print(f"No apply records found for job {job_id_str}.")
        return

    print(f"Apply records for job {job_id_str}:")
    for r in records_out:
        print(
            f"  {r['apply_id']}  state={r['state']}  "
            f"snapshot={r['snapshot_id'][:12]}  "
            f"paths={r['path_count']}  "
            f"verified={r['snapshot_verified']}"
        )


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "snapshot.inspect": lambda args: _cmd_snapshot_inspect(
        args.job_id, args.snapshot_id, as_json=getattr(args, "json", False)
    ),
    "snapshot.list-applies": lambda args: _cmd_snapshot_list_applies(
        args.job_id, as_json=getattr(args, "json", False)
    ),
}
