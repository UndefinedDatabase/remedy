"""Tests for token-cost policy evidence (token_cost_policy)."""
from __future__ import annotations

from packages.orchestration.token_cost_policy import (
    SCHEMA_VERSION,
    build_token_cost_policy,
)

_JOB_ID = "job-5741-5820"
_STEP_RANGE = "5741-5820"


def _role_configs():
    return {
        "builder": {"model": "qwen3-coder", "context_budget": 40_000, "max_prompt_chars": 120_000},
        "reviewer": {"model": "qwen3-coder", "context_budget": 30_000, "max_prompt_chars": 80_000},
    }


def _token_truth(**overrides):
    truth = {
        "actual_available": False,
        "actual_total_tokens": None,
        "actual_prompt_tokens": None,
        "actual_completion_tokens": None,
        "builder_estimated_total": 20_000,
        "reviewer_estimated_total": 15_000,
        "repair_estimated_total": 0,
        "per_task": {
            "T001": {"role": "builder", "actual_available": False},
        },
    }
    truth.update(overrides)
    return truth


def _prompt_trace(**overrides):
    trace = {
        "total_builder_prompts": 3,
        "total_reviewer_prompts": 3,
        "total_prompts": 6,
        "total_prompt_chars": 100_000,
        "builder_prompt_chars": 60_000,
        "reviewer_prompt_chars": 40_000,
    }
    trace.update(overrides)
    return trace


def _build(**kwargs):
    args = {
        "job_id": _JOB_ID,
        "step_range": _STEP_RANGE,
        "role_configs": _role_configs(),
        "token_truth": _token_truth(),
        "prompt_trace_summary": _prompt_trace(),
        "max_rounds": 4,
        "repair_budget": 3,
    }
    args.update(kwargs)
    return build_token_cost_policy(**args)


def test_basic_policy_shape():
    report = _build()
    expected_keys = {
        "schema_version",
        "job_id",
        "step_range",
        "per_role_model_policy",
        "context_budget_policy",
        "max_prompt_chars_per_role",
        "max_rounds",
        "repair_budget",
        "actual_available_by_role",
        "estimated_tokens_by_role",
        "provider_call_count_by_role",
        "cost_risk_findings",
        "recommendations",
    }
    assert set(report) == expected_keys
    assert report["schema_version"] == SCHEMA_VERSION
    assert report["job_id"] == _JOB_ID
    assert report["step_range"] == _STEP_RANGE
    assert report["max_rounds"] == 4
    assert report["repair_budget"] == 3


def test_per_role_breakdown():
    report = _build()
    assert report["per_role_model_policy"] == {
        "builder": "qwen3-coder",
        "reviewer": "qwen3-coder",
    }
    assert report["context_budget_policy"] == {"builder": 40_000, "reviewer": 30_000}
    assert report["max_prompt_chars_per_role"] == {"builder": 120_000, "reviewer": 80_000}


def test_provider_call_counts():
    report = _build()
    assert report["provider_call_count_by_role"] == {"builder": 3, "reviewer": 3}


def test_estimate_recording():
    report = _build()
    assert report["estimated_tokens_by_role"] == {"builder": 20_000, "reviewer": 15_000}


def test_budget_tracking_clamps_negatives():
    report = _build(max_rounds=-2, repair_budget=-5)
    assert report["max_rounds"] == 0
    assert report["repair_budget"] == 0


def test_cost_risk_full_repo_context():
    configs = _role_configs()
    configs["builder"]["full_repo_context"] = True
    report = _build(role_configs=configs)
    codes = {f["code"] for f in report["cost_risk_findings"]}
    assert "FULL_REPO_CONTEXT" in codes
    finding = next(f for f in report["cost_risk_findings"] if f["code"] == "FULL_REPO_CONTEXT")
    assert finding["role"] == "builder"


def test_cost_risk_prompt_over_budget():
    # Reviewer cap is 80k; make its prompt chars exceed that.
    report = _build(prompt_trace_summary=_prompt_trace(reviewer_prompt_chars=90_000))
    over = [f for f in report["cost_risk_findings"] if f["code"] == "PROMPT_TRACE_OVER_BUDGET"]
    assert len(over) == 1
    assert over[0]["role"] == "reviewer"


def test_missing_actual_warning():
    # A role claims actual usage available, but no measured number exists.
    truth = _token_truth(
        actual_available=True,
        per_task={
            "T001": {"role": "builder", "actual_available": True},
            "T002": {"role": "reviewer", "actual_available": False},
        },
    )
    report = _build(token_truth=truth)
    assert report["actual_available_by_role"]["builder"] is True
    findings = [f for f in report["cost_risk_findings"] if f["code"] == "ACTUAL_REPORTED_UNAVAILABLE"]
    assert len(findings) == 1
    assert findings[0]["severity"] == "critical"


def test_missing_estimate_warning():
    # Reviewer made calls but recorded no estimate.
    truth = _token_truth(reviewer_estimated_total=0)
    report = _build(token_truth=truth)
    findings = [
        f for f in report["cost_risk_findings"]
        if f["code"] == "ESTIMATE_MISSING" and f["role"] == "reviewer"
    ]
    assert len(findings) == 1


def test_recommendations_present_on_clean_run():
    report = _build()
    # Clean policy but no actual usage -> low-confidence estimate recommendation.
    assert report["recommendations"]
    assert any("low-confidence estimates" in r for r in report["recommendations"])


def test_recommendations_map_to_findings():
    configs = _role_configs()
    configs["builder"]["full_repo_context"] = True
    report = _build(role_configs=configs)
    assert any("scoped context packs" in r for r in report["recommendations"])
