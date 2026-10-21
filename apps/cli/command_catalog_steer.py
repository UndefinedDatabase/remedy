"""The `job steer` entry of the command catalog, moved out unchanged (DECISION F303 D2 (1)):
`apps/cli/command_catalog.py` sits exactly at its row on `docs/system/structure-ledger-v1.md`,
with no room left for the `--source` option this round adds. `_BASE_CATALOG` splices
`JOB_STEER_COMMANDS` back in right after `job.veto-task`, the same place, so the help keeps its
order.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import _JOB_ID, _JSON_OPT, ArgDef, CommandEntry

JOB_STEER_COMMANDS: tuple[CommandEntry, ...] = (
    # ── job steer (F030 T002, DECISION F030 D2) ───────────────────────────
    CommandEntry(
        command_id="job.steer",
        group_id="job",
        subcommand="steer",
        description="Address a steering note to one task of a running job; it is recorded as "
                    "evidence and read at the start of that task's next build round, never "
                    "inside a model call (F030).",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("text", "The note, quoted as one argument"),
            ArgDef("--task", "The task to address the note to: its id in the job, or its id "
                   "in the job plan, as `remedy job plan-show` prints them",
                   required=True, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("chat.send", "chat.show", "job.veto-task"),
        exit_codes=(0, 1, 2, 3),
    ),
)
