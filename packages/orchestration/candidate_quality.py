"""
Local Candidate Quality Evaluation v1 (Steps 1645-1680).

Evidence-based quality scoring of candidate-generation OUTCOMES. After a candidate is generated and
run through trust → verification → materialization → approval → apply → test → proof, this module
scores whether it was actually USEFUL (not merely safe), and aggregates model/route scorecards that
feed FUTURE routing. It is EVALUATION / REPORTING / ROUTING-FEEDBACK ONLY.

Core principle:
  Evidence, not model confidence, determines quality. No score claims success without linked
  proof/test evidence. Candidate quality feeds future routing. No automatic execution.

Hard rules enforced here:
  - NO candidate generation, NO model/provider calls, NO approval/apply/test/PR/git/mutation,
    NO network, NO subprocess, NO provider/cloud SDK.
  - A score may NOT claim success without linked proof/test evidence: ≤ medium when verification is
    missing; not high when the human decision is unknown; not excellent without proof_verified;
    rejected / trust-failed candidates score low. Pending approval is NOT completed. Model
    confidence is NOT truth.
  - Reports carry safe IDs / hashes / counts / statuses / evidence refs only — never raw prompt/
    output/candidate/diff/source/stdout/stderr/secrets/tracebacks/absolute paths.
  - No token/cost invention (unknown stays unknown). Every next_safe_action is catalog + entity backed.

Public API::

    evaluate_candidate_quality(generation_id=None, trust_report_id=None, verification_id=None,
                               intent_id=None, job_id=None, data_dir=None) -> CandidateQualityEvaluation
    build_candidate_scorecards(job_id=None, model=None, route_tier=None, data_dir=None) -> dict
    route_quality_feedback(model_label, route_tier, data_dir=None) -> dict
    load_candidate_quality_evaluations(job_id=None, data_dir=None) -> list[dict]
    get_candidate_quality_evaluation(evaluation_id, data_dir=None) -> dict | None
    candidate_quality_integrity(data_dir=None) -> dict
    export_candidate_quality_json(evaluation) -> dict
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.provider_trust import _scrub_public

# ---------------------------------------------------------------------------
# Vocabularies (Steps 1646 / 1647 / 1650)
# ---------------------------------------------------------------------------


class QualityStopReason:
    OK = "ok"
    NO_EVIDENCE = "no_evidence"
    GENERATION_NOT_FOUND = "generation_not_found"
    JOB_NOT_FOUND = "job_not_found"
    CONTRACT_DENIED = "contract_denied"


class QualitySeverity:
    BLOCKER = "blocker"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class QualityOutcome:
    GENERATED_UNAVAILABLE = "generated_unavailable"
    GENERATED_BLOCKED = "generated_blocked"
    TRUST_REJECTED = "trust_rejected"
    VERIFICATION_REJECTED = "verification_rejected"
    NEEDS_HUMAN_REVIEW = "needs_human_review"
    MATERIALIZATION_FAILED = "materialization_failed"
    PENDING_APPROVAL = "pending_approval"
    HUMAN_REJECTED = "human_rejected"
    APPROVED_PENDING_CONTINUE = "approved_pending_continue"
    APPLIED_PENDING_TESTS = "applied_pending_tests"
    TESTS_FAILED = "tests_failed"
    PROOF_VERIFIED = "proof_verified"
    COMPLETED_SUCCESS = "completed_success"
    COMPLETED_WITH_RISKS = "completed_with_risks"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"


class QualityFindingCode:
    REQUEST_MATCH_UNKNOWN = "request_match_unknown"
    REQUEST_MATCH_LOW = "request_match_low"
    TRUST_REJECTED = "trust_rejected"
    VERIFICATION_REJECTED = "verification_rejected"
    VERIFICATION_NEEDS_REVIEW = "verification_needs_review"
    MATERIALIZATION_FAILED = "materialization_failed"
    PENDING_HUMAN_APPROVAL = "pending_human_approval"
    REJECTED_BY_HUMAN = "rejected_by_human"
    APPLIED_WITHOUT_TEST_EVIDENCE = "applied_without_test_evidence"
    TESTS_FAILED = "tests_failed"
    PROOF_MISSING = "proof_missing"
    PROOF_VERIFIED = "proof_verified"
    CANDIDATE_TOO_BROAD = "candidate_too_broad"
    CANDIDATE_OVERCLAIMED = "candidate_overclaimed"
    REPEATED_FAILED_CANDIDATE = "repeated_failed_candidate"
    ROUTE_LOOP_RISK = "route_loop_risk"
    MODEL_UNAVAILABLE = "model_unavailable"
    MODEL_TIMEOUT = "model_timeout"
    GENERATED_NO_CANDIDATE = "generated_no_candidate"
    SAFE_BUT_NOT_USEFUL = "safe_but_not_useful"
    USEFUL_AND_VERIFIED = "useful_and_verified"


class QualityBand:
    EXCELLENT = "excellent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"


_BAND_VALUE = {
    QualityBand.EXCELLENT: 0.95, QualityBand.HIGH: 0.8, QualityBand.MEDIUM: 0.55,
    QualityBand.LOW: 0.3, QualityBand.VERY_LOW: 0.1,
}
_BAND_ORDER = [QualityBand.VERY_LOW, QualityBand.LOW, QualityBand.MEDIUM,
               QualityBand.HIGH, QualityBand.EXCELLENT]


def _cap(band: str, ceiling: str) -> str:
    """Cap a band at a ceiling (return the lower of the two)."""
    return band if _BAND_ORDER.index(band) <= _BAND_ORDER.index(ceiling) else ceiling


# ---------------------------------------------------------------------------
# Models (Step 1646) — no raw prompt/output/diff/source fields.
# ---------------------------------------------------------------------------


@dataclass
class CandidateQualityFinding:
    code: str
    severity: str
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "severity": self.severity, "summary": self.summary}


@dataclass
class CandidateQualityEvidenceRef:
    kind: str
    ref_id: str
    status: str = "available"

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "ref_id": self.ref_id, "status": self.status}


@dataclass
class CandidateQualityScore:
    value: float = 0.0
    band: str = QualityBand.VERY_LOW
    confidence: str = "low"            # low | medium | high (lowered by unknown evidence)
    dimensions: dict[str, str] = field(default_factory=dict)  # dim -> pass|fail|partial|unknown|n/a

    def to_dict(self) -> dict[str, Any]:
        return {"value": self.value, "band": self.band, "confidence": self.confidence,
                "dimensions": self.dimensions}


@dataclass
class CandidateQualityEvaluation:
    evaluation_id: str
    generation_id: str = ""
    trust_report_id: str = ""
    verification_id: str = ""
    material_id: str = ""
    intent_id: str = ""
    apply_id: str = ""
    test_run_id: str = ""
    proof_id: str = ""
    job_id: str = ""
    request_package_id: str = ""
    failure_artifact_id: str = ""
    self_attempt_id: str = ""
    route_tier: str = ""
    model_label: str = ""
    decision: str = ""                # short headline decision string
    score: CandidateQualityScore = field(default_factory=CandidateQualityScore)
    outcome: str = QualityOutcome.EVIDENCE_INCOMPLETE
    stop_reason: str = QualityStopReason.OK
    findings: list[CandidateQualityFinding] = field(default_factory=list)
    evidence_refs: list[CandidateQualityEvidenceRef] = field(default_factory=list)
    evidence_fingerprint: str = ""
    next_safe_action: str = ""
    safe_summary: str = ""
    created_at: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scope(job_id: str) -> str:
    return f"job:{job_id}" if job_id else "repository"


# ---------------------------------------------------------------------------
# Step 1648 — evidence inputs (safe summaries only; unknown stays unknown)
# ---------------------------------------------------------------------------


def _gather_evidence(
    *, generation_id: str, trust_report_id: str, verification_id: str, intent_id: str,
    job_id: str, data_dir: Path,
) -> dict[str, Any]:
    """Collect SAFE durable facts for one candidate. Reads summaries only; unknown stays unknown."""
    ev: dict[str, Any] = {
        "run": None, "trust": None, "verification": None, "material": None,
        "intent_state": "unknown", "proof_status": "unknown", "apply_state": "unknown",
        "test_state": "unknown", "route_tier": "", "model_label": "",
        "repeated_failures": 0,
    }

    # Local candidate run manifest (the headline pipeline outcome + linkage).
    try:
        from packages.orchestration.local_candidate_generator import list_local_candidate_runs
        runs = list_local_candidate_runs(data_dir)
        run = None
        if generation_id:
            run = next((r for r in runs if r.get("generation_id") == generation_id), None)
        if run is None and intent_id:
            run = next((r for r in runs if r.get("intent_id") == intent_id), None)
        if run is None and trust_report_id:
            run = next((r for r in runs if r.get("trust_report_id") == trust_report_id), None)
        if run is None and verification_id:
            run = next((r for r in runs if r.get("verification_id") == verification_id), None)
        ev["run"] = run
        if run:
            ev["model_label"] = run.get("model_name", "")
            trust_report_id = trust_report_id or run.get("trust_report_id", "")
            verification_id = verification_id or run.get("verification_id", "")
            intent_id = intent_id or run.get("intent_id", "")
            job_id = job_id or run.get("job_id", "")
            # repeated failed candidates for this request/model
            rpid = run.get("request_package_id", "")
            ev["repeated_failures"] = sum(
                1 for r in runs if r.get("request_package_id") == rpid
                and r.get("status") in ("trust_rejected", "verification_rejected",
                                        "materialization_failed", "unavailable"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass
    ev["_ids"] = {"trust_report_id": trust_report_id, "verification_id": verification_id,
                  "intent_id": intent_id, "job_id": job_id}

    if not job_id:
        return ev

    # Job-scoped reports.
    try:
        from packages.orchestration.storage import JobNotFoundError, load_job
        job = load_job(UUID(job_id), data_dir)
    except (ValueError, JobNotFoundError, OSError, TypeError):
        return ev

    try:
        from packages.orchestration.provider_trust import get_trust_report
        ev["trust"] = get_trust_report(job, trust_report_id) if trust_report_id else None
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass
    try:
        from packages.orchestration.provider_trust_verification import get_verification_report
        ev["verification"] = get_verification_report(job, verification_id) if verification_id else None
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass

    # Builder routing tier (latest for this job).
    try:
        from packages.orchestration.builder_routing import load_builder_routing_traces
        traces = load_builder_routing_traces(scope=_scope(job_id), data_dir=data_dir)
        if traces:
            ev["route_tier"] = traces[-1].get("selected_tier", "")
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass

    # Intent approval state + proof chain (authoritative apply/test/proof).
    if intent_id:
        try:
            from packages.orchestration.approval_queue import get_patch_intent
            rec = get_patch_intent(job, intent_id)
            if rec is not None:
                ev["intent_state"] = rec.get("state", "unknown")
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass
        try:
            from packages.orchestration.proof_chain import build_proof_chain
            from packages.orchestration.repair_loop import _load_events_safe
            chain = build_proof_chain(job, _load_events_safe(data_dir, job_id), data_dir=data_dir)
            ch = next((c for c in chain.changes
                       if c.intent_id == intent_id or c.patch_intent_id == intent_id), None)
            if ch is not None:
                ev["proof_status"] = ch.proof_status
                ev["apply_state"] = ch.apply_state
                ev["test_state"] = ch.test_state
                if ev["intent_state"] == "unknown":
                    ev["intent_state"] = ch.approval_state
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass
    return ev


# ---------------------------------------------------------------------------
# Steps 1649 / 1650 — scoring + outcome classification
# ---------------------------------------------------------------------------


def _finding(code: str, severity: str, summary: str) -> CandidateQualityFinding:
    return CandidateQualityFinding(code=code, severity=severity, summary=_scrub_public(summary)[:200])


def _classify(ev: dict[str, Any]) -> tuple[str, CandidateQualityScore, list[CandidateQualityFinding]]:
    """Return (outcome, score, findings). Evidence-driven; success requires proof."""
    findings: list[CandidateQualityFinding] = []
    dims: dict[str, str] = {
        "request_adherence": "unknown", "safety_trust": "unknown", "verification_quality": "unknown",
        "materialization_quality": "unknown", "human_decision": "unknown", "apply_outcome": "unknown",
        "test_outcome": "unknown", "proof_outcome": "unknown", "scope_minimality": "unknown",
        "loop_risk": "unknown", "cost_efficiency": "unknown",  # cost never invented → unknown
    }
    run = ev.get("run") or {}
    run_status = run.get("status", "")
    trust = ev.get("trust") or {}
    verification = ev.get("verification") or {}
    intent_state = ev.get("intent_state", "unknown")
    proof_status = ev.get("proof_status", "unknown")
    test_state = ev.get("test_state", "unknown")
    apply_state = ev.get("apply_state", "unknown")

    # Repeated-failure / loop-risk findings (informational; lower confidence).
    if ev.get("repeated_failures", 0) >= 2:
        findings.append(_finding(QualityFindingCode.REPEATED_FAILED_CANDIDATE, QualitySeverity.MEDIUM,
                                 "Repeated failed candidates for this request."))
        dims["loop_risk"] = "fail"

    # --- Stage gates (earliest failing stage wins) ---
    if run_status == "unavailable":
        findings.append(_finding(QualityFindingCode.MODEL_UNAVAILABLE, QualitySeverity.HIGH,
                                 "Local model unavailable / no candidate produced."))
        return QualityOutcome.GENERATED_UNAVAILABLE, _score(QualityBand.VERY_LOW, dims), findings
    if run_status == "blocked":
        return QualityOutcome.GENERATED_BLOCKED, _score(QualityBand.VERY_LOW, dims), findings

    # Trust.
    trust_status = trust.get("trust_status", "") if trust else ""
    if trust_status == "rejected" or run_status == "trust_rejected":
        dims["safety_trust"] = "fail"
        findings.append(_finding(QualityFindingCode.TRUST_REJECTED, QualitySeverity.HIGH,
                                 "Candidate rejected by the Trust Gate."))
        return QualityOutcome.TRUST_REJECTED, _score(QualityBand.LOW, dims), findings
    if trust_status == "accepted":
        dims["safety_trust"] = "pass"

    # Verification.
    vdec = verification.get("decision", "") if verification else ""
    if vdec == "verification_rejected" or run_status == "verification_rejected":
        dims["verification_quality"] = "fail"
        findings.append(_finding(QualityFindingCode.VERIFICATION_REJECTED, QualitySeverity.HIGH,
                                 "Candidate rejected by Verification."))
        return QualityOutcome.VERIFICATION_REJECTED, _score(QualityBand.LOW, dims), findings
    if vdec == "needs_human_review" or run_status == "needs_review":
        dims["verification_quality"] = "partial"
        findings.append(_finding(QualityFindingCode.VERIFICATION_NEEDS_REVIEW, QualitySeverity.MEDIUM,
                                 "Candidate needs human review after verification."))
        return QualityOutcome.NEEDS_HUMAN_REVIEW, _score(QualityBand.MEDIUM, dims), findings
    if vdec == "verification_passed":
        dims["verification_quality"] = "pass"
        dims["request_adherence"] = "pass"      # verification checks request relevance
    else:
        # No verification evidence → cannot exceed medium.
        findings.append(_finding(QualityFindingCode.REQUEST_MATCH_UNKNOWN, QualitySeverity.LOW,
                                 "No verification evidence; request match unknown."))

    if run_status == "materialization_failed":
        dims["materialization_quality"] = "fail"
        findings.append(_finding(QualityFindingCode.MATERIALIZATION_FAILED, QualitySeverity.MEDIUM,
                                 "Verified candidate could not be materialized."))
        return QualityOutcome.MATERIALIZATION_FAILED, _score(QualityBand.LOW, dims), findings

    intent_id = (ev.get("_ids") or {}).get("intent_id", "")
    if not intent_id:
        return QualityOutcome.EVIDENCE_INCOMPLETE, _score(QualityBand.MEDIUM, dims, conf="low"), findings
    dims["materialization_quality"] = "pass"

    # Human decision.
    if intent_state == "rejected":
        dims["human_decision"] = "fail"
        findings.append(_finding(QualityFindingCode.REJECTED_BY_HUMAN, QualitySeverity.HIGH,
                                 "Pending intent was rejected by a human."))
        return QualityOutcome.HUMAN_REJECTED, _score(QualityBand.LOW, dims), findings
    if intent_state in ("pending", "unknown"):
        findings.append(_finding(QualityFindingCode.PENDING_HUMAN_APPROVAL, QualitySeverity.INFO,
                                 "Pending human approval — not yet applied (not complete)."))
        return QualityOutcome.PENDING_APPROVAL, _score(QualityBand.MEDIUM, dims, conf="low"), findings
    if intent_state == "approved":
        dims["human_decision"] = "pass"

    # Apply / test / proof.
    if proof_status == "verified":
        dims["apply_outcome"] = "pass"
        dims["proof_outcome"] = "pass"
        dims["test_outcome"] = "pass" if test_state in ("passed", "not_required") else dims["test_outcome"]
        findings.append(_finding(QualityFindingCode.PROOF_VERIFIED, QualitySeverity.INFO,
                                 "Apply + linked test + proof verified."))
        findings.append(_finding(QualityFindingCode.USEFUL_AND_VERIFIED, QualitySeverity.INFO,
                                 "Candidate is useful and proof-verified."))
        band = QualityBand.EXCELLENT if test_state == "passed" else QualityBand.HIGH
        return QualityOutcome.COMPLETED_SUCCESS, _score(band, dims, conf="high"), findings
    if test_state == "failed":
        dims["apply_outcome"] = "pass"
        dims["test_outcome"] = "fail"
        findings.append(_finding(QualityFindingCode.TESTS_FAILED, QualitySeverity.HIGH,
                                 "Applied candidate's linked test failed."))
        return QualityOutcome.TESTS_FAILED, _score(QualityBand.LOW, dims), findings
    if apply_state == "applied":
        dims["apply_outcome"] = "pass"
        findings.append(_finding(QualityFindingCode.APPLIED_WITHOUT_TEST_EVIDENCE, QualitySeverity.MEDIUM,
                                 "Applied but no passing test/proof evidence yet."))
        findings.append(_finding(QualityFindingCode.PROOF_MISSING, QualitySeverity.MEDIUM,
                                 "Proof not yet verified."))
        return QualityOutcome.APPLIED_PENDING_TESTS, _score(QualityBand.MEDIUM, dims, conf="low"), findings
    # Approved but not yet continued/applied.
    findings.append(_finding(QualityFindingCode.SAFE_BUT_NOT_USEFUL, QualitySeverity.LOW,
                             "Approved but not yet applied — usefulness unproven."))
    return QualityOutcome.APPROVED_PENDING_CONTINUE, _score(QualityBand.MEDIUM, dims, conf="low"), findings


def _score(band: str, dims: dict[str, str], conf: str = "medium") -> CandidateQualityScore:
    """Build a score with the no-success-without-proof invariants enforced as ceilings."""
    # Invariant ceilings.
    if dims.get("verification_quality") not in ("pass",):
        band = _cap(band, QualityBand.MEDIUM)            # ≤ medium without verification
    if dims.get("human_decision") == "unknown":
        band = _cap(band, QualityBand.MEDIUM)            # not high without a known human decision
    if dims.get("proof_outcome") != "pass":
        band = _cap(band, QualityBand.HIGH)              # not excellent without proof_verified
    # Confidence lowered by unknowns.
    unknowns = sum(1 for v in dims.values() if v == "unknown")
    if unknowns >= 5:
        conf = "low"
    return CandidateQualityScore(value=_BAND_VALUE[band], band=band, confidence=conf, dimensions=dims)


# ---------------------------------------------------------------------------
# Persistence + idempotency (Step 1651)
# ---------------------------------------------------------------------------

_EVAL_DIRNAME = "candidate_quality"


def _eval_root(data_dir: Path, job_id: str) -> Path:
    if job_id:
        return data_dir / "workspaces" / job_id / _EVAL_DIRNAME
    return data_dir / "workspaces" / "orchestrator" / _EVAL_DIRNAME


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> None:
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
    except OSError:
        pass


def export_candidate_quality_json(e: CandidateQualityEvaluation) -> dict[str, Any]:
    return {
        "version": 1, "evaluation_id": e.evaluation_id, "generation_id": e.generation_id,
        "trust_report_id": e.trust_report_id, "verification_id": e.verification_id,
        "material_id": e.material_id, "intent_id": e.intent_id, "apply_id": e.apply_id,
        "test_run_id": e.test_run_id, "proof_id": e.proof_id, "job_id": e.job_id,
        "request_package_id": e.request_package_id, "failure_artifact_id": e.failure_artifact_id,
        "self_attempt_id": e.self_attempt_id, "route_tier": e.route_tier,
        "model_label": e.model_label, "decision": e.decision, "score": e.score.to_dict(),
        "outcome": e.outcome, "stop_reason": e.stop_reason,
        "findings": [f.to_dict() for f in e.findings],
        "evidence_refs": [r.to_dict() for r in e.evidence_refs],
        "evidence_fingerprint": e.evidence_fingerprint, "next_safe_action": e.next_safe_action,
        "safe_summary": e.safe_summary, "created_at": e.created_at,
    }


def _fingerprint(ev: dict[str, Any], ids: dict[str, str]) -> str:
    run = ev.get("run") or {}
    parts = [
        ids.get("trust_report_id", ""), ids.get("verification_id", ""), ids.get("intent_id", ""),
        run.get("generation_id", ""), run.get("status", ""),
        str(ev.get("intent_state", "")), str(ev.get("proof_status", "")),
        str(ev.get("test_state", "")), str(ev.get("apply_state", "")),
    ]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


def load_candidate_quality_evaluations(job_id: str | None = None, data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    roots = []
    if job_id:
        roots.append(_eval_root(ddir, job_id))
    else:
        ws = ddir / "workspaces"
        try:
            for child in ws.iterdir():
                roots.append(child / _EVAL_DIRNAME)
        except OSError:
            pass
    out: list[dict] = []
    for root in roots:
        try:
            for child in sorted(root.iterdir()):
                f = child / "evaluation.json"
                if f.is_file():
                    try:
                        out.append(json.loads(f.read_text(encoding="utf-8")))
                    except (OSError, ValueError):
                        continue
        except OSError:
            continue
    out.sort(key=lambda r: r.get("created_at", ""))
    return out


def get_candidate_quality_evaluation(evaluation_id: str, data_dir: Path | None = None) -> dict | None:
    for e in load_candidate_quality_evaluations(data_dir=data_dir):
        if e.get("evaluation_id") == evaluation_id:
            return e
    return None


def _find_existing(job_id: str, fingerprint: str, data_dir: Path) -> dict | None:
    for e in load_candidate_quality_evaluations(job_id=job_id or None, data_dir=data_dir):
        if e.get("evidence_fingerprint") == fingerprint:
            return e
    return None


# ---------------------------------------------------------------------------
# Top-level evaluation
# ---------------------------------------------------------------------------


def _next_action(e: CandidateQualityEvaluation) -> str:
    if e.outcome == QualityOutcome.PENDING_APPROVAL and e.intent_id:
        return f"remedy patch approve {e.job_id} {e.intent_id} --json"
    if e.outcome == QualityOutcome.APPROVED_PENDING_CONTINUE and e.intent_id:
        return f"remedy do continue {e.job_id} --intent-id {e.intent_id} --json"
    if e.outcome in (QualityOutcome.NEEDS_HUMAN_REVIEW, QualityOutcome.VERIFICATION_REJECTED) and e.verification_id:
        return f"remedy provider verification-show {e.job_id} {e.verification_id} --json"
    if e.outcome == QualityOutcome.TRUST_REJECTED and e.trust_report_id:
        return f"remedy provider trust-show {e.job_id} {e.trust_report_id} --json"
    return f"remedy candidate-quality show {e.evaluation_id} --json"


def evaluate_candidate_quality(
    generation_id: str | None = None, trust_report_id: str | None = None,
    verification_id: str | None = None, intent_id: str | None = None,
    job_id: str | None = None, data_dir: Path | None = None, new: bool = False,
    model_label: str | None = None, route_tier: str | None = None,
) -> CandidateQualityEvaluation:
    """Evaluate one candidate's outcome from durable evidence. Read-only inputs; writes a SAFE
    evaluation report. Never generates/approves/applies/tests.

    ``model_label`` / ``route_tier`` override the source/route labels when there is no local
    generation run manifest (e.g. an EXTERNAL builder submission) so scorecards can aggregate by
    external source/route. They NEVER affect scoring — only the safe labels."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    ev = _gather_evidence(
        generation_id=generation_id or "", trust_report_id=trust_report_id or "",
        verification_id=verification_id or "", intent_id=intent_id or "",
        job_id=job_id or "", data_dir=ddir)
    ids = ev.get("_ids", {})
    eid = uuid4().hex[:16]

    if ev.get("run") is None and not (ids.get("trust_report_id") or ids.get("intent_id")):
        e = CandidateQualityEvaluation(evaluation_id=eid, generation_id=generation_id or "",
                                       created_at=_now(), stop_reason=QualityStopReason.NO_EVIDENCE,
                                       outcome=QualityOutcome.EVIDENCE_INCOMPLETE)
        e.next_safe_action = "remedy local-candidate status --json"
        e.safe_summary = "No candidate evidence found to evaluate."
        return e

    fp = _fingerprint(ev, ids)
    if not new:
        existing = _find_existing(ids.get("job_id", ""), fp, ddir)
        if existing is not None:
            return _from_dict(existing)

    outcome, score, findings = _classify(ev)
    run = ev.get("run") or {}
    e = CandidateQualityEvaluation(
        evaluation_id=eid, generation_id=run.get("generation_id", generation_id or ""),
        trust_report_id=ids.get("trust_report_id", ""), verification_id=ids.get("verification_id", ""),
        material_id=run.get("material_id", ""), intent_id=ids.get("intent_id", ""),
        job_id=ids.get("job_id", ""), request_package_id=run.get("request_package_id", ""),
        failure_artifact_id=run.get("failure_artifact_id", ""),
        self_attempt_id=run.get("self_attempt_id", ""),
        route_tier=(ev.get("route_tier", "") or route_tier or "local_candidate_generator"),
        model_label=(ev.get("model_label", "") or model_label or ""),
        outcome=outcome, score=score, findings=findings,
        evidence_fingerprint=fp, created_at=_now())
    # Evidence refs (safe IDs only).
    for kind, rid in (("generation", e.generation_id), ("trust_report", e.trust_report_id),
                      ("verification", e.verification_id), ("material", e.material_id),
                      ("intent", e.intent_id)):
        if rid:
            e.evidence_refs.append(CandidateQualityEvidenceRef(kind, rid))
    e.decision = outcome
    e.next_safe_action = _next_action(e)
    e.safe_summary = (f"outcome={outcome}; score={score.band}({score.value}); "
                      f"conf={score.confidence}; {len(findings)} finding(s).")
    # Persist (idempotent file per evaluation).
    _atomic_write(_eval_root(ddir, e.job_id) / e.evaluation_id / "evaluation.json",
                  json.dumps(export_candidate_quality_json(e), indent=2).encode("utf-8"))
    return e


def _from_dict(d: dict) -> CandidateQualityEvaluation:
    e = CandidateQualityEvaluation(
        evaluation_id=str(d.get("evaluation_id", "")), generation_id=str(d.get("generation_id", "")),
        trust_report_id=str(d.get("trust_report_id", "")), verification_id=str(d.get("verification_id", "")),
        material_id=str(d.get("material_id", "")), intent_id=str(d.get("intent_id", "")),
        apply_id=str(d.get("apply_id", "")), test_run_id=str(d.get("test_run_id", "")),
        proof_id=str(d.get("proof_id", "")), job_id=str(d.get("job_id", "")),
        request_package_id=str(d.get("request_package_id", "")),
        failure_artifact_id=str(d.get("failure_artifact_id", "")),
        self_attempt_id=str(d.get("self_attempt_id", "")), route_tier=str(d.get("route_tier", "")),
        model_label=str(d.get("model_label", "")), decision=str(d.get("decision", "")),
        outcome=str(d.get("outcome", QualityOutcome.EVIDENCE_INCOMPLETE)),
        stop_reason=str(d.get("stop_reason", QualityStopReason.OK)),
        evidence_fingerprint=str(d.get("evidence_fingerprint", "")),
        next_safe_action=str(d.get("next_safe_action", "")), safe_summary=str(d.get("safe_summary", "")),
        created_at=str(d.get("created_at", "")))
    sc = d.get("score", {}) or {}
    e.score = CandidateQualityScore(float(sc.get("value", 0.0)), str(sc.get("band", QualityBand.VERY_LOW)),
                                    str(sc.get("confidence", "low")), dict(sc.get("dimensions", {})))
    e.findings = [CandidateQualityFinding(f.get("code", ""), f.get("severity", ""), f.get("summary", ""))
                  for f in d.get("findings", []) if isinstance(f, dict)]
    e.evidence_refs = [CandidateQualityEvidenceRef(r.get("kind", ""), r.get("ref_id", ""), r.get("status", ""))
                       for r in d.get("evidence_refs", []) if isinstance(r, dict)]
    return e


# ---------------------------------------------------------------------------
# Step 1652 — model / route scorecards
# ---------------------------------------------------------------------------

_SUCCESS_OUTCOMES = (QualityOutcome.PROOF_VERIFIED, QualityOutcome.COMPLETED_SUCCESS)


def build_candidate_scorecards(
    job_id: str | None = None, model: str | None = None, route_tier: str | None = None,
    data_dir: Path | None = None,
) -> dict[str, Any]:
    """Aggregate safe scorecards by model and route from persisted evaluations. No raw content."""
    evals = load_candidate_quality_evaluations(job_id=job_id, data_dir=data_dir)
    if model:
        evals = [e for e in evals if e.get("model_label") == model]
    if route_tier:
        evals = [e for e in evals if e.get("route_tier") == route_tier]

    def _bucket(key: str) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for e in evals:
            k = e.get(key, "") or "unknown"
            b = out.setdefault(k, {"run_count": 0, "trust_pass": 0, "verification_pass": 0,
                                   "materialized": 0, "approved": 0, "apply_success": 0,
                                   "proof_verified": 0, "rejected": 0, "score_sum": 0.0,
                                   "unknown_cost_count": 0, "loop_risk": 0})
            b["run_count"] += 1
            outcome = e.get("outcome", "")
            dims = (e.get("score", {}) or {}).get("dimensions", {})
            if dims.get("safety_trust") == "pass":
                b["trust_pass"] += 1
            if dims.get("verification_quality") == "pass":
                b["verification_pass"] += 1
            if dims.get("materialization_quality") == "pass":
                b["materialized"] += 1
            if dims.get("human_decision") == "pass":
                b["approved"] += 1
            if dims.get("apply_outcome") == "pass":
                b["apply_success"] += 1
            if outcome in _SUCCESS_OUTCOMES or dims.get("proof_outcome") == "pass":
                b["proof_verified"] += 1
            if outcome in (QualityOutcome.TRUST_REJECTED, QualityOutcome.VERIFICATION_REJECTED,
                           QualityOutcome.HUMAN_REJECTED):
                b["rejected"] += 1
            if dims.get("loop_risk") == "fail":
                b["loop_risk"] += 1
            b["unknown_cost_count"] += 1  # cost is always unknown in v1
            b["score_sum"] += float((e.get("score", {}) or {}).get("value", 0.0))
        # finalize rates
        for b in out.values():
            n = max(1, b["run_count"])
            b["trust_pass_rate"] = round(b.pop("trust_pass") / n, 2)
            b["verification_pass_rate"] = round(b.pop("verification_pass") / n, 2)
            b["materialization_rate"] = round(b.pop("materialized") / n, 2)
            b["approval_rate"] = round(b.pop("approved") / n, 2)
            b["apply_success_rate"] = round(b.pop("apply_success") / n, 2)
            b["proof_verified_rate"] = round(b.pop("proof_verified") / n, 2)
            b["rejection_rate"] = round(b.pop("rejected") / n, 2)
            b["average_score"] = round(b.pop("score_sum") / n, 2)
        return out

    return {
        "evaluation_count": len(evals),
        "by_model": _bucket("model_label"),
        "by_route_tier": _bucket("route_tier"),
        "filter": {"job_id": job_id or "", "model": model or "", "route_tier": route_tier or ""},
    }


# ---------------------------------------------------------------------------
# Step 1653 — routing feedback (read-only signal; NEVER triggers generation)
# ---------------------------------------------------------------------------


def route_quality_feedback(
    model_label: str = "", route_tier: str = "local_candidate_generator",
    data_dir: Path | None = None,
) -> dict[str, Any]:
    """Return a SAFE confidence signal for Builder Routing from durable scorecards. Read-only.
    NEVER triggers generation; only advises confidence up/down/neutral."""
    cards = build_candidate_scorecards(model=model_label or None, route_tier=route_tier,
                                       data_dir=data_dir)
    bucket = (cards.get("by_route_tier", {}) or {}).get(route_tier, {})
    if model_label:
        bucket = (cards.get("by_model", {}) or {}).get(model_label, bucket)
    n = bucket.get("run_count", 0)
    if not n:
        return {"confidence": "unknown", "recommend": "neutral", "run_count": 0,
                "reason": "no quality evidence yet"}
    proof_rate = bucket.get("proof_verified_rate", 0.0)
    reject_rate = bucket.get("rejection_rate", 0.0)
    loop = bucket.get("loop_risk", 0)
    if reject_rate >= 0.5 or loop >= 2:
        rec = "lower"          # repeated poor quality → lower local candidate confidence
    elif proof_rate >= 0.5:
        rec = "raise"          # proof-verified successes → raise confidence for this route/model
    else:
        rec = "neutral"
    return {"confidence": bucket.get("average_score", 0.0), "recommend": rec, "run_count": n,
            "proof_verified_rate": proof_rate, "rejection_rate": reject_rate, "loop_risk": loop,
            "reason": "evidence-based; unknown quality never promotes an expensive builder"}


# ---------------------------------------------------------------------------
# Step 1679 — lightweight quality integrity check
# ---------------------------------------------------------------------------


def candidate_quality_integrity(data_dir: Path | None = None) -> dict[str, Any]:
    """Read-only invariant check over persisted evaluations. No mutation."""
    evals = load_candidate_quality_evaluations(data_dir=data_dir)
    violations: list[dict] = []
    seen_fp: dict[str, str] = {}
    for e in evals:
        outcome = e.get("outcome", "")
        dims = (e.get("score", {}) or {}).get("dimensions", {})
        band = (e.get("score", {}) or {}).get("band", "")
        # No proof_verified outcome without proof dimension.
        if outcome in _SUCCESS_OUTCOMES and dims.get("proof_outcome") != "pass":
            violations.append({"evaluation_id": e.get("evaluation_id"), "code": "success_without_proof"})
        # No high/excellent for rejected candidate.
        if outcome in (QualityOutcome.TRUST_REJECTED, QualityOutcome.VERIFICATION_REJECTED,
                       QualityOutcome.HUMAN_REJECTED) and band in (QualityBand.HIGH, QualityBand.EXCELLENT):
            violations.append({"evaluation_id": e.get("evaluation_id"), "code": "high_score_for_rejected"})
        # No duplicate active evaluation per evidence fingerprint.
        fp = e.get("evidence_fingerprint", "")
        if fp and fp in seen_fp:
            violations.append({"evaluation_id": e.get("evaluation_id"), "code": "duplicate_fingerprint"})
        elif fp:
            seen_fp[fp] = e.get("evaluation_id", "")
    return {"version": 1, "evaluation_count": len(evals), "violation_count": len(violations),
            "passed": not violations, "violations": violations[:50]}
