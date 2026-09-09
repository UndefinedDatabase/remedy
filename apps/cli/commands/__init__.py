"""Per-group CLI command handler modules.

Each module exposes ``COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]]``
mapping catalog command_ids to handler functions.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def read_agent_file(name: str) -> str:
    """Read an .agent/ file if it exists. Shared by progress/feature commands."""
    from pathlib import Path

    p = Path(".agent") / name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    return ""


def collect_all_handlers() -> dict[str, Callable[[argparse.Namespace], None]]:
    """Collect COMMAND_HANDLERS from every group module."""
    from apps.cli.commands import (
        bench_cmd,
        blocker,
        brain,
        change,
        ci_cmd,
        config_cmd,
        context,
        contract_cmd,
        dashboard_cmd,
        decision,
        dev,
        do_cmd,
        event,
        external_builder_cmd,
        failure_stats_cmd,
        file,
        guide,
        init_cmd,
        integrity_cmd,
        job,
        job_context_cmd,
        job_rerun_cmd,
        job_stop_cmd,
        local_advisor_cmd,
        loop_cmd,
        main_builder_adapter_cmd,
        managed_builder_execution_cmd,
        memory,
        mission_cmd,
        orchestrator_cmd,
        overnight_cmd,
        patch,
        plan_cmd,
        policy,
        project,
        propose_cmd,
        provider_cmd,
        queue_cmd,
        readiness,
        real_test_execution_cmd,
        repair_cmd,
        repo,
        review_cmd,
        route_policy_cmd,
        runtime_cmd,
        self_cmd,
        snapshot_cmds,
        stats_ledger_cmd,
        status_cmd,
        teach_cmd,
        test_cmds,
        token_cmd,
        ui,
        worker,
        worker_facade_cmd,
    )

    table: dict[str, Callable[[argparse.Namespace], None]] = {}
    for mod in (init_cmd, job, project, patch, test_cmds, brain, policy, worker, memory, readiness, context, file, change, repo, event, blocker, decision, dashboard_cmd, guide, ui, do_cmd, repair_cmd, overnight_cmd, provider_cmd, review_cmd, self_cmd, orchestrator_cmd, local_advisor_cmd, external_builder_cmd, route_policy_cmd, token_cmd, real_test_execution_cmd, propose_cmd, dev, plan_cmd, integrity_cmd, contract_cmd, snapshot_cmds, main_builder_adapter_cmd, managed_builder_execution_cmd, config_cmd, worker_facade_cmd, runtime_cmd, failure_stats_cmd, stats_ledger_cmd, job_stop_cmd, job_rerun_cmd, job_context_cmd, status_cmd, queue_cmd, mission_cmd, loop_cmd, bench_cmd, ci_cmd, teach_cmd):
        table.update(mod.COMMAND_HANDLERS)
    return table
