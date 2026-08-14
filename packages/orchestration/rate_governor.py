"""Rate-limit signal normalization for the per-provider governor (F057 T001).

ONE place that turns the provider rate-limit / overload / throttle wording this
repository actually emits into a :class:`RateLimitSignal` a governor can act on.
The governor itself — cooldown state, ``acquire()``, the injected clock — is
T002; the seam that calls either of them is T003.

Remedy deliberately does NOT wait, sleep, retry, or hold state in this module,
and nothing imports it yet. T001 is recognition only: normalization is separated
from waiting so the wording table can be tested against real evidence samples
without a clock. Searching this file for ``sleep``, ``acquire`` or ``cooldown``
finds nothing on purpose.

Observed signal shapes (the T001 inventory; every entry verified on disk on the
F057 branch, cut from main at 21c8148e):

1. ``packages/orchestration/stream_evidence.py:296-302`` — ``normalize_stream_object``
   turns a ``{"type": "api_retry"|"retry", ...}`` stream object into
   ``{"event_type": "api_retry", "attempt": int, "reason": str}``. ``reason`` is
   bounded to 300 chars and falls back to the object's ``error`` key.
2. ``packages/orchestration/stream_evidence.py:290-295`` — the same function turns
   ``{"type": "error"|"provider_error", ...}`` into
   ``{"event_type": "provider_error", "error": str}``, bounded to 500 chars.
3. ``packages/orchestration/pingpong_loop.py:2211`` — each ``retry_reasons`` entry is
   ``f"{role}:attempt{attempt + 1}:{out.error[:120]}"``, so the provider wording
   arrives as the tail of a role/attempt-prefixed string.
4. ``tests/orchestration/fixtures/stream/retry_and_error.jsonl:2`` — literal sample
   ``{"type":"api_retry","attempt":1,"reason":"overloaded_error"}``. The same token is
   asserted at ``tests/orchestration/test_stream_evidence.py:136`` and produced at
   ``tests/orchestration/test_stream_evidence_integration.py:50``.
5. ``tests/orchestration/fixtures/stream/retry_and_error.jsonl:3`` — literal sample
   ``{"type":"api_retry","attempt":2,"reason":"rate_limit"}``.

Inspected and EXCLUDED, so the next reader does not re-open it:
``packages/orchestration/mission_dossier.py:980`` contains the words "rate-limits", but
it is the body of a ``RecallFact`` demo record, not a provider signal.

That is the whole inventory. No further rate-limit wording exists in ``packages/``,
``apps/`` or ``tests/`` — every other hit of ``overload|throttl|429|rate.?limit`` is an
unrelated number (``4294967295``) or a step id. Patterns below that cover provider
vocabulary this repo has no sample for say so on their own line.

Public API:
    RateLimitSignal              — the normalized, JSON-safe signal
    is_rate_limit_error()        — THE rate-limit predicate
    classify_rate_limit_reason() — the normalized reason token, or None
    parse_retry_after_seconds()  — the provider's retry hint, or None
    normalize_rate_limit_signal()— one piece of evidence -> signal or None
    read_run_event_signals()     — reader for shapes 1 and 2
    read_retry_reason_signals()  — reader for shape 3
"""
from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from packages.orchestration.stream_evidence import EVENT_API_RETRY, EVENT_PROVIDER_ERROR

RATE_LIMIT_SIGNAL_VERSION = 1

#: Which evidence shape a signal was read out of. Named constants, never bare strings at
#: call sites, so a source value greps back to the inventory entry that defines it.
RATE_SIGNAL_SOURCE_API_RETRY = "stream_api_retry"          # inventory 1
RATE_SIGNAL_SOURCE_PROVIDER_ERROR = "stream_provider_error"  # inventory 2
RATE_SIGNAL_SOURCE_RETRY_REASON = "loop_retry_reason"      # inventory 3

#: Normalized reason tokens. A signal carries one of these, never the raw sentence: the
#: governor keys cooldown state off the reason, and free text would give every provider
#: message its own bucket.
RATE_LIMIT_REASON_OVERLOADED = "overloaded"
RATE_LIMIT_REASON_RATE_LIMITED = "rate_limited"
RATE_LIMIT_REASON_QUOTA_EXCEEDED = "quota_exceeded"
RATE_LIMIT_REASON_THROTTLED = "throttled"

#: The widest bound any inbound shape already applies (stream_evidence.py:293 bounds a
#: provider error to 500 chars). Bounding here too means ``raw`` is safe to copy into
#: evidence even when a reader hands us an unbounded string.
RATE_SIGNAL_RAW_MAX_CHARS = 500

#: A retry hint longer than an hour is not a pacing instruction, it is a bad parse or a
#: broken provider. Rejected rather than clamped, so the governor falls back to its own
#: cooldown instead of sleeping on a number nobody vouched for.
MAX_RETRY_AFTER_S = 3600.0

#: The ONE wording table. Ordered: the first marker that appears in the text decides the
#: reason, so `is_rate_limit_error` and `classify_rate_limit_reason` can never disagree.
#: Every entry names the in-repo evidence for its marker, or says it has none.
_RATE_LIMIT_MARKERS: tuple[tuple[str, str], ...] = (
    # tests/orchestration/fixtures/stream/retry_and_error.jsonl:2 — "overloaded_error".
    # Matched on the stem so "overload", "overloaded" and "overloading" are one entry;
    # a second entry for the longer spelling would be unreachable, not safer.
    ("overload", RATE_LIMIT_REASON_OVERLOADED),
    # tests/orchestration/fixtures/stream/retry_and_error.jsonl:3 — "rate_limit"
    ("rate_limit", RATE_LIMIT_REASON_RATE_LIMITED),
    # no in-repo sample; provider vocabulary (prose spelling, e.g. "rate limit exceeded")
    ("rate limit", RATE_LIMIT_REASON_RATE_LIMITED),
    # no in-repo sample; provider vocabulary (hyphenated prose spelling)
    ("rate-limit", RATE_LIMIT_REASON_RATE_LIMITED),
    # no in-repo sample; provider vocabulary (class names such as RateLimitError)
    ("ratelimit", RATE_LIMIT_REASON_RATE_LIMITED),
    # no in-repo sample; provider vocabulary (HTTP 429 reason phrase)
    ("too many requests", RATE_LIMIT_REASON_RATE_LIMITED),
    # no in-repo sample; provider vocabulary (HTTP 429 status, spelled with its label).
    # The bare number is deliberately NOT a marker: "4294967295" occurs in this repo at
    # packages/orchestration/run_manifest.py:4059 and would match it.
    ("http 429", RATE_LIMIT_REASON_RATE_LIMITED),
    ("status 429", RATE_LIMIT_REASON_RATE_LIMITED),
    ("error 429", RATE_LIMIT_REASON_RATE_LIMITED),
    # no in-repo sample; provider vocabulary (billing/plan ceilings)
    ("quota exceeded", RATE_LIMIT_REASON_QUOTA_EXCEEDED),
    ("quota_exceeded", RATE_LIMIT_REASON_QUOTA_EXCEEDED),
    ("insufficient_quota", RATE_LIMIT_REASON_QUOTA_EXCEEDED),
    # no in-repo sample; provider vocabulary (matches throttled / throttling / throttle)
    ("throttl", RATE_LIMIT_REASON_THROTTLED),
)

#: The provider's own hint, in the HTTP ``Retry-After`` spelling and its JSON cousins.
#: no in-repo sample; provider vocabulary — this repo emits no retry-after today, which is
#: exactly why absence must stay distinguishable from zero.
_RETRY_AFTER_RE = re.compile(
    r"retry[-_ ]?after[\"']?\s*(?:[:=]|\bis\b|\bin\b)?\s*(-?\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RateLimitSignal:
    """RateLimitSignalV1 — one normalized provider rate-limit observation.

    Immutable and bounded: it is copied into cycle evidence and a run report, which a
    person reads. ``retry_after_s`` is None when the provider gave no hint — never 0.0,
    because "retry immediately" and "no hint at all" are different instructions to the
    governor T002 builds.
    """

    provider: str
    reason: str
    retry_after_s: float | None = None
    source: str = ""
    raw: str = ""
    rate_limit_signal_v: int = RATE_LIMIT_SIGNAL_VERSION

    def to_json(self) -> dict[str, Any]:
        return {
            "rate_limit_signal_v": self.rate_limit_signal_v,
            "provider": self.provider,
            "reason": self.reason,
            "retry_after_s": self.retry_after_s,
            "source": self.source,
            "raw": self.raw,
        }


def is_rate_limit_error(text: str | None) -> bool:
    """Does this provider text mean "the provider is rate-limiting us"?

    THE rate-limit predicate, for callers that only need a yes or no — T003's seam, and
    any guard that branches on "is this a rate limit at all". It is the emptiness test of
    :func:`classify_rate_limit_reason`, which owns the single wording table; the readers
    in this module reach that table through :func:`normalize_rate_limit_signal` rather
    than through this predicate, so the two can never disagree about a marker. That
    single-table shape is what ``is_timeout_error`` in
    ``packages/orchestration/provider_timeouts.py`` argues for: two definitions of "what
    counts as X" drift apart, and the drift is the bug.

    It returns False for the strings the existing transport predicates already own. A bare
    timeout ("claude CLI timed out after 600s") is ``is_timeout_error``'s; a bare non-zero
    exit ("process exited with code 1") is ``is_nonzero_exit_error``'s. Neither is a rate
    limit, and this predicate must not start answering for them.
    """
    return classify_rate_limit_reason(text) is not None


def classify_rate_limit_reason(text: str | None) -> str | None:
    """Which normalized reason token does this text carry, if any?

    The same table :func:`is_rate_limit_error` answers from — the predicate is this
    function's emptiness test, so a marker can never match one and miss the other.
    """
    if not text:
        return None
    lowered = text.lower()
    for marker, reason in _RATE_LIMIT_MARKERS:
        if marker in lowered:
            return reason
    return None


def parse_retry_after_seconds(text: str | None) -> float | None:
    """Pull the provider's retry-after hint out of ``text``, or None when there is none.

    Absent is None, never 0.0: a governor that reads a missing hint as "wait zero seconds"
    hammers the provider it is supposed to be pacing. A negative value and anything above
    :data:`MAX_RETRY_AFTER_S` are rejected the same way — the caller falls back to its own
    cooldown rather than trusting a number that cannot be right.
    """
    if not text:
        return None
    match = _RETRY_AFTER_RE.search(text)
    if match is None:
        return None
    try:
        seconds = float(match.group(1))
    except ValueError:  # pragma: no cover — the regex only captures parseable numbers
        return None
    if seconds < 0.0 or seconds > MAX_RETRY_AFTER_S:
        return None
    return seconds


def normalize_rate_limit_signal(
    text: str | None,
    *,
    provider: str,
    source: str,
) -> RateLimitSignal | None:
    """Turn ONE piece of evidence text into a signal, or None when it is not a rate limit.

    Every reader funnels through here, so bounding, reason classification and retry-hint
    parsing happen once rather than once per evidence shape.
    """
    reason = classify_rate_limit_reason(text)
    if reason is None:
        return None
    raw = (text or "")[:RATE_SIGNAL_RAW_MAX_CHARS]
    return RateLimitSignal(
        provider=provider,
        reason=reason,
        retry_after_s=parse_retry_after_seconds(text),
        source=source,
        raw=raw,
    )


#: Which key of a normalized run event carries the provider's wording, per event type.
#: Inventory entries 1 and 2; the event-type constants come from ``stream_evidence`` rather
#: than being re-spelled here, so there is one definition of "api_retry" in the repo.
_RUN_EVENT_TEXT_KEYS: dict[str, tuple[str, str]] = {
    EVENT_API_RETRY: ("reason", RATE_SIGNAL_SOURCE_API_RETRY),
    EVENT_PROVIDER_ERROR: ("error", RATE_SIGNAL_SOURCE_PROVIDER_ERROR),
}


def read_run_event_signals(
    events: Iterable[Mapping[str, Any]],
    *,
    provider: str,
) -> list[RateLimitSignal]:
    """Read rate-limit signals out of normalized run events (inventory shapes 1 and 2).

    Events of any other type, and rate-limit-free retries or errors, yield nothing: a run
    that hit a timeout has no rate-limit signal to report, and saying otherwise would make
    the governor pace a provider that never asked it to.
    """
    signals: list[RateLimitSignal] = []
    for event in events:
        if not isinstance(event, Mapping):
            continue
        keyed = _RUN_EVENT_TEXT_KEYS.get(str(event.get("event_type") or ""))
        if keyed is None:
            continue
        text_key, source = keyed
        value = event.get(text_key)
        signal = normalize_rate_limit_signal(
            value if isinstance(value, str) else None,
            provider=provider,
            source=source,
        )
        if signal is not None:
            signals.append(signal)
    return signals


def read_retry_reason_signals(
    reasons: Iterable[str],
    *,
    provider: str,
) -> list[RateLimitSignal]:
    """Read rate-limit signals out of ``PingPongResult.retry_reasons`` (inventory shape 3).

    Each entry is ``"{role}:attempt{n}:{error}"`` (pingpong_loop.py:2211). The role and
    attempt prefix is left on the ``raw`` text deliberately — it is part of the evidence a
    reader wants, and the predicate matches on the provider wording in the tail regardless.
    """
    signals: list[RateLimitSignal] = []
    for reason in reasons:
        if not isinstance(reason, str):
            continue
        signal = normalize_rate_limit_signal(
            reason,
            provider=provider,
            source=RATE_SIGNAL_SOURCE_RETRY_REASON,
        )
        if signal is not None:
            signals.append(signal)
    return signals
