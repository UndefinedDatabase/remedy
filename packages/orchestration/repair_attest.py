"""Operator repair attestation — records a manual operator repair as a valid
evidence path for a single task.

When an operator fixes a task by hand (no provider ran), that work still needs
to be recorded as first-class evidence so downstream verifiers and gates treat
the task as honestly executed rather than as a phantom-provider run.

This module collects the workspace diff since the last valid state, hashes it,
and writes four schema-valid evidence artifacts into the task's evidence
directory:

    provider_evidence.json          execution_mode = "manual_operator_repair"
    review.json                     verdict = "operator_attested", reviewer = operator
    token_accounting.json           actual_available = false, reason = "manual"
    manual_repair_provenance.json   diff_sha256, changed_files, note, timestamp

Attestation applies per task, never per job. Each call targets exactly one
(job_id, task_id) pair.

Public API:
    attest_operator_repair(job_id, task_id, note, repo_path) -> dict
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.data_paths import job_evidence_dir
from packages.orchestration.evidence_mode import ExecutionMode
from packages.orchestration.pingpong_evidence import _validate_output_path
from packages.orchestration.pingpong_job import load_job_plan

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")
_DIFF_MAX_CHARS = 500_000


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_outside_repo(rel: str) -> bool:
    """True when a declared path escapes the repository root."""
    if not rel or rel.startswith("/") or rel.startswith("~"):
        return True
    parts = Path(rel).parts
    return ".." in parts


def is_attestable_source(rel: str) -> bool:
    """F9 (round 13): is this file part of a task's ATTESTED source change?

    `.agent/context.md`, `.agent/plan.md` and `.agent/live_review.md` are OPERATOR STATE — the
    notes the operator keeps about the work, not the work. Every authoritative Evidence view
    already says so and excludes them (`final_verifier._OPERATIONAL_PREFIXES`,
    `change_provenance_gate._EXCLUDE_DIRS`, the packager's alignment scan). The ATTESTED union
    was the one view that did not, so a hand-attested diff containing them disagreed with every
    proof set built from the same change — and the package was correctly refused as
    non-authoritative:

        changed-file union mismatch vs current_change_content_proof.file_hashes:
          only_in_union=['.agent/context.md', '.agent/live_review.md', '.agent/plan.md']

    One policy, applied at the one place that dissented. The files still travel in the review ZIP
    as non-authoritative operator context — excluded from the proofs, not from the reader.

    The predicate is the EXISTING one (A6: no parallel taxonomy) — imported, not re-stated.
    """
    from packages.orchestration.final_verifier import _is_source_for_alignment

    return _is_source_for_alignment(rel)


# ---------------------------------------------------------------------------
# Canonical provenance hashing — ONE shared implementation used by both the
# writer (this module) and the validator (build_review_manifest). Any drift
# between the two would let a tampered bundle validate, so they must call this.
# ---------------------------------------------------------------------------

def canonical_provenance_sha256(
    tracked_diff_sha256: str,
    untracked_file_hashes: list[dict[str, Any]],
) -> str:
    """Deterministic provenance hash over tracked diff + sorted untracked files.

    Recomputed from: the tracked diff hash, then for each untracked file (sorted
    by path) the path, its content sha256, and its byte size.
    """
    h = hashlib.sha256()
    h.update(str(tracked_diff_sha256).encode("utf-8"))
    for uf in sorted(untracked_file_hashes, key=lambda u: str(u.get("path", ""))):
        h.update(str(uf.get("path", "")).encode("utf-8"))
        h.update(str(uf.get("sha256", "")).encode("utf-8"))
        h.update(str(uf.get("size_bytes", "")).encode("utf-8"))
    return h.hexdigest()


def build_safe_diff_text(
    tracked_diff: str,
    untracked_file_hashes: list[dict[str, Any]],
) -> str:
    """Build the exact ``safe.diff`` content: tracked diff + untracked headers.

    Kept in one place so the emitted content and its recorded ``safe_diff_sha256``
    can never diverge.
    """
    parts = [tracked_diff]
    for uf in untracked_file_hashes:
        parts.append(
            f"--- /dev/null\n+++ b/{uf['path']}\n"
            f"# new untracked file (sha256={uf['sha256']}, "
            f"size={uf['size_bytes']})\n"
        )
    return "".join(parts)


def sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def parse_safe_diff_paths(safe_diff_text: str) -> list[str]:
    """Return sorted unique file paths represented in a ``safe.diff``.

    Reads ``+++ b/<path>`` headers (skipping ``/dev/null``); handles both the
    tracked ``git diff`` hunks and the untracked ``+++ b/<path>`` markers.
    """
    paths: set[str] = set()
    for line in safe_diff_text.splitlines():
        if line.startswith("+++ "):
            p = line[4:].strip()
            if p.startswith("b/"):
                p = p[2:]
            if p and p != "/dev/null":
                paths.add(p)
    return sorted(paths)


def _task_evidence_dir(job_id: str, task_id: str) -> Path:
    """Return the contained evidence directory for a task under the job.

    Only allows task IDs matching the expected format (T001, T002, ...) to
    prevent path traversal via corrupt or malicious task IDs.
    """
    if not task_id or not _SAFE_TASK_ID_RE.fullmatch(task_id):
        raise ValueError(
            f"Unsafe task ID {task_id!r}: must match T<digits> (e.g. T001)."
        )
    base = job_evidence_dir(job_id)
    return _validate_output_path(str(base), f"task_runs/{task_id}")


@dataclass
class _WorkspaceDiff:
    tracked_diff: str
    tracked_diff_sha256: str
    tracked_diff_truncated: bool
    changed_files: list[str]
    untracked_file_hashes: list[dict[str, Any]]
    provenance_sha256: str


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()


def _collect_workspace_diff(repo_path: str) -> _WorkspaceDiff:
    """Collect tracked diff and untracked file hashes for provenance.

    Uses git when the path is a git repo. Returns an empty result when git is
    unavailable or the path is not a git repo.
    """
    empty = _WorkspaceDiff(
        tracked_diff="",
        tracked_diff_sha256=hashlib.sha256(b"").hexdigest(),
        tracked_diff_truncated=False,
        changed_files=[],
        untracked_file_hashes=[],
        provenance_sha256=hashlib.sha256(b"").hexdigest(),
    )
    repo = Path(repo_path)
    if not repo.exists():
        return empty

    def _git(args: list[str]) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                ["git", *args],
                cwd=str(repo),
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError):
            return None

    inside = _git(["rev-parse", "--is-inside-work-tree"])
    if inside is None or inside.returncode != 0:
        return empty

    changed: list[str] = []
    status = _git(["status", "--porcelain", "-u"])
    if status is not None and status.returncode == 0:
        for line in status.stdout.splitlines():
            if not line.strip():
                continue
            path = line[3:]
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            path = path.strip().strip('"')
            # F9 (round 13): operator-state files are not part of the attested SOURCE change.
            # Every authoritative Evidence view already excludes them; the attested union was
            # the lone dissenter, and the mismatch made the whole package non-authoritative.
            if path and is_attestable_source(path):
                changed.append(path)

    # F9 (round 13): the diff is scoped to the ATTESTABLE paths, so `safe.diff` and
    # `changed_files` are the same account BY CONSTRUCTION. The packager requires those two views
    # to be exactly equal, so filtering only the file list would simply move the mismatch:
    #   "safe.diff paths != provenance.changed_files (only_in_diff=['.agent/plan.md'])"
    # `--` ends the option list, so no path can be read as a flag.
    full_tracked_diff = ""
    tracked_targets = [p for p in changed if is_attestable_source(p)]
    diff = _git(["diff", "HEAD", "--", *tracked_targets]) if tracked_targets else None
    if diff is not None and diff.returncode == 0:
        full_tracked_diff = diff.stdout
    tracked_diff_sha256 = hashlib.sha256(
        full_tracked_diff.encode("utf-8")
    ).hexdigest()
    tracked_diff_truncated = len(full_tracked_diff) > _DIFF_MAX_CHARS
    if tracked_diff_truncated:
        tracked_diff = (
            full_tracked_diff[:_DIFF_MAX_CHARS] + "\n# [truncated]\n"
        )
    else:
        tracked_diff = full_tracked_diff

    untracked_file_hashes: list[dict[str, Any]] = []
    ls_files = _git(["ls-files", "--others", "--exclude-standard"])
    if ls_files is not None and ls_files.returncode == 0:
        for upath in ls_files.stdout.splitlines():
            upath = upath.strip()
            if not upath or not is_attestable_source(upath):   # F9: same one policy
                continue
            full = repo / upath
            if full.is_file():
                file_hash = _hash_file(full)
                try:
                    size_bytes = full.stat().st_size
                except OSError:
                    size_bytes = 0
                untracked_file_hashes.append({
                    "path": upath,
                    "sha256": file_hash,
                    "size_bytes": size_bytes,
                })
                if upath not in changed:
                    changed.append(upath)

    provenance_sha256 = canonical_provenance_sha256(
        tracked_diff_sha256, untracked_file_hashes,
    )

    return _WorkspaceDiff(
        tracked_diff=tracked_diff,
        tracked_diff_sha256=tracked_diff_sha256,
        tracked_diff_truncated=tracked_diff_truncated,
        changed_files=sorted(set(changed)),
        untracked_file_hashes=untracked_file_hashes,
        provenance_sha256=provenance_sha256,
    )


def collect_diff_stat(repo_path: str) -> str:
    """Return a concise diff stat for CLI confirmation display."""
    repo = Path(repo_path)
    if not repo.exists():
        return "no repo"
    try:
        stat = subprocess.run(
            ["git", "diff", "--stat", "HEAD"],
            cwd=str(repo), capture_output=True, text=True, timeout=15,
        )
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=str(repo), capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return "diff stat unavailable"
    parts: list[str] = []
    if stat.returncode == 0 and stat.stdout.strip():
        parts.append(stat.stdout.strip())
    ut_lines = [l.strip() for l in (untracked.stdout or "").splitlines() if l.strip()]
    if ut_lines:
        parts.append(f"untracked: {len(ut_lines)} file(s)")
        for f in ut_lines[:10]:
            parts.append(f"  ?? {f}")
        if len(ut_lines) > 10:
            parts.append(f"  ... and {len(ut_lines) - 10} more")
    return "\n".join(parts) if parts else "no changes detected"


def _resolve_original_task_info(task: Any) -> dict[str, Any]:
    """Extract the original task status and failure information."""
    status = getattr(task, "status", "unknown")
    error = getattr(task, "error", "") or ""
    failure_kind = "none"
    if status == "blocked":
        if "target_repo_mutated" in error:
            failure_kind = "target_repo_mutated"
        elif "completion_gate_failed" in error:
            failure_kind = "completion_gate_failed"
        else:
            failure_kind = "blocked"
    elif status == "failed":
        failure_kind = "failed"
    elif status == "skipped":
        failure_kind = "skipped_no_run"
    elif status == "pending":
        failure_kind = "pending_no_run"
    return {
        "original_task_status": status,
        "original_failure_kind": failure_kind,
        "original_failure_summary": error[:500] if error else "",
    }


def _resolve_task_scope(
    task: Any, ws: _WorkspaceDiff, task_scoped: bool = False,
) -> dict[str, Any]:
    """Determine whether attestation covers per-task or full workspace scope.

    When ``task_scoped`` is set the freshly collected manual diff
    (``ws.changed_files``) is authoritative and a stale provider-run
    ``safe_diff_files`` never overrides it — the operator attested exactly what
    is in the isolated worktree. Otherwise the legacy behaviour applies: prefer a
    recorded ``safe_diff_files`` if present, else fall back to the full tree.
    """
    if task_scoped:
        return {
            "workspace_scope": "task_scoped",
            "task_scope_known": True,
            "task_scoped_files": sorted(ws.changed_files),
            "task_scope_source": "attested_diff",
        }
    safe_diff_files = getattr(task, "safe_diff_files", None) or []
    if safe_diff_files:
        return {
            "workspace_scope": "task_scoped",
            "task_scope_known": True,
            "task_scoped_files": list(safe_diff_files),
            "task_scope_source": "recorded_safe_diff_files",
        }
    return {
        "workspace_scope": "full_working_tree",
        "task_scope_known": False,
        "task_scoped_files": [],
        "task_scope_source": "full_working_tree",
    }


def _prior_provider_call_count(task: Any) -> int | None:
    """Best-effort provider-call count of the task's ORIGINAL execution.

    Precedence: an explicit ``provider_call_count`` attribute on the task, then
    the persisted run's prompt-trace summary. Returns None when unknown.
    """
    explicit = getattr(task, "provider_call_count", None)
    if isinstance(explicit, int) and not isinstance(explicit, bool):
        return explicit
    run_id = getattr(task, "run_id", "") or ""
    if not run_id:
        return None
    try:
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        trace = Path(_pingpong_runs_dir()) / run_id / "prompt_trace_summary.json"
        if trace.exists():
            data = json.loads(trace.read_text(encoding="utf-8"))
            return int(data.get("builder_prompts", 0)) + int(data.get("reviewer_prompts", 0))
    except (OSError, ValueError, json.JSONDecodeError, ImportError):
        return None
    return None


def _resolve_prior_execution(task: Any) -> dict[str, Any] | None:
    """Describe the task's ORIGINAL execution layer, preserved separately.

    A manual completion supersedes — but never erases — an earlier provider run.
    Returns None when there was no prior real execution (a freshly planned task
    that was only ever completed by hand).
    """
    status = str(getattr(task, "status", "") or "")
    final_status = str(getattr(task, "final_status", "") or "")
    run_id = getattr(task, "run_id", "") or ""
    prior_calls = _prior_provider_call_count(task)
    had_provider_run = bool(run_id) or status in ("blocked", "failed") or bool(final_status)
    if not had_provider_run:
        return None
    return {
        "mode": "provider_backed",
        "status": final_status or status or "unknown",
        "run_id": run_id,
        "provider_call_count": prior_calls,
    }


def attest_operator_repair(
    job_id: str,
    task_id: str,
    note: str,
    repo_path: str,
    *,
    task_scoped: bool = False,
    allowed_files: list[str] | None = None,
    linked_prior_job_id: str = "",
) -> dict[str, Any]:
    """Record a manual operator repair for one task as valid evidence.

    Loads the persisted job, verifies the task exists, collects and hashes the
    workspace diff, and writes four evidence artifacts into the task's evidence
    directory. Never calls a provider. Never mutates the target repo or the
    persisted job state. Applies per task, never per job.

    When ``task_scoped`` is set the freshly collected diff is the authoritative
    scope of the completion (a stale provider-run ``safe_diff_files`` is ignored).
    In that mode ``allowed_files`` is the EXACT expected task file set: the
    attested diff must equal it exactly (not merely be a subset). The diff must
    be non-empty; unexpected files, missing files, duplicate expected paths, and
    paths outside the repository are each rejected and reported separately.

    ``linked_prior_job_id`` records a superseded/related prior job through a
    generic mechanism (stored in this task's provenance) — never a hardcoded,
    feature-specific path. Empty means no linked prior job, which is valid.

    Returns a JSON-serializable dict describing the written artifacts, or an
    ``{"error": ...}`` dict on a non-existent job/task or a scope violation.
    """
    job = load_job_plan(job_id)
    if job is None:
        return {"error": f"Job {job_id!r} not found", "job_id": job_id}

    task = next((t for t in job.tasks if t.task_id == task_id), None)
    if task is None:
        return {
            "error": f"Task {task_id!r} not found in job {job_id!r}",
            "job_id": job_id,
            "task_id": task_id,
        }

    if not note or not note.strip():
        note = "operator attested manual repair"

    ws = _collect_workspace_diff(repo_path)

    if task_scoped:
        if not ws.changed_files:
            return {
                "error": (
                    "task-scoped attestation requires a non-empty diff, but the "
                    f"worktree {repo_path!r} has no changes for {task_id!r}"
                ),
                "job_id": job_id,
                "task_id": task_id,
            }
        if allowed_files:
            # Exact-scope: the attested diff must equal the expected set exactly.
            expected_list = [str(f) for f in allowed_files]
            duplicate_expected = sorted(
                {f for f in expected_list if expected_list.count(f) > 1}
            )
            if duplicate_expected:
                return {
                    "error": (
                        f"duplicate expected paths for {task_id!r}: "
                        f"{duplicate_expected}"
                    ),
                    "job_id": job_id, "task_id": task_id,
                    "duplicate_expected_files": duplicate_expected,
                }
            outside_repo = sorted(f for f in expected_list if _is_outside_repo(f))
            if outside_repo:
                return {
                    "error": (
                        f"expected paths outside the repository for {task_id!r}: "
                        f"{outside_repo}"
                    ),
                    "job_id": job_id, "task_id": task_id,
                    "outside_repo_files": outside_repo,
                }
            expected_set = set(expected_list)
            actual_set = set(ws.changed_files)
            unexpected = sorted(actual_set - expected_set)
            missing = sorted(expected_set - actual_set)
            if unexpected or missing:
                return {
                    "error": (
                        f"task-scoped attestation for {task_id!r} does not match the "
                        f"exact expected file set "
                        f"(unexpected={unexpected}, missing={missing})"
                    ),
                    "job_id": job_id, "task_id": task_id,
                    "unexpected_files": unexpected,
                    "missing_files": missing,
                    # Back-compat alias retained for existing callers/tests.
                    "out_of_scope_files": unexpected,
                }

    timestamp = _now()
    original_info = _resolve_original_task_info(task)
    scope_info = _resolve_task_scope(task, ws, task_scoped=task_scoped)
    prior_execution = _resolve_prior_execution(task)

    task_dir = _task_evidence_dir(job_id, task_id)
    task_dir.mkdir(parents=True, exist_ok=True)

    written: dict[str, str] = {}

    def _write_json(filename: str, data: Any) -> None:
        target = _validate_output_path(str(task_dir), filename)
        target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        written[filename] = str(target)

    from packages.orchestration.provider_token_evidence import PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION
    _write_json(
        "provider_evidence.json",
        {
            "schema_version": PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION,
            "task_id": task_id,
            "execution_mode": ExecutionMode.MANUAL_OPERATOR_REPAIR.value,
            "builder_provider": "operator",
            "reviewer_provider": "operator",
            "provider_call_count": 0,
            "prompt_trace_available": False,
            "prompt_trace_status": "not_applicable_manual_repair",
            "actual_provider_available": False,
            # Two honest layers: the manual completion (this attestation) never
            # calls a provider; any earlier provider-backed execution is
            # preserved separately and never folded into the completion total.
            "completion_execution_mode": ExecutionMode.MANUAL_OPERATOR_REPAIR.value,
            "completion_provider_call_count": 0,
            "supersedes_prior_execution": prior_execution is not None,
            "prior_execution": prior_execution,
        },
    )

    _write_json(
        "review.json",
        {
            "task_id": task_id,
            "verdict": "operator_attested",
            "final_verdict": "operator_attested",
            "reviewer": "operator",
            "note": note,
            "timestamp": timestamp,
            "total_reviews": 1,
            "human_final_reviewer_required": True,
            **original_info,
            "reviews": [
                {
                    "round": 1,
                    "kind": "operator_attestation",
                    "verdict": "operator_attested",
                    "reviewer": "operator",
                    "summary": note,
                    "finding_count": 0,
                    "findings": [],
                }
            ],
        },
    )

    _write_json(
        "token_accounting.json",
        {
            "task_id": task_id,
            "kind": "manual",
            "actual_available": False,
            "actual_tokens_available": False,
            "reason": "manual",
            # A manual operator attestation made zero provider calls. The manual-completion validator
            # requires this to be the integer 0 (matching the canonical manual_attestation producer);
            # omitting it made an attested export disagree with the validator's schema.
            "provider_call_count": 0,
            "timestamp": timestamp,
        },
    )

    # Build the safe.diff content once and hash the exact emitted bytes so the
    # recorded safe_diff_sha256 can never drift from what is written.
    safe_diff_content = build_safe_diff_text(ws.tracked_diff, ws.untracked_file_hashes)
    safe_diff_digest = sha256_text(safe_diff_content)

    provenance_data: dict[str, Any] = {
        "schema_version": "1.0.0",
        "manual_operator_repair": True,
        "no_provider_calls": True,
        "task_id": task_id,
        "job_id": job_id,
        "tracked_diff_sha256": ws.tracked_diff_sha256,
        "untracked_file_hashes": ws.untracked_file_hashes,
        "diff_sha256": ws.provenance_sha256,
        "provenance_sha256": ws.provenance_sha256,
        "safe_diff_sha256": safe_diff_digest,
        "changed_files": ws.changed_files,
        "note": note,
        "timestamp": timestamp,
        "supersedes_prior_execution": prior_execution is not None,
        "prior_execution": prior_execution,
        # Generic linked-prior-job mechanism (any feature, any repo). Empty
        # string means no linked prior job, which is valid.
        "linked_prior_job_id": linked_prior_job_id or "",
        **scope_info,
    }
    if ws.tracked_diff_truncated:
        provenance_data["tracked_diff_truncated"] = True
    _write_json("manual_repair_provenance.json", provenance_data)

    safe_diff_target = _validate_output_path(str(task_dir), "safe.diff")
    safe_diff_target.write_text(safe_diff_content, encoding="utf-8")
    written["safe.diff"] = str(safe_diff_target)

    return {
        "job_id": job_id,
        "task_id": task_id,
        "diff_sha256": ws.provenance_sha256,
        "changed_files": ws.changed_files,
        "out_dir": str(task_dir),
        "files": written,
        "completion_execution_mode": ExecutionMode.MANUAL_OPERATOR_REPAIR.value,
        "completion_provider_call_count": 0,
        "supersedes_prior_execution": prior_execution is not None,
        "prior_execution": prior_execution,
        "linked_prior_job_id": linked_prior_job_id or "",
        **original_info,
        **scope_info,
    }
