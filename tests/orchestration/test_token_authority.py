"""F2 (round 31) — token_truth is a validated authority. An empty / whitespace / malformed /
wrong-root / enum-violating / incoherent token truth is rejected; the deterministic zero-provider
manual token truth is accepted and drives the producer's token_status."""
from __future__ import annotations

from packages.orchestration.manual_attestation import MANUAL_TOKEN_TRUTH
from packages.orchestration.token_authority import validate_token_truth
from packages.orchestration.token_measurement import token_measurement_summary


class TestTokenTruthValidator:
    def test_manual_token_truth_is_valid(self):
        assert validate_token_truth(MANUAL_TOKEN_TRUTH) == []

    def test_non_object_and_empty(self):
        assert validate_token_truth(None)
        assert validate_token_truth([])
        assert validate_token_truth("")
        assert validate_token_truth({}) == ["token_truth.json is empty"]

    def test_wrong_schema_version(self):
        t = dict(MANUAL_TOKEN_TRUTH); t["schema_version"] = "9.9.9"
        assert any("schema_version" in x for x in validate_token_truth(t))

    def test_bad_confidence_enum(self):
        t = dict(MANUAL_TOKEN_TRUTH); t["measurement_confidence"] = "banana"
        assert any("measurement_confidence" in x for x in validate_token_truth(t))

    def test_bad_source_enum(self):
        t = dict(MANUAL_TOKEN_TRUTH); t["measurement_source"] = "psychic"
        assert any("measurement_source" in x for x in validate_token_truth(t))

    def test_boolean_count_rejected(self):
        t = dict(MANUAL_TOKEN_TRUTH); t["provider_call_count"] = True
        assert any("provider_call_count" in x for x in validate_token_truth(t))

    def test_negative_count_rejected(self):
        t = dict(MANUAL_TOKEN_TRUTH); t["actual_call_count"] = -1
        assert any("actual_call_count" in x for x in validate_token_truth(t))

    def test_negative_cost_rejected(self):
        t = dict(MANUAL_TOKEN_TRUTH); t["total_cost_usd"] = -0.5
        assert any("total_cost_usd" in x for x in validate_token_truth(t))

    def test_infinite_cost_rejected(self):
        t = dict(MANUAL_TOKEN_TRUTH); t["total_cost_usd"] = float("inf")
        assert any("total_cost_usd" in x for x in validate_token_truth(t))

    def test_totals_incoherent_rejected(self):
        t = dict(MANUAL_TOKEN_TRUTH)
        t.update({"measurement_confidence": "high", "measurement_source": "provider_actuals",
                  "actual_available": True, "actual_call_count": 2, "provider_call_count": 2,
                  "actual_prompt_tokens": 100, "actual_completion_tokens": 50,
                  "actual_total_tokens": 999})
        assert any("actual_total_tokens" in x for x in validate_token_truth(t))

    def test_available_without_call_rejected(self):
        t = dict(MANUAL_TOKEN_TRUTH)
        t.update({"actual_available": True, "actual_call_count": 0})
        assert any("actual_available is true but actual_call_count is 0" in x
                   for x in validate_token_truth(t))

    def test_actual_tokens_present_while_unavailable_rejected(self):
        t = dict(MANUAL_TOKEN_TRUTH); t["actual_prompt_tokens"] = 10
        assert any("actual_prompt_tokens" in x for x in validate_token_truth(t))

    def test_measured_provider_truth_is_valid_and_coherent(self):
        # A COMPLETE, coherent high-confidence measured TokenTruthV1 (round 34: coverage flags, cost
        # coverage and missing_reason must all agree with the counts).
        t = dict(MANUAL_TOKEN_TRUTH)
        t.update({"measurement_confidence": "high", "measurement_source": "provider_actuals",
                  "actual_available": True, "actual_call_count": 2, "provider_call_count": 2,
                  "cost_call_count": 2, "actual_prompt_tokens": 100, "actual_completion_tokens": 50,
                  "actual_total_tokens": 150, "total_cost_usd": 0.01,
                  "actual_coverage_complete": True, "cost_coverage_complete": True,
                  "cost_coverage_reason": None, "missing_reason": None})
        assert validate_token_truth(t) == [], validate_token_truth(t)
        # And the shared producer derives a non-null summary from it.
        assert token_measurement_summary(t)["actual_summary"] is not None
