"""F018 T001 — budget resolution: CLI flags > env vars > project config > no limit.

Resolves a JobBudgets from the three precedence layers.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
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


_ENV_MAP = {
    "max_total_tokens": "REMEDY_BUDGET_MAX_TOTAL_TOKENS",
    "max_provider_calls": "REMEDY_BUDGET_MAX_PROVIDER_CALLS",
    "max_wall_clock_minutes": "REMEDY_BUDGET_MAX_WALL_CLOCK_MINUTES",
    "deadline": "REMEDY_BUDGET_DEADLINE",
}


def _load_budget_toml(config_path: str) -> dict[str, Any]:
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]
    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
    except Exception:
        return {}
    budget = data.get("remedy", {}).get("budget", {})
    if not isinstance(budget, dict):
        raise BudgetConfigError(
            f"[remedy.budget] must be a table, got {type(budget).__name__}"
        )
    return budget


def resolve_job_budgets(
    *,
    cli_max_total_tokens: str | None = None,
    cli_max_provider_calls: str | None = None,
    cli_max_wall_clock_minutes: str | None = None,
    cli_deadline: str | None = None,
    config_path: str | None = None,
) -> JobBudgets | None:
    budget_cfg = _load_budget_toml(config_path) if config_path else {}

    def _resolve_int(name: str, cli_val: str | None) -> int | None:
        if cli_val is not None:
            return _pos_int(name, cli_val)
        env_val = os.environ.get(_ENV_MAP[name])
        if env_val is not None:
            return _pos_int(name, env_val)
        cfg_val = budget_cfg.get(name)
        if cfg_val is not None:
            return _pos_int(name, cfg_val)
        return None

    max_total_tokens = _resolve_int("max_total_tokens", cli_max_total_tokens)
    max_provider_calls = _resolve_int("max_provider_calls", cli_max_provider_calls)
    max_wall_clock_minutes = _resolve_int("max_wall_clock_minutes", cli_max_wall_clock_minutes)

    deadline: datetime | None = None
    if cli_deadline is not None:
        deadline = _parse_deadline(cli_deadline)
    else:
        env_dl = os.environ.get(_ENV_MAP["deadline"])
        if env_dl is not None and env_dl.strip():
            deadline = _parse_deadline(env_dl)
        elif "deadline" in budget_cfg:
            raw_dl = budget_cfg["deadline"]
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
