"""Remedy's ceiling on ONE Pi agent loop: model turns and input tokens, read from the live event stream.

One Pi invocation runs an agent loop that resends the prompt and its growing history on every model
turn. On 2026-10-17 a three-line README append took 28 turns and 223,221 input tokens in one call,
and nothing stopped it: Remedy's budgets were checked between provider calls, never inside one.
Pi 1.2.0 has no turn or token limit of its own (its options list none), so Remedy reads the JSONL
stream as it arrives (`exec_guard.ExecGuardPolicy.stdout_observer`) and ends the sandboxed process
through the existing cancel path once the loop has used its turns or its input tokens and asks for
one more tool. A final answer is never cut off: the limit trips only when the model wants to go on.

The caps are `pi.max_turns_per_call` and `pi.max_input_tokens_per_call`, and the job's remaining
`max_total_tokens` lowers the input cap further, so an order's token cap holds inside a call too.
A tripped call ends `provider_error: pi_loop_limit: …`: the workspace keeps what the loop wrote,
the task ends `budget_exhausted`, and the turns and tokens it used are recorded, never lost.
"""
from __future__ import annotations

import threading
from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from packages.orchestration.pi_events import PiEventStream, PiRunSummary, PiStreamError, summarize_pi_events

#: The defaults of `pi.max_turns_per_call` and `pi.max_input_tokens_per_call` (measured: the
#: 2026-10-16 and 2026-10-17 incident calls took 19 to 28 turns at about 125,000 to 223,000 input
#: tokens, so a cap above both stops only a loop that is clearly running away).
PI_MAX_TURNS_PER_CALL_DEFAULT = 40
PI_MAX_INPUT_TOKENS_PER_CALL_DEFAULT = 400_000

#: The marker a capped call's error carries; `pingpong_loop.provider_failure_status` reads it.
PI_LOOP_LIMIT_MARK = "pi_loop_limit"

#: Yields the running job's tokens left under its `max_total_tokens`, or None without that cap.
_JOB_TOKENS_LEFT: ContextVar[Callable[[], int | None] | None] = ContextVar("pi_job_tokens_left", default=None)


@dataclass(frozen=True)
class PiLoopLimits:
    """The caps of one Pi call and what set each: `config`, `default` or `job_tokens_left`."""

    max_turns: int
    max_input_tokens: int
    turns_source: str = "default"
    input_source: str = "default"

    def to_json(self) -> dict[str, Any]:
        return {"max_turns": self.max_turns, "max_input_tokens": self.max_input_tokens,
                "turns_source": self.turns_source, "input_source": self.input_source}


def bind_job_token_budget(job: Any) -> None:
    """Let Pi calls made for *job* read its tokens left under `max_total_tokens` (None: no cap)."""
    def left() -> int | None:
        budgets = job.budgets if isinstance(job.budgets, dict) else (
            job.budgets.model_dump() if job.budgets is not None else {})
        cap = budgets.get("max_total_tokens")
        if not isinstance(cap, int):
            return None
        used = (getattr(job, "budget_actuals", None) or {}).get("total_tokens") or 0
        return max(cap - int(used), 0)

    _JOB_TOKENS_LEFT.set(left)


def _configured(key: str, default: int) -> tuple[int, str]:
    try:
        from packages.orchestration.config import get_config
        value = get_config().get(key)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        value = None                 # an unreadable config keeps the documented default
    if isinstance(value, int) and not isinstance(value, bool) and value > 0:
        return value, "config" if value != default else "default"
    return default, "default"


def pi_loop_limits() -> PiLoopLimits:
    """The caps for the next Pi call: the configured ones, the input cap lowered to the job's tokens left."""
    turns, turns_source = _configured("pi.max_turns_per_call", PI_MAX_TURNS_PER_CALL_DEFAULT)
    tokens, input_source = _configured("pi.max_input_tokens_per_call", PI_MAX_INPUT_TOKENS_PER_CALL_DEFAULT)
    clock = _JOB_TOKENS_LEFT.get()
    left = clock() if clock is not None else None
    if left is not None and left < tokens:
        tokens, input_source = max(left, 1), "job_tokens_left"
    return PiLoopLimits(turns, tokens, turns_source, input_source)


class PiLoopWatch:
    """Fed every stdout chunk of one Pi call (from the stream pump's thread); `tripped` says why to stop."""

    def __init__(self, limits: PiLoopLimits) -> None:
        self.limits = limits
        self.tripped = ""
        self._stream = PiEventStream()
        self._events: list[dict[str, Any]] = []
        self._turns = 0
        self._input = 0
        self._lock = threading.Lock()

    def feed(self, chunk: bytes) -> None:
        try:
            records = self._stream.feed(chunk)
        except PiStreamError:
            return                   # the whole-stream parse after the call reports a malformed stream
        with self._lock:
            for record in records:
                self._events.append(record)
                self._count(record)

    def _count(self, record: dict[str, Any]) -> None:
        kind = record.get("type")
        message = record.get("message")
        if kind == "message_end" and isinstance(message, dict) and message.get("role") == "assistant":
            self._turns += 1
            usage = message.get("usage")
            value = usage.get("input") if isinstance(usage, dict) else None
            self._input += value if isinstance(value, int) and not isinstance(value, bool) else 0
        elif kind == "tool_execution_start" and not self.tripped:
            if self._turns >= self.limits.max_turns:
                self.tripped = (f"the agent loop used its {self.limits.max_turns} model turns "
                                f"(pi.max_turns_per_call) and asked for another tool")
            elif self._input >= self.limits.max_input_tokens:
                self.tripped = (f"the agent loop used {self._input} input tokens over {self._turns} turns, "
                                f"at or above its cap of {self.limits.max_input_tokens} "
                                f"({self.limits.input_source}), and asked for another tool")

    def cancel_check(self, job_stop: Callable[[], bool] | None) -> Callable[[], bool]:
        """The guard's cancel predicate: this loop's limit, or the job's stop request."""
        return lambda: bool(self.tripped) or bool(job_stop is not None and job_stop())

    def summary(self) -> PiRunSummary:
        """What the events received so far say: a cut stream's turns and usage are still real."""
        with self._lock:
            return summarize_pi_events(list(self._events))
