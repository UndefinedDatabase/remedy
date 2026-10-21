"""The worker pulse: a small per-job file every Pi call keeps current (DECISION F311 D2).

The runner holds a job in memory and rewrites `job.json` whole at its own safe points, so a
stamp written into the job record from the thread that reads a worker's stream would be
overwritten at the runner's next safe point, and the active role, model and round exist only
in memory while a call runs. The worker pulse is a file of its own, owned here, so a running
job's current call, when it last produced output, and its last `PULSE_STREAM_LIMIT` stream
entries survive a restart of the daemon without competing with the job record's own writer.
"""
from __future__ import annotations

import json
import threading
from collections.abc import Callable
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.common.secure_fs import durable_write_json
from packages.orchestration.data_paths import worker_pulse_path
from packages.orchestration.stream_evidence import redact_text

#: Version of the pulse file's shape; `read_worker_pulse` refuses any other.
WORKER_PULSE_VERSION = 1
#: The kinds one stream entry may carry (DECISION F311 D2).
PULSE_STREAM_KINDS = ("model_text", "tool_call", "tool_result", "system")
#: At most this many stream entries are kept, oldest first.
PULSE_STREAM_LIMIT = 200
#: A stream entry's text is cut to this many characters, after redaction.
PULSE_TEXT_LIMIT = 200
#: `observe_output` and `add_pi_record` write to disk only after this many seconds have passed
#: since the last disk write; `bind`, `begin_call` and `end_call` always write at once.
PULSE_WRITE_INTERVAL_S = 2.0

#: The pulse `bind_worker_pulse` bound for the job whose calls are running in this context.
_CURRENT_PULSE: ContextVar[WorkerPulse | None] = ContextVar("worker_pulse_current", default=None)


def _compact_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _pulse_text(text: str) -> str:
    return redact_text(text)[:PULSE_TEXT_LIMIT]


def _pulse_entry(record: dict[str, Any], *, at: str, role: str | None) -> dict[str, Any] | None:
    """One stream entry for *record*, or None when it maps to none (DECISION F311 D2)."""
    kind = record.get("type")
    if kind == "message_end":
        message = record.get("message")
        if not isinstance(message, dict) or message.get("role") != "assistant":
            return None
        blocks = message.get("content")
        texts = [b.get("text", "") for b in blocks
                 if isinstance(b, dict) and b.get("type") == "text"] if isinstance(blocks, list) else []
        text = "".join(t for t in texts if isinstance(t, str))
        return {"at": at, "role": role, "kind": "model_text", "text": _pulse_text(text)}
    if kind == "tool_execution_start":
        tool = str(record.get("toolName") or "?")
        args = record.get("args")
        text = _compact_json(args) if args is not None else ""
        return {"at": at, "role": role, "kind": "tool_call", "tool": tool, "text": _pulse_text(text)}
    if kind == "tool_execution_end":
        tool = str(record.get("toolName") or "?")
        result = record.get("result")
        length = len(_compact_json(result)) if result is not None else 0
        return {"at": at, "role": role, "kind": "tool_result", "tool": tool, "length": length}
    if kind in ("auto_retry_start", "agent_settled"):
        return {"at": at, "role": role, "kind": "system", "text": _pulse_text(str(kind))}
    return None


class WorkerPulse:
    """One job's own worker pulse: the call in progress, its role and round, when it last
    produced output, and its last `PULSE_STREAM_LIMIT` stream entries.

    Every method is safe to call from the stream pump's thread; one lock serializes every read
    and write of the in-memory state. A disk write that raises `OSError` is swallowed and leaves
    the pulse in memory: a pulse never fails the call it describes.
    """

    def __init__(self, job_id: str, path: Path, *, clock: Callable[[], datetime] | None = None) -> None:
        self._job_id = job_id
        self._path = path
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._lock = threading.Lock()
        self._state: dict[str, Any] = {}
        self._last_write_at: datetime | None = None

    def _now_str(self) -> str:
        # The time format `serve_runs._now` writes.
        return self._clock().strftime("%Y-%m-%dT%H:%M:%SZ")

    def _write_locked(self) -> None:
        """Write the current state to disk now; called with the lock held. Never raises."""
        try:
            durable_write_json(self._path, dict(self._state))
        except OSError:
            pass    # DECISION F311 D2: a pulse write never fails the call it describes
        self._last_write_at = self._clock()

    def _throttled_write_locked(self) -> None:
        now = self._clock()
        if self._last_write_at is None or (now - self._last_write_at).total_seconds() >= PULSE_WRITE_INTERVAL_S:
            self._write_locked()

    def bind(self) -> None:
        """Write a fresh pulse: no call in progress, no stream, silence counted from now."""
        now = self._now_str()
        with self._lock:
            self._state = {
                "version": WORKER_PULSE_VERSION, "job_id": self._job_id, "bound_at": now,
                "role": None, "provider": None, "model": None, "round": None, "call_kind": None,
                "call_started_at": None, "call_ended_at": None, "last_output_at": now, "stream": [],
            }
            self._write_locked()

    def begin_call(self, *, role: str, provider: str, model: str, round_no: int, kind: str) -> None:
        """Record the call about to start; written at once."""
        with self._lock:
            self._state.update({
                "role": role, "provider": provider, "model": model, "round": round_no,
                "call_kind": kind, "call_started_at": self._now_str(), "call_ended_at": None,
            })
            self._write_locked()

    def end_call(self) -> None:
        """Record that the call ended; written at once."""
        with self._lock:
            self._state["call_ended_at"] = self._now_str()
            self._write_locked()

    def observe_output(self) -> None:
        """One chunk of standard output arrived: move the silence clock."""
        with self._lock:
            self._state["last_output_at"] = self._now_str()
            self._throttled_write_locked()

    def add_pi_record(self, record: dict[str, Any]) -> None:
        """Map one parsed Pi event record to at most one stream entry (DECISION F311 D2)."""
        now = self._now_str()
        with self._lock:
            self._state["last_output_at"] = now
            entry = _pulse_entry(record, at=now, role=self._state.get("role"))
            if entry is not None:
                stream = self._state.setdefault("stream", [])
                stream.append(entry)
                if len(stream) > PULSE_STREAM_LIMIT:
                    del stream[: len(stream) - PULSE_STREAM_LIMIT]
            self._throttled_write_locked()

    def snapshot(self) -> dict[str, Any]:
        """A copy of the pulse's current in-memory state."""
        with self._lock:
            return json.loads(json.dumps(self._state))


def bind_worker_pulse(job: Any) -> WorkerPulse | None:
    """Build this job's worker pulse, bind it for `current_worker_pulse`, and return it.

    A job with no `job_id` (a run with no persisted record) gets no pulse: `current_worker_pulse`
    then answers None and a Pi call behaves exactly as it did before `worker_pulse` existed.
    """
    job_id = getattr(job, "job_id", None)
    if not job_id:
        _CURRENT_PULSE.set(None)
        return None
    pulse = WorkerPulse(job_id, worker_pulse_path(job_id))
    pulse.bind()
    _CURRENT_PULSE.set(pulse)
    return pulse


def current_worker_pulse() -> WorkerPulse | None:
    """The pulse `bind_worker_pulse` bound for this job's calls, or None."""
    return _CURRENT_PULSE.get()


def read_worker_pulse(job_id: str, root: Path | None = None) -> dict[str, Any] | None:
    """The pulse as written on disk, or None when it is absent, unreadable, not a JSON object,
    or of another `version`."""
    path = worker_pulse_path(job_id, root)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = json.loads(raw)
    except ValueError:
        return None
    if not isinstance(data, dict) or data.get("version") != WORKER_PULSE_VERSION:
        return None
    return data
