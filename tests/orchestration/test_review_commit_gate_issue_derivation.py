"""F4 (round 25) — the commit gate's `issues` list is EXACTLY derived from gate_checks by the same
deterministic rule as build_commit_execution_gate (the writer). An empty or unrelated issues list is
no longer accepted as a second source of truth.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_iss", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_iss", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)

_NAME = "commit_execution_gate.json"


def _gates(**commit_over):
    g = {k: dict(v) for k, v in _E2E._complete_gates().items()}
    if commit_over:
        g[_NAME] = {**g[_NAME], **commit_over}
    return g


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


def test_the_derived_issue_passes():
    # _complete_gates ships the exact derived issue for final_verifier=PASS_WITH_RISKS.
    assert _ok(_gates()) is True


def test_empty_issues_blocks():
    assert _ok(_gates(issues=[])) is False


def test_unrelated_issue_blocks():
    assert _ok(_gates(issues=["totally unrelated"])) is False


def test_wrong_verdict_text_in_issue_blocks():
    assert _ok(_gates(
        issues=["gate 'final_verifier' is not PASS (verdict 'PASS')"])) is False


def test_extra_trailing_issue_blocks():
    assert _ok(_gates(issues=[
        "gate 'final_verifier' is not PASS (verdict 'PASS_WITH_RISKS')",
        "extra"])) is False


def test_blocked_gates_must_be_derived():
    assert _ok(_gates(blocked_gates=["final_verifier"])) is False


def test_all_pass_derives_empty_issues():
    g = _gates()
    g["final_verifier_report.json"]["verdict"] = "PASS"   # keep packaged verdict consistent
    g[_NAME]["gate_checks"] = {**g[_NAME]["gate_checks"], "final_verifier": "PASS"}
    g[_NAME]["non_pass_gates"] = []
    g[_NAME]["issues"] = []
    assert _ok(g) is True
