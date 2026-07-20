"""F1 (round 25) — every gate is validated by an EXACT RECURSIVE schema: an unknown NESTED field, a
wrong element type or a dynamic-map key that violates its grammar all BLOCK. The round-24 validator
closed only the top-level field set, so an injected nested field rode straight through.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_rec", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_rec", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates():
    return {k: dict(v) for k, v in _E2E._complete_gates().items()}


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


def _mut(fname, mut):
    g = _gates()
    obj = {k: (dict(v) if isinstance(v, dict) else v) for k, v in g[fname].items()}
    g[fname] = obj
    mut(obj)
    return g


def test_the_complete_recursive_matrix_passes():
    assert _ok(_gates()) is True


class TestUnknownNestedFieldBlocks:
    def test_final_verifier_test_status_nested_unknown(self):
        assert _ok(_mut("final_verifier_report.json",
                        lambda o: o.__setitem__("test_status",
                                                {**o["test_status"], "EXTRA_SECRET": "benign"}))) is False

    def test_final_verifier_evidence_completeness_nested_unknown(self):
        assert _ok(_mut("final_verifier_report.json",
                        lambda o: o.__setitem__("evidence_completeness",
                                                {**o["evidence_completeness"], "EXTRA": True}))) is False

    def test_fresh_evidence_validity_nested_unknown(self):
        assert _ok(_mut("fresh_evidence_gate.json",
                        lambda o: o.__setitem__("evidence_validity",
                                                {**o["evidence_validity"], "EXTRA": "x"}))) is False

    def test_artifact_stream_nested_unknown(self):
        assert _ok(_mut("artifact_contract_gate.json",
                        lambda o: o.__setitem__("stream_artifacts",
                                                {**o["stream_artifacts"], "EXTRA": "x"}))) is False

    def test_change_provenance_top_unknown(self):
        assert _ok(_mut("change_provenance_gate.json",
                        lambda o: o.__setitem__("EXTRA_NESTED", {"a": 1}))) is False


class TestWrongTypeBlocks:
    def test_test_status_passed_bool_not_int(self):
        assert _ok(_mut("final_verifier_report.json",
                        lambda o: o.__setitem__("test_status",
                                                {**o["test_status"], "passed": True}))) is False

    def test_checks_total_string_blocks(self):
        assert _ok(_mut("runtime_integration_gate.json",
                        lambda o: o.__setitem__("checks_total", "3"))) is False

    def test_required_artifacts_value_not_bool(self):
        assert _ok(_mut("artifact_contract_gate.json",
                        lambda o: o.__setitem__("required_artifacts",
                                                {**o["required_artifacts"], "manifest.json": "yes"}))) is False


class TestDynamicKeyGrammar:
    def test_bad_task_id_key_blocks(self):
        assert _ok(_mut("final_verifier_report.json",
                        lambda o: o.__setitem__("execution_mode_by_task", {"BADID": "x"}))) is False

    def test_good_task_id_key_passes(self):
        g = _mut("final_verifier_report.json",
                 lambda o: o.__setitem__("execution_mode_by_task", {"T001": "operator"}))
        assert _ok(g) is True

    def test_change_hash_map_abs_path_key_blocks(self):
        assert _ok(_mut("change_provenance_gate.json",
                        lambda o: o.__setitem__("current_hashes",
                                                {**o["current_hashes"], "/etc/passwd": "0" * 64}))) is False
