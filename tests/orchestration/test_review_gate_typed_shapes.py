"""F1+F2 (round 26) — the gate schema is FULLY typed (no accept-anything node) and REQUIRES the
complete producer shape. A structurally-variable informational field can no longer carry an
arbitrary object, and a nested object that omits its required fields no longer passes.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_typed", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_typed", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates():
    return {k: copy.deepcopy(v) for k, v in _E2E._complete_gates().items()}


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


def test_no_ANY_node_remains():
    # F1: the schema engine no longer defines an accept-anything node.
    assert not hasattr(_brm, "ANY")


def test_baseline_complete_matrix_passes():
    assert _ok(_gates()) is True


class TestFullyTypedNoCatchAll:
    def test_token_status_field_object_blocks(self):
        g = _gates()
        g["final_verifier_report.json"]["token_status"]["actual_prompt_tokens"] = {"unexpected": 1}
        assert _ok(g) is False

    def test_token_actual_summary_object_blocks(self):
        g = _gates()
        g["final_verifier_report.json"]["token_actual_summary"] = {"nested": 1}
        assert _ok(g) is False

    def test_sticky_binding_warning_object_blocks(self):
        g = _gates()
        g["final_verifier_report.json"]["sticky_binding_warnings"] = [{"unexpected": True}]
        assert _ok(g) is False

    def test_total_cost_usd_bool_blocks(self):
        g = _gates()
        g["final_verifier_report.json"]["token_status"]["total_cost_usd"] = True
        assert _ok(g) is False

    def test_token_status_null_int_ok(self):
        # A legitimately-null producer field is accepted by the _Nullable union.
        g = _gates()
        g["final_verifier_report.json"]["token_status"]["actual_total_tokens"] = None
        assert _ok(g) is True

    def test_content_hash_mismatch_record_shape(self):
        # An arbitrary object in content_hash_mismatches is refused (it must be the exact record) —
        # but the list is required empty for READY anyway, so a populated one blocks either way.
        g = _gates()
        g["final_verifier_report.json"]["content_hash_mismatches"] = [{"random": 1}]
        assert _ok(g) is False


class TestRequiredFields:
    def test_missing_token_status_blocks(self):
        g = _gates()
        del g["final_verifier_report.json"]["token_status"]
        assert _ok(g) is False

    def test_stream_section_only_two_fields_blocks(self):
        g = _gates()
        g["artifact_contract_gate.json"]["stream_artifacts"] = {"applicable": False,
                                                                "verdict": "NOT_APPLICABLE"}
        assert _ok(g) is False

    def test_worktree_section_incomplete_blocks(self):
        g = _gates()
        g["artifact_contract_gate.json"]["worktree_artifacts"] = {"applicable": False,
                                                                  "verdict": "NOT_APPLICABLE"}
        assert _ok(g) is False

    def test_test_status_missing_failed_blocks(self):
        g = _gates()
        g["final_verifier_report.json"]["test_status"] = {"ran": True, "passed": 1}
        assert _ok(g) is False

    def test_evidence_freshness_missing_field_blocks(self):
        g = _gates()
        g["fresh_evidence_gate.json"]["evidence_freshness"] = {"is_fresh": True, "job_id_match": True}
        assert _ok(g) is False

    def test_manifest_integrity_missing_notes_blocks(self):
        g = _gates()
        del g["manifest_integrity.json"]["notes"]
        assert _ok(g) is False
