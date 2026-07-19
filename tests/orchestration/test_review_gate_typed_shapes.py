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

    def test_token_actual_summary_unknown_field_blocks(self):
        # An INVALID summary object (unknown fields, missing required) blocks — a VALID producer
        # summary is proven to PASS in TestRealTokenSummary below.
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


class TestRealTokenSummary:
    """F1 (round 27) — the gate schema accepts the ACTUAL final_verifier token-measurement producer
    output for every confidence branch, using producer-generated data (not hand-written dicts)."""

    def _ts(self, confidence):
        # A token_status the real producer accepts; high/mixed carry real measured values.
        return {"measurement_confidence": confidence, "measurement_source": "provider_api",
                "actual_prompt_tokens": 100, "actual_completion_tokens": 50,
                "actual_total_tokens": 150, "total_cost_usd": 0.01, "cost_call_count": 2,
                "cost_coverage_complete": True, "cost_coverage_reason": "ok", "provider_call_count": 2,
                "actual_call_count": 2, "actual_coverage_complete": True, "actual_missing_reasons": None,
                "cli_version": "1.2.3", "configured_models": {"builder": "c", "reviewer": "c"},
                "actual_models": {"builder": "c", "reviewer": "c"}, "actual_model_verified": True}

    def _fv_with(self, confidence):
        from packages.orchestration.final_verifier import _token_measurement_summary
        tm = _token_measurement_summary(self._ts(confidence))
        g = _gates()
        fv = g["final_verifier_report.json"]
        fv["token_measurement"] = copy.deepcopy(tm)
        fv["token_actual_summary"] = copy.deepcopy(tm["actual_summary"])
        fv["token_measurement_note"] = tm["measurement_note"]
        fv["token_measurement_confidence"] = tm["measurement_confidence"]
        return g

    def test_high_confidence_producer_summary_passes(self):
        assert _ok(self._fv_with("high")) is True

    def test_mixed_confidence_producer_summary_passes(self):
        assert _ok(self._fv_with("mixed")) is True

    def test_low_confidence_null_summary_and_note_passes(self):
        # low → actual_summary null, measurement_note the informational string.
        g = self._fv_with("low")
        assert g["final_verifier_report.json"]["token_actual_summary"] is None
        assert _ok(g) is True

    def test_unknown_summary_field_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_actual_summary"]["surprise"] = 1
        g["final_verifier_report.json"]["token_measurement"]["actual_summary"]["surprise"] = 1
        assert _ok(g) is False

    def test_wrong_summary_scalar_type_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_actual_summary"]["actual_prompt_tokens"] = "100"
        g["final_verifier_report.json"]["token_measurement"]["actual_summary"]["actual_prompt_tokens"] = "100"
        assert _ok(g) is False

    def test_bool_cost_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_actual_summary"]["total_cost_usd"] = True
        g["final_verifier_report.json"]["token_measurement"]["actual_summary"]["total_cost_usd"] = True
        assert _ok(g) is False

    def test_missing_required_summary_field_blocks(self):
        g = self._fv_with("high")
        del g["final_verifier_report.json"]["token_actual_summary"]["actual_model_verified"]
        del g["final_verifier_report.json"]["token_measurement"]["actual_summary"]["actual_model_verified"]
        assert _ok(g) is False

    def test_top_and_nested_summary_contradiction_blocks(self):
        g = self._fv_with("high")
        # top-level summary null while the nested block carries one — a forged view.
        g["final_verifier_report.json"]["token_actual_summary"] = None
        assert _ok(g) is False

    def test_note_contradiction_blocks(self):
        g = self._fv_with("low")
        g["final_verifier_report.json"]["token_measurement_note"] = "different note"
        assert _ok(g) is False
