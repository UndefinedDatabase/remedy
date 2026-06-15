"""Per-group CLI command handler modules.

Each module exposes ``COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]]``
mapping catalog command_ids to handler functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse


def read_agent_file(name: str) -> str:
    """Read an .agent/ file if it exists. Shared by progress/feature commands."""
    from pathlib import Path

    p = Path(".agent") / name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    return ""


def collect_all_handlers() -> dict[str, Callable[["argparse.Namespace"], None]]:
    """Collect COMMAND_HANDLERS from every group module."""
    from apps.cli.commands import blocker, brain, builder_routing_cmd, candidate_quality_cmd, change, context, contract_cmd, dashboard_cmd, decision, dev, do_cmd, event, external_builder_cmd, feature_cmd, file, guide, integrity_cmd, job, local_advisor_cmd, local_candidate_cmd, memory, overnight_cmd, orchestrator_cmd, patch, policy, progress_cmd, project, propose_cmd, provider_cmd, readiness, repair_cmd, repo, review_cmd, route_policy_cmd, self_cmd, snapshot_cmds, test_cmds, token_cmd, ui, worker

    table: dict[str, Callable[["argparse.Namespace"], None]] = {}
    for mod in (job, project, patch, test_cmds, brain, policy, worker, memory, readiness, context, file, change, repo, event, blocker, decision, dashboard_cmd, guide, ui, do_cmd, repair_cmd, overnight_cmd, provider_cmd, review_cmd, self_cmd, orchestrator_cmd, local_advisor_cmd, builder_routing_cmd, local_candidate_cmd, candidate_quality_cmd, external_builder_cmd, route_policy_cmd, token_cmd, propose_cmd, dev, progress_cmd, feature_cmd, integrity_cmd, contract_cmd, snapshot_cmds):
        table.update(mod.COMMAND_HANDLERS)
    return table
