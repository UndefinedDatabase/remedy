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
    from apps.cli.commands import blocker, brain, change, context, dashboard_cmd, decision, dev, do_cmd, event, file, guide, job, memory, patch, policy, project, readiness, repo, review_cmd, test_cmds, ui, worker

    table: dict[str, Callable[["argparse.Namespace"], None]] = {}
    for mod in (job, project, patch, test_cmds, brain, policy, worker, memory, readiness, context, file, change, repo, event, blocker, decision, dashboard_cmd, guide, ui, do_cmd, review_cmd, dev):
        table.update(mod.COMMAND_HANDLERS)
    return table
