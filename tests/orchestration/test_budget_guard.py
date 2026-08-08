"""F018 T002 — budget_guard evaluation tests."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from packages.core.models import Job, JobBudgets
from packages.orchestration.budget_guard import (
    BudgetCounterError,
    BudgetCounters,
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
        c = BudgetCounters(provider_calls=5, measured_call_count=3, unmeasured_call_count=2, actual_sources=("pingpong_actuals",))
        assert c.total_call_count == 5

    def test_has_unmeasured(self):
        c = BudgetCounters(provider_calls=1, measured_call_count=0, unmeasured_call_count=1)
        assert c.has_unmeasured is True

    def test_token_description_all_measured(self):
        c = BudgetCounters(provider_calls=1, measured_token_total=5000, measured_call_count=1, actual_sources=("pingpong_actuals",))
        assert c.token_description() == "5000 tokens"

    def test_token_description_with_unmeasured(self):
        c = BudgetCounters(
            provider_calls=3, measured_token_total=5000,
            measured_call_count=1, unmeasured_call_count=2,
            actual_sources=("pingpong_actuals",),
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
            actual_sources=("pingpong_actuals", "token_actuals"),
        )
        d = c.to_json()
        assert d["provider_calls"] == 5
        assert d["measured_token_total"] == 10000
        assert d["measured_call_count"] == 4
        assert d["unmeasured_call_count"] == 1
        assert d["elapsed_seconds"] == 120.5
        assert d["actual_sources"] == ["pingpong_actuals", "token_actuals"]
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
            BudgetCounters(provider_calls=5, measured_call_count=1, unmeasured_call_count=1, actual_sources=("pingpong_actuals",))

    def test_consistent_call_counts_pass(self):
        c = BudgetCounters(provider_calls=5, measured_call_count=3, unmeasured_call_count=2, actual_sources=("pingpong_actuals",))
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
        c = BudgetCounters(provider_calls=5, measured_call_count=5, actual_sources=("pingpong_actuals",))
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False

    def test_at_limit(self):
        b = JobBudgets(max_provider_calls=10)
        c = BudgetCounters(provider_calls=10, measured_call_count=10, actual_sources=("pingpong_actuals",))
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_provider_calls"

    def test_over_limit(self):
        b = JobBudgets(max_provider_calls=10)
        c = BudgetCounters(provider_calls=15, measured_call_count=15, actual_sources=("pingpong_actuals",))
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_provider_calls"


class TestEvaluateTokens:
    def test_under_limit_all_measured(self):
        b = JobBudgets(max_total_tokens=100_000)
        c = BudgetCounters(provider_calls=5, measured_token_total=50_000, measured_call_count=5, actual_sources=("pingpong_actuals",))
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False
        assert r.token_lower_bound is False

    def test_at_limit_all_measured(self):
        b = JobBudgets(max_total_tokens=100_000)
        c = BudgetCounters(provider_calls=5, measured_token_total=100_000, measured_call_count=5, actual_sources=("pingpong_actuals",))
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
            actual_sources=("pingpong_actuals",),
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
            actual_sources=("pingpong_actuals",),
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
            actual_sources=("pingpong_actuals",),
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
            actual_sources=("pingpong_actuals",),
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
            actual_sources=("pingpong_actuals",),
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
            actual_sources=("pingpong_actuals",),
        )
        r = evaluate_budget(b, c, now=T0)
        assert r.exhausted is False


class TestEvaluationSerialization:
    def test_to_json_structure(self):
        b = JobBudgets(max_provider_calls=10)
        c = BudgetCounters(provider_calls=5, measured_call_count=5, evaluated_at=T0, actual_sources=("pingpong_actuals",))
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
        c = BudgetCounters(provider_calls=5, measured_call_count=5, actual_sources=("pingpong_actuals",))
        r = evaluate_budget(b, c, now=T0)
        assert any("provider_calls: 5/10" in s for s in r.source_descriptions)

    def test_tokens_source(self):
        b = JobBudgets(max_total_tokens=100_000)
        c = BudgetCounters(provider_calls=1, measured_token_total=50_000, measured_call_count=1, actual_sources=("pingpong_actuals",))
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


class TestRunContractConsolidation:
    def test_contract_inherits_tokens_from_budgets(self):
        from packages.orchestration.run_contract import build_default_run_contract
        job = Job(name="test", budgets=JobBudgets(max_total_tokens=50000))
        c = build_default_run_contract(job)
        assert c.max_tokens == 50000

    def test_contract_inherits_runtime_from_budgets(self):
        from packages.orchestration.run_contract import build_default_run_contract
        job = Job(name="test", budgets=JobBudgets(max_wall_clock_minutes=30))
        c = build_default_run_contract(job)
        assert c.max_runtime_seconds == 1800

    def test_contract_defaults_without_budgets(self):
        from packages.orchestration.run_contract import build_default_run_contract
        job = Job(name="test")
        c = build_default_run_contract(job)
        assert c.max_tokens == 200_000
        assert c.max_runtime_seconds == 600

    def test_contract_partial_budgets_only_overrides_set_fields(self):
        from packages.orchestration.run_contract import build_default_run_contract
        job = Job(name="test", budgets=JobBudgets(max_total_tokens=80000))
        c = build_default_run_contract(job)
        assert c.max_tokens == 80000
        assert c.max_runtime_seconds == 600

    def test_no_contradictory_evaluation(self):
        from packages.orchestration.run_contract import RunUsage, build_default_run_contract, check_budget
        job = Job(name="test", budgets=JobBudgets(max_total_tokens=10000))
        c = build_default_run_contract(job)
        assert c.max_tokens == 10000
        usage = RunUsage(tokens_used=5000)
        status = check_budget(c, usage)
        assert "max_tokens" not in status.exhausted_budgets
        counters = BudgetCounters(
            provider_calls=1, measured_token_total=5000, measured_call_count=1,
            actual_sources=("pingpong_actuals",),
        )
        evaluation = evaluate_budget(job.budgets, counters, now=T0)
        assert evaluation.exhausted is False


# --- F104 T001: the max_cost_usd money limit -------------------------------
# A cost of None means UNPRICED. Every assertion below exists so that None can
# never quietly become 0.0 (P6).

_PRICED_SOURCES = ("token_actuals",)


def _cost_counters(cost, *, calls=2, unpriced=0):
    """Counters whose token side is fixed so only the money side varies."""
    return BudgetCounters(
        provider_calls=calls,
        measured_token_total=100,
        measured_call_count=calls,
        unmeasured_call_count=0,
        actual_sources=_PRICED_SOURCES,
        evaluated_at=T0,
        measured_cost_usd=cost,
        unpriced_call_count=unpriced,
    )


class TestCostDescription:
    def test_no_cost_at_all_is_not_measured(self):
        c = BudgetCounters(provider_calls=1, unmeasured_call_count=1, unpriced_call_count=1)
        assert c.cost_description() == "not-measured"
        assert c.measured_cost_usd is None

    def test_fully_priced_renders_the_amount(self):
        assert _cost_counters(1.5).cost_description() == "$1.5000"

    def test_partially_priced_renders_a_lower_bound(self):
        c = _cost_counters(0.25, calls=3, unpriced=1)
        assert c.cost_description() == ">= $0.2500 (1 provider calls unpriced)"

    def test_measured_zero_is_not_the_unmeasured_string(self):
        assert _cost_counters(0.0).cost_description() == "$0.0000"
        assert _cost_counters(0.0).cost_description() != "not-measured"

    def test_has_unpriced_mirrors_has_unmeasured(self):
        assert _cost_counters(1.0).has_unpriced is False
        assert _cost_counters(1.0, calls=3, unpriced=2).has_unpriced is True


class TestBudgetCountersCostValidation:
    def test_negative_cost_rejected(self):
        with pytest.raises(BudgetCounterError, match="measured_cost_usd.*non-negative"):
            BudgetCounters(measured_cost_usd=-0.01)

    def test_nan_cost_rejected(self):
        with pytest.raises(BudgetCounterError, match="measured_cost_usd.*finite"):
            BudgetCounters(measured_cost_usd=float("nan"))

    def test_infinite_cost_rejected(self):
        with pytest.raises(BudgetCounterError, match="measured_cost_usd.*finite"):
            BudgetCounters(measured_cost_usd=float("inf"))

    def test_bool_cost_rejected(self):
        with pytest.raises(BudgetCounterError, match="measured_cost_usd.*bool"):
            BudgetCounters(measured_cost_usd=True)  # type: ignore[arg-type]

    def test_unpriced_count_above_provider_calls_rejected(self):
        with pytest.raises(BudgetCounterError, match="unpriced_call_count.*provider_calls"):
            BudgetCounters(
                provider_calls=1, unmeasured_call_count=1, unpriced_call_count=2)

    def test_bool_unpriced_count_rejected(self):
        with pytest.raises(BudgetCounterError, match="unpriced_call_count.*bool"):
            BudgetCounters(unpriced_call_count=True)  # type: ignore[arg-type]

    def test_negative_unpriced_count_rejected(self):
        with pytest.raises(BudgetCounterError, match="unpriced_call_count.*non-negative"):
            BudgetCounters(unpriced_call_count=-1)

    def test_positive_cost_with_every_call_unpriced_is_impossible(self):
        with pytest.raises(BudgetCounterError, match="all 2 provider calls are unpriced"):
            BudgetCounters(
                provider_calls=2,
                unmeasured_call_count=2,
                unpriced_call_count=2,
                measured_cost_usd=1.0,
            )

    def test_zero_cost_with_every_call_unpriced_is_allowed(self):
        c = BudgetCounters(
            provider_calls=2, unmeasured_call_count=2,
            unpriced_call_count=2, measured_cost_usd=0.0)
        assert c.measured_cost_usd == 0.0

    def test_json_keeps_unpriced_as_null_not_zero(self):
        j = BudgetCounters(provider_calls=1, unmeasured_call_count=1,
                           unpriced_call_count=1).to_json()
        assert j["measured_cost_usd"] is None
        assert j["unpriced_call_count"] == 1


class TestEvaluateCostLimit:
    def test_priced_over_limit_is_exhausted(self):
        r = evaluate_budget(JobBudgets(max_cost_usd=1.0), _cost_counters(2.5), now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_cost_usd"
        assert r.cost_lower_bound is False

    def test_priced_at_limit_is_exhausted(self):
        r = evaluate_budget(JobBudgets(max_cost_usd=2.5), _cost_counters(2.5), now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_cost_usd"

    def test_priced_under_limit_is_not_exhausted(self):
        r = evaluate_budget(JobBudgets(max_cost_usd=10.0), _cost_counters(2.5), now=T0)
        assert r.exhausted is False
        assert r.first_exhausted_limit is None
        assert r.cost_lower_bound is False
        assert r.warnings == ()

    def test_unpriced_mixed_over_limit_is_a_definite_breach(self):
        # A lower bound already past the limit cannot be undone by pricing more.
        c = _cost_counters(5.0, calls=4, unpriced=2)
        r = evaluate_budget(JobBudgets(max_cost_usd=1.0), c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_cost_usd"
        assert r.cost_lower_bound is True

    def test_unpriced_mixed_under_limit_only_warns(self):
        c = _cost_counters(0.5, calls=4, unpriced=3)
        r = evaluate_budget(JobBudgets(max_cost_usd=100.0), c, now=T0)
        assert r.exhausted is False
        assert r.cost_lower_bound is True
        assert any("3 calls unpriced" in w for w in r.warnings)

    def test_fully_unpriced_never_renders_as_zero(self):
        c = BudgetCounters(
            provider_calls=3, unmeasured_call_count=3, unpriced_call_count=3,
            evaluated_at=T0)
        r = evaluate_budget(JobBudgets(max_cost_usd=2.0), c, now=T0)
        assert r.exhausted is False
        assert r.cost_lower_bound is True
        assert r.warnings
        # The unknown stays a null everywhere it can be read.
        assert r.counters.measured_cost_usd is None
        assert r.to_json()["counters"]["measured_cost_usd"] is None
        rendered = " ".join(r.source_descriptions)
        assert "not-measured" in rendered
        assert "$0.0000/" not in rendered

    def test_no_usd_limit_leaves_the_cost_path_inert(self):
        c = _cost_counters(999.0)
        r = evaluate_budget(JobBudgets(max_total_tokens=1_000_000), c, now=T0)
        assert r.exhausted is False
        assert r.cost_lower_bound is False
        assert not any("cost:" in s for s in r.source_descriptions)
        pre_feature = evaluate_budget(
            JobBudgets(max_total_tokens=1_000_000),
            BudgetCounters(
                provider_calls=2, measured_token_total=100, measured_call_count=2,
                actual_sources=_PRICED_SOURCES, evaluated_at=T0),
            now=T0,
        )
        assert r.to_json()["cost_lower_bound"] == pre_feature.to_json()["cost_lower_bound"]
        assert pre_feature.to_json()["counters"]["measured_cost_usd"] is None

    def test_token_limit_wins_the_ordering_when_both_breach(self):
        c = BudgetCounters(
            provider_calls=2, measured_token_total=10_000, measured_call_count=2,
            actual_sources=_PRICED_SOURCES, evaluated_at=T0, measured_cost_usd=50.0)
        r = evaluate_budget(
            JobBudgets(max_total_tokens=100, max_cost_usd=1.0), c, now=T0)
        assert r.exhausted is True
        assert r.first_exhausted_limit == "max_total_tokens"

    def test_collect_counters_from_actuals_passes_money_through(self):
        c = collect_counters_from_actuals(
            {"provider_call_count": 3, "actual_call_count": 2, "total_tokens": 40},
            now=T0,
            actual_sources=_PRICED_SOURCES,
            measured_cost_usd=0.75,
            unpriced_call_count=1,
        )
        assert c.measured_cost_usd == 0.75
        assert c.unpriced_call_count == 1

    def test_collect_counters_from_actuals_defaults_to_unpriced(self):
        c = collect_counters_from_actuals(
            {"provider_call_count": 1, "actual_call_count": 1, "total_tokens": 10},
            now=T0, actual_sources=_PRICED_SOURCES)
        assert c.measured_cost_usd is None
        assert c.unpriced_call_count == 0


class TestCollectLedgerCostForJob:
    """The read-only bridge from the F103 ledger into the budget counters."""

    def _record(self, path, *, call_id, job_id, cost):
        from packages.orchestration.token_ledger import (
            COST_BASIS_PROVIDER_REPORTED,
            COST_BASIS_UNKNOWN,
            CallRecord,
            record_call,
        )
        ok = record_call(
            CallRecord(
                call_id=call_id,
                job_id=job_id,
                ts_utc="2026-08-08T10:00:00+00:00",
                cost_usd=cost,
                cost_basis=(
                    COST_BASIS_PROVIDER_REPORTED if cost is not None
                    else COST_BASIS_UNKNOWN
                ),
            ),
            path=path,
        )
        assert ok is True

    def test_priced_and_unpriced_calls_return_the_right_triple(self, tmp_path):
        from packages.orchestration.budget_guard import collect_ledger_cost_for_job
        ledger = tmp_path / "ledger.sqlite"
        self._record(ledger, call_id="c1", job_id="job-a", cost=1.25)
        self._record(ledger, call_id="c2", job_id="job-a", cost=0.75)
        self._record(ledger, call_id="c3", job_id="job-a", cost=None)
        self._record(ledger, call_id="c4", job_id="job-b", cost=99.0)

        cost, priced, unpriced = collect_ledger_cost_for_job(
            job_id="job-a", path=ledger)
        assert cost == pytest.approx(2.0)
        assert priced == 2
        assert unpriced == 1

    def test_all_unpriced_job_keeps_the_cost_null(self, tmp_path):
        from packages.orchestration.budget_guard import collect_ledger_cost_for_job
        ledger = tmp_path / "ledger.sqlite"
        self._record(ledger, call_id="u1", job_id="job-c", cost=None)
        self._record(ledger, call_id="u2", job_id="job-c", cost=None)

        cost, priced, unpriced = collect_ledger_cost_for_job(
            job_id="job-c", path=ledger)
        assert cost is None
        assert priced == 0
        assert unpriced == 2

    def test_missing_ledger_returns_none_and_creates_nothing(self, tmp_path):
        from packages.orchestration.budget_guard import collect_ledger_cost_for_job
        ledger = tmp_path / "never-created.sqlite"
        assert collect_ledger_cost_for_job(job_id="job-x", path=ledger) == (None, 0, 0)
        assert not ledger.exists()
