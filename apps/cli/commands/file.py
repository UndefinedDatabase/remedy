"""File group command handlers."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_file_why(job_id_str: str, path: str, *, json_output: bool = False) -> None:
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

    from packages.orchestration.file_provenance import (
        build_file_provenance,
        export_file_provenance_json,
        summarize_file_provenance,
    )
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)

    # Pass data_dir so provenance uses the authoritative DurableApplyRecord /
    # snapshot truth, not stale artifact metadata (Step 1157).
    prov = build_file_provenance(job, events, path, data_dir=data_dir)

    if json_output:
        print(_json.dumps(export_file_provenance_json(prov), sort_keys=True))
    else:
        print(summarize_file_provenance(prov))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "file.why": lambda args: _cmd_file_why(args.job_id, args.path, json_output=args.json),
}
