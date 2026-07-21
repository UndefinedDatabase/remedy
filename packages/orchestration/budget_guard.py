"""F018 T002 — actual-only budget evaluation.

Pure, deterministic evaluation of job budgets against recorded actuals.
No writes, no stop, no side effects. Injected clock for wall-time/deadline.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from packages.core.models import JobBudgets


class BudgetCounterError(ValueError):
    """Impossible counter data detected."""


@dataclass(frozen=True)
class BudgetCounters:
    """Observed actuals for budget evaluation."""

    provider_calls: int = 0
    measured_token_total: int = 0
    measured_call_count: int = 0
    unmeasured_call_count: int = 0
    elapsed_seconds: float = 0.0
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    actual_sources: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("provider_calls", "measured_token_total", "measured_call_count",
                      "unmeasured_call_count"):
            val = getattr(self, name)
            if isinstance(val, bool):
                raise BudgetCounterError(f"{name} must be int, got bool")
            if not isinstance(val, int) or val < 0:
                raise BudgetCounterError(
                    f"{name} must be a non-negative integer, got {val!r}")
        if isinstance(self.elapsed_seconds, bool):
            raise BudgetCounterError(
                f"elapsed_seconds must be a number, got bool")
        if not isinstance(self.elapsed_seconds, (int, float)) or self.elapsed_seconds < 0:
            raise BudgetCounterError(
                f"elapsed_seconds must be non-negative, got {self.elapsed_seconds!r}")
        if isinstance(self.elapsed_seconds, float) and not math.isfinite(self.elapsed_seconds):
            raise BudgetCounterError(
                f"elapsed_seconds must be finite, got {self.elapsed_seconds!r}")
        if not isinstance(self.evaluated_at, datetime):
            raise BudgetCounterError(
                f"evaluated_at must be a datetime, got {type(self.evaluated_at).__name__}")
        if not isinstance(self.actual_sources, tuple):
            raise BudgetCounterError(
                f"actual_sources must be a tuple, got {type(self.actual_sources).__name__}")
        for i, src in enumerate(self.actual_sources):
            if not isinstance(src, str):
                raise BudgetCounterError(
                    f"actual_sources[{i}] must be str, got {type(src).__name__}")
        if self.started_at is not None:
            if not isinstance(self.started_at, datetime):
                raise BudgetCounterError(
                    f"started_at must be a datetime or None, got {type(self.started_at).__name__}")
            if self.started_at > self.evaluated_at:
                raise BudgetCounterError(
                    f"started_at ({self.started_at.isoformat()}) is after "
                    f"evaluated_at ({self.evaluated_at.isoformat()})")
        expected = self.measured_call_count + self.unmeasured_call_count
        if self.provider_calls != expected:
            raise BudgetCounterError(
                f"provider_calls ({self.provider_calls}) != "
                f"measured_call_count ({self.measured_call_count}) + "
                f"unmeasured_call_count ({self.unmeasured_call_count})")

    @property
    def total_call_count(self) -> int:
        return self.measured_call_count + self.unmeasured_call_count

    @property
    def has_unmeasured(self) -> bool:
        return self.unmeasured_call_count > 0

    def token_description(self) -> str:
        if self.unmeasured_call_count > 0:
            return (
                f">= {self.measured_token_total} tokens "
                f"({self.unmeasured_call_count} provider calls unmeasured)"
            )
        return f"{self.measured_token_total} tokens"

    def to_json(self) -> dict[str, Any]:
        return {
            "provider_calls": self.provider_calls,
            "measured_token_total": self.measured_token_total,
            "measured_call_count": self.measured_call_count,
            "unmeasured_call_count": self.unmeasured_call_count,
            "elapsed_seconds": self.elapsed_seconds,
            "evaluated_at": self.evaluated_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "actual_sources": list(self.actual_sources),
        }


@dataclass(frozen=True)
class BudgetEvaluation:
    """Result of evaluating budgets against actuals."""

    configured_limits: JobBudgets | None
    counters: BudgetCounters
    exhausted: bool
    first_exhausted_limit: str | None = None
    token_lower_bound: bool = False
    warnings: tuple[str, ...] = ()
    source_descriptions: tuple[str, ...] = ()

    def to_json(self) -> dict[str, Any]:
        return {
            "configured_limits": (
                self.configured_limits.model_dump(mode="json")
                if self.configured_limits else None
            ),
            "counters": self.counters.to_json(),
            "exhausted": self.exhausted,
            "first_exhausted_limit": self.first_exhausted_limit,
            "token_lower_bound": self.token_lower_bound,
            "warnings": list(self.warnings),
            "source_descriptions": list(self.source_descriptions),
        }


_LIMIT_ORDER = (
    "max_provider_calls",
    "max_total_tokens",
    "max_wall_clock_minutes",
    "deadline",
)


def evaluate_budget(
    budgets: JobBudgets | None,
    counters: BudgetCounters,
    *,
    now: datetime | None = None,
) -> BudgetEvaluation:
    if budgets is None:
        return BudgetEvaluation(
            configured_limits=None,
            counters=counters,
            exhausted=False,
        )

    if now is None:
        now = datetime.now(timezone.utc)

    elapsed = counters.elapsed_seconds
    if counters.started_at is not None:
        elapsed = max(0.0, (now - counters.started_at).total_seconds())

    exhausted_limits: list[str] = []
    warnings: list[str] = []
    sources: list[str] = []
    token_lower_bound = False

    if budgets.max_provider_calls is not None:
        sources.append(f"provider_calls: {counters.provider_calls}/{budgets.max_provider_calls}")
        if counters.provider_calls >= budgets.max_provider_calls:
            exhausted_limits.append("max_provider_calls")

    if budgets.max_total_tokens is not None:
        sources.append(f"tokens: {counters.token_description()}/{budgets.max_total_tokens}")
        if counters.has_unmeasured:
            token_lower_bound = True
            if counters.measured_token_total >= budgets.max_total_tokens:
                exhausted_limits.append("max_total_tokens")
            else:
                warnings.append(
                    f"token count is a lower bound "
                    f"({counters.unmeasured_call_count} calls unmeasured); "
                    f"cannot definitively determine exhaustion"
                )
        else:
            if counters.measured_token_total >= budgets.max_total_tokens:
                exhausted_limits.append("max_total_tokens")

    if budgets.max_wall_clock_minutes is not None:
        limit_secs = budgets.max_wall_clock_minutes * 60
        sources.append(f"wall_clock: {elapsed:.0f}s/{limit_secs}s")
        if elapsed >= limit_secs:
            exhausted_limits.append("max_wall_clock_minutes")

    if budgets.deadline is not None:
        sources.append(f"deadline: {budgets.deadline.isoformat()}")
        if now >= budgets.deadline:
            exhausted_limits.append("deadline")

    first = None
    for limit_name in _LIMIT_ORDER:
        if limit_name in exhausted_limits:
            first = limit_name
            break

    return BudgetEvaluation(
        configured_limits=budgets,
        counters=counters,
        exhausted=len(exhausted_limits) > 0,
        first_exhausted_limit=first,
        token_lower_bound=token_lower_bound,
        warnings=tuple(warnings),
        source_descriptions=tuple(sources),
    )


def collect_counters_from_actuals(
    actuals: dict[str, Any],
    *,
    started_at: datetime | None = None,
    now: datetime | None = None,
) -> BudgetCounters:
    """Build BudgetCounters from _aggregate_usage_actuals() output.

    This is the public bridge from PingPongResult's aggregated actuals
    to the budget evaluation system. Never re-parses provider output.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    provider_call_count = actuals.get("provider_call_count", 0)
    actual_call_count = actuals.get("actual_call_count", 0)
    unmeasured = max(0, provider_call_count - actual_call_count)
    total_tokens = actuals.get("total_tokens", 0) or 0
    elapsed = 0.0
    if started_at is not None:
        elapsed = max(0.0, (now - started_at).total_seconds())
    return BudgetCounters(
        provider_calls=provider_call_count,
        measured_token_total=total_tokens,
        measured_call_count=actual_call_count,
        unmeasured_call_count=unmeasured,
        elapsed_seconds=elapsed,
        evaluated_at=now,
        started_at=started_at,
        actual_sources=("pingpong_actuals",),
    )
