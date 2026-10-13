"""The `doctor` group's entries of the command catalog (F199, DECISION F199 D1).

Moved unchanged out of `apps/cli/command_catalog.py`, whose `_BASE_CATALOG` splices
`DOCTOR_COMMANDS` in at the group's own place, so the help keeps its order.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import (
    _JSON_OPT,
    ArgDef,
    CommandEntry,
)

DOCTOR_COMMANDS: tuple[CommandEntry, ...] = (
    # ── doctor (product spine health check) ──────────────────────────────
    CommandEntry(
        command_id="doctor.core",
        group_id="doctor",
        subcommand="core",
        description="Read-only core product spine health check — modules, scripts, config (no execution; no network; no secrets).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("mission.report",),
    ),
    CommandEntry(
        command_id="doctor.toolchain",
        group_id="doctor",
        subcommand="toolchain",
        description=("Each pinned tool's installed, pinned and newest version; the newest needs the "
                     "network and reads unknown without it (read-only)."),
        action_class="read_only",
        args=(
            # is_flag: `--offline` takes no value, and only `--json` is special-cased by name.
            ArgDef("--offline", "Do not ask the package index; newest reads unknown",
                   required=False, is_option=True, is_flag=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("doctor.core",),
    ),
    CommandEntry(
        command_id="doctor.health",
        group_id="doctor",
        subcommand="health",
        description=("Read-only health of Remedy itself: its settings, cost ledgers, snapshots, "
                     "worktrees, model providers, staging copies, free disk and recent crash "
                     "reports, each PASS, WARN or FAIL with a hint; exits 1 on a FAIL."),
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("doctor.core",),
    ),
    CommandEntry(
        command_id="doctor.logs",
        group_id="doctor",
        subcommand="logs",
        description=("Read-only: the operations log's lines of one job, oldest first, each with "
                     "its task and run; --run keeps one run of a task (the log is never evidence)."),
        action_class="read_only",
        args=(
            ArgDef("job_id", "The job id, or its first characters; a job's lines carry its task and run"),
            ArgDef("--run", "Only the lines of this run id, one execution of a task",
                   required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("doctor.health",),
    ),
)
