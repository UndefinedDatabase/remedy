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
        # The FULL 25-field token_status (F1 round 28: token_measurement projects it, so the two must
        # agree). Start from the low default and overlay real measured values for high/mixed.
        ts = _E2E._token_status()
        ts.update({"measurement_confidence": confidence, "measurement_source": "provider_api",
                   "actual_prompt_tokens": 100, "actual_completion_tokens": 50,
                   "actual_total_tokens": 150, "total_cost_usd": 0.01, "cost_call_count": 2,
                   "cost_coverage_complete": True, "cost_coverage_reason": "ok",
                   "provider_call_count": 2, "actual_call_count": 2, "actual_coverage_complete": True,
                   "actual_missing_reasons": None, "cli_version": "1.2.3",
                   "configured_models": {"builder": "c", "reviewer": "c"},
                   "actual_models": {"builder": "c", "reviewer": "c"}, "actual_model_verified": True})
        return ts

    def _fv_with(self, confidence):
        from packages.orchestration.final_verifier import _token_measurement_summary
        ts = self._ts(confidence)
        tm = _token_measurement_summary(ts)
        g = _gates()
        fv = g["final_verifier_report.json"]
        fv["token_status"] = copy.deepcopy(ts)             # authoritative source the projections copy
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

    # --- F1 (round 28): token_status is authoritative; each projection must equal it. ---
    def test_provider_call_count_projection_mismatch_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_status"]["provider_call_count"] = 999
        assert _ok(g) is False

    def test_actual_total_tokens_projection_mismatch_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_status"]["actual_total_tokens"] = 42
        assert _ok(g) is False

    def test_total_cost_usd_projection_mismatch_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_status"]["total_cost_usd"] = 9.99
        assert _ok(g) is False

    def test_actual_models_projection_mismatch_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_status"]["actual_models"] = {"builder": "x",
                                                                            "reviewer": "x"}
        assert _ok(g) is False

    def test_actual_coverage_complete_projection_mismatch_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_status"]["actual_coverage_complete"] = False
        assert _ok(g) is False

    def test_measurement_source_projection_mismatch_blocks(self):
        g = self._fv_with("high")
        g["final_verifier_report.json"]["token_measurement"]["measurement_source"] = "different"
        assert _ok(g) is False

    def test_low_null_summary_no_projection_block(self):
        # low confidence: actual_summary is null, so no summary-field projection is checked.
        assert _ok(self._fv_with("low")) is True

    # --- F1 (round 29): the whole block must be REPRODUCIBLE from the one shared producer, so the
    # impossible confidence/summary/note combinations the field-list check missed now block. ---
    def test_packaged_block_equals_a_fresh_producer_rebuild(self):
        from packages.orchestration.token_measurement import token_measurement_summary
        for conf in ("high", "mixed", "low"):
            g = self._fv_with(conf)
            fv = g["final_verifier_report.json"]
            assert fv["token_measurement"] == token_measurement_summary(fv["token_status"])
            assert _ok(g) is True

    def test_high_confidence_with_null_summary_blocks(self):
        g = self._fv_with("high")
        fv = g["final_verifier_report.json"]
        fv["token_measurement"]["actual_summary"] = None
        fv["token_actual_summary"] = None
        assert _ok(g) is False

    def test_mixed_confidence_with_null_summary_blocks(self):
        g = self._fv_with("mixed")
        fv = g["final_verifier_report.json"]
        fv["token_measurement"]["actual_summary"] = None
        fv["token_actual_summary"] = None
        assert _ok(g) is False

    def test_low_confidence_with_fabricated_summary_blocks(self):
        g = self._fv_with("low")
        fv = g["final_verifier_report.json"]
        fake = {"measurement_confidence": "low"}
        fv["token_measurement"]["actual_summary"] = fake
        fv["token_actual_summary"] = fake
        assert _ok(g) is False

    def test_arbitrary_matching_note_blocks_when_low(self):
        # A note that matches top+nested but is NOT the producer's low-confidence note blocks.
        g = self._fv_with("low")
        fv = g["final_verifier_report.json"]
        fv["token_measurement"]["measurement_note"] = "arbitrary but consistent"
        fv["token_measurement_note"] = "arbitrary but consistent"
        assert _ok(g) is False

    def test_arbitrary_matching_note_blocks_when_high(self):
        # High confidence's producer note is null; a matching non-null note on both views blocks.
        g = self._fv_with("high")
        fv = g["final_verifier_report.json"]
        fv["token_measurement"]["measurement_note"] = "informational"
        fv["token_measurement_note"] = "informational"
        assert _ok(g) is False
