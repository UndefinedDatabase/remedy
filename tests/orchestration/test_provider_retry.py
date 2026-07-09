"""Tests for F001 retry behavior and timeout profile integration.

Covers:
  - Fake provider that times out once then succeeds → retries_used=1
  - retry_reasons records the failure
  - Review reject does NOT trigger retry
  - Timeout profile wires correct seconds into builder/reviewer
  - Attempts are separately recorded in evidence
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any
from unittest.mock import patch

import pytest

from packages.orchestration.pingpong_loop import (
    PingPongResult,
    _call_with_retry,
    run_pingpong,
)
from packages.orchestration.pingpong_provider import (
    BuilderOutput,
    FakeProvider,
    ReviewerOutput,
)
from packages.orchestration.provider_timeouts import (
    PROFILES,
    compute_timeout,
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
    ) -> BuilderOutput:
        self._build_attempts += 1
        if self._build_attempts == 1:
            return BuilderOutput(
                error="provider_error: TimeoutExpired: timed out after 120s",
                provider="fake",
            )
        return super().build(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars)


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
    ) -> ReviewerOutput:
        self._review_attempts += 1
        if self._review_attempts == 1:
            return ReviewerOutput(
                error="provider_error: TimeoutExpired: reviewer timed out",
                provider="fake",
            )
        return super().review(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars)


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
    ) -> BuilderOutput:
        self._build_attempts += 1
        if self._build_attempts == 1:
            return BuilderOutput(
                error="provider_error: RuntimeError: claude CLI exited 1: internal error",
                provider="fake",
            )
        return super().build(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars)


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
