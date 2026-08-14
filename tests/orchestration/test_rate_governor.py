"""Tests for F057 T001 — provider rate-limit signal normalization.

Pure logic: no clock, no sleep, no network, no filesystem. Every positive sample below
is either a literal taken from in-repo evidence (the fixture at
tests/orchestration/fixtures/stream/retry_and_error.jsonl, whose two api_retry reasons
are the only rate-limit literals this repo has) or a provider spelling the module marks
as such in its wording table.
"""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest

from packages.orchestration.rate_governor import (
    MAX_RETRY_AFTER_S,
    RATE_LIMIT_REASON_OVERLOADED,
    RATE_LIMIT_REASON_QUOTA_EXCEEDED,
    RATE_LIMIT_REASON_RATE_LIMITED,
    RATE_LIMIT_REASON_THROTTLED,
    RATE_LIMIT_SIGNAL_VERSION,
    RATE_SIGNAL_RAW_MAX_CHARS,
    RATE_SIGNAL_SOURCE_API_RETRY,
    RATE_SIGNAL_SOURCE_PROVIDER_ERROR,
    RATE_SIGNAL_SOURCE_RETRY_REASON,
    RateLimitSignal,
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
