"""F303 R4 C4 — `packages/orchestration/mcp_server.serve_mcp`, the stdio transport of the Model
Context Protocol (DECISION F303 D4).

Every test drives `serve_mcp` over an `io.StringIO` reader and writer with two stand-in tools:
`echo`, which answers `{"ok": True, "got": arguments}`, and `fails`, which answers
`{"ok": False, "error": "x"}`. The writer's lines are parsed back as JSON to read the answers in
the order they were written.
"""
from __future__ import annotations

import io
import json

import pytest

from packages.orchestration.mcp_server import (
    MCP_INVALID_PARAMS,
    MCP_INVALID_REQUEST,
    MCP_METHOD_NOT_FOUND,
    MCP_PARSE_ERROR,
    MCP_PROTOCOL_VERSION,
    MCP_SERVER_NAME,
    McpServerError,
    McpTool,
    serve_mcp,
)

ECHO = McpTool(name="echo", description="echoes its arguments",
               input_schema={"type": "object"}, call=lambda arguments: {"ok": True, "got": arguments})
FAILS = McpTool(name="fails", description="always fails",
                input_schema={"type": "object"}, call=lambda arguments: {"ok": False, "error": "x"})


def _serve(lines: list[str], tools, allowed) -> tuple[int, list[dict]]:
    reader = io.StringIO("\n".join(lines) + ("\n" if lines else ""))
    writer = io.StringIO()
    code = serve_mcp(reader, writer, tools, allowed, version="9.9")
    answers = [json.loads(line) for line in writer.getvalue().splitlines() if line.strip()]
    return code, answers


def test_initialize_then_a_notification_then_tools_list_answers_twice_with_both_tools_sorted():
    lines = [
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
        json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}),
    ]
    code, answers = _serve(lines, [ECHO, FAILS], {"echo", "fails"})
    assert code == 0
    assert len(answers) == 2
    assert answers[0]["id"] == 1
    assert answers[0]["result"] == {
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": {"name": MCP_SERVER_NAME, "version": "9.9"},
    }
    assert answers[1]["id"] == 2
    assert [tool["name"] for tool in answers[1]["result"]["tools"]] == ["echo", "fails"]


def test_an_empty_allowlist_lists_no_tool_and_refuses_every_call():
    lines = [
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                   "params": {"name": "echo", "arguments": {}}}),
    ]
    code, answers = _serve(lines, [ECHO, FAILS], ())
    assert code == 0
    assert answers[0]["result"]["tools"] == []
    assert answers[1]["error"]["code"] == MCP_INVALID_PARAMS


def test_only_the_allowed_tool_is_listed_and_the_other_is_not_callable():
    lines = [
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                   "params": {"name": "fails", "arguments": {}}}),
    ]
    code, answers = _serve(lines, [ECHO, FAILS], {"echo"})
    assert code == 0
    assert [tool["name"] for tool in answers[0]["result"]["tools"]] == ["echo"]
    assert answers[1]["error"]["code"] == MCP_INVALID_PARAMS


def test_a_calls_result_carries_content_structured_content_and_is_error():
    lines = [
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                   "params": {"name": "echo", "arguments": {"x": 1}}}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                   "params": {"name": "fails", "arguments": {}}}),
    ]
    code, answers = _serve(lines, [ECHO, FAILS], {"echo", "fails"})
    assert code == 0
    echo_answer = {"ok": True, "got": {"x": 1}}
    fails_answer = {"ok": False, "error": "x"}
    [content] = answers[0]["result"]["content"]
    assert content["type"] == "text"
    assert json.loads(content["text"]) == json.loads(json.dumps(echo_answer, sort_keys=True))
    assert answers[0]["result"]["structuredContent"] == echo_answer
    assert answers[0]["result"]["isError"] is False
    assert answers[1]["result"]["structuredContent"] == fails_answer
    assert answers[1]["result"]["isError"] is True


@pytest.mark.parametrize("line, expected_code, expected_id", [
    pytest.param("not json at all", MCP_PARSE_ERROR, None, id="a_line_that_is_not_json"),
    pytest.param(json.dumps([1, 2, 3]), MCP_INVALID_REQUEST, None, id="a_json_array"),
    pytest.param(json.dumps({"jsonrpc": "1.0", "id": 5, "method": "ping"}), MCP_INVALID_REQUEST, 5,
                id="jsonrpc_1_0"),
    pytest.param(json.dumps({"jsonrpc": "2.0", "id": 6}), MCP_INVALID_REQUEST, 6,
                id="a_missing_method"),
    pytest.param(json.dumps({"jsonrpc": "2.0", "id": 7, "method": "nope"}), MCP_METHOD_NOT_FOUND, 7,
                id="an_unknown_method"),
    pytest.param(json.dumps({"jsonrpc": "2.0", "id": 8, "method": "tools/call",
                            "params": {"name": "echo", "arguments": [1, 2]}}),
                MCP_INVALID_PARAMS, 8, id="arguments_a_list"),
    pytest.param(json.dumps({"jsonrpc": "2.0", "id": 9, "method": "tools/call",
                            "params": {"name": "nope"}}),
                MCP_INVALID_PARAMS, 9, id="an_unknown_tool"),
])
def test_a_refusal_carries_its_code_and_the_requests_id_where_it_had_one(line, expected_code, expected_id):
    code, answers = _serve([line], [ECHO, FAILS], {"echo", "fails"})
    assert code == 0
    [answer] = answers
    assert answer["error"]["code"] == expected_code
    assert answer["id"] == expected_id


def test_a_notification_of_an_unknown_method_writes_nothing_and_ping_answers_empty():
    lines = [
        json.dumps({"jsonrpc": "2.0", "method": "notifications/surprise"}),
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping"}),
    ]
    code, answers = _serve(lines, [ECHO, FAILS], {"echo", "fails"})
    assert code == 0
    [answer] = answers
    assert answer == {"jsonrpc": "2.0", "id": 1, "result": {}}


def test_an_allowed_name_no_tool_has_refuses_before_anything_is_written():
    reader = io.StringIO("")
    writer = io.StringIO()
    with pytest.raises(McpServerError):
        serve_mcp(reader, writer, [ECHO], {"nope"}, version="1")
    assert writer.getvalue() == ""


def test_two_tools_of_one_name_refuses_before_anything_is_written():
    reader = io.StringIO("")
    writer = io.StringIO()
    duplicate = McpTool(name="echo", description="a second echo",
                        input_schema={"type": "object"}, call=lambda arguments: {"ok": True})
    with pytest.raises(McpServerError):
        serve_mcp(reader, writer, [ECHO, duplicate], {"echo"}, version="1")
    assert writer.getvalue() == ""


def test_the_return_value_is_0_and_a_blank_line_is_skipped():
    reader = io.StringIO("\n   \n" + json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping"}) + "\n")
    writer = io.StringIO()
    code = serve_mcp(reader, writer, [ECHO], {"echo"}, version="1")
    assert code == 0
    answers = [json.loads(line) for line in writer.getvalue().splitlines() if line.strip()]
    assert len(answers) == 1
