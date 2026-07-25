"""Raw stream evidence (F004) — bounded, redacted capture of Claude CLI
``stream-json`` output plus an inline-normalized event log.

Opt-in only. The default provider path stays the F003 JSON mode; nothing here
runs unless a caller explicitly asks for stream evidence.

Two artifacts are produced per task:

    task_runs/<task>/raw_stream.jsonl   redacted raw stream lines, byte-bounded
    task_runs/<task>/run_events.jsonl   normalized events, each carrying a
                                        raw line/byte offset backreference

Guarantees:

* Redaction runs BEFORE any raw byte is persisted. The normalizer reads the
  redacted line, so a secret cannot reach either file.
* Tool inputs are never persisted verbatim — only a sha256 digest, a byte size
  and an explicitly safe key list.
* The stream is consumed line by line; the whole stream is never buffered.
* The byte cap is honest: at the cap the capture stops, records ``cap_reached``,
  counts the dropped lines, and emits a terminal ``stream_cap_reached`` event.
  Nothing is silently truncated.
* A malformed line becomes a ``malformed`` event with offsets and never raises.

No provider is invoked by this module: it consumes an iterable of lines.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.prompt_trace import redact_prompt_text
from packages.orchestration.token_actuals import STRUCTURED_RETRY_EXHAUSTED_SUBTYPE

SCHEMA_VERSION = "1.0.0"

#: 50 MB per task, per the F004 design. Tests override with a tiny cap.
DEFAULT_MAX_BYTES = 50 * 1024 * 1024

RAW_STREAM_FILENAME = "raw_stream.jsonl"
RUN_EVENTS_FILENAME = "run_events.jsonl"

#: Tool-input keys that are safe to record verbatim. Anything else is reduced to
#: its key name only; values never leave this module.
_SAFE_TOOL_INPUT_KEYS = frozenset({
    "file_path", "path", "pattern", "glob", "command_name",
    "limit", "offset", "timeout", "type", "name",
})

#: Event types emitted by the normalizer.
EVENT_TOOL_USE = "tool_use"
EVENT_TOOL_RESULT = "tool_result"
EVENT_API_RETRY = "api_retry"
EVENT_TOKEN_USAGE = "token_usage"
EVENT_RESULT = "result"
EVENT_PROVIDER_ERROR = "provider_error"
EVENT_MALFORMED = "malformed"
EVENT_CAP_REACHED = "stream_cap_reached"


@dataclass
class StreamCaptureResult:
    """Outcome of one stream capture. Honest about what was and was not kept."""
    raw_path: str = ""
    events_path: str = ""
    raw_bytes_written: int = 0
    raw_lines_written: int = 0
    events_written: int = 0
    malformed_lines: int = 0
    cap_reached: bool = False
    dropped_lines: int = 0
    remaining_lines_unknown: bool = False
    max_bytes: int = DEFAULT_MAX_BYTES
    event_counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "raw_path": self.raw_path,
            "events_path": self.events_path,
            "raw_bytes_written": self.raw_bytes_written,
            "raw_lines_written": self.raw_lines_written,
            "events_written": self.events_written,
            "malformed_lines": self.malformed_lines,
            "cap_reached": self.cap_reached,
            "dropped_lines": self.dropped_lines,
            "remaining_lines_unknown": self.remaining_lines_unknown,
            "max_bytes": self.max_bytes,
            "event_counts": dict(self.event_counts),
        }


# ---------------------------------------------------------------------------
# Redaction + digests
# ---------------------------------------------------------------------------

#: Stream lines are JSON, so a secret usually appears as a quoted value under a
#: sensitive key. These patterns close gaps the prompt corpus does not cover
#: (provider keys containing '-'/'_', *_SECRET_*/*_KEY assignments, key blocks).
_SENSITIVE_JSON_KEY_RE = re.compile(
    r'("(?:[A-Za-z0-9_\-]*'
    r'(?:api[_-]?key|apikey|secret|token|password|passwd|authorization|auth'
    r'|credential|private[_-]?key|session[_-]?key)'
    r'[A-Za-z0-9_\-]*)"\s*:\s*)"(?:\\.|[^"\\])*"',
    re.IGNORECASE,
)

_ENV_ASSIGN_RE = re.compile(
    r"\b([A-Za-z0-9_]*(?:KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL)[A-Za-z0-9_]*)"
    r"\s*=\s*[^\s\"',;]+",
    re.IGNORECASE,
)

_STREAM_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    # Provider keys whose bodies contain '-' or '_' (e.g. sk-ant-api03-...).
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"),
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"anthropic[_-]?api[_-]?key[\"'\s:=]+[A-Za-z0-9_\-]{10,}", re.IGNORECASE),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ASIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"glpat-[A-Za-z0-9_\-]{15,}"),
    re.compile(r"xox[abprs]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=\-]{16,}"),
    re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{5,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


#: Whole-value replacement marker.
REDACTED = "[REDACTED]"
PRIVATE_KEY_REDACTED = "[PRIVATE_KEY_REDACTED]"

#: Substrings that make a key sensitive once punctuation is stripped.
_SENSITIVE_KEY_SUBSTRINGS = (
    "apikey", "secret", "password", "passwd", "credential",
    "privatekey", "sessionkey", "accesskey", "authorization", "bearer",
)
#: Exact normalized key names that are sensitive on their own.
_SENSITIVE_KEY_EXACT = frozenset({
    "token", "auth", "key", "authtoken", "accesstoken", "refreshtoken",
    "idtoken", "apitoken", "cookie", "signature",
})


def _normalize_key(key: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(key).lower())


def is_sensitive_key(key: Any) -> bool:
    """True when a JSON key's value must be replaced wholesale, whatever its type.

    Deliberately precise: ``input_tokens`` / ``output_tokens`` / ``session_id``
    are measurement fields the accepted F003 accounting depends on and must never
    be redacted, while ``api_key``, ``password``, ``credentials``,
    ``authorization`` and bare ``token`` must be.
    """
    norm = _normalize_key(key)
    if not norm:
        return False
    if norm in _SENSITIVE_KEY_EXACT:
        return True
    if any(sub in norm for sub in _SENSITIVE_KEY_SUBSTRINGS):
        return True
    # ``access_token`` yes, ``input_tokens`` no.
    return norm.endswith("token") and not norm.endswith("tokens")


def redact_text(text: str) -> str:
    """Textual secret redaction over an already-decoded string."""
    if "PRIVATE KEY" in text:
        return PRIVATE_KEY_REDACTED
    out = redact_prompt_text(text)
    out = _SENSITIVE_JSON_KEY_RE.sub(r'\1"[REDACTED]"', out)
    for pat in _STREAM_SECRET_PATTERNS:
        out = pat.sub(REDACTED, out)
    out = _ENV_ASSIGN_RE.sub(r"\1=[REDACTED]", out)
    return out


def redact_json_value(value: Any) -> Any:
    """Recursively redact a decoded JSON value.

    Any value under a sensitive key is replaced entirely — string, number,
    boolean, list or object alike. Every remaining string is redacted after JSON
    decoding, so ``\\u002d``-escaped tokens cannot slip past pattern matching.
    """
    if isinstance(value, dict):
        return {
            k: (REDACTED if is_sensitive_key(k) else redact_json_value(v))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [redact_json_value(v) for v in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def redact_stream_payload(line: str) -> tuple[str, Any]:
    """Redact one raw stream line, returning ``(persisted_text, decoded_object)``.

    A valid JSON line is parsed in memory, redacted structurally, and re-serialized
    — only that serialization is ever persisted, and normalization reads the very
    same redacted object. A malformed line falls back to best-effort textual
    redaction; the original line is never persisted. ``decoded_object`` is None
    when the line was not valid JSON.
    """
    try:
        obj = json.loads(line)
    except (ValueError, TypeError):
        return redact_text(line), None
    if isinstance(obj, (dict, list)):
        redacted = redact_json_value(obj)
        return json.dumps(redacted, ensure_ascii=False), redacted
    # Bare JSON scalar: nothing structural to walk.
    return redact_text(line), None


def redact_stream_line(line: str) -> str:
    """Return only the redacted text that would be persisted for ``line``."""
    return redact_stream_payload(line)[0]


def _digest(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def summarize_tool_input(value: Any) -> dict[str, Any]:
    """Represent a tool input by digest and explicitly safe metadata only.

    The raw input is never returned. Safe keys keep their scalar value; every
    other key contributes its name only.
    """
    try:
        serialized = json.dumps(value, sort_keys=True, default=str)
    except (TypeError, ValueError):
        serialized = str(value)
    summary: dict[str, Any] = {
        "input_digest": _digest(serialized),
        "input_size_bytes": len(serialized.encode("utf-8")),
    }
    if isinstance(value, dict):
        summary["input_keys"] = sorted(str(k) for k in value)
        safe: dict[str, Any] = {}
        for k, v in value.items():
            if str(k) in _SAFE_TOOL_INPUT_KEYS and isinstance(v, (str, int, float, bool)):
                safe[str(k)] = v
        if safe:
            summary["safe_input"] = safe
    return summary


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def _usage_delta(usage: Any) -> dict[str, int]:
    u = usage if isinstance(usage, dict) else {}
    def _i(*keys: str) -> int:
        for k in keys:
            v = u.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return int(v)
        return 0
    return {
        "input_tokens": _i("input_tokens", "prompt_tokens"),
        "output_tokens": _i("output_tokens", "completion_tokens"),
        "cache_read": _i("cache_read_input_tokens", "cache_read"),
        "cache_creation": _i("cache_creation_input_tokens", "cache_creation"),
    }


def normalize_stream_object(obj: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize one parsed stream-json object into zero or more safe events.

    Recognizes tool use, tool result, API retry, token usage/deltas, the final
    result, and provider errors. Unknown shapes yield no event (the raw line is
    still persisted and remains addressable by offset).
    """
    events: list[dict[str, Any]] = []
    otype = str(obj.get("type") or "")

    # Provider error / API retry envelopes.
    if otype in ("error", "provider_error"):
        events.append({
            "event_type": EVENT_PROVIDER_ERROR,
            "error": str(obj.get("error") or obj.get("message") or "")[:500],
        })
        return events
    if otype in ("api_retry", "retry"):
        events.append({
            "event_type": EVENT_API_RETRY,
            "attempt": int(obj.get("attempt") or 0),
            "reason": str(obj.get("reason") or obj.get("error") or "")[:300],
        })
        return events

    message = obj.get("message") if isinstance(obj.get("message"), dict) else {}
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = str(block.get("type") or "")
            if btype == "tool_use":
                ev = {
                    "event_type": EVENT_TOOL_USE,
                    "tool_name": str(block.get("name") or ""),
                    "tool_use_id": str(block.get("id") or ""),
                }
                ev.update(summarize_tool_input(block.get("input")))
                events.append(ev)
            elif btype == "tool_result":
                raw = block.get("content")
                serialized = raw if isinstance(raw, str) else json.dumps(raw, default=str)
                events.append({
                    "event_type": EVENT_TOOL_RESULT,
                    "tool_use_id": str(block.get("tool_use_id") or ""),
                    "is_error": bool(block.get("is_error")),
                    "result_digest": _digest(serialized),
                    "result_size_bytes": len(serialized.encode("utf-8")),
                })

    # Token usage may ride on the message or the envelope.
    usage = None
    if isinstance(message, dict) and isinstance(message.get("usage"), dict):
        usage = message["usage"]
    elif isinstance(obj.get("usage"), dict):
        usage = obj["usage"]
    if usage is not None and otype != "result":
        delta = _usage_delta(usage)
        if any(delta.values()):
            events.append({"event_type": EVENT_TOKEN_USAGE, **delta})

    if otype == "result":
        ev: dict[str, Any] = {
            "event_type": EVENT_RESULT,
            "is_error": bool(obj.get("is_error")),
            "subtype": str(obj.get("subtype") or ""),
        }
        cost = obj.get("total_cost_usd")
        if isinstance(cost, (int, float)) and not isinstance(cost, bool):
            ev["total_cost_usd"] = float(cost)
        if obj.get("session_id"):
            ev["session_id"] = str(obj["session_id"])
        if isinstance(obj.get("usage"), dict):
            ev["usage"] = _usage_delta(obj["usage"])
        events.append(ev)

    return events


# ---------------------------------------------------------------------------
# Capture
# ---------------------------------------------------------------------------

def capture_stream_evidence(
    lines: Iterable[str],
    out_dir: str | Path,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    drain_on_cap: bool = True,
    on_cap: Any = None,
) -> StreamCaptureResult:
    """Tee a redacted stream to ``raw_stream.jsonl`` and normalize it inline.

    ``lines`` is consumed lazily — the complete stream is never buffered. Each
    normalized event records the raw line number, byte offset and byte length of
    the redacted line it came from, so any event can be traced back to its bytes.

    At the byte cap the capture stops honestly. For a finite recorded stream
    (``drain_on_cap=True``) the remainder is counted so ``dropped_lines`` is
    exact. For a live provider process (``drain_on_cap=False``) the remainder is
    NOT drained — ``on_cap`` is invoked so the caller can terminate the process,
    ``dropped_lines`` stays 0 and ``remaining_lines_unknown`` is recorded.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_path = out / RAW_STREAM_FILENAME
    events_path = out / RUN_EVENTS_FILENAME

    result = StreamCaptureResult(
        raw_path=str(raw_path), events_path=str(events_path), max_bytes=max_bytes,
    )
    seq = 0
    offset = 0
    line_no = 0

    def _emit(fh, ev: dict[str, Any]) -> None:
        nonlocal seq
        seq += 1
        ev["schema_version"] = SCHEMA_VERSION
        ev["seq"] = seq
        fh.write(json.dumps(ev, sort_keys=False) + "\n")
        result.events_written += 1
        et = str(ev.get("event_type", ""))
        result.event_counts[et] = result.event_counts.get(et, 0) + 1

    # One shared iterator: the cap-drain below must continue where the main loop
    # stopped, never restart a re-iterable input such as a list.
    line_iter = iter(lines)

    with open(raw_path, "w", encoding="utf-8") as raw_fh, \
            open(events_path, "w", encoding="utf-8") as ev_fh:
        for line in line_iter:
            stripped = line.rstrip("\n")
            if not stripped.strip():
                continue
            line_no += 1

            # Redact BEFORE anything is persisted. Structural redaction returns
            # the decoded, already-redacted object so normalization never re-reads
            # unredacted bytes.
            redacted, decoded = redact_stream_payload(stripped)
            payload = (redacted + "\n").encode("utf-8")

            if result.raw_bytes_written + len(payload) > max_bytes:
                # Honest stop: nothing is silently dropped.
                result.cap_reached = True
                if drain_on_cap:
                    result.dropped_lines += 1
                    for _ in line_iter:  # count the remainder without persisting it
                        result.dropped_lines += 1
                else:
                    # Live stream: terminate the producer instead of draining it.
                    result.remaining_lines_unknown = True
                    if callable(on_cap):
                        try:
                            on_cap()
                        except Exception:
                            pass
                cap_ev: dict[str, Any] = {
                    "event_type": EVENT_CAP_REACHED,
                    "raw_line_number": line_no,
                    "raw_byte_offset": offset,
                    "raw_byte_length": 0,
                    "max_bytes": max_bytes,
                    "raw_bytes_written": result.raw_bytes_written,
                }
                if result.remaining_lines_unknown:
                    cap_ev["dropped_lines"] = None
                    cap_ev["remaining_lines"] = "unknown"
                    cap_ev["reason"] = "provider_process_terminated_at_cap"
                else:
                    cap_ev["dropped_lines"] = result.dropped_lines
                _emit(ev_fh, cap_ev)
                break

            raw_fh.write(redacted + "\n")
            line_offset = offset
            offset += len(payload)
            result.raw_bytes_written += len(payload)
            result.raw_lines_written += 1

            backref = {
                "raw_line_number": line_no,
                "raw_byte_offset": line_offset,
                "raw_byte_length": len(payload),
            }

            if decoded is None:
                result.malformed_lines += 1
                _emit(ev_fh, {
                    "event_type": EVENT_MALFORMED,
                    **backref,
                    "reason": "line is not valid json",
                })
                continue
            if not isinstance(decoded, dict):
                result.malformed_lines += 1
                _emit(ev_fh, {
                    "event_type": EVENT_MALFORMED,
                    **backref,
                    "reason": "line is not a json object",
                })
                continue

            for ev in normalize_stream_object(decoded):
                _emit(ev_fh, {**ev, **backref})

    return result


def iter_process_lines(stdout: Iterable[str]) -> Iterator[str]:
    """Yield lines from a subprocess stdout without buffering the whole stream."""
    yield from stdout


class StreamCapReached(RuntimeError):
    """Raised when the stream byte cap forced the provider to be terminated.

    This is an INCOMPLETE result, not a transport failure: it must not be retried
    like a timeout or a non-zero exit, and it must never be treated as a
    successful Builder/Reviewer response.
    """

    def __init__(self, message: str, *, capture: Any = None) -> None:
        super().__init__(message)
        self.capture = capture


#: Bytes of stderr retained. Stderr is drained concurrently and never buffered
#: whole, so a stderr flood can neither deadlock the child nor exhaust memory.
STDERR_TAIL_BYTES = 4000

#: Grace period between TERM and KILL when stopping a provider process tree.
_TERM_GRACE_SEC = 0.5


@dataclass
class StreamRunResult:
    """Outcome of running a provider process under stream capture."""
    capture: StreamCaptureResult
    returncode: int = 0
    terminated_at_cap: bool = False
    timed_out: bool = False
    stderr_tail: str = ""
    stderr_truncated: bool = False
    duration_ms: int = 0
    events: list[dict[str, Any]] = field(default_factory=list)


def _stop_process_tree(proc: Any) -> None:
    """TERM the whole process group, then KILL after a short grace period.

    Killing the group (not just the direct child) stops shells that spawned
    sleeping grandchildren. Falls back to the direct process when the platform
    has no process groups.
    """
    import os
    import signal

    def _signal_group(sig: int) -> bool:
        try:
            os.killpg(os.getpgid(proc.pid), sig)
            return True
        except Exception:
            return False

    if proc.poll() is not None:
        return
    if not _signal_group(signal.SIGTERM):
        try:
            proc.terminate()
        except Exception:
            pass
    try:
        proc.wait(timeout=_TERM_GRACE_SEC)
        return
    except Exception:
        pass
    if not _signal_group(signal.SIGKILL):
        try:
            proc.kill()
        except Exception:
            pass
    try:
        proc.wait(timeout=_TERM_GRACE_SEC)
    except Exception:
        pass


def run_streamed_command(
    argv: list[str],
    out_dir: str | Path,
    *,
    cwd: str | None = None,
    timeout_sec: int = 120,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> StreamRunResult:
    """Run a provider command, capturing its stream-json stdout incrementally.

    A real wall-clock deadline starts the moment the process launches. A watchdog
    stops the whole process group (TERM, then KILL after a grace period) once
    ``timeout_sec`` elapses, so a process that emits nothing — or emits one line
    and hangs — is still terminated. The deadline never waits for stdout EOF.

    stderr is drained concurrently into a bounded tail: a stderr flood can neither
    deadlock the child nor be buffered without limit.

    At the byte cap the process tree is stopped rather than drained, so an
    unbounded live stream is never read just to count what was skipped.
    """
    import subprocess
    import threading
    import time

    start = time.monotonic()
    proc = subprocess.Popen(
        argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1,
        start_new_session=True,  # own process group: we can stop the whole tree
    )

    terminated_at_cap = threading.Event()
    timed_out = threading.Event()
    finished = threading.Event()

    def _terminate_at_cap() -> None:
        terminated_at_cap.set()
        _stop_process_tree(proc)

    def _watchdog() -> None:
        # Deadline covers the entire process, not just the stdout phase.
        if not finished.wait(timeout=max(0.0, float(timeout_sec))):
            timed_out.set()
            _stop_process_tree(proc)

    stderr_chunks: list[str] = []
    stderr_bytes = {"n": 0}

    def _drain_stderr() -> None:
        if proc.stderr is None:
            return
        try:
            for chunk in iter(lambda: proc.stderr.read(4096), ""):
                if not chunk:
                    break
                stderr_bytes["n"] += len(chunk)
                stderr_chunks.append(chunk)
                # Keep only a bounded tail; older chunks are discarded.
                while len(stderr_chunks) > 2 and sum(
                    len(c) for c in stderr_chunks
                ) > STDERR_TAIL_BYTES * 2:
                    stderr_chunks.pop(0)
        except Exception:
            pass

    watchdog = threading.Thread(target=_watchdog, daemon=True)
    stderr_thread = threading.Thread(target=_drain_stderr, daemon=True)
    watchdog.start()
    stderr_thread.start()

    try:
        capture = capture_stream_evidence(
            iter_process_lines(proc.stdout or []), out_dir,
            max_bytes=max_bytes, drain_on_cap=False, on_cap=_terminate_at_cap,
        )
    finally:
        if proc.stdout is not None:
            try:
                proc.stdout.close()
            except Exception:
                pass
        # stdout is exhausted (or the tree was stopped); reap without hanging.
        try:
            proc.wait(timeout=max(0.0, timeout_sec - (time.monotonic() - start)) + _TERM_GRACE_SEC)
        except Exception:
            timed_out.set()
            _stop_process_tree(proc)
            try:
                proc.wait(timeout=_TERM_GRACE_SEC)
            except Exception:
                pass
        finished.set()          # release the watchdog immediately
        watchdog.join(timeout=_TERM_GRACE_SEC + 1.0)
        stderr_thread.join(timeout=_TERM_GRACE_SEC + 1.0)
        if proc.stderr is not None:
            try:
                proc.stderr.close()
            except Exception:
                pass

    tail = "".join(stderr_chunks)[-STDERR_TAIL_BYTES:]

    return StreamRunResult(
        capture=capture,
        returncode=proc.returncode if proc.returncode is not None else -1,
        terminated_at_cap=terminated_at_cap.is_set(),
        timed_out=timed_out.is_set(),
        stderr_tail=tail,
        stderr_truncated=stderr_bytes["n"] > len(tail),
        duration_ms=int((time.monotonic() - start) * 1000),
        events=read_run_events(capture.events_path),
    )


def usage_actuals_from_events(
    events: list[dict[str, Any]], *, cli_version: str = "",
) -> tuple[dict[str, Any] | None, str]:
    """Derive F003-compatible ``usage_actuals`` from normalized stream events.

    The final ``result`` event carries the authoritative cumulative usage; when
    it is absent, nothing is claimed (the caller falls back to the heuristic and
    records an honest missing reason).
    """
    final = None
    for ev in reversed(events):
        if ev.get("event_type") == EVENT_RESULT:
            final = ev
            break
    if final is None or not isinstance(final.get("usage"), dict):
        return None, "usage_missing"
    usage = final["usage"]
    actuals: dict[str, Any] = {
        "input_tokens": int(usage.get("input_tokens", 0) or 0),
        "output_tokens": int(usage.get("output_tokens", 0) or 0),
        "cache_read": int(usage.get("cache_read", 0) or 0),
        "cache_creation": int(usage.get("cache_creation", 0) or 0),
        "total_cost_usd": final.get("total_cost_usd"),
        "num_turns": 0,
        "duration_ms": 0,
        "session_id": str(final.get("session_id", "") or ""),
        "cli_version": cli_version,
        "parse_source": "claude_cli_stream_json",
    }
    return actuals, ""


@dataclass
class FinalStreamResult:
    """The complete classification of a stream's final ``result`` line.

    Read back from the persisted, redacted raw stream (the normalized events
    deliberately never carry model text). Carries everything the structured
    Reviewer needs to classify the call exactly like the non-stream JSON path —
    not just the extracted value.
    """

    found: bool = False
    #: Native structured output object (``structured_output``), or None.
    structured_output: Any = None
    has_structured_output: bool = False
    #: Legacy string ``result`` ("" when absent / non-string).
    result_text: str = ""
    is_error: bool = False
    subtype: str = ""
    errors: list = field(default_factory=list)
    total_cost_usd: float | None = None
    usage: dict[str, Any] = field(default_factory=dict)
    #: Backreference into the redacted raw stream.
    raw_line_number: int = 0
    raw_byte_offset: int = 0
    raw_byte_length: int = 0

    @property
    def structured_retry_exhausted(self) -> bool:
        return self.subtype == STRUCTURED_RETRY_EXHAUSTED_SUBTYPE

    @property
    def value_text(self) -> str:
        """Compact JSON of ``structured_output``, else the legacy result string."""
        if self.has_structured_output:
            try:
                return json.dumps(self.structured_output, separators=(",", ":"))
            except (TypeError, ValueError):
                return ""
        return self.result_text


def final_result_envelope(
    events: list[dict[str, Any]], raw_path: str | Path,
) -> FinalStreamResult:
    """Read the final result line from the redacted raw stream and classify it.

    Never raises. ``found=False`` when the stream carried no result line.
    """
    final = None
    for ev in reversed(events):
        if ev.get("event_type") == EVENT_RESULT:
            final = ev
            break
    if final is None:
        return FinalStreamResult()

    off, length = final.get("raw_byte_offset"), final.get("raw_byte_length")
    if not isinstance(off, int) or not isinstance(length, int) or length <= 0:
        return FinalStreamResult()
    try:
        with open(raw_path, "rb") as fh:
            fh.seek(off)
            chunk = fh.read(length).decode("utf-8", errors="replace")
        obj = json.loads(chunk)
    except (OSError, ValueError):
        return FinalStreamResult()
    if not isinstance(obj, dict):
        return FinalStreamResult()

    so = obj.get("structured_output")
    has_so = "structured_output" in obj and so is not None
    result_field = obj.get("result")
    errs = obj.get("errors")
    cost = obj.get("total_cost_usd")
    return FinalStreamResult(
        found=True,
        structured_output=so if has_so else None,
        has_structured_output=has_so,
        result_text=result_field if isinstance(result_field, str) else "",
        is_error=bool(obj.get("is_error", False)),
        subtype=str(obj.get("subtype", "") or ""),
        errors=list(errs) if isinstance(errs, list) else [],
        total_cost_usd=float(cost) if isinstance(cost, (int, float)) and not isinstance(cost, bool) else None,
        usage=obj["usage"] if isinstance(obj.get("usage"), dict) else {},
        raw_line_number=int(final.get("raw_line_number", 0) or 0),
        raw_byte_offset=off,
        raw_byte_length=length,
    )


def final_result_text(events: list[dict[str, Any]], raw_path: str | Path) -> str:
    """Recover the provider's final result value from the redacted raw stream.

    A native structured result carries the validated object in
    ``structured_output``; it is compact-serialized so the streamed path yields
    the same value as the non-stream JSON path. Legacy string ``result``
    otherwise. Kept as the thin value-only view over ``final_result_envelope``.
    """
    return final_result_envelope(events, raw_path).value_text


def read_run_events(path: str | Path) -> list[dict[str, Any]]:
    """Load normalized run events; malformed lines are skipped, never raised."""
    events: list[dict[str, Any]] = []
    p = Path(path)
    if not p.is_file():
        return events
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except (ValueError, TypeError):
                continue
            if isinstance(obj, dict):
                events.append(obj)
    return events


def sum_token_deltas(events: list[dict[str, Any]]) -> dict[str, int]:
    """Sum streamed token deltas. The final ``result`` usage wins when present,
    because the CLI reports cumulative totals there; otherwise deltas are summed.
    """
    for ev in reversed(events):
        if ev.get("event_type") == EVENT_RESULT and isinstance(ev.get("usage"), dict):
            return dict(ev["usage"])
    totals = {"input_tokens": 0, "output_tokens": 0, "cache_read": 0, "cache_creation": 0}
    for ev in events:
        if ev.get("event_type") != EVENT_TOKEN_USAGE:
            continue
        for k in totals:
            v = ev.get(k)
            if isinstance(v, int):
                totals[k] += v
    return totals
