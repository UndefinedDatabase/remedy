"""Pi's JSON event stream (operator amendment amend1014b, DECISION D3): framing and the run summary."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.pi_events import (
    PiEventStream,
    PiStreamError,
    parse_pi_events,
    summarize_pi_events,
)


def _line(event: dict) -> bytes:
    return json.dumps(event, ensure_ascii=False).encode("utf-8") + b"\n"


def _assistant(text: str, *, stop: str = "stop", usage: dict | None = None, **extra) -> dict:
    return {"type": "message_end", "message": {
        "role": "assistant", "content": [{"type": "thinking", "thinking": "hm"},
                                         {"type": "text", "text": text}],
        "provider": "ollama", "model": "muse-glimmer:latest", "stopReason": stop,
        "usage": usage or {"input": 10, "output": 2, "cacheRead": 0, "cacheWrite": 0,
                           "totalTokens": 12}, **extra}}


def test_fragmented_reads_and_several_records_per_read_yield_the_same_records():
    data = _line({"type": "agent_start"}) + _line({"type": "turn_start"}) + _line({"type": "x"})
    whole = parse_pi_events(data)
    stream, fragmented = PiEventStream(), []
    for i in range(0, len(data), 7):
        fragmented += stream.feed(data[i:i + 7])
    fragmented += stream.close()
    assert fragmented == whole and [e["type"] for e in whole] == ["agent_start", "turn_start", "x"]


def test_crlf_is_stripped_and_unicode_line_separators_inside_strings_are_not_boundaries():
    payload = {"type": "message_update", "text": "a b c\x85d"}
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    assert b"\xe2\x80\xa8" in raw
    events = parse_pi_events(raw + b"\r\n" + _line({"type": "agent_start"}))
    assert events[0] == payload and events[1]["type"] == "agent_start"


def test_a_final_record_without_a_trailing_lf_is_read_and_a_partial_one_is_refused():
    assert parse_pi_events(b'{"type":"agent_settled","aborted":false}')[0]["type"] == "agent_settled"
    with pytest.raises(PiStreamError):
        parse_pi_events(b'{"type":"agent_start"}\n{"type":"agent_se')


@pytest.mark.parametrize("bad", [b"not json\n", b"[1,2]\n", b'{"no_type":1}\n', b"\xff\xfe\n"])
def test_a_malformed_record_is_a_stream_error(bad):
    with pytest.raises(PiStreamError):
        parse_pi_events(bad)


def test_the_summary_takes_message_end_as_authoritative_and_sums_every_model_turn():
    events = [
        {"type": "agent_start"},
        {"type": "message_update", "usage": {"input": 99, "output": 99}},   # never authoritative
        _assistant("", stop="toolUse", usage={"input": 100, "output": 10, "cacheRead": 5,
                                              "cacheWrite": 0, "totalTokens": 115}),
        {"type": "tool_execution_start", "toolName": "read"},
        {"type": "tool_execution_end", "toolName": "read", "isError": False},
        {"type": "tool_execution_start", "toolName": "bash"},
        {"type": "tool_execution_end", "toolName": "bash", "isError": True},
        {"type": "auto_retry_start", "attempt": 1},
        _assistant("done", usage={"input": 200, "output": 20, "cacheRead": 0, "cacheWrite": 0,
                                  "totalTokens": 220}),
        {"type": "agent_end", "messages": [], "willRetry": False},
        {"type": "agent_settled", "aborted": False},
    ]
    out = summarize_pi_events(events)
    assert (out.final_text, out.settled, out.aborted) == ("done", True, False)
    assert out.model_turns == 2 and out.stop_reason == "stop" and out.retries == 1
    assert out.tool_calls == ["read", "bash"] and out.tool_errors == 1
    assert out.usage == {"input": 300, "output": 30, "cacheRead": 5, "cacheWrite": 0, "totalTokens": 335}
    assert (out.inner_provider, out.inner_model) == ("ollama", "muse-glimmer:latest")


def test_agent_end_alone_does_not_settle_the_run_and_an_abort_is_reported():
    unsettled = summarize_pi_events([_assistant("x"), {"type": "agent_end", "willRetry": True}])
    assert not unsettled.settled
    aborted = summarize_pi_events([_assistant("x", stop="aborted"),
                                   {"type": "agent_settled", "aborted": True}])
    assert aborted.aborted and aborted.model_error == "aborted"


def test_a_provider_error_message_carries_its_error_text():
    out = summarize_pi_events([_assistant("", stop="error", errorMessage="connection refused"),
                               {"type": "agent_settled", "aborted": False}])
    assert out.model_error == "connection refused"
