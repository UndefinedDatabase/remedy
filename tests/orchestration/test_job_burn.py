"""F116 T002, first part — the job burn monitor's tests (DECISION F116 D3).

One test function per behaviour. Fixtures are built IN-PROCESS — a small
permissive config double and plain dicts, no JSONL file, no disk, no
conftest, exactly as ``test_watchdog.py`` and ``test_burn_detector.py`` build
their own.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from packages.orchestration.burn_detector import (
    BASIS_TRAILING_BASELINE,
    RATE_UNIT_PER_SAMPLE,
    BurnReading,
    BurnSample,
    BurnThresholds,
    evaluate_burn_rate,
)
from packages.orchestration.job_burn import (
    CONFIG_KEY_JOB_BURN_EXPECTED_TOKENS_PER_HOUR,
    CONFIG_KEY_JOB_BURN_MIN_SAMPLES,
    CONFIG_KEY_JOB_BURN_MIN_SPEND_TOKENS,
    CONFIG_KEY_JOB_BURN_MULTIPLIER,
    CONFIG_KEY_JOB_BURN_WINDOW,
    JOB_BURN_UNIT,
    JobBurnMonitor,
    job_burn_record,
    job_burn_thresholds_from_config,
)

_AT = datetime(2026, 9, 1, tzinfo=timezone.utc)


class _FakeConfig:
    """A permissive config double: ``values`` wins, everything else is ``None``."""

    def __init__(self, values: dict[str, Any]):
        self._values = values

    def get(self, key: str) -> Any:
        return self._values.get(key)


def _usage(amount: int) -> dict[str, int]:
    """The usage dict shape a provider call reports, all of it input tokens."""
    return {"input_tokens": amount, "output_tokens": 0}


# ── the resolver ─────────────────────────────────────────────────────────────


def test_resolver_with_no_override_returns_the_defaults():
    thresholds = job_burn_thresholds_from_config(_FakeConfig({}))

    assert thresholds == BurnThresholds(
        window=3, min_samples=5, multiplier=3.0, min_spend=20000.0,
        expected_per_hour=None)


def test_resolver_given_other_values_for_all_five_keys_returns_those():
    config = _FakeConfig({
        CONFIG_KEY_JOB_BURN_WINDOW: 7,
        CONFIG_KEY_JOB_BURN_MIN_SAMPLES: 2,
        CONFIG_KEY_JOB_BURN_MULTIPLIER: 5.0,
        CONFIG_KEY_JOB_BURN_MIN_SPEND_TOKENS: 999,
        CONFIG_KEY_JOB_BURN_EXPECTED_TOKENS_PER_HOUR: 42.0,
    })

    thresholds = job_burn_thresholds_from_config(config)

    assert thresholds == BurnThresholds(
        window=7, min_samples=2, multiplier=5.0, min_spend=999.0,
        expected_per_hour=42.0)


# ── record_call ──────────────────────────────────────────────────────────────


def test_record_call_sums_input_and_output_tokens_and_labels_by_position():
    monitor = JobBurnMonitor(BurnThresholds())

    monitor.record_call({"input_tokens": 1000, "output_tokens": 500}, at=_AT)
    monitor.record_call({"input_tokens": 1000, "output_tokens": 500}, at=_AT)

    assert monitor._samples[0] == BurnSample(amount=1500.0, at=_AT, label=1)
    assert monitor._samples[1].label == 2


def test_unmeasured_usage_records_a_sample_with_no_amount():
    monitor = JobBurnMonitor(BurnThresholds())

    for usage in (None, "not-a-dict", {"input_tokens": "100"},
                  {"input_tokens": True}):
        monitor.record_call(usage, at=_AT)

    assert [s.amount for s in monitor._samples] == [None, None, None, None]


def test_usage_missing_output_tokens_records_the_input_tokens_alone():
    monitor = JobBurnMonitor(BurnThresholds())

    monitor.record_call({"input_tokens": 700}, at=_AT)

    assert monitor._samples[0].amount == 700.0


# ── reading ──────────────────────────────────────────────────────────────────


def test_reading_equals_evaluate_burn_rate_over_the_recorded_samples():
    thresholds = BurnThresholds(window=3, min_samples=5, multiplier=3.0)
    monitor = JobBurnMonitor(thresholds)
    amounts = [100] * 5 + [400] * 3
    for amount in amounts:
        monitor.record_call(_usage(amount), at=_AT)

    expected = evaluate_burn_rate(
        [BurnSample(amount=float(a), at=_AT, label=i)
         for i, a in enumerate(amounts, start=1)],
        thresholds)

    assert monitor.reading() == expected


def test_default_thresholds_trip_when_the_window_clears_the_floor():
    thresholds = job_burn_thresholds_from_config(_FakeConfig({}))
    monitor = JobBurnMonitor(thresholds)
    for amount in [1500] * 5 + [15000] * 3:
        monitor.record_call(_usage(amount), at=_AT)

    reading = monitor.reading()

    assert reading is not None
    assert reading.tripped is True


def test_default_thresholds_do_not_trip_below_the_spend_floor():
    thresholds = job_burn_thresholds_from_config(_FakeConfig({}))
    monitor = JobBurnMonitor(thresholds)
    for amount in [100] * 5 + [1000] * 3:
        monitor.record_call(_usage(amount), at=_AT)

    reading = monitor.reading()

    assert reading is not None
    assert reading.tripped is False


def test_default_thresholds_return_none_under_seven_calls():
    thresholds = job_burn_thresholds_from_config(_FakeConfig({}))
    monitor = JobBurnMonitor(thresholds)
    for _ in range(7):
        monitor.record_call(_usage(100), at=_AT)

    assert monitor.reading() is None


# ── job_burn_record ───────────────────────────────────────────────────────────


def test_job_burn_record_returns_the_readings_keys_plus_unit():
    reading = BurnReading(
        tripped=True, basis=BASIS_TRAILING_BASELINE, rate_unit=RATE_UNIT_PER_SAMPLE,
        rate=1.0, expectation=1.0, multiplier=1.0, window_samples=1,
        baseline_samples=1, window_spend=1.0, since_label=1)

    record = job_burn_record(reading)

    assert set(record.keys()) == {
        "tripped", "basis", "rate_unit", "rate", "expectation", "multiplier",
        "window_samples", "baseline_samples", "window_spend", "since_label", "unit"}
    assert record["unit"] == JOB_BURN_UNIT == "tokens"
