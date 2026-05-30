"""Dev group command handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse

# Re-use brain module's agent_loop handler for dev.agent-loop
from apps.cli.commands.brain import _cmd_agent_loop


def _dev_smoke_help() -> None:
    print("Smoke test:")
    print("  source scripts/remedy_smoke.sh && remedy_smoke")
    print("")
    print("Or run directly:")
    print("  bash scripts/remedy_smoke.sh")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "dev.agent-loop": lambda args: _cmd_agent_loop(args.job_id),
    "dev.smoke-help": lambda args: _dev_smoke_help(),
}
