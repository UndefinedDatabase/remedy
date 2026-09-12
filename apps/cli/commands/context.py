"""Context group command handlers."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

from packages.orchestration.data_paths import lookup_job_id
from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_context_inspect(
    job_id_str: str,
    *,
    task_id: str | None = None,
    budget: int = 4000,
    json_output: bool = False,
) -> None:
    try:
        job_id = lookup_job_id(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if task_id is not None:
        try:
            UUID(task_id)
        except ValueError:
            print(f"Error: invalid task ID: {task_id!r}", file=sys.stderr)
            sys.exit(1)
        task_ids = {str(t.id) for t in job.tasks}
        if task_id not in task_ids:
            print(f"Error: task {task_id!r} not found in job", file=sys.stderr)
            sys.exit(1)

    from packages.orchestration.context_inspector import (
        export_context_inspection_json,
        inspect_context,
        summarize_context_inspection,
    )
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    inspection = inspect_context(
        job, events,
        task_id=task_id,
        budget_tokens=budget,
    )

    if json_output:
        print(_json.dumps(export_context_inspection_json(inspection), sort_keys=True))
    else:
        print(summarize_context_inspection(inspection))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "context.inspect": lambda args: _cmd_context_inspect(
        args.job_id,
        task_id=getattr(args, "task_id", None),
        budget=int(getattr(args, "budget", "4000")),
        json_output=getattr(args, "json", False),
    ),
}
