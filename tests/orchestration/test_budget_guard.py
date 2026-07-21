"""F018 T002 — budget_guard evaluation tests."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import (
    BudgetCounterError,
    BudgetCounters,
    BudgetEvaluation,
    collect_counters_from_actuals,
    evaluate_budget,
)

UTC = timezone.utc
T0 = datetime(2026, 7, 1, 12, 0, 0, tzinfo=UTC)


class TestBudgetCounters:
    def test_defaults(self):
        c = BudgetCounters()
        assert c.provider_calls == 0
        assert c.measured_token_total == 0
        assert c.measured_call_count == 0
        assert c.unmeasured_call_count == 0
        assert c.elapsed_seconds == 0.0
        assert c.has_unmeasured is False
        assert c.total_call_count == 0

    def test_total_call_count(self):
        c = BudgetCounters(provider_calls=5, measured_call_count=3, unmeasured_call_count=2)
        assert c.total_call_count == 5

    def test_has_unmeasured(self):
        c = BudgetCounters(provider_calls=1, measured_call_count=0, unmeasured_call_count=1)
        assert c.has_unmeasured is True

    def test_token_description_all_measured(self):
        c = BudgetCounters(provider_calls=1, measured_token_total=5000, measured_call_count=1)
        assert c.token_description() == "5000 tokens"

    def test_token_description_with_unmeasured(self):
        c = BudgetCounters(
            provider_calls=3, measured_token_total=5000,
            measured_call_count=1, unmeasured_call_count=2,
        )
        desc = c.token_description()
        assert ">=" in desc
        assert "5000" in desc
        assert "2 provider calls unmeasured" in desc

    def test_to_json_roundtrip(self):
        c = BudgetCounters(
            provider_calls=5,
            measured_token_total=10000,
            measured_call_count=4,
            unmeasured_call_count=1,
            elapsed_seconds=120.5,
            evaluated_at=T0,
            started_at=T0 - timedelta(minutes=2),
            actual_sources=("cli", "log"),
        )
        d = c.to_json()
        assert d["provider_calls"] == 5
        assert d["measured_token_total"] == 10000
        assert d["measured_call_count"] == 4
        assert d["unmeasured_call_count"] == 1
        assert d["elapsed_seconds"] == 120.5
        assert d["actual_sources"] == ["cli", "log"]
        assert d["started_at"] is not None

    def test_frozen(self):
        c = BudgetCounters()
        with pytest.raises(AttributeError):
            c.provider_calls = 5  # type: ignore[misc]

    def test_rejects_negative_provider_calls(self):
        with pytest.raises(BudgetCounterError, match="non-negative"):
            BudgetCounters(provider_calls=-1)

    def test_rejects_negative_tokens(self):
        with pytest.raises(BudgetCounterError, match="non-negative"):
            BudgetCounters(measured_token_total=-100)

    def test_rejects_boolean_provider_calls(self):
        with pytest.raises(BudgetCounterError, match="bool"):
            BudgetCounters(provider_calls=True)  # type: ignore[arg-type]

    def test_rejects_boolean_measured_count(self):
        with pytest.raises(BudgetCounterError, match="bool"):
            BudgetCounters(measured_call_count=True)  # type: ignore[arg-type]

    def test_rejects_negative_elapsed(self):
        with pytest.raises(BudgetCounterError, match="non-negative"):
            BudgetCounters(elapsed_seconds=-1.0)

    def test_rejects_inconsistent_call_counts(self):
        with pytest.raises(BudgetCounterError, match="!="):
            BudgetCounters(provider_calls=5, measured_call_count=1, unmeasured_call_count=1)

    def test_consistent_call_counts_pass(self):
        c = BudgetCounters(provider_calls=5, measured_call_count=3, unmeasured_call_count=2)
        assert c.provider_calls == 5

    def test_rejects_nan_elapsed(self):
        with pytest.raises(BudgetCounterError, match="finite"):
            BudgetCounters(elapsed_seconds=float("nan"))

    def test_rejects_inf_elapsed(self):
        with pytest.raises(BudgetCounterError, match="finite"):
            BudgetCounters(elapsed_seconds=float("inf"))

    def test_rejects_neg_inf_elapsed(self):
        with pytest.raises(BudgetCounterError, match="non-negative"):
            BudgetCounters(elapsed_seconds=float("-inf"))


class TestEvaluateNoBudgets:
    def test_none_budgets_not_exhausted(self):
        result = evaluate_budget(None, BudgetCounters())
        assert result.exhausted is False
        assert result.configured_limits is None
        assert result.first_exhausted_limit is None


class TestEvaluateProviderCalls:
    def test_under_limit(self):
        b = JobBudgets(max_provider_calls=10)
        c = BudgetCounters(provider_calls=5, measured_call_count=5)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False

    def test_at_limit(self):
        b = JobBudgets(max_provider_calls=10)
        c = BudgetCounters(provider_calls=10, measured_call_count=10)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_provider_calls"

    def test_over_limit(self):
        b = JobBudgets(max_provider_calls=10)
        c = BudgetCounters(provider_calls=15, measured_call_count=15)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_provider_calls"


class TestEvaluateTokens:
    def test_under_limit_all_measured(self):
        b = JobBudgets(max_total_tokens=100_000)
        c = BudgetCounters(provider_calls=5, measured_token_total=50_000, measured_call_count=5)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False
        assert r.token_lower_bound is False

    def test_at_limit_all_measured(self):
        b = JobBudgets(max_total_tokens=100_000)
        c = BudgetCounters(provider_calls=5, measured_token_total=100_000, measured_call_count=5)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_total_tokens"
        assert r.token_lower_bound is False

    def test_under_limit_with_unmeasured_warns(self):
        b = JobBudgets(max_total_tokens=100_000)
        c = BudgetCounters(
            provider_calls=5,
            measured_token_total=50_000,
            measured_call_count=3,
            unmeasured_call_count=2,
        )
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False
        assert r.token_lower_bound is True
        assert len(r.warnings) == 1
        assert "lower bound" in r.warnings[0]
        assert "2 calls unmeasured" in r.warnings[0]

    def test_over_limit_with_unmeasured(self):
        b = JobBudgets(max_total_tokens=100_000)
        c = BudgetCounters(
            provider_calls=5,
            measured_token_total=120_000,
            measured_call_count=4,
            unmeasured_call_count=1,
        )
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_total_tokens"
        assert r.token_lower_bound is True


class TestEvaluateWallClock:
    def test_under_limit(self):
        b = JobBudgets(max_wall_clock_minutes=60)
        c = BudgetCounters(elapsed_seconds=1800.0)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False

    def test_at_limit(self):
        b = JobBudgets(max_wall_clock_minutes=60)
        c = BudgetCounters(elapsed_seconds=3600.0)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_wall_clock_minutes"

    def test_over_limit(self):
        b = JobBudgets(max_wall_clock_minutes=10)
        c = BudgetCounters(elapsed_seconds=900.0)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True

    def test_wall_clock_from_started_at(self):
        started = T0 - timedelta(minutes=65)
        b = JobBudgets(max_wall_clock_minutes=60)
        c = BudgetCounters(started_at=started, elapsed_seconds=0.0)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_wall_clock_minutes"

    def test_wall_clock_started_at_under_limit(self):
        started = T0 - timedelta(minutes=30)
        b = JobBudgets(max_wall_clock_minutes=60)
        c = BudgetCounters(started_at=started, elapsed_seconds=0.0)
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False


class TestEvaluateDeadline:
    def test_before_deadline(self):
        dl = T0 + timedelta(hours=1)
        b = JobBudgets(deadline=dl)
        c = BudgetCounters()
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False

    def test_at_deadline(self):
        b = JobBudgets(deadline=T0)
        c = BudgetCounters()
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "deadline"

    def test_past_deadline(self):
        dl = T0 - timedelta(hours=1)
        b = JobBudgets(deadline=dl)
        c = BudgetCounters()
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "deadline"


class TestEvaluateMultipleLimits:
    def test_two_exhausted_first_by_priority(self):
        b = JobBudgets(max_provider_calls=5, max_total_tokens=1000)
        c = BudgetCounters(
            provider_calls=10,
            measured_token_total=2000,
            measured_call_count=10,
        )
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_provider_calls"

    def test_tokens_first_when_calls_ok(self):
        b = JobBudgets(max_provider_calls=50, max_total_tokens=1000)
        c = BudgetCounters(
            provider_calls=5,
            measured_token_total=2000,
            measured_call_count=5,
        )
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_total_tokens"

    def test_all_four_exhausted(self):
        dl = T0 - timedelta(hours=1)
        b = JobBudgets(
            max_provider_calls=1,
            max_total_tokens=100,
            max_wall_clock_minutes=1,
            deadline=dl,
        )
        c = BudgetCounters(
            provider_calls=5,
            measured_token_total=500,
            measured_call_count=5,
            elapsed_seconds=600.0,
        )
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_provider_calls"

    def test_no_limits_configured_not_exhausted(self):
        b = JobBudgets()
        c = BudgetCounters(
            provider_calls=999,
            measured_token_total=999_999,
            measured_call_count=999,
            elapsed_seconds=99999.0,
        )
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False


class TestEvaluationSerialization:
    def test_to_json_structure(self):
        b = JobBudgets(max_provider_calls=10)
        c = BudgetCounters(provider_calls=5, measured_call_count=5, evaluated_at=T0)
        r = evaluate_budget(b, c, now=T0)
        d = r.to_json()
        assert "configured_limits" in d
        assert "counters" in d
        assert "exhausted" in d
        assert d["exhausted"] is False
        assert d["configured_limits"]["max_provider_calls"] == 10

    def test_to_json_none_budgets(self):
        r = evaluate_budget(None, BudgetCounters(evaluated_at=T0))
        d = r.to_json()
        assert d["configured_limits"] is None
        assert d["exhausted"] is False


class TestSourceDescriptions:
    def test_provider_calls_source(self):
        b = JobBudgets(max_provider_calls=10)
        c = BudgetCounters(provider_calls=5, measured_call_count=5)
        r = evaluate_budget(b, c, now=T0)
        assert any("provider_calls: 5/10" in s for s in r.source_descriptions)

    def test_tokens_source(self):
        b = JobBudgets(max_total_tokens=100_000)
        c = BudgetCounters(provider_calls=1, measured_token_total=50_000, measured_call_count=1)
        r = evaluate_budget(b, c, now=T0)
        assert any("tokens:" in s for s in r.source_descriptions)

    def test_wall_clock_source(self):
        b = JobBudgets(max_wall_clock_minutes=60)
        c = BudgetCounters(elapsed_seconds=1800.0)
        r = evaluate_budget(b, c, now=T0)
        assert any("wall_clock:" in s for s in r.source_descriptions)

    def test_deadline_source(self):
        dl = T0 + timedelta(hours=1)
        b = JobBudgets(deadline=dl)
        c = BudgetCounters()
        r = evaluate_budget(b, c, now=T0)
        assert any("deadline:" in s for s in r.source_descriptions)


class TestCollectCountersFromActuals:
    def test_basic_collection(self):
        actuals = {
            "provider_call_count": 5,
            "actual_call_count": 4,
            "total_tokens": 10000,
        }
        c = collect_counters_from_actuals(actuals, now=T0)
        assert c.provider_calls == 5
        assert c.measured_call_count == 4
        assert c.unmeasured_call_count == 1
        assert c.measured_token_total == 10000

    def test_with_started_at(self):
        actuals = {"provider_call_count": 1, "actual_call_count": 1, "total_tokens": 500}
        started = T0 - timedelta(minutes=10)
        c = collect_counters_from_actuals(actuals, started_at=started, now=T0)
        assert c.elapsed_seconds == pytest.approx(600.0)
        assert c.started_at == started

    def test_no_provider_calls(self):
        actuals = {"provider_call_count": 0, "actual_call_count": 0, "total_tokens": 0}
        c = collect_counters_from_actuals(actuals, now=T0)
        assert c.provider_calls == 0
        assert c.measured_call_count == 0

    def test_all_unmeasured(self):
        actuals = {"provider_call_count": 3, "actual_call_count": 0, "total_tokens": 0}
        c = collect_counters_from_actuals(actuals, now=T0)
        assert c.provider_calls == 3
        assert c.unmeasured_call_count == 3
        assert c.has_unmeasured is True
