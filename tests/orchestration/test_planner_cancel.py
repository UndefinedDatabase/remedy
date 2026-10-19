"""exec-1018 (R-1346) — a planner call its order no longer wants ends in flight.

The Ollama case runs the real `ollama.Client` against a real local HTTP server that speaks Ollama's
streaming `/api/chat` protocol and never finishes on its own, and reads on the SERVER side that
the request's connection was closed: the call is ended, not merely abandoned. The Claude CLI case
runs a real child that sleeps, under the real execution guard. Both measure the latency from the
cancel to the end of the call.
"""
from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import SimpleNamespace

import pytest

from packages.orchestration.planner_cancel import (
    PLANNER_CANCEL_POLL_SECONDS,
    PlannerCallCancelled,
    cancellable_ollama_chat,
    planner_call_scope,
    planner_cancel_check,
    planner_cancel_reason,
)


class _EndlessChat(BaseHTTPRequestHandler):
    """`POST /api/chat`: one NDJSON chunk every 50 ms until the client goes away."""

    disconnected: threading.Event
    chunks_sent: list[int]

    def do_POST(self):  # noqa: N802 — the stdlib's handler name
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson")
        self.end_headers()
        chunk = json.dumps({"model": "m", "created_at": "2026-10-18T00:00:00Z",
                            "message": {"role": "assistant", "content": "{"}, "done": False}) + "\n"
        try:
            for n in range(2000):                  # about 100 s, far beyond any test's budget
                self.wfile.write(chunk.encode())
                self.wfile.flush()
                self.chunks_sent.append(n)
                time.sleep(0.05)
        except (BrokenPipeError, ConnectionResetError):
            type(self).disconnected.set()

    def log_message(self, *args):
        pass


@pytest.fixture
def endless_ollama():
    pytest.importorskip("ollama")
    handler = type("Handler", (_EndlessChat,), {"disconnected": threading.Event(), "chunks_sent": []})
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}", handler
    finally:
        server.shutdown()
        server.server_close()


def _cancel_after(seconds: float) -> tuple[callable, dict]:
    marks: dict[str, float] = {}
    began = time.monotonic()

    def reader() -> str:
        if time.monotonic() - began < seconds:
            return ""
        marks.setdefault("cancelled_at", time.monotonic())
        return "the order was cancelled (not wanted)"
    return reader, marks


def test_a_cancel_closes_the_ollama_request_itself_within_about_a_poll(endless_ollama):
    # The real client class: conftest's `_no_live_ollama_reach` refuses `ollama.Client` so that no
    # test reaches a LIVE server, and this one reaches only the fake server it started itself.
    from ollama._client import Client

    host, handler = endless_ollama
    reader, marks = _cancel_after(0.5)
    with planner_call_scope(reader), pytest.raises(PlannerCallCancelled) as ended:
        cancellable_ollama_chat(Client(host=host), model="m",
                                messages=[{"role": "user", "content": "plan"}], format={"type": "object"})
    latency = time.monotonic() - marks["cancelled_at"]

    assert ended.value.interrupted and ended.value.reason.startswith("the order was cancelled")
    assert latency < 2 * PLANNER_CANCEL_POLL_SECONDS + 1.0, latency
    assert handler.disconnected.wait(3.0), "the server never saw the request end"
    sent = len(handler.chunks_sent)
    time.sleep(0.3)
    assert len(handler.chunks_sent) == sent           # nothing more is generated for it


def test_without_a_bound_reader_the_call_is_the_plain_blocking_call():
    seen: list[dict] = []

    class Client:
        def chat(self, **request):
            seen.append(request)
            return SimpleNamespace(message=SimpleNamespace(content='{"ok": true}'))

    assert planner_cancel_reason() == "" and planner_cancel_check() is None
    assert cancellable_ollama_chat(Client(), model="m", messages=[]) == '{"ok": true}'
    assert seen == [{"model": "m", "messages": []}]       # no stream, nothing else changed


def test_a_bound_call_that_is_not_cancelled_answers_the_whole_streamed_text():
    class Client:
        def chat(self, *, stream, **request):
            assert stream is True
            return iter(SimpleNamespace(message=SimpleNamespace(content=part)) for part in ('{"a"', ": 1}"))

    with planner_call_scope(lambda: ""):
        assert cancellable_ollama_chat(Client(), model="m", messages=[]) == '{"a": 1}'


def test_an_answer_that_arrives_after_the_cancel_is_discarded_and_a_stream_error_is_the_calls_own():
    released = threading.Event()

    class Late:
        _client = SimpleNamespace(close=released.set)

        def chat(self, **request):
            released.wait(5)
            yield SimpleNamespace(message=SimpleNamespace(content='{"late": true}'))

    with planner_call_scope(lambda: "the order was cancelled (late)"), pytest.raises(PlannerCallCancelled):
        cancellable_ollama_chat(Late(), model="m", messages=[])

    class Broken:
        def chat(self, **request):
            raise ConnectionError("Failed to connect to Ollama")

    with planner_call_scope(lambda: ""), pytest.raises(ConnectionError):
        cancellable_ollama_chat(Broken(), model="m", messages=[])


@pytest.mark.subprocess
def test_a_cancel_ends_the_claude_cli_planners_child_through_its_guard(tmp_path, monkeypatch):
    from packages.providers.claude_planner.provider import ClaudeCliPlanner

    marker = f"{7000 + os.getpid() % 900}.{int(time.time()) % 89 + 10}"
    bindir = tmp_path / "bin"
    bindir.mkdir()
    (bindir / "claude").write_text(f"#!/bin/sh\nexec sleep {marker}\n")
    (bindir / "claude").chmod(0o755)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    reader, marks = _cancel_after(0.5)
    began = time.monotonic()
    with planner_call_scope(reader), pytest.raises(PlannerCallCancelled) as ended:
        ClaudeCliPlanner(timeout_sec=60).raw_call("plan", schema={"type": "object"})

    assert time.monotonic() - began < 5 and ended.value.interrupted
    assert time.monotonic() - marks["cancelled_at"] < 3
    alive = subprocess.run(["pgrep", "-f", f"sleep {marker}"], capture_output=True, text=True).stdout
    assert alive.strip() == ""                         # the child's process tree is gone
