"""Readiness group command handlers."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_readiness_job(job_id_str: str, *, json_output: bool = False) -> None:
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

    from packages.orchestration.autonomy_readiness import (
        assess_job_readiness,
        export_readiness_json,
        summarize_readiness,
    )
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    report = assess_job_readiness(job, events, data_dir=data_dir)

    if json_output:
        print(_json.dumps(export_readiness_json(report), sort_keys=True))
    else:
        print(summarize_readiness(report))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "readiness_assessed",
        scope=report.scope,
        highest_eligible_level=report.highest_eligible_level,
        missing_count=sum(len(a.missing_signals) for a in report.levels),
        blocker_count=sum(len(a.blockers) for a in report.levels),
    )


def _cmd_readiness_project(project_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.autonomy_readiness import (
        assess_project_readiness,
        export_readiness_json,
        summarize_readiness,
    )
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.project_registry import ProjectNotFoundError, load_project
    from packages.orchestration.storage import load_job
    from packages.orchestration.timeline import load_run_events

    try:
        project = load_project(UUID(project_id_str))
    except (ValueError, ProjectNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    data_dir = resolve_data_root()
    jobs = []
    all_events: dict[str, list] = {}
    for jid in project.job_ids:
        try:
            j = load_job(UUID(jid))
            jobs.append(j)
            all_events[jid] = load_run_events(data_dir, j.id)
        except Exception:
            continue

    report = assess_project_readiness(str(project.id), jobs, all_events, data_dir=data_dir)

    if json_output:
        print(_json.dumps(export_readiness_json(report), sort_keys=True))
    else:
        print(summarize_readiness(report))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "readiness.job": lambda args: _cmd_readiness_job(args.job_id, json_output=args.json),
    "readiness.project": lambda args: _cmd_readiness_project(args.project_id, json_output=args.json),
}
