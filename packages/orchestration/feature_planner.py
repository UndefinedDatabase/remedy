"""
Feature Planner v0 — deterministic next-work suggestions.

No LLM. Rules-based only. Suggestions must be explicitly accepted by user.

Public API::

    build_feature_plan(ledger, job=None) -> FeaturePlan
    export_feature_plan_json(plan) -> dict
    summarize_feature_plan(plan) -> str
    accept_feature_suggestion(plan, suggestion_id, job_id) -> dict
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from packages.orchestration.progress_ledger import (
    ProgressLedger,
    ProgressSource,
    ProgressStatus,
)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class FeaturePlanPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FeaturePlanSource(str, Enum):
    OPEN_FINDING = "open_finding"
    KNOWN_RISK = "known_risk"
    PROOF_GAP = "proof_gap"
    REPAIR_ARTIFACT = "repair_artifact"
    FAILED_TEST = "failed_test"
    STALE_HANDOFF = "stale_handoff"
    ROADMAP = "roadmap"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class FeatureSuggestion:
    """One deterministic suggestion."""

    suggestion_id: str = ""
    title: str = ""
    rationale: str = ""
    priority: FeaturePlanPriority = FeaturePlanPriority.MEDIUM
    source_type: FeaturePlanSource = FeaturePlanSource.ROADMAP
    source_refs: list[str] = field(default_factory=list)
    estimated_risk: str = "low"
    suggested_steps: list[str] = field(default_factory=list)
    acceptance_summary: str = ""
    default_selected: bool = False
    creates_proposed_task: bool = True
    next_action: str = ""


@dataclass
class FeaturePlan:
    """Full feature plan."""

    version: int = 0
    planner_version: str = "v0-deterministic"
    suggestions: list[FeatureSuggestion] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Deterministic suggestion ID
# ---------------------------------------------------------------------------


def _make_suggestion_id(source_type: str, title: str) -> str:
    """Stable, deterministic suggestion ID."""
    raw = f"{source_type}:{title}"
    return "sug-" + hashlib.sha256(raw.encode()).hexdigest()[:8]


# ---------------------------------------------------------------------------
# Roadmap suggestions (when everything is clean)
# ---------------------------------------------------------------------------

_ROADMAP_SUGGESTIONS = [
    FeatureSuggestion(
        suggestion_id="sug-roadmap-provenance",
        title="File Provenance v1 expansion",
        rationale="Extend file provenance chain to cover full lifecycle.",
        priority=FeaturePlanPriority.MEDIUM,
        source_type=FeaturePlanSource.ROADMAP,
        suggested_steps=["Expand proof chain", "Add file-level trust scores", "CLI integration"],
        next_action="remedy feature accept <job_id> sug-roadmap-provenance",
    ),
    FeatureSuggestion(
        suggestion_id="sug-roadmap-contract",
        title="Run Contract Enforcement v1",
        rationale="Enforce execution contracts before applying changes.",
        priority=FeaturePlanPriority.MEDIUM,
        source_type=FeaturePlanSource.ROADMAP,
        suggested_steps=["Define run contracts", "Pre-apply validation", "CLI enforcement"],
        next_action="remedy feature accept <job_id> sug-roadmap-contract",
    ),
    FeatureSuggestion(
        suggestion_id="sug-roadmap-test-exec",
        title="Real Test Execution v1",
        rationale="Run actual project tests (not just fixture stubs).",
        priority=FeaturePlanPriority.MEDIUM,
        source_type=FeaturePlanSource.ROADMAP,
        suggested_steps=["Test discovery", "Sandboxed execution", "Result collection"],
        next_action="remedy feature accept <job_id> sug-roadmap-test-exec",
    ),
    FeatureSuggestion(
        suggestion_id="sug-roadmap-cockpit",
        title="Operator Cockpit read-only v0.2",
        rationale="Read-only dashboard for monitoring job progress.",
        priority=FeaturePlanPriority.LOW,
        source_type=FeaturePlanSource.ROADMAP,
        suggested_steps=["Status endpoint", "Progress view", "Finding summary"],
        next_action="remedy feature accept <job_id> sug-roadmap-cockpit",
    ),
]


# ---------------------------------------------------------------------------
# Step 1018: Deterministic suggestion rules
# ---------------------------------------------------------------------------


def build_feature_plan(ledger: ProgressLedger, job: Any = None) -> FeaturePlan:
    """Build deterministic feature plan from ledger state."""
    plan = FeaturePlan()
    seen_ids: set[str] = set()

    # Rule 0: Continuation outcomes (Step 1176) — tailored next actions, no
    # automatic action or policy relaxation. Claims the relevant ledger item so
    # the generic rules below do not also emit a duplicate suggestion.
    _CONT_RULES = {
        "cont-test-fail": (
            "Start repair for failed continuation test",
            "Continuation test failed — repair available (no auto-repair).",
            FeaturePlanSource.FAILED_TEST,
            "remedy repair start <job_id> <failure_artifact_id> --json",
        ),
        "cont-evidence-incomplete": (
            "Repair continuation evidence",
            "Apply may have succeeded but evidence degraded — manual review.",
            FeaturePlanSource.PROOF_GAP,
            "remedy change proof <job_id> --json",
        ),
        "cont-snapshot-failed": (
            "Investigate continuation snapshot failure",
            "Snapshot could not be created or verified — investigate before retry.",
            FeaturePlanSource.PROOF_GAP,
            "remedy snapshot inspect <job_id> --json",
        ),
        "test-budget-exhausted": (
            "Review run contract test budget",
            "Test budget blocked the continuation — review the contract (no auto-raise).",
            FeaturePlanSource.KNOWN_RISK,
            "remedy contract inspect <job_id> --json",
        ),
    }
    for item in ledger.items:
        rule = _CONT_RULES.get(item.item_id)
        if rule is None:
            continue
        title, rationale, source, next_action = rule
        sug_id = _make_suggestion_id("continuation", item.item_id)
        if sug_id in seen_ids:
            continue
        seen_ids.add(sug_id)
        # Suppress the generic finding/gap suggestions for this same item.
        seen_ids.add(_make_suggestion_id("finding", item.title))
        seen_ids.add(_make_suggestion_id("gap", item.title))
        plan.suggestions.append(FeatureSuggestion(
            suggestion_id=sug_id,
            title=title,
            rationale=rationale,
            priority=FeaturePlanPriority.HIGH,
            source_type=source,
            source_refs=[item.item_id],
            estimated_risk="medium",
            default_selected=True,
            next_action=next_action,
        ))

    # Rule 0b: Repair Loop v1 outcomes (Step 1207) — evidence-backed next actions,
    # no automatic approval or contract relaxation.
    _REPAIR_RULES = {
        "repair-needed": (
            "Propose a repair for the failing test",
            "A failing test has no completed repair proposal yet.",
            FeaturePlanSource.FAILED_TEST,
            "remedy repair propose <job_id> <failure_artifact_id> --json",
        ),
        "repair-approval": (
            "Approve or reject the repair patch intent",
            "A repair patch intent is pending approval — your decision is required.",
            FeaturePlanSource.OPEN_FINDING,
            "remedy patch approve <job_id> <repair_intent_id>",
        ),
        "repair-blocked": (
            "Review the repair blocker",
            "A repair attempt was blocked (e.g. contract or eligibility) — review it.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy repair status <job_id> --json",
        ),
        "repair-apply-tested-failed": (
            "Propose a new repair attempt",
            "The applied repair did not pass its test — propose another repair "
            "(no automatic loop). Provider/source repair may be needed.",
            FeaturePlanSource.FAILED_TEST,
            "remedy repair propose <job_id> <failure_artifact_id> --json",
        ),
        "repair-apply-evidence-incomplete": (
            "Inspect repair evidence",
            "Repair applied but evidence is incomplete — inspect before trusting it.",
            FeaturePlanSource.PROOF_GAP,
            "remedy change proof <job_id> --json",
        ),
        # Bounded Overnight Prep follow-ups (Step 1260).
        "overnight-blocked": (
            "Review overnight readiness",
            "Job is not safe to run unattended — review readiness blockers.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy overnight readiness <job_id> --json",
        ),
        "overnight-human-decision": (
            "Approve or reject pending intents",
            "Unattended run is blocked on pending approvals — decide first.",
            FeaturePlanSource.OPEN_FINDING,
            "remedy overnight readiness <job_id> --json",
        ),
        "overnight-repair-pending": (
            "Approve or reject the repair",
            "A repair patch intent is pending approval before any unattended run.",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy repair status <job_id> --json",
        ),
        "overnight-budget-exhausted": (
            "Review the run-contract budget",
            "A run-contract budget is exhausted — review it (no automatic raise).",
            FeaturePlanSource.KNOWN_RISK,
            "remedy contract inspect <job_id> --json",
        ),
        "overnight-evidence-incomplete": (
            "Inspect incomplete evidence",
            "Evidence is incomplete — inspect before any unattended run.",
            FeaturePlanSource.PROOF_GAP,
            "remedy change proof <job_id> --json",
        ),
        # Bounded Overnight Executor run follow-ups (Step 1290).
        "overnight-run-blocked": (
            "Resolve overnight run blocker",
            "An overnight run was blocked (review findings / budget / risk / approval) — "
            "resolve it manually. No automatic policy relaxation.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy overnight readiness <job_id> --json",
        ),
        "overnight-run-evidence-incomplete": (
            "Inspect overnight run evidence",
            "An overnight run stopped with incomplete evidence — inspect before trusting it.",
            FeaturePlanSource.PROOF_GAP,
            "remedy change proof <job_id> --json",
        ),
        # Provider Trust Gate follow-ups (Step 1323). No automatic provider
        # invocation, no automatic approval.
        "provider-trust-rejected": (
            "Review rejected provider output",
            "External provider output was rejected by the trust gate — inspect findings and "
            "retry with a safer candidate (manual; no automatic provider invocation).",
            FeaturePlanSource.KNOWN_RISK,
            "remedy provider trust-show <job_id> <report_id> --json",
        ),
        "provider-trust-needs-review": (
            "Review provider output (needs human review)",
            "External provider output needs human review before any repair intent.",
            FeaturePlanSource.OPEN_FINDING,
            "remedy provider trust-show <job_id> <report_id> --json",
        ),
        "provider-repair-intent-pending": (
            "Approve or reject the provider repair",
            "A provider-sourced repair patch intent is pending approval (apply via do continue).",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy patch approve <job_id> <intent_id> --json",
        ),
        # Provider Trust Verification v1 follow-ups (Step 1557). No auto provider retry,
        # no auto approval — verification only marks eligibility for a pending intent.
        "provider-verification-passed": (
            "Approve or reject the verified provider repair",
            "A candidate passed verification and has a pending intent — approve or reject "
            "it (apply later via do continue). Passed ≠ approved ≠ applied.",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy patch approve <job_id> <intent_id> --json",
        ),
        "provider-verification-needs-review": (
            "Inspect the verification report (needs review)",
            "A candidate passed the trust gate but verification flagged concerns — inspect "
            "the safe verification report before any approval. No intent was created.",
            FeaturePlanSource.OPEN_FINDING,
            "remedy provider verification-show <job_id> <verification_id> --json",
        ),
        "provider-verification-rejected": (
            "Revise the candidate or request (verification rejected)",
            "Verification rejected the candidate (wrong problem / overclaim / too broad / "
            "unrelated). Revise the request package or candidate manually; no auto retry.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy provider verification-show <job_id> <verification_id> --json",
        ),
        "provider-verification-loop-risk": (
            "Change approach (verification loop risk)",
            "An identical/repeated candidate keeps failing verification — change approach or "
            "escalate to human review. Do not resubmit the same candidate.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy provider verification-show <job_id> <verification_id> --json",
        ),
        # Expensive Builder Routing v0 follow-ups (Step 1593). Routing recommends only;
        # nothing is executed/generated/approved automatically.
        "builder-routing-local-candidate": (
            "Set up local candidate generation (future)",
            "Routing recommends a local candidate generator — relay the request package "
            "manually for now; an Automated Local Candidate Generator Adapter is a future block.",
            FeaturePlanSource.ROADMAP,
            "remedy builder-routing report --job-id <job_id> --json",
        ),
        "builder-routing-external-candidate": (
            "Prepare external candidate generation (manual / enable policy)",
            "Routing recommends an external candidate generator — prepare/relay the request "
            "package manually or enable the external policy. External execution is not built.",
            FeaturePlanSource.ROADMAP,
            "remedy repair request <job_id> --json",
        ),
        "builder-routing-human-review": (
            "Human review required by routing",
            "Builder routing escalated to human review (loop risk / unknown evidence / blocked "
            "generation). A human must decide the next step.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy builder-routing report --job-id <job_id> --json",
        ),
        "builder-routing-blocked": (
            "Gather evidence (no safe builder route)",
            "Routing found no safe builder route — gather evidence or prepare a repair request "
            "package before any generation.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy builder-routing report --job-id <job_id> --json",
        ),
        # Automated Local Candidate Generator v0 follow-ups (Step 1625). No auto retry/approval;
        # generation is disabled by default + routing-gated; output still goes through trust+verif.
        "local-candidate-unavailable": (
            "Configure the local candidate generator (optional)",
            "Local candidate generation is disabled/unavailable — configure an explicit loopback "
            "model if you want it; deterministic flow is unaffected.",
            FeaturePlanSource.ROADMAP,
            "remedy local-candidate status --json",
        ),
        "local-candidate-intent-pending": (
            "Approve or reject the local candidate repair",
            "A local-candidate-generated repair intent is pending approval (apply via do continue).",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy patch approve <job_id> <intent_id> --json",
        ),
        "local-candidate-trust-rejected": (
            "Revise the request (local candidate trust-rejected)",
            "A local candidate was rejected by the Trust Gate — revise the request package or "
            "model; no automatic retry.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy local-candidate status --json",
        ),
        "local-candidate-verification-rejected": (
            "Revise the request (local candidate verification-rejected)",
            "A local candidate was rejected by Verification — revise the request/approach or "
            "escalate to human review; no automatic retry.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy provider verification-show <job_id> <verification_id> --json",
        ),
        "local-candidate-needs-review": (
            "Inspect the local candidate verification (needs review)",
            "A local candidate needs human review after verification — inspect the safe report.",
            FeaturePlanSource.OPEN_FINDING,
            "remedy provider verification-show <job_id> <verification_id> --json",
        ),
        # Local Candidate Quality Evaluation v1 follow-ups (Step 1662). No auto execution.
        "candidate-quality-proof-verified": (
            "Prefer this route (proof-verified quality)",
            "A generated candidate completed with verified proof — prefer the same route/model in "
            "future routing (review the scorecard).",
            FeaturePlanSource.ROADMAP,
            "remedy candidate-quality scorecard --json",
        ),
        "candidate-quality-tests-failed": (
            "Revise candidate (tests failed)",
            "An applied generated candidate's linked test failed — revise the request/approach or "
            "escalate to human review; no automatic retry.",
            FeaturePlanSource.FAILED_TEST,
            "remedy candidate-quality report --json",
        ),
        "candidate-quality-rejected": (
            "Avoid repeat / refine request (candidate rejected)",
            "A generated candidate was rejected — avoid repeating the same route/model; refine the "
            "request or escalate to human review.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy candidate-quality report --json",
        ),
        "candidate-quality-evidence-incomplete": (
            "Gather proof/test evidence (quality incomplete)",
            "A candidate evaluation lacks proof/test evidence — approve + apply via do continue, or "
            "gather proof before claiming success.",
            FeaturePlanSource.PROOF_GAP,
            "remedy candidate-quality report --json",
        ),
        "candidate-quality-loop-risk": (
            "Change approach (candidate quality loop risk)",
            "Repeated failed candidates flagged loop risk — change approach or human review; do not "
            "keep generating.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy candidate-quality report --json",
        ),
        # External Builder Sandbox v0 follow-ups (Step 1691). Suggestions from evidence only — no
        # new external execution is proposed without a user request.
        "external-builder-pending-approval": (
            "Approve or reject the external candidate",
            "An external-builder candidate passed trust+verification and has a pending intent — "
            "approve or reject it (apply via do continue). Untrusted source; human-gated.",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy patch approve <job_id> <intent_id> --json",
        ),
        "external-builder-trust-rejected": (
            "Review external builder route contract (trust rejected)",
            "An external candidate was rejected by the Trust Gate — review the request package / "
            "worker contract; do not auto-resubmit.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy external-builder submission-list <job_id> --json",
        ),
        "external-builder-verification-rejected": (
            "Review external builder route contract (verification rejected)",
            "An external candidate was rejected by Verification — revise the request package / "
            "worker contract or escalate to human review.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy external-builder submission-list <job_id> --json",
        ),
        # Provider patch materialization follow-ups (Step 1349). No auto approve/retry.
        "provider-repair-intent-pending-approval": (
            "Approve or reject the materialized provider repair",
            "A materialized provider repair intent is pending approval; apply later via do continue.",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy patch approve <job_id> <intent_id> --json",
        ),
        "provider-materialization-failed": (
            "Inspect failed provider materialization",
            "An accepted provider candidate could not be materialized (unsupported patch shape) — "
            "inspect the material; retry with a conservative single-.md patch (manual).",
            FeaturePlanSource.KNOWN_RISK,
            "remedy provider material-show <job_id> <material_id> --json",
        ),
        # Repair Request Builder follow-ups (Step 1379). Provider-agnostic; no auto
        # external execution, no auto approval.
        "external-candidate-pending": (
            "Import the external candidate response",
            "A repair request was prepared — relay it to any external actor, then import "
            "the response (it will be quarantined + trust-validated).",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy provider intake-repair <job_id> --failure-artifact-id <id> --input <file> --provider <label> --json",
        ),
        # Self-Dogfood follow-ups (Step 1416). No automatic execution/approval.
        "self-improvement-pending-evaluation": (
            "Evaluate self-proposed improvement tasks",
            "Self-dogfood proposed improvement tasks await human evaluation/approval "
            "(no self-apply / self-merge).",
            FeaturePlanSource.KNOWN_RISK,
            "remedy decision list <job_id> --json",
        ),
        # Self-Dogfood Execution follow-ups (Step 1443). No automatic execution.
        "self-execution-awaiting-candidate": (
            "Provide the external candidate for a self-improvement attempt",
            "A self-improvement request is prepared — relay it externally and import the "
            "response via provider intake-repair (trust-validated).",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy provider intake-repair <job_id> --input <file> --provider self_dogfood --json",
        ),
        "self-execution-intent-pending": (
            "Approve or reject the self-improvement intent",
            "A self-improvement patch intent is pending approval (apply via do continue).",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy patch approve <job_id> <intent_id> --json",
        ),
        "self-execution-blocked": (
            "Review the blocked self-improvement attempt",
            "A self-improvement attempt is blocked — inspect its state.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy self status --json",
        ),
        # Orchestrator Brain follow-ups (Step 1482). No automatic execution.
        "orchestrator-human-review": (
            "Resolve the orchestrator's human-review decision",
            "The orchestrator routed the next step to human review (open blocker/high or "
            "loop guard) — decide before any execution.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy orchestrator report --json",
        ),
        "orchestrator-local-advisor": (
            "Consider a local model advisor (future)",
            "The orchestrator found close options where a cheap local advisor could help "
            "critique the plan — Local Model Advisor Adapter v0 is the next block.",
            FeaturePlanSource.ROADMAP,
            "remedy orchestrator report --json",
        ),
        "orchestrator-external-builder": (
            "Provide an external candidate (trust-gated)",
            "Candidate generation is the bottleneck — relay a request and import the "
            "response through the Provider Trust Gate (no direct provider execution).",
            FeaturePlanSource.REPAIR_ARTIFACT,
            "remedy orchestrator report --json",
        ),
        # Local Model Advisor follow-ups (Step 1518). No automatic execution.
        "local-advisor-unavailable": (
            "Configure a local model advisor (optional)",
            "The orchestrator could not reach a local advisor — configure a loopback "
            "Ollama endpoint + model if you want optional advisory critique (disabled by "
            "default; never required for deterministic operation).",
            FeaturePlanSource.ROADMAP,
            "remedy local-advisor status --json",
        ),
        "local-advisor-concern": (
            "Review the local advisor's concern",
            "A local advisor raised a concern about the deterministic plan — review the "
            "orchestrator report. The advisor is advisory only; it never changes the action.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy orchestrator report --json",
        ),
        "local-advisor-human-review": (
            "Resolve the advisor-escalated human review",
            "The local advisor flagged high risk on weak/unknown evidence; the orchestrator "
            "escalated to human review — gather evidence or decide before any execution.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy orchestrator report --json",
        ),
    }
    for item in ledger.items:
        rule = _REPAIR_RULES.get(item.item_id)
        if rule is None:
            continue
        title, rationale, source, next_action = rule
        sug_id = _make_suggestion_id("repair", item.item_id)
        if sug_id in seen_ids:
            continue
        seen_ids.add(sug_id)
        seen_ids.add(_make_suggestion_id("finding", item.title))
        seen_ids.add(_make_suggestion_id("gap", item.title))
        plan.suggestions.append(FeatureSuggestion(
            suggestion_id=sug_id,
            title=title,
            rationale=rationale,
            priority=FeaturePlanPriority.HIGH,
            source_type=source,
            source_refs=[item.item_id],
            estimated_risk="medium",
            default_selected=True,
            next_action=next_action,
        ))

    # Rule 0b: Worker Registry + Route Policy evidence (Step 1728) — forward-looking, user-choice
    # suggestions. Item-id driven (only fire when the ledger surfaced the matching evidence), so
    # they never fabricate provider availability and never auto-build. Effort ≈ suggested_steps;
    # impact ≈ priority. No execution; the user must choose.
    _WORKER_REGISTRY_RULES = {
        "worker-registry-available": (
            "Add a Model/Route Tournament Harness (compare workers/routes)",
            "The Worker Registry now models replaceable workers — a Tournament Harness could "
            "compare routes by evidence (cost/quality). Metadata/eval only; no execution added here.",
            FeaturePlanSource.ROADMAP, FeaturePlanPriority.LOW, "low",
            ["Define route trial schema", "Score by candidate-quality evidence", "Read-only report"],
            "remedy worker registry-list --json",
        ),
        "route-policy-local-first": (
            "Add a real Ollama adapter for the local route",
            "Local/Ollama-first preference is enabled but the Ollama worker is a non-executable "
            "placeholder. A real loopback adapter would let cheap tasks run locally to cut tokens.",
            FeaturePlanSource.ROADMAP, FeaturePlanPriority.MEDIUM, "medium",
            ["Loopback-only transport", "Config-gated + disabled by default", "Trust+verify output"],
            "remedy worker registry-show ollama.placeholder --json",
        ),
        "route-policy-expensive-approval": (
            "Review expensive route usage",
            "The recommended route is expensive/high-risk/placeholder and needs human approval — "
            "review whether a cheaper local route or a tighter policy fits.",
            FeaturePlanSource.KNOWN_RISK, FeaturePlanPriority.MEDIUM, "low",
            ["Inspect route policy", "Consider --max-cost-tier", "Prefer local for cheap tasks"],
            "remedy route-policy show <job_id> --json",
        ),
        "route-policy-token-warning": (
            "Tighten the token/context budget",
            "Estimated context/token exceeds the recommended route's band (estimate). Consider a "
            "smaller context or a larger-context worker.",
            FeaturePlanSource.KNOWN_RISK, FeaturePlanPriority.MEDIUM, "low",
            ["Set token_budget_hint", "Add Context Budget Optimizer", "Prefer smaller context"],
            "remedy route-policy evaluate <job_id> --json",
        ),
    }
    for item in ledger.items:
        rule = _WORKER_REGISTRY_RULES.get(item.item_id)
        if rule is None:
            continue
        title, rationale, source, priority, risk, steps, next_action = rule
        sug_id = _make_suggestion_id("worker-registry", item.item_id)
        if sug_id in seen_ids:
            continue
        seen_ids.add(sug_id)
        # Claim generic variants so Rules 1-3 don't double-emit for the same ledger item.
        seen_ids.add(_make_suggestion_id("risk", item.title))
        seen_ids.add(_make_suggestion_id("finding", item.title))
        seen_ids.add(_make_suggestion_id("gap", item.title))
        plan.suggestions.append(FeatureSuggestion(
            suggestion_id=sug_id,
            title=title,
            rationale=rationale,
            priority=priority,
            source_type=source,
            source_refs=[item.item_id],
            estimated_risk=risk,
            suggested_steps=steps,
            creates_proposed_task=False,
            next_action=next_action,
        ))

    # Rule 0c: Token Economy + Context Budget evidence (Step 1768) — forward-looking, user-choice
    # suggestions. Item-id driven (fire only on real budget/context evidence). Effort ≈
    # suggested_steps; impact ≈ priority. No auto-build, no execution, no fake evidence.
    _TOKEN_ECONOMY_RULES = {
        "token-budget-over": (
            "Add Context Budget Optimizer enforcement",
            "Estimated tokens exceed the budget — an enforcing optimizer could trim context to the "
            "budget automatically (still no execution; recommendation-gated).",
            FeaturePlanSource.KNOWN_RISK, FeaturePlanPriority.MEDIUM, "low",
            ["Define enforcement policy", "Wire to context pack recommender", "Human-gated apply"],
            "remedy context-pack recommend <job_id> --json",
        ),
        "token-economy-expensive-route": (
            "Tighten expensive-route approval policy",
            "An expensive/unknown/high-risk route is being recommended — consider a tighter "
            "route policy (max cost tier, approval-over-tokens threshold).",
            FeaturePlanSource.KNOWN_RISK, FeaturePlanPriority.MEDIUM, "low",
            ["Lower --max-cost-tier", "Lower --require-human-approval-over-tokens", "Prefer local"],
            "remedy route-policy show <job_id> --json",
        ),
        "token-economy-local-route": (
            "Configure a real Ollama worker for the local route",
            "A cheap/local route fits the budget — a real Ollama adapter would let this run "
            "locally to cut tokens (placeholder is non-executable today).",
            FeaturePlanSource.ROADMAP, FeaturePlanPriority.MEDIUM, "medium",
            ["Loopback-only transport", "Config-gated + disabled by default", "Trust+verify output"],
            "remedy worker registry-show ollama.placeholder --json",
        ),
        "token-memory-candidates": (
            "Add MemPalace project memory v0",
            "Durable-knowledge candidates were suggested — a MemPalace memory layer could retain "
            "them across runs (suggestions only today; nothing is persisted as memory).",
            FeaturePlanSource.ROADMAP, FeaturePlanPriority.LOW, "medium",
            ["Define memory schema", "Safe retention policy", "Read-only recall surface"],
            "remedy token economy-report <job_id> --json",
        ),
        "token-context-compression": (
            "Add a token savings report to the Cockpit",
            "Context compression is recommended — a Cockpit savings view would make token "
            "reduction visible and actionable for the user (estimates only).",
            FeaturePlanSource.ROADMAP, FeaturePlanPriority.LOW, "low",
            ["Aggregate estimated savings", "Cockpit read-only panel", "No verified-savings claim"],
            "remedy token economy-report <job_id> --json",
        ),
    }
    for item in ledger.items:
        rule = _TOKEN_ECONOMY_RULES.get(item.item_id)
        if rule is None:
            continue
        title, rationale, source, priority, risk, steps, next_action = rule
        sug_id = _make_suggestion_id("token-economy", item.item_id)
        if sug_id in seen_ids:
            continue
        seen_ids.add(sug_id)
        # Claim the generic risk/finding/gap variants for this item so Rules 1-3 below do not also
        # emit a duplicate (creates_proposed_task=True) suggestion for the same ledger item.
        seen_ids.add(_make_suggestion_id("risk", item.title))
        seen_ids.add(_make_suggestion_id("finding", item.title))
        seen_ids.add(_make_suggestion_id("gap", item.title))
        plan.suggestions.append(FeatureSuggestion(
            suggestion_id=sug_id,
            title=title,
            rationale=rationale,
            priority=priority,
            source_type=source,
            source_refs=[item.item_id],
            estimated_risk=risk,
            suggested_steps=steps,
            creates_proposed_task=False,
            next_action=next_action,
        ))

    # Rule 0d: Model/Route Tournament evidence (Step 1809) — item-id driven, evidence-based,
    # user-choice suggestions. Effort ≈ suggested_steps; impact ≈ priority. No auto-build.
    _TOURNAMENT_RULES = {
        "tournament-insufficient-evidence": (
            "Gather route evidence (run an external builder package)",
            "The route tournament has insufficient evidence to pick a winner — generating a safe "
            "external builder request package (or local candidate) would produce comparable "
            "evidence. No execution is added; the candidate stays untrusted + verified.",
            FeaturePlanSource.KNOWN_RISK, FeaturePlanPriority.MEDIUM, "low",
            ["Export external builder package", "Submit candidate (untrusted)", "Compare evidence"],
            "remedy external-builder package-create <job_id> --json",
        ),
        "tournament-winner": (
            "Tighten route policy around the winning route",
            "An evidence-backed route is recommended — consider a route policy that prefers it for "
            "this task type while keeping safety floors (approval for expensive/high-risk).",
            FeaturePlanSource.ROADMAP, FeaturePlanPriority.LOW, "low",
            ["Review tournament report", "Set --prefer-worker", "Keep approval floors"],
            "remedy route-policy show <job_id> --json",
        ),
    }
    for item in ledger.items:
        rule = _TOURNAMENT_RULES.get(item.item_id)
        if rule is None:
            continue
        title, rationale, source, priority, risk, steps, next_action = rule
        sug_id = _make_suggestion_id("tournament", item.item_id)
        if sug_id in seen_ids:
            continue
        seen_ids.add(sug_id)
        seen_ids.add(_make_suggestion_id("risk", item.title))
        seen_ids.add(_make_suggestion_id("finding", item.title))
        seen_ids.add(_make_suggestion_id("gap", item.title))
        plan.suggestions.append(FeatureSuggestion(
            suggestion_id=sug_id, title=title, rationale=rationale, priority=priority,
            source_type=source, source_refs=[item.item_id], estimated_risk=risk,
            suggested_steps=steps, creates_proposed_task=False, next_action=next_action))

    # Rule 0e: Real Test Execution + Snapshot/Rollback evidence (Step 1890). Item-id driven; required
    # vs optional clear; Impact (priority) + Effort (estimated_risk) included; no auto-build/exec.
    _REAL_TEST_RULES = {
        "test-run-failed": (
            "Create a repair task from the failing test",
            "The latest allowed test run failed — turn the safe Test Failure Artifact into a repair "
            "task (no auto-repair; candidate stays untrusted + re-tested).",
            FeaturePlanSource.FAILED_TEST, FeaturePlanPriority.HIGH, "medium",
            ["Inspect failure artifact", "Create fix task", "Re-run allowed test"],
            "remedy repair status <job_id> --json",
        ),
        "rollback-restore-unavailable": (
            "Implement real rollback restore (currently metadata-only)",
            "A snapshot proof exists but no real restore path — v1 records metadata only. A future "
            "block can add a verified restore so the rollback gate can be satisfied.",
            FeaturePlanSource.PROOF_GAP, FeaturePlanPriority.MEDIUM, "high",
            ["Design restore from recovery blobs", "Verify restore", "Mark restore_available honestly"],
            "remedy rollback show <rollback_proof_id> --json",
        ),
    }
    for item in ledger.items:
        rule = _REAL_TEST_RULES.get(item.item_id)
        if rule is None:
            continue
        title, rationale, source, priority, risk, steps, next_action = rule
        sug_id = _make_suggestion_id("real-test", item.item_id)
        if sug_id in seen_ids:
            continue
        seen_ids.add(sug_id)
        seen_ids.add(_make_suggestion_id("risk", item.title))
        seen_ids.add(_make_suggestion_id("finding", item.title))
        seen_ids.add(_make_suggestion_id("gap", item.title))
        plan.suggestions.append(FeatureSuggestion(
            suggestion_id=sug_id, title=title, rationale=rationale, priority=priority,
            source_type=source, source_refs=[item.item_id], estimated_risk=risk,
            suggested_steps=steps, creates_proposed_task=False, next_action=next_action))

    # Rule 1: Open blocker/high findings -> high priority suggestions
    for item in ledger.items:
        if item.status == ProgressStatus.BLOCKED:
            sug_id = _make_suggestion_id("finding", item.title)
            if sug_id in seen_ids:
                continue
            seen_ids.add(sug_id)
            plan.suggestions.append(FeatureSuggestion(
                suggestion_id=sug_id,
                title=f"Resolve: {item.title}"[:200],
                rationale=f"Open {item.severity} finding blocks progress.",
                priority=FeaturePlanPriority.HIGH,
                source_type=FeaturePlanSource.OPEN_FINDING,
                source_refs=[item.item_id],
                estimated_risk="medium",
                default_selected=True,
                next_action=f"Fix {item.item_id}",
            ))

    # Rule 2: Known risks / pre-existing failures -> medium/high suggestions
    for item in ledger.items:
        if item.status == ProgressStatus.RISK:
            sug_id = _make_suggestion_id("risk", item.title)
            if sug_id in seen_ids:
                continue
            seen_ids.add(sug_id)

            is_test_failure = item.source_type in (
                ProgressSource.REPAIR_ARTIFACT, ProgressSource.KNOWN_RISK
            ) and "fail" in item.title.lower()

            priority = FeaturePlanPriority.HIGH if is_test_failure else FeaturePlanPriority.MEDIUM
            source = FeaturePlanSource.FAILED_TEST if is_test_failure else FeaturePlanSource.KNOWN_RISK

            plan.suggestions.append(FeatureSuggestion(
                suggestion_id=sug_id,
                title=f"Address risk: {item.title}"[:200],
                rationale="Known risk should be tracked and resolved.",
                priority=priority,
                source_type=source,
                source_refs=[item.item_id],
                estimated_risk="medium",
                next_action=f"Investigate {item.item_id}",
            ))

    # Rule 3: Proof gaps — snapshot-unverified applies get HIGH priority (no revert capability)
    for item in ledger.items:
        if item.source_type == ProgressSource.PROOF_GAP:
            sug_id = _make_suggestion_id("gap", item.title)
            if sug_id in seen_ids:
                continue
            seen_ids.add(sug_id)
            is_snapshot_gap = "snapshot" in item.title.lower() or "snapshot" in item.safe_summary.lower()
            plan.suggestions.append(FeatureSuggestion(
                suggestion_id=sug_id,
                title=f"Close proof gap: {item.title}"[:200],
                rationale=(
                    "Apply without verified snapshot — revert capability unavailable."
                    if is_snapshot_gap else
                    "Proof chain incomplete — close gap for verification."
                ),
                priority=FeaturePlanPriority.HIGH if is_snapshot_gap else FeaturePlanPriority.MEDIUM,
                source_type=FeaturePlanSource.PROOF_GAP,
                source_refs=[item.item_id],
                estimated_risk="high" if is_snapshot_gap else "low",
                next_action=(
                    "Re-apply with snapshot or run remedy snapshot inspect"
                    if is_snapshot_gap else
                    "File Provenance expansion"
                ),
            ))

    # Rule 4: Stale handoff (inconsistencies in ledger)
    if ledger.inconsistencies:
        sug_id = _make_suggestion_id("handoff", "stale-handoff")
        if sug_id not in seen_ids:
            seen_ids.add(sug_id)
            plan.suggestions.append(FeatureSuggestion(
                suggestion_id=sug_id,
                title="Fix stale handoff state",
                rationale=f"{len(ledger.inconsistencies)} inconsistency(ies) in progress ledger.",
                priority=FeaturePlanPriority.HIGH,
                source_type=FeaturePlanSource.STALE_HANDOFF,
                source_refs=[],
                estimated_risk="low",
                next_action="Update .agent/ files to resolve inconsistencies",
            ))

    # Rule 5: If no issues, suggest roadmap items
    if not plan.suggestions:
        for roadmap in _ROADMAP_SUGGESTIONS:
            if roadmap.suggestion_id not in seen_ids:
                seen_ids.add(roadmap.suggestion_id)
                plan.suggestions.append(roadmap)

    # Sort: high first, then medium, then low
    priority_order = {FeaturePlanPriority.HIGH: 0, FeaturePlanPriority.MEDIUM: 1, FeaturePlanPriority.LOW: 2}
    plan.suggestions.sort(key=lambda s: priority_order.get(s.priority, 1))

    return plan


# ---------------------------------------------------------------------------
# Accept suggestion -> ProposedTask
# ---------------------------------------------------------------------------


def accept_feature_suggestion(plan: FeaturePlan, suggestion_id: str, job_id: str) -> dict:
    """Accept a suggestion — returns ProposedTask metadata dict.

    Does NOT create a real task or execute anything.
    Returns metadata for creating a ProposedTask.
    """
    suggestion = None
    for s in plan.suggestions:
        if s.suggestion_id == suggestion_id:
            suggestion = s
            break

    if suggestion is None:
        return {"error": f"Suggestion {suggestion_id} not found", "accepted": False}

    return {
        "accepted": True,
        "suggestion_id": suggestion.suggestion_id,
        "title": suggestion.title,
        "rationale": suggestion.rationale,
        "priority": suggestion.priority.value,
        "source_type": suggestion.source_type.value,
        "source_refs": suggestion.source_refs,
        "planner_version": plan.planner_version,
        "job_id": job_id,
        "creates_proposed_task": True,
        "executed": False,
        "applied": False,
    }


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_feature_plan_json(plan: FeaturePlan) -> dict:
    """Export feature plan as safe JSON dict."""
    return {
        "version": plan.version,
        "planner_version": plan.planner_version,
        "suggestion_count": len(plan.suggestions),
        "suggestions": [
            {
                "suggestion_id": s.suggestion_id,
                "title": s.title,
                "rationale": s.rationale,
                "priority": s.priority.value,
                "source_type": s.source_type.value,
                "source_refs": s.source_refs,
                "estimated_risk": s.estimated_risk,
                "suggested_steps": s.suggested_steps,
                "default_selected": s.default_selected,
                "next_action": s.next_action,
            }
            for s in plan.suggestions
        ],
    }


def summarize_feature_plan(plan: FeaturePlan) -> str:
    """Human-readable feature plan summary."""
    lines = ["Feature Plan (v0 — deterministic)", "=" * 40]
    lines.append(f"Suggestions: {len(plan.suggestions)}")
    lines.append("")

    for s in plan.suggestions:
        selected = "*" if s.default_selected else " "
        lines.append(f"  [{selected}] {s.suggestion_id} — {s.title}")
        lines.append(f"      Priority: {s.priority.value}  Source: {s.source_type.value}")
        lines.append(f"      Rationale: {s.rationale}")
        if s.next_action:
            lines.append(f"      Next: {s.next_action}")
        lines.append("")

    lines.append("To accept: remedy feature accept <job_id> <suggestion_id>")
    return "\n".join(lines)
