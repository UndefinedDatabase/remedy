"""Tests for F003 T002 — provider integration + evidence for real token usage.

Covers:
  - ClaudeCliProvider._call parsing the JSON usage block into usage_actuals.
  - Heuristic fallback when the CLI output is not parseable JSON.
  - Loop-level token accounting and provider evidence carrying actuals.
  - token_truth confidence (high/mixed/low) and cost aggregation.
  - Manual operator repair never regressing to actual usage.
"""

from __future__ import annotations

import json
import stat
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import (
    PingPongResult,
    PingPongRound,
    ProviderAttempt,
    _aggregate_usage_actuals,
    _build_provider_evidence,
    _build_token_accounting,
)
from packages.orchestration.pingpong_provider import (
    BuilderOutput,
    ClaudeCliProvider,
    ReviewerOutput,
)
from packages.orchestration.token_truth import build_token_truth


def _cli_json_payload() -> dict:
    return {
        "type": "result",
        "is_error": False,
        "result": "Builder made changes\n- docs/README.md updated",
        "session_id": "sess-123",
        "total_cost_usd": 0.065,
        "num_turns": 1,
        "duration_ms": 3397,
        "usage": {
            "input_tokens": 6013,
            "cache_creation_input_tokens": 2788,
            "cache_read_input_tokens": 15079,
            "output_tokens": 42,
        },
    }


def _fake_claude_json_bin(tmp_path: Path, payload: dict) -> Path:
    bin_dir = tmp_path / "json_bin"
    bin_dir.mkdir()
    script = bin_dir / "claude"
    escaped = json.dumps(payload).replace("'", "'\\''")
    script.write_text(f"#!/bin/bash\nprintf '%s\\n' '{escaped}'\n")
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


def _fake_claude_text_bin(tmp_path: Path, text: str) -> Path:
    bin_dir = tmp_path / "text_bin"
    bin_dir.mkdir()
    script = bin_dir / "claude"
    escaped = text.replace("'", "'\\''")
    script.write_text(f"#!/bin/bash\nprintf '%s\\n' '{escaped}'\n")
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


# ---------------------------------------------------------------------------
# Provider: JSON usage parsing
# ---------------------------------------------------------------------------

class TestClaudeCliUsageParsing:
    def test_build_parses_usage_actuals(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, _cli_json_payload())))
        out = ClaudeCliProvider().build("do stuff")
        assert not out.error
        # Text comes from the result field, not the raw JSON envelope.
        assert "Builder made changes" in out.raw_text
        assert out.tokens_used == 6013 + 42
        assert out.usage_actuals is not None
        ua = out.usage_actuals
        assert ua["input_tokens"] == 6013
        assert ua["output_tokens"] == 42
        assert ua["cache_read"] == 15079
        assert ua["cache_creation"] == 2788
        assert ua["total_cost_usd"] == 0.065
        assert ua["session_id"] == "sess-123"
        assert ua["parse_source"] == "claude_cli_json"

    def test_review_parses_usage_actuals(self, monkeypatch, tmp_path):
        payload = _cli_json_payload()
        payload["result"] = json.dumps(
            {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"}
        )
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().review("review this")
        assert out.verdict == "pass"
        assert out.usage_actuals is not None
        assert out.usage_actuals["output_tokens"] == 42
        assert out.usage_actuals["parse_source"] == "claude_cli_json"

    def test_build_heuristic_fallback_on_non_json(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "PATH", str(_fake_claude_text_bin(tmp_path, "plain builder output, not json"))
        )
        out = ClaudeCliProvider().build("do stuff")
        assert not out.error
        assert "plain builder output" in out.raw_text
        assert out.tokens_used == 0
        assert out.usage_actuals is None


@pytest.fixture(autouse=True)
def _legacy_cli_reviewer(monkeypatch):
    """This file exercises CLI provider transport/usage/parse with pre-F005
    reviewer fixtures (legacy JSON, fake bins without --json-schema). F005
    native reviewer schema enforcement has its own dedicated tests, so here we
    pin the legacy free-text reviewer path explicitly."""
    monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")


class TestResultIndependentOfUsage:
    """F002/F003 finding: a valid JSON ``result`` is authoritative text even when
    the Usage block is missing/incomplete. Missing Usage only downgrades token
    accounting; it never invalidates a valid Builder/Reviewer result."""

    def test_builder_valid_result_no_usage(self, monkeypatch, tmp_path):
        payload = {
            "result": "Builder made changes\n- docs/README.md updated",
            "is_error": False,
        }
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().build("do stuff")
        assert not out.error
        assert "Builder made changes" in out.raw_text
        # Envelope key is not leaked into the text.
        assert '"result"' not in out.raw_text
        assert out.files_changed == ["docs/README.md"]
        assert out.usage_actuals is None
        assert out.actual_missing_reason == "usage_missing"
        assert out.tokens_used == 0

    def test_reviewer_valid_pass_no_usage(self, monkeypatch, tmp_path):
        payload = {
            "result": json.dumps(
                {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"}
            ),
            "is_error": False,
        }
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().review("review this")
        assert not out.error
        assert out.verdict == "pass"
        assert out.usage_actuals is None
        assert out.actual_missing_reason == "usage_missing"

    def test_valid_result_incomplete_usage_block(self, monkeypatch, tmp_path):
        payload = {
            "result": json.dumps(
                {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"}
            ),
            "is_error": False,
            "usage": {"input_tokens": 0},  # incomplete -> usage_missing
        }
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().review("review this")
        assert not out.error
        assert out.verdict == "pass"
        assert out.usage_actuals is None
        assert out.actual_missing_reason == "usage_missing"

    def test_non_json_raw_text_fallback(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "PATH", str(_fake_claude_text_bin(tmp_path, "just plain text output"))
        )
        out = ClaudeCliProvider().build("do stuff")
        assert not out.error
        assert "just plain text output" in out.raw_text
        assert out.usage_actuals is None
        assert out.actual_missing_reason == "parse_failed"

    def test_valid_usage_plus_result(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, _cli_json_payload())))
        out = ClaudeCliProvider().build("do stuff")
        assert not out.error
        assert "Builder made changes" in out.raw_text
        assert out.usage_actuals is not None
        assert out.usage_actuals["input_tokens"] == 6013
        assert out.actual_missing_reason == ""

    def test_is_error_true_is_provider_error(self, monkeypatch, tmp_path):
        payload = {
            "result": "ignored because is_error is true",
            "is_error": True,
        }
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().build("do stuff")
        assert out.error
        assert "provider_error" in out.error
        assert out.actual_missing_reason == "provider_error"

    def test_malformed_reviewer_rejected_independently(self, monkeypatch, tmp_path):
        # Valid JSON envelope, no Usage, but the result is NOT a valid reviewer
        # verdict -> still rejected as malformed, independent of measurement.
        payload = {"result": "this is not a verdict object", "is_error": False}
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().review("review this")
        assert out.error
        assert "malformed_output" in out.error


# ---------------------------------------------------------------------------
# Loop: token accounting + provider evidence
# ---------------------------------------------------------------------------

def _result_with_actuals() -> PingPongResult:
    builder = BuilderOutput(
        provider="claude-cli",
        tokens_used=42,
        usage_actuals={
            "input_tokens": 6013,
            "output_tokens": 42,
            "cache_read": 15079,
            "cache_creation": 2788,
            "total_cost_usd": 0.065,
            "session_id": "sess-123",
            "parse_source": "claude_cli_json",
        },
    )
    reviewer = ReviewerOutput(
        provider="claude-cli",
        verdict="pass",
        tokens_used=10,
        usage_actuals={
            "input_tokens": 1000,
            "output_tokens": 10,
            "cache_read": 0,
            "cache_creation": 0,
            "total_cost_usd": 0.01,
            "session_id": "sess-456",
            "parse_source": "claude_cli_json",
        },
    )
    rd = PingPongRound(round_number=1, builder_output=builder, reviewer_output=reviewer)
    return PingPongResult(
        builder_provider="claude-cli", reviewer_provider="claude-cli", rounds=[rd],
    )


class TestLoopTokenAccounting:
    def test_aggregate_usage_actuals(self):
        agg = _aggregate_usage_actuals(_result_with_actuals())
        assert agg is not None
        assert agg["input_tokens"] == 7013
        assert agg["output_tokens"] == 52
        assert agg["total_tokens"] == 7065
        assert agg["cache_read"] == 15079
        assert agg["total_cost_usd"] == 0.075
        assert agg["parse_source"] == "claude_cli_json"

    def test_token_accounting_high_confidence(self):
        acc = _build_token_accounting(_result_with_actuals())
        assert acc["measurement_confidence"] == "high"
        assert acc["usage_actuals"]["output_tokens"] == 52
        assert acc["parse_source"] == "claude_cli_json"

    def test_provider_evidence_carries_usage(self):
        ev = _build_provider_evidence(_result_with_actuals())
        assert ev["actual_available"] is True
        assert ev["usage"]["input_tokens"] == 7013
        assert ev["usage"]["output_tokens"] == 52
        assert ev["usage"]["cache_read_input_tokens"] == 15079
        assert ev["total_cost_usd"] == 0.075
        assert ev["parse_source"] == "claude_cli_json"

    def test_fake_provider_not_actual(self):
        rd = PingPongRound(
            round_number=1,
            builder_output=BuilderOutput(provider="fake", tokens_used=100),
        )
        result = PingPongResult(builder_provider="fake", rounds=[rd])
        acc = _build_token_accounting(result)
        assert acc["measurement_confidence"] == "low"
        assert acc["parse_source"] == "heuristic_fallback"
        ev = _build_provider_evidence(result)
        assert ev["actual_available"] is False


# ---------------------------------------------------------------------------
# token_truth: confidence + cost aggregation
# ---------------------------------------------------------------------------

def _seed(base: Path, tid: str, *, actual: bool, cost: float | None = None,
          execution_mode: str = "") -> None:
    d = base / "task_runs" / tid
    d.mkdir(parents=True, exist_ok=True)
    (d / "token_accounting.json").write_text(json.dumps({
        "kind": "actual" if actual else "estimated",
        "builder_prompt_tokens_estimated": 100,
        "reviewer_prompt_tokens_estimated": 50,
        "repair_prompt_tokens_estimated": 0,
    }))
    is_manual = execution_mode == "manual_operator_repair"
    pe: dict = {
        "schema_version": "1.0.0",
        "execution_mode": execution_mode or ("manual_operator_repair" if is_manual else "provider_backed"),
        "builder_provider": "claude-cli",
    }
    if is_manual:
        pe["provider_call_count"] = 0
    elif actual:
        pe["usage"] = {"input_tokens": 1000, "output_tokens": 500}
        pe["provider_call_count"] = 1
        pe["actual_call_count"] = 1
        if cost is not None:
            pe["total_cost_usd"] = cost
            pe["cost_call_count"] = 1
        else:
            pe["cost_call_count"] = 0
    else:
        pe["provider_call_count"] = 1
        pe["actual_call_count"] = 0
        pe["cost_call_count"] = 0
    (d / "provider_evidence.json").write_text(json.dumps(pe))


class TestTokenTruthConfidence:
    def test_all_actual_high(self, tmp_path):
        _seed(tmp_path, "T001", actual=True, cost=0.05)
        _seed(tmp_path, "T002", actual=True, cost=0.03)
        report = build_token_truth(str(tmp_path))
        assert report["measurement_confidence"] == "high"
        assert report["total_cost_usd"] == 0.08

    def test_some_actual_mixed(self, tmp_path):
        """One measured task + one real task without actuals: the partial cost
        sum is never labeled as the job total."""
        _seed(tmp_path, "T001", actual=True, cost=0.05)
        _seed(tmp_path, "T002", actual=False)
        report = build_token_truth(str(tmp_path))
        assert report["measurement_confidence"] == "mixed"
        assert report["actual_available"] is True
        assert report["total_cost_usd"] is None
        assert report["cost_coverage_complete"] is False
        assert report["cost_coverage_reason"] == "missing_actuals"

    def test_no_actual_low(self, tmp_path):
        _seed(tmp_path, "T001", actual=False)
        report = build_token_truth(str(tmp_path))
        assert report["measurement_confidence"] == "low"
        # Cost is never fabricated from estimates.
        assert report["total_cost_usd"] is None

    def test_manual_operator_repair_stays_low(self, tmp_path):
        _seed(tmp_path, "T001", actual=True, cost=0.05,
              execution_mode="manual_operator_repair")
        report = build_token_truth(str(tmp_path))
        assert report["actual_available"] is False
        assert report["measurement_confidence"] == "low"
        assert report["total_cost_usd"] is None
        assert report["per_task"]["T001"]["actual_available"] is False


# ---------------------------------------------------------------------------
# Provider: zero output_tokens, missing cost, cli_version
# ---------------------------------------------------------------------------

class TestProviderEdgeCases:
    def test_zero_output_tokens_still_sets_usage_actuals(self, monkeypatch, tmp_path):
        payload = _cli_json_payload()
        payload["usage"]["output_tokens"] = 0
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().build("do stuff")
        assert not out.error
        assert out.usage_actuals is not None
        assert out.usage_actuals["output_tokens"] == 0
        assert out.usage_actuals["input_tokens"] == 6013

    def test_missing_cost_does_not_fabricate(self, monkeypatch, tmp_path):
        payload = _cli_json_payload()
        del payload["total_cost_usd"]
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().build("do stuff")
        assert not out.error
        assert out.usage_actuals is not None
        assert out.usage_actuals["total_cost_usd"] is None

    def test_cli_version_in_usage_actuals(self, monkeypatch, tmp_path):
        payload = _cli_json_payload()
        payload["cli_version"] = "1.0.42"
        monkeypatch.setenv("PATH", str(_fake_claude_json_bin(tmp_path, payload)))
        out = ClaudeCliProvider().build("do stuff")
        assert not out.error
        assert out.usage_actuals is not None
        assert out.usage_actuals["cli_version"] == "1.0.42"


class TestLoopEdgeCases:
    def test_zero_output_tokens_actual_accounting(self):
        builder = BuilderOutput(
            provider="claude-cli",
            tokens_used=6013,
            usage_actuals={
                "input_tokens": 6013, "output_tokens": 0,
                "cache_read": 0, "cache_creation": 0,
                "total_cost_usd": 0.01, "session_id": "s1",
                "parse_source": "claude_cli_json",
            },
        )
        rd = PingPongRound(round_number=1, builder_output=builder)
        result = PingPongResult(builder_provider="claude-cli", rounds=[rd])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["output_tokens"] == 0
        assert agg["input_tokens"] == 6013
        acc = _build_token_accounting(result)
        assert acc["kind"] == "actual"
        assert acc["actual_tokens_available"] is True
        assert acc["measurement_confidence"] == "high"

    def test_no_actual_cost_gives_none(self):
        builder = BuilderOutput(
            provider="claude-cli",
            tokens_used=100,
            usage_actuals={
                "input_tokens": 100, "output_tokens": 50,
                "cache_read": 0, "cache_creation": 0,
                "total_cost_usd": None, "session_id": "s1",
                "parse_source": "claude_cli_json",
            },
        )
        rd = PingPongRound(round_number=1, builder_output=builder)
        result = PingPongResult(builder_provider="claude-cli", rounds=[rd])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["total_cost_usd"] is None

    def test_cli_version_in_provider_evidence(self):
        builder = BuilderOutput(
            provider="claude-cli",
            tokens_used=100,
            usage_actuals={
                "input_tokens": 100, "output_tokens": 50,
                "cache_read": 0, "cache_creation": 0,
                "total_cost_usd": 0.01, "session_id": "s1",
                "cli_version": "1.0.42",
                "parse_source": "claude_cli_json",
            },
        )
        rd = PingPongRound(round_number=1, builder_output=builder)
        result = PingPongResult(builder_provider="claude-cli", rounds=[rd])
        ev = _build_provider_evidence(result)
        assert ev["cli_version"] == "1.0.42"
        acc = _build_token_accounting(result)
        assert acc["cli_version"] == "1.0.42"

    def test_manual_operator_repair_remains_manual(self):
        rd = PingPongRound(round_number=1, builder_output=BuilderOutput(provider="operator"))
        result = PingPongResult(
            builder_provider="operator", rounds=[rd],
            execution_mode="manual_operator_repair",
        )
        acc = _build_token_accounting(result)
        assert acc["measurement_confidence"] == "low"
        assert acc["parse_source"] == "manual"
        ev = _build_provider_evidence(result)
        assert ev["actual_available"] is False
        assert ev["parse_source"] == "manual"


class TestProviderAttemptAccounting:
    """Fix 1: every provider invocation retained for usage accounting."""

    def test_reviewer_parse_retry_both_calls_counted(self):
        """Malformed reviewer + parse retry: both calls contribute to totals."""
        ua_first = {
            "input_tokens": 1000, "output_tokens": 200, "total_tokens": 1200,
            "cache_read": 0, "cache_creation": 0,
            "total_cost_usd": 0.01, "session_id": "s1",
        }
        ua_retry = {
            "input_tokens": 500, "output_tokens": 100, "total_tokens": 600,
            "cache_read": 0, "cache_creation": 0,
            "total_cost_usd": 0.005, "session_id": "s1",
        }
        result = PingPongResult(
            builder_provider="claude-cli",
            reviewer_provider="claude-cli",
            rounds=[PingPongRound(
                round_number=1,
                builder_output=BuilderOutput(
                    provider="claude-cli",
                    usage_actuals={"input_tokens": 2000, "output_tokens": 300,
                                   "total_cost_usd": 0.02},
                ),
                reviewer_output=ReviewerOutput(
                    provider="claude-cli", verdict="pass",
                    usage_actuals=ua_retry,
                    parse_retried=True, parse_retry_recovered=True,
                ),
            )],
            provider_attempts=[
                ProviderAttempt(role="builder", provider="claude-cli",
                                usage_actuals={"input_tokens": 2000, "output_tokens": 300,
                                               "total_cost_usd": 0.02}),
                ProviderAttempt(role="reviewer", provider="claude-cli",
                                usage_actuals=ua_first),
                ProviderAttempt(role="reviewer", provider="claude-cli",
                                usage_actuals=ua_retry, is_retry=True,
                                is_parse_retry=True),
            ],
        )
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 3
        assert agg["actual_call_count"] == 3
        assert agg["input_tokens"] == 2000 + 1000 + 500
        assert agg["output_tokens"] == 300 + 200 + 100
        assert agg["total_cost_usd"] == round(0.02 + 0.01 + 0.005, 6)

    def test_timeout_then_success(self):
        """Provider timeout followed by success: call_count=2, actual=1."""
        result = PingPongResult(
            builder_provider="claude-cli",
            reviewer_provider="claude-cli",
            rounds=[PingPongRound(
                round_number=1,
                builder_output=BuilderOutput(provider="claude-cli",
                    usage_actuals={"input_tokens": 500, "output_tokens": 50,
                                   "total_cost_usd": 0.005}),
                reviewer_output=ReviewerOutput(provider="claude-cli", verdict="pass",
                    usage_actuals={"input_tokens": 400, "output_tokens": 40,
                                   "total_cost_usd": 0.004}),
            )],
            provider_attempts=[
                ProviderAttempt(role="builder", provider="claude-cli",
                                error="timeout", actual_missing_reason="timeout"),
                ProviderAttempt(role="builder", provider="claude-cli",
                                usage_actuals={"input_tokens": 500, "output_tokens": 50,
                                               "total_cost_usd": 0.005},
                                is_retry=True),
                ProviderAttempt(role="reviewer", provider="claude-cli",
                                usage_actuals={"input_tokens": 400, "output_tokens": 40,
                                               "total_cost_usd": 0.004}),
            ],
        )
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 3
        assert agg["actual_call_count"] == 2
        assert agg["actual_coverage_complete"] is False
        assert agg["actual_missing_reasons"] == ["timeout"]

    def test_repair_round_calls_included(self):
        """Repair round builder+reviewer calls included in totals."""
        attempts = [
            ProviderAttempt(role="builder", provider="claude-cli",
                            usage_actuals={"input_tokens": 100, "output_tokens": 10,
                                           "total_cost_usd": 0.001}),
            ProviderAttempt(role="reviewer", provider="claude-cli",
                            usage_actuals={"input_tokens": 200, "output_tokens": 20,
                                           "total_cost_usd": 0.002}),
            ProviderAttempt(role="builder", provider="claude-cli",
                            usage_actuals={"input_tokens": 150, "output_tokens": 15,
                                           "total_cost_usd": 0.0015}),
            ProviderAttempt(role="reviewer", provider="claude-cli",
                            usage_actuals={"input_tokens": 250, "output_tokens": 25,
                                           "total_cost_usd": 0.0025}),
        ]
        result = PingPongResult(
            builder_provider="claude-cli",
            reviewer_provider="claude-cli",
            rounds=[
                PingPongRound(round_number=1, kind="initial",
                    builder_output=BuilderOutput(provider="claude-cli"),
                    reviewer_output=ReviewerOutput(provider="claude-cli", verdict="needs_repair")),
                PingPongRound(round_number=2, kind="repair",
                    builder_output=BuilderOutput(provider="claude-cli"),
                    reviewer_output=ReviewerOutput(provider="claude-cli", verdict="pass")),
            ],
            provider_attempts=attempts,
        )
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 4
        assert agg["actual_call_count"] == 4
        assert agg["input_tokens"] == 100 + 200 + 150 + 250
        assert agg["total_cost_usd"] == round(0.001 + 0.002 + 0.0015 + 0.0025, 6)
        assert agg["actual_coverage_complete"] is True
        assert agg["cost_coverage_complete"] is True


class TestPerCallFakeClassification:
    """Fix 2: fake classification per call/role, not per result."""

    def test_fake_builder_real_reviewer(self):
        """fake builder + claude-cli reviewer: reviewer actuals counted."""
        result = PingPongResult(
            builder_provider="fake",
            reviewer_provider="claude-cli",
            rounds=[PingPongRound(
                round_number=1,
                builder_output=BuilderOutput(provider="fake"),
                reviewer_output=ReviewerOutput(provider="claude-cli", verdict="pass",
                    usage_actuals={"input_tokens": 300, "output_tokens": 30,
                                   "total_cost_usd": 0.003}),
            )],
            provider_attempts=[
                ProviderAttempt(role="builder", provider="fake"),
                ProviderAttempt(role="reviewer", provider="claude-cli",
                                usage_actuals={"input_tokens": 300, "output_tokens": 30,
                                               "total_cost_usd": 0.003}),
            ],
        )
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 1
        assert agg["actual_call_count"] == 1
        assert agg["input_tokens"] == 300
        assert agg["total_cost_usd"] == 0.003

    def test_real_builder_fake_reviewer(self):
        """claude-cli builder + fake reviewer: builder actuals counted."""
        result = PingPongResult(
            builder_provider="claude-cli",
            reviewer_provider="fake",
            rounds=[PingPongRound(
                round_number=1,
                builder_output=BuilderOutput(provider="claude-cli",
                    usage_actuals={"input_tokens": 500, "output_tokens": 50,
                                   "total_cost_usd": 0.005}),
                reviewer_output=ReviewerOutput(provider="fake", verdict="pass"),
            )],
            provider_attempts=[
                ProviderAttempt(role="builder", provider="claude-cli",
                                usage_actuals={"input_tokens": 500, "output_tokens": 50,
                                               "total_cost_usd": 0.005}),
                ProviderAttempt(role="reviewer", provider="fake"),
            ],
        )
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 1
        assert agg["actual_call_count"] == 1
        assert agg["input_tokens"] == 500
        assert agg["total_cost_usd"] == 0.005

    def test_fake_builder_real_reviewer_token_accounting(self):
        """Token accounting marks actual_available when reviewer is real."""
        result = PingPongResult(
            builder_provider="fake",
            reviewer_provider="claude-cli",
            rounds=[PingPongRound(
                round_number=1,
                builder_output=BuilderOutput(provider="fake"),
                reviewer_output=ReviewerOutput(provider="claude-cli", verdict="pass",
                    usage_actuals={"input_tokens": 300, "output_tokens": 30,
                                   "total_cost_usd": 0.003}),
            )],
            provider_attempts=[
                ProviderAttempt(role="builder", provider="fake"),
                ProviderAttempt(role="reviewer", provider="claude-cli",
                                usage_actuals={"input_tokens": 300, "output_tokens": 30,
                                               "total_cost_usd": 0.003}),
            ],
        )
        acc = _build_token_accounting(result)
        assert acc["actual_tokens_available"] is True
        assert acc["measurement_confidence"] == "high"


# ---------------------------------------------------------------------------
# F003 findings fix — helpers for attempt-based scenarios
# ---------------------------------------------------------------------------

def _attempt(
    role: str,
    *,
    provider: str = "claude-cli",
    input_tokens: int | None = None,
    output_tokens: int = 0,
    cost: float | None = None,
    cache_read: int = 0,
    cache_creation: int = 0,
    error: str = "",
    missing_reason: str = "",
    is_retry: bool = False,
    is_parse_retry: bool = False,
) -> ProviderAttempt:
    """Build a ProviderAttempt; input_tokens=None means no parsed actuals."""
    ua = None
    if input_tokens is not None:
        ua = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_read": cache_read,
            "cache_creation": cache_creation,
            "total_cost_usd": cost,
            "session_id": "s1",
            "parse_source": "claude_cli_json",
        }
    return ProviderAttempt(
        role=role, provider=provider, usage_actuals=ua,
        actual_missing_reason=missing_reason, error=error,
        is_retry=is_retry, is_parse_retry=is_parse_retry,
    )


def _result_from_attempts(attempts: list[ProviderAttempt],
                          *, builder_provider: str = "claude-cli",
                          reviewer_provider: str = "claude-cli") -> PingPongResult:
    return PingPongResult(
        builder_provider=builder_provider,
        reviewer_provider=reviewer_provider,
        rounds=[PingPongRound(round_number=1)],
        provider_attempts=list(attempts),
    )


class TestCostCompleteness:
    """F003 findings Fix Block 1: total cost only when every real call has
    actuals AND provider-reported cost; partial sums never labeled as total."""

    def test_one_call_missing_actuals_cost_null(self):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01),
            _attempt("reviewer", missing_reason="parse_failed"),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 2
        assert agg["actual_call_count"] == 1
        assert agg["cost_call_count"] == 1
        assert agg["actual_coverage_complete"] is False
        assert agg["cost_coverage_complete"] is False
        assert agg["total_cost_usd"] is None
        assert agg["cost_coverage_reason"] == "missing_actuals"

    def test_one_call_missing_cost_cost_null(self):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01),
            _attempt("reviewer", input_tokens=200, output_tokens=20, cost=None),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 2
        assert agg["actual_call_count"] == 2
        assert agg["cost_call_count"] == 1
        assert agg["actual_coverage_complete"] is True
        assert agg["cost_coverage_complete"] is False
        assert agg["total_cost_usd"] is None
        assert agg["cost_coverage_reason"] == "missing_provider_cost"

    def test_all_calls_covered_cost_is_sum(self):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01),
            _attempt("reviewer", input_tokens=200, output_tokens=20, cost=0.02),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["actual_coverage_complete"] is True
        assert agg["cost_coverage_complete"] is True
        assert agg["total_cost_usd"] == 0.03
        assert agg["cost_coverage_reason"] is None

    def test_no_actuals_still_counts_real_calls_and_evidence_honest(self):
        """Two real provider attempts, neither exposing actuals (e.g. both
        failed / usage-limited). The record is NOT dropped: provider coverage
        and the exact missing reasons are preserved, while actual_available is
        false and no partial cost is labeled as the total."""
        result = _result_from_attempts([
            _attempt("builder", missing_reason="parse_failed"),
            _attempt("reviewer", missing_reason="usage_missing"),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["actual_available"] is False
        assert agg["provider_call_count"] == 2
        assert agg["actual_call_count"] == 0
        assert agg["cost_call_count"] == 0
        assert agg["actual_coverage_complete"] is False
        assert agg["cost_coverage_complete"] is False
        assert agg["total_cost_usd"] is None
        assert agg["actual_missing_reasons"] == ["parse_failed", "usage_missing"]
        ev = _build_provider_evidence(result)
        assert ev["actual_available"] is False
        assert ev["provider_call_count"] == 2
        assert ev["actual_call_count"] == 0
        assert ev["cost_call_count"] == 0
        assert ev.get("total_cost_usd") is None
        assert "usage" not in ev
        assert ev["actual_missing_reasons"] == ["parse_failed", "usage_missing"]

    def test_mixed_fake_and_real_roles_cost_complete(self):
        """Fake calls are not real provider calls; the real call's full
        coverage makes its cost the truthful total."""
        result = _result_from_attempts([
            _attempt("builder", provider="fake"),
            _attempt("reviewer", input_tokens=300, output_tokens=30, cost=0.003),
        ], builder_provider="fake")
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 1
        assert agg["cost_coverage_complete"] is True
        assert agg["total_cost_usd"] == 0.003
        assert agg["cost_coverage_reason"] is None

    def test_missing_actuals_and_cost_reason(self):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=None),
            _attempt("reviewer", missing_reason="parse_failed"),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["total_cost_usd"] is None
        assert agg["cost_coverage_reason"] == "missing_actuals_and_provider_cost"


class TestProviderCallCountScenarios:
    """F003 findings Fix Block 2: provider_call_count counts every real
    provider attempt (initial, retries, parse retries, repair rounds)."""

    def _truth_from_result(self, base: Path, result: PingPongResult,
                           *, total_prompts: int) -> dict:
        d = base / "task_runs" / "T001"
        d.mkdir(parents=True, exist_ok=True)
        (d / "token_accounting.json").write_text(json.dumps({
            "kind": "actual",
            "builder_prompt_tokens_estimated": 100,
            "reviewer_prompt_tokens_estimated": 50,
            "repair_prompt_tokens_estimated": 0,
        }))
        (d / "provider_evidence.json").write_text(
            json.dumps(_build_provider_evidence(result)))
        (base / "prompt_trace_summary.json").write_text(json.dumps({
            "total_prompts": total_prompts,
        }))
        return build_token_truth(str(base))

    def test_builder_reviewer_parse_retry(self, tmp_path):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01),
            _attempt("reviewer", input_tokens=200, output_tokens=20, cost=0.02),
            _attempt("reviewer", input_tokens=50, output_tokens=5, cost=0.005,
                     is_retry=True, is_parse_retry=True),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg["provider_call_count"] == 3
        assert agg["actual_call_count"] == 3
        truth = self._truth_from_result(tmp_path, result, total_prompts=2)
        assert truth["provider_call_count"] == 3
        assert truth["prompt_trace_count"] == 2

    def test_builder_transport_retry(self, tmp_path):
        result = _result_from_attempts([
            _attempt("builder", error="timeout", missing_reason="timeout"),
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01,
                     is_retry=True),
            _attempt("reviewer", input_tokens=200, output_tokens=20, cost=0.02),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg["provider_call_count"] == 3
        assert agg["actual_call_count"] == 2
        assert agg["actual_call_count"] <= agg["provider_call_count"]
        truth = self._truth_from_result(tmp_path, result, total_prompts=2)
        assert truth["provider_call_count"] == 3

    def test_reviewer_transport_retry(self, tmp_path):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01),
            _attempt("reviewer", error="exited nonzero", missing_reason="nonzero_exit"),
            _attempt("reviewer", input_tokens=200, output_tokens=20, cost=0.02,
                     is_retry=True),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg["provider_call_count"] == 3
        assert agg["actual_call_count"] == 2
        truth = self._truth_from_result(tmp_path, result, total_prompts=2)
        assert truth["provider_call_count"] == 3

    def test_repair_builder_and_repair_reviewer(self, tmp_path):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01),
            _attempt("reviewer", input_tokens=200, output_tokens=20, cost=0.02),
            _attempt("builder", input_tokens=150, output_tokens=15, cost=0.015),
            _attempt("reviewer", input_tokens=250, output_tokens=25, cost=0.025),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg["provider_call_count"] == 4
        assert agg["actual_call_count"] == 4
        truth = self._truth_from_result(tmp_path, result, total_prompts=4)
        assert truth["provider_call_count"] == 4

    def test_fake_builder_real_reviewer_count(self, tmp_path):
        result = _result_from_attempts([
            _attempt("builder", provider="fake"),
            _attempt("reviewer", input_tokens=300, output_tokens=30, cost=0.003),
        ], builder_provider="fake")
        agg = _aggregate_usage_actuals(result)
        assert agg["provider_call_count"] == 1
        assert agg["actual_call_count"] == 1
        truth = self._truth_from_result(tmp_path, result, total_prompts=2)
        assert truth["provider_call_count"] == 1

    def test_real_builder_fake_reviewer_count(self, tmp_path):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=500, output_tokens=50, cost=0.005),
            _attempt("reviewer", provider="fake"),
        ], reviewer_provider="fake")
        agg = _aggregate_usage_actuals(result)
        assert agg["provider_call_count"] == 1
        assert agg["actual_call_count"] == 1
        truth = self._truth_from_result(tmp_path, result, total_prompts=2)
        assert truth["provider_call_count"] == 1


class TestRoleActualTotals:
    """F003 findings Fix Block 3: role-specific actual totals from every
    recorded real ProviderAttempt, not only the final stored round result."""

    def test_parse_retry_both_reviewer_usages_counted(self):
        """First reviewer call malformed with valid usage; parse retry succeeds
        with additional usage. Both reviewer usages must be present."""
        result = PingPongResult(
            builder_provider="claude-cli",
            reviewer_provider="claude-cli",
            rounds=[PingPongRound(
                round_number=1,
                builder_output=BuilderOutput(
                    provider="claude-cli",
                    usage_actuals={"input_tokens": 1000, "output_tokens": 100,
                                   "total_cost_usd": 0.01},
                ),
                # Only the retry output is stored on the round.
                reviewer_output=ReviewerOutput(
                    provider="claude-cli", verdict="pass",
                    usage_actuals={"input_tokens": 400, "output_tokens": 40,
                                   "total_cost_usd": 0.004},
                    parse_retried=True, parse_retry_recovered=True,
                ),
            )],
            provider_attempts=[
                _attempt("builder", input_tokens=1000, output_tokens=100, cost=0.01),
                _attempt("reviewer", input_tokens=800, output_tokens=80, cost=0.008),
                _attempt("reviewer", input_tokens=400, output_tokens=40, cost=0.004,
                         is_retry=True, is_parse_retry=True),
            ],
        )
        acc = _build_token_accounting(result)
        assert acc["builder_tokens_actual"] == 1000 + 100
        # Both reviewer usages: malformed-but-measured first call + parse retry.
        assert acc["reviewer_tokens_actual"] == (800 + 80) + (400 + 40)
        agg = _aggregate_usage_actuals(result)
        assert (acc["builder_tokens_actual"] + acc["reviewer_tokens_actual"]
                == agg["total_tokens"])

    def test_role_totals_include_retries_and_repairs(self):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01),
            _attempt("builder", input_tokens=120, output_tokens=12, cost=0.012,
                     is_retry=True),
            _attempt("reviewer", input_tokens=200, output_tokens=20, cost=0.02),
            _attempt("builder", input_tokens=150, output_tokens=15, cost=0.015),
            _attempt("reviewer", input_tokens=250, output_tokens=25, cost=0.025),
        ])
        acc = _build_token_accounting(result)
        assert acc["builder_tokens_actual"] == (100 + 10) + (120 + 12) + (150 + 15)
        assert acc["reviewer_tokens_actual"] == (200 + 20) + (250 + 25)
        agg = _aggregate_usage_actuals(result)
        assert (acc["builder_tokens_actual"] + acc["reviewer_tokens_actual"]
                == agg["total_tokens"])

    def test_cache_tokens_reconcile_by_role(self):
        result = _result_from_attempts([
            _attempt("builder", input_tokens=100, output_tokens=10, cost=0.01,
                     cache_read=500, cache_creation=200),
            _attempt("reviewer", input_tokens=200, output_tokens=20, cost=0.02,
                     cache_read=300, cache_creation=100),
            _attempt("reviewer", input_tokens=50, output_tokens=5, cost=0.005,
                     cache_read=30, cache_creation=10, is_retry=True,
                     is_parse_retry=True),
        ])
        acc = _build_token_accounting(result)
        agg = _aggregate_usage_actuals(result)
        assert acc["builder_cache_read_tokens_actual"] == 500
        assert acc["builder_cache_creation_tokens_actual"] == 200
        assert acc["reviewer_cache_read_tokens_actual"] == 300 + 30
        assert acc["reviewer_cache_creation_tokens_actual"] == 100 + 10
        assert (acc["builder_cache_read_tokens_actual"]
                + acc["reviewer_cache_read_tokens_actual"] == agg["cache_read"])
        assert (acc["builder_cache_creation_tokens_actual"]
                + acc["reviewer_cache_creation_tokens_actual"]
                == agg["cache_creation"])

    def test_manual_repair_never_counted_as_usage(self):
        result = PingPongResult(
            builder_provider="operator",
            reviewer_provider="operator",
            rounds=[PingPongRound(round_number=1)],
            provider_attempts=[
                # Stray attempt with usage must not count under manual mode.
                _attempt("builder", provider="operator",
                         input_tokens=999, output_tokens=99, cost=1.0),
            ],
            execution_mode="manual_operator_repair",
        )
        acc = _build_token_accounting(result)
        assert acc["actual_tokens_available"] is False
        assert "builder_tokens_actual" not in acc
        assert acc["parse_source"] == "manual"
        ev = _build_provider_evidence(result)
        assert ev["actual_available"] is False

    def test_final_attempt_not_double_counted(self):
        """The round-stored reviewer output equals the last attempt; totals come
        from attempts only, so the final call appears exactly once."""
        final_ua = {"input_tokens": 400, "output_tokens": 40,
                    "total_cost_usd": 0.004}
        result = PingPongResult(
            builder_provider="claude-cli",
            reviewer_provider="claude-cli",
            rounds=[PingPongRound(
                round_number=1,
                reviewer_output=ReviewerOutput(
                    provider="claude-cli", verdict="pass", usage_actuals=final_ua,
                ),
            )],
            provider_attempts=[
                _attempt("reviewer", input_tokens=400, output_tokens=40, cost=0.004),
            ],
        )
        acc = _build_token_accounting(result)
        assert acc["reviewer_tokens_actual"] == 440
        agg = _aggregate_usage_actuals(result)
        assert agg["provider_call_count"] == 1
        assert agg["total_tokens"] == 440


class TestNoActualProviderAttemptAccounting:
    """F003 findings fix: a real provider attempt that exposes no actuals — a
    provider failure or usage/session-limit — must remain counted. The record is
    returned (never collapsed to None) whenever at least one real provider
    attempt exists; actual_available is separately false; provider coverage and
    the exact deduplicated missing reasons are preserved; a partial or absent
    cost is never labeled as the total; and token_truth consumes the real
    attempt counts instead of the one-call-per-task fallback."""

    def _seed_truth(self, base: Path, result: PingPongResult,
                    *, total_prompts: int) -> dict:
        d = base / "task_runs" / "T001"
        d.mkdir(parents=True, exist_ok=True)
        (d / "token_accounting.json").write_text(json.dumps({
            "kind": "estimated",
            "builder_prompt_tokens_estimated": 100,
            "reviewer_prompt_tokens_estimated": 50,
            "repair_prompt_tokens_estimated": 0,
        }))
        (d / "provider_evidence.json").write_text(
            json.dumps(_build_provider_evidence(result)))
        (base / "prompt_trace_summary.json").write_text(json.dumps({
            "total_prompts": total_prompts,
        }))
        return build_token_truth(str(base))

    def test_two_real_failed_attempts_no_actuals(self, tmp_path):
        """Case 1: initial builder + builder retry, both failed with no actuals.
        provider_call_count stays 2; token_truth must not fall back to 1."""
        result = _result_from_attempts([
            _attempt("builder", missing_reason="usage_limit_reached"),
            _attempt("builder", missing_reason="usage_limit_reached", is_retry=True),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["actual_available"] is False
        assert agg["provider_call_count"] == 2
        assert agg["actual_call_count"] == 0
        assert agg["cost_call_count"] == 0
        assert agg["total_cost_usd"] is None
        assert agg["actual_missing_reasons"] == ["usage_limit_reached"]
        acc = _build_token_accounting(result)
        assert acc["kind"] == "estimated"
        assert acc["actual_tokens_available"] is False
        assert acc["measurement_confidence"] == "low"
        assert acc["provider_call_count"] == 2
        assert acc["actual_call_count"] == 0
        assert acc["parse_source"] == "heuristic_fallback"
        truth = self._seed_truth(tmp_path, result, total_prompts=1)
        # The authoritative count is the real attempt count (2), never the
        # one-provider-call-per-task fallback that would report 1.
        assert truth["provider_call_count"] == 2
        assert truth["actual_call_count"] == 0
        assert truth["actual_available"] is False

    def test_initial_failed_then_successful_retry(self):
        """Case 2: first call fails with no actuals, retry succeeds with actuals.
        Both counted; actual_available true but coverage incomplete."""
        result = _result_from_attempts([
            _attempt("builder", missing_reason="timeout"),
            _attempt("builder", input_tokens=500, output_tokens=50, cost=0.005,
                     is_retry=True),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["actual_available"] is True
        assert agg["provider_call_count"] == 2
        assert agg["actual_call_count"] == 1
        assert agg["actual_coverage_complete"] is False
        # Partial coverage: the single measured cost is never the job total.
        assert agg["total_cost_usd"] is None
        assert agg["cost_coverage_reason"] == "missing_actuals"
        assert agg["actual_missing_reasons"] == ["timeout"]
        ev = _build_provider_evidence(result)
        assert ev["actual_available"] is True
        assert ev["provider_call_count"] == 2
        assert ev["actual_call_count"] == 1
        assert ev["total_cost_usd"] is None

    def test_specific_missing_reason_propagated(self):
        """Case 3: a specific reason is preserved verbatim, never collapsed to
        the generic 'provider_actuals_unavailable'."""
        result = _result_from_attempts([
            _attempt("builder", missing_reason="usage_limit_reached"),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["actual_missing_reasons"] == ["usage_limit_reached"]
        assert "provider_actuals_unavailable" not in agg["actual_missing_reasons"]
        ev = _build_provider_evidence(result)
        assert ev["actual_missing_reasons"] == ["usage_limit_reached"]

    def test_multiple_distinct_missing_reasons_deduped(self):
        """Case 4: distinct reasons preserved and deduplicated in order."""
        result = _result_from_attempts([
            _attempt("builder", missing_reason="timeout"),
            _attempt("reviewer", missing_reason="parse_failed"),
            _attempt("reviewer", missing_reason="timeout", is_retry=True),
        ])
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["provider_call_count"] == 3
        assert agg["actual_call_count"] == 0
        assert agg["actual_missing_reasons"] == ["timeout", "parse_failed"]

    def test_fake_builder_failed_real_reviewer(self):
        """Case 5: fake builder is not a real call; a failed real reviewer is
        counted even though it exposes no actuals."""
        result = _result_from_attempts([
            _attempt("builder", provider="fake"),
            _attempt("reviewer", missing_reason="nonzero_exit"),
        ], builder_provider="fake")
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["actual_available"] is False
        assert agg["provider_call_count"] == 1
        assert agg["actual_call_count"] == 0
        assert agg["actual_missing_reasons"] == ["nonzero_exit"]
        ev = _build_provider_evidence(result)
        assert ev["actual_available"] is False
        assert ev["provider_call_count"] == 1

    def test_failed_real_builder_fake_reviewer(self):
        """Case 6: symmetric — failed real builder counted, fake reviewer not."""
        result = _result_from_attempts([
            _attempt("builder", missing_reason="empty_input"),
            _attempt("reviewer", provider="fake"),
        ], reviewer_provider="fake")
        agg = _aggregate_usage_actuals(result)
        assert agg is not None
        assert agg["actual_available"] is False
        assert agg["provider_call_count"] == 1
        assert agg["actual_call_count"] == 0
        assert agg["actual_missing_reasons"] == ["empty_input"]

    def test_no_real_provider_calls_returns_none(self):
        """Case 7: every attempt fake — no real provider call at all — so the
        aggregate is None and evidence stays honestly estimated."""
        result = _result_from_attempts([
            _attempt("builder", provider="fake"),
            _attempt("reviewer", provider="fake"),
        ], builder_provider="fake", reviewer_provider="fake")
        assert _aggregate_usage_actuals(result) is None
        ev = _build_provider_evidence(result)
        assert ev["actual_available"] is False
        assert "provider_call_count" not in ev
        acc = _build_token_accounting(result)
        assert acc["actual_tokens_available"] is False
        assert acc["measurement_confidence"] == "low"

    def test_manual_operator_repair_not_counted(self):
        """Case 8: manual operator repair is never provider usage; a stray
        attempt with usage must not be counted."""
        result = PingPongResult(
            builder_provider="operator",
            reviewer_provider="operator",
            rounds=[PingPongRound(round_number=1)],
            provider_attempts=[
                _attempt("builder", provider="operator",
                         input_tokens=999, output_tokens=99, cost=1.0),
            ],
            execution_mode="manual_operator_repair",
        )
        acc = _build_token_accounting(result)
        assert acc["actual_tokens_available"] is False
        assert acc["parse_source"] == "manual"
        assert "provider_call_count" not in acc
        ev = _build_provider_evidence(result)
        assert ev["actual_available"] is False
        assert ev["parse_source"] == "manual"
        assert "provider_call_count" not in ev


class TestManualPECrossFieldRejection:
    """Round 40 F3: trust-bearing claims on a manual PE must be rejected, not silently discarded."""

    def test_combined_contradiction_blocks(self):
        from packages.orchestration.provider_token_evidence import validate_provider_token_evidence
        from packages.orchestration.token_truth import TokenEvidenceError
        pe = {
            "schema_version": "1.0.0",
            "task_id": "T999",
            "execution_mode": "manual_operator_repair",
            "provider_call_count": 0,
            "provider_attempts": [{"call_id": "claimed-call", "status": "success"}],
            "actual_provider_available": True,
            "prompt_trace_available": True,
            "completion_provider_call_count": 999,
            "reviewer_provider": "forged-provider",
            "cli_versions": {"reviewer": 123},
        }
        with pytest.raises(TokenEvidenceError):
            validate_provider_token_evidence(pe, "test")

    def test_provider_attempts_on_manual_blocks(self):
        from packages.orchestration.provider_token_evidence import validate_provider_token_evidence
        from packages.orchestration.token_truth import TokenEvidenceError
        pe = {
            "schema_version": "1.0.0",
            "execution_mode": "manual_operator_repair",
            "provider_call_count": 0,
            "provider_attempts": [{"call_id": "x"}],
        }
        with pytest.raises(TokenEvidenceError, match="provider_attempts"):
            validate_provider_token_evidence(pe, "test")

    def test_actual_provider_available_on_manual_blocks(self):
        from packages.orchestration.provider_token_evidence import validate_provider_token_evidence
        from packages.orchestration.token_truth import TokenEvidenceError
        pe = {
            "schema_version": "1.0.0",
            "execution_mode": "manual_operator_repair",
            "provider_call_count": 0,
            "actual_provider_available": True,
        }
        with pytest.raises(TokenEvidenceError, match="actual_provider_available"):
            validate_provider_token_evidence(pe, "test")

    def test_prompt_trace_available_on_manual_blocks(self):
        from packages.orchestration.provider_token_evidence import validate_provider_token_evidence
        from packages.orchestration.token_truth import TokenEvidenceError
        pe = {
            "schema_version": "1.0.0",
            "execution_mode": "manual_operator_repair",
            "provider_call_count": 0,
            "prompt_trace_available": True,
        }
        with pytest.raises(TokenEvidenceError, match="prompt_trace_available"):
            validate_provider_token_evidence(pe, "test")

    def test_completion_provider_call_count_nonzero_blocks(self):
        from packages.orchestration.provider_token_evidence import validate_provider_token_evidence
        from packages.orchestration.token_truth import TokenEvidenceError
        pe = {
            "schema_version": "1.0.0",
            "execution_mode": "manual_operator_repair",
            "provider_call_count": 0,
            "completion_provider_call_count": 5,
        }
        with pytest.raises(TokenEvidenceError, match="completion_provider_call_count"):
            validate_provider_token_evidence(pe, "test")

    def test_prior_execution_dict_on_manual_accepted(self):
        from packages.orchestration.provider_token_evidence import validate_provider_token_evidence
        pe = {
            "schema_version": "1.0.0",
            "execution_mode": "manual_operator_repair",
            "provider_call_count": 0,
            "prior_execution": {"provider_call_count": 1},
        }
        validate_provider_token_evidence(pe, "test")

    def test_prior_execution_non_dict_on_manual_blocks(self):
        from packages.orchestration.provider_token_evidence import validate_provider_token_evidence
        from packages.orchestration.token_truth import TokenEvidenceError
        pe = {
            "schema_version": "1.0.0",
            "execution_mode": "manual_operator_repair",
            "provider_call_count": 0,
            "prior_execution": "stale",
        }
        with pytest.raises(TokenEvidenceError, match="prior_execution"):
            validate_provider_token_evidence(pe, "test")

    def test_task_id_mismatch_blocks_in_token_truth(self, tmp_path):
        from packages.orchestration.token_truth import TokenEvidenceError, build_token_truth
        td = tmp_path / "task_runs" / "T001"
        td.mkdir(parents=True)
        pe = {
            "schema_version": "1.0.0",
            "task_id": "T999",
            "execution_mode": "manual_operator_repair",
            "provider_call_count": 0,
        }
        (td / "provider_evidence.json").write_text(json.dumps(pe))
        (td / "token_accounting.json").write_text(json.dumps({
            "task_id": "T001", "kind": "manual", "reason": "manual",
            "actual_available": False, "actual_tokens_available": False,
            "provider_call_count": 0, "estimated_total_tokens": 0,
            "builder_prompt_tokens_estimated": 0, "reviewer_prompt_tokens_estimated": 0,
            "repair_prompt_tokens_estimated": 0,
        }))
        with pytest.raises(TokenEvidenceError, match="does not match containing directory"):
            build_token_truth(str(tmp_path))
