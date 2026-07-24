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
    project_flag: str | None = None,
    all_projects: bool = False,
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

    from packages.orchestration.project_scope import resolve_scope, scoped_jobs

    scope = resolve_scope(
        project_flag=project_flag,
        all_projects=all_projects,
        cwd=repo,
    )
    jobs, degraded, skipped_files = scoped_jobs(scope)

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

    first_active_short = None
    for s in ("running", "planned", "pending", "paused"):
        group = by_state.get(s, [])
        if group:
            first_active_short = group[0]["short_id"]
            break

    jobs_next = 'remedy do "<mission>"'
    if first_active_short:
        jobs_next = f"remedy decision list {first_active_short}"
    decisions_next = 'remedy do "<mission>"'
    if decisions_open and first_active_short:
        decisions_next = f"remedy decision list {first_active_short}"
    stops_next = "remedy status"
    if stops_pending and first_active_short:
        stops_next = f"remedy job stop --status {first_active_short}"
    runtime_next = 'remedy do "<mission>"'

    if json_output:
        result = {
            "project": project_slug,
            "scope": "all projects" if scope.all_projects else (project_slug or "current"),
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

    scope_label = "all projects" if scope.all_projects else (project_slug or "current project")
    print(f"Jobs ({scope_label}):")
    if not jobs and not degraded:
        print("  No jobs.")
    else:
        state_order = ["running", "planned", "pending", "paused", "completed", "failed", "cancelled"]
        printed = False
        for s in state_order:
            group = by_state.get(s, [])
            if group:
                print(f"  {s} ({len(group)}):")
                for entry in group:
                    print(f"    {entry['short_id']}  {entry['name']}")
                printed = True
        for s in sorted(by_state.keys()):
            if s not in state_order:
                group = by_state[s]
                print(f"  {s} ({len(group)}):")
                for entry in group:
                    print(f"    {entry['short_id']}  {entry['name']}")
                printed = True
        if not printed:
            print("  No jobs.")

    if degraded:
        print(f"  Warning: {len(skipped_files)} corrupt job file(s) skipped.")
    print(f"  Next: {jobs_next}")

    print(f"\nDecisions: {decisions_open} open")
    print(f"  Next: {decisions_next}")
    print(f"Runtime: {runtime_status}")
    if runtime_warning:
        print(f"  Warning: {runtime_warning}")
    print(f"  Next: {runtime_next}")
    print(f"Stops: {stops_pending} pending")
    print(f"  Next: {stops_next}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "status.run": lambda args: _cmd_status(
        repo=getattr(args, "repo", None) or ".",
        project_flag=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=getattr(args, "json", False),
    ),
}
