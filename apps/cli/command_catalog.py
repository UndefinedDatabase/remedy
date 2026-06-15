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
    "repo": GroupDef("repo", "Repo", "Read-only repository inspection (commit-readiness does not commit)."),
    "event": GroupDef("event", "Event", "Query the audit event ledger."),
    "blocker": GroupDef("blocker", "Blocker", "View and resolve stop reasons."),
    "decision": GroupDef("decision", "Decision", "Human decision queue."),
    "dashboard": GroupDef("dashboard", "Dashboard", "Project and job dashboards."),
    "guide": GroupDef("guide", "Guide", "Human guidance rail — next safe actions."),
    "ui": GroupDef("ui", "UI", "Localhost UI server — primary interactive experience."),
    "do": GroupDef("do", "Do", "High-level guided autorun — one command to start a Remedy run."),
    "repair": GroupDef("repair", "Repair", "Test failure repair — structured failure evidence and fix tasks."),
    "overnight": GroupDef("overnight", "Overnight", "Bounded overnight preparation — read-only readiness, plan, morning report."),
    "provider": GroupDef("provider", "Provider", "Provider Trust Gate — quarantine + validate UNTRUSTED external model output (no provider execution)."),
    "self": GroupDef("self", "Self", "Self-dogfood — inspect Remedy's own evidence and propose self-improvement tasks (read/metadata-only)."),
    "orchestrator": GroupDef("orchestrator", "Orchestrator", "Main orchestrator brain — evidence-backed next-step decisions (read/metadata-only; no execution)."),
    "local-advisor": GroupDef("local-advisor", "Local Advisor", "Optional local-model advisory critique (loopback-only Ollama; disabled by default; advisory-only, never executes)."),
    "review": GroupDef("review", "Review", "Reviewer recommendations — suggest, accept, reject follow-up tasks."),
    "propose": GroupDef("propose", "Propose", "Proposed task evaluation — list, evaluate, approve, reject, defer."),
    "dev": GroupDef("dev", "Dev", "Developer utilities."),
    "integrity": GroupDef("integrity", "Integrity", "Pre-handoff integrity checks."),
    "contract": GroupDef("contract", "Contract", "Run contract inspection and action checks."),
    "progress": GroupDef("progress", "Progress", "Progress ledger — structured checklist and evidence."),
    "feature": GroupDef("feature", "Feature", "Feature planner — deterministic suggestions and acceptance."),
    "snapshot": GroupDef("snapshot", "Snapshot", "Repository snapshot and rollback — pre-apply proof and recovery metadata."),
}


# ---------------------------------------------------------------------------
# Argument shorthands
# ---------------------------------------------------------------------------

_JOB_ID = ArgDef("job_id", "UUID of the job")
_PROJECT_ID = ArgDef("project_id", "UUID or name of the project")
_INTENT_ID = ArgDef("intent_id", "Intent ID (integer)")
_JSON_OPT = ArgDef("--json", "Output as JSON", required=False, is_option=True, default="false")
_REASON_OPT = ArgDef("--reason", "Reason text", required=False, is_option=True)
_APPLY_ID_OPT = ArgDef("--apply-id", "Explicit apply_id (overrides intent_id lookup)", required=False, is_option=True)


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

    CommandEntry(
        command_id="job.summary",
        group_id="job",
        subcommand="summary",
        description="Print an honest summary of job state (truth contract).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
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
        args=(_JOB_ID, _INTENT_ID, _APPLY_ID_OPT, _JSON_OPT),
        supports_json=True,
        may_mutate_repo=True,
        requires_permission=True,
        related=("patch.apply", "snapshot.list-applies"),
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
        command_id="worker.run",
        group_id="worker",
        subcommand="run",
        description="Run local worker (one job or bounded loop).",
        action_class="local_state_change",
        args=(
            ArgDef("--once", "Process one job and stop", required=False, is_option=True),
            ArgDef("--max-jobs", "Max jobs to process", required=False, is_option=True, default="1"),
            ArgDef("--max-seconds", "Max seconds to run", required=False, is_option=True, default="60"),
            ArgDef("--max-steps", "Max task execution steps (0=no budget)", required=False, is_option=True, default="1"),
            ArgDef("--max-tokens", "Max token budget (0=unlimited)", required=False, is_option=True, default="0"),
            ArgDef("--max-runtime-seconds", "Max runtime seconds for execution", required=False, is_option=True, default="60"),
            ArgDef("--provider", "Builder provider (none|fixture|ollama)", required=False, is_option=True, default="none"),
            ArgDef("--job", "Specific job ID", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("worker.status", "job.enqueue"),
    ),
    CommandEntry(
        command_id="worker.status",
        group_id="worker",
        subcommand="status",
        description="Show current worker status.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("worker.run",),
    ),
    CommandEntry(
        command_id="job.enqueue",
        group_id="job",
        subcommand="enqueue",
        description="Add a job to the local work queue.",
        action_class="local_state_change",
        args=(_JOB_ID,),
        related=("worker.run", "job.pause"),
    ),
    CommandEntry(
        command_id="job.pause",
        group_id="job",
        subcommand="pause",
        description="Pause a queued or running job.",
        action_class="local_state_change",
        args=(_JOB_ID,),
        related=("job.enqueue", "job.cancel"),
    ),
    CommandEntry(
        command_id="job.cancel",
        group_id="job",
        subcommand="cancel",
        description="Cancel a queued or running job.",
        action_class="local_state_change",
        args=(_JOB_ID,),
        related=("job.pause", "job.enqueue"),
    ),

    CommandEntry(
        command_id="job.resume-queue",
        group_id="job",
        subcommand="resume-queue",
        description="Resume a paused job back into the queue.",
        action_class="local_state_change",
        args=(_JOB_ID,),
        related=("job.pause", "job.enqueue"),
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
        command_id="context.inspect",
        group_id="context",
        subcommand="inspect",
        description="Inspect what a worker will see — paths, budget, policy gates.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("task_id", "Task UUID (optional, narrows inspection)", required=False, default=None),
            ArgDef("--budget", "Token budget (default: 4000)", required=False, is_option=True, default="4000"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("context.pack", "context.explain"),
    ),
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

    CommandEntry(
        command_id="repo.commit-readiness",
        group_id="repo",
        subcommand="commit-readiness",
        description="Preview commit readiness — read-only, no git writes.",
        action_class="read_only",
        args=(
            _JOB_ID,
            _JSON_OPT,
        ),
        supports_json=True,
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
        description="Resume a job from a safe checkpoint.",
        action_class="apply_write",
        args=(
            _JOB_ID,
            ArgDef("--checkpoint", "Checkpoint ID to resume from", required=True, is_option=True),
            ArgDef("--dry-run", "Preview resume without executing", required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=True,
        may_execute_commands=True,
        requires_permission=True,
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
            ArgDef("--no-open", "Do not open browser automatically", required=False, is_option=True, default="false"),
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
        action_class="write_metadata",
        supports_json=True,
        related=("job.show", "context.inspect", "change.proof"),
        args=(
            ArgDef("goal", "The goal to accomplish", required=True),
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
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="do.continue",
        group_id="do",
        subcommand="continue",
        description="Run one controlled continuation cycle for an approved intent.",
        action_class="apply_write",
        supports_json=True,
        related=("change.proof", "repair.start", "snapshot.inspect"),
        args=(
            _JOB_ID,
            ArgDef("--intent-id", "Approved intent ID (required when several are approved)",
                   required=False, is_option=True),
            _JSON_OPT,
        ),
        may_mutate_repo=True,
        may_execute_commands=True,
    ),

    # ── repair ──────────────────────────────────────────────────────────
    CommandEntry(
        command_id="repair.start",
        group_id="repair",
        subcommand="start",
        description="Start repair loop v0 for a test failure.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("failure_artifact_id", "Failure artifact ID"),
            ArgDef("--fixture-patch-intent", "Create fixture patch intent", required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("repair.failure-show", "job.show"),
    ),
    CommandEntry(
        command_id="repair.failure-show",
        group_id="repair",
        subcommand="failure-show",
        description="Show a test failure artifact.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("failure_artifact_id", "Failure artifact ID"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("repair.start",),
    ),
    CommandEntry(
        command_id="repair.propose",
        group_id="repair",
        subcommand="propose",
        description="Propose a bounded, approval-gated repair for a test failure (v1).",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("failure_artifact_id", "Failure artifact ID"),
            ArgDef("--fixture-builder", "Use the deterministic fixture repair builder",
                   required=False, is_option=True, default="false"),
            ArgDef("--fixture-source-builder", "Opt-in deterministic SOURCE fixture repair (needs a safe target)",
                   required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("repair.status", "repair.failure-show", "patch.approve"),
    ),
    CommandEntry(
        command_id="repair.status",
        group_id="repair",
        subcommand="status",
        description="Show repair attempts and their approval state (read-only).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--failure-artifact-id", "Filter to one failure artifact",
                   required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("repair.propose", "repair.failure-show"),
    ),
    CommandEntry(
        command_id="repair.request",
        group_id="repair",
        subcommand="request",
        description="Build a safe, provider-agnostic repair request package for an external actor (no execution).",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--failure-artifact-id", "Failure artifact to build a request for",
                   required=False, is_option=True),
            ArgDef("--target", "Target template label (external|docs_only|test_failure|markdown_only)",
                   required=False, is_option=True, default="external"),
            ArgDef("--model", "Optional non-binding model/worker hint", required=False, is_option=True),
            ArgDef("--new", "Force a fresh request package (else idempotent)",
                   required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("repair.request-show", "provider.intake-repair"),
    ),
    CommandEntry(
        command_id="repair.request-show",
        group_id="repair",
        subcommand="request-show",
        description="Read-only: show a repair request package (safe metadata; no raw content).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("request_package_id", "Repair request package id"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("repair.request", "provider.intake-repair"),
    ),

    # ── overnight (read-only preparation) ─────────────────────────────────
    CommandEntry(
        command_id="overnight.readiness",
        group_id="overnight",
        subcommand="readiness",
        description="Read-only: is this job safe to run unattended? (Bounded Overnight Prep v0)",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("overnight.plan", "overnight.report"),
    ),
    CommandEntry(
        command_id="overnight.plan",
        group_id="overnight",
        subcommand="plan",
        description="Read-only dry-run: what Remedy would do in one bounded cycle.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("overnight.readiness", "overnight.report"),
    ),
    CommandEntry(
        command_id="overnight.report",
        group_id="overnight",
        subcommand="report",
        description="Read-only morning-style report from current job evidence.",
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
        related=("overnight.readiness", "overnight.plan"),
    ),
    CommandEntry(
        command_id="overnight.run",
        group_id="overnight",
        subcommand="run",
        description="Foreground: perform AT MOST ONE bounded reviewable step (report-only by default).",
        action_class="apply_write",
        args=(
            _JOB_ID,
            ArgDef("--allow-one-cycle",
                   "Explicitly permit ONE bounded execution cycle (else report-only)",
                   required=False, is_option=True, default="false"),
            ArgDef("--allow-apply",
                   "Permit applying an approved intent via do continue (needs --allow-one-cycle)",
                   required=False, is_option=True, default="false"),
            ArgDef("--allow-repair-propose",
                   "Permit proposing a repair for an existing failure (needs --allow-one-cycle)",
                   required=False, is_option=True, default="false"),
            ArgDef("--allow-repair-apply",
                   "Permit applying an approved repair via do continue (needs --allow-one-cycle)",
                   required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        requires_permission=True,
        may_mutate_repo=True,
        may_execute_commands=True,
        related=("overnight.readiness", "overnight.plan", "overnight.report"),
    ),

    # ── provider (trust gate — intake UNTRUSTED external output) ──────────
    CommandEntry(
        command_id="provider.intake-repair",
        group_id="provider",
        subcommand="intake-repair",
        description="Quarantine + trust-validate an external repair candidate; create a pending intent only if accepted.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--input", "Path to a local file with the candidate repair", required=False, is_option=True),
            ArgDef("--stdin", "Read the candidate repair from stdin", required=False, is_option=True, default="false"),
            ArgDef("--failure-artifact-id", "Failure artifact this repair targets", required=False, is_option=True),
            ArgDef("--provider", "Provider name (e.g. claude, fable, ollama)", required=False, is_option=True, default="unknown"),
            ArgDef("--model", "Model name", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        requires_permission=False,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("provider.trust-show", "patch.approve", "repair.propose"),
    ),
    CommandEntry(
        command_id="provider.trust-show",
        group_id="provider",
        subcommand="trust-show",
        description="Read-only: show a ProviderTrustReport (safe findings/IDs; no raw output).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("trust_report_id", "Trust report id"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("provider.intake-repair",),
    ),
    CommandEntry(
        command_id="provider.material-show",
        group_id="provider",
        subcommand="material-show",
        description="Read-only: show provider patch material status + verification (no raw diff).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("material_id", "Provider patch material id"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("provider.intake-repair", "provider.trust-show", "patch.approve"),
    ),
    CommandEntry(
        command_id="provider.verify",
        group_id="provider",
        subcommand="verify",
        description="Second-stage SAFE verification of a quarantined candidate (relevance/overclaim/scope/loop). Metadata-only; never applies/approves.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("trust_report_id", "Trust report id to verify"),
            ArgDef("--request-package-id", "Repair request package to check consistency against", required=False, is_option=True),
            ArgDef("--self-attempt-id", "Self-improvement attempt this candidate targets", required=False, is_option=True),
            ArgDef("--new", "Force a fresh verification (ignore idempotent reuse)", required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        requires_permission=False,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("provider.verification-show", "provider.trust-show", "patch.approve"),
    ),
    CommandEntry(
        command_id="provider.verification-show",
        group_id="provider",
        subcommand="verification-show",
        description="Read-only: show a ProviderVerificationReport (safe findings/score/refs; no raw candidate/diff).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("verification_id", "Verification report id"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("provider.verify", "provider.trust-show"),
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
        related=("self.status", "self.reconcile", "provider.intake-repair"),
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

    # ── orchestrator (main brain — read/metadata-only) ────────────────────
    CommandEntry(
        command_id="orchestrator.inspect",
        group_id="orchestrator",
        subcommand="inspect",
        description="Read-only: build the orchestrator situation (options/risks/loop guard/routing).",
        action_class="read_only",
        args=(ArgDef("--job-id", "Optional job to include", required=False, is_option=True), _JSON_OPT),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("orchestrator.decide", "orchestrator.report"),
    ),
    CommandEntry(
        command_id="orchestrator.decide",
        group_id="orchestrator",
        subcommand="decide",
        description="Decide the single safest next action (read/metadata-only decision trace).",
        action_class="write_metadata",
        args=(
            ArgDef("--job-id", "Optional job to include", required=False, is_option=True),
            ArgDef("--use-local-advisor", "Optionally consult a local advisor (advisory-only)",
                   required=False, is_option=True, default="false"),
            ArgDef("--new", "Force a fresh advisor run (ignore idempotent reuse)",
                   required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("orchestrator.inspect", "orchestrator.report", "local-advisor.run"),
    ),
    CommandEntry(
        command_id="orchestrator.report",
        group_id="orchestrator",
        subcommand="report",
        description="Read-only: orchestrator report (situation, best next action, why-not, routing).",
        action_class="read_only",
        args=(
            ArgDef("--job-id", "Optional job to include", required=False, is_option=True),
            ArgDef("--markdown", "Render as markdown", required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("orchestrator.inspect", "orchestrator.decide"),
    ),
    CommandEntry(
        command_id="orchestrator.idea",
        group_id="orchestrator",
        subcommand="idea",
        description="Metadata-only: capture a user idea as a safe, classified roadmap hint.",
        action_class="write_metadata",
        args=(ArgDef("text", "Idea text"), _JSON_OPT),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("orchestrator.inspect",),
    ),

    # ── local-advisor (optional loopback advisory — disabled by default) ───
    CommandEntry(
        command_id="local-advisor.status",
        group_id="local-advisor",
        subcommand="status",
        description="Read-only: local advisor enabled/availability (loopback only; no secrets).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("local-advisor.run", "orchestrator.decide"),
    ),
    CommandEntry(
        command_id="local-advisor.run",
        group_id="local-advisor",
        subcommand="run",
        description="Metadata-only: advise on the latest orchestrator decision (advisory critique only).",
        action_class="write_metadata",
        args=(
            ArgDef("--job-id", "Optional job to scope the decision", required=False, is_option=True),
            ArgDef("--new", "Force a fresh advisor run (ignore idempotent reuse)",
                   required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True, may_mutate_repo=False, may_execute_commands=False,
        related=("local-advisor.status", "orchestrator.decide"),
    ),

    # ── review ───────────────────────────────────────────────────────────
    CommandEntry(
        command_id="review.bundle",
        group_id="review",
        subcommand="bundle",
        description="Generate a safe review bundle zip for a job.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--output", "Output zip path (default: .data/review_bundles/)", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("review.run", "job.summary"),
    ),
    CommandEntry(
        command_id="review.run",
        group_id="review",
        subcommand="run",
        description="Run reviewer to suggest follow-up tasks (human approval required).",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--after-task", "Task ID to review after", required=False, is_option=True),
            ArgDef("--fixture-reviewer", "Use deterministic fixture reviewer", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="review.list",
        group_id="review",
        subcommand="list",
        description="List reviewer recommendations for a job.",
        action_class="read_only",
        args=(
            _JOB_ID,
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="review.accept",
        group_id="review",
        subcommand="accept",
        description="Accept a reviewer recommendation (append as pending task).",
        action_class="approval_gate",
        args=(
            _JOB_ID,
            ArgDef("recommendation_id", "Recommendation ID to accept", required=True),
            _JSON_OPT,
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="review.reject",
        group_id="review",
        subcommand="reject",
        description="Reject a reviewer recommendation.",
        action_class="approval_gate",
        args=(
            _JOB_ID,
            ArgDef("recommendation_id", "Recommendation ID to reject", required=True),
            _JSON_OPT,
        ),
        supports_json=True,
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
    CommandEntry(
        command_id="progress.checklist",
        group_id="progress",
        subcommand="checklist",
        description="Show structured progress checklist with evidence.",
        action_class="read_only",
        args=(
            ArgDef("job_id", "Job UUID (omit for agent mode)", required=False, default=""),
            ArgDef("--agent", "Use .agent/ files instead of job", required=False, is_option=True, default="false"),
            ArgDef("--json", "Output as JSON", required=False, is_option=True),
        ),
        supports_json=True,
    ),

    # ── feature ─────────────────────────────────────────────────────────
    CommandEntry(
        command_id="feature.plan",
        group_id="feature",
        subcommand="plan",
        description="Show deterministic feature suggestions.",
        action_class="read_only",
        args=(
            ArgDef("job_id", "Job UUID (omit for agent mode)", required=False, default=""),
            ArgDef("--agent", "Use .agent/ files instead of job", required=False, is_option=True, default="false"),
            ArgDef("--json", "Output as JSON", required=False, is_option=True),
        ),
        supports_json=True,
    ),
    CommandEntry(
        command_id="feature.accept",
        group_id="feature",
        subcommand="accept",
        description="Accept a feature suggestion — creates ProposedTask.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("suggestion_id", "Suggestion ID to accept"),
            ArgDef("--json", "Output as JSON", required=False, is_option=True),
        ),
        supports_json=True,
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

    # ── contract ───────────────────────────────────────────────────────
    CommandEntry(
        command_id="contract.inspect",
        group_id="contract",
        subcommand="inspect",
        description="Show the run contract for a job.",
        action_class="read_only",
        args=(
            _JOB_ID,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("contract.check", "policy.contract"),
    ),
    CommandEntry(
        command_id="contract.check",
        group_id="contract",
        subcommand="check",
        description="Check whether an action is allowed by the run contract.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("action", "Action to check (e.g. apply, plan, build_artifact)"),
            ArgDef("--path", "File path to check against path policy", required=False, is_option=True),
            ArgDef("--risk", "Risk level to check (unknown, medium, high)", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("contract.inspect",),
    ),
    CommandEntry(
        command_id="contract.set",
        group_id="contract",
        subcommand="set",
        description="Set a contract field on a job.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("field", "Field to set (e.g. max_loops, stop_before_apply)"),
            ArgDef("value", "New value"),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("contract.inspect",),
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
