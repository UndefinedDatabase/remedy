# MCP server v1

> Status (F303, DECISION F303 D4 and D5, 2026-10-21): built. `remedy client mcp` serves three
> tools; the machine client contract (`docs/system/machine-client-contract-v1.md`) and the public
> HTTP API (`docs/system/public-http-api-v1.md`) describe the other two ways a program drives
> Remedy.

The Model Context Protocol (MCP) lets an orchestrator, a program that runs coding tools for a
person, call Remedy's gates without adopting Remedy's own loop. The orchestrator starts Remedy as a
child process and speaks JSON-RPC 2.0 to it over standard input and standard output, one message
per line. `remedy client mcp` is that child: it answers `initialize`, `ping`, `tools/list` and
`tools/call`, ignores every message without an `id` (a notification), and ends when its input
ends, with exit code 0. The protocol revision it speaks is `2025-06-18`.

## Closed by default

The server offers only the tools `--allow` names, once for each tool. With no `--allow` it lists
no tool and refuses every call with the JSON-RPC error -32602. A name that no tool has is refused
before any line is read: standard output stays empty, standard error names the name and the three
tools, and the exit code is 2. The allowlist is the command line itself, so the person who writes
the orchestrator's server entry sees it there.

## Starting it

An orchestrator's server entry names the command and the tools it may use:

```json
{
  "mcpServers": {
    "remedy": {
      "command": "remedy",
      "args": ["client", "mcp", "--allow", "verify"]
    }
  }
}
```

Run the server from the project the orchestrator works on, with the same data root (`REMEDY_DATA_DIR`)
the person's own `remedy` commands use, because each tool reads what its twin command reads.

## The three tools

Each tool runs its twin command as a child `remedy` with `--json`, so a call answers what that
command prints. A call carries its answer as `structuredContent`, the same answer as sorted JSON
text in `content`, and `isError`, which is true when the answer's `ok` is false. A required
argument that is missing or not a non-empty string is answered `invalid_argument` and runs nothing.
A child that cannot start, outlives 600 seconds or prints no envelope is answered
`mcp_tool_failed`.

| Tool | Arguments | Runs | Answers |
|------|-----------|------|---------|
| `verify` | `bundle` | `remedy verify run` | whether the certificate at `bundle` is intact, as that command answers |
| `gate_status` | `job` | `remedy client story` | the job's `job_id`, `state`, `state_detail` and `verification`, the gate reading every surface shows; a refusal is answered as printed |
| `evidence_bundle` | `job`, optional `out` | `remedy job certificate` | the certificate the job's evidence makes, written to `out` or to the command's default file, with its path and manifest digest |

Every input schema is a closed JSON object: an argument the tool does not name is not part of it.

## One exchange

The orchestrator writes, one line each:

```
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
{"jsonrpc": "2.0", "method": "notifications/initialized"}
{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "gate_status", "arguments": {"job": "<job id>"}}}
```

and reads the answer to the first and to the third, since a notification is never answered. The
third answer has `result.structuredContent` holding `job_id`, `state`, `state_detail` and
`verification`, and `result.isError` false.

## Remedy deliberately does not

- offer a tool beyond these three: a program that needs more reads the machine client contract or
  the public HTTP API;
- listen on a network port: the server speaks over the standard input and output of the process
  that started it, and nothing else reaches it;
- write anything but the certificate file that `evidence_bundle` asks for, and a second call to a
  path that already holds a file is refused as `job certificate` refuses it;
- read an allowlist from a file: the command line names the tools, so no second place can disagree
  with it.
