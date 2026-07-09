"""Tests for the claude CLI token/cost actuals parser."""

from __future__ import annotations

import json

from packages.orchestration.token_actuals import UsageActuals, parse_cli_result, parse_cli_result_detailed


def _full_payload() -> dict:
    return {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "duration_ms": 3397,
        "num_turns": 1,
        "result": "the text content",
        "session_id": "uuid-here",
        "total_cost_usd": 0.065,
        "usage": {
            "input_tokens": 6013,
            "cache_creation_input_tokens": 2788,
            "cache_read_input_tokens": 15079,
            "output_tokens": 4,
        },
    }


def test_valid_full_usage():
    actuals = parse_cli_result(json.dumps(_full_payload()))
    assert actuals == UsageActuals(
        input_tokens=6013,
        output_tokens=4,
        cache_read=15079,
        cache_creation=2788,
        total_cost_usd=0.065,
        num_turns=1,
        duration_ms=3397,
        session_id="uuid-here",
        cli_version=None,
    )


def test_partial_usage_defaults_cache_to_zero():
    payload = _full_payload()
    payload["usage"] = {"input_tokens": 100, "output_tokens": 20}
    actuals = parse_cli_result(json.dumps(payload))
    assert actuals is not None
    assert actuals.cache_read == 0
    assert actuals.cache_creation == 0
    assert actuals.input_tokens == 100
    assert actuals.output_tokens == 20


def test_cli_version_captured_when_present():
    payload = _full_payload()
    payload["cli_version"] = "1.2.3"
    actuals = parse_cli_result(json.dumps(payload))
    assert actuals is not None
    assert actuals.cli_version == "1.2.3"


def test_empty_string_returns_none():
    assert parse_cli_result("") is None
    assert parse_cli_result("   ") is None


def test_non_json_returns_none():
    assert parse_cli_result("not json at all") is None


def test_missing_usage_block_returns_none():
    payload = _full_payload()
    del payload["usage"]
    assert parse_cli_result(json.dumps(payload)) is None


def test_is_error_true_returns_none():
    payload = _full_payload()
    payload["is_error"] = True
    assert parse_cli_result(json.dumps(payload)) is None


def test_usage_missing_required_fields_returns_none():
    payload = _full_payload()
    payload["usage"] = {"cache_read_input_tokens": 10}  # no input/output tokens
    assert parse_cli_result(json.dumps(payload)) is None

    payload["usage"] = {"input_tokens": 5}  # output missing
    assert parse_cli_result(json.dumps(payload)) is None


def test_missing_total_cost_usd_returns_actuals_with_none_cost():
    payload = _full_payload()
    del payload["total_cost_usd"]
    actuals = parse_cli_result(json.dumps(payload))
    assert actuals is not None
    assert actuals.total_cost_usd is None
    assert actuals.input_tokens == 6013


def test_output_tokens_zero_with_valid_input_returns_actuals():
    payload = _full_payload()
    payload["usage"]["output_tokens"] = 0
    actuals = parse_cli_result(json.dumps(payload))
    assert actuals is not None
    assert actuals.output_tokens == 0
    assert actuals.input_tokens == 6013


def test_invalid_cost_value_returns_none_cost():
    payload = _full_payload()
    payload["total_cost_usd"] = "not-a-number"
    actuals = parse_cli_result(json.dumps(payload))
    assert actuals is not None
    assert actuals.total_cost_usd is None


# --- parse_cli_result_detailed reason tests (Fix 1) ---

def test_detailed_empty_input_reason():
    actuals, reason = parse_cli_result_detailed("")
    assert actuals is None
    assert reason == "empty_input"
    actuals2, reason2 = parse_cli_result_detailed("   ")
    assert actuals2 is None
    assert reason2 == "empty_input"


def test_detailed_parse_failed_reason():
    actuals, reason = parse_cli_result_detailed("not json at all")
    assert actuals is None
    assert reason == "parse_failed"


def test_detailed_parse_failed_non_dict():
    actuals, reason = parse_cli_result_detailed(json.dumps([1, 2, 3]))
    assert actuals is None
    assert reason == "parse_failed"


def test_detailed_is_error_reason():
    payload = _full_payload()
    payload["is_error"] = True
    actuals, reason = parse_cli_result_detailed(json.dumps(payload))
    assert actuals is None
    assert reason == "is_error"


def test_detailed_usage_missing_no_usage_key():
    payload = {"result": "hello", "is_error": False}
    actuals, reason = parse_cli_result_detailed(json.dumps(payload))
    assert actuals is None
    assert reason == "usage_missing"


def test_detailed_usage_missing_no_tokens():
    payload = {"result": "hello", "is_error": False, "usage": {}}
    actuals, reason = parse_cli_result_detailed(json.dumps(payload))
    assert actuals is None
    assert reason == "usage_missing"


def test_detailed_ok_on_success():
    actuals, reason = parse_cli_result_detailed(json.dumps(_full_payload()))
    assert actuals is not None
    assert reason == "ok"
    assert actuals.input_tokens == 6013


def test_detailed_cli_version_preserved():
    payload = _full_payload()
    payload["cli_version"] = "1.0.42"
    actuals, reason = parse_cli_result_detailed(json.dumps(payload))
    assert actuals is not None
    assert actuals.cli_version == "1.0.42"
    assert reason == "ok"
