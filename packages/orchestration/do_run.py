"""
The `Next:` line contract: one next action.

`DoRunNextAction` is the label, command and reason of the one thing a user should
do next. The repair loop that built its results with it was deleted by F273
(R-0923), so no production module imports it now. The check that such a command
names a real catalog entry had test callers only and moved to
`tests/orchestration/catalog_commands.py` (R-0903).

The phased `remedy do` v1 flow this module used to hold was deleted by F268
round 10: every `remedy do` walks `packages/orchestration/do_sequence.py`
(DECISION F268 D16).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DoRunNextAction:
    """What the user should do next."""

    label: str
    command: str
    reason: str
