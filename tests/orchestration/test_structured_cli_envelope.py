"""F005 correction — native Claude CLI structured_output envelope handling.

All cases use recorded envelopes and a mocked subprocess. No provider call.
"""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from packages.orchestration.pingpong_provider import ClaudeCliProvider
from packages.orchestration.token_actuals import (
    STRUCTURED_RETRY_EXHAUSTED_SUBTYPE,
    parse_cli_envelope,
)

_SO = {"schema_v": "rv1", "verdict": "pass", "findings": [],
       "confidence": "high", "summary": "ok"}


def _envelope(**kw) -> str:
    base = {"type": "result", "subtype": "success", "is_error": False}
    base.update(kw)
    return json.dumps(base)


def _review(stdout: str, *, rc: int = 0, stderr: str = ""):
    prov = ClaudeCliProvider()
    prov._claude_path = "/fake/claude"
    prov._cli_version = "1.0.0 (test)"
    prov._cli_version_resolved = True
    proc = MagicMock(returncode=rc, stdout=stdout, stderr=stderr)
    with patch("packages.orchestration.pingpong_provider.subprocess.run", return_value=proc):
        return prov.review("REVIEW BASE")


# ---------------------------------------------------------------------------
# Envelope parser (single parse point)
# ---------------------------------------------------------------------------

class TestEnvelopeParser:
    def test_object_structured_output_extracted(self):
        e = parse_cli_envelope(_envelope(structured_output=_SO))
        assert e.has_structured_output and e.structured_output["verdict"] == "pass"

    def test_usage_and_cost_retained_even_on_error(self):
        e = parse_cli_envelope(_envelope(
            subtype=STRUCTURED_RETRY_EXHAUSTED_SUBTYPE, is_error=True,
            usage={"input_tokens": 50, "output_tokens": 5}, total_cost_usd=0.001))
        assert e.structured_retry_exhausted
        assert e.usage_actuals is not None
        assert e.usage_actuals.total_cost_usd == 0.001

    def test_legacy_result_string_still_read(self):
        e = parse_cli_envelope(_envelope(result="plain text"))
        assert not e.has_structured_output and e.result_text == "plain text"


# ---------------------------------------------------------------------------
# Finding 1 — non-stream structured_output extraction and classification
# ---------------------------------------------------------------------------

class TestJsonStructuredOutput:
    def test_1_success_object_structured_output(self):
        out = _review(_envelope(structured_output=_SO))
        assert out.verdict == "pass" and not out.error and out.error_class == ""
        assert out.schema_v == "rv1"

    def test_2_structured_output_with_usage_and_cost(self):
        out = _review(_envelope(structured_output=_SO,
                                usage={"input_tokens": 120, "output_tokens": 8},
                                total_cost_usd=0.003))
        assert out.verdict == "pass"
        assert out.usage_actuals["input_tokens"] == 120
        assert out.usage_actuals["total_cost_usd"] == 0.003

    def test_3_structured_output_preferred_over_legacy_result(self):
        # structured mode: structured_output wins over a (misleading) result string.
        out = _review(_envelope(structured_output=_SO, result='{"verdict":"blocked"}'))
        assert out.verdict == "pass"

    def test_4_legacy_non_schema_call_uses_result(self, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        out = _review(_envelope(result=json.dumps(
            {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"})))
        assert out.verdict == "pass"

    def test_5_success_missing_structured_output_is_parse(self):
        out = _review(_envelope(usage={"input_tokens": 5, "output_tokens": 1}))
        assert out.error_class == "parse"
        assert out.error.startswith("malformed_output:")
        assert out.usage_actuals is not None  # usage retained

    def test_6_malformed_structured_output_is_parse(self):
        out = _review(_envelope(structured_output={"schema_v": "rv1", "verdict": "nope"},
                                usage={"input_tokens": 3, "output_tokens": 1}))
        assert out.error_class == "parse"
        assert out.usage_actuals is not None


# ---------------------------------------------------------------------------
# Finding 3 — native structured exhaustion classified parse
# ---------------------------------------------------------------------------

class TestStructuredExhaustion:
    def test_exhaustion_is_parse_not_provider_error(self):
        out = _review(_envelope(subtype=STRUCTURED_RETRY_EXHAUSTED_SUBTYPE, is_error=True,
                                errors=["schema validation failed"],
                                usage={"input_tokens": 50, "output_tokens": 5},
                                total_cost_usd=0.001))
        assert out.error_class == "parse"
        assert "provider_error" not in out.error
        assert out.schema_v == "rv1"
        assert out.error.startswith("malformed_output:")  # triggers one Remedy retry

    def test_exhaustion_on_nonzero_exit_still_parse(self):
        out = _review(_envelope(subtype=STRUCTURED_RETRY_EXHAUSTED_SUBTYPE, is_error=True,
                                usage={"input_tokens": 10, "output_tokens": 2}),
                      rc=1)
        assert out.error_class == "parse"

    def test_unrelated_is_error_remains_provider_error(self):
        out = _review(_envelope(subtype="success", is_error=True,
                                usage={"input_tokens": 1, "output_tokens": 1}))
        assert out.error_class != "parse"
        assert "provider_error" in out.error


# ---------------------------------------------------------------------------
# Finding 4 — failed structured calls retain Usage/cost
# ---------------------------------------------------------------------------

class TestFailedCallUsageRetained:
    def test_exhaustion_attempt_carries_usage_and_cost(self):
        out = _review(_envelope(subtype=STRUCTURED_RETRY_EXHAUSTED_SUBTYPE, is_error=True,
                                usage={"input_tokens": 50, "output_tokens": 5},
                                total_cost_usd=0.001))
        assert out.usage_actuals is not None
        assert out.usage_actuals["input_tokens"] == 50
        assert out.usage_actuals["total_cost_usd"] == 0.001
        assert out.actual_missing_reason == ""  # coverage complete: usage present


# ---------------------------------------------------------------------------
# Finding 6 — capability detection by actual invocation, not --help
# ---------------------------------------------------------------------------

class TestCapabilityDetection:
    def test_1_help_omits_flag_but_invocation_succeeds(self):
        # No --help preflight exists; a successful invocation just works.
        out = _review(_envelope(structured_output=_SO))
        assert out.verdict == "pass" and out.error_class == ""

    def test_2_unknown_option_error_is_config(self):
        out = _review("", rc=2, stderr="error: unknown option '--json-schema'")
        assert out.error_class == "config"
        assert "structured_mode_unavailable" in out.error

    def test_3_help_includes_flag_invocation_succeeds(self):
        out = _review(_envelope(structured_output=_SO))
        assert out.error_class == ""

    def test_4_ordinary_nonzero_error_not_misclassified(self):
        out = _review("", rc=1, stderr="Error: authentication failed")
        assert out.error_class != "config"
        assert "provider_error" in out.error

    def test_no_help_preflight_function_remains(self):
        import packages.orchestration.pingpong_provider as pp
        assert not hasattr(pp, "claude_cli_supports_json_schema")
