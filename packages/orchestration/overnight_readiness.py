"""
Bounded Overnight Preparation v0 — read-only readiness / plan / morning report.

This module answers, WITHOUT running anything: is a job safe to run unattended,
what would Remedy do next, what are the limits, what would stop it, what evidence
exists/is missing, and what the morning checklist looks like.

It is preparation only. It NEVER applies code, runs tests, proposes/applies
repairs, calls a provider, mutates the repo, or starts a background worker. All
truth is derived from durable sources (DurableApplyRecord + Snapshot Truth +
Proof Chain + RunContract/Usage + RepairAttempt), never from event presence
alone. Unknown stays unknown.

Public API::

    build_overnight_readiness(job_id, data_dir=None, policy=None) -> OvernightReadinessReport
    build_overnight_plan(job_id, data_dir=None, policy=None) -> OvernightRunPlan
    build_overnight_report(job_id, data_dir=None, policy=None) -> dict
    export_readiness_json(report) -> dict
    render_overnight_report_markdown(report_dict) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID


# ---------------------------------------------------------------------------
# Vocabularies (Steps 1246/1250)
# ---------------------------------------------------------------------------


class OvernightEvidenceStatus:
    COMPLETE = "complete"
    PARTIAL = "partial"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"
    MISSING = "missing"


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
_CAP_UNKNOWN = "unknown"
_CAP_NOT_SUPPORTED = "not_supported"


# ---------------------------------------------------------------------------
# Bounded policy (Step 1247) — conservative defaults: planning/report ONLY.
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Result models (Step 1246)
# ---------------------------------------------------------------------------


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
class OvernightRunPlan:
    job_id: str
    generated_at: str = ""
    would_run: bool = False
    hypothetical_cycle: list[dict[str, str]] = field(default_factory=list)
    required_permissions: list[str] = field(default_factory=list)
    required_contract: list[str] = field(default_factory=list)
    stop_points: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    human_approvals_needed: list[str] = field(default_factory=list)
    policy_summary: dict[str, Any] = field(default_factory=dict)
    safe_summary: str = ""


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


# ---------------------------------------------------------------------------
# Readiness inputs (Step 1248) — durable truth only, never event-only proof.
# ---------------------------------------------------------------------------


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
    from packages.orchestration.storage import load_job, JobNotFoundError
    from packages.orchestration.approval_queue import list_patch_intents, APPROVAL_APPROVED, APPROVAL_PENDING
    from packages.orchestration.repository_snapshot import build_snapshot_truth, list_durable_apply_ids
    from packages.orchestration.run_contract import ensure_contract, load_usage
    from packages.orchestration.repair_loop import load_repair_attempts

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


# ---------------------------------------------------------------------------
# Budget summary (Step 1253)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Evidence summary (Step 1248)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Capability matrix (Step 1249)
# ---------------------------------------------------------------------------


def _build_capabilities(inp: _Inputs, job_id: str) -> list[OvernightCapability]:
    from packages.orchestration.permissions import is_allowed, Capability
    from packages.orchestration.run_contract import evaluate_run_action, ContractAction

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


# ---------------------------------------------------------------------------
# Risk summary (Step 1254)
# ---------------------------------------------------------------------------


def _build_risks(inp: _Inputs) -> list[OvernightRisk]:
    risks: list[OvernightRisk] = []
    if inp.unresolved_failures > 0:
        risks.append(OvernightRisk(
            id="unresolved_failures", severity="high",
            summary=f"{inp.unresolved_failures} unresolved test failure(s).",
            source="failure_artifacts"))
    if inp.pending_repair_intents:
        risks.append(OvernightRisk(
            id="repair_pending_approval", severity="medium",
            summary="Repair patch intent pending approval.", source="repair_attempts"))
    if inp.pending_intents:
        risks.append(OvernightRisk(
            id="intents_pending_approval", severity="medium",
            summary=f"{len(inp.pending_intents)} patch intent(s) pending approval.",
            source="approval_queue"))
    if inp.applied_records > 0 and inp.verified_snapshots < inp.applied_records:
        risks.append(OvernightRisk(
            id="apply_without_verified_snapshot", severity="high",
            summary="Applied record without a verified snapshot.", source="snapshot_truth"))
    if inp.proof_status in ("incomplete", "unverified", "unknown") and inp.applied_records > 0:
        risks.append(OvernightRisk(
            id="proof_incomplete", severity="medium",
            summary=f"Proof status is {inp.proof_status} after apply.", source="proof_chain"))
    # Integrity gate (lightweight, best-effort).
    integ = _integrity_status()
    if integ == "fail":
        risks.append(OvernightRisk(id="integrity_failed", severity="blocker",
                                   summary="Integrity gate failed.", source="integrity_gate"))
    elif integ == "unknown":
        risks.append(OvernightRisk(id="integrity_unknown", severity="low",
                                   summary="Integrity status unknown.", source="integrity_gate"))
    # Open blocker/high review findings (Step 1254 / R-0080). No per-job
    # programmatic findings source exists in v0 — report the dimension as an
    # explicit unknown rather than silently omitting it (truthful-unknown).
    risks.append(OvernightRisk(
        id="review_findings_unknown", severity="low",
        summary="Open review findings status is unknown (no per-job findings source in v0).",
        source="review"))
    return risks


def _integrity_status() -> str:
    """Lightweight integrity status: pass | fail | unknown. Never runs tests."""
    try:
        from packages.orchestration.integrity_gate import run_integrity_checks, IntegrityStatus
        result = run_integrity_checks(collect_only=True)
        status = getattr(result, "status", None)
        if status == IntegrityStatus.FAIL:
            return "fail"
        if status == IntegrityStatus.PASS:
            return "pass"
        return "unknown"
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return "unknown"


# ---------------------------------------------------------------------------
# Morning checklist (Step 1252) — every "done" needs durable evidence.
# ---------------------------------------------------------------------------


def _ci(id, label, status, **kw) -> OvernightChecklistItem:
    return OvernightChecklistItem(id=id, label=label, status=status, **kw)


def _build_checklist(inp: _Inputs, job_id: str) -> list[OvernightChecklistItem]:
    items: list[OvernightChecklistItem] = []
    items.append(_ci("job_initialized", "Job initialized", "done",
                     evidence_kind="job", evidence_id=job_id))
    items.append(_ci("task_selected", "Task selected",
                     "done" if inp.job.tasks else "pending", evidence_kind="task",
                     evidence_id=str(inp.job.tasks[0].id) if inp.job.tasks else ""))
    items.append(_ci("patch_intent_created", "Patch intent created",
                     "done" if inp.intents else "pending", evidence_kind="intent",
                     evidence_id=inp.intents[0]["intent_id"] if inp.intents else ""))
    items.append(_ci("intent_approved", "Intent approved",
                     "done" if inp.approved_intents else ("pending" if inp.intents else "skipped"),
                     evidence_kind="intent",
                     evidence_id=inp.approved_intents[0]["intent_id"] if inp.approved_intents else "",
                     next_action=(f"remedy patch approve {job_id} {inp.pending_intents[0]['intent_id']}"
                                  if inp.pending_intents else "")))
    items.append(_ci("snapshot_verified", "Snapshot verified",
                     "done" if inp.verified_snapshots > 0 else ("pending" if inp.applied_records else "skipped"),
                     evidence_kind="snapshot_truth"))
    items.append(_ci("apply_completed", "Apply completed",
                     "done" if inp.applied_records > 0 else "pending", evidence_kind="apply_record"))
    items.append(_ci("test_run_completed", "Test run completed",
                     "done" if (inp.usage.test_runs_used > 0) else "pending", evidence_kind="run_usage"))
    items.append(_ci("proof_verified", "Proof verified",
                     "done" if inp.proof_status == "verified" else (
                         "blocked" if inp.proof_status in ("failed",) else
                         "pending" if inp.applied_records else "skipped"),
                     evidence_kind="proof_chain", reason=f"proof={inp.proof_status}"))
    items.append(_ci("failure_artifact_created", "Failure artifact created",
                     "done" if inp.failure_artifacts else "skipped", evidence_kind="failure_artifact"))
    proposed = [a for a in inp.repair_attempts if a.repair_intent_id]
    items.append(_ci("repair_proposed", "Repair proposed",
                     "done" if proposed else ("pending" if inp.failure_artifacts else "skipped"),
                     evidence_kind="repair_attempt"))
    repair_approved = [a for a in inp.repair_attempts
                       if a.status in ("approved", "applied", "tested_passed", "tested_failed")]
    items.append(_ci("repair_approved", "Repair approved",
                     "done" if repair_approved else ("pending" if proposed else "skipped"),
                     evidence_kind="repair_attempt"))
    repair_applied = [a for a in inp.repair_attempts
                      if a.status in ("applied", "tested_passed", "tested_failed")]
    items.append(_ci("repair_applied", "Repair applied",
                     "done" if repair_applied else ("pending" if repair_approved else "skipped"),
                     evidence_kind="repair_attempt"))
    resolved = [a for a in inp.repair_attempts if a.resolved_failure]
    items.append(_ci("failure_resolved", "Failure resolved",
                     "done" if resolved else ("pending" if inp.unresolved_failures else "skipped"),
                     evidence_kind="failure_artifact"))
    human_needed = bool(inp.pending_intents or inp.pending_repair_intents)
    items.append(_ci("human_decision_needed", "Human decision needed",
                     "pending" if human_needed else "skipped",
                     reason="Approvals pending." if human_needed else "",
                     next_action=(f"remedy patch approve {job_id} {inp.pending_intents[0]['intent_id']}"
                                  if inp.pending_intents else "")))
    return items


# ---------------------------------------------------------------------------
# Next safe action selector (Step 1251) — deterministic, catalog-backed.
# ---------------------------------------------------------------------------


def select_overnight_next_action(inp: _Inputs | None, job_id: str) -> OvernightNextAction:
    """One best next action. Never fake; only when the entity exists."""
    if inp is None:
        return OvernightNextAction("Review jobs", "remedy job list --json",
                                   "Job not found.", requires_human=True)
    # Pending repair intent → approve it.
    if inp.pending_repair_intents:
        iid = inp.pending_repair_intents[0].repair_intent_id
        return OvernightNextAction("Approve repair patch", f"remedy patch approve {job_id} {iid}",
                                   "A repair patch intent is pending approval.", requires_human=True)
    # Pending normal intent → approve it.
    if inp.pending_intents:
        iid = inp.pending_intents[0]["intent_id"]
        return OvernightNextAction("Approve patch", f"remedy patch approve {job_id} {iid}",
                                   "A patch intent is pending approval.", requires_human=True)
    # Approved intent + plausible apply gates → continue one cycle.
    if inp.approved_intents and not inp.contract.stop_before_apply:
        return OvernightNextAction("Continue one cycle", f"remedy do continue {job_id} --json",
                                   "An approved intent is ready for one continuation cycle.",
                                   requires_human=True)
    # Unresolved failure with no repair attempt yet → propose repair.
    if inp.failure_artifacts and inp.unresolved_failures > 0 and not any(
            a.repair_intent_id for a in inp.repair_attempts):
        fa = str(inp.failure_artifacts[0].id)
        return OvernightNextAction("Propose repair", f"remedy repair propose {job_id} {fa} --json",
                                   "An unresolved failure has no repair proposal yet.",
                                   requires_human=True)
    # Uncertain → human review.
    return OvernightNextAction("Review job state", f"remedy job show {job_id} --json",
                               "No safe automatic action; human review required.", requires_human=True)


# ---------------------------------------------------------------------------
# Stop reasons that WOULD apply right now (Step 1250)
# ---------------------------------------------------------------------------


def _build_stop_reasons(inp: _Inputs, budget: dict[str, Any], risks: list[OvernightRisk]) -> list[str]:
    out: list[str] = []
    if inp.pending_intents or inp.pending_repair_intents:
        out.append(OvernightStopReason.HUMAN_APPROVAL_REQUIRED)
    if inp.contract.stop_before_apply:
        out.append(OvernightStopReason.CONTRACT_BLOCKED)
    if budget.get("loops_exhausted") or budget.get("test_runs_exhausted"):
        out.append(OvernightStopReason.BUDGET_EXHAUSTED)
    if inp.unresolved_failures > 0:
        out.append(OvernightStopReason.TEST_FAILED)
    if inp.pending_repair_intents:
        out.append(OvernightStopReason.REPAIR_PENDING_APPROVAL)
    if any(r.severity in ("blocker", "high") for r in risks):
        out.append(OvernightStopReason.MEDIUM_OR_HIGH_RISK)
    if any(r.id == "integrity_failed" for r in risks):
        out.append(OvernightStopReason.INTEGRITY_FAILED)
    out.append(OvernightStopReason.PROVIDER_UNAVAILABLE)  # provider deferred this block
    if not out:
        out.append(OvernightStopReason.NO_SAFE_ACTION)
    return out


# ---------------------------------------------------------------------------
# Top-level builders
# ---------------------------------------------------------------------------


def build_overnight_readiness(
    job_id: str,
    data_dir: "Path | None" = None,
    policy: BoundedOvernightPolicy | None = None,
) -> OvernightReadinessReport:
    """Read-only readiness assessment. Never executes anything."""
    from packages.orchestration.data_paths import resolve_data_root

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    policy = policy or default_overnight_policy()
    report = OvernightReadinessReport(job_id=job_id, generated_at=_now())
    report.policy_summary = _policy_summary(policy)

    inp = _gather_inputs(job_id, ddir)
    if inp is None:
        report.blockers.append("job_not_found")
        report.stop_reasons = [OvernightStopReason.UNSUPPORTED_STATE]
        report.next_action = select_overnight_next_action(None, job_id)
        report.safe_summary = "Job not found."
        return report

    report.budget_summary = _build_budget_summary(inp)
    report.evidence_summary = _build_evidence_summary(inp)
    report.capabilities = _build_capabilities(inp, job_id)
    report.risks = _build_risks(inp)
    # Exhausted budgets block readiness (Step 1253 / R-0079): an exhausted
    # loop/test budget is a blocker, surfaced as a blocker-severity risk too.
    _budget_exhausted = bool(report.budget_summary.get("loops_exhausted")
                             or report.budget_summary.get("test_runs_exhausted"))
    if _budget_exhausted:
        report.risks.append(OvernightRisk(
            id="budget_exhausted", severity="blocker",
            summary="A run-contract budget (loops/test runs) is exhausted.",
            source="run_contract+run_usage"))
    report.checklist = _build_checklist(inp, job_id)
    report.next_action = select_overnight_next_action(inp, job_id)
    report.stop_reasons = _build_stop_reasons(inp, report.budget_summary, report.risks)

    # Blockers: hard reasons a future unattended run could not proceed.
    if not inp.job.tasks:
        report.blockers.append("no_tasks")
    if inp.unresolved_failures > 0:
        report.blockers.append("unresolved_failures")
    if inp.pending_repair_intents:
        report.blockers.append("repair_pending_approval")
    if _budget_exhausted:
        report.blockers.append("budget_exhausted")
    if any(r.severity == "blocker" for r in report.risks):
        report.blockers.append("blocker_risk")

    # Report-readiness: the job is coherent enough to assess (always, if it loads
    # with tasks). Unattended-readiness additionally requires the policy to permit
    # execution AND no blockers — under the default policy this is ALWAYS False.
    report.ready = bool(inp.job.tasks) and "no_tasks" not in report.blockers
    report.can_run_unattended = (
        report.ready and not report.blockers and policy.execution_enabled
    )
    if report.can_run_unattended:
        report.readiness_level = "execution_candidate"
        report.recommended_mode = "bounded_execution"
    elif report.ready and not report.blockers:
        report.readiness_level = "plan_only"
        report.recommended_mode = "plan_only"
    elif report.ready:
        report.readiness_level = "report_only"
        report.recommended_mode = "report_only"
    else:
        report.readiness_level = "not_ready"
        report.recommended_mode = "report_only"

    nb = len(report.blockers)
    report.safe_summary = (
        f"Readiness: {report.readiness_level}; unattended={report.can_run_unattended}; "
        f"{nb} blocker(s), {len(report.risks)} risk(s)."
    )
    return report


def _policy_summary(p: BoundedOvernightPolicy) -> dict[str, Any]:
    return {
        "max_cycles": p.max_cycles, "max_test_runs": p.max_test_runs,
        "max_repair_attempts": p.max_repair_attempts, "max_apply_count": p.max_apply_count,
        "allow_apply": p.allow_apply, "allow_repair_propose": p.allow_repair_propose,
        "allow_repair_apply": p.allow_repair_apply, "allow_provider": p.allow_provider,
        "allow_revert": p.allow_revert, "require_verified_snapshot": p.require_verified_snapshot,
        "require_linked_tests": p.require_linked_tests, "require_clean_review": p.require_clean_review,
        "require_human_approval_for_new_intents": p.require_human_approval_for_new_intents,
        "execution_enabled": p.execution_enabled,
    }


def build_overnight_plan(
    job_id: str,
    data_dir: "Path | None" = None,
    policy: BoundedOvernightPolicy | None = None,
) -> OvernightRunPlan:
    """Dry-run plan: what Remedy WOULD do (≤1 hypothetical cycle). No execution."""
    from packages.orchestration.data_paths import resolve_data_root

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    policy = policy or default_overnight_policy()
    plan = OvernightRunPlan(job_id=job_id, generated_at=_now(), policy_summary=_policy_summary(policy))

    inp = _gather_inputs(job_id, ddir)
    if inp is None:
        plan.safe_summary = "Job not found — nothing to plan."
        plan.stop_points = [OvernightStopReason.UNSUPPORTED_STATE]
        return plan

    plan.would_run = policy.execution_enabled and bool(inp.approved_intents)
    if inp.approved_intents and not inp.contract.stop_before_apply:
        plan.hypothetical_cycle = [
            {"phase": "eligibility", "detail": "Verify approved intent + gates."},
            {"phase": "snapshot", "detail": "Create + verify a durable snapshot (mandatory)."},
            {"phase": "apply", "detail": "Apply the approved intent via the central service."},
            {"phase": "test", "detail": "Run the linked test via the Test Execution Service."},
            {"phase": "proof", "detail": "Rebuild proof from authoritative snapshot truth."},
            {"phase": "stop", "detail": "Stop truthfully; no second cycle."},
        ]
    plan.required_permissions = ["repo_generated_write", "repo_test_run"]
    plan.required_contract = ["patch_apply allowed", "stop_before_apply=false", "max_test_runs>0"]
    if inp.contract.stop_before_apply:
        plan.stop_points.append(OvernightStopReason.CONTRACT_BLOCKED)
    if inp.pending_intents or inp.pending_repair_intents:
        plan.stop_points.append(OvernightStopReason.HUMAN_APPROVAL_REQUIRED)
        plan.human_approvals_needed = [i["intent_id"] for i in inp.pending_intents] + [
            a.repair_intent_id for a in inp.pending_repair_intents]
    if not policy.execution_enabled:
        plan.stop_points.append(OvernightStopReason.UNSUPPORTED_STATE)
    if not inp.approved_intents:
        plan.missing_evidence.append("approved_intent")
    if inp.verified_snapshots == 0 and inp.applied_records == 0:
        plan.missing_evidence.append("verified_snapshot")
    plan.safe_summary = (
        f"Plan: would_run={plan.would_run} (default policy is report-only); "
        f"{len(plan.stop_points)} stop point(s), {len(plan.missing_evidence)} missing evidence."
    )
    return plan


def build_overnight_report(
    job_id: str,
    data_dir: "Path | None" = None,
    policy: BoundedOvernightPolicy | None = None,
) -> dict[str, Any]:
    """Morning-style report built from current job evidence (read-only)."""
    report = build_overnight_readiness(job_id, data_dir, policy)
    data = export_readiness_json(report)
    done = [c for c in report.checklist if c.status == "done"]
    blocked = [c for c in report.checklist if c.status in ("blocked", "pending", "risk")]
    data["report"] = {
        "completed_checklist": [c.id for c in done],
        "blocked_checklist": [c.id for c in blocked],
        "completed_count": len(done),
        "blocked_count": len(blocked),
    }
    return data


# ---------------------------------------------------------------------------
# Export / render (no raw content)
# ---------------------------------------------------------------------------


def export_readiness_json(report: OvernightReadinessReport) -> dict[str, Any]:
    return {
        "version": 1,
        "job_id": report.job_id,
        "generated_at": report.generated_at,
        "readiness_level": report.readiness_level,
        "ready": report.ready,
        "can_run_unattended": report.can_run_unattended,
        "recommended_mode": report.recommended_mode,
        "blockers": report.blockers,
        "stop_reasons": report.stop_reasons,
        "risks": [{"id": r.id, "severity": r.severity, "summary": r.summary, "source": r.source}
                  for r in report.risks],
        "capabilities": [
            {"name": c.name, "status": c.status, "reason": c.reason,
             "required_permission": c.required_permission,
             "required_contract_action": c.required_contract_action,
             "evidence_ids": c.evidence_ids, "next_safe_action": c.next_safe_action}
            for c in report.capabilities
        ],
        "checklist": [
            {"id": i.id, "label": i.label, "status": i.status,
             "evidence_kind": i.evidence_kind, "evidence_id": i.evidence_id,
             "reason": i.reason, "next_action": i.next_action}
            for i in report.checklist
        ],
        "next_action": (
            {"label": report.next_action.label, "command": report.next_action.command,
             "reason": report.next_action.reason, "requires_human": report.next_action.requires_human}
            if report.next_action else None
        ),
        "budget_summary": report.budget_summary,
        "evidence_summary": report.evidence_summary,
        "policy_summary": report.policy_summary,
        "safe_summary": report.safe_summary,
    }


def export_plan_json(plan: OvernightRunPlan) -> dict[str, Any]:
    return {
        "version": 1, "job_id": plan.job_id, "generated_at": plan.generated_at,
        "would_run": plan.would_run, "hypothetical_cycle": plan.hypothetical_cycle,
        "required_permissions": plan.required_permissions,
        "required_contract": plan.required_contract, "stop_points": plan.stop_points,
        "missing_evidence": plan.missing_evidence,
        "human_approvals_needed": plan.human_approvals_needed,
        "policy_summary": plan.policy_summary, "safe_summary": plan.safe_summary,
    }


_CHECK_ICON = {"done": "[x]", "pending": "[ ]", "blocked": "[!]", "risk": "[~]",
               "skipped": "[-]", "unknown": "[?]"}


def render_overnight_report_markdown(data: dict[str, Any]) -> str:
    """Render a morning report as safe markdown. No raw content."""
    lines: list[str] = []
    lines.append(f"# Overnight Report — job {str(data.get('job_id',''))[:8]}")
    lines.append("")
    lines.append(f"- Readiness: **{data.get('readiness_level')}**")
    lines.append(f"- Can run unattended: **{data.get('can_run_unattended')}**")
    lines.append(f"- Recommended mode: {data.get('recommended_mode')}")
    lines.append("")
    lines.append("## Summary")
    lines.append(data.get("safe_summary", ""))
    lines.append("")
    lines.append("## Completed checklist")
    for c in data.get("checklist", []):
        if c["status"] == "done":
            lines.append(f"- {_CHECK_ICON['done']} {c['label']}")
    lines.append("")
    lines.append("## Blocked / pending checklist")
    for c in data.get("checklist", []):
        if c["status"] in ("blocked", "pending", "risk"):
            icon = _CHECK_ICON.get(c["status"], "[ ]")
            lines.append(f"- {icon} {c['label']}" + (f" — {c['reason']}" if c.get("reason") else ""))
    lines.append("")
    lines.append("## Risks")
    for r in data.get("risks", []):
        lines.append(f"- ({r['severity']}) {r['summary']}")
    lines.append("")
    bs = data.get("budget_summary", {})
    lines.append("## Budgets")
    lines.append(f"- Loops: {bs.get('loops_used')}/{bs.get('max_loops')} "
                 f"(remaining {bs.get('remaining_loops')})")
    lines.append(f"- Test runs: {bs.get('test_runs_used')}/{bs.get('max_test_runs')} "
                 f"(remaining {bs.get('remaining_test_runs')})")
    lines.append(f"- Tokens used: {bs.get('tokens_used')}")
    lines.append("")
    lines.append("## Stop reasons")
    for s in data.get("stop_reasons", []):
        lines.append(f"- {s}")
    lines.append("")
    na = data.get("next_action")
    lines.append("## Next safe action")
    if na:
        lines.append(f"- {na['label']}: `{na['command']}`")
        lines.append(f"  - {na['reason']}")
    return "\n".join(lines)
