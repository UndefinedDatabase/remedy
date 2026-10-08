"""Client group command handlers (F298 T001, DECISION F298 D2; F253 S3a, DECISION F253 D4 (3);
F253 S5a, DECISION F253 D13).

`remedy client interface` prints the machine client interface that
`apps/cli/client_interface.py` builds from the code: with `--json` as one envelope whose keys are
the document's, and otherwise as a short summary a person reads.

`remedy client changes` prints what changed since a cursor the client holds, from
`packages.orchestration.client_changes.build_client_changes`.

`remedy client order <order>` reads an order the supervisor started as a record of its own
(`packages.orchestration.serve_runs.read_order_record`): its state, its exit code and, once it is
not `running`, the answer `remedy do` printed. An order id that names no record is refused
`order_not_found`, exit 3.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse


def _cmd_client_interface(*, json_output: bool = False) -> None:
    from apps.cli.client_interface import build_client_interface

    interface = build_client_interface()
    if json_output:
        emit_ok(**interface)
        return
    print(f"Machine client interface {interface['interface_version']}")
    print("Operations:")
    for operation in interface["operations"]:
        print(f"  {operation['command']} — {operation['description']}")
    print(f"Job states: {', '.join(interface['job_states'])}")
    print(f"Mission statuses: {', '.join(interface['mission_statuses'])}")
    print(f"Contract templates: {', '.join(interface['contract_templates']) or '(none)'}")
    print(f"Budget kinds: {', '.join(interface['budget_kinds'])}")
    codes = ", ".join(f"{entry['code']} {entry['name']}" for entry in interface["exit_codes"])
    print(f"Exit codes: {codes}")
    print(f"Digest (remedy status --json, under client): {', '.join(interface['digest'])}")
    print("A program reads the whole interface with: remedy client interface --json")


def _cmd_client_changes(*, since: str | None, json_output: bool = False) -> None:
    from packages.orchestration.client_changes import (
        build_client_changes,
        client_cursor_refusal_message,
        parse_client_cursor,
    )

    parsed_since = None
    if since is not None:
        try:
            parsed_since = parse_client_cursor(since)
        except ValueError:
            fail(
                "invalid_cursor",
                client_cursor_refusal_message(since),
                json_output=json_output, exit_code=2,
            )

    changes = build_client_changes(parsed_since)
    if json_output:
        emit_ok(**changes)
        return
    print(f"Jobs changed: {len(changes['jobs'])}")
    print(f"Decisions open: {len(changes['decisions'])}")
    print(f"Decisions closed: {len(changes['closed_decisions'])}")
    print(f"Missions changed: {len(changes['missions'])}")
    print(f"Applies changed: {len(changes['applies'])}")
    print(f"Next cursor: {changes['cursor']}")


def _cmd_client_order(order_id: str, *, json_output: bool = False) -> None:
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import order_answer, order_state, read_order_record

    paths = serve_paths()
    record = read_order_record(paths, order_id)
    if record is None:
        fail(
            "order_not_found",
            f"no order record names {order_id!r}.",
            json_output=json_output, exit_code=3,
        )
    state = order_state(paths, record)
    answer = order_answer(record) if state != "running" else None
    # A dict literal unpacked by name, not `exit_code=...` written out at the call site: the
    # answer carries the order's own `exit_code` (DECISION F253 D13 (4)), and a literal keyword
    # of that name at an emit_ok call site reads, to tests/cli/test_client_interface.py's static
    # answer-key reader, as fail()'s OWN exit-code parameter instead of a payload key.
    payload = {
        "order_id": record.order_id,
        "state": state,
        "started_at": record.started_at,
        "ended_at": record.ended_at,
        "exit_code": record.exit_code,
        "order_file": record.order_file,
        "answer": answer,
    }
    if json_output:
        emit_ok(**payload)
        return
    print(f"Order {record.order_id}: {state}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "client.interface": lambda args: _cmd_client_interface(json_output=getattr(args, "json", False)),
    "client.changes": lambda args: _cmd_client_changes(
        since=getattr(args, "since", None), json_output=getattr(args, "json", False)),
    "client.order": lambda args: _cmd_client_order(
        args.order, json_output=getattr(args, "json", False)),
}
