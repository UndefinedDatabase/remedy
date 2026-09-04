"""F018 T002 — actual-only budget evaluation.

Pure, deterministic evaluation of job budgets against recorded actuals.
No writes, no stop, no side effects. Injected clock for wall-time/deadline.

F104 adds a second, FORWARD-looking evaluation next to the reactive one:
``predict_next_task_cost``. ``run_job`` calls it at the task-dispatch safe
point in ``packages/orchestration/pingpong_job.py``, after the operator stop
and after the reactive check, on the same counters the reactive check just
evaluated. The band it needs is derived there by ``derive_next_task_token_band``
from the next task's own text (DECISION F104 D3 and D6) — a JobTask stores no
band, and the prompt is deliberately not built before the safe point.

The reactive check in ``evaluate_budget`` remains the BACKSTOP: prediction only
ever stops earlier than the backstop would, never instead of it, and both
functions here stay pure so the stop path holds no estimation logic of its own.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import UUID

from packages.core.models import JobBudgets
from packages.orchestration import token_economy
from packages.orchestration.token_economy import TokenBand

if TYPE_CHECKING:  # import-light at runtime: the config type is duck-typed here
    from packages.orchestration.budget_resolution import PredictiveBudgetConfig

VALID_ACTUAL_SOURCES = frozenset({
    "pingpong_actuals", "pingpong_live", "persisted_job_actuals",
    "token_actuals", "aggregate_actuals",
})


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
    # F104 money actuals. None means UNPRICED — no provider reported a cost —
    # and it is NOT interchangeable with 0.0, which means "measured, and free".
    measured_cost_usd: float | None = None
    unpriced_call_count: int = 0
    # WHY these two are never compared against provider_calls: the cost-side
    # call counts come from the F103 ledger and are counted per FINALIZED TASK
    # RUN across every run of the job, while provider_calls counts ATTEMPTS in
    # THIS run (skipping the fake provider). They are different measurements of
    # different things and must never be compared (R-0224, DECISION F104 D5).
    priced_call_count: int = 0

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
                "elapsed_seconds must be a number, got bool")
        if not isinstance(self.elapsed_seconds, (int, float)) or self.elapsed_seconds < 0:
            raise BudgetCounterError(
                f"elapsed_seconds must be non-negative, got {self.elapsed_seconds!r}")
        if isinstance(self.elapsed_seconds, float) and not math.isfinite(self.elapsed_seconds):
            raise BudgetCounterError(
                f"elapsed_seconds must be finite, got {self.elapsed_seconds!r}")
        if not isinstance(self.evaluated_at, datetime):
            raise BudgetCounterError(
                f"evaluated_at must be a datetime, got {type(self.evaluated_at).__name__}")
        if self.evaluated_at.tzinfo is None:
            raise BudgetCounterError("evaluated_at must be timezone-aware")
        if not isinstance(self.actual_sources, tuple):
            raise BudgetCounterError(
                f"actual_sources must be a tuple, got {type(self.actual_sources).__name__}")
        for i, src in enumerate(self.actual_sources):
            if not isinstance(src, str):
                raise BudgetCounterError(
                    f"actual_sources[{i}] must be str, got {type(src).__name__}")
            if not src:
                raise BudgetCounterError(
                    f"actual_sources[{i}] must not be empty")
            if src not in VALID_ACTUAL_SOURCES:
                raise BudgetCounterError(
                    f"actual_sources[{i}] unknown source: {src!r}")
        if self.started_at is not None:
            if not isinstance(self.started_at, datetime):
                raise BudgetCounterError(
                    f"started_at must be a datetime or None, got {type(self.started_at).__name__}")
            if self.started_at.tzinfo is None:
                raise BudgetCounterError("started_at must be timezone-aware")
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
        if self.measured_token_total > 0 and self.measured_call_count == 0:
            raise BudgetCounterError(
                f"measured_token_total ({self.measured_token_total}) > 0 "
                f"but measured_call_count is 0")
        if self.measured_call_count > 0 and not self.actual_sources:
            raise BudgetCounterError(
                "measured_call_count > 0 but actual_sources is empty")
        # measured_cost_usd is None when NOTHING reported a cost. None and 0.0
        # are different facts (P6) and neither is ever repaired into the other.
        if self.measured_cost_usd is not None:
            if isinstance(self.measured_cost_usd, bool):
                raise BudgetCounterError(
                    "measured_cost_usd must be a number or None, got bool")
            if not isinstance(self.measured_cost_usd, (int, float)):
                raise BudgetCounterError(
                    f"measured_cost_usd must be a number or None, got "
                    f"{type(self.measured_cost_usd).__name__}")
            if not math.isfinite(self.measured_cost_usd):
                raise BudgetCounterError(
                    f"measured_cost_usd must be finite, got {self.measured_cost_usd!r}")
            if self.measured_cost_usd < 0:
                raise BudgetCounterError(
                    f"measured_cost_usd must be non-negative, got "
                    f"{self.measured_cost_usd!r}")
        for name in ("unpriced_call_count", "priced_call_count"):
            val = getattr(self, name)
            if isinstance(val, bool):
                raise BudgetCounterError(f"{name} must be int, got bool")
            if not isinstance(val, int) or val < 0:
                raise BudgetCounterError(
                    f"{name} must be a non-negative integer, got {val!r}")
        # The cost side is validated against the COST SIDE only (R-0224,
        # DECISION F104 D5): money reported with nothing priced to explain it is
        # still a contradiction, but neither count is ever weighed against
        # provider_calls, which counts something else entirely.
        if (
            self.measured_cost_usd is not None
            and self.measured_cost_usd > 0
            and self.priced_call_count == 0
            and self.unpriced_call_count > 0
        ):
            raise BudgetCounterError(
                f"measured_cost_usd ({self.measured_cost_usd}) > 0 but "
                f"priced_call_count is 0 and all {self.unpriced_call_count} "
                f"cost-side calls are unpriced")

    @property
    def total_call_count(self) -> int:
        return self.measured_call_count + self.unmeasured_call_count

    @property
    def has_unmeasured(self) -> bool:
        return self.unmeasured_call_count > 0

    # The money mirror of has_unmeasured: at least one call carries no price.
    @property
    def has_unpriced(self) -> bool:
        return self.unpriced_call_count > 0

    def token_description(self) -> str:
        if self.unmeasured_call_count > 0:
            return (
                f">= {self.measured_token_total} tokens "
                f"({self.unmeasured_call_count} provider calls unmeasured)"
            )
        return f"{self.measured_token_total} tokens"

    # The money mirror of token_description: an unpriced figure says so in words.
    def cost_description(self) -> str:
        """Render the cost actuals without ever printing an unknown as a zero."""
        if self.measured_cost_usd is None:
            return "not-measured"
        if self.unpriced_call_count > 0:
            return (
                f">= ${self.measured_cost_usd:.4f} "
                f"({self.unpriced_call_count} provider calls unpriced)"
            )
        return f"${self.measured_cost_usd:.4f}"

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
            # Stays None in JSON when unpriced — a null, never a zero (P6).
            "measured_cost_usd": self.measured_cost_usd,
            "unpriced_call_count": self.unpriced_call_count,
            "priced_call_count": self.priced_call_count,
        }


@dataclass(frozen=True)
class BudgetEvaluation:
    """Result of evaluating budgets against actuals."""

    configured_limits: JobBudgets | None
    counters: BudgetCounters
    exhausted: bool
    first_exhausted_limit: str | None = None
    token_lower_bound: bool = False
    # True when the cost figure is a floor, not a total: some call was unpriced.
    cost_lower_bound: bool = False
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
            "cost_lower_bound": self.cost_lower_bound,
            "warnings": list(self.warnings),
            "source_descriptions": list(self.source_descriptions),
        }


_LIMIT_ORDER = (
    "max_provider_calls",
    "max_total_tokens",
    "max_cost_usd",
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
    cost_lower_bound = False

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

    if budgets.max_cost_usd is not None:
        sources.append(
            f"cost: {counters.cost_description()}/${budgets.max_cost_usd:.4f}")
        if counters.measured_cost_usd is None:
            cost_lower_bound = True
            warnings.append(
                f"cost is unpriced "
                f"({counters.unpriced_call_count} calls unpriced); "
                f"no call reported a cost; cannot determine exhaustion"
            )
        elif counters.has_unpriced:
            # A lower bound ALREADY over the limit is a definite breach: pricing
            # the remaining calls can only add money, never remove it. A lower
            # bound still under the limit is genuinely undecidable, so it warns.
            cost_lower_bound = True
            if counters.measured_cost_usd >= budgets.max_cost_usd:
                exhausted_limits.append("max_cost_usd")
            else:
                warnings.append(
                    f"cost is a lower bound "
                    f"({counters.unpriced_call_count} calls unpriced); "
                    f"cannot definitively determine exhaustion"
                )
        else:
            if counters.measured_cost_usd >= budgets.max_cost_usd:
                exhausted_limits.append("max_cost_usd")

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
        cost_lower_bound=cost_lower_bound,
        warnings=tuple(warnings),
        source_descriptions=tuple(sources),
    )


# F104 predictive cost — the five labels a prediction may wear, and no others.
# Every user-facing predicted number carries one of these; that is an acceptance
# criterion of the feature, not decoration.
VALID_ESTIMATE_BASES = frozenset({
    "class_default",
    "class_default_missing_band",
    "no_price_basis",
    "no_cost_limit",
    "unpriced_spend",
})

_PREDICTABLE_BASES = ("class_default", "class_default_missing_band")


# Renders a money figure, or says out loud that there is none. An unmeasured
# figure is NEVER rendered as a measured zero (P6).
def _format_prediction_usd(value: float | None) -> str:
    return "not-measured" if value is None else f"${value:.4f}"


@dataclass(frozen=True)
class BudgetPrediction:
    """What the NEXT task is expected to cost, and whether it would breach.

    An ESTIMATE, never a measurement: ``estimate_basis`` names where the number
    came from and is always one of ``VALID_ESTIMATE_BASES``. ``arithmetic`` is
    the one-line human-readable justification — a human must be able to see WHY
    a predictive stop happened without reading this module.
    """

    would_breach: bool
    estimate_basis: str
    band: str
    expected_tokens: int | None
    expected_cost_usd: float | None
    spent_cost_usd: float | None
    limit_usd: float | None
    arithmetic: str

    def to_json(self) -> dict[str, Any]:
        return {
            "would_breach": self.would_breach,
            # The label travels with the numbers wherever they surface.
            "estimate_basis": self.estimate_basis,
            "band": self.band,
            "expected_tokens": self.expected_tokens,
            # Stays None when no price basis is configured — never a zero.
            "expected_cost_usd": self.expected_cost_usd,
            "spent_cost_usd": self.spent_cost_usd,
            "limit_usd": self.limit_usd,
            "arithmetic": self.arithmetic,
        }


# Derives the band for the NEXT task from the text that will make up its
# context. A JobTask carries no band field (DECISION F104 D3), and this
# deliberately does NOT call `_build_task_prompt`: building the prompt
# before the safe point would move work ahead of the stop consumption
# guarantee that the safe point exists to provide (DECISION F104 D6).
def derive_next_task_token_band(task, previous_summaries=()) -> str:
    """Estimate the next task's token band from its own text plus prior proofs.

    Pure: no I/O, no clock. The estimate is a FLOOR — it counts the task's own
    text and the token counts of the proof summaries that will be folded into
    its prompt, not the assembled prompt itself (DECISION F104 D6).

    NEVER raises. It runs inside a stop check, and a stop check that dies on a
    malformed task would take a healthy job down with it; every degradation
    path ends at ``TokenBand.UNKNOWN``, which the A9 path in
    ``predict_next_task_cost`` treats as the LARGEST class default.
    """
    if task is None:
        return TokenBand.UNKNOWN
    try:
        total = 0
        for _name in ("title", "body", "acceptance"):
            total += token_economy.estimate_text_tokens(getattr(task, _name, "") or "")
        for _summary in previous_summaries or ():
            _tokens = getattr(_summary, "tokens_estimated", 0)
            # bool is an int subclass; a True here would be a data bug, not a count.
            if isinstance(_tokens, int) and not isinstance(_tokens, bool) and _tokens >= 0:
                total += _tokens
        return token_economy.estimate_task_token_band(
            task_type="job_task", context_estimate=total)
    except Exception:
        return TokenBand.UNKNOWN


# Predicts what the next task will cost so a job can stop BEFORE it overspends.
# Pure: no reads, no writes, no clock. Called by `run_job`'s `_stop_check` at the
# task-dispatch safe point, with the band from `derive_next_task_token_band`
# (DECISION F104 D3/D6) and the counters the reactive check just used. The
# reactive check in `evaluate_budget` remains the backstop for what this misses.
def predict_next_task_cost(
    budgets: JobBudgets | None,
    counters: BudgetCounters,
    *,
    band: str | None,
    config: PredictiveBudgetConfig,
) -> BudgetPrediction:
    """Estimate the next task's cost against the money limit.

    ``band`` is a ``TokenBand`` value. ``"unknown"``, None and any unrecognised
    string all mean the band could not be derived, and take the feature's A9
    path: the LARGEST class default, labelled ``class_default_missing_band``,
    because over-stopping beats overspending.

    ``would_breach`` is True ONLY when real numbers could be compared, and uses
    a strict ``>``: the exact-limit case belongs to the reactive check in
    ``evaluate_budget``, and duplicating it here would let the two disagree
    about the boundary.
    """
    class_defaults = dict(getattr(config, "class_default_tokens", None) or {})
    price_basis = getattr(config, "price_basis_usd_per_1k_tokens", None)
    limit = budgets.max_cost_usd if budgets is not None else None

    if band in (TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH) and band in class_defaults:
        resolved_band = band
        expected_tokens: int | None = class_defaults[band]
        band_basis = "class_default"
    else:
        resolved_band = TokenBand.UNKNOWN
        expected_tokens = max(class_defaults.values()) if class_defaults else None
        band_basis = "class_default_missing_band"

    expected_cost_usd = token_economy.tokens_to_cost_usd(expected_tokens, price_basis)

    spent = counters.measured_cost_usd
    # WHY the exception: a job that has made NO provider call has definitionally
    # spent nothing, so 0.0 there is a measurement and not an assumed zero.
    if spent is None and counters.provider_calls == 0:
        spent = 0.0

    note: str | None = None
    if limit is None:
        estimate_basis = "no_cost_limit"
        note = "no cost limit is configured"
    elif price_basis is None:
        estimate_basis = "no_price_basis"
        note = "the price basis is unset, so no cost is predicted"
    elif spent is None:
        estimate_basis = "unpriced_spend"
        note = (
            f"spend so far is unpriced "
            f"({counters.unpriced_call_count} of {counters.provider_calls} "
            f"provider calls unpriced)"
        )
    else:
        estimate_basis = band_basis

    comparable = (
        estimate_basis in _PREDICTABLE_BASES
        and expected_cost_usd is not None
        and spent is not None
        and limit is not None
    )
    would_breach = bool(comparable and (spent + expected_cost_usd) > limit)

    if not comparable:
        comparison = "?"
    elif would_breach:
        comparison = ">"
    else:
        comparison = "<="
    tokens_label = "not-measured" if expected_tokens is None else str(expected_tokens)
    arithmetic = (
        f"spent {_format_prediction_usd(spent)} + "
        f"expected {_format_prediction_usd(expected_cost_usd)} "
        f"({tokens_label} tokens, band={resolved_band}, basis={estimate_basis}) "
        f"{comparison} limit {_format_prediction_usd(limit)}"
    )
    if note is not None:
        arithmetic = f"{arithmetic}; {note}"

    return BudgetPrediction(
        would_breach=would_breach,
        estimate_basis=estimate_basis,
        band=resolved_band,
        expected_tokens=expected_tokens,
        expected_cost_usd=expected_cost_usd,
        spent_cost_usd=spent,
        limit_usd=limit,
        arithmetic=arithmetic,
    )


def collect_counters_from_actuals(
    actuals: dict[str, Any],
    *,
    started_at: datetime | None = None,
    now: datetime | None = None,
    actual_sources: tuple[str, ...] | None = None,
    measured_cost_usd: float | None = None,
    unpriced_call_count: int = 0,
    priced_call_count: int = 0,
) -> BudgetCounters:
    """Build BudgetCounters from _aggregate_usage_actuals() output.

    This is the public bridge from PingPongResult's aggregated actuals
    to the budget evaluation system. Never re-parses provider output.

    *actual_sources*: provenance of the actuals data. Must not be empty
    when measured calls are present.

    *measured_cost_usd* / *unpriced_call_count* / *priced_call_count*: F104
    money actuals, passed straight through. The two call counts are the ledger's
    own cost-side split and are never compared against *provider_call_count*,
    which counts something else (R-0224, DECISION F104 D5).
    This function deliberately does NOT read the ledger —
    it stays the pure actuals bridge; ``collect_ledger_cost_for_job`` is the
    ledger reader, and a caller composes the two.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise BudgetCounterError("now must be a timezone-aware datetime")

    provider_call_count = actuals.get("provider_call_count", 0)
    actual_call_count = actuals.get("actual_call_count", 0)
    total_tokens = actuals.get("total_tokens", 0)
    for _name, _val in (("provider_call_count", provider_call_count),
                        ("actual_call_count", actual_call_count),
                        ("total_tokens", total_tokens)):
        if _val is None:
            _val = 0
        if isinstance(_val, bool):
            raise BudgetCounterError(f"{_name} must be int, got bool")
        if isinstance(_val, float):
            raise BudgetCounterError(f"{_name} must be int, got float")
        if isinstance(_val, str):
            raise BudgetCounterError(f"{_name} must be int, got str")
        if not isinstance(_val, int):
            raise BudgetCounterError(
                f"{_name} must be int, got {type(_val).__name__}")
        if _val < 0:
            raise BudgetCounterError(f"{_name} must be non-negative, got {_val}")
    if provider_call_count is None:
        provider_call_count = 0
    if actual_call_count is None:
        actual_call_count = 0
    if total_tokens is None:
        total_tokens = 0
    if actual_call_count > provider_call_count:
        raise BudgetCounterError(
            f"actual_call_count ({actual_call_count}) > "
            f"provider_call_count ({provider_call_count})")
    unmeasured = provider_call_count - actual_call_count
    if total_tokens > 0 and actual_call_count == 0:
        raise BudgetCounterError(
            f"measured tokens ({total_tokens}) without any measured calls")
    elapsed = 0.0
    if started_at is not None:
        if not isinstance(started_at, datetime):
            raise BudgetCounterError(
                f"started_at must be datetime, got {type(started_at).__name__}")
        if started_at.tzinfo is None:
            raise BudgetCounterError("started_at must be timezone-aware")
        elapsed = max(0.0, (now - started_at).total_seconds())

    if actual_sources is None:
        actual_sources = ("pingpong_actuals",) if actual_call_count > 0 else ()
    if actual_call_count > 0 and not actual_sources:
        raise BudgetCounterError(
            "measured calls present but actual_sources is empty")
    for _s in actual_sources:
        if not isinstance(_s, str) or not _s:
            raise BudgetCounterError(f"actual_sources contains invalid entry: {_s!r}")
        if _s not in VALID_ACTUAL_SOURCES:
            raise BudgetCounterError(f"unknown actual source: {_s!r}")
    return BudgetCounters(
        provider_calls=provider_call_count,
        measured_token_total=total_tokens,
        measured_call_count=actual_call_count,
        unmeasured_call_count=unmeasured,
        elapsed_seconds=elapsed,
        evaluated_at=now,
        started_at=started_at,
        actual_sources=actual_sources,
        measured_cost_usd=measured_cost_usd,
        unpriced_call_count=unpriced_call_count,
        priced_call_count=priced_call_count,
    )


# Budgets learn what a job has actually cost by reading the F103 ledger, which
# is the only place in Remedy a real provider cost figure lives.
def collect_ledger_cost_for_job(
    *,
    job_id: str,
    project_id: UUID | str | None = None,
    path: Path | str | None = None,
) -> tuple[float | None, int, int]:
    """Return (measured_cost_usd, priced_call_count, unpriced_call_count).

    The cost stays None when NO call in the job reported one — ``query_cost``
    preserves SQLite's NULL over an all-NULL ``SUM()`` and nothing here coerces
    it to 0.0 (P6). No price is ever invented.

    ``CostRow.measured_calls``/``unmeasured_calls`` count the ledger's
    ``cost_basis`` column — ``provider_reported`` versus ``unknown`` — which is
    exactly the priced/unpriced split budgets need.

    A ledger file that does not exist yields an EMPTY report rather than an
    error, so a project that has never recorded a call returns (None, 0, 0).
    That is deliberate: asking what a job cost must not create its ledger.
    """
    # Imported inside the function on purpose: this module is import-light
    # (stdlib plus the models) and evaluating a budget must not drag SQLite in.
    from packages.orchestration.token_ledger import query_cost

    report = query_cost(project_id=project_id, path=path, job_id=job_id)
    total = report.total
    return (total.cost_usd, total.measured_calls, total.unmeasured_calls)


_PERSISTED_ACTUALS_FIELDS = frozenset({
    "schema_version", "provider_call_count", "actual_call_count",
    "unmeasured_call_count", "total_tokens", "actual_sources", "started_at",
})


def decode_persisted_budget_actuals(
    raw: dict[str, Any],
    *,
    first_running_at: str | None = None,
) -> dict[str, Any]:
    """Decode and validate a PersistedBudgetActualsV1 record.

    Returns a validated dict with typed values. Raises BudgetCounterError on
    any schema violation — no default-zero repair, no invented sources.

    When *first_running_at* is provided, the persisted started_at must
    represent the same UTC instant; a mismatch is corrupt state.
    """
    if not isinstance(raw, dict):
        raise BudgetCounterError(
            f"persisted actuals must be a dict, got {type(raw).__name__}")
    missing = _PERSISTED_ACTUALS_FIELDS - set(raw)
    if missing:
        raise BudgetCounterError(
            f"persisted actuals missing required fields: {sorted(missing)}")
    extra = set(raw) - _PERSISTED_ACTUALS_FIELDS
    if extra:
        raise BudgetCounterError(
            f"persisted actuals has unknown fields: {sorted(extra)}")
    sv = raw["schema_version"]
    if sv != "1.0.0":
        raise BudgetCounterError(
            f"persisted actuals schema_version {sv!r} is not '1.0.0'")

    for name in ("provider_call_count", "actual_call_count",
                 "unmeasured_call_count", "total_tokens"):
        val = raw[name]
        if isinstance(val, bool):
            raise BudgetCounterError(f"persisted {name} is bool, not int")
        if isinstance(val, float):
            raise BudgetCounterError(f"persisted {name} is float, not int")
        if isinstance(val, str):
            raise BudgetCounterError(f"persisted {name} is str, not int")
        if not isinstance(val, int):
            raise BudgetCounterError(
                f"persisted {name} has type {type(val).__name__}")
        if val < 0:
            raise BudgetCounterError(f"persisted {name} is negative: {val}")

    pc = raw["provider_call_count"]
    ac = raw["actual_call_count"]
    umc = raw["unmeasured_call_count"]
    tt = raw["total_tokens"]
    if umc != pc - ac:
        raise BudgetCounterError(
            f"persisted unmeasured_call_count ({umc}) != "
            f"provider_call_count ({pc}) - actual_call_count ({ac})")
    if tt > 0 and ac == 0:
        raise BudgetCounterError(
            f"persisted total_tokens ({tt}) > 0 but actual_call_count is 0")
    if ac > pc:
        raise BudgetCounterError(
            f"persisted actual_call_count ({ac}) > "
            f"provider_call_count ({pc})")

    asrc = raw["actual_sources"]
    if not isinstance(asrc, (list, tuple)):
        raise BudgetCounterError(
            f"persisted actual_sources has type {type(asrc).__name__}")
    for i, s in enumerate(asrc):
        if not isinstance(s, str) or not s:
            raise BudgetCounterError(
                f"persisted actual_sources[{i}] is not a nonempty string")
        if s not in VALID_ACTUAL_SOURCES:
            raise BudgetCounterError(
                f"persisted actual_sources[{i}] unknown: {s!r}")
    if ac > 0 and len(asrc) == 0:
        raise BudgetCounterError(
            f"persisted actual_call_count ({ac}) > 0 but actual_sources empty")

    sa_raw = raw["started_at"]
    if not isinstance(sa_raw, str) or not sa_raw:
        raise BudgetCounterError(
            f"persisted started_at must be a nonempty string, got {sa_raw!r}")
    try:
        sa_parsed = datetime.fromisoformat(sa_raw)
    except (ValueError, TypeError) as exc:
        raise BudgetCounterError(
            f"persisted started_at cannot be parsed: {sa_raw!r}: {exc}")
    if sa_parsed.tzinfo is None:
        raise BudgetCounterError(
            f"persisted started_at is timezone-naive: {sa_raw!r}")

    if first_running_at is not None:
        try:
            fra_parsed = datetime.fromisoformat(first_running_at)
        except (ValueError, TypeError) as exc:
            raise BudgetCounterError(
                f"first_running_at cannot be parsed: {first_running_at!r}: {exc}")
        if fra_parsed.tzinfo is None:
            raise BudgetCounterError(
                f"first_running_at is timezone-naive: {first_running_at!r}")
        if sa_parsed != fra_parsed:
            raise BudgetCounterError(
                f"persisted started_at ({sa_raw}) != "
                f"first_running_at ({first_running_at}): wall-clock split")

    return {
        "schema_version": sv,
        "provider_call_count": pc,
        "actual_call_count": ac,
        "unmeasured_call_count": umc,
        "total_tokens": tt,
        "actual_sources": tuple(str(s) for s in asrc),
        "started_at": sa_parsed,
    }


def counters_from_persisted(
    validated: dict[str, Any],
    *,
    now: datetime | None = None,
) -> BudgetCounters:
    """Build BudgetCounters from a validated persisted actuals record.

    The record must have been validated by decode_persisted_budget_actuals first.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    sa = validated["started_at"]
    elapsed = max(0.0, (now - sa).total_seconds()) if isinstance(sa, datetime) else 0.0
    return BudgetCounters(
        provider_calls=validated["provider_call_count"],
        measured_token_total=validated["total_tokens"],
        measured_call_count=validated["actual_call_count"],
        unmeasured_call_count=validated["unmeasured_call_count"],
        elapsed_seconds=elapsed,
        evaluated_at=now,
        started_at=sa,
        actual_sources=validated["actual_sources"],
    )
