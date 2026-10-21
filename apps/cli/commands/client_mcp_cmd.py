"""`remedy client mcp` — Remedy's MCP server over standard input and output (F303, DECISION F303 D5).

It calls `serve_mcp` over the process's standard input and output with the three tools of
`remedy_mcp_tools` and the names `--allow` gave, and returns when the input ends, so the command
exits 0 (no `sys.exit` of a call's value). It is closed by default: with no `--allow` no tool is
offered. A name no tool has is refused before any line is read, `invalid_argument` on standard
error and exit 2, so standard output only ever carries the protocol. It answers no `--json`
envelope: its standard output is the protocol's channel.
"""
from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from apps.cli.json_envelope import fail
from apps.cli.version_report import resolve_distribution_version
from packages.orchestration.mcp_server import McpServerError, serve_mcp
from packages.orchestration.mcp_tools import remedy_mcp_tools

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

EXIT_USAGE = 2


def _cmd_client_mcp(allowed: list[str]) -> None:
    try:
        serve_mcp(sys.stdin, sys.stdout, remedy_mcp_tools(), allowed,
                  version=resolve_distribution_version())
    except McpServerError as exc:
        fail("invalid_argument", str(exc), json_output=False, exit_code=EXIT_USAGE)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "client.mcp": lambda args: _cmd_client_mcp(list(getattr(args, "allow", None) or [])),
}
