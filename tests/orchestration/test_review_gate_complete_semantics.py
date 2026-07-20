"""F2 (round 25) — the COMPLETE READY semantics of every gate. A PASS/ok label can no longer sit on
top of an internally READY-incompatible body: incomplete evidence, a BLOCKED sub-status, a match
Boolean over unequal actual values, an empty required-artifact map, a nested BLOCKED section, or a
change-provenance set/hash map that disagrees with the packaged ContentProof all block.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_sem25", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_sem25", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates(with_proof=False):
    g = {k: dict(v) for k, v in _E2E._complete_gates().items()}
    if with_proof:
        cp = g["change_provenance_gate.json"]
        g["current_change_content_proof.json"] = {
            "schema_version": "1.1.0", "base_commit": "b", "head_commit": "h",
            "file_hashes": dict(cp["current_hashes"]), "file_count": len(cp["current_hashes"]),
            "tombstones": {}, "tombstone_count": 0}
    return g


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


def _fv(**over):
    g = _gates()
    g["final_verifier_report.json"] = {**g["final_verifier_report.json"], **over}
    return g


class TestFinalVerifierComplete:
    def test_incomplete_evidence_completeness_blocks(self):
        g = _gates()
        g["final_verifier_report.json"]["evidence_completeness"] = {
            **g["final_verifier_report.json"]["evidence_completeness"], "review_json": False}
        assert _ok(g) is False

    def test_spec_compliance_blocked(self):
        assert _ok(_fv(spec_compliance="BLOCKED")) is False

    def test_scratch_file_guard_blocked(self):
        assert _ok(_fv(scratch_file_guard="BLOCKED")) is False

    def test_alignment_blocked(self):
        assert _ok(_fv(file_set_alignment_status="BLOCKED")) is False

    def test_change_provenance_blocked(self):
        assert _ok(_fv(change_provenance="BLOCKED")) is False

    def test_token_cost_critical_blocks(self):
        assert _ok(_fv(token_cost_has_critical=True)) is False

    def test_token_cost_risk_finding_blocks(self):
        assert _ok(_fv(token_cost_risk_findings=["critical"])) is False

    def test_negative_passed_blocks(self):
        g = _fv()
        g["final_verifier_report.json"]["test_status"] = {"ran": True, "passed": -1, "failed": 0}
        assert _ok(g) is False

    def test_passed_disagrees_with_verification_total_blocks(self):
        g = _gates()
        g["verification_tests.json"] = {"schema_version": "1.0.0", "passed": 4242, "failed": 0,
                                        "exit_code": 0}
        assert _ok(g) is False   # fv.test_status.passed=1 != 4242


class TestFreshEvidenceEquality:
    def test_id_mismatch_with_true_boolean_blocks(self):
        g = _gates()
        g["fresh_evidence_gate.json"] = {**g["fresh_evidence_gate.json"],
                                         "evidence_job_id": "OTHER", "job_id_match": True}
        assert _ok(g) is False

    def test_range_mismatch_blocks(self):
        g = _gates()
        g["fresh_evidence_gate.json"] = {**g["fresh_evidence_gate.json"], "plan_step_range": "9-9"}
        assert _ok(g) is False


class TestArtifactContractComplete:
    def test_empty_required_artifacts_blocks(self):
        g = _gates()
        g["artifact_contract_gate.json"] = {**g["artifact_contract_gate.json"],
                                            "required_artifacts": {}}
        assert _ok(g) is False

    def test_nested_stream_blocked_verdict_blocks(self):
        g = _gates()
        g["artifact_contract_gate.json"]["stream_artifacts"] = {
            **g["artifact_contract_gate.json"]["stream_artifacts"],
            "applicable": True, "verdict": "BLOCKED"}
        assert _ok(g) is False

    def test_not_applicable_with_nonempty_list_blocks(self):
        g = _gates()
        g["artifact_contract_gate.json"]["worktree_artifacts"] = {
            **g["artifact_contract_gate.json"]["worktree_artifacts"],
            "missing_result_diffs": ["x"]}
        assert _ok(g) is False


class TestChangeProvenanceCoherence:
    def test_empty_covered_blocks(self):
        g = _gates()
        g["change_provenance_gate.json"]["covered_files"] = []
        assert _ok(g) is False

    def test_covered_not_source_minus_excluded_blocks(self):
        g = _gates()
        g["change_provenance_gate.json"]["excluded_files"] = \
            list(g["change_provenance_gate.json"]["covered_files"])[:1]
        assert _ok(g) is False

    def test_current_ne_evidence_hashes_blocks(self):
        g = _gates()
        cp = g["change_provenance_gate.json"]
        k = list(cp["current_hashes"])[0]
        cp["current_hashes"] = {**cp["current_hashes"], k: "f" * 64}
        assert _ok(g) is False

    def test_covered_ne_content_proof_authority_blocks(self):
        g = _gates(with_proof=True)
        g["change_provenance_gate.json"]["covered_files"] = \
            g["change_provenance_gate.json"]["covered_files"] + ["ghost.py"]
        g["change_provenance_gate.json"]["source_files"] = \
            g["change_provenance_gate.json"]["covered_files"]
        assert _ok(g) is False

    def test_matching_content_proof_passes(self):
        assert _ok(_gates(with_proof=True)) is True
