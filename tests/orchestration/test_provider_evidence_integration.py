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
    pe: dict = {"builder_provider": "claude-cli"}
    if execution_mode:
        pe["execution_mode"] = execution_mode
    if actual:
        pe["usage"] = {"input_tokens": 1000, "output_tokens": 500}
        if cost is not None:
            pe["total_cost_usd"] = cost
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

