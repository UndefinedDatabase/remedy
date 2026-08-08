"""F018 T001 — budget resolution: CLI flags > env vars > project config > no limit.

Resolves a JobBudgets from the central config system (config.py).
CLI flags override env/TOML; malformed values raise BudgetConfigError.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.core.models import JobBudgets
from packages.orchestration.token_economy import TokenBand


class BudgetConfigError(ValueError):
    pass


def _parse_deadline(raw: str) -> datetime:
    raw = raw.strip()
    if not raw:
        raise BudgetConfigError("deadline string is empty")
    try:
        dt = datetime.fromisoformat(raw)
    except (ValueError, TypeError) as exc:
        raise BudgetConfigError(f"invalid deadline: {raw!r}") from exc
    if dt.tzinfo is None:
        raise BudgetConfigError(
            f"deadline has no timezone: {raw!r}; use UTC or explicit offset"
        )
    return dt.astimezone(timezone.utc)


def _pos_int(name: str, raw: Any) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, bool):
        raise BudgetConfigError(f"{name} must be an integer, got bool")
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            return None
        try:
            raw = int(raw)
        except ValueError:
            raise BudgetConfigError(f"{name} is not a valid integer: {raw!r}")
    if isinstance(raw, float):
        if raw != int(raw):
            raise BudgetConfigError(f"{name} must be an integer, got float {raw}")
        raw = int(raw)
    if not isinstance(raw, int):
        raise BudgetConfigError(f"{name} must be an integer, got {type(raw).__name__}")
    if raw <= 0:
        raise BudgetConfigError(f"{name} must be strictly positive, got {raw}")
    return raw


# The money mirror of _pos_int: dollars are fractional, so floats are allowed.
def _pos_float(name: str, raw: Any) -> float | None:
    if raw is None:
        return None
    if isinstance(raw, bool):
        raise BudgetConfigError(f"{name} must be a number, got bool")
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            return None
        try:
            raw = float(raw)
        except ValueError:
            raise BudgetConfigError(f"{name} is not a valid number: {raw!r}")
    if not isinstance(raw, (int, float)):
        raise BudgetConfigError(f"{name} must be a number, got {type(raw).__name__}")
    raw = float(raw)
    if not math.isfinite(raw):
        raise BudgetConfigError(f"{name} must be finite, got {raw}")
    if raw <= 0:
        raise BudgetConfigError(f"{name} must be strictly positive, got {raw}")
    return raw


# F104 predictive inputs, resolved separately from JobBudgets: these are not
# limits, they are the arithmetic a prediction is made of.
_PREDICTIVE_CONFIG_KEYS = {
    "price_basis_usd_per_1k_tokens": "budget.price_basis_usd_per_1k_tokens",
    TokenBand.LOW: "budget.class_default_tokens_low",
    TokenBand.MEDIUM: "budget.class_default_tokens_medium",
    TokenBand.HIGH: "budget.class_default_tokens_high",
}

_CLASS_DEFAULT_TOKENS_FALLBACK = {
    TokenBand.LOW: 8000,
    TokenBand.MEDIUM: 32000,
    TokenBand.HIGH: 120000,
}


@dataclass(frozen=True)
class PredictiveBudgetConfig:
    """The provisional inputs a cost prediction is computed from (F104).

    ``price_basis_usd_per_1k_tokens`` is None unless an operator configured one.
    That None is load-bearing: no price is ever invented (P6, DECISION F104 D4),
    so an unconfigured price basis makes the predictive path inert rather than
    making up a number and labelling the fabrication honestly.

    ``class_default_tokens`` is keyed by ``TokenBand`` values — "low", "medium",
    "high". These are DOCUMENTED CLASS DEFAULTS, not calibration from history;
    calibration is explicitly out of scope for F104.
    """

    price_basis_usd_per_1k_tokens: float | None = None
    class_default_tokens: dict[str, int] = field(
        default_factory=lambda: dict(_CLASS_DEFAULT_TOKENS_FALLBACK))


_CONFIG_KEYS = {
    "max_total_tokens": "budget.max_total_tokens",
    "max_provider_calls": "budget.max_provider_calls",
    "max_wall_clock_minutes": "budget.max_wall_clock_minutes",
    "max_cost_usd": "budget.max_cost_usd",
    "deadline": "budget.deadline",
}


def resolve_job_budgets(
    *,
    cli_max_total_tokens: str | None = None,
    cli_max_provider_calls: str | None = None,
    cli_max_wall_clock_minutes: str | None = None,
    cli_max_cost_usd: str | None = None,
    cli_deadline: str | None = None,
    config_path: str | None = None,
    project_root: str | None = None,
) -> JobBudgets | None:
    """Resolve budget values through CLI > env > TOML > no-limit precedence.

    Uses config.py as the single authority for env/TOML resolution.
    CLI flags, when present, override everything.
    Malformed values raise BudgetConfigError (never silently returns None).

    *project_root*: if given, resolve project config from that directory
    instead of process CWD. A ``config_path`` takes precedence.
    """
    from packages.orchestration.config import ConfigSource, load_config

    if config_path:
        cfg = load_config(project_path=Path(config_path))
    elif project_root:
        cfg = load_config(project_path=Path(project_root) / "remedy.toml")
    else:
        cfg = load_config()

    def _resolve_int(name: str, cli_val: str | None) -> int | None:
        if cli_val is not None:
            return _pos_int(name, cli_val)
        cv = cfg.get_value(_CONFIG_KEYS[name])
        if cv is not None and cv.source != ConfigSource.DEFAULT and cv.value is not None:
            return _pos_int(name, cv.value)
        return None

    # Same CLI > env > TOML > no-limit precedence as _resolve_int, for money.
    def _resolve_float(name: str, cli_val: str | None) -> float | None:
        if cli_val is not None:
            return _pos_float(name, cli_val)
        cv = cfg.get_value(_CONFIG_KEYS[name])
        if cv is not None and cv.source != ConfigSource.DEFAULT and cv.value is not None:
            return _pos_float(name, cv.value)
        return None

    max_total_tokens = _resolve_int("max_total_tokens", cli_max_total_tokens)
    max_provider_calls = _resolve_int("max_provider_calls", cli_max_provider_calls)
    max_wall_clock_minutes = _resolve_int("max_wall_clock_minutes", cli_max_wall_clock_minutes)
    max_cost_usd = _resolve_float("max_cost_usd", cli_max_cost_usd)

    deadline: datetime | None = None
    if cli_deadline is not None:
        deadline = _parse_deadline(cli_deadline)
    else:
        cv = cfg.get_value(_CONFIG_KEYS["deadline"])
        if cv is not None and cv.source != ConfigSource.DEFAULT and cv.value is not None:
            raw_dl = cv.value
            if not isinstance(raw_dl, str):
                raise BudgetConfigError(
                    f"budget.deadline must be a string, got {type(raw_dl).__name__}"
                )
            deadline = _parse_deadline(raw_dl)

    if all(v is None for v in (max_total_tokens, max_provider_calls,
                               max_wall_clock_minutes, max_cost_usd, deadline)):
        return None

    return JobBudgets(
        max_total_tokens=max_total_tokens,
        max_provider_calls=max_provider_calls,
        max_wall_clock_minutes=max_wall_clock_minutes,
        max_cost_usd=max_cost_usd,
        deadline=deadline,
    )


def resolve_predictive_budget_config(
    *,
    config_path: str | None = None,
    project_root: str | None = None,
) -> PredictiveBudgetConfig:
    """Resolve the F104 predictive inputs through env > TOML > documented default.

    Same config authority and the same ``ConfigSource.DEFAULT`` handling as
    ``resolve_job_budgets``; there is no CLI layer here because these are
    operator settings, not per-invocation limits.

    The price basis stays None when nothing is configured — no substitute number
    is supplied (DECISION F104 D4). The class defaults DO have documented
    defaults, because a token count for a band is a stated assumption rather
    than a measurement claim, and they are provisional until calibration.
    """
    from packages.orchestration.config import ConfigSource, load_config

    if config_path:
        cfg = load_config(project_path=Path(config_path))
    elif project_root:
        cfg = load_config(project_path=Path(project_root) / "remedy.toml")
    else:
        cfg = load_config()

    def _configured(key: str) -> Any:
        cv = cfg.get_value(key)
        if cv is not None and cv.source != ConfigSource.DEFAULT and cv.value is not None:
            return cv.value
        return None

    price_basis = _pos_float(
        "price_basis_usd_per_1k_tokens",
        _configured(_PREDICTIVE_CONFIG_KEYS["price_basis_usd_per_1k_tokens"]),
    )

    class_defaults: dict[str, int] = {}
    for band, fallback in _CLASS_DEFAULT_TOKENS_FALLBACK.items():
        name = _PREDICTIVE_CONFIG_KEYS[band]
        resolved = _pos_int(name, _configured(name))
        class_defaults[band] = fallback if resolved is None else resolved

    return PredictiveBudgetConfig(
        price_basis_usd_per_1k_tokens=price_basis,
        class_default_tokens=class_defaults,
    )
