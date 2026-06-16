"""
Model/Route Tournament Harness v0 (Steps 1797-1836).

An EVIDENCE-BASED comparison layer for Remedy's worker routes. It helps Remedy learn which worker/
route is best for which kind of task by comparing durable evidence — Candidate Quality, Token
Economy, Worker Registry metadata, route policy, trust/verification outcomes, approval states,
proof/test state, and safe submission history.

  Workers execute. Remedy governs. Tournament compares and recommends — it does not run workers.

This module is METADATA + SCORING + REPORTING only. It NEVER calls a provider/model/Ollama/cloud/
local service, the network, a browser, a subprocess, or a shell; it never executes a worker, runs a
tournament, generates a candidate, calls the external builder, or applies/approves/tests anything.
No self-claim becomes truth; unknown evidence stays unknown; insufficient evidence yields NO winner;
a cheaper token cost can never override failed trust/verification.

Hard rules enforced here:
  - NO provider/model/Ollama/cloud/local execution, network, browser, subprocess, shell.
  - NO candidate generation, external-builder auto-call, apply/approve/test/git/PR, MemPalace, real
    pricing sync.
  - Evidence absence is `insufficient_evidence`, never failure.
  - Scoring hard ceilings: no proof/test → not excellent; rejected/unverified → blocked/weak;
    unknown → insufficient_evidence or usable-at-most; high-risk without approval → blocked; unknown
    context/budget → approval required; placeholder executable claim → blocked; cheaper cost cannot
    override failed trust/verification.
  - No winner without sufficient evidence.
  - No raw prompts/candidates/diffs/logs/secrets/absolute paths in any public export.

Public API::

    build_tournament_spec(job_id, *, task_id, task_type, data_dir=None) -> TournamentSpec
    list_tournament_competitors(job_id, *, task_id, task_type, data_dir=None) -> list[TournamentCompetitor]
    generate_tournament_report(job_id, *, task_id, task_type, data_dir=None, persist=True) -> TournamentReport
    save_tournament_report(report, data_dir=None) -> bool
    load_tournament_report(tournament_id, data_dir=None) -> dict | None
    list_tournament_reports(job_id=None, data_dir=None) -> list[dict]
    routing_tournament_hint(job_id, *, task_type, data_dir=None) -> dict
    tournament_integrity(data_dir=None) -> dict
    export_*_json(...) -> dict
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.provider_trust import _safe_path_label, _scrub_public

# ---------------------------------------------------------------------------
# Constants / vocabularies
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "model-route-tournament-v0"
_MRT_DIRNAME = "model_route_tournament"

_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-ant", "sk-proj",
                "api_key", "password", "secret_key")


class ScoreBand:
    EXCELLENT = "excellent"
    STRONG = "strong"
    USABLE = "usable"
    WEAK = "weak"
    BLOCKED = "blocked"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


_BAND_RANK = {
    ScoreBand.EXCELLENT: 5, ScoreBand.STRONG: 4, ScoreBand.USABLE: 3,
    ScoreBand.WEAK: 2, ScoreBand.INSUFFICIENT_EVIDENCE: 1, ScoreBand.BLOCKED: 0,
}
# Bands that may win a tournament (need real, positive evidence).
_WINNER_BANDS = frozenset({ScoreBand.EXCELLENT, ScoreBand.STRONG})


class TournamentStatus:
    COMPLETE = "complete"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    NO_COMPETITORS = "no_competitors"


class EvidenceStatus:
    COMPLETE = "complete"
    PARTIAL = "partial"
    INSUFFICIENT = "insufficient_evidence"


# Worker kind → Candidate Quality route_tier (only these kinds have quality evidence).
_ROUTE_TIER_BY_KIND = {
    "local_candidate": "local_candidate_generator",
    "ollama_candidate": "local_candidate_generator",
    "external_builder": "external_candidate_generator",
    "cloud_candidate": "external_candidate_generator",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Models (Step 1799)
# ---------------------------------------------------------------------------


@dataclass
class TournamentSpec:
    tournament_id: str = ""
    job_id: str = ""
    task_id: str = ""
    task_type: str = ""
    candidate_route_ids: list[str] = field(default_factory=list)
    worker_ids: list[str] = field(default_factory=list)
    policy_id: str = ""
    created_at: str = ""
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "tournament_id": self.tournament_id, "job_id": self.job_id, "task_id": self.task_id,
            "task_type": self.task_type, "candidate_route_ids": list(self.candidate_route_ids),
            "worker_ids": list(self.worker_ids), "policy_id": self.policy_id,
            "created_at": self.created_at, "schema_version": self.schema_version,
        }


@dataclass
class TournamentCompetitor:
    competitor_id: str = ""
    route_id: str = ""
    worker_id: str = ""
    worker_kind: str = ""
    enabled: bool = False
    eligible: bool = False
    blocked_reason: str = ""
    cost_tier: str = "unknown"
    risk_tier: str = "unknown"
    supports_external_package: bool = False
    supports_candidate_quality: bool = False
    token_band: str = "unknown"
    context_fit: str = "unknown"
    approval_required: bool = True
    is_placeholder: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "competitor_id": self.competitor_id, "route_id": self.route_id,
            "worker_id": self.worker_id, "worker_kind": self.worker_kind, "enabled": self.enabled,
            "eligible": self.eligible, "blocked_reason": self.blocked_reason,
            "cost_tier": self.cost_tier, "risk_tier": self.risk_tier,
            "supports_external_package": self.supports_external_package,
            "supports_candidate_quality": self.supports_candidate_quality,
            "token_band": self.token_band, "context_fit": self.context_fit,
            "approval_required": self.approval_required, "is_placeholder": self.is_placeholder,
        }


@dataclass
class TournamentEvidence:
    competitor_id: str = ""
    candidate_quality_summary: dict[str, Any] = field(default_factory=dict)
    token_economy_summary: dict[str, Any] = field(default_factory=dict)
    trust_summary: dict[str, Any] = field(default_factory=dict)
    verification_summary: dict[str, Any] = field(default_factory=dict)
    approval_summary: dict[str, Any] = field(default_factory=dict)
    proof_summary: dict[str, Any] = field(default_factory=dict)
    test_summary: dict[str, Any] = field(default_factory=dict)
    submission_summary: dict[str, Any] = field(default_factory=dict)
    evidence_status: str = EvidenceStatus.INSUFFICIENT

    def to_dict(self) -> dict[str, Any]:
        return {
            "competitor_id": self.competitor_id,
            "candidate_quality_summary": dict(self.candidate_quality_summary),
            "token_economy_summary": dict(self.token_economy_summary),
            "trust_summary": dict(self.trust_summary),
            "verification_summary": dict(self.verification_summary),
            "approval_summary": dict(self.approval_summary),
            "proof_summary": dict(self.proof_summary),
            "test_summary": dict(self.test_summary),
            "submission_summary": dict(self.submission_summary),
            "evidence_status": self.evidence_status,
        }


@dataclass
class TournamentScore:
    competitor_id: str = ""
    score_band: str = ScoreBand.INSUFFICIENT_EVIDENCE
    rank: int = 0
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    risk_notes: list[str] = field(default_factory=list)
    estimated_token_band: str = "unknown"
    approval_required: bool = True
    recommendation: str = ""
    next_safe_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "competitor_id": self.competitor_id, "score_band": self.score_band, "rank": self.rank,
            "strengths": list(self.strengths), "weaknesses": list(self.weaknesses),
            "risk_notes": list(self.risk_notes), "estimated_token_band": self.estimated_token_band,
            "approval_required": self.approval_required, "recommendation": self.recommendation,
            "next_safe_action": self.next_safe_action,
        }


@dataclass
class TournamentReport:
    tournament_id: str = ""
    job_id: str = ""
    task_id: str = ""
    task_type: str = ""
    status: str = TournamentStatus.INSUFFICIENT_EVIDENCE
    competitors: list[TournamentCompetitor] = field(default_factory=list)
    evidence: list[TournamentEvidence] = field(default_factory=list)
    scores: list[TournamentScore] = field(default_factory=list)
    winner_competitor_id: str = ""
    confidence: str = "low"
    warnings: list[str] = field(default_factory=list)
    next_safe_actions: list[str] = field(default_factory=list)
    safe_reason: str = ""
    created_at: str = ""
    content_sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 1, "tournament_id": self.tournament_id, "job_id": self.job_id,
            "task_id": self.task_id, "task_type": self.task_type, "status": self.status,
            "competitors": [c.to_dict() for c in self.competitors],
            "evidence": [e.to_dict() for e in self.evidence],
            "scores": [s.to_dict() for s in self.scores],
            "winner_competitor_id": self.winner_competitor_id, "confidence": self.confidence,
            "warnings": list(self.warnings), "next_safe_actions": list(self.next_safe_actions),
            "safe_reason": self.safe_reason, "created_at": self.created_at,
            "schema_version": SCHEMA_VERSION,
        }


def export_tournament_report_json(r: TournamentReport) -> dict[str, Any]:
    return r.to_dict()


def export_tournament_spec_json(s: TournamentSpec) -> dict[str, Any]:
    return s.to_dict()


# ---------------------------------------------------------------------------
# Competitor discovery (Step 1800)
# ---------------------------------------------------------------------------


def build_tournament_spec(
    job_id: str, *, task_id: str = "", task_type: str = "repair", data_dir: Path | None = None,
) -> TournamentSpec:
    """Build a tournament spec from the Worker Registry + Route Policy. Metadata only."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_registry import load_route_policy, load_worker_registry
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    registry = load_worker_registry(ddir)
    policy = load_route_policy(job_id, ddir) if job_id else None
    return TournamentSpec(
        tournament_id=f"trn-{uuid4().hex[:12]}", job_id=job_id, task_id=task_id, task_type=task_type,
        candidate_route_ids=[s.worker_id for s in registry],
        worker_ids=[s.worker_id for s in registry],
        policy_id=getattr(policy, "policy_id", ""), created_at=_now())


def list_tournament_competitors(
    job_id: str, *, task_id: str = "", task_type: str = "repair", data_dir: Path | None = None,
) -> list[TournamentCompetitor]:
    """Discover competitors (one per registry worker) with eligibility from the route policy. A
    disabled/blocked/missing-capability worker is ineligible; placeholders are eligible for
    comparison/planning only (never execution)."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_registry import (
        WorkerSelectionRequest,
        evaluate_worker_selection,
        hard_safety_requires_approval,
        is_placeholder,
        load_worker_registry,
    )
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    registry = load_worker_registry(ddir)
    selection = evaluate_worker_selection(
        WorkerSelectionRequest(job_id=job_id, task_type=task_type), registry=registry, data_dir=ddir)
    eligible_reason = {c.worker_id: c for c in selection.eligible_candidates}
    rejected_reason = {c.worker_id: c.reason for c in selection.rejected_candidates}

    competitors: list[TournamentCompetitor] = []
    for spec in registry:
        ph = is_placeholder(spec)
        eligible = spec.worker_id in eligible_reason
        competitors.append(TournamentCompetitor(
            competitor_id=f"cmp-{uuid4().hex[:10]}", route_id=spec.worker_id, worker_id=spec.worker_id,
            worker_kind=spec.kind, enabled=spec.enabled, eligible=eligible,
            blocked_reason="" if eligible else rejected_reason.get(spec.worker_id, "ineligible"),
            cost_tier=spec.cost_tier, risk_tier=spec.risk_tier,
            supports_external_package=spec.supports_external_builder_package,
            supports_candidate_quality=spec.supports_candidate_quality,
            approval_required=hard_safety_requires_approval(spec), is_placeholder=ph))
    return competitors


def _competitor_next_action(c: TournamentCompetitor, job_id: str) -> str:
    """Catalog-valid next action per competitor — placeholders → configuration/planning, never exec."""
    jid = job_id or "<job_id>"
    if c.is_placeholder:
        return f"remedy worker registry-show {c.worker_id} --json"
    if c.worker_kind == "external_builder":
        return f"remedy external-builder package-create {jid} --json"
    if c.worker_kind in ("local_candidate",):
        return f"remedy builder-routing report --job-id {jid} --json"
    if c.worker_kind == "human":
        return f"remedy guide next {jid} --json" if job_id else "remedy guide next --json"
    if c.worker_kind == "reviewer":
        return "remedy review list --json"
    return f"remedy tournament report {jid} --json"


# ---------------------------------------------------------------------------
# Evidence gathering (Step 1801)
# ---------------------------------------------------------------------------


def _gather_evidence(
    competitor: TournamentCompetitor, job_id: str, task_type: str, data_dir: Path,
) -> TournamentEvidence:
    """Gather SAFE durable evidence for a competitor. Absence → insufficient_evidence, never failure.
    Never uses raw candidate/prompt/output; reuses existing safe summary APIs only."""
    ev = TournamentEvidence(competitor_id=competitor.competitor_id)
    have_signal = False

    # Candidate Quality (route-tier feedback — read-only, evidence-only ceilings).
    route_tier = _ROUTE_TIER_BY_KIND.get(competitor.worker_kind, "")
    if route_tier:
        try:
            from packages.orchestration.candidate_quality import route_quality_feedback
            fb = route_quality_feedback(model_label="", route_tier=route_tier, data_dir=data_dir)
            ev.candidate_quality_summary = {
                "run_count": fb.get("run_count", 0), "recommend": fb.get("recommend", "neutral"),
                "proof_verified_rate": fb.get("proof_verified_rate", 0.0),
                "rejection_rate": fb.get("rejection_rate", 0.0), "loop_risk": fb.get("loop_risk", 0),
                "confidence": fb.get("confidence", "unknown")}
            ev.proof_summary = {"proof_verified_rate": fb.get("proof_verified_rate", 0.0)}
            ev.verification_summary = {"rejection_rate": fb.get("rejection_rate", 0.0)}
            ev.test_summary = {"loop_risk": fb.get("loop_risk", 0)}
            if fb.get("run_count", 0) > 0:
                have_signal = True
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            ev.candidate_quality_summary = {"run_count": 0, "error": "candidate_quality_unavailable"}

    # Token Economy (shared estimate hint; cost band from competitor metadata).
    try:
        from packages.orchestration.token_economy import routing_token_hint
        h = routing_token_hint(job_id, task_type=task_type, data_dir=data_dir)
        ev.token_economy_summary = {
            "estimated_token_band": h.get("estimated_token_band", "unknown"),
            "budget_status": h.get("budget_status", "unknown_budget"),
            "cost_tier": competitor.cost_tier,
            "requires_human_approval": h.get("requires_human_approval", True)}
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        ev.token_economy_summary = {"estimated_token_band": "unknown"}

    # External builder submission history (external worker only).
    if competitor.worker_kind == "external_builder":
        try:
            from packages.orchestration.external_builder_sandbox import load_external_submissions
            subs = load_external_submissions(job_id=job_id, data_dir=data_dir)
            by_state: dict[str, int] = {}
            for s in subs:
                by_state[s.get("state", "")] = by_state.get(s.get("state", ""), 0) + 1
            ev.submission_summary = {"submission_count": len(subs), "by_state": by_state}
            ev.trust_summary = {"trust_rejected": by_state.get("trust_rejected", 0)}
            ev.approval_summary = {"pending_approval": by_state.get("pending_approval", 0)}
            if subs:
                have_signal = True
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            ev.submission_summary = {"submission_count": 0}

    ev.evidence_status = (EvidenceStatus.COMPLETE if have_signal and route_tier
                          else EvidenceStatus.PARTIAL if have_signal
                          else EvidenceStatus.INSUFFICIENT)
    return ev


# ---------------------------------------------------------------------------
# Scoring (Step 1802) — deterministic; hard safety ceilings.
# ---------------------------------------------------------------------------


def _score_competitor(
    competitor: TournamentCompetitor, evidence: TournamentEvidence, job_id: str,
) -> TournamentScore:
    from packages.orchestration.worker_registry import WorkerRiskTier
    sc = TournamentScore(competitor_id=competitor.competitor_id,
                         approval_required=competitor.approval_required)
    sc.estimated_token_band = evidence.token_economy_summary.get("estimated_token_band", "unknown")
    sc.next_safe_action = _competitor_next_action(competitor, job_id)
    strengths, weaknesses, risks = sc.strengths, sc.weaknesses, sc.risk_notes

    # 1. Ineligible (disabled/blocked/missing capability) → BLOCKED.
    if not competitor.eligible:
        sc.score_band = ScoreBand.BLOCKED
        weaknesses.append(competitor.blocked_reason or "ineligible under route policy")
        sc.recommendation = "Not eligible under the current route policy — excluded from winner."
        return sc

    # 2. High/unknown risk that somehow is not approval-gated → BLOCKED (defense in depth).
    if competitor.risk_tier in (WorkerRiskTier.HIGH, WorkerRiskTier.BLOCKED, WorkerRiskTier.UNKNOWN) \
            and not competitor.approval_required:
        sc.score_band = ScoreBand.BLOCKED
        risks.append("high/unknown risk without required approval")
        sc.recommendation = "High/unknown-risk route without approval — blocked."
        return sc

    cq = evidence.candidate_quality_summary or {}
    n = int(cq.get("run_count", 0) or 0)
    proof_rate = float(cq.get("proof_verified_rate", 0.0) or 0.0)
    reject_rate = float(cq.get("rejection_rate", 0.0) or 0.0)
    loop_risk = int(cq.get("loop_risk", 0) or 0)
    subs = (evidence.submission_summary or {}).get("submission_count", 0)

    # 3. Insufficient evidence → INSUFFICIENT_EVIDENCE (never a fake high score).
    if n == 0 and not subs:
        sc.score_band = ScoreBand.INSUFFICIENT_EVIDENCE
        weaknesses.append("no candidate-quality or submission evidence yet")
        if competitor.is_placeholder:
            risks.append("placeholder route — comparison/planning only, not executable")
        sc.recommendation = ("Insufficient evidence — run the route's safe next action to gather "
                             "evidence before relying on it.")
        return sc

    # 4. Rejected/unverified dominates → BLOCKED or WEAK (cheaper cost cannot lift this).
    if reject_rate >= 0.5 or loop_risk >= 2:
        sc.score_band = ScoreBand.WEAK if reject_rate < 0.8 else ScoreBand.BLOCKED
        weaknesses.append(f"high rejection rate ({reject_rate}) / loop risk ({loop_risk})")
        risks.append("repeated rejection/verification failure — cost is irrelevant here")
        sc.recommendation = "Poor trust/verification history — avoid for this task type."
        return sc

    # 5. Placeholder cannot be excellent/strong (non-executable) — cap at USABLE for planning.
    if competitor.is_placeholder:
        sc.score_band = ScoreBand.USABLE
        strengths.append("eligible placeholder — useful once configured")
        risks.append("placeholder route — not executable until a real adapter/config exists")
        sc.recommendation = "Configure this route before it can compete for real."
        return sc

    # 6. Positive evidence banding.
    if proof_rate >= 0.5 and reject_rate < 0.25:
        # EXCELLENT only with real proof AND clean rejection AND a known (not unknown) token band.
        if proof_rate >= 0.5 and sc.estimated_token_band != "unknown" and not competitor.approval_required:
            sc.score_band = ScoreBand.EXCELLENT
            strengths.append(f"proof-verified rate {proof_rate}; clean rejection history")
        else:
            sc.score_band = ScoreBand.STRONG
            strengths.append(f"proof-verified rate {proof_rate}")
            if competitor.approval_required:
                risks.append("approval required before use")
    elif proof_rate > 0.0 or (n > 0 and reject_rate < 0.5):
        sc.score_band = ScoreBand.USABLE
        strengths.append("some positive evidence; no strong proof yet")
    else:
        sc.score_band = ScoreBand.WEAK
        weaknesses.append("no proof and weak evidence")

    if competitor.cost_tier in ("free", "cheap"):
        strengths.append(f"estimated {competitor.cost_tier} cost route")
    sc.recommendation = {
        ScoreBand.EXCELLENT: "Strong evidence-backed route — recommended for this task type.",
        ScoreBand.STRONG: "Good evidence-backed route — recommended (approval may apply).",
        ScoreBand.USABLE: "Usable route — limited evidence; verify before relying on it.",
        ScoreBand.WEAK: "Weak route — gather more evidence or prefer another route.",
    }.get(sc.score_band, "See evidence summary.")
    return sc


# ---------------------------------------------------------------------------
# Report generation (Step 1803)
# ---------------------------------------------------------------------------


def generate_tournament_report(
    job_id: str, *, task_id: str = "", task_type: str = "repair", data_dir: Path | None = None,
    persist: bool = True,
) -> TournamentReport:
    """Generate a SAFE, evidence-based tournament report. No execution. No fake winner: a winner is
    set only when the top eligible competitor scores excellent/strong on real evidence."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    spec = build_tournament_spec(job_id, task_id=task_id, task_type=task_type, data_dir=ddir)
    competitors = list_tournament_competitors(job_id, task_id=task_id, task_type=task_type, data_dir=ddir)
    report = TournamentReport(
        tournament_id=spec.tournament_id, job_id=job_id, task_id=task_id, task_type=task_type,
        competitors=competitors, created_at=_now())

    if not competitors:
        report.status = TournamentStatus.NO_COMPETITORS
        report.safe_reason = "No worker competitors in the registry."
        report.next_safe_actions = ["remedy worker registry-list --json"]
        if persist:
            save_tournament_report(report, ddir)
        return report

    evidence = [_gather_evidence(c, job_id, task_type, ddir) for c in competitors]
    scores = [_score_competitor(c, e, job_id) for c, e in zip(competitors, evidence)]
    report.evidence = evidence

    # Rank by band (desc), then by approval not required, then competitor_id for determinism.
    order = sorted(scores, key=lambda s: (-_BAND_RANK.get(s.score_band, 0),
                                          1 if s.approval_required else 0, s.competitor_id))
    for i, s in enumerate(order, start=1):
        s.rank = i
    report.scores = order

    top = order[0] if order else None
    if top is not None and top.score_band in _WINNER_BANDS:
        report.winner_competitor_id = top.competitor_id
        report.status = TournamentStatus.COMPLETE
        report.confidence = "high" if top.score_band == ScoreBand.EXCELLENT else "medium"
        wc = next((c for c in competitors if c.competitor_id == top.competitor_id), None)
        report.safe_reason = (f"Winner: route '{wc.worker_id if wc else top.competitor_id}' scored "
                              f"{top.score_band} on durable evidence (estimate; nothing executed).")
    else:
        report.winner_competitor_id = ""
        report.status = TournamentStatus.INSUFFICIENT_EVIDENCE
        report.confidence = "low"
        report.warnings.append("insufficient_evidence_for_winner")
        report.safe_reason = ("No evidence-backed winner yet — gather more candidate-quality / "
                              "submission evidence before relying on a route.")

    report.next_safe_actions = [
        f"remedy tournament show {report.tournament_id} --json",
        (top.next_safe_action if top else "remedy worker registry-list --json"),
        f"remedy token economy-report {job_id} --json" if job_id else "remedy worker registry-list --json",
    ]
    if persist:
        save_tournament_report(report, ddir)
    return report


# ---------------------------------------------------------------------------
# Storage (Step 1804)
# ---------------------------------------------------------------------------


def _mrt_root(job_id: str, data_dir: Path) -> Path:
    base = job_id if job_id else "orchestrator"
    return data_dir / "workspaces" / base / _MRT_DIRNAME


def _report_path(job_id: str, tournament_id: str, data_dir: Path) -> Path:
    return _mrt_root(job_id, data_dir) / tournament_id / "report.json"


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


def save_tournament_report(report: TournamentReport, data_dir: Path | None = None) -> bool:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    payload = report.to_dict()
    import hashlib
    payload["content_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    payload["scope"] = f"job:{report.job_id}" if report.job_id else "repository"
    return _atomic_write(_report_path(report.job_id, report.tournament_id, ddir),
                         json.dumps(payload, indent=2).encode("utf-8"))


def list_tournament_reports(job_id: str | None = None, data_dir: Path | None = None) -> list[dict]:
    """List persisted tournament reports. Corruption-aware; never raises."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    roots: list[Path] = []
    ws = ddir / "workspaces"
    if job_id:
        roots.append(_mrt_root(job_id, ddir))
    else:
        try:
            for child in ws.iterdir():
                roots.append(child / _MRT_DIRNAME)
        except OSError:
            pass
    out: list[dict] = []
    for root in roots:
        try:
            for child in sorted(root.iterdir()):
                f = child / "report.json"
                if not f.is_file():
                    continue
                try:
                    out.append(json.loads(f.read_text(encoding="utf-8")))
                except (OSError, ValueError):
                    continue
        except OSError:
            continue
    out.sort(key=lambda r: r.get("created_at", ""))
    return out


def load_tournament_report(tournament_id: str, data_dir: Path | None = None) -> dict | None:
    return next((r for r in list_tournament_reports(data_dir=data_dir)
                 if r.get("tournament_id") == tournament_id), None)


# ---------------------------------------------------------------------------
# Builder routing hint (Step 1805)
# ---------------------------------------------------------------------------


def routing_tournament_hint(job_id: str, *, task_type: str = "repair",
                            data_dir: Path | None = None) -> dict[str, Any]:
    """Lean read-only tournament hint for Builder Routing. Never generates a report side-effect that
    executes anything; computes a non-persisted report. No winner when evidence is insufficient."""
    try:
        rep = generate_tournament_report(job_id, task_type=task_type, data_dir=data_dir, persist=False)
        top = rep.scores[0] if rep.scores else None
        winner = next((c for c in rep.competitors if c.competitor_id == rep.winner_competitor_id),
                      None)
        return {
            "tournament_score_band": top.score_band if top else ScoreBand.INSUFFICIENT_EVIDENCE,
            "recommended_competitor": (winner.worker_id if winner else ""),
            "confidence": rep.confidence,
            "tournament_warning": rep.warnings[0] if rep.warnings else "",
            "next_safe_action": f"remedy tournament report {job_id} --json" if job_id
                                else "remedy worker registry-list --json",
            "estimated": True,
        }
    except Exception:
        return {"tournament_score_band": ScoreBand.INSUFFICIENT_EVIDENCE, "recommended_competitor": "",
                "confidence": "low", "tournament_warning": "", "next_safe_action": "", "estimated": True}


# ---------------------------------------------------------------------------
# Integrity (Step 1812)
# ---------------------------------------------------------------------------


def audit_report_safety(report: dict[str, Any]) -> list[dict[str, str]]:
    """Focused invariant helper: flag unsafe tournament report states. Safe public codes only."""
    if not isinstance(report, dict):
        return []
    out: list[dict[str, str]] = []
    tid = report.get("tournament_id", "")
    scores = {s.get("competitor_id"): s for s in report.get("scores", [])}
    competitors = {c.get("competitor_id"): c for c in report.get("competitors", [])}
    winner = report.get("winner_competitor_id", "")
    status = report.get("status", "")

    # Winner cannot exist with insufficient evidence.
    if winner and status == TournamentStatus.INSUFFICIENT_EVIDENCE:
        out.append({"tournament_id": tid, "code": "winner_with_insufficient_evidence"})
    # Winner band must be a real winner band.
    if winner:
        wb = (scores.get(winner) or {}).get("score_band", "")
        if wb not in _WINNER_BANDS:
            out.append({"tournament_id": tid, "code": "winner_not_winner_band"})
    # Per-score ceilings.
    for cid, s in scores.items():
        band = s.get("score_band", "")
        comp = competitors.get(cid, {})
        # Placeholder cannot be excellent/strong (executable claim).
        if comp.get("is_placeholder") and band in _WINNER_BANDS:
            out.append({"tournament_id": tid, "code": "placeholder_ranked_winner"})
        # Ineligible cannot rank above blocked.
        if comp.get("eligible") is False and band != ScoreBand.BLOCKED:
            out.append({"tournament_id": tid, "code": "ineligible_not_blocked"})
        # High/unknown risk without approval cannot be a winner band.
        if comp.get("risk_tier") in ("high", "blocked", "unknown") and not comp.get("approval_required") \
                and band in _WINNER_BANDS:
            out.append({"tournament_id": tid, "code": "high_risk_no_approval_ranked"})
    # No raw/secret/abs-path in public report.
    blob = json.dumps(report).lower()
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"tournament_id": tid, "code": "raw_or_secret_in_public"})
    if "/home/" in blob or "/users/" in blob or "/root/" in blob:
        out.append({"tournament_id": tid, "code": "absolute_path_in_public"})
    return out


def tournament_integrity(data_dir: Path | None = None,
                         reports: list[dict] | None = None) -> dict[str, Any]:
    """Read-only invariant check over persisted (or supplied) tournament reports. Safe codes only."""
    scan = reports if reports is not None else list_tournament_reports(data_dir=data_dir)
    violations: list[dict] = []
    seen_fp: set[str] = set()
    for r in scan:
        violations.extend(audit_report_safety(r))
        fp = r.get("content_sha256", "")
        if fp and fp in seen_fp:
            violations.append({"tournament_id": r.get("tournament_id", ""),
                               "code": "duplicate_report_fingerprint"})
        elif fp:
            seen_fp.add(fp)
    return {"version": 1, "report_count": len(scan), "violation_count": len(violations),
            "passed": not violations, "violations": violations[:50]}


# Keep redaction helpers referenced for parity with the rest of the orchestration package.
_REDACTION_HELPERS = (_scrub_public, _safe_path_label)
