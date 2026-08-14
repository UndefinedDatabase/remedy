"""Tests for F057 T001 — signal normalization — and T002 — the governor.

No network and no filesystem beyond the one in-repo fixture; the governor's clock and
sleep are INJECTED FAKES (:class:`FakeClock`), so no test here sleeps for real and none
asserts on wall-clock duration — the fake advances only when the code under test asks
it to. Every positive sample below is either a literal taken from in-repo evidence (the
fixture at tests/orchestration/fixtures/stream/retry_and_error.jsonl, whose two
api_retry reasons are the only rate-limit literals this repo has) or a provider spelling
the module marks as such in its wording table.
"""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest

from packages.orchestration.rate_governor import (
    MAX_RETRY_AFTER_S,
    RATE_ACQUIRE_DEADLINE_EXCEEDED,
    RATE_ACQUIRE_GRANTED,
    RATE_ACQUIRE_STOPPED,
    RATE_LIMIT_COOLDOWN_BASE_S,
    RATE_LIMIT_COOLDOWN_MAX_S,
    RATE_LIMIT_REASON_OVERLOADED,
    RATE_LIMIT_REASON_QUOTA_EXCEEDED,
    RATE_LIMIT_REASON_RATE_LIMITED,
    RATE_LIMIT_REASON_THROTTLED,
    RATE_LIMIT_SIGNAL_VERSION,
    RATE_LIMIT_WAIT_VERSION,
    RATE_SIGNAL_RAW_MAX_CHARS,
    RATE_SIGNAL_SOURCE_API_RETRY,
    RATE_SIGNAL_SOURCE_PROVIDER_ERROR,
    RATE_SIGNAL_SOURCE_RETRY_REASON,
    ProviderRateGovernor,
    RateLimitSignal,
    RateLimitWaitEvent,
    classify_rate_limit_reason,
    is_rate_limit_error,
    normalize_rate_limit_signal,
    parse_retry_after_seconds,
    read_retry_reason_signals,
    read_run_event_signals,
)
from packages.orchestration.stream_evidence import (
    EVENT_API_RETRY,
    EVENT_PROVIDER_ERROR,
    EVENT_TOKEN_USAGE,
    normalize_stream_object,
)

#: The only rate-limit literals in the repository, read from the fixture rather than
#: retyped, so the test fails if the fixture ever stops carrying them.
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "stream" / "retry_and_error.jsonl"


def _fixture_api_retry_reasons() -> list[str]:
    reasons: list[str] = []
    for line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj.get("type") == "api_retry":
            reasons.append(str(obj.get("reason") or ""))
    return reasons


# ---------------------------------------------------------------------------
# The step-1 inventory samples, by their real shape
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_fixture_still_carries_both_rate_limit_literals():
    assert _fixture_api_retry_reasons() == ["overloaded_error", "rate_limit"]


@pytest.mark.unit
@pytest.mark.parametrize(
    ("reason", "expected"),
    [
        ("overloaded_error", RATE_LIMIT_REASON_OVERLOADED),
        ("rate_limit", RATE_LIMIT_REASON_RATE_LIMITED),
    ],
)
def test_in_repo_fixture_reasons_classify(reason, expected):
    assert reason in _fixture_api_retry_reasons()
    assert is_rate_limit_error(reason) is True
    assert classify_rate_limit_reason(reason) == expected


@pytest.mark.unit
def test_inventory_shape_1_api_retry_event_from_normalize_stream_object():
    """Inventory 1: the api_retry event shape, built by the real normalizer."""
    events = normalize_stream_object({"type": "api_retry", "attempt": 1, "reason": "overloaded_error"})
    assert events == [{"event_type": EVENT_API_RETRY, "attempt": 1, "reason": "overloaded_error"}]

    signals = read_run_event_signals(events, provider="claude")
    assert [s.reason for s in signals] == [RATE_LIMIT_REASON_OVERLOADED]
    assert signals[0].source == RATE_SIGNAL_SOURCE_API_RETRY
    assert signals[0].raw == "overloaded_error"
    assert signals[0].retry_after_s is None


@pytest.mark.unit
def test_inventory_shape_2_provider_error_event_from_normalize_stream_object():
    """Inventory 2: the provider_error event shape, built by the real normalizer."""
    events = normalize_stream_object({"type": "error", "error": "HTTP 429 Too Many Requests"})
    assert events == [{"event_type": EVENT_PROVIDER_ERROR, "error": "HTTP 429 Too Many Requests"}]

    signals = read_run_event_signals(events, provider="codex")
    assert [s.reason for s in signals] == [RATE_LIMIT_REASON_RATE_LIMITED]
    assert signals[0].source == RATE_SIGNAL_SOURCE_PROVIDER_ERROR
    assert signals[0].provider == "codex"


@pytest.mark.unit
def test_inventory_shape_3_retry_reason_string():
    """Inventory 3: pingpong_loop.py:2211 builds "{role}:attempt{n}:{error}"."""
    role, attempt, error = "builder", 1, "rate_limit: slow down"
    entry = f"{role}:attempt{attempt + 1}:{error[:120]}"

    signals = read_retry_reason_signals([entry], provider="claude")
    assert len(signals) == 1
    assert signals[0].reason == RATE_LIMIT_REASON_RATE_LIMITED
    assert signals[0].source == RATE_SIGNAL_SOURCE_RETRY_REASON
    # The role/attempt prefix stays on raw: it is evidence, not noise.
    assert signals[0].raw == "builder:attempt2:rate_limit: slow down"


@pytest.mark.unit
def test_inventory_shape_4_provider_error_from_the_fixture_line_is_not_a_rate_limit():
    """The fixture's error line is a connection reset, which is somebody else's predicate."""
    events = normalize_stream_object({"type": "error", "error": "upstream connection reset"})
    assert read_run_event_signals(events, provider="claude") == []


# ---------------------------------------------------------------------------
# Negatives — the strings the existing transport predicates own
# ---------------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    "text",
    [
        "claude CLI timed out after 600s",          # is_timeout_error owns this
        "TimeoutExpired",                            # is_timeout_error owns this
        "process exited with code 1",                # is_nonzero_exit_error owns this
        "nonzero exit status",                       # is_nonzero_exit_error owns this
        "connection refused",                        # is_provider_connection_error owns this
        "no such file or directory",                 # is_provider_unavailable_error owns this
        "too many open files",                       # is_io_failure_error owns this
        "value must be in [0..4294967295]",          # contains 429, is not a rate limit
        "review rejected: needs_repair",
    ],
)
def test_non_rate_limit_strings_are_rejected(text):
    assert is_rate_limit_error(text) is False
    assert classify_rate_limit_reason(text) is None


@pytest.mark.unit
@pytest.mark.parametrize("text", [None, "", "   "])
def test_empty_input_is_not_a_rate_limit(text):
    assert is_rate_limit_error(text) is False
    assert classify_rate_limit_reason(text) is None
    assert parse_retry_after_seconds(text) is None


@pytest.mark.unit
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("RateLimitError: please retry", RATE_LIMIT_REASON_RATE_LIMITED),
        ("rate limit exceeded for this key", RATE_LIMIT_REASON_RATE_LIMITED),
        ("rate-limited by upstream", RATE_LIMIT_REASON_RATE_LIMITED),
        ("429 Too Many Requests", RATE_LIMIT_REASON_RATE_LIMITED),
        ("quota exceeded for this month", RATE_LIMIT_REASON_QUOTA_EXCEEDED),
        ("insufficient_quota", RATE_LIMIT_REASON_QUOTA_EXCEEDED),
        ("request was throttled", RATE_LIMIT_REASON_THROTTLED),
        ("the server is overloaded", RATE_LIMIT_REASON_OVERLOADED),
    ],
)
def test_provider_vocabulary_spellings_classify(text, expected):
    assert is_rate_limit_error(text) is True
    assert classify_rate_limit_reason(text) == expected


# ---------------------------------------------------------------------------
# parse_retry_after_seconds
# ---------------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("rate_limit; retry-after: 30", 30.0),
        ("rate_limit retry_after=12.5", 12.5),
        ("rate limit, Retry-After 45s", 45.0),
        ('overloaded {"retry_after": 7}', 7.0),
        ("rate_limit; retry-after: 0", 0.0),
    ],
)
def test_retry_after_present_is_parsed(text, expected):
    assert parse_retry_after_seconds(text) == pytest.approx(expected)


@pytest.mark.unit
def test_retry_after_absent_is_none_not_zero():
    value = parse_retry_after_seconds("rate_limit with no hint at all")
    assert value is None
    assert value != 0


@pytest.mark.unit
@pytest.mark.parametrize(
    "text",
    [
        "rate_limit; retry-after: -5",
        f"rate_limit; retry-after: {int(MAX_RETRY_AFTER_S) + 1}",
        "rate_limit; retry-after: 999999",
    ],
)
def test_retry_after_out_of_bounds_is_rejected(text):
    assert parse_retry_after_seconds(text) is None


@pytest.mark.unit
def test_retry_after_at_the_bound_is_accepted():
    assert parse_retry_after_seconds(f"rate_limit; retry-after: {int(MAX_RETRY_AFTER_S)}") == MAX_RETRY_AFTER_S


# ---------------------------------------------------------------------------
# normalize_rate_limit_signal
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_normalize_returns_none_for_non_rate_limit_text():
    assert normalize_rate_limit_signal(
        "claude CLI timed out after 600s",
        provider="claude",
        source=RATE_SIGNAL_SOURCE_API_RETRY,
    ) is None


@pytest.mark.unit
def test_normalize_bounds_the_raw_text():
    long_text = "rate_limit " + ("x" * (RATE_SIGNAL_RAW_MAX_CHARS * 2))
    signal = normalize_rate_limit_signal(long_text, provider="claude", source=RATE_SIGNAL_SOURCE_API_RETRY)
    assert signal is not None
    assert len(signal.raw) == RATE_SIGNAL_RAW_MAX_CHARS


# ---------------------------------------------------------------------------
# Readers, end to end on realistic mixed input
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_read_run_event_signals_on_a_mixed_event_list():
    events = [
        {"event_type": EVENT_API_RETRY, "attempt": 1, "reason": "overloaded_error"},
        {"event_type": EVENT_API_RETRY, "attempt": 2, "reason": "rate_limit"},
        {"event_type": EVENT_API_RETRY, "attempt": 3, "reason": "claude CLI timed out after 600s"},
        {"event_type": EVENT_PROVIDER_ERROR, "error": "upstream connection reset"},
        {"event_type": EVENT_PROVIDER_ERROR, "error": "429 Too Many Requests; retry-after: 20"},
        {"event_type": EVENT_TOKEN_USAGE, "input_tokens": 10, "output_tokens": 1},
        "not a mapping",
        {"event_type": EVENT_API_RETRY, "attempt": 4},  # no reason key at all
    ]

    signals = read_run_event_signals(events, provider="claude")

    assert [(s.reason, s.source, s.retry_after_s) for s in signals] == [
        (RATE_LIMIT_REASON_OVERLOADED, RATE_SIGNAL_SOURCE_API_RETRY, None),
        (RATE_LIMIT_REASON_RATE_LIMITED, RATE_SIGNAL_SOURCE_API_RETRY, None),
        (RATE_LIMIT_REASON_RATE_LIMITED, RATE_SIGNAL_SOURCE_PROVIDER_ERROR, 20.0),
    ]
    assert {s.provider for s in signals} == {"claude"}


@pytest.mark.unit
def test_read_run_event_signals_on_an_empty_list():
    assert read_run_event_signals([], provider="claude") == []


@pytest.mark.unit
def test_read_retry_reason_signals_on_a_mixed_reason_list():
    reasons = [
        "builder:attempt2:claude CLI timed out after 600s",
        "builder:attempt3:rate_limit",
        "reviewer:attempt2:process exited with code 1",
        "reviewer:attempt3:overloaded_error; retry-after: 15",
    ]

    signals = read_retry_reason_signals(reasons, provider="claude")

    assert [(s.reason, s.retry_after_s) for s in signals] == [
        (RATE_LIMIT_REASON_RATE_LIMITED, None),
        (RATE_LIMIT_REASON_OVERLOADED, 15.0),
    ]
    assert {s.source for s in signals} == {RATE_SIGNAL_SOURCE_RETRY_REASON}


@pytest.mark.unit
def test_read_retry_reason_signals_on_an_empty_list():
    assert read_retry_reason_signals([], provider="claude") == []


# ---------------------------------------------------------------------------
# to_json
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_to_json_is_plain_json_types_and_round_trips():
    signal = RateLimitSignal(
        provider="claude",
        reason=RATE_LIMIT_REASON_RATE_LIMITED,
        retry_after_s=20.0,
        source=RATE_SIGNAL_SOURCE_PROVIDER_ERROR,
        raw="429 Too Many Requests; retry-after: 20",
    )

    payload = signal.to_json()
    assert payload == {
        "rate_limit_signal_v": RATE_LIMIT_SIGNAL_VERSION,
        "provider": "claude",
        "reason": RATE_LIMIT_REASON_RATE_LIMITED,
        "retry_after_s": 20.0,
        "source": RATE_SIGNAL_SOURCE_PROVIDER_ERROR,
        "raw": "429 Too Many Requests; retry-after: 20",
    }
    assert json.loads(json.dumps(payload)) == payload


@pytest.mark.unit
def test_to_json_keeps_a_missing_retry_hint_as_null():
    signal = normalize_rate_limit_signal(
        "overloaded_error",
        provider="claude",
        source=RATE_SIGNAL_SOURCE_API_RETRY,
    )
    assert signal is not None
    assert json.loads(json.dumps(signal.to_json()))["retry_after_s"] is None


@pytest.mark.unit
def test_signal_is_frozen():
    signal = RateLimitSignal(provider="claude", reason=RATE_LIMIT_REASON_OVERLOADED)
    with pytest.raises(dataclasses.FrozenInstanceError):
        signal.provider = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# T002 — the governor. Everything below runs on FakeClock; nothing sleeps for real.
# ---------------------------------------------------------------------------


class FakeClock:
    """The INJECTED clock and sleep the governor's tests run on.

    ``sleep`` advances ``now`` instead of blocking and records what it was asked for, so
    a test can assert both how long a wait lasted and that a wait never started at all.
    Remedy deliberately never calls the real clock or the real sleep in this file: a unit
    test that really sleeps buys flakiness and wall-clock assertions a loaded machine
    breaks, so the whole ``time`` module stays out of the test's imports.
    """

    def __init__(self, start_s: float = 0.0) -> None:
        self.now = start_s
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


#: A poll slice chosen so every wait below divides into an exact number of binary-clean
#: slices; the production default is RATE_GOVERNOR_POLL_SLICE_S and is not under test.
TEST_POLL_SLICE_S = 0.25


def _governor(clock: FakeClock) -> ProviderRateGovernor:
    return ProviderRateGovernor(
        monotonic_fn=clock.monotonic,
        sleep_fn=clock.sleep,
        poll_slice_s=TEST_POLL_SLICE_S,
    )


def _limit_signal(
    *,
    provider: str = "claude",
    reason: str = RATE_LIMIT_REASON_RATE_LIMITED,
    retry_after_s: float | None = None,
) -> RateLimitSignal:
    return RateLimitSignal(
        provider=provider,
        reason=reason,
        retry_after_s=retry_after_s,
        source=RATE_SIGNAL_SOURCE_API_RETRY,
        raw="rate_limit",
    )


@pytest.mark.unit
def test_observe_applies_the_providers_retry_after_hint_verbatim():
    clock = FakeClock()
    governor = _governor(clock)
    assert governor.observe(_limit_signal(retry_after_s=7.5)) == 7.5
    assert governor.cooldown_remaining_s("claude") == 7.5


@pytest.mark.unit
def test_observe_without_a_hint_escalates_and_never_passes_the_cap():
    clock = FakeClock()
    governor = _governor(clock)
    applied = [governor.observe(_limit_signal()) for _ in range(9)]
    assert applied[0] == RATE_LIMIT_COOLDOWN_BASE_S
    assert applied[1] == 2.0 * RATE_LIMIT_COOLDOWN_BASE_S
    assert applied[2] == 4.0 * RATE_LIMIT_COOLDOWN_BASE_S
    assert applied[3] == 8.0 * RATE_LIMIT_COOLDOWN_BASE_S
    # streak 7 would be 64.0 uncapped; the cap is what makes it 60.0, and streaks 8 and 9
    # keep it there — the escalation passes the cap and stays under it.
    assert applied[6] == RATE_LIMIT_COOLDOWN_MAX_S
    assert applied[7] == RATE_LIMIT_COOLDOWN_MAX_S
    assert applied[8] == RATE_LIMIT_COOLDOWN_MAX_S
    assert max(applied) <= RATE_LIMIT_COOLDOWN_MAX_S


@pytest.mark.unit
def test_two_providers_hold_independent_cooldowns():
    clock = FakeClock()
    governor = _governor(clock)
    governor.observe(_limit_signal(provider="claude", retry_after_s=5.0))
    assert governor.cooldown_remaining_s("claude") == 5.0
    assert governor.cooldown_remaining_s("codex") == 0.0
    governor.observe(_limit_signal(provider="codex", retry_after_s=2.0))
    assert governor.cooldown_remaining_s("codex") == 2.0
    assert governor.cooldown_remaining_s("claude") == 5.0


@pytest.mark.unit
def test_a_later_signal_never_shortens_a_cooldown_already_running():
    # observe() stores max(existing_deadline, now + duration), so a stray short hint
    # cannot cancel a long wait already under way and let the run hammer the provider.
    clock = FakeClock()
    governor = _governor(clock)
    governor.observe(_limit_signal(retry_after_s=30.0))
    assert governor.cooldown_remaining_s("claude") == 30.0
    # The clock does NOT advance between the two signals: the only thing that can move
    # the stored deadline down is the guard being gone.
    assert governor.observe(_limit_signal(retry_after_s=1.0)) == 1.0
    assert governor.cooldown_remaining_s("claude") == 30.0


@pytest.mark.unit
def test_acquire_on_an_unobserved_provider_grants_without_waiting():
    clock = FakeClock()
    governor = _governor(clock)
    result = governor.acquire("claude", role="architect")
    assert result.outcome == RATE_ACQUIRE_GRANTED
    assert result.granted is True
    assert result.waited_s == 0.0
    assert governor.wait_events() == []
    assert clock.sleeps == []


@pytest.mark.unit
def test_acquire_waits_out_a_cooldown_and_records_exactly_one_event():
    clock = FakeClock()
    governor = _governor(clock)
    governor.observe(_limit_signal(reason=RATE_LIMIT_REASON_OVERLOADED, retry_after_s=1.0))
    result = governor.acquire("claude")
    assert result.outcome == RATE_ACQUIRE_GRANTED
    assert result.waited_s == pytest.approx(1.0)
    assert result.reason == RATE_LIMIT_REASON_OVERLOADED
    assert clock.sleeps == [TEST_POLL_SLICE_S] * 4
    events = governor.wait_events()
    assert len(events) == 1
    assert events[0].provider == "claude"
    assert events[0].waited_s == pytest.approx(1.0)
    assert events[0].reason == RATE_LIMIT_REASON_OVERLOADED
    # wait_events() hands back a copy: clearing it cannot erase the run's evidence.
    events.clear()
    assert len(governor.wait_events()) == 1


@pytest.mark.unit
def test_stop_beats_wait_when_the_run_is_already_stopped():
    clock = FakeClock()
    governor = _governor(clock)
    governor.observe(_limit_signal(retry_after_s=10.0))
    result = governor.acquire("claude", stop_check=lambda: "stopped by operator")
    assert result.outcome == RATE_ACQUIRE_STOPPED
    assert result.granted is False
    assert result.waited_s == 0.0
    assert clock.sleeps == []
    assert clock.now == 0.0
    assert governor.wait_events() == []


@pytest.mark.unit
def test_stop_beats_wait_when_the_stop_arrives_mid_wait():
    clock = FakeClock()
    governor = _governor(clock)
    governor.observe(_limit_signal(retry_after_s=1.0))
    probes: list[int] = []

    def stop_check() -> str | None:
        probes.append(len(probes) + 1)
        return "stopped by operator" if len(probes) > 2 else None

    result = governor.acquire("claude", stop_check=stop_check)
    assert result.outcome == RATE_ACQUIRE_STOPPED
    assert result.waited_s == pytest.approx(TEST_POLL_SLICE_S)
    assert result.waited_s < 1.0
    # The fake clock is the proof: acquire did NOT sleep the cooldown out.
    assert clock.now == pytest.approx(TEST_POLL_SLICE_S)
    assert clock.sleeps == [TEST_POLL_SLICE_S]
    events = governor.wait_events()
    assert len(events) == 1
    assert events[0].waited_s == pytest.approx(TEST_POLL_SLICE_S)


@pytest.mark.unit
def test_a_deadline_expiring_mid_wait_returns_deadline_exceeded():
    clock = FakeClock()
    governor = _governor(clock)
    governor.observe(_limit_signal(retry_after_s=1.0))
    result = governor.acquire("claude", deadline_s=0.5)
    assert result.outcome == RATE_ACQUIRE_DEADLINE_EXCEEDED
    assert result.granted is False
    assert result.waited_s == pytest.approx(0.5)
    assert clock.now == pytest.approx(0.5)
    events = governor.wait_events()
    assert len(events) == 1
    assert events[0].waited_s == pytest.approx(0.5)


@pytest.mark.unit
def test_a_granted_acquire_that_waited_nothing_resets_the_streak():
    clock = FakeClock()
    governor = _governor(clock)
    assert governor.observe(_limit_signal()) == RATE_LIMIT_COOLDOWN_BASE_S
    assert governor.observe(_limit_signal()) == 2.0 * RATE_LIMIT_COOLDOWN_BASE_S
    clock.now = 100.0  # the cooldown elapsed on its own; the provider recovered
    assert governor.acquire("claude").granted is True
    assert governor.wait_events() == []
    assert governor.observe(_limit_signal()) == RATE_LIMIT_COOLDOWN_BASE_S


@pytest.mark.unit
def test_wait_event_to_json_survives_a_json_round_trip():
    event = RateLimitWaitEvent(
        provider="claude",
        waited_s=1.5,
        reason=RATE_LIMIT_REASON_RATE_LIMITED,
    )
    payload = event.to_json()
    assert payload == {
        "rate_limit_wait_v": RATE_LIMIT_WAIT_VERSION,
        "provider": "claude",
        "waited_s": 1.5,
        "reason": RATE_LIMIT_REASON_RATE_LIMITED,
    }
    assert json.loads(json.dumps(payload)) == payload


@pytest.mark.unit
def test_wait_event_is_frozen():
    event = RateLimitWaitEvent(
        provider="claude",
        waited_s=1.5,
        reason=RATE_LIMIT_REASON_RATE_LIMITED,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        event.waited_s = 2.0  # type: ignore[misc]


@pytest.mark.unit
def test_total_waited_s_sums_the_rounds_waits():
    clock = FakeClock()
    governor = _governor(clock)
    governor.observe(_limit_signal(provider="claude", retry_after_s=1.0))
    governor.acquire("claude")
    governor.observe(_limit_signal(provider="codex", retry_after_s=0.5))
    governor.acquire("codex")
    events = governor.wait_events()
    assert len(events) == 2
    assert governor.total_waited_s() == pytest.approx(1.5)
    assert governor.total_waited_s() == pytest.approx(sum(event.waited_s for event in events))
