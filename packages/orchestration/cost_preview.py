"""F114 T001 — the shared cost-band estimator.

Computes an upfront USD cost BAND (never a point) from the class-default
token counts and price basis ``resolve_predictive_budget_config``
resolves (budget_resolution.py) — one estimator, shared with
``predict_next_task_cost`` (budget_guard.py) via
``token_economy.tokens_to_cost_usd``. Pure: no reads/writes/clock/prompt
(scanned by tests/test_no_interactive_guard.py). CLI confirmation is
built in a later round, entirely inside apps/cli.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.token_economy import TokenBand, tokens_to_cost_usd

#: The estimate could not be computed - an unrecognised class, an unpriced
#: config, or an invalid repeat count. Never a fabricated number (P6).
ESTIMATE_UNAVAILABLE = "estimate_unavailable"

_VALID_BANDS = (TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH)


@dataclass(frozen=True)
class CostBandEstimate:
    """A USD cost estimate - always a band, never a point.

    ``band_usd_low``/``band_usd_high`` are None together, never separately:
    an unrecognised class or an unset price basis makes the WHOLE estimate
    unavailable rather than half of it fabricated. ``band_usd_low ==
    band_usd_high`` is a real duplicate (caller named one class twice),
    not evidence of missing math.
    """

    band_usd_low: float | None
    band_usd_high: float | None
    basis: str
    inputs: dict[str, Any] = field(default_factory=dict)


def estimate_cost_band(
    band_a: str,
    band_b: str,
    *,
    repeat_count: int = 1,
    config: PredictiveBudgetConfig,
) -> CostBandEstimate:
    """Estimate a USD cost band spanning ``band_a`` and ``band_b``.

    Both are ``TokenBand`` values (LOW/MEDIUM/HIGH); pass the same value
    twice for a single confidently-known class (an honest degenerate
    band, not a fabricated spread). ``repeat_count`` scales a single
    unit's cost. Argument order does not matter - the lower resulting
    USD figure is always ``band_usd_low``.

    Returns UNAVAILABLE (both bounds None) rather than a guess when:
    either band is unrecognised or has no configured class default,
    ``repeat_count`` is negative, or ``config`` has no price basis
    (A9: unknown is treated as expensive, never guessed here).
    """
    inputs: dict[str, Any] = {
        "band_a": band_a,
        "band_b": band_b,
        "repeat_count": repeat_count,
    }
    class_defaults = config.class_default_tokens
    if (
        band_a not in _VALID_BANDS
        or band_b not in _VALID_BANDS
        or band_a not in class_defaults
        or band_b not in class_defaults
        or repeat_count < 0
    ):
        return CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, inputs)

    price_basis = config.price_basis_usd_per_1k_tokens
    usd_a = tokens_to_cost_usd(class_defaults[band_a] * repeat_count, price_basis)
    usd_b = tokens_to_cost_usd(class_defaults[band_b] * repeat_count, price_basis)
    if usd_a is None or usd_b is None:
        return CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, inputs)

    basis = (
        f"class defaults ({band_a}/{band_b} token bands) x "
        f"price_basis_usd_per_1k_tokens={price_basis}"
    )
    return CostBandEstimate(min(usd_a, usd_b), max(usd_a, usd_b), basis, inputs)


#: Default confirm-above threshold (F114 Design: "around half a dollar").
#: Config source of truth is cost_preview.confirm_above_usd; this is only
#: the fallback when nothing is configured (same non-invention posture as
#: token_economy - a real number, not a magic default hidden in the CLI).
DEFAULT_CONFIRM_ABOVE_USD = 0.5


def resolve_confirm_above_usd(
    *,
    config_path: str | None = None,
    project_root: str | None = None,
) -> float:
    """Resolve the F114 confirm-above-USD threshold: env > TOML > default.

    Same config authority as ``resolve_predictive_budget_config``. A
    malformed or non-positive configured value falls back to
    ``DEFAULT_CONFIRM_ABOVE_USD`` rather than raising - this threshold is
    a UX policy, not a budget limit, so a bad config value degrades to
    the safe default instead of blocking every command.
    """
    from packages.orchestration.config import ConfigSource, load_config

    if config_path:
        cfg = load_config(project_path=Path(config_path))
    elif project_root:
        cfg = load_config(project_path=Path(project_root) / "remedy.toml")
    else:
        cfg = load_config()

    cv = cfg.get_value("cost_preview.confirm_above_usd")
    if cv is not None and cv.source != ConfigSource.DEFAULT and cv.value is not None:
        try:
            value = float(cv.value)
        except (TypeError, ValueError):
            return DEFAULT_CONFIRM_ABOVE_USD
        if value > 0:
            return value
    return DEFAULT_CONFIRM_ABOVE_USD
