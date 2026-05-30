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
    get_group(group_id) -> GroupDef
    get_command(command_id) -> CommandEntry
    get_commands_for_group(group_id) -> list[CommandEntry]
"""

from __future__ import annotations

from dataclasses import dataclass
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
]


@dataclass(frozen=True)
class GroupDef:
    """A top-level command group (e.g. 'job', 'brain')."""

    id: str
    label: str
    description: str


@dataclass(frozen=True)
class ArgDef:
    """A single CLI argument or option."""

    name: str
    help: str
    required: bool = True
    is_option: bool = False
    default: str | None = None


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
    related: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------

GROUPS: dict[str, GroupDef] = {
    "job": GroupDef("job", "Job", "Create, inspect, and manage jobs."),
    "project": GroupDef("project", "Project", "Create, inspect, and manage projects."),
    "patch": GroupDef("patch", "Patch", "Review and apply patch intents."),
    "test": GroupDef("test", "Test", "Discover and run project tests."),
    "brain": GroupDef("brain", "Brain", "Inspect the project brain graph."),
    "policy": GroupDef("policy", "Policy", "Inspect execution policies."),
    "worker": GroupDef("worker", "Worker", "List worker provider specs."),
    "memory": GroupDef("memory", "Memory", "Store and recall project memory."),
    "readiness": GroupDef("readiness", "Readiness", "Inspect autonomy readiness."),
    "context": GroupDef("context", "Context", "Context pack and coverage."),
    "change": GroupDef("change", "Change", "Review change sets (proof chain view)."),
    "file": GroupDef("file", "File", "File-level provenance and tracing."),
    "repo": GroupDef("repo", "Repo", "Read-only repository inspection."),
    "event": GroupDef("event", "Event", "Query the audit event ledger."),
    "blocker": GroupDef("blocker", "Blocker", "View and resolve stop reasons."),
    "decision": GroupDef("decision", "Decision", "Human decision queue."),
    "dashboard": GroupDef("dashboard", "Dashboard", "Project and job dashboards."),
    "guide": GroupDef("guide", "Guide", "Human guidance rail — next safe actions."),
    "ui": GroupDef("ui", "UI", "Localhost UI server — primary interactive experience."),
    "do": GroupDef("do", "Do", "High-level guided autorun — one command to start a Remedy run."),
    "review": GroupDef("review", "Review", "Reviewer recommendations — suggest, accept, reject follow-up tasks."),
    "dev": GroupDef("dev", "Dev", "Developer utilities."),
}


# ---------------------------------------------------------------------------
# Argument shorthands
# ---------------------------------------------------------------------------

_JOB_ID = ArgDef("job_id", "UUID of the job")
_PROJECT_ID = ArgDef("project_id", "UUID or name of the project")
_INTENT_ID = ArgDef("intent_id", "Intent ID (integer)")
_JSON_OPT = ArgDef("--json", "Output as JSON", required=False, is_option=True, default="false")
_REASON_OPT = ArgDef("--reason", "Reason text", required=False, is_option=True)


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

CATALOG: tuple[CommandEntry, ...] = (
    # ── job ──────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="job.create",
        group_id="job",
        subcommand="create",
        description="Create a new job from a prompt.",
        action_class="write_metadata",
        args=(
            ArgDef("prompt", "What the job should accomplish"),
            ArgDef("--project", "Project UUID to link", required=False, is_option=True),
            ArgDef("--task-type", "Task type override", required=False, is_option=True),
            ArgDef("--task-description", "Task description override", required=False, is_option=True),
        ),
        related=("job.show", "job.attach-repo"),
    ),
    CommandEntry(
        command_id="job.list",
        group_id="job",
        subcommand="list",
        description="List all jobs.",
        action_class="read_only",
    ),
    CommandEntry(
        command_id="job.show",
        group_id="job",
        subcommand="show",
        description="Show job details (always JSON).",
        action_class="read_only",
        args=(_JOB_ID,),
        supports_json=False,
        related=("job.list", "brain.graph"),
    ),
    CommandEntry(
        command_id="job.attach-repo",
        group_id="job",
        subcommand="attach-repo",
        description="Attach a repository path to a job.",
        action_class="write_metadata",
        args=(_JOB_ID, ArgDef("repo_path", "Path to the repository")),
        related=("job.create",),
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
        related=("job.permissions",),
    ),
    CommandEntry(
        command_id="job.permissions",
        group_id="job",
        subcommand="permissions",
        description="Show current permissions for a job.",
        action_class="read_only",
        args=(_JOB_ID,),
        related=("job.permit",),
    ),
    CommandEntry(
        command_id="job.run-next",
        group_id="job",
        subcommand="run-next",
        description="Run the next pending task for a job.",
        action_class="write_metadata",
        args=(_JOB_ID,),
        may_execute_commands=True,
        related=("job.show", "test.run"),
    ),

    CommandEntry(
        command_id="job.plan",
        group_id="job",
        subcommand="plan",
        description="Plan tasks for a job using local LLM.",
        action_class="write_metadata",
        args=(_JOB_ID,),
        related=("job.create", "job.run-next"),
    ),
    CommandEntry(
        command_id="job.run-loop",
        group_id="job",
        subcommand="run-loop",
        description="Run the contract-gated autonomy loop for a job.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--max-cycles", "Maximum cycles (default: 3)", required=False, is_option=True, default="3"),
            ArgDef("--autonomy-level", "Autonomy level 0-6 (default: 1)", required=False, is_option=True, default="1"),
            ArgDef("--auto-approve-low-risk", "Auto-approve low-risk intents", required=False, is_option=True, default="false"),
            ArgDef("--no-tests", "Skip test runs", required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_execute_commands=True,
        requires_permission=True,
        related=("job.run-next", "job.plan"),
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

    # ── patch ────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="patch.list",
        group_id="patch",
        subcommand="list",
        description="List patch intents for a job.",
        action_class="read_only",
        args=(_JOB_ID,),
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
        args=(_JOB_ID, _INTENT_ID, _JSON_OPT),
        supports_json=True,
        may_mutate_repo=True,
        related=("patch.apply",),
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
        description="Run discovered tests for a job.",
        action_class="test_execution",
        args=(_JOB_ID,),
        may_execute_commands=True,
        requires_permission=True,
        related=("test.discover",),
    ),

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

    # ── policy ───────────────────────────────────────────────────────────
    CommandEntry(
        command_id="policy.contract",
        group_id="policy",
        subcommand="contract",
        description="Show the run contract for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("policy.token",),
    ),
    CommandEntry(
        command_id="policy.token",
        group_id="policy",
        subcommand="token",
        description="Show the token routing policy for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("policy.contract", "policy.token-explain"),
    ),
    CommandEntry(
        command_id="policy.token-explain",
        group_id="policy",
        subcommand="token-explain",
        description="Explain the token economy policy (text only).",
        action_class="read_only",
        args=(),
        supports_json=False,
        related=("policy.token",),
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
        command_id="worker.recommend",
        group_id="worker",
        subcommand="recommend",
        description="Recommend a worker for a job (local-first, no execution).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("worker.list", "policy.token"),
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
        command_id="worker.explain",
        group_id="worker",
        subcommand="explain",
        description="Explain worker recommendation scoring for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("worker.recommend", "policy.token"),
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

    # ── readiness ────────────────────────────────────────────────────────
    CommandEntry(
        command_id="readiness.job",
        group_id="readiness",
        subcommand="job",
        description="Assess autonomy readiness for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("brain.graph", "policy.contract"),
    ),
    CommandEntry(
        command_id="readiness.project",
        group_id="readiness",
        subcommand="project",
        description="Assess autonomy readiness for a project.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
    ),

    # ── context ──────────────────────────────────────────────────────────
    CommandEntry(
        command_id="context.pack",
        group_id="context",
        subcommand="pack",
        description="Build a token-budget-aware context pack.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--budget", "Max tokens (default: 2000)", required=False, is_option=True, default="2000"),
            ArgDef("--mode", "Pack mode: caveman, compact, or standard (default: compact)", required=False, is_option=True, default="compact"),
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

    # ── repo ────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="repo.status",
        group_id="repo",
        subcommand="status",
        description="Show read-only git status of job's target repository.",
        action_class="read_only",
        args=(
            ArgDef("job_id", "Job UUID (reads target_repo from job)", required=False, default=None),
            ArgDef("--path", "Explicit path (dev override, default: job target_repo or cwd)", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("readiness.show",),
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

    # ── dashboard ──────────────────────────────────────────────────────
    CommandEntry(
        command_id="dashboard.job",
        group_id="dashboard",
        subcommand="job",
        description="Show the job dashboard overview.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
    ),
    CommandEntry(
        command_id="dashboard.project",
        group_id="dashboard",
        subcommand="project",
        description="Show the project dashboard overview.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
    ),

    # ── context (additional) ──────────────────────────────────────────
    CommandEntry(
        command_id="context.explain",
        group_id="context",
        subcommand="explain",
        description="Explain what a context pack contains and why.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--mode", "Pack mode: caveman, compact, or standard", required=False, is_option=True, default="compact"),
            ArgDef("--budget", "Token budget (default: 2000)", required=False, is_option=True, default="2000"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="context.optimize",
        group_id="context",
        subcommand="optimize",
        description="Recommend optimal context configuration for a budget.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--budget", "Token budget (default: 2000)", required=False, is_option=True, default="2000"),
            _JSON_OPT,
        ),
        supports_json=True,
    ),

    # ── guide ─────────────────────────────────────────────────────────
    CommandEntry(
        command_id="guide.job",
        group_id="guide",
        subcommand="job",
        description="Show human guidance rail for a job — next safe actions.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("readiness.job", "decision.list", "dashboard.job"),
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
            ArgDef("--open", "Open browser (default: false)", required=False, is_option=True, default="false"),
            ArgDef("--info-file", "Write server info JSON to this path", required=False, is_option=True),
        ),
        related=("brain.view", "dashboard.job"),
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
        action_class="apply_write",
        args=(
            ArgDef("goal", "The goal to accomplish", required=True),
            ArgDef("--repo", "Path to target repository", required=False, is_option=True, default="."),
            ArgDef("--project", "Project ID to use or create", required=False, is_option=True),
            ArgDef("--autonomy-level", "Autonomy level 0-7 (default: 2)", required=False, is_option=True, default="2"),
            ArgDef("--max-cycles", "Maximum cycles (default: 3)", required=False, is_option=True, default="3"),
            ArgDef("--ui", "Start UI alongside run (default: false)", required=False, is_option=True, default="false"),
            ArgDef("--dry-run", "Show plan without executing", required=False, is_option=True, default="false"),
            ArgDef("--json", "Output JSON", required=False, is_option=True, default="false"),
            ArgDef("--fixture-builder", "Use fixture builder for testing", required=False, is_option=True, default="false"),
        ),
        may_mutate_repo=True,
        may_execute_commands=True,
    ),

    # ── review ───────────────────────────────────────────────────────────
    CommandEntry(
        command_id="review.run",
        group_id="review",
        subcommand="run",
        description="Run reviewer to suggest follow-up tasks.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--after-task", "Task ID to review after", required=False, is_option=True),
            ArgDef("--json", "Output JSON", required=False, is_option=True),
        ),
    ),
    CommandEntry(
        command_id="review.list",
        group_id="review",
        subcommand="list",
        description="List reviewer recommendations for a job.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--json", "Output JSON", required=False, is_option=True),
        ),
    ),
    CommandEntry(
        command_id="review.accept",
        group_id="review",
        subcommand="accept",
        description="Accept a reviewer recommendation (append as task).",
        action_class="apply_write",
        args=(
            _JOB_ID,
            ArgDef("recommendation_id", "Recommendation ID to accept", required=True),
        ),
    ),
    CommandEntry(
        command_id="review.reject",
        group_id="review",
        subcommand="reject",
        description="Reject a reviewer recommendation.",
        action_class="apply_write",
        args=(
            _JOB_ID,
            ArgDef("recommendation_id", "Recommendation ID to reject", required=True),
        ),
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
)


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------


def get_group(group_id: str) -> GroupDef:
    """Return group definition or raise KeyError."""
    return GROUPS[group_id]


def get_command(command_id: str) -> CommandEntry:
    """Return command entry by command_id or raise KeyError."""
    for cmd in CATALOG:
        if cmd.command_id == command_id:
            return cmd
    raise KeyError(command_id)


def get_commands_for_group(group_id: str) -> list[CommandEntry]:
    """Return all commands belonging to a group."""
    return [cmd for cmd in CATALOG if cmd.group_id == group_id]
