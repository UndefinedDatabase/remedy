"""Serve group command handlers (F200, DECISION F200 D1).

`remedy serve start` runs the supervisor in the foreground until Ctrl-C or
SIGTERM; `remedy serve status` reports whether one answers on this data root's
socket; `remedy serve stop` stops it.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse


def _cmd_serve_start(*, json_output: bool = False) -> None:
    from packages.orchestration.serve_daemon import ServeError, SupervisorState, run_supervisor

    def ready(state: SupervisorState) -> None:
        if json_output:
            emit_ok(**state.to_json())
        else:
            print(f"Remedy serve supervisor answering on {state.socket} "
                  f"(process {state.pid}). Press Ctrl-C to stop.")
        sys.stdout.flush()

    try:
        run_supervisor(on_ready=ready)
    except ServeError as exc:
        fail(exc.token, str(exc), json_output=json_output)
    if not json_output:
        print("Remedy serve supervisor stopped.")


def _cmd_serve_status(*, json_output: bool = False) -> None:
    from packages.orchestration.serve_daemon import supervisor_state

    state = supervisor_state()
    if json_output:
        emit_ok(**state.to_json())
        return
    if state.running:
        print(f"Serve supervisor: running (process {state.pid}) on {state.socket}")
    else:
        print(f"Serve supervisor: not running (no answer on {state.socket})")


def _cmd_serve_stop(*, json_output: bool = False) -> None:
    from packages.orchestration.serve_daemon import ServeError, stop_supervisor

    try:
        stopped = stop_supervisor()
    except ServeError as exc:
        fail(exc.token, str(exc), json_output=json_output)
    if json_output:
        emit_ok(stopped=stopped)
    elif stopped:
        print("Stopped the serve supervisor.")
    else:
        print("No serve supervisor is running for this data root.")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "serve.start": lambda args: _cmd_serve_start(json_output=getattr(args, "json", False)),
    "serve.status": lambda args: _cmd_serve_status(json_output=getattr(args, "json", False)),
    "serve.stop": lambda args: _cmd_serve_stop(json_output=getattr(args, "json", False)),
}
