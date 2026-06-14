"""
Main Orchestrator Brain v0 (Steps 1465-1498) — Decision Engine, Anti-Loop Guard,
Model Routing Plan.

Reads the current project/job/system state from SAFE summaries, builds a Situation,
generates deterministic Options, scores them, guards against repeated failed loops,
defines a model routing PLAN (never calls a model), and selects exactly ONE structured
next-step Decision with rationale.

Core principle: LLMs are advisors/builders. The orchestrator is the controller.
Evidence is truth. This module is planning/decision ONLY — it never executes an
action, never calls Ollama/a provider/the network/a subprocess, never applies/approves/
creates a PR/mutates code, and never inserts Job.tasks. Model routing is a plan, not a
call. Every emitted next_safe_action is catalog-backed and references a real entity.

Public API::

    build_orchestrator_situation(job_id=None, data_dir=None, agent_dir=None) -> OrchestratorSituation
    select_orchestrator_decision(situation, data_dir=None, persist=False) -> OrchestratorDecision
    build_orchestrator_report(job_id=None, data_dir=None) -> dict
    record_idea(text, data_dir=None) -> OrchestratorIdeaRecord
    list_ideas(data_dir=None) -> list[dict]
    list_decisions(scope, data_dir=None) -> list[dict]
    export_situation_json / export_decision_json / render_report_markdown
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


# ---------------------------------------------------------------------------
# Vocabularies (Steps 1466/1470/1471/1472)
# ---------------------------------------------------------------------------


class StopReason:
    SELECTED = "selected"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    NO_SAFE_ACTION = "no_safe_action"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"
    BLOCKED = "blocked"


class RoutingTier:
    DETERMINISTIC_ONLY = "deterministic_only"
    LOCAL_ADVISOR_PREFERRED = "local_advisor_preferred"
    EXTERNAL_BUILDER_NEEDED = "external_builder_needed"
    HUMAN_REVIEW_REQUIRED = "human_review_required"


class LoopGuardStatus:
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"
    REQUIRE_HUMAN_REVIEW = "require_human_review"


class OptionKind:
    INSPECT = "inspect"
    PROPOSE_REPAIR = "propose_repair"
    PREPARE_REPAIR_REQUEST = "prepare_repair_request"
    IMPORT_CANDIDATE = "import_candidate"
    APPROVE_INTENT = "approve_intent"
    CONTINUE_INTENT = "continue_intent"
    OVERNIGHT_RUN = "overnight_run"
    SELF_INSPECT = "self_inspect"
    SELF_PROPOSE = "self_propose"
    SELF_EXECUTE = "self_execute"
    PROVIDER_TRUST_VERIFICATION = "provider_trust_verification"
    LOCAL_ADVISOR_NEEDED = "local_advisor_needed"
    HUMAN_REVIEW = "human_review"


# ---------------------------------------------------------------------------
# Models (Step 1466) — no raw content fields.
# ---------------------------------------------------------------------------


@dataclass
class OrchestratorEvidenceRef:
    source: str
    status: str = "available"   # available | missing | malformed | unknown
    ref: str = ""
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source, "status": self.status, "ref": self.ref,
                "summary": self.summary}


@dataclass
class OrchestratorRisk:
    id: str
    severity: str
    summary: str
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "severity": self.severity, "summary": self.summary,
                "source": self.source}


@dataclass
class OrchestratorOption:
    option_id: str
    kind: str
    label: str
    command: str = ""
    entity_ids: list[str] = field(default_factory=list)
    required_permission: str = ""
    required_contract_action: str = ""
    risk_level: str = "low"
    expected_outcome: str = ""
    why_now: str = ""
    why_not_now: str = ""
    available: bool = True
    score: int = 0
    reason_codes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "option_id": self.option_id, "kind": self.kind, "label": self.label,
            "command": self.command, "entity_ids": self.entity_ids,
            "required_permission": self.required_permission,
            "required_contract_action": self.required_contract_action,
            "risk_level": self.risk_level, "expected_outcome": self.expected_outcome,
            "why_now": self.why_now, "why_not_now": self.why_not_now,
            "available": self.available, "score": self.score, "reason_codes": self.reason_codes,
        }


@dataclass
class OrchestratorModelRoutingPlan:
    tier: str = RoutingTier.DETERMINISTIC_ONLY
    reason: str = ""
    allow_external: bool = False
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"tier": self.tier, "reason": self.reason,
                "allow_external": self.allow_external, "notes": self.notes}


@dataclass
class OrchestratorLoopGuard:
    status: str = LoopGuardStatus.ALLOW
    reason: str = ""
    repeated_signal: str = ""
    count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"status": self.status, "reason": self.reason,
                "repeated_signal": self.repeated_signal, "count": self.count}


@dataclass
class OrchestratorIdeaRecord:
    idea_id: str
    fingerprint: str
    classification: str
    summary: str
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"idea_id": self.idea_id, "fingerprint": self.fingerprint,
                "classification": self.classification, "summary": self.summary,
                "created_at": self.created_at}


@dataclass
class OrchestratorSituation:
    generated_at: str = ""
    scope: str = "repository"
    job_id: str = ""
    repository_identity: str = ""
    current_phase: str = "unknown"
    options: list[OrchestratorOption] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    risks: list[OrchestratorRisk] = field(default_factory=list)
    evidence_refs: list[OrchestratorEvidenceRef] = field(default_factory=list)
    loop_guard: OrchestratorLoopGuard = field(default_factory=OrchestratorLoopGuard)
    model_routing_plan: OrchestratorModelRoutingPlan = field(default_factory=OrchestratorModelRoutingPlan)
    evidence_fingerprint: str = ""
    evidence_status: str = "complete"
    safe_summary: str = ""
    _signals: dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class OrchestratorDecision:
    decision_id: str = ""
    generated_at: str = ""
    scope: str = "repository"
    job_id: str = ""
    current_phase: str = "unknown"
    selected_option: dict[str, Any] | None = None
    rejected_options: list[dict[str, Any]] = field(default_factory=list)
    confidence: str = "low"
    risks: list[OrchestratorRisk] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    evidence_refs: list[OrchestratorEvidenceRef] = field(default_factory=list)
    model_routing_plan: OrchestratorModelRoutingPlan = field(default_factory=OrchestratorModelRoutingPlan)
    loop_guard_status: str = LoopGuardStatus.ALLOW
    next_safe_action: str = ""
    stop_reason: str = StopReason.NO_SAFE_ACTION
    rationale: str = ""
    evidence_fingerprint: str = ""
    safe_summary: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scrub(text: str) -> str:
    from packages.orchestration.provider_trust import _scrub_public
    return _scrub_public(str(text))[:300]


def _agent_dir() -> Path:
    return Path(os.environ.get("REMEDY_AGENT_DIR") or ".agent")


# ---------------------------------------------------------------------------
# Idea intake (Steps 1479/1480) — metadata-only, scrubbed, classified.
# ---------------------------------------------------------------------------

_IDEA_RULES = [
    ("safety_concern", ("unsafe", "security", "secret", "leak", "danger", "vulnerab")),
    ("bug_report", ("bug", "broken", "fails", "error", "crash", "regression")),
    ("feature_request", ("add", "support", "feature", "would be nice", "ability to")),
    ("roadmap_hint", ("eventually", "future", "later", "roadmap", "next")),
]


def _classify_idea(text: str) -> str:
    low = text.lower()
    for label, kws in _IDEA_RULES:
        if any(k in low for k in kws):
            return label
    return "product_goal"


def _ideas_dir(data_dir: Path) -> Path:
    return data_dir / "orchestrator" / "ideas"


def record_idea(text: str, data_dir: Path | None = None) -> OrchestratorIdeaRecord:
    """Capture a user idea as a safe, scrubbed, classified record. Metadata-only;
    never executes anything, never creates a ProposedTask."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    safe = _scrub(text)
    fp = hashlib.sha256(safe.lower().encode("utf-8")).hexdigest()[:12]
    rec = OrchestratorIdeaRecord(
        idea_id=fp, fingerprint=fp, classification=_classify_idea(safe),
        summary=safe, created_at=_now())
    d = _ideas_dir(ddir)
    try:
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{fp}.json"
        if not path.exists():  # dedupe by fingerprint
            tmp = path.with_suffix(".json.tmp")
            tmp.write_bytes(json.dumps(rec.to_dict(), indent=2, sort_keys=True).encode("utf-8"))
            os.replace(tmp, path)
    except OSError:
        pass
    return rec


def list_ideas(data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    d = _ideas_dir(ddir)
    if not d.is_dir():
        return []
    out: list[dict] = []
    try:
        for p in sorted(d.glob("*.json")):
            try:
                out.append(json.loads(p.read_bytes()))
            except (OSError, json.JSONDecodeError):
                continue
    except OSError:
        return []
    return out


# ---------------------------------------------------------------------------
# Situation builder (Step 1467) — safe summaries only.
# ---------------------------------------------------------------------------


def _review_state() -> tuple[str, bool, int]:
    """Return (verdict, blocks, open_blocker_high)."""
    from packages.orchestration.overnight_executor import (
        parse_review_findings, review_findings_block_execution,
    )
    f = parse_review_findings(_agent_dir() / "live_review.md")
    blocks, _ = review_findings_block_execution(f)
    return f.verdict, blocks, f.open_blocker_or_high


def _gather_signals(job_id: str, data_dir: Path,
                    refs: list[OrchestratorEvidenceRef]) -> dict[str, Any]:
    """Collect safe, durable signals for a job. Unknown stays unknown."""
    sig: dict[str, Any] = {
        "unresolved_failures": 0, "failure_ids": [], "repair_attempts": 0,
        "repair_failed": 0, "pending_intents": [], "approved_intents": [],
        "trust_accepted": 0, "trust_rejected": 0, "materialized": 0,
        "request_packages": 0, "self_attempts_awaiting": 0, "self_attempts_pending": 0,
        "self_proposed_approved": [], "self_items": 0, "budget_exhausted": False,
    }
    from packages.orchestration.storage import load_job, JobNotFoundError
    try:
        job = load_job(UUID(job_id), data_dir)
    except (ValueError, JobNotFoundError):
        refs.append(OrchestratorEvidenceRef("job", "missing"))
        return sig
    refs.append(OrchestratorEvidenceRef("job", "available", ref=job_id))

    # Failures + repair attempts.
    failures = [a for a in job.artifacts if (a.metadata or {}).get("test_failure")
                and not (a.metadata or {}).get("failure_resolved")]
    sig["unresolved_failures"] = len(failures)
    sig["failure_ids"] = [str(a.id) for a in failures]
    try:
        from packages.orchestration.repair_loop import load_repair_attempts
        attempts = list(load_repair_attempts(job).values())
        sig["repair_attempts"] = len(attempts)
        sig["repair_failed"] = sum(1 for a in attempts if a.status == "tested_failed")
        refs.append(OrchestratorEvidenceRef("repair_attempts", "available"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        refs.append(OrchestratorEvidenceRef("repair_attempts", "unknown"))

    # Patch intents.
    try:
        from packages.orchestration.approval_queue import (
            list_patch_intents, APPROVAL_PENDING, APPROVAL_APPROVED,
        )
        intents = list_patch_intents(job)
        sig["pending_intents"] = [i["intent_id"] for i in intents if i["state"] == APPROVAL_PENDING]
        sig["approved_intents"] = [i["intent_id"] for i in intents if i["state"] == APPROVAL_APPROVED]
        refs.append(OrchestratorEvidenceRef("patch_intents", "available"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        refs.append(OrchestratorEvidenceRef("patch_intents", "unknown"))

    # Provider trust + materials + requests.
    try:
        from packages.orchestration.provider_trust import load_trust_reports
        reps = list(load_trust_reports(job).values())
        sig["trust_accepted"] = sum(1 for r in reps if r.get("trust_status") == "accepted")
        sig["trust_rejected"] = sum(1 for r in reps if r.get("trust_status") == "rejected")
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass
    try:
        from packages.orchestration.provider_patch_material import load_materials
        sig["materialized"] = sum(1 for m in load_materials(job).values()
                                  if m.get("material_state") == "materialized")
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass
    try:
        from packages.orchestration.repair_request_builder import load_request_packages
        sig["request_packages"] = len(load_request_packages(job))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass

    # Self attempts + proposed tasks.
    try:
        from packages.orchestration.self_dogfood_execution import list_attempts
        mine = [a for a in list_attempts(data_dir) if a.get("job_id") == job_id]
        sig["self_attempts_awaiting"] = sum(1 for a in mine if a.get("state") == "awaiting_external_candidate")
        sig["self_attempts_pending"] = sum(1 for a in mine if a.get("state") == "intent_pending_approval")
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass
    try:
        from packages.orchestration.proposed_tasks import load_proposed_tasks_safe, ProposedTaskStatus
        pts, _ = load_proposed_tasks_safe(job_id, data_dir)
        sig["self_proposed_approved"] = [
            t.id for t in pts if getattr(t, "task_type", "") == "self_dogfood"
            and t.status == ProposedTaskStatus.APPROVED_FOR_BUILD and not t.materialized_task_id]
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass

    # Budget.
    try:
        from packages.orchestration.run_contract import (
            ensure_contract, load_usage, evaluate_run_action, ContractAction,
        )
        c = ensure_contract(job)
        u = load_usage(job)
        loops_left = c.max_loops - u.loops_used
        tests_left = c.max_test_runs - u.test_runs_used
        sig["budget_exhausted"] = (loops_left <= 0) or (tests_left <= 0)
        # Contract permission for the apply path (R-0086): do not recommend a
        # do-continue (patch_apply) option the contract denies / stop_before_apply blocks.
        sig["patch_apply_allowed"] = bool(
            evaluate_run_action(c, ContractAction.PATCH_APPLY).allowed)
        refs.append(OrchestratorEvidenceRef("run_contract", "available"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        sig["patch_apply_allowed"] = False
        refs.append(OrchestratorEvidenceRef("run_contract", "unknown"))
    return sig


def _repository_identity() -> str:
    try:
        return Path.cwd().name
    except OSError:
        return "repository"


def _phase(sig: dict[str, Any], job_id: str) -> str:
    if not job_id:
        return "no_job"
    if sig.get("pending_intents"):
        return "intent_pending_approval"
    if sig.get("approved_intents"):
        return "intent_approved"
    if sig.get("self_attempts_pending"):
        return "self_intent_pending_approval"
    if sig.get("self_attempts_awaiting"):
        return "self_awaiting_candidate"
    if sig.get("unresolved_failures"):
        return "unresolved_failure"
    return "idle"


def build_orchestrator_situation(
    job_id: str | None = None, data_dir: Path | None = None, agent_dir: Path | None = None,
) -> OrchestratorSituation:
    """Read safe state into a Situation: evidence refs, deterministic options, risks,
    loop guard, and a model routing plan. Read-only."""
    from packages.orchestration.data_paths import resolve_data_root
    if agent_dir is not None:
        os.environ["REMEDY_AGENT_DIR"] = str(agent_dir)
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    s = OrchestratorSituation(generated_at=_now(), job_id=job_id or "",
                              scope=("job" if job_id else "repository"),
                              repository_identity=_repository_identity())

    refs: list[OrchestratorRisk] = []
    verdict, review_blocks, open_bh = _review_state()
    s.evidence_refs.append(OrchestratorEvidenceRef(".agent/live_review.md",
                                                   "available" if verdict != "unknown" else "missing",
                                                   summary=f"verdict={verdict}"))
    if review_blocks:
        s.blockers.append("review_findings_open")
        s.risks.append(OrchestratorRisk("review_findings_open", "blocker",
                                        f"Live review verdict={verdict}, open blocker/high={open_bh}.",
                                        "live_review"))

    sig: dict[str, Any] = {}
    if job_id:
        sig = _gather_signals(job_id, ddir, s.evidence_refs)
        if sig.get("budget_exhausted"):
            s.blockers.append("budget_exhausted")
            s.risks.append(OrchestratorRisk("budget_exhausted", "high",
                                            "Run-contract budget exhausted.", "run_contract"))
        if sig.get("unresolved_failures", 0) > 0:
            s.risks.append(OrchestratorRisk("unresolved_failures", "high",
                                            f"{sig['unresolved_failures']} unresolved failure(s).",
                                            "failure_artifacts"))
    s._signals = sig
    s.current_phase = _phase(sig, job_id or "")

    # Self-improvement items (repository-level, read-only) for inspect/propose options.
    try:
        from packages.orchestration import self_dogfood as SD
        insp = SD.build_self_dogfood_inspection(job_id, ddir)
        sig["self_items"] = len(insp.items)
        s.evidence_refs.append(OrchestratorEvidenceRef("self_dogfood", "available",
                                                       summary=f"{len(insp.items)} item(s)"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        s.evidence_refs.append(OrchestratorEvidenceRef("self_dogfood", "unknown"))

    # Ideas as roadmap hints (not truth).
    ideas = list_ideas(ddir)
    if ideas:
        s.evidence_refs.append(OrchestratorEvidenceRef("ideas", "available",
                                                       summary=f"{len(ideas)} idea(s)"))

    s.options = _generate_options(s, sig, job_id or "", review_blocks, ideas)
    s.evidence_fingerprint = _evidence_fingerprint(sig, verdict)
    s.loop_guard = _loop_guard(s, sig, ddir)
    _score_options(s, sig, review_blocks)
    s.model_routing_plan = _routing_plan(s, sig, review_blocks)
    s.evidence_status = "degraded" if any(r.status in ("missing", "malformed")
                                          for r in s.evidence_refs) else "complete"
    avail = [o for o in s.options if o.available]
    s.safe_summary = (f"phase={s.current_phase}; {len(avail)} available option(s); "
                      f"{len(s.blockers)} blocker(s); loop={s.loop_guard.status}; "
                      f"routing={s.model_routing_plan.tier}")
    return s


# ---------------------------------------------------------------------------
# Option generator (Step 1468) — real entities + catalog-backed commands only.
# ---------------------------------------------------------------------------


def _catalog_ok(command: str) -> bool:
    if not command:
        return True
    try:
        from packages.orchestration.do_run import validate_next_safe_action_command
        return validate_next_safe_action_command(command)
    except (ImportError, ValueError, TypeError):
        return False


def _opt(kind: str, label: str, *, command: str = "", entity_ids: list[str] | None = None,
         risk: str = "low", outcome: str = "", why_now: str = "", why_not: str = "",
         contract_action: str = "", permission: str = "") -> OrchestratorOption:
    available = True
    if command and not _catalog_ok(command):
        available = False
        why_not = (why_not + " (command not catalog-backed)").strip()
    return OrchestratorOption(
        option_id=hashlib.sha256(f"{kind}:{command}".encode()).hexdigest()[:12],
        kind=kind, label=label, command=command, entity_ids=entity_ids or [],
        risk_level=risk, expected_outcome=outcome, why_now=why_now, why_not_now=why_not,
        required_contract_action=contract_action, required_permission=permission,
        available=available)


def _generate_options(s: OrchestratorSituation, sig: dict[str, Any], job_id: str,
                      review_blocks: bool, ideas: list[dict]) -> list[OrchestratorOption]:
    opts: list[OrchestratorOption] = []
    # Always-safe inspect baseline.
    opts.append(_opt(OptionKind.SELF_INSPECT, "Inspect self-improvement evidence",
                     command="remedy self inspect --json",
                     outcome="Refresh improvement items.", why_now="Always safe, read-only."))

    if job_id:
        # Pending approval (human decision unblocks the most).
        for iid in sig.get("pending_intents", [])[:1]:
            opts.append(_opt(OptionKind.APPROVE_INTENT, "Approve a pending patch intent",
                             command=f"remedy patch approve {job_id} {iid} --json",
                             entity_ids=[iid], risk="medium",
                             outcome="Unblocks apply via do continue.",
                             why_now="A patch intent is pending human approval.",
                             contract_action="patch_apply"))
        # Approved intent → continue.
        for iid in sig.get("approved_intents", [])[:1]:
            cont = _opt(OptionKind.CONTINUE_INTENT, "Continue an approved intent",
                        command=f"remedy do continue {job_id} --intent-id {iid} --json",
                        entity_ids=[iid], risk="medium",
                        outcome="Snapshot → apply → test → proof.",
                        why_now="An approved intent is ready for one cycle.",
                        contract_action="patch_apply", permission="repo_generated_write")
            # R-0086: do not recommend apply when the contract denies it.
            if not sig.get("patch_apply_allowed", False):
                cont.available = False
                cont.why_not_now = "Contract denies patch_apply (or stop_before_apply)."
            opts.append(cont)
        # Unresolved failure with no repair attempt → propose repair.
        if sig.get("unresolved_failures", 0) > 0 and sig.get("repair_attempts", 0) == 0:
            fa = sig["failure_ids"][0]
            opts.append(_opt(OptionKind.PROPOSE_REPAIR, "Propose a repair for an unresolved failure",
                             command=f"remedy repair propose {job_id} {fa} --json",
                             entity_ids=[fa], risk="low",
                             outcome="Creates a repair proposal (no apply).",
                             why_now="Unresolved failure with no repair attempt."))
        # Self attempt awaiting candidate.
        if sig.get("self_attempts_awaiting", 0) > 0:
            opts.append(_opt(OptionKind.IMPORT_CANDIDATE, "Import an external candidate for a self attempt",
                             command=(f"remedy provider intake-repair {job_id} --input <file> "
                                      f"--provider self_dogfood --json"),
                             risk="low", outcome="Candidate enters the Trust Gate.",
                             why_now="A self attempt awaits an external candidate."))
        # Approved self ProposedTask → execute.
        for pt in sig.get("self_proposed_approved", [])[:1]:
            opts.append(_opt(OptionKind.SELF_EXECUTE, "Execute an approved self-improvement task",
                             command=f"remedy self execute {pt} --job-id {job_id} --json",
                             entity_ids=[pt], risk="low",
                             outcome="Prepares a self request (no apply).",
                             why_now="An approved self-dogfood task has no attempt yet."))

    # Self propose if items exist.
    if sig.get("self_items", 0) > 0:
        opts.append(_opt(OptionKind.SELF_PROPOSE, "Propose self-improvement tasks",
                         command="remedy self plan --json", risk="low",
                         outcome="Plan improvement items for human approval.",
                         why_now="Self-improvement items exist."))

    # Repeated trust rejection → roadmap option (verification), human-gated.
    if sig.get("trust_rejected", 0) >= 2:
        opts.append(_opt(OptionKind.PROVIDER_TRUST_VERIFICATION,
                         "Provider Trust Verification needed (roadmap)",
                         risk="medium", outcome="Stronger trust verification (future).",
                         why_now="Repeated provider trust rejections.",
                         why_not="Not built yet — human review / future block."))
        opts[-1].available = False

    # Ideas as roadmap hints → human review only.
    for idea in ideas[:1]:
        opts.append(_opt(OptionKind.HUMAN_REVIEW, f"Review user idea ({idea.get('classification','')})",
                         risk="low", outcome="Human decides if the idea becomes work.",
                         why_now="A captured user idea may inform the roadmap.",
                         why_not="Ideas are hints, not evidence — require human review."))
        opts[-1].available = False

    # Human-review fallback always present (never executes).
    opts.append(_opt(OptionKind.HUMAN_REVIEW, "Human review required",
                     risk="low", outcome="A human chooses the next step.",
                     why_now="No safe automatic action, or gates require a human."))
    opts[-1].available = False
    return opts


# ---------------------------------------------------------------------------
# Decision scorer (Step 1469)
# ---------------------------------------------------------------------------

_BASE_SCORE = {
    OptionKind.APPROVE_INTENT: 90,
    OptionKind.CONTINUE_INTENT: 85,
    OptionKind.IMPORT_CANDIDATE: 70,
    OptionKind.PROPOSE_REPAIR: 65,
    OptionKind.SELF_EXECUTE: 55,
    OptionKind.SELF_PROPOSE: 40,
    OptionKind.SELF_INSPECT: 20,
    OptionKind.PROVIDER_TRUST_VERIFICATION: 10,
    OptionKind.LOCAL_ADVISOR_NEEDED: 10,
    OptionKind.HUMAN_REVIEW: 5,
}


def _score_options(s: OrchestratorSituation, sig: dict[str, Any], review_blocks: bool) -> None:
    for o in s.options:
        score = _BASE_SCORE.get(o.kind, 10)
        codes: list[str] = []
        if not o.available:
            score = 0
            codes.append("unavailable")
        # Open blocker/high review forces human-review: execution-like options unsafe.
        if review_blocks and o.kind not in (OptionKind.SELF_INSPECT, OptionKind.HUMAN_REVIEW):
            score = min(score, 1)
            codes.append("review_blocks_execution")
        # Budget exhaustion suppresses apply-type options.
        if sig.get("budget_exhausted") and o.kind in (OptionKind.CONTINUE_INTENT,):
            score = min(score, 2)
            codes.append("budget_exhausted")
        # Loop guard block suppresses the repeated option kind.
        if s.loop_guard.status in (LoopGuardStatus.BLOCK, LoopGuardStatus.REQUIRE_HUMAN_REVIEW) \
                and o.kind == s.loop_guard.repeated_signal:
            score = min(score, 1)
            codes.append("loop_guard_block")
        if o.risk_level == "medium":
            codes.append("medium_risk")
        o.score = score
        o.reason_codes = codes


# ---------------------------------------------------------------------------
# Anti-loop guard (Step 1470)
# ---------------------------------------------------------------------------


def _evidence_fingerprint(sig: dict[str, Any], verdict: str) -> str:
    key = json.dumps({
        "verdict": verdict,
        "unresolved_failures": sig.get("unresolved_failures", 0),
        "repair_attempts": sig.get("repair_attempts", 0),
        "repair_failed": sig.get("repair_failed", 0),
        "pending_intents": len(sig.get("pending_intents", [])),
        "approved_intents": len(sig.get("approved_intents", [])),
        "trust_rejected": sig.get("trust_rejected", 0),
        "trust_accepted": sig.get("trust_accepted", 0),
        "materialized": sig.get("materialized", 0),
        "self_attempts_awaiting": sig.get("self_attempts_awaiting", 0),
        "self_attempts_pending": sig.get("self_attempts_pending", 0),
        "self_items": sig.get("self_items", 0),
    }, sort_keys=True)
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def _loop_guard(s: OrchestratorSituation, sig: dict[str, Any], data_dir: Path) -> OrchestratorLoopGuard:
    # Durable failure signals first.
    if sig.get("repair_failed", 0) >= 2:
        return OrchestratorLoopGuard(LoopGuardStatus.REQUIRE_HUMAN_REVIEW,
                                     "Repeated repair failures for this job.",
                                     OptionKind.PROPOSE_REPAIR, sig["repair_failed"])
    if sig.get("trust_rejected", 0) >= 2:
        return OrchestratorLoopGuard(LoopGuardStatus.BLOCK,
                                     "Repeated provider trust rejections.",
                                     OptionKind.IMPORT_CANDIDATE, sig["trust_rejected"])
    # Decision-history repetition: same selected kind + same evidence fingerprint.
    prior = list_decisions(s.scope_key(), data_dir)
    same = [d for d in prior if d.get("evidence_fingerprint") == s.evidence_fingerprint
            and (d.get("selected_option") or {}).get("kind")]
    if len(same) >= 2:
        kind = (same[-1].get("selected_option") or {}).get("kind", "")
        return OrchestratorLoopGuard(LoopGuardStatus.BLOCK,
                                     "Same decision repeated with no new evidence.", kind, len(same))
    if len(same) == 1:
        kind = (same[-1].get("selected_option") or {}).get("kind", "")
        return OrchestratorLoopGuard(LoopGuardStatus.WARN,
                                     "Decision repeats; provide new evidence to advance.", kind, 1)
    return OrchestratorLoopGuard(LoopGuardStatus.ALLOW, "", "", 0)


# OrchestratorSituation helper for scope key (job vs repository).
def _scope_key(self: OrchestratorSituation) -> str:
    return f"job:{self.job_id}" if self.job_id else "repository"


OrchestratorSituation.scope_key = _scope_key  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Model routing plan (Step 1471) — PLAN ONLY, never a call.
# ---------------------------------------------------------------------------


def _routing_plan(s: OrchestratorSituation, sig: dict[str, Any],
                  review_blocks: bool) -> OrchestratorModelRoutingPlan:
    if review_blocks or s.loop_guard.status in (LoopGuardStatus.BLOCK,
                                                LoopGuardStatus.REQUIRE_HUMAN_REVIEW):
        return OrchestratorModelRoutingPlan(
            RoutingTier.HUMAN_REVIEW_REQUIRED,
            "Open blocker/high review or loop guard block — a human decides.", False)
    avail = [o for o in s.options if o.available and o.score > 1]
    if not avail:
        return OrchestratorModelRoutingPlan(
            RoutingTier.HUMAN_REVIEW_REQUIRED, "No safe deterministic option.", False)
    avail.sort(key=lambda o: o.score, reverse=True)
    top = avail[0].score
    gap = top - (avail[1].score if len(avail) > 1 else 0)
    # Candidate generation needed + complete evidence + budget → external builder (PLAN).
    needs_candidate = sig.get("self_attempts_awaiting", 0) > 0 or (
        sig.get("unresolved_failures", 0) > 0 and sig.get("repair_attempts", 0) == 0)
    if needs_candidate and not sig.get("budget_exhausted") and s.evidence_status == "complete":
        return OrchestratorModelRoutingPlan(
            RoutingTier.EXTERNAL_BUILDER_NEEDED,
            "Candidate generation is the bottleneck; external builder output would help — "
            "but only through the Trust Gate, never applied directly.", True,
            notes="Plan only — no model is called in v0. Output is untrusted.")
    if gap >= 30:
        return OrchestratorModelRoutingPlan(
            RoutingTier.DETERMINISTIC_ONLY,
            "A single deterministic option clearly dominates; no model needed.", False)
    return OrchestratorModelRoutingPlan(
        RoutingTier.LOCAL_ADVISOR_PREFERRED,
        "Options are close; a cheap local advisor could critique the plan (future).", False,
        notes="Plan only — local advisor adapter not built; deterministic choice still applies.")


# ---------------------------------------------------------------------------
# Decision selector (Step 1472) + trace (Step 1473)
# ---------------------------------------------------------------------------


def _decisions_root(scope_key: str, data_dir: Path) -> Path:
    safe = scope_key.replace(":", "_").replace("/", "_")
    return data_dir / "workspaces" / "orchestrator" / "decisions" / safe


def list_decisions(scope_key: str, data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    base = _decisions_root(scope_key, ddir)
    if not base.is_dir():
        return []
    out: list[dict] = []
    try:
        files = sorted(base.glob("*/decision.json"))
        for p in files:
            try:
                out.append(json.loads(p.read_bytes()))
            except (OSError, json.JSONDecodeError):
                continue
    except OSError:
        return []
    out.sort(key=lambda d: d.get("generated_at", ""))
    return out


def _save_decision(decision: OrchestratorDecision, data_dir: Path) -> None:
    base = _decisions_root(f"job:{decision.job_id}" if decision.job_id else "repository", data_dir)
    ddir = base / decision.decision_id
    try:
        ddir.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(export_decision_json(decision), indent=2, sort_keys=True).encode("utf-8")
        tmp = ddir / "decision.json.tmp"
        tmp.write_bytes(payload)
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        os.replace(tmp, ddir / "decision.json")
        (ddir / "decision.sha256").write_text(hashlib.sha256(payload).hexdigest())
    except OSError:
        pass


def select_orchestrator_decision(
    situation: OrchestratorSituation, data_dir: Path | None = None, persist: bool = False,
) -> OrchestratorDecision:
    """Choose exactly one outcome: a selected option, human_review_required,
    no_safe_action, or evidence_incomplete. Deterministic. No execution."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    s = situation
    d = OrchestratorDecision(
        decision_id=uuid4().hex[:12], generated_at=_now(), scope=s.scope, job_id=s.job_id,
        current_phase=s.current_phase, risks=s.risks, blockers=s.blockers,
        evidence_refs=s.evidence_refs, model_routing_plan=s.model_routing_plan,
        loop_guard_status=s.loop_guard.status, evidence_fingerprint=s.evidence_fingerprint)

    executable = [o for o in s.options if o.available and o.score > 1]
    executable.sort(key=lambda o: o.score, reverse=True)
    rejected = [o for o in s.options if o is not (executable[0] if executable else None)]
    d.rejected_options = [{"kind": o.kind, "label": o.label, "score": o.score,
                           "why_not": o.why_not_now or "; ".join(o.reason_codes)}
                          for o in rejected[:8]]

    if "review_findings_open" in s.blockers or s.loop_guard.status == LoopGuardStatus.REQUIRE_HUMAN_REVIEW:
        d.stop_reason = StopReason.HUMAN_REVIEW_REQUIRED
        d.confidence = "high"
        d.next_safe_action = "remedy self inspect --json"
        d.rationale = ("Open blocker/high review or repeated-failure loop guard — a human "
                       "must decide before any execution-like action.")
    elif s.evidence_status == "degraded" and not executable:
        d.stop_reason = StopReason.EVIDENCE_INCOMPLETE
        d.confidence = "low"
        d.next_safe_action = "remedy self inspect --json"
        d.rationale = "Evidence is incomplete; inspect before acting."
    elif not executable:
        d.stop_reason = StopReason.NO_SAFE_ACTION
        d.confidence = "medium"
        d.next_safe_action = "remedy self inspect --json"
        d.rationale = "No safe automatic action; inspect or wait for human input."
    else:
        top = executable[0]
        d.selected_option = top.to_dict()
        d.stop_reason = StopReason.SELECTED
        d.next_safe_action = top.command or "remedy self inspect --json"
        gap = top.score - (executable[1].score if len(executable) > 1 else 0)
        d.confidence = "high" if gap >= 30 else ("medium" if gap >= 10 else "low")
        d.rationale = f"{top.label}: {top.why_now}".strip()

    d.safe_summary = (f"decision={d.stop_reason}; "
                      f"selected={(d.selected_option or {}).get('kind', 'none')}; "
                      f"confidence={d.confidence}; routing={d.model_routing_plan.tier}; "
                      f"loop={d.loop_guard_status}")
    if persist:
        _save_decision(d, ddir)
    return d


# ---------------------------------------------------------------------------
# Report (Step 1476) + exports
# ---------------------------------------------------------------------------


def export_situation_json(s: OrchestratorSituation) -> dict[str, Any]:
    return {
        "version": 1, "generated_at": s.generated_at, "scope": s.scope, "job_id": s.job_id,
        "repository_identity": s.repository_identity, "current_phase": s.current_phase,
        "options": [o.to_dict() for o in s.options],
        "available_option_count": sum(1 for o in s.options if o.available and o.score > 1),
        "blockers": s.blockers, "risks": [r.to_dict() for r in s.risks],
        "evidence_refs": [e.to_dict() for e in s.evidence_refs],
        "loop_guard": s.loop_guard.to_dict(),
        "model_routing_plan": s.model_routing_plan.to_dict(),
        "evidence_fingerprint": s.evidence_fingerprint,
        "evidence_status": s.evidence_status, "safe_summary": s.safe_summary,
    }


def export_decision_json(d: OrchestratorDecision) -> dict[str, Any]:
    return {
        "version": 1, "decision_id": d.decision_id, "generated_at": d.generated_at,
        "scope": d.scope, "job_id": d.job_id, "current_phase": d.current_phase,
        "selected_option": d.selected_option,
        "rejected_options": d.rejected_options, "confidence": d.confidence,
        "risks": [r.to_dict() for r in d.risks], "blockers": d.blockers,
        "evidence_refs": [e.to_dict() for e in d.evidence_refs],
        "model_routing_plan": d.model_routing_plan.to_dict(),
        "loop_guard_status": d.loop_guard_status, "next_safe_action": d.next_safe_action,
        "stop_reason": d.stop_reason, "rationale": d.rationale,
        "evidence_fingerprint": d.evidence_fingerprint, "safe_summary": d.safe_summary,
    }


def build_orchestrator_report(
    job_id: str | None = None, data_dir: Path | None = None, agent_dir: Path | None = None,
) -> dict[str, Any]:
    s = build_orchestrator_situation(job_id, data_dir, agent_dir)
    d = select_orchestrator_decision(s, data_dir, persist=False)
    return {"situation": export_situation_json(s), "decision": export_decision_json(d)}


def render_report_markdown(data: dict[str, Any]) -> str:
    s = data.get("situation", {})
    d = data.get("decision", {})
    lines = [f"# Orchestrator Report — {s.get('repository_identity', '')}", ""]
    lines.append("## Current situation")
    lines.append(s.get("safe_summary", ""))
    lines.append("")
    lines.append("## Best next action")
    sel = d.get("selected_option")
    if sel:
        lines.append(f"- {sel.get('label')} → `{d.get('next_safe_action')}`")
        lines.append(f"  - why: {d.get('rationale')}")
    else:
        lines.append(f"- {d.get('stop_reason')}: {d.get('rationale')}")
    lines.append("")
    lines.append("## Why not other actions")
    for r in d.get("rejected_options", [])[:6]:
        lines.append(f"- {r.get('label')} (score {r.get('score')}): {r.get('why_not')}")
    lines.append("")
    lines.append("## Evidence gaps")
    for e in s.get("evidence_refs", []):
        if e.get("status") in ("missing", "malformed", "unknown"):
            lines.append(f"- {e['source']}: {e['status']}")
    lines.append("")
    lines.append("## Risks")
    for r in s.get("risks", []):
        lines.append(f"- ({r['severity']}) {r['summary']}")
    lines.append("")
    lines.append("## Loop guard")
    lg = s.get("loop_guard", {})
    lines.append(f"- {lg.get('status')}: {lg.get('reason') or 'no repetition detected'}")
    lines.append("")
    lines.append("## Model routing recommendation")
    mrp = d.get("model_routing_plan", {})
    lines.append(f"- tier: {mrp.get('tier')} — {mrp.get('reason')}")
    lines.append(f"  - (plan only; no model is called in v0)")
    lines.append("")
    lines.append("## Human decisions needed")
    if d.get("stop_reason") == "human_review_required" or s.get("blockers"):
        for b in s.get("blockers", []):
            lines.append(f"- {b}")
        if not s.get("blockers"):
            lines.append("- human review required")
    else:
        lines.append("- (none)")
    return "\n".join(lines)
