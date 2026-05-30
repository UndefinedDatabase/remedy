"""Patch group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, load_job, save_job

if TYPE_CHECKING:
    import argparse


def _cmd_list_patch_intents(job_id_str: str) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import format_intent_list, list_patch_intents
    intents = list_patch_intents(job)
    print(format_intent_list(intents))


def _cmd_show_patch_intent(job_id_str: str, intent_id: str) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
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
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
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
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
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
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
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


def _cmd_revert_patch_intent(job_id_str: str, intent_id: str, *, json_output: bool = False) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.patch_revert import format_revert_result, revert_patch_intent

    result = revert_patch_intent(job, intent_id)
    if result.state == "blocked":
        print(f"Error: {result.blocked_reason}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "state": result.state, "intent_id": result.intent_id,
            "target_path": result.target_path, "action": result.action,
            "outcome": result.outcome, "existed_before": result.existed_before,
            "bytes_written": result.bytes_written, "line_count": result.line_count,
            "before_sha256": result.before_sha256, "after_sha256": result.after_sha256,
        }, sort_keys=True))
    else:
        print(format_revert_result(result))


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "patch.list": lambda args: _cmd_list_patch_intents(args.job_id),
    "patch.show": lambda args: _cmd_show_patch_intent(args.job_id, args.intent_id),
    "patch.approve": lambda args: _cmd_approve_patch_intent(args.job_id, args.intent_id, getattr(args, "reason", None)),
    "patch.reject": lambda args: _cmd_reject_patch_intent(args.job_id, args.intent_id, getattr(args, "reason", None)),
    "patch.apply": lambda args: _cmd_apply_patch_intent(args.job_id, args.intent_id, json_output=getattr(args, "json", False)),
    "patch.revert": lambda args: _cmd_revert_patch_intent(args.job_id, args.intent_id, json_output=getattr(args, "json", False)),
}
