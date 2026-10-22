"""The `job run` entry of the command catalog (DECISION F307 D22).

Kept in a module of its own as the next structural step of `apps/cli/command_catalog.py`'s
boundary on `docs/system/structure-ledger-v1.md`, which that file's row may not grow past;
`_BASE_CATALOG` splices `JOB_RUN_COMMANDS` in at the entry's own place, after `run.list`, so the
help keeps its order.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import _JSON_OPT, ArgDef, CommandEntry

JOB_RUN_COMMANDS: tuple[CommandEntry, ...] = (
    CommandEntry(
        command_id="job.run",
        group_id="job",
        subcommand="run",
        description="Run pending job tasks sequentially through Builder/Reviewer/Repair.",
        action_class="write_metadata",
        supports_json=True,
        related=("job.show",),
        args=(
            ArgDef("job_id", "Job ID (under its mission)"),
            ArgDef("--max-rounds", "Max ping-pong rounds per task's run (default: 3, persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--repair-rounds", "Max repair attempts per task's run (default: 2, 0=disabled, persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--test-command", "Test command to execute in staging (persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--claude-cli-write-mode", "Claude CLI write mode for the BUILDER: none, allowed-tools, dangerous-skip (default: allowed-tools, persisted on continuation). The reviewer never writes", required=False, is_option=True, default=None),
            ArgDef("--stream-evidence", "Opt-in F004 raw stream evidence: use Claude CLI stream-json and write redacted raw_stream.jsonl + run_events.jsonl. Omitted keeps the persisted/default mode", required=False, is_option=True),
            ArgDef("--no-stream-evidence", "Explicitly disable this run's raw stream evidence (overrides a persisted true). Omitted keeps the persisted/default mode", required=False, is_option=True),
            ArgDef("--tasks", "Max tasks to execute (omitted keeps persisted; 0=all)", required=False, is_option=True, default=None),
            ArgDef("--timeout-sec", "Raw per-call timeout in seconds (omitted keeps persisted/default)", required=False, is_option=True, default=None),
            ArgDef("--max-output-chars", "Max provider output chars (omitted keeps persisted/default)", required=False, is_option=True, default=None),
            ArgDef("--builder-provider", "Builder provider: claude, claude-cli, fake or pi (default: pi, the local Pi harness with Ollama; ollama alone cannot write files; persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--builder-model", "Model for builder role", required=False, is_option=True, default=None),
            ArgDef("--builder-effort", "Effort level for builder role", required=False, is_option=True, default=None),
            ArgDef("--reviewer-provider", "Reviewer provider: claude, claude-cli, fake, ollama or pi (default: pi, read-only tools; persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--reviewer-model", "Model for reviewer role", required=False, is_option=True, default=None),
            ArgDef("--reviewer-effort", "Effort level for reviewer role", required=False, is_option=True, default=None),
            ArgDef("--repair-provider", "Provider for repair role", required=False, is_option=True, default=None),
            ArgDef("--repair-model", "Model for repair role", required=False, is_option=True, default=None),
            ArgDef("--repair-effort", "Effort level for repair role", required=False, is_option=True, default=None),
            ArgDef("--timeout-profile", "Timeout profile: fast, normal, patient (default: normal unless raw timeout is explicitly set)", required=False, is_option=True, default=None),
            ArgDef("--max-total-tokens", "Maximum total tokens (F018 budget override)", required=False, is_option=True, default=None),
            ArgDef("--max-provider-calls", "Maximum provider calls (F018 budget override)", required=False, is_option=True, default=None),
            ArgDef("--max-wall-clock-minutes", "Maximum wall-clock minutes (F018 budget override)", required=False, is_option=True, default=None),
            ArgDef("--max-cost-usd", "Maximum cost in USD (F104 budget override)", required=False, is_option=True, default=None),
            ArgDef("--deadline", "UTC deadline as ISO 8601 string (F018 budget override)", required=False, is_option=True, default=None),
            ArgDef("--retry", "Put the tasks that ended blocked or failed back to pending first, so they run "
                   "again; a plain run re-attempts none of them", required=False, is_option=True, is_flag=True),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=True, exit_codes=(0, 1, 2, 3),
    ),
)
