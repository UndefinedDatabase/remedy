"""A planner call its order no longer wants ends in flight (operator order exec-1018, R-1346).

`order_cancel.cancel_order` writes the order's cancel request first, and the walk reads it before
and after every step. A step whose planner call was already running kept the walk busy until the
model finished: the local planner is one blocking `ollama.Client().chat()` with no timeout. Worse,
`mission_compiler.compile_mission_plan` turns any failure of its call into the deterministic
fallback plan, so even an interrupted call would have left a plan written after the cancel.

While a supervised walk makes a planner call, `planner_call_scope` binds the walk's reader of its
order's cancel request (`order_cancel.walk_cancel_reader`). Each planner reads it:

* the Ollama planner streams its answer (`cancellable_ollama_chat`) and the calling thread asks
  the reader every `PLANNER_CANCEL_POLL_SECONDS`; on a cancel it closes the HTTP connection of THIS
  request, which makes the Ollama server stop generating for it. No process is killed, so no
  Ollama server, model and other client is touched;
* the Claude CLI planner's guarded child gets the reader as its `cancel_check`
  (`pingpong_provider._cli_exec_policy`), so the guard ends that child's process tree as it ends a
  stopped job's Pi call.

Either raises `PlannerCallCancelled`, a `BaseException` on purpose, as `asyncio.CancelledError` is
one: every `except Exception` of the planning chain degrades to a fallback, and a cancelled call
must produce no plan at all. The walk's step catches it (`order_cancel._cancellable_step`) and
reads the request as it reads it after any step. An answer that arrives after the cancel is
discarded unread, so a late provider response cannot resume the order. Outside a supervised walk
nothing is bound, and every planner call is exactly the call it was before.

Remedy deliberately measures no token figure for a cancelled Ollama call: the server reports its
counts only in the final chunk, which a cancelled stream never receives. The order ledger records
the call with its seconds, the outcome `cancelled` and the size estimate it keeps for every planner
call (labelled an estimate there), never a measured count.
"""
from __future__ import annotations

import importlib
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

#: How often the calling thread asks whether the order was cancelled while the planner answers.
PLANNER_CANCEL_POLL_SECONDS = 0.25
#: How long a cancelled stream's reader thread is given to see its closed connection.
_READER_JOIN_SECONDS = 2.0

#: The reader of the walk's cancel request ("" while the order stands), bound for one planner call.
_PLANNER_CANCEL_READER: ContextVar[Callable[[], str] | None] = ContextVar("planner_cancel_reader", default=None)


class PlannerCallCancelled(BaseException):
    """A planner call ended in flight because its order was cancelled; never a planner failure.

    *seconds* is how long the call ran, *interrupted* whether the request itself was ended (its
    connection closed, its child process tree ended); False when the answer had already arrived
    and was discarded, or the client offered no way to end it.
    """

    def __init__(self, reason: str, *, seconds: float = 0.0, interrupted: bool = False) -> None:
        super().__init__(reason)
        self.reason = reason
        self.seconds = seconds
        self.interrupted = interrupted


@contextmanager
def planner_call_scope(reader: Callable[[], str] | None) -> Iterator[None]:
    """Bind *reader* (or nothing, for None) as the cancel reader of the planner calls inside."""
    token = _PLANNER_CANCEL_READER.set(reader)
    try:
        yield
    finally:
        _PLANNER_CANCEL_READER.reset(token)


def planner_cancel_reason() -> str:
    """Why the planner call in progress must end, or "" when nothing asks it to (or nothing is bound)."""
    reader = _PLANNER_CANCEL_READER.get()
    return reader() if reader is not None else ""


def planner_cancel_check() -> Callable[[], bool] | None:
    """The bound reader as an execution guard `cancel_check`, or None outside a cancellable call."""
    reader = _PLANNER_CANCEL_READER.get()
    return None if reader is None else (lambda: bool(reader()))


def cancellable_ollama_chat(client: Any, **request: Any) -> str:
    """The answer of `client.chat(**request)`, ended by the order's cancel when a reader is bound.

    Unbound, this is the plain blocking call. Bound, the answer is streamed by a reader thread while
    this thread polls the cancel reader; a cancel closes the client's HTTP connection (the server
    then stops generating for this request) and raises `PlannerCallCancelled`.
    """
    reader = _PLANNER_CANCEL_READER.get()
    if reader is None:
        return client.chat(**request).message.content
    began = time.monotonic()
    parts: list[str] = []
    failure: list[BaseException] = []
    done = threading.Event()
    errors = _stream_errors()

    def consume() -> None:
        try:
            for chunk in client.chat(stream=True, **request):
                parts.append(chunk.message.content or "")
            done.set()
        except errors as exc:      # handed to the calling thread, which raises it as the call's own
            failure.append(exc)

    worker = threading.Thread(target=consume, name="planner-stream", daemon=True)
    worker.start()
    while worker.is_alive():
        worker.join(PLANNER_CANCEL_POLL_SECONDS)
        reason = reader()
        if reason:
            closed = _close_connection(client) if worker.is_alive() else False
            worker.join(_READER_JOIN_SECONDS)
            raise PlannerCallCancelled(reason, seconds=time.monotonic() - began, interrupted=closed)
    if failure:
        raise failure[0]
    if not done.is_set():
        raise RuntimeError("the planner's answer stream ended without its answer")
    return "".join(parts)


def _stream_errors() -> tuple[type[BaseException], ...]:
    """What a streamed `ollama.Client.chat` raises: its own and httpx's errors where installed."""
    found: list[type[BaseException]] = [OSError, ValueError, RuntimeError]
    for module, name in (("httpx", "HTTPError"), ("ollama", "ResponseError")):
        try:
            found.append(getattr(importlib.import_module(module), name))
        except (ImportError, AttributeError):
            continue
    return tuple(found)


def _close_connection(client: Any) -> bool:
    """Close the HTTP client under *client* (`ollama.Client` keeps it as `_client`); False when absent."""
    transport = getattr(client, "_client", None)
    close = getattr(transport, "close", None)
    if not callable(close):
        return False
    try:
        close()
    except (OSError, RuntimeError):     # a connection that fails to close is still abandoned
        return False
    return True
