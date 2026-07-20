"""Tests for token_truth.py — honest actual-vs-estimated aggregation + writer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.token_truth import (
    TokenEvidenceError,
    build_token_truth,
    write_token_truth,
)


def _run_dir(base: Path, task_id: str) -> Path:
    d = base / "task_runs" / task_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _seed_task(
    base: Path,
    task_id: str = "T001",
    *,
    builder: int = 8573,
    reviewer: int = 4923,
    repair: int = 0,
    provider_evidence: dict | None = None,
) -> None:
    d = _run_dir(base, task_id)
    (d / "token_accounting.json").write_text(json.dumps({
        "kind": "estimated",
        "actual_tokens_available": False,
        "builder_prompt_tokens_estimated": builder,
        "reviewer_prompt_tokens_estimated": reviewer,
        "repair_prompt_tokens_estimated": repair,
    }))
    if provider_evidence is None:
        provider_evidence = {
            "builder_provider": "claude-cli",
            "reviewer_provider": "claude-cli",
        }
    (d / "provider_evidence.json").write_text(json.dumps(provider_evidence))


def test_estimated_only_no_actual(tmp_path: Path) -> None:
    _seed_task(tmp_path)
    (tmp_path / "prompt_trace_summary.json").write_text(json.dumps({
        "total_prompts": 2,
    }))

    report = build_token_truth(str(tmp_path))

    assert report["schema_version"] == "1.0.0"
    assert report["source"] == "evidence_aggregation"
    assert report["provider"] == "claude-cli"
    assert report["actual_available"] is False
    assert report["actual_prompt_tokens"] is None
    assert report["actual_completion_tokens"] is None
    assert report["actual_total_tokens"] is None
    assert report["actual_cache_creation_tokens"] is None
    assert report["actual_cache_read_tokens"] is None
    assert report["estimated_prompt_tokens"] == 13496
    assert report["estimated_completion_tokens"] == 0
    assert report["estimated_total_tokens"] == 13496
    assert report["measurement_source"] == "character_heuristic"
    assert report["measurement_confidence"] == "low"
    assert report["missing_reason"]
    assert report["builder_estimated_total"] == 8573
    assert report["reviewer_estimated_total"] == 4923
    assert report["repair_estimated_total"] == 0
    # provider_call_count comes from provider_evidence aggregation (legacy
    # single-call fallback here), NOT from the prompt trace.
    assert report["provider_call_count"] == 1
    assert report["prompt_trace_count"] == 2
    t001 = report["per_task"]["T001"]
    assert t001["builder_estimated"] == 8573
    assert t001["reviewer_estimated"] == 4923
    assert t001["repair_estimated"] == 0
    assert t001["actual_available"] is False
    assert t001["role"] == "unknown"
    assert t001["estimation_method"] == "character_heuristic"


def test_multiple_tasks_aggregate(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=1000, reviewer=500, repair=0)
    _seed_task(tmp_path, "T002", builder=2000, reviewer=1500, repair=300)

    report = build_token_truth(str(tmp_path))

    assert report["builder_estimated_total"] == 3000
    assert report["reviewer_estimated_total"] == 2000
    assert report["repair_estimated_total"] == 300
    assert report["estimated_prompt_tokens"] == 5300
    assert report["estimated_total_tokens"] == 5300
    assert set(report["per_task"]) == {"T001", "T002"}


def test_actual_usage_populated(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", provider_evidence={
        "builder_provider": "anthropic-api",
        "model": "claude-opus-4-8",
        "usage": {
            "input_tokens": 1200,
            "output_tokens": 340,
            "total_tokens": 1540,
            "cache_creation_input_tokens": 800,
            "cache_read_input_tokens": 200,
        },
    })

    report = build_token_truth(str(tmp_path))

    assert report["provider"] == "anthropic-api"
    assert report["model"] == "claude-opus-4-8"
    assert report["actual_available"] is True
    assert report["actual_prompt_tokens"] == 1200
    assert report["actual_completion_tokens"] == 340
    assert report["actual_total_tokens"] == 1540
    assert report["actual_cache_creation_tokens"] == 800
    assert report["actual_cache_read_tokens"] == 200
    assert report["missing_reason"] is None
    assert report["per_task"]["T001"]["actual_available"] is True


def test_empty_evidence_dir(tmp_path: Path) -> None:
    report = build_token_truth(str(tmp_path))

    assert report["actual_available"] is False
    assert report["estimated_prompt_tokens"] == 0
    assert report["per_task"] == {}
    assert report["provider"] == "claude-cli"
    assert report["provider_call_count"] == 0


def test_write_token_truth(tmp_path: Path) -> None:
    _seed_task(tmp_path)
    written: dict[str, str] = {}

    write_token_truth(str(tmp_path), written)

    out = tmp_path / "token_truth.json"
    assert out.exists()
    assert written["token_truth.json"] == str(out)
    data = json.loads(out.read_text())
    assert data["estimated_total_tokens"] == 13496


def test_write_token_truth_no_dir() -> None:
    written: dict[str, str] = {}
    write_token_truth("", written)
    assert written == {}


def test_no_cross_contamination(tmp_path: Path) -> None:
    """Estimated values must never appear in actual_* fields."""
    _seed_task(tmp_path, builder=9999, reviewer=7777, repair=3333)

    report = build_token_truth(str(tmp_path))

    assert report["actual_available"] is False
    assert report["actual_prompt_tokens"] is None
    assert report["actual_completion_tokens"] is None
    assert report["actual_total_tokens"] is None
    assert report["actual_cache_creation_tokens"] is None
    assert report["actual_cache_read_tokens"] is None

    assert report["estimated_prompt_tokens"] == 9999 + 7777 + 3333
    assert report["builder_estimated_total"] == 9999
    assert report["reviewer_estimated_total"] == 7777
    assert report["repair_estimated_total"] == 3333


def test_per_task_includes_role(tmp_path: Path) -> None:
    d = _run_dir(tmp_path, "T001")
    (d / "token_accounting.json").write_text(json.dumps({
        "kind": "estimated",
        "builder_prompt_tokens_estimated": 100,
        "reviewer_prompt_tokens_estimated": 50,
        "repair_prompt_tokens_estimated": 0,
        "role": "builder",
        "configured_model": "opus",
    }))
    (d / "provider_evidence.json").write_text(json.dumps({
        "builder_provider": "claude-cli",
    }))
    report = build_token_truth(str(tmp_path))
    t001 = report["per_task"]["T001"]
    assert t001["role"] == "builder"
    assert t001["configured_model"] == "opus"


def test_per_task_actual_model_from_provider_evidence(tmp_path: Path) -> None:
    d = _run_dir(tmp_path, "T001")
    (d / "token_accounting.json").write_text(json.dumps({
        "kind": "estimated",
        "builder_prompt_tokens_estimated": 100,
        "reviewer_prompt_tokens_estimated": 50,
        "repair_prompt_tokens_estimated": 0,
    }))
    (d / "provider_evidence.json").write_text(json.dumps({
        "builder_provider": "claude-cli",
        "actual_model": "claude-opus-4-20250514",
        "actual_model_verified": True,
    }))
    report = build_token_truth(str(tmp_path))
    t001 = report["per_task"]["T001"]
    assert t001["actual_model"] == "claude-opus-4-20250514"
    assert t001["actual_model_verified"] is True


def test_per_task_actual_model_verified(tmp_path: Path) -> None:
    d = _run_dir(tmp_path, "T001")
    (d / "token_accounting.json").write_text(json.dumps({
        "kind": "estimated",
        "builder_prompt_tokens_estimated": 100,
        "reviewer_prompt_tokens_estimated": 50,
        "repair_prompt_tokens_estimated": 0,
    }))
    (d / "provider_evidence.json").write_text(json.dumps({
        "builder_provider": "claude-cli",
        "builder_actual_model": "claude-opus-4-20250514",
        "actual_model_verified": True,
    }))
    report = build_token_truth(str(tmp_path))
    t001 = report["per_task"]["T001"]
    assert t001["actual_model"] == "claude-opus-4-20250514"
    assert t001["actual_model_verified"] is True


def test_actual_available_false_no_fake_actuals(tmp_path: Path) -> None:
    _seed_task(tmp_path, builder=500, reviewer=200, repair=0)
    report = build_token_truth(str(tmp_path))
    t001 = report["per_task"]["T001"]
    assert t001["actual_available"] is False
    assert t001["estimation_method"] == "character_heuristic"


def test_actual_available_true_no_estimation_method(tmp_path: Path) -> None:
    _seed_task(tmp_path, builder=500, reviewer=200, repair=0,
               provider_evidence={
                   "builder_provider": "claude",
                   "usage": {"input_tokens": 1000, "output_tokens": 500},
               })
    report = build_token_truth(str(tmp_path))
    t001 = report["per_task"]["T001"]
    assert t001["actual_available"] is True
    assert t001["estimation_method"] is None


def test_missing_role_defaults_to_unknown(tmp_path: Path) -> None:
    d = _run_dir(tmp_path, "T001")
    (d / "token_accounting.json").write_text(json.dumps({
        "kind": "estimated",
        "builder_prompt_tokens_estimated": 100,
        "reviewer_prompt_tokens_estimated": 50,
        "repair_prompt_tokens_estimated": 0,
    }))
    (d / "provider_evidence.json").write_text(json.dumps({
        "builder_provider": "claude-cli",
    }))
    report = build_token_truth(str(tmp_path))
    t001 = report["per_task"]["T001"]
    assert t001["role"] == "unknown"


def test_estimation_method_recorded_when_estimated(tmp_path: Path) -> None:
    _seed_task(tmp_path, builder=100, reviewer=50, repair=0)
    report = build_token_truth(str(tmp_path))
    t001 = report["per_task"]["T001"]
    assert t001["estimation_method"] == "character_heuristic"
    assert t001["actual_available"] is False


def test_manual_operator_repair_not_actual_usage(tmp_path: Path) -> None:
    """A manual operator repair must never be labeled as actual provider usage."""
    _seed_task(tmp_path, provider_evidence={
        "builder_provider": "operator",
        "reviewer_provider": "operator",
        "execution_mode": "manual_operator_repair",
        # Stray counters must NOT be counted as actual usage.
        "usage": {"input_tokens": 1000, "output_tokens": 500},
    })
    report = build_token_truth(str(tmp_path))
    assert report["actual_available"] is False
    assert report["actual_prompt_tokens"] is None
    assert report["actual_completion_tokens"] is None
    assert report["per_task"]["T001"]["actual_available"] is False


# -- F003 regression: mixed provider/manual runs must stay honest ----------


def test_mixed_provider_and_manual_no_double_count(tmp_path: Path) -> None:
    """A provider-measured task plus a manual-repair task: actuals count only the
    measured task, estimates are never absorbed into actuals, and confidence is
    'mixed' (some measured, some not)."""
    _seed_task(tmp_path, "T001", builder=1000, reviewer=0, repair=0,
               provider_evidence={
                   "builder_provider": "anthropic-api",
                   "usage": {"input_tokens": 1200, "output_tokens": 300,
                             "total_tokens": 1500},
                   "total_cost_usd": 0.01,
               })
    _seed_task(tmp_path, "T002", builder=2000, reviewer=0, repair=0,
               provider_evidence={
                   "builder_provider": "operator",
                   "execution_mode": "manual_operator_repair",
                   "usage": {"input_tokens": 9999, "output_tokens": 8888},
                   "total_cost_usd": 5.0,
               })

    report = build_token_truth(str(tmp_path))

    assert report["actual_prompt_tokens"] == 1200
    assert report["actual_completion_tokens"] == 300
    assert report["actual_total_tokens"] == 1500
    assert report["total_cost_usd"] == 0.01
    assert report["estimated_prompt_tokens"] == 3000
    assert report["measurement_confidence"] == "mixed"
    assert report["measurement_source"] == "mixed_provider_actuals_and_heuristic"
    assert report["per_task"]["T001"]["actual_available"] is True
    assert report["per_task"]["T002"]["actual_available"] is False


def test_estimated_never_labeled_actual_all_manual(tmp_path: Path) -> None:
    """An all-manual run keeps every estimate as estimate and never fabricates
    actual usage or cost."""
    _seed_task(tmp_path, "T001", builder=4000, reviewer=1000, repair=0,
               provider_evidence={
                   "builder_provider": "operator",
                   "execution_mode": "manual_operator_repair",
                   "usage": {"input_tokens": 7000, "output_tokens": 6000},
                   "total_cost_usd": 3.0,
               })

    report = build_token_truth(str(tmp_path))

    assert report["actual_available"] is False
    assert report["actual_prompt_tokens"] is None
    assert report["actual_total_tokens"] is None
    assert report["total_cost_usd"] is None
    assert report["estimated_prompt_tokens"] == 5000
    assert report["measurement_confidence"] == "low"
    assert report["measurement_source"] == "character_heuristic"


def test_manual_repair_kind_manual_no_provider_usage(tmp_path: Path) -> None:
    """Manual repair token_accounting stays kind=manual and yields no actuals."""
    d = _run_dir(tmp_path, "T001")
    (d / "token_accounting.json").write_text(json.dumps({
        "task_id": "T001",
        "kind": "manual",
        "reason": "manual",
        "actual_available": False,
        "builder_prompt_tokens_estimated": 0,
        "reviewer_prompt_tokens_estimated": 0,
        "repair_prompt_tokens_estimated": 0,
    }))
    (d / "provider_evidence.json").write_text(json.dumps({
        "task_id": "T001",
        "builder_provider": "operator",
        "execution_mode": "manual_operator_repair",
        "provider_call_count": 0,
    }))

    report = build_token_truth(str(tmp_path))

    # kind is preserved on the source artifact.
    acc = json.loads((d / "token_accounting.json").read_text())
    assert acc["kind"] == "manual"
    # And the aggregate reports no actual provider usage for the manual task.
    assert report["actual_available"] is False
    assert report["per_task"]["T001"]["actual_available"] is False


# -- F003 findings: measurement_source honesty + missing cost ----------------


def test_high_confidence_measurement_source(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.005,
               })
    report = build_token_truth(str(tmp_path))
    assert report["measurement_confidence"] == "high"
    assert report["measurement_source"] == "provider_actuals"


def test_mixed_confidence_measurement_source(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.005,
               })
    _seed_task(tmp_path, "T002", builder=100, reviewer=50, repair=0,
               provider_evidence={"builder_provider": "claude-cli"})
    report = build_token_truth(str(tmp_path))
    assert report["measurement_confidence"] == "mixed"
    assert report["measurement_source"] == "mixed_provider_actuals_and_heuristic"


def test_low_confidence_measurement_source(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={"builder_provider": "claude-cli"})
    report = build_token_truth(str(tmp_path))
    assert report["measurement_confidence"] == "low"
    assert report["measurement_source"] == "character_heuristic"


def test_actual_usage_without_cost_keeps_cost_none(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
               })
    report = build_token_truth(str(tmp_path))
    assert report["actual_available"] is True
    assert report["actual_prompt_tokens"] == 200
    assert report["total_cost_usd"] is None


# --- Fix 3: configured vs actual model separation ---

def test_configured_model_does_not_become_actual(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "builder_configured_model": "opus",
                   "reviewer_configured_model": "opus",
               })
    report = build_token_truth(str(tmp_path))
    assert report["builder_configured_model"] == "opus"
    assert report["reviewer_configured_model"] == "opus"
    assert report["builder_actual_model"] is None
    assert report["reviewer_actual_model"] is None
    assert report["actual_model_verified"] is False


def test_actual_model_without_verified_raises(tmp_path: Path) -> None:
    """Round 37 F3: actual model identity without actual_model_verified=true is contradictory."""
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "builder_configured_model": "opus",
                   "builder_actual_model": "claude-opus-4-20250514",
               })
    with pytest.raises(TokenEvidenceError, match="actual model identity present"):
        build_token_truth(str(tmp_path))


# --- Fix 4: provider-call actual coverage ---

def test_actual_coverage_all_measured(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.01,
                   "provider_call_count": 2,
                   "actual_call_count": 2,
                   "cost_call_count": 2,
               })
    report = build_token_truth(str(tmp_path))
    assert report["measurement_confidence"] == "high"
    assert report["actual_coverage_complete"] is True
    assert report["actual_call_count"] == 2


def test_actual_coverage_mixed(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.01,
                   "provider_call_count": 4,
                   "actual_call_count": 2,
                   "cost_call_count": 2,
               })
    report = build_token_truth(str(tmp_path))
    assert report["measurement_confidence"] == "mixed"
    assert report["actual_coverage_complete"] is False


def test_actual_coverage_none(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "provider_call_count": 2,
                   "actual_call_count": 0,
                   "cost_call_count": 0,
               })
    report = build_token_truth(str(tmp_path))
    assert report["measurement_confidence"] == "low"


# --- Fix 5: partial cost never labeled as total ---

def test_partial_cost_returns_null(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.01,
                   "provider_call_count": 4,
                   "actual_call_count": 4,
                   "cost_call_count": 2,
               })
    report = build_token_truth(str(tmp_path))
    assert report["total_cost_usd"] is None
    assert report["cost_coverage_complete"] is False
    assert report["cost_coverage_reason"] == "missing_provider_cost"


def test_full_cost_returns_sum(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.05,
                   "provider_call_count": 2,
                   "actual_call_count": 2,
                   "cost_call_count": 2,
               })
    report = build_token_truth(str(tmp_path))
    assert report["total_cost_usd"] == 0.05
    assert report["cost_coverage_complete"] is True


def test_no_cost_returns_null_no_heuristic(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "provider_call_count": 2,
                   "actual_call_count": 2,
                   "cost_call_count": 0,
               })
    report = build_token_truth(str(tmp_path))
    assert report["total_cost_usd"] is None


# --- F003 findings fix: cost completeness against ALL real provider calls ---


def test_cost_missing_because_actuals_missing(tmp_path: Path) -> None:
    """Two real calls, one with actuals+cost, one without actuals:
    total_cost_usd stays null and the reason names the missing actuals."""
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.01,
                   "provider_call_count": 2,
                   "actual_call_count": 1,
                   "cost_call_count": 1,
               })
    report = build_token_truth(str(tmp_path))
    assert report["total_cost_usd"] is None
    assert report["actual_coverage_complete"] is False
    assert report["cost_coverage_complete"] is False
    assert report["cost_coverage_reason"] == "missing_actuals"


def test_cost_missing_because_actuals_and_cost_missing(tmp_path: Path) -> None:
    """Some calls lack actuals AND some actual-covered calls lack cost."""
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.01,
                   "provider_call_count": 4,
                   "actual_call_count": 3,
                   "cost_call_count": 1,
               })
    report = build_token_truth(str(tmp_path))
    assert report["total_cost_usd"] is None
    assert report["cost_coverage_complete"] is False
    assert report["cost_coverage_reason"] == "missing_actuals_and_provider_cost"


def test_no_actuals_at_all_cost_null(tmp_path: Path) -> None:
    """Real provider calls with no parsed actuals: cost null, reason honest."""
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "provider_call_count": 2,
                   "actual_call_count": 0,
                   "cost_call_count": 0,
               })
    report = build_token_truth(str(tmp_path))
    assert report["total_cost_usd"] is None
    assert report["actual_coverage_complete"] is False
    assert report["cost_coverage_complete"] is False
    assert report["cost_coverage_reason"] == "missing_actuals"


def test_cost_coverage_reason_none_when_complete(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.05,
                   "provider_call_count": 3,
                   "actual_call_count": 3,
                   "cost_call_count": 3,
               })
    report = build_token_truth(str(tmp_path))
    assert report["total_cost_usd"] == 0.05
    assert report["cost_coverage_complete"] is True
    assert report["cost_coverage_reason"] is None


# --- F003 findings fix: root provider_call_count from provider_evidence ---


def test_root_provider_call_count_from_provider_evidence(tmp_path: Path) -> None:
    """Root provider_call_count aggregates provider_evidence counts; the prompt
    trace count is exposed separately as prompt_trace_count."""
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.01,
                   "provider_call_count": 3,
                   "actual_call_count": 3,
                   "cost_call_count": 3,
               })
    _seed_task(tmp_path, "T002", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 100, "output_tokens": 50, "total_tokens": 150},
                   "total_cost_usd": 0.02,
                   "provider_call_count": 2,
                   "actual_call_count": 2,
                   "cost_call_count": 2,
               })
    (tmp_path / "prompt_trace_summary.json").write_text(json.dumps({
        "total_prompts": 99,
    }))
    report = build_token_truth(str(tmp_path))
    assert report["provider_call_count"] == 5
    assert report["prompt_trace_count"] == 99
    assert report["actual_call_count"] == 5
    assert report["actual_coverage_complete"] is True


def test_actual_call_count_exceeding_provider_is_a_producer_error(tmp_path: Path) -> None:
    """Round 34 F2: malformed per-task counts (actual > provider, or cost > actual) are NOT clamped
    into a plausible value — the producer raises a bounded TokenEvidenceError so the packaging
    authority reports PRODUCER_ERROR and BLOCKED_EVIDENCE."""
    import pytest
    from packages.orchestration.token_truth import TokenEvidenceError
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.01,
                   "provider_call_count": 2,
                   "actual_call_count": 5,
                   "cost_call_count": 9,
               })
    with pytest.raises(TokenEvidenceError):
        build_token_truth(str(tmp_path))


def test_manual_repair_task_not_in_provider_call_count(tmp_path: Path) -> None:
    """Manual/fake tasks never contribute real provider calls."""
    _seed_task(tmp_path, "T001", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "claude-cli",
                   "usage": {"input_tokens": 200, "output_tokens": 100, "total_tokens": 300},
                   "total_cost_usd": 0.01,
                   "provider_call_count": 2,
                   "actual_call_count": 2,
                   "cost_call_count": 2,
               })
    _seed_task(tmp_path, "T002", builder=100, reviewer=50, repair=0,
               provider_evidence={
                   "builder_provider": "operator",
                   "execution_mode": "manual_operator_repair",
                   "provider_call_count": 0,
                   "actual_call_count": 0,
                   "cost_call_count": 0,
               })
    report = build_token_truth(str(tmp_path))
    assert report["provider_call_count"] == 2
    assert report["actual_call_count"] == 2
    assert report["total_cost_usd"] == 0.01
