"""Pi's JSON event stream: the framing reader and the run summary (amend1014b, DECISION D3).

Pi prints one JSON object per LF-terminated line. `message_end` is the authoritative final
message, `agent_settled` (not the first `agent_end`) ends the run, and the usage on each
completed assistant message is that response's final figure. Nothing here reads a terminal's
prose, and nothing here decides that a file changed: the workspace diff does.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# D3 — the JSONL stream
# ---------------------------------------------------------------------------

class PiStreamError(ValueError):
    """The JSONL stream is malformed or truncated."""


class PiEventStream:
    """An incremental reader of Pi's JSONL framing: LF only, an optional CR stripped.

    Unicode line and paragraph separators are valid inside JSON strings and are never record
    boundaries, which is why this works on bytes and splits on b"\\n" alone rather than on
    `str.splitlines()`. A chunk may end mid-record or carry several records.
    """

    def __init__(self) -> None:
        self._pending = b""

    def feed(self, chunk: bytes) -> list[dict[str, Any]]:
        self._pending += chunk
        *lines, self._pending = self._pending.split(b"\n")
        return [self._decode(line) for line in lines if line.strip(b"\r")]

    def close(self) -> list[dict[str, Any]]:
        """The final record when the stream ended without a trailing LF; a partial one raises."""
        tail, self._pending = self._pending, b""
        return [self._decode(tail)] if tail.strip(b"\r") else []

    @staticmethod
    def _decode(line: bytes) -> dict[str, Any]:
        try:
            record = json.loads(line.rstrip(b"\r").decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise PiStreamError(f"a Pi event record is not valid JSON ({type(exc).__name__})") from exc
        if not isinstance(record, dict) or not isinstance(record.get("type"), str):
            raise PiStreamError("a Pi event record is not an object with a type")
        return record


def parse_pi_events(data: bytes) -> list[dict[str, Any]]:
    """Every record of a whole captured stdout; a malformed or truncated record raises."""
    stream = PiEventStream()
    return stream.feed(data) + stream.close()


@dataclass
class PiRunSummary:
    """What the event stream says one Pi invocation did. Prose here is evidence, not a change."""

    final_text: str = ""
    settled: bool = False
    aborted: bool = False
    model_turns: int = 0
    stop_reason: str = ""
    model_error: str = ""
    retries: int = 0
    tool_calls: list[str] = field(default_factory=list)
    tool_errors: int = 0
    inner_provider: str = ""
    inner_model: str = ""
    usage: dict[str, int] = field(default_factory=lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "totalTokens": 0})


def _int_of(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0


def summarize_pi_events(events: list[dict[str, Any]]) -> PiRunSummary:
    """Fold the records into a summary. `message_end` is authoritative; `agent_settled` ends it.

    `agent_end` only closes one low-level run, so it settles nothing: Pi may still retry,
    compact or take queued work after it. Each completed assistant message is one real model
    turn and its usage the final figure for that response, so the aggregate sums them.
    """
    out = PiRunSummary()
    for event in events:
        kind = event["type"]
        if kind == "message_end":
            message = event.get("message")
            if not isinstance(message, dict) or message.get("role") != "assistant":
                continue
            out.model_turns += 1
            usage = message.get("usage")
            if isinstance(usage, dict):
                for key in out.usage:
                    out.usage[key] += _int_of(usage.get(key))
            out.stop_reason = str(message.get("stopReason") or "")
            out.inner_provider = str(message.get("provider") or out.inner_provider)
            out.inner_model = str(message.get("model") or out.inner_model)
            blocks = message.get("content")
            texts = [b.get("text", "") for b in blocks
                     if isinstance(b, dict) and b.get("type") == "text"] if isinstance(blocks, list) else []
            out.final_text = "".join(t for t in texts if isinstance(t, str))
            out.model_error = (str(message.get("errorMessage") or out.stop_reason)
                               if out.stop_reason in ("error", "aborted") else "")
        elif kind == "tool_execution_start":
            out.tool_calls.append(str(event.get("toolName") or "?"))
        elif kind == "tool_execution_end":
            out.tool_errors += 1 if event.get("isError") is True else 0
        elif kind == "auto_retry_start":
            out.retries += 1
        elif kind == "agent_settled":
            out.settled = True
            out.aborted = event.get("aborted") is True
    return out


