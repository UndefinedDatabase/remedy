"""Tests for F004 T001 — raw stream evidence capture, redaction and parsing.

Uses recorded stream fixtures. No provider is invoked; no 50 MB fixture is ever
allocated (the cap is configurable and tests use a tiny one).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.stream_evidence import (
    DEFAULT_MAX_BYTES,
    EVENT_API_RETRY,
    EVENT_CAP_REACHED,
    EVENT_MALFORMED,
    EVENT_PROVIDER_ERROR,
    EVENT_RESULT,
    EVENT_TOKEN_USAGE,
    EVENT_TOOL_RESULT,
    EVENT_TOOL_USE,
    RAW_STREAM_FILENAME,
    RUN_EVENTS_FILENAME,
    capture_stream_evidence,
    read_run_events,
    redact_stream_line,
    summarize_tool_input,
    sum_token_deltas,
)

_FIXTURES = Path(__file__).parent / "fixtures" / "stream"

#: Canary strings planted in the secrets fixture. None may reach any artifact.
_CANARIES = (
    "CANARYONEDEADBEEF",
    "CANARYTWOsecretvalue123",
    "CANARYTHREEabcdefghijklmnop",
    "CANARYFOUR1234567890abcdefghij123456",
)


def _fixture_lines(name: str) -> list[str]:
    return (_FIXTURES / name).read_text(encoding="utf-8").splitlines()


def _capture(name: str, tmp_path: Path, **kw):
    return capture_stream_evidence(_fixture_lines(name), tmp_path, **kw)


# ---------------------------------------------------------------------------
# Redaction before write
# ---------------------------------------------------------------------------

class TestRedaction:
    def test_canaries_absent_from_raw_and_normalized(self, tmp_path):
        res = _capture("secrets_canary.jsonl", tmp_path)
        raw = Path(res.raw_path).read_text(encoding="utf-8")
        events = Path(res.events_path).read_text(encoding="utf-8")
        for canary in _CANARIES:
            assert canary not in raw, f"{canary} leaked into raw_stream.jsonl"
            assert canary not in events, f"{canary} leaked into run_events.jsonl"
        assert "[REDACTED]" in raw

    def test_redacted_line_stays_valid_json(self):
        line = json.dumps({"api_key": "sk-ant-api03-CANARYONEDEADBEEF0123456789",
                           "file_path": "/safe/x.py"})
        red = redact_stream_line(line)
        obj = json.loads(red)
        assert obj["file_path"] == "/safe/x.py"
        assert "CANARY" not in red

    def test_safe_values_survive_redaction(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path)
        raw = Path(res.raw_path).read_text(encoding="utf-8")
        assert "/tmp/work/hello.py" in raw

    @pytest.mark.parametrize("secret", [
        "sk-ant-api03-AAAABBBBCCCCDDDD1234",
        "AKIAIOSFODNN7EXAMPLE",
        "ghp_1234567890abcdef1234567890abcdef1234",
        "glpat-abcdefghijklmnopqrst",
        "Bearer abcdefghijklmnopqrstuvwxyz012345",
        "-----BEGIN RSA PRIVATE KEY-----",
    ])
    def test_secret_shapes_redacted(self, secret):
        assert secret not in redact_stream_line(json.dumps({"v": secret}))


# ---------------------------------------------------------------------------
# Tool input safety
# ---------------------------------------------------------------------------

class TestToolInputSafety:
    def test_tool_input_is_digest_and_safe_metadata_only(self):
        summary = summarize_tool_input(
            {"file_path": "/a/b.py", "old_string": "TOPSECRETVALUE", "limit": 5}
        )
        assert summary["input_digest"].startswith("sha256:")
        assert summary["input_size_bytes"] > 0
        assert summary["input_keys"] == ["file_path", "limit", "old_string"]
        assert summary["safe_input"] == {"file_path": "/a/b.py", "limit": 5}
        assert "TOPSECRETVALUE" not in json.dumps(summary)

    def test_tool_use_event_never_carries_raw_input(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path)
        events = read_run_events(res.events_path)
        tool_uses = [e for e in events if e["event_type"] == EVENT_TOOL_USE]
        assert len(tool_uses) == 2
        blob = json.dumps(tool_uses)
        assert "return 'hi'" not in blob  # old_string value never persisted
        for ev in tool_uses:
            assert ev["input_digest"].startswith("sha256:")


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

class TestNormalization:
    def test_tool_use_and_result(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path)
        events = read_run_events(res.events_path)
        names = [e["tool_name"] for e in events if e["event_type"] == EVENT_TOOL_USE]
        assert names == ["Read", "Edit"]
        results = [e for e in events if e["event_type"] == EVENT_TOOL_RESULT]
        assert [r["tool_use_id"] for r in results] == ["tu_1", "tu_2"]
        assert all(r["result_digest"].startswith("sha256:") for r in results)
        assert all(r["is_error"] is False for r in results)

    def test_api_retry_events_visible(self, tmp_path):
        res = _capture("retry_and_error.jsonl", tmp_path)
        events = read_run_events(res.events_path)
        retries = [e for e in events if e["event_type"] == EVENT_API_RETRY]
        assert [r["attempt"] for r in retries] == [1, 2]
        assert retries[0]["reason"] == "overloaded_error"

    def test_provider_error_normalized(self, tmp_path):
        res = _capture("retry_and_error.jsonl", tmp_path)
        events = read_run_events(res.events_path)
        errs = [e for e in events if e["event_type"] == EVENT_PROVIDER_ERROR]
        assert len(errs) == 1
        assert "upstream connection reset" in errs[0]["error"]

    def test_final_result_normalized(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path)
        events = read_run_events(res.events_path)
        finals = [e for e in events if e["event_type"] == EVENT_RESULT]
        assert len(finals) == 1
        final = finals[0]
        assert final["is_error"] is False
        assert final["total_cost_usd"] == 0.0123
        assert final["session_id"] == "sess-f004"
        assert final["usage"]["input_tokens"] == 180

    def test_token_delta_aggregation(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path)
        events = read_run_events(res.events_path)
        deltas = [e for e in events if e["event_type"] == EVENT_TOKEN_USAGE]
        assert len(deltas) == 2
        assert sum(d["output_tokens"] for d in deltas) == 38
        # The final result carries cumulative totals and wins.
        totals = sum_token_deltas(events)
        assert totals["input_tokens"] == 180
        assert totals["output_tokens"] == 38
        assert totals["cache_read"] == 900

    def test_token_deltas_summed_when_no_final_usage(self):
        events = [
            {"event_type": EVENT_TOKEN_USAGE, "input_tokens": 5, "output_tokens": 1,
             "cache_read": 0, "cache_creation": 0},
            {"event_type": EVENT_TOKEN_USAGE, "input_tokens": 7, "output_tokens": 2,
             "cache_read": 3, "cache_creation": 0},
        ]
        assert sum_token_deltas(events) == {
            "input_tokens": 12, "output_tokens": 3, "cache_read": 3, "cache_creation": 0,
        }


# ---------------------------------------------------------------------------
# Raw offset backreferences
# ---------------------------------------------------------------------------

class TestRawOffsets:
    def test_every_event_has_offsets_that_resolve(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path)
        raw_bytes = Path(res.raw_path).read_bytes()
        events = read_run_events(res.events_path)
        assert events
        for ev in events:
            assert "raw_line_number" in ev
            assert "raw_byte_offset" in ev
            assert "raw_byte_length" in ev
            off, length = ev["raw_byte_offset"], ev["raw_byte_length"]
            chunk = raw_bytes[off:off + length].decode("utf-8")
            # The referenced bytes are exactly the source line.
            assert chunk.endswith("\n")
            json.loads(chunk)  # the raw line it came from is valid JSON

    def test_offsets_point_at_the_originating_line(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path)
        raw_lines = Path(res.raw_path).read_text(encoding="utf-8").splitlines()
        raw_bytes = Path(res.raw_path).read_bytes()
        for ev in read_run_events(res.events_path):
            if ev["event_type"] == EVENT_TOOL_USE and ev["tool_name"] == "Edit":
                chunk = raw_bytes[
                    ev["raw_byte_offset"]:ev["raw_byte_offset"] + ev["raw_byte_length"]
                ].decode("utf-8").rstrip("\n")
                assert chunk == raw_lines[ev["raw_line_number"] - 1]
                assert "tu_2" in chunk


# ---------------------------------------------------------------------------
# Malformed lines
# ---------------------------------------------------------------------------

class TestMalformedLines:
    def test_malformed_lines_recorded_not_fatal(self, tmp_path):
        res = _capture("malformed.jsonl", tmp_path)
        events = read_run_events(res.events_path)
        malformed = [e for e in events if e["event_type"] == EVENT_MALFORMED]
        # "this is not json at all" and the bare JSON array [1,2,3].
        assert res.malformed_lines == 2
        assert len(malformed) == 2
        assert {m["reason"] for m in malformed} == {
            "line is not valid json", "line is not a json object",
        }
        # Valid lines around them still normalize.
        assert any(e["event_type"] == EVENT_TOOL_USE for e in events)
        assert any(e["event_type"] == EVENT_RESULT for e in events)

    def test_malformed_line_still_persisted_and_addressable(self, tmp_path):
        res = _capture("malformed.jsonl", tmp_path)
        raw_bytes = Path(res.raw_path).read_bytes()
        malformed = [e for e in read_run_events(res.events_path)
                     if e["event_type"] == EVENT_MALFORMED]
        chunk = raw_bytes[
            malformed[0]["raw_byte_offset"]:
            malformed[0]["raw_byte_offset"] + malformed[0]["raw_byte_length"]
        ].decode("utf-8")
        assert "this is not json at all" in chunk


# ---------------------------------------------------------------------------
# Size cap
# ---------------------------------------------------------------------------

class TestSizeCap:
    def test_default_cap_is_50mb(self):
        assert DEFAULT_MAX_BYTES == 50 * 1024 * 1024

    def test_cap_stops_honestly_without_silent_truncation(self, tmp_path):
        lines = _fixture_lines("basic_session.jsonl")
        # Tiny cap: only the first line fits. The cap counts the REDACTED bytes
        # that are actually persisted, not the original line.
        first_len = len(redact_stream_line(lines[0]).encode("utf-8")) + 1
        res = capture_stream_evidence(lines, tmp_path, max_bytes=first_len)
        assert res.cap_reached is True
        assert res.raw_lines_written == 1
        assert res.dropped_lines == len(lines) - 1
        assert res.raw_bytes_written <= first_len

        events = read_run_events(res.events_path)
        cap_events = [e for e in events if e["event_type"] == EVENT_CAP_REACHED]
        assert len(cap_events) == 1
        assert cap_events[0]["dropped_lines"] == res.dropped_lines
        assert cap_events[0]["max_bytes"] == first_len

    def test_under_cap_writes_everything(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path, max_bytes=DEFAULT_MAX_BYTES)
        assert res.cap_reached is False
        assert res.dropped_lines == 0
        assert res.raw_lines_written == 6

    def test_cap_drain_consumes_generator_without_restart(self, tmp_path):
        lines = _fixture_lines("basic_session.jsonl")
        gen = (line for line in lines)
        res = capture_stream_evidence(gen, tmp_path, max_bytes=10)
        assert res.cap_reached is True
        assert res.raw_lines_written == 0
        assert res.dropped_lines == len(lines)


# ---------------------------------------------------------------------------
# Streaming behaviour
# ---------------------------------------------------------------------------

class TestStreamingBehaviour:
    def test_stream_is_consumed_lazily(self, tmp_path):
        consumed: list[int] = []

        def gen():
            for i, line in enumerate(_fixture_lines("basic_session.jsonl")):
                consumed.append(i)
                yield line

        res = capture_stream_evidence(gen(), tmp_path)
        # All lines consumed exactly once, one at a time (no full buffering).
        assert consumed == list(range(6))
        assert res.raw_lines_written == 6

    def test_artifact_names_and_summary(self, tmp_path):
        res = _capture("basic_session.jsonl", tmp_path)
        assert Path(res.raw_path).name == RAW_STREAM_FILENAME
        assert Path(res.events_path).name == RUN_EVENTS_FILENAME
        d = res.to_dict()
        assert d["event_counts"][EVENT_TOOL_USE] == 2
        assert d["events_written"] == res.events_written
        assert d["cap_reached"] is False


# ---------------------------------------------------------------------------
# Structural redaction (F004 finding 5)
# ---------------------------------------------------------------------------

_STRUCT_CANARIES = {
    "numeric_password": ('{"password": 123456}', "123456"),
    "nested_credentials": ('{"api_key": {"value": "SOMESECRET123"}}', "SOMESECRET123"),
    "token_in_list": ('{"args": ["sk-ant-api03-CANARYLIST0123456789"]}', "CANARYLIST"),
    "unicode_escaped_token":
        ('{"result": "sk\\u002dant\\u002dapi03\\u002dCANARYUNI0123456789"}', "CANARYUNI"),
    "escaped_private_key":
        ('{"blob": "-----BEGIN RSA PRIVATE KEY-----\\nMIICANARYKEY\\n"}', "MIICANARYKEY"),
    "nested_bearer":
        ('{"headers": {"Authorization": "Bearer CANARYBEARERabcdefghijk"}}', "CANARYBEARER"),
    "malformed_with_token":
        ("garbage not json sk-ant-api03-CANARYMALFORMED0123456789", "CANARYMALFORMED"),
}


class TestStructuralRedaction:
    @pytest.mark.parametrize("name", sorted(_STRUCT_CANARIES))
    def test_canary_absent_from_both_files(self, tmp_path, name):
        line, canary = _STRUCT_CANARIES[name]
        res = capture_stream_evidence([line], tmp_path)
        raw = Path(res.raw_path).read_text(encoding="utf-8")
        events = Path(res.events_path).read_text(encoding="utf-8")
        assert canary not in raw, f"{name}: canary leaked into raw_stream.jsonl"
        assert canary not in events, f"{name}: canary leaked into run_events.jsonl"

    def test_sensitive_key_value_replaced_whatever_the_type(self):
        from packages.orchestration.stream_evidence import redact_json_value
        out = redact_json_value({
            "password": 123456,
            "secret": True,
            "credentials": {"user": "u", "pass": "p"},
            "tokens": ["a", "b"],          # plural: not a secret key
            "access_token": ["x"],
        })
        assert out["password"] == "[REDACTED]"
        assert out["secret"] == "[REDACTED]"
        assert out["credentials"] == "[REDACTED]"
        assert out["access_token"] == "[REDACTED]"
        assert out["tokens"] == ["a", "b"]

    def test_measurement_fields_are_never_redacted(self):
        """F003 accounting depends on these; redacting them would corrupt totals."""
        from packages.orchestration.stream_evidence import redact_json_value
        payload = {
            "usage": {"input_tokens": 120, "output_tokens": 15,
                      "cache_read_input_tokens": 300, "cache_creation_input_tokens": 20},
            "session_id": "sess-1", "total_cost_usd": 0.002,
        }
        assert redact_json_value(payload) == payload

    def test_persisted_line_is_the_redacted_serialization(self, tmp_path):
        line = '{"api_key": "sk-ant-api03-CANARYSER0123456789", "file_path": "/a/b.py"}'
        res = capture_stream_evidence([line], tmp_path)
        persisted = Path(res.raw_path).read_text(encoding="utf-8").strip()
        obj = json.loads(persisted)
        assert obj["api_key"] == "[REDACTED]"
        assert obj["file_path"] == "/a/b.py"

    def test_malformed_line_falls_back_to_textual_redaction(self, tmp_path):
        res = capture_stream_evidence(["oops sk-ant-api03-CANARYFB0123456789"], tmp_path)
        raw = Path(res.raw_path).read_text(encoding="utf-8")
        assert "CANARYFB" not in raw
        assert "[REDACTED]" in raw
        assert res.malformed_lines == 1
