"""Tests for F001 retry behavior and timeout profile integration.

Covers:
  - Fake provider that times out once then succeeds → retries_used=1
  - retry_reasons records the failure
  - Review reject does NOT trigger retry
  - Timeout profile wires correct seconds into builder/reviewer
  - Attempts are separately recorded in evidence
"""
from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from packages.orchestration.pingpong_loop import (
    PingPongResult,
    _call_with_retry,
    export_pingpong_json,
    run_pingpong,
    summarize_pingpong,
)
from packages.orchestration.pingpong_provider import (
    BuilderOutput,
    FakeProvider,
    ReviewerOutput,
)
from packages.orchestration.provider_timeouts import (
    PROFILES,
)
from packages.orchestration.rate_governor import (
    RATE_LIMIT_REASON_RATE_LIMITED,
    RATE_SIGNAL_SOURCE_RETRY_REASON,
    ProviderRateGovernor,
    normalize_rate_limit_signal,
)

# ---------------------------------------------------------------------------
# Helpers: providers that fail once then succeed
# ---------------------------------------------------------------------------

class TimeoutOnceFakeProvider(FakeProvider):
    """Fake provider that reports a timeout error on the first build call."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._build_attempts = 0

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        self._build_attempts += 1
        if self._build_attempts == 1:
            return BuilderOutput(
                error="provider_error: TimeoutExpired: timed out after 120s",
                provider="fake",
            )
        return super().build(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume)


class ReviewerTimeoutOnceFakeProvider(FakeProvider):
    """Fake provider where reviewer times out on first call."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._review_attempts = 0

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        self._review_attempts += 1
        if self._review_attempts == 1:
            return ReviewerOutput(
                error="provider_error: TimeoutExpired: reviewer timed out",
                provider="fake",
            )
        return super().review(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume)


class NonzeroExitOnceFakeProvider(FakeProvider):
    """Fake provider that reports nonzero exit on first build call."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._build_attempts = 0

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        self._build_attempts += 1
        if self._build_attempts == 1:
            return BuilderOutput(
                error="provider_error: RuntimeError: claude CLI exited 1: internal error",
                provider="fake",
            )
        return super().build(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume)


# ---------------------------------------------------------------------------
# _call_with_retry unit tests
# ---------------------------------------------------------------------------

class TestCallWithRetry:
    def test_success_no_retry(self):
        result = PingPongResult()
        out = BuilderOutput(summary="ok", provider="fake")
        val = _call_with_retry(lambda: out, result=result, role="builder")
        assert val is out
        assert result.retries_used == 0
        assert result.retry_reasons == []

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_timeout_retries_once(self, mock_sleep):
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return BuilderOutput(error="provider_error: TimeoutExpired", provider="fake")
            return BuilderOutput(summary="ok", provider="fake")

        out = _call_with_retry(call_fn, result=result, role="builder")
        assert out.summary == "ok"
        assert result.retries_used == 1
        assert len(result.retry_reasons) == 1
        assert "TimeoutExpired" in result.retry_reasons[0]
        mock_sleep.assert_called_once_with(30)

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_nonzero_exit_retries(self, mock_sleep):
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return BuilderOutput(error="exited 1: fail", provider="fake")
            return BuilderOutput(summary="recovered", provider="fake")

        out = _call_with_retry(call_fn, result=result, role="builder")
        assert out.summary == "recovered"
        assert result.retries_used == 1

    def test_review_reject_no_retry(self):
        """A genuine review verdict (needs_repair) must not trigger provider retry."""
        result = PingPongResult()
        out = ReviewerOutput(
            verdict="needs_repair",
            summary="Found issues",
            provider="fake",
        )
        val = _call_with_retry(lambda: out, result=result, role="reviewer")
        assert val is out
        assert result.retries_used == 0

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_provider_error_with_blocked_verdict_retries(self, mock_sleep):
        """A provider error that sets verdict=blocked should still retry."""
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return ReviewerOutput(
                    verdict="blocked",
                    error="provider_error: TimeoutExpired",
                    provider="fake",
                )
            return ReviewerOutput(verdict="pass", provider="fake")

        out = _call_with_retry(call_fn, result=result, role="reviewer")
        assert out.verdict == "pass"
        assert result.retries_used == 1

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_max_retries_bounded(self, mock_sleep):
        result = PingPongResult()

        def always_timeout():
            return BuilderOutput(error="provider_error: TimeoutExpired", provider="fake")

        out = _call_with_retry(always_timeout, result=result, role="builder")
        assert out.error  # still error after exhausting retries
        assert result.retries_used == 2  # MAX_RETRIES = 2
        assert len(result.retry_reasons) == 2
        assert mock_sleep.call_count == 2


# ---------------------------------------------------------------------------
# Integration: timeout profile wiring through run_pingpong
# ---------------------------------------------------------------------------

class TestTimeoutProfileIntegration:
    def test_profile_sets_evidence_fields(self, tmp_path):
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_name="fake",
            reviewer_name="fake",
            timeout_profile="fast",
        )
        assert result.timeout_profile == "fast"
        assert result.timeout_s_effective_builder == PROFILES["fast"].builder_base_s
        assert result.timeout_s_effective_reviewer == PROFILES["fast"].reviewer_base_s
        assert result.timeout_s_effective_builder >= result.timeout_s_effective_reviewer

    def test_no_profile_uses_raw_timeout(self, tmp_path):
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_name="fake",
            reviewer_name="fake",
            timeout_sec=999,
        )
        assert result.timeout_profile == ""
        assert result.timeout_s_effective_builder == 999
        assert result.timeout_s_effective_reviewer == 999

    def test_all_profiles_valid(self, tmp_path):
        for pname in ("fast", "normal", "patient"):
            result = run_pingpong(
                "test goal",
                str(tmp_path),
                builder_name="fake",
                reviewer_name="fake",
                timeout_profile=pname,
            )
            assert result.timeout_profile == pname
            assert result.timeout_s_effective_builder > 0
            assert result.timeout_s_effective_reviewer > 0

    def test_invalid_profile_fails_fast(self, tmp_path):
        with pytest.raises(ValueError, match="Invalid --timeout-profile"):
            run_pingpong(
                "test goal",
                str(tmp_path),
                builder_name="fake",
                reviewer_name="fake",
                timeout_profile="turbo",
            )


# ---------------------------------------------------------------------------
# Integration: retry with fake provider through run_pingpong
# ---------------------------------------------------------------------------

class TestRetryIntegration:
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_timeout_once_provider_retries(self, mock_sleep, tmp_path):
        provider = TimeoutOnceFakeProvider()
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_provider=provider,
            reviewer_name="fake",
        )
        assert result.retries_used == 1
        assert len(result.retry_reasons) == 1
        assert "TimeoutExpired" in result.retry_reasons[0]
        # Should continue after retry (may pass, exhaust rounds, or exhaust repair)
        assert result.retries_used == 1

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_nonzero_exit_once_retries(self, mock_sleep, tmp_path):
        provider = NonzeroExitOnceFakeProvider()
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_provider=provider,
            reviewer_name="fake",
        )
        assert result.retries_used == 1
        assert "exited" in result.retry_reasons[0]

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_reviewer_timeout_once_retries(self, mock_sleep, tmp_path):
        """Reviewer provider timeout triggers retry (finding 7 fix)."""
        provider = ReviewerTimeoutOnceFakeProvider(pass_on_round=1)
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_name="fake",
            reviewer_provider=provider,
        )
        assert result.retries_used >= 1
        assert any("reviewer" in r for r in result.retry_reasons)

    def test_review_reject_no_retry(self, tmp_path):
        """Review reject (needs_repair) must NOT trigger retry."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=2)
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_name="fake",
            reviewer_provider=provider,
        )
        # Reviewer says needs_repair on round 1 — this is NOT a retry scenario
        assert result.retries_used == 0


# ---------------------------------------------------------------------------
# Evidence export contains F001 fields
# ---------------------------------------------------------------------------

class TestEvidenceExport:
    def test_export_contains_timeout_fields(self, tmp_path):
        from packages.orchestration.pingpong_loop import export_pingpong_json

        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_name="fake",
            reviewer_name="fake",
            timeout_profile="normal",
        )
        exported = export_pingpong_json(result)

        assert "timeout_profile" in exported
        assert exported["timeout_profile"] == "normal"
        assert "timeout_s_effective_builder" in exported
        assert "timeout_s_effective_reviewer" in exported
        assert "retries_used" in exported
        assert "retry_reasons" in exported
        assert exported["timeout_s_effective_builder"] == PROFILES["normal"].builder_base_s
        assert exported["timeout_s_effective_reviewer"] == PROFILES["normal"].reviewer_base_s


# ---------------------------------------------------------------------------
# CLI timeout precedence (F001)
# ---------------------------------------------------------------------------

class TestTimeoutPrecedence:
    """Test _resolve_timeout_precedence from do_cmd."""

    def test_explicit_raw_wins_over_default_profile(self):
        from apps.cli.commands.do_cmd import _resolve_timeout_precedence
        sec, prof = _resolve_timeout_precedence(999, None)
        assert sec == 999
        assert prof == ""

    def test_explicit_raw_wins_over_explicit_profile(self):
        """When both are explicitly set, raw timeout takes priority."""
        from apps.cli.commands.do_cmd import _resolve_timeout_precedence
        sec, prof = _resolve_timeout_precedence(999, "fast")
        assert sec == 999
        assert prof == ""

    def test_explicit_profile_used_when_no_raw(self):
        from apps.cli.commands.do_cmd import _resolve_timeout_precedence
        sec, prof = _resolve_timeout_precedence(None, "fast")
        assert prof == "fast"

    def test_default_adaptive_normal_when_neither(self):
        from apps.cli.commands.do_cmd import _resolve_timeout_precedence
        sec, prof = _resolve_timeout_precedence(None, None)
        assert prof == "normal"
        assert sec == 120

    def test_raw_timeout_with_run_pingpong(self, tmp_path):
        """--timeout-sec 999 must result in 999s for both roles, no profile."""
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_name="fake",
            reviewer_name="fake",
            timeout_sec=999,
            timeout_profile="",
        )
        assert result.timeout_profile == ""
        assert result.timeout_s_effective_builder == 999
        assert result.timeout_s_effective_reviewer == 999

    def test_default_profile_with_run_pingpong(self, tmp_path):
        """No flags → adaptive normal."""
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_name="fake",
            reviewer_name="fake",
            timeout_profile="normal",
        )
        assert result.timeout_profile == "normal"
        assert result.timeout_s_effective_builder == PROFILES["normal"].builder_base_s
        assert result.timeout_s_effective_reviewer == PROFILES["normal"].reviewer_base_s


# ---------------------------------------------------------------------------
# F057 T003 — the rate-governor seam inside _call_with_retry
#
# These live HERE, and not in tests/orchestration/test_rate_governor.py, because the
# code under test is the SEAM in packages/orchestration/pingpong_loop.py, not the
# governor: AGENTS.md's Code Discoverability rule names a test file after the source it
# covers, and this file already owns _call_with_retry. test_rate_governor.py still owns
# the governor's own behaviour. Do not re-litigate the split; move the tests only if the
# seam moves.
#
# Every governor below runs on an INJECTED FakeClock and its sleep — no test here sleeps
# for real, and none asserts on wall-clock duration. The transport backoff at
# pingpong_loop._time.sleep is patched separately; it is F001's, not F057's.
# ---------------------------------------------------------------------------

#: A rate-limit error that the EXISTING transport predicates also call retryable
#: ("exited" -> is_nonzero_exit_error), so it would be retried even with no governor.
RATE_LIMITED_RETRYABLE_ERROR = (
    "provider_error: RuntimeError: claude CLI exited 1: rate_limit exceeded for this key"
)

#: A BARE rate limit: no "exited", no timeout wording, so every transport predicate
#: declines it and only the seam's own R-0373 rule can make it retryable.
BARE_RATE_LIMIT_ERROR = "429 Too Many Requests"

#: Slice size chosen so the waits below divide into an exact number of binary-clean
#: slices; the production default is RATE_GOVERNOR_POLL_SLICE_S and is not under test.
SEAM_POLL_SLICE_S = 0.25


class SeamFakeClock:
    """The injected clock and sleep for the seam tests: sleep advances time, never blocks."""

    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def _seam_governor(clock: SeamFakeClock) -> ProviderRateGovernor:
    return ProviderRateGovernor(
        monotonic_fn=clock.monotonic,
        sleep_fn=clock.sleep,
        poll_slice_s=SEAM_POLL_SLICE_S,
    )


def _observe_cooldown(governor: ProviderRateGovernor, provider: str) -> float:
    """Put ``provider`` into a real cooldown through the governor's own normalizer."""
    signal = normalize_rate_limit_signal(
        RATE_LIMITED_RETRYABLE_ERROR,
        provider=provider,
        source=RATE_SIGNAL_SOURCE_RETRY_REASON,
    )
    assert signal is not None
    return governor.observe(signal)


class TestRateGovernorSeam:
    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_rate_limited_retry_waits_and_records_one_event(self, mock_sleep):
        clock = SeamFakeClock()
        governor = _seam_governor(clock)
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return BuilderOutput(error=RATE_LIMITED_RETRYABLE_ERROR, provider="acme")
            return BuilderOutput(summary="ok", provider="acme")

        out = _call_with_retry(
            call_fn,
            result=result,
            role="builder",
            provider="acme",
            rate_governor=governor,
        )

        assert out.summary == "ok"
        assert calls[0] == 2
        assert result.retries_used == 1
        assert clock.sleeps  # the governor really waited, on its own injected sleep
        assert len(result.rate_limit_waits) == 1
        event = result.rate_limit_waits[0]
        assert event["provider"] == "acme"
        assert event["reason"] == RATE_LIMIT_REASON_RATE_LIMITED
        assert event["waited_s"] > 0.0

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_stop_during_the_wait_ends_the_call_without_counting_a_retry(self, mock_sleep):
        clock = SeamFakeClock()
        governor = _seam_governor(clock)
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            return BuilderOutput(error=RATE_LIMITED_RETRYABLE_ERROR, provider="acme")

        # The stop ARRIVES DURING the wait: nothing is stopped while the clock is at 0.0,
        # so the first call and the first wait slice both happen, and only then does the
        # operator's stop appear.
        def stop_check():
            return "stopped" if clock.now >= SEAM_POLL_SLICE_S else None

        out = _call_with_retry(
            call_fn,
            result=result,
            role="builder",
            provider="acme",
            stop_check=stop_check,
            rate_governor=governor,
        )

        assert out.error == RATE_LIMITED_RETRYABLE_ERROR
        assert calls[0] == 1  # the call count did NOT grow after the stop
        assert result.retries_used == 0
        assert result.retry_reasons == []
        # The seconds really were spent, so they are still recorded.
        assert len(result.rate_limit_waits) == 1
        assert result.rate_limit_waits[0]["waited_s"] > 0.0

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_empty_provider_skips_the_governor_entirely(self, mock_sleep):
        clock = SeamFakeClock()
        governor = _seam_governor(clock)
        # A cooldown DOES exist on the empty key, so a seam that consulted the governor
        # anyway would wait here — which is exactly the shared-bucket bug D5 forbids.
        _observe_cooldown(governor, "")
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return BuilderOutput(error=RATE_LIMITED_RETRYABLE_ERROR, provider="")
            return BuilderOutput(summary="ok", provider="")

        out = _call_with_retry(
            call_fn,
            result=result,
            role="builder",
            provider="",
            rate_governor=governor,
        )

        assert out.summary == "ok"
        assert result.retries_used == 1
        assert result.rate_limit_waits == []
        assert clock.sleeps == []
        assert governor.total_waited_s() == 0.0

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_no_governor_leaves_retry_behaviour_identical(self, mock_sleep):
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return BuilderOutput(error=RATE_LIMITED_RETRYABLE_ERROR, provider="acme")
            return BuilderOutput(summary="ok", provider="acme")

        out = _call_with_retry(call_fn, result=result, role="builder", provider="acme")

        assert out.summary == "ok"
        assert calls[0] == 2
        assert result.retries_used == 1
        assert len(result.retry_reasons) == 1
        assert result.rate_limit_waits == []

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_first_call_is_paced_by_a_cooldown_already_running(self, mock_sleep):
        clock = SeamFakeClock()
        governor = _seam_governor(clock)
        cooldown_s = _observe_cooldown(governor, "acme")
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            return BuilderOutput(summary="ok", provider="acme")

        out = _call_with_retry(
            call_fn,
            result=result,
            role="builder",
            provider="acme",
            rate_governor=governor,
        )

        # The seam PACES the first call, it never cancels it (DECISION F057 D3).
        assert out.summary == "ok"
        assert calls[0] == 1
        assert result.retries_used == 0
        assert len(result.rate_limit_waits) == 1
        assert result.rate_limit_waits[0]["waited_s"] == cooldown_s
        assert sum(clock.sleeps) == cooldown_s

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_bare_rate_limit_is_retried_when_a_governor_is_active(self, mock_sleep):
        """R-0373: without the seam's own rule this error never reaches the governor."""
        clock = SeamFakeClock()
        governor = _seam_governor(clock)
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return BuilderOutput(error=BARE_RATE_LIMIT_ERROR, provider="acme")
            return BuilderOutput(summary="ok", provider="acme")

        out = _call_with_retry(
            call_fn,
            result=result,
            role="builder",
            provider="acme",
            rate_governor=governor,
        )

        assert out.summary == "ok"
        assert calls[0] == 2
        assert result.retries_used == 1
        assert len(result.rate_limit_waits) == 1
        assert result.rate_limit_waits[0]["provider"] == "acme"
        assert result.rate_limit_waits[0]["reason"] == RATE_LIMIT_REASON_RATE_LIMITED
        assert result.rate_limit_waits[0]["waited_s"] > 0.0

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_bare_rate_limit_without_a_governor_is_still_not_retried(self, mock_sleep):
        """The pre-F057 path is untouched: no governor, no new retryable error class."""
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            return BuilderOutput(error=BARE_RATE_LIMIT_ERROR, provider="acme")

        out = _call_with_retry(call_fn, result=result, role="builder", provider="acme")

        assert out.error == BARE_RATE_LIMIT_ERROR
        assert calls[0] == 1
        assert result.retries_used == 0
        assert result.retry_reasons == []
        assert result.rate_limit_waits == []

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_review_reject_is_never_retried_even_with_a_governor(self, mock_sleep):
        """The reject carries the rate-limit wording ON PURPOSE.

        A reject with no ``error`` — the shape ``test_review_reject_no_retry`` above
        builds — returns at the loop's ``if not out.error`` before the reject exclusion
        is ever reached, so it cannot pin this property. Only a reject whose error text
        the governor WOULD call a rate limit reaches the guard, which is why R-0373's
        precedence rule names the reject explicitly instead of leaning on should_retry.
        """
        clock = SeamFakeClock()
        governor = _seam_governor(clock)
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            return ReviewerOutput(
                verdict="needs_repair",
                summary="Found issues",
                error=BARE_RATE_LIMIT_ERROR,
                provider="acme",
            )

        out = _call_with_retry(
            call_fn,
            result=result,
            role="reviewer",
            provider="acme",
            rate_governor=governor,
        )

        assert out.verdict == "needs_repair"
        assert calls[0] == 1
        assert result.retries_used == 0
        assert result.rate_limit_waits == []

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_parse_retry_rate_limit_is_paced_end_to_end(self, mock_sleep, tmp_path):
        """R-0374: the reviewer PARSE-RETRY call site is paced by the governor too.

        WHY the rate limit is wrapped as ``provider_error:`` — this is the whole reason
        the fixture looks the way it does. ``ReviewerOutput.verdict`` DEFAULTS to
        ``"blocked"``, and ``_call_with_retry`` computes ``is_reject`` from that field, so
        ANY ReviewerOutput carrying an error is a review reject and returns BEFORE the
        governor is consulted — unless the error starts with ``provider_error:``, the one
        shape the reject rule exempts. A bare ``429 Too Many Requests`` from a reviewer is
        therefore never retried and records no wait. The real claude-cli reviewer wraps
        every transport failure as ``provider_error: <Type>: <message>``, so the shape
        below is what production actually emits. R-0378 registers that this coupling is
        documented nowhere in the production code. The wording deliberately carries
        neither ``exited`` nor timeout wording, so no pre-existing transport predicate
        retries it and only the seam's own rate-limit rule can.
        """
        clock = SeamFakeClock()
        governor = _seam_governor(clock)

        class ParseRetryRateLimitedProvider(FakeProvider):
            """Malformed review, then a rate-limited parse retry, then a clean verdict."""

            def __init__(self) -> None:
                super().__init__()
                self.review_calls = 0

            def review(
                self,
                prompt: str,
                *,
                timeout_sec: int = 120,
                max_output_chars: int = 50000,
                resume: str | None = None,
            ) -> ReviewerOutput:
                self.review_calls += 1
                if self.review_calls == 1:
                    return ReviewerOutput(
                        verdict="",
                        raw_text="not valid json {{{",
                        error="malformed_output: no JSON found in reviewer response",
                        provider="fake",
                    )
                if self.review_calls == 2:
                    return ReviewerOutput(
                        error="provider_error: RuntimeError: 429 Too Many Requests",
                        provider="fake",
                    )
                return ReviewerOutput(
                    verdict="pass",
                    confidence="high",
                    summary="Parse retry recovered after the governor's wait.",
                    provider="fake",
                )

        provider = ParseRetryRateLimitedProvider()
        result = run_pingpong(
            "test goal",
            str(tmp_path),
            builder_name="fake",
            reviewer_provider=provider,
            rate_governor=governor,
        )

        # (a) the run really entered the single bounded parse retry...
        assert result.reviewer_parse_retry_count == 1
        # ...and the rate-limited parse-retry call really was retried.
        assert provider.review_calls == 3
        # (b) the seam retried it rather than returning the rate limit as terminal.
        assert result.retries_used >= 1
        # (c) the governor's wait is recorded, with its own provider and reason.
        assert result.rate_limit_waits
        for wait in result.rate_limit_waits:
            assert wait["provider"] == "fake"
            assert wait["reason"] == RATE_LIMIT_REASON_RATE_LIMITED
            assert wait["waited_s"] > 0.0
        # (d) nothing slept for real: the seconds were spent on the INJECTED clock.
        assert clock.sleeps
        assert sum(clock.sleeps) > 0.0


# ---------------------------------------------------------------------------
# F057 T003 — the report surfaces built on the recorded waits
#
# These live HERE with the rest of the F057 seam tests even though the code under
# test is the REPORT rather than the seam: this file already owns this feature's
# tests against pingpong_loop.py, and the five files that read the export stay an
# untouched regression signal that way.
# ---------------------------------------------------------------------------


def _paced_builder_result(clock: SeamFakeClock) -> PingPongResult:
    """A run that really was paced by the governor, through the only writer of the waits."""
    governor = _seam_governor(clock)
    result = PingPongResult()
    calls = [0]

    def call_fn():
        calls[0] += 1
        if calls[0] == 1:
            return BuilderOutput(error=BARE_RATE_LIMIT_ERROR, provider="acme")
        return BuilderOutput(summary="ok", provider="acme")

    _call_with_retry(
        call_fn,
        result=result,
        role="builder",
        provider="acme",
        rate_governor=governor,
    )
    assert result.rate_limit_waits  # the fixture is worthless if nothing waited
    return result


class TestRateLimitWaitExportSurface:
    """The exported run JSON carries the waits that ``_record_rate_limit_wait`` recorded."""

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_paced_run_exports_its_rate_limit_waits(self, mock_sleep):
        result = _paced_builder_result(SeamFakeClock())

        exported = export_pingpong_json(result)

        assert len(exported["rate_limit_waits"]) == len(result.rate_limit_waits)
        for wait in exported["rate_limit_waits"]:
            assert wait["provider"] == "acme"
            assert wait["reason"] == RATE_LIMIT_REASON_RATE_LIMITED
            assert wait["waited_s"] > 0.0

    @pytest.mark.unit
    def test_unpaced_run_exports_an_empty_list_not_a_missing_key(self):
        """The key is unconditional: absence is a contract a reader would have to branch on."""
        exported = export_pingpong_json(PingPongResult())

        assert "rate_limit_waits" in exported
        assert exported["rate_limit_waits"] == []


class TestRateLimitWaitSummarySurface:
    """The human summary says a run was paced, once, with the total and the count."""

    @pytest.mark.unit
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_paced_run_summary_reports_the_total_and_the_count(self, mock_sleep):
        result = _paced_builder_result(SeamFakeClock())
        expected_total_s = sum(w["waited_s"] for w in result.rate_limit_waits)

        rate_lines = [
            line
            for line in summarize_pingpong(result).splitlines()
            if line.startswith("Rate limits: ")
        ]

        assert len(rate_lines) == 1
        assert rate_lines[0] == (
            f"Rate limits: waited {expected_total_s:.1f}s "
            f"across {len(result.rate_limit_waits)} wait(s)"
        )

    @pytest.mark.unit
    def test_unpaced_run_summary_has_no_rate_limit_line(self):
        """A run nothing ever paced must not grow a line about pacing."""
        rate_lines = [
            line
            for line in summarize_pingpong(PingPongResult()).splitlines()
            if line.startswith("Rate limits: ")
        ]

        assert rate_lines == []
