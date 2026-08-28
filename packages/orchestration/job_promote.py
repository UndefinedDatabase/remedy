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

from packages.orchestration.exec_guard import run_guarded_test_command
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
    Blocks ALL destination symlinks — even those resolving inside target.
    Writing through a symlink changes a different path than the planned one.
    """
    try:
        dest_resolved = (target / rel_path).resolve()
    except OSError:
        return f"dest_resolve_failed: {rel_path}"

    target_resolved = target.resolve()
    if not str(dest_resolved).startswith(str(target_resolved) + os.sep) and dest_resolved != target_resolved:
        return f"dest_escapes_target: {rel_path}"

    dest = target / rel_path
    if dest.is_symlink():
        return f"dest_is_symlink: {rel_path}"

    current = dest.parent
    while current != target and current != current.parent:
        if current.exists() and current.is_symlink():
            return f"dest_parent_symlink: {rel_path}"
        current = current.parent

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
                    # The reviewed change includes the file mode, so drift detection
                    # must see it: an external chmod on an otherwise untouched
                    # target file would silently be reverted by promotion.
                    "baseline_mode": proof.baseline_mode,
                    "final_mode": proof.final_mode,
                }
            else:
                consolidated[proof.path]["final_workspace_sha256"] = (
                    proof.final_workspace_sha256
                )
                consolidated[proof.path]["final_mode"] = proof.final_mode
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
            baseline_mode = proof.get("baseline_mode", "")
            current_mode = _mode_of(target_file)
            if current_target_hash != baseline_hash:
                blocks.append(f"target_changed_since_job: {rel_path}")
                b_status = "target_changed_since_job"
            elif baseline_mode and current_mode != baseline_mode:
                # Content still matches the baseline, but somebody chmod'ed the
                # target after the job ran. Promoting would silently revert that.
                blocks.append(f"target_mode_changed_since_job: {rel_path}")
                b_status = "target_mode_changed_since_job"
            else:
                b_status = "target_matches_baseline"
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
    status: str = ""  # blocked, dry_run, approved_apply_started, promoted, promoted_test_failed, promoted_record_update_failed
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
    #: True when the operator passed --skip-blocked, i.e. acknowledged the blocked
    #: set and asked for the remainder anyway. ``files_blocked`` still names every
    #: path that was withheld, so a promotion that skipped is never silent.
    skip_blocked: bool = False
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
    # F006 fidelity + honest temp cleanup
    source_changed_files: list[str] = field(default_factory=list)
    reviewed_task_files: list[str] = field(default_factory=list)
    unexpected_source_files: list[str] = field(default_factory=list)
    missing_source_files: list[str] = field(default_factory=list)
    modes_applied: dict[str, str] = field(default_factory=dict)
    temporary_worktree_removed: bool = False
    temporary_registration_removed: bool = False
    cleanup_status: str = ""          # "" | "clean" | "failed"
    cleanup_error: str = ""


# ---------------------------------------------------------------------------
# Promotion logic
# ---------------------------------------------------------------------------

def _block(
    result: JobPromotionResult,
    reason: str,
    *,
    persist: bool = True,
) -> JobPromotionResult:
    result.status = "blocked"
    result.blocked_reason = reason
    result.blocked_reasons.append(reason)
    result.finished_at = datetime.now(timezone.utc).isoformat()
    return result


def _safe_persist(
    job_id: str,
    result: JobPromotionResult,
    applied: list[str],
    *,
    final: bool = False,
) -> None:
    """Persist promotion record, structuring any failure after target mutation.

    ``final=True`` is the one post-cleanup write: a failure there is reported
    honestly rather than pretending a durable record (or a durable preview) exists.
    """
    try:
        _persist_job_promotion(job_id, result)
    except OSError as exc:
        if final and not applied:
            original_status = result.status
            result.status = "record_update_failed"
            result.blocked_reason = (
                f"promotion_record_update_failed: {exc} — "
                f"original_status={original_status}; no durable record exists"
            )
            result.blocked_reasons.append(result.blocked_reason)
            result.finished_at = datetime.now(timezone.utc).isoformat()
            return
        if applied:
            original_status = result.status
            original_reason = result.blocked_reason
            result.status = "promoted_record_update_failed"
            result.blocked_reason = (
                f"promotion_record_update_failed: {exc} — "
                f"original_status={original_status}, "
                f"original_reason={original_reason}, "
                f"target files may have changed ({len(applied)} applied)"
            )
            result.finished_at = datetime.now(timezone.utc).isoformat()


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
        # Guarded since F085 T002b: rlimits, an env allowlist, a pinned cwd and the
        # guard's own wall deadline replace the bare spawn. The observable outcome is
        # unchanged — same returncode, same TimeoutExpired, same FileNotFoundError —
        # except that the guard hands back BYTES, which the decode below turns into
        # the str this function has always returned.
        proc = run_guarded_test_command(
            argv,
            timeout_sec=timeout_sec,
            cwd=str(target),
        )
    except FileNotFoundError:
        return False, f"Test command not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return False, f"Test command timed out after {timeout_sec}s"

    output = (proc.stdout or b"").decode("utf-8", "replace") + (proc.stderr or b"").decode("utf-8", "replace")
    if len(output) > _TEST_OUTPUT_CAP:
        output = output[:_TEST_OUTPUT_CAP] + "\n[OUTPUT TRUNCATED]"
    passed = proc.returncode == 0
    summary = f"exit={proc.returncode}"
    if output.strip():
        last_lines = output.strip().splitlines()[-5:]
        summary += " | " + " ".join(last_lines)
    return passed, summary


# ---------------------------------------------------------------------------
# F006: materialize a promotion source from the verified JobPlan hand-off
# ---------------------------------------------------------------------------

@dataclass
class PromotionSource:
    """A temporary, read-only materialization of a completed job's hand-off."""

    path: Path
    repo: Path
    temp_root: Path
    materialized: bool = False


def _materialize_promotion_source(job: Any) -> tuple[PromotionSource | None, str]:
    """Deprecated shim kept for callers/tests that only want (source, error).

    The lifecycle owner is :func:`_materialize_promotion_source_owned`, which never
    cleans up behind the caller's back: a temporary worktree that could not be
    removed must reach the caller, not vanish into a discarded return value.
    """
    source, err = _materialize_promotion_source_owned(job)
    if source is not None and err:
        # A partially materialized source with an error: the OWNER cleans it up.
        return None, err
    return source, err


def _materialize_promotion_source_owned(job: Any) -> tuple[PromotionSource | None, str]:
    """Rebuild the completed job's result from base commit + verified result.diff.

    The execution worktree is deliberately disposable: after a clean cleanup the
    authoritative hand-off is the recorded base commit plus the job directory's
    ``result.diff`` (hash- and size-verified). This creates a TEMPORARY DETACHED
    git worktree at the recorded base commit, ``git apply --check``s the diff and
    then applies it. The original execution worktree is never recreated at its
    recorded path, no branch is merged, nothing is committed and nothing is pushed.
    """
    import subprocess
    import tempfile

    from packages.orchestration.job_evidence import job_result_diff_source

    src, err = job_result_diff_source(job)
    if src is None:
        return None, f"job_result_diff_invalid: {err}"

    repo = Path(job.repo_path)
    base = getattr(job, "worktree_base_commit", "")
    if not base:
        return None, "job_result_diff_invalid: no recorded base commit"

    from packages.orchestration import worktrees as W
    if not W.is_git_repo(repo):
        return None, f"target_not_git_repository: {repo}"
    if not W.commit_exists(repo, base):
        return None, f"base_commit_missing: {base[:12]}"

    temp_root = Path(tempfile.mkdtemp(prefix="remedy-promo-"))
    ws = temp_root / "source"
    source = PromotionSource(path=ws, repo=repo, temp_root=temp_root)

    # From here on a temporary directory (and possibly a registered worktree) may
    # exist, so the SOURCE is always returned — even on failure — and the caller
    # owns the checked cleanup. Nothing is cleaned up and discarded here.
    try:
        proc = subprocess.run(
            ["git", "worktree", "add", "--detach", str(ws), base],
            cwd=str(repo), capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            return source, f"promotion_worktree_failed: {proc.stderr.strip()[:200]}"
        source.materialized = True

        diff_arg = str(src)
        check = subprocess.run(
            ["git", "apply", "--check", diff_arg], cwd=str(ws),
            capture_output=True, text=True, timeout=120,
        )
        if check.returncode != 0:
            return source, f"job_diff_not_applicable: {check.stderr.strip()[:200]}"

        applied = subprocess.run(
            ["git", "apply", diff_arg], cwd=str(ws),
            capture_output=True, text=True, timeout=120,
        )
        if applied.returncode != 0:
            return source, f"job_diff_apply_failed: {applied.stderr.strip()[:200]}"
    except Exception as exc:
        return source, f"promotion_materialization_error: {type(exc).__name__}: {exc}"

    return source, ""


def _run_cleanup_git(argv: list[str], *, cwd: str, timeout: int) -> tuple[bool, str]:
    """Run one cleanup git command. NEVER raises: returns (ok, error_text).

    A cleanup step that explodes (timeout, missing git, any OS error) must not
    abort the rest of the cleanup or replace the promotion outcome — it must be
    recorded and the remaining steps must still run.
    """
    try:
        proc = subprocess.run(
            argv, cwd=cwd, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"{' '.join(argv[:3])} timed out after {timeout}s"
    except FileNotFoundError as exc:
        return False, f"{' '.join(argv[:3])} could not run: FileNotFoundError: {exc}"
    except OSError as exc:
        return False, f"{' '.join(argv[:3])} failed: {type(exc).__name__}: {exc}"
    except Exception as exc:                      # last resort: still no raise
        return False, f"{' '.join(argv[:3])} failed: {type(exc).__name__}: {exc}"
    if proc.returncode != 0:
        return False, f"{' '.join(argv[:3])} failed: {proc.stderr.strip()[:150]}"
    return True, ""


def _failed_cleanup(error: str) -> dict[str, Any]:
    """A cleanup result for the case where cleanup itself could not be completed."""
    return {
        "temporary_worktree_removed": False,
        "temporary_registration_removed": False,
        "cleanup_status": "failed",
        "cleanup_error": error,
    }


def _cleanup_promotion_source(source: PromotionSource | None) -> dict[str, Any]:
    """Remove the temporary promotion worktree — and SAY what actually happened.

    TOTAL function: it never raises. Every step (remove, prune, physical delete,
    inventory, path check) is guarded independently, each failure is recorded, and
    the remaining steps still run — a cleanup exception must never escape and take
    the promotion result, the applied-file list and the durable record with it.
    """
    out: dict[str, Any] = {
        "temporary_worktree_removed": False,
        "temporary_registration_removed": False,
        "cleanup_status": "clean",
        "cleanup_error": "",
    }
    if source is None:
        return out

    import shutil

    errors: list[str] = []
    try:
        if source.materialized:
            ok, err = _run_cleanup_git(
                ["git", "worktree", "remove", "--force", str(source.path)],
                cwd=str(source.repo), timeout=120,
            )
            if not ok:
                errors.append(err)
            ok, err = _run_cleanup_git(
                ["git", "worktree", "prune"],
                cwd=str(source.repo), timeout=60,
            )
            if not ok:
                errors.append(err)

        # Best-effort secondary cleanup — a failure is still recorded.
        try:
            if source.temp_root.exists():
                shutil.rmtree(source.temp_root)
        except Exception as exc:
            errors.append(
                f"temporary directory not deleted: {type(exc).__name__}: {exc}")

        try:
            from packages.orchestration import worktrees as W
            registered = W._worktree_registered(source.repo, source.path)
        except Exception as exc:
            registered = True
            errors.append(f"worktree inventory failed: {type(exc).__name__}: {exc}")
        out["temporary_registration_removed"] = not registered
        if registered:
            errors.append(f"temporary worktree {source.path.name} is still registered")

        try:
            still_there = source.path.exists()
        except Exception as exc:
            still_there = True
            errors.append(f"path check failed: {type(exc).__name__}: {exc}")
        out["temporary_worktree_removed"] = not still_there
        if still_there:
            errors.append(
                f"temporary worktree directory {source.path.name} still exists")
    except Exception as exc:                      # belt and braces: never raise
        errors.append(f"cleanup aborted: {type(exc).__name__}: {exc}")

    if errors:
        out["cleanup_status"] = "failed"
        out["cleanup_error"] = "; ".join(errors)
    return out


def promote_job(
    job_id: str,
    target_repo: str = ".",
    *,
    approve: bool = False,
    dry_run: bool = False,
    test_command: str = "",
    skip_blocked: bool = False,
) -> JobPromotionResult:
    """Promote reviewed job workspace changes into target repo.

    Without --approve, returns dry-run preview only. Never auto-promotes.
    No git commit, no git push, no git reset, no git checkout.

    Every promoted file must come from a task apply manifest.
    No workspace fallback scanning. Baseline-aware target safety.

    ``skip_blocked`` is the operator's SECOND, explicit decision, taken after
    reading the blocked list — it does not weaken the fence. See
    ``_promote_from_workspace`` for what it does and, more importantly, does not
    change.
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
        skip_blocked=skip_blocked,
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

    # --- Promotion source ---
    # F006: a completed worktree job has NO live workspace by design (a clean
    # cleanup removed it). Its hand-off is the recorded base commit plus the
    # verified result.diff, materialized into a TEMPORARY detached worktree here.
    # This function is the single lifecycle owner: from the moment a temporary
    # directory may exist, every exit path runs the checked cleanup, records its
    # result on the returned object, and persists that final record exactly once.
    promo_source: PromotionSource | None = None
    out = result
    try:
        if getattr(job, "isolation_mode", "copy") == "worktree":
            promo_source, perr = _materialize_promotion_source_owned(job)
            if perr:
                out = _block(result, perr, persist=False)
            else:
                out = _promote_from_workspace(
                    job, result, promo_source.path, target_repo,
                    approve=approve, dry_run=dry_run, test_command=test_command,
                    skip_blocked=skip_blocked,
                    persist_final=False,
                )
        else:
            ws_path = job.job_workspace_path
            if not ws_path:
                return _block(result, "no_job_workspace_path")
            workspace = Path(ws_path)
            if not workspace.is_dir():
                return _block(result, f"workspace_missing: {ws_path}")
            return _promote_from_workspace(
                job, result, workspace, target_repo,
                approve=approve, dry_run=dry_run, test_command=test_command,
                skip_blocked=skip_blocked,
            )
    finally:
        if promo_source is not None:
            try:
                cleanup = _cleanup_promotion_source(promo_source)
            except Exception as exc:
                # _cleanup_promotion_source is total, but a cleanup bug must still
                # never destroy the promotion outcome or the durable record.
                cleanup = _failed_cleanup(
                    f"cleanup raised unexpectedly: {type(exc).__name__}: {exc}")
            out.temporary_worktree_removed = cleanup["temporary_worktree_removed"]
            out.temporary_registration_removed = cleanup["temporary_registration_removed"]
            out.cleanup_status = cleanup["cleanup_status"]
            out.cleanup_error = cleanup["cleanup_error"]

    if promo_source is not None and out.cleanup_status == "failed":
        # Never claim a clean run. The promotion outcome and the applied-file list
        # are preserved: the target WAS touched if the status says so. A cleanup
        # failure during a materialization failure reports BOTH.
        if out.status == "promoted":
            out.status = "promoted_cleanup_failed"
        elif out.status == "dry_run":
            out.status = "dry_run_cleanup_failed"
        elif out.status == "blocked" and not out.files_applied:
            out.status = "materialization_failed_cleanup_failed"
        out.blocked_reasons = list(out.blocked_reasons) + [
            f"temporary_promotion_cleanup_failed: {out.cleanup_error}"
        ]

    # ONE final persistence, after cleanup, for every materialized outcome — so the
    # persisted record's cleanup fields and status match the object the CLI got.
    if promo_source is not None:
        _safe_persist(job_id, out, out.files_applied, final=True)
    return out


def _reviewed_files_and_proofs(job: Any) -> tuple[list[str], dict[str, Any]]:
    from packages.orchestration.pingpong_job import (
        _latest_task_proofs,
        _reviewed_task_files,
    )
    return _reviewed_task_files(job), _latest_task_proofs(job)


def _check_source_coverage(job: Any, result: JobPromotionResult, workspace: Path) -> str:
    """The materialized source's changed paths must equal the reviewed file set.

    An extra file in the root diff (a finalization hook writing ``rogue.txt``) would
    otherwise be materialized into the promotion source and quietly ignored, so the
    hand-off, the task evidence and the promotion would all disagree. Any extra or
    missing path blocks.
    """
    import subprocess

    proc = subprocess.run(
        ["git", "status", "--porcelain", "-z", "--untracked-files=all"],
        cwd=str(workspace), capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0:
        return f"promotion_source_inspect_failed: {proc.stderr.strip()[:150]}"
    changed = sorted({
        entry[3:] for entry in proc.stdout.split("\0") if len(entry) > 3
    })
    reviewed, _proofs = _reviewed_files_and_proofs(job)

    result.source_changed_files = changed
    result.reviewed_task_files = reviewed
    result.unexpected_source_files = sorted(set(changed) - set(reviewed))
    result.missing_source_files = sorted(set(reviewed) - set(changed))

    if result.unexpected_source_files or result.missing_source_files:
        return (
            "promotion_coverage_failed: "
            f"unexpected={result.unexpected_source_files} "
            f"missing={result.missing_source_files}"
        )
    return ""


def _mode_of(path: Path) -> str:
    from packages.orchestration import worktrees as W
    return W.file_mode(path)


def _promote_from_workspace(
    job: Any,
    result: JobPromotionResult,
    workspace: Path,
    target_repo: str,
    *,
    approve: bool,
    dry_run: bool,
    test_command: str,
    skip_blocked: bool = False,
    persist_final: bool = True,
) -> JobPromotionResult:
    """The existing baseline-aware promotion, against a resolved source.

    ``persist_final=False`` means an outer owner (the temporary-worktree lifecycle)
    will write the ONE final record after cleanup, so this function must not write
    a record that would later disagree with the returned object.

    ``skip_blocked`` CHANGES ONE DECISION AND NOTHING ELSE: whether a non-empty
    blocked set aborts the whole promotion. It does not widen what may be written.
    Every blocked path is still detected by the same ``_is_blocked_path``,
    ``_validate_dest_containment`` and ``_validate_source_containment`` checks, is
    still kept out of ``planned``, is still never opened for writing, and is still
    named in ``files_blocked`` and in the summary. What it buys is the operator's
    second explicit decision, taken AFTER reading that list: promote the remainder
    as its own atomic change set. That is a different question from "apply
    everything or nothing", and answering it does not make the fence weaker —
    a silent skip would, and this is the opposite of silent.
    """
    job_id = job.job_id

    def _persist_outcome(applied_files: list[str]) -> None:
        if persist_final:
            _safe_persist(job_id, result, applied_files, final=True)

    # --- Target repo exists ---
    target = Path(target_repo).resolve()
    if not target.is_dir():
        return _block(result, f"target_not_directory: {target_repo}")

    # --- Fidelity: the materialized source must be EXACTLY the reviewed work ---
    if getattr(job, "isolation_mode", "copy") == "worktree":
        cov_err = _check_source_coverage(job, result, workspace)
        if cov_err:
            return _block(result, cov_err)

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

    if blocked and not skip_blocked:
        return _block(result, f"blocked_paths: {blocked}")

    if not planned:
        # Reached with a non-empty blocked set only when --skip-blocked was passed
        # and EVERY file was blocked: there is no remainder to promote, so the
        # honest answer is still a block rather than an empty success.
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

    # --- Mode fidelity: the source must still carry the reviewed file mode ---
    _reviewed, mode_proofs = _reviewed_files_and_proofs(job)
    mode_blocks: list[str] = []
    for rel_path in planned:
        proof = mode_proofs.get(rel_path)
        expected = getattr(proof, "final_mode", "") if proof else ""
        if not expected:
            continue
        actual = _mode_of(workspace / rel_path)
        if actual != expected:
            mode_blocks.append(
                f"{rel_path}: source mode {actual} != reviewed {expected}"
            )
    if mode_blocks:
        return _block(result, f"mode_check_failed: {mode_blocks}")

    # --- Dry-run or unapproved: preview only ---
    if dry_run or not approve:
        result.status = "dry_run"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        _persist_outcome([])
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

    # --- Durable pre-apply promotion record ---
    result.status = "approved_apply_started"
    result.files_applied = []
    try:
        _persist_job_promotion(job_id, result)
    except OSError as exc:
        return _block(result, f"pre_apply_record_failed: {exc}")

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
            _persist_outcome(applied)
            return result

        dest_reason = _validate_dest_containment(target, rel_path)
        if dest_reason:
            result.status = "blocked"
            result.blocked_reason = f"dest_unsafe_at_apply: {rel_path}: {dest_reason}"
            result.files_applied = applied
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

        dest = target / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            content = ws_file.read_bytes()
            dest.write_bytes(content)
            reviewed_mode = _mode_of(ws_file)
            if reviewed_mode == "100755":
                dest.chmod(dest.stat().st_mode | 0o111)
            else:
                dest.chmod(dest.stat().st_mode & ~0o111)
            result.modes_applied[rel_path] = reviewed_mode
            applied.append(rel_path)
        except OSError as exc:
            result.status = "blocked"
            result.blocked_reason = f"write_failed: {rel_path}: {exc}"
            result.files_applied = applied
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
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
                _persist_outcome(applied)
                return result
            src_mode, dst_mode = _mode_of(ws_file), _mode_of(dest)
            if src_mode != dst_mode:
                # A filesystem that cannot represent the reviewed mode must block,
                # not claim a faithful promotion.
                result.status = "blocked"
                result.blocked_reason = (
                    f"post_apply_mode_mismatch: {rel_path}: "
                    f"target {dst_mode} != reviewed {src_mode}"
                )
                result.finished_at = datetime.now(timezone.utc).isoformat()
                _persist_outcome(applied)
                return result
        except OSError as exc:
            result.status = "blocked"
            result.blocked_reason = f"post_apply_verify_failed: {rel_path}: {exc}"
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

    # --- Post-promotion tests ---
    if test_command:
        passed, summary = _run_post_test(test_command, target)
        result.post_test_passed = passed
        result.post_test_summary = summary
        if not passed:
            result.status = "promoted_test_failed"
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

    result.status = "promoted"
    result.finished_at = datetime.now(timezone.utc).isoformat()
    _persist_outcome(applied)
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
        "source_changed_files": result.source_changed_files,
        "reviewed_task_files": result.reviewed_task_files,
        "unexpected_source_files": result.unexpected_source_files,
        "missing_source_files": result.missing_source_files,
        "modes_applied": result.modes_applied,
        "temporary_worktree_cleanup": {
            "temporary_worktree_removed": result.temporary_worktree_removed,
            "temporary_registration_removed": result.temporary_registration_removed,
            "cleanup_status": result.cleanup_status,
            "cleanup_error": result.cleanup_error,
        },
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
        "skip_blocked": result.skip_blocked,
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


def _blocked_path_names(files_blocked: list[str]) -> list[str]:
    """The bare paths out of ``files_blocked``, whose entries read ``path: reason``."""
    return [entry.split(":", 1)[0].strip() for entry in files_blocked]


def _next_step_for_promotion(result: JobPromotionResult) -> str:
    """The honest ``Next:`` line a stalled promotion owes its operator.

    Every other stalled surface in Remedy ends with one — `remedy do`,
    `remedy status`, the orchestrator's ``next_safe_action``, the proof chain —
    and a blocked promotion used to print its reason and stop, leaving the
    operator's only remaining move to go and read the source.

    The line names the route that ACTUALLY applies to the block in hand.
    ``--skip-blocked`` lifts a protected-path block and nothing else, so it is
    offered where it is true and explicitly ruled out where it is not.
    """
    reason = result.blocked_reason or ""

    if reason.startswith("blocked_paths:"):
        names = _blocked_path_names(result.files_blocked)
        listed = ", ".join(names) if names else "the paths listed above"
        remaining = len(result.files_planned)
        return (
            f"Next: remove {listed} from the job workspace and re-run, or re-run "
            f"with --skip-blocked to promote the remaining {remaining} file(s) and "
            f"deliberately leave {listed} unpromoted."
        )

    if reason == "no_promotable_files" and result.files_blocked:
        names = _blocked_path_names(result.files_blocked)
        listed = ", ".join(names) if names else "every file"
        return (
            f"Next: every file in this job is protected ({listed}), so there is no "
            f"remainder for --skip-blocked to promote. Remove the protected path(s) "
            f"from the job workspace and re-run."
        )

    return (
        "Next: resolve the blocked reason above and re-run. --skip-blocked lifts a "
        "protected-path block only and does not apply to this one."
    )


def summarize_job_promotion(result: JobPromotionResult) -> str:
    lines = [
        f"Job: {result.job_id}",
        f"Title: {result.job_title}",
        f"Promotion: {result.promotion_id}",
        f"Status: {result.status}",
        f"Approved: {result.approved}",
        f"Target: {_sanitize_path(result.target_repo)}",
    ]
    if result.cleanup_status:
        lines.append(f"Temp worktree cleanup: {result.cleanup_status}")
        if result.cleanup_error:
            lines.append(f"  Cleanup error: {result.cleanup_error}")

    if result.cleanup_status == "failed":
        # Never let a reader infer the damage from a status string alone: say
        # plainly whether the target was touched, which files, and what is left over.
        lines.append("")
        if result.files_applied:
            lines.append("The target was changed.")
            lines.append(f"Files applied: {result.files_applied}")
        else:
            lines.append("The target was NOT changed"
                         + (" (dry-run only)." if result.dry_run or not result.approved
                            else "."))
        lines.append("Temporary promotion cleanup failed.")
        lines.append(f"Cleanup error: {result.cleanup_error}")
        if not result.temporary_registration_removed:
            lines.append(
                "A temporary git worktree registration may remain "
                "(check `git worktree list`)."
            )
        if not result.temporary_worktree_removed:
            lines.append("A temporary promotion directory may remain on disk.")
        lines.append("Manual cleanup is required.")

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
        if result.skip_blocked and result.files_blocked:
            # Never let a partial promotion read as a whole one: say what was
            # withheld, in the same breath as what was applied.
            lines.append(
                f"--skip-blocked deliberately left {len(result.files_blocked)} "
                f"protected path(s) unpromoted; they were not written to the target "
                f"and are listed below."
            )
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

    elif result.status == "promoted_record_update_failed":
        lines.append("")
        lines.append(f"WARNING: Applied {len(result.files_applied)} file(s) but promotion record update FAILED.")
        lines.append(f"Reason: {result.blocked_reason}")
        lines.append("Target files may have changed. Manual review required.")
        lines.append("Pre-apply record exists. Final record could not be written.")

    elif result.status == "approved_apply_started":
        lines.append("")
        lines.append("Apply in progress. This status should not appear in final output.")

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

    # A blocked promotion ALWAYS ends with its next step, after the file lists so
    # the operator reads the paths before the route through them.
    if result.status == "blocked":
        lines.append("")
        lines.append(_next_step_for_promotion(result))

    return _redact_secrets("\n".join(lines) + "\n")
