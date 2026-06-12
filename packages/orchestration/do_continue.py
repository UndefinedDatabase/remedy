"""
remedy do --continue v1 — one controlled continuation cycle (Steps 1164-1177).

Given an approved patch intent, performs exactly ONE evidence-backed cycle:

    eligibility → verified snapshot → apply → real test → proof → safe final stop

Hard rules (enforced here and in central services):
  - No automatic repair, no automatic revert, no multi-cycle loops.
  - No real provider/Ollama execution. Test runs go through the central
    Test Execution Service (real pytest via scripts/remedy_pytest.sh).
  - Permission, approval, Run Contract, snapshot, and test gates live in central
    services — this orchestrator calls them, it does not reimplement them.
  - Crash-safe and idempotent: a retry after a successful apply must not apply
    again; a retry after a completed test must not consume test budget again; a
    retry after failure must not create a duplicate Failure Artifact / Fix Task.
  - No raw source, diff, snapshot blob, output, secrets, or tracebacks in any
    public surface.

Public API::

    evaluate_continue_eligibility(job_id, intent_id=None, data_dir=None) -> ContinueEligibility
    run_do_continue(request) -> ContinueResult
    export_continue_result_json(result) -> dict
    summarize_continue_result(result) -> str
"""

from __future__ import annotations

import fcntl
import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID


# ---------------------------------------------------------------------------
# Phase / stop-reason vocabulary (Step 1164)
# ---------------------------------------------------------------------------

class ContinuePhase:
    ELIGIBILITY = "eligibility"
    SNAPSHOT = "snapshot"
    APPLY = "apply"
    TEST = "test"
    PROOF = "proof"
    FINAL_STOP = "final_stop"


CONTINUE_PHASES = (
    ContinuePhase.ELIGIBILITY,
    ContinuePhase.SNAPSHOT,
    ContinuePhase.APPLY,
    ContinuePhase.TEST,
    ContinuePhase.PROOF,
    ContinuePhase.FINAL_STOP,
)


class ContinueStopReason:
    COMPLETED_VERIFIED = "completed_verified"
    TEST_FAILED_REPAIR_AVAILABLE = "test_failed_repair_available"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"
    BLOCKED_INELIGIBLE = "blocked_ineligible"
    SNAPSHOT_FAILED = "snapshot_failed"
    APPLY_FAILED = "apply_failed"
    TEST_BLOCKED = "test_blocked"
    LEASE_UNAVAILABLE = "lease_unavailable"
    ERROR = "error"


# ---------------------------------------------------------------------------
# Models (Step 1164)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ContinueRequest:
    """Input to run_do_continue."""

    job_id: str
    intent_id: str = ""
    source: str = "cli_v1"


@dataclass(frozen=True)
class ContinueCheckpoint:
    """Durable record of a completed/attempted phase. Safe IDs only."""

    phase: str
    status: str            # completed | failed | blocked | skipped
    at: str
    evidence_status: str = "complete"
    ids: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ContinuePhaseResult:
    """One phase outcome surfaced in the result."""

    phase: str
    status: str            # completed | failed | blocked | skipped | resumed
    safe_summary: str


@dataclass
class ContinueEligibility:
    """Outcome of evaluate_continue_eligibility. No raw content."""

    eligible: bool
    job_id: str
    intent_id: str = ""
    apply_id: str = ""
    blockers: list[str] = field(default_factory=list)
    next_safe_action: str = ""
    safe_summary: str = ""


@dataclass
class ContinueResult:
    """Full result of one continuation cycle. No raw content."""

    version: int = 1
    job_id: str = ""
    task_id: str = ""
    intent_id: str = ""
    apply_id: str = ""
    snapshot_id: str = ""
    test_run_id: str = ""
    failure_artifact_id: str = ""
    contract_id: str = ""
    phases: list[ContinuePhaseResult] = field(default_factory=list)
    current_phase: str = ContinuePhase.ELIGIBILITY
    stop_reason: str = ""
    next_safe_action: str = ""
    proof_status: str = ""
    evidence_status: str = "complete"   # complete | partial | degraded | unknown
    usage_before: dict[str, Any] = field(default_factory=dict)
    usage_after: dict[str, Any] = field(default_factory=dict)
    generated_at: str = ""
    safe_summary: str = ""


# ---------------------------------------------------------------------------
# Durable checkpoint store (Step 1168)
# ---------------------------------------------------------------------------


def _continue_dir(job_id: str, data_dir: Path) -> Path:
    return data_dir / "workspaces" / job_id / "do_continue"


def _checkpoints_path(job_id: str, data_dir: Path) -> Path:
    return _continue_dir(job_id, data_dir) / "checkpoints.json"


def load_checkpoints(job_id: str, data_dir: Path) -> list[ContinueCheckpoint]:
    """Load durable phase checkpoints. Returns [] when none/unreadable."""
    path = _checkpoints_path(job_id, data_dir)
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError):
        return []
    out: list[ContinueCheckpoint] = []
    for c in raw if isinstance(raw, list) else []:
        out.append(ContinueCheckpoint(
            phase=c.get("phase", ""),
            status=c.get("status", ""),
            at=c.get("at", ""),
            evidence_status=c.get("evidence_status", "complete"),
            ids=c.get("ids", {}) or {},
        ))
    return out


def save_checkpoint(
    job_id: str,
    data_dir: Path,
    checkpoint: ContinueCheckpoint,
) -> bool:
    """Append a checkpoint atomically. Returns True if persisted."""
    cdir = _continue_dir(job_id, data_dir)
    try:
        cdir.mkdir(parents=True, exist_ok=True)
        existing = load_checkpoints(job_id, data_dir)
        existing.append(checkpoint)
        payload = [
            {
                "phase": c.phase, "status": c.status, "at": c.at,
                "evidence_status": c.evidence_status, "ids": c.ids,
            }
            for c in existing
        ]
        path = _checkpoints_path(job_id, data_dir)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_bytes(json.dumps(payload, indent=2, sort_keys=True).encode("utf-8"))
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def latest_checkpoint(
    checkpoints: list[ContinueCheckpoint], phase: str
) -> ContinueCheckpoint | None:
    """Return the most recent checkpoint for *phase*, or None."""
    for c in reversed(checkpoints):
        if c.phase == phase:
            return c
    return None


def _phase_completed(checkpoints: list[ContinueCheckpoint], phase: str) -> bool:
    cp = latest_checkpoint(checkpoints, phase)
    return cp is not None and cp.status in ("completed", "resumed")


# ---------------------------------------------------------------------------
# Continuation lease (Step 1167)
# ---------------------------------------------------------------------------


@dataclass
class ContinuationLease:
    """File-backed exclusive lease keyed by job + repo + intent.

    Deterministic acquire order (job → repo → intent). Released on every exit.
    A stale inactive lease is recoverable because flock is released when the
    holding process dies; the lock file is unlinked on clean release.
    """

    job_id: str
    repo_key: str
    intent_id: str
    lease_dir: Path
    _fhs: list[Any] = field(default_factory=list, repr=False, compare=False)
    _paths: list[Path] = field(default_factory=list, repr=False, compare=False)

    def _names(self) -> list[str]:
        import hashlib
        repo_hash = hashlib.sha256(self.repo_key.encode("utf-8")).hexdigest()[:32]
        # Deterministic order — no deadlock.
        return [
            f"cont-job-{self.job_id}.lock",
            f"cont-repo-{repo_hash}.lock",
            f"cont-intent-{self.job_id}-{self.intent_id}.lock",
        ]

    def acquire(self, *, timeout_seconds: float = 2.0) -> bool:
        self.lease_dir.mkdir(parents=True, exist_ok=True)
        for name in self._names():
            path = self.lease_dir / name
            fh = open(path, "w")  # noqa: SIM115 — must stay open while held
            deadline = time.monotonic() + timeout_seconds
            acquired = False
            while True:
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fh.write(f"{os.getpid()}\n{datetime.now(timezone.utc).isoformat()}\n")
                    fh.flush()
                    acquired = True
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        break
                    time.sleep(0.05)
            if not acquired:
                fh.close()
                self.release()
                return False
            self._fhs.append(fh)
            self._paths.append(path)
        return True

    def release(self) -> None:
        # Reverse order release; both leases freed on every exit path.
        while self._fhs:
            fh = self._fhs.pop()
            try:
                fcntl.flock(fh, fcntl.LOCK_UN)
                fh.close()
            except OSError:
                pass
        while self._paths:
            p = self._paths.pop()
            try:
                p.unlink(missing_ok=True)
            except OSError:
                pass


def _repo_key(job: Any) -> str:
    repo = job.metadata.get("target_repo", "") or ""
    if not repo:
        return ""
    try:
        return str(Path(repo).resolve())
    except OSError:
        return repo


# ---------------------------------------------------------------------------
# Eligibility (Step 1165)
# ---------------------------------------------------------------------------


def evaluate_continue_eligibility(
    job_id: str,
    intent_id: str | None = None,
    data_dir: Path | None = None,
) -> ContinueEligibility:
    """Decide whether one continuation cycle may proceed (Step 1165).

    Read-only. Every block returns a real next-safe-action. Gates:
      job exists; exactly one approved intent (or explicit intent_id); intent
      approved and not rejected; no conflicting unresolved apply; write
      permission; persisted contract allows patch_apply; stop_before_apply is
      false; safe target repository; valid patch structure; test permission +
      budget configured; no active continuation lease.
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, JobNotFoundError
    from packages.orchestration.approval_queue import (
        list_patch_intents, APPROVAL_APPROVED, APPROVAL_REJECTED,
    )
    from packages.orchestration.permissions import is_allowed, Capability
    from packages.orchestration.run_contract import (
        ensure_contract, evaluate_run_action, ContractAction,
    )
    from packages.orchestration.repository_snapshot import (
        build_snapshot_truth, list_durable_apply_ids, load_durable_apply_record,
    )

    data_dir = Path(data_dir) if data_dir is not None else resolve_data_root()
    elig = ContinueEligibility(eligible=False, job_id=job_id)

    # 1. Job exists.
    try:
        job = load_job(UUID(job_id), data_dir)
    except (ValueError, JobNotFoundError):
        elig.blockers.append("job_not_found")
        elig.next_safe_action = "remedy job list --json"
        elig.safe_summary = "Job not found."
        return elig

    intents = list_patch_intents(job)
    # 2. Resolve the target intent.
    if intent_id:
        match = next((i for i in intents if i["intent_id"] == intent_id), None)
        if match is None:
            elig.blockers.append("intent_not_found")
            elig.next_safe_action = f"remedy change list {job_id} --json"
            elig.safe_summary = "Supplied intent_id not found."
            return elig
        target = match
    else:
        approved = [i for i in intents if i["state"] == APPROVAL_APPROVED]
        if not approved:
            elig.blockers.append("no_approved_intent")
            elig.next_safe_action = f"remedy change list {job_id} --json"
            elig.safe_summary = "No approved patch intent to continue."
            return elig
        if len(approved) > 1:
            elig.blockers.append("multiple_approved_intents")
            elig.next_safe_action = (
                f"remedy do --continue {job_id} --intent-id <id> --json"
            )
            elig.safe_summary = (
                f"{len(approved)} approved intents — specify one with --intent-id."
            )
            return elig
        target = approved[0]

    iid = target["intent_id"]
    elig.intent_id = iid
    elig.apply_id = iid  # markdown apply uses intent_id as apply_id

    # 3. Approval state.
    if target["state"] == APPROVAL_REJECTED:
        elig.blockers.append("intent_rejected")
        elig.next_safe_action = f"remedy change list {job_id} --json"
        elig.safe_summary = "Intent was rejected."
        return elig
    if target["state"] != APPROVAL_APPROVED:
        elig.blockers.append("intent_not_approved")
        elig.next_safe_action = f"remedy patch approve {job_id} {iid}"
        elig.safe_summary = "Intent is not approved."
        return elig

    # 4. No conflicting unresolved apply from a DIFFERENT intent.
    for aid in list_durable_apply_ids(job_id, data_dir):
        rec = load_durable_apply_record(aid, job_id, data_dir)
        if rec is None or rec.intent_id == iid:
            continue
        if rec.state in ("applied", "test_pending"):
            elig.blockers.append("conflicting_unresolved_apply")
            elig.next_safe_action = f"remedy change proof {job_id} --json"
            elig.safe_summary = "Another apply is unresolved — resolve it first."
            return elig

    # 5. Write permission.
    if not is_allowed(job, Capability.repo_generated_write):
        elig.blockers.append("permission_denied")
        elig.next_safe_action = f"remedy job permit {job_id} repo_generated_write allow"
        elig.safe_summary = "repo_generated_write permission not granted."
        return elig

    # 6/7. stop_before_apply must be false, then the contract must allow apply.
    contract = ensure_contract(job)
    if contract.stop_before_apply:
        elig.blockers.append("stop_before_apply_true")
        elig.next_safe_action = f"remedy contract set {job_id} stop_before_apply false"
        elig.safe_summary = "Contract has stop_before_apply=true."
        return elig
    decision = evaluate_run_action(contract, ContractAction.PATCH_APPLY)
    if not decision.allowed:
        elig.blockers.append("contract_apply_denied")
        elig.next_safe_action = "remedy contract inspect " + job_id + " --json"
        elig.safe_summary = f"Contract blocks apply: {decision.reason[:80]}"
        return elig

    # 8. Safe target repository.
    repo = job.metadata.get("target_repo", "") or ""
    if not repo or not Path(repo).is_dir():
        elig.blockers.append("no_target_repo")
        elig.next_safe_action = f"remedy job attach-repo {job_id} <path>"
        elig.safe_summary = "No safe target repository attached."
        return elig

    # 9. Valid patch structure.
    if not target.get("target_path"):
        elig.blockers.append("invalid_patch_structure")
        elig.next_safe_action = f"remedy change list {job_id} --json"
        elig.safe_summary = "Patch intent has no target path."
        return elig

    # 10. Test permission + budget (testing is required for the cycle).
    if not is_allowed(job, Capability.repo_test_run):
        elig.blockers.append("test_permission_missing")
        elig.next_safe_action = f"remedy job permit {job_id} repo_test_run allow"
        elig.safe_summary = "repo_test_run permission not granted."
        return elig
    if contract.max_test_runs <= 0:
        elig.blockers.append("test_budget_unconfigured")
        elig.next_safe_action = f"remedy contract set {job_id} max_test_runs 1"
        elig.safe_summary = "Test budget (max_test_runs) is 0."
        return elig

    # 11. No active continuation lease (best-effort non-blocking peek).
    lease = ContinuationLease(
        job_id=job_id, repo_key=_repo_key(job), intent_id=iid,
        lease_dir=_continue_dir(job_id, data_dir) / "leases",
    )
    if not lease.acquire(timeout_seconds=0.1):
        elig.blockers.append("lease_active")
        elig.next_safe_action = f"remedy change proof {job_id} --json"
        elig.safe_summary = "A continuation is already active for this job."
        return elig
    lease.release()

    # All gates pass.
    elig.eligible = True
    elig.safe_summary = f"Eligible: intent {iid} ready for one continuation cycle."
    elig.next_safe_action = f"remedy do --continue {job_id} --json"
    return elig
