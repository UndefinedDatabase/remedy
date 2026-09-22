"""Change group command handlers."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

if TYPE_CHECKING:
    import argparse


def _cmd_change_list(
    job_id_str: str,
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    from packages.orchestration.approval_queue import list_patch_intents
    from packages.orchestration.change_set import (
        derive_change_set,
        export_change_list_json,
        summarize_change_list,
    )
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    changes = derive_change_set(job, events)
    # A change's date is its patch intent's own `created_at` — the field
    # `patch list` already sorts by; a change has no flat date of its own.
    created = {i["intent_id"]: i.get("created_at") or "" for i in list_patch_intents(job)}
    try:
        changes = apply_list_options(
            changes,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda c: created.get(c.intent_id, ""),
                "status": lambda c: c.status,
                "risk": lambda c: c.risk,
                "target_path": lambda c: c.target_path,
            },
            default_sort_field="created_at",
            date_getter=lambda c: created.get(c.intent_id) or None,
        )
    except ListOptionError as exc:
        fail("invalid_list_option", str(exc), json_output=json_output)

    if json_output:
        emit_ok(**export_change_list_json(str(job_id), changes))
    else:
        print(summarize_change_list(changes))


def _cmd_change_show(job_id_str: str, intent_id: str, *, json_output: bool = False) -> None:
    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    from packages.orchestration.change_set import (
        derive_change_set,
        export_change_show_json,
        summarize_change_show,
    )
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    changes = derive_change_set(job, events)

    entry = next((c for c in changes if c.intent_id == intent_id), None)
    if entry is None:
        fail("change_not_found", f"change not found for intent {intent_id!r}",
             json_output=json_output)

    if json_output:
        emit_ok(**export_change_show_json(str(job_id), entry))
    else:
        print(summarize_change_show(entry))


def _cmd_change_proof(job_id_str: str, *, path: str | None = None, json_output: bool = False) -> None:
    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    # Validate path — no traversal
    if path and (".." in path or path.startswith("/")):
        fail("invalid_path", "path must be relative without '..'",
             json_output=json_output)

    from packages.orchestration.proof_chain import (
        build_proof_chain,
        export_proof_chain_json,
        summarize_proof_chain,
    )
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    # Pass data_dir so proof uses authoritative snapshot truth, not stale
    # artifact metadata or event presence (Step 1158).
    chain = build_proof_chain(job, events, path=path, data_dir=data_dir)

    if json_output:
        emit_ok(**export_proof_chain_json(chain))
    else:
        print(summarize_proof_chain(chain))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "change.list": lambda args: _cmd_change_list(
        args.job_id,
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "change.show": lambda args: _cmd_change_show(args.job_id, args.intent_id, json_output=args.json),
    "change.proof": lambda args: _cmd_change_proof(args.job_id, path=getattr(args, "path", None), json_output=args.json),
}
