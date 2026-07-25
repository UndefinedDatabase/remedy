"""Patch group command handlers."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from packages.orchestration.data_paths import resolve_job_id
from packages.orchestration.storage import JobNotFoundError, load_job, save_job

if TYPE_CHECKING:
    import argparse


def _cmd_list_patch_intents(job_id_str: str) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import format_intent_list, list_patch_intents
    intents = list_patch_intents(job)
    print(format_intent_list(intents))


def _cmd_show_patch_intent(job_id_str: str, intent_id: str) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import (
        _find_artifact_for_intent,
        format_intent_detail,
        get_patch_intent,
    )

    item = get_patch_intent(job, intent_id)
    if item is None:
        print(f"Error: patch intent {intent_id!r} not found in job {job_id}.", file=sys.stderr)
        print("Use 'remedy patch list <job_id>' to see available intent IDs.", file=sys.stderr)
        sys.exit(1)

    diff_preview: str | None = None
    found = _find_artifact_for_intent(job, intent_id)
    if found is not None:
        artifact, _ = found
        diff_preview = artifact.metadata.get("patch_intent_diff_preview")

    print(format_intent_detail(item, diff_preview))


def _cmd_approve_patch_intent(job_id_str: str, intent_id: str, reason: str | None) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import set_approval_state
    from packages.orchestration.run_log import RunLogWriter

    try:
        entry = set_approval_state(job, intent_id, "approved", reason=reason)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    save_job(job)
    log = RunLogWriter(job_id=job.id)
    log.log(
        "patch_intent_approved", outcome="approved",
        intent_id=entry["intent_id"], target_path=entry["target_path"],
        risk=entry["risk"], reason_present=reason is not None,
    )
    print(f"Approved: {entry['intent_id']} ({entry['target_path']})")
    print(f"  reason: {'recorded' if reason else 'none'}")
    print("Note: approval is metadata only — no files have been modified.")


def _cmd_reject_patch_intent(job_id_str: str, intent_id: str, reason: str | None) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import set_approval_state
    from packages.orchestration.run_log import RunLogWriter

    try:
        entry = set_approval_state(job, intent_id, "rejected", reason=reason)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    save_job(job)
    log = RunLogWriter(job_id=job.id)
    log.log(
        "patch_intent_rejected", outcome="rejected",
        intent_id=entry["intent_id"], target_path=entry["target_path"],
        risk=entry["risk"], reason_present=reason is not None,
    )
    print(f"Rejected: {entry['intent_id']} ({entry['target_path']})")
    print(f"  reason: {'recorded' if reason else 'none'}")
    print("Note: rejection is metadata only — no files have been modified.")


def _cmd_apply_patch_intent(job_id_str: str, intent_id: str, *, json_output: bool = False) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.patch_apply import apply_patch_intent, format_apply_result

    result = apply_patch_intent(job, intent_id)
    if result.state == "blocked":
        print(f"Error: {result.blocked_reason}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "state": result.state, "intent_id": result.intent_id,
            "target_path": result.target_path, "action": result.action,
            "outcome": result.outcome, "bytes_written": result.bytes_written,
            "line_count": result.line_count,
        }, sort_keys=True))
    else:
        print(format_apply_result(result))


def _cmd_revert_patch_intent(
    job_id_str: str,
    intent_id: str,
    *,
    apply_id: str | None = None,
    json_output: bool = False,
) -> None:
    """Revert a patch apply via the durable Repository Snapshot service.

    apply_id is canonical. intent_id is used as apply_id fallback (patch_apply.py
    stores apply_id == intent_id for markdown applies).
    """
    job_id = resolve_job_id(job_id_str)
    try:
        load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from pathlib import Path as _Path

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.repository_snapshot import (
        load_durable_apply_record,
        revert_repository_apply,
    )
    from packages.orchestration.storage import load_job as _load_job

    data_dir = resolve_data_root()
    job = _load_job(job_id)

    # Resolve apply_id: explicit arg → intent_id-as-apply_id fallback
    resolved_apply_id = apply_id or intent_id

    # Validate apply record exists; if not and apply_id not given, report clearly
    rec = load_durable_apply_record(resolved_apply_id, job_id_str, data_dir)
    if rec is None and not apply_id:
        # intent_id may not match apply_id — check by scanning records
        records_dir = data_dir / "workspaces" / job_id_str / "apply_records"
        matches = []
        if records_dir.exists():
            for p in records_dir.glob("*.json"):
                candidate = load_durable_apply_record(p.stem, job_id_str, data_dir)
                if candidate and candidate.intent_id == intent_id:
                    matches.append(candidate)
        if len(matches) == 1:
            resolved_apply_id = matches[0].apply_id
        elif len(matches) > 1:
            if json_output:
                print(_json.dumps({
                    "error": "ambiguous_intent_id",
                    "intent_id": intent_id,
                    "apply_ids": [m.apply_id for m in matches],
                }))
            else:
                print(
                    f"Error: intent {intent_id!r} matches {len(matches)} apply records. "
                    "Use --apply-id to specify one.",
                    file=sys.stderr,
                )
            sys.exit(1)
        else:
            if json_output:
                print(_json.dumps({"error": "no_apply_record", "intent_id": intent_id}))
            else:
                print(
                    f"Error: no durable apply record found for intent {intent_id!r}. "
                    "Use 'remedy snapshot list-applies <job_id>' to inspect.",
                    file=sys.stderr,
                )
            sys.exit(1)

    # repo_root from job metadata
    target_repo_str: str = job.metadata.get("target_repo", "") or ""
    if not target_repo_str:
        if json_output:
            print(_json.dumps({"error": "no_target_repo", "job_id": job_id_str}))
        else:
            print(f"Error: job {job_id_str!r} has no target_repo in metadata.", file=sys.stderr)
        sys.exit(1)
    repo_root = _Path(target_repo_str)

    result = revert_repository_apply(job_id_str, resolved_apply_id, repo_root, data_dir)

    if json_output:
        print(_json.dumps({
            "success": result.success,
            "apply_id": result.apply_id,
            "snapshot_id": result.snapshot_id,
            "state": result.state,
            "paths_restored": result.paths_restored,
            "paths_deleted": result.paths_deleted,
            "paths_failed": result.paths_failed,
            "block_reason": result.block_reason,
            "drift_path_count": result.drift_path_count,
            "verification_failures": result.verification_failures,
            "safe_summary": result.safe_summary,
        }, sort_keys=True))
        if not result.success:
            sys.exit(1)
        return

    if not result.success:
        print(f"Error: revert blocked — {result.block_reason}", file=sys.stderr)
        print(f"  {result.safe_summary}", file=sys.stderr)
        sys.exit(1)

    print(f"Reverted: {result.apply_id}")
    print(f"  {result.safe_summary}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "patch.list": lambda args: _cmd_list_patch_intents(args.job_id),
    "patch.show": lambda args: _cmd_show_patch_intent(args.job_id, args.intent_id),
    "patch.approve": lambda args: _cmd_approve_patch_intent(args.job_id, args.intent_id, getattr(args, "reason", None)),
    "patch.reject": lambda args: _cmd_reject_patch_intent(args.job_id, args.intent_id, getattr(args, "reason", None)),
    "patch.apply": lambda args: _cmd_apply_patch_intent(args.job_id, args.intent_id, json_output=getattr(args, "json", False)),
    "patch.revert": lambda args: _cmd_revert_patch_intent(
        args.job_id, args.intent_id,
        apply_id=getattr(args, "apply_id", None),
        json_output=getattr(args, "json", False),
    ),
}
