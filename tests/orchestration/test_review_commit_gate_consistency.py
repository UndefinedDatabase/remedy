"""F2 (round 23) — the commit_execution gate is CHECKED (nonblocking verdict, but validated)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location("_brm_cg", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location("_e2e_cg", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates(**over):
    g = {k: dict(v) for k, v in _E2E._complete_gates().items()}
    for name, patch in over.items():
        g[name] = None if patch is None else {**g[name], **patch}
    return g


def _res(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))


def test_a_valid_commit_gate_is_recorded_nonblocking():
    r = _res(_gates())
    assert r["ok"] is True
    assert r["gate_verdicts"]["commit_execution_gate.json"] == "NEEDS_HUMAN_APPROVAL"


def test_missing_commit_gate_blocks():
    assert _res(_gates(**{"commit_execution_gate.json": None}))["ok"] is False


def test_unsupported_version_blocks():
    assert _res(_gates(**{"commit_execution_gate.json": {"schema_version": "9.9"}}))["ok"] is False


def test_unexpected_verdict_blocks():
    assert _res(_gates(**{"commit_execution_gate.json": {"verdict": "COMMIT_READY"}}))["ok"] is False


def test_promote_ready_true_blocks():
    assert _res(_gates(**{"commit_execution_gate.json": {"promote_ready": True}}))["ok"] is False


def test_blocked_gates_nonempty_blocks():
    assert _res(_gates(**{"commit_execution_gate.json": {"blocked_gates": ["final_verifier"]}}))["ok"] is False


def test_embedded_gate_checks_must_equal_packaged():
    # commit gate claims fresh_evidence PASS while... the packaged verdict IS PASS; force a mismatch
    g = _gates()
    g["commit_execution_gate.json"]["gate_checks"]["final_verifier"] = "PASS"   # != PASS_WITH_RISKS
    assert _res(g)["ok"] is False
