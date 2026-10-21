"""The three tools Remedy's MCP server offers an orchestrator: `verify`, `gate_status` and
`evidence_bundle` (DECISION F303 D5).

Each tool runs its twin command as a child process (`remedy verify run`, `remedy client story`,
`remedy job certificate`, always with `--json`) and answers what that command prints, as the public
API's write routes do, so a tool never says more or less than its twin and a failing call cannot end
the server. A tool's input schema is a closed JSON Schema object, and a required argument that is
missing or not a non-empty string is refused with `invalid_argument` before anything runs.
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Callable, Sequence
from typing import Any

from packages.orchestration.mcp_server import McpTool

# WHY: the three tool names the server can offer, sorted, so `--allow` and its refusal name one list.
MCP_TOOL_NAMES = ("evidence_bundle", "gate_status", "verify")

# WHY: a child that outlives this is answered as a failure, so one stuck command cannot hold a call forever.
MCP_TOOL_TIMEOUT_SECONDS = 600

# WHY: the one set of keys a gate reading carries, the same four every surface shows of a job.
_GATE_STATUS_KEYS = ("job_id", "state", "state_detail", "verification")


def _failure(error: str, message: str) -> dict[str, Any]:
    return {"ok": False, "error": error, "message": message}


def _last_envelope_line(text: str) -> dict[str, Any] | None:
    """The last non-empty line of TEXT read as JSON, when that is an object holding `ok`."""
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    try:
        envelope = json.loads(lines[-1])
    except ValueError:
        return None
    return envelope if isinstance(envelope, dict) and "ok" in envelope else None


# WHY: the one place a tool starts a child `remedy`, so its failures are answered in one shape.
def run_remedy_json(argv: Sequence[str], *,
                    timeout: float = MCP_TOOL_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Run `remedy ARGV` as a child and answer the envelope it prints.

    The envelope is the last non-empty line of standard output, parsed as JSON, when that is an
    object holding `ok`. A child that cannot start, outlives TIMEOUT seconds or prints no envelope
    is answered `{"ok": False, "error": "mcp_tool_failed", "message": ...}`.
    """
    command = [sys.executable, "-m", "apps.cli.main", *argv]
    try:
        done = subprocess.run(command, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return _failure("mcp_tool_failed",
                        f"the command outlived {timeout:g} seconds and was stopped")
    except OSError as exc:
        return _failure("mcp_tool_failed", f"the command could not be started: {exc}")
    envelope = _last_envelope_line(done.stdout)
    if envelope is None:
        return _failure("mcp_tool_failed",
                        f"the command printed no envelope (it exited {done.returncode})")
    return envelope


def _required_text(arguments: dict[str, Any], key: str) -> str | None:
    value = arguments.get(key)
    return value if isinstance(value, str) and value else None


def _invalid_argument(key: str) -> dict[str, Any]:
    return _failure("invalid_argument", f"the argument {key!r} is required and must be a non-empty string")


def _schema(properties: dict[str, str], required: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {name: {"type": "string", "description": text}
                       for name, text in properties.items()},
        "required": required,
        "additionalProperties": False,
    }


# WHY: the three tools, each a thin call of a twin command, built around one `run` so tests inject a fake.
def remedy_mcp_tools(*, run: Callable[[Sequence[str]], dict[str, Any]] = run_remedy_json
                     ) -> tuple[McpTool, ...]:
    """The three MCP tools, sorted by name, each calling RUN with its twin command's arguments."""

    def evidence_bundle(arguments: dict[str, Any]) -> dict[str, Any]:
        job = _required_text(arguments, "job")
        if job is None:
            return _invalid_argument("job")
        out = _required_text(arguments, "out")
        if "out" in arguments and out is None:
            return _invalid_argument("out")
        out_args = [f"--out={out}"] if out else []
        return run(["job", "certificate", *out_args, "--json", "--", job])

    def gate_status(arguments: dict[str, Any]) -> dict[str, Any]:
        job = _required_text(arguments, "job")
        if job is None:
            return _invalid_argument("job")
        story = run(["client", "story", "--json", "--", job])
        if story.get("ok") is not True:
            return story
        return {key: story[key] for key in _GATE_STATUS_KEYS if key in story}

    def verify(arguments: dict[str, Any]) -> dict[str, Any]:
        bundle = _required_text(arguments, "bundle")
        if bundle is None:
            return _invalid_argument("bundle")
        return run(["verify", "run", "--json", "--", bundle])

    return (
        McpTool(
            name="evidence_bundle",
            description=("Write the evidence certificate of a finished job, optionally to the path "
                         "given in out, and answer what `remedy job certificate` answers."),
            input_schema=_schema(
                {"job": "The id of the job to certify.",
                 "out": "Where to write the certificate; omit it for the command's own default."},
                ["job"]),
            call=evidence_bundle),
        McpTool(
            name="gate_status",
            description=("Read a job's gate status: its state, the detail of that state and the "
                         "verification of its checks, as every Remedy surface shows them."),
            input_schema=_schema({"job": "The id of the job to read."}, ["job"]),
            call=gate_status),
        McpTool(
            name="verify",
            description=("Verify an evidence certificate or bundle and answer what "
                         "`remedy verify run` answers."),
            input_schema=_schema({"bundle": "The path of the certificate or bundle to verify."},
                                 ["bundle"]),
            call=verify),
    )
