"""
Command Catalog v0 — source of truth for Remedy's grouped CLI surface.

Every public CLI command has exactly one entry here.  The catalog defines:
- group membership
- argument shapes
- action classification (read_only, write_metadata, etc.)
- JSON support, permission requirements, mutation/execution flags

The grouped CLI (apps.cli.grouped) consumes this catalog to build
argparse trees and help pages.

Public API::

    CATALOG: tuple[CommandEntry, ...]
    GROUPS: dict[str, GroupDef]
    UI_EXPOSED_COMMANDS: frozenset[str]
    get_group(group_id) -> GroupDef
    resolve_group(word) -> str | None
    get_command(command_id) -> CommandEntry
    get_commands_for_group(group_id) -> list[CommandEntry]
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

ActionClass = Literal[
    "read_only",
    "write_metadata",
    "approval_gate",
    "apply_write",
    "test_execution",
    "dev_helper",
    "local_state_change",
    "controlled_builder_execution",
]


@dataclass(frozen=True)
class GroupDef:
    """A top-level command group (e.g. 'job', 'brain')."""

    id: str
    label: str
    description: str
    user_facing: bool = True
    #: A hidden group appears in no help at all, neither `remedy --help` nor
    #: `remedy --all-commands`, and stays callable: its own help and its commands
    #: still work (DECISION amend0905-vocab D4).
    hidden: bool = False
    #: Further words that reach this same group (DECISION amend0831 D-D): one
    #: `GroupDef` and one set of commands, never a duplicated definition.
    #: `resolve_group` maps each of them to `id` for every group lookup.
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class ArgDef:
    """A single CLI argument or option."""

    name: str
    help: str
    required: bool = True
    is_option: bool = False
    default: str | None = None
    #: A boolean flag takes NO value (`--status`), a valued option does (`--status pending`).
    #: Declared per ARGUMENT, because the same option name means different things to
    #: different commands: `job stop --status` is a flag, `propose list --status pending`
    #: is not. F011 briefly special-cased the NAME in the parser and broke `propose list`.
    is_flag: bool = False
    #: A repeatable option collects every occurrence into a list
    #: (`--answer q1=a --answer q2=b`) instead of last-one-wins.
    is_repeatable: bool = False


@dataclass(frozen=True)
class CommandEntry:
    """One entry in the command catalog."""

    command_id: str
    group_id: str
    subcommand: str
    description: str
    action_class: ActionClass
    args: tuple[ArgDef, ...] = ()
    supports_json: bool = False
    requires_permission: bool = False
    may_mutate_repo: bool = False
    may_execute_commands: bool = False
    #: True marks a command whose real-money spend requires an upfront
    #: estimate and, above a configured threshold, operator confirmation
    #: before it runs (F114). Explicit and reviewable per command - never
    #: derived from another flag such as may_execute_commands.
    is_expensive: bool = False
    related: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------

GROUPS: dict[str, GroupDef] = {
    # -- Golden path (pinned first in help) --
    "do": GroupDef("do", "Do", "Run, report, and apply Remedy tasks."),
    "status": GroupDef("status", "Status", "Project status overview."),
    "decision": GroupDef("decision", "Decision", "Human decision queue."),
    # -- User-facing primary commands --
    "init": GroupDef("init", "Init", "Initialize a Remedy project in a git repo."),
    "job": GroupDef("job", "Job", "Create, inspect, and manage jobs."),
    "run": GroupDef("run", "Run", "Show and list persisted ping-pong runs."),
    "project": GroupDef("project", "Project", "Create, inspect, and manage projects."),
    "ui": GroupDef("ui", "UI", "Open the local UI."),
    "doctor": GroupDef("doctor", "Doctor", "Check Remedy health."),
    "config": GroupDef("config", "Config", "View or change settings.", aliases=("settings",)),
    "worker": GroupDef("worker", "Worker", "Manage worker connections."),
    "memory": GroupDef("memory", "Memory", "Project memory."),
    "teacher": GroupDef("teacher", "Teacher", "Explain a run. Read-only, never steers it."),
    "runtime": GroupDef("runtime", "Runtime", "Start, probe and stop the project dev server."),
    "stats": GroupDef("stats", "Stats", "Honest counts from the evidence on disk."),
    # -- Advanced / internal commands (callable but hidden from default help) --
    "patch": GroupDef("patch", "Patch", "Review and apply patch intents.", user_facing=False),
    "test": GroupDef("test", "Test", "Discover and run project tests.", user_facing=False),
    "brain": GroupDef("brain", "Brain", "Inspect the project brain graph.", user_facing=False),
    "mission": GroupDef("mission", "Mission", "Persistent goals above jobs, and the bounded run-loop facade (internal).", user_facing=False),
    "change": GroupDef("change", "Change", "Review change sets (proof chain view).", user_facing=False),
    "file": GroupDef("file", "File", "File-level provenance and tracing.", user_facing=False),
    "event": GroupDef("event", "Event", "Query the audit event ledger.", user_facing=False),
    "blocker": GroupDef("blocker", "Blocker", "View and resolve stop reasons.", user_facing=False),
    "self": GroupDef("self", "Self", "Self-dogfood — inspect own evidence.", user_facing=False),
    "propose": GroupDef("propose", "Propose", "Proposed task evaluation.", user_facing=False),
    "dev": GroupDef("dev", "Dev", "Developer utilities.", user_facing=False),
    "ci": GroupDef("ci", "CI", "Remedy's own CI stages, run locally.", user_facing=False),
    "integrity": GroupDef("integrity", "Integrity", "Pre-handoff integrity checks.", user_facing=False),
    "snapshot": GroupDef("snapshot", "Snapshot", "Repository snapshot and rollback.", user_facing=False),
    # -- Hidden: in no help at all, callable (DECISION amend0905-vocab D4) --
    "roadmap": GroupDef("roadmap", "Roadmap", "Read-only roadmap mirror — what is active, what is next. Proposes, never starts.", user_facing=False, hidden=True),
}


# ---------------------------------------------------------------------------
# Argument shorthands
# ---------------------------------------------------------------------------

_JOB_ID = ArgDef("job_id", "UUID of the job")
_PROJECT_ID = ArgDef("project_id", "UUID or name of the project")
_INTENT_ID = ArgDef("intent_id", "Intent ID (integer)")
_JSON_OPT = ArgDef("--json", "Output as JSON", required=False, is_option=True, default="false")
#: F107: names ONE task of a job — its planned id (`T001`) or a prefix of its
#: task UUID. A valued option, never a flag, and never defaulted to a guess.
_TASK_OPT = ArgDef(
    "--task", "Task to select: planned id (T001) or task-id prefix",
    required=False, is_option=True)
_REASON_OPT = ArgDef("--reason", "Reason text", required=False, is_option=True)
_ANSWER_OPT = ArgDef(
    "--answer",
    'Answer one bundled clarification: --answer q1="use PostgreSQL" (repeatable)',
    required=False, is_option=True, is_repeatable=True)
_APPLY_ID_OPT = ArgDef("--apply-id", "Explicit apply_id (overrides intent_id lookup)", required=False, is_option=True)
#: F033: names ONE task run whose diff to decide hunks over. Deliberately NOT
#: `_TASK_OPT`, which promises "planned id (T001) or task-id prefix":
#: `diff_view_source.build_diff_view` does no prefix resolution at all — it
#: requires exact membership in the real `task_runs/` listing — and promising a
#: prefix match the code does not perform is worse than a second option name.
_TASK_RUN_OPT = ArgDef(
    "--task-run",
    "Task run to decide over, exactly as it is named under task_runs/ (T001); "
    "omit it to decide over the job-level diff",
    required=False, is_option=True)
#: F033: repeatable, one hunk id per occurrence.
_APPROVE_HUNK_OPT = ArgDef(
    "--approve-hunk", "Approve one hunk by id (repeatable)",
    required=False, is_option=True, is_repeatable=True)
#: F033: repeatable. The reason is kept VERBATIM — T003 quotes it into the next
#: repair prompt — so the shape is shown rather than described away.
_REJECT_HUNK_OPT = ArgDef(
    "--reject-hunk",
    'Reject one hunk with a reason: --reject-hunk <hunk-id>=<reason>, '
    'e.g. --reject-hunk h3="renames a public name" (repeatable)',
    required=False, is_option=True, is_repeatable=True)
#: F056: the plan-approval opt-in. Its ABSENCE is the default — approving
#: without it creates no mission, which is the whole point of the opt-in.
_AS_MISSION_FLAG = ArgDef(
    "--as-mission",
    "When approving: also create a mission for this goal and link this job as its initial job",
    required=False, is_option=True, is_flag=True)
_PROJECT_SCOPE_OPT = ArgDef("--project", "Scope to project (slug or UUID)", required=False, is_option=True)
_ALL_PROJECTS_FLAG = ArgDef("--all-projects", "Show jobs from all projects", required=False, is_option=True, is_flag=True)


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

_BASE_CATALOG: tuple[CommandEntry, ...] = (
    # ── init ─────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="init.run",
        group_id="init",
        subcommand="run",
        description="Initialize a Remedy project in the current git repo.",
        action_class="write_metadata",
        args=(
            ArgDef("--project-name", "Project display name (default: directory name)", required=False, is_option=True),
            ArgDef("--print-only", "Show what would happen without writing anything", required=False, is_option=True, is_flag=True),
            ArgDef("--json", "Output as JSON", required=False, is_option=True, default="false"),
        ),
    ),

    # ── status ──────────────────────────────────────────────────────────
    CommandEntry(
        command_id="status.run",
        group_id="status",
        subcommand="run",
        description="Show project status overview.",
        action_class="read_only",
        args=(
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
            ArgDef("--json", "Output as JSON", required=False, is_option=True, default="false"),
        ),
        supports_json=True,
    ),

    # ── job ──────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="job.list",
        group_id="job",
        subcommand="list",
        description="List jobs (scoped to current project by default).",
        action_class="read_only",
        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG, _JSON_OPT),
        supports_json=True,
    ),
    CommandEntry(
        command_id="job.show",
        group_id="job",
        subcommand="show",
        description="Show job details; the output is always JSON, so --json is accepted and changes nothing.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--full", "Print every finding of a blocked task instead of the first ten, "
                   "and the job's sections (its permissions, fences, assumptions, "
                   "completion digest, summary, status, report and Definition of Done)",
                   required=False, is_option=True, is_flag=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("job.list", "brain.graph"),
    ),
    CommandEntry(
        command_id="teacher.narrate",
        group_id="teacher",
        subcommand="narrate",
        description="Narrate a job's run log in plain sentences (read-only).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("job.show",),
    ),
    CommandEntry(
        # write_metadata, NOT read_only (DECISION F255 D10): answering costs a
        # model call, and that call is recorded as exactly one token-ledger row.
        # The invariant this role really carries — never influencing the RUN —
        # is proven behaviourally in tests/cli/test_teacher_cmd.py.
        command_id="teacher.ask",
        group_id="teacher",
        subcommand="ask",
        description="Ask the teacher about a run or your code. Records one spend row; never steers the run.",
        action_class="write_metadata",
        args=(
            ArgDef("question", "What you want explained"),
            ArgDef("--job-id", "Job whose run log grounds the answer", required=False, is_option=True),
            # Grounding source (2), the workspace code. Read-only: the file is
            # opened for reading and nothing is written back, so this option
            # leaves the write_metadata class above untouched.
            ArgDef("--file", "Source file to ground the answer in; read only, never written", required=False, is_option=True),
            ArgDef("--level", "Explanation depth: student, beginner or pro", required=False, is_option=True),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("teacher.narrate",),
    ),
    CommandEntry(
        command_id="job.attach-repo",
        group_id="job",
        subcommand="attach-repo",
        description="Attach a repository path to a job.",
        action_class="write_metadata",
        args=(_JOB_ID, ArgDef("repo_path", "Path to the repository")),
    ),
    CommandEntry(
        command_id="job.permit",
        group_id="job",
        subcommand="permit",
        description="Grant or deny a permission for a job.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("permission", "Permission name"),
            ArgDef("action", "allow or deny"),
        ),
        requires_permission=True,
        related=("job.show",),
    ),
    CommandEntry(
        command_id="job.stop",
        group_id="job",
        subcommand="stop",
        description="Request a safe stop of a running job (F011 kill switch).",
        action_class="write_metadata",
        supports_json=True,
        args=(
            ArgDef("job_id", "Job ID to stop"),
            ArgDef("--reason", "Why the job is being stopped (recorded in the evidence)", required=False, is_option=True, default=""),
            ArgDef("--source", "Who requested the stop (default: cli)", required=False, is_option=True, default="cli"),
            ArgDef("--status", "Show pending and consumed stop requests instead of requesting one", required=False, is_option=True, is_flag=True),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("job.run", "job.show"),
    ),
    CommandEntry(
        command_id="job.budget",
        group_id="job",
        subcommand="budget",
        description="Show a job's budget limits and counters (F018), or with set <field> <value> "
                    "write one integer field of its execution limits or its token budget profile.",
        # write_metadata, NOT read_only (DECISION F280 D3): the set form writes the job record's
        # run contract or the job's token budget profile. The show form still writes nothing.
        action_class="write_metadata",
        supports_json=True,
        args=(
            ArgDef("job_id", "Job ID to inspect"),
            ArgDef("action", "Omit to show the budget; set writes one field", required=False),
            ArgDef("field", "The field set writes; a wrong name lists the settable ones", required=False),
            ArgDef("value", "The integer value set writes", required=False),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("job.show", "job.stop"),
    ),

    CommandEntry(
        command_id="job.plan",
        group_id="job",
        subcommand="plan",
        description="Plan tasks for a job using local LLM.",
        action_class="write_metadata",
        args=(_JOB_ID,),
        related=("job.resume",),
    ),

    CommandEntry(
        command_id="job.context",
        group_id="job",
        subcommand="context",
        description=("Show the compiled context for one task — what it "
                     "receives and what was omitted (F107)."),
        action_class="read_only",
        args=(_JOB_ID, _TASK_OPT, _JSON_OPT),
        supports_json=True,
        related=("job.show",),
    ),

    # ── project ──────────────────────────────────────────────────────────
    CommandEntry(
        command_id="project.create",
        group_id="project",
        subcommand="create",
        description="Create a new project.",
        action_class="write_metadata",
        args=(
            ArgDef("name", "Project name"),
            ArgDef("--description", "Project description", required=False, is_option=True),
        ),
        related=("project.show",),
    ),
    CommandEntry(
        command_id="project.list",
        group_id="project",
        subcommand="list",
        description="List all projects.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
    ),
    CommandEntry(
        command_id="project.show",
        group_id="project",
        subcommand="show",
        description="Show project details.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
        related=("project.list", "project.context"),
    ),
    CommandEntry(
        command_id="project.attach-repo",
        group_id="project",
        subcommand="attach-repo",
        description="Attach a repository path to a project.",
        action_class="write_metadata",
        args=(_PROJECT_ID, ArgDef("repo_path", "Path to the repository")),
    ),
    CommandEntry(
        command_id="project.attach-job",
        group_id="project",
        subcommand="attach-job",
        description="Link a job to a project.",
        action_class="write_metadata",
        args=(_PROJECT_ID, _JOB_ID),
    ),
    CommandEntry(
        command_id="project.brain",
        group_id="project",
        subcommand="brain",
        description="Show the aggregate project brain graph across all jobs.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
        related=("brain.graph", "project.show"),
    ),
    CommandEntry(
        command_id="project.context",
        group_id="project",
        subcommand="context",
        description="Show project context and constitution.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
        related=("project.show",),
    ),

    CommandEntry(
        command_id="project.summary",
        group_id="project",
        subcommand="summary",
        description="Show project-level summary with patterns and suggestions.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
        related=("project.show", "project.brain"),
    ),
    CommandEntry(
        command_id="project.current",
        group_id="project",
        subcommand="current",
        description="Show the project resolved from the current directory.",
        action_class="read_only",
        args=(
            ArgDef("--project", "Project slug or UUID", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("project.show", "project.list"),
    ),
    CommandEntry(
        command_id="project.attach",
        group_id="project",
        subcommand="attach",
        description="Attach a repository path to the current project.",
        action_class="write_metadata",
        args=(
            ArgDef("--project", "Project slug or UUID", required=False, is_option=True),
            ArgDef("--repo", "Path to the repository", required=True, is_option=True),
        ),
        related=("project.current",),
    ),
    CommandEntry(
        command_id="project.adopt",
        group_id="project",
        subcommand="adopt",
        description="Adopt a single unscoped job into the current project.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--project", "Project slug or UUID", required=False, is_option=True),
        ),
        related=("project.attach-job", "job.list"),
    ),

    # ── patch ────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="patch.list",
        group_id="patch",
        subcommand="list",
        description="List patch intents for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("patch.show", "patch.approve"),
    ),
    CommandEntry(
        command_id="patch.show",
        group_id="patch",
        subcommand="show",
        description="Show a specific patch intent.",
        action_class="read_only",
        args=(_JOB_ID, _INTENT_ID),
        related=("patch.approve", "patch.reject"),
    ),
    CommandEntry(
        command_id="patch.approve",
        group_id="patch",
        subcommand="approve",
        description="Approve a patch intent for application.",
        action_class="approval_gate",
        args=(_JOB_ID, _INTENT_ID, _REASON_OPT),
        related=("patch.apply", "patch.reject"),
    ),
    CommandEntry(
        command_id="patch.reject",
        group_id="patch",
        subcommand="reject",
        description="Reject a patch intent.",
        action_class="approval_gate",
        args=(_JOB_ID, _INTENT_ID, _REASON_OPT),
        related=("patch.approve",),
    ),
    CommandEntry(
        command_id="patch.apply",
        group_id="patch",
        subcommand="apply",
        description="Apply an approved patch intent to the repo.",
        action_class="apply_write",
        args=(_JOB_ID, _INTENT_ID, _JSON_OPT),
        supports_json=True,
        may_mutate_repo=True,
        requires_permission=True,
        related=("patch.approve", "test.run"),
    ),

    CommandEntry(
        command_id="patch.revert",
        group_id="patch",
        subcommand="revert",
        description="Revert a previously applied patch intent using stored snapshot.",
        action_class="apply_write",
        args=(_JOB_ID, _INTENT_ID, _APPLY_ID_OPT, _JSON_OPT),
        supports_json=True,
        may_mutate_repo=True,
        requires_permission=True,
        related=("patch.apply", "snapshot.list-applies"),
    ),

    CommandEntry(
        command_id="patch.approve-hunks",
        group_id="patch",
        subcommand="approve-hunks",
        description="Record a hunk-level approve and reject decision over a job's diff.",
        action_class="approval_gate",
        args=(_JOB_ID, _TASK_RUN_OPT, _APPROVE_HUNK_OPT, _REJECT_HUNK_OPT, _JSON_OPT),
        supports_json=True,
        # `may_mutate_repo` and `requires_permission` are LEFT AT False on
        # purpose: DECISION F033 D4 rules that recording a decision is not
        # applying it. This command writes `job.metadata` and touches no
        # repository, and this table is the one place the UI reads capability
        # from, so claiming otherwise would misdescribe the decision.
        related=("patch.approve", "patch.apply"),
    ),

    # ── test ─────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="test.discover",
        group_id="test",
        subcommand="discover",
        description="Discover available test commands in the repo.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("test.run",),
    ),
    CommandEntry(
        command_id="test.run",
        group_id="test",
        subcommand="run",
        description="Run discovered tests for a job (contract-gated, resource-safe).",
        action_class="test_execution",
        args=(
            _JOB_ID,
            ArgDef("--task-id", "Link run to a task ID", required=False,
                   is_option=True, default=""),
            ArgDef("--intent-id", "Link run to a patch intent ID", required=False,
                   is_option=True, default=""),
            ArgDef("--apply-id", "Link run to an apply record ID", required=False,
                   is_option=True, default=""),
            ArgDef("--timeout-seconds", "Override process timeout (seconds)", required=False,
                   is_option=True, default=""),
            _JSON_OPT,
        ),
        supports_json=True,
        may_execute_commands=True,
        requires_permission=True,
        related=("test.discover",),
    ),

    CommandEntry(
        command_id="test.status",
        group_id="test",
        subcommand="status",
        description="Show current test run status for a job (lease state, latest run, usage).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("test.run", "test.discover"),
    ),
    # ── real test execution v1 (result/list/integrity; snapshot proof) ──
    CommandEntry(
        command_id="test.result",
        group_id="test",
        subcommand="result",
        description="Show a safe test run result by test_run_id (read-only; no raw output).",
        action_class="read_only",
        args=(ArgDef("test_run_id", "Test run ID"), _JSON_OPT),
        supports_json=True,
        related=("test.run", "test.list"),
    ),
    CommandEntry(
        command_id="test.list",
        group_id="test",
        subcommand="list",
        description="List safe test run records for a job (read-only; no raw output).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("test.result", "test.status"),
    ),
    CommandEntry(
        command_id="test.integrity",
        group_id="test",
        subcommand="integrity",
        description="Check test-execution / snapshot / rollback invariants (read-only; safe codes — no fake pass/restore).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("test.list", "snapshot.create"),
    ),
    CommandEntry(
        command_id="snapshot.create",
        group_id="snapshot",
        subcommand="create",
        description="Record an honest metadata snapshot proof of a job's repo (write_metadata; NOT a rollback restore).",
        action_class="write_metadata",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("snapshot.show",),
    ),
    CommandEntry(
        command_id="snapshot.show",
        group_id="snapshot",
        subcommand="show",
        description="Show a snapshot proof by snapshot_id (read-only).",
        action_class="read_only",
        args=(ArgDef("snapshot_id", "Snapshot proof ID"), _JSON_OPT),
        supports_json=True,
        related=("snapshot.create",),
    ),

    # ── repair (Token-Aware Repair Loop v1/v2) ───────────────────────────


    # ── brain ────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="brain.graph",
        group_id="brain",
        subcommand="graph",
        description="Show the project brain graph.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("brain.node", "brain.view"),
    ),
    CommandEntry(
        command_id="brain.node",
        group_id="brain",
        subcommand="node",
        description="Show details for a specific brain node.",
        action_class="read_only",
        args=(_JOB_ID, ArgDef("node_id", "Brain node ID"), _JSON_OPT),
        supports_json=True,
        related=("brain.graph",),
    ),
    CommandEntry(
        command_id="brain.view",
        group_id="brain",
        subcommand="view",
        description="Open the interactive brain viewer.",
        action_class="read_only",
        args=(_JOB_ID,),
        related=("brain.graph",),
    ),
    CommandEntry(
        command_id="brain.context",
        group_id="brain",
        subcommand="context",
        description="Show brain context for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("brain.graph",),
    ),
    CommandEntry(
        command_id="brain.trust",
        group_id="brain",
        subcommand="trust",
        description="Show the trust report for a job.",
        action_class="read_only",
        args=(_JOB_ID,),
        related=("brain.timeline",),
    ),
    CommandEntry(
        command_id="brain.timeline",
        group_id="brain",
        subcommand="timeline",
        description="Show the event timeline for a job.",
        action_class="read_only",
        args=(_JOB_ID,),
        related=("brain.trust",),
    ),

    CommandEntry(
        command_id="brain.cockpit",
        group_id="brain",
        subcommand="cockpit",
        description="Show the human cockpit summary for a job.",
        action_class="read_only",
        args=(_JOB_ID,),
        related=("brain.graph", "brain.trust"),
    ),
    CommandEntry(
        command_id="brain.continue",
        group_id="brain",
        subcommand="continue",
        description="Create a child job from a brain node (continue-from-node).",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("node_id", "Brain node ID to continue from"),
            ArgDef("--prompt", "Prompt for the child job", required=True, is_option=True),
            ArgDef("--task-type", "Task type for the child job", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("brain.graph", "brain.node"),
    ),
    CommandEntry(
        command_id="brain.constitution",
        group_id="brain",
        subcommand="constitution",
        description="Show the project constitution for a job.",
        action_class="read_only",
        args=(_JOB_ID,),
        related=("brain.context",),
    ),
    CommandEntry(
        command_id="brain.open",
        group_id="brain",
        subcommand="open",
        description="Generate and open the brain viewer in default browser.",
        action_class="read_only",
        args=(_JOB_ID,),
        related=("brain.view", "brain.viewer-path"),
    ),
    CommandEntry(
        command_id="brain.viewer-path",
        group_id="brain",
        subcommand="viewer-path",
        description="Print the path to the brain viewer index.html.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("brain.open", "brain.export-viewer"),
    ),
    CommandEntry(
        command_id="brain.export-viewer",
        group_id="brain",
        subcommand="export-viewer",
        description="Export the brain viewer to a target directory.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--out", "Output directory path", required=True, is_option=True),
        ),
        related=("brain.open", "brain.viewer-path"),
    ),

    # ── worker ───────────────────────────────────────────────────────────
    CommandEntry(
        command_id="worker.list",
        group_id="worker",
        subcommand="list",
        description="List known worker provider specs.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
    ),

    CommandEntry(
        command_id="worker.show",
        group_id="worker",
        subcommand="show",
        description="Show details of a single worker adapter.",
        action_class="read_only",
        args=(ArgDef("provider_id", "Provider ID (e.g. ollama)"), _JSON_OPT),
        supports_json=True,
        related=("worker.list",),
    ),

    CommandEntry(
        command_id="worker.resources",
        group_id="worker",
        subcommand="resources",
        description="Show GPU/VRAM and loaded model resources (best-effort).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("worker.unload",),
    ),
    CommandEntry(
        command_id="worker.unload",
        group_id="worker",
        subcommand="unload",
        description="Unload local models from VRAM (Ollama).",
        action_class="write_metadata",
        args=(
            ArgDef("--provider", "Provider to unload (default: ollama)", required=False, is_option=True, default="ollama"),
            ArgDef("--model", "Specific model to unload", required=False, is_option=True),
            ArgDef("--all", "Unload all loaded models", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("worker.resources",),
    ),
    CommandEntry(
        command_id="worker.status",
        group_id="worker",
        subcommand="status",
        description="Show current worker status.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("worker.list",),
    ),

    # ── mission (the F070 orchestrator loop, keyed on a mission id) ──────
    CommandEntry(
        command_id="mission.run",
        group_id="mission",
        subcommand="run",
        description="Run the F070 orchestrator loop for one mission. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
        action_class="write_metadata",
        args=(
            ArgDef("run_id", "Mission id (F070 loop)"),
            ArgDef("--iterations", "Max orchestrator iterations this run", required=False, is_option=True),
            ArgDef("--no-llm", "Run without a provider — reports the honest no_provider terminal", required=False, is_option=True, is_flag=True),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.report", "mission.watchdog"),
    ),
    CommandEntry(
        command_id="mission.watchdog",
        group_id="mission",
        subcommand="watchdog",
        description="Evaluate a mission's autonomy tripwires and report what fired, with the evidence behind it (read-only: it pauses nothing and raises no decision).",
        action_class="read_only",
        args=(
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.show", "mission.resume"),
    ),
    CommandEntry(
        command_id="mission.handoff",
        group_id="mission",
        subcommand="handoff",
        description="Compose this mission's handoff artifact — dossier, checkpoint reference, open decisions and next intent — so a fresh context can resume from it (F079).",
        action_class="write_metadata",
        args=(
            ArgDef("mission_id", "Mission id"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.show", "mission.watchdog"),
    ),
    CommandEntry(
        command_id="mission.report",
        group_id="mission",
        subcommand="report",
        description="Read-only morning-style report built from the job's current evidence.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--markdown", "Render the report as markdown",
                   required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("mission.readiness", "mission.show"),
    ),

    # ── mission (F056: the persistent goal above a chain of jobs) ────────
    CommandEntry(
        command_id="mission.start",
        group_id="mission",
        subcommand="start",
        description="Create a mission — a persistent goal above the jobs that will serve it (explicit; never automatic).",
        action_class="write_metadata",
        args=(
            ArgDef("goal", "The persistent goal this mission exists for"),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.list", "mission.show"),
    ),
    CommandEntry(
        command_id="mission.list",
        group_id="mission",
        subcommand="list",
        description="List missions (scoped to the current project by default; unreadable records are skipped and counted).",
        action_class="read_only",
        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG, _JSON_OPT),
        supports_json=True,
        related=("mission.start", "mission.show"),
    ),
    CommandEntry(
        command_id="mission.continue",
        group_id="mission",
        subcommand="continue",
        description="Add the next job to a mission — its plan always begins with a task that verifies the previous job's Definition of Done.",
        action_class="write_metadata",
        args=(
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
            ArgDef("next_step", "What this next job should do"),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.show", "mission.start"),
    ),
    CommandEntry(
        command_id="mission.plan",
        group_id="mission",
        subcommand="plan",
        description="Compile a mission's goal into a milestone plan (recompiles keep prior versions; refused once a milestone is in progress). Creates no jobs and starts nothing.",
        action_class="write_metadata",
        args=(
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
            ArgDef("--no-llm", "Compile deterministically (no LLM provider call)", required=False, is_option=True, is_flag=True),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.show", "mission.start"),
    ),
    CommandEntry(
        command_id="mission.show",
        group_id="mission",
        subcommand="show",
        description="Show one mission and its job chain, each job with the state the job store reports now.",
        action_class="read_only",
        args=(
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.list", "mission.start"),
    ),
    # Status transitions are their own explicit subcommands (R-0163): the verb
    # names the status, and nothing else in Remedy ever moves it.
    CommandEntry(
        command_id="mission.achieve",
        group_id="mission",
        subcommand="achieve",
        description="Mark a mission achieved — an explicit human judgement, never inferred from its jobs.",
        action_class="write_metadata",
        args=(
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.show", "mission.list"),
    ),
    CommandEntry(
        command_id="mission.abandon",
        group_id="mission",
        subcommand="abandon",
        description="Mark a mission abandoned — the goal is dropped; its jobs and their evidence stay.",
        action_class="write_metadata",
        args=(
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.show", "mission.list"),
    ),
    CommandEntry(
        command_id="mission.pause",
        group_id="mission",
        subcommand="pause",
        description="Mark a mission paused — the goal still stands, work on it does not.",
        action_class="write_metadata",
        args=(
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.show", "mission.list"),
    ),
    CommandEntry(
        command_id="mission.resume",
        group_id="mission",
        subcommand="resume",
        description="Mark a mission active again — the pause is lifted; the tripwire that caused it is not cleared.",
        action_class="write_metadata",
        args=(
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.pause", "mission.watchdog"),
    ),
    CommandEntry(
        command_id="mission.readiness",
        group_id="mission",
        subcommand="readiness",
        description="Read-only: is this job safe to run unattended?",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("mission.show", "mission.watchdog"),
    ),

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

    # ── memory ───────────────────────────────────────────────────────────
    CommandEntry(
        command_id="memory.store",
        group_id="memory",
        subcommand="store",
        description="Store a memory entry (key=value).",
        action_class="write_metadata",
        args=(
            ArgDef("key", "Memory key"),
            ArgDef("value", "Memory value"),
            ArgDef("--project", "Project UUID scope", required=False, is_option=True),
            ArgDef("--job", "Job UUID scope", required=False, is_option=True),
            ArgDef("--tags", "Comma-separated tags", required=False, is_option=True),
            ArgDef("--approved", "Mark as approved", required=False, is_option=True),
        ),
    ),
    CommandEntry(
        command_id="memory.recall",
        group_id="memory",
        subcommand="recall",
        description="Recall memory entries by keyword.",
        action_class="read_only",
        args=(
            ArgDef("--project", "Project UUID scope", required=False, is_option=True),
            ArgDef("--job", "Job UUID scope", required=False, is_option=True),
            ArgDef("--keyword", "Search keyword", required=False, is_option=True),
            ArgDef("--limit", "Max entries to return (default: 5)", required=False, is_option=True, default="5"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="memory.list",
        group_id="memory",
        subcommand="list",
        description="List all memory entries for a scope.",
        action_class="read_only",
        args=(
            ArgDef("--project", "Project UUID scope", required=False, is_option=True),
            ArgDef("--job", "Job UUID scope", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),

    CommandEntry(
        command_id="memory.learn",
        group_id="memory",
        subcommand="learn",
        description="Learn memory from job run evidence.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--approved", "Mark learned entries as approved", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),

    CommandEntry(
        command_id="memory.card-show",
        group_id="memory",
        subcommand="card-show",
        description="Show a memory card by ID.",
        action_class="read_only",
        args=(
            ArgDef("memory_id", "Memory entry ID", required=True),
            ArgDef("--project", "Project ID scope", required=False, is_option=True),
            ArgDef("--job", "Job ID scope", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="memory.card-approve",
        group_id="memory",
        subcommand="card-approve",
        description="Approve a memory card.",
        action_class="write_metadata",
        args=(
            ArgDef("memory_id", "Memory entry ID", required=True),
            ArgDef("--project", "Project ID scope", required=False, is_option=True),
            ArgDef("--job", "Job ID scope", required=False, is_option=True),
        ),
    ),
    CommandEntry(
        command_id="memory.card-reject",
        group_id="memory",
        subcommand="card-reject",
        description="Reject a memory card.",
        action_class="write_metadata",
        args=(
            ArgDef("memory_id", "Memory entry ID", required=True),
            ArgDef("--project", "Project ID scope", required=False, is_option=True),
            ArgDef("--job", "Job ID scope", required=False, is_option=True),
        ),
    ),
    CommandEntry(
        command_id="memory.card-stale",
        group_id="memory",
        subcommand="card-stale",
        description="Mark a memory card as stale.",
        action_class="write_metadata",
        args=(
            ArgDef("memory_id", "Memory entry ID", required=True),
            ArgDef("--project", "Project ID scope", required=False, is_option=True),
            ArgDef("--job", "Job ID scope", required=False, is_option=True),
        ),
    ),
    CommandEntry(
        command_id="memory.card-supersede",
        group_id="memory",
        subcommand="card-supersede",
        description="Mark a memory card as superseded by another.",
        action_class="write_metadata",
        args=(
            ArgDef("old_id", "Memory ID to supersede", required=True),
            ArgDef("new_id", "Memory ID that supersedes", required=True),
            ArgDef("--project", "Project ID scope", required=False, is_option=True),
            ArgDef("--job", "Job ID scope", required=False, is_option=True),
        ),
    ),
    CommandEntry(
        command_id="memory.card-contradict",
        group_id="memory",
        subcommand="card-contradict",
        description="Mark a memory card as contradicted by another.",
        action_class="write_metadata",
        args=(
            ArgDef("memory_id", "Memory ID to contradict", required=True),
            ArgDef("by_id", "Memory ID that contradicts", required=True),
            ArgDef("--project", "Project ID scope", required=False, is_option=True),
            ArgDef("--job", "Job ID scope", required=False, is_option=True),
        ),
    ),
    CommandEntry(
        command_id="memory.candidates",
        group_id="memory",
        subcommand="candidates",
        description="List memory candidates for a job (pending human approval).",
        action_class="read_only",
        args=(
            _JOB_ID,
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="memory.approve-candidate",
        group_id="memory",
        subcommand="approve-candidate",
        description="Approve a memory candidate (creates approved memory).",
        action_class="approval_gate",
        args=(
            _JOB_ID,
            ArgDef("candidate_id", "Candidate ID to approve", required=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="memory.reject-candidate",
        group_id="memory",
        subcommand="reject-candidate",
        description="Reject a memory candidate (no memory created).",
        action_class="approval_gate",
        args=(
            _JOB_ID,
            ArgDef("candidate_id", "Candidate ID to reject", required=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),

    # ── change ───────────────────────────────────────────────────────────
    CommandEntry(
        command_id="change.list",
        group_id="change",
        subcommand="list",
        description="List change sets for a job (proof chain review).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("change.show", "patch.list"),
    ),
    CommandEntry(
        command_id="change.show",
        group_id="change",
        subcommand="show",
        description="Show a single change set in detail.",
        action_class="read_only",
        args=(_JOB_ID, _INTENT_ID, _JSON_OPT),
        supports_json=True,
        related=("change.list",),
    ),
    CommandEntry(
        command_id="change.proof",
        group_id="change",
        subcommand="proof",
        description="Show proof chain — why changes happened and verification status.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--path", "Filter to a specific file path", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("change.list", "change.show", "file.why"),
    ),

    # ── file ─────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="file.why",
        group_id="file",
        subcommand="why",
        description="Trace why a file was changed (causal provenance chain).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("path", "File path to trace"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("brain.graph", "patch.show"),
    ),

    # ── event ────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="event.list",
        group_id="event",
        subcommand="list",
        description="List audit events for a job (safe, redacted).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--type", "Filter by event type", required=False, is_option=True),
            ArgDef("--since", "Filter events after timestamp", required=False, is_option=True),
            ArgDef("--limit", "Max events (default: 50)", required=False, is_option=True, default="50"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="event.show",
        group_id="event",
        subcommand="show",
        description="Show a single audit event by ID.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("event_id", "Event ID (hex prefix)"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="event.timeline",
        group_id="event",
        subcommand="timeline",
        description="Show full event timeline for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
    ),

    CommandEntry(
        command_id="event.replay",
        group_id="event",
        subcommand="replay",
        description="Replay job progress from event ledger (safe, redacted).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("event.timeline", "job.checkpoints"),
    ),

    # ── job (additional) ────────────────────────────────────────────────
    CommandEntry(
        command_id="job.checkpoints",
        group_id="job",
        subcommand="checkpoints",
        description="List resume-safe checkpoints for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("event.replay", "job.resume"),
    ),
    CommandEntry(
        command_id="job.resume",
        group_id="job",
        subcommand="resume",
        description=(
            "Resume a job. Without --checkpoint: continue from the newest valid "
            "cycle checkpoint (F047) — a pending stop request is consumed first, "
            "worktree drift refuses, the plan-approval gate still applies. With "
            "--checkpoint <id>: resume from that safe event-replay checkpoint."
        ),
        action_class="apply_write",
        args=(
            _JOB_ID,
            ArgDef("--checkpoint", "Event-replay checkpoint ID to resume from",
                   required=False, is_option=True),
            ArgDef("--dry-run", "Preview resume without executing", required=False, is_option=True, default="false"),
            ArgDef("--cycles", "Maximum cycles for the resumed run (capped by the rollout default)",
                   required=False, is_option=True),
            ArgDef("--unattended",
                   "Run without a human present: a task decision that carries a safe "
                   "default is auto-answered from it and recorded in the escalation "
                   "assumption log. A question with no safe default still waits.",
                   required=False, is_option=True, is_flag=True),
            ArgDef("--yes", "Skip the cost-preview confirmation prompt above the "
                            "configured threshold (F114). Never bypasses budget "
                            "limits or the escalation log.",
                   required=False, is_option=True, is_flag=True),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=True,
        may_execute_commands=True,
        requires_permission=True,
        is_expensive=True,
        related=("job.checkpoints", "event.replay"),
    ),

    # ── blocker ─────────────────────────────────────────────────────────
    CommandEntry(
        command_id="blocker.list",
        group_id="blocker",
        subcommand="list",
        description="List stop reasons / blockers for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
    ),
    CommandEntry(
        command_id="blocker.show",
        group_id="blocker",
        subcommand="show",
        description="Show a single blocker by ID.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("stop_id", "Stop reason ID"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="blocker.resolve",
        group_id="blocker",
        subcommand="resolve",
        description="Resolve a blocker.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("stop_id", "Stop reason ID"),
            _REASON_OPT,
        ),
    ),

    # ── decision ────────────────────────────────────────────────────────
    CommandEntry(
        command_id="decision.list",
        group_id="decision",
        subcommand="list",
        description="List pending human decisions for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
    ),
    CommandEntry(
        command_id="decision.show",
        group_id="decision",
        subcommand="show",
        description="Show a single decision by ID.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("decision_id", "Decision ID"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="decision.resolve",
        group_id="decision",
        subcommand="resolve",
        description="Resolve a decision (if backed by a resolvable record).",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("decision_id", "Decision ID"),
            _REASON_OPT,
            _ANSWER_OPT,
            _AS_MISSION_FLAG,
        ),
    ),
    CommandEntry(
        command_id="decision.explain",
        group_id="decision",
        subcommand="explain",
        description="Explain all pending decisions for a job.",
        action_class="read_only",
        args=(_JOB_ID,),
    ),

    # ── ui ───────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="ui.start",
        group_id="ui",
        subcommand="start",
        description="Start the localhost UI server for a job.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--port", "Port number (0 = auto, default: 8787)", required=False, is_option=True, default="8787"),
            ArgDef("--host", "Bind host (only 127.0.0.1 allowed)", required=False, is_option=True, default="127.0.0.1"),
            ArgDef("--no-open", "Do not open browser automatically", required=False, is_option=True, default="false"),
            ArgDef("--info-file", "Write server info JSON to this path", required=False, is_option=True),
        ),
        related=("brain.view",),
    ),
    CommandEntry(
        command_id="ui.latest",
        group_id="ui",
        subcommand="latest",
        description="Open the most recently started UI session in a browser.",
        action_class="read_only",
        args=(),
    ),
    CommandEntry(
        command_id="ui.status",
        group_id="ui",
        subcommand="status",
        description="Show status of all UI sessions.",
        action_class="read_only",
        args=(),
    ),
    CommandEntry(
        command_id="ui.stop",
        group_id="ui",
        subcommand="stop",
        description="Stop all running UI sessions.",
        action_class="read_only",
        args=(),
    ),
    CommandEntry(
        command_id="ui.open",
        group_id="ui",
        subcommand="open",
        description="Open browser for a specific job UI session.",
        action_class="read_only",
        args=(_JOB_ID,),
    ),

    # ── do ───────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="do.run",
        group_id="do",
        subcommand="run",
        description="Start a controlled autorun for a goal.",
        action_class="write_metadata",
        supports_json=True,
        related=("job.show", "change.proof"),
        args=(
            ArgDef("goal", "Goal to accomplish", required=False),
            ArgDef("--repo", "Path to target repository", required=False, is_option=True, default="."),
            ArgDef("--project", "Project ID to use or create", required=False, is_option=True),
            ArgDef("--autonomy-level", "Autonomy level 0-7 (default: 2)", required=False, is_option=True, default="2"),
            ArgDef("--max-cycles", "Maximum cycles (default: 3)", required=False, is_option=True, default="3"),
            ArgDef("--ui", "Start UI alongside run", required=False, is_option=True, default="false"),
            ArgDef("--dry-run", "Show plan without executing", required=False, is_option=True, default="false"),
            ArgDef("--json", "Output JSON", required=False, is_option=True, default="false"),
            ArgDef("--fixture-builder", "Fixture builder mode: true (default) or repair-loop", required=False, is_option=True, default="false"),
            ArgDef("--builder-provider", "Builder provider: none, fixture, ollama (default: none)", required=False, is_option=True, default="none"),
            ArgDef("--no-ui", "Suppress UI server even if --ui is set", required=False, is_option=True, default="false"),
            ArgDef("--max-total-tokens", "Maximum total tokens for this job (F018 budget)", required=False, is_option=True, default=None),
            ArgDef("--max-provider-calls", "Maximum provider calls for this job (F018 budget)", required=False, is_option=True, default=None),
            ArgDef("--max-wall-clock-minutes", "Maximum wall-clock minutes for this job (F018 budget)", required=False, is_option=True, default=None),
            ArgDef("--max-cost-usd", "Maximum cost in USD for this job (F104 budget)", required=False, is_option=True, default=None),
            ArgDef("--deadline", "UTC deadline for this job as ISO 8601 string (F018 budget)", required=False, is_option=True, default=None),
            ArgDef("--no-llm", "Force heuristic intake (no LLM provider call)", required=False, is_option=True, is_flag=True),
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="run.show",
        group_id="run",
        subcommand="show",
        description="Show a persisted ping-pong run report.",
        action_class="read_only",
        supports_json=True,
        related=("do.run",),
        args=(
            ArgDef("run_id", "Run ID"),
            ArgDef("--repo", "Path to target repository", required=False, is_option=True, default="."),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),

    CommandEntry(
        command_id="run.list",
        group_id="run",
        subcommand="list",
        description="List persisted ping-pong runs.",
        action_class="read_only",
        supports_json=True,
        related=("do.run",),
        args=(
            ArgDef("--repo", "Path to target repository", required=False, is_option=True, default="."),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),

    # ── do.job-* ──────────────────────────────────────────────────────
    CommandEntry(
        command_id="job.run",
        group_id="job",
        subcommand="run",
        description="Run pending job tasks sequentially through Builder/Reviewer/Repair.",
        action_class="write_metadata",
        supports_json=True,
        related=("job.show",),
        args=(
            ArgDef("job_id", "Job ID"),
            ArgDef("--max-rounds", "Max ping-pong rounds per task (default: 3, persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--repair-rounds", "Max repair attempts per task (default: 2, 0=disabled, persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--test-command", "Test command to run in staging (persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--claude-cli-write-mode", "Claude CLI write mode: none, allowed-tools, dangerous-skip (default: none, persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--stream-evidence", "Opt-in F004 raw stream evidence: use Claude CLI stream-json and write redacted raw_stream.jsonl + run_events.jsonl. Omitted keeps the persisted/default mode", required=False, is_option=True),
            ArgDef("--no-stream-evidence", "Explicitly disable raw stream evidence (overrides a persisted true). Omitted keeps the persisted/default mode", required=False, is_option=True),
            ArgDef("--tasks", "Max tasks to execute (omitted keeps persisted; 0=all)", required=False, is_option=True, default=None),
            ArgDef("--timeout-sec", "Raw per-call timeout in seconds (omitted keeps persisted/default)", required=False, is_option=True, default=None),
            ArgDef("--max-output-chars", "Max provider output chars (omitted keeps persisted/default)", required=False, is_option=True, default=None),
            ArgDef("--builder-provider", "Builder provider: claude, claude-cli, fake or ollama (persisted on continuation)", required=False, is_option=True, default=None),
            ArgDef("--builder-model", "Model for builder role", required=False, is_option=True, default=None),
            ArgDef("--builder-effort", "Effort level for builder role", required=False, is_option=True, default=None),
            ArgDef("--reviewer-provider", "Reviewer provider: claude, claude-cli, fake or ollama (persisted on continuation)", required=False, is_option=True, default=None),
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
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=True,
    ),
    # ── stats (F010) ─────────────────────────────────────────────────────
    CommandEntry(
        command_id="stats.failures",
        group_id="stats",
        subcommand="failures",
        description="Failure histogram from the recorded post-mortems (read-only).",
        action_class="read_only",
        supports_json=True,
        args=(
            ArgDef("--job", "Only this job's evidence export", required=False, is_option=True),
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
            "Capability trend from the append-only bench history: the last run, "
            "the series before it, and a regression warning naming the order and "
            "both numbers. Never runs the bench (read-only)."
        ),
        action_class="read_only",
        supports_json=True,
        related=("stats.cost", "stats.report"),
        args=(
            ArgDef("--series", "Which bench series to read (default: the series of the latest run)", required=False, is_option=True),
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
            ArgDef("--job", "Only this job's calls", required=False, is_option=True),
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
            ArgDef("--job", "Only this job's calls", required=False, is_option=True),
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
            ArgDef("--job", "Only this job's calls, in this period and in the one before it", required=False, is_option=True),
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
            "Mirror an evidence directory's finalized task runs into the project's token "
            "ledger. WRITES the ledger (never the evidence) and is idempotent: a re-run "
            "adds no row."
        ),
        action_class="write_metadata",
        supports_json=True,
        related=("stats.cost", "stats.verify-ledger"),
        args=(
            ArgDef("evidence_dir", "Path to the job evidence directory to scan"),
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
            "Reconcile the evidence files against the token ledger rows (read-only). "
            "Exits 0 on a clean reconcile and non-zero when drift is found, so it is "
            "usable as a check."
        ),
        action_class="read_only",
        supports_json=True,
        related=("stats.cost", "stats.backfill-ledger"),
        args=(
            ArgDef("evidence_dir", "Path to the job evidence directory to reconcile"),
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="runtime.serve",
        group_id="runtime",
        subcommand="serve",
        description="Start the project dev server and leave it running.",
        action_class="write_metadata",
        supports_json=True,
        related=("runtime.probe", "runtime.stop"),
        args=(
            ArgDef("--repo", "Path to the project (defaults to the current directory)", required=False, is_option=True, default="."),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=True,
    ),
    CommandEntry(
        command_id="runtime.probe",
        group_id="runtime",
        subcommand="probe",
        description="One-shot readiness probe. Stops any server it started itself.",
        action_class="write_metadata",
        supports_json=True,
        related=("runtime.serve", "runtime.stop"),
        args=(
            ArgDef("--repo", "Path to the project (defaults to the current directory)", required=False, is_option=True, default="."),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=True,
    ),
    CommandEntry(
        command_id="runtime.stop",
        group_id="runtime",
        subcommand="stop",
        description="Stop the managed dev server and its whole process tree.",
        action_class="write_metadata",
        supports_json=True,
        related=("runtime.serve", "runtime.probe"),
        args=(
            ArgDef("--repo", "Path to the project (defaults to the current directory)", required=False, is_option=True, default="."),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=True,
    ),

    CommandEntry(
        command_id="job.evidence",
        group_id="job",
        subcommand="evidence",
        description="Export a self-contained evidence bundle for an entire job.",
        action_class="test_execution",
        supports_json=True,
        related=("job.run", "job.show"),
        args=(
            ArgDef("job_id", "Job ID"),
            ArgDef("--out", "Output directory for bundle files", required=False, is_option=True, default=""),
            ArgDef("--verification-command", "Explicit verification command to execute and record (repeatable). Each is run and stored as a verification run covering the test files it names", required=False, is_option=True),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=True,
    ),
    CommandEntry(
        command_id="job.apply",
        group_id="job",
        subcommand="apply",
        description="Review and apply job workspace changes to target repo. Dry-run by default; --approve applies.",
        action_class="write_metadata",
        supports_json=True,
        related=("job.run", "job.evidence"),
        args=(
            ArgDef("job_id", "Job ID"),
            ArgDef("--repo", "Path to target repository", required=False, is_option=True, default="."),
            ArgDef("--approve", "Apply changes (without this flag, dry-run only)", required=False, is_option=True, default="false"),
            ArgDef("--dry-run", "Preview only, no target mutation", required=False, is_option=True, default="false"),
            ArgDef("--test-command", "Post-apply test command", required=False, is_option=True, default=""),
            ArgDef("--skip-blocked", "Apply the non-blocked files and deliberately leave the protected ones not applied (they are named, never written)", required=False, is_option=True, is_flag=True),
            _JSON_OPT,
        ),
        may_mutate_repo=True,
        may_execute_commands=True,
    ),

    # ── self (self-dogfood planner — read/metadata-only) ──────────────────
    CommandEntry(
        command_id="self.inspect",
        group_id="self",
        subcommand="inspect",
        description="Read-only: inspect Remedy's own evidence for self-improvement items.",
        action_class="read_only",
        args=(
            ArgDef("--job-id", "Optional job to include in inspection", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("self.plan", "self.propose", "self.report"),
    ),
    CommandEntry(
        command_id="self.plan",
        group_id="self",
        subcommand="plan",
        description="Read-only: build a self-improvement plan (grouped items, top recommendations).",
        action_class="read_only",
        args=(
            ArgDef("--job-id", "Optional job to include in the plan", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("self.inspect", "self.propose"),
    ),
    CommandEntry(
        command_id="self.propose",
        group_id="self",
        subcommand="propose",
        description="Metadata-only: create ProposedTask(s) from self-improvement items (existing approval flow).",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--item-id", "Self-improvement item id to propose", required=False, is_option=True),
            ArgDef("--top", "Propose the top N items", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("self.inspect", "self.plan"),
    ),
    CommandEntry(
        command_id="self.execute",
        group_id="self",
        subcommand="execute",
        description="Metadata-only: start/resume a bounded self-improvement attempt (prepares a request; no apply).",
        action_class="write_metadata",
        args=(
            ArgDef("proposed_task_id", "Approved self-dogfood proposed task id"),
            ArgDef("--job-id", "Job that owns the proposed task", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("self.status", "self.reconcile"),
    ),
    CommandEntry(
        command_id="self.status",
        group_id="self",
        subcommand="status",
        description="Read-only: show self-improvement attempts and their state.",
        action_class="read_only",
        args=(
            ArgDef("--attempt-id", "Filter to one attempt", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("self.execute", "self.reconcile"),
    ),
    CommandEntry(
        command_id="self.reconcile",
        group_id="self",
        subcommand="reconcile",
        description="Metadata-only: refresh a self-improvement attempt from durable truth (no apply/provider).",
        action_class="write_metadata",
        args=(
            ArgDef("attempt_id", "Self-improvement attempt id"),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("self.status", "self.execute"),
    ),
    CommandEntry(
        command_id="self.integrity",
        group_id="self",
        subcommand="integrity",
        description="Read-only: self-dogfood integrity checks (no attempt on main, no completed-without-proof, no dup).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("self.status",),
    ),
    CommandEntry(
        command_id="self.report",
        group_id="self",
        subcommand="report",
        description="Read-only: self-dogfood report (what Remedy thinks is wrong + evidence).",
        action_class="read_only",
        args=(
            ArgDef("--job-id", "Optional job to include in the report", required=False, is_option=True),
            ArgDef("--markdown", "Render the report as markdown", required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("self.inspect", "self.plan"),
    ),

    # ── propose ─────────────────────────────────────────────────────────
    CommandEntry(
        command_id="propose.list",
        group_id="propose",
        subcommand="list",
        description="List proposed tasks for a job.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--status", "Filter by status", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="propose.show",
        group_id="propose",
        subcommand="show",
        description="Show a single proposed task.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("task_id", "Proposed task ID"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="propose.evaluate",
        group_id="propose",
        subcommand="evaluate",
        description="Run deterministic evaluation on proposed tasks.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--task-id", "Evaluate a specific task (default: all)", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="propose.approve",
        group_id="propose",
        subcommand="approve",
        description="Approve a proposed task for build.",
        action_class="approval_gate",
        args=(
            _JOB_ID,
            ArgDef("task_id", "Proposed task ID to approve"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="propose.reject",
        group_id="propose",
        subcommand="reject",
        description="Reject a proposed task.",
        action_class="approval_gate",
        args=(
            _JOB_ID,
            ArgDef("task_id", "Proposed task ID to reject"),
            _REASON_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="propose.defer",
        group_id="propose",
        subcommand="defer",
        description="Defer a proposed task.",
        action_class="approval_gate",
        args=(
            _JOB_ID,
            ArgDef("task_id", "Proposed task ID to defer"),
            _REASON_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
    ),

    CommandEntry(
        command_id="propose.materialize",
        group_id="propose",
        subcommand="materialize",
        description="Materialize approved proposed tasks into real build tasks.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--task-id", "Specific proposed task ID to materialize", required=False, is_option=True),
            ArgDef("--all", "Materialize all approved un-materialized tasks", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),

    # ── dev ──────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="dev.agent-loop",
        group_id="dev",
        subcommand="agent-loop",
        description="Run the agent loop for a job (dev/testing).",
        action_class="dev_helper",
        args=(_JOB_ID,),
        may_execute_commands=True,
    ),
    CommandEntry(
        command_id="dev.smoke-help",
        group_id="dev",
        subcommand="smoke-help",
        description="Show smoke test instructions.",
        action_class="dev_helper",
    ),
    CommandEntry(
        command_id="dev.status",
        group_id="dev",
        subcommand="status",
        description="Show developer status summary.",
        action_class="dev_helper",
        args=(
            ArgDef("--json", "Output JSON", required=False, is_option=True),
        ),
    ),

    # ── progress ────────────────────────────────────────────────────────

    # ── roadmap (F080: the roadmap mirror; hidden; proposes, never starts) ─
    CommandEntry(
        command_id="roadmap.status",
        group_id="roadmap",
        subcommand="status",
        description="Show the active roadmap feature, its blockers and its milestone.",
        action_class="read_only",
        args=(
            ArgDef("--repo", "Repository to mirror (default: this Remedy checkout)", required=False, is_option=True),
            ArgDef("--json", "Output as JSON", required=False, is_option=True),
        ),
        supports_json=True,
        related=("roadmap.next",),
    ),
    CommandEntry(
        command_id="roadmap.next",
        group_id="roadmap",
        subcommand="next",
        description="Propose the next roadmap feature and its file path. Starts nothing.",
        action_class="read_only",
        args=(
            ArgDef("--repo", "Repository to mirror (default: this Remedy checkout)", required=False, is_option=True),
            ArgDef("--json", "Output as JSON", required=False, is_option=True),
        ),
        supports_json=True,
        related=("roadmap.status",),
    ),

    # ── ci ─────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="ci.run",
        group_id="ci",
        subcommand="run",
        description="Run Remedy's own CI stages locally and print the summary.",
        action_class="test_execution",
        args=(
            ArgDef("--stage", "Run one stage by name instead of all of them", required=False, is_option=True),
            ArgDef("--json", "Output as JSON", required=False, is_option=True),
        ),
        supports_json=True,
        may_execute_commands=True,
    ),

    # ── integrity ───────────────────────────────────────────────────────
    CommandEntry(
        command_id="integrity.check",
        group_id="integrity",
        subcommand="check",
        description="Run pre-handoff integrity checks.",
        action_class="read_only",
        args=(
            ArgDef("--json", "Output as JSON", required=False, is_option=True),
            ArgDef("--collect-only", "Also run pytest collect-only", required=False, is_option=True, default="false"),
        ),
        supports_json=True,
    ),

    # ── snapshot ─────────────────────────────────────────────────────────
    CommandEntry(
        command_id="snapshot.inspect",
        group_id="snapshot",
        subcommand="inspect",
        description="Show snapshot metadata for a specific snapshot (safe fields only, no recovery content).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("snapshot_id", "Snapshot ID to inspect"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("snapshot.list-applies",),
    ),

    CommandEntry(
        command_id="snapshot.list-applies",
        group_id="snapshot",
        subcommand="list-applies",
        description="List durable apply records for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("snapshot.inspect",),
    ),

    # ── config ──────────────────────────────────────────────────────────
    CommandEntry(
        command_id="config.list",
        group_id="config",
        subcommand="list",
        description="List all config keys with current values and sources.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
    ),
    CommandEntry(
        command_id="config.show",
        group_id="config",
        subcommand="show",
        description="Show all config keys (alias for list).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("config.list",),
    ),
    CommandEntry(
        command_id="config.get",
        group_id="config",
        subcommand="get",
        description="Show value and source for one config key.",
        action_class="read_only",
        args=(
            ArgDef("key", "Config key (e.g. ollama.host)"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="config.sources",
        group_id="config",
        subcommand="sources",
        description="Show which config files are loaded and their paths.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
    ),
    CommandEntry(
        command_id="config.init",
        group_id="config",
        subcommand="init",
        description="Create a remedy.toml template in the current directory.",
        action_class="write_metadata",
        args=(
            ArgDef("--path", "Target file path (default: ./remedy.toml)", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="config.set",
        group_id="config",
        subcommand="set",
        description="Set a config key in ./remedy.toml.",
        action_class="write_metadata",
        args=(
            ArgDef("key", "Config key (e.g. ollama.host)"),
            ArgDef("value", "Value to set"),
            ArgDef("--path", "Target file path (default: ./remedy.toml)", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="config.validate",
        group_id="config",
        subcommand="validate",
        description="Validate loaded config against key specs.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
    ),

    # ── self-repair (self-repair proposals — metadata only) ──────────────
)


# ---------------------------------------------------------------------------
# List command shared option surface (F262 T001)
# ---------------------------------------------------------------------------

_LIST_SORT_ARG = ArgDef(
    "--sort", "Sort field; this command's own columns are the valid set (see --help)",
    required=False, is_option=True)
_LIST_DESC_ARG = ArgDef(
    "--desc", "Reverse the sort order",
    required=False, is_option=True, is_flag=True)
_LIST_SINCE_ARG = ArgDef(
    "--since",
    "Only rows at or after this time: an ISO-8601 timestamp, or a relative "
    "form such as 2d or 12h",
    required=False, is_option=True)
_LIST_UNTIL_ARG = ArgDef(
    "--until",
    "Only rows before this time: an ISO-8601 timestamp, or a relative form "
    "such as 2d or 12h",
    required=False, is_option=True)
_LIST_LIMIT_ARG = ArgDef(
    "--limit", "Max rows to return",
    required=False, is_option=True)

_LIST_OPTION_ARGS: tuple[ArgDef, ...] = (
    _LIST_SORT_ARG,
    _LIST_DESC_ARG,
    _LIST_SINCE_ARG,
    _LIST_UNTIL_ARG,
    _LIST_LIMIT_ARG,
)


def _is_list_command(entry: CommandEntry) -> bool:
    """True for a catalog entry whose subcommand is list-shaped (F262 T001)."""
    return entry.subcommand == "list" or entry.subcommand.endswith("-list")


def _with_list_options(entry: CommandEntry) -> CommandEntry:
    """Attach the shared list-option surface to a list-shaped entry.

    Add-only-if-missing: a command that already declares one of these flags
    by name (today only `event.list`, which already has `--since` and
    `--limit`) keeps its own existing ArgDef for that name untouched and
    only gains the flags it is missing. Appending a second ArgDef of an
    already-present name crashes argparse at parser-build time with a
    conflicting-option error (verified against `grouped.build_parser()`).
    """
    if not _is_list_command(entry):
        return entry
    existing = {a.name for a in entry.args}
    missing = tuple(a for a in _LIST_OPTION_ARGS if a.name not in existing)
    if not missing:
        return entry
    return replace(entry, args=(*entry.args, *missing))


CATALOG: tuple[CommandEntry, ...] = tuple(_with_list_options(c) for c in _BASE_CATALOG)


# The whole surface of the UI write door: no other `command_id` above is
# reachable from a browser, and plan approval arrives here as `decision.resolve`
# carrying an `fp:`-prefixed decision id rather than as a command of its own
# (DECISION F009 D4).
UI_EXPOSED_COMMANDS: frozenset[str] = frozenset({
    "job.stop",
    "decision.resolve",
    "patch.approve-hunks",
})


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------


def resolve_group(word: str) -> str | None:
    """Return the id of the group a typed word names, by its id or an alias, or None."""
    if word in GROUPS:
        return word
    return next((g.id for g in GROUPS.values() if word in g.aliases), None)


def get_group(group_id: str) -> GroupDef:
    """Return group definition by id or alias, or raise KeyError."""
    resolved = resolve_group(group_id)
    if resolved is None:
        raise KeyError(group_id)
    return GROUPS[resolved]


def get_command(command_id: str) -> CommandEntry:
    """Return command entry by command_id or raise KeyError."""
    for cmd in CATALOG:
        if cmd.command_id == command_id:
            return cmd
    raise KeyError(command_id)


def get_commands_for_group(group_id: str) -> list[CommandEntry]:
    """Return all commands belonging to a group, named by its id or an alias."""
    group_id = resolve_group(group_id) or group_id
    return [cmd for cmd in CATALOG if cmd.group_id == group_id]
