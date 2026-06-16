"""Guide group command handlers."""

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


def _cmd_guide_job(job_id_str: str, *, json_output: bool = False) -> None:
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

    from packages.orchestration.guidance import (
        build_guidance_cards,
        export_guidance_json,
        summarize_guidance,
    )
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    cards = build_guidance_cards(job, events)

    if json_output:
        print(_json.dumps(export_guidance_json(job, cards), sort_keys=True))
    else:
        print(summarize_guidance(job, cards))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "guide.job": lambda args: _cmd_guide_job(args.job_id, json_output=args.json),
}
