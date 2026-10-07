"""F116 T002, first part — the job burn monitor's tests (DECISION F116 D3).

One test function per behaviour. Fixtures are built IN-PROCESS — a small
permissive config double and plain dicts, no JSONL file, no disk, no
conftest, exactly as ``test_watchdog.py`` and ``test_burn_detector.py`` build
their own.
"""
from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any

from packages.orchestration.burn_detector import (
    BASIS_TRAILING_BASELINE,
    RATE_UNIT_PER_HOUR,
    RATE_UNIT_PER_SAMPLE,
    BurnReading,
    BurnSample,
    BurnThresholds,
    evaluate_burn_rate,
)
from packages.orchestration.job_burn import (
    BURN_DECISION_MARKER,
    BURN_PAUSE_SOURCE,
    CONFIG_KEY_JOB_BURN_EXPECTED_TOKENS_PER_HOUR,
    CONFIG_KEY_JOB_BURN_MIN_SAMPLES,
    CONFIG_KEY_JOB_BURN_MIN_SPEND_TOKENS,
    CONFIG_KEY_JOB_BURN_MULTIPLIER,
    CONFIG_KEY_JOB_BURN_WINDOW,
    JOB_BURN_UNIT,
    JobBurnMonitor,
    job_approved_unattended,
    job_burn_record,
    job_burn_sentence,
    job_burn_thresholds_from_config,
)
from packages.orchestration.job_plan import AUTO_APPROVAL_MODE
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PAUSED,
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


def _run_burn_job(repo, *, builder_name, builder_provider, reviewer_provider,
                  prepare=None):
    """A real, SINGLE, un-capped `run_job` over the two-task job above.

    As `_run_and_mirror` (`tests/orchestration/test_job_digest.py`) runs one,
    with `measured=True`, `runs=1`, `mirror=False`, but with no `max_tasks`
    limit, so both tasks' four provider calls land inside this ONE `run_job`
    call — the shape the trip-persistence behaviour needs: the fourth call's
    own safe-point reading must see the third call's trip already recorded.
    *prepare*, when given, is called with the parsed plan before it is saved.
    """
    from packages.orchestration.pingpong_job import (
        load_job_plan,
        parse_job_file,
        run_job,
        save_job_plan,
    )

    plan = parse_job_file(_BURN_TWO_TASK_JOB, str(repo))
    if prepare is not None:
        prepare(plan)
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
    # D5: an attended job only records the warning and runs to its end.
    assert job.state == JOB_COMPLETED


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


class _DiskReadingProvider(_BurnSequenceProvider):
    """A burn-sequence stand-in that, when its FOURTH call starts, reads the job
    back from disk and keeps the ``burn_reading`` it finds there (R-1168)."""

    def __init__(self, *args: Any, job_id_holder: list[str], seen: list[Any],
                 **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._job_id_holder = job_id_holder
        self._seen = seen

    def _read_disk_at_fourth_call(self) -> None:
        from packages.orchestration.pingpong_job import load_job_plan

        if self._counter[0] == 3:
            self._seen.append(load_job_plan(self._job_id_holder[0]).burn_reading)

    def build(self, prompt, **kwargs):
        self._read_disk_at_fourth_call()
        return super().build(prompt, **kwargs)

    def review(self, prompt, **kwargs):
        self._read_disk_at_fourth_call()
        return super().review(prompt, **kwargs)


def test_the_trip_is_on_disk_when_the_fourth_provider_call_starts(tmp_path, monkeypatch):
    _patch_burn_thresholds(
        monkeypatch,
        BurnThresholds(window=1, min_samples=2, multiplier=3.0, min_spend=0.0))
    repo = _burn_job_repo(tmp_path)
    counter = [0]
    holder: list[str] = []
    seen: list[Any] = []
    sequence = [1500, 1500, 15000, 1500]
    kwargs = dict(pass_on_round=1, fail_on_round=99, job_id_holder=holder, seen=seen)
    builder = _DiskReadingProvider(sequence, counter, **kwargs)
    reviewer = _DiskReadingProvider(sequence, counter, **kwargs)

    job = _run_burn_job(
        repo, builder_name=_BurnSequenceProvider.PROVIDER_NAME,
        builder_provider=builder, reviewer_provider=reviewer,
        prepare=lambda plan: holder.append(plan.job_id))

    assert len(seen) == 1
    assert seen[0] is not None
    assert seen[0] == job.burn_reading


# ── job_approved_unattended ───────────────────────────────────────────────────


def test_job_approved_unattended_is_true_for_the_auto_approval_audit():
    job = SimpleNamespace(task_plan={"_approval_audit": {"mode": AUTO_APPROVAL_MODE}})

    assert job_approved_unattended(job) is True


def test_job_approved_unattended_is_false_for_every_other_plan_shape():
    for task_plan in (
        None,
        {},
        {"_approval_audit": {"mode": "interactive"}},
        {"_approval_audit": "auto_yes"},
    ):
        assert job_approved_unattended(SimpleNamespace(task_plan=task_plan)) is False


# ── job_burn_sentence ─────────────────────────────────────────────────────────


def test_job_burn_sentence_for_a_per_sample_record():
    record = {
        "rate_unit": RATE_UNIT_PER_SAMPLE, "window_samples": 1, "rate": 15000.0,
        "expectation": 1500.0, "multiplier": 3.0, "since_label": 3}

    assert job_burn_sentence(record) == (
        "The last 1 provider calls spent 15000.0 tokens each on average, more "
        "than 3 times the 1500.0 tokens per call this job spent before them "
        "(from call 3 on).")


def test_job_burn_sentence_for_a_per_hour_record():
    record = {
        "rate_unit": RATE_UNIT_PER_HOUR, "window_samples": 5, "rate": 90000.0,
        "expectation": 30000.0, "multiplier": 2.5, "since_label": 4}

    assert job_burn_sentence(record) == (
        "The last 5 provider calls spent 90000.0 tokens per hour, more than "
        "2.5 times the 30000.0 tokens per hour set in configuration "
        "(from call 4 on).")


# ── the unattended run: a trip pauses the job with one decision ──────────────


def _approve_unattended(plan) -> None:
    plan.task_plan = {"_approval_audit": {"mode": AUTO_APPROVAL_MODE}}


def _run_unattended_spike(tmp_path, monkeypatch, *, prepare=None):
    """The round 4 spike run over an unattended job; returns the reloaded job
    and the shared provider-call counter."""
    _patch_burn_thresholds(
        monkeypatch,
        BurnThresholds(window=1, min_samples=2, multiplier=3.0, min_spend=0.0))
    repo = _burn_job_repo(tmp_path)
    counter = [0]
    sequence = [1500, 1500, 15000, 1500]
    builder = _BurnSequenceProvider(sequence, counter, pass_on_round=1, fail_on_round=99)
    reviewer = _BurnSequenceProvider(sequence, counter, pass_on_round=1, fail_on_round=99)

    def _prepare(plan) -> None:
        _approve_unattended(plan)
        if prepare is not None:
            prepare(plan)

    job = _run_burn_job(
        repo, builder_name=_BurnSequenceProvider.PROVIDER_NAME,
        builder_provider=builder, reviewer_provider=reviewer, prepare=_prepare)
    return job, counter


def test_an_unattended_trip_pauses_the_job_before_the_next_call(tmp_path, monkeypatch):
    from packages.orchestration.escalation import open_task_decisions

    job, counter = _run_unattended_spike(tmp_path, monkeypatch)

    assert job.state == JOB_PAUSED
    assert job.pause["source"] == BURN_PAUSE_SOURCE == "burn_alarm"
    assert job.pause["reason"].startswith("burn_alarm: ")
    assert counter[0] == 3
    open_decisions = open_task_decisions(job)
    assert len(open_decisions) == 1
    decision = open_decisions[0]
    assert decision["question"].startswith(BURN_DECISION_MARKER + " ")
    assert decision["options"] == ["resume", "abandon"]
    assert decision["safe_default"] == ""
    assert decision["task_id"] == job.tasks[1].task_id


def test_a_second_trip_updates_the_open_burn_decision_in_place(tmp_path, monkeypatch):
    from packages.orchestration.escalation import (
        enqueue_task_decision,
        open_task_decisions,
    )

    def _seed_open_decision(plan) -> None:
        enqueue_task_decision(
            plan, task_id=plan.tasks[0].task_id,
            question=f"{BURN_DECISION_MARKER} an older sentence",
            options=("resume", "abandon"), safe_default="", impact="older",
            now=_AT)

    job, _counter = _run_unattended_spike(
        tmp_path, monkeypatch, prepare=_seed_open_decision)

    open_decisions = [
        r for r in open_task_decisions(job)
        if r["question"].startswith(BURN_DECISION_MARKER)]
    assert len(open_decisions) == 1
    assert open_decisions[0]["question"] == (
        f"{BURN_DECISION_MARKER} {job_burn_sentence(job.burn_reading)}")
    # R-1171: the re-trip replaces the seeded impact as well as the question.
    assert open_decisions[0]["impact"] == (
        f"job {job.job_id} is paused until this is answered; continue it "
        f"with `remedy job unpause {job.job_id}`")


def test_an_unattended_trip_blocks_the_job_when_the_pause_request_fails(
        tmp_path, monkeypatch):
    from packages.orchestration import pause_control

    def _refuse(*args, **kwargs):
        raise pause_control.PauseControlError("control area unusable")

    monkeypatch.setattr(pause_control, "request_pause", _refuse)

    job, _counter = _run_unattended_spike(tmp_path, monkeypatch)

    assert job.state == JOB_BLOCKED
    assert job.burn_reading is not None
    assert job.burn_reading["tripped"] is True
