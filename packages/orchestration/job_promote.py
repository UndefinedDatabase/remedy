"""Job promotion — apply reviewed job workspace changes into target repo.

Promotion is a separate explicit human-approved action.
Never auto-promotes. Requires --approve flag.
No git commit, no git push, no git reset, no git checkout.

Public API:
    promote_job(job_id, target_repo, *, approve, dry_run, test_command) -> JobPromotionResult
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

_BLOCKED_PREFIXES = (
    ".git/", ".git\\",
    ".env", "node_modules/", "node_modules\\",
    "__pycache__/", "__pycache__\\",
    ".mypy_cache/", ".pytest_cache/", ".ruff_cache/",
    ".tox/", "dist/", "build/", ".eggs/",
    ".cache/", "htmlcov/",
)

_BLOCKED_EXACT = frozenset({
    ".git", ".env", ".gitignore",
})

_UNSAFE_EXTENSIONS = frozenset({
    ".pem", ".key", ".p12", ".pfx", ".jks",
})

_MAX_FILE_SIZE = 1_000_000
_TEST_OUTPUT_CAP = 10000


def _is_blocked_path(rel_path: str) -> str:
    """Return block reason or empty string if path is allowed."""
    norm = rel_path.replace("\\", "/")

    if ".." in norm.split("/"):
        return "path_traversal"

    if os.path.isabs(rel_path):
        return "absolute_path"

    if norm in _BLOCKED_EXACT or norm.rstrip("/") in _BLOCKED_EXACT:
        return f"blocked_path: {norm}"

    base = os.path.basename(norm)
    if base == ".env" or base.startswith(".env.") or base.startswith(".env-"):
        return "secret_file"

    for prefix in _BLOCKED_PREFIXES:
        p = prefix.replace("\\", "/")
        if norm.startswith(p) or norm == p.rstrip("/"):
            return f"blocked_path: {p.rstrip('/')}"

    suffix = os.path.splitext(norm)[1].lower()
    if suffix in _UNSAFE_EXTENSIONS:
        return "private_key_file"

    return ""


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        h.update(path.read_bytes())
    except OSError:
        return ""
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------

@dataclass
class TaskPromoSummary:
    """Per-task promotion readiness summary."""
    task_id: str = ""
    title: str = ""
    status: str = ""
    run_id: str = ""
    reviewer_verdict: str = ""
    test_passed: bool | None = None
    repair_rounds_used: int = 0
    repair_rounds_allowed: int = 0
    applied_files: list[str] = field(default_factory=list)


@dataclass
class JobPromotionResult:
    """Result of a job promotion attempt."""
    job_id: str = ""
    promotion_id: str = field(default_factory=lambda: uuid4().hex[:16])
    status: str = ""  # ready, blocked, dry_run, promoted, promoted_test_failed
    approved: bool = False
    dry_run: bool = False
    target_repo: str = ""
    job_status: str = ""
    job_title: str = ""
    job_workspace_path: str = ""
    task_summaries: list[TaskPromoSummary] = field(default_factory=list)
    files_planned: list[str] = field(default_factory=list)
    files_applied: list[str] = field(default_factory=list)
    files_blocked: list[str] = field(default_factory=list)
    files_skipped: list[str] = field(default_factory=list)
    blocked_reason: str = ""
    blocked_reasons: list[str] = field(default_factory=list)
    target_guard_ok: bool = False
    execution_config: dict[str, Any] = field(default_factory=dict)
    context_strategy: str = ""
    post_test_command: str = ""
    post_test_passed: bool | None = None
    post_test_summary: str = ""
    started_at: str = ""
    finished_at: str = ""


# ---------------------------------------------------------------------------
# Promotion logic
# ---------------------------------------------------------------------------

def _block(
    result: JobPromotionResult,
    reason: str,
) -> JobPromotionResult:
    result.status = "blocked"
    result.blocked_reason = reason
    result.blocked_reasons.append(reason)
    result.finished_at = datetime.now(timezone.utc).isoformat()
    return result


def _run_post_test(
    command: str,
    target: Path,
    *,
    timeout_sec: int = 120,
) -> tuple[bool, str]:
    try:
        argv = shlex.split(command)
    except ValueError as exc:
        return False, f"Invalid test command: {exc}"
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=str(target),
        )
    except FileNotFoundError:
        return False, f"Test command not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return False, f"Test command timed out after {timeout_sec}s"

    output = (proc.stdout or "") + (proc.stderr or "")
    if len(output) > _TEST_OUTPUT_CAP:
        output = output[:_TEST_OUTPUT_CAP] + "\n[OUTPUT TRUNCATED]"
    passed = proc.returncode == 0
    summary = f"exit={proc.returncode}"
    if output.strip():
        last_lines = output.strip().splitlines()[-5:]
        summary += " | " + " ".join(last_lines)
    return passed, summary


def _collect_workspace_files(workspace: Path, repo: Path) -> list[str]:
    """Collect files that differ between workspace and target repo.

    Only considers files that exist in the workspace. Uses relative paths.
    Does not use git commands.
    """
    changed: list[str] = []
    for ws_file in sorted(workspace.rglob("*")):
        if not ws_file.is_file():
            continue
        try:
            rel = str(ws_file.relative_to(workspace))
        except ValueError:
            continue
        repo_file = repo / rel
        if not repo_file.exists():
            changed.append(rel)
            continue
        try:
            if ws_file.read_bytes() != repo_file.read_bytes():
                changed.append(rel)
        except OSError:
            changed.append(rel)
    return changed


def promote_job(
    job_id: str,
    target_repo: str = ".",
    *,
    approve: bool = False,
    dry_run: bool = False,
    test_command: str = "",
) -> JobPromotionResult:
    """Promote reviewed job workspace changes into target repo.

    Without --approve, returns dry-run preview only. Never auto-promotes.
    No git commit, no git push, no git reset, no git checkout.
    """
    from packages.orchestration.pingpong_job import (
        JOB_COMPLETED,
        TASK_APPLIED,
        _export_execution_config,
        load_job_plan,
    )

    result = JobPromotionResult(
        job_id=job_id,
        approved=approve,
        dry_run=dry_run,
        target_repo=str(Path(target_repo).resolve()),
        post_test_command=test_command,
        started_at=datetime.now(timezone.utc).isoformat(),
    )

    # --- Load job ---
    job = load_job_plan(job_id)
    if job is None:
        return _block(result, f"job_not_found: {job_id}")

    result.job_status = job.status
    result.job_title = job.job_title
    result.job_workspace_path = job.job_workspace_path or ""

    ec = _export_execution_config(job.execution_config)
    result.execution_config = ec or {}
    result.context_strategy = (
        job.execution_config.context_strategy
        if job.execution_config else "unknown"
    )

    # --- Task summaries ---
    for t in job.tasks:
        result.task_summaries.append(TaskPromoSummary(
            task_id=t.task_id,
            title=t.title,
            status=t.status,
            run_id=t.run_id,
            reviewer_verdict=t.reviewer_verdict,
            test_passed=t.test_passed,
            repair_rounds_used=t.repair_rounds_used,
            repair_rounds_allowed=t.repair_rounds_allowed,
            applied_files=(
                t.apply_manifest.applied_files
                if t.apply_manifest else []
            ),
        ))

    # --- Readiness gates ---
    if job.status != JOB_COMPLETED:
        return _block(result, f"job_not_completed: status={job.status}")

    for t in job.tasks:
        if t.status != TASK_APPLIED:
            return _block(result, f"task_not_applied: {t.task_id} status={t.status}")
        if not t.run_id:
            return _block(result, f"task_missing_run_id: {t.task_id}")
        if t.reviewer_verdict != "pass":
            return _block(result, f"reviewer_not_pass: {t.task_id} verdict={t.reviewer_verdict}")
        if t.test_passed is False:
            return _block(result, f"tests_failed: {t.task_id}")

    # --- Target guard ---
    tg = job.target_guard
    if tg and tg.target_mutated:
        return _block(result, "target_mutated_during_job")
    result.target_guard_ok = True

    # --- Workspace exists ---
    ws_path = job.job_workspace_path
    if not ws_path:
        return _block(result, "no_job_workspace_path")

    workspace = Path(ws_path)
    if not workspace.is_dir():
        return _block(result, f"workspace_missing: {ws_path}")

    # --- Target repo exists ---
    target = Path(target_repo).resolve()
    if not target.is_dir():
        return _block(result, f"target_not_directory: {target_repo}")

    # --- Collect files to promote ---
    all_applied: list[str] = []
    for t in job.tasks:
        if t.apply_manifest and t.apply_manifest.applied_files:
            all_applied.extend(t.apply_manifest.applied_files)

    if not all_applied:
        changed = _collect_workspace_files(workspace, target)
        if not changed:
            return _block(result, "no_files_to_promote")
        all_applied = changed

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_files: list[str] = []
    for f in all_applied:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    # --- Validate each file ---
    planned: list[str] = []
    blocked: list[str] = []
    skipped: list[str] = []

    for rel_path in unique_files:
        block_reason = _is_blocked_path(rel_path)
        if block_reason:
            blocked.append(f"{rel_path}: {block_reason}")
            continue

        # Path containment
        dest = (target / rel_path).resolve()
        try:
            dest.relative_to(target)
        except ValueError:
            blocked.append(f"{rel_path}: path_escape")
            continue

        ws_file = workspace / rel_path
        if not ws_file.is_file():
            skipped.append(f"{rel_path}: not_in_workspace")
            continue

        try:
            size = ws_file.stat().st_size
        except OSError:
            skipped.append(f"{rel_path}: unreadable")
            continue

        if size > _MAX_FILE_SIZE:
            skipped.append(f"{rel_path}: too_large ({size})")
            continue

        planned.append(rel_path)

    result.files_planned = planned
    result.files_blocked = blocked
    result.files_skipped = skipped

    if blocked:
        return _block(result, f"blocked_paths: {blocked}")

    if not planned:
        return _block(result, "no_promotable_files")

    # --- Dry-run or unapproved: preview only ---
    if dry_run or not approve:
        result.status = "dry_run"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        _persist_job_promotion(job_id, result)
        return result

    # --- Pre-apply target repo check ---
    for rel_path in planned:
        target_file = target / rel_path
        ws_file = workspace / rel_path
        if target_file.exists():
            ws_content = ws_file.read_bytes()
            target_content = target_file.read_bytes()
            if ws_content == target_content:
                skipped.append(f"{rel_path}: already_identical")
                planned = [p for p in planned if p != rel_path]

    result.files_planned = planned
    result.files_skipped = skipped

    if not planned:
        result.status = "dry_run"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        _persist_job_promotion(job_id, result)
        return result

    # --- Apply files ---
    applied: list[str] = []
    for rel_path in planned:
        ws_file = workspace / rel_path
        dest = target / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            content = ws_file.read_bytes()
            dest.write_bytes(content)
            applied.append(rel_path)
        except OSError as exc:
            result.status = "blocked"
            result.blocked_reason = f"write_failed: {rel_path}: {exc}"
            result.files_applied = applied
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_job_promotion(job_id, result)
            return result

    result.files_applied = applied

    # --- Post-apply verification ---
    for rel_path in applied:
        ws_file = workspace / rel_path
        dest = target / rel_path
        try:
            if ws_file.read_bytes() != dest.read_bytes():
                result.status = "blocked"
                result.blocked_reason = f"post_apply_mismatch: {rel_path}"
                result.finished_at = datetime.now(timezone.utc).isoformat()
                _persist_job_promotion(job_id, result)
                return result
        except OSError as exc:
            result.status = "blocked"
            result.blocked_reason = f"post_apply_verify_failed: {rel_path}: {exc}"
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_job_promotion(job_id, result)
            return result

    # --- Post-promotion tests ---
    if test_command:
        passed, summary = _run_post_test(test_command, target)
        result.post_test_passed = passed
        result.post_test_summary = summary
        if not passed:
            result.status = "promoted_test_failed"
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_job_promotion(job_id, result)
            return result

    result.status = "promoted"
    result.finished_at = datetime.now(timezone.utc).isoformat()
    _persist_job_promotion(job_id, result)
    return result


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _promotions_dir() -> Path:
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root() / "job_promotions"


def _persist_job_promotion(
    job_id: str,
    result: JobPromotionResult,
) -> None:
    try:
        promo_dir = _promotions_dir() / job_id
        promo_dir.mkdir(parents=True, exist_ok=True)
        promo_file = promo_dir / f"{result.promotion_id}.json"
        promo_file.write_text(
            json.dumps(export_job_promotion_json(result), indent=2) + "\n"
        )
    except OSError:
        pass


def load_job_promotion(job_id: str, promotion_id: str) -> dict[str, Any] | None:
    promo_file = _promotions_dir() / job_id / f"{promotion_id}.json"
    if not promo_file.exists():
        return None
    try:
        return json.loads(promo_file.read_text())
    except (OSError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# Export / summary
# ---------------------------------------------------------------------------

def export_job_promotion_json(result: JobPromotionResult) -> dict[str, Any]:
    return {
        "job_id": result.job_id,
        "promotion_id": result.promotion_id,
        "status": result.status,
        "approved": result.approved,
        "dry_run": result.dry_run,
        "target_repo": result.target_repo,
        "job_status": result.job_status,
        "job_title": result.job_title,
        "job_workspace_path": result.job_workspace_path,
        "task_summaries": [
            {
                "task_id": ts.task_id,
                "title": ts.title,
                "status": ts.status,
                "run_id": ts.run_id,
                "reviewer_verdict": ts.reviewer_verdict,
                "test_passed": ts.test_passed,
                "repair_rounds_used": ts.repair_rounds_used,
                "repair_rounds_allowed": ts.repair_rounds_allowed,
                "applied_files": ts.applied_files,
            }
            for ts in result.task_summaries
        ],
        "files_planned": result.files_planned,
        "files_applied": result.files_applied,
        "files_blocked": result.files_blocked,
        "files_skipped": result.files_skipped,
        "blocked_reason": result.blocked_reason,
        "blocked_reasons": result.blocked_reasons,
        "target_guard_ok": result.target_guard_ok,
        "execution_config": result.execution_config,
        "context_strategy": result.context_strategy,
        "post_test_command": result.post_test_command,
        "post_test_passed": result.post_test_passed,
        "post_test_summary": result.post_test_summary,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
    }


def summarize_job_promotion(result: JobPromotionResult) -> str:
    lines = [
        f"Job: {result.job_id}",
        f"Title: {result.job_title}",
        f"Promotion: {result.promotion_id}",
        f"Status: {result.status}",
        f"Approved: {result.approved}",
        f"Target: {result.target_repo}",
    ]

    if result.task_summaries:
        lines.append("")
        lines.append("Tasks:")
        for ts in result.task_summaries:
            verdict = ts.reviewer_verdict or "none"
            test = "passed" if ts.test_passed else ("failed" if ts.test_passed is False else "n/a")
            lines.append(f"  {ts.task_id}: {ts.title} — {ts.status} "
                         f"(reviewer: {verdict}, tests: {test})")

    if result.status == "dry_run":
        lines.append("")
        lines.append("Dry-run preview only. No target files changed.")
        if result.files_planned:
            lines.append(f"Would apply {len(result.files_planned)} file(s):")
            for f in result.files_planned:
                lines.append(f"  {f}")
        lines.append("")
        lines.append(
            f"To apply: remedy do job-promote {result.job_id}"
            f" --repo {result.target_repo} --approve"
        )

    elif result.status == "promoted":
        lines.append("")
        lines.append(f"Applied {len(result.files_applied)} file(s):")
        for f in result.files_applied:
            lines.append(f"  {f}")
        if result.post_test_passed is not None:
            lines.append(
                f"Post-test: {'passed' if result.post_test_passed else 'FAILED'}"
            )
            if result.post_test_summary:
                lines.append(f"  {result.post_test_summary}")
        lines.append("")
        lines.append("No commits or pushes were made. Review and commit manually.")

    elif result.status == "promoted_test_failed":
        lines.append("")
        lines.append(f"Applied {len(result.files_applied)} file(s) but post-test FAILED.")
        lines.append("Manual review required. Changes are in working tree, not committed.")
        if result.post_test_summary:
            lines.append(f"  {result.post_test_summary}")

    elif result.status == "blocked":
        lines.append("")
        lines.append(f"BLOCKED: {result.blocked_reason}")

    if result.files_blocked:
        lines.append("")
        lines.append("Blocked files:")
        for f in result.files_blocked:
            lines.append(f"  {f}")

    if result.files_skipped:
        lines.append("")
        lines.append("Skipped files:")
        for f in result.files_skipped:
            lines.append(f"  {f}")

    return "\n".join(lines) + "\n"
