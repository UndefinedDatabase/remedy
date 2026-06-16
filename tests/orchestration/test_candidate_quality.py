"""Unit + integration tests for Local Candidate Quality Evaluation v1 (Steps 1665-1671, 1679).

Evidence, not model confidence, determines quality. No score claims success without linked
proof/test evidence; pending approval is not completed; rejected/unverified candidates score low.
Evaluation/reporting/routing-feedback ONLY — never generates/approves/applies/tests, never calls
models/network/subprocess, never leaks raw prompt/output/secrets/paths.
"""
from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration.candidate_quality import (
    QualityBand,
    QualityOutcome,
    _classify,
    _score,
    candidate_quality_integrity,
    evaluate_candidate_quality,
    export_candidate_quality_json,
    route_quality_feedback,
)


def _ev(**kw):
    base = {
        "run": kw.pop("run", {"status": "", "model_name": "qwen", "request_package_id": "rp1",
                              "generation_id": "g1"}),
        "trust": kw.pop("trust", None), "verification": kw.pop("verification", None),
        "material": None, "intent_state": kw.pop("intent_state", "unknown"),
        "proof_status": kw.pop("proof_status", "unknown"),
        "apply_state": kw.pop("apply_state", "unknown"),
        "test_state": kw.pop("test_state", "unknown"), "route_tier": "local_candidate_generator",
        "model_label": "qwen", "repeated_failures": kw.pop("repeated_failures", 0),
        "_ids": kw.pop("ids", {"intent_id": "i1", "job_id": "J", "trust_report_id": "t1",
                               "verification_id": "v1"}),
    }
    base.update(kw)
    return base


_TRUST_OK = {"trust_status": "accepted"}
_VERIF_OK = {"decision": "verification_passed"}


# ---------------------------------------------------------------------------
# Step 1666 — scoring
# ---------------------------------------------------------------------------


class TestScoring:
    def test_trust_rejected_low(self):
        o, s, _ = _classify(_ev(run={"status": "trust_rejected", "model_name": "m"},
                                 trust={"trust_status": "rejected"}))
        assert o == QualityOutcome.TRUST_REJECTED
        assert s.band == QualityBand.LOW

    def test_verification_rejected_low(self):
        o, s, _ = _classify(_ev(trust=_TRUST_OK, verification={"decision": "verification_rejected"}))
        assert o == QualityOutcome.VERIFICATION_REJECTED
        assert s.band == QualityBand.LOW

    def test_needs_review_medium(self):
        o, s, _ = _classify(_ev(trust=_TRUST_OK, verification={"decision": "needs_human_review"}))
        assert o == QualityOutcome.NEEDS_HUMAN_REVIEW
        assert s.band == QualityBand.MEDIUM

    def test_pending_approval_capped(self):
        o, s, _ = _classify(_ev(trust=_TRUST_OK, verification=_VERIF_OK, intent_state="pending"))
        assert o == QualityOutcome.PENDING_APPROVAL
        assert s.band == QualityBand.MEDIUM     # capped: human decision unknown

    def test_approved_not_continued_not_success(self):
        o, s, _ = _classify(_ev(trust=_TRUST_OK, verification=_VERIF_OK, intent_state="approved",
                                apply_state="not_applied", proof_status="incomplete"))
        assert o == QualityOutcome.APPROVED_PENDING_CONTINUE
        assert s.band != QualityBand.EXCELLENT

    def test_applied_without_tests_incomplete(self):
        o, s, f = _classify(_ev(trust=_TRUST_OK, verification=_VERIF_OK, intent_state="approved",
                                apply_state="applied", test_state="not_tested", proof_status="incomplete"))
        assert o == QualityOutcome.APPLIED_PENDING_TESTS
        assert any(x.code == "applied_without_test_evidence" for x in f)
        assert s.band != QualityBand.EXCELLENT

    def test_tests_failed_low(self):
        o, s, _ = _classify(_ev(trust=_TRUST_OK, verification=_VERIF_OK, intent_state="approved",
                                apply_state="applied", test_state="failed", proof_status="failed"))
        assert o == QualityOutcome.TESTS_FAILED
        assert s.band == QualityBand.LOW

    def test_proof_verified_excellent(self):
        o, s, f = _classify(_ev(trust=_TRUST_OK, verification=_VERIF_OK, intent_state="approved",
                                apply_state="applied", test_state="passed", proof_status="verified"))
        assert o == QualityOutcome.COMPLETED_SUCCESS
        assert s.band == QualityBand.EXCELLENT
        assert any(x.code == "useful_and_verified" for x in f)

    def test_missing_verification_caps_medium(self):
        # No verification evidence → cannot exceed medium even if intent approved.
        o, s, _ = _classify(_ev(trust=_TRUST_OK, verification=None, intent_state="approved",
                                apply_state="applied", test_state="not_tested"))
        assert s.band in (QualityBand.MEDIUM, QualityBand.LOW, QualityBand.VERY_LOW)

    def test_no_cost_invention(self):
        _o, s, _ = _classify(_ev(trust=_TRUST_OK, verification=_VERIF_OK, intent_state="pending"))
        assert s.dimensions["cost_efficiency"] == "unknown"

    def test_score_cap_helper_no_excellent_without_proof(self):
        s = _score(QualityBand.EXCELLENT, {"verification_quality": "pass", "human_decision": "pass",
                                           "proof_outcome": "unknown"})
        assert s.band != QualityBand.EXCELLENT


# ---------------------------------------------------------------------------
# Persisted-evaluation helpers for feedback / integrity tests
# ---------------------------------------------------------------------------


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _write_eval(env, *, outcome, band, dims=None, job_id="J", model="qwen",
                route="local_candidate_generator", fp=None):
    eid = uuid4().hex[:16]
    rec = {
        "version": 1, "evaluation_id": eid, "job_id": job_id, "model_label": model,
        "route_tier": route, "outcome": outcome,
        "score": {"value": 0.5, "band": band, "confidence": "medium", "dimensions": dims or {}},
        "evidence_fingerprint": fp or eid, "created_at": "2026-06-15T00:00:00Z", "findings": [],
        "evidence_refs": [],
    }
    p = env / "workspaces" / job_id / "candidate_quality" / eid / "evaluation.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec))
    return eid


# ---------------------------------------------------------------------------
# Step 1667 — routing feedback
# ---------------------------------------------------------------------------


class TestRoutingFeedback:
    def test_no_evidence_neutral(self, env):
        fb = route_quality_feedback("qwen", data_dir=env)
        assert fb["recommend"] == "neutral"
        assert fb["run_count"] == 0

    def test_repeated_rejection_lowers(self, env):
        for _ in range(2):
            _write_eval(env, outcome=QualityOutcome.VERIFICATION_REJECTED, band=QualityBand.LOW)
        fb = route_quality_feedback("qwen", data_dir=env)
        assert fb["recommend"] == "lower"

    def test_proof_verified_raises(self, env):
        for _ in range(2):
            _write_eval(env, outcome=QualityOutcome.COMPLETED_SUCCESS, band=QualityBand.EXCELLENT,
                        dims={"proof_outcome": "pass"})
        fb = route_quality_feedback("qwen", data_dir=env)
        assert fb["recommend"] == "raise"

    def test_unknown_quality_not_external(self, env):
        # No evidence → unknown/neutral; never promotes an expensive builder.
        fb = route_quality_feedback("qwen", route_tier="external_candidate_generator", data_dir=env)
        assert fb["recommend"] in ("neutral", "unknown") or fb["confidence"] == "unknown"


# ---------------------------------------------------------------------------
# Step 1679 — integrity
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_clean(self, env):
        _write_eval(env, outcome=QualityOutcome.PENDING_APPROVAL, band=QualityBand.MEDIUM)
        assert candidate_quality_integrity(env)["passed"] is True

    def test_success_without_proof_flagged(self, env):
        _write_eval(env, outcome=QualityOutcome.COMPLETED_SUCCESS, band=QualityBand.EXCELLENT,
                    dims={"proof_outcome": "unknown"})
        r = candidate_quality_integrity(env)
        assert r["passed"] is False
        assert any(v["code"] == "success_without_proof" for v in r["violations"])

    def test_high_score_for_rejected_flagged(self, env):
        _write_eval(env, outcome=QualityOutcome.VERIFICATION_REJECTED, band=QualityBand.HIGH)
        r = candidate_quality_integrity(env)
        assert any(v["code"] == "high_score_for_rejected" for v in r["violations"])


# ---------------------------------------------------------------------------
# Integration through the generator + redaction
# ---------------------------------------------------------------------------


class TestIntegration:
    def _setup_pending(self, env, monkeypatch, rationale="addresses the documentation gap"):
        rv = env / "review.md"; rv.write_text("## Verdict\nPASS\n")
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rv))
        for k, v in {"ENABLED": "1", "ENDPOINT": "http://127.0.0.1:11434", "MODEL": "qwen"}.items():
            monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_" + k, v)
        from packages.core.models import Artifact, ArtifactKind, Job, RunState
        from packages.orchestration.storage import save_job
        fa = Artifact(name="f", content="x", kind=ArtifactKind.VERIFICATION, task_id=None,
                      metadata={"test_failure": True, "related_files": ["docs/note.md"], "test_command": "pytest"})
        job = Job(id=uuid4(), name="t", user_prompt="x", state=RunState.RUNNING, artifacts=[fa],
                  metadata={"target_repo": ".",
                            "repair_attempts_v1": {"a1": {"attempt_id": "a1", "failure_artifact_id": str(fa.id), "status": "tested_failed"}},
                            "repair_request_packages_v0": {"rp1": {"request_package_id": "rp1", "job_id": "", "failure_artifact_id": str(fa.id), "target_kind": "docs", "sections": [{"title": "G", "body": "fix", "files": ["docs/note.md"]}]}}})
        save_job(job, root=env)
        cand = json.dumps({"summary": "Add", "rationale": rationale, "target_files": ["docs/note.md"],
                           "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "hi"}]})
        def tx(m, u, b, t):
            return (200, json.dumps({"response": cand}).encode())
        from packages.orchestration.local_candidate_generator import (
            LocalCandidateGenerationRequest,
            run_local_candidate_generation,
        )
        g = run_local_candidate_generation(
            LocalCandidateGenerationRequest(request_package_id="rp1", job_id=str(job.id),
                                            failure_artifact_id=str(fa.id)), data_dir=env, transport=tx)
        return str(job.id), g

    def test_pending_eval_and_idempotent(self, env, monkeypatch):
        jid, g = self._setup_pending(env, monkeypatch)
        assert g.status == "intent_pending_approval"
        e1 = evaluate_candidate_quality(generation_id=g.generation_id, data_dir=env)
        assert e1.outcome == QualityOutcome.PENDING_APPROVAL
        assert e1.score.band == QualityBand.MEDIUM
        e2 = evaluate_candidate_quality(generation_id=g.generation_id, data_dir=env)
        assert e2.evaluation_id == e1.evaluation_id

    def test_no_raw_leak(self, env, monkeypatch):
        jid, g = self._setup_pending(env, monkeypatch,
                                     rationale="/home/u/.ssh/id_rsa Traceback secret sk-ABCDEFGHIJKLMNOP")
        e = evaluate_candidate_quality(generation_id=g.generation_id, data_dir=env)
        blob = json.dumps(export_candidate_quality_json(e))
        for bad in ("/home/u/.ssh/id_rsa", "Traceback", "sk-ABCDEFGHIJKLMNOP"):
            assert bad not in blob

    def test_missing_evidence_safe(self, env):
        e = evaluate_candidate_quality(generation_id="nope", data_dir=env)
        assert e.outcome == QualityOutcome.EVIDENCE_INCOMPLETE
        assert e.next_safe_action.startswith("remedy ")


# ---------------------------------------------------------------------------
# Step 1669 — architecture guards
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _code(self):
        import re
        src = Path("packages/orchestration/candidate_quality.py").read_text()
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        return "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))

    def test_no_forbidden_imports(self):
        code = self._code()
        for bad in ("import requests", "import httpx", "import openai", "import anthropic",
                    "import subprocess", "shell=True", "urllib.request", "import socket"):
            assert bad not in code, f"forbidden: {bad}"

    def test_no_execution_or_generation(self):
        code = self._code()
        for bad in ("source_apply", "patch_apply", "apply_patch", "approve_intent",
                    "run_local_candidate_generation", "intake_provider_repair",
                    "create_pr", "git commit", "git push", ".tasks.append"):
            assert bad not in code, f"forbidden execution token: {bad}"

    def test_export_has_no_raw_fields(self):
        from packages.orchestration.candidate_quality import CandidateQualityEvaluation
        d = export_candidate_quality_json(CandidateQualityEvaluation(evaluation_id="e"))
        for forbidden in ("prompt", "raw", "output_text", "diff", "source", "stdout", "stderr"):
            assert forbidden not in d
