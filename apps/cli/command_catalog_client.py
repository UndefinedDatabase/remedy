"""The `client` group's entries of the command catalog (operator amendment amend1015-face-migration,
DECISION amend1015f D10).

Moved unchanged out of `apps/cli/command_catalog.py`, whose `_BASE_CATALOG` splices
`CLIENT_COMMANDS` in at the group's own place, so the help keeps its order.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import (
    _JSON_OPT,
    ArgDef,
    CommandEntry,
)

CLIENT_COMMANDS: tuple[CommandEntry, ...] = (
    # ── client (F298: the machine client interface as data, DECISION F298 D2) ──
    CommandEntry(
        command_id="client.interface",
        group_id="client",
        subcommand="interface",
        description="Show what a program that drives Remedy can rely on: its commands, arguments, exit codes, state words, templates and budget kinds (read-only).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("status.run", "do.run"),
    ),
    # F253 S3a (DECISION F253 D4 (3)): what changed since a cursor the client holds.
    CommandEntry(
        command_id="client.changes",
        group_id="client",
        subcommand="changes",
        description="List what changed since a cursor: jobs, open and resolved decisions, missions and applies, with a cursor for the next read (read-only).",
        action_class="read_only",
        args=(
            ArgDef(
                "--since",
                "The cursor of the last read: a time with its offset, such as the digest's "
                "read_at or the cursor the last read answered",
                required=False, is_option=True,
            ),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.interface", "status.run"),
    ),
    # F253 S5a (DECISION F253 D13): read an order the supervisor started as a record of its own.
    CommandEntry(
        command_id="client.order",
        group_id="client",
        subcommand="order",
        description="Read an order (an order file or text) the supervisor started, as a record of its own: its state, its exit code and the answer remedy do printed (read-only).",
        action_class="read_only",
        args=(
            ArgDef("order", "The order id the supervisor answered when it started your order "
                  "file or text"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.interface", "client.changes"),
        # A value that names no order is absent, which exit 3's `not_ready` meaning covers.
        exit_codes=(0, 1, 2, 3),
    ),
    # F253 (DECISION F253 D20): read the run the supervisor started for a job, as `client.order`
    # reads an order.
    CommandEntry(
        command_id="client.run",
        group_id="client",
        subcommand="run",
        # Both texts carry a word of tests/docs/test_vocabulary.py's meaning table ("task" is a
        # fragment of Job and of Run), because they use the binding words Job and Run.
        description="Read the run the supervisor started for a job, as a record of its own: its state, its exit code and the answer remedy job run printed once its tasks ended (read-only).",
        action_class="read_only",
        args=(
            ArgDef("job", "The id of the job, or a prefix of it, whose task run the supervisor "
                  "started"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.interface", "client.order"),
        # A value that names no job, or a job with no run record, is absent, which exit 3's
        # `not_ready` meaning covers.
        exit_codes=(0, 1, 2, 3),
    ),
    CommandEntry(
        command_id="client.story",
        group_id="client",
        subcommand="story",
        # amend1015-face-migration Phase 1.1 (DECISION amend1015f D14): the story a client renders in
        # its own words; every word of it is in `remedy client interface`'s `story` key.
        description="Read one Job's run story in closed words a client translates: its state, the one next step and the HTTP route that takes it, the five steps with the Job's tasks, the changed files and its numbers (read-only).",
        action_class="read_only",
        args=(
            ArgDef("job", "The id of the job, or a prefix of it, whose tasks' run story is read"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.interface", "client.run"),
    ),
)
