"""One provider call of the ping-pong loop: its bounded retry, its pacing and its booking.

``_call_with_retry`` makes one logical provider call with the bounded transport retry and the
rate governor's pacing, and books every real invocation on the run's result as a
:class:`ProviderAttempt`; ``_begin_stream_call`` and ``_offer_stable_prefix`` are the two
duck-typed hints the loop hands a provider before it calls. F307 moved them here from
``pingpong_loop.py`` as that file's structural step (3) in ``docs/system/structure-ledger-v1.md``.
"""
from __future__ import annotations

import time as _time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from packages.orchestration.model_failover import FailoverCall
from packages.orchestration.provider_timeouts import (
    is_nonzero_exit_error,
    is_timeout_error,
    next_backoff,
    should_retry,
)
from packages.orchestration.rate_governor import (
    RATE_SIGNAL_SOURCE_RETRY_REASON,
    ProviderRateGovernor,
    RateLimitAcquireResult,
    RateLimitWaitEvent,
    is_rate_limit_error,
    normalize_rate_limit_signal,
)

if TYPE_CHECKING:
    from packages.orchestration.pingpong_loop import PingPongResult


@dataclass
class ProviderAttempt:
    """Record of a single provider invocation for usage accounting."""
    role: str = ""          # "builder" or "reviewer"
    provider: str = ""      # provider name (e.g. "claude-cli", "fake")
    usage_actuals: dict[str, Any] | None = None
    actual_missing_reason: str = ""
    is_retry: bool = False
    is_parse_retry: bool = False
    error: str = ""
    # F004: which per-call stream directory this attempt produced (empty when
    # stream evidence is off, or for fake/manual providers which never stream).
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    # R-0807: the loop round this invocation belongs to (0 = not recorded).
    round: int = 0
    # R-1276: the model this invocation ran on — a backup link's own, else the role's configured one.
    model: str = ""


def _begin_stream_call(provider: Any, round_no: int, kind: str = "attempt") -> None:
    """Tell a stream-capable provider which round/kind its next call belongs to.

    A no-op for providers without stream evidence (fake, manual, JSON-mode).
    """
    fn = getattr(provider, "begin_stream_call", None)
    if callable(fn):
        try:
            fn(round_no, kind)
        except Exception:  # noqa: BLE001 — a stream hint is optional; the call must not fail on it
            pass


def _offer_stable_prefix(provider: Any, composed: Any) -> None:
    """Hand a cache-capable provider the stable prefix of the prompt it is sent next.

    A no-op for providers that do not cache a prefix (every one but the
    direct-API provider), the same duck-typed shape as ``_begin_stream_call``.
    """
    fn = getattr(provider, "offer_stable_prefix", None)
    if callable(fn):
        try:
            fn(composed.stable_prefix())
        except Exception:  # noqa: BLE001 — prefix caching is optional; the call must not fail on it
            pass


def _record_attempt(
    result: PingPongResult,
    out: Any,
    role: str,
    provider: str,
    *,
    is_retry: bool = False,
    is_parse_retry: bool = False,
    round_num: int = 0,
) -> list[ProviderAttempt]:
    """Book every real provider invocation behind ``out`` for usage accounting; return the rows.

    One row under the configured ``provider`` and the role's configured model, unless a failover
    walk made more than one call: then one row per call, under the provider and model that served
    or failed it, each read from that call's own answer (R-1276).
    """
    configured_model = getattr(result, f"{role}_model", "") or ""
    calls = getattr(out, "failover_calls", None) or (FailoverCall(provider, configured_model),)
    rows: list[ProviderAttempt] = []
    for call in calls:
        answer = out if call.output is None else call.output
        rows.append(ProviderAttempt(
            round=round_num,
            role=role,
            provider=call.provider,
            model=call.model,
            usage_actuals=getattr(answer, "usage_actuals", None),
            actual_missing_reason=getattr(answer, "actual_missing_reason", ""),
            is_retry=is_retry,
            is_parse_retry=is_parse_retry,
            error=getattr(answer, "error", ""),
            stream_call_id=getattr(answer, "stream_call_id", "") or "",
            stream_artifact_refs=list(getattr(answer, "stream_artifact_refs", []) or []),
        ))
    result.provider_attempts.extend(rows)
    return rows


def _record_rate_limit_wait(result: PingPongResult, acquired: RateLimitAcquireResult) -> None:
    """Record ONE governor wait on the run result — the only writer of ``rate_limit_waits``.

    An acquire that waited nothing records nothing: zero-second entries would bury the
    waits a reader is looking for. The dict is built THROUGH :class:`RateLimitWaitEvent`
    rather than by hand, so the report surface reads exactly the shape the governor
    already emits and there is one spelling of a wait in the repository.
    """
    if acquired.waited_s <= 0.0:
        return
    result.rate_limit_waits.append(
        RateLimitWaitEvent(
            provider=acquired.provider,
            waited_s=acquired.waited_s,
            reason=acquired.reason,
        ).to_json()
    )


def _call_with_retry(
    call_fn: Any,
    *,
    result: PingPongResult,
    role: str,
    provider: str = "",
    on_call: Any = None,
    on_provider_attempt: Callable[[ProviderAttempt], None] | None = None,
    is_parse_retry: bool = False,
    call_reasons: list[str] | None = None,
    stop_check: Callable[[], Any] | None = None,
    rate_governor: ProviderRateGovernor | None = None,
    round_num: int = 0,
) -> Any:
    """Call a provider function with bounded retry on transient failures.

    Only retries on timeout or nonzero exit (detected via error string) — plus, when
    a governor is active for this call, on a rate limit (R-0373; see the decision below).
    Never retries review rejects. Records retry evidence on result.
    Every real call (initial + retries, and each one a failover walk made) is a ProviderAttempt.

    ``stop_check`` (F018) is evaluated before each transport retry. A budget
    exhaustion observed between retries prevents the next call from starting.

    ``on_call(transport_attempt, is_transport_retry)`` — when given — runs
    IMMEDIATELY BEFORE every real ``call_fn()`` invocation, so a caller can
    record exactly one prompt-trace entry per actual provider call (F005). This
    is the same retry mechanism, not a second one.

    ``rate_governor`` (F057) is the pacing seam. When one is given and ``provider``
    is non-empty, the governor waits out that provider's running cooldown before the
    first call and before every retry, and observes the failed call's own error so
    the cooldown a rate limit announces is the one the next retry waits out; a retry
    observes and waits on the provider that answered, ``out.provider`` (R-1277). Every
    wait that cost more than zero seconds is recorded on
    ``result.rate_limit_waits``. Before the FIRST call the wait only PACES — the call
    is made whatever the acquire outcome (DECISION F057 D3); before a RETRY a
    non-granted outcome returns the last ``out``, joining the terminal path the stop
    probe already owns. No ``deadline_s`` is passed: the budget reaches the wait
    through the same ``stop_check`` the governor re-probes each slice
    (DECISION F057 D4). A falsy ``provider`` skips the governor entirely
    (DECISION F057 D5), and ``rate_governor=None`` — every pre-F057 caller — leaves
    this function's behaviour exactly as it was.
    """
    from packages.orchestration.provider_timeouts import MAX_RETRIES

    # F057: pace the FIRST call. This seam only WAITS — it never decides not to call
    # (DECISION F057 D3), so the acquire outcome is recorded, not branched on.
    if rate_governor is not None and provider:
        _record_rate_limit_wait(
            result,
            rate_governor.acquire(provider, role=role, stop_check=stop_check),
        )
    if on_call is not None:
        on_call(1, False)
    out = call_fn()
    # The parse-retry call is itself a retry of the logical review; its transport
    # retries stay part of that ONE logical parse retry.
    for _row in _record_attempt(result, out, role, provider, is_retry=is_parse_retry,
                                is_parse_retry=is_parse_retry, round_num=round_num):
        if on_provider_attempt is not None:
            on_provider_attempt(_row)
    for attempt in range(MAX_RETRIES):
        if not out.error:
            return out

        # A reached stream-evidence cap is a deliberate, honest termination —
        # not a transport failure. It must never be retried like a timeout or a
        # non-zero exit, and it must not be treated as a successful call.
        if getattr(out, "stream_cap_reached", False):
            return out

        # THE predicates — the same functions F010's classifier uses. A second copy of
        # "what counts as a timeout" is a second definition, and definitions drift.
        is_timeout = is_timeout_error(out.error)
        is_nonzero = is_nonzero_exit_error(out.error)
        # WHY: ReviewerOutput.verdict defaults to "blocked", so ONLY the "provider_error:" prefix keeps a reviewer transport error (a rate limit too) retryable — R-0378.
        is_reject = (
            hasattr(out, "verdict")
            and out.verdict in ("needs_repair", "fail", "blocked")
            and not out.error.startswith("provider_error:")
        )

        # F057 R-0373: a rate limit is retryable AT THIS SEAM — the precedence rule lives
        # here and NOT in provider_timeouts.py, whose per-call transport policy this
        # feature must not move. Guarded on an active governor, so a caller without one
        # keeps its pre-F057 behaviour byte for byte. Without this the whole seam is
        # unreachable: should_retry declines a bare rate limit before the governor below
        # ever observes it, so no cooldown is created and the pacing has nothing to pace.
        is_rate_limit = bool(
            rate_governor is not None and provider and is_rate_limit_error(out.error)
        )
        _transport_retries = should_retry(
            is_timeout=is_timeout, exit_code=1 if is_nonzero else 0, is_review_reject=is_reject
        )
        # A review reject is NEVER retried, whatever else is true of it.
        if is_reject or not (_transport_retries or is_rate_limit):
            return out

        backoff = next_backoff(attempt)
        if backoff is None:
            return out

        # F018: check budget before spending another transport call
        if stop_check is not None and stop_check() is not None:
            return out

        # F057: pace the RETRY. OBSERVE this failure first, so the cooldown it announces
        # is the one this retry waits out, then wait it out. Placed BEFORE the retry
        # counters below on purpose: a stop during the wait must leave them exactly where
        # the stop probe above leaves them, so no evidence claims a retry that never ran.
        if rate_governor is not None and provider:
            _served = getattr(out, "provider", "") or provider  # R-1277: a backup link answers for itself
            _rate_signal = normalize_rate_limit_signal(out.error, provider=_served,
                                                       source=RATE_SIGNAL_SOURCE_RETRY_REASON)
            if _rate_signal is not None:
                rate_governor.observe(_rate_signal)
            _acquired = rate_governor.acquire(_served, role=role, stop_check=stop_check)
            _record_rate_limit_wait(result, _acquired)
            if not _acquired.granted:
                return out

        result.retries_used += 1
        _reason = f"{role}:attempt{attempt + 1}:{out.error[:120]}"
        result.retry_reasons.append(_reason)          # the run-global summary, unchanged
        if call_reasons is not None:
            # ...and the evidence of THIS logical call, which is what a post-mortem may
            # honestly cite. A builder timeout in round 1 is not evidence about a reviewer
            # failure in round 3.
            call_reasons.append(_reason)
        _time.sleep(backoff)
        if on_call is not None:
            on_call(attempt + 2, True)
        out = call_fn()
        for _row in _record_attempt(result, out, role, provider, is_retry=True,
                                    is_parse_retry=is_parse_retry, round_num=round_num):
            if on_provider_attempt is not None:
                on_provider_attempt(_row)

    return out
