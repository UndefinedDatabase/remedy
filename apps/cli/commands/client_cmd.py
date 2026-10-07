"""Client group command handlers (F298 T001, DECISION F298 D2).

`remedy client interface` prints the machine client interface that
`apps/cli/client_interface.py` builds from the code: with `--json` as one envelope whose keys are
the document's, and otherwise as a short summary a person reads.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok

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
    print("A program reads the whole interface with: remedy client interface --json")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "client.interface": lambda args: _cmd_client_interface(json_output=getattr(args, "json", False)),
}
