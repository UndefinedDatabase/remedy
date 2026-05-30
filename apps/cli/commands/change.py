"""Change group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_change_list(job_id_str: str, *, json_output: bool = False) -> None:
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

    from packages.orchestration.change_set import (
        derive_change_set,
        export_change_list_json,
        summarize_change_list,
    )
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    changes = derive_change_set(job, events)

    if json_output:
        print(_json.dumps(export_change_list_json(str(job_id), changes), sort_keys=True))
    else:
        print(summarize_change_list(changes))


def _cmd_change_show(job_id_str: str, intent_id: str, *, json_output: bool = False) -> None:
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
        print(f"Error: change not found for intent {intent_id!r}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps(export_change_show_json(str(job_id), entry), sort_keys=True))
    else:
        print(summarize_change_show(entry))


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "change.list": lambda args: _cmd_change_list(args.job_id, json_output=args.json),
    "change.show": lambda args: _cmd_change_show(args.job_id, args.intent_id, json_output=args.json),
}
