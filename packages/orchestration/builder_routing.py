"""
Expensive Builder Routing v0 (Steps 1573-1608).

A LOCAL-FIRST, budgeted, anti-loop ROUTING / POLICY layer that decides *when* Remedy should
use deterministic logic, local advisory, local candidate generation, or expensive external
candidate generation. This module is **routing / policy / planning ONLY** — it never executes
a builder/model/provider, never calls the network, never generates candidates, and never
creates Patch Intents or ProposedTasks. It reads safe durable summaries and emits ONE routing
decision + a safe trace.

Core principle:
  LLMs advise or build candidates. The orchestrator controls. Evidence is truth. Local first
  when useful. Expensive builders only when targeted, budgeted, and bounded. No loops.

Hard rules enforced here:
  - NO provider/model/builder execution, NO candidate generation, NO network, NO subprocess,
    NO provider SDK, NO apply/approval/test/PR/git, NO Patch Intent / ProposedTask creation.
  - An external candidate generator is NEVER recommended without ALL of: request package ready,
    Trust Gate available, Verification available, budget allowed, loop risk not high, and no
    pending approval/intent. Unknown external cost stays unknown and BLOCKS external by default.
  - No repeated expensive route without NEW evidence (loop governor).
  - No raw prompt/response/source/diff/log/secrets/tracebacks/absolute paths in any surface.
  - Every emitted next_safe_action is catalog-backed and entity-backed.

Public API::

    default_builder_routing_policy() -> BuilderRoutingPolicy
    select_builder_routing_decision(request, policy=None, data_dir=None, persist=True)
        -> BuilderRoutingDecision
    export_builder_routing_json(decision) -> dict
    load_builder_routing_traces(scope=None, data_dir=None) -> list[dict]
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.provider_trust import _scrub_public


# ---------------------------------------------------------------------------
# Vocabularies (Steps 1574 / 1579 / 1581)
# ---------------------------------------------------------------------------


class BuilderRoutingTier:
    DETERMINISTIC_ONLY = "deterministic_only"
    LOCAL_ADVISOR = "local_advisor"
    LOCAL_CANDIDATE_GENERATOR = "local_candidate_generator"
    EXTERNAL_CANDIDATE_GENERATOR = "external_candidate_generator"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    NO_SAFE_ROUTE = "no_safe_route"


class BuilderRoutingStopReason:
    OK = "ok"
    PENDING_APPROVAL = "pending_approval_exists"
    PENDING_INTENT = "pending_intent_exists"
    REVIEW_BLOCKER = "review_blocker_open"
    BUDGET_EXHAUSTED = "budget_exhausted"
    LOOP_BLOCK = "loop_guard_block"
    MISSING_REQUEST_PACKAGE = "missing_request_package"
    NO_TRUST_VERIFICATION = "trust_or_verification_unavailable"
    UNKNOWN_EVIDENCE = "unknown_evidence"
    NO_NEED = "no_candidate_generation_need"
    JOB_NOT_FOUND = "job_not_found"
    CONTRACT_DENIED = "contract_denied"


class BuilderRoutingJustification:
    NO_DETERMINISTIC_FIX_AVAILABLE = "no_deterministic_fix_available"
    LOCAL_ADVISOR_INSUFFICIENT = "local_advisor_insufficient"
    REPEATED_LOCAL_FAILURE = "repeated_local_failure"
    HIGH_VALUE_FAILURE = "high_value_failure"
    REQUEST_PACKAGE_READY = "request_package_ready"
    TRUST_AND_VERIFICATION_AVAILABLE = "trust_and_verification_available"
    BUDGET_AVAILABLE = "budget_available"
    USER_EXPLICITLY_REQUESTED = "user_explicitly_requested"
    LOOP_RISK_LOW = "loop_risk_low"
    HUMAN_APPROVAL_REQUIRED_AFTER_GENERATION = "human_approval_required_after_generation"


class LoopGovernorStatus:
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"
    HUMAN_REVIEW_REQUIRED = "human_review_required"


# Constant external preconditions — an external builder route requires ALL of these.
_EXTERNAL_REQUIRED_JUSTIFICATIONS = (
    BuilderRoutingJustification.REQUEST_PACKAGE_READY,
    BuilderRoutingJustification.TRUST_AND_VERIFICATION_AVAILABLE,
    BuilderRoutingJustification.BUDGET_AVAILABLE,
    BuilderRoutingJustification.LOOP_RISK_LOW,
)

# Worker Registry route-policy bridge (Step 1723). Maps a routing tier to the registry worker it
# would use, so a user RoutePolicy that blocks/disables that worker (or caps cost/risk) can
# escalate the route to human review. READ-ONLY: this never executes a worker and is a no-op under
# the default policy (which blocks nothing and selects nothing).
_TIER_TO_WORKER_ID: dict[str, str] = {
    BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR: "local.candidate_generator",
    BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR: "external.builder_package",
}


def _route_policy_blocks_tier(job_id: str, tier: str, data_dir: Path) -> tuple[bool, str]:
    """Return (blocked, reason) if a persisted user RoutePolicy would block the worker this tier
    maps to. No-op (False) when no constraining policy exists. READ-ONLY; never executes."""
    worker_id = _TIER_TO_WORKER_ID.get(tier, "")
    if not worker_id or not job_id:
        return False, ""
    try:
        from packages.orchestration.worker_registry import (
            load_route_policy, load_worker_registry, evaluate_worker_selection,
            WorkerSelectionRequest, get_worker_spec,
        )
        pol = load_route_policy(job_id, data_dir)
        # Only a policy that actually constrains anything can block — keep default behaviour intact.
        constrains = bool(pol.blocked_worker_ids or pol.blocked_worker_kinds
                          or pol.allowed_worker_kinds or pol.user_selected_worker_ids)
        if not constrains:
            return False, ""
        registry = load_worker_registry(data_dir)
        spec = get_worker_spec(worker_id, registry)
        if spec is None:
            return False, ""
        result = evaluate_worker_selection(
            WorkerSelectionRequest(job_id=job_id, task_type="repair", user_requested_worker_id=""),
            policy=pol, registry=registry, data_dir=data_dir)
        eligible_ids = {c.worker_id for c in result.eligible_candidates}
        # If the user selected a DIFFERENT worker, or this tier's worker is not eligible under the
        # policy, the route is constrained → escalate to human review (recommendation only).
        if pol.user_selected_worker_ids and worker_id not in pol.user_selected_worker_ids:
            return True, (f"route policy selects {pol.user_selected_worker_ids[0]}, not "
                          f"{worker_id} — human review before routing this tier.")
        if worker_id not in eligible_ids:
            return True, (f"route policy blocks/disables worker '{worker_id}' for this route — "
                          "human review or adjust the policy.")
        return False, ""
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return False, ""


# ---------------------------------------------------------------------------
# Models (Step 1574) — no raw content fields anywhere.
# ---------------------------------------------------------------------------


@dataclass
class BuilderRoutingEvidence:
    kind: str
    status: str           # available | unknown | missing
    ref_id: str = ""
    label: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "status": self.status,
                "ref_id": self.ref_id, "label": self.label}


@dataclass
class BuilderRoutingBudget:
    local_advisor_runs_remaining: Any = "unknown"
    local_candidate_runs_remaining: Any = "unknown"
    external_candidate_runs_remaining: Any = "unknown"
    estimated_external_cost: str = "unknown"      # never invented
    daily_external_attempts: int = 0
    per_failure_attempts: int = 0
    per_self_item_attempts: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "local_advisor_runs_remaining": self.local_advisor_runs_remaining,
            "local_candidate_runs_remaining": self.local_candidate_runs_remaining,
            "external_candidate_runs_remaining": self.external_candidate_runs_remaining,
            "estimated_external_cost": self.estimated_external_cost,
            "daily_external_attempts": self.daily_external_attempts,
            "per_failure_attempts": self.per_failure_attempts,
            "per_self_item_attempts": self.per_self_item_attempts,
        }


@dataclass
class BuilderRoutingRisk:
    level: str = "low"            # low | medium | high | unknown
    codes: list[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"level": self.level, "codes": self.codes, "summary": self.summary}


@dataclass
class BuilderRoutingOption:
    tier: str
    available: bool = False
    reason: str = ""
    why_not: str = ""
    justification_codes: list[str] = field(default_factory=list)
    next_command: str = ""
    entity_ids: list[str] = field(default_factory=list)
    score: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "tier": self.tier, "available": self.available, "reason": self.reason,
            "why_not": self.why_not, "justification_codes": self.justification_codes,
            "next_command": self.next_command, "entity_ids": self.entity_ids,
            "score": self.score,
        }


@dataclass
class BuilderRoutingPolicy:
    prefer_deterministic: bool = True
    prefer_local_advisor: bool = True
    allow_local_candidate_generator: bool = False
    allow_external_candidate_generator: bool = False
    max_builder_attempts_per_failure: int = 2
    max_builder_attempts_per_self_item: int = 2
    max_external_builder_attempts_per_day: int = 3
    max_estimated_cost: Any = "unknown"
    require_request_package: bool = True
    require_trust_gate: bool = True
    require_verification: bool = True
    require_human_approval: bool = True
    stop_on_loop_risk: bool = True
    stop_on_medium_risk: bool = False
    stop_on_unknown_evidence: bool = True
    local_first: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "prefer_deterministic": self.prefer_deterministic,
            "prefer_local_advisor": self.prefer_local_advisor,
            "allow_local_candidate_generator": self.allow_local_candidate_generator,
            "allow_external_candidate_generator": self.allow_external_candidate_generator,
            "max_builder_attempts_per_failure": self.max_builder_attempts_per_failure,
            "max_builder_attempts_per_self_item": self.max_builder_attempts_per_self_item,
            "max_external_builder_attempts_per_day": self.max_external_builder_attempts_per_day,
            "max_estimated_cost": self.max_estimated_cost,
            "require_request_package": self.require_request_package,
            "require_trust_gate": self.require_trust_gate,
            "require_verification": self.require_verification,
            "require_human_approval": self.require_human_approval,
            "stop_on_loop_risk": self.stop_on_loop_risk,
            "stop_on_medium_risk": self.stop_on_medium_risk,
            "stop_on_unknown_evidence": self.stop_on_unknown_evidence,
            "local_first": self.local_first,
        }


def default_builder_routing_policy() -> BuilderRoutingPolicy:
    """Safe defaults: deterministic + local advisor allowed; local candidate generation
    disabled unless explicitly enabled; external candidate generation disabled. No execution."""
    return BuilderRoutingPolicy()


@dataclass(frozen=True)
class BuilderRoutingRequest:
    job_id: str = ""
    failure_artifact_id: str = ""
    self_attempt_id: str = ""
    request_package_id: str = ""
    orchestrator_decision_id: str = ""
    user_requested: bool = False
    new: bool = False


@dataclass
class BuilderRoutingDecision:
    routing_id: str
    job_id: str = ""
    failure_artifact_id: str = ""
    self_attempt_id: str = ""
    request_package_id: str = ""
    orchestrator_decision_id: str = ""
    selected_tier: str = BuilderRoutingTier.NO_SAFE_ROUTE
    selected_reason: str = ""
    stop_reason: str = BuilderRoutingStopReason.OK
    rejected_tiers: list[dict[str, Any]] = field(default_factory=list)
    justification_codes: list[str] = field(default_factory=list)
    budget_summary: BuilderRoutingBudget = field(default_factory=BuilderRoutingBudget)
    risk_summary: BuilderRoutingRisk = field(default_factory=BuilderRoutingRisk)
    loop_guard_status: str = LoopGovernorStatus.ALLOW
    evidence_refs: list[BuilderRoutingEvidence] = field(default_factory=list)
    evidence_fingerprint: str = ""
    next_safe_action: str = ""
    safe_summary: str = ""
    created_at: str = ""
    # Token Economy + Context Budget hint (Step 1764) — read-only estimate metadata; never executes.
    token_economy: dict[str, Any] = field(default_factory=dict)


# BuilderRoutingTrace is the persisted form of a decision (same safe shape).
BuilderRoutingTrace = BuilderRoutingDecision


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Step 1576 — routing inputs (safe summaries only; unknown stays unknown)
# ---------------------------------------------------------------------------


def gather_routing_inputs(job_id: str, data_dir: Path, request: BuilderRoutingRequest) -> dict[str, Any]:
    """Collect SAFE durable signals for routing. Reuses the orchestrator's signal gatherer
    (durable stores only, try/except→unknown) and adds local-advisor availability + request
    package presence. Reads safe summaries only; never raw content."""
    inputs: dict[str, Any] = {
        "job_available": False, "review_blocks": False, "advisor_enabled": False,
        "advisor_runs_for_scope": 0, "request_packages": 0,
        "request_package_for_failure": False,
    }
    refs: list[BuilderRoutingEvidence] = []
    if not job_id:
        inputs["_signals"] = {}
        inputs["_refs"] = refs
        return inputs

    from packages.orchestration.orchestrator_brain import _gather_signals, OrchestratorEvidenceRef
    sig_refs: list[OrchestratorEvidenceRef] = []
    sig = _gather_signals(job_id, data_dir, sig_refs)
    inputs["_signals"] = sig
    inputs["job_available"] = any(r.source == "job" and r.status == "available" for r in sig_refs)

    # Review verdict gate (blocker/high open blocks generation).
    try:
        from packages.orchestration.overnight_executor import (
            parse_review_findings, review_findings_block_execution,
        )
        rf = parse_review_findings()
        blocked, _why = review_findings_block_execution(rf)
        inputs["review_blocks"] = bool(blocked)
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        inputs["review_blocks"] = False  # unknown → do not fabricate a block here; risk handled separately

    # Local advisor availability (config only — NEVER calls the model).
    try:
        from packages.orchestration.local_model_advisor import (
            load_local_advisor_config, load_local_advisor_usage,
        )
        cfg = load_local_advisor_config()
        inputs["advisor_enabled"] = bool(getattr(cfg, "enabled", False))
        scope = f"job:{job_id}"
        usage = load_local_advisor_usage(scope, data_dir)
        inputs["advisor_runs_for_scope"] = int(usage.get("run_count", 0))
        inputs["advisor_max_runs"] = int(getattr(cfg, "max_runs", 0))
        refs.append(BuilderRoutingEvidence("local_advisor",
                                           "available" if inputs["advisor_enabled"] else "missing"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        refs.append(BuilderRoutingEvidence("local_advisor", "unknown"))

    # Request package presence (global + for the targeted failure).
    try:
        from packages.orchestration.storage import load_job
        from uuid import UUID
        from packages.orchestration.repair_request_builder import load_request_packages
        job = load_job(UUID(job_id), data_dir)
        pkgs = list(load_request_packages(job).values())
        inputs["request_packages"] = len(pkgs)
        if request.failure_artifact_id:
            inputs["request_package_for_failure"] = any(
                p.get("failure_artifact_id") == request.failure_artifact_id for p in pkgs)
        elif request.request_package_id:
            inputs["request_package_for_failure"] = any(
                p.get("request_package_id") == request.request_package_id for p in pkgs)
        refs.append(BuilderRoutingEvidence("request_package",
                                           "available" if pkgs else "missing"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        refs.append(BuilderRoutingEvidence("request_package", "unknown"))

    # Trust + verification availability (the modules + any reports on the job).
    refs.append(BuilderRoutingEvidence("trust_gate", "available"))
    refs.append(BuilderRoutingEvidence("verification", "available"))
    refs.append(BuilderRoutingEvidence(
        "orchestrator_decision",
        "available" if request.orchestrator_decision_id else "unknown",
        ref_id=request.orchestrator_decision_id))
    inputs["_refs"] = refs
    return inputs


def _deterministic_action(job_id: str, sig: dict[str, Any]) -> tuple[str, list[str]]:
    """Return (catalog command, entity_ids) for a concrete deterministic next step, or ("",[])."""
    if sig.get("pending_intents"):
        iid = sig["pending_intents"][0]
        return f"remedy patch approve {job_id} {iid} --json", [iid]
    if sig.get("approved_intents"):
        iid = sig["approved_intents"][0]
        return f"remedy do continue {job_id} --intent-id {iid} --json", [iid]
    if sig.get("trust_accepted_unverified", 0) > 0 and sig.get("unverified_trust_report_id"):
        trid = sig["unverified_trust_report_id"]
        return f"remedy provider verify {job_id} {trid} --json", [trid]
    if sig.get("verification_needs_review", 0) > 0 and sig.get("verification_needs_review_id"):
        vid = sig["verification_needs_review_id"]
        return f"remedy provider verification-show {job_id} {vid} --json", [vid]
    if sig.get("self_attempts_pending", 0) > 0:
        # self status supports --attempt-id (not --job-id); use it when an id is available,
        # else the scope-less form. Never emit an unsupported flag.
        aid = sig.get("self_pending_attempt_id", "")
        if aid:
            return f"remedy self status --attempt-id {aid} --json", [aid]
        return "remedy self status --json", []
    if sig.get("unresolved_failures", 0) > 0 and sig.get("repair_attempts", 0) == 0:
        fa = sig["failure_ids"][0]
        return f"remedy repair propose {job_id} {fa} --json", [fa]
    return "", []


# ---------------------------------------------------------------------------
# Step 1577 — candidate generation need detector
# ---------------------------------------------------------------------------


def detect_candidate_generation_need(
    inputs: dict[str, Any], request: BuilderRoutingRequest,
) -> tuple[bool, list[str], str]:
    """Return (need, justification_codes, suppress_reason). Need is True only when generation
    MIGHT be justified AND no hard suppressor applies."""
    sig = inputs.get("_signals", {})
    # Hard suppressors first.
    if sig.get("pending_intents"):
        return False, [], BuilderRoutingStopReason.PENDING_INTENT
    if sig.get("approved_intents"):
        return False, [], BuilderRoutingStopReason.PENDING_APPROVAL
    if inputs.get("review_blocks"):
        return False, [], BuilderRoutingStopReason.REVIEW_BLOCKER
    # NOTE: the orchestrator's `budget_exhausted` reflects the loop/test-run budget (test runs
    # are 0 by default) — it is NOT the builder budget and must not suppress generation NEED.
    # The dedicated builder budget (compute_budget) gates the local/external routes instead.
    if sig.get("trust_accepted_unverified", 0) > 0:
        # An accepted candidate awaits verification — verify before generating more.
        return False, [], BuilderRoutingStopReason.NO_NEED
    if sig.get("verification_needs_review", 0) > 0:
        return False, [], BuilderRoutingStopReason.NO_NEED

    codes: list[str] = []
    need = False
    # Unresolved failure with no viable repair intent.
    if sig.get("unresolved_failures", 0) > 0 and not sig.get("pending_intents"):
        need = True
        if sig.get("repair_attempts", 0) == 0:
            codes.append(BuilderRoutingJustification.NO_DETERMINISTIC_FIX_AVAILABLE)
        if sig.get("repair_failed", 0) >= 1:
            codes.append(BuilderRoutingJustification.REPEATED_LOCAL_FAILURE)
    # Approved self-improvement attempt awaiting candidate.
    if sig.get("self_attempts_awaiting", 0) > 0:
        need = True
        codes.append(BuilderRoutingJustification.NO_DETERMINISTIC_FIX_AVAILABLE)
    # Trust/verification rejected a prior candidate — the request may be refinable.
    if sig.get("trust_rejected", 0) > 0 or sig.get("verification_rejected", 0) > 0:
        need = True
        codes.append(BuilderRoutingJustification.LOCAL_ADVISOR_INSUFFICIENT)
    return need, codes, BuilderRoutingStopReason.OK if need else BuilderRoutingStopReason.NO_NEED


# ---------------------------------------------------------------------------
# Step 1580 — budget model
# ---------------------------------------------------------------------------


def compute_budget(
    inputs: dict[str, Any], request: BuilderRoutingRequest, policy: BuilderRoutingPolicy,
    data_dir: Path,
) -> BuilderRoutingBudget:
    b = BuilderRoutingBudget()
    # Local advisor remaining (config max - usage). Unknown if config unavailable.
    if inputs.get("advisor_enabled"):
        mx = int(inputs.get("advisor_max_runs", 0))
        used = int(inputs.get("advisor_runs_for_scope", 0))
        b.local_advisor_runs_remaining = max(0, mx - used)
    else:
        b.local_advisor_runs_remaining = "unknown"
    # Prior builder routing attempts for this failure / self item (durable traces).
    traces = load_builder_routing_traces(scope=_scope(request.job_id), data_dir=data_dir)
    per_failure = sum(1 for t in traces
                      if request.failure_artifact_id
                      and t.get("failure_artifact_id") == request.failure_artifact_id
                      and t.get("selected_tier") in (
                          BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR,
                          BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR))
    per_self = sum(1 for t in traces
                   if request.self_attempt_id
                   and t.get("self_attempt_id") == request.self_attempt_id
                   and t.get("selected_tier") in (
                       BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR,
                       BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR))
    daily = sum(1 for t in traces
                if t.get("selected_tier") == BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR
                and str(t.get("created_at", ""))[:10] == _now()[:10])
    b.per_failure_attempts = per_failure
    b.per_self_item_attempts = per_self
    b.daily_external_attempts = daily
    b.local_candidate_runs_remaining = max(0, policy.max_builder_attempts_per_failure - per_failure)
    b.external_candidate_runs_remaining = max(0, policy.max_external_builder_attempts_per_day - daily)
    # Estimated external cost is NEVER invented.
    b.estimated_external_cost = "unknown"
    return b


def _budget_allows_external(budget: BuilderRoutingBudget, policy: BuilderRoutingPolicy) -> bool:
    if isinstance(budget.external_candidate_runs_remaining, int) \
            and budget.external_candidate_runs_remaining <= 0:
        return False
    # Unknown cost blocks external unless the policy explicitly sets a known max cost.
    if budget.estimated_external_cost == "unknown" and policy.max_estimated_cost == "unknown":
        return False
    return True


def _budget_allows_local(budget: BuilderRoutingBudget) -> bool:
    return not (isinstance(budget.local_candidate_runs_remaining, int)
                and budget.local_candidate_runs_remaining <= 0)


# ---------------------------------------------------------------------------
# Step 1581 — loop governor
# ---------------------------------------------------------------------------


def loop_governor(
    inputs: dict[str, Any], request: BuilderRoutingRequest, fingerprint: str, data_dir: Path,
) -> tuple[str, list[str], str]:
    sig = inputs.get("_signals", {})
    codes: list[str] = []
    # Repeated failure signals → escalate.
    if sig.get("verification_loop_risk", 0) > 0 or sig.get("repair_failed", 0) >= 2 \
            or sig.get("verification_rejected", 0) >= 2 or sig.get("trust_rejected", 0) >= 2:
        codes.append("repeated_failure")
        return LoopGovernorStatus.HUMAN_REVIEW_REQUIRED, codes, \
            "Repeated trust/verification/repair failure — human review before more generation."
    # No repeated EXPENSIVE route for the same evidence fingerprint.
    traces = load_builder_routing_traces(scope=_scope(request.job_id), data_dir=data_dir)
    same_fp_external = [t for t in traces
                        if t.get("evidence_fingerprint") == fingerprint
                        and t.get("selected_tier") == BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR]
    if same_fp_external:
        codes.append("repeated_external_same_evidence")
        return LoopGovernorStatus.BLOCK, codes, \
            "External route already taken for this evidence — needs new evidence."
    if sig.get("trust_rejected", 0) == 1 or sig.get("verification_rejected", 0) == 1:
        codes.append("one_prior_rejection")
        return LoopGovernorStatus.WARN, codes, "One prior rejection — proceed cautiously."
    return LoopGovernorStatus.ALLOW, codes, "No loop risk."


# ---------------------------------------------------------------------------
# Step 1578 / 1582 — local-first option building + selector
# ---------------------------------------------------------------------------


def _trust_and_verification_available(inputs: dict[str, Any]) -> bool:
    refs = inputs.get("_refs", [])
    t = any(r.kind == "trust_gate" and r.status == "available" for r in refs)
    v = any(r.kind == "verification" and r.status == "available" for r in refs)
    return t and v


def _risk(inputs: dict[str, Any], policy: BuilderRoutingPolicy) -> BuilderRoutingRisk:
    sig = inputs.get("_signals", {})
    codes: list[str] = []
    level = "low"
    if inputs.get("review_blocks"):
        codes.append("review_blocker_open"); level = "high"
    # Only SAFETY-CRITICAL inputs being unknown elevate risk — an absent optional
    # orchestrator_decision ref is benign.
    _critical = {"trust_gate", "verification"}
    unknown_critical = [r for r in inputs.get("_refs", [])
                        if r.status == "unknown" and r.kind in _critical]
    if unknown_critical and policy.stop_on_unknown_evidence:
        codes.append("unknown_evidence")
        level = "high"
    return BuilderRoutingRisk(level=level, codes=codes,
                              summary="; ".join(codes) or "No elevated risk.")


def select_builder_routing_decision(
    request: BuilderRoutingRequest, policy: BuilderRoutingPolicy | None = None,
    data_dir: Path | None = None, persist: bool = True,
) -> BuilderRoutingDecision:
    """Choose exactly ONE routing tier (or no_safe_route / human_review_required). Deterministic.
    Reads safe summaries only. NEVER executes a builder/model/provider, generates a candidate,
    or creates an intent/task."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    pol = policy or default_builder_routing_policy()
    from uuid import uuid4
    rid = uuid4().hex[:16]

    d = BuilderRoutingDecision(
        routing_id=rid, job_id=request.job_id, failure_artifact_id=request.failure_artifact_id,
        self_attempt_id=request.self_attempt_id, request_package_id=request.request_package_id,
        orchestrator_decision_id=request.orchestrator_decision_id, created_at=_now())

    # Contract gate (metadata-only routing).
    if request.job_id:
        try:
            from packages.orchestration.storage import load_job, JobNotFoundError
            from packages.orchestration.run_contract import (
                ensure_contract, evaluate_run_action, ContractAction,
            )
            from uuid import UUID
            job = load_job(UUID(request.job_id), ddir)
            contract = ensure_contract(job)
            if not evaluate_run_action(contract, ContractAction.BUILDER_ROUTING_DECIDE).allowed:
                return _finalize(d, BuilderRoutingTier.NO_SAFE_ROUTE,
                                 BuilderRoutingStopReason.CONTRACT_DENIED,
                                 "Contract denies builder routing.",
                                 f"remedy contract inspect {request.job_id} --json", ddir, persist)
        except (ValueError, JobNotFoundError):
            return _finalize(d, BuilderRoutingTier.NO_SAFE_ROUTE,
                             BuilderRoutingStopReason.JOB_NOT_FOUND, "Job not found.",
                             "remedy job list --json", ddir, persist)

    # Token Economy + Context Budget hint (Step 1764) — read-only estimate metadata attached to
    # every decision. Best-effort; never executes a worker / calls a model. No-op-safe on failure.
    if request.job_id:
        try:
            from packages.orchestration.token_economy import routing_token_hint
            d.token_economy = routing_token_hint(request.job_id, data_dir=ddir)
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            d.token_economy = {}

    inputs = gather_routing_inputs(request.job_id, ddir, request)
    sig = inputs.get("_signals", {})
    d.evidence_refs = list(inputs.get("_refs", []))
    d.evidence_fingerprint = _fingerprint(request, sig)
    d.risk_summary = _risk(inputs, pol)
    budget = compute_budget(inputs, request, pol, ddir)
    d.budget_summary = budget
    loop_status, loop_codes, loop_summary = loop_governor(inputs, request, d.evidence_fingerprint, ddir)
    d.loop_guard_status = loop_status

    # Idempotency: reuse an existing trace for the same fingerprint unless --new.
    if not request.new:
        existing = _find_existing_trace(request.job_id, d.evidence_fingerprint, ddir)
        if existing is not None:
            return _decision_from_dict(existing)

    options = _build_options(request, inputs, pol, budget, loop_status, sig)
    rejected = []

    # ---- Selection priority (local-first; safety first) ----
    # 1. Hard human-review / block conditions.
    if d.risk_summary.level == "high" or loop_status == LoopGovernorStatus.HUMAN_REVIEW_REQUIRED:
        d.rejected_tiers = [o.to_dict() for o in options if o.tier != BuilderRoutingTier.HUMAN_REVIEW_REQUIRED]
        sr = (BuilderRoutingStopReason.REVIEW_BLOCKER if inputs.get("review_blocks")
              else (BuilderRoutingStopReason.LOOP_BLOCK
                    if loop_status == LoopGovernorStatus.HUMAN_REVIEW_REQUIRED
                    else BuilderRoutingStopReason.UNKNOWN_EVIDENCE))
        return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED, sr,
                         loop_summary if loop_codes else d.risk_summary.summary,
                         _report_cmd(request.job_id), ddir, persist)

    # 2. Pending approval / deterministic action dominates new generation.
    det_cmd, det_ids = _deterministic_action(request.job_id, sig)
    if det_cmd:
        d.justification_codes = []
        d.rejected_tiers = [o.to_dict() for o in options
                            if o.tier != BuilderRoutingTier.DETERMINISTIC_ONLY]
        sr = (BuilderRoutingStopReason.PENDING_INTENT if sig.get("pending_intents")
              else (BuilderRoutingStopReason.PENDING_APPROVAL if sig.get("approved_intents")
                    else BuilderRoutingStopReason.OK))
        d.evidence_refs.append(BuilderRoutingEvidence("deterministic_action", "available",
                                                      label=det_cmd.split(" --", 1)[0]))
        return _finalize(d, BuilderRoutingTier.DETERMINISTIC_ONLY, sr,
                         "A safe deterministic next action exists; no model needed.",
                         det_cmd, ddir, persist, entity_ids=det_ids)

    # 3. Detect candidate-generation need.
    need, need_codes, suppress = detect_candidate_generation_need(inputs, request)
    if not need:
        # Ambiguity but no generation need → local advisor if untried, else gather evidence.
        if pol.prefer_local_advisor and inputs.get("advisor_enabled") \
                and inputs.get("advisor_runs_for_scope", 0) == 0 and sig.get("unresolved_failures", 0) > 0:
            return _finalize(d, BuilderRoutingTier.LOCAL_ADVISOR, BuilderRoutingStopReason.OK,
                             "Ambiguity exists and local advisor has not been consulted for this evidence.",
                             f"remedy orchestrator decide {request.job_id} --use-local-advisor --json",
                             ddir, persist)
        return _finalize(d, BuilderRoutingTier.NO_SAFE_ROUTE, suppress,
                         "No candidate-generation need; gather evidence or wait.",
                         "remedy self inspect --json", ddir, persist)
    d.justification_codes = list(need_codes)

    # 4. Need exists → local advisor first if untried.
    if pol.prefer_local_advisor and inputs.get("advisor_enabled") \
            and inputs.get("advisor_runs_for_scope", 0) == 0:
        return _finalize(d, BuilderRoutingTier.LOCAL_ADVISOR, BuilderRoutingStopReason.OK,
                         "Local advisor has not been consulted for this evidence; try cheap advice first.",
                         f"remedy orchestrator decide {request.job_id} --use-local-advisor --json",
                         ddir, persist)
    if inputs.get("advisor_runs_for_scope", 0) > 0:
        d.justification_codes.append(BuilderRoutingJustification.LOCAL_ADVISOR_INSUFFICIENT)

    # 5. Request package required before any generation route.
    has_pkg = inputs.get("request_package_for_failure") or inputs.get("request_packages", 0) > 0
    if pol.require_request_package and not has_pkg:
        return _finalize(d, BuilderRoutingTier.NO_SAFE_ROUTE,
                         BuilderRoutingStopReason.MISSING_REQUEST_PACKAGE,
                         "Candidate generation needs a repair request package first.",
                         _prepare_request_cmd(request), ddir, persist)

    # 6. Trust + verification must be available.
    if (pol.require_trust_gate or pol.require_verification) and not _trust_and_verification_available(inputs):
        return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED,
                         BuilderRoutingStopReason.NO_TRUST_VERIFICATION,
                         "Trust Gate / Verification unavailable for safe ingestion.",
                         _report_cmd(request.job_id), ddir, persist)

    # 7. Loop block (non-fatal) on expensive route.
    if loop_status == LoopGovernorStatus.BLOCK:
        return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED,
                         BuilderRoutingStopReason.LOOP_BLOCK, loop_summary,
                         _report_cmd(request.job_id), ddir, persist)

    d.justification_codes += [
        BuilderRoutingJustification.REQUEST_PACKAGE_READY,
        BuilderRoutingJustification.TRUST_AND_VERIFICATION_AVAILABLE,
        BuilderRoutingJustification.HUMAN_APPROVAL_REQUIRED_AFTER_GENERATION,
    ]
    if loop_status in (LoopGovernorStatus.ALLOW, LoopGovernorStatus.WARN):
        d.justification_codes.append(BuilderRoutingJustification.LOOP_RISK_LOW)

    # 8. Local candidate generation (recommended only — never executed).
    if pol.allow_local_candidate_generator and _budget_allows_local(budget):
        # User RoutePolicy gate (Step 1723): if the user blocked/disabled the local worker or
        # selected a different one, escalate to human review. Read-only; no-op under default policy.
        blocked_local, why_local = _route_policy_blocks_tier(
            request.job_id, BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR, ddir)
        if blocked_local:
            return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED,
                             BuilderRoutingStopReason.CONTRACT_DENIED, why_local,
                             _route_policy_cmd(request.job_id), ddir, persist)
        # Candidate Quality feedback (Step 1653): repeated poor quality for this route lowers
        # confidence → escalate to human review instead of recommending more generation. Read-only;
        # NEVER triggers generation. Unknown quality is neutral (does not block).
        try:
            from packages.orchestration.candidate_quality import route_quality_feedback
            fb = route_quality_feedback(model_label="", route_tier=BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR,
                                        data_dir=ddir)
            if fb.get("recommend") == "lower":
                return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED,
                                 BuilderRoutingStopReason.LOOP_BLOCK,
                                 "Candidate quality history is poor for this route — human review "
                                 "before more local generation.",
                                 _report_cmd(request.job_id), ddir, persist)
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass
        d.justification_codes.append(BuilderRoutingJustification.BUDGET_AVAILABLE)
        d.rejected_tiers = [o.to_dict() for o in options
                            if o.tier == BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR]
        return _finalize(d, BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR, BuilderRoutingStopReason.OK,
                         "Local candidate generation is justified (recommended).",
                         _generation_next_cmd(request, d.routing_id), ddir, persist)

    # 9. External candidate generation — strict preconditions.
    if pol.allow_external_candidate_generator:
        # User RoutePolicy gate (Step 1723): if the user blocked/disabled the external worker or
        # selected a different one, escalate to human review. Read-only; no-op under default policy.
        blocked_ext, why_ext = _route_policy_blocks_tier(
            request.job_id, BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR, ddir)
        if blocked_ext:
            return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED,
                             BuilderRoutingStopReason.CONTRACT_DENIED, why_ext,
                             _route_policy_cmd(request.job_id), ddir, persist)
        # External builder quality feedback (Step 1690): poor external-route history escalates to
        # human review. Read-only; NEVER starts a worker or generation. Unknown history is neutral.
        try:
            from packages.orchestration.candidate_quality import route_quality_feedback
            efb = route_quality_feedback(model_label="", route_tier=BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR,
                                         data_dir=ddir)
            if efb.get("recommend") == "lower":
                return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED,
                                 BuilderRoutingStopReason.LOOP_BLOCK,
                                 "External builder quality history is poor — human review before "
                                 "more external work.",
                                 _report_cmd(request.job_id), ddir, persist)
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass
        ext_ok, ext_why = _external_allowed(request, inputs, pol, budget, loop_status, d.justification_codes)
        if ext_ok:
            if request.user_requested:
                d.justification_codes.append(BuilderRoutingJustification.USER_EXPLICITLY_REQUESTED)
            d.justification_codes.append(BuilderRoutingJustification.BUDGET_AVAILABLE)
            return _finalize(d, BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR,
                             BuilderRoutingStopReason.OK,
                             "External candidate generation is justified (recommended; not executed in v0).",
                             _external_package_cmd(request, d.routing_id), ddir, persist)
        # External wanted but not allowed → human review with the reason.
        return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED,
                         BuilderRoutingStopReason.BUDGET_EXHAUSTED if "budget" in ext_why else
                         BuilderRoutingStopReason.NO_TRUST_VERIFICATION,
                         ext_why, _report_cmd(request.job_id), ddir, persist)

    # 10. Generation needed but all generators disabled → human review.
    return _finalize(d, BuilderRoutingTier.HUMAN_REVIEW_REQUIRED, BuilderRoutingStopReason.NO_NEED,
                     "Candidate generation is justified but no generator is enabled by policy.",
                     _report_cmd(request.job_id), ddir, persist)


def _external_allowed(
    request: BuilderRoutingRequest, inputs: dict[str, Any], policy: BuilderRoutingPolicy,
    budget: BuilderRoutingBudget, loop_status: str, have_codes: list[str],
) -> tuple[bool, str]:
    """External builder requires ALL hard preconditions. user_requested can JUSTIFY but never
    bypass trust/verification/budget/loop."""
    if not _trust_and_verification_available(inputs):
        return False, "External route requires Trust Gate + Verification."
    if loop_status == LoopGovernorStatus.BLOCK or loop_status == LoopGovernorStatus.HUMAN_REVIEW_REQUIRED:
        return False, "External route blocked by loop guard."
    if not _budget_allows_external(budget, policy):
        return False, "External route blocked by budget (unknown cost / exhausted)."
    # Budget is verified directly above → BUDGET_AVAILABLE is satisfied here.
    have = set(have_codes) | {BuilderRoutingJustification.BUDGET_AVAILABLE}
    missing = [c for c in _EXTERNAL_REQUIRED_JUSTIFICATIONS if c not in have]
    if missing:
        return False, f"External route missing preconditions: {', '.join(missing)}."
    return True, "ok"


# ---------------------------------------------------------------------------
# Options (for rejected-tiers transparency)
# ---------------------------------------------------------------------------


def _build_options(
    request: BuilderRoutingRequest, inputs: dict[str, Any], policy: BuilderRoutingPolicy,
    budget: BuilderRoutingBudget, loop_status: str, sig: dict[str, Any],
) -> list[BuilderRoutingOption]:
    opts = [
        BuilderRoutingOption(BuilderRoutingTier.DETERMINISTIC_ONLY,
                             available=bool(_deterministic_action(request.job_id, sig)[0])),
        BuilderRoutingOption(BuilderRoutingTier.LOCAL_ADVISOR,
                             available=bool(inputs.get("advisor_enabled"))),
        BuilderRoutingOption(BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR,
                             available=policy.allow_local_candidate_generator,
                             why_not="" if policy.allow_local_candidate_generator else "disabled by policy"),
        BuilderRoutingOption(BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR,
                             available=policy.allow_external_candidate_generator,
                             why_not="" if policy.allow_external_candidate_generator else "disabled by policy"),
    ]
    return opts


# ---------------------------------------------------------------------------
# Next-action command helpers (all catalog-backed + entity-backed)
# ---------------------------------------------------------------------------


def _report_cmd(job_id: str) -> str:
    # builder-routing.report takes --job-id (not positional) per the command catalog.
    return f"remedy builder-routing report --job-id {job_id} --json" if job_id else "remedy self inspect --json"


def _route_policy_cmd(job_id: str) -> str:
    # Catalog-valid route-policy inspection (Step 1723) — the safe next action when a user route
    # policy constrains a route. Read-only; never executes a worker.
    return f"remedy route-policy show {job_id} --json" if job_id else "remedy worker registry-list --json"


def _prepare_request_cmd(request: BuilderRoutingRequest) -> str:
    if request.failure_artifact_id:
        return (f"remedy repair request {request.job_id} "
                f"--failure-artifact-id {request.failure_artifact_id} --json")
    return f"remedy repair request {request.job_id} --json"


def _external_package_cmd(request: BuilderRoutingRequest, routing_id: str = "") -> str:
    # External builder route points at the External Builder Sandbox package export (R-0094), not
    # the old repair-request rail. Export-only; no auto-run, no generation, no provider call.
    if request.job_id:
        rid = f" --route-id {routing_id}" if routing_id else ""
        return f"remedy external-builder package-create {request.job_id}{rid} --json"
    return _prepare_request_cmd(request)


def _generation_next_cmd(request: BuilderRoutingRequest, routing_id: str = "") -> str:
    # When a request package is known, the safe next action is the routing-gated local candidate
    # generator (it runs only if explicitly enabled + routed; output still goes through Trust Gate
    # + Verification + human approval). Otherwise prepare a request package first.
    if request.request_package_id:
        rid = f" --routing-id {routing_id}" if routing_id else ""
        job = f" --job-id {request.job_id}" if request.job_id else ""
        return (f"remedy local-candidate generate "
                f"--request-package-id {request.request_package_id}{job}{rid} --json")
    return _prepare_request_cmd(request)


# ---------------------------------------------------------------------------
# Fingerprint + finalize + persistence (Step 1583)
# ---------------------------------------------------------------------------


def _fingerprint(request: BuilderRoutingRequest, sig: dict[str, Any]) -> str:
    parts = [
        request.job_id, request.failure_artifact_id, request.self_attempt_id,
        str(sig.get("unresolved_failures", 0)), str(sig.get("repair_failed", 0)),
        str(sig.get("trust_accepted", 0)), str(sig.get("trust_rejected", 0)),
        str(sig.get("verification_passed", 0)), str(sig.get("verification_rejected", 0)),
        str(len(sig.get("pending_intents", []))), str(sig.get("request_packages", 0)),
    ]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


def _finalize(
    d: BuilderRoutingDecision, tier: str, stop_reason: str, reason: str, next_action: str,
    data_dir: Path, persist: bool, *, entity_ids: list[str] | None = None,
) -> BuilderRoutingDecision:
    d.selected_tier = tier
    d.stop_reason = stop_reason
    d.selected_reason = _scrub_public(reason)[:300]
    d.next_safe_action = next_action
    d.safe_summary = (f"tier={tier}; stop={stop_reason}; loop={d.loop_guard_status}; "
                      f"risk={d.risk_summary.level}")
    if persist:
        _save_trace(d, data_dir)
    return d


def _scope(job_id: str) -> str:
    return f"job:{job_id}" if job_id else "repository"


def _routing_root(data_dir: Path) -> Path:
    return data_dir / "workspaces" / "orchestrator" / "builder_routing"


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


def export_builder_routing_json(d: BuilderRoutingDecision) -> dict[str, Any]:
    return {
        "version": 1,
        "routing_id": d.routing_id,
        "job_id": d.job_id,
        "failure_artifact_id": d.failure_artifact_id,
        "self_attempt_id": d.self_attempt_id,
        "request_package_id": d.request_package_id,
        "orchestrator_decision_id": d.orchestrator_decision_id,
        "selected_tier": d.selected_tier,
        "selected_reason": d.selected_reason,
        "stop_reason": d.stop_reason,
        "rejected_tiers": d.rejected_tiers,
        "justification_codes": d.justification_codes,
        "budget_summary": d.budget_summary.to_dict(),
        "risk_summary": d.risk_summary.to_dict(),
        "loop_guard_status": d.loop_guard_status,
        "evidence_refs": [e.to_dict() for e in d.evidence_refs],
        "evidence_fingerprint": d.evidence_fingerprint,
        "next_safe_action": d.next_safe_action,
        "safe_summary": d.safe_summary,
        "created_at": d.created_at,
        "token_economy": d.token_economy,
    }


def _save_trace(d: BuilderRoutingDecision, data_dir: Path) -> None:
    path = _routing_root(data_dir) / d.routing_id / "routing.json"
    payload = export_builder_routing_json(d)
    payload["scope"] = _scope(d.job_id)
    payload["content_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    _atomic_write(path, json.dumps(payload, indent=2).encode("utf-8"))


def load_builder_routing_traces(scope: str | None = None, data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    root = _routing_root(ddir)
    out: list[dict] = []
    try:
        for child in sorted(root.iterdir()):
            f = child / "routing.json"
            if not f.is_file():
                continue
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if scope is None or d.get("scope") == scope:
                out.append(d)
    except OSError:
        return out
    out.sort(key=lambda r: r.get("created_at", ""))
    return out


def get_builder_routing_trace(routing_id: str, data_dir: Path | None = None) -> dict | None:
    for t in load_builder_routing_traces(data_dir=data_dir):
        if t.get("routing_id") == routing_id:
            return t
    return None


def _find_existing_trace(job_id: str, fingerprint: str, data_dir: Path) -> dict | None:
    for t in load_builder_routing_traces(scope=_scope(job_id), data_dir=data_dir):
        if t.get("evidence_fingerprint") == fingerprint:
            return t
    return None


def _decision_from_dict(d: dict) -> BuilderRoutingDecision:
    dec = BuilderRoutingDecision(
        routing_id=str(d.get("routing_id", "")), job_id=str(d.get("job_id", "")),
        failure_artifact_id=str(d.get("failure_artifact_id", "")),
        self_attempt_id=str(d.get("self_attempt_id", "")),
        request_package_id=str(d.get("request_package_id", "")),
        orchestrator_decision_id=str(d.get("orchestrator_decision_id", "")),
        selected_tier=str(d.get("selected_tier", BuilderRoutingTier.NO_SAFE_ROUTE)),
        selected_reason=str(d.get("selected_reason", "")),
        stop_reason=str(d.get("stop_reason", "")),
        rejected_tiers=list(d.get("rejected_tiers", [])),
        justification_codes=list(d.get("justification_codes", [])),
        loop_guard_status=str(d.get("loop_guard_status", LoopGovernorStatus.ALLOW)),
        evidence_fingerprint=str(d.get("evidence_fingerprint", "")),
        next_safe_action=str(d.get("next_safe_action", "")),
        safe_summary=str(d.get("safe_summary", "")), created_at=str(d.get("created_at", "")),
        token_economy=dict(d.get("token_economy", {})) if isinstance(d.get("token_economy"), dict) else {},
    )
    b = d.get("budget_summary", {}) or {}
    dec.budget_summary = BuilderRoutingBudget(
        local_advisor_runs_remaining=b.get("local_advisor_runs_remaining", "unknown"),
        local_candidate_runs_remaining=b.get("local_candidate_runs_remaining", "unknown"),
        external_candidate_runs_remaining=b.get("external_candidate_runs_remaining", "unknown"),
        estimated_external_cost=str(b.get("estimated_external_cost", "unknown")),
        daily_external_attempts=int(b.get("daily_external_attempts", 0)),
        per_failure_attempts=int(b.get("per_failure_attempts", 0)),
        per_self_item_attempts=int(b.get("per_self_item_attempts", 0)))
    r = d.get("risk_summary", {}) or {}
    dec.risk_summary = BuilderRoutingRisk(level=str(r.get("level", "low")),
                                          codes=list(r.get("codes", [])),
                                          summary=str(r.get("summary", "")))
    dec.evidence_refs = [BuilderRoutingEvidence(e.get("kind", ""), e.get("status", ""),
                                                e.get("ref_id", ""), e.get("label", ""))
                         for e in d.get("evidence_refs", []) if isinstance(e, dict)]
    return dec
