"""Worker group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_workers(*, json_output: bool = False) -> None:
    from packages.orchestration.worker_adapters import (
        export_worker_specs_json, list_worker_specs, summarize_worker_specs,
    )

    specs = list_worker_specs()
    if json_output:
        print(_json.dumps(export_worker_specs_json(specs), sort_keys=True))
    else:
        print(summarize_worker_specs(specs))


def _cmd_worker_recommend(job_id_str: str, *, json_output: bool = False) -> None:
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

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events
    from packages.orchestration.worker_recommend import (
        export_worker_recommendation_json,
        recommend_worker,
        summarize_worker_recommendation,
    )

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    rec = recommend_worker(job, events)

    if json_output:
        print(_json.dumps(export_worker_recommendation_json(rec), sort_keys=True))
    else:
        print(summarize_worker_recommendation(rec))


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "worker.list": lambda args: _cmd_workers(json_output=args.json),
    "worker.recommend": lambda args: _cmd_worker_recommend(args.job_id, json_output=args.json),
}
