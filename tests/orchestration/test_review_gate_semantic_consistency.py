"""F1 (round 23) — a gate's PASS/ok label must be consistent with its own internal truth."""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location("_brm_sem", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location("_e2e_sem", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates(fname, **patch):
    g = {k: dict(v) for k, v in _E2E._complete_gates().items()}
    g[fname] = {**g[fname], **patch}
    return g


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


class TestFinalVerifier:
    def test_also_needs_repair_blocks(self):
        assert _ok(_gates("final_verifier_report.json", also_needs_repair=True)) is False

    def test_unresolved_findings_block(self):
        assert _ok(_gates("final_verifier_report.json",
                          unresolved_findings=["REAL_BLOCK"])) is False

    def test_failed_tests_block(self):
        assert _ok(_gates("final_verifier_report.json",
                          test_status={"ran": True, "passed": 0, "failed": 12})) is False

    def test_tests_not_run_blocks(self):
        assert _ok(_gates("final_verifier_report.json",
                          test_status={"ran": False, "passed": 0, "failed": 0})) is False

    def test_missing_tests_gate_not_pass_blocks(self):
        assert _ok(_gates("final_verifier_report.json", missing_tests_gate="NEEDS_TESTS")) is False

    def test_uncovered_files_block(self):
        assert _ok(_gates("final_verifier_report.json",
                          review_subject_uncovered_files=["x.py"])) is False

    def test_content_hash_mismatch_blocks(self):
        assert _ok(_gates("final_verifier_report.json",
                          content_hash_mismatches=[{"file": "x"}])) is False

    def test_postmortem_blocked_flag_blocks(self):
        assert _ok(_gates("final_verifier_report.json", postmortem_integrity_blocked=True)) is False

    def test_unsupported_version_blocks(self):
        assert _ok(_gates("final_verifier_report.json", schema_version="9.9.9")) is False


class TestFreshEvidence:
    def test_not_authoritative_blocks(self):
        assert _ok(_gates("fresh_evidence_gate.json", evidence_authoritative=False)) is False

    def test_issues_block(self):
        assert _ok(_gates("fresh_evidence_gate.json", issues=["STALE"])) is False

    def test_not_fresh_blocks(self):
        assert _ok(_gates("fresh_evidence_gate.json",
                          evidence_freshness={"is_fresh": False})) is False


class TestArtifactContract:
    def test_missing_required_blocks(self):
        assert _ok(_gates("artifact_contract_gate.json", missing_required=["review.json"])) is False

    def test_critical_fv_missing_blocks(self):
        assert _ok(_gates("artifact_contract_gate.json", critical_fv_missing=["x"])) is False


class TestChangeProvenance:
    def test_uncovered_files_block(self):
        assert _ok(_gates("change_provenance_gate.json", uncovered_files=["x.py"])) is False

    def test_content_hash_not_verified_blocks(self):
        assert _ok(_gates("change_provenance_gate.json", content_hash_verified=False)) is False


class TestRuntimeIntegration:
    def test_checks_passed_lt_total_blocks(self):
        assert _ok(_gates("runtime_integration_gate.json",
                          checks_total=5, checks_passed=3, checks=["a", "b", "c", "d", "e"])) is False

    def test_missing_check_blocks(self):
        assert _ok(_gates("runtime_integration_gate.json",
                          checks_total=3, checks_passed=3, checks=["a", "b"])) is False


class TestIntegrityGates:
    def test_manifest_integrity_failures_block(self):
        assert _ok(_gates("manifest_integrity.json", failures=["bad"])) is False

    def test_postmortem_integrity_failures_block(self):
        assert _ok(_gates("postmortem_integrity.json", failures=["bad"])) is False


def test_the_complete_consistent_matrix_passes():
    assert _ok({k: dict(v) for k, v in _E2E._complete_gates().items()}) is True
