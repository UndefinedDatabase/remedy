"""Per-group CLI command handler modules.

Each module exposes ``COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]]``
mapping catalog command_ids to handler functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse


def collect_all_handlers() -> dict[str, Callable[["argparse.Namespace"], None]]:
    """Collect COMMAND_HANDLERS from every group module."""
    from apps.cli.commands import brain, dev, job, memory, patch, policy, project, test_cmds, worker

    table: dict[str, Callable[["argparse.Namespace"], None]] = {}
    for mod in (job, project, patch, test_cmds, brain, policy, worker, memory, dev):
        table.update(mod.COMMAND_HANDLERS)
    return table
