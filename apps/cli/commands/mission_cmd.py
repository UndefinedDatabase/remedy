"""`remedy mission` — the persistent goal above a chain of jobs (F056).

``start`` creates a mission, ``list`` shows the ones this project has, ``show``
renders one mission's chain with each linked job's state as the job store
reports it right now, ``plan`` compiles the goal into milestones (F069), and
``continue`` adds the next job — with a task that
verifies the previous one already sitting at the head of its plan.
``achieve``/``abandon``/``pause``/``resume`` are the explicit status
transitions, and ``watchdog`` reports F077's tripwires without writing
anything.  They are not the only writers: the orchestrator loop's terminal
moves and the watchdog's own pause move the status with no human in the loop.

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
    """``remedy mission show <id>`` — one mission's chain, led by why it stopped.

    Read-only.  When the mission is PAUSED, the trips its ledger already
    RECORDS lead the output (DECISION F077 D12): nothing is re-evaluated here,
    so a reader sees the trip that actually caused THIS pause rather than a
    fresh verdict over the same ledger, and ``remedy mission watchdog`` stays
    the one surface that re-evaluates.

    The lead lives in this handler and not in ``render_mission_chain`` because
    that renderer takes a ``Mission`` and nothing else: the trips live in the
    LEDGER, which ``orchestrator_loop`` owns, and ``orchestrator_loop`` imports
    ``mission_state`` — so reaching the ledger from the renderer would invert
    that dependency and build the very import cycle ``watchdog`` keeps its own
    imports inside function bodies to avoid.
    """
    from packages.orchestration.mission_state import (
        MISSION_STATUS_PAUSED,
        render_mission_chain,
    )

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)

    # The PAUSE is the condition, not the history: a mission that ran past an
    # old trip and is active again is not waiting for anybody.
    trips: list[Any] = []
    if mission.status == MISSION_STATUS_PAUSED:
        from packages.orchestration.orchestrator_loop import read_ledger
        from packages.orchestration.watchdog import latest_trips_from_ledger

        trips = latest_trips_from_ledger(read_ledger(project_id, mission.id))

    if json_output:
        print(_json.dumps({"version": 1, "mission": _mission_json(mission),
                           "watchdog_trips": [t.to_json() for t in trips]},
                          sort_keys=True))
        return

    # Empty trips print NOTHING, so an unpaused mission's output is byte for
    # byte what it was before F077.
    if trips:
        print("STOPPED: this mission was paused automatically and is waiting "
              "for you.")
        for trip in trips:
            print(f"  {trip.kind}  (since iteration {trip.since_iteration})")
            print(f"    {trip.what}")
            for key in sorted(trip.numbers):
                print(f"    {key}: {trip.numbers[key]}")
        print(f"  Full evidence: remedy mission watchdog {mission.id}")
        print("")
    for line in render_mission_chain(mission):
        print(line)


def _cmd_mission_plan(mission_id: str, *, project: str | None = None,
                      json_output: bool = False, no_llm: bool = False) -> None:
    """``remedy mission plan`` — compile the mission's goal into milestones.

    Compiling creates NO jobs and starts nothing: it writes the plan, the
    per-milestone Definition-of-Done files and a rendered ``mission_plan.md``
    into the mission's evidence area, and records the plan on the record.
    """
    from packages.orchestration.mission_compiler import (
        MissionPlanInProgressError,
        plan_mission,
    )
    from packages.orchestration.mission_state import MissionError

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)

    call_fn = None
    if not no_llm:
        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.mission_plan_schema import MissionPlanDraft

        call_fn = make_structured_call_fn(MissionPlanDraft)

    try:
        # `make_structured_call_fn` is Ollama-backed, so the provider is named
        # here exactly as the flight-plan site names it in `do_cmd.py`. Under
        # `--no-llm` there is no call and therefore no trace to carry a label.
        outcome = plan_mission(project_id, mission.id, call_fn,
                               provider="ollama", provider_kind="ollama")
    except MissionPlanInProgressError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    except MissionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "mission_id": mission.id,
            "plan_version": outcome.version,
            "source": outcome.source,
            "error_hint": outcome.error_hint,
            "plan_path": str(outcome.plan_path or ""),
            "milestones": [
                {"id": m.id, "goal": m.goal, "depends_on": list(m.depends_on),
                 "dod_ref": m.dod_ref, "jobs_draft": len(m.jobs_draft)}
                for m in outcome.plan.milestones
            ],
            "jobs_created": 0,
        }, sort_keys=True))
        return

    print(mission.id)
    print(f"  Plan v{outcome.version}  ({outcome.source}, "
          f"{len(outcome.plan.milestones)} milestone(s))")
    if outcome.error_hint:
        print(f"  No provider plan: {outcome.error_hint}")
    for ms in outcome.plan.milestones:
        deps = ", ".join(ms.depends_on) if ms.depends_on else "none"
        print(f"    {ms.id}  {ms.goal}")
        print(f"          depends on: {deps}  |  DoD: {ms.dod_ref}  |  "
              f"{len(ms.jobs_draft)} draft job outline(s)")
    print(f"  Rendered: {outcome.plan_path}")
    print("  No jobs were created and nothing was started — draft outlines are "
          "not runnable jobs.")


def _status_for_verb(verb: str) -> str:
    """The status a transition verb names.  The verb IS the rule."""
    from packages.orchestration.mission_state import (
        MISSION_STATUS_ABANDONED,
        MISSION_STATUS_ACHIEVED,
        MISSION_STATUS_ACTIVE,
        MISSION_STATUS_PAUSED,
    )

    return {
        "achieve": MISSION_STATUS_ACHIEVED,
        "abandon": MISSION_STATUS_ABANDONED,
        "pause": MISSION_STATUS_PAUSED,
        "resume": MISSION_STATUS_ACTIVE,
    }[verb]


def _cmd_mission_set_status(mission_id: str, verb: str, *,
                            project: str | None = None,
                            json_output: bool = False) -> None:
    """The body behind ``achieve``, ``abandon``, ``pause`` and ``resume``.

    A thin wrapper over ``mission_state.set_mission_status``: the verb names
    the status, and that is the whole rule.  There is deliberately NO
    transition table here — any valid status may follow any other, because a
    human typing the command is the authority on what the mission's state is.

    This surface is not the only writer, though.  The orchestrator loop's own
    terminal moves write ``achieved`` and ``abandoned`` with no human in the
    loop — see ``mission_state.set_mission_status`` for the full caller list —
    so F056's "nothing moves on its own" holds for this COMMAND, not for the
    status field.

    Since F077 the autonomy watchdog writes ``paused`` the same way and with no
    human in the loop either, so the status field has three kinds of writer and
    this command is only one of them.
    """
    from packages.orchestration.mission_state import MissionError, set_mission_status

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)

    try:
        updated = set_mission_status(project_id, mission.id, _status_for_verb(verb))
    except MissionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if json_output:
        print(_json.dumps({"version": 1, "mission": _mission_json(updated)},
                          sort_keys=True))
        return
    print(updated.id)
    print(f"  Status: {updated.status}")


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


def _orchestrator_call_fn():
    """The orchestrator role's provider call_fn, or None when there is none.

    The SAME factory the mission plan command uses (``make_structured_call_fn``),
    bound to the move schema and to the model named by ``orchestrator.model``.
    Returning None is not a failure mode to work around — it is the honest
    "no provider" the loop turns into a terminal, never a fake run.
    """
    from packages.orchestration.intake import make_structured_call_fn
    from packages.orchestration.orchestrator_move_schema import OrchestratorMove
    from packages.orchestration.role_config import resolve_orchestrator_model

    return make_structured_call_fn(
        OrchestratorMove, model=resolve_orchestrator_model())


def _cmd_mission_run_loop(mission_id: str, *, project: str | None = None,
                          iterations: str | None = None,
                          json_output: bool = False,
                          no_llm: bool = False) -> None:
    """``remedy mission run <id>`` — run the F070 orchestrator loop.

    One iteration is: assemble the mission's context, take ONE
    schema-validated move from the orchestrator-role model, execute it through
    Remedy's existing verbs, append a ledger entry. The loop stops on a
    terminal move, the iteration limit, a stop request, or a refusal that had
    to be escalated — every one of them an honest status, printed here.
    """
    from packages.orchestration.orchestrator_loop import (
        TERMINAL_NO_PROVIDER,
        loop_limits_from_config,
        read_ledger,
        render_ledger,
        run_mission,
    )

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)

    try:
        limits = loop_limits_from_config(
            iterations_flag=int(iterations) if iterations else None)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_USAGE)

    call_fn = None if no_llm else _orchestrator_call_fn()
    # `_orchestrator_call_fn` is unconditionally `make_structured_call_fn`,
    # which is Ollama-backed, so the provider is named here exactly as the plan
    # site above names it. Under `--no-llm` there is no call and so no trace to
    # label. The label reaches the prompt trace through `run_mission`'s own
    # per-iteration recorder (DECISION F105 D11).
    result = run_mission(mission.id, limits, project_id=project_id,
                         call_fn=call_fn,
                         provider="ollama", provider_kind="ollama")
    entries = read_ledger(project_id, mission.id)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "mission_id": mission.id,
            "terminal": result.terminal,
            "detail": result.detail,
            "iterations": result.iterations,
            "max_iterations": limits.max_iterations,
            "ledger_entries": len(entries),
        }, sort_keys=True))
        return

    print(mission.id)
    print(f"  Terminal: {result.terminal}")
    if result.detail:
        print(f"  {result.detail}")
    print(f"  Iterations this run: {result.iterations} "
          f"(limit {limits.max_iterations})")
    if result.terminal == TERMINAL_NO_PROVIDER:
        print("  No orchestrator provider is available, so nothing was "
              "decided. Remedy does not invent a run.")
    if result.entries:
        print("")
        print(render_ledger([e.to_json() for e in result.entries]))
    print(f"  Full ledger: remedy mission ledger {mission.id[:12]}")


def _cmd_mission_ledger(mission_id: str, *, project: str | None = None,
                        json_output: bool = False) -> None:
    """``remedy mission ledger <id>`` — the mission's decision trail, in full.

    Read-only. Renders every iteration the loop ever recorded for this
    mission, across every run, so a human can reconstruct what was decided
    without opening a source file.
    """
    from packages.orchestration.orchestrator_loop import read_ledger, render_ledger

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)
    entries = read_ledger(project_id, mission.id)

    if json_output:
        print(_json.dumps({"version": 1, "mission_id": mission.id,
                           "entries": entries}, sort_keys=True))
        return

    print(mission.id)
    print(f"  Goal: {mission.goal}")
    print(f"  Iterations recorded: {len(entries)}")
    print("")
    print(render_ledger(entries))


def _cmd_mission_watchdog(mission_id: str, *, project: str | None = None,
                          json_output: bool = False) -> None:
    """``remedy mission watchdog <id>`` — what the watchdog sees, on demand.

    Read-only, and that is the whole point of the command: it evaluates every
    F077 tripwire over the mission's ledger and reports what fired, pausing
    nothing and raising no decision.  The watchdog acts only from inside
    ``remedy mission run``; asking it what it sees must not itself stop a
    mission.
    """
    from packages.orchestration.watchdog import evaluate_mission

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)
    trips = evaluate_mission(project_id, mission.id)

    if json_output:
        print(_json.dumps({"version": 1, "mission_id": mission.id,
                           "trips": [trip.to_json() for trip in trips]},
                          sort_keys=True))
        return

    print(mission.id)
    print(f"  Status: {mission.status}")
    print(f"  Tripwires fired: {len(trips)}")
    for trip in trips:
        print("")
        print(f"  {trip.kind}  (since iteration {trip.since_iteration})")
        print(f"    {trip.what}")
        for key in sorted(trip.numbers):
            print(f"    {key}: {trip.numbers[key]}")


def _cmd_mission_handoff(mission_id: str, *, json_output: bool = False) -> None:
    """``remedy mission handoff <id>`` — the explicit boundary trigger (F079).

    The mission id alone is enough: ``build_handoff`` resolves which project
    holds the mission, exactly as ``run_mission`` does, so a boundary can be
    declared from wherever the operator happens to be standing. Composing is a
    pure artifact — no mission, job or queue state moves — and building twice
    on unchanged state returns the SAME file rather than a second account.
    """
    from packages.orchestration.handoff import (
        MissionForHandoffNotFoundError,
        build_handoff,
        read_handoff,
    )

    try:
        path = build_handoff(mission_id)
    except MissionForHandoffNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    body = read_handoff(path)
    rendered = path.with_suffix(".md")
    if json_output:
        print(_json.dumps({"version": 1, "mission_id": body["mission_id"],
                           "handoff": str(path), "rendered": str(rendered),
                           "gaps": body.get("gaps", [])}, sort_keys=True))
        return

    print(str(path))
    print(f"  Rendered: {rendered}")
    gaps = body.get("gaps") or []
    print(f"  Gaps: {len(gaps)}")
    for gap in gaps:
        print(f"    - {gap.get('source', '')}: {gap.get('detail', '')}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "mission.handoff": lambda args: _cmd_mission_handoff(
        args.mission_id,
        json_output=getattr(args, "json", False),
    ),
    "mission.ledger": lambda args: _cmd_mission_ledger(
        args.mission_id,
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "mission.watchdog": lambda args: _cmd_mission_watchdog(
        args.mission_id,
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
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
    "mission.plan": lambda args: _cmd_mission_plan(
        args.mission_id,
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
        no_llm=getattr(args, "no_llm", False),
    ),
    "mission.show": lambda args: _cmd_mission_show(
        args.mission_id,
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "mission.achieve": lambda args: _cmd_mission_set_status(
        args.mission_id, "achieve",
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "mission.abandon": lambda args: _cmd_mission_set_status(
        args.mission_id, "abandon",
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "mission.pause": lambda args: _cmd_mission_set_status(
        args.mission_id, "pause",
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "mission.resume": lambda args: _cmd_mission_set_status(
        args.mission_id, "resume",
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
}
