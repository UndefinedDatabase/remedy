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

from packages.orchestration.data_paths import jobs_dir
from packages.orchestration.evidence_mode import ExecutionMode
from packages.orchestration.pingpong_evidence import _validate_output_path
from packages.orchestration.pingpong_job import load_job_plan

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")
_DIFF_MAX_CHARS = 500_000


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _task_evidence_dir(job_id: str, task_id: str) -> Path:
    """Return the contained evidence directory for a task under the job.

    Only allows task IDs matching the expected format (T001, T002, ...) to
    prevent path traversal via corrupt or malicious task IDs.
    """
    if not task_id or not _SAFE_TASK_ID_RE.fullmatch(task_id):
        raise ValueError(
            f"Unsafe task ID {task_id!r}: must match T<digits> (e.g. T001)."
        )
    base = jobs_dir() / job_id / "evidence"
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
            if path:
                changed.append(path)

    full_tracked_diff = ""
    diff = _git(["diff", "HEAD"])
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
            if not upath:
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

    prov_hasher = hashlib.sha256()
    prov_hasher.update(tracked_diff_sha256.encode("utf-8"))
    for uf in sorted(untracked_file_hashes, key=lambda u: u["path"]):
        prov_hasher.update(uf["path"].encode("utf-8"))
        prov_hasher.update(uf["sha256"].encode("utf-8"))
        prov_hasher.update(str(uf["size_bytes"]).encode("utf-8"))
    provenance_sha256 = prov_hasher.hexdigest()

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


def _resolve_task_scope(task: Any, ws: _WorkspaceDiff) -> dict[str, Any]:
    """Determine whether attestation covers per-task or full workspace scope."""
    safe_diff_files = getattr(task, "safe_diff_files", None) or []
    if safe_diff_files:
        return {
            "workspace_scope": "task_scoped",
            "task_scope_known": True,
            "task_scoped_files": list(safe_diff_files),
        }
    return {
        "workspace_scope": "full_working_tree",
        "task_scope_known": False,
        "task_scoped_files": [],
    }


def attest_operator_repair(
    job_id: str,
    task_id: str,
    note: str,
    repo_path: str,
) -> dict[str, Any]:
    """Record a manual operator repair for one task as valid evidence.

    Loads the persisted job, verifies the task exists, collects and hashes the
    workspace diff, and writes four evidence artifacts into the task's evidence
    directory. Never calls a provider. Never mutates the target repo or the
    persisted job state. Applies per task, never per job.

    Returns a JSON-serializable dict describing the written artifacts, or an
    ``{"error": ...}`` dict on a non-existent job or task.
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
    timestamp = _now()
    original_info = _resolve_original_task_info(task)
    scope_info = _resolve_task_scope(task, ws)

    task_dir = _task_evidence_dir(job_id, task_id)
    task_dir.mkdir(parents=True, exist_ok=True)

    written: dict[str, str] = {}

    def _write_json(filename: str, data: Any) -> None:
        target = _validate_output_path(str(task_dir), filename)
        target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        written[filename] = str(target)

    _write_json(
        "provider_evidence.json",
        {
            "task_id": task_id,
            "execution_mode": ExecutionMode.MANUAL_OPERATOR_REPAIR.value,
            "builder_provider": "operator",
            "reviewer_provider": "operator",
            "provider_call_count": 0,
            "prompt_trace_available": False,
            "prompt_trace_status": "not_applicable_manual_repair",
            "actual_provider_available": False,
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
            "timestamp": timestamp,
        },
    )

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
        "changed_files": ws.changed_files,
        "note": note,
        "timestamp": timestamp,
        **scope_info,
    }
    if ws.tracked_diff_truncated:
        provenance_data["tracked_diff_truncated"] = True
    _write_json("manual_repair_provenance.json", provenance_data)

    safe_diff_parts = [ws.tracked_diff]
    for uf in ws.untracked_file_hashes:
        safe_diff_parts.append(
            f"--- /dev/null\n+++ b/{uf['path']}\n"
            f"# new untracked file (sha256={uf['sha256']}, "
            f"size={uf['size_bytes']})\n"
        )
    safe_diff_target = _validate_output_path(str(task_dir), "safe.diff")
    safe_diff_target.write_text("".join(safe_diff_parts), encoding="utf-8")
    written["safe.diff"] = str(safe_diff_target)

    return {
        "job_id": job_id,
        "task_id": task_id,
        "diff_sha256": ws.provenance_sha256,
        "changed_files": ws.changed_files,
        "out_dir": str(task_dir),
        "files": written,
        **original_info,
        **scope_info,
    }
