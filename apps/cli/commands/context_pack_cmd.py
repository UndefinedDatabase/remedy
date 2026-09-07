"""The `context.pack` handler, split out of `context.py` so its import can die.

WHY THIS FILE EXISTS. `packages.orchestration.context_pack` is one of the twenty-four
prototype-cluster modules F260's Design deletes. While this handler sat in
`apps/cli/commands/context.py` — which also hosts the SURVIVING `context.inspect` — that file
was a surviving CONSUMER of the cluster, and its import was an edge the deletion had to cut
first. This file is instead listed in `CLUSTER_COMMAND_HANDLERS` in
`tests/orchestration/test_cluster_deletion_map.py`, so it dies WITH the module rather than
blocking it.

The command id `context.pack` is UNCHANGED. This is a move, not a rename; renaming commands is
F261's work.
"""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_context_pack(
    job_id_str: str,
    *,
    budget: int = 2000,
    mode: str = "compact",
    json_output: bool = False,
) -> None:
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

    from packages.orchestration.context_pack import (
        build_context_pack,
        export_context_pack_json,
        summarize_context_pack,
    )
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    pack = build_context_pack(job, events, budget=budget, mode=mode)

    if json_output:
        print(_json.dumps(export_context_pack_json(pack), sort_keys=True))
    else:
        print(summarize_context_pack(pack))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "context_pack_created",
        budget=pack.budget,
        estimated_tokens=pack.estimated_tokens,
        mode=pack.mode,
        truncated=pack.truncated,
        section_count=len(pack.sections),
    )


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "context.pack": lambda args: _cmd_context_pack(
        args.job_id,
        budget=int(getattr(args, "budget", "2000")),
        mode=getattr(args, "mode", "compact"),
        json_output=args.json,
    ),
}
