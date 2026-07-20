"""F3 (round 33) — the token-truth PRODUCER and VALIDATOR share one schema, so every legitimate output
of build_token_truth validates. This meta-regression drives the real producer across its emitted states
(heuristic-only, complete provider actuals, mixed, provider-calls-without-usage, zero-provider manual)
and proves validate_token_truth accepts each; it also re-runs every test_token_truth scenario's producer
output through the validator to prevent future enum drift.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from packages.orchestration.token_truth import (
    MEASUREMENT_SOURCES, build_token_truth,
)
from packages.orchestration.token_authority import validate_token_truth

REPO_ROOT = Path(__file__).resolve().parents[2]
_tt = importlib.util.spec_from_file_location(
    "_tt_fixtures", REPO_ROOT / "tests" / "orchestration" / "test_token_truth.py")
_TT = importlib.util.module_from_spec(_tt); _tt.loader.exec_module(_TT)


def _seed(base: Path, tid: str, acc: dict, pe: dict):
    d = base / "task_runs" / tid
    d.mkdir(parents=True, exist_ok=True)
    (d / "token_accounting.json").write_text(json.dumps(acc))
    (d / "provider_evidence.json").write_text(json.dumps(pe))


class TestProducerOutputAlwaysValidates:
    def test_producer_sources_are_exactly_the_validator_sources(self):
        # The exact strings build_token_truth can emit are the validator's accepted set — no drift.
        assert MEASUREMENT_SOURCES == frozenset(
            {"character_heuristic", "provider_actuals", "mixed_provider_actuals_and_heuristic"})

    def test_manual_zero_provider(self, tmp_path):
        _seed(tmp_path, "T001", {"task_id": "T001", "kind": "manual", "reason": "manual"},
              {"schema_version": "1.0.0", "task_id": "T001", "execution_mode": "manual_operator_repair", "provider_call_count": 0})
        tt = build_token_truth(str(tmp_path))
        assert tt["measurement_source"] == "character_heuristic" and tt["measurement_confidence"] == "low"
        assert validate_token_truth(tt) == []

    def test_complete_provider_actuals_high(self, tmp_path):
        _seed(tmp_path, "T001", {"task_id": "T001", "builder_prompt_tokens_estimated": 0},
              {"schema_version": "1.0.0", "task_id": "T001", "execution_mode": "provider_backed",
               "provider_call_count": 1, "actual_call_count": 1, "cost_call_count": 1,
               "actual_prompt_tokens": 10, "actual_completion_tokens": 5, "actual_total_tokens": 15,
               "total_cost_usd": 0.01, "actual_model_verified": True, "builder_actual_model": "c",
               "builder_provider": "claude"})
        tt = build_token_truth(str(tmp_path))
        assert tt["measurement_source"] == "provider_actuals" and tt["measurement_confidence"] == "high"
        assert validate_token_truth(tt) == []

    def test_mixed_partial_actual_coverage(self, tmp_path):
        # One task measured, one heuristic → mixed.
        _seed(tmp_path, "T001", {"task_id": "T001", "builder_prompt_tokens_estimated": 0},
              {"schema_version": "1.0.0", "task_id": "T001", "execution_mode": "provider_backed",
               "provider_call_count": 1, "actual_call_count": 1, "cost_call_count": 0,
               "actual_prompt_tokens": 10, "actual_completion_tokens": 5, "actual_total_tokens": 15,
               "builder_provider": "claude"})
        _seed(tmp_path, "T002", {"task_id": "T002", "builder_prompt_tokens_estimated": 3},
              {"schema_version": "1.0.0", "task_id": "T002", "execution_mode": "provider_backed",
               "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0})
        tt = build_token_truth(str(tmp_path))
        assert tt["measurement_source"] == "mixed_provider_actuals_and_heuristic"
        assert tt["measurement_confidence"] == "mixed"
        assert validate_token_truth(tt) == []

    def test_provider_calls_without_measured_usage_is_low(self, tmp_path):
        _seed(tmp_path, "T001", {"task_id": "T001", "builder_prompt_tokens_estimated": 5},
              {"schema_version": "1.0.0", "task_id": "T001", "execution_mode": "provider_backed",
               "provider_call_count": 1, "actual_call_count": 0, "cost_call_count": 0})
        tt = build_token_truth(str(tmp_path))
        assert tt["measurement_confidence"] == "low" and tt["actual_available"] is False
        assert validate_token_truth(tt) == []

    def test_empty_evidence_validates(self, tmp_path):
        tt = build_token_truth(str(tmp_path))
        assert validate_token_truth(tt) == []


class TestSharedProducerHelperValidates:
    """The shared test_token_truth _seed_task helper's producer output validates — the fixtures the
    producer's own suite uses must all pass the validator, blocking future enum drift."""

    def test_default_seed_validates(self, tmp_path):
        _TT._seed_task(tmp_path, "T001")
        assert validate_token_truth(build_token_truth(str(tmp_path))) == []

    def test_seed_with_actuals_validates(self, tmp_path):
        _TT._seed_task(tmp_path, "T001", provider_evidence={
            "schema_version": "1.0.0", "task_id": "T001", "execution_mode": "provider_backed",
            "provider_call_count": 1, "actual_call_count": 1, "cost_call_count": 1,
            "actual_prompt_tokens": 8, "actual_completion_tokens": 4, "actual_total_tokens": 12,
            "total_cost_usd": 0.02, "actual_model_verified": True, "builder_actual_model": "c",
            "builder_provider": "claude"})
        assert validate_token_truth(build_token_truth(str(tmp_path))) == []
