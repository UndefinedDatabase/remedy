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
class ApplyManifest:
    """Result of a strict workspace apply for one task."""
    task_id: str = ""
    run_id: str = ""
    applied_files: list[str] = field(default_factory=list)
    missing_files: list[str] = field(default_factory=list)
    unsupported_files: list[str] = field(default_factory=list)
    unexpected_files: list[str] = field(default_factory=list)
    duplicate_files: list[str] = field(default_factory=list)
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


@dataclass
class TargetGuard:
    """Job-level target repo mutation guard."""
    target_mutated: bool = False
    changed_target_files: list[str] = field(default_factory=list)
    ignored_target_noise_files: list[str] = field(default_factory=list)


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


def _export_target_guard(g: TargetGuard | None) -> dict[str, Any] | None:
    if g is None:
        return None
    return {
        "target_mutated": g.target_mutated,
        "changed_target_files": g.changed_target_files,
        "ignored_target_noise_files": g.ignored_target_noise_files,
    }


def _import_target_guard(d: dict[str, Any] | None) -> TargetGuard | None:
    if d is None:
        return None
    return TargetGuard(
        target_mutated=d.get("target_mutated", False),
        changed_target_files=d.get("changed_target_files", []),
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

def _create_job_workspace(job: JobPlan) -> str:
    """Create an isolated job workspace as a filtered copy of the target repo.

    Reuses staging_workspace filtering logic to exclude .git, .env, etc.
    Returns the workspace path string.
    """
    from packages.orchestration.staging_workspace import create_staging_workspace

    data_root = _jobs_dir().parent
    ws_parent = data_root / "job_workspaces"
    ws_parent.mkdir(parents=True, exist_ok=True)

    target = Path(job.repo_path)
    ws = create_staging_workspace(target, ws_parent, job.job_id)
    return str(ws.staging_dir)


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
    from packages.orchestration.pingpong_loop import _check_target_mutation
    meaningful, noise = _check_target_mutation(Path(repo_path), before_snap)
    return TargetGuard(
        target_mutated=bool(meaningful),
        changed_target_files=meaningful,
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


def _strict_apply_to_workspace(
    task: TaskEntry,
    result: Any,
    workspace_path: str,
) -> ApplyManifest:
    """Strict workspace apply with full manifest.

    Every staged file must be accounted for. Missing, duplicate, traversal,
    and unsafe paths block the apply.
    """
    manifest = ApplyManifest(
        task_id=task.task_id,
        run_id=result.run_id,
    )

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
    for rel_path in staged_files:
        unsafe_reason = _is_unsafe_path(rel_path)
        if unsafe_reason:
            manifest.unsupported_files.append(f"{rel_path} ({unsafe_reason})")
            continue

        src = staging / rel_path
        if not src.exists():
            manifest.missing_files.append(rel_path)
            continue

        # Path containment check
        try:
            resolved_dst = (workspace / rel_path).resolve()
            if not resolved_dst.is_relative_to(workspace.resolve()):
                manifest.unsupported_files.append(
                    f"{rel_path} (escapes workspace)"
                )
                continue
        except (OSError, ValueError):
            manifest.unsupported_files.append(
                f"{rel_path} (path resolution failed)"
            )
            continue

        dst = workspace / rel_path
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dst))
            manifest.applied_files.append(rel_path)
        except OSError as exc:
            manifest.unexpected_files.append(f"{rel_path} (copy failed: {exc})")

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
# Sequential job runner (Steps 4829-4830, 4837-4838)
# ---------------------------------------------------------------------------

def run_job(
    job_id: str,
    *,
    builder_name: str = "fake",
    reviewer_name: str = "fake",
    builder_provider: Any = None,
    reviewer_provider: Any = None,
    max_rounds: int = 3,
    repair_rounds: int = 2,
    test_command: str = "",
    timeout_sec: int = 120,
    max_output_chars: int = 50000,
    claude_cli_write_mode: str = "none",
    max_tasks: int = 0,
) -> JobPlan:
    """Execute pending tasks sequentially through the ping-pong loop.

    Each task runs Builder → tests → Reviewer → repair. If a task passes,
    its staged result is strictly applied into the job workspace. If any task
    fails, the job is blocked and execution stops.

    The real target repo is never mutated — a snapshot guard verifies this
    after each task.
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

    # Create job workspace if not yet created
    if not job.job_workspace_path:
        try:
            job.job_workspace_path = _create_job_workspace(job)
        except Exception as exc:
            job.status = JOB_BLOCKED
            job.error = f"workspace_creation_failed: {exc}"
            _persist_job(job)
            return job

    # Step 4837: Snapshot real target repo before any task runs
    target_snap = _snapshot_target_repo(job.repo_path)

    job.status = JOB_RUNNING
    _persist_job(job)

    tasks_run = 0
    previous_summaries: list[TaskProofSummary] = []

    # Collect existing proof summaries from already-done tasks
    for t in job.tasks:
        if t.proof_summary and t.status in (TASK_APPLIED, TASK_PASSED):
            previous_summaries.append(t.proof_summary)

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
                max_rounds=max_rounds,
                timeout_sec=timeout_sec,
                max_output_chars=max_output_chars,
                test_command=test_command,
                claude_cli_write_mode=claude_cli_write_mode,
                task_input=task_input,
                repair_rounds=repair_rounds,
                keep_staging=True,
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

        # Step 4838: Task completion gate
        if result.final_status != "staged_review_passed":
            task.status = TASK_FAILED
            task.error = f"not_passed: {result.final_status}"
            _block_job(job, idx, f"task_{task.task_id}_not_passed: {result.final_status}")
            return job

        task.status = TASK_PASSED

        # Step 4835: Strict workspace apply
        manifest = _strict_apply_to_workspace(task, result, job.job_workspace_path)
        task.apply_manifest = manifest

        if manifest.status != "applied":
            task.status = TASK_BLOCKED
            task.error = f"workspace_apply_blocked: {_manifest_block_reason(manifest)}"
            _block_job(job, idx, f"task_{task.task_id}_workspace_apply_blocked")
            return job

        task.status = TASK_APPLIED

        # Step 4837: Check target repo guard after each task
        guard = _check_target_repo_guard(job.repo_path, target_snap)
        job.target_guard = guard
        if guard.target_mutated:
            task.status = TASK_BLOCKED
            task.error = f"target_repo_mutated: {guard.changed_target_files}"
            _block_job(job, idx, "target_repo_mutated_during_job")
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

    # Check if all tasks are done
    all_done = all(
        t.status in (TASK_APPLIED, TASK_SKIPPED)
        for t in job.tasks
    )
    if all_done:
        job.status = JOB_COMPLETED
        job.finished_at = datetime.now(timezone.utc).isoformat()

    _persist_job(job)
    return job


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

    has_workspace_changes = False
    if job.job_workspace_path:
        ws = Path(job.job_workspace_path)
        if ws.exists():
            has_workspace_changes = any(
                t.status == TASK_APPLIED for t in job.tasks
            )

    next_cmd = _suggest_next_command(job)

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
        "next_command": next_cmd,
        "target_guard": _export_target_guard(job.target_guard),
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
    """Suggest the next CLI command based on job state."""
    if job.status == JOB_PLANNED:
        return f"remedy do job-run {job.job_id}"
    if job.status == JOB_COMPLETED:
        return f"remedy do job-report {job.job_id} --json"
    if job.status == JOB_BLOCKED:
        return f"remedy do job-report {job.job_id}"
    pending = [t for t in job.tasks if t.status == TASK_PENDING]
    if pending:
        return f"remedy do job-run {job.job_id}"
    return ""
