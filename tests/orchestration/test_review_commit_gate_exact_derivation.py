"""F4 (round 24) — the commit_execution gate is CHECKED (nonblocking) but must be an EXACT derived
document: its gate_checks are exactly the five packaged gate verdicts, non_pass_gates is the derived
set of non-PASS gates, blocked_gates is empty, promote_ready is false, and the verdict stays
NEEDS_HUMAN_APPROVAL. An empty, missing, extra-key or contradictory commit gate blocks Evidence
integrity even though human approval itself is expected.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_cg", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_cg", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)

_NAME = "commit_execution_gate.json"


def _gates(**commit_over):
    g = {k: dict(v) for k, v in _E2E._complete_gates().items()}
    if commit_over:
        cg = dict(g[_NAME])
        cg.update(commit_over)
        g[_NAME] = cg
    return g


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


def test_the_derived_commit_gate_passes():
    assert _ok(_gates()) is True


class TestExactGateChecks:
    def test_missing_gate_check_key_blocks(self):
        checks = {"final_verifier": "PASS_WITH_RISKS", "fresh_evidence_gate": "PASS",
                  "artifact_contract_gate": "PASS", "change_provenance_gate": "PASS"}
        assert _ok(_gates(gate_checks=checks)) is False

    def test_extra_gate_check_key_blocks(self):
        g = _gates()
        g[_NAME]["gate_checks"]["phantom_gate"] = "PASS"
        assert _ok(g) is False

    def test_empty_gate_checks_blocks(self):
        assert _ok(_gates(gate_checks={})) is False

    def test_gate_check_value_contradicts_packaged_blocks(self):
        g = _gates()
        g[_NAME]["gate_checks"]["fresh_evidence_gate"] = "STALE"   # packaged fresh gate is PASS
        assert _ok(g) is False


class TestDerivedFields:
    def test_wrong_non_pass_gates_blocks(self):
        # final_verifier is PASS_WITH_RISKS (not PASS), so the derived non_pass_gates is
        # ['final_verifier']; anything else is a contradiction.
        assert _ok(_gates(non_pass_gates=[])) is False
        assert _ok(_gates(non_pass_gates=["fresh_evidence_gate"])) is False

    def test_nonempty_blocked_gates_blocks(self):
        assert _ok(_gates(blocked_gates=["final_verifier"])) is False

    def test_promote_ready_true_blocks(self):
        assert _ok(_gates(promote_ready=True)) is False

    def test_wrong_verdict_blocks(self):
        assert _ok(_gates(verdict="PASS")) is False


class TestPresenceAndValidity:
    def test_missing_commit_gate_blocks(self):
        g = {k: dict(v) for k, v in _E2E._complete_gates().items()}
        g[_NAME] = None
        assert _ok(g) is False

    def test_invalid_json_commit_gate_blocks(self):
        g = {k: dict(v) for k, v in _E2E._complete_gates().items()}

        def loader(name):
            if name == _NAME:
                raise ValueError("corrupt commit gate JSON")
            return g.get(name)
        assert _brm.evaluate_ready_gate_matrix(loader)["ok"] is False
