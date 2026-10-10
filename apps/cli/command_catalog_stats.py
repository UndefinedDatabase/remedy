"""The `stats` group's entries of the command catalog (F302, DECISION F302 D1).

Moved unchanged out of `apps/cli/command_catalog.py`, whose `_BASE_CATALOG` splices
`STATS_COMMANDS` in at the group's own place, so the help keeps its order.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import (
    _ALL_PROJECTS_FLAG,
    _JSON_OPT,
    _PROJECT_SCOPE_OPT,
    ArgDef,
    CommandEntry,
)

STATS_COMMANDS: tuple[CommandEntry, ...] = (
    # ── stats (F010) ─────────────────────────────────────────────────────
    CommandEntry(
        command_id="stats.failures",
        group_id="stats",
        subcommand="failures",
        description="Failure histogram from the recorded post-mortems (read-only).",
        action_class="read_only",
        supports_json=True,
        args=(
            ArgDef("--job", "Only this job's evidence export, from its run, under its mission", required=False, is_option=True),
            ArgDef("--since", "Only post-mortems at or after this ISO-8601 timestamp", required=False, is_option=True),
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    # ── stats — the self-benchmark trend (F082) ──────────────────────────
    CommandEntry(
        command_id="stats.bench",
        group_id="stats",
        subcommand="bench",
        description=(
            "Capability trend from the append-only bench history: the latest entry, "
            "the series before it, and a regression warning naming the sequence and "
            "both numbers. Never executes the bench (read-only)."
        ),
        action_class="read_only",
        supports_json=True,
        related=("stats.cost", "stats.report"),
        args=(
            ArgDef("--series", "Which bench series to read (default: the series of the latest entry)", required=False, is_option=True),
            ArgDef("--multiplier", "Warn when cost or wall time exceeds the trailing median by this factor (default: 1.5)", required=False, is_option=True),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    # ── stats — the token ledger (F103) ──────────────────────────────────
    CommandEntry(
        command_id="stats.cost",
        group_id="stats",
        subcommand="cost",
        description=(
            "Token and cost actuals from the ledger. Every figure names its basis: "
            "an unmeasured figure prints 'unmeasured', never 0, and no price is ever "
            "computed (read-only)."
        ),
        action_class="read_only",
        supports_json=True,
        related=("stats.backfill-ledger", "stats.verify-ledger"),
        args=(
            ArgDef("--since", "Only calls at or after this ISO-8601 timestamp", required=False, is_option=True),
            ArgDef("--job", "Only this job's calls (under its mission)", required=False, is_option=True),
            ArgDef("--by", "Group the figures by role, model or day (default: grand total only)", required=False, is_option=True),
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="stats.cache",
        group_id="stats",
        subcommand="cache",
        description=(
            "Cache-read share per bucket from the ledger. A share nobody could "
            "measure prints a word, never 0 %, and a role split names the limit "
            "it cannot show (read-only)."
        ),
        action_class="read_only",
        supports_json=True,
        related=("stats.cost", "stats.backfill-ledger"),
        args=(
            ArgDef("--since", "Only calls at or after this ISO-8601 timestamp", required=False, is_option=True),
            ArgDef("--job", "Only this job's calls (under its mission)", required=False, is_option=True),
            ArgDef("--by", "Group the shares by role, model or day (default: grand total only)", required=False, is_option=True),
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    # ── stats — the cost report (F115) ───────────────────────────────────
    # Deliberately NO --all-projects, and the description says so where a
    # reader looks for it: `remedy stats --help` prints the description, and a
    # deliberate absence nobody can find is indistinguishable from an omission.
    CommandEntry(
        command_id="stats.report",
        group_id="stats",
        subcommand="report",
        description=(
            "Cost report over ONE project's ledger: the cost table, where the "
            "prompt tokens went, and the equal-length period before this one, as "
            "markdown or json (read-only). There is deliberately no "
            "--all-projects: cost folds across projects but the segment "
            "breakdown does not, so an all-projects report would publish one "
            "project's breakdown under a multi-project total."
        ),
        action_class="read_only",
        supports_json=True,
        related=("stats.cost", "stats.cache"),
        args=(
            ArgDef("--since", "Period start: only calls at or after this ISO-8601 timestamp", required=False, is_option=True),
            ArgDef("--until", "Period end, EXCLUSIVE: only calls before this ISO-8601 timestamp", required=False, is_option=True),
            ArgDef("--job", "Only this job's calls, under its mission, in this period and in the one before it", required=False, is_option=True),
            ArgDef("--by", "Group the cost table by role, model or day (default: grand total only)", required=False, is_option=True),
            ArgDef("--label", "Name the scope this report covers, printed in its header", required=False, is_option=True),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="stats.backfill-ledger",
        group_id="stats",
        subcommand="backfill-ledger",
        description=(
            "Mirror an evidence directory's finalized task runs into the project's repo-scoped token "
            "ledger. WRITES the ledger (never the evidence) and is idempotent: a re-run "
            "adds no row."
        ),
        action_class="write_metadata",
        supports_json=True,
        related=("stats.cost", "stats.verify-ledger"),
        args=(
            ArgDef("evidence_dir", "Path to the job evidence folder to scan (under its mission)"),
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="stats.verify-ledger",
        group_id="stats",
        subcommand="verify-ledger",
        description=(
            "Reconcile the run evidence files against the token ledger rows (read-only). "
            "Exits 0 on a clean reconcile and non-zero when drift is found, so it is "
            "usable as a check."
        ),
        action_class="read_only",
        supports_json=True,
        related=("stats.cost", "stats.backfill-ledger"),
        args=(
            ArgDef("evidence_dir", "Path to the job evidence folder to reconcile (under its mission)"),
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
)
