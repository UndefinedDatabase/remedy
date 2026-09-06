"""Job Task Runner — sequential multi-task execution with review/repair gates.

Parses a Markdown job file into ordered tasks, executes each through the
existing ping-pong loop (Builder → tests → Reviewer → repair), and applies
passed results into an isolated job workspace. The real target repo is never
mutated.

Public API:
    parse_job_file(text, repo_path) -> JobPlan
    plan_job_from_file(job_file_path, repo_path) -> JobPlan
    run_job(job_id, ...) -> JobPlan
    export_job_report(job) -> dict
    format_job_report_text(job) -> str
    load_job_plan(job_id) -> JobPlan | None
"""

from __future__ import annotations

import hashlib
import json as _json
import os
import re
import shutil
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

# F260 D2: one minting function per KIND of id. This module names JOBs and
# EPISODEs, so it mints through data_paths rather than spelling uuid4 inline.
# Module-level and not function-scoped: JobPlan's default_factory below is read
# when the class body runs, which a local import could never reach.
from packages.orchestration.data_paths import mint_episode_id, mint_job_id

if TYPE_CHECKING:
    from packages.orchestration.schemas.models import PlannedTask

# ---------------------------------------------------------------------------
# Task / Job state enums (string constants for JSON safety)
# ---------------------------------------------------------------------------

TASK_PENDING = "pending"
TASK_RUNNING = "running"
TASK_PASSED = "passed"
TASK_APPLIED = "applied_to_job_workspace"
TASK_BLOCKED = "blocked"
TASK_FAILED = "failed"
TASK_SKIPPED = "skipped"
# F112 T003b2b2b2: a task that never dispatched because its declared scope
# could not fit its class cap and was replaced by split_one_task's children
# instead (DECISION F112 D7/D8) — distinct from TASK_SKIPPED, which means
# "the job blocked and this never got a chance."
TASK_SPLIT = "split"

# F112 T003b1: every TaskEntry's model-routing class, honestly defaulted rather
# than inferred from title text (DECISION F112 D2) — the seeded
# model_routing.TASK_CLASS_TIERS key F016's own build/repair tasks already are.
TASK_CLASS_DEFAULT = "standard_build"

JOB_PLANNED = "planned"
JOB_RUNNING = "running"
JOB_BLOCKED = "blocked"
JOB_COMPLETED = "completed"
JOB_PAUSED = "paused"
#: F011. Additive and distinct: a STOPPED job was stopped ON PURPOSE at a safe point. It is
#: not `blocked` (nothing failed), not `paused` (nothing hit a task cap) and not a cancelled
#: queue item. It keeps its pending work and resumes at the first pending task.
JOB_STOPPED = "stopped"

# Token context policy constants
_PREVIOUS_SUMMARY_LIMIT = 5
_TASK_BODY_LIMIT = 2000

# Unsafe path patterns for workspace apply
_UNSAFE_EXTENSIONS = frozenset({".pem", ".key", ".p12", ".pfx", ".jks"})
_UNSAFE_PREFIXES = frozenset({".env", ".git"})
_UNSAFE_DIRS = frozenset({
    "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".tox", "dist", "build", ".eggs", "venv", ".venv",
})


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class AppliedFileProof:
    """Per-file baseline and final hash proof for promotion safety."""
    path: str = ""
    existed_before_job: bool = False
    baseline_sha256: str = ""
    final_workspace_sha256: str = ""
    task_id: str = ""
    run_id: str = ""
    # F006: the reviewed git file mode. Promotion must reproduce the whole
    # reviewed change, executable bit included — never just the bytes.
    baseline_mode: str = ""      # "" when the file did not exist before the job
    final_mode: str = ""         # "100644" | "100755"


@dataclass
class ApplyManifest:
    """Result of a strict workspace apply for one task."""
    task_id: str = ""
    run_id: str = ""
    applied_files: list[str] = field(default_factory=list)
    missing_files: list[str] = field(default_factory=list)
    unsupported_files: list[str] = field(default_factory=list)
    unexpected_files: list[str] = field(default_factory=list)
    duplicate_files: list[str] = field(default_factory=list)
    applied_file_proofs: list[AppliedFileProof] = field(default_factory=list)
    status: str = "pending"  # applied | blocked


@dataclass
class TaskProofSummary:
    """Bounded proof summary for a completed task."""
    task_id: str = ""
    title: str = ""
    run_id: str = ""
    final_status: str = ""
    applied_files: list[str] = field(default_factory=list)
    test_passed: bool | None = None
    reviewer_verdict: str = ""
    repair_rounds_used: int = 0
    repair_rounds_allowed: int = 0
    tokens_estimated: int = 0


@dataclass
class TaskEntry:
    """A single task within a job."""
    task_id: str = ""          # T001, T002, ... (by parse order)
    source_heading_number: int = 0  # Original ## Task N number
    title: str = ""
    task_class: str = TASK_CLASS_DEFAULT
    # F112 T003b2b1: durable per-task answers to escalated decisions this
    # task raised (e.g. a cannot_fit split-or-proceed choice) — keyed like
    # Core Job's Task.inputs so escalation.py's answer-recording path
    # (DECISION F112 D4) works unmodified against either task shape.
    inputs: dict = field(default_factory=dict)
    # F112 T003c: this task's declared fenced scope, parsed from a "Files:"
    # section in job markdown (mirrors "Acceptance:") — the
    # compiled_context_paths source T003b2b2's run_pingpong call needs
    # (DECISION F112 D5); empty when the job file declares none.
    files_hint: list = field(default_factory=list)
    body: str = ""
    acceptance: str = ""
    status: str = TASK_PENDING
    run_id: str = ""
    final_status: str = ""
    safe_diff_files: list[str] = field(default_factory=list)
    test_passed: bool | None = None
    reviewer_verdict: str = ""
    repair_rounds_used: int = 0
    repair_rounds_allowed: int = 0
    error: str = ""
    apply_manifest: ApplyManifest | None = None
    proof_summary: TaskProofSummary | None = None
    # F006 durable task checkpoint: the workspace tree BEFORE this task's first
    # provider call. Persisted so a crash cannot hide partial work: the resumed
    # attempt keeps reviewing and diffing against the ORIGINAL start tree.
    task_start_tree: str = ""
    task_start_tree_ref: str = ""     # checkpoint ref protecting that tree object
    task_start_recorded_at: str = ""
    task_attempt_state: str = ""      # "" | "active" | "complete"


# F112 T003b2a: translates a live TaskEntry into the granularity machinery's
# own PlannedTask so `task_granularity.split_one_task` (DECISION F112 D2) can
# run against a dispatched task without re-deciding its own band/acceptance
# trigger. `est_tokens_band` is fixed at "XL" (never read by `split_one_task`,
# which clusters on `acceptance`/`files_hint` alone — task_granularity.py:230)
# and is present only because `PlannedTask` requires a valid TokenBand.
def task_entry_to_planned_task(task: TaskEntry) -> PlannedTask | None:
    """Adapt one dispatched ``TaskEntry`` into a plan-time ``PlannedTask``.

    Returns None when ``task.acceptance`` holds no non-blank line: an empty
    acceptance list violates ``PlannedTask``'s own validator, and per
    T3_F112.md's edge case rule a split that cannot help drops the option
    rather than raising. ``acceptance`` otherwise splits ``task.acceptance``
    on newlines, dropping blank lines. ``files_hint`` carries whatever the
    job markdown declared (T3_F112.md T003c, ``TaskEntry.files_hint``) —
    empty when the file has no "Files:" section, in which case
    `_cluster_acceptance` degrades safely to one cluster per acceptance
    item (DECISION F112 D2 MEASURED — an empty hint is a safe, not a
    broken, input).
    """
    from packages.orchestration.schemas.models import PlannedTask

    lines = [line for line in task.acceptance.splitlines() if line.strip()]
    if not lines:
        return None
    return PlannedTask(
        id=task.task_id,
        title=task.title,
        goal=task.body or task.title,
        acceptance=lines,
        files_hint=list(task.files_hint),
        est_tokens_band="XL",
    )


# F112 T003b2b2b1: the reverse of task_entry_to_planned_task, above — turns
# one split_one_task (DECISION F112 D2) child PlannedTask back into a
# dispatchable TaskEntry. task_class and source_heading_number are not
# PlannedTask fields, so the caller (T003b2b2b2's dispatch-loop wiring,
# DECISION F112 D7) passes the parent task's own values through; every
# other field is a direct or joined mapping. Not yet called from run_job —
# T003b2b2b2 is the wiring that calls it.
def planned_task_to_task_entry(
    planned: PlannedTask,
    *,
    task_class: str = TASK_CLASS_DEFAULT,
    source_heading_number: int = 0,
) -> TaskEntry:
    """Adapt one split-off ``PlannedTask`` back into a dispatchable ``TaskEntry``."""
    return TaskEntry(
        task_id=planned.id,
        source_heading_number=source_heading_number,
        title=planned.title,
        task_class=task_class,
        body=planned.goal,
        acceptance="\n".join(planned.acceptance),
        files_hint=list(planned.files_hint),
        status=TASK_PENDING,
    )


@dataclass
class TargetGuard:
    """Job-level target repo mutation guard.

    ``target_mutated`` is the headline flag and tracks real source changes only
    (``target_content_mutated``). Operational review/evidence artifacts and
    volatile cache noise are reported separately but never count as a mutation.
    """
    target_mutated: bool = False
    target_content_mutated: bool = False
    target_operational_artifacts_changed: bool = False
    target_noise_changed: bool = False
    changed_target_files: list[str] = field(default_factory=list)
    ignored_operational_artifacts: list[str] = field(default_factory=list)
    ignored_target_noise_files: list[str] = field(default_factory=list)


@dataclass
class ExecutionConfig:
    """Durable execution config for job continuation."""
    builder: str = "fake"
    builder_source: str = "default"
    reviewer: str = "fake"
    reviewer_source: str = "default"
    builder_model: str = ""
    builder_model_source: str = "default"
    builder_effort: str = ""
    builder_effort_source: str = "default"
    reviewer_model: str = ""
    reviewer_model_source: str = "default"
    reviewer_effort: str = ""
    reviewer_effort_source: str = "default"
    repair_provider: str = ""
    repair_provider_source: str = "default"
    repair_model: str = ""
    repair_model_source: str = "default"
    repair_effort: str = ""
    repair_effort_source: str = "default"
    max_rounds: int = 3
    max_rounds_source: str = "default"
    repair_rounds_allowed: int = 2
    repair_rounds_source: str = "default"
    test_command: str = ""
    test_command_source: str = "default"
    claude_cli_write_mode: str = "none"
    claude_cli_write_mode_source: str = "default"
    context_strategy: str = "task_bounded_sequential_job"
    # F012 round 4 (F2): invocation-level controls that alter execution/evidence. Material
    # inputs, persisted with their source so `explicit > persisted > default` is auditable.
    timeout_sec: int = 120
    timeout_sec_source: str = "default"
    timeout_profile: str = ""
    timeout_profile_source: str = "default"
    max_output_chars: int = 50000
    max_output_chars_source: str = "default"
    stream_evidence: bool = False
    stream_evidence_source: str = "default"
    max_tasks: int = 0
    max_tasks_source: str = "default"


@dataclass
class JobPlan:
    """Durable job plan with ordered tasks."""
    job_id: str = field(default_factory=mint_job_id)
    job_file_sha256: str = ""
    repo_path: str = ""
    job_workspace_path: str = ""
    job_title: str = ""
    status: str = JOB_PLANNED
    tasks: list[TaskEntry] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    finished_at: str = ""
    error: str = ""
    target_guard: TargetGuard | None = None
    repair_rounds_allowed: int = 0
    repair_rounds_source: str = ""
    execution_config: ExecutionConfig | None = None
    # F006: how the job workspace is isolated, and the job-level hand-off.
    isolation_mode: str = "copy"          # "worktree" | "copy"
    worktree_branch: str = ""
    worktree_path: str = ""               # repository-relative, shareable
    worktree_base_commit: str = ""
    worktree_head: str = ""
    worktree_cleanup_status: str = ""     # "active"|"clean"|"retained"|"failed_recoverable"
    # F010: the job-level post-mortem this job left (evidence-relative), and the reason one
    # could not be written. A job that failed before any task ran must not vanish.
    postmortem_path: str = ""
    postmortem_error: str = ""
    worktree_cleanup_error: str = ""
    result_diff_path: str = ""
    result_diff_sha256: str = ""
    result_diff_size_bytes: int = 0
    result_diff_error: str = ""
    job_initial_tree: str = ""            # tree of the workspace before task 1
    job_initial_tree_ref: str = ""        # checkpoint ref keeping that tree alive
    # F006 hand-off coverage: the root diff must be EXACTLY the reviewed task work.
    root_changed_files: list[str] = field(default_factory=list)
    reviewed_task_files: list[str] = field(default_factory=list)
    unexpected_root_files: list[str] = field(default_factory=list)
    missing_root_files: list[str] = field(default_factory=list)
    handoff_coverage_verdict: str = ""    # "PASS" | "FAIL" | ""
    # F011: the LAST stop episode. Older job files have none of this and load unchanged.
    stop_request_id: str = ""
    stop_reason: str = ""
    stop_source: str = ""
    stopped_at: str = ""
    stop_archive_ref: str = ""            # control-relative, never absolute
    stop_postmortem_path: str = ""        # evidence-relative, never absolute
    stop_error: str = ""                  # a recording failure, kept durable (blocking)
    stop_event_error: str = ""
    # F012: the run-input manifest this job left (evidence-relative), and the reason one
    # could not be written. A write failure is durable and blocks a falsely clean package.
    run_manifest_path: str = ""
    run_manifest_error: str = ""
    run_manifest_created_at: str = ""
    # F012 episode model + start snapshot + legacy marker.
    run_manifest_required_v: int = 0          # >0 marks a job created/first-run under F012
    active_episode_id: str = ""               # this run episode's id (completed episodes)
    episode_start_workspace_tree: str = ""    # F4: workspace tree at this episode's start
    input_snapshot: dict = field(default_factory=dict)   # captured at episode start
    # F1/F12: a durable reason the MANDATORY episode-start snapshot could not be captured (or
    # was invalid). Its presence means the job was HARD-BLOCKED before any provider work — the
    # runner started zero tasks and made zero provider calls.
    input_snapshot_error: str = ""
    run_manifest_episodes: list = field(default_factory=list)  # index of episode dicts
    # F018: job budget limits (serialized dict from JobBudgets.model_dump, or None).
    budgets: dict | None = None
    # F018: set exactly once immediately before the first real work begins.
    # Planning and waiting time do not count. Resume preserves the original.
    first_running_at: str = ""
    budget_actuals: dict | None = None
    # F104: the prediction that justified a predictive stop — its arithmetic is
    # what a human reads to see WHY the job stopped before doing any work.
    budget_prediction: dict | None = None
    # F112 T003: durable escalation/decision state (e.g. `enqueue_task_decision`'s
    # `job.metadata["escalations"]` list) — a plain dict, exported and imported
    # verbatim like `input_snapshot` above so a cannot_fit decision survives a
    # persist/resume cycle instead of vanishing as a Python-only attribute.
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _persist_job(job: JobPlan) -> Path:
    # ``data_paths`` owns "where the ping-pong record lives" (DECISION F260 D1),
    # so this writer and the readers that resolve an id cannot drift apart.
    from packages.orchestration.data_paths import job_record_path

    out = job_record_path(job.job_id)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(_json.dumps(_export_job(job), indent=2) + "\n")
    return out


def save_job_plan(job: JobPlan) -> Path:
    """Public API to persist a JobPlan. Returns path to job.json."""
    return _persist_job(job)


def load_job_plan(job_id: str) -> JobPlan | None:
    from packages.orchestration.data_paths import job_record_path

    job_file = job_record_path(job_id)
    if not job_file.exists():
        return None
    try:
        data = _json.loads(job_file.read_text())
        return _import_job(data)
    except (OSError, _json.JSONDecodeError, KeyError):
        return None


def _export_file_proof(p: AppliedFileProof) -> dict[str, Any]:
    return {
        "path": p.path,
        "existed_before_job": p.existed_before_job,
        "baseline_sha256": p.baseline_sha256,
        "final_workspace_sha256": p.final_workspace_sha256,
        "task_id": p.task_id,
        "run_id": p.run_id,
        "baseline_mode": p.baseline_mode,
        "final_mode": p.final_mode,
    }


def _import_file_proof(d: dict[str, Any]) -> AppliedFileProof:
    return AppliedFileProof(
        path=d.get("path", ""),
        existed_before_job=d.get("existed_before_job", False),
        baseline_sha256=d.get("baseline_sha256", ""),
        final_workspace_sha256=d.get("final_workspace_sha256", ""),
        task_id=d.get("task_id", ""),
        run_id=d.get("run_id", ""),
        baseline_mode=d.get("baseline_mode", ""),
        final_mode=d.get("final_mode", ""),
    )


def _export_apply_manifest(m: ApplyManifest | None) -> dict[str, Any] | None:
    if m is None:
        return None
    return {
        "task_id": m.task_id,
        "run_id": m.run_id,
        "applied_files": m.applied_files,
        "missing_files": m.missing_files,
        "unsupported_files": m.unsupported_files,
        "unexpected_files": m.unexpected_files,
        "duplicate_files": m.duplicate_files,
        "applied_file_proofs": [_export_file_proof(p) for p in m.applied_file_proofs],
        "status": m.status,
    }


def _import_apply_manifest(d: dict[str, Any] | None) -> ApplyManifest | None:
    if d is None:
        return None
    return ApplyManifest(
        task_id=d.get("task_id", ""),
        run_id=d.get("run_id", ""),
        applied_files=d.get("applied_files", []),
        missing_files=d.get("missing_files", []),
        unsupported_files=d.get("unsupported_files", []),
        unexpected_files=d.get("unexpected_files", []),
        duplicate_files=d.get("duplicate_files", []),
        applied_file_proofs=[
            _import_file_proof(p) for p in d.get("applied_file_proofs", [])
        ],
        status=d.get("status", "pending"),
    )


def _export_proof_summary(p: TaskProofSummary | None) -> dict[str, Any] | None:
    if p is None:
        return None
    return {
        "task_id": p.task_id,
        "title": p.title,
        "run_id": p.run_id,
        "final_status": p.final_status,
        "applied_files": p.applied_files,
        "test_passed": p.test_passed,
        "reviewer_verdict": p.reviewer_verdict,
        "repair_rounds_used": p.repair_rounds_used,
        "repair_rounds_allowed": p.repair_rounds_allowed,
        "tokens_estimated": p.tokens_estimated,
    }


def _import_proof_summary(d: dict[str, Any] | None) -> TaskProofSummary | None:
    if d is None:
        return None
    return TaskProofSummary(
        task_id=d.get("task_id", ""),
        title=d.get("title", ""),
        run_id=d.get("run_id", ""),
        final_status=d.get("final_status", ""),
        applied_files=d.get("applied_files", []),
        test_passed=d.get("test_passed"),
        reviewer_verdict=d.get("reviewer_verdict", ""),
        repair_rounds_used=d.get("repair_rounds_used", 0),
        repair_rounds_allowed=d.get("repair_rounds_allowed", 0),
        tokens_estimated=d.get("tokens_estimated", 0),
    )


def _export_execution_config(c: ExecutionConfig | None) -> dict[str, Any] | None:
    if c is None:
        return None
    return {
        "builder": c.builder,
        "builder_source": c.builder_source,
        "reviewer": c.reviewer,
        "reviewer_source": c.reviewer_source,
        "builder_model": c.builder_model,
        "builder_model_source": c.builder_model_source,
        "builder_effort": c.builder_effort,
        "builder_effort_source": c.builder_effort_source,
        "reviewer_model": c.reviewer_model,
        "reviewer_model_source": c.reviewer_model_source,
        "reviewer_effort": c.reviewer_effort,
        "reviewer_effort_source": c.reviewer_effort_source,
        "repair_provider": c.repair_provider,
        "repair_provider_source": c.repair_provider_source,
        "repair_model": c.repair_model,
        "repair_model_source": c.repair_model_source,
        "repair_effort": c.repair_effort,
        "repair_effort_source": c.repair_effort_source,
        "max_rounds": c.max_rounds,
        "max_rounds_source": c.max_rounds_source,
        "repair_rounds_allowed": c.repair_rounds_allowed,
        "repair_rounds_source": c.repair_rounds_source,
        "test_command": c.test_command,
        "test_command_present": bool(c.test_command),
        "test_command_source": c.test_command_source,
        "claude_cli_write_mode": c.claude_cli_write_mode,
        "claude_cli_write_mode_source": c.claude_cli_write_mode_source,
        "context_strategy": c.context_strategy,
        "timeout_sec": c.timeout_sec,
        "timeout_sec_source": c.timeout_sec_source,
        "timeout_profile": c.timeout_profile,
        "timeout_profile_source": c.timeout_profile_source,
        "max_output_chars": c.max_output_chars,
        "max_output_chars_source": c.max_output_chars_source,
        "stream_evidence": c.stream_evidence,
        "stream_evidence_source": c.stream_evidence_source,
        "max_tasks": c.max_tasks,
        "max_tasks_source": c.max_tasks_source,
    }


def _import_execution_config(d: dict[str, Any] | None) -> ExecutionConfig | None:
    if d is None:
        return None
    return ExecutionConfig(
        builder=d.get("builder", "fake"),
        builder_source=d.get("builder_source", "default"),
        reviewer=d.get("reviewer", "fake"),
        reviewer_source=d.get("reviewer_source", "default"),
        builder_model=d.get("builder_model", ""),
        builder_model_source=d.get("builder_model_source", "default"),
        builder_effort=d.get("builder_effort", ""),
        builder_effort_source=d.get("builder_effort_source", "default"),
        reviewer_model=d.get("reviewer_model", ""),
        reviewer_model_source=d.get("reviewer_model_source", "default"),
        reviewer_effort=d.get("reviewer_effort", ""),
        reviewer_effort_source=d.get("reviewer_effort_source", "default"),
        repair_provider=d.get("repair_provider", ""),
        repair_provider_source=d.get("repair_provider_source", "default"),
        repair_model=d.get("repair_model", ""),
        repair_model_source=d.get("repair_model_source", "default"),
        repair_effort=d.get("repair_effort", ""),
        repair_effort_source=d.get("repair_effort_source", "default"),
        max_rounds=d.get("max_rounds", 3),
        max_rounds_source=d.get("max_rounds_source", "default"),
        repair_rounds_allowed=d.get("repair_rounds_allowed", 2),
        repair_rounds_source=d.get("repair_rounds_source", "default"),
        test_command=d.get("test_command", ""),
        test_command_source=d.get("test_command_source", "default"),
        claude_cli_write_mode=d.get("claude_cli_write_mode", "none"),
        claude_cli_write_mode_source=d.get("claude_cli_write_mode_source", "default"),
        context_strategy=d.get("context_strategy", "task_bounded_sequential_job"),
        timeout_sec=int(d.get("timeout_sec", 120) or 120),
        timeout_sec_source=d.get("timeout_sec_source", "default"),
        timeout_profile=d.get("timeout_profile", ""),
        timeout_profile_source=d.get("timeout_profile_source", "default"),
        max_output_chars=int(d.get("max_output_chars", 50000) or 50000),
        max_output_chars_source=d.get("max_output_chars_source", "default"),
        stream_evidence=bool(d.get("stream_evidence", False)),
        stream_evidence_source=d.get("stream_evidence_source", "default"),
        max_tasks=int(d.get("max_tasks", 0) or 0),
        max_tasks_source=d.get("max_tasks_source", "default"),
    )


def _export_target_guard(g: TargetGuard | None) -> dict[str, Any] | None:
    if g is None:
        return None
    return {
        "target_mutated": g.target_mutated,
        "target_content_mutated": g.target_content_mutated,
        "target_operational_artifacts_changed": g.target_operational_artifacts_changed,
        "target_noise_changed": g.target_noise_changed,
        "changed_target_files": g.changed_target_files,
        "ignored_operational_artifacts": g.ignored_operational_artifacts,
        "ignored_target_noise_files": g.ignored_target_noise_files,
    }


def _import_target_guard(d: dict[str, Any] | None) -> TargetGuard | None:
    if d is None:
        return None
    return TargetGuard(
        target_mutated=d.get("target_mutated", False),
        target_content_mutated=d.get(
            "target_content_mutated", d.get("target_mutated", False)
        ),
        target_operational_artifacts_changed=d.get(
            "target_operational_artifacts_changed", False
        ),
        target_noise_changed=d.get("target_noise_changed", False),
        changed_target_files=d.get("changed_target_files", []),
        ignored_operational_artifacts=d.get("ignored_operational_artifacts", []),
        ignored_target_noise_files=d.get("ignored_target_noise_files", []),
    )


def _export_job(job: JobPlan) -> dict[str, Any]:
    return {
        "job_id": job.job_id,
        "job_file_sha256": job.job_file_sha256,
        "repo_path": job.repo_path,
        "job_workspace_path": job.job_workspace_path,
        "job_title": job.job_title,
        "status": job.status,
        "created_at": job.created_at,
        "finished_at": job.finished_at,
        "error": job.error,
        "target_guard": _export_target_guard(job.target_guard),
        # F010: the job-level post-mortem, and the reason one could not be written. A
        # recording failure that did not survive `_persist_job` was a recording failure the
        # evidence export could never see.
        "postmortem": {
            "path": job.postmortem_path,      # evidence-relative, never absolute
            "error": job.postmortem_error,
        },
        "repair_rounds_allowed": job.repair_rounds_allowed,
        "repair_rounds_source": job.repair_rounds_source,
        "execution_config": _export_execution_config(job.execution_config),
        "isolation_mode": job.isolation_mode,
        "worktree": {
            "isolation_mode": job.isolation_mode,
            "branch": job.worktree_branch,
            "path": job.worktree_path,
            "base_commit": job.worktree_base_commit,
            "head": job.worktree_head,
            "cleanup_status": job.worktree_cleanup_status,
            "cleanup_error": job.worktree_cleanup_error,
            "result_diff": (
                {
                    "path": job.result_diff_path,
                    "sha256": job.result_diff_sha256,
                    "size_bytes": job.result_diff_size_bytes,
                }
                if job.result_diff_path else None
            ),
            "result_diff_error": job.result_diff_error,
        },
        "job_initial_tree": job.job_initial_tree,
        "job_initial_tree_ref": job.job_initial_tree_ref,
        # F011: the last stop episode. Absent from every job file written before F011, and
        # absent from a job that was never stopped — both load as "no stop", not as an error.
        "stop": {
            "request_id": job.stop_request_id,
            "reason": job.stop_reason,
            "source": job.stop_source,
            "stopped_at": job.stopped_at,
            "archive_ref": job.stop_archive_ref,
            "postmortem_path": job.stop_postmortem_path,
            "error": job.stop_error,
            "event_error": job.stop_event_error,
        },
        "run_manifest": {
            "path": job.run_manifest_path,
            "error": job.run_manifest_error,
            "created_at": job.run_manifest_created_at,
            "required_v": job.run_manifest_required_v,
            "active_episode_id": job.active_episode_id,
            "episode_start_workspace_tree": job.episode_start_workspace_tree,
            "input_snapshot": job.input_snapshot,
            "input_snapshot_error": job.input_snapshot_error,
            "episodes": job.run_manifest_episodes,
        },
        "budgets": job.budgets,
        "first_running_at": job.first_running_at,
        "budget_actuals": job.budget_actuals,
        "budget_prediction": job.budget_prediction,
        "metadata": job.metadata,
        "handoff_coverage": {
            "verdict": job.handoff_coverage_verdict,
            "root_changed_files": job.root_changed_files,
            "reviewed_task_files": job.reviewed_task_files,
            "unexpected_root_files": job.unexpected_root_files,
            "missing_root_files": job.missing_root_files,
        },
        "tasks": [
            {
                "task_id": t.task_id,
                "source_heading_number": t.source_heading_number,
                "title": t.title,
                "task_class": t.task_class,
                "inputs": t.inputs,
                "files_hint": t.files_hint,
                "body": t.body,
                "acceptance": t.acceptance,
                "status": t.status,
                "run_id": t.run_id,
                "final_status": t.final_status,
                "safe_diff_files": t.safe_diff_files,
                "test_passed": t.test_passed,
                "reviewer_verdict": t.reviewer_verdict,
                "repair_rounds_used": t.repair_rounds_used,
                "repair_rounds_allowed": t.repair_rounds_allowed,
                "error": t.error,
                "apply_manifest": _export_apply_manifest(t.apply_manifest),
                "proof_summary": _export_proof_summary(t.proof_summary),
                "task_start_tree": t.task_start_tree,
                "task_start_tree_ref": t.task_start_tree_ref,
                "task_start_recorded_at": t.task_start_recorded_at,
                "task_attempt_state": t.task_attempt_state,
            }
            for t in job.tasks
        ],
    }


def _import_job(data: dict[str, Any]) -> JobPlan:
    job = JobPlan(
        job_id=data["job_id"],
        job_file_sha256=data.get("job_file_sha256", ""),
        repo_path=data.get("repo_path", ""),
        job_workspace_path=data.get("job_workspace_path", ""),
        job_title=data.get("job_title", ""),
        status=data.get("status", JOB_PLANNED),
        created_at=data.get("created_at", ""),
        finished_at=data.get("finished_at", ""),
        error=data.get("error", ""),
        target_guard=_import_target_guard(data.get("target_guard")),
        # Older job files have no `postmortem` block at all; they load as empty, not as an
        # error.
        postmortem_path=str((data.get("postmortem") or {}).get("path", "") or ""),
        postmortem_error=str((data.get("postmortem") or {}).get("error", "") or ""),
        isolation_mode=data.get("isolation_mode", "copy"),
        worktree_branch=(data.get("worktree") or {}).get("branch", ""),
        worktree_path=(data.get("worktree") or {}).get("path", ""),
        worktree_base_commit=(data.get("worktree") or {}).get("base_commit", ""),
        worktree_head=(data.get("worktree") or {}).get("head", ""),
        worktree_cleanup_status=(data.get("worktree") or {}).get("cleanup_status", ""),
        worktree_cleanup_error=(data.get("worktree") or {}).get("cleanup_error", ""),
        result_diff_path=((data.get("worktree") or {}).get("result_diff") or {}).get("path", ""),
        result_diff_sha256=((data.get("worktree") or {}).get("result_diff") or {}).get("sha256", ""),
        result_diff_size_bytes=((data.get("worktree") or {}).get("result_diff") or {}).get("size_bytes", 0),
        result_diff_error=(data.get("worktree") or {}).get("result_diff_error", ""),
        job_initial_tree=data.get("job_initial_tree", ""),
        job_initial_tree_ref=data.get("job_initial_tree_ref", ""),
        handoff_coverage_verdict=(data.get("handoff_coverage") or {}).get("verdict", ""),
        root_changed_files=(data.get("handoff_coverage") or {}).get("root_changed_files", []),
        reviewed_task_files=(data.get("handoff_coverage") or {}).get("reviewed_task_files", []),
        unexpected_root_files=(data.get("handoff_coverage") or {}).get("unexpected_root_files", []),
        missing_root_files=(data.get("handoff_coverage") or {}).get("missing_root_files", []),
        repair_rounds_allowed=data.get("repair_rounds_allowed", 0),
        repair_rounds_source=data.get("repair_rounds_source", ""),
        execution_config=_import_execution_config(data.get("execution_config")),
        stop_request_id=str((data.get("stop") or {}).get("request_id", "") or ""),
        stop_reason=str((data.get("stop") or {}).get("reason", "") or ""),
        stop_source=str((data.get("stop") or {}).get("source", "") or ""),
        stopped_at=str((data.get("stop") or {}).get("stopped_at", "") or ""),
        stop_archive_ref=str((data.get("stop") or {}).get("archive_ref", "") or ""),
        stop_postmortem_path=str((data.get("stop") or {}).get("postmortem_path", "") or ""),
        stop_error=str((data.get("stop") or {}).get("error", "") or ""),
        stop_event_error=str((data.get("stop") or {}).get("event_error", "") or ""),
        run_manifest_path=str((data.get("run_manifest") or {}).get("path", "") or ""),
        run_manifest_error=str((data.get("run_manifest") or {}).get("error", "") or ""),
        run_manifest_created_at=str((data.get("run_manifest") or {}).get("created_at", "") or ""),
        run_manifest_required_v=int((data.get("run_manifest") or {}).get("required_v", 0) or 0),
        active_episode_id=str((data.get("run_manifest") or {}).get("active_episode_id", "") or ""),
        episode_start_workspace_tree=str((data.get("run_manifest") or {}).get("episode_start_workspace_tree", "") or ""),
        input_snapshot=dict((data.get("run_manifest") or {}).get("input_snapshot") or {}),
        input_snapshot_error=str((data.get("run_manifest") or {}).get("input_snapshot_error", "") or ""),
        run_manifest_episodes=list((data.get("run_manifest") or {}).get("episodes") or []),
        budgets=data.get("budgets"),
        first_running_at=str(data.get("first_running_at", "") or ""),
        budget_actuals=data.get("budget_actuals"),
        # Absent in job files written before F104 — loads as None, unchanged.
        budget_prediction=data.get("budget_prediction"),
        metadata=dict(data.get("metadata") or {}),
    )
    for t in data.get("tasks", []):
        job.tasks.append(TaskEntry(
            task_id=t.get("task_id", ""),
            source_heading_number=t.get("source_heading_number", 0),
            title=t.get("title", ""),
            task_class=t.get("task_class", TASK_CLASS_DEFAULT),
            inputs=dict(t.get("inputs") or {}),
            files_hint=list(t.get("files_hint") or []),
            body=t.get("body", ""),
            acceptance=t.get("acceptance", ""),
            status=t.get("status", TASK_PENDING),
            run_id=t.get("run_id", ""),
            final_status=t.get("final_status", ""),
            safe_diff_files=t.get("safe_diff_files", []),
            test_passed=t.get("test_passed"),
            reviewer_verdict=t.get("reviewer_verdict", ""),
            repair_rounds_used=t.get("repair_rounds_used", 0),
            repair_rounds_allowed=t.get("repair_rounds_allowed", 0),
            error=t.get("error", ""),
            apply_manifest=_import_apply_manifest(t.get("apply_manifest")),
            proof_summary=_import_proof_summary(t.get("proof_summary")),
            task_start_tree=t.get("task_start_tree", ""),
            task_start_tree_ref=t.get("task_start_tree_ref", ""),
            task_start_recorded_at=t.get("task_start_recorded_at", ""),
            task_attempt_state=t.get("task_attempt_state", ""),
        ))
    return job


# ---------------------------------------------------------------------------
# Markdown job-file parser (deterministic, no provider call)
# ---------------------------------------------------------------------------

_TASK_HEADING_RE = re.compile(
    r"^##\s+Task\s+(\d+)\s*(?:[:\-—–]\s*)?(.*)$",
    re.IGNORECASE,
)


def parse_job_file(text: str, repo_path: str = ".") -> JobPlan:
    """Parse a Markdown job file into a JobPlan with ordered tasks.

    Task IDs are assigned by parse order (T001, T002, ...), not by heading
    number. The original heading number is stored in source_heading_number.

    Returns a JobPlan with status=planned. No provider calls, no repo mutation.
    """
    sha256 = hashlib.sha256(text.encode()).hexdigest()

    # Extract job title from first H1
    job_title = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            job_title = stripped[2:].strip()
            if job_title.lower().startswith("job:"):
                job_title = job_title[4:].strip()
            break

    # Split into task sections
    lines = text.splitlines()
    task_sections: list[dict[str, Any]] = []
    current_task: dict[str, Any] | None = None

    for line in lines:
        m = _TASK_HEADING_RE.match(line.strip())
        if m:
            if current_task is not None:
                task_sections.append(current_task)
            heading_num = int(m.group(1))
            task_title = m.group(2).strip()
            current_task = {
                "heading_num": heading_num,
                "title": task_title,
                "body_lines": [],
                "acceptance_lines": [],
                "files_lines": [],
            }
            continue

        if current_task is not None:
            stripped = line.strip()
            if stripped.lower().startswith("acceptance:") or stripped.lower().startswith("acceptance :"):
                current_task["_in_acceptance"] = True
                current_task["_in_files"] = False
                continue
            # F112 T003c: a third parser state, mirroring "Acceptance:" —
            # "Files:" declares this task's fenced scope (DECISION F112 D5),
            # the compiled_context_paths source T003b2b2 needs.
            if stripped.lower().startswith("files:") or stripped.lower().startswith("files :"):
                current_task["_in_files"] = True
                current_task["_in_acceptance"] = False
                continue
            if current_task.get("_in_files"):
                current_task["files_lines"].append(line)
            elif current_task.get("_in_acceptance"):
                current_task["acceptance_lines"].append(line)
            else:
                current_task["body_lines"].append(line)

    if current_task is not None:
        task_sections.append(current_task)

    if not task_sections:
        job = JobPlan(
            job_file_sha256=sha256,
            repo_path=str(Path(repo_path).resolve()),
            job_title=job_title or "(untitled)",
            status=JOB_BLOCKED,
            error="no_tasks_found: job file has no ## Task N headings",
        )
        _persist_job(job)
        return job

    tasks: list[TaskEntry] = []
    for parse_idx, sec in enumerate(task_sections):
        # Deterministic ID by parse order, not heading number
        task_id = f"T{parse_idx + 1:03d}"
        body = "\n".join(sec["body_lines"]).strip()
        acceptance = "\n".join(sec["acceptance_lines"]).strip()
        title = sec["title"] or f"Task {sec['heading_num']}"
        if len(body) > _TASK_BODY_LIMIT:
            body = body[:_TASK_BODY_LIMIT] + "\n[truncated]"
        # F112 T003c: "- path" / "path" bullet lines under "Files:" become
        # TaskEntry.files_hint — unlike acceptance, these are literal repo-
        # relative paths (compile_task_context checks them against disk), so
        # the leading bullet marker is stripped rather than kept verbatim.
        files_hint: list[str] = []
        for fl in sec["files_lines"]:
            fl_stripped = fl.strip()
            if fl_stripped.startswith("-"):
                fl_stripped = fl_stripped[1:].strip()
            if fl_stripped:
                files_hint.append(fl_stripped)
        tasks.append(TaskEntry(
            task_id=task_id,
            source_heading_number=sec["heading_num"],
            title=title,
            body=body,
            acceptance=acceptance,
            files_hint=files_hint,
        ))

    job = JobPlan(
        job_file_sha256=sha256,
        repo_path=str(Path(repo_path).resolve()),
        job_title=job_title or "(untitled)",
        tasks=tasks,
    )
    _persist_job(job)
    return job


def plan_job_from_file(job_file_path: str, repo_path: str = ".") -> JobPlan:
    """Read a job file from disk and parse it."""
    path = Path(job_file_path)
    if not path.exists():
        job = JobPlan(
            repo_path=str(Path(repo_path).resolve()),
            status=JOB_BLOCKED,
            error=f"job_file_not_found: {job_file_path}",
        )
        _persist_job(job)
        return job
    text = path.read_text()
    return parse_job_file(text, repo_path)


# ---------------------------------------------------------------------------
# Job workspace creation (filtered copy of target repo)
# ---------------------------------------------------------------------------

#: The job-owned worktree's safe id: one worktree, one branch, per job.
def job_worktree_id(job_id: str) -> str:
    return f"job-{job_id}"


def _create_job_workspace_copy(job: JobPlan) -> str:
    """Non-git fallback: a filtered copy of the target (isolation_mode=copy)."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.staging_workspace import create_staging_workspace

    data_root = resolve_data_root()
    ws_parent = data_root / "job_workspaces"
    ws_parent.mkdir(parents=True, exist_ok=True)

    target = Path(job.repo_path)
    ws = create_staging_workspace(target, ws_parent, job.job_id)
    return str(ws.staging_dir)


def _create_job_workspace(job: JobPlan) -> tuple[str, Any]:
    """The job's workspace. For a GIT target this is a job-owned WORKTREE.

    One worktree per job at ``<target>/.remedy-wt/job-<job-id>`` on branch
    ``remedy/job-<job-id>``, owned by the job runner for the whole execution: the
    tasks run sequentially inside it, so task 2 sees task 1's accepted changes,
    and NO complete copy of the repository is ever made. The normal checkout is
    untouched and nothing is ever merged.

    Returns ``(workspace_path, handle)``; ``handle`` is None only for the non-git
    copy fallback.
    """
    from packages.orchestration import worktrees as W

    if not W.is_git_repo(job.repo_path):
        job.isolation_mode = "copy"
        return _create_job_workspace_copy(job), None

    wt_id = job_worktree_id(job.job_id)
    handle = W.create(wt_id, job.repo_path)
    job.isolation_mode = "worktree"
    job.worktree_branch = handle.branch
    job.worktree_path = handle.relative_path
    job.worktree_base_commit = handle.base_commit
    job.worktree_head = handle.head_commit
    job.worktree_cleanup_status = "active"
    job.job_initial_tree = W.write_tree(handle)
    job.job_initial_tree_ref = W.checkpoint_ref(
        job_worktree_id(job.job_id), "job-initial")
    W.set_checkpoint_ref(job.repo_path, job.job_initial_tree_ref, job.job_initial_tree)
    return handle.path, handle


def _acquire_job_workspace(job: JobPlan) -> tuple[str, Any]:
    """Re-claim an existing job workspace, or create it on first run."""
    from packages.orchestration import worktrees as W

    if not job.job_workspace_path:
        path, handle = _create_job_workspace(job)
        job.job_workspace_path = path
        return path, handle

    if job.isolation_mode != "worktree":
        return job.job_workspace_path, None

    handle = W.recover(job_worktree_id(job.job_id), job.repo_path)
    if handle is None or not Path(handle.path).is_dir():
        raise RuntimeError(
            f"job worktree {job.worktree_path!r} is gone; refusing to silently "
            f"fall back to a copied workspace"
        )
    if handle.branch != job.worktree_branch:
        from packages.orchestration import worktrees as _W
        _W.release_lock(handle)
        raise RuntimeError(
            f"job worktree is on branch {handle.branch!r}, not the recorded "
            f"{job.worktree_branch!r}"
        )
    err = _verify_checkpoints(job)
    if err:
        # NEVER re-snapshot a lost checkpoint: a fresh baseline would silently
        # swallow whatever the interrupted attempt had already written.
        W.retain_for_recovery(handle, err)
        job.worktree_cleanup_status = "retained"
        job.worktree_cleanup_error = err
        raise RuntimeError(err)

    job.worktree_cleanup_status = "active"
    return handle.path, handle


def _verify_checkpoints(job: JobPlan) -> str:
    """Every ACTIVE checkpoint ref must still resolve to its recorded tree."""
    from packages.orchestration import worktrees as W

    def _check(ref: str, sha: str, what: str) -> str:
        if not sha:
            return ""
        if not ref:
            return f"checkpoint_ref_missing: {what} has no protecting ref"
        actual = W.resolve_checkpoint_ref(job.repo_path, ref)
        if not actual:
            return f"checkpoint_ref_missing: {what} ref {ref} does not exist"
        if actual != sha:
            return (
                f"checkpoint_ref_mismatch: {what} ref {ref} points at {actual[:12]}, "
                f"not the recorded {sha[:12]}"
            )
        if not W.object_exists(job.repo_path, sha):
            return f"checkpoint_object_missing: {what} tree {sha[:12]} is gone"
        return ""

    err = _check(job.job_initial_tree_ref, job.job_initial_tree, "job_initial_tree")
    if err:
        return err
    for t in job.tasks:
        if t.task_attempt_state == "active" and t.task_start_tree:
            err = _check(t.task_start_tree_ref, t.task_start_tree,
                         f"{t.task_id} task_start_tree")
            if err:
                return err
    return ""


def _reviewed_task_files(job: JobPlan) -> list[str]:
    """Union of every successfully applied task manifest — the reviewed work."""
    files: set[str] = set()
    for t in job.tasks:
        if t.apply_manifest and t.apply_manifest.status == "applied":
            files.update(t.apply_manifest.applied_files)
    return sorted(files)


def _latest_task_proofs(job: JobPlan) -> dict[str, AppliedFileProof]:
    """The LAST accepted proof per path — that is the reviewed final state."""
    latest: dict[str, AppliedFileProof] = {}
    for t in job.tasks:
        if t.apply_manifest and t.apply_manifest.status == "applied":
            for proof in t.apply_manifest.applied_file_proofs:
                latest[proof.path] = proof
    return latest


def _check_handoff_coverage(job: JobPlan, handle: Any) -> str:
    """The root hand-off must be EXACTLY the reviewed task work — nothing else.

    Byte-integrity of ``result.diff`` proves nobody edited the file; it does NOT
    prove the diff only contains reviewed changes. A finalization hook writing
    ``rogue.txt`` into the worktree would sail through a hash check. So the final
    tree's changed-path set must equal the union of the applied task manifests, and
    every reviewed path must still hold the content and mode its task proved.
    """
    from packages.orchestration import worktrees as W

    final_tree = W.write_tree(handle)
    root_files = W.changed_files_between(handle, job.job_initial_tree, final_tree)
    reviewed = _reviewed_task_files(job)

    job.root_changed_files = list(root_files)
    job.reviewed_task_files = reviewed
    job.unexpected_root_files = sorted(set(root_files) - set(reviewed))
    job.missing_root_files = sorted(set(reviewed) - set(root_files))

    drift: list[str] = []
    proofs = _latest_task_proofs(job)
    ws = Path(job.job_workspace_path)
    for rel, proof in proofs.items():
        f = ws / rel
        if not f.is_file():
            drift.append(f"{rel}: reviewed file is gone from the workspace")
            continue
        if _sha256_of(f) != proof.final_workspace_sha256:
            drift.append(f"{rel}: content differs from the reviewed proof")
        elif proof.final_mode and W.file_mode(f) != proof.final_mode:
            drift.append(f"{rel}: file mode differs from the reviewed proof")

    if job.unexpected_root_files or job.missing_root_files or drift:
        job.handoff_coverage_verdict = "FAIL"
        parts = []
        if job.unexpected_root_files:
            parts.append(f"unexpected={job.unexpected_root_files}")
        if job.missing_root_files:
            parts.append(f"missing={job.missing_root_files}")
        if drift:
            parts.append(f"drift={drift}")
        return "job_handoff_coverage_failed: " + "; ".join(parts)

    job.handoff_coverage_verdict = "PASS"
    return ""


def _drop_checkpoint_refs(job: JobPlan) -> str:
    """Remove obsolete checkpoint refs after a verified final hand-off."""
    from packages.orchestration import worktrees as W

    errors: list[str] = []
    refs = [job.job_initial_tree_ref] + [
        t.task_start_tree_ref for t in job.tasks if t.task_start_tree_ref
    ]
    for ref in [r for r in refs if r]:
        err = W.delete_checkpoint_ref(job.repo_path, ref)
        if err:
            errors.append(f"{ref}: {err}")
    return "; ".join(errors)


def _finalize_job_workspace(job: JobPlan, handle: Any) -> None:
    """The ONE cleanup path for a job-owned worktree.

    Completed job: persist the job-level ``result.diff`` (tree-to-tree — no commit,
    no merge), remove the physical worktree, keep the result branch, release the
    lock, mark ``clean``. Any other end state (paused, blocked, failed, raised):
    persist what we can, KEEP the worktree and its uncommitted changes, release the
    lock, and stay recoverable. A clean cleanup is never claimed before it happened.
    """
    if handle is None:
        return
    from packages.orchestration import worktrees as W
    from packages.orchestration.data_paths import job_dir

    job_root = job_dir(job.job_id)

    # --- Completion gate: the root hand-off must be exactly the reviewed work ---
    coverage_error = ""
    if job.status == JOB_COMPLETED:
        try:
            coverage_error = _check_handoff_coverage(job, handle)
        except Exception as exc:
            coverage_error = f"job_handoff_coverage_failed: {type(exc).__name__}: {exc}"
        if coverage_error:
            # Block BEFORE the worktree may be removed and before any root hand-off
            # is presented as authoritative.
            job.status = JOB_BLOCKED
            job.error = coverage_error
            job.finished_at = ""
            job.result_diff_path = ""
            job.result_diff_sha256 = ""
            job.result_diff_size_bytes = 0
            try:
                (job_root / "result.diff").unlink()
            except OSError:
                pass

    try:
        W.snapshot(handle)
        job.worktree_head = handle.head_commit
        if not coverage_error:
            info = W.write_tree_diff(
                handle, job.job_initial_tree, W.write_tree(handle),
                job_root / "result.diff",
            )
            job.result_diff_path = "result.diff"
            job.result_diff_sha256 = info["sha256"]
            job.result_diff_size_bytes = info["size_bytes"]
            job.result_diff_error = ""
    except Exception as exc:
        job.result_diff_error = f"{type(exc).__name__}: {exc}"

    if job.status == JOB_COMPLETED and not job.result_diff_error:
        try:
            res = W.remove(handle, keep_branch=True)      # never a merge
            job.worktree_cleanup_status = res["cleanup_status"]
            job.worktree_cleanup_error = res.get("cleanup_error", "")
        except Exception as exc:
            job.worktree_cleanup_status = "failed_recoverable"
            job.worktree_cleanup_error = f"{type(exc).__name__}: {exc}"
        if job.worktree_cleanup_status == "clean":
            # The hand-off is complete and verified: the checkpoints are obsolete.
            ref_err = _drop_checkpoint_refs(job)
            if ref_err:
                job.worktree_cleanup_error = (
                    f"checkpoint_ref_cleanup_failed: {ref_err}"
                )
    else:
        # Not finished, blocked by the coverage gate, or the hand-off could not be
        # persisted: the accepted changes are uncommitted and live ONLY in this
        # worktree. Keep it. A coverage block is an honest RETAIN (the diff was
        # writable, it just was not the reviewed work), not a storage failure.
        res = W.retain_for_recovery(
            handle, job.result_diff_error if job.result_diff_error else "")
        job.worktree_cleanup_status = (
            "failed_recoverable" if job.result_diff_error else "retained"
        )
        job.worktree_cleanup_error = (
            coverage_error or res.get("cleanup_error", "")
        )
    _persist_job(job)


# ---------------------------------------------------------------------------
# Target repo snapshot guard (Step 4837)
# ---------------------------------------------------------------------------

def _snapshot_target_repo(repo_path: str) -> dict[str, bytes]:
    """Snapshot target repo for mutation detection. Reuses pingpong logic."""
    from packages.orchestration.pingpong_loop import _snapshot_target
    return _snapshot_target(Path(repo_path))


def _check_target_repo_guard(
    repo_path: str,
    before_snap: dict[str, bytes],
) -> TargetGuard:
    """Check if target repo was mutated since snapshot."""
    from packages.orchestration.pingpong_loop import _classify_target_changes
    content, operational, noise = _classify_target_changes(
        Path(repo_path), before_snap
    )
    return TargetGuard(
        target_mutated=bool(content),
        target_content_mutated=bool(content),
        target_operational_artifacts_changed=bool(operational),
        target_noise_changed=bool(noise),
        changed_target_files=content,
        ignored_operational_artifacts=operational,
        ignored_target_noise_files=noise,
    )


# ---------------------------------------------------------------------------
# Strict workspace apply (Steps 4835-4836)
# ---------------------------------------------------------------------------

def _is_unsafe_path(rel_path: str) -> str:
    """Check if a relative path is unsafe for workspace apply.

    Returns empty string if safe, or a reason string if unsafe.
    """
    # Absolute paths
    if os.path.isabs(rel_path):
        return f"absolute_path: {rel_path}"

    # Path traversal
    normalized = os.path.normpath(rel_path)
    if normalized.startswith("..") or normalized.startswith("/"):
        return f"path_traversal: {rel_path}"

    parts = Path(rel_path).parts
    for part in parts:
        # .env files
        if part == ".env" or part.startswith(".env.") or part.startswith(".env-"):
            return f"env_file: {rel_path}"
        # .git directory
        if part == ".git":
            return f"git_directory: {rel_path}"
        # Unsafe directories
        if part in _UNSAFE_DIRS:
            return f"unsafe_directory: {rel_path}"

    # Private key files
    suffix = Path(rel_path).suffix.lower()
    if suffix in _UNSAFE_EXTENSIONS:
        return f"private_key_file: {rel_path}"

    return ""


def _sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    try:
        h.update(path.read_bytes())
    except OSError:
        return ""
    return h.hexdigest()


def _verify_in_place_apply(
    task: TaskEntry,
    result: Any,
    workspace_path: str,
    handle: Any,
    initial_tree: str,
    *,
    job_baselines: dict[str, tuple[bool, str]] | None = None,
) -> ApplyManifest:
    """Manifest for a task that ran INSIDE the job-owned worktree.

    Nothing is copied: the accepted changes are already in the workspace, which is
    exactly what lets the next task see them. Every changed path is still validated
    (no traversal, no symlink, regular file, contained in the workspace) and still
    gets a baseline proof — the baseline comes from the job's INITIAL tree, so it
    is the state before the job started, not the state after this task ran.
    """
    from packages.orchestration import worktrees as W

    manifest = ApplyManifest(task_id=task.task_id, run_id=result.run_id)
    if job_baselines is None:
        job_baselines = {}

    workspace = Path(workspace_path)
    if not workspace.exists():
        manifest.status = "blocked"
        manifest.missing_files = ["(workspace directory missing)"]
        return manifest
    workspace_resolved = workspace.resolve()

    staged_files = list(result.staged_files)
    seen: set[str] = set()
    for rel in staged_files:
        if rel in seen:
            manifest.duplicate_files.append(rel)
        seen.add(rel)
    if manifest.duplicate_files:
        manifest.status = "blocked"
        return manifest

    for rel_path in staged_files:
        unsafe_reason = _is_unsafe_path(rel_path)
        if unsafe_reason:
            manifest.unsupported_files.append(f"{rel_path} ({unsafe_reason})")
            continue

        dst = workspace / rel_path
        if dst.is_symlink():
            manifest.unsupported_files.append(f"{rel_path} (workspace_dest_is_symlink)")
            continue
        if not dst.exists():
            manifest.missing_files.append(rel_path)
            continue
        if not dst.is_file():
            manifest.unsupported_files.append(
                f"{rel_path} (workspace_dest_not_regular_file)")
            continue
        try:
            resolved = dst.resolve()
        except OSError:
            manifest.unsupported_files.append(f"{rel_path} (workspace_dest_resolve_failed)")
            continue
        if not str(resolved).startswith(str(workspace_resolved) + os.sep):
            manifest.unsupported_files.append(
                f"{rel_path} (workspace_dest_escapes_workspace)")
            continue

        if rel_path not in job_baselines:
            blob = W.blob_at(handle, initial_tree, rel_path) if initial_tree else None
            existed = blob is not None
            baseline_hash = hashlib.sha256(blob).hexdigest() if existed else ""
            job_baselines[rel_path] = (existed, baseline_hash)

        manifest.applied_files.append(rel_path)
        existed_before, baseline_hash = job_baselines[rel_path]
        # The reviewed change includes the git file mode. A promotion that copies
        # only the bytes would silently drop a chmod, so the mode is proven here.
        baseline_mode = (
            W.mode_at(handle, initial_tree, rel_path) if initial_tree else ""
        )
        manifest.applied_file_proofs.append(AppliedFileProof(
            path=rel_path,
            existed_before_job=existed_before,
            baseline_sha256=baseline_hash,
            final_workspace_sha256=_sha256_of(dst),
            task_id=task.task_id,
            run_id=result.run_id,
            baseline_mode=baseline_mode,
            final_mode=W.file_mode(dst),
        ))

    blocked = (manifest.missing_files or manifest.unsupported_files
               or manifest.unexpected_files or manifest.duplicate_files)
    manifest.status = "blocked" if blocked else "applied"
    return manifest


def _strict_apply_to_workspace(
    task: TaskEntry,
    result: Any,
    workspace_path: str,
    *,
    job_baselines: dict[str, tuple[bool, str]] | None = None,
) -> ApplyManifest:
    """Strict workspace apply with full manifest and baseline proof.

    Every staged file must be accounted for. Missing, duplicate, traversal,
    and unsafe paths block the apply.

    job_baselines tracks first-seen baseline per path across tasks.
    Key: rel_path, Value: (existed_before_job, baseline_sha256).
    """
    manifest = ApplyManifest(
        task_id=task.task_id,
        run_id=result.run_id,
    )

    if job_baselines is None:
        job_baselines = {}

    staging_path = result.staging_path
    if not staging_path or not workspace_path:
        manifest.status = "blocked"
        manifest.missing_files = ["(no staging or workspace path)"]
        return manifest

    staging = Path(staging_path)
    workspace = Path(workspace_path)

    if not staging.exists():
        manifest.status = "blocked"
        manifest.missing_files = ["(staging directory missing)"]
        return manifest

    if not workspace.exists():
        manifest.status = "blocked"
        manifest.missing_files = ["(workspace directory missing)"]
        return manifest

    staged_files = list(result.staged_files)

    # Check for duplicates
    seen: set[str] = set()
    for rel in staged_files:
        if rel in seen:
            manifest.duplicate_files.append(rel)
        seen.add(rel)

    if manifest.duplicate_files:
        manifest.status = "blocked"
        return manifest

    # Validate and apply each file
    staging_resolved = staging.resolve()
    workspace_resolved = workspace.resolve()

    for rel_path in staged_files:
        unsafe_reason = _is_unsafe_path(rel_path)
        if unsafe_reason:
            manifest.unsupported_files.append(f"{rel_path} ({unsafe_reason})")
            continue

        src = staging / rel_path

        # --- Source containment: staging ---
        if src.is_symlink():
            manifest.unsupported_files.append(
                f"{rel_path} (staging_source_is_symlink)")
            continue

        if not src.exists():
            manifest.missing_files.append(rel_path)
            continue

        if not src.is_file():
            manifest.unsupported_files.append(
                f"{rel_path} (staging_source_not_regular_file)")
            continue

        src_parent = src.parent
        while src_parent != staging and src_parent != src_parent.parent:
            if src_parent.is_symlink():
                manifest.unsupported_files.append(
                    f"{rel_path} (staging_source_parent_symlink)")
                break
            src_parent = src_parent.parent
        else:
            src_parent = None
        if src_parent is not None:
            continue

        try:
            src_resolved = src.resolve()
        except OSError:
            manifest.unsupported_files.append(
                f"{rel_path} (staging_source_resolve_failed)")
            continue

        if not str(src_resolved).startswith(
            str(staging_resolved) + os.sep
        ) and src_resolved != staging_resolved:
            manifest.unsupported_files.append(
                f"{rel_path} (staging_source_escapes_staging)")
            continue

        # --- Destination containment: workspace ---
        dst = workspace / rel_path

        if dst.is_symlink():
            manifest.unsupported_files.append(
                f"{rel_path} (workspace_dest_is_symlink)")
            continue

        try:
            resolved_dst = dst.resolve()
            if not str(resolved_dst).startswith(
                str(workspace_resolved) + os.sep
            ) and resolved_dst != workspace_resolved:
                manifest.unsupported_files.append(
                    f"{rel_path} (workspace_dest_escapes_workspace)")
                continue
        except (OSError, ValueError):
            manifest.unsupported_files.append(
                f"{rel_path} (workspace_dest_resolve_failed)")
            continue

        dst_parent = dst.parent
        while dst_parent != workspace and dst_parent != dst_parent.parent:
            if dst_parent.exists() and dst_parent.is_symlink():
                manifest.unsupported_files.append(
                    f"{rel_path} (workspace_dest_parent_symlink)")
                break
            dst_parent = dst_parent.parent
        else:
            dst_parent = None
        if dst_parent is not None:
            continue

        # Capture baseline before first modification to this path
        # Do not hash through symlinks — dst already verified non-symlink above
        if rel_path not in job_baselines:
            existed = dst.exists()
            baseline_hash = _sha256_of(dst) if existed else ""
            job_baselines[rel_path] = (existed, baseline_hash)

        # Recheck containment immediately before copy (defense-in-depth)
        if src.is_symlink():
            manifest.unsupported_files.append(
                f"{rel_path} (staging_source_is_symlink_at_copy)")
            continue
        if dst.is_symlink():
            manifest.unsupported_files.append(
                f"{rel_path} (workspace_dest_is_symlink_at_copy)")
            continue

        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            content = src.read_bytes()
            dst.write_bytes(content)
            manifest.applied_files.append(rel_path)
        except OSError as exc:
            manifest.unexpected_files.append(f"{rel_path} (copy failed: {exc})")
            continue

        # Capture final workspace hash — dst verified non-symlink above
        final_hash = _sha256_of(dst)
        existed_before, baseline_hash = job_baselines[rel_path]
        manifest.applied_file_proofs.append(AppliedFileProof(
            path=rel_path,
            existed_before_job=existed_before,
            baseline_sha256=baseline_hash,
            final_workspace_sha256=final_hash,
            task_id=task.task_id,
            run_id=result.run_id,
        ))

    # Block if any files were not applied
    if manifest.missing_files or manifest.unsupported_files or manifest.unexpected_files:
        manifest.status = "blocked"
    else:
        manifest.status = "applied"

    # Clean up staging on success
    if manifest.status == "applied" and staging.exists():
        shutil.rmtree(staging, ignore_errors=True)

    return manifest


# ---------------------------------------------------------------------------
# Deterministic job task completion gate (Step 4857)
# ---------------------------------------------------------------------------

def validate_job_task_result(result: Any) -> tuple[bool, list[str]]:
    """Validate a ping-pong result before applying to job workspace.

    Does NOT rely solely on final_status. Independently checks test results,
    reviewer verdict, findings, target mutation, and staging path consistency.

    Returns (ok, reasons). If ok is False, reasons lists all failures.
    """
    reasons: list[str] = []

    if result.final_status != "staged_review_passed":
        reasons.append(f"final_status={result.final_status}")

    if result.target_mutated:
        reasons.append("target_mutated=True")

    # Check final test result and reviewer evidence from last round
    if result.rounds:
        last_round = result.rounds[-1]
        if last_round.test_passed is False:
            reasons.append("test_passed=False")
        if last_round.reviewer_output:
            ro = last_round.reviewer_output
            if ro.verdict != "pass":
                reasons.append(f"reviewer_verdict={ro.verdict}")
            if ro.verdict == "pass" and ro.findings:
                reasons.append(
                    f"reviewer_pass_with_{len(ro.findings)}_findings"
                )
        else:
            reasons.append("missing_reviewer_output")
    else:
        reasons.append("no_rounds")

    # Staging path must exist when staged files need apply
    if result.staged_files:
        staging = Path(result.staging_path) if result.staging_path else None
        if staging is None or not staging.exists():
            reasons.append("staging_path_missing")

    return (len(reasons) == 0, reasons)


# The recorded provider must NAME WHAT ACTUALLY RAN: a literal default made an
# unflagged run report a provider it never used (finding R-0768). One function so
# ``run_job``'s own precedence chain stops being a rival answer to role_config's.
def default_role_provider_name(role: str, injected_provider: Any = None) -> str:
    """Return the provider name to record for ``role`` when nothing was given.

    Used as ``_resolve_cfg``'s product default, i.e. only when neither an
    explicit CLI value nor a persisted one exists. An INJECTED provider object
    wins, because that object is what will really run; otherwise the answer
    comes from ``role_config``, the single seam that owns provider defaults.

    ``role_config`` is imported inside the body on purpose: this module has no
    module-level import of it, and adding one risks an import cycle.
    """
    if injected_provider is not None:
        name = getattr(injected_provider, "name", None)
        if isinstance(name, str) and name:
            return name

    from packages.orchestration import role_config

    return role_config.resolve_role_config(role).provider


def _resolve_cfg(cli_val: Any, persisted_val: Any, default: Any) -> tuple[Any, str]:
    """Resolve config field: explicit CLI > persisted > product default."""
    if cli_val is not None:
        return cli_val, "cli"
    if persisted_val is not None:
        return persisted_val, "persisted"
    return default, "default"


# Answers "which task would run next, and with what prior context" for anyone
# who needs the F104 prediction WITHOUT running the job — today `remedy job
# budget`. One function so the read-only inspector and `run_job`'s task-dispatch
# safe point can never drift into predicting against different tasks.
def select_next_predictable_task(job) -> tuple[object | None, list]:
    """Return ``(next_task, previous_summaries)`` for a persisted job plan.

    The rule is EXACTLY the one ``run_job``'s dispatch loop applies:

    * ``previous_summaries`` collects the ``proof_summary`` of every task that
      is ``TASK_APPLIED`` or ``TASK_PASSED`` and actually carries one, in task
      order — the same list the loop pre-fills before its first dispatch.
    * ``next_task`` is the first task the loop would not ``continue`` past, i.e.
      the first whose status is not applied/passed/skipped. If that task is
      ``TASK_BLOCKED`` or ``TASK_FAILED`` the loop ``break``s instead of
      dispatching, so there is no next task and None is returned.

    Pure and NEVER raises: it is read by a read-only CLI over possibly-legacy
    job files, where a missing attribute must degrade rather than kill an
    inspection command. Every degradation returns ``(None, [])``.
    """
    try:
        tasks = list(getattr(job, "tasks", None) or ())
        # Pass 1 — the SAME pre-fill the loop does over EVERY task, not only the
        # ones before the next pending one: a later completed task still feeds
        # its proof summary into the context of an earlier pending task.
        summaries: list = [
            t.proof_summary for t in tasks
            if getattr(t, "status", None) in (TASK_APPLIED, TASK_PASSED)
            and getattr(t, "proof_summary", None)
        ]
        # Pass 2 — the first task the loop would not `continue` past. If the loop
        # would `break` on it instead of dispatching, there is no next task.
        next_task = None
        for task in tasks:
            status = getattr(task, "status", None)
            if status in (TASK_APPLIED, TASK_PASSED, TASK_SKIPPED, TASK_SPLIT):
                continue
            if status not in (TASK_BLOCKED, TASK_FAILED):
                next_task = task
            break
        return next_task, summaries
    except Exception:
        return None, []


# ---------------------------------------------------------------------------
# F033: the operator's recorded hunk decision, on its way to the next prompt
# ---------------------------------------------------------------------------

def _recorded_hunk_ledger_for_task(job: Any, task: Any):
    """The ledger of ``task``'s LATEST recorded hunk decision, read off ``job.metadata``.

    THIS IS THE LAST HOP of F033's rejected-hunks route. ``hunk_decision_record.py`` writes
    each decision onto ``job.metadata`` and ``run_pingpong`` forwards a ``hunk_ledger`` into
    ``compose_builder_prompt``, but this module is the only place that holds BOTH the job and
    the task, so the lookup that joins them belongs here. It is a NAMED function rather than an
    inline expression at the call site so that it can be TESTED: that call site is reached only
    by a full job run, so an inline form would be provable only by its shape, and a gate over a
    call's shape is not a gate over its truth.

    IT LOOKS UP TASK-SCOPED DECISIONS ONLY, deliberately. A decision the operator takes at JOB
    scope is recorded under ``diff_view_source.DIFF_SCOPE_JOB`` — the literal ``"job"`` — rather
    than under a task id, and is therefore NOT quoted into any one task's prompt, because it was
    never attributed to one. That separation rests on the id comparison alone, so it admits
    exactly one collision, said here rather than left for a reader to find: a task whose own
    ``task_id`` were literally ``"job"`` WOULD match a job-scoped record. No guard against it is
    added here — keeping the sentinel and the task-id space apart is the RECORDING door's to do,
    and a guard here would put that one decision in two places.

    TOTAL — a job with no usable ``metadata``, or a task with no usable ``task_id``, yields an
    EMPTY ledger and raises nothing. THE ONE ``try`` BELOW IS THE WHOLE STRUCTURAL GUARD and
    there is deliberately no second one nested inside it, for the reason
    ``load_latest_hunk_ledger_from_metadata`` gives about its own: a redundant inner layer makes
    the outer one unobservable, and a guard no test can redden is a guard nobody knows is there.

    AN EMPTY LEDGER IS THE HONEST ANSWER to "this task recorded no decision at all". It is not
    an error, and it is indistinguishable from an unreadable job ON PURPOSE: to a prompt the two
    mean the same thing — there is nothing of the operator's to quote.
    """
    from packages.orchestration.hunk_decision_record import (
        load_latest_hunk_ledger_from_metadata,
    )
    from packages.orchestration.hunk_ledger import HunkDecisionLedger

    try:
        return load_latest_hunk_ledger_from_metadata(
            job.metadata,
            task_id=task.task_id,
        )
    except Exception:
        return HunkDecisionLedger(())


# ---------------------------------------------------------------------------
# Sequential job runner (Steps 4829-4830, 4837-4838, 4857-4869)
# ---------------------------------------------------------------------------

def run_job(
    job_id: str,
    *,
    builder_name: str | None = None,
    reviewer_name: str | None = None,
    builder_provider: Any = None,
    reviewer_provider: Any = None,
    builder_model: str | None = None,
    builder_effort: str | None = None,
    reviewer_model: str | None = None,
    reviewer_effort: str | None = None,
    repair_provider_name: str | None = None,
    repair_model: str | None = None,
    repair_effort: str | None = None,
    max_rounds: int | None = None,
    repair_rounds: int | None = None,
    repair_rounds_source: str | None = None,
    test_command: str | None = None,
    timeout_sec: int | None = None,
    timeout_profile: str | None = None,
    max_output_chars: int | None = None,
    claude_cli_write_mode: str | None = None,
    stream_evidence: bool | None = None,
    max_tasks: int | None = None,
    budgets: dict | None = None,
) -> JobPlan:
    """Execute pending tasks sequentially through the ping-pong loop.

    Each task runs Builder → tests → Reviewer → repair. If a task passes,
    its staged result is strictly applied into the job workspace. If any task
    fails, the job is blocked and execution stops.

    The real target repo is never mutated — a snapshot guard verifies this
    after each task.

    None parameters mean "omitted by caller". Resolution order:
    explicit CLI value > persisted config > product default.
    """
    from packages.orchestration.pingpong_loop import (
        TaskInput,
        run_pingpong,
    )

    job = load_job_plan(job_id)
    if job is None:
        return JobPlan(
            job_id=job_id,
            status=JOB_BLOCKED,
            error=f"job_not_found: {job_id}",
        )

    # F018 Scope 6: a stopped job with a pending operator stop signal must not silently
    # resume.  Check HERE — before config resolution, budget setup, or any timestamp —
    # so the guard lives in the run_job boundary, not only in the CLI.
    if job.status == JOB_STOPPED:
        from packages.orchestration.safe_points import (
            acknowledge_stop as _ack_guard,
        )
        from packages.orchestration.safe_points import (
            control_root as _cr_guard,
        )
        from packages.orchestration.safe_points import (
            stop_requested as _sr_guard,
        )
        _pending_guard = _sr_guard(job.job_id, control_root_path=_cr_guard())
        if _pending_guard is not None:
            if job.stop_request_id == _pending_guard.request_id:
                try:
                    _ack_guard(job.job_id, _pending_guard,
                               control_root_path=_cr_guard())
                except Exception:
                    pass
            else:
                job.error = (
                    f"stopped_job_has_pending_stop: {_pending_guard.reason} "
                    f"(request_id={_pending_guard.request_id})")
                _persist_job(job)
            return job

    if budgets is not None and job.status == JOB_STOPPED:
        job.error = (
            "stopped_budget_override_rejected: a stopped job's budget cannot be "
            "replaced via run_job; use the Decision workflow (extend/abandon)")
        _persist_job(job)
        return job

    if budgets is not None:
        job.budgets = budgets
        _persist_job(job)

    # Step 4869: Resolve each config field — explicit > persisted > default
    ec = job.execution_config

    builder_name, builder_src = _resolve_cfg(
        builder_name, ec.builder if ec else None,
        default_role_provider_name("builder", builder_provider))
    reviewer_name, reviewer_src = _resolve_cfg(
        reviewer_name, ec.reviewer if ec else None,
        default_role_provider_name("reviewer", reviewer_provider))
    max_rounds, max_rounds_src = _resolve_cfg(
        max_rounds, ec.max_rounds if ec else None, 3)
    test_command, test_cmd_src = _resolve_cfg(
        test_command, ec.test_command if ec else None, "")
    claude_cli_write_mode, write_mode_src = _resolve_cfg(
        claude_cli_write_mode,
        ec.claude_cli_write_mode if ec else None, "none")

    if repair_rounds is not None:
        rr_src = repair_rounds_source or "cli"
    elif ec is not None:
        repair_rounds = ec.repair_rounds_allowed
        rr_src = "persisted"
    else:
        repair_rounds = 2
        rr_src = "default"

    builder_model, bm_src = _resolve_cfg(
        builder_model, ec.builder_model if ec else None, "")
    builder_effort, be_src = _resolve_cfg(
        builder_effort, ec.builder_effort if ec else None, "")
    reviewer_model, rm_src = _resolve_cfg(
        reviewer_model, ec.reviewer_model if ec else None, "")
    reviewer_effort, re_src = _resolve_cfg(
        reviewer_effort, ec.reviewer_effort if ec else None, "")
    repair_provider_name, rp_src = _resolve_cfg(
        repair_provider_name, ec.repair_provider if ec else None, "")
    repair_model, rpm_src = _resolve_cfg(
        repair_model, ec.repair_model if ec else None, "")
    repair_effort, rpe_src = _resolve_cfg(
        repair_effort, ec.repair_effort if ec else None, "")

    # F3: resolve the invocation-level controls with an OMISSION SENTINEL (None). Only a value
    # the caller actually supplied (``passed is not None``) is an explicit invocation — so an
    # explicit value that happens to equal the product default STILL overrides a persisted one,
    # and an omitted flag never masquerades as an explicit default. Precedence is strictly
    # explicit(non-None) > persisted > product default, mirroring ``_resolve_cfg``.
    def _resolve_inv(passed: Any, default: Any, persisted: Any):
        if passed is not None:
            return passed, "invocation"
        if persisted is not None:
            return persisted, "persisted"
        return default, "default"

    _ts, _ts_src = _resolve_inv(timeout_sec, 120, ec.timeout_sec if ec else None)
    _tp, _tp_src = _resolve_inv(timeout_profile, "", ec.timeout_profile if ec else None)
    _moc, _moc_src = _resolve_inv(max_output_chars, 50000,
                                  ec.max_output_chars if ec else None)
    _se, _se_src = _resolve_inv(stream_evidence, False, ec.stream_evidence if ec else None)
    _mt, _mt_src = _resolve_inv(max_tasks, 0, ec.max_tasks if ec else None)

    # F2: from here on the ONLY values that exist are the RESOLVED ones. Rebind the canonical
    # locals so every downstream use — the task cap, the provider kwargs, the stream-evidence
    # switch, the reports and the manifest — executes exactly what was recorded. There is no
    # second, un-resolved variable that the runner could accidentally use instead.
    timeout_sec, timeout_profile, max_output_chars = _ts, _tp, _moc
    stream_evidence, max_tasks = _se, _mt

    job.execution_config = ExecutionConfig(
        builder=builder_name,
        builder_source=builder_src,
        reviewer=reviewer_name,
        reviewer_source=reviewer_src,
        builder_model=builder_model,
        builder_model_source=bm_src,
        builder_effort=builder_effort,
        builder_effort_source=be_src,
        reviewer_model=reviewer_model,
        reviewer_model_source=rm_src,
        reviewer_effort=reviewer_effort,
        reviewer_effort_source=re_src,
        repair_provider=repair_provider_name,
        repair_provider_source=rp_src,
        repair_model=repair_model,
        repair_model_source=rpm_src,
        repair_effort=repair_effort,
        repair_effort_source=rpe_src,
        max_rounds=max_rounds,
        max_rounds_source=max_rounds_src,
        repair_rounds_allowed=repair_rounds,
        repair_rounds_source=rr_src,
        test_command=test_command,
        test_command_source=test_cmd_src,
        claude_cli_write_mode=claude_cli_write_mode,
        claude_cli_write_mode_source=write_mode_src,
        timeout_sec=_ts, timeout_sec_source=_ts_src,
        timeout_profile=_tp, timeout_profile_source=_tp_src,
        max_output_chars=_moc, max_output_chars_source=_moc_src,
        stream_evidence=_se, stream_evidence_source=_se_src,
        max_tasks=_mt, max_tasks_source=_mt_src,
    )

    # Record repair-round metadata at job level
    job.repair_rounds_allowed = repair_rounds
    job.repair_rounds_source = rr_src

    # F012/F1: mark the job as manifest-required now, but capture the typed episode-start
    # snapshot only once the active episode id exists and is bound to it (below).
    _mark_manifest_required(job)

    # F011 SAFE POINT ZERO — before ANY work. The job is loaded and its config resolved;
    # nothing has been acquired, locked, snapshotted or mutated. A stop that was already
    # pending is honoured HERE, so it can never be overtaken by a worktree lock failure
    # (which is what happened in the reviewed build: the job came out `blocked` with the
    # stop still sitting on disk).
    #
    # Binding the control root resolves a path. It creates nothing, and it touches neither
    # the repository nor the workspace.
    from packages.orchestration.safe_points import StopSignal as _StopSignal
    from packages.orchestration.safe_points import control_root as _control_root
    from packages.orchestration.safe_points import should_stop as _should_stop
    _control = _control_root()

    # F018: seed accumulators from persisted budget_actuals on resume.
    # A stopped-then-resumed job must NOT reset counters to zero.
    # Strict decode — corrupt persisted actuals block, never coerce.
    _prior_raw = getattr(job, "budget_actuals", None) or {}
    _prior_validated: dict[str, Any] = {}
    if _prior_raw:
        from packages.orchestration.budget_guard import (
            decode_persisted_budget_actuals as _decode_actuals,
        )
        _fra_for_check = getattr(job, "first_running_at", "") or None
        _prior_validated = _decode_actuals(
            _prior_raw, first_running_at=_fra_for_check)
    _accumulated_provider_calls = _prior_validated.get("provider_call_count", 0)
    _accumulated_tokens = _prior_validated.get("total_tokens", 0)
    _accumulated_measured = _prior_validated.get("actual_call_count", 0)
    _accumulated_unmeasured = _accumulated_provider_calls - _accumulated_measured
    # F018 Scope 7: compute _run_started_at from persisted first_running_at on resume.
    # Invalid or timezone-naive values block — never silently become now().
    _run_started_at = datetime.now(timezone.utc)
    _first_run_already_set = bool(getattr(job, "first_running_at", ""))
    if _first_run_already_set:
        _fra_raw = job.first_running_at
        try:
            _fra_parsed = datetime.fromisoformat(_fra_raw)
        except (ValueError, TypeError) as _fra_exc:
            job.status = JOB_BLOCKED
            job.error = (
                f"corrupt_first_running_at: cannot parse {_fra_raw!r}: {_fra_exc}")
            _persist_job(job)
            return job
        if _fra_parsed.tzinfo is None:
            job.status = JOB_BLOCKED
            job.error = (
                f"corrupt_first_running_at: timezone-naive value {_fra_raw!r}")
            _persist_job(job)
            return job
        _run_started_at = _fra_parsed

    # F018: reconstruct JobBudgets from the persisted dict once (reused by _stop_check).
    # A malformed persisted budget MUST block — never silently continue as unlimited.
    _job_budgets = None
    if job.budgets is not None:
        from packages.core.models import JobBudgets as _JobBudgets
        try:
            _job_budgets = _JobBudgets.model_validate(job.budgets)
        except Exception as _budget_exc:
            job.status = JOB_BLOCKED
            job.error = f"corrupt_budget_state: {_budget_exc}"
            _write_job_postmortem_record(job, _budget_exc)
            _persist_job(job)
            return job

    # F104: the predictive inputs (price basis + class defaults) are OPERATOR
    # config, so they are read once per run, not once per safe point. Resolved
    # only when a money limit exists — with no `max_cost_usd` there is nothing
    # to predict against and every existing path stays byte for byte unchanged.
    _predictive_config = None
    if _job_budgets is not None and _job_budgets.max_cost_usd is not None:
        try:
            from packages.orchestration.budget_resolution import (
                resolve_predictive_budget_config as _resolve_predictive_config,
            )
            _predictive_config = _resolve_predictive_config(
                project_root=job.repo_path or None)
        except Exception:
            # A config read must never block a healthy job: with no config the
            # predictive path is inert and the reactive check still enforces.
            import logging as _logging
            _logging.getLogger(__name__).error(
                "predictive budget config read FAILED for job %r; the predictive "
                "check is disabled for this run and the reactive budget check "
                "continues to enforce every limit",
                job.job_id, exc_info=True,
            )
            _predictive_config = None

    def _on_provider_call(attempt):
        nonlocal _accumulated_provider_calls, _accumulated_tokens
        nonlocal _accumulated_measured, _accumulated_unmeasured
        if getattr(attempt, "provider", "fake") == "fake":
            return
        _accumulated_provider_calls += 1
        ua = getattr(attempt, "usage_actuals", None)
        if ua is not None:
            _accumulated_measured += 1
            _accumulated_tokens += (
                getattr(ua, "input_tokens", 0) +
                getattr(ua, "output_tokens", 0)
            )
        else:
            _accumulated_unmeasured += 1

    def _build_budget_counters():
        """The counters this safe point evaluates against — built ONCE per check.

        Extracted so the reactive check and the F104 predictive check read the
        same numbers from the same ledger query: two reads could disagree, and a
        prediction that disagrees with the backstop it is supposed to precede is
        worse than no prediction.
        """
        from packages.orchestration.budget_guard import collect_counters_from_actuals
        _actuals = {
            "provider_call_count": _accumulated_provider_calls,
            "actual_call_count": _accumulated_measured,
            "total_tokens": _accumulated_tokens,
        }
        _sources = ("pingpong_live",) if _accumulated_measured > 0 else ()
        counters = None
        # F104: a `--max-cost-usd` limit is only enforceable if the guard knows what
        # the job has really cost, and the F103 ledger is the only place a real
        # provider cost figure lives. Skipped entirely when no cost limit is set —
        # a SQLite query per safe point for a limit nobody configured is waste, and
        # skipping keeps every existing budget path byte for byte unchanged.
        if _job_budgets is not None and _job_budgets.max_cost_usd is not None:
            # WHY the swallow: budgets read a MIRROR — the ledger reflects evidence
            # files that are already the source of truth — and a broken mirror must
            # never stop a healthy job. Any failure leaves the cost UNMEASURED
            # (None, never 0.0 — P6) and the token/call/time limits still enforce.
            try:
                from packages.orchestration.budget_guard import (
                    collect_ledger_cost_for_job as _collect_ledger_cost,
                )
                from packages.orchestration.job_evidence import (
                    _resolve_job_ledger_project_id as _resolve_ledger_project,
                )

                # The SAME resolver the write side uses, so the read and the write
                # can never disagree about which project's ledger this job owns.
                _ledger_project = _resolve_ledger_project(job)
                if _ledger_project is not None:
                    # All THREE ledger figures travel together: the priced count
                    # is what the cost side validates against, so discarding it
                    # is what made R-0224 (DECISION F104 D5).
                    _ledger_cost, _ledger_priced, _ledger_unpriced = _collect_ledger_cost(
                        job_id=job.job_id, project_id=_ledger_project)
                    counters = collect_counters_from_actuals(
                        _actuals,
                        started_at=_run_started_at,
                        actual_sources=_sources,
                        measured_cost_usd=_ledger_cost,
                        unpriced_call_count=_ledger_unpriced,
                        priced_call_count=_ledger_priced,
                    )
            except Exception:
                import logging as _logging
                _logging.getLogger(__name__).error(
                    "budget ledger cost read FAILED for job %r; the cost stays "
                    "unmeasured for this safe point and the run continues (the "
                    "evidence files remain the source of truth and the remaining "
                    "budget limits are unaffected)",
                    job.job_id, exc_info=True,
                )
                counters = None
        if counters is None:
            counters = collect_counters_from_actuals(
                _actuals,
                started_at=_run_started_at,
                actual_sources=_sources,
            )
        return counters

    def _stop_check(*, next_task=None, previous_summaries=()):
        counters = _build_budget_counters()
        result = _should_stop(
            job.job_id,
            budgets=_job_budgets,
            counters=counters,
            control_root_path=_control,
        )
        if not result.should_stop:
            # F104: neither the operator stop nor the REACTIVE budget check fired,
            # so — and only so — ask whether the NEXT task would breach the money
            # limit. The predictive check runs LAST on purpose: it never replaces
            # the backstop, it only ever stops EARLIER than the backstop would.
            if (
                next_task is not None
                and _job_budgets is not None
                and _job_budgets.max_cost_usd is not None
                and _predictive_config is not None
            ):
                # WHY the swallow: a prediction is an ESTIMATE, and a broken
                # estimate must never stop a healthy job. Any failure here leaves
                # the run going with the reactive check still enforcing every limit.
                try:
                    from packages.orchestration.budget_guard import (
                        derive_next_task_token_band as _derive_band,
                    )
                    from packages.orchestration.budget_guard import (
                        predict_next_task_cost as _predict_cost,
                    )
                    _prediction = _predict_cost(
                        _job_budgets,
                        counters,
                        band=_derive_band(next_task, previous_summaries),
                        config=_predictive_config,
                    )
                    if _prediction.would_breach:
                        # The arithmetic is persisted BEFORE the stop so a human
                        # reading job.json sees WHY no work was done.
                        job.budget_prediction = _prediction.to_json()
                        # One possible limit on this path; the reactive path
                        # derives its name from first_exhausted_limit instead.
                        _pred_reason = f"predicted_budget_exhausted:{'max_cost_usd'}"
                        import hashlib as _phl
                        _pred_episode = getattr(job, "active_episode_id", "") or ""
                        _pred_id = _phl.sha256(
                            f"{job.job_id}:{_pred_episode}:{_pred_reason}".encode()
                        ).hexdigest()[:16]
                        return _StopSignal(
                            job_id=job.job_id,
                            request_id=f"budget_{_pred_id}",
                            reason=_pred_reason,
                            source="budget",
                        )
                except Exception:
                    import logging as _logging
                    _logging.getLogger(__name__).error(
                        "predictive budget check FAILED for job %r; the run "
                        "continues and the reactive budget check still enforces "
                        "every configured limit",
                        job.job_id, exc_info=True,
                    )
                    return None
            return None
        if result.source == "operator":
            return result.operator_signal
        import hashlib as _hl
        _episode = getattr(job, "active_episode_id", "") or ""
        _budget_id = _hl.sha256(
            f"{job.job_id}:{_episode}:{result.reason}".encode()).hexdigest()[:16]
        return _StopSignal(
            job_id=job.job_id,
            request_id=f"budget_{_budget_id}",
            reason=result.reason,
            source="budget",
        )

    def _persist_budget_actuals():
        """Persist live counters so they survive stop/resume.

        Actual_sources preserves the original measurement sources from prior runs
        and adds "pingpong_live" only when this run measured new calls. Resume is
        a lifecycle state, not a measurement source.
        """
        _sources: set[str] = set()
        _prior_src = _prior_validated.get("actual_sources", ()) if _prior_validated else ()
        if isinstance(_prior_src, (list, tuple)):
            _sources.update(s for s in _prior_src if isinstance(s, str))
        if _accumulated_measured > _prior_validated.get("actual_call_count", 0) if _prior_validated else _accumulated_measured > 0:
            _sources.add("pingpong_live")
        _sources.discard("persisted_resume")
        job.budget_actuals = {
            "schema_version": "1.0.0",
            "provider_call_count": _accumulated_provider_calls,
            "actual_call_count": _accumulated_measured,
            "total_tokens": _accumulated_tokens,
            "started_at": _run_started_at.isoformat(),
            "actual_sources": tuple(sorted(_sources)),
            "unmeasured_call_count": _accumulated_unmeasured,
        }

    # F018: allocate episode BEFORE computing budget identity so the stop
    # request_id is stable across finalization failures.
    if not job.active_episode_id:
        job.active_episode_id = mint_episode_id()

    # Deliberately argument-free: there is no "next task" before the episode loop,
    # and inventing one would predict against a task that may never be reached.
    _pre_stop = _stop_check()
    if _pre_stop is not None:
        if not _episode_snapshot_bound_ok(job):
            _capture_input_snapshot(job, phase=_PHASE_PRE_WORK_STOP)
        _persist_budget_actuals()
        _persist_job(job)
        try:
            return _stop_job(job, _pre_stop, task=None, control_root_path=_control)
        except StopFinalizationError:
            return job

    # F018 Scope 7: all pre-work validation passed (budget decoded, no pending stop).
    # NOW stamp first_running_at so it's never set on a job that blocked before running.
    if not _first_run_already_set:
        job.first_running_at = _run_started_at.isoformat()

    # F012: no pending pre-work stop — this is a real execution EPISODE. Allocate a fresh
    # episode id now (a resume gets its own episode; only calls made in THIS episode are
    # collected into its manifest).
    job.active_episode_id = mint_episode_id()

    # F006: the job workspace IS a job-owned git worktree for a git target.
    # The runner owns the handle (and its lock) for the whole execution.
    job_handle = None
    try:
        job.job_workspace_path, job_handle = _acquire_job_workspace(job)
    except Exception as exc:
        # F010: the job died before ANY task could own the failure. A worktree lock is not
        # a pending task's fault, so it gets a JOB-scope post-mortem — with the typed
        # exception reaching the classifier intact, not stringified into anonymity.
        job.status = JOB_BLOCKED
        job.error = f"workspace_creation_failed: {exc}"
        _write_job_postmortem_record(job, exc)
        _persist_job(job)
        return job


    try:
        # Step 4837: Snapshot real target repo before any task runs
        target_snap = _snapshot_target_repo(job.repo_path)

        # F012 (F4): record the job-workspace tree at THIS episode's start. For a resume, it
        # already contains the work applied by earlier episodes, which is a material input.
        # F12: a FAILURE to capture it is a snapshot-capture failure — it is NEVER silently
        # substituted with an empty tree. The typed reason is folded into the snapshot wrapper.
        job.episode_start_workspace_tree = ""
        _ws_tree_problems: tuple[str, ...] = ()
        if job_handle is not None:
            try:
                from packages.orchestration import worktrees as _W
                job.episode_start_workspace_tree = _W.write_tree(job_handle)
            except Exception as exc:
                from packages.orchestration.failure_postmortem import safe_text
                job.episode_start_workspace_tree = ""
                _ws_tree_problems = (safe_text(
                    f"episode_start_workspace_tree capture failed: "
                    f"{type(exc).__name__}: {exc}")[:300],)

        # F012/F1: capture the typed episode-start snapshot now that the workspace is acquired
        # and the base identity (target_base_commit, job_initial_tree) is populated — this is
        # the stable, episode-bound snapshot the completed manifest consumes verbatim.
        _snap_wrapper = _capture_input_snapshot(
            job, phase=_PHASE_EPISODE_START, extra_problems=_ws_tree_problems)

        # F1/F12: VALIDATE the wrapper immediately. A failed or invalid mandatory snapshot is a
        # HARD BLOCK *before any task or provider call* — the job is set to a durable non-running
        # blocked state carrying the reason, persisted, and returned. Zero tasks run, zero
        # provider calls happen, and no false "completed" result is produced. The failure is
        # discovered HERE, not later at terminal manifest writing.
        _snap_block = _snapshot_block_reason(job, _snap_wrapper, phase=_PHASE_EPISODE_START)
        if _snap_block:
            job.status = JOB_BLOCKED
            job.input_snapshot_error = _snap_block
            job.error = f"episode_start_snapshot_failed: {_snap_block}"
            _persist_job(job)
            return job

        job.status = JOB_RUNNING
        _persist_job(job)

        tasks_run = 0
        previous_summaries: list[TaskProofSummary] = []
        job_baselines: dict[str, tuple[bool, str]] = {}

        # Collect existing proof summaries and baselines from already-done tasks
        for t in job.tasks:
            if t.proof_summary and t.status in (TASK_APPLIED, TASK_PASSED):
                previous_summaries.append(t.proof_summary)
            if t.apply_manifest:
                for proof in t.apply_manifest.applied_file_proofs:
                    if proof.path not in job_baselines:
                        job_baselines[proof.path] = (
                            proof.existed_before_job, proof.baseline_sha256,
                        )

        for idx, task in enumerate(job.tasks):
            if task.status in (TASK_APPLIED, TASK_PASSED, TASK_SKIPPED, TASK_SPLIT):
                continue

            if task.status in (TASK_BLOCKED, TASK_FAILED):
                break

            if max_tasks > 0 and tasks_run >= max_tasks:
                break

            # SAFE POINT — before dispatching a task. A stop that was requested while the
            # job was not running is consumed HERE, before any work begins: zero provider
            # calls, every task still pending.
            # F104: this is also the only place the PREDICTIVE check has a real next
            # task to predict against, so the task and the summaries that will feed
            # its context are handed over here and nowhere else.
            _stop = _stop_check(next_task=task, previous_summaries=previous_summaries)
            if _stop is not None:
                _persist_budget_actuals()
                _persist_job(job)
                try:
                    return _stop_job(job, _stop, task=None, control_root_path=_control)
                except StopFinalizationError:
                    return job

            # Build bounded task prompt
            task_prompt = _build_task_prompt(job, task, previous_summaries)

            task.status = TASK_RUNNING

            # F006 durable task checkpoint. The tree is captured BEFORE the first
            # provider call and persisted; a task that resumes after a crash keeps
            # its ORIGINAL start tree, so partial work written before the crash
            # stays inside this task's diff, review scope and apply manifest
            # instead of silently leaking into the final job hand-off unreviewed.
            if job_handle is not None:
                from packages.orchestration import worktrees as _W
                if not (task.task_start_tree and task.task_attempt_state == "active"):
                    task.task_start_tree = _W.write_tree(job_handle)
                    task.task_start_tree_ref = _W.checkpoint_ref(
                        job_worktree_id(job.job_id), "start", task.task_id)
                    _W.set_checkpoint_ref(
                        job.repo_path, task.task_start_tree_ref, task.task_start_tree)
                    task.task_start_recorded_at = datetime.now(timezone.utc).isoformat()
                task.task_attempt_state = "active"
            _persist_job(job)

            # Create TaskInput for ping-pong
            task_input = TaskInput(
                kind="job_task",
                path="",
                title=task.title,
                body=task_prompt,
                sha256=hashlib.sha256(task_prompt.encode()).hexdigest(),
                byte_count=len(task_prompt.encode()),
                char_count=len(task_prompt),
                tokens_estimated=len(task_prompt) // 4,
                excerpt=task_prompt[:200],
            )

            compiled_context_paths: list[str] | None = None
            compiled_context_candidates: list[str] | None = None
            compiled_context_token_budget: int | None = None
            if task.files_hint:
                from packages.orchestration.context_compiler import (
                    fit_task_context_to_class_cap,
                )
                fit_result = fit_task_context_to_class_cap(
                    Path(job.job_workspace_path),
                    task.files_hint,
                    task.files_hint,
                    task.task_class,
                )
                if fit_result.fits:
                    compiled_context_paths = list(task.files_hint)
                    compiled_context_candidates = list(task.files_hint)
                    compiled_context_token_budget = fit_result.cap_tokens
                else:
                    from packages.orchestration.escalation import (
                        auto_apply_safe_default,
                        enqueue_task_decision,
                    )
                    from packages.orchestration.task_granularity import (
                        split_one_task,
                    )
                    decision = enqueue_task_decision(
                        job,
                        task_id=task.task_id,
                        question="task context exceeds its class cap",
                        options=["split task"],
                        safe_default="split task",
                        impact=(
                            f"tier1_tokens={fit_result.tier1_tokens} "
                            f"cap_tokens={fit_result.cap_tokens} "
                            f"task_class={fit_result.task_class}"
                        ),
                        now=datetime.now(timezone.utc),
                    )
                    answered = auto_apply_safe_default(
                        job, decision, now=datetime.now(timezone.utc))
                    split_entries: list[TaskEntry] = []
                    if answered is not None and answered["answer"] == "split task":
                        planned = task_entry_to_planned_task(task)
                        if planned is not None:
                            used_ids = {t.task_id for t in job.tasks}
                            children = split_one_task(planned, used_ids=used_ids)
                            if children:
                                split_entries = [
                                    planned_task_to_task_entry(
                                        child,
                                        task_class=task.task_class,
                                        source_heading_number=task.source_heading_number,
                                    )
                                    for child in children
                                ]
                    if split_entries:
                        job.tasks[idx + 1:idx + 1] = split_entries
                        task.status = TASK_SPLIT
                        _persist_job(job)
                        continue

            try:
                result = run_pingpong(
                    task.title,
                    job.job_workspace_path,
                    builder_provider=builder_provider,
                    reviewer_provider=reviewer_provider,
                    builder_name=builder_name,
                    reviewer_name=reviewer_name,
                    builder_model=builder_model,
                    reviewer_model=reviewer_model,
                    max_rounds=max_rounds,
                    timeout_sec=timeout_sec,
                    timeout_profile=timeout_profile,
                    max_output_chars=max_output_chars,
                    test_command=test_command,
                    claude_cli_write_mode=claude_cli_write_mode,
                    stream_evidence=stream_evidence,
                    stream_evidence_dir=(
                        str(_task_stream_dir(job.job_id, task.task_id))
                        if stream_evidence else None
                    ),
                    task_input=task_input,
                    hunk_ledger=_recorded_hunk_ledger_for_task(job, task),
                    repair_rounds=repair_rounds,
                    repair_rounds_source=rr_src,
                    keep_staging=True,
                    job_id=job.job_id,
                    task_id=task.task_id,
                    workspace_root=job.job_workspace_path,
                    workspace_handle=job_handle,
                    workspace_owner="job" if job_handle is not None else "run",
                    workspace_start_tree=task.task_start_tree,
                    stop_check=_stop_check,
                    episode_id=job.active_episode_id,
                    on_provider_call=_on_provider_call,
                    compiled_context_paths=compiled_context_paths,
                    compiled_context_candidates=compiled_context_candidates,
                    compiled_context_token_budget=compiled_context_token_budget,
                )
            except Exception as exc:
                task.status = TASK_FAILED
                task.error = f"pingpong_exception: {exc}"
                job.status = JOB_BLOCKED
                job.error = f"task_{task.task_id}_failed: {exc}"
                _persist_job(job)
                return job

            # Record task result
            task.run_id = result.run_id
            task.final_status = result.final_status
            task.safe_diff_files = list(result.safe_diff_files)
            task.repair_rounds_used = result.repair_rounds_used
            task.repair_rounds_allowed = result.repair_rounds_allowed

            # Extract test/reviewer info from rounds
            if result.rounds:
                last_round = result.rounds[-1]
                task.test_passed = last_round.test_passed
                if last_round.reviewer_output:
                    task.reviewer_verdict = last_round.reviewer_output.verdict

            # F011: the loop stopped on purpose. The in-flight provider call finished and
            # its evidence is in the run record; the task never reached its completion/apply
            # boundary, so it goes back to `pending` and the job is stopped — NOT blocked,
            # NOT failed, and never dressed up as a provider or review failure.
            if result.final_status == "stopped":
                from packages.orchestration.safe_points import StopSignal as _StopSignal
                signal = _StopSignal(
                    job_id=job.job_id,
                    request_id=result.stop_request_id,
                    reason=result.stop_reason or "unknown",
                    source=result.stop_source or "unknown",
                    requested_at=result.stop_requested_at,
                )
                _persist_budget_actuals()
                try:
                    return _stop_job(job, signal, task=task, control_root_path=_control)
                except StopFinalizationError:
                    # The task is already back to pending; the request stays pending too.
                    task.status = TASK_PENDING
                    _persist_job(job)
                    return job

            # Step 4857: Deterministic task completion gate
            gate_ok, gate_reasons = validate_job_task_result(result)
            if not gate_ok:
                task.status = TASK_BLOCKED
                task.error = f"completion_gate_failed: {'; '.join(gate_reasons)}"
                _block_job(job, idx, f"task_{task.task_id}_gate_failed: {'; '.join(gate_reasons)}")
                return job

            task.status = TASK_PASSED

            # Step 4887: Pre-apply target repo guard — blocks before workspace apply
            pre_guard = _check_target_repo_guard(job.repo_path, target_snap)
            job.target_guard = pre_guard
            if pre_guard.target_mutated:
                task.status = TASK_BLOCKED
                task.error = f"target_repo_mutated: {pre_guard.changed_target_files}"
                _block_job(job, idx, "target_repo_mutated_during_job")
                return job

            # Step 4835: Strict workspace apply (Step 4976: baseline capture).
            # In a job-owned worktree the task already wrote INTO the workspace,
            # so there is nothing to copy: the manifest is verified in place.
            if job_handle is not None:
                manifest = _verify_in_place_apply(
                    task, result, job.job_workspace_path, job_handle,
                    job.job_initial_tree, job_baselines=job_baselines,
                )
            else:
                manifest = _strict_apply_to_workspace(
                    task, result, job.job_workspace_path,
                    job_baselines=job_baselines,
                )
            task.apply_manifest = manifest

            if manifest.status != "applied":
                task.status = TASK_BLOCKED
                task.error = f"workspace_apply_blocked: {_manifest_block_reason(manifest)}"
                _block_job(job, idx, f"task_{task.task_id}_workspace_apply_blocked")
                return job

            task.status = TASK_APPLIED
            task.task_attempt_state = "complete"   # the tree id is kept for audit

            # Step 4889: Post-apply target guard — defense-in-depth sanity check
            post_guard = _check_target_repo_guard(job.repo_path, target_snap)
            job.target_guard = post_guard
            if post_guard.target_mutated:
                task.status = TASK_BLOCKED
                task.error = f"target_repo_mutated_after_apply: {post_guard.changed_target_files}"
                _block_job(job, idx, "target_repo_mutated_after_apply")
                return job

            # Step 4839: Build proof summary
            task.proof_summary = TaskProofSummary(
                task_id=task.task_id,
                title=task.title,
                run_id=task.run_id,
                final_status=task.final_status,
                applied_files=manifest.applied_files,
                test_passed=task.test_passed,
                reviewer_verdict=task.reviewer_verdict,
                repair_rounds_used=task.repair_rounds_used,
                repair_rounds_allowed=task.repair_rounds_allowed,
                tokens_estimated=len(task_prompt) // 4,
            )
            previous_summaries.append(task.proof_summary)

            tasks_run += 1
            _persist_job(job)

            # SAFE POINT — the task is durably APPLIED and stays that way. A stop observed
            # now takes effect before the NEXT task is dispatched.
            _stop = _stop_check()
            if _stop is not None:
                _persist_budget_actuals()
                if isinstance(_stop, _StopSignal):
                    try:
                        return _stop_job(job, _stop, task=None, control_root_path=_control)
                    except StopFinalizationError:
                        return job          # no further task is dispatched
                else:
                    job.status = JOB_BLOCKED
                    job.error = f"budget_exhausted: {getattr(_stop, 'reason', 'budget')}"
                    _persist_job(job)
                    return job

        # Determine final job status
        all_done = all(
            t.status in (TASK_APPLIED, TASK_SKIPPED, TASK_SPLIT)
            for t in job.tasks
        )
        has_pending = any(t.status == TASK_PENDING for t in job.tasks)

        if all_done:
            job.status = JOB_COMPLETED
            job.finished_at = datetime.now(timezone.utc).isoformat()

            # Final job review — job-level review after all per-task reviewers pass
            try:
                from packages.orchestration.data_paths import job_dir
                from packages.orchestration.final_job_review import build_final_job_review

                _task_verdicts_fjr = [
                    {"task_id": t.task_id, "verdict": t.reviewer_verdict or t.final_status or ""}
                    for t in job.tasks
                ]
                _task_summaries_fjr = [t.title or "" for t in job.tasks]
                _task_diffs_fjr = [
                    (getattr(t, "safe_diff_summary", "") or "")[:2000]
                    for t in job.tasks
                ]
                _fjr = build_final_job_review(
                    job_goal=job.job_title,
                    task_plan=[{"task_id": t.task_id, "title": t.title} for t in job.tasks],
                    task_summaries=_task_summaries_fjr,
                    task_diffs=_task_diffs_fjr,
                    task_verdicts=_task_verdicts_fjr,
                    test_evidence={},
                    gate_verdicts=[],
                    job_id=job.job_id,
                )
                _fjr_dir = job_dir(job.job_id)
                _fjr_dir.mkdir(parents=True, exist_ok=True)
                (_fjr_dir / "final_job_review.json").write_text(
                    _json.dumps(_fjr, indent=2) + "\n"
                )

                # If findings exist, persist final_job_repair_loop.json
                if _fjr.get("findings"):
                    from packages.orchestration.final_job_review import build_final_job_repair_loop
                    _repair_loop = build_final_job_repair_loop(
                        findings=_fjr["findings"],
                        repair_tasks=[],
                        re_review_verdict=_fjr["verdict"],
                        rounds=0,
                        budget=0,
                    )
                    (_fjr_dir / "final_job_repair_loop.json").write_text(
                        _json.dumps(_repair_loop, indent=2) + "\n"
                    )
            except Exception:
                pass  # Best-effort; do not block job completion

        elif has_pending and max_tasks > 0 and tasks_run >= max_tasks:
            job.status = JOB_PAUSED

        _persist_budget_actuals()

        # F012: a completed job records its episode's manifest, after every call input is
        # known. A paused/partial job is not a finished run and gets none yet.
        if job.status == JOB_COMPLETED:
            _write_run_manifest_record(job, status="completed",
                                       episode_id=job.active_episode_id)

        _persist_job(job)
        return job

    finally:
        # The job runner — not the task loop — owns the worktree's cleanup.
        _finalize_job_workspace(job, job_handle)

#: JobPlan worktree states that a resume may pick up.
JOB_RECOVERABLE_STATES = frozenset({"active", "retained", "failed_recoverable"})


def resume_job_plan(job_id: str, **run_kwargs: Any) -> JobPlan:
    """Resume an interrupted JobPlan in its OWN job-owned worktree.

    This is the JobPlan-level recovery record: it reads ``jobs/<job-id>/
    job.json``, NOT a Core Job event log and not per-task ping-pong run records
    (those correctly say ``cleanup_status=job_owned``; the job owns the worktree).

    The same worktree (``job-<job-id>``), the same branch and the same base commit
    are reused — never a replacement branch, never a copied workspace — and the
    task loop continues from the correct task boundary, keeping each interrupted
    task's ORIGINAL start tree so pre-crash work stays inside that task's diff and
    review scope. A completed, cleanly cleaned job is NOT re-materialized.
    """
    job = load_job_plan(job_id)
    if job is None:
        raise ValueError(f"job_not_found: {job_id}")

    if job.status == JOB_COMPLETED and job.worktree_cleanup_status == "clean":
        return job                      # nothing to resume; do not recreate anything

    if job.isolation_mode == "worktree":
        if job.worktree_cleanup_status not in JOB_RECOVERABLE_STATES:
            raise ValueError(
                f"job_not_resumable: worktree cleanup_status="
                f"{job.worktree_cleanup_status!r}"
            )
        from packages.orchestration import worktrees as W
        if not W._branch_exists(job.repo_path, job.worktree_branch):
            raise ValueError(
                f"job_branch_missing: {job.worktree_branch!r}; refusing to create "
                f"a replacement branch or fall back to a copy"
            )

    return run_job(job_id, **run_kwargs)


def _block_job(job: JobPlan, failed_idx: int, error: str) -> None:
    """Block job and skip remaining pending tasks."""
    job.status = JOB_BLOCKED
    job.error = error
    for remaining in job.tasks[failed_idx + 1:]:
        if remaining.status == TASK_PENDING:
            remaining.status = TASK_SKIPPED
    _persist_job(job)


def _manifest_block_reason(manifest: ApplyManifest) -> str:
    """Extract first block reason from manifest."""
    if manifest.missing_files:
        return f"missing: {manifest.missing_files[0]}"
    if manifest.unsupported_files:
        return f"unsupported: {manifest.unsupported_files[0]}"
    if manifest.duplicate_files:
        return f"duplicate: {manifest.duplicate_files[0]}"
    if manifest.unexpected_files:
        return f"unexpected: {manifest.unexpected_files[0]}"
    return "unknown"


# ---------------------------------------------------------------------------
# Task prompt builder (Step 4840 — token context policy)
# ---------------------------------------------------------------------------

def _build_task_prompt(
    job: JobPlan,
    task: TaskEntry,
    previous_summaries: list[TaskProofSummary],
) -> str:
    """Build a bounded task prompt with job context.

    Token context policy v1:
    - Job title
    - Current task title/body/acceptance
    - Previous task bounded proof summaries (last N)
    - Previous applied file list
    - NOT full previous prompts
    - NOT full prior diffs
    - NOT full repo
    """
    parts = [f"# Job: {job.job_title}"]

    if previous_summaries:
        bounded = previous_summaries[-_PREVIOUS_SUMMARY_LIMIT:]
        parts.append("\n## Previous tasks")
        for ps in bounded:
            files_str = ", ".join(ps.applied_files[:10]) if ps.applied_files else "(none)"
            parts.append(
                f"- {ps.task_id}: {ps.title} — {ps.final_status} "
                f"(reviewer: {ps.reviewer_verdict}, "
                f"files: {files_str})"
            )

    parts.append(f"\n## Current task: {task.task_id} — {task.title}")
    parts.append(task.body)

    if task.acceptance:
        parts.append("\n### Acceptance criteria")
        parts.append(task.acceptance)

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Job report (Step 4831, 4839, 4840)
# ---------------------------------------------------------------------------

def export_job_report(job: JobPlan) -> dict[str, Any]:
    """Export a JSON-serializable job report."""
    # Function-scoped, like every other data_paths import in this module. The
    # single use below sits inside a compound boolean, where a missing import is
    # a runtime NameError on the worktree path only — so it is bound HERE, at
    # the top of the function, where it is visible to a reader.
    from packages.orchestration.data_paths import job_dir

    task_reports = []
    for t in job.tasks:
        task_reports.append({
            "task_id": t.task_id,
            "source_heading_number": t.source_heading_number,
            "title": t.title,
            "status": t.status,
            "run_id": t.run_id,
            "final_status": t.final_status,
            "test_passed": t.test_passed,
            "reviewer_verdict": t.reviewer_verdict,
            "repair_rounds_used": t.repair_rounds_used,
            "repair_rounds_allowed": t.repair_rounds_allowed,
            "safe_diff_files": t.safe_diff_files,
            "error": t.error,
            "apply_manifest": _export_apply_manifest(t.apply_manifest),
            "proof_summary": _export_proof_summary(t.proof_summary),
        })

    # F006: a completed worktree job's execution workspace is deliberately gone.
    # Availability of the hand-off is decided by the worktree cleanup status plus a
    # verified job-level result.diff — never by "is that directory still there?".
    # The recorded relative worktree path is kept as audit data.
    has_workspace_changes = False
    handoff_available = False
    if job.isolation_mode == "worktree":
        handoff_available = bool(
            job.result_diff_path
            and job.result_diff_sha256
            and (job_dir(job.job_id) / job.result_diff_path).is_file()
        )
        has_workspace_changes = handoff_available and any(
            t.status == TASK_APPLIED for t in job.tasks
        )
    elif job.job_workspace_path:
        ws = Path(job.job_workspace_path)
        if ws.exists():
            has_workspace_changes = any(
                t.status == TASK_APPLIED for t in job.tasks
            )
            handoff_available = has_workspace_changes

    next_cmd = _suggest_next_command(job)

    pending_count = sum(1 for t in job.tasks if t.status == TASK_PENDING)

    return {
        "job_id": job.job_id,
        "job_title": job.job_title,
        "status": job.status,
        "repo_path": job.repo_path,
        "job_workspace_path": job.job_workspace_path,
        "created_at": job.created_at,
        "finished_at": job.finished_at,
        "tasks": task_reports,
        "has_workspace_changes": has_workspace_changes,
        "isolation_mode": job.isolation_mode,
        "worktree": {
            "branch": job.worktree_branch,
            "path": job.worktree_path,          # repo-relative audit path
            "base_commit": job.worktree_base_commit,
            "head": job.worktree_head,
            "cleanup_status": job.worktree_cleanup_status,
            "workspace_expected_present": (
                job.isolation_mode == "worktree"
                and job.worktree_cleanup_status != "clean"
            ),
        },
        "handoff_available": handoff_available,
        "result_diff": (
            {
                "path": job.result_diff_path,
                "sha256": job.result_diff_sha256,
                "size_bytes": job.result_diff_size_bytes,
            }
            if job.result_diff_path else None
        ),
        "next_command": next_cmd,
        "target_guard": _export_target_guard(job.target_guard),
        # F010: the job-level post-mortem, and the reason one could not be written. A
        # recording failure that did not survive `_persist_job` was a recording failure the
        # evidence export could never see.
        "postmortem": {
            "path": job.postmortem_path,      # evidence-relative, never absolute
            "error": job.postmortem_error,
        },
        "repair_rounds_allowed": job.repair_rounds_allowed,
        "repair_rounds_source": job.repair_rounds_source,
        "pending_tasks": pending_count,
        "execution_config": _export_execution_config(job.execution_config),
        "context_strategy": {
            "strategy": "task_bounded_sequential_job",
            "previous_task_summary_limit": _PREVIOUS_SUMMARY_LIMIT,
            "full_job_history_in_prompt": False,
            "full_repo_in_prompt": False,
        },
        "warning": (
            "Real target repo was NOT mutated. "
            "Changes exist only in the isolated job workspace."
        ),
    }


def format_job_report_text(job: JobPlan) -> str:
    """Format a human-readable job report."""
    lines = [
        f"Job {job.job_id}: {job.job_title}",
        f"Status: {job.status}",
        f"Repo: {job.repo_path}",
        "",
        "Tasks:",
    ]

    for t in job.tasks:
        status_icon = {
            TASK_PENDING: " ",
            TASK_RUNNING: ">",
            TASK_PASSED: "+",
            TASK_APPLIED: "*",
            TASK_BLOCKED: "!",
            TASK_FAILED: "X",
            TASK_SKIPPED: "-",
        }.get(t.status, "?")

        line = f"  [{status_icon}] {t.task_id}: {t.title} — {t.status}"
        if t.run_id:
            line += f" (run: {t.run_id})"
        lines.append(line)

        if t.reviewer_verdict:
            lines.append(f"      Reviewer: {t.reviewer_verdict}")
        if t.repair_rounds_used:
            lines.append(
                f"      Repair: {t.repair_rounds_used}/{t.repair_rounds_allowed}"
            )
        if t.apply_manifest and t.apply_manifest.applied_files:
            lines.append(
                f"      Applied: {len(t.apply_manifest.applied_files)} files"
            )
        if t.error:
            lines.append(f"      Error: {t.error}")

    lines.append("")

    if job.repair_rounds_source:
        disabled = " (disabled)" if job.repair_rounds_allowed == 0 else ""
        lines.append(
            f"Repair: {job.repair_rounds_allowed} rounds"
            f" (source: {job.repair_rounds_source}){disabled}"
        )

    pending_count = sum(1 for t in job.tasks if t.status == TASK_PENDING)
    if job.status == JOB_PAUSED and pending_count > 0:
        lines.append(f"Paused: {pending_count} tasks pending")

    ec = job.execution_config
    if ec:
        lines.append(f"Builder: {ec.builder} (source: {ec.builder_source})")
        lines.append(f"Reviewer: {ec.reviewer} (source: {ec.reviewer_source})")
        lines.append(f"Max rounds: {ec.max_rounds} (source: {ec.max_rounds_source})")
        tc = ec.test_command
        if tc:
            tc_display = tc[:80] + "..." if len(tc) > 80 else tc
            lines.append(f"Test command: {tc_display} (source: {ec.test_command_source})")
        if ec.claude_cli_write_mode != "none":
            lines.append(
                f"Write mode: {ec.claude_cli_write_mode}"
                f" (source: {ec.claude_cli_write_mode_source})"
            )
        if job.status == JOB_PAUSED:
            lines.append("Continuation config: persisted from previous run")

    if any(t.status == TASK_APPLIED for t in job.tasks):
        lines.append("Job workspace has accumulated changes.")
    lines.append(
        "WARNING: Real target repo was NOT mutated. "
        "Changes exist only in the isolated job workspace."
    )

    next_cmd = _suggest_next_command(job)
    if next_cmd:
        lines.append(f"\nNext: {next_cmd}")

    return "\n".join(lines)


def _suggest_next_command(job: JobPlan) -> str:
    """Suggest the next CLI command based on job state.

    For paused jobs with persisted config, the short command is safe — config
    is restored from persistence. The report text shows the config that will
    be used.
    """
    if job.status == JOB_PLANNED:
        return f"remedy do job-run {job.job_id}"
    if job.status == JOB_PAUSED:
        return f"remedy do job-run {job.job_id}"
    if job.status == JOB_COMPLETED:
        return f"remedy do job-promote {job.job_id} --repo . --dry-run"
    if job.status == JOB_BLOCKED:
        return f"remedy do job-report {job.job_id}"
    pending = [t for t in job.tasks if t.status == TASK_PENDING]
    if pending:
        return f"remedy do job-run {job.job_id}"
    return ""


def job_evidence_dir(job_id: str):
    """The job's own (hidden) evidence directory — where a job-level record lives.

    ``data_paths`` OWNS this layout (DECISION F260 D1); this is not a second
    answer to the same question. The NAME survives only until F260 T004 moves
    its remaining callers onto ``data_paths.job_evidence_dir`` directly.
    """
    from packages.orchestration.data_paths import job_evidence_dir as _job_evidence_dir
    return _job_evidence_dir(job_id)


def job_postmortem_path(job_id: str):
    """The job-level post-mortem, before the export copies it into the bundle."""
    from packages.orchestration.failure_postmortem import POSTMORTEM_FILENAME
    return job_evidence_dir(job_id) / POSTMORTEM_FILENAME


def _write_job_postmortem_record(job: JobPlan, exc: BaseException) -> None:
    """Record a job-level failure that happened before any task ran.

    Never raises into the runner: the job failure itself is already recorded on the job,
    and a post-mortem that could not be written is captured as ``job.postmortem_error``,
    which the evidence export turns into a BLOCKING integrity failure rather than a
    silently pretty package.
    """
    from packages.orchestration.failure_postmortem import (
        POSTMORTEM_FILENAME,
        FailureSignals,
        build_job_rollup,
        write_postmortem,
    )

    try:
        record = build_job_rollup(
            job_id=job.job_id,
            signals=FailureSignals(exception=exc, error_text=f"{type(exc).__name__}: {exc}"),
        )
        directory = job_evidence_dir(job.job_id)
        directory.mkdir(parents=True, exist_ok=True)
        write_postmortem(directory, record, root=directory)
        job.postmortem_path = POSTMORTEM_FILENAME
    except Exception as write_exc:                # never mask the original failure
        from packages.orchestration.failure_postmortem import safe_text
        job.postmortem_error = safe_text(
            f"{type(write_exc).__name__}: {write_exc}")[:500]


# ---------------------------------------------------------------------------
# F011 — the stop episode
# ---------------------------------------------------------------------------

#: Where a stop episode's post-mortem lives. Keyed by REQUEST id, because a job may be
#: stopped, resumed and stopped again, and the second stop must not overwrite the first.
STOP_POSTMORTEM_SUBDIR = "stop_postmortems"


def stop_postmortem_dir(job_id: str, request_id: str):
    """``jobs/<job_id>/evidence/stop_postmortems/<request_id>/`` — one per episode."""
    from packages.orchestration.safe_points import validate_job_id

    return job_evidence_dir(job_id) / STOP_POSTMORTEM_SUBDIR / validate_job_id(request_id)


def _write_stop_postmortem(job: JobPlan, signal: Any, task_id: str) -> None:
    """The F010 record for a deliberate stop: class ``stopped``, scope ``job``.

    Never raises into the runner. A record that could not be written becomes
    ``job.stop_error``, which the evidence export turns into a BLOCKING integrity failure —
    the same rule F010 already applies to a failure it could not explain.
    """
    from packages.orchestration.failure_postmortem import (
        POSTMORTEM_FILENAME,
        FailureSignals,
        build_job_rollup,
        write_postmortem,
    )

    _is_budget = getattr(signal, "source", "") == "budget"
    _terminal = "budget_exhausted" if _is_budget else "stopped"

    try:
        record = build_job_rollup(
            job_id=job.job_id,
            signals=FailureSignals(
                terminal_status=_terminal,
                error_text=f"stop requested: {signal.reason}",
            ),
        )
        record = replace(
            record,
            task_id=task_id or "",
            raw_reason=f"stop requested: {signal.reason} (source: {signal.source})",
        )
        directory = stop_postmortem_dir(job.job_id, signal.request_id)
        directory.mkdir(parents=True, exist_ok=True)
        write_postmortem(directory, record, root=job_evidence_dir(job.job_id))
        job.stop_postmortem_path = (
            f"{STOP_POSTMORTEM_SUBDIR}/{signal.request_id}/{POSTMORTEM_FILENAME}")
    except Exception as write_exc:
        from packages.orchestration.failure_postmortem import safe_text
        job.stop_error = safe_text(
            f"stop_postmortem_write_failed: {type(write_exc).__name__}: {write_exc}")[:500]


def _append_job_stopped_event(job: JobPlan, signal: Any, task_id: str) -> None:
    """Exactly one ``job_stopped`` ledger event per CONSUMED request.

    Written through the existing run-log ledger (``<data_root>/runs/<job_id>/<run>.jsonl``),
    which is what `remedy event list` and the replay tooling already read. Nothing in the
    payload is a path or a secret. A ledger failure is durable on the job, never silent.
    """
    from packages.orchestration.failure_postmortem import safe_text

    try:
        from packages.orchestration.run_log import RunLogWriter

        completed = sum(
            1 for t in job.tasks if t.status in (TASK_APPLIED, TASK_PASSED, TASK_SKIPPED))
        pending = sum(1 for t in job.tasks if t.status == TASK_PENDING)
        writer = RunLogWriter(job.job_id)
        writer.log(
            "job_stopped",
            task_id=task_id or None,
            outcome="stopped",
            request_id=signal.request_id,
            reason=signal.reason,
            source=signal.source,
            requested_at=signal.requested_at,
            consumed_at=job.stopped_at,
            completed_task_count=completed,
            pending_task_count=pending,
            postmortem_ref=job.stop_postmortem_path,
        )
    except Exception as exc:
        job.stop_event_error = safe_text(
            f"job_stopped_event_failed: {type(exc).__name__}: {exc}")[:500]


class StopFinalizationError(RuntimeError):
    """The stop could not be made durable. The request stays pending; nothing is faked."""


def _job_stopped_event_exists(job_id: str, request_id: str) -> bool | None:
    """Has this exact request already produced a ``job_stopped`` event?

    Returns True/False, or None when the ledger could not be read at all (which must not be
    mistaken for "no event": appending a second one would break exactly-once).

    This scan happens ONLY during stop finalization — never at an ordinary safe point, which
    stays a single stat plus a small read.
    """
    try:
        from packages.orchestration.data_paths import run_log_dir

        job_runs = run_log_dir(job_id)
        if not job_runs.is_dir():
            return False
        for jsonl in sorted(job_runs.glob("*.jsonl")):
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    raw = _json.loads(line)
                except ValueError:
                    continue                      # a torn line is not our event
                if (raw.get("event") == "job_stopped"
                        and str(raw.get("job_id")) == job_id
                        and str((raw.get("metadata") or {}).get("request_id")) == request_id):
                    return True
        return False
    except OSError:
        return None


def _stop_job(job: JobPlan, signal: Any, *, task: TaskEntry | None,
              control_root_path: Any = None) -> JobPlan:
    """Turn an observed stop signal into a durable, resumable STOPPED job.

    **The order is the feature.** The reviewed build archived the request, deleted the
    pending file, and only then tried to persist the job — so a failing `_persist_job` left
    a job that still said `planned` and a stop request that no longer existed anywhere. The
    stop was simply lost.

    The pending request is now the transaction's commit record, and it is removed LAST:

    1. archive the request (idempotent; a different record under the same id conflicts);
    2. write the stopped post-mortem (idempotent — F010's writer settles an identical record
       and refuses a conflicting one);
    3. append the ``job_stopped`` event, but only if this request has not already produced
       one (exactly-once by request id);
    4. set the STOPPED state and every stop field;
    5. persist the job — the durable checkpoint;
    6. only now remove the pending request.

    A failure anywhere in 1-5 leaves the request PENDING and raises: the runner starts no
    new work, and the next run sees the same request, recognises the parts already done, and
    completes the SAME episode — one archive, one post-mortem, one event. A failure at 6
    leaves a stopped job with a pending request; the next run acknowledges it without a
    second event or post-mortem.
    """
    from packages.orchestration.failure_postmortem import safe_text
    from packages.orchestration.safe_points import (
        acknowledge_stop,
        archive_stop,
    )

    task_id = task.task_id if task is not None else ""

    # The incomplete task goes back to pending, exactly like the provider-failure path. A
    # task that already reached TASK_APPLIED is durable and is NOT rolled back.
    if task is not None and task.status not in (TASK_APPLIED, TASK_PASSED, TASK_SKIPPED):
        task.status = TASK_PENDING
        task.task_attempt_state = "active"     # its start tree stays valid for the resume

    _is_budget_stop = getattr(signal, "source", "") == "budget"

    # --- 1. archive (no removal yet) --------------------------------------------------
    archive_ref = ""
    if not _is_budget_stop:
        try:
            archive_ref = archive_stop(job.job_id, signal,
                                       control_root_path=control_root_path)
        except Exception as exc:
            job.stop_error = safe_text(
                f"stop_archive_failed: {type(exc).__name__}: {exc}")[:500]
            job.stop_request_id = getattr(signal, "request_id", "")
            _persist_job(job)
            raise StopFinalizationError(job.stop_error) from exc

    # --- 2. post-mortem (idempotent) --------------------------------------------------
    # The request id goes on the job as soon as the archive exists: whatever happens next,
    # the job names the episode it is trying to finalize, so a retry can recognise it.
    job.stop_error = ""
    job.stop_event_error = ""
    job.stop_archive_ref = archive_ref
    job.stop_request_id = signal.request_id
    _write_stop_postmortem(job, signal, task_id)
    if job.stop_error:
        _persist_job(job)
        raise StopFinalizationError(job.stop_error)

    # --- 3. event, exactly once per request id ----------------------------------------
    job.stop_reason = signal.reason
    job.stop_source = signal.source
    job.stopped_at = datetime.now(timezone.utc).isoformat()

    already = _job_stopped_event_exists(job.job_id, signal.request_id)
    if already is None:
        job.stop_event_error = safe_text(
            "job_stopped_event_unverifiable: the run ledger could not be read, so a second "
            "event cannot be ruled out")[:500]
        _persist_job(job)
        raise StopFinalizationError(job.stop_event_error)
    if not already:
        _append_job_stopped_event(job, signal, task_id)
        if job.stop_event_error:
            _persist_job(job)
            raise StopFinalizationError(job.stop_event_error)

    # --- 4. the F012 manifest is part of the stop transaction -------------------------
    # It must PUBLISH before the stop request is acknowledged. If it fails, the request
    # stays pending (raise below), the next run observes the same request and finalizes the
    # SAME stop episode (episode id derived from the request id, so archive/post-mortem/event
    # /manifest all stay exactly once). The stop reason is never replaced by the manifest
    # error — the primary stop stands.
    # F5: the stopped manifest represents the ACTIVE execution episode — same episode id as its
    # snapshot and its calls. The stop request id is carried as SEPARATE terminal metadata, not
    # smuggled in as the episode id. (A pre-work stop already allocated an active episode.)
    if not _write_run_manifest_record(job, status="stopped",
                                      episode_id=job.active_episode_id,
                                      stop_request_id=signal.request_id):
        _persist_job(job)             # durable blocking error; request still pending
        raise StopFinalizationError(job.run_manifest_error)

    # --- 5. the durable STOPPED checkpoint --------------------------------------------
    job.status = JOB_STOPPED
    job.error = ""
    _persist_job(job)                 # if THIS throws, the request is still pending: good

    # --- 6. the request has done its job ----------------------------------------------
    if not _is_budget_stop:
        try:
            acknowledge_stop(job.job_id, signal, control_root_path=control_root_path)
        except Exception as exc:
            job.stop_error = safe_text(
                f"stop_acknowledge_failed: {type(exc).__name__}: {exc}")[:500]
            _persist_job(job)
    return job


_PHASE_EPISODE_START = "episode_start"
_PHASE_PRE_WORK_STOP = "pre_work_stop"


def _mark_manifest_required(job: JobPlan) -> None:
    """Stamp the F012 marker: a job first run under F012 is expected to have a manifest, so a
    later completed/stopped job WITHOUT one is blocking rather than legacy."""
    from packages.orchestration.run_manifest import MANIFEST_REQUIRED_VERSION
    job.run_manifest_required_v = MANIFEST_REQUIRED_VERSION


def _capture_input_snapshot(job: JobPlan, *, phase: str,
                            extra_problems: tuple[str, ...] = ()) -> Any:
    """F1/F11/F12: capture the typed, EPISODE-OWNED input snapshot at episode START, bound to
    the active episode and a named ``phase``. The result is stored as an
    ``EpisodeInputSnapshotV1`` wrapper (status ok|failed) — a capture FAILURE (including a
    ``extra_problems`` failure such as a failed episode-start workspace-tree capture) is
    recorded as data, never swallowed to an empty dict, and NEVER re-probed at episode end. The
    caller must treat a non-``ok`` wrapper as a blocking pre-work condition."""
    from packages.orchestration.run_manifest import capture_episode_input_snapshot

    _mark_manifest_required(job)
    wrapper = capture_episode_input_snapshot(
        job, episode_id=job.active_episode_id, capture_phase=phase,
        extra_problems=extra_problems)
    job.input_snapshot = wrapper.to_json()
    return wrapper


def _snapshot_block_reason(job: JobPlan, wrapper: Any, *, phase: str) -> str:
    """Return a non-empty reason string when the mandatory episode snapshot is NOT usable
    (capture failed or the wrapper is invalid / foreign to the active episode), else ''.
    Used to HARD-BLOCK the job before any task or provider call (F1/F6/F12)."""
    from packages.orchestration.run_manifest import validate_episode_input_snapshot

    probs = validate_episode_input_snapshot(
        wrapper, expected_episode_id=job.active_episode_id)
    if wrapper.capture_phase != phase:
        probs = [*probs, f"snapshot phase {wrapper.capture_phase!r} != expected {phase!r}"]
    if not wrapper.is_ok():
        # is_ok() already folds in validate(); surface the captured failure problems too.
        probs = [*probs, *[str(p) for p in wrapper.problems]]
    return "; ".join(dict.fromkeys(p for p in probs if p))[:500]


def _episode_snapshot_bound_ok(job: JobPlan) -> bool:
    """True when a persisted, ``ok`` episode snapshot is already bound to the active episode —
    the signal that a stop-retry must REUSE it rather than recapture (F1)."""
    from packages.orchestration.run_manifest import decode_episode_snapshot_v1

    if not job.input_snapshot or not job.active_episode_id:
        return False
    try:
        # F5: the persisted JobPlan snapshot is UNTRUSTED disk state — strict-decode it. A
        # malformed record never returns ok and is never reused.
        w = decode_episode_snapshot_v1(job.input_snapshot)
    except Exception:
        return False
    return w.is_ok() and w.episode_id == job.active_episode_id


def _episodes_from_canonical(order: list) -> list:
    """The JobPlan-level episode index, taken verbatim from the CANONICAL on-disk order (F10)."""
    return [{"episode_id": e["episode_id"], "status": e["status"],
             "created_at": e["created_at"], "episode_ordinal": e["episode_ordinal"],
             "previous_episode_id": e["previous_episode_id"]} for e in order]


def _crosscheck_jobplan_vs_canonical(job: JobPlan, canonical_existing: list,
                                     current_episode_id: str) -> list:
    """F9/F10: the JobPlan's own episode view (excluding the episode being written) MUST agree
    with the canonical on-disk index. A divergence means the durable index and the job's view
    have drifted — the append is refused, never silently reconciled."""
    job_eps = {str(e.get("episode_id", "")): e for e in job.run_manifest_episodes
               if e.get("episode_id") and e.get("episode_id") != current_episode_id}
    if len([e for e in job.run_manifest_episodes
            if e.get("episode_id") and e.get("episode_id") != current_episode_id]) != len(job_eps):
        return ["duplicate episode ids in JobPlan"]
    can_eps = {str(e["episode_id"]): e for e in canonical_existing}
    problems: list = []
    if set(job_eps) != set(can_eps):
        problems.append(f"episode id set differs: job {sorted(job_eps)} vs "
                        f"index {sorted(can_eps)}")
    for eid, ce in can_eps.items():
        je = job_eps.get(eid)
        if je is None:
            continue
        if int(je.get("episode_ordinal", 0) or 0) != int(ce["episode_ordinal"]):
            problems.append(f"episode {eid} ordinal differs")
        if str(je.get("status", "")) != str(ce["status"]):
            problems.append(f"episode {eid} status differs")
        if str(je.get("created_at", "")) != str(ce["created_at"]):
            problems.append(f"episode {eid} created_at differs")
        if str(je.get("previous_episode_id", "") or "") != str(ce["previous_episode_id"] or ""):
            problems.append(f"episode {eid} previous_episode_id differs")
    return problems


def _write_run_manifest_record(job: JobPlan, *, status: str, episode_id: str,
                               created_at: str | None = None,
                               stop_request_id: str = "") -> bool:
    """F012: write ONE immutable manifest for one execution EPISODE. Never raises.

    Uses the typed episode-start snapshot wrapper captured at episode start (F4). The episode
    ordinal + immediate predecessor are derived from the CANONICAL verified index, never from
    mutable JobPlan state (F10), after cross-checking the two agree (F9). Idempotent for the
    same episode content; a conflicting write for the same episode is captured as an error.
    Returns True on success, False on a recording failure (``job.run_manifest_error`` carries
    why, and the evidence export turns it into a BLOCKING integrity failure)."""
    from packages.orchestration.run_manifest import (
        MANIFEST_FILENAME,
        ManifestError,
        build_run_manifest,
        decode_episode_snapshot_v1,
        ensure_evidence_root_anchored,
        episode_manifest_exists_anchored,
        load_episode_manifest_verified,
        read_canonical_episode_order,
        rebuild_manifest_mirror_and_index_from_canonical_episodes,
        utc_now_iso,
        validate_episode_input_snapshot,
        write_run_manifest,
    )

    try:
        ev = job_evidence_dir(job.job_id)
        # F5: a stopped/completed manifest's episode id IS the active execution episode — the
        # snapshot, the calls and the manifest all name the same episode. The stop REQUEST id is
        # carried separately as terminal metadata, never used as the episode id.
        if episode_id != job.active_episode_id:
            raise ManifestError(
                f"manifest episode {episode_id!r} != active episode "
                f"{job.active_episode_id!r} (F5)")

        # F11: an episode manifest is IMMUTABLE. Decide whether it already exists through
        # ANCHORED reads (never Path.is_file()). If it does (a retry of a stop whose
        # acknowledge/persist failed), re-issue the CANONICAL on-disk record through the
        # verified trust chain — never a rebuild from possibly-shifted job state.
        if episode_manifest_exists_anchored(ev, episode_id):
            try:
                canonical = load_episode_manifest_verified(ev, episode_id,
                                                           expected_job_id=job.job_id)
            except ManifestError:
                # F3/F4: the IMMUTABLE episode exists but the DERIVED mirror/index is
                # broken/partial (a crash during index publication). Recover by rebuilding the
                # derived projection PURELY from the immutable episode records, then reload —
                # so a partial publication converges on retry instead of failing forever.
                rebuild_manifest_mirror_and_index_from_canonical_episodes(
                    ev, root=ev, job_id=job.job_id)
                canonical = load_episode_manifest_verified(ev, episode_id,
                                                           expected_job_id=job.job_id)
            write_run_manifest(ev, canonical, root=ev)
            job.run_manifest_path = MANIFEST_FILENAME
            job.run_manifest_created_at = canonical.created_at
            job.run_manifest_error = ""
            job.run_manifest_episodes = _episodes_from_canonical(
                read_canonical_episode_order(ev, job_id=job.job_id))
            return True

        # F5: creation time is PER EPISODE. A retry reuses its stamp; a resumed episode gets its
        # own — never the prior episode's timestamp.
        prior_stamp = ""
        for e in job.run_manifest_episodes:
            if e.get("episode_id") == episode_id:
                prior_stamp = e.get("created_at", "")
                break
        stamp = created_at or prior_stamp or utc_now_iso()

        # F4/F6: consume the typed, episode-bound snapshot WRAPPER verbatim and validate it
        # strictly. A missing / FAILED / invalid / foreign snapshot is a BLOCKING recording
        # error — the finalizer NEVER re-probes a fresh terminal snapshot to paper over it.
        # F5: strict-decode the persisted snapshot; a malformed record is a durable bounded
        # manifest error, never coerced into a usable snapshot.
        wrapper = (decode_episode_snapshot_v1(job.input_snapshot)
                   if job.input_snapshot else None)
        if wrapper is None:
            raise ManifestError("no episode-start input snapshot (F1 blocking)")
        sp = validate_episode_input_snapshot(wrapper, expected_episode_id=job.active_episode_id)
        if sp or not wrapper.is_ok():
            raise ManifestError(
                "episode-start snapshot invalid or a failed capture (F1/F4/F6): "
                + "; ".join(sp or list(wrapper.problems))[:300])

        # F10: derive the ordinal + immediate predecessor from the CANONICAL verified index —
        # NOT mutable JobPlan metadata. Then cross-check the JobPlan agrees (F9) and refuse the
        # append on any disagreement, so tampered JobPlan state cannot redirect episode order.
        ensure_evidence_root_anchored(ev)
        canonical_order = read_canonical_episode_order(ev, job_id=job.job_id)
        existing = [e for e in canonical_order if e["episode_id"] != episode_id]
        xcheck = _crosscheck_jobplan_vs_canonical(job, existing, episode_id)
        if xcheck:
            raise ManifestError("JobPlan/index disagreement (F9/F10): " + "; ".join(xcheck))
        ordinal = len(existing) + 1
        previous_episode_id = existing[-1]["episode_id"] if existing else ""
        prior = tuple(e["episode_id"] for e in existing)     # ascending ordinal order (F8)

        # F5 (round 10): the CANONICAL prior-episode set and its ordinals — the only ground on
        # which a call may be excluded as "someone else's history". A call naming an episode
        # that is not in this map is unattributable, and unattributable is a coverage problem,
        # never a silent exclusion.
        prior_ordinals = {e["episode_id"]: int(e["episode_ordinal"]) for e in existing}
        manifest = build_run_manifest(job, status=status, episode_id=episode_id,
                                      created_at=stamp, episode_snapshot=wrapper,
                                      prior_episode_ids=prior,
                                      owned_episode_id=job.active_episode_id,
                                      prior_episode_ordinals=prior_ordinals,
                                      episode_ordinal=ordinal,
                                      previous_episode_id=previous_episode_id,
                                      stop_request_id=stop_request_id)
        write_run_manifest(ev, manifest, root=ev)
        job.run_manifest_path = MANIFEST_FILENAME
        job.run_manifest_created_at = stamp          # job-level = latest episode
        job.run_manifest_error = ""
        # F10: refresh the JobPlan's episode index from the RESULTING canonical order.
        job.run_manifest_episodes = _episodes_from_canonical(
            read_canonical_episode_order(ev, job_id=job.job_id))
        return True
    except Exception as exc:                       # never mask the primary job outcome
        from packages.orchestration.failure_postmortem import safe_text
        job.run_manifest_error = safe_text(
            f"run_manifest_write_failed: {type(exc).__name__}: {exc}")[:500]
        return False


def _task_stream_dir(job_id: str, task_id: str):
    """Return the per-task F004 raw stream evidence directory (hidden data dir).

    Streams land beside the job's persisted evidence so `job-evidence` picks them
    up as ``task_runs/<task>/`` artifacts without polluting the repository.

    ``data_paths`` owns the evidence root (DECISION F260 D1); only the
    ``task_runs/<task>/`` tail below is this module's own.
    """
    from packages.orchestration.data_paths import job_evidence_dir as _job_evidence_dir
    return _job_evidence_dir(job_id) / "task_runs" / task_id
