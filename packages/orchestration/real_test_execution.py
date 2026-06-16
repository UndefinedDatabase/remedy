"""
Real Test Execution + Snapshot/Rollback Proof v1 (Steps 1877-1916).

The first safe execution gate for Overnight Mode. Remedy can run ALLOWED test commands through the
EXISTING bounded safe runner, turn results into durable evidence, create Test Failure Artifacts on
failure, and record honest Snapshot/Rollback Proof that the Mission Contract can consume.

  Workers execute. Remedy governs. Tests and rollback proof become durable gates.

This module is a SAFE FACADE. It does NOT re-implement subprocess execution — it reuses
``test_execution_service.execute_test_run`` (the single contract-gated, leased, sandboxed, output-
capped, no-shell entry point) and ``repository_snapshot`` for recovery truth. It performs NO arbitrary
command execution, NO shell, NO network, NO provider/model/worker execution, NO auto-apply/approve/
repair, NO git writes.

Honesty rules:
  - A metadata snapshot is NOT a rollback restore. ``restore_available`` is False unless apply-scoped
    recovery material is verified; ``restore_tested`` is always False (no revert is performed here).
  - No fake test pass: pass requires the runner's ``passed`` status + a 0 exit code.
  - Raw stdout/stderr stays private (referenced by ``output_ref`` only); public surfaces get safe
    summaries; secrets/absolute paths scrubbed.

Public API::

    resolve_allowed_command(job_id, command_id, *, data_dir=None) -> (ok, candidate|None, reason)
    run_allowed_test(job_id, *, command_id="", timeout_seconds=None, data_dir=None) -> TestRunResult
    list_test_runs(job_id, data_dir=None) -> list[dict]
    get_test_run(test_run_id, data_dir=None) -> dict | None
    create_snapshot_proof(job_id, *, data_dir=None) -> SnapshotProof
    get_snapshot_proof / list_snapshot_proofs
    create_rollback_proof(job_id, snapshot_id, *, data_dir=None) -> RollbackProof
    get_rollback_proof
    test_execution_integrity(data_dir=None) -> dict
    export_*_json(...)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.provider_trust import _safe_path_label, _scrub_public

SCHEMA_VERSION = "real-test-execution-v1"
_RTE_DIRNAME = "real_test_execution"
_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-ant", "sk-proj",
                "api_key", "password", "secret_key")
# Shell metacharacters that must never appear in an allowed command argv token.
_SHELL_METACHARS = (";", "|", "&", "$", "`", ">", "<", "\n", "&&", "||", "$(")
# Destructive / forbidden tokens never allowed in a test command.
_FORBIDDEN_TOKENS = ("rm", "rmdir", "mkfs", "dd", ":(){", "sudo", "shutdown", "reboot", "curl",
                     "wget", "pip", "npm", "git", "ssh", "scp", "chmod", "chown")
_SNAPSHOT_SKIP_DIRS = {".git", "node_modules", ".data", "__pycache__", ".venv", "venv", ".mypy_cache",
                       ".pytest_cache", "dist", "build", ".tox"}
_SNAPSHOT_MAX_FILES = 5000


class TestRunStatus:
    NOT_STARTED = "not_started"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    BLOCKED_BY_CONTRACT = "blocked_by_contract"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    ERROR = "error"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_ddir(data_dir: Path | None) -> Path:
    from packages.orchestration.data_paths import resolve_data_root
    return Path(data_dir) if data_dir is not None else resolve_data_root()


# ---------------------------------------------------------------------------
# Models (Step 1879)
# ---------------------------------------------------------------------------


@dataclass
class TestRunRequest:
    request_id: str = ""
    job_id: str = ""
    repo_path: str = ""
    command_id: str = ""
    allowed_command: str = ""
    timeout_seconds: int = 0
    max_output_bytes: int = 0
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"request_id": self.request_id, "job_id": self.job_id,
                "repo_path": _safe_path_label(self.repo_path), "command_id": self.command_id,
                "allowed_command": self.allowed_command, "timeout_seconds": self.timeout_seconds,
                "max_output_bytes": self.max_output_bytes, "created_at": self.created_at,
                "schema_version": SCHEMA_VERSION}


@dataclass
class TestRunResult:
    test_run_id: str = ""
    job_id: str = ""
    command_id: str = ""
    status: str = TestRunStatus.NOT_STARTED
    exit_code: int | None = None
    duration_ms: int = 0
    output_ref: str = ""
    safe_summary: str = ""
    failure_artifact_id: str = ""
    snapshot_id: str = ""
    rollback_proof_id: str = ""
    stop_reason: str = ""
    next_safe_action: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "test_run_id": self.test_run_id, "job_id": self.job_id, "command_id": self.command_id,
            "status": self.status, "exit_code": self.exit_code, "duration_ms": self.duration_ms,
            "output_ref": self.output_ref, "safe_summary": _scrub_public(self.safe_summary)[:300],
            "failure_artifact_id": self.failure_artifact_id, "snapshot_id": self.snapshot_id,
            "rollback_proof_id": self.rollback_proof_id, "stop_reason": self.stop_reason,
            "next_safe_action": self.next_safe_action, "created_at": self.created_at,
            "schema_version": SCHEMA_VERSION,
        }


@dataclass
class SnapshotProof:
    snapshot_id: str = ""
    job_id: str = ""
    repo_path: str = ""
    created_at: str = ""
    strategy: str = "metadata_only"
    tracked_files_hash: str = ""
    dirty_files_summary: str = ""
    restore_available: bool = False
    safe_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id, "job_id": self.job_id,
            "repo_path": _safe_path_label(self.repo_path), "created_at": self.created_at,
            "strategy": self.strategy, "tracked_files_hash": self.tracked_files_hash,
            "dirty_files_summary": self.dirty_files_summary,
            "restore_available": self.restore_available,
            "safe_summary": _scrub_public(self.safe_summary)[:300], "schema_version": SCHEMA_VERSION,
        }


@dataclass
class RollbackProof:
    rollback_proof_id: str = ""
    job_id: str = ""
    snapshot_id: str = ""
    created_at: str = ""
    restore_available: bool = False
    restore_tested: bool = False
    strategy: str = "none_v1"
    safe_summary: str = ""
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollback_proof_id": self.rollback_proof_id, "job_id": self.job_id,
            "snapshot_id": self.snapshot_id, "created_at": self.created_at,
            "restore_available": self.restore_available, "restore_tested": self.restore_tested,
            "strategy": self.strategy, "safe_summary": _scrub_public(self.safe_summary)[:300],
            "limitations": list(self.limitations), "schema_version": SCHEMA_VERSION,
        }


def export_test_run_result_json(r: TestRunResult) -> dict[str, Any]:
    return r.to_dict()


def export_snapshot_proof_json(s: SnapshotProof) -> dict[str, Any]:
    return s.to_dict()


def export_rollback_proof_json(r: RollbackProof) -> dict[str, Any]:
    return r.to_dict()


# ---------------------------------------------------------------------------
# Allowed command resolution (Step 1880)
# ---------------------------------------------------------------------------


def _argv_is_safe(argv: tuple[str, ...] | list[str]) -> tuple[bool, str]:
    if not argv:
        return False, "empty argv"
    for tok in argv:
        if any(meta in tok for meta in _SHELL_METACHARS):
            return False, "shell metacharacter in command"
    # First token (the program) must not be a forbidden/destructive tool.
    prog = os.path.basename(str(argv[0]))
    if prog in _FORBIDDEN_TOKENS:
        return False, f"forbidden command program: {prog}"
    # No bare destructive token anywhere.
    for tok in argv:
        base = os.path.basename(str(tok))
        if base in ("rm", "rmdir", "mkfs", "dd", "sudo", "shutdown", "reboot"):
            return False, f"destructive token: {base}"
    return True, "ok"


def resolve_allowed_command(
    job_id: str, command_id: str, *, data_dir: Path | None = None,
) -> tuple[bool, Any, str]:
    """Resolve a command_id to a discovered, allowlisted TEST command. Returns (ok, candidate, reason).
    Never executes. Blocks unknown ids, non-test purposes, shell metacharacters, and destructive
    programs. An empty command_id is allowed (the safe runner will discover the best candidate)."""
    ddir = _resolve_ddir(data_dir)
    try:
        from packages.orchestration.command_discovery import discover_commands
        from packages.orchestration.storage import load_job
        job = load_job(UUID(job_id), ddir)
    except Exception:
        return False, None, "job not found or unloadable"
    repo = (job.metadata or {}).get("target_repo", "")
    if not repo:
        return False, None, "job has no target repo"
    try:
        candidates = discover_commands(job, Path(repo))
    except Exception:
        return False, None, "command discovery failed"
    if not command_id:
        # No explicit id → the safe runner will select the best test candidate itself.
        return True, None, "no command_id (runner selects best test candidate)"
    match = next((c for c in candidates if c.id == command_id), None)
    if match is None:
        return False, None, f"unknown command_id: {command_id}"
    if match.purpose != "test":
        return False, match, f"command '{command_id}' is not a test command (purpose={match.purpose})"
    ok, why = _argv_is_safe(match.argv)
    if not ok:
        return False, match, why
    return True, match, "ok"


# ---------------------------------------------------------------------------
# Run allowed test (Step 1883) — wraps the existing safe runner.
# ---------------------------------------------------------------------------


_STATUS_MAP = {
    "passed": TestRunStatus.PASSED,
    "failed": TestRunStatus.FAILED,
    "timeout": TestRunStatus.TIMEOUT,
    "environment_failure": TestRunStatus.ERROR,
    "blocked": TestRunStatus.BLOCKED_BY_CONTRACT,
}


def run_allowed_test(
    job_id: str, *, command_id: str = "", timeout_seconds: int | None = None,
    data_dir: Path | None = None,
) -> TestRunResult:
    """Run an ALLOWED test command via the existing contract-gated safe runner. NEVER uses shell or
    arbitrary commands; a non-allowlisted command_id is blocked before any execution."""
    res = TestRunResult(job_id=job_id, command_id=command_id, created_at=_now())

    ok, _cand, reason = resolve_allowed_command(job_id, command_id, data_dir=data_dir)
    if not ok:
        res.status = TestRunStatus.BLOCKED_BY_POLICY
        res.stop_reason = reason
        res.safe_summary = f"Command blocked by policy: {reason}"
        res.next_safe_action = f"remedy test discover {job_id} --json"
        return res

    try:
        from packages.orchestration.test_execution_service import (
            TestExecutionRequest,
            execute_test_run,
        )
        out = execute_test_run(TestExecutionRequest(
            job_id=job_id, source="real_test_execution_v1",
            command_id=command_id,
            requested_timeout_seconds=float(timeout_seconds) if timeout_seconds else None))
    except Exception as exc:  # the runner is the only execution path; failures stay safe metadata
        res.status = TestRunStatus.ERROR
        res.stop_reason = "runner_error"
        res.safe_summary = _scrub_public(f"Test runner error: {type(exc).__name__}")[:200]
        return res

    res.test_run_id = getattr(out, "test_run_id", "")
    # Honesty (R-0104): report the command the runner ACTUALLY executed, not just the
    # requested id. The runner now executes the requested command_id when supplied.
    res.command_id = getattr(out, "command_id", "") or command_id
    res.status = _STATUS_MAP.get(getattr(out, "status", ""), TestRunStatus.ERROR)
    res.exit_code = getattr(out, "exit_code", None)
    res.duration_ms = getattr(out, "duration_ms", 0)
    res.output_ref = getattr(out, "output_ref", "")
    res.failure_artifact_id = getattr(out, "failure_artifact_id", "")
    res.stop_reason = getattr(out, "stop_reason", "")
    res.safe_summary = getattr(out, "safe_summary", "")
    res.next_safe_action = getattr(out, "next_safe_action", "") or (
        f"remedy test result {res.test_run_id} --json" if res.test_run_id else
        f"remedy test status {job_id} --json")
    # Honesty: only the runner's "passed" + exit 0 is a real pass.
    if res.status == TestRunStatus.PASSED and (res.exit_code not in (0, None)):
        res.status = TestRunStatus.FAILED
        res.stop_reason = res.stop_reason or "nonzero_exit_despite_passed"
    return res


def list_test_runs(job_id: str, data_dir: Path | None = None) -> list[dict]:
    """List a job's persisted safe test records (job.metadata['test_runs']). No raw output."""
    ddir = _resolve_ddir(data_dir)
    try:
        from packages.orchestration.storage import load_job
        job = load_job(UUID(job_id), ddir)
    except Exception:
        return []
    runs = (job.metadata or {}).get("test_runs", [])
    return list(runs) if isinstance(runs, list) else []


def get_test_run(test_run_id: str, data_dir: Path | None = None) -> dict | None:
    ddir = _resolve_ddir(data_dir)
    # Scan all jobs' test_runs for the id.
    try:
        from packages.orchestration.storage import list_jobs, load_job
        for jref in list_jobs(ddir):
            jid = jref.get("id") if isinstance(jref, dict) else getattr(jref, "id", None)
            if jid is None:
                continue
            try:
                job = load_job(UUID(str(jid)), ddir)
            except Exception:
                continue
            for r in (job.metadata or {}).get("test_runs", []):
                if r.get("test_run_id") == test_run_id:
                    return r
    except Exception:
        return None
    return None


# ---------------------------------------------------------------------------
# Snapshot proof (Step 1881) — honest metadata snapshot; NOT a rollback restore.
# ---------------------------------------------------------------------------


def _rte_root(job_id: str, data_dir: Path) -> Path:
    base = job_id if job_id else "orchestrator"
    return data_dir / "workspaces" / base / _RTE_DIRNAME


def _snap_path(job_id: str, snapshot_id: str, data_dir: Path) -> Path:
    return _rte_root(job_id, data_dir) / "snapshots" / f"{snapshot_id}.json"


def _rollback_path(job_id: str, rollback_id: str, data_dir: Path) -> Path:
    return _rte_root(job_id, data_dir) / "rollbacks" / f"{rollback_id}.json"


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(data)
        try:
            os.chmod(tmp, mode)
        except OSError:
            pass
        os.replace(tmp, path)
        try:
            os.chmod(path, mode)
        except OSError:
            pass
        return True
    except OSError:
        return False


def _inventory_hash(repo_root: Path) -> tuple[str, int]:
    """Deterministic, bounded metadata hash over the repo's tracked-ish file inventory: sorted
    (rel_path, size) pairs. No file contents are read. Skips VCS/build/data dirs. Returns (hash, n)."""
    items: list[str] = []
    count = 0
    try:
        for root, dirs, files in os.walk(repo_root):
            dirs[:] = [d for d in dirs if d not in _SNAPSHOT_SKIP_DIRS and not d.startswith(".")]
            for fn in files:
                fp = Path(root) / fn
                try:
                    rel = fp.relative_to(repo_root).as_posix()
                    size = fp.stat().st_size
                except (OSError, ValueError):
                    continue
                items.append(f"{rel}:{size}")
                count += 1
                if count >= _SNAPSHOT_MAX_FILES:
                    break
            if count >= _SNAPSHOT_MAX_FILES:
                break
    except OSError:
        pass
    items.sort()
    h = hashlib.sha256("\n".join(items).encode("utf-8")).hexdigest()
    return h, count


def create_snapshot_proof(job_id: str, *, data_dir: Path | None = None) -> SnapshotProof:
    """Record an HONEST metadata snapshot proof of the job's repo. v1 is metadata-only: it captures a
    bounded inventory hash + a dirty-file count; it does NOT capture recovery content, so
    ``restore_available`` is False (a real rollback restore is not implemented in v1)."""
    ddir = _resolve_ddir(data_dir)
    proof = SnapshotProof(snapshot_id=f"snap-{uuid4().hex[:12]}", job_id=job_id, created_at=_now())
    try:
        from packages.orchestration.storage import load_job
        job = load_job(UUID(job_id), ddir)
        repo = (job.metadata or {}).get("target_repo", "")
    except Exception:
        repo = ""
    if not repo or not Path(repo).is_dir():
        proof.strategy = "unavailable"
        proof.safe_summary = "No repo available — snapshot proof unavailable."
        proof.restore_available = False
        _atomic_write(_snap_path(job_id, proof.snapshot_id, ddir),
                      json.dumps(proof.to_dict(), indent=2).encode("utf-8"))
        return proof
    proof.repo_path = repo
    h, n = _inventory_hash(Path(repo))
    proof.tracked_files_hash = h
    proof.dirty_files_summary = f"{n} file(s) inventoried (metadata only; no content captured)"
    proof.restore_available = False   # metadata-only — never claims restore
    proof.safe_summary = (f"Metadata snapshot recorded over {n} file(s). This is a snapshot POINT "
                          "(inventory hash) only — it does NOT provide rollback restore.")
    _atomic_write(_snap_path(job_id, proof.snapshot_id, ddir),
                  json.dumps(proof.to_dict(), indent=2).encode("utf-8"))
    return proof


def _load_proofs(kind: str, job_id: str | None, data_dir: Path) -> list[dict]:
    roots: list[Path] = []
    ws = data_dir / "workspaces"
    if job_id:
        roots.append(_rte_root(job_id, data_dir) / kind)
    else:
        try:
            for child in ws.iterdir():
                roots.append(child / _RTE_DIRNAME / kind)
        except OSError:
            pass
    out: list[dict] = []
    for root in roots:
        try:
            for f in sorted(root.iterdir()):
                if not f.is_file() or f.suffix != ".json":
                    continue
                try:
                    out.append(json.loads(f.read_text(encoding="utf-8")))
                except (OSError, ValueError):
                    continue
        except OSError:
            continue
    out.sort(key=lambda r: r.get("created_at", ""))
    return out


def list_snapshot_proofs(job_id: str | None = None, data_dir: Path | None = None) -> list[dict]:
    return _load_proofs("snapshots", job_id, _resolve_ddir(data_dir))


def get_snapshot_proof(snapshot_id: str, data_dir: Path | None = None) -> dict | None:
    return next((s for s in list_snapshot_proofs(data_dir=data_dir)
                 if s.get("snapshot_id") == snapshot_id), None)


# ---------------------------------------------------------------------------
# Rollback proof (Step 1882) — honest restore availability; never auto-reverts.
# ---------------------------------------------------------------------------


def create_rollback_proof(job_id: str, snapshot_id: str, *,
                          data_dir: Path | None = None) -> RollbackProof:
    """Record an HONEST rollback proof. v1 performs NO revert and NEVER sets restore_tested. Restore
    is available ONLY when apply-scoped recovery material is verified (via build_snapshot_truth);
    a metadata snapshot proof yields restore_available=False with explicit limitations."""
    ddir = _resolve_ddir(data_dir)
    rp = RollbackProof(rollback_proof_id=f"rbk-{uuid4().hex[:12]}", job_id=job_id,
                       snapshot_id=snapshot_id, created_at=_now())
    restore_available = False
    limitations = ["v1 performs no revert; restore_tested is always False"]
    # If a verified apply-scoped recovery exists for this job, restore MAY be available.
    try:
        from packages.orchestration.repository_snapshot import build_snapshot_truth
        truth = build_snapshot_truth(job_id, data_dir=ddir)
        if getattr(truth, "recovery_material_available", False) and getattr(truth, "snapshot_exists", False):
            restore_available = True
            rp.strategy = "apply_scoped_recovery"
        else:
            limitations.append("no verified apply-scoped recovery material for this job")
    except Exception:
        limitations.append("snapshot truth unavailable")
    # A metadata-only snapshot proof never provides restore, regardless of the above.
    snap = get_snapshot_proof(snapshot_id, ddir)
    if snap is not None and snap.get("strategy") in ("metadata_only", "unavailable"):
        restore_available = False
        limitations.append("referenced snapshot is metadata-only (no recovery content)")
    rp.restore_available = restore_available
    rp.restore_tested = False
    rp.limitations = limitations
    rp.safe_summary = ("Rollback restore AVAILABLE (apply-scoped recovery verified); not yet tested."
                       if restore_available else
                       "Rollback restore NOT available — metadata snapshot only; no revert in v1.")
    _atomic_write(_rollback_path(job_id, rp.rollback_proof_id, ddir),
                  json.dumps(rp.to_dict(), indent=2).encode("utf-8"))
    return rp


def list_rollback_proofs(job_id: str | None = None, data_dir: Path | None = None) -> list[dict]:
    return _load_proofs("rollbacks", job_id, _resolve_ddir(data_dir))


def get_rollback_proof(rollback_proof_id: str, data_dir: Path | None = None) -> dict | None:
    return next((r for r in list_rollback_proofs(data_dir=data_dir)
                 if r.get("rollback_proof_id") == rollback_proof_id), None)


# ---------------------------------------------------------------------------
# Integrity (Step 1893)
# ---------------------------------------------------------------------------


def audit_test_run_safety(run: dict[str, Any]) -> list[dict[str, str]]:
    """Flag unsafe test-run states. Safe public codes only."""
    if not isinstance(run, dict):
        return []
    out: list[dict[str, str]] = []
    rid = run.get("test_run_id", "")
    status = run.get("status", "")
    exit_code = run.get("exit_code")
    if status == "passed" and isinstance(exit_code, int) and exit_code != 0:
        out.append({"test_run_id": rid, "code": "passed_with_nonzero_exit"})
    blob = json.dumps(run).lower()
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"test_run_id": rid, "code": "raw_or_secret_in_public"})
    if "/home/" in blob or "/users/" in blob or "/root/" in blob:
        out.append({"test_run_id": rid, "code": "absolute_path_in_public"})
    return out


def audit_rollback_safety(rb: dict[str, Any], snapshots: dict[str, dict]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    rid = rb.get("rollback_proof_id", "")
    if rb.get("restore_tested") and not rb.get("restore_available"):
        out.append({"rollback_proof_id": rid, "code": "restore_tested_without_available"})
    # restore_available must not be claimed against a metadata-only snapshot.
    snap = snapshots.get(rb.get("snapshot_id", ""))
    if rb.get("restore_available") and snap is not None and snap.get("strategy") in (
            "metadata_only", "unavailable"):
        out.append({"rollback_proof_id": rid, "code": "restore_available_on_metadata_snapshot"})
    return out


def test_execution_integrity(data_dir: Path | None = None,
                             test_runs: list[dict] | None = None) -> dict[str, Any]:
    """Read-only invariant check over test runs + snapshot/rollback proofs. Safe codes only."""
    ddir = _resolve_ddir(data_dir)
    violations: list[dict] = []
    runs = test_runs if test_runs is not None else list_test_runs("", ddir)
    for r in (runs or []):
        violations.extend(audit_test_run_safety(r))
    snaps = {s.get("snapshot_id"): s for s in list_snapshot_proofs(data_dir=ddir)}
    for s in snaps.values():
        if s.get("restore_available") is True and s.get("strategy") in ("metadata_only", "unavailable"):
            violations.append({"snapshot_id": s.get("snapshot_id"),
                               "code": "snapshot_metadata_claims_restore"})
        blob = json.dumps(s).lower()
        if "/home/" in blob or "/users/" in blob:
            violations.append({"snapshot_id": s.get("snapshot_id"), "code": "absolute_path_in_public"})
    for rb in list_rollback_proofs(data_dir=ddir):
        violations.extend(audit_rollback_safety(rb, snaps))
    return {"version": 1, "test_run_count": len(runs or []), "snapshot_count": len(snaps),
            "rollback_count": len(list_rollback_proofs(data_dir=ddir)),
            "violation_count": len(violations), "passed": not violations, "violations": violations[:50]}


# Keep redaction helpers referenced for parity with the rest of the orchestration package.
_REDACTION_HELPERS = (_scrub_public, _safe_path_label, re)
