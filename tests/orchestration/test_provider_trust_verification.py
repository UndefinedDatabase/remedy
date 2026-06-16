"""Unit + integration tests for Provider Trust Verification v1 (Steps 1560-1563).

Verification is a SAFE second-stage check on UNTRUSTED candidate output before it can
become a pending repair intent. It NEVER executes providers/models/patches/tests, never
approves/applies, never imports a provider SDK / network / subprocess, and never leaks raw
candidate/diff/source/secrets/tracebacks/absolute paths. Overclaim/unrelated/repeated-failed
candidates must not pass silently. Local advisor (if used) is critique-only.
"""
from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.orchestration.provider_trust import Severity
from packages.orchestration.provider_trust_verification import (
    CANONICAL_FINDING_CODES,
    LoopRisk,
    ProviderCandidateRepair,
    ProviderVerificationReport,
    ProviderVerificationRequest,
    VerificationDecision,
    VerificationFindingCode,
    VerificationStatus,
    check_loop_risk,
    check_minimality,
    check_overclaims,
    check_request_consistency,
    decide_verification,
    export_verification_report_json,
    get_verification_report,
    load_verification_reports,
    scan_candidate_secrets,
    score_findings,
    verify_provider_candidate,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _patch_candidate(targets, *, summary="Fix", rationale="addresses the gap", blocks=1):
    return ProviderCandidateRepair(
        candidate_kind="patch", summary=summary, target_files=list(targets),
        patch_format="unified_diff", has_patch=True, patch_block_count=blocks,
        rationale=rationale, line_count=10)


def _make_job(data_dir, *, failure_meta=None):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState
    from packages.orchestration.storage import save_job
    arts = []
    fid = ""
    if failure_meta is not None:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=None,
                      metadata=failure_meta)
        arts.append(fa)
        fid = str(fa.id)
    job = Job(id=uuid4(), name="v", user_prompt="x", state=RunState.RUNNING,
              artifacts=arts, metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id), fid


@pytest.fixture()
def data_dir(tmp_path, monkeypatch):
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


# ---------------------------------------------------------------------------
# Taxonomy + decision rules
# ---------------------------------------------------------------------------


class TestTaxonomyAndDecision:
    def test_canonical_codes_present(self):
        for code in (
            "candidate_not_linked_to_failure", "candidate_overclaims_apply",
            "candidate_overclaims_tests", "candidate_too_broad", "candidate_loop_risk",
            "candidate_repeats_failed_attempt", "candidate_verification_incomplete",
        ):
            assert code in CANONICAL_FINDING_CODES

    def test_blocker_or_high_rejects(self):
        f = [type("F", (), {"severity": Severity.HIGH})()]
        dec, status, _ = decide_verification(f, candidate_present=True)
        assert dec == VerificationDecision.REJECTED
        assert status == VerificationStatus.REJECTED

    def test_medium_needs_review(self):
        f = [type("F", (), {"severity": Severity.MEDIUM})()]
        dec, status, _ = decide_verification(f, candidate_present=True)
        assert dec == VerificationDecision.NEEDS_HUMAN_REVIEW

    def test_low_only_passes(self):
        f = [type("F", (), {"severity": Severity.LOW})()]
        dec, status, _ = decide_verification(f, candidate_present=True)
        assert dec == VerificationDecision.PASSED

    def test_missing_candidate_incomplete(self):
        dec, status, _ = decide_verification([], candidate_present=False)
        assert dec == VerificationDecision.INCOMPLETE

    def test_score_monotonic(self):
        from packages.orchestration.provider_trust_verification import _finding
        clean = score_findings([])
        noisy = score_findings([_finding(VerificationFindingCode.CANDIDATE_TOO_BROAD,
                                         Severity.HIGH, "x")])
        assert clean.value >= noisy.value
        assert clean.value == 1.0


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


class TestChecks:
    def test_overclaim_apply_tests_verify(self):
        codes = {f.code for f in check_overclaims("I applied this and all tests passed; verified fix")}
        assert VerificationFindingCode.CANDIDATE_OVERCLAIMS_APPLY in codes
        assert VerificationFindingCode.CANDIDATE_OVERCLAIMS_TESTS in codes
        assert VerificationFindingCode.CANDIDATE_OVERCLAIMS_VERIFICATION in codes

    def test_overclaim_intent_framing_ok(self):
        # "intended to fix" / "should fix" framing is NOT an overclaim.
        assert check_overclaims("This change is intended to fix the bug and should resolve it") == []

    def test_overclaim_never_echoes_raw(self):
        findings = check_overclaims("secret: I applied ghp_abcdefghijklmnop")
        for f in findings:
            assert "ghp_" not in f.summary

    def test_minimality_too_broad(self):
        cand = _patch_candidate([f"src/f{i}.py" for i in range(15)])
        codes = {f.code for f in check_minimality(cand)}
        assert VerificationFindingCode.CANDIDATE_TOO_BROAD in codes

    def test_minimality_unexpected_lock_file(self):
        cand = _patch_candidate(["poetry.lock"])
        codes = {f.code for f in check_minimality(cand)}
        assert VerificationFindingCode.PATCH_TARGETS_UNEXPECTED_FILE in codes

    def test_consistency_missing_package_is_low(self):
        cand = _patch_candidate(["docs/a.md"])
        findings = check_request_consistency(cand, None)
        assert all(f.severity == Severity.LOW for f in findings)

    def test_consistency_docs_request_source_change(self):
        cand = _patch_candidate(["src/app.py"])
        pkg = {"target_kind": "docs", "sections": []}
        codes = {f.code for f in check_request_consistency(cand, pkg)}
        assert VerificationFindingCode.CANDIDATE_SOURCE_CHANGE_FOR_DOCS_REQUEST in codes

    def test_secret_scan_no_echo(self):
        findings = scan_candidate_secrets("token = 'ghp_abcdefghijklmnopqrstuvwxyz0123'")
        assert findings
        for f in findings:
            assert "ghp_" not in f.summary

    def test_entropy_high_token_detected(self):
        findings = scan_candidate_secrets("x = 'A9f3Kd02LmZqWxYbT7uVc1Ne8Rs5Gh4Jp'")
        codes = {f.code for f in findings}
        assert VerificationFindingCode.CANDIDATE_HIGH_ENTROPY_TOKEN in codes

    def test_url_credentials_detected(self):
        findings = scan_candidate_secrets("clone https://user:p4ssw0rd@example.com/repo.git")
        codes = {f.code for f in findings}
        assert VerificationFindingCode.CANDIDATE_URL_CREDENTIALS in codes


# ---------------------------------------------------------------------------
# Loop risk
# ---------------------------------------------------------------------------


class TestLoopRisk:
    def test_repeat_rejected_hash_is_high(self, data_dir):
        from packages.orchestration.storage import load_job, save_job
        jid, _ = _make_job(data_dir)
        job = load_job(UUID(jid), data_dir)
        job.metadata["provider_verifications_v1"] = {
            "v1": {"candidate_hash": "h1", "decision": "verification_rejected",
                   "failure_artifact_id": ""},
        }
        save_job(job, root=data_dir)
        job = load_job(UUID(jid), data_dir)
        findings, risk = check_loop_risk(job, "h1", "")
        assert risk == LoopRisk.HIGH
        assert any(f.code == VerificationFindingCode.CANDIDATE_REPEATS_FAILED_ATTEMPT
                   for f in findings)


# ---------------------------------------------------------------------------
# Integration through intake
# ---------------------------------------------------------------------------


class TestIntakeIntegration:
    _DOCS_CAND = json.dumps({
        "summary": "Add note", "rationale": "addresses the documentation gap",
        "target_files": ["docs/note.md"],
        "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "hi"}],
    })

    def _intake(self, data_dir, fid, raw):
        from packages.orchestration.provider_trust import (
            ProviderOutputIntakeRequest,
            export_intake_result_json,
            intake_provider_repair,
        )
        res = intake_provider_repair(
            ProviderOutputIntakeRequest(job_id=fid[0], provider_name="claude",
                                        failure_artifact_id=fid[1]),
            stdin_text=raw, data_dir=data_dir)
        return export_intake_result_json(res)

    def test_passed_creates_intent(self, data_dir):
        jid, fid = _make_job(data_dir, failure_meta={
            "test_failure": True, "related_files": ["docs/note.md"], "test_command": "pytest"})
        out = self._intake(data_dir, (jid, fid), self._DOCS_CAND)
        assert out["trust_status"] == "accepted"
        assert out["verification_decision"] == VerificationDecision.PASSED
        assert out["repair_intent_id"]

    def test_unlinked_candidate_no_intent(self, data_dir):
        jid, _ = _make_job(data_dir)  # no failure artifact
        out = self._intake(data_dir, (jid, ""), self._DOCS_CAND)
        # Trust may accept (low-only), but verification withholds the intent.
        assert out["verification_decision"] != VerificationDecision.PASSED
        assert not out["repair_intent_id"]

    def test_overclaim_candidate_no_intent(self, data_dir):
        jid, fid = _make_job(data_dir, failure_meta={
            "test_failure": True, "related_files": ["docs/note.md"], "test_command": "pytest"})
        raw = json.dumps({
            "summary": "Add note", "rationale": "I applied this and all tests passed",
            "target_files": ["docs/note.md"],
            "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "hi"}],
        })
        out = self._intake(data_dir, (jid, fid), raw)
        assert out["verification_decision"] in (
            VerificationDecision.NEEDS_HUMAN_REVIEW, VerificationDecision.REJECTED)
        assert not out["repair_intent_id"]
        assert "all tests passed" not in json.dumps(out)

    def test_self_dogfood_candidate_links_verification(self, data_dir):
        # A self-linked candidate (provider label self_dogfood:<attempt>) is verified via
        # the self-relevance path, not failure-relevance — it should pass + link a report.
        from packages.orchestration.provider_trust import (
            ProviderOutputIntakeRequest,
            export_intake_result_json,
            intake_provider_repair,
        )
        from packages.orchestration.storage import load_job
        jid, _ = _make_job(data_dir)
        res = intake_provider_repair(
            ProviderOutputIntakeRequest(job_id=jid, provider_name="self_dogfood:att-1"),
            stdin_text=self._DOCS_CAND, data_dir=data_dir)
        out = export_intake_result_json(res)
        assert out["verification_decision"] == VerificationDecision.PASSED
        assert out["verification_id"]
        job = load_job(UUID(jid), data_dir)
        rep = get_verification_report(job, out["verification_id"])
        assert rep is not None
        assert rep["self_attempt_id"] == "att-1"

    def test_verification_report_persisted_and_safe(self, data_dir):
        from packages.orchestration.storage import load_job
        jid, fid = _make_job(data_dir, failure_meta={
            "test_failure": True, "related_files": ["docs/note.md"], "test_command": "pytest"})
        self._intake(data_dir, (jid, fid), self._DOCS_CAND)
        job = load_job(UUID(jid), data_dir)
        reps = load_verification_reports(job)
        assert reps
        rep = list(reps.values())[0]
        blob = json.dumps(rep)
        for leak in ("/home/", "Traceback", "-----BEGIN"):
            assert leak not in blob
        # private report.json exists on disk
        vdir = data_dir / "workspaces" / jid / "provider_verification"
        assert any(p.name == "report.json" for p in vdir.rglob("report.json"))


# ---------------------------------------------------------------------------
# Standalone verify + idempotency
# ---------------------------------------------------------------------------


class TestStandaloneVerify:
    def test_missing_trust_report_incomplete(self, data_dir):
        jid, _ = _make_job(data_dir)
        rep = verify_provider_candidate(
            ProviderVerificationRequest(job_id=jid, trust_report_id="nope"), data_dir=data_dir)
        assert rep.decision == VerificationDecision.INCOMPLETE
        assert not rep.allowed_to_create_intent

    def test_idempotent_reuse(self, data_dir):
        from packages.orchestration.provider_trust import (
            ProviderOutputIntakeRequest,
            intake_provider_repair,
        )
        jid, fid = _make_job(data_dir, failure_meta={
            "test_failure": True, "related_files": ["docs/note.md"], "test_command": "pytest"})
        res = intake_provider_repair(
            ProviderOutputIntakeRequest(job_id=jid, provider_name="claude", failure_artifact_id=fid),
            stdin_text=TestIntakeIntegration._DOCS_CAND, data_dir=data_dir)
        trid = res.trust_report_id
        r1 = verify_provider_candidate(
            ProviderVerificationRequest(job_id=jid, trust_report_id=trid), data_dir=data_dir)
        r2 = verify_provider_candidate(
            ProviderVerificationRequest(job_id=jid, trust_report_id=trid), data_dir=data_dir)
        # Reused (same verification id), not duplicated.
        assert r2.verification_id == r1.verification_id


# ---------------------------------------------------------------------------
# Architecture guards
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _code_lines(self):
        src = Path("packages/orchestration/provider_trust_verification.py").read_text()
        # Strip the module docstring + comment lines so prose can't false-positive.
        out, in_doc = [], False
        for ln in src.splitlines():
            s = ln.strip()
            if s.startswith('"""'):
                in_doc = not in_doc and s.count('"""') == 1
                continue
            if in_doc or s.startswith("#"):
                continue
            out.append(ln)
        return "\n".join(out)

    def test_no_forbidden_imports(self):
        code = self._code_lines()
        for bad in ("import requests", "import httpx", "import openai", "import anthropic",
                    "import subprocess", "shell=True", "urllib.request", "import socket"):
            assert bad not in code, f"forbidden token: {bad}"

    def test_no_apply_or_approval_calls(self):
        code = self._code_lines()
        for bad in ("source_apply", "patch_apply(", "apply_patch", "approve_intent",
                    "create_pr", "git commit", "git push"):
            assert bad not in code, f"forbidden execution token: {bad}"

    def test_export_has_no_raw_fields(self):
        rep = ProviderVerificationReport(verification_id="v", job_id="j")
        d = export_verification_report_json(rep)
        for forbidden in ("raw", "diff", "source", "patch_body", "stdout", "stderr"):
            assert forbidden not in d
