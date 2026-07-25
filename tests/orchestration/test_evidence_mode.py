"""Tests for evidence execution mode taxonomy (evidence_mode)."""
from __future__ import annotations

import pytest

from packages.orchestration.evidence_mode import (
    ExecutionMode,
    build_task_execution_evidence,
    classify_execution_mode,
)

# --- Enum shape ------------------------------------------------------------

def test_enum_has_five_values():
    assert len(ExecutionMode) == 5


def test_enum_values_are_expected_strings():
    assert {m.value for m in ExecutionMode} == {
        "provider_backed",
        "fake_provider_test",
        "manual_operator_repair",
        "operator_built_no_provider",
        "unknown",
    }


def test_enum_is_str_enum():
    assert ExecutionMode.PROVIDER_BACKED == "provider_backed"


# --- classify_execution_mode ----------------------------------------------

def test_provider_backed_when_prompts_and_calls():
    assert (
        classify_execution_mode(3, 3, "ollama", "ollama")
        is ExecutionMode.PROVIDER_BACKED
    )


def test_operator_built_no_provider_when_zero_zero_non_fake():
    assert (
        classify_execution_mode(0, 0, "ollama", "ollama")
        is ExecutionMode.OPERATOR_BUILT_NO_PROVIDER
    )


def test_operator_built_no_provider_with_no_provider_names():
    assert (
        classify_execution_mode(0, 0, None, None)
        is ExecutionMode.OPERATOR_BUILT_NO_PROVIDER
    )


def test_manual_operator_repair_when_prompts_but_no_calls():
    assert (
        classify_execution_mode(2, 0, "ollama", "ollama")
        is ExecutionMode.MANUAL_OPERATOR_REPAIR
    )


def test_unknown_when_calls_but_no_prompts():
    assert (
        classify_execution_mode(0, 4, "ollama", "ollama")
        is ExecutionMode.UNKNOWN
    )


def test_fake_provider_builder_detected():
    assert (
        classify_execution_mode(5, 5, "FakeBuilder", "ollama")
        is ExecutionMode.FAKE_PROVIDER_TEST
    )


def test_fake_provider_reviewer_detected():
    assert (
        classify_execution_mode(5, 5, "ollama", "stub-reviewer")
        is ExecutionMode.FAKE_PROVIDER_TEST
    )


def test_fake_provider_takes_precedence_over_provider_backed():
    # Even with real signals, a fake provider must classify as a test.
    assert (
        classify_execution_mode(9, 9, "mock", "mock")
        is ExecutionMode.FAKE_PROVIDER_TEST
    )


@pytest.mark.parametrize("marker", ["fake", "stub", "mock", "FAKE", "MockProvider"])
def test_fake_markers_case_insensitive(marker):
    assert (
        classify_execution_mode(1, 1, marker, None)
        is ExecutionMode.FAKE_PROVIDER_TEST
    )


def test_negative_counts_treated_as_zero():
    assert (
        classify_execution_mode(-5, -5, "ollama", "ollama")
        is ExecutionMode.OPERATOR_BUILT_NO_PROVIDER
    )


def test_none_counts_treated_as_zero():
    assert (
        classify_execution_mode(None, None, "ollama", "ollama")
        is ExecutionMode.OPERATOR_BUILT_NO_PROVIDER
    )


# --- build_task_execution_evidence ----------------------------------------

_REQUIRED_FIELDS = {
    "execution_mode",
    "builder_provider",
    "reviewer_provider",
    "builder_identity",
    "reviewer_identity",
    "prompt_trace_available",
    "provider_call_count",
    "actual_provider_available",
    "actual_model_available",
    "actual_token_usage_available",
}


def test_evidence_dict_has_all_required_fields():
    ev = build_task_execution_evidence(
        "T001",
        ExecutionMode.PROVIDER_BACKED,
        builder_provider="ollama",
        reviewer_provider="ollama",
        builder_identity="qwen3-coder",
        reviewer_identity="qwen3-coder",
    )
    assert _REQUIRED_FIELDS.issubset(ev.keys())


def test_evidence_dict_carries_values():
    ev = build_task_execution_evidence(
        "T001",
        ExecutionMode.PROVIDER_BACKED,
        builder_provider="ollama",
        reviewer_provider="claude",
        builder_identity="qwen3-coder",
        reviewer_identity="sonnet",
        prompt_trace_available=True,
        provider_call_count=7,
        actual_provider_available=True,
        actual_model_available=True,
        actual_token_usage_available=True,
    )
    assert ev["task_id"] == "T001"
    assert ev["execution_mode"] == "provider_backed"
    assert ev["builder_provider"] == "ollama"
    assert ev["reviewer_provider"] == "claude"
    assert ev["builder_identity"] == "qwen3-coder"
    assert ev["reviewer_identity"] == "sonnet"
    assert ev["prompt_trace_available"] is True
    assert ev["provider_call_count"] == 7
    assert ev["actual_provider_available"] is True
    assert ev["actual_model_available"] is True
    assert ev["actual_token_usage_available"] is True


def test_evidence_accepts_string_mode():
    ev = build_task_execution_evidence("T002", "unknown")
    assert ev["execution_mode"] == "unknown"


def test_evidence_rejects_invalid_string_mode():
    with pytest.raises(ValueError):
        build_task_execution_evidence("T003", "not_a_mode")


def test_evidence_defaults_are_safe():
    ev = build_task_execution_evidence("T004", ExecutionMode.OPERATOR_BUILT_NO_PROVIDER)
    assert ev["prompt_trace_available"] is False
    assert ev["provider_call_count"] == 0
    assert ev["actual_provider_available"] is False
    assert ev["actual_model_available"] is False
    assert ev["actual_token_usage_available"] is False


def test_evidence_provider_call_count_clamped():
    ev = build_task_execution_evidence(
        "T005", ExecutionMode.UNKNOWN, provider_call_count=-3
    )
    assert ev["provider_call_count"] == 0


def test_end_to_end_classify_then_build():
    mode = classify_execution_mode(4, 4, "ollama", "ollama")
    ev = build_task_execution_evidence(
        "T006",
        mode,
        builder_provider="ollama",
        reviewer_provider="ollama",
        prompt_trace_available=True,
        provider_call_count=4,
    )
    assert ev["execution_mode"] == "provider_backed"
    assert ev["provider_call_count"] == 4
