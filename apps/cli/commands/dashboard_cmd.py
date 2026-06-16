"""Dashboard group command handlers."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    import argparse


def _cmd_dashboard_job(job_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.dashboard import build_job_dashboard, summarize_job_dashboard
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import JobNotFoundError, load_job
    from packages.orchestration.timeline import load_run_events

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

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    data = build_job_dashboard(job, events)

    if json_output:
        print(_json.dumps(data, sort_keys=True))
    else:
        print(summarize_job_dashboard(data))


def _cmd_dashboard_project(project_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.project_store import load_project

    from packages.orchestration.dashboard import build_project_dashboard
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job
    from packages.orchestration.timeline import load_run_events

    try:
        project = load_project(project_id_str)
    except (KeyError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    data_dir = resolve_data_root()
    jobs = []
    all_events: dict[str, list] = {}
    for jid in project.get("job_ids", []):
        try:
            j = load_job(UUID(jid))
            jobs.append(j)
            all_events[jid] = load_run_events(data_dir, UUID(jid))
        except Exception:
            pass

    data = build_project_dashboard(project_id_str, jobs, all_events)

    if json_output:
        print(_json.dumps(data, sort_keys=True))
    else:
        lines = [
            f"Project Dashboard: {project_id_str[:8]}",
            f"  Jobs: {data['job_count']}",
            f"  Open decisions: {data['open_decision_count']}",
            f"  Readiness: min={data['readiness_summary']['min_level']}, max={data['readiness_summary']['max_level']}",
        ]
        print("\n".join(lines))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "dashboard.job": lambda args: _cmd_dashboard_job(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "dashboard.project": lambda args: _cmd_dashboard_project(
        args.project_id,
        json_output=getattr(args, "json", False),
    ),
}
