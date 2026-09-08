"""
Mission readiness — the read-only readiness view carried out of the prototype cluster.

This module is the destination DECISION F275 D1 ruled for the first of the two
carry-overs F260's Design section orders before the prototype cluster is deleted.
Each definition below is a BYTE-IDENTICAL move of the definition of the same name
in `packages/orchestration/overnight_readiness.py`, so the move is provable by a
gate rather than reviewable by eye, and nothing is renamed: the carried symbols
keep their `overnight_` spelling because F261 owns renames.

STAGED BATCH 1 OF 2, AND UNWIRED. The full carry-over is 655 lines, which exceeds
the DECISION F104 D1 cap of 500 insertions for one commit, so it lands across two
commits in different rounds. Until the wiring round NOTHING IMPORTS THIS MODULE —
that is deliberate, it is what keeps every intermediate commit green, and it is
gated. `overnight_readiness.py` itself is not touched by either batch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID


class OvernightStopReason:
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    CONTRACT_BLOCKED = "contract_blocked"
    PERMISSION_MISSING = "permission_missing"
    BUDGET_EXHAUSTED = "budget_exhausted"
    NO_SAFE_ACTION = "no_safe_action"
    UNKNOWN_RISK = "unknown_risk"
    MEDIUM_OR_HIGH_RISK = "medium_or_high_risk"
    SNAPSHOT_MISSING = "snapshot_missing"
    SNAPSHOT_UNVERIFIED = "snapshot_unverified"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"
    TEST_FAILED = "test_failed"
    REPAIR_AVAILABLE = "repair_available"
    REPAIR_PENDING_APPROVAL = "repair_pending_approval"
    REPAIR_UNAVAILABLE = "repair_unavailable"
    REVIEW_FINDINGS_OPEN = "review_findings_open"
    INTEGRITY_FAILED = "integrity_failed"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    UNSUPPORTED_STATE = "unsupported_state"
    COMPLETED_VERIFIED = "completed_verified"


_CAP_AVAILABLE = "available"


_CAP_BLOCKED = "blocked"


_CAP_NOT_SUPPORTED = "not_supported"


@dataclass(frozen=True)
class BoundedOvernightPolicy:
    """Conservative bounds for a FUTURE bounded overnight run.

    Defaults are planning/report-only: no apply, no repair apply, no provider, no
    revert, zero cycles. This block must never silently enable execution.
    """

    max_cycles: int = 0
    max_runtime_seconds: int = 0
    max_test_runs: int = 0
    max_repair_attempts: int = 0
    max_apply_count: int = 0
    allow_apply: bool = False
    allow_repair_propose: bool = False
    allow_repair_apply: bool = False
    allow_provider: bool = False
    allow_revert: bool = False
    stop_on_unknown_risk: bool = True
    stop_on_medium_risk: bool = True
    require_verified_snapshot: bool = True
    require_linked_tests: bool = True
    require_clean_review: bool = True
    require_human_approval_for_new_intents: bool = True

    @property
    def execution_enabled(self) -> bool:
        """True only if the policy actually permits any unattended execution."""
        return self.max_cycles > 0 and (
            self.allow_apply or self.allow_repair_apply
        )


def default_overnight_policy() -> BoundedOvernightPolicy:
    """The safe default: planning/report only."""
    return BoundedOvernightPolicy()


@dataclass
class OvernightCapability:
    name: str
    status: str                      # available | blocked | unknown | not_supported
    reason: str = ""
    required_permission: str = ""
    required_contract_action: str = ""
    evidence_ids: list[str] = field(default_factory=list)
    next_safe_action: str = ""


@dataclass
class OvernightChecklistItem:
    id: str
    label: str
    status: str                      # done | pending | blocked | risk | skipped | unknown
    evidence_kind: str = ""
    evidence_id: str = ""
    reason: str = ""
    next_action: str = ""


@dataclass
class OvernightRisk:
    id: str
    severity: str                    # blocker | high | medium | low
    summary: str
    source: str = ""


@dataclass
class OvernightNextAction:
    label: str
    command: str
    reason: str
    requires_human: bool = True


@dataclass
class OvernightReadinessReport:
    job_id: str
    generated_at: str = ""
    readiness_level: str = "not_ready"   # not_ready | report_only | plan_only | execution_candidate
    ready: bool = False
    can_run_unattended: bool = False
    blockers: list[str] = field(default_factory=list)
    risks: list[OvernightRisk] = field(default_factory=list)
    capabilities: list[OvernightCapability] = field(default_factory=list)
    checklist: list[OvernightChecklistItem] = field(default_factory=list)
    next_action: OvernightNextAction | None = None
    stop_reasons: list[str] = field(default_factory=list)
    budget_summary: dict[str, Any] = field(default_factory=dict)
    evidence_summary: dict[str, Any] = field(default_factory=dict)
    recommended_mode: str = "report_only"
    policy_summary: dict[str, Any] = field(default_factory=dict)
    safe_summary: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class _Inputs:
    job: Any
    data_dir: Path
    intents: list[dict[str, Any]]
    approved_intents: list[dict[str, Any]]
    pending_intents: list[dict[str, Any]]
    apply_ids: list[str]
    verified_snapshots: int
    applied_records: int
    tested_passed: int
    failure_artifacts: list[Any]
    unresolved_failures: int
    repair_attempts: list[Any]
    pending_repair_intents: list[Any]
    proof_status: str
    contract: Any
    usage: Any


def _gather_inputs(job_id: str, data_dir: Path) -> _Inputs | None:
    from packages.orchestration.approval_queue import APPROVAL_APPROVED, APPROVAL_PENDING, list_patch_intents
    from packages.orchestration.repair_loop import load_repair_attempts
    from packages.orchestration.repository_snapshot import build_snapshot_truth, list_durable_apply_ids
    from packages.orchestration.run_contract import ensure_contract, load_usage
    from packages.orchestration.storage import JobNotFoundError, load_job

    try:
        job = load_job(UUID(job_id), data_dir)
    except (ValueError, JobNotFoundError):
        return None

    intents = list_patch_intents(job)
    approved = [i for i in intents if i.get("state") == APPROVAL_APPROVED]
    pending = [i for i in intents if i.get("state") == APPROVAL_PENDING]

    apply_ids = list_durable_apply_ids(job_id, data_dir)
    verified = applied = tested_passed = 0
    # "applied" durable states persist after the post-apply test runs.
    _APPLIED_STATES = ("applied", "test_pending", "tested_passed", "tested_failed")
    for aid in apply_ids:
        truth = build_snapshot_truth(job_id, apply_id=aid, data_dir=data_dir)
        if truth.apply_state in _APPLIED_STATES:
            applied += 1
        if (truth.apply_state in _APPLIED_STATES and truth.snapshot_verified_now
                and truth.recovery_material_available and truth.evidence_status == "complete"):
            verified += 1

    failure_arts = [a for a in job.artifacts if (a.metadata or {}).get("test_failure")]
    unresolved = sum(1 for a in failure_arts if not (a.metadata or {}).get("failure_resolved"))

    attempts = list(load_repair_attempts(job).values())
    pending_repair = [a for a in attempts if a.status == "approval_required" and a.repair_intent_id]
    tested_passed = sum(1 for a in attempts if a.status == "tested_passed")

    # Proof chain — authoritative (durable snapshot truth), best-effort.
    proof_status = "unknown"
    try:
        from packages.orchestration.proof_chain import build_proof_chain
        from packages.orchestration.timeline import load_run_events
        events = load_run_events(data_dir, UUID(job_id))
        chain = build_proof_chain(job, events, data_dir=data_dir)
        proof_status = chain.overall_status if chain.changes else "none"
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        proof_status = "unknown"

    contract = ensure_contract(job)
    usage = load_usage(job)

    return _Inputs(
        job=job, data_dir=data_dir, intents=intents, approved_intents=approved,
        pending_intents=pending, apply_ids=apply_ids, verified_snapshots=verified,
        applied_records=applied, tested_passed=tested_passed,
        failure_artifacts=failure_arts, unresolved_failures=unresolved,
        repair_attempts=attempts, pending_repair_intents=pending_repair,
        proof_status=proof_status, contract=contract, usage=usage,
    )


def _build_budget_summary(inp: _Inputs) -> dict[str, Any]:
    c, u = inp.contract, inp.usage
    remaining_loops = max(0, c.max_loops - u.loops_used)
    remaining_tests = max(0, c.max_test_runs - u.test_runs_used)
    remaining_runtime = max(0, c.max_runtime_seconds - int(u.runtime_seconds_used))
    return {
        "max_loops": c.max_loops, "loops_used": u.loops_used,
        "remaining_loops": remaining_loops, "loops_exhausted": remaining_loops <= 0,
        "max_test_runs": c.max_test_runs, "test_runs_used": u.test_runs_used,
        "remaining_test_runs": remaining_tests, "test_runs_exhausted": remaining_tests <= 0,
        "max_runtime_seconds": c.max_runtime_seconds,
        "remaining_runtime_seconds": remaining_runtime,
        # Token/cost usage is not measured here — report limits + unknown, never invent.
        "max_tokens": c.max_tokens, "tokens_used": "unknown",
        "max_cost_cents": c.max_cost_cents, "cost_cents_used": "unknown",
        "source": "run_contract+run_usage",
    }


def _build_evidence_summary(inp: _Inputs) -> dict[str, Any]:
    return {
        "intents": len(inp.intents),
        "approved_intents": len(inp.approved_intents),
        "pending_intents": len(inp.pending_intents),
        "apply_records": len(inp.apply_ids),
        "applied": inp.applied_records,
        "verified_snapshots": inp.verified_snapshots,
        "failure_artifacts": len(inp.failure_artifacts),
        "unresolved_failures": inp.unresolved_failures,
        "repair_attempts": len(inp.repair_attempts),
        "pending_repair_intents": len(inp.pending_repair_intents),
        "proof_status": inp.proof_status,
        "source": "durable_records+snapshot_truth+proof_chain",
    }


def _build_capabilities(inp: _Inputs, job_id: str) -> list[OvernightCapability]:
    from packages.orchestration.permissions import Capability, is_allowed
    from packages.orchestration.run_contract import ContractAction, evaluate_run_action

    job, c = inp.job, inp.contract

    def perm(cap) -> bool:
        try:
            return is_allowed(job, cap)
        except (ValueError, KeyError, TypeError, AttributeError):
            return False

    def action_allowed(act) -> bool:
        try:
            return evaluate_run_action(c, act).allowed
        except (ValueError, KeyError, TypeError, AttributeError):
            return False

    caps: list[OvernightCapability] = []

    caps.append(OvernightCapability(
        name="can_plan", status=_CAP_AVAILABLE, reason="Read-only planning is always available."))

    caps.append(OvernightCapability(
        name="can_build_fixture", status=_CAP_AVAILABLE,
        reason="Deterministic fixture repair builder available (docs-only by default)."))

    caps.append(OvernightCapability(
        name="can_create_patch_intent",
        status=_CAP_AVAILABLE if action_allowed(ContractAction.CREATE_PATCH_INTENT) else _CAP_BLOCKED,
        reason="" if action_allowed(ContractAction.CREATE_PATCH_INTENT) else "Contract denies create_patch_intent.",
        required_contract_action=ContractAction.CREATE_PATCH_INTENT))

    apply_ok = (perm(Capability.repo_generated_write) and not c.stop_before_apply
                and action_allowed(ContractAction.PATCH_APPLY))
    caps.append(OvernightCapability(
        name="can_apply_approved_intent",
        status=_CAP_AVAILABLE if (apply_ok and inp.approved_intents) else _CAP_BLOCKED,
        reason=("" if apply_ok else "Needs repo_generated_write, stop_before_apply=false, contract patch_apply.")
               or ("No approved intent." if not inp.approved_intents else ""),
        required_permission="repo_generated_write",
        required_contract_action=ContractAction.PATCH_APPLY,
        next_safe_action=(f"remedy do continue {job_id} --json" if apply_ok and inp.approved_intents else "")))

    test_ok = perm(Capability.repo_test_run) and c.max_test_runs > 0
    caps.append(OvernightCapability(
        name="can_run_tests",
        status=_CAP_AVAILABLE if test_ok else _CAP_BLOCKED,
        reason="" if test_ok else "Needs repo_test_run and max_test_runs>0.",
        required_permission="repo_test_run", required_contract_action=ContractAction.RUN_TEST))

    caps.append(OvernightCapability(
        name="can_create_failure_artifact",
        status=_CAP_AVAILABLE if test_ok else _CAP_BLOCKED,
        reason="" if test_ok else "Failure artifacts come from real test runs."))

    repair_ok = action_allowed(ContractAction.CREATE_FIX_TASK)
    caps.append(OvernightCapability(
        name="can_propose_repair",
        status=_CAP_AVAILABLE if (repair_ok and inp.failure_artifacts) else _CAP_BLOCKED,
        reason="" if inp.failure_artifacts else "No failure artifact to repair.",
        required_contract_action=ContractAction.CREATE_FIX_TASK,
        next_safe_action=(f"remedy repair propose {job_id} {str(inp.failure_artifacts[0].id)} --json"
                          if repair_ok and inp.failure_artifacts else "")))

    caps.append(OvernightCapability(
        name="can_apply_approved_repair",
        status=_CAP_AVAILABLE if (apply_ok and inp.pending_repair_intents == [] and any(
            a.status == "approval_required" for a in inp.repair_attempts) is False and inp.approved_intents) else _CAP_BLOCKED,
        reason="Approved repair intent flows through do continue once approved.",
        required_contract_action=ContractAction.PATCH_APPLY))

    revert_ok = perm(Capability.repo_revert) and action_allowed(ContractAction.REVERT)
    caps.append(OvernightCapability(
        name="can_revert_explicitly",
        status=_CAP_AVAILABLE if revert_ok else _CAP_BLOCKED,
        reason="" if revert_ok else "Revert denied by default (needs repo_revert + contract revert).",
        required_permission="repo_revert", required_contract_action=ContractAction.REVERT))

    cont_ok = bool(inp.approved_intents) and apply_ok and test_ok
    caps.append(OvernightCapability(
        name="can_continue_one_cycle",
        status=_CAP_AVAILABLE if cont_ok else _CAP_BLOCKED,
        reason="" if cont_ok else "Needs an approved intent + apply + test gates.",
        next_safe_action=(f"remedy do continue {job_id} --json" if cont_ok else "")))

    caps.append(OvernightCapability(
        name="can_commit", status=_CAP_NOT_SUPPORTED,
        reason="Git commit gate is not enabled in this block."))
    caps.append(OvernightCapability(
        name="can_provider_build", status=_CAP_NOT_SUPPORTED,
        reason="Provider/Ollama execution is deferred (no_cloud)."))
    caps.append(OvernightCapability(
        name="can_run_overnight", status=_CAP_BLOCKED,
        reason="Bounded overnight executor not enabled; default policy is report-only."))

    return caps
