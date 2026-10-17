"""The `job cancel` entry of the command catalog (operator order exec-1017c).

Kept in a module of its own because `apps/cli/command_catalog.py` may not grow (its row in
`docs/system/structure-ledger-v1.md`); `_BASE_CATALOG` splices `JOB_CANCEL_COMMANDS` in right after
`job.stop`, so the help lists the two endings of a job together.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import _JSON_OPT, ArgDef, CommandEntry

JOB_CANCEL_COMMANDS: tuple[CommandEntry, ...] = (
    CommandEntry(
        command_id="job.cancel",
        group_id="job",
        subcommand="cancel",
        description="End a job for good, under its mission: it never runs again and leaves the active views, its record and evidence stay; a running job ends at its next safe point. A completed result is declined, not cancelled.",
        action_class="write_metadata",
        supports_json=True,
        args=(
            ArgDef("job_id", "Job ID to cancel (under its mission)"),
            ArgDef("--reason", "Why the job, under its mission, is cancelled (kept on the job)", required=False, is_option=True, default=""),
            ArgDef("--source", "Who requested the cancel (default: cli)", required=False, is_option=True, default="cli"),
            _JSON_OPT,
        ),
        related=("job.stop", "job.decline", "client.cancel-order"),
        exit_codes=(0, 1, 2, 3),
    ),
)
