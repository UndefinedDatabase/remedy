"""F1 (round 22) — READY_FOR_REVIEW requires the complete packaged gate verdict matrix."""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location("_brm_gate", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_brm)


def _gates(**over):
    g = {"final_verifier_report.json": {"verdict": "PASS_WITH_RISKS"},
         "fresh_evidence_gate.json": {"verdict": "PASS"},
         "artifact_contract_gate.json": {"verdict": "PASS"},
         "change_provenance_gate.json": {"verdict": "PASS"},
         "runtime_integration_gate.json": {"verdict": "PASS"},
         "manifest_integrity.json": {"ok": True},
         "postmortem_integrity.json": {"ok": True}}
    g.update(over)
    return g


def _eval(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))


def test_all_pass_is_ok():
    assert _eval(_gates())["ok"] is True


def test_final_verifier_pass_is_ok():
    assert _eval(_gates(**{"final_verifier_report.json": {"verdict": "PASS"}}))["ok"] is True


def test_final_verifier_blocked_blocks():
    r = _eval(_gates(**{"final_verifier_report.json": {"verdict": "BLOCKED"}}))
    assert r["ok"] is False and any("final_verifier" in x for x in r["blocking_reasons"])


def test_final_verifier_missing_blocks():
    assert _eval(_gates(**{"final_verifier_report.json": None}))["ok"] is False


def test_fresh_evidence_non_pass_blocks():
    assert _eval(_gates(**{"fresh_evidence_gate.json": {"verdict": "FAIL"}}))["ok"] is False


def test_artifact_contract_non_pass_blocks():
    assert _eval(_gates(**{"artifact_contract_gate.json": {"verdict": "BLOCKED"}}))["ok"] is False


def test_change_provenance_non_pass_blocks():
    assert _eval(_gates(**{"change_provenance_gate.json": {"verdict": "BLOCKED"}}))["ok"] is False


def test_runtime_integration_non_pass_blocks():
    assert _eval(_gates(**{"runtime_integration_gate.json": {"verdict": "FAIL"}}))["ok"] is False


def test_manifest_integrity_false_blocks():
    assert _eval(_gates(**{"manifest_integrity.json": {"ok": False}}))["ok"] is False


def test_postmortem_integrity_false_blocks():
    assert _eval(_gates(**{"postmortem_integrity.json": {"ok": False}}))["ok"] is False


def test_unknown_gate_schema_blocks():
    assert _eval(_gates(**{"final_verifier_report.json": {"nope": 1}}))["ok"] is False


def test_invalid_gate_json_blocks():
    def loader(name):
        if name == "artifact_contract_gate.json":
            raise ValueError("bad json")
        return _gates().get(name)
    assert _brm.evaluate_ready_gate_matrix(loader)["ok"] is False


def test_commit_execution_gate_is_not_in_the_matrix():
    # NEEDS_HUMAN_APPROVAL commit gate is expected and never consulted here
    assert "commit_execution_gate.json" not in _brm._ALL_READY_GATES
