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

from packages.orchestration.pingpong_evidence import (
    _redact_json_value,
    _redact_secrets,
    _sanitize_path,
)

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


def _validate_source_containment(
    workspace: Path,
    rel_path: str,
) -> str:
    """Validate that a workspace source file is safe to read.

    Returns empty string if safe, or reason string if blocked.
    Blocks symlinks, escapes, non-regular files.
    """
    ws_resolved = workspace.resolve()
    src = workspace / rel_path

    if src.is_symlink():
        return f"source_is_symlink: {rel_path}"

    try:
        src_resolved = src.resolve()
    except OSError:
        return f"source_resolve_failed: {rel_path}"

    if not str(src_resolved).startswith(str(ws_resolved) + os.sep) and src_resolved != ws_resolved:
        return f"source_escapes_workspace: {rel_path}"

    if not src_resolved.exists():
        return f"source_missing: {rel_path}"

    if not src_resolved.is_file():
        return f"source_not_regular_file: {rel_path}"

    current = src.parent
    while current != workspace and current != current.parent:
        if current.is_symlink():
            return f"parent_symlink_in_path: {rel_path}"
        current = current.parent

    return ""


def _validate_dest_containment(
    target: Path,
    rel_path: str,
) -> str:
    """Validate that a target destination path is safe to write.

    Returns empty string if safe, or reason string if blocked.
    """
    try:
        dest_resolved = (target / rel_path).resolve()
    except OSError:
        return f"dest_resolve_failed: {rel_path}"

    target_resolved = target.resolve()
    if not str(dest_resolved).startswith(str(target_resolved) + os.sep) and dest_resolved != target_resolved:
        return f"dest_escapes_target: {rel_path}"

    dest = target / rel_path
    if dest.exists() and dest.is_symlink():
        link_target = dest.resolve()
        if not str(link_target).startswith(str(target_resolved) + os.sep):
            return f"dest_symlink_escape: {rel_path}"

    return ""


# ---------------------------------------------------------------------------
# Baseline readiness model
# ---------------------------------------------------------------------------

@dataclass
class FileReadiness:
    """Per-file baseline readiness status for promotion."""
    path: str = ""
    kind: str = ""  # created | modified
    baseline_status: str = ""
    workspace_status: str = ""


def _consolidate_file_proofs(
    job: Any,
) -> dict[str, dict[str, Any]]:
    """Consolidate file proofs across all tasks: earliest baseline, latest final hash."""
    consolidated: dict[str, dict[str, Any]] = {}
    for t in job.tasks:
        if not t.apply_manifest:
            continue
        for proof in t.apply_manifest.applied_file_proofs:
            if proof.path not in consolidated:
                consolidated[proof.path] = {
                    "existed_before_job": proof.existed_before_job,
                    "baseline_sha256": proof.baseline_sha256,
                    "final_workspace_sha256": proof.final_workspace_sha256,
                }
            else:
                consolidated[proof.path]["final_workspace_sha256"] = (
                    proof.final_workspace_sha256
                )
    return consolidated


def _check_baseline_readiness(
    target: Path,
    workspace: Path,
    planned_files: list[str],
    proofs: dict[str, dict[str, Any]],
) -> tuple[bool, list[str], list[FileReadiness]]:
    """Baseline-aware readiness check.

    Returns (clean, block_reasons, file_readiness_list).
    """
    blocks: list[str] = []
    readiness: list[FileReadiness] = []

    for rel_path in planned_files:
        proof = proofs.get(rel_path)
        target_file = target / rel_path
        ws_file = workspace / rel_path

        if proof is None:
            if target_file.exists():
                blocks.append(f"missing_baseline_for_existing_file: {rel_path}")
                readiness.append(FileReadiness(
                    path=rel_path,
                    kind="modified",
                    baseline_status="missing_baseline_for_existing_file",
                    workspace_status="unknown",
                ))
            else:
                readiness.append(FileReadiness(
                    path=rel_path,
                    kind="created",
                    baseline_status="target_missing_as_expected",
                    workspace_status="unknown",
                ))
            continue

        existed = proof["existed_before_job"]
        baseline_hash = proof["baseline_sha256"]
        final_hash = proof["final_workspace_sha256"]

        ws_current_hash = _hash_file(ws_file)
        if ws_current_hash != final_hash:
            blocks.append(f"workspace_changed_since_review: {rel_path}")
            readiness.append(FileReadiness(
                path=rel_path,
                kind="modified" if existed else "created",
                baseline_status="unknown",
                workspace_status="workspace_changed_since_review",
            ))
            continue

        ws_status = "final_hash_matches"

        if existed:
            kind = "modified"
            if not target_file.exists():
                blocks.append(f"target_deleted_since_job: {rel_path}")
                readiness.append(FileReadiness(
                    path=rel_path, kind=kind,
                    baseline_status="target_deleted_since_job",
                    workspace_status=ws_status,
                ))
                continue
            current_target_hash = _hash_file(target_file)
            if current_target_hash == baseline_hash:
                b_status = "target_matches_baseline"
            else:
                blocks.append(f"target_changed_since_job: {rel_path}")
                b_status = "target_changed_since_job"
        else:
            kind = "created"
            if target_file.exists():
                blocks.append(f"target_created_since_job: {rel_path}")
                b_status = "target_created_since_job"
            else:
                b_status = "target_missing_as_expected"

        readiness.append(FileReadiness(
            path=rel_path, kind=kind,
            baseline_status=b_status,
            workspace_status=ws_status,
        ))

    return len(blocks) == 0, blocks, readiness


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
    file_readiness: list[FileReadiness] = field(default_factory=list)
    blocked_reason: str = ""
    blocked_reasons: list[str] = field(default_factory=list)
    target_guard_ok: bool = False
    target_clean: bool = False
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

    Every promoted file must come from a task apply manifest.
    No workspace fallback scanning. Baseline-aware target safety.
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

    # --- Require explicit apply manifests, no fallback ---
    for t in job.tasks:
        if not t.apply_manifest:
            return _block(result, f"missing_apply_manifest: {t.task_id}")
        if t.apply_manifest.status != "applied":
            return _block(result, f"apply_manifest_not_applied: {t.task_id} status={t.apply_manifest.status}")

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

    # --- Collect files from apply manifests only ---
    all_applied: list[str] = []
    for t in job.tasks:
        if t.apply_manifest and t.apply_manifest.applied_files:
            all_applied.extend(t.apply_manifest.applied_files)

    if not all_applied:
        return _block(result, "no_files_in_apply_manifests")

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

        dest_reason = _validate_dest_containment(target, rel_path)
        if dest_reason:
            blocked.append(f"{rel_path}: {dest_reason}")
            continue

        src_reason = _validate_source_containment(workspace, rel_path)
        if src_reason:
            blocked.append(f"{rel_path}: {src_reason}")
            continue

        ws_file = workspace / rel_path
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

    # --- Baseline-aware readiness check ---
    proofs = _consolidate_file_proofs(job)
    clean, block_reasons, readiness = _check_baseline_readiness(
        target, workspace, planned, proofs,
    )
    result.file_readiness = readiness
    result.target_clean = clean
    if not clean:
        return _block(result, f"baseline_check_failed: {block_reasons}")

    # --- Dry-run or unapproved: preview only ---
    if dry_run or not approve:
        result.status = "dry_run"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        _persist_job_promotion(job_id, result)
        return result

    # --- Preflight promotion record writability ---
    try:
        promo_dir = _promotions_dir() / job_id
        promo_dir.mkdir(parents=True, exist_ok=True)
        test_file = promo_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
    except OSError as exc:
        return _block(result, f"promotion_record_not_writable: {exc}")

    # --- Recheck baseline readiness immediately before apply ---
    clean2, blocks2, _ = _check_baseline_readiness(
        target, workspace, planned, proofs,
    )
    if not clean2:
        return _block(result, f"baseline_check_before_apply_failed: {blocks2}")

    # --- Apply files ---
    applied: list[str] = []
    for rel_path in planned:
        ws_file = workspace / rel_path

        src_reason = _validate_source_containment(workspace, rel_path)
        if src_reason:
            result.status = "blocked"
            result.blocked_reason = f"source_unsafe_at_apply: {rel_path}: {src_reason}"
            result.files_applied = applied
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_job_promotion(job_id, result)
            return result

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
    """Persist promotion record. Raises on write failure for approved promotes."""
    promo_dir = _promotions_dir() / job_id
    promo_dir.mkdir(parents=True, exist_ok=True)
    promo_file = promo_dir / f"{result.promotion_id}.json"
    data = export_job_promotion_json(result)
    promo_file.write_text(json.dumps(data, indent=2) + "\n")


def load_job_promotion(job_id: str, promotion_id: str) -> dict[str, Any] | None:
    promo_file = _promotions_dir() / job_id / f"{promotion_id}.json"
    if not promo_file.exists():
        return None
    try:
        return json.loads(promo_file.read_text())
    except (OSError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# Export / summary (redacted, baseline-aware)
# ---------------------------------------------------------------------------

def export_job_promotion_json(result: JobPromotionResult) -> dict[str, Any]:
    raw = {
        "job_id": result.job_id,
        "promotion_id": result.promotion_id,
        "status": result.status,
        "approved": result.approved,
        "dry_run": result.dry_run,
        "target_repo": _sanitize_path(result.target_repo),
        "job_status": result.job_status,
        "job_title": result.job_title,
        "job_workspace_path": _sanitize_path(result.job_workspace_path),
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
        "file_readiness": [
            {
                "path": fr.path,
                "kind": fr.kind,
                "baseline_status": fr.baseline_status,
                "workspace_status": fr.workspace_status,
            }
            for fr in result.file_readiness
        ],
        "blocked_reason": result.blocked_reason,
        "blocked_reasons": result.blocked_reasons,
        "target_guard_ok": result.target_guard_ok,
        "target_clean": result.target_clean,
        "execution_config": result.execution_config,
        "context_strategy": result.context_strategy,
        "post_test_command_present": bool(result.post_test_command),
        "post_test_passed": result.post_test_passed,
        "post_test_summary": result.post_test_summary,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
    }
    return _redact_json_value(raw)


def summarize_job_promotion(result: JobPromotionResult) -> str:
    lines = [
        f"Job: {result.job_id}",
        f"Title: {result.job_title}",
        f"Promotion: {result.promotion_id}",
        f"Status: {result.status}",
        f"Approved: {result.approved}",
        f"Target: {_sanitize_path(result.target_repo)}",
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
        if result.file_readiness:
            lines.append(f"Would apply {len(result.files_planned)} file(s):")
            for fr in result.file_readiness:
                lines.append(f"  {fr.path} [{fr.kind}] "
                             f"baseline={fr.baseline_status} ws={fr.workspace_status}")
        lines.append("")
        lines.append(
            f"To apply: remedy do job-promote {result.job_id}"
            f" --repo <target> --approve"
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
        lines.append("")
        lines.append("No commits or pushes were made. Review and commit manually.")

    elif result.status == "promoted_test_failed":
        lines.append("")
        lines.append(f"Applied {len(result.files_applied)} file(s) but post-test FAILED.")
        lines.append("Manual review required. Changes are in working tree, not committed.")

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

    return _redact_secrets("\n".join(lines) + "\n")
