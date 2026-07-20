"""F2 (round 24) — the final_verifier's EMBEDDED gate verdicts must equal the separately packaged
gate verdicts, all its blocking fields must be clear, and its own commit-readiness view must never
claim an auto-promotable state for a pre-acceptance package.

Reproduction that previously survived: final_verifier_report.json carries
``artifact_contract_gate: "BLOCKED"`` while the packaged artifact_contract_gate.json is PASS — two
documents disagreeing about the same gate, with the READY package trusting the optimistic one.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_emb", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_emb", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates(fname=None, **patch):
    g = {k: dict(v) for k, v in _E2E._complete_gates().items()}
    if fname is not None:
        g[fname] = {**g[fname], **patch}
    return g


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


class TestEmbeddedGateEquality:
    def test_embedded_artifact_blocked_while_packaged_passes_blocks(self):
        assert _ok(_gates("final_verifier_report.json",
                          artifact_contract_gate="BLOCKED")) is False

    def test_embedded_change_disagrees_blocks(self):
        assert _ok(_gates("final_verifier_report.json",
                          change_provenance_gate="NEEDS_REPAIR")) is False

    def test_embedded_fresh_disagrees_blocks(self):
        assert _ok(_gates("final_verifier_report.json",
                          fresh_evidence_gate="STALE")) is False

    def test_embedded_runtime_disagrees_blocks(self):
        assert _ok(_gates("final_verifier_report.json",
                          runtime_integration_gate="FAIL")) is False

    def test_all_embedded_equal_passes(self):
        # When BOTH the embedded value and the packaged gate move together, it is consistent.
        g = _gates()
        g["final_verifier_report.json"]["fresh_evidence_gate"] = "PASS"
        g["fresh_evidence_gate.json"]["verdict"] = "PASS"
        assert _ok(g) is True


class TestBlockingFieldsClear:
    def test_final_job_review_blocked_blocks(self):
        assert _ok(_gates("final_verifier_report.json", final_job_review_blocked=True)) is False

    def test_execution_mode_blocked_blocks(self):
        assert _ok(_gates("final_verifier_report.json", execution_mode_blocked=True)) is False

    def test_model_mismatch_blocked_blocks(self):
        assert _ok(_gates("final_verifier_report.json", model_mismatch_blocked=True)) is False

    def test_model_needs_repair_blocks(self):
        assert _ok(_gates("final_verifier_report.json", model_needs_repair=True)) is False

    def test_missing_evidence_blocks(self):
        assert _ok(_gates("final_verifier_report.json", missing_evidence=["x.json"])) is False

    def test_execution_mode_findings_block(self):
        assert _ok(_gates("final_verifier_report.json",
                          execution_mode_findings=["provider-backed"])) is False

    def test_final_job_review_findings_block(self):
        assert _ok(_gates("final_verifier_report.json",
                          final_job_review_findings=["unresolved"])) is False


class TestFvCommitReadinessView:
    def test_auto_promotable_commit_view_blocks(self):
        # The FV's OWN commit-readiness view is a distinct field from the packaged commit gate's
        # verdict; a pre-acceptance package must never claim it is auto-promotable.
        for promotable in ("PASS", "COMMIT_READY", "READY"):
            assert _ok(_gates("final_verifier_report.json",
                              commit_execution_gate=promotable)) is False, promotable

    def test_not_ready_commit_view_passes(self):
        for not_ready in ("BLOCKED", "NEEDS_HUMAN_APPROVAL", "NEEDS_REPAIR"):
            assert _ok(_gates("final_verifier_report.json",
                              commit_execution_gate=not_ready)) is True, not_ready
