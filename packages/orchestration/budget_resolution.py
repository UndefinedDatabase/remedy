"""F018 T001 — budget resolution: CLI flags > env vars > project config > no limit.

Resolves a JobBudgets from the central config system (config.py).
CLI flags override env/TOML; malformed values raise BudgetConfigError.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.core.models import JobBudgets


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
    if not isinstance(raw, int):
        raise BudgetConfigError(f"{name} must be an integer, got {type(raw).__name__}")
    if raw <= 0:
        raise BudgetConfigError(f"{name} must be strictly positive, got {raw}")
    return raw


_CONFIG_KEYS = {
    "max_total_tokens": "budget.max_total_tokens",
    "max_provider_calls": "budget.max_provider_calls",
    "max_wall_clock_minutes": "budget.max_wall_clock_minutes",
    "deadline": "budget.deadline",
}


def resolve_job_budgets(
    *,
    cli_max_total_tokens: str | None = None,
    cli_max_provider_calls: str | None = None,
    cli_max_wall_clock_minutes: str | None = None,
    cli_deadline: str | None = None,
    config_path: str | None = None,
) -> JobBudgets | None:
    """Resolve budget values through CLI > env > TOML > no-limit precedence.

    Uses config.py as the single authority for env/TOML resolution.
    CLI flags, when present, override everything.
    Malformed values raise BudgetConfigError (never silently returns None).
    """
    from packages.orchestration.config import ConfigSource, load_config

    cfg = load_config() if not config_path else load_config(
        project_path=Path(config_path))

    def _resolve_int(name: str, cli_val: str | None) -> int | None:
        if cli_val is not None:
            return _pos_int(name, cli_val)
        cv = cfg.get_value(_CONFIG_KEYS[name])
        if cv is not None and cv.source != ConfigSource.DEFAULT and cv.value is not None:
            return _pos_int(name, cv.value)
        return None

    max_total_tokens = _resolve_int("max_total_tokens", cli_max_total_tokens)
    max_provider_calls = _resolve_int("max_provider_calls", cli_max_provider_calls)
    max_wall_clock_minutes = _resolve_int("max_wall_clock_minutes", cli_max_wall_clock_minutes)

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

    if all(v is None for v in (max_total_tokens, max_provider_calls, max_wall_clock_minutes, deadline)):
        return None

    return JobBudgets(
        max_total_tokens=max_total_tokens,
        max_provider_calls=max_provider_calls,
        max_wall_clock_minutes=max_wall_clock_minutes,
        deadline=deadline,
    )
