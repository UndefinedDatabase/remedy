"""`remedy loop` — the operator's surface over the declarative loops (F045 T003).

A LOOP is user-authored configuration in the project's ``remedy.toml``
(``[[loop]]``, DECISION F045 D1). ``list`` and ``validate`` only READ. ``run``
is the one write in this module: it materializes a loop through
``loop_run.run_loop`` and STOPS at a planned job. DECISION F045 D7 — ``--yes``
skips the confirmation prompt and approves NOTHING else. Nothing here executes
a task, and Remedy deliberately offers no flag that would make it.

All three commands read the config exactly where
:mod:`packages.orchestration.loop_spec` already looks: they call
``load_loop_specs()`` / ``validate_loop_specs()`` with NO path argument, so the
default ``remedy.toml`` relative to the working directory is the one config
location the feature has. Remedy deliberately does not offer a ``--config``
option here: a second way to name the file would be a second config location in
all but name.

``list`` and ``validate`` differ on purpose in WHICH loader they use.
``load_loop_specs`` raises on the FIRST error, which is what a listing wants —
it cannot honestly list a config it could not read. ``validate_loop_specs``
never raises and returns EVERY message in file order, which is what a check
wants: the feature requires all errors and a nonzero exit, not the first error.
"""
from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse

#: The same "the command refused" code `remedy queue` uses, so a caller
#: scripting the CLI does not need a per-group exit table.
EXIT_ERROR = 1

#: The same "you invoked it wrongly" code `remedy queue add` uses.
EXIT_USAGE = 2

#: The contract's exit code for "no project" — the same one `job create`,
#: `queue add` and `mission start` use.
EXIT_NO_PROJECT = 3

#: What the LAST RUN column says when the job store holds no run for a loop.
NEVER_RAN = "never"

#: How an inert trigger is marked in its own row (LoopSpec.is_inert).
INERT_MARK = "inert"

#: A listing deliberately does NOT reuse ``loop_spec.INERT_TRIGGER_NOTICE``: that
#: sentence reports a RUN, and a listing runs nothing, so it may say only what an
#: unfired trigger means. ``remedy loop run`` is where the notice belongs.
INERT_TRIGGER_LEGEND = "cannot fire until the scheduler exists; run such a loop manually"


def _last_run_label(name: str) -> str:
    """``never``, or the STORED run's creation time and state.

    The job store is the one source the feature specifies for a last run
    (``loop_ref`` provenance); there is deliberately no second one, so a loop
    whose run is not in the store reports ``never`` rather than a guess.
    """
    from packages.orchestration.loop_run import last_run_for_loop

    job = last_run_for_loop(name)
    if job is None:
        return NEVER_RAN
    created = getattr(job.created_at, "isoformat", lambda: str(job.created_at))()
    state = getattr(job.state, "value", job.state)
    return f"{created}  {state}"


def _trigger_label(spec: Any) -> str:
    """The trigger kind, marked ``inert`` when it cannot fire without being run."""
    if spec.is_inert:
        return f"{spec.trigger.kind} ({INERT_MARK})"
    return str(spec.trigger.kind)


def _cmd_loop_list(
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    """List every loop: name, trigger, action, last run. Reads, never writes."""
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.loop_run import last_run_for_loop
    from packages.orchestration.loop_spec import LoopSpecError, load_loop_specs

    try:
        specs = load_loop_specs()
    except LoopSpecError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    rows = []
    for spec in specs:
        job = last_run_for_loop(spec.name)
        last_run_created_at = None
        last_run_state = None
        if job is not None:
            last_run_created_at = getattr(
                job.created_at, "isoformat", lambda: str(job.created_at)
            )()
            last_run_state = getattr(job.state, "value", job.state)
        rows.append((spec, last_run_created_at, last_run_state))

    try:
        rows = apply_list_options(
            rows,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "last_run_created_at": lambda r: r[1] or "",
            },
            default_sort_field=None,
            date_getter=lambda r: r[1],
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if json_output:
        loops = [{
            "name": spec.name,
            "trigger": spec.trigger.kind,
            "is_inert": spec.is_inert,
            "action": spec.action.kind,
            "last_run_created_at": last_run_created_at,
            "last_run_state": last_run_state,
        } for spec, last_run_created_at, last_run_state in rows]
        print(json.dumps({"version": 1, "loops": loops}, sort_keys=True))
        return

    if not rows:
        print("No loops defined. Add a [[loop]] table to remedy.toml.")
        return

    for spec, last_run_created_at, last_run_state in rows:
        last_run_label = (
            NEVER_RAN if last_run_created_at is None
            else f"{last_run_created_at}  {last_run_state}"
        )
        print(f"{spec.name:<24}  {_trigger_label(spec):<20}  "
              f"{spec.action.kind:<8}  last run: {last_run_label}")

    if any(spec.is_inert for spec, _, _ in rows):
        print(f"  ({INERT_MARK}: {INERT_TRIGGER_LEGEND})")


def _cmd_loop_validate() -> None:
    """Report EVERY loop error and exit nonzero, or say how many validated."""
    from packages.orchestration.loop_spec import load_loop_specs, validate_loop_specs

    messages = validate_loop_specs()
    if messages:
        for message in messages:
            print(message, file=sys.stderr)
        print(f"Error: {len(messages)} loop error(s).", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    # No messages means the file parsed AND every entry validated, so this load
    # cannot raise — validate_loop_specs reports file-level failures too.
    print(f"{len(load_loop_specs())} loop(s) validated; no errors.")


# WHY: the one project a run belongs to, resolved the way every other command
# group resolves it. Deliberately a THIRD private copy of the same six lines
# rather than a shared helper: `mission_cmd` and `queue_cmd` each define their
# own, and extracting one would be a refactor across three command modules
# riding along with a feature, which AGENTS.md forbids in the same commit.
def _resolve_project_id(project_flag: str | None) -> str:
    """The one project this run belongs to, or exit 3 with the same wording as job create."""
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


# WHY: its own function so the confirmation path is steerable in a test without
# reaching into a captured stdin object.
def _stdin_is_a_tty() -> bool:
    """Whether there is an operator on the other end who could answer a prompt."""
    return sys.stdin.isatty()


def _confirm_materialization(spec: Any) -> bool:
    """Ask before creating work; REFUSE rather than block when nobody can answer.

    A non-TTY stdin gets an error and the name of the flag, never a prompt:
    ``input()`` under a pipe or a non-interactive SSH session would hang the run
    forever, and this feature exists to be driven exactly that way.
    """
    if not _stdin_is_a_tty():
        print(f"Error: stdin is not a terminal, so there is nobody to confirm. "
              f"Pass --yes to materialize loop '{spec.name}' without a prompt.",
              file=sys.stderr)
        sys.exit(EXIT_USAGE)
    print(f"Loop '{spec.name}' will create one planned {spec.action.kind}. "
          f"Nothing will run.")
    return input("Continue? [y/N] ").strip().lower() in ("y", "yes")


def _cmd_loop_run(name: str, *, project: str | None = None, yes: bool = False) -> None:
    """Materialize the named loop and STOP; the job it creates is planned, not run.

    DECISION F045 D7: ``--yes`` skips the confirmation and approves nothing
    else. The job reaches the operator's approval gate exactly like a typed
    goal, so the last line printed names the command that would start it.
    """
    from packages.orchestration.loop_run import run_loop
    from packages.orchestration.loop_spec import LoopSpecError, load_loop_specs

    project_id = _resolve_project_id(project)

    try:
        specs = load_loop_specs()
    except LoopSpecError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    spec = next((candidate for candidate in specs if candidate.name == name), None)
    if spec is None:
        # Naming what DOES exist is the whole fix for a typo'd loop name.
        defined = ", ".join(candidate.name for candidate in specs) or "(none)"
        print(f"Error: no loop named '{name}'. Defined loops: {defined}",
              file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if not yes and not _confirm_materialization(spec):
        print("Cancelled. Nothing was created.")
        return

    outcome = run_loop(spec, project_id=project_id)

    state = getattr(outcome.job.state, "value", outcome.job.state)
    print(f"job {outcome.job.id}  {state}")
    if outcome.mission_id:
        print(f"mission {outcome.mission_id}")
    if outcome.notice:
        # The OUTCOME knows whether this run was inert; the display must not
        # re-derive that from a constant (finding R-0355).
        print(outcome.notice)
    print(f"Nothing has run yet. Start it with: remedy job run {outcome.job.id}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "loop.list": lambda args: _cmd_loop_list(
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "loop.validate": lambda args: _cmd_loop_validate(),
    "loop.run": lambda args: _cmd_loop_run(
        args.name,
        project=getattr(args, "project", None),
        yes=getattr(args, "yes", False),
    ),
}
