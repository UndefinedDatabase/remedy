"""F116 T001 — the burn detector's table tests (DECISION F116 D2).

One test function per behaviour. The trailing basis reproduces the
watchdog's own ``evaluate_burn_anomaly`` exactly (DECISION F116 D1), so the
table test at the bottom builds the SAME ledger entries ``test_watchdog.py``
builds and asserts the two evaluators agree, number for number, rather than
asserting each in isolation and hoping they stay in step.

Fixtures are built IN-PROCESS — plain dataclasses and plain dicts, no JSONL
file, no disk, no conftest, exactly as ``test_watchdog.py`` builds its own.
"""
from __future__ import annotations

import ast
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.orchestration.burn_detector import (
    BASIS_CLASS_DEFAULT,
    BASIS_TRAILING_BASELINE,
    RATE_UNIT_PER_HOUR,
    RATE_UNIT_PER_SAMPLE,
    BurnReading,
    BurnSample,
    BurnThresholds,
    evaluate_burn_rate,
)
from packages.orchestration.watchdog import evaluate_burn_anomaly, measured_tokens
from tests.orchestration.test_watchdog import _entry

MODULE_PATH = Path(__file__).resolve().parents[2] / "packages/orchestration/burn_detector.py"


def _samples(amounts: list[float], *, start: int = 1) -> list[BurnSample]:
    """One ``BurnSample`` per amount, labelled by position, no timestamps."""
    return [BurnSample(amount=amount, label=label)
            for label, amount in enumerate(amounts, start=start)]


# ── the trailing basis ──────────────────────────────────────────────────────


def test_a_trailing_spike_trips_with_its_arithmetic():
    samples = _samples([100, 100, 100, 100, 100, 400, 400, 400])

    reading = evaluate_burn_rate(samples, BurnThresholds())

    assert reading is not None
    assert reading.tripped is True
    assert reading.basis == BASIS_TRAILING_BASELINE
    assert reading.rate_unit == RATE_UNIT_PER_SAMPLE
    assert reading.rate == 400.0
    assert reading.expectation == 100.0
    assert reading.multiplier == 3.0
    assert reading.window_samples == 3
    assert reading.baseline_samples == 5
    assert reading.window_spend == 1200.0
    assert reading.since_label == 6


def test_steady_expensive_work_does_not_trip():
    samples = _samples([5000] * 10)

    reading = evaluate_burn_rate(samples, BurnThresholds())

    assert reading is not None
    assert reading.tripped is False
    assert reading.rate == 5000.0
    assert reading.expectation == 5000.0


def test_tiny_spend_trips_with_no_floor_and_not_with_one():
    samples = _samples([1, 1, 1, 1, 1, 10, 10, 10])

    uncapped = evaluate_burn_rate(samples, BurnThresholds(min_spend=0.0))
    floored = evaluate_burn_rate(samples, BurnThresholds(min_spend=50.0))

    assert uncapped is not None and uncapped.tripped is True
    assert uncapped.window_spend == 30.0
    assert floored is not None and floored.tripped is False
    assert floored.window_spend == 30.0


def test_fewer_than_min_samples_plus_window_returns_none():
    samples = _samples([100, 100, 100, 100, 100, 400, 400])

    assert evaluate_burn_rate(samples, BurnThresholds()) is None


def test_trailing_basis_equality_boundary_does_not_trip():
    """R-1165: rate EQUALS ``multiplier * expectation`` — the comparison is strict."""
    samples = _samples([100, 100, 100, 100, 100, 300, 300, 300])

    reading = evaluate_burn_rate(samples, BurnThresholds())

    assert reading is not None
    assert reading.tripped is False
    assert reading.rate == 300.0
    assert reading.expectation == 100.0


def test_unmeasured_samples_interleaved_give_the_same_reading_as_without_them():
    clean = _samples([100, 100, 100, 100, 100, 400, 400, 400])
    noisy = [
        BurnSample(amount=None, label=90),
        clean[0],
        BurnSample(amount=True, label=91),
        clean[1],
        BurnSample(amount=-5.0, label=92),
        clean[2],
        BurnSample(amount=float("nan"), label=93),
        clean[3],
        clean[4],
        clean[5],
        BurnSample(amount=None, label=94),
        clean[6],
        clean[7],
    ]

    clean_reading = evaluate_burn_rate(clean, BurnThresholds())
    noisy_reading = evaluate_burn_rate(noisy, BurnThresholds())

    assert clean_reading is not None and noisy_reading is not None
    assert noisy_reading == clean_reading


# ── the class_default (per-hour) basis ──────────────────────────────────────

_ANCHOR = datetime(2026, 9, 1, 0, 0, 0, tzinfo=timezone.utc)


def _hour_samples(*, naive_last: bool = False, missing_last: bool = False,
                   zero_span: bool = False) -> list[BurnSample]:
    """One anchor at ``_ANCHOR`` plus three samples at +20, +40 and +60 minutes."""
    anchor = BurnSample(amount=1.0, at=_ANCHOR, label=0)
    offsets = [20, 40, 60]
    recent = []
    for i, minutes in enumerate(offsets, start=1):
        at = _ANCHOR if zero_span else _ANCHOR + timedelta(minutes=minutes)
        if i == len(offsets) and missing_last:
            at = None
        elif i == len(offsets) and naive_last:
            at = at.replace(tzinfo=None)
        recent.append(BurnSample(amount=1.0, at=at, label=i))
    return [anchor, *recent]


def test_per_hour_basis_trips_above_the_expectation():
    reading = evaluate_burn_rate(
        _hour_samples(), BurnThresholds(expected_per_hour=0.5))

    assert reading is not None
    assert reading.tripped is True
    assert reading.basis == BASIS_CLASS_DEFAULT
    assert reading.rate_unit == RATE_UNIT_PER_HOUR
    assert reading.rate == 3.0
    assert reading.expectation == 0.5
    assert reading.baseline_samples == 0


def test_per_hour_basis_does_not_trip_below_the_expectation():
    reading = evaluate_burn_rate(
        _hour_samples(), BurnThresholds(expected_per_hour=1.5))

    assert reading is not None
    assert reading.tripped is False
    assert reading.rate == 3.0
    assert reading.expectation == 1.5


def test_per_hour_basis_with_a_missing_at_returns_none():
    reading = evaluate_burn_rate(
        _hour_samples(missing_last=True), BurnThresholds(expected_per_hour=0.5))

    assert reading is None


def test_per_hour_basis_with_a_naive_at_returns_none():
    reading = evaluate_burn_rate(
        _hour_samples(naive_last=True), BurnThresholds(expected_per_hour=0.5))

    assert reading is None


def test_per_hour_basis_with_a_zero_span_returns_none():
    reading = evaluate_burn_rate(
        _hour_samples(zero_span=True), BurnThresholds(expected_per_hour=0.5))

    assert reading is None


def test_per_hour_basis_with_too_few_samples_returns_none():
    samples = _hour_samples()[:3]  # anchor plus two recent — one short of window+1

    reading = evaluate_burn_rate(samples, BurnThresholds(expected_per_hour=0.5))

    assert reading is None


def test_per_hour_basis_equality_boundary_does_not_trip():
    """R-1165: rate EQUALS ``multiplier * expectation`` — the comparison is strict."""
    reading = evaluate_burn_rate(
        _hour_samples(), BurnThresholds(expected_per_hour=1.0))

    assert reading is not None
    assert reading.tripped is False
    assert reading.rate == 3.0
    assert reading.expectation == 1.0


# ── to_json ──────────────────────────────────────────────────────────────────


def test_to_json_returns_exactly_the_ten_keys():
    reading = BurnReading(
        tripped=True, basis=BASIS_TRAILING_BASELINE, rate_unit=RATE_UNIT_PER_SAMPLE,
        rate=1.0, expectation=1.0, multiplier=1.0, window_samples=1,
        baseline_samples=1, window_spend=1.0, since_label=1)

    assert set(reading.to_json().keys()) == {
        "tripped", "basis", "rate_unit", "rate", "expectation", "multiplier",
        "window_samples", "baseline_samples", "window_spend", "since_label"}


# ── no clock read ───────────────────────────────────────────────────────────

_CLOCK_CALL_NAMES = frozenset({"now", "utcnow", "today", "time", "monotonic"})


def _called_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def test_the_module_reads_no_clock():
    text = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(MODULE_PATH))
    calls = {_called_name(node) for node in ast.walk(tree) if isinstance(node, ast.Call)}

    assert not calls & _CLOCK_CALL_NAMES


# ── agreement with the watchdog's own trailing tripwire ────────────────────

#: (case id, token sequence — None marks an unmeasured sample). Fixed window,
#: min_samples and multiplier below, same as the watchdog's own call.
_AGREEMENT_CASES = [
    ("trips", (100, 100, 100, 100, 100, 400, 400, 400)),
    ("steady_no_trip", (5000,) * 10),
    ("below_threshold", (100, 100)),
    ("trips_with_unmeasured",
     (None, 100, None, 100, None, 100, None, 100, None, 100,
      None, 400, None, 400, None, 400)),
    ("zero_baseline", (100, 100, 100)),
]


@pytest.mark.parametrize(
    "tokens", [case[1] for case in _AGREEMENT_CASES],
    ids=[case[0] for case in _AGREEMENT_CASES])
def test_the_trailing_basis_agrees_with_the_watchdogs_own_tripwire(tokens):
    entries = [_entry(i, tokens=t) for i, t in enumerate(tokens, start=1)]
    # ``amount`` comes from the watchdog's own accessor, not the raw token
    # value, so a change to what counts as measured is caught here too.
    samples = [BurnSample(amount=measured_tokens(entry), label=entry["iteration"])
               for entry in entries]
    thresholds = BurnThresholds(window=3, min_samples=0, multiplier=3.0)

    trip = evaluate_burn_anomaly(entries, window=3, min_samples=0, multiplier=3.0)
    reading = evaluate_burn_rate(samples, thresholds)

    assert (trip is None) == (reading is None or not reading.tripped)
    if trip is not None:
        assert reading.rate == trip.numbers["window_mean"]
        assert reading.expectation == trip.numbers["baseline_mean"]
        assert reading.baseline_samples == trip.numbers["baseline_samples"]
        assert reading.since_label == trip.since_iteration


#: R-1165: the first agreement table runs every case with ``min_samples=0``,
#: so the watchdog's own default minimum, 5, is never exercised, and its
#: ``zero_baseline`` case has an EMPTY baseline rather than one whose amounts
#: are zero. This table runs at the watchdog's real default minimum and adds
#: a zero-valued baseline followed by a positive window, plus the equality
#: boundary both sides must refuse to trip on.
_AGREEMENT_BOUNDARY_CASES = [
    ("trips_at_the_window_floor", (100, 100, 100, 100, 100, 400, 400, 400)),
    ("too_few_samples_returns_none", (100, 100, 100, 100, 100, 400, 400)),
    ("zero_valued_baseline_trips_on_any_positive_window",
     (0, 0, 0, 0, 0, 100, 100, 100)),
    ("the_equality_boundary_does_not_trip", (100, 100, 100, 100, 100, 300, 300, 300)),
]


@pytest.mark.parametrize(
    "tokens", [case[1] for case in _AGREEMENT_BOUNDARY_CASES],
    ids=[case[0] for case in _AGREEMENT_BOUNDARY_CASES])
def test_the_trailing_basis_agrees_with_the_watchdog_at_a_real_minimum(tokens):
    entries = [_entry(i, tokens=t) for i, t in enumerate(tokens, start=1)]
    samples = [BurnSample(amount=measured_tokens(entry), label=entry["iteration"])
               for entry in entries]
    thresholds = BurnThresholds(window=3, min_samples=5, multiplier=3.0)

    trip = evaluate_burn_anomaly(entries, window=3, min_samples=5, multiplier=3.0)
    reading = evaluate_burn_rate(samples, thresholds)

    assert (trip is None) == (reading is None or not reading.tripped)
    if trip is not None:
        assert reading.rate == trip.numbers["window_mean"]
        assert reading.expectation == trip.numbers["baseline_mean"]
        assert reading.baseline_samples == trip.numbers["baseline_samples"]
        assert reading.since_label == trip.since_iteration
