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
from packages.orchestration.pingpong_provider import FakeProvider

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


# ── the resolver reads the REGISTRY, not a hardcoded fallback ────────────────


class _RegisteredDefaultsConfig:
    """Stands in for the real config, answering each key's OWN registered
    default (``get_key_spec(key).default``) rather than a test-chosen value —
    the registry and the resolver's fallback must agree (DECISION F116 D4
    (5))."""

    def get(self, key: str) -> Any:
        from packages.orchestration.config import get_key_spec
        spec = get_key_spec(key)
        return spec.default if spec is not None else None


def test_the_registered_defaults_through_the_resolver_match_the_fallback():
    thresholds = job_burn_thresholds_from_config(_RegisteredDefaultsConfig())

    assert thresholds == BurnThresholds(
        window=3, min_samples=5, multiplier=3.0, min_spend=20000.0,
        expected_per_hour=None)


# ── run_job wiring (DECISION F116 D4): the monitor reads every counted call ──


_BURN_TWO_TASK_JOB = """\
# Job: Burn monitor

## Task 1
Add a greeting.

Acceptance:
- file exists

## Task 2
Add a farewell.

Acceptance:
- file exists
"""


class _BurnSequenceProvider(FakeProvider):
    """A FakeProvider whose counted calls report ONE fixed token sequence.

    Builder and reviewer instances share ``counter`` (a one-item list), so
    the sequence reads across BOTH roles in the order `run_job` actually
    calls them — never each role's own separate count, which is what a
    plain per-instance counter would give.
    """

    PROVIDER_NAME = "burn-sequence-stub"

    def __init__(self, sequence: list[int], counter: list[int], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._sequence = sequence
        self._counter = counter

    @property
    def name(self) -> str:
        return self.PROVIDER_NAME

    def _next_usage(self) -> dict[str, int]:
        amount = self._sequence[self._counter[0]]
        self._counter[0] += 1
        return {"input_tokens": amount, "output_tokens": 0}

    def build(self, prompt, **kwargs):
        out = super().build(prompt, **kwargs)
        out.usage_actuals = self._next_usage()
        return out

    def review(self, prompt, **kwargs):
        out = super().review(prompt, **kwargs)
        out.usage_actuals = self._next_usage()
        return out


def _burn_job_repo(tmp_path):
    """A plain project directory — no git needed, as `demo_repo` in
    `tests/orchestration/test_predictive_budget.py` establishes for a run
    with no money limit and so no ledger-project resolution."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# demo\n")
    return repo


def _run_burn_job(repo, *, builder_name, builder_provider, reviewer_provider):
    """A real, SINGLE, un-capped `run_job` over the two-task job above.

    As `_run_and_mirror` (`tests/orchestration/test_job_digest.py`) runs one,
    with `measured=True`, `runs=1`, `mirror=False`, but with no `max_tasks`
    limit, so both tasks' four provider calls land inside this ONE `run_job`
    call — the shape the trip-persistence behaviour needs: the fourth call's
    own safe-point reading must see the third call's trip already recorded.
    """
    from packages.orchestration.pingpong_job import (
        load_job_plan,
        parse_job_file,
        run_job,
        save_job_plan,
    )

    plan = parse_job_file(_BURN_TWO_TASK_JOB, str(repo))
    save_job_plan(plan)
    run_job(
        plan.job_id,
        builder_name=builder_name, reviewer_name=builder_name,
        builder_provider=builder_provider, reviewer_provider=reviewer_provider,
        repair_rounds=0,
    )
    return load_job_plan(plan.job_id)


def _patch_burn_thresholds(monkeypatch, thresholds: BurnThresholds) -> None:
    """Replaces `job_burn.job_burn_thresholds_from_config` for the test, as
    DECISION F116 D4 (5)'s test plan orders — `run_job`'s local import picks
    up the replacement at call time."""
    from packages.orchestration import job_burn as _job_burn_module
    monkeypatch.setattr(
        _job_burn_module, "job_burn_thresholds_from_config",
        lambda *a, **kw: thresholds)


def test_run_job_keeps_the_trip_read_before_the_fourth_call(tmp_path, monkeypatch):
    _patch_burn_thresholds(
        monkeypatch,
        BurnThresholds(window=1, min_samples=2, multiplier=3.0, min_spend=0.0))
    repo = _burn_job_repo(tmp_path)
    counter = [0]
    sequence = [1500, 1500, 15000, 1500]
    builder = _BurnSequenceProvider(sequence, counter, pass_on_round=1, fail_on_round=99)
    reviewer = _BurnSequenceProvider(sequence, counter, pass_on_round=1, fail_on_round=99)

    job = _run_burn_job(
        repo, builder_name=_BurnSequenceProvider.PROVIDER_NAME,
        builder_provider=builder, reviewer_provider=reviewer)

    # The third call (15000 against a baseline of two calls at 1500) trips;
    # the fourth call (1500) pulls the window off the spike and no longer
    # trips, but the job keeps the earlier, tripped reading as its record.
    assert job.burn_reading is not None
    assert job.burn_reading["tripped"] is True
    assert job.burn_reading["rate"] == 15000.0
    assert job.burn_reading["expectation"] == 1500.0
    assert job.burn_reading["since_label"] == 3
    assert job.burn_reading["basis"] == BASIS_TRAILING_BASELINE
    assert job.burn_reading["unit"] == JOB_BURN_UNIT


def test_run_job_leaves_burn_reading_none_when_nothing_trips(tmp_path, monkeypatch):
    _patch_burn_thresholds(
        monkeypatch,
        BurnThresholds(window=1, min_samples=2, multiplier=3.0, min_spend=0.0))
    repo = _burn_job_repo(tmp_path)
    counter = [0]
    sequence = [15000, 15000, 15000, 15000]
    builder = _BurnSequenceProvider(sequence, counter, pass_on_round=1, fail_on_round=99)
    reviewer = _BurnSequenceProvider(sequence, counter, pass_on_round=1, fail_on_round=99)

    job = _run_burn_job(
        repo, builder_name=_BurnSequenceProvider.PROVIDER_NAME,
        builder_provider=builder, reviewer_provider=reviewer)

    assert job.burn_reading is None


def test_run_job_leaves_burn_reading_none_for_a_fake_provider(tmp_path, monkeypatch):
    _patch_burn_thresholds(
        monkeypatch,
        BurnThresholds(window=1, min_samples=2, multiplier=3.0, min_spend=0.0))
    repo = _burn_job_repo(tmp_path)

    # "fake" is never counted at all (`_on_provider_call`'s early return), so
    # the monitor never sees a sample whatever its thresholds read.
    job = _run_burn_job(
        repo, builder_name="fake",
        builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
        reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99))

    assert job.burn_reading is None


def test_run_job_leaves_burn_reading_none_and_logs_one_error_when_the_resolver_raises(
        tmp_path, monkeypatch, caplog):
    import logging

    from packages.orchestration import job_burn as _job_burn_module

    def _raise(*a, **kw):
        raise ValueError("REMEDY_JOB_BURN_WINDOW=abc")

    monkeypatch.setattr(_job_burn_module, "job_burn_thresholds_from_config", _raise)
    repo = _burn_job_repo(tmp_path)
    counter = [0]
    sequence = [1500, 1500, 15000, 1500]
    builder = _BurnSequenceProvider(sequence, counter, pass_on_round=1, fail_on_round=99)
    reviewer = _BurnSequenceProvider(sequence, counter, pass_on_round=1, fail_on_round=99)

    with caplog.at_level(logging.ERROR, logger="packages.orchestration.pingpong_job"):
        job = _run_burn_job(
            repo, builder_name=_BurnSequenceProvider.PROVIDER_NAME,
            builder_provider=builder, reviewer_provider=reviewer)

    assert job.burn_reading is None
    records = [
        r for r in caplog.records
        if r.levelno == logging.ERROR and "job burn monitor config read FAILED" in r.getMessage()
    ]
    assert len(records) == 1, [r.getMessage() for r in caplog.records]
    assert records[0].exc_info is not None
