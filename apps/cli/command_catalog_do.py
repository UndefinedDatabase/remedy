"""The `do` group's entries of the command catalog (F055, DECISION F055 D1).

Moved unchanged out of `apps/cli/command_catalog.py`, whose `_BASE_CATALOG` splices
`DO_COMMANDS` in at the group's own place, so the help keeps its order.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import (
    ArgDef,
    CommandEntry,
)

DO_COMMANDS: tuple[CommandEntry, ...] = (
    # ── do ───────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="do.run",
        group_id="do",
        subcommand="run",
        description="Plan and run what you ask: study the repo, plan a mission of jobs and their tasks, run the first job, and stop before apply unless --apply.",
        action_class="write_metadata",
        supports_json=True,
        related=("job.show", "change.proof"),
        args=(
            ArgDef("goal", "What you ask, as text, or one path ending in .md to an order file", required=False),
            ArgDef("--repo", "Path to target repository (default: the registered repository of the project --project or the order file names, else the current directory)", required=False, is_option=True, default=None),
            ArgDef("--project", "Select a registered project by slug or id instead of the repository's own", required=False, is_option=True),
            ArgDef("--json", "Output JSON", required=False, is_option=True, default="false"),
            ArgDef("--builder-provider", "Builder provider for `do`: claude, claude-cli, fake or pi (default: pi, the local Pi harness with the Ollama model muse-glimmer:latest; ollama alone cannot write files)", required=False, is_option=True, default=None),
            ArgDef("--reviewer-provider", "Reviewer provider for `do`: claude, claude-cli, fake, ollama or pi (default: pi, read-only tools)", required=False, is_option=True, default=None),
            ArgDef("--builder-model", "Model for the builder role on every task `do` runs (default: the builder role config)", required=False, is_option=True, default=None),
            ArgDef("--reviewer-model", "Model for the reviewer role on every task `do` runs (default: the reviewer role config)", required=False, is_option=True, default=None),
            ArgDef("--planner-model", "Model for every planner call of the plan and shape steps (default: the planner's configured model)", required=False, is_option=True, default=None),
            ArgDef("--planner-provider", "Which service plans: ollama or claude-cli (default: the configured planner role)", required=False, is_option=True, default=None),
            ArgDef("--run-unattended", "Run a generated plan of tasks without interactive confirmation and use the documented default for every open planning question, audited; it never implies --apply, a commit, a push, a merge or a deployment", required=False, is_option=True, is_flag=True),
            ArgDef("--no-ui", "Deprecated and inert: the old cockpit was deleted, so there is nothing to open; kept so existing scripts keep working", required=False, is_option=True, default="false"),
            ArgDef("--max-total-tokens", "Maximum total tokens for this job (F018 budget)", required=False, is_option=True, default=None),
            ArgDef("--max-provider-calls", "Maximum provider calls for this job (F018 budget)", required=False, is_option=True, default=None),
            ArgDef("--max-wall-clock-minutes", "Maximum wall-clock minutes for this job (F018 budget)", required=False, is_option=True, default=None),
            ArgDef("--max-cost-usd", "Maximum cost in USD for this job (F104 budget)", required=False, is_option=True, default=None),
            ArgDef("--deadline", "UTC deadline for this job as ISO 8601 string (F018 budget)", required=False, is_option=True, default=None),
            ArgDef("--no-llm", "Force heuristic intake (no LLM provider call)", required=False, is_option=True, is_flag=True),
            ArgDef("--force-job", "One job for what you ask, its tasks under the mission, whatever shape the planner chose", required=False, is_option=True, is_flag=True),
            ArgDef("--force-mission", "Two or more jobs under the mission, one per milestone outline or deliverable, whatever shape the planner chose", required=False, is_option=True, is_flag=True),
            ArgDef("--new-mission", "Accept an order file again although an earlier order of it still has unfinished jobs; it adds one more order to the repository's one mission and never starts a second mission; without it such an order file is refused before any step, naming that mission", required=False, is_option=True, is_flag=True),
            ArgDef("--step-by-step", "Halt after each step that did work: print what happened and what comes next; Enter continues, q stops", required=False, is_option=True, is_flag=True),
            ArgDef("--plan-only", "Stop after the shape step: nothing is executed, and the output lists every deliverable", required=False, is_option=True, is_flag=True),
            ArgDef("--rehearse", "Plan what you ask as `remedy do` does and stop before any job of the mission runs: no builder or reviewer worker is built, nothing is applied and nothing is written into the repository, and the job's plan of tasks keeps its approval open for you; refused with --run-unattended, --apply, a commit flag or --push", required=False, is_option=True, is_flag=True),
            ArgDef("--apply", "Apply each job of the mission to the repository, one after another, as `remedy job apply --approve` does; stops at the first that is not applied", required=False, is_option=True, is_flag=True),
            ArgDef("--contract", "Force this contract template as the floor of the mission's acceptance criteria, instead of the one Remedy proposes: api-service, cli-tool, python-library or website", required=False, is_option=True, default=None),
            ArgDef("--commit", "Implies --apply: apply each job as `remedy job apply --approve --commit` does, landing one commit of exactly its copied files on your current branch, as you, with this one line as its first line, followed by the job's number when the mission has several jobs; each job runs only after the one before it is committed. Refused before any step with --plan-only, another commit flag, a dirty tree or a detached HEAD", required=False, is_option=True, default=None),
            ArgDef("--commit-auto", "As --commit, with a first line Remedy writes from the job's title or the mission's goal", required=False, is_option=True, is_flag=True),
            ArgDef("--commit-with-history", "Implies --apply: merge each job's commits, one per applied task step, onto your current branch with git merge --no-ff instead of copying, as `remedy job apply --approve --commit-with-history` does; each job runs only after the one before it is merged", required=False, is_option=True, is_flag=True),
            ArgDef("--push", "With a commit flag only: push your branch to its configured upstream once, after the mission's last job, never forced; refused alone and, before any step, without an upstream; refused while any blocking criteria of the mission contract are unmet, naming those still open. The config key apply.push_after_mission does the same", required=False, is_option=True, is_flag=True),
        ),
        # R-0969: `remedy do "<order>" --apply` writes the repository through
        # `job_apply`, exactly as `job.apply` does, which declares the same.
        may_mutate_repo=True,
        # R-0965: a bare `remedy do "<order>"` runs its job through the same
        # runner as `job.run`, so it declares the same execution metadata.
        may_execute_commands=True,
        # R-1183: an order whose project has no registered repository names a project the
        # walk cannot act on, which is exit 3's meaning (DECISION F283 D12).
        exit_codes=(0, 1, 2, 3),
    ),
)
