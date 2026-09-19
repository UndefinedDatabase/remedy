"""Test helper: does a printed next-action command name a real catalog entry?

Moved here from `packages/orchestration/do_run.py` by R-0903: no production code called it, and
the tests that check a module's next action against the command catalog keep their assertion.
"""

from __future__ import annotations

import re

_REMEDY_CMD_RE = re.compile(r"^remedy\s+(\S+)\s+(\S+)")


def names_catalog_command(command: str) -> bool:
    """True when ``remedy <group> <subcommand> ...`` names a ``<group>.<subcommand>`` of CATALOG."""
    m = _REMEDY_CMD_RE.match(command)
    if not m:
        return False
    from apps.cli.command_catalog import CATALOG
    return any(entry.command_id == f"{m.group(1)}.{m.group(2)}" for entry in CATALOG)
