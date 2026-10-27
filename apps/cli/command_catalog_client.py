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
    # Operator order exec-1017 (D6): what this server offers an execution, read from its own configuration.
    CommandEntry(
        command_id="client.execution",
        group_id="client",
        subcommand="execution",
        description="Show what this server offers an execution: each role's providers with their defaults, availability, isolation and installed models, which of them a client may choose over HTTP, the lanes, request flags, budget caps, verification statuses, review reports, phases and the routes that show progress (read-only).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("client.interface", "do.run"),
    ),
    # Operator amendment amend1026-go-live-and-ask, Part C1: the projects a client may see.
    CommandEntry(
        command_id="client.projects",
        group_id="client",
        subcommand="projects",
        description="List the registered projects with their slug, name, repository and description, how many of their Jobs with their tasks are still open, when their newest Job was made and whether the tests of the newest Job that tested passed (read-only).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("client.ask", "status.run"),
    ),
    # Operator amendment amend1026-go-live-and-ask, Part C2: a question to a project, answered by the
    # Claude Code CLI that may only read (Read, Glob, Grep); its evidence lands in the data root.
    CommandEntry(
        command_id="client.ask",
        group_id="client",
        subcommand="ask",
        description="Ask a question about a project's repository: the Claude Code CLI reads it with Read, Glob and Grep only, never edits, writes or runs a command, and answers in Markdown with the tokens and calls it used; the question, the answer and every tool call are kept under the data root.",
        action_class="write_metadata",
        args=(
            ArgDef("project", "The slug or id of the project whose repo is asked about, as remedy client projects lists it"),
            ArgDef("question", "The question, in any language"),
            ArgDef("--max-total-tokens", "The most input and output tokens the ask may use (default: 150000)",
                   required=False, is_option=True, default="150000"),
            ArgDef("--asked-by", "Who asks, kept in the evidence folder (default: cli)", required=False,
                   is_option=True, default="cli"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.projects", "client.execution"),
        # A project no registry entry names, or one with no repository, is absent (exit 3).
        exit_codes=(0, 1, 2, 3),
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
    # Operator amendment amend1023-universe-trust (DECISION amend1023 D11): an order's story.
    CommandEntry(
        command_id="client.order-story",
        group_id="client",
        subcommand="order-story",
        description="Read the story of an order (an order file or text) the supervisor started, in closed words a client translates: who gave it, its missions and milestones, each Job's state, the criterion a blocked Job did not meet, its tasks done and total, and for the Job that runs its round, one pass of build and review inside its run, and the last tool its model called (read-only).",
        action_class="read_only",
        args=(
            ArgDef("order", "The order id the supervisor answered when it started your order "
                  "file or text"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.order", "client.story"),
        # A value that names no order is absent, which exit 3's `not_ready` meaning covers.
        exit_codes=(0, 1, 2, 3),
    ),
    # Operator amendment amend1026-go-live-and-ask, Part D3: an order's captured review report.
    CommandEntry(
        command_id="client.order-review",
        group_id="client",
        subcommand="order-review",
        description="Read the review report an order (an order file or text) sent with capture_review kept, as Markdown a person reads: its outcome, its configuration, each Job with its tasks, rounds and verdicts, its usage and what it cannot measure (read-only).",
        action_class="read_only",
        args=(
            ArgDef("order", "The order id the supervisor answered when it started your order "
                  "file or text"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.order", "client.order-story"),
        # A value that names no order, or an order that kept no report, is absent (exit 3).
        exit_codes=(0, 1, 2, 3),
    ),
    # exec-1017c: cancel an order the supervisor started, whatever it is doing (`order_cancel.py`).
    CommandEntry(
        command_id="client.cancel-order",
        group_id="client",
        subcommand="cancel-order",
        description="Cancel an order (an order file or text) the supervisor started, planning, running or waiting: its jobs end for good, nothing of it starts again and nothing is applied after it; a result waiting for its apply stays for you to answer unless --decline-results.",
        action_class="write_metadata",
        args=(
            ArgDef("order", "The order id the supervisor answered when it started your order "
                  "file or text"),
            ArgDef("--reason", "Why the order file or text is cancelled (kept with it and with each job of its mission)",
                   required=False, is_option=True, default=""),
            ArgDef("--source", "Who requested the cancel (default: cli)", required=False,
                   is_option=True, default="cli"),
            ArgDef("--decline-results", "Also decline each result of the order file or text still waiting for its apply",
                   required=False, is_option=True, is_flag=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.order", "job.abandon"),
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
    CommandEntry(
        command_id="client.now",
        group_id="client",
        subcommand="now",
        # F311 (DECISION F311 D1): what runs now, in closed words; every word of it is in
        # `remedy client interface`'s `insight` key (DECISION F311 D5).
        description="Read what runs now in closed words a client translates: every running Job with its phase (plan, build, review, repair), task, round, worker, budget and how long its worker's model has been silent, the orders that wait, and the local model server's state (read-only).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("client.interface", "client.insight"),
    ),
    CommandEntry(
        command_id="client.insight",
        group_id="client",
        subcommand="insight",
        # F311 (DECISION F311 D1): one Job's worker, seen from outside; every word of it is in
        # `remedy client interface`'s `insight` key (DECISION F311 D5).
        description="Read one Job's insight in closed words a client translates: its phase (plan, build, review, repair), the task it runs, its round, its worker's role and model, and its budget, whether the worker is stalled and why, what the operator can do, and the last lines the worker's model wrote (read-only).",
        action_class="read_only",
        args=(
            ArgDef("job", "The id of the job, or a prefix of it, whose running task's worker model is read"),
            ArgDef("--lines", "How many of the worker model's last stream lines to show, at most 200 "
                   "(default 40; a value that is not a whole number reads 40)", required=False,
                   is_option=True, default="40"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.interface", "client.now", "client.story"),
    ),
    CommandEntry(
        command_id="client.diff",
        group_id="client",
        subcommand="diff",
        # Operator order amend1015-final-closure E3 (DECISION amend1015c D5): the change a client
        # shows before a person applies it, read from git.
        description="Read the change one ended Job's tasks made, as git prints it file by file with its unified patch: before apply against the commit the Job started from, after apply the commit it landed (read-only).",
        action_class="read_only",
        args=(
            ArgDef("job", "The id of the job, or a prefix of it, whose tasks' change is read"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.interface", "client.story"),
        # A job that has not ended, or whose commits git no longer has, exits 3 (`not_ready`).
        exit_codes=(0, 1, 2, 3),
    ),
    # Operator amendment amend1027-green-builds E1: a job's evidence files, as text.
    CommandEntry(
        command_id="client.evidence",
        group_id="client",
        subcommand="evidence",
        description="Read the files of one Job's evidence folder, kept for each of its task runs, each file with its path, its size and its text cut to its last 20,000 characters: the size choice, the DoD and its result, the builder's commands and test runs, the raw streams (read-only).",
        action_class="read_only",
        args=(
            ArgDef("job", "The id of the job, or a prefix of it, whose task runs' evidence folder is read"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.story", "client.diff"),
        exit_codes=(0, 1, 2),
    ),
    # Operator amendment amend1023-universe-trust (DECISION amend1023 D6): the client registry,
    # read and changed on this machine's command line only; never published over HTTP.
    CommandEntry(
        command_id="client.show",
        group_id="client",
        subcommand="show",
        description="Show the clients of the operator's registry, or the one named: each one's projects, its token and call ceilings, whether it may apply a result and whether it holds host_tools, and its token's fingerprint, never the token (read-only).",
        action_class="read_only",
        args=(
            ArgDef("client", "The name of one client (default: every client)", required=False),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.grant-host-tools", "client.revoke-host-tools"),
        # A name no entry holds is absent, which exit 3's `not_ready` meaning covers.
        exit_codes=(0, 1, 2, 3),
    ),
    CommandEntry(
        command_id="client.grant-host-tools",
        group_id="client",
        subcommand="grant-host-tools",
        description="Grant a client of the registry host_tools: over HTTP it may then name claude-cli, the Claude Code CLI that runs with this machine's own file and shell tools, as builder and reviewer, and choose the planner. Only this command grants it.",
        action_class="local_state_change",
        args=(
            ArgDef("client", "The name of the client, as remedy client show lists it"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.show", "client.revoke-host-tools", "client.execution"),
        exit_codes=(0, 1, 2, 3),
    ),
    CommandEntry(
        command_id="client.revoke-host-tools",
        group_id="client",
        subcommand="revoke-host-tools",
        description="Revoke host_tools from a client of the registry: over HTTP it is offered again only what every client is offered.",
        action_class="local_state_change",
        args=(
            ArgDef("client", "The name of the client, as remedy client show lists it"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("client.show", "client.grant-host-tools"),
        exit_codes=(0, 1, 2, 3),
    ),
    # F303 (DECISION F303 D5): the MCP server; not read_only, because every call starts a child
    # `remedy` and `evidence_bundle` writes a certificate file, and it has no `--json` envelope.
    CommandEntry(
        command_id="client.mcp",
        group_id="client",
        subcommand="mcp",
        description="Serve Remedy's verify check, gate status and evidence bundle as tools of the Model Context Protocol over standard input and output for an orchestrator that starts it, offering only the tools --allow names.",
        action_class="local_state_change",
        args=(
            ArgDef("--allow", "A tool to offer: evidence_bundle, gate_status or verify; repeat it for each (default: none, so no tool is offered)",
                   required=False, is_option=True, is_repeatable=True),
        ),
        supports_json=False,
        may_execute_commands=True,
        related=("client.interface", "verify.run", "job.certificate"),
    ),
)
