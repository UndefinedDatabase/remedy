"""F114 T001 — tests for the shared cost-band estimator.

Covers ``estimate_cost_band`` / ``CostBandEstimate`` in
``packages.orchestration.cost_preview`` — one estimator, shared with
``budget_guard.predict_next_task_cost`` via
``token_economy.tokens_to_cost_usd``, per T3_F114.md.
"""
from __future__ import annotations

import pytest

from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.cost_preview import ESTIMATE_UNAVAILABLE, estimate_cost_band
from packages.orchestration.token_economy import TokenBand

CLASS_DEFAULTS = {TokenBand.LOW: 8000, TokenBand.MEDIUM: 32000, TokenBand.HIGH: 120000}


def _config(price_basis, defaults=None):
    return PredictiveBudgetConfig(
        price_basis_usd_per_1k_tokens=price_basis,
        class_default_tokens=dict(CLASS_DEFAULTS if defaults is None else defaults),
    )


class TestSingleConfidentBand:
    def test_same_band_twice_gives_a_degenerate_band(self):
        # 8000 tokens x $0.02/1k = $0.16, both bounds identical.
        e = estimate_cost_band(TokenBand.LOW, TokenBand.LOW, config=_config(0.02))
        assert e.band_usd_low == 0.16
        assert e.band_usd_high == 0.16
        assert e.basis != ESTIMATE_UNAVAILABLE

    def test_repeat_count_scales_both_bounds(self):
        e = estimate_cost_band(TokenBand.LOW, TokenBand.LOW, repeat_count=3, config=_config(0.02))
        assert e.band_usd_low == pytest.approx(0.48)
        assert e.band_usd_high == pytest.approx(0.48)

    def test_zero_repeat_count_is_a_measured_zero(self):
        e = estimate_cost_band(TokenBand.HIGH, TokenBand.HIGH, repeat_count=0, config=_config(0.02))
        assert e.band_usd_low == 0.0
        assert e.band_usd_high == 0.0


class TestSpanningBand:
    def test_low_and_high_span_produces_a_real_range(self):
        # LOW=8000 tok -> $0.16 ; HIGH=120000 tok -> $2.40, at $0.02/1k.
        e = estimate_cost_band(TokenBand.LOW, TokenBand.HIGH, config=_config(0.02))
        assert e.band_usd_low == pytest.approx(0.16)
        assert e.band_usd_high == pytest.approx(2.40)

    def test_argument_order_does_not_matter(self):
        a = estimate_cost_band(TokenBand.LOW, TokenBand.HIGH, config=_config(0.02))
        b = estimate_cost_band(TokenBand.HIGH, TokenBand.LOW, config=_config(0.02))
        assert (a.band_usd_low, a.band_usd_high) == (b.band_usd_low, b.band_usd_high)


class TestBasisLabel:
    def test_basis_names_both_bands_and_the_price(self):
        e = estimate_cost_band(TokenBand.LOW, TokenBand.MEDIUM, config=_config(0.02))
        assert TokenBand.LOW in e.basis
        assert TokenBand.MEDIUM in e.basis
        assert "0.02" in e.basis

    def test_every_available_estimate_carries_a_non_unavailable_basis(self):
        for band_a in (TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH):
            for band_b in (TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH):
                e = estimate_cost_band(band_a, band_b, config=_config(0.02))
                assert e.basis != ESTIMATE_UNAVAILABLE
                assert e.band_usd_low is not None
                assert e.band_usd_high is not None


class TestUnavailable:
    def test_unknown_band_is_unavailable_not_guessed(self):
        e = estimate_cost_band(TokenBand.UNKNOWN, TokenBand.LOW, config=_config(0.02))
        assert e.band_usd_low is None
        assert e.band_usd_high is None
        assert e.basis == ESTIMATE_UNAVAILABLE

    def test_nonsense_band_is_unavailable(self):
        e = estimate_cost_band("nonsense", TokenBand.LOW, config=_config(0.02))
        assert e.basis == ESTIMATE_UNAVAILABLE

    def test_missing_price_basis_is_unavailable(self):
        e = estimate_cost_band(TokenBand.LOW, TokenBand.LOW, config=_config(None))
        assert e.band_usd_low is None
        assert e.band_usd_high is None
        assert e.basis == ESTIMATE_UNAVAILABLE

    def test_negative_repeat_count_is_unavailable(self):
        e = estimate_cost_band(TokenBand.LOW, TokenBand.LOW, repeat_count=-1, config=_config(0.02))
        assert e.basis == ESTIMATE_UNAVAILABLE

    def test_class_missing_from_config_is_unavailable(self):
        partial = {TokenBand.LOW: 8000}
        e = estimate_cost_band(TokenBand.LOW, TokenBand.HIGH, config=_config(0.02, defaults=partial))
        assert e.basis == ESTIMATE_UNAVAILABLE


class TestInputsRecordWhatWasAsked:
    def test_inputs_carry_the_raw_request(self):
        e = estimate_cost_band(TokenBand.MEDIUM, TokenBand.HIGH, repeat_count=2, config=_config(0.02))
        assert e.inputs == {"band_a": TokenBand.MEDIUM, "band_b": TokenBand.HIGH, "repeat_count": 2}


# ---------------------------------------------------------------------------
# resolve_confirm_above_usd (F114 T002 — the CLI confirm threshold)
# ---------------------------------------------------------------------------


class TestResolveConfirmAboveUsd:
    def test_documented_default_when_nothing_is_configured(self):
        from packages.orchestration.cost_preview import (
            DEFAULT_CONFIRM_ABOVE_USD,
            resolve_confirm_above_usd,
        )
        assert resolve_confirm_above_usd() == DEFAULT_CONFIRM_ABOVE_USD == 0.5

    def test_toml_sets_the_threshold(self, tmp_path):
        from packages.orchestration.cost_preview import resolve_confirm_above_usd
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.cost_preview]\nconfirm_above_usd = 2.5\n")
        assert resolve_confirm_above_usd(config_path=str(toml)) == 2.5

    def test_env_sets_the_threshold(self, monkeypatch):
        from packages.orchestration.cost_preview import resolve_confirm_above_usd
        monkeypatch.setenv("REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD", "1.25")
        assert resolve_confirm_above_usd() == 1.25

    def test_negative_configured_value_falls_back_to_default(self, tmp_path):
        from packages.orchestration.cost_preview import (
            DEFAULT_CONFIRM_ABOVE_USD,
            resolve_confirm_above_usd,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.cost_preview]\nconfirm_above_usd = -1.0\n")
        assert resolve_confirm_above_usd(config_path=str(toml)) == DEFAULT_CONFIRM_ABOVE_USD

    def test_zero_configured_value_falls_back_to_default(self, tmp_path):
        from packages.orchestration.cost_preview import (
            DEFAULT_CONFIRM_ABOVE_USD,
            resolve_confirm_above_usd,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.cost_preview]\nconfirm_above_usd = 0\n")
        assert resolve_confirm_above_usd(config_path=str(toml)) == DEFAULT_CONFIRM_ABOVE_USD

    def test_project_root_form_reads_the_same_file(self, tmp_path):
        from packages.orchestration.cost_preview import resolve_confirm_above_usd
        (tmp_path / "remedy.toml").write_text(
            "[remedy.cost_preview]\nconfirm_above_usd = 3.0\n")
        assert resolve_confirm_above_usd(project_root=str(tmp_path)) == 3.0
