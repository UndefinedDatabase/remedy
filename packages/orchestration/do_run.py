"""
The `Next:` line contract: one next action, and the check that its command is real.

`DoRunNextAction` is the label, command and reason of the one thing a user should
do next; `packages/orchestration/repair_loop.py` builds its results with it.
`validate_next_safe_action_command` checks that such a command names a real
`<group>.<subcommand>` entry of the command catalog.

The phased `remedy do` v1 flow this module used to hold was deleted by F268
round 10: every `remedy do` walks `packages/orchestration/do_sequence.py`
(DECISION F268 D16).
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DoRunNextAction:
    """What the user should do next."""

    label: str
    command: str
    reason: str


# ---------------------------------------------------------------------------
# Next safe action validation (Step 926)
# ---------------------------------------------------------------------------

_REMEDY_CMD_RE = re.compile(r"^remedy\s+(\S+)\s+(\S+)")


def validate_next_safe_action_command(command: str) -> bool:
    """Validate that a next_safe_action command maps to a real catalog entry.

    Parses ``remedy <group> <subcommand> ...`` and verifies
    ``<group>.<subcommand>`` exists in CATALOG.
    """
    m = _REMEDY_CMD_RE.match(command)
    if not m:
        return False
    group, subcommand = m.group(1), m.group(2)
    command_id = f"{group}.{subcommand}"

    from apps.cli.command_catalog import CATALOG
    return any(entry.command_id == command_id for entry in CATALOG)
