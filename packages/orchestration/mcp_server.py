"""The stdio transport of the Model Context Protocol: JSON-RPC 2.0, one message per line over
standard input and standard output, so a third-party orchestrator can start Remedy as a child
process and speak `initialize`, `tools/list` and `tools/call` to it without adopting Remedy's own
loop (DECISION F303 D4).

Closed by default: a server offers only the tools the person starting it names in `allowed`; an
empty allowlist lists no tool and answers every call -32602, and a name in `allowed` that no tool
has is refused before the first line is even read. Standard library only.
"""
from __future__ import annotations

import json
from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, TextIO

# WHY: the protocol revision this server speaks; it is fixed, never negotiated with a client.
MCP_PROTOCOL_VERSION = "2025-06-18"

# WHY: the name a client's `initialize` answer reports this server under.
MCP_SERVER_NAME = "remedy"

# WHY: the JSON-RPC 2.0 reserved error codes this server answers, pinned by that spec, not chosen.
MCP_PARSE_ERROR = -32700
MCP_INVALID_REQUEST = -32600
MCP_METHOD_NOT_FOUND = -32601
MCP_INVALID_PARAMS = -32602


# WHY: the server's own setup mistake, raised before a line is read, never a protocol answer.
class McpServerError(Exception):
    """A server was asked to run with a tool list or an allowlist that cannot be served."""


# WHY: one tool offered to a client, named so `serve_mcp` never needs to know what a tool does.
@dataclass(frozen=True)
class McpTool:
    """A tool `serve_mcp` may offer: its machine name, its description, its JSON Schema input
    shape, and the function that turns a call's arguments into its answer."""

    name: str
    description: str
    input_schema: Mapping[str, Any]
    call: Callable[[dict[str, Any]], dict[str, Any]]


def _response(message_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def _error_response(message_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}


def _write(writer: TextIO, payload: dict[str, Any]) -> None:
    writer.write(json.dumps(payload, ensure_ascii=False) + "\n")
    writer.flush()


def _request_id(value: Any) -> Any:
    """The JSON-RPC id of a parsed message that failed basic validation: `value`'s own `id` when
    it is a string or an integer (a JSON boolean is neither, though Python's `bool` is an `int`
    subtype), else `None`."""
    message_id = value.get("id") if isinstance(value, dict) else None
    if isinstance(message_id, bool) or not isinstance(message_id, (str, int)):
        return None
    return message_id


# WHY: the one entry point an orchestrator speaks JSON-RPC 2.0 to, one message per line (DECISION F303 D4).
def serve_mcp(reader: TextIO, writer: TextIO, tools: Sequence[McpTool], allowed: Collection[str],
             *, version: str) -> int:
    """Serve the Model Context Protocol's stdio transport over READER and WRITER until READER
    ends, offering only the ALLOWED names of TOOLS. Returns 0.

    Raises `McpServerError` before any line is read when two of TOOLS share a name, or when a name
    in ALLOWED names no tool.
    """
    names: list[str] = []
    seen: set[str] = set()
    for tool in tools:
        if tool.name in seen:
            raise McpServerError(f"two MCP tools are named {tool.name!r}")
        seen.add(tool.name)
        names.append(tool.name)
    missing = sorted(set(allowed) - seen)
    if missing:
        raise McpServerError(
            f"no MCP tool is named {missing[0]!r}; the tools are: {', '.join(sorted(names))}")

    tools_by_name = {tool.name: tool for tool in tools}
    allowed_names = set(allowed)

    for raw_line in reader:
        line = raw_line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            _write(writer, _error_response(None, MCP_PARSE_ERROR, "the line is not JSON"))
            continue

        if (not isinstance(value, dict) or value.get("jsonrpc") != "2.0"
                or not isinstance(value.get("method"), str)):
            _write(writer, _error_response(
                _request_id(value), MCP_INVALID_REQUEST,
                "the message is not a JSON-RPC 2.0 request naming a method"))
            continue

        if "id" not in value:
            continue  # a notification: never answered, whatever its method.

        message_id = value["id"]
        method = value["method"]
        params = value.get("params")

        if method == "initialize":
            _write(writer, _response(message_id, {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": MCP_SERVER_NAME, "version": version},
            }))
        elif method == "ping":
            _write(writer, _response(message_id, {}))
        elif method == "tools/list":
            _write(writer, _response(message_id, {"tools": [
                {"name": tool.name, "description": tool.description,
                 "inputSchema": tool.input_schema}
                for tool in sorted(tools, key=lambda t: t.name) if tool.name in allowed_names
            ]}))
        elif method == "tools/call":
            tool_name = params.get("name") if isinstance(params, dict) else None
            if tool_name not in allowed_names:
                _write(writer, _error_response(
                    message_id, MCP_INVALID_PARAMS,
                    f"the tool {tool_name!r} is not offered by this server"))
                continue
            arguments = params.get("arguments")
            if arguments is not None and not isinstance(arguments, dict):
                _write(writer, _error_response(
                    message_id, MCP_INVALID_PARAMS, "the arguments must be an object"))
                continue
            answer = tools_by_name[tool_name].call(arguments or {})
            _write(writer, _response(message_id, {
                "content": [{"type": "text",
                            "text": json.dumps(answer, sort_keys=True, ensure_ascii=False)}],
                "structuredContent": answer,
                "isError": answer.get("ok") is False,
            }))
        else:
            _write(writer, _error_response(
                message_id, MCP_METHOD_NOT_FOUND, f"unknown method {method!r}"))

    return 0
