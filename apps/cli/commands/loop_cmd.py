"""`remedy loop` — read-only views over the declarative loops (F045 T003).

A LOOP is user-authored configuration in the project's ``remedy.toml``
(``[[loop]]``, DECISION F045 D1). This module SHOWS loops and CHECKS them; it
materializes nothing. ``remedy loop run`` is the write half and lives in its own
round — a reader of this file who is looking for it will not find it here.

Both commands read the config exactly where
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

import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse

#: The same "the command refused" code `remedy queue` uses, so a caller
#: scripting the CLI does not need a per-group exit table.
EXIT_ERROR = 1

#: What the LAST RUN column says when the job store holds no run for a loop.
NEVER_RAN = "never"

#: How an inert trigger is marked in its own row (LoopSpec.is_inert).
INERT_MARK = "inert"


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


def _cmd_loop_list() -> None:
    """List every loop: name, trigger, action, last run. Reads, never writes."""
    from packages.orchestration.loop_spec import (
        INERT_TRIGGER_NOTICE,
        LoopSpecError,
        load_loop_specs,
    )

    try:
        specs = load_loop_specs()
    except LoopSpecError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if not specs:
        print("No loops defined. Add a [[loop]] table to remedy.toml.")
        return

    for spec in specs:
        print(f"{spec.name:<24}  {_trigger_label(spec):<20}  "
              f"{spec.action.kind:<8}  last run: {_last_run_label(spec.name)}")

    if any(spec.is_inert for spec in specs):
        print(f"  ({INERT_MARK}: {INERT_TRIGGER_NOTICE})")


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


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "loop.list": lambda args: _cmd_loop_list(),
    "loop.validate": lambda args: _cmd_loop_validate(),
}
