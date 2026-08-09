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

Since F104 R4 the engine has a PRODUCTION CALLER: ``run_job``'s ``_stop_check``
at the task-dispatch safe point. ``TestPredictiveStopAtTheLiveDispatchSafePoint``
below drives the real ``run_job`` end to end for that wiring — a unit gate on a
pure function cannot tell a wired engine from an unwired one, which is exactly
what R-0222 was. ``TestLiveSafePointReadsTheLedgerCost`` in
``test_budget_guard.py`` pins the REACTIVE cost path at the same safe point.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import (
    VALID_ESTIMATE_BASES,
    BudgetCounters,
    BudgetPrediction,
    derive_next_task_token_band,
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


def _counters(*, spent: float | None, provider_calls: int = 4, unpriced: int = 0,
              priced: int | None = None):
    """Priced-and-measured counters, or unpriced ones when ``spent`` is None.

    ``priced`` defaults to ``provider_calls - unpriced`` so a caller pairing a
    real ``spent`` with an ``unpriced`` count does not trip the cost-side
    contradiction check added in R3 (a priced total with zero priced calls).
    """
    return BudgetCounters(
        provider_calls=provider_calls,
        measured_call_count=provider_calls,
        unmeasured_call_count=0,
        measured_token_total=1000 * provider_calls,
        actual_sources=("pingpong_actuals",) if provider_calls else (),
        evaluated_at=T0,
        measured_cost_usd=spent,
        unpriced_call_count=unpriced,
        priced_call_count=(provider_calls - unpriced) if priced is None else priced,
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


class TestDeriveNextTaskTokenBand:
    """The band is DERIVED at the safe point (F104 D3) from the task's own text.

    DECISION F104 D6: the estimate deliberately does NOT build the task prompt,
    so it is a FLOOR. These tests pin the floor's inputs — the task text and the
    prior proof summaries' token counts — and the never-raises contract, which
    matters because this runs inside a stop check.
    """

    def _task(self, **kw):
        from packages.orchestration.pingpong_job import TaskEntry
        return TaskEntry(**kw)

    def _summary(self, tokens):
        from packages.orchestration.pingpong_job import TaskProofSummary
        return TaskProofSummary(tokens_estimated=tokens)

    def test_a_small_task_is_low(self):
        task = self._task(title="Add a flag", body="Add --max-cost-usd.",
                          acceptance="A test covers it.")
        assert derive_next_task_token_band(task) == TokenBand.LOW

    def test_text_across_the_32k_boundary_is_high(self):
        # >32_000 estimated tokens at 4 chars/token is >128_000 chars of text.
        task = self._task(title="Big", body="x" * 200_000, acceptance="")
        assert derive_next_task_token_band(task) == TokenBand.HIGH

    def test_all_three_text_fields_are_counted(self):
        # MEDIUM starts above 8_000 tokens; no single field crosses it alone.
        chunk = "y" * 16_000          # 4_000 tokens each
        assert derive_next_task_token_band(self._task(body=chunk)) == TokenBand.LOW
        task = self._task(title=chunk, body=chunk, acceptance=chunk)
        assert derive_next_task_token_band(task) == TokenBand.MEDIUM

    def test_a_none_task_is_unknown(self):
        assert derive_next_task_token_band(None) == TokenBand.UNKNOWN
        assert derive_next_task_token_band(None, [self._summary(50_000)]) == TokenBand.UNKNOWN

    def test_missing_attributes_contribute_zero_and_never_raise(self):
        class _Bare:
            pass
        # A task object with none of the three text fields degrades to an empty
        # context rather than raising inside a stop check.
        assert derive_next_task_token_band(_Bare()) in {
            TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH, TokenBand.UNKNOWN}
        assert derive_next_task_token_band(_Bare()) == TokenBand.LOW

    def test_a_task_whose_attribute_raises_degrades_to_unknown(self):
        class _Hostile:
            title = "t"
            @property
            def body(self):
                raise RuntimeError("boom")
        # Never raises: a broken task must not take a healthy job down from
        # inside the stop check. UNKNOWN then takes the conservative A9 path.
        assert derive_next_task_token_band(_Hostile()) == TokenBand.UNKNOWN

    def test_prior_summaries_are_counted_into_the_total(self):
        # The PAIR differs only in the summaries; the task text is identical.
        task = self._task(title="Same", body="Same body.", acceptance="Same.")
        assert derive_next_task_token_band(task, ()) == TokenBand.LOW
        assert derive_next_task_token_band(
            task, [self._summary(20_000)]) == TokenBand.MEDIUM
        assert derive_next_task_token_band(
            task, [self._summary(20_000), self._summary(20_000)]) == TokenBand.HIGH

    def test_unusable_summary_token_counts_contribute_zero(self):
        task = self._task(title="Same", body="Same body.", acceptance="Same.")
        class _NoTokens:
            pass
        for bad in (_NoTokens(), self._summary(-5), self._summary("40000")):
            assert derive_next_task_token_band(task, [bad]) == TokenBand.LOW

    def test_a_non_iterable_summaries_argument_never_raises(self):
        task = self._task(title="Same", body="Same body.", acceptance="Same.")
        assert derive_next_task_token_band(task, 17) == TokenBand.UNKNOWN


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


# ---------------------------------------------------------------------------
# The LIVE wiring (F104 R4). These drive the real ``run_job``.
# ---------------------------------------------------------------------------

_TWO_TASK_JOB = """\
# Job: Predictive Budget

## Task 1
Add a helper module.

Acceptance:
- module exists

## Task 2
Add a second module.

Acceptance:
- module exists
"""

_LEDGER_PROJECT_ID = "11111111-2222-3333-4444-555555555555"


@pytest.fixture
def isolate_data_root(tmp_path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# demo\n")
    return repo


def _configure_price_basis(repo, *, price_basis):
    """Write the operator's predictive config where the job's repo_path finds it."""
    (repo / "remedy.toml").write_text(
        "[remedy.budget]\n"
        f"price_basis_usd_per_1k_tokens = {price_basis}\n"
    )


def _record_cost(job_id, *, call_id, cost):
    """Put a REAL priced row in the F103 ledger under the isolated data root."""
    from packages.orchestration.token_ledger import (
        COST_BASIS_PROVIDER_REPORTED,
        CallRecord,
        record_call,
    )
    ok = record_call(
        CallRecord(
            call_id=call_id,
            job_id=job_id,
            ts_utc="2026-08-09T10:00:00+00:00",
            cost_usd=cost,
            cost_basis=COST_BASIS_PROVIDER_REPORTED,
        ),
        project_id=_LEDGER_PROJECT_ID,
    )
    assert ok is True


def _arm_the_ledger(monkeypatch):
    """Point the live safe point's ledger read at the seeded project.

    The production resolver needs a git repo registered in the project
    registry; the SAME resolver is stubbed by
    ``TestLiveSafePointReadsTheLedgerCost`` in ``test_budget_guard.py``, for the
    same reason. Everything downstream of it here is production code.
    """
    from packages.orchestration import job_evidence as je
    monkeypatch.setattr(
        je, "_resolve_job_ledger_project_id", lambda job: _LEDGER_PROJECT_ID)


class _CountingProvider:
    """Wraps FakeProvider and counts calls, so "zero tasks ran" is provable."""

    def __init__(self, **kwargs):
        from packages.orchestration.pingpong_provider import FakeProvider
        self._inner = FakeProvider(pass_on_round=1, fail_on_round=99, **kwargs)
        self.build_calls = 0
        self.review_calls = 0

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def build(self, prompt, **kwargs):
        self.build_calls += 1
        return self._inner.build(prompt, **kwargs)

    def review(self, prompt, **kwargs):
        self.review_calls += 1
        return self._inner.review(prompt, **kwargs)


class TestPredictiveStopAtTheLiveDispatchSafePoint:
    """F104 acceptance, driven through the REAL ``run_job``.

    A unit gate on ``predict_next_task_cost`` cannot tell a wired engine from an
    unwired one — that was R-0222 — so the acceptance criteria (zero tasks run,
    the stop reason, the arithmetic persisted) are pinned against a real run
    with a real safe point, a real ``_stop_job`` and real F103 ledger rows.

    The terminal JOB_STOPPED state is asserted separately, for BOTH cost stops.
    That assertion is R-0226's repair: until R5 this file stopped at the stop
    SIGNAL, which cannot tell a finalized stop from one that raises three frames
    later — and R-0225 was exactly such a raise (the F012 manifest write rejected
    `max_cost_usd`, leaving the job RUNNING with the stop request pending).
    """

    def _run(self, monkeypatch, repo, *, budgets, seeded_cost=None,
             arm_ledger=True):
        from packages.orchestration.pingpong_job import parse_job_file, run_job
        if arm_ledger:
            _arm_the_ledger(monkeypatch)
        job = parse_job_file(_TWO_TASK_JOB, str(repo))
        if seeded_cost is not None:
            _record_cost(job.job_id, call_id=f"{job.job_id}-seed", cost=seeded_cost)
        builder = _CountingProvider()
        reviewer = _CountingProvider()
        done = run_job(
            job.job_id,
            builder_provider=builder,
            reviewer_provider=reviewer,
            repair_rounds=0,
            budgets=budgets,
        )
        return done, builder, reviewer

    # -- ACCEPTANCE: just-under -------------------------------------------
    def test_just_under_the_limit_stops_before_any_task_is_dispatched(
            self, isolate_data_root, demo_repo, monkeypatch):
        # $0.01/1k tokens x the 8000-token LOW class default = $0.08 expected.
        # Spend is $0.95 against a $1.00 limit: under the REACTIVE boundary, so
        # only a PREDICTION can stop this job — 0.95 + 0.08 > 1.00.
        from packages.orchestration.pingpong_job import TASK_PENDING
        _configure_price_basis(demo_repo, price_basis=0.01)
        done, builder, reviewer = self._run(
            monkeypatch, demo_repo,
            budgets={"max_cost_usd": 1.00},
            seeded_cost=0.95,
        )

        assert done.stop_reason == "predicted_budget_exhausted:max_cost_usd"
        assert done.stop_source == "budget"

        # Nothing was executed: that is the whole point of stopping BEFORE.
        assert all(t.status == TASK_PENDING for t in done.tasks)
        assert builder.build_calls == 0
        assert reviewer.review_calls == 0

        # The arithmetic a human reads to see WHY.
        pred = done.budget_prediction
        assert isinstance(pred, dict)
        assert pred["estimate_basis"] == "class_default"
        arithmetic = pred["arithmetic"]
        assert isinstance(arithmetic, str) and arithmetic
        assert "0.95" in arithmetic          # spent
        assert "0.08" in arithmetic          # expected
        assert "1.00" in arithmetic          # limit
        assert pred["expected_tokens"] == 8000
        assert pred["band"] == TokenBand.LOW

    def test_the_persisted_prediction_survives_a_reload(
            self, isolate_data_root, demo_repo, monkeypatch):
        from packages.orchestration.pingpong_job import load_job_plan
        _configure_price_basis(demo_repo, price_basis=0.01)
        done, _b, _r = self._run(
            monkeypatch, demo_repo,
            budgets={"max_cost_usd": 1.00},
            seeded_cost=0.95,
        )
        reloaded = load_job_plan(done.job_id)
        assert reloaded is not None
        assert reloaded.budget_prediction == done.budget_prediction

    # -- ACCEPTANCE: prediction-wrong -------------------------------------
    def test_a_wrong_prediction_is_still_caught_by_the_reactive_backstop(
            self, isolate_data_root, demo_repo, monkeypatch):
        # At dispatch: 0.10 spent + 0.08 expected = 0.18, far under the $5.00
        # limit, so the prediction correctly does NOT stop. The task then really
        # costs $50 — the prediction was WRONG — and the REACTIVE check catches
        # it at the next safe point.
        from packages.orchestration.pingpong_job import (
            TASK_PENDING,
            parse_job_file,
            run_job,
        )
        _configure_price_basis(demo_repo, price_basis=0.01)
        _arm_the_ledger(monkeypatch)
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        _record_cost(job.job_id, call_id=f"{job.job_id}-seed", cost=0.10)

        class _ExpensiveProvider(_CountingProvider):
            """Bills $50 to the ledger the first time it is asked to build."""

            def build(self, prompt, **kwargs):
                if self.build_calls == 0:
                    _record_cost(job.job_id, call_id=f"{job.job_id}-overrun",
                                 cost=50.0)
                return super().build(prompt, **kwargs)

        builder = _ExpensiveProvider()
        reviewer = _CountingProvider()
        done = run_job(job.job_id, builder_provider=builder,
                       reviewer_provider=reviewer, repair_rounds=0,
                       budgets={"max_cost_usd": 5.00})

        assert done.stop_source == "budget"
        # The REACTIVE reason, not the predicted one: the backstop still catches
        # what the prediction missed.
        assert done.stop_reason.startswith("budget_exhausted:")
        assert not done.stop_reason.startswith("predicted_")
        # No prediction ever breached, so nothing was recorded.
        assert done.budget_prediction is None
        # Real work happened — the prediction let this task through — and the
        # overrun was caught MID-TASK, the incomplete task rolled back to
        # pending by the ordinary stop path and no further task dispatched.
        assert builder.build_calls >= 1
        assert all(t.status == TASK_PENDING for t in done.tasks)

    # -- the terminal state: the stop must FINALIZE, not just be signalled --
    def test_a_predictive_stop_reaches_the_stopped_state(
            self, isolate_data_root, demo_repo, monkeypatch):
        from packages.orchestration.pingpong_job import JOB_STOPPED
        _configure_price_basis(demo_repo, price_basis=0.01)
        done, _b, _r = self._run(
            monkeypatch, demo_repo,
            budgets={"max_cost_usd": 1.00},
            seeded_cost=0.95,
        )
        assert done.status == JOB_STOPPED
        assert done.stop_reason == "predicted_budget_exhausted:max_cost_usd"
        # R-0225: the F012 manifest write and the stop recording both have to
        # SUCCEED for the checkpoint to be reached. An empty error on each is
        # what distinguishes a finalized stop from a job left running.
        assert done.run_manifest_error == ""
        assert done.stop_error == ""

    def test_a_reactive_cost_stop_reaches_the_stopped_state(
            self, isolate_data_root, demo_repo, monkeypatch):
        # R-0226: the REACTIVE cost stop that R2 built had no terminal-state pin
        # at all, which is how R-0225 survived two reviewed rounds. No price
        # basis is configured, so the predictive path is inert (DECISION F104 D4)
        # and only the backstop can stop this job: $5.00 already spent against a
        # $1.00 limit, before a single task is dispatched.
        from packages.orchestration.pingpong_job import JOB_STOPPED
        assert not (demo_repo / "remedy.toml").exists()
        done, builder, _r = self._run(
            monkeypatch, demo_repo,
            budgets={"max_cost_usd": 1.00},
            seeded_cost=5.00,
        )
        assert done.status == JOB_STOPPED
        assert done.stop_reason == "budget_exhausted:max_cost_usd"
        assert done.run_manifest_error == ""
        assert done.stop_error == ""
        # The predictive path really was inert — this is the backstop's stop.
        assert done.budget_prediction is None
        assert builder.build_calls == 0

    # -- REGRESSION: the inert paths --------------------------------------
    def test_without_a_cost_limit_nothing_is_predicted(
            self, isolate_data_root, demo_repo, monkeypatch):
        # A price basis IS configured; the missing money limit alone must keep
        # the whole predictive path inert.
        from packages.orchestration.pingpong_job import JOB_COMPLETED
        _configure_price_basis(demo_repo, price_basis=0.01)
        done, builder, _r = self._run(
            monkeypatch, demo_repo,
            budgets={"max_total_tokens": 1_000_000},
        )
        assert done.status == JOB_COMPLETED
        assert done.budget_prediction is None
        assert builder.build_calls >= 1

    def test_with_no_price_basis_configured_nothing_is_predicted(
            self, isolate_data_root, demo_repo, monkeypatch):
        # DECISION F104 D4: no price is ever invented, so a money limit with no
        # configured price basis leaves the path inert — and a job that would
        # have breached an invented price runs to completion instead.
        from packages.orchestration.pingpong_job import JOB_COMPLETED
        assert not (demo_repo / "remedy.toml").exists()
        done, builder, _r = self._run(
            monkeypatch, demo_repo,
            budgets={"max_cost_usd": 1.00},
            seeded_cost=0.95,
        )
        assert done.status == JOB_COMPLETED
        assert done.budget_prediction is None
        assert builder.build_calls >= 1


class TestTheA9PathAtTheDeriveThenPredictSeam:
    """A task whose band cannot be derived predicts against the LARGEST default.

    Pinned at the ``derive_next_task_token_band`` -> ``predict_next_task_cost``
    SEAM rather than through ``run_job``: a real ``TaskEntry`` always yields a
    derivable band (missing text estimates to 0 tokens, which is honestly LOW),
    so no run-level fixture can reach ``TokenBand.UNKNOWN`` without faking the
    task — and a fabricated run would prove nothing. Declared in the R4
    handback.
    """

    class _UnderivableTask:
        title = "legacy task"

        @property
        def body(self):
            raise RuntimeError("this task's text cannot be read")

    def test_the_seam_takes_the_largest_class_default_and_says_the_band_was_missing(self):
        band = derive_next_task_token_band(self._UnderivableTask())
        assert band == TokenBand.UNKNOWN

        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=10.0), _counters(spent=1.0),
            band=band, config=_config(0.01))
        assert p.estimate_basis == "class_default_missing_band"
        assert p.expected_tokens == LARGEST_CLASS_DEFAULT
        # Over-stopping beats overspending: 120k tokens, not the 8k LOW default.
        assert p.expected_cost_usd == pytest.approx(1.20)
        assert "basis=class_default_missing_band" in p.arithmetic

    def test_a_none_task_takes_the_same_path(self):
        band = derive_next_task_token_band(None)
        p = predict_next_task_cost(
            JobBudgets(max_cost_usd=10.0), _counters(spent=1.0),
            band=band, config=_config(0.01))
        assert p.estimate_basis == "class_default_missing_band"
        assert p.expected_tokens == LARGEST_CLASS_DEFAULT


def _summary_ids(summaries):
    """Compare summary LISTS by identity-free content: their task ids, in order."""
    return [getattr(s, "task_id", None) for s in summaries]


class TestSelectNextPredictableTaskAgreesWithTheLiveSafePoint:
    """``select_next_predictable_task`` must pick what ``run_job`` really picks.

    The helper exists so ``remedy job budget`` can predict WITHOUT running the
    job. Its only real specification is the dispatch loop in ``run_job``, so the
    pin below does not restate the rule — it drives the real runner, captures the
    ``(next_task, previous_summaries)`` the LIVE ``_stop_check`` hands to
    ``derive_next_task_token_band``, and asserts the helper reproduces exactly
    that from the persisted job state at the same moment.

    The seam is monkeypatched the way ``TestTheA9PathAtTheDeriveThenPredictSeam``
    reasons about it — at the ``derive`` boundary — and the original function is
    still called, so the run's behaviour is unchanged by the observation.
    """

    def test_the_helper_reproduces_every_live_dispatch_selection(
            self, isolate_data_root, demo_repo, monkeypatch):
        from packages.orchestration import budget_guard as _bg
        from packages.orchestration.pingpong_job import (
            JOB_COMPLETED,
            load_job_plan,
            parse_job_file,
            run_job,
            select_next_predictable_task,
        )

        # No price basis is configured, so the prediction is inert (D4) and the
        # job runs BOTH tasks — one capture per dispatch safe point.
        assert not (demo_repo / "remedy.toml").exists()
        _arm_the_ledger(monkeypatch)
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        job_id = job.job_id

        observed: list[tuple] = []
        _real_derive = _bg.derive_next_task_token_band

        def _spy(task, previous_summaries=()):
            # What the runner passed, and what the helper says about the job as
            # it stands at this very safe point.
            helper_task, helper_summaries = select_next_predictable_task(
                load_job_plan(job_id))
            observed.append((
                getattr(task, "task_id", None),
                _summary_ids(previous_summaries),
                getattr(helper_task, "task_id", None),
                _summary_ids(helper_summaries),
            ))
            return _real_derive(task, previous_summaries)

        monkeypatch.setattr(_bg, "derive_next_task_token_band", _spy)

        done = run_job(
            job_id,
            builder_provider=_CountingProvider(),
            reviewer_provider=_CountingProvider(),
            repair_rounds=0,
            budgets={"max_cost_usd": 1000.0},
        )
        assert done.status == JOB_COMPLETED

        # Two dispatches really happened, and the summaries really grew.
        assert len(observed) == 2, observed
        assert observed[0][0] == "T001"
        assert observed[0][1] == []
        assert observed[1][0] == "T002"
        assert observed[1][1] == ["T001"]

        # ...and the helper agreed at BOTH of them.
        for live_task, live_summaries, helper_task, helper_summaries in observed:
            assert helper_task == live_task
            assert helper_summaries == live_summaries

    def test_a_blocked_first_pending_task_has_no_next_task(self, demo_repo):
        from packages.orchestration.pingpong_job import (
            TASK_BLOCKED,
            parse_job_file,
            select_next_predictable_task,
        )
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        job.tasks[0].status = TASK_BLOCKED
        # The runner BREAKS on a blocked task rather than dispatching it, so
        # there is nothing to predict against — and no summaries exist yet.
        assert select_next_predictable_task(job) == (None, [])

    def test_a_failed_first_pending_task_has_no_next_task(self, demo_repo):
        from packages.orchestration.pingpong_job import (
            TASK_FAILED,
            parse_job_file,
            select_next_predictable_task,
        )
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        job.tasks[0].status = TASK_FAILED
        assert select_next_predictable_task(job) == (None, [])

    def test_an_all_passed_job_has_no_next_task_but_keeps_every_summary(
            self, demo_repo):
        from packages.orchestration.pingpong_job import (
            TASK_PASSED,
            TaskProofSummary,
            parse_job_file,
            select_next_predictable_task,
        )
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        for t in job.tasks:
            t.status = TASK_PASSED
            t.proof_summary = TaskProofSummary(task_id=t.task_id, tokens_estimated=10)
        next_task, summaries = select_next_predictable_task(job)
        assert next_task is None
        assert _summary_ids(summaries) == ["T001", "T002"]

    def test_a_skipped_task_is_stepped_over_and_contributes_no_summary(
            self, demo_repo):
        from packages.orchestration.pingpong_job import (
            TASK_SKIPPED,
            parse_job_file,
            select_next_predictable_task,
        )
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        job.tasks[0].status = TASK_SKIPPED
        next_task, summaries = select_next_predictable_task(job)
        assert next_task is job.tasks[1]
        assert summaries == []

    def test_a_later_completed_task_still_contributes_its_summary(self, demo_repo):
        # The runner pre-fills previous_summaries from EVERY applied/passed task,
        # not only the ones before the pending one; the helper must match that.
        from packages.orchestration.pingpong_job import (
            TASK_APPLIED,
            TaskProofSummary,
            parse_job_file,
            select_next_predictable_task,
        )
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        job.tasks[1].status = TASK_APPLIED
        job.tasks[1].proof_summary = TaskProofSummary(task_id="T002", tokens_estimated=7)
        next_task, summaries = select_next_predictable_task(job)
        assert next_task is job.tasks[0]
        assert _summary_ids(summaries) == ["T002"]

    def test_a_completed_task_without_a_proof_summary_contributes_nothing(
            self, demo_repo):
        from packages.orchestration.pingpong_job import (
            TASK_APPLIED,
            parse_job_file,
            select_next_predictable_task,
        )
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        job.tasks[0].status = TASK_APPLIED
        job.tasks[0].proof_summary = None
        next_task, summaries = select_next_predictable_task(job)
        assert next_task is job.tasks[1]
        assert summaries == []

    def test_it_never_raises_on_junk(self):
        from packages.orchestration.pingpong_job import select_next_predictable_task

        class _Hostile:
            @property
            def tasks(self):
                raise RuntimeError("this job file cannot be read")

        # A read-only inspection command must degrade, never die.
        assert select_next_predictable_task(None) == (None, [])
        assert select_next_predictable_task(object()) == (None, [])
        assert select_next_predictable_task(_Hostile()) == (None, [])
