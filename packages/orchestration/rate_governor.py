"""Rate-limit signal normalization and the per-provider governor (F057 T001+T002).

ONE place that turns the provider rate-limit / overload / throttle wording this
repository actually emits into a :class:`RateLimitSignal` a governor can act on,
and ONE governor that acts on it. :class:`ProviderRateGovernor` holds the
per-provider cooldown state that :meth:`ProviderRateGovernor.observe` feeds, and
:meth:`ProviderRateGovernor.acquire` waits that cooldown out in slices against an
INJECTED clock, so a stop request beats a wait instead of queueing behind it. The
seam that calls the governor from ``_call_with_retry`` is T003.

Normalization still holds no clock: the wording table below is tested against real
evidence samples without one, and only the governor sleeps.

Remedy deliberately does NOT coordinate ACROSS PROCESSES: two Remedy processes hold
independent governors and pace their providers independently. Cross-process pacing
belongs to the scheduler tier, as the F057 feature file states under Edge cases, so a
run that needs one shared budget across processes will not get it here.

Remedy deliberately does NOT queue or fairly order N concurrent acquirers inside one
process either. :meth:`ProviderRateGovernor.acquire` is SHAPED for N callers — it
takes no caller identity, hands back no reservation and needs no release — but the
implementation is single-flight, per the feature file's "design the interface for N
concurrent acquirers now, implement single-flight now". Fair queueing is a later
tier's change to this class rather than a second class beside it.

Remedy deliberately does NOT call :meth:`ProviderRateGovernor.acquire` from anywhere
yet: nothing outside this module and its test imports the governor. The seam is T003,
and until it lands, searching for a caller finds none on purpose.

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
    RateLimitWaitEvent           — one wait a run actually paid for
    RateLimitAcquireResult       — granted / stopped / deadline_exceeded, plus waited_s
    ProviderRateGovernor         — per-provider cooldown state, observe() and acquire()
"""
from __future__ import annotations

import re
import time
from collections.abc import Callable, Iterable, Mapping
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


# ---------------------------------------------------------------------------
# T002 — the governor: cooldown state, acquire(), and the waits it records.
# ---------------------------------------------------------------------------

#: The first cooldown applied when the provider sent no ``retry_after_s`` hint, then
#: doubled per consecutive signal. Small enough that one stray signal costs almost
#: nothing, large enough to break a hot retry loop.
RATE_LIMIT_COOLDOWN_BASE_S = 1.0

#: THE documented cap the exponential never exceeds. A provider that keeps saying "slow
#: down" must not turn one call into a wait longer than a person will sit through
#: without an explanation.
RATE_LIMIT_COOLDOWN_MAX_S = 60.0

#: Wait granularity: :meth:`ProviderRateGovernor.acquire` sleeps at most this long at a
#: time and probes ``stop_check`` once per slice, so a stop request costs at most one
#: slice of latency instead of the whole cooldown.
RATE_GOVERNOR_POLL_SLICE_S = 0.05

#: The three ``acquire`` outcomes. Named constants, never bare strings at call sites, so
#: an outcome greps back to the contract that defines it (DECISION F057 D2).
RATE_ACQUIRE_GRANTED = "granted"
RATE_ACQUIRE_STOPPED = "stopped"
RATE_ACQUIRE_DEADLINE_EXCEEDED = "deadline_exceeded"

RATE_LIMIT_WAIT_VERSION = 1


@dataclass(frozen=True)
class RateLimitWaitEvent:
    """RateLimitWaitEventV1 — one wait a run actually paid for.

    Recorded for every ``acquire`` that spent more than zero seconds, INCLUDING the ones
    that ended in a stop or in a deadline: the time was really spent, and evidence that
    dropped it would make a paced-then-stopped run look like a run that never waited
    (DECISION F057 D2).
    """

    provider: str
    waited_s: float
    reason: str
    rate_limit_wait_v: int = RATE_LIMIT_WAIT_VERSION

    def to_json(self) -> dict[str, Any]:
        return {
            "rate_limit_wait_v": self.rate_limit_wait_v,
            "provider": self.provider,
            "waited_s": self.waited_s,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class RateLimitAcquireResult:
    """What ONE ``acquire`` call did: the outcome, the seconds waited, and the reason.

    Deliberately not a bool: "did not wait at all" and "was stopped mid-wait" are
    different facts to the caller and to the run report, and a bool erases the
    difference (DECISION F057 D2). ``reason`` is "" when nothing was waited on.
    """

    outcome: str
    provider: str
    waited_s: float = 0.0
    reason: str = ""

    @property
    def granted(self) -> bool:
        return self.outcome == RATE_ACQUIRE_GRANTED


class ProviderRateGovernor:
    """Per-provider cooldown state, fed by :class:`RateLimitSignal` and read by acquire().

    The clock and the sleep are INJECTED: a unit test hands in a fake pair and never
    sleeps for real, while production hands in nothing and gets ``time.monotonic`` and
    ``time.sleep``. Single-flight — see the module docstring for what this class
    deliberately does not do.
    """

    def __init__(
        self,
        *,
        monotonic_fn: Callable[[], float] = time.monotonic,
        sleep_fn: Callable[[float], None] = time.sleep,
        base_cooldown_s: float = RATE_LIMIT_COOLDOWN_BASE_S,
        max_cooldown_s: float = RATE_LIMIT_COOLDOWN_MAX_S,
        poll_slice_s: float = RATE_GOVERNOR_POLL_SLICE_S,
    ) -> None:
        self._monotonic_fn = monotonic_fn
        self._sleep_fn = sleep_fn
        self._base_cooldown_s = base_cooldown_s
        self._max_cooldown_s = max_cooldown_s
        self._poll_slice_s = poll_slice_s
        self._cooldown_until: dict[str, float] = {}
        self._streaks: dict[str, int] = {}
        self._reasons: dict[str, str] = {}
        self._wait_events: list[RateLimitWaitEvent] = []

    def observe(self, signal: RateLimitSignal) -> float:
        """Feed ONE signal into that provider's cooldown; return the seconds just applied.

        The provider's own ``retry_after_s`` wins verbatim when it sent one — a provider
        that states its own recovery time knows better than a backoff curve, and
        :func:`parse_retry_after_seconds` already rejected the absurd values. Only in its
        absence does the exponential run, doubling per consecutive signal and never
        exceeding :data:`RATE_LIMIT_COOLDOWN_MAX_S`.

        A signal never SHORTENS a running cooldown: the stored deadline moves to the
        later of the two, so a late 1-second hint cannot cancel a 30-second wait already
        under way.
        """
        provider = signal.provider
        streak = self._streaks.get(provider, 0) + 1
        self._streaks[provider] = streak
        if signal.retry_after_s is not None:
            duration = float(signal.retry_after_s)
        else:
            duration = min(self._base_cooldown_s * (2.0 ** (streak - 1)), self._max_cooldown_s)
        now = self._monotonic_fn()
        self._cooldown_until[provider] = max(self._cooldown_until.get(provider, 0.0), now + duration)
        self._reasons[provider] = signal.reason
        return duration

    def cooldown_remaining_s(self, provider: str) -> float:
        """How much of ``provider``'s cooldown is left; 0.0 for one never observed."""
        return max(0.0, self._cooldown_until.get(provider, 0.0) - self._monotonic_fn())

    def acquire(
        self,
        provider: str,
        *,
        role: str = "",
        deadline_s: float | None = None,
        stop_check: Callable[[], Any] | None = None,
    ) -> RateLimitAcquireResult:
        """Wait out ``provider``'s cooldown unless a stop or a deadline says otherwise.

        The ORDER below is the F057 acceptance criterion, not an implementation detail
        (DECISION F057 D2):

        1. ``stop_check`` is probed FIRST, before any cooldown is read, so a stop can
           never be delayed by a pacing decision. Non-None means stopped — the same
           convention ``_call_with_retry`` already uses
           (``packages/orchestration/pingpong_loop.py:2207``).
        2. No cooldown left means GRANTED with nothing waited, no wait event, and the
           provider's streak reset: it recovered.
        3. Otherwise the wait runs in slices of at most ``poll_slice_s``, re-probing
           ``stop_check`` BEFORE every slice. ``deadline_s``, when given, is an absolute
           value on the SAME monotonic scale as ``monotonic_fn``; a cooldown running past
           it is waited only up to it and returns DEADLINE_EXCEEDED.
        4. Every outcome that waited more than 0.0 seconds records exactly one
           :class:`RateLimitWaitEvent` — granted, stopped and deadline alike.

        ``role`` is carried for the caller's evidence and does not affect pacing.
        """
        if stop_check is not None and stop_check() is not None:
            return RateLimitAcquireResult(outcome=RATE_ACQUIRE_STOPPED, provider=provider)
        started_at = self._monotonic_fn()
        if self.cooldown_remaining_s(provider) <= 0.0:
            self._streaks[provider] = 0
            return RateLimitAcquireResult(outcome=RATE_ACQUIRE_GRANTED, provider=provider)
        reason = self._reasons.get(provider, "")
        cooldown_until = self._cooldown_until.get(provider, 0.0)
        wait_until = cooldown_until
        outcome = RATE_ACQUIRE_GRANTED
        if deadline_s is not None and deadline_s < cooldown_until:
            wait_until = deadline_s
            outcome = RATE_ACQUIRE_DEADLINE_EXCEEDED
        now = started_at
        while now < wait_until:
            if stop_check is not None and stop_check() is not None:
                outcome = RATE_ACQUIRE_STOPPED
                break
            self._sleep_fn(min(self._poll_slice_s, wait_until - now))
            now = self._monotonic_fn()
        waited_s = max(0.0, self._monotonic_fn() - started_at)
        if waited_s > 0.0:
            self._wait_events.append(
                RateLimitWaitEvent(provider=provider, waited_s=waited_s, reason=reason)
            )
        return RateLimitAcquireResult(
            outcome=outcome,
            provider=provider,
            waited_s=waited_s,
            reason=reason,
        )

    def wait_events(self) -> list[RateLimitWaitEvent]:
        """A COPY of the waits recorded so far; the live list is never handed out."""
        return list(self._wait_events)

    def total_waited_s(self) -> float:
        """Every second this governor made the run wait — the T003 report line's number."""
        return sum(event.waited_s for event in self._wait_events)
