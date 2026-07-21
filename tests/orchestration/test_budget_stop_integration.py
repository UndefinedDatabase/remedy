"""F018 T003 — budget stop integration tests.

Tests the unified should_stop() predicate, budget-triggered stopping,
decision queue entries, and deadline-at-start refusal.
"""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import (
    BudgetCounterError,
    BudgetCounters,
    BudgetEvaluation,
    collect_counters_from_actuals,
    evaluate_budget,
)
from packages.orchestration.safe_points import (
    ShouldStopResult,
    StopSignal,
    request_stop,
    should_stop,
    stop_requested,
)

UTC = timezone.utc
T0 = datetime(2026, 7, 1, 12, 0, 0, tzinfo=UTC)


class TestShouldStopOperatorFirst:
    """Operator stop takes precedence over budget."""

    def test_no_stop_no_budget(self, tmp_path):
        r = should_stop("test-job-001", control_root_path=tmp_path)
        assert r.should_stop is False
        assert r.reason == ""
        assert r.operator_signal is None
        assert r.budget_evaluation is None

    def test_operator_stop_wins(self, tmp_path):
        request_stop("test-job-002", reason="manual", control_root_path=tmp_path)
        r = should_stop("test-job-002", control_root_path=tmp_path)
        assert r.should_stop is True
        assert "operator_stop" in r.reason
        assert r.source == "operator"
        assert r.operator_signal is not None

    def test_operator_stop_before_budget(self, tmp_path):
        request_stop("test-job-003", reason="kill", control_root_path=tmp_path)
        budgets = JobBudgets(max_provider_calls=10)
        counters = BudgetCounters(provider_calls=100, measured_call_count=100)
        r = should_stop(
            "test-job-003",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is True
        assert r.source == "operator"

    def test_budget_exhausted_no_operator(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=3)
        counters = BudgetCounters(provider_calls=3, measured_call_count=3)
        r = should_stop(
            "test-job-004",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is True
        assert r.source == "budget"
        assert "budget_exhausted:max_provider_calls" in r.reason
        assert r.budget_evaluation is not None

    def test_budget_not_exhausted_continues(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=10)
        counters = BudgetCounters(provider_calls=2, measured_call_count=2)
        r = should_stop(
            "test-job-005",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is False


class TestThreeCallLimit:
    """A three-call limit stops before call four."""

    def test_three_calls_allowed(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=3)
        counters = BudgetCounters(provider_calls=2, measured_call_count=2)
        r = should_stop(
            "test-job-3c1",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is False

    def test_at_three_calls_stops(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=3)
        counters = BudgetCounters(provider_calls=3, measured_call_count=3)
        r = should_stop(
            "test-job-3c2",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is True
        assert "max_provider_calls" in r.reason


class TestDeadlineAtStart:
    """Past deadline at start refuses work."""

    def test_past_deadline_stops(self, tmp_path):
        dl = T0 - timedelta(hours=1)
        budgets = JobBudgets(deadline=dl)
        counters = BudgetCounters()
        r = should_stop(
            "test-job-dl1",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is True
        assert "deadline" in r.reason

    def test_future_deadline_continues(self, tmp_path):
        dl = T0 + timedelta(hours=1)
        budgets = JobBudgets(deadline=dl)
        counters = BudgetCounters()
        r = should_stop(
            "test-job-dl2",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is False


class TestShouldStopSerialization:
    def test_no_stop_to_json(self, tmp_path):
        r = should_stop("test-job-j1", control_root_path=tmp_path)
        d = r.to_json()
        assert d["should_stop"] is False
        assert d["reason"] == ""

    def test_budget_stop_to_json(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=1)
        counters = BudgetCounters(provider_calls=5, measured_call_count=5)
        r = should_stop(
            "test-job-j2",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        d = r.to_json()
        assert d["should_stop"] is True
        assert "budget_evaluation" in d


class TestDecisionQueueEntry:
    """Budget exhaustion produces a token_budget decision type."""

    def test_token_budget_in_decision_types(self):
        from packages.orchestration.decision_queue import DECISION_TYPES
        assert "token_budget" in DECISION_TYPES

    def test_budget_evaluation_carries_limit_info(self):
        budgets = JobBudgets(max_total_tokens=1000)
        counters = BudgetCounters(provider_calls=5, measured_token_total=2000, measured_call_count=5)
        evaluation = evaluate_budget(budgets, counters, now=T0)
        assert evaluation.exhausted is True
        assert evaluation.first_exhausted_limit == "max_total_tokens"
        d = evaluation.to_json()
        assert d["first_exhausted_limit"] == "max_total_tokens"


class TestPostmortemClass:
    """FailureClass.BUDGET_EXHAUSTED exists and is classifiable."""

    def test_budget_exhausted_exists(self):
        from packages.orchestration.failure_postmortem import FailureClass
        assert hasattr(FailureClass, "BUDGET_EXHAUSTED")
        assert FailureClass.BUDGET_EXHAUSTED.value == "budget_exhausted"


class TestStopReasonCode:
    """Stop reasons include token_budget_exceeded."""

    def test_stop_reason_code_exists(self):
        from packages.orchestration.stop_reasons import REASON_CODES
        assert "token_budget_exceeded" in REASON_CODES


class TestWallClockFromStartedAt:
    """Wall clock derives from started_at + now, not arbitrary elapsed."""

    def test_started_at_overrides_elapsed(self):
        started = T0 - timedelta(minutes=120)
        budgets = JobBudgets(max_wall_clock_minutes=60)
        counters = BudgetCounters(started_at=started, elapsed_seconds=0.0)
        evaluation = evaluate_budget(budgets, counters, now=T0)
        assert evaluation.exhausted is True

    def test_no_started_at_uses_elapsed(self):
        budgets = JobBudgets(max_wall_clock_minutes=60)
        counters = BudgetCounters(elapsed_seconds=1800.0)
        evaluation = evaluate_budget(budgets, counters, now=T0)
        assert evaluation.exhausted is False


class TestCounterValidation:
    """BudgetCounters rejects impossible data."""

    def test_negative_values_rejected(self):
        with pytest.raises(BudgetCounterError):
            BudgetCounters(provider_calls=-1)

    def test_boolean_values_rejected(self):
        with pytest.raises(BudgetCounterError):
            BudgetCounters(provider_calls=True)  # type: ignore[arg-type]

    def test_inconsistent_counts_rejected(self):
        with pytest.raises(BudgetCounterError):
            BudgetCounters(provider_calls=5, measured_call_count=2, unmeasured_call_count=1)

    def test_consistent_counts_accepted(self):
        c = BudgetCounters(provider_calls=3, measured_call_count=2, unmeasured_call_count=1)
        assert c.provider_calls == 3
