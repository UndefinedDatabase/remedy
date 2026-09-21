"""File group command handlers."""

from __future__ import annotations

import json as _json
from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import fail
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

if TYPE_CHECKING:
    import argparse


def _cmd_file_why(job_id_str: str, path: str, *, json_output: bool = False) -> None:
    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

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
