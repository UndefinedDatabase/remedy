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
        decision,
        dev,
        do_cmd,
        event,
        failure_stats_cmd,
        file,
        init_cmd,
        integrity_cmd,
        job,
        job_context_cmd,
        job_stop_cmd,
        memory,
        mission_cmd,
        patch,
        project,
        real_test_execution_cmd,
        roadmap_cmd,
        runtime_cmd,
        self_cmd,
        snapshot_cmds,
        stats_ledger_cmd,
        status_cmd,
        teacher_cmd,
        test_cmds,
        ui,
        worker,
        worker_facade_cmd,
    )

    table: dict[str, Callable[[argparse.Namespace], None]] = {}
    for mod in (init_cmd, job, project, patch, test_cmds, brain, worker, memory, file, change, event, blocker, decision, ui, do_cmd, self_cmd, real_test_execution_cmd, dev, roadmap_cmd, integrity_cmd, snapshot_cmds, config_cmd, worker_facade_cmd, runtime_cmd, failure_stats_cmd, stats_ledger_cmd, job_stop_cmd, job_context_cmd, status_cmd, mission_cmd, bench_cmd, ci_cmd, teacher_cmd):
        table.update(mod.COMMAND_HANDLERS)
    return table
