"""F116 T001 — the burn detector: the one definition of expected spend.

A runaway between checkpoints burns quietly unless something compares what a
run is spending NOW with what it was expected to spend. This module is that
comparison, factored out of the watchdog's own tripwire (DECISION F116 D1) so
every caller — the watchdog today, the job runner from T002 on — reads the
same arithmetic rather than keeping its own copy.

Two BASES, chosen by whether the caller supplies an hourly expectation:

  * ``trailing_baseline`` (rate unit ``per_sample``) — no outside expectation
    at all. The expected rate is the run's OWN earlier measured samples; a
    recent window is compared against everything measured before it. This is
    exactly the watchdog's present contract (DECISION F116 D2), reproduced
    here rather than re-derived, so T003 can delete the watchdog's private
    copy once it calls this one.
  * ``class_default`` (rate unit ``per_hour``) — the caller supplies
    ``expected_per_hour``, a configured class expectation. The rate is read
    across wall-clock time between a fixed anchor sample and the most recent
    window, because an hourly rate needs an hour to measure against.

DELIBERATE ABSENCES. This module reads no clock: every time value its
arithmetic uses comes from a sample's own ``at``, never from
``datetime.now()`` or an equivalent — a detector that could read the clock
itself would need to be trusted the way the clock is, and nothing here is
trusted; it is only checked. It reads no configuration and no file: the
watchdog already resolves its own thresholds once at the edge and hands them
down as a plain value (``watchdog_thresholds_from_config``), and this module
follows that same shape — a caller resolves ``BurnThresholds`` once, wherever
it reads config, and this function stays callable with no config layer
present.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

#: The ``class_default`` basis: an outside, configured hourly expectation.
BASIS_CLASS_DEFAULT = "class_default"
#: The ``trailing_baseline`` basis: the run's own earlier measured samples.
BASIS_TRAILING_BASELINE = "trailing_baseline"
#: The trailing basis compares means of samples; its rate has no time unit.
RATE_UNIT_PER_SAMPLE = "per_sample"
#: The class basis compares spend against wall-clock time between samples.
RATE_UNIT_PER_HOUR = "per_hour"


#: One spend observation. ``label`` is carried into the reading for a caller
#: to attribute back to its own record (an iteration, a task id); it is never
#: used as an index here, exactly as the watchdog's own ``_iteration`` is only
#: ever evidence and never a position.
@dataclass(frozen=True)
class BurnSample:
    """``amount`` is spend in whatever unit the caller measures; ``at`` is when."""

    amount: float | None
    at: datetime | None = None
    label: int = 0


#: The four numbers and the one switch a caller resolves once, at the edge.
#: ``expected_per_hour`` set at all is what chooses the ``class_default``
#: basis over ``trailing_baseline`` — there is no separate flag, because a
#: caller that has an hourly expectation to give always means to use it.
@dataclass(frozen=True)
class BurnThresholds:
    """Conservative by default, exactly as the watchdog's own thresholds are."""

    window: int = 3
    min_samples: int = 5
    multiplier: float = 3.0
    min_spend: float = 0.0
    expected_per_hour: float | None = None


#: What the evaluator found, whether or not it tripped — a caller that is
#: showing an attended run the numbers needs them even when nothing is wrong.
@dataclass(frozen=True)
class BurnReading:
    """The evidence behind one verdict: which basis, which numbers, since when."""

    tripped: bool
    basis: str
    rate_unit: str
    rate: float
    expectation: float
    multiplier: float
    window_samples: int
    baseline_samples: int
    window_spend: float
    since_label: int

    #: The wire form. Exactly these ten keys — a reading carries no hidden state.
    def to_json(self) -> dict[str, Any]:
        return {
            "tripped": self.tripped,
            "basis": self.basis,
            "rate_unit": self.rate_unit,
            "rate": self.rate,
            "expectation": self.expectation,
            "multiplier": self.multiplier,
            "window_samples": self.window_samples,
            "baseline_samples": self.baseline_samples,
            "window_spend": self.window_spend,
            "since_label": self.since_label,
        }


#: A sample counts only when it is a real, non-negative, finite measurement.
#: ``bool`` is excluded even though it is an ``int`` subclass, and a negative
#: or non-finite amount is excluded outright: either would drag a baseline or
#: a rate to a value no provider reported (DECISION F116 D2, ALTERNATIVES).
def _is_measured(amount: float | None) -> bool:
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return False
    return math.isfinite(amount) and amount >= 0


#: Timezone-aware only — a naive datetime cannot be measured against another
#: sample's clock without guessing an offset, so it is treated as missing.
def _is_aware(at: datetime | None) -> bool:
    return at is not None and at.tzinfo is not None


#: The one definition of "expected spend" (DECISION F116 D2). Standard
#: library only; no clock read, no file, no configuration — see the module
#: docstring's deliberate absences.
def evaluate_burn_rate(
    samples: Sequence[BurnSample],
    thresholds: BurnThresholds,
) -> BurnReading | None:
    """``None`` while there is too little to judge; otherwise always a reading."""
    if thresholds.window < 1:
        return None
    measured = [s for s in samples if _is_measured(s.amount)]

    if thresholds.expected_per_hour is None:
        basis = BASIS_TRAILING_BASELINE
        rate_unit = RATE_UNIT_PER_SAMPLE
        if len(measured) < thresholds.min_samples + thresholds.window:
            return None
        recent = measured[-thresholds.window:]
        baseline = measured[:-thresholds.window]
        if not baseline:
            return None
        rate = sum(s.amount for s in recent) / len(recent)
        expectation = sum(s.amount for s in baseline) / len(baseline)
        baseline_samples = len(baseline)
    else:
        basis = BASIS_CLASS_DEFAULT
        rate_unit = RATE_UNIT_PER_HOUR
        if len(measured) < thresholds.window + 1:
            return None
        recent = measured[-thresholds.window:]
        anchor = measured[-(thresholds.window + 1)]
        if not _is_aware(anchor.at) or any(not _is_aware(s.at) for s in recent):
            return None
        span_hours = (recent[-1].at - anchor.at).total_seconds() / 3600.0
        if not span_hours > 0:
            return None
        rate = sum(s.amount for s in recent) / span_hours
        expectation = thresholds.expected_per_hour
        baseline_samples = 0

    window_spend = sum(s.amount for s in recent)
    tripped = (window_spend > thresholds.min_spend
               and rate > thresholds.multiplier * expectation)
    return BurnReading(
        tripped=tripped,
        basis=basis,
        rate_unit=rate_unit,
        rate=rate,
        expectation=expectation,
        multiplier=thresholds.multiplier,
        window_samples=len(recent),
        baseline_samples=baseline_samples,
        window_spend=window_spend,
        since_label=recent[0].label,
    )
