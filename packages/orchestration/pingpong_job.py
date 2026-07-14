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
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

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

JOB_PLANNED = "planned"
JOB_RUNNING = "running"
JOB_BLOCKED = "blocked"
JOB_COMPLETED = "completed"
JOB_PAUSED = "paused"

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


@dataclass
class JobPlan:
    """Durable job plan with ordered tasks."""
    job_id: str = field(default_factory=lambda: uuid4().hex[:16])
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


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _jobs_dir() -> Path:
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root() / "task_jobs"


def _persist_job(job: JobPlan) -> Path:
    job_dir = _jobs_dir() / job.job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    out = job_dir / "job.json"
    out.write_text(_json.dumps(_export_job(job), indent=2) + "\n")
    return out


def load_job_plan(job_id: str) -> JobPlan | None:
    job_file = _jobs_dir() / job_id / "job.json"
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
    )
    for t in data.get("tasks", []):
        job.tasks.append(TaskEntry(
            task_id=t.get("task_id", ""),
            source_heading_number=t.get("source_heading_number", 0),
            title=t.get("title", ""),
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
            }
            continue

        if current_task is not None:
            stripped = line.strip()
            if stripped.lower().startswith("acceptance:") or stripped.lower().startswith("acceptance :"):
                current_task["_in_acceptance"] = True
                continue
            if current_task.get("_in_acceptance"):
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
        tasks.append(TaskEntry(
            task_id=task_id,
            source_heading_number=sec["heading_num"],
            title=title,
            body=body,
            acceptance=acceptance,
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
    from packages.orchestration.staging_workspace import create_staging_workspace

    data_root = _jobs_dir().parent
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

    job_dir = _jobs_dir() / job.job_id

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
                (job_dir / "result.diff").unlink()
            except OSError:
                pass

    try:
        W.snapshot(handle)
        job.worktree_head = handle.head_commit
        if not coverage_error:
            info = W.write_tree_diff(
                handle, job.job_initial_tree, W.write_tree(handle),
                job_dir / "result.diff",
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


def _resolve_cfg(cli_val: Any, persisted_val: Any, default: Any) -> tuple[Any, str]:
    """Resolve config field: explicit CLI > persisted > product default."""
    if cli_val is not None:
        return cli_val, "cli"
    if persisted_val is not None:
        return persisted_val, "persisted"
    return default, "default"


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
    timeout_sec: int = 120,
    timeout_profile: str = "",
    max_output_chars: int = 50000,
    claude_cli_write_mode: str | None = None,
    stream_evidence: bool = False,
    max_tasks: int = 0,
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

    # Step 4869: Resolve each config field — explicit > persisted > default
    ec = job.execution_config

    builder_name, builder_src = _resolve_cfg(
        builder_name, ec.builder if ec else None, "fake")
    reviewer_name, reviewer_src = _resolve_cfg(
        reviewer_name, ec.reviewer if ec else None, "fake")
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
    )

    # Record repair-round metadata at job level
    job.repair_rounds_allowed = repair_rounds
    job.repair_rounds_source = rr_src

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
            if task.status in (TASK_APPLIED, TASK_PASSED, TASK_SKIPPED):
                continue

            if task.status in (TASK_BLOCKED, TASK_FAILED):
                break

            if max_tasks > 0 and tasks_run >= max_tasks:
                break

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
                    repair_rounds=repair_rounds,
                    repair_rounds_source=rr_src,
                    keep_staging=True,
                    job_id=job.job_id,
                    task_id=task.task_id,
                    workspace_root=job.job_workspace_path,
                    workspace_handle=job_handle,
                    workspace_owner="job" if job_handle is not None else "run",
                    workspace_start_tree=task.task_start_tree,
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

        # Determine final job status
        all_done = all(
            t.status in (TASK_APPLIED, TASK_SKIPPED)
            for t in job.tasks
        )
        has_pending = any(t.status == TASK_PENDING for t in job.tasks)

        if all_done:
            job.status = JOB_COMPLETED
            job.finished_at = datetime.now(timezone.utc).isoformat()

            # Final job review — job-level review after all per-task reviewers pass
            try:
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
                _fjr_dir = _jobs_dir() / job.job_id
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

        _persist_job(job)
        return job

    finally:
        # The job runner — not the task loop — owns the worktree's cleanup.
        _finalize_job_workspace(job, job_handle)

#: JobPlan worktree states that a resume may pick up.
JOB_RECOVERABLE_STATES = frozenset({"active", "retained", "failed_recoverable"})


def resume_job_plan(job_id: str, **run_kwargs: Any) -> JobPlan:
    """Resume an interrupted JobPlan in its OWN job-owned worktree.

    This is the JobPlan-level recovery record: it reads ``task_jobs/<job-id>/
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
            and (_jobs_dir() / job.job_id / job.result_diff_path).is_file()
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
    """The job's own (hidden) evidence directory — where a job-level record lives."""
    from packages.orchestration.data_paths import jobs_dir
    return jobs_dir() / job_id / "evidence"


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


def _task_stream_dir(job_id: str, task_id: str):
    """Return the per-task F004 raw stream evidence directory (hidden data dir).

    Streams land beside the job's persisted evidence so `job-evidence` picks them
    up as ``task_runs/<task>/`` artifacts without polluting the repository.
    """
    from packages.orchestration.data_paths import jobs_dir
    return jobs_dir() / job_id / "evidence" / "task_runs" / task_id
