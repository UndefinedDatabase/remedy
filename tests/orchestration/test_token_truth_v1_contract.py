"""F2 (round 34) — the COMPLETE TokenTruthV1 input + output contract.

The producer strictly validates its provider_evidence/token_accounting inputs (a malformed field is a
bounded ``TokenEvidenceError`` — never clamped or ``int()``-coerced), and ``validate_token_truth`` is a
closed, fully-typed output schema with every state invariant. This suite proves: every legitimate real
producer state validates; every malformed input fails BEFORE a TokenTruthV1 is accepted; and every
internally-incoherent output the reproductions describe is blocked.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.token_authority import validate_token_truth
from packages.orchestration.token_truth import TokenEvidenceError, build_token_truth


def _seed(base: Path, tid: str, acc: dict, pe: dict) -> None:
    d = base / "task_runs" / tid
    d.mkdir(parents=True, exist_ok=True)
    (d / "token_accounting.json").write_text(json.dumps(acc))
    (d / "provider_evidence.json").write_text(json.dumps(pe))


def _complete_actuals_pe(**over) -> dict:
    pe = {"schema_version": "1.0.0",
          "task_id": "T001", "execution_mode": "provider_backed", "provider_call_count": 1,
          "actual_call_count": 1, "cost_call_count": 1, "actual_prompt_tokens": 10,
          "actual_completion_tokens": 5, "actual_total_tokens": 15,
          "actual_cache_creation_tokens": 3, "actual_cache_read_tokens": 2,
          "total_cost_usd": 0.01, "actual_model_verified": True, "builder_actual_model": "claude-x",
          "builder_provider": "claude"}
    pe.update(over)
    return pe


def _valid_high_truth(tmp_path: Path) -> dict:
    _seed(tmp_path, "T001", {"task_id": "T001", "builder_prompt_tokens_estimated": 0},
          _complete_actuals_pe())
    t = build_token_truth(str(tmp_path))
    assert validate_token_truth(t) == [], validate_token_truth(t)
    return t


# --------------------------------------------------------------------------- valid producer states
class TestValidProducerStates:
    def test_zero_provider_manual(self, tmp_path):
        _seed(tmp_path, "T001", {"kind": "manual", "reason": "manual"},
              {"schema_version": "1.0.0", "execution_mode": "manual_operator_repair",
               "provider_call_count": 0})
        assert validate_token_truth(build_token_truth(str(tmp_path))) == []

    def test_provider_without_usage(self, tmp_path):
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 5},
              {"schema_version": "1.0.0", "execution_mode": "provider_backed",
               "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0})
        assert validate_token_truth(build_token_truth(str(tmp_path))) == []

    def test_complete_actuals_and_cost_with_cache_and_model(self, tmp_path):
        t = _valid_high_truth(tmp_path)
        assert t["measurement_confidence"] == "high"
        assert t["actual_cache_creation_tokens"] == 3 and t["actual_cache_read_tokens"] == 2
        assert t["actual_model_verified"] is True and t["builder_actual_model"] == "claude-x"

    def test_complete_actuals_missing_cost(self, tmp_path):
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0},
              _complete_actuals_pe(cost_call_count=0, total_cost_usd=None))
        t = build_token_truth(str(tmp_path))
        assert t["total_cost_usd"] is None and t["cost_coverage_complete"] is False
        assert validate_token_truth(t) == []

    def test_mixed_coverage(self, tmp_path):
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0}, _complete_actuals_pe(
            cost_call_count=0, total_cost_usd=None))
        _seed(tmp_path, "T002", {"builder_prompt_tokens_estimated": 3},
              {"schema_version": "1.0.0", "execution_mode": "provider_backed",
               "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0})
        t = build_token_truth(str(tmp_path))
        assert t["measurement_confidence"] == "mixed"
        assert validate_token_truth(t) == []


# --------------------------------------------------------------------- malformed INPUT → producer err
_BAD_PE = {
    "negative_cache_creation": _complete_actuals_pe(actual_cache_creation_tokens=-5),
    "negative_cache_read": _complete_actuals_pe(actual_cache_read_tokens=-1),
    "boolean_call_count": _complete_actuals_pe(actual_call_count=True),
    "float_token_count": _complete_actuals_pe(actual_prompt_tokens=10.5),
    "string_provider_count": _complete_actuals_pe(provider_call_count="2"),
    "actual_exceeds_provider": _complete_actuals_pe(actual_call_count=2, provider_call_count=1),
    "cost_exceeds_actual": _complete_actuals_pe(cost_call_count=2, actual_call_count=1),
    "nonbool_model_verified": _complete_actuals_pe(actual_model_verified="yes"),
    "inconsistent_actual_total": _complete_actuals_pe(actual_total_tokens=999),
    "nonfinite_cost": _complete_actuals_pe(total_cost_usd=float("inf")),
    "negative_cost": _complete_actuals_pe(total_cost_usd=-0.5),
    "boolean_token": _complete_actuals_pe(actual_prompt_tokens=True),
    "cost_without_cost_call_count": {
        "schema_version": "1.0.0",
        "task_id": "T001", "execution_mode": "provider_backed", "provider_call_count": 1,
        "actual_call_count": 1, "actual_prompt_tokens": 10, "actual_completion_tokens": 5,
        "actual_total_tokens": 15, "total_cost_usd": 0.25},
    "ambiguous_actual_model": {
        "schema_version": "1.0.0",
        "task_id": "T001", "execution_mode": "provider_backed", "provider_call_count": 1,
        "actual_call_count": 0, "cost_call_count": 0,
        "actual_model": "claude-x", "actual_model_verified": True},
    "verified_model_zero_provider_calls": {
        "schema_version": "1.0.0",
        "task_id": "T001", "execution_mode": "provider_backed", "provider_call_count": 0,
        "actual_call_count": 0, "cost_call_count": 0,
        "actual_model_verified": True, "builder_actual_model": "claude-x"},
    "missing_schema_version": {
        "execution_mode": "provider_backed", "provider_call_count": 0,
        "actual_call_count": 0, "cost_call_count": 0},
    "wrong_schema_version": {
        "schema_version": "999.0", "execution_mode": "provider_backed",
        "provider_call_count": 0, "actual_call_count": 0, "cost_call_count": 0},
    "unknown_trust_bearing_field": {
        "schema_version": "1.0.0", "execution_mode": "provider_backed",
        "provider_call_count": 0, "actual_call_count": 0, "cost_call_count": 0,
        "claimed_actual_cost_usd": 999},
    "unknown_execution_mode": {
        "schema_version": "1.0.0", "execution_mode": "banana",
        "provider_call_count": 0, "actual_call_count": 0, "cost_call_count": 0},
    "missing_provider_call_count": {
        "schema_version": "1.0.0", "execution_mode": "provider_backed",
        "actual_call_count": 0, "cost_call_count": 0},
}


class TestMalformedInputIsProducerError:
    @pytest.mark.parametrize("name", sorted(_BAD_PE))
    def test_producer_raises(self, tmp_path, name):
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0}, _BAD_PE[name])
        with pytest.raises(TokenEvidenceError):
            build_token_truth(str(tmp_path))

    def test_negative_estimated_is_producer_error(self, tmp_path):
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": -3},
              {"schema_version": "1.0.0", "execution_mode": "provider_backed",
               "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0})
        with pytest.raises(TokenEvidenceError):
            build_token_truth(str(tmp_path))


# -------------------------------------------------------- strict raw JSON decoding (round 35 F2)
class TestStrictRawJsonDecoding:
    """Round 35 F2: _read_json uses strict_loads — duplicate keys, NaN, Infinity, invalid UTF-8, and
    wrong root types in token_accounting/provider_evidence/prompt_trace_summary raise
    TokenEvidenceError (present-invalid), while genuinely absent files degrade to None."""

    def _base(self, tmp_path, tid="T001"):
        d = tmp_path / "task_runs" / tid
        d.mkdir(parents=True, exist_ok=True)
        return d

    def test_duplicate_key_in_token_accounting_raises(self, tmp_path):
        d = self._base(tmp_path)
        (d / "token_accounting.json").write_text(
            '{"builder_prompt_tokens_estimated": 0, "builder_prompt_tokens_estimated": 1}')
        (d / "provider_evidence.json").write_text('{}')
        with pytest.raises(TokenEvidenceError, match="duplicate"):
            build_token_truth(str(tmp_path))

    def test_nan_in_provider_evidence_raises(self, tmp_path):
        d = self._base(tmp_path)
        (d / "token_accounting.json").write_text('{"builder_prompt_tokens_estimated": 0}')
        (d / "provider_evidence.json").write_text('{"total_cost_usd": NaN}')
        with pytest.raises(TokenEvidenceError, match="non-standard|malformed"):
            build_token_truth(str(tmp_path))

    def test_infinity_in_provider_evidence_raises(self, tmp_path):
        d = self._base(tmp_path)
        (d / "token_accounting.json").write_text('{"builder_prompt_tokens_estimated": 0}')
        (d / "provider_evidence.json").write_text('{"total_cost_usd": Infinity}')
        with pytest.raises(TokenEvidenceError, match="non-standard|malformed"):
            build_token_truth(str(tmp_path))

    def test_invalid_utf8_raises(self, tmp_path):
        d = self._base(tmp_path)
        (d / "token_accounting.json").write_bytes(b'{"builder_prompt_tokens_estimated": \xff}')
        (d / "provider_evidence.json").write_text('{}')
        with pytest.raises(TokenEvidenceError, match="UTF-8|malformed"):
            build_token_truth(str(tmp_path))

    def test_malformed_json_raises(self, tmp_path):
        d = self._base(tmp_path)
        (d / "token_accounting.json").write_text('{bad json}')
        (d / "provider_evidence.json").write_text('{}')
        with pytest.raises(TokenEvidenceError, match="malformed"):
            build_token_truth(str(tmp_path))

    def test_absent_files_degrade_gracefully(self, tmp_path):
        """Genuinely absent token_accounting/provider_evidence files degrade to empty — no error."""
        d = self._base(tmp_path)
        # Only create the directory, no files inside
        report = build_token_truth(str(tmp_path))
        assert report["per_task"]["T001"]["builder_estimated"] == 0

    def test_duplicate_key_in_prompt_trace_raises(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text(
            '{"total_prompts": 1, "total_prompts": 2}')
        with pytest.raises(TokenEvidenceError, match="duplicate"):
            build_token_truth(str(tmp_path))

    def test_bool_prompt_trace_count_raises(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text('{"total_prompts": true}')
        with pytest.raises(TokenEvidenceError, match="nonnegative integer"):
            build_token_truth(str(tmp_path))

    def test_float_prompt_trace_count_raises(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text('{"total_prompts": 1.5}')
        with pytest.raises(TokenEvidenceError, match="nonnegative integer"):
            build_token_truth(str(tmp_path))

    def test_string_prompt_trace_count_raises(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text('{"total_prompts": "3"}')
        with pytest.raises(TokenEvidenceError, match="nonnegative integer"):
            build_token_truth(str(tmp_path))


# ---------------------------------------------------------------- incoherent OUTPUT → validator blocks
class TestOutputInvariantsBlock:
    def _t(self, tmp_path):
        return _valid_high_truth(tmp_path)

    def test_verified_model_without_identity(self, tmp_path):
        t = self._t(tmp_path); t["builder_actual_model"] = None; t["reviewer_actual_model"] = None
        assert any("actual_model_verified is true but no actual model" in x
                   for x in validate_token_truth(t))

    def test_model_without_verification(self, tmp_path):
        t = self._t(tmp_path); t["actual_model_verified"] = False
        assert any("actual_model_verified is false" in x for x in validate_token_truth(t))

    def test_cost_complete_null_cost(self, tmp_path):
        t = self._t(tmp_path); t["total_cost_usd"] = None
        assert any("cost_coverage_complete is true but total_cost_usd is null" in x
                   for x in validate_token_truth(t))

    def test_total_cost_with_zero_cost_calls(self, tmp_path):
        t = self._t(tmp_path); t["cost_call_count"] = 0; t["cost_coverage_complete"] = False
        t["cost_coverage_reason"] = "missing_provider_cost"
        assert any("cost_call_count is 0" in x for x in validate_token_truth(t))

    def test_cost_exceeds_actual(self, tmp_path):
        t = self._t(tmp_path); t["cost_call_count"] = 5
        assert any("cost_call_count > actual_call_count" in x for x in validate_token_truth(t))

    def test_actual_exceeds_provider(self, tmp_path):
        t = self._t(tmp_path); t["actual_call_count"] = 9
        assert any("actual_call_count > provider_call_count" in x for x in validate_token_truth(t))

    def test_coverage_flag_inconsistent(self, tmp_path):
        t = self._t(tmp_path); t["actual_coverage_complete"] = False
        assert any("actual_coverage_complete disagrees" in x for x in validate_token_truth(t))

    def test_high_with_incomplete_totals(self, tmp_path):
        t = self._t(tmp_path); t["actual_total_tokens"] = None
        probs = validate_token_truth(t)
        assert any("requires complete actual token totals" in x for x in probs)

    def test_mixed_with_no_actual_coverage(self, tmp_path):
        t = self._t(tmp_path)
        t.update({"measurement_confidence": "mixed",
                  "measurement_source": "mixed_provider_actuals_and_heuristic",
                  "actual_available": False})
        assert any("'mixed' but no actual usage" in x for x in validate_token_truth(t))

    def test_low_with_actual_usage(self, tmp_path):
        t = self._t(tmp_path)
        t.update({"measurement_confidence": "low", "measurement_source": "character_heuristic"})
        assert any("'low' but actual usage is present" in x for x in validate_token_truth(t))

    def test_unknown_field_blocks(self, tmp_path):
        t = self._t(tmp_path); t["surprise"] = 1
        assert any("unknown fields" in x for x in validate_token_truth(t))

    def test_missing_field_blocks(self, tmp_path):
        t = self._t(tmp_path); del t["provider"]
        assert any("missing required fields" in x for x in validate_token_truth(t))

    def test_negative_cache_in_output_blocks(self, tmp_path):
        t = self._t(tmp_path); t["actual_cache_creation_tokens"] = -1
        assert any("actual_cache_creation_tokens" in x for x in validate_token_truth(t))

    def test_reason_null_while_incomplete(self, tmp_path):
        t = self._t(tmp_path)
        t.update({"cost_call_count": 0, "cost_coverage_complete": False,
                  "cost_coverage_reason": None, "total_cost_usd": None})
        assert any("cost_coverage_reason must be a nonempty string" in x
                   for x in validate_token_truth(t))

    def test_malformed_per_task_blocks(self, tmp_path):
        t = self._t(tmp_path)
        t["per_task"] = {"T001": {"role": "builder"}}       # missing closed fields
        assert any("per_task" in x for x in validate_token_truth(t))

    def test_per_task_sum_disagreement_blocks(self, tmp_path):
        t = self._t(tmp_path)
        # inflate the aggregate away from the per_task sum
        t["builder_estimated_total"] = t["builder_estimated_total"] + 100
        assert any("builder_estimated_total" in x and "sum of per_task" in x
                   for x in validate_token_truth(t))


class TestPackagingAuthorityBlocksMalformedInput:
    """Malformed task/provider token Evidence → the token-truth producer raises → the packaging
    authority reports PRODUCER_ERROR (which forces BLOCKED_EVIDENCE), never a false VERIFIED_EQUAL."""

    def test_producer_error_at_authority(self, tmp_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "_brm_tt", Path(__file__).resolve().parents[2] / "scripts" / "build_review_manifest.py")
        brm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(brm)
        # A bundle carrying a token_truth.json but whose task evidence is malformed.
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0},
              _complete_actuals_pe(actual_cache_creation_tokens=-5))
        (tmp_path / "token_truth.json").write_text(json.dumps({"schema_version": "1.0.0"}))
        ev = brm._view_from_dir(str(tmp_path))
        res = brm._token_truth_authority(ev)
        assert res["status"] == "PRODUCER_ERROR", res


class TestProducerDerivesMissingTotal:
    """Round 35 F3: when prompt and completion are present but total is absent, the producer derives
    actual_total_tokens = prompt + completion rather than emitting null (which would be invalid at
    high confidence)."""

    def test_prompt_completion_without_total_derives(self, tmp_path):
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0},
              {"schema_version": "1.0.0", "execution_mode": "provider_backed",
               "provider_call_count": 1,
               "actual_call_count": 1, "cost_call_count": 1, "total_cost_usd": 0.01,
               "actual_prompt_tokens": 10, "actual_completion_tokens": 5,
               "builder_provider": "claude"})
        t = build_token_truth(str(tmp_path))
        assert t["actual_total_tokens"] == 15
        assert t["measurement_confidence"] == "high"
        assert validate_token_truth(t) == []


class TestCacheOnlyNotHigh:
    """Round 35 F3: cache-only evidence (only cache_creation/cache_read, no prompt/completion/total)
    is supplementary metadata — it must not trigger high confidence."""

    def test_cache_only_is_not_high(self, tmp_path):
        """Cache-only evidence (only cache_creation/cache_read, no prompt/completion/total) is
        treated as no-actual-usage — low confidence, actual_available=False."""
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0},
              {"schema_version": "1.0.0", "execution_mode": "provider_backed",
               "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0,
               "actual_cache_creation_tokens": 5, "actual_cache_read_tokens": 3,
               "builder_provider": "claude"})
        t = build_token_truth(str(tmp_path))
        assert t["measurement_confidence"] == "low"
        assert t["actual_available"] is False
        assert validate_token_truth(t) == []


class TestNonStringModelIdentityBlocks:
    """Round 35 F3: a non-string model identity (int, bool, list) in provider_evidence is a
    producer error — not silently accepted."""

    def test_integer_builder_model_raises(self, tmp_path):
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0},
              _complete_actuals_pe(builder_actual_model=123))
        with pytest.raises(TokenEvidenceError, match="not a string"):
            build_token_truth(str(tmp_path))

    def test_list_reviewer_model_raises(self, tmp_path):
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0},
              {**_complete_actuals_pe(), "reviewer_actual_model": ["m"]})
        with pytest.raises(TokenEvidenceError, match="not a string"):
            build_token_truth(str(tmp_path))


class TestAuthorityValidatesBothOutputs:
    """Round 35 F4: _token_truth_authority validates BOTH canonical and supplied before declaring
    VERIFIED_EQUAL. An invalid canonical → PRODUCER_ERROR; an invalid supplied → MISMATCH."""

    def _brm(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "_brm_tt", Path(__file__).resolve().parents[2] / "scripts" / "build_review_manifest.py")
        brm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(brm)
        return brm

    def test_invalid_supplied_is_mismatch(self, tmp_path):
        brm = self._brm()
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0}, _complete_actuals_pe())
        # Build valid token truth, then corrupt the supplied copy
        t = build_token_truth(str(tmp_path))
        t["surprise_field"] = True  # unknown field → invalid
        (tmp_path / "token_truth.json").write_text(json.dumps(t))
        ev = brm._view_from_dir(str(tmp_path))
        res = brm._token_truth_authority(ev)
        assert res["status"] == "MISMATCH", res
        assert any("invalid" in p for p in res["problems"])

    def test_valid_equal_is_verified_equal(self, tmp_path):
        brm = self._brm()
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0}, _complete_actuals_pe())
        t = build_token_truth(str(tmp_path))
        (tmp_path / "token_truth.json").write_text(json.dumps(t))
        ev = brm._view_from_dir(str(tmp_path))
        res = brm._token_truth_authority(ev)
        assert res["status"] == "VERIFIED_EQUAL", res


class TestTypedRootContract:
    """Round 36 F3: a present token Evidence file with a non-object root (null, list, string, number,
    Boolean) is PRESENT_INVALID and raises TokenEvidenceError — never treated as absent."""

    def _base(self, tmp_path, tid="T001"):
        d = tmp_path / "task_runs" / tid
        d.mkdir(parents=True, exist_ok=True)
        return d

    @pytest.mark.parametrize("root", ["[]", "null", '"string"', "42", "true"])
    def test_provider_evidence_non_object_raises(self, tmp_path, root):
        d = self._base(tmp_path)
        (d / "token_accounting.json").write_text('{"builder_prompt_tokens_estimated": 0}')
        (d / "provider_evidence.json").write_text(root)
        with pytest.raises(TokenEvidenceError, match="not an object"):
            build_token_truth(str(tmp_path))

    @pytest.mark.parametrize("root", ["[]", "null", '"string"', "42", "true"])
    def test_token_accounting_non_object_raises(self, tmp_path, root):
        d = self._base(tmp_path)
        (d / "token_accounting.json").write_text(root)
        (d / "provider_evidence.json").write_text("{}")
        with pytest.raises(TokenEvidenceError, match="not an object"):
            build_token_truth(str(tmp_path))

    @pytest.mark.parametrize("root", ["[]", "null", '"string"', "42", "true"])
    def test_prompt_trace_non_object_raises(self, tmp_path, root):
        (tmp_path / "prompt_trace_summary.json").write_text(root)
        with pytest.raises(TokenEvidenceError, match="not an object"):
            build_token_truth(str(tmp_path))

    def test_read_error_is_present_invalid(self, tmp_path):
        """A directory at the expected file path is a read error, not absent."""
        d = self._base(tmp_path)
        (d / "token_accounting.json").mkdir()
        (d / "provider_evidence.json").write_text("{}")
        with pytest.raises(TokenEvidenceError, match="cannot read"):
            build_token_truth(str(tmp_path))


class TestScalarCoercionBlocked:
    """Round 36 F4: trust-bearing provider/model values must be actual strings — ``str()`` coercion
    of non-string types is a producer error."""

    _SCALAR_MUTATIONS = [
        ("builder_provider", 123),
        ("builder_provider", True),
        ("builder_provider", ["forged"]),
        ("provider", 123),
        ("model", ["forged"]),
        ("model", 42),
        ("builder_model", True),
        ("builder_configured_model", 123),
        ("reviewer_configured_model", False),
        ("cli_version", 42),
    ]

    @pytest.mark.parametrize("field,val", _SCALAR_MUTATIONS, ids=[f"{f}={v!r}" for f, v in _SCALAR_MUTATIONS])
    def test_non_string_identity_raises(self, tmp_path, field, val):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0}
        pe[field] = val
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0}, pe)
        with pytest.raises(TokenEvidenceError, match="not a string"):
            build_token_truth(str(tmp_path))

    def test_non_string_actual_missing_reason_raises(self, tmp_path):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0,
              "actual_missing_reasons": [123]}
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0}, pe)
        with pytest.raises(TokenEvidenceError, match="not a list of strings"):
            build_token_truth(str(tmp_path))

    def test_usage_non_object_raises(self, tmp_path):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0,
              "usage": [1, 2, 3]}
        _seed(tmp_path, "T001", {"builder_prompt_tokens_estimated": 0}, pe)
        with pytest.raises(TokenEvidenceError, match="usage is not an object"):
            build_token_truth(str(tmp_path))

    def test_non_string_role_raises(self, tmp_path):
        d = tmp_path / "task_runs" / "T001"
        d.mkdir(parents=True)
        (d / "token_accounting.json").write_text('{"role": 123, "builder_prompt_tokens_estimated": 0}')
        with pytest.raises(TokenEvidenceError, match="not a string"):
            build_token_truth(str(tmp_path))

    def test_non_string_configured_model_raises(self, tmp_path):
        d = tmp_path / "task_runs" / "T001"
        d.mkdir(parents=True)
        (d / "token_accounting.json").write_text('{"configured_model": 42, "builder_prompt_tokens_estimated": 0}')
        with pytest.raises(TokenEvidenceError, match="not a string"):
            build_token_truth(str(tmp_path))


class TestSemanticProviderEvidenceContract:
    """Round 37 F3: contradictory provider evidence raises TokenEvidenceError — never silently
    normalized. Each test proves one exact contradiction → PRODUCER_ERROR → BLOCKED_EVIDENCE."""

    _ACC = {"builder_prompt_tokens_estimated": 0}

    def test_verified_true_without_model_identity(self, tmp_path):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0,
              "actual_model_verified": True}
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="actual_model_verified=true but no actual model"):
            build_token_truth(str(tmp_path))

    def test_model_identity_without_verified(self, tmp_path):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0,
              "builder_actual_model": "claude-x", "actual_model_verified": False}
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="actual model identity present but actual_model_verified is not true"):
            build_token_truth(str(tmp_path))

    def test_model_identity_without_verified_field(self, tmp_path):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0,
              "reviewer_actual_model": "claude-y"}
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="actual model identity present"):
            build_token_truth(str(tmp_path))

    def test_cost_present_but_cost_call_count_zero(self, tmp_path):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1,
              "actual_call_count": 1, "cost_call_count": 0, "total_cost_usd": 0.05,
              "actual_prompt_tokens": 10, "actual_completion_tokens": 5, "actual_total_tokens": 15,
              "actual_model_verified": True, "builder_actual_model": "claude-x"}
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="total_cost_usd present.*cost_call_count is 0"):
            build_token_truth(str(tmp_path))

    def test_actual_counters_with_actual_call_count_zero(self, tmp_path):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1,
              "actual_call_count": 0, "cost_call_count": 0,
              "actual_prompt_tokens": 10, "actual_completion_tokens": 5}
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="actual_call_count=0 but actual token counters present"):
            build_token_truth(str(tmp_path))

    def test_valid_zero_calls_zero_counters_passes(self, tmp_path):
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 0, "actual_call_count": 0, "cost_call_count": 0}
        _seed(tmp_path, "T001", self._ACC, pe)
        t = build_token_truth(str(tmp_path))
        assert validate_token_truth(t) == []

    def test_valid_model_with_verified_passes(self, tmp_path):
        _seed(tmp_path, "T001", self._ACC, _complete_actuals_pe())
        t = build_token_truth(str(tmp_path))
        assert validate_token_truth(t) == []

    def test_actual_model_field_rejected_as_ambiguous(self, tmp_path):
        """Round 38 F2 / Round 39: actual_model rejected — closed schema excludes it."""
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0,
              "actual_model": "claude-z"}
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="unknown fields"):
            build_token_truth(str(tmp_path))

    def test_cost_without_cost_call_count_raises(self, tmp_path):
        """Round 38 F1 / Round 39: cost_call_count required for provider_backed."""
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 1,
              "actual_call_count": 1, "actual_prompt_tokens": 10, "actual_completion_tokens": 5,
              "actual_total_tokens": 15, "total_cost_usd": 0.25}
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="cost_call_count.*missing"):
            build_token_truth(str(tmp_path))

    def test_verified_model_with_zero_provider_calls_raises(self, tmp_path):
        """Round 38 F3: actual_model_verified=true with provider_call_count=0 is contradictory."""
        pe = {"schema_version": "1.0.0", "execution_mode": "provider_backed",
              "provider_call_count": 0,
              "actual_call_count": 0, "cost_call_count": 0,
              "actual_model_verified": True, "builder_actual_model": "claude-x"}
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="actual_model_verified=true but provider_call_count is 0"):
            build_token_truth(str(tmp_path))

    def test_actual_model_with_verified_and_cost_call_count(self, tmp_path):
        """Round 38 F2 / Round 39: actual_model rejected — closed schema excludes it."""
        pe = _complete_actuals_pe(actual_model="claude-z")
        _seed(tmp_path, "T001", self._ACC, pe)
        with pytest.raises(TokenEvidenceError, match="unknown fields"):
            build_token_truth(str(tmp_path))


class TestMetaRegression:
    """Every valid producer fixture validates; a representative malformed input never yields an
    accepted TokenTruthV1 (it raises before one is produced)."""

    def test_all_valid_states_validate_and_all_malformed_raise(self, tmp_path):
        (tmp_path / "ok").mkdir()
        _seed(tmp_path / "ok", "T001", {"builder_prompt_tokens_estimated": 0}, _complete_actuals_pe())
        assert validate_token_truth(build_token_truth(str(tmp_path / "ok"))) == []
        for i, (name, pe) in enumerate(sorted(_BAD_PE.items())):
            d = tmp_path / f"bad{i}"
            d.mkdir()
            _seed(d, "T001", {"builder_prompt_tokens_estimated": 0}, pe)
            with pytest.raises(TokenEvidenceError):
                build_token_truth(str(d))
