"""F104 T002 — the pure predictive next-task cost engine.

Covers ``predict_next_task_cost`` / ``BudgetPrediction`` in
``packages.orchestration.budget_guard`` and the operator inputs they run on,
``resolve_predictive_budget_config`` in
``packages.orchestration.budget_resolution``.

Two rules are load-bearing and each has its own test rather than being folded
into a happy path:

* P6 — an unmeasured figure is never rendered or computed as a measured zero.
  A missing price basis leaves ``expected_cost_usd`` None and renders
  ``not-measured``; it never becomes ``$0.0000``.
* The exact-limit boundary belongs to the REACTIVE check in ``evaluate_budget``.
  The prediction uses a strict ``>`` so the two can never disagree about it.

There is deliberately NO test here that the job loop calls this engine: it has
no production caller yet, by design (F104 R3 wires it at the task-dispatch safe
point). ``TestLiveSafePointReadsTheLedgerCost`` in ``test_budget_guard.py`` is
where the live wiring of the REACTIVE cost path is pinned.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import (
    VALID_ESTIMATE_BASES,
    BudgetCounters,
    BudgetPrediction,
    predict_next_task_cost,
)
from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.token_economy import TokenBand

UTC = timezone.utc
T0 = datetime(2026, 8, 9, 12, 0, 0, tzinfo=UTC)

# 8000 / 32000 / 120000 are the documented class defaults; the tests spell them
# out rather than importing the fallback so a silent change to them is caught.
CLASS_DEFAULTS = {TokenBand.LOW: 8000, TokenBand.MEDIUM: 32000, TokenBand.HIGH: 120000}
LARGEST_CLASS_DEFAULT = 120000


def _config(price_basis: float | None, defaults: dict | None = None):
    return PredictiveBudgetConfig(
        price_basis_usd_per_1k_tokens=price_basis,
        class_default_tokens=dict(CLASS_DEFAULTS if defaults is None else defaults),
    )


def _counters(*, spent: float | None, provider_calls: int = 4, unpriced: int = 0):
    """Priced-and-measured counters, or unpriced ones when ``spent`` is None."""
    return BudgetCounters(
        provider_calls=provider_calls,
        measured_call_count=provider_calls,
        unmeasured_call_count=0,
        measured_token_total=1000 * provider_calls,
        actual_sources=("pingpong_actuals",) if provider_calls else (),
        evaluated_at=T0,
        measured_cost_usd=spent,
        unpriced_call_count=unpriced,
    )


class TestEstimateBasisVocabulary:
    def test_valid_bases_are_exactly_the_five_documented_labels(self):
        assert VALID_ESTIMATE_BASES == frozenset({
            "class_default",
            "class_default_missing_band",
            "no_price_basis",
            "no_cost_limit",
            "unpriced_spend",
        })

    @pytest.mark.parametrize(
        "budgets,counters_kwargs,band,price_basis,expected_basis,expected_breach",
        [
            # A band was known and priced: the ordinary case.
            (JobBudgets(max_cost_usd=10.0), {"spent": 1.0}, TokenBand.MEDIUM,
             0.01, "class_default", False),
            # No band could be derived: the A9 path.
            (JobBudgets(max_cost_usd=10.0), {"spent": 1.0}, None,
             0.01, "class_default_missing_band", False),
            # No price basis configured: inert (DECISION F104 D4).
            (JobBudgets(max_cost_usd=10.0), {"spent": 1.0}, TokenBand.MEDIUM,
             None, "no_price_basis", False),
            # No money limit at all: nothing to predict against.
            (JobBudgets(max_total_tokens=1000), {"spent": 1.0}, TokenBand.MEDIUM,
             0.01, "no_cost_limit", False),
            # Spend so far is unknown, and calls WERE made.
            (JobBudgets(max_cost_usd=10.0), {"spent": None, "unpriced": 4},
             TokenBand.MEDIUM, 0.01, "unpriced_spend", False),
        ],
        ids=["class_default", "missing_band", "no_price_basis", "no_cost_limit",
             "unpriced_spend"],
    )
    def test_each_basis_is_reachable_and_reports_its_breach_verdict(
        self, budgets, counters_kwargs, band, price_basis, expected_basis,
        expected_breach,
    ):
        p = predict_next_task_cost(
            budgets, _counters(**counters_kwargs),
            band=band, config=_config(price_basis))
        assert p.estimate_basis == expected_basis
        assert p.would_breach is expected_breach
        # Every observed label is a member of the declared vocabulary.
        assert p.estimate_basis in VALID_ESTIMATE_BASES

    def test_basis_is_always_a_non_empty_member_of_the_vocabulary(self):
        for band in (TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH,
                     TokenBand.UNKNOWN, None, "nonsense"):
            for price_basis in (None, 0.01):
                for budgets in (None, JobBudgets(max_cost_usd=10.0)):
                    for spent in (None, 0.0, 3.0):
                        p = predict_next_task_cost(
                            budgets, _counters(spent=spent, unpriced=4 if spent is None else 0),
                            band=band, config=_config(price_basis))
                        assert p.estimate_basis
                        assert p.estimate_basis in VALID_ESTIMATE_BASES


class TestBreachBoundary:
    def test_over_the_limit_breaches(self):
        # 8000 tokens x $0.02/1k = $0.16; 1.90 + 0.16 = 2.06 > 2.00.
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=1.90),
            band=TokenBand.LOW, config=_config(0.02))
        assert p.estimate_basis == "class_default"
        assert p.expected_tokens == 8000
        assert p.expected_cost_usd == pytest.approx(0.16)
        assert p.would_breach is True

    def test_exactly_at_the_limit_does_not_breach(self):
        # 8000 tokens x $0.125/1k = $1.00 exactly; 1.00 + 1.00 == 2.00.
        # The reactive check in evaluate_budget owns this boundary; predicting a
        # breach here would make the two disagree about the same number.
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=1.0),
            band=TokenBand.LOW, config=_config(0.125))
        assert p.expected_cost_usd == pytest.approx(1.0)
        assert p.spent_cost_usd + p.expected_cost_usd == pytest.approx(p.limit_usd)
        assert p.would_breach is False

    def test_just_under_the_limit_does_not_breach(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=0.5),
            band=TokenBand.LOW, config=_config(0.02))
        assert p.would_breach is False

    def test_already_over_the_limit_breaches(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=7.5),
            band=TokenBand.LOW, config=_config(0.02))
        assert p.spent_cost_usd == 7.5
        assert p.would_breach is True

    def test_expected_cost_is_tokens_over_1000_times_the_price_basis(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=100.0), _counters(spent=0.0),
            band=TokenBand.HIGH, config=_config(0.003))
        assert p.expected_tokens == 120000
        assert p.expected_cost_usd == pytest.approx(120000 / 1000 * 0.003)


class TestMissingBandTakesTheLargestClassDefault:
    @pytest.mark.parametrize(
        "band", [None, TokenBand.UNKNOWN, "unknown", "not-a-band", ""],
        ids=["none", "TokenBand.UNKNOWN", "literal-unknown", "unrecognised", "empty"],
    )
    def test_missing_band_uses_the_largest_default_and_says_so(self, band):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=100.0), _counters(spent=1.0),
            band=band, config=_config(0.01))
        assert p.band == "unknown"
        assert p.estimate_basis == "class_default_missing_band"
        assert p.expected_tokens == LARGEST_CLASS_DEFAULT
        assert p.expected_tokens == max(CLASS_DEFAULTS.values())

    def test_a_known_band_uses_its_own_default_not_the_largest(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=100.0), _counters(spent=1.0),
            band=TokenBand.LOW, config=_config(0.01))
        assert p.band == TokenBand.LOW
        assert p.expected_tokens == CLASS_DEFAULTS[TokenBand.LOW]
        assert p.estimate_basis == "class_default"

    def test_missing_band_over_stopping_beats_overspending(self):
        # The conservative choice must be able to actually stop: the largest
        # default at the same price breaches where a low band would not.
        budgets, config = JobBudgets(max_cost_usd=2.0), _config(0.01)
        low = predict_next_task_cost(
            budgets, _counters(spent=1.0), band=TokenBand.LOW, config=config)
        missing = predict_next_task_cost(
            budgets, _counters(spent=1.0), band=None, config=config)
        assert low.would_breach is False
        assert missing.would_breach is True


class TestNoPriceBasisIsInert:
    def test_no_price_basis_predicts_nothing_and_breaches_nothing(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=1.0),
            band=TokenBand.MEDIUM, config=_config(None))
        assert p.estimate_basis == "no_price_basis"
        assert p.expected_cost_usd is None
        assert p.would_breach is False

    def test_the_unpredicted_cost_renders_as_not_measured_never_as_zero(self):
        # P6. The spent figure here is a real measurement ($1.00) so it renders
        # as money; only the EXPECTED figure is unmeasured, and it says so.
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=1.0),
            band=TokenBand.MEDIUM, config=_config(None))
        assert "expected not-measured" in p.arithmetic
        assert "expected $0.0000" not in p.arithmetic
        assert "$1.0000" in p.arithmetic

    def test_no_cost_limit_renders_the_limit_as_not_measured(self):
        p = predict_next_task_cost(
            None, _counters(spent=1.0), band=TokenBand.MEDIUM, config=_config(0.01))
        assert p.estimate_basis == "no_cost_limit"
        assert p.limit_usd is None
        assert p.would_breach is False
        assert "limit not-measured" in p.arithmetic


class TestUnknownSpend:
    def test_unpriced_spend_with_provider_calls_does_not_breach(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=0.01), _counters(spent=None, provider_calls=4, unpriced=4),
            band=TokenBand.HIGH, config=_config(1.0))
        assert p.estimate_basis == "unpriced_spend"
        assert p.spent_cost_usd is None
        # Even though the expected cost alone dwarfs the limit: an unknown
        # baseline cannot be added to, so no honest comparison exists.
        assert p.would_breach is False
        assert "spent not-measured" in p.arithmetic

    def test_zero_provider_calls_means_a_measured_zero_and_prediction_proceeds(self):
        # A job that has made NO provider call has definitionally spent nothing,
        # so 0.0 there is a measurement rather than an assumed zero.
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=None, provider_calls=0),
            band=TokenBand.MEDIUM, config=_config(0.01))
        assert p.estimate_basis == "class_default"
        assert p.spent_cost_usd == 0.0
        assert p.would_breach is False

    def test_zero_provider_calls_can_still_breach_on_the_expected_cost_alone(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=0.10), _counters(spent=None, provider_calls=0),
            band=TokenBand.MEDIUM, config=_config(0.01))
        assert p.estimate_basis == "class_default"
        assert p.spent_cost_usd == 0.0
        assert p.would_breach is True


class TestPredictionJsonAndArithmetic:
    def test_to_json_carries_the_estimate_basis(self):
        # The grep-style pin F104 T003 extends: the label travels with the
        # numbers wherever a prediction surfaces.
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=10.0), _counters(spent=1.0),
            band=TokenBand.MEDIUM, config=_config(0.01))
        data = p.to_json()
        assert data["estimate_basis"] == "class_default"
        assert set(data) == {
            "would_breach", "estimate_basis", "band", "expected_tokens",
            "expected_cost_usd", "spent_cost_usd", "limit_usd", "arithmetic",
        }

    def test_to_json_keeps_an_unpredicted_cost_as_null(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=10.0), _counters(spent=1.0),
            band=TokenBand.MEDIUM, config=_config(None))
        data = p.to_json()
        assert data["expected_cost_usd"] is None
        assert data["estimate_basis"] == "no_price_basis"

    def test_to_json_is_a_plain_serializable_dict(self):
        import json
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=10.0), _counters(spent=1.0),
            band=TokenBand.MEDIUM, config=_config(0.01))
        assert json.loads(json.dumps(p.to_json())) == p.to_json()

    def test_arithmetic_is_one_non_empty_line_carrying_the_whole_comparison(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=1.90),
            band=TokenBand.LOW, config=_config(0.02))
        line = p.arithmetic
        assert line
        assert "\n" not in line
        assert "spent $1.9000" in line
        assert "expected $0.1600" in line
        assert "limit $2.0000" in line
        assert "basis=class_default" in line
        assert "band=low" in line
        assert "8000 tokens" in line

    def test_the_prediction_is_frozen(self):
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=2.0), _counters(spent=1.0),
            band=TokenBand.LOW, config=_config(0.02))
        assert isinstance(p, BudgetPrediction)
        with pytest.raises(Exception):
            p.would_breach = True


class TestResolvePredictiveBudgetConfig:
    """Operator inputs: env > TOML > documented default, same as the limits."""

    def test_documented_defaults_when_nothing_is_configured(self):
        from packages.orchestration.budget_resolution import (
            resolve_predictive_budget_config,
        )
        cfg = resolve_predictive_budget_config()
        # No price is ever invented (DECISION F104 D4).
        assert cfg.price_basis_usd_per_1k_tokens is None
        assert cfg.class_default_tokens == {
            TokenBand.LOW: 8000,
            TokenBand.MEDIUM: 32000,
            TokenBand.HIGH: 120000,
        }

    def test_the_default_config_makes_the_predictor_inert(self):
        from packages.orchestration.budget_resolution import (
            resolve_predictive_budget_config,
        )
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=0.0001), _counters(spent=1.0),
            band=TokenBand.HIGH, config=resolve_predictive_budget_config())
        assert p.estimate_basis == "no_price_basis"
        assert p.would_breach is False

    def test_toml_sets_the_price_basis_and_the_class_defaults(self, tmp_path):
        from packages.orchestration.budget_resolution import (
            resolve_predictive_budget_config,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text(
            "[remedy.budget]\n"
            "price_basis_usd_per_1k_tokens = 0.004\n"
            "class_default_tokens_low = 1111\n"
            "class_default_tokens_medium = 2222\n"
            "class_default_tokens_high = 3333\n"
        )
        cfg = resolve_predictive_budget_config(config_path=str(toml))
        assert cfg.price_basis_usd_per_1k_tokens == 0.004
        assert cfg.class_default_tokens == {
            TokenBand.LOW: 1111, TokenBand.MEDIUM: 2222, TokenBand.HIGH: 3333,
        }

    def test_toml_may_set_only_the_price_basis(self, tmp_path):
        from packages.orchestration.budget_resolution import (
            resolve_predictive_budget_config,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.budget]\nprice_basis_usd_per_1k_tokens = 0.02\n")
        cfg = resolve_predictive_budget_config(config_path=str(toml))
        assert cfg.price_basis_usd_per_1k_tokens == 0.02
        assert cfg.class_default_tokens[TokenBand.MEDIUM] == 32000

    def test_env_sets_the_price_basis(self, monkeypatch):
        from packages.orchestration.budget_resolution import (
            resolve_predictive_budget_config,
        )
        monkeypatch.setenv("REMEDY_BUDGET_PRICE_BASIS_USD_PER_1K_TOKENS", "0.015")
        cfg = resolve_predictive_budget_config()
        assert cfg.price_basis_usd_per_1k_tokens == 0.015

    def test_env_sets_a_class_default(self, monkeypatch):
        from packages.orchestration.budget_resolution import (
            resolve_predictive_budget_config,
        )
        monkeypatch.setenv("REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_HIGH", "999999")
        cfg = resolve_predictive_budget_config()
        assert cfg.class_default_tokens[TokenBand.HIGH] == 999999
        assert cfg.class_default_tokens[TokenBand.LOW] == 8000

    def test_env_beats_toml(self, tmp_path, monkeypatch):
        from packages.orchestration.budget_resolution import (
            resolve_predictive_budget_config,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.budget]\nprice_basis_usd_per_1k_tokens = 0.004\n")
        monkeypatch.setenv("REMEDY_BUDGET_PRICE_BASIS_USD_PER_1K_TOKENS", "0.09")
        cfg = resolve_predictive_budget_config(config_path=str(toml))
        assert cfg.price_basis_usd_per_1k_tokens == 0.09

    def test_a_configured_price_basis_makes_the_predictor_live(self, tmp_path):
        from packages.orchestration.budget_resolution import (
            resolve_predictive_budget_config,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.budget]\nprice_basis_usd_per_1k_tokens = 0.01\n")
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=0.10), _counters(spent=0.0),
            band=TokenBand.MEDIUM,
            config=resolve_predictive_budget_config(config_path=str(toml)))
        assert p.estimate_basis == "class_default"
        assert p.expected_cost_usd == pytest.approx(0.32)
        assert p.would_breach is True

    def test_a_malformed_price_basis_fails_closed(self, tmp_path):
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_predictive_budget_config,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nprice_basis_usd_per_1k_tokens = "free"\n')
        with pytest.raises(BudgetConfigError):
            resolve_predictive_budget_config(config_path=str(toml))
