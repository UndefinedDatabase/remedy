"""F018 T002 — actual-only budget evaluation.

Pure, deterministic evaluation of job budgets against recorded actuals.
No writes, no stop, no side effects. Injected clock for wall-time/deadline.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from packages.core.models import JobBudgets


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
        sources.append(f"wall_clock: {counters.elapsed_seconds:.0f}s/{limit_secs}s")
        if counters.elapsed_seconds >= limit_secs:
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
