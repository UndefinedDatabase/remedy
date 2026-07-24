"""Handler for ``remedy status`` — honest overview of project state (F147 T002)."""

from __future__ import annotations

import json as _json
import sys
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable


def _cmd_status(
    *,
    repo: str = ".",
    json_output: bool = False,
) -> None:
    """Golden-path: project status overview. Always exits 0."""
    from packages.orchestration.project_registry import resolve_project

    project = resolve_project(repo)
    project_slug = None
    if project is None:
        if not json_output:
            print(
                "No project registered for this repo. Run: remedy init",
                file=sys.stderr,
            )
    else:
        project_slug = project.slug

    from packages.orchestration.storage import list_jobs_safe

    jobs, degraded, skipped_files = list_jobs_safe()

    by_state: dict[str, list[dict]] = defaultdict(list)
    for j in jobs:
        state = j.state.value
        by_state[state].append({
            "job_id": str(j.id),
            "short_id": str(j.id)[:8],
            "name": j.name,
            "state": state,
        })

    decisions_open = 0
    for j in jobs:
        try:
            from packages.orchestration.data_paths import resolve_data_root
            from packages.orchestration.decision_queue import list_decisions
            from packages.orchestration.timeline import load_run_events

            events = load_run_events(resolve_data_root(), j.id)
            decs = list_decisions(j, events)
            decisions_open += sum(1 for d in decs if d.status == "open")
        except Exception:
            pass

    _TERMINAL = {"completed", "failed", "cancelled"}
    stops_pending = 0
    for j in jobs:
        if j.state.value in _TERMINAL:
            continue
        try:
            from packages.orchestration.safe_points import stop_requested
            if stop_requested(str(j.id)) is not None:
                stops_pending += 1
        except Exception:
            pass

    runtime_status = "unknown"
    runtime_warning = None
    try:
        from packages.runtimes.dev_server import (
            STATE_ABSENT,
            STATE_VALID,
            load_state_result,
        )
        load = load_state_result(repo)
        if load.kind == STATE_ABSENT:
            runtime_status = "stopped"
        elif load.kind == STATE_VALID and load.state is not None:
            runtime_status = load.state.status
        else:
            runtime_status = "unknown"
            runtime_warning = f"runtime state unreadable: {load.error or load.kind}"
    except Exception:
        pass

    if json_output:
        result = {
            "project": project_slug,
            "jobs": dict(by_state),
            "decisions_open": decisions_open,
            "runtime": runtime_status,
            "stops_pending": stops_pending,
        }
        if runtime_warning:
            result["runtime_warning"] = runtime_warning
        if degraded:
            result["degraded"] = True
            result["skipped_files"] = skipped_files
        print(_json.dumps(result, indent=2))
        return

    if project_slug:
        print(f"Project: {project_slug}")
    print()

    if not jobs and not degraded:
        print("No jobs.")
    else:
        state_order = ["running", "planned", "pending", "paused", "completed", "failed", "cancelled"]
        printed = False
        for s in state_order:
            group = by_state.get(s, [])
            if group:
                print(f"{s} ({len(group)}):")
                for entry in group:
                    print(f"  {entry['short_id']}  {entry['name']}")
                printed = True
        for s in sorted(by_state.keys()):
            if s not in state_order:
                group = by_state[s]
                print(f"{s} ({len(group)}):")
                for entry in group:
                    print(f"  {entry['short_id']}  {entry['name']}")
                printed = True
        if not printed:
            print("No jobs.")

    if degraded:
        print(f"\nWarning: {len(skipped_files)} corrupt job file(s) skipped.")

    print(f"\nDecisions: {decisions_open} open")
    print(f"Runtime: {runtime_status}")
    if runtime_warning:
        print(f"  Warning: {runtime_warning}")
    print(f"Stops: {stops_pending} pending")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "status.run": lambda args: _cmd_status(
        repo=getattr(args, "repo", None) or ".",
        json_output=getattr(args, "json", False),
    ),
}
