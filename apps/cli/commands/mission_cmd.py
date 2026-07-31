"""`remedy mission` — the persistent goal above a chain of jobs (F056).

``start`` creates a mission, ``list`` shows the ones this project has, ``show``
renders one mission's chain with each linked job's state as the job store
reports it right now, and ``continue`` adds the next job — with a task that
verifies the previous one already sitting at the head of its plan.

Creation is ALWAYS explicit.  There is no code path here that a run can trip
over: a mission exists because someone typed ``remedy mission start``, or
because someone answered the plan-approval opt-in with yes.  A plain do-flow
leaves no mission behind.

Scoping follows F148: the project comes from ``--project``, ``REMEDY_PROJECT``
or the working directory, exactly as ``remedy job list`` and ``remedy queue``
resolve it.  There is no cross-project mission; ``--all-projects`` only widens
the LISTING over the project areas that exist on disk.
"""
from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse

EXIT_ERROR = 1
EXIT_USAGE = 2
#: The contract's exit code for "no project" — the same one `job create` uses.
EXIT_NO_PROJECT = 3


def _resolve_project_id(project_flag: str | None) -> str:
    """The one project this command acts on, or exit 3 with the same wording as job create."""
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        select_project,
    )

    try:
        project, _source = select_project(project_flag, ".")
    except ProjectNotFoundError:
        print(
            "Error: no project found. Run: remedy init\n"
            "  or pass --project <slug-or-id>",
            file=sys.stderr,
        )
        sys.exit(EXIT_NO_PROJECT)
    return str(project.id)


def _mission_json(mission: Any) -> dict[str, Any]:
    """The JSON shape of one mission — the record, plus the states it renders."""
    from packages.orchestration.mission_state import mission_job_state_label

    body = mission.to_json()
    body["job_links"] = [
        {**link.to_json(), "job_state": mission_job_state_label(link.job_id)}
        for link in mission.job_links
    ]
    return body


def _cmd_mission_start(goal: str, *, project: str | None = None,
                       json_output: bool = False) -> None:
    from packages.orchestration.mission_state import MissionError, create_mission

    project_id = _resolve_project_id(project)
    try:
        mission = create_mission(project_id, goal)
    except MissionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if json_output:
        print(_json.dumps({"version": 1, "mission": _mission_json(mission)},
                          sort_keys=True))
        return
    print(mission.id)
    print(f"  Goal: {mission.goal}")
    print(f"  Link the first job with: remedy mission continue "
          f"{mission.id[:12]} \"<next step>\"")


def _cmd_mission_list(*, project: str | None = None, all_projects: bool = False,
                      json_output: bool = False) -> None:
    from packages.orchestration.mission_state import (
        list_missions_safe,
        project_ids_with_missions,
        render_mission_row,
    )

    if all_projects:
        project_ids = project_ids_with_missions()
    else:
        project_ids = [_resolve_project_id(project)]

    rows: list[tuple[str, Any]] = []
    skipped_total = 0
    for project_id in project_ids:
        missions, _degraded, skipped = list_missions_safe(project_id)
        skipped_total += len(skipped)
        rows.extend((project_id, mission) for mission in missions)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "missions": [_mission_json(m) for _pid, m in rows],
            "skipped_records": skipped_total,
        }, sort_keys=True))
        return

    if not rows:
        print("No missions found.")
    for project_id, mission in rows:
        label = f"  (project: {project_id[:8]})" if all_projects else ""
        print(f"{render_mission_row(mission)}{label}")
    if skipped_total:
        print(f"  ({skipped_total} unreadable mission record(s) skipped)",
              file=sys.stderr)


def _load_mission_or_exit(project_id: str, mission_id: str) -> Any:
    from packages.orchestration.mission_state import (
        MissionError,
        MissionNotFoundError,
        load_mission,
        resolve_mission_id,
    )

    try:
        resolved = resolve_mission_id(project_id, mission_id)
        return load_mission(project_id, resolved)
    except MissionNotFoundError:
        print(f"Error: no mission {mission_id} in this project.", file=sys.stderr)
        print("  List them with: remedy mission list", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    except MissionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)


def _cmd_mission_show(mission_id: str, *, project: str | None = None,
                      json_output: bool = False) -> None:
    from packages.orchestration.mission_state import render_mission_chain

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)

    if json_output:
        print(_json.dumps({"version": 1, "mission": _mission_json(mission)},
                          sort_keys=True))
        return
    for line in render_mission_chain(mission):
        print(line)


def _cmd_mission_continue(mission_id: str, next_step: str, *,
                          project: str | None = None,
                          json_output: bool = False) -> None:
    from packages.orchestration.mission_state import (
        MissionError,
        continue_mission,
        is_verify_task,
    )

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)

    try:
        job = continue_mission(project_id, mission.id, next_step)
    except MissionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    verify = job.tasks[0] if job.tasks and is_verify_task(job.tasks[0]) else None
    if json_output:
        print(_json.dumps({
            "version": 1,
            "mission_id": mission.id,
            "job_id": str(job.id),
            "role": job.metadata.get("mission_role", ""),
            "verify_first_task": (
                {"description": verify.description,
                 "verify_command": verify.inputs.get("verify_command", "")}
                if verify is not None else None),
            "tasks": [t.description for t in job.tasks],
        }, sort_keys=True))
        return

    print(str(job.id))
    print(f"  Mission: {mission.id[:12]}  ({job.metadata.get('mission_role', '')})")
    if verify is not None:
        print(f"  Task 1 (injected): {verify.description}")
        print("  The follow-up work cannot start until that task completes.")
    else:
        print("  First job of this mission — there is no previous state to verify.")
    print(f"  Chain: remedy mission show {mission.id[:12]}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "mission.start": lambda args: _cmd_mission_start(
        args.goal,
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "mission.list": lambda args: _cmd_mission_list(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=getattr(args, "json", False),
    ),
    "mission.continue": lambda args: _cmd_mission_continue(
        args.mission_id,
        args.next_step,
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "mission.show": lambda args: _cmd_mission_show(
        args.mission_id,
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
}
