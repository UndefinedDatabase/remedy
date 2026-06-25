"""Job Task Runner — sequential multi-task execution with review/repair gates.

Parses a Markdown job file into ordered tasks, executes each through the
existing ping-pong loop (Builder → tests → Reviewer → repair), and applies
passed results into an isolated job workspace. The real target repo is never
mutated.

Public API:
    parse_job_file(text, repo_path) -> JobPlan
    plan_job_from_file(job_file_path, repo_path) -> JobPlan
    run_job(job_id, ...) -> JobPlan
    apply_task_to_workspace(job, task_idx) -> bool
    export_job_report(job) -> dict
    load_job_plan(job_id) -> JobPlan | None
"""

from __future__ import annotations

import hashlib
import json as _json
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


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class TaskEntry:
    """A single task within a job."""
    task_id: str = ""          # T001, T002, ...
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
        "tasks": [
            {
                "task_id": t.task_id,
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
    )
    for t in data.get("tasks", []):
        job.tasks.append(TaskEntry(
            task_id=t.get("task_id", ""),
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

    Expected format:
        # Job: <title>
        ## Task 1
        <body>
        Acceptance:
        - <criteria>
        ## Task 2
        ...

    Returns a JobPlan with status=planned. No provider calls, no repo mutation.
    """
    sha256 = hashlib.sha256(text.encode()).hexdigest()

    # Extract job title from first H1
    job_title = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            job_title = stripped[2:].strip()
            # Remove "Job:" prefix if present
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
            task_num = int(m.group(1))
            task_title = m.group(2).strip()
            current_task = {
                "num": task_num,
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
    for sec in task_sections:
        task_id = f"T{sec['num']:03d}"
        body = "\n".join(sec["body_lines"]).strip()
        acceptance = "\n".join(sec["acceptance_lines"]).strip()
        title = sec["title"] or f"Task {sec['num']}"
        # Bound stored body to 2000 chars for token safety
        if len(body) > 2000:
            body = body[:2000] + "\n[truncated]"
        tasks.append(TaskEntry(
            task_id=task_id,
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
# Sequential job runner (Step 4829 + 4830)
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
    its staged result is applied into the job workspace. If any task fails,
    the job is blocked and execution stops.

    The real target repo is never mutated.
    """
    from packages.orchestration.pingpong_loop import (
        TaskInput,
        run_pingpong,
    )

    job = load_job_plan(job_id)
    if job is None:
        err_job = JobPlan(
            job_id=job_id,
            status=JOB_BLOCKED,
            error=f"job_not_found: {job_id}",
        )
        return err_job

    # Create job workspace if not yet created
    if not job.job_workspace_path:
        try:
            job.job_workspace_path = _create_job_workspace(job)
        except Exception as exc:
            job.status = JOB_BLOCKED
            job.error = f"workspace_creation_failed: {exc}"
            _persist_job(job)
            return job

    job.status = JOB_RUNNING
    _persist_job(job)

    tasks_run = 0
    previous_summaries: list[str] = []

    for idx, task in enumerate(job.tasks):
        if task.status in (TASK_APPLIED, TASK_PASSED, TASK_SKIPPED):
            # Already done — collect summary for context
            previous_summaries.append(
                f"{task.task_id}: {task.title} — {task.status}"
            )
            continue

        if task.status in (TASK_BLOCKED, TASK_FAILED):
            # Prior failure — skip remaining
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
                keep_staging=True,  # Need staging for workspace apply
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

        # Check if task passed
        if result.final_status == "staged_review_passed":
            task.status = TASK_PASSED

            # Step 4830: Apply to job workspace
            applied = _apply_task_to_workspace(job, idx, result)
            if applied:
                task.status = TASK_APPLIED
                previous_summaries.append(
                    f"{task.task_id}: {task.title} — {task.status}"
                )
            else:
                task.status = TASK_BLOCKED
                task.error = "workspace_apply_failed"
                job.status = JOB_BLOCKED
                job.error = f"task_{task.task_id}_workspace_apply_failed"
                _persist_job(job)
                return job
        else:
            # Task did not pass — block job
            task.status = TASK_FAILED
            job.status = JOB_BLOCKED
            job.error = (
                f"task_{task.task_id}_not_passed: {result.final_status}"
            )
            # Mark remaining tasks as skipped
            for remaining in job.tasks[idx + 1:]:
                if remaining.status == TASK_PENDING:
                    remaining.status = TASK_SKIPPED
            _persist_job(job)
            return job

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


def _build_task_prompt(
    job: JobPlan,
    task: TaskEntry,
    previous_summaries: list[str],
) -> str:
    """Build a bounded task prompt with job context."""
    parts = [f"# Job: {job.job_title}"]

    if previous_summaries:
        parts.append("\n## Previous tasks")
        for s in previous_summaries[-5:]:  # Bound to last 5
            parts.append(f"- {s}")

    parts.append(f"\n## Current task: {task.task_id} — {task.title}")
    parts.append(task.body)

    if task.acceptance:
        parts.append("\n### Acceptance criteria")
        parts.append(task.acceptance)

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Workspace apply (Step 4830)
# ---------------------------------------------------------------------------

def _apply_task_to_workspace(
    job: JobPlan,
    task_idx: int,
    result: Any,
) -> bool:
    """Apply a passed task's staged files into the job workspace.

    Copies changed files from staging to job workspace.
    Returns True on success.
    """
    staging_path = result.staging_path
    workspace_path = job.job_workspace_path

    if not staging_path or not workspace_path:
        return False

    staging = Path(staging_path)
    workspace = Path(workspace_path)

    if not staging.exists() or not workspace.exists():
        return False

    try:
        for rel_path in result.staged_files:
            src = staging / rel_path
            dst = workspace / rel_path
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(dst))
        # Clean up staging after successful apply
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Job report (Step 4831)
# ---------------------------------------------------------------------------

def export_job_report(job: JobPlan) -> dict[str, Any]:
    """Export a JSON-serializable job report."""
    task_reports = []
    for t in job.tasks:
        task_reports.append({
            "task_id": t.task_id,
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
        return f"remedy do job run {job.job_id}"
    if job.status == JOB_COMPLETED:
        return f"remedy do job report {job.job_id} --json"
    if job.status == JOB_BLOCKED:
        return f"remedy do job report {job.job_id}"
    pending = [t for t in job.tasks if t.status == TASK_PENDING]
    if pending:
        return f"remedy do job run {job.job_id}"
    return ""
