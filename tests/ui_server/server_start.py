"""Waiting for a UI server a test started in a thread to publish its info file.

Two findings, one wait.

R-0734. `start_ui_server` writes its info file with `Path.write_text`, which
CREATES the file before it WRITES it, so a poll landing between the two reads
zero bytes — or a prefix of the JSON. The old helpers tested `exists()` and then
parsed inside that branch, so `json.loads("")` raised `JSONDecodeError` out of
the retry loop and the fifty-attempt budget never got its second chance. Here a
file that is absent, empty or not yet a complete JSON object is one thing: "not
started yet".

R-0708. The old wait was a flat fifty polls at 0.1s — five seconds of wall clock
that a `pytest -n auto` run spends competing for CPU with every other worker, so
a perfectly healthy start lost the race and closure precondition 2 went red for
no reason of its own. The wait now reads the one signal that really says a start
FAILED: the server thread exited without publishing. While that thread is alive
the start is still in progress and the wait continues; when it has exited the
wait fails AT ONCE instead of burning a budget. `SERVER_START_BACKSTOP_S` exists
only so a start that hangs forever cannot hang the suite with it — it is not the
operative bound, and no healthy start comes near it.
"""
from __future__ import annotations

import json
import threading
import time
from collections.abc import Callable
from pathlib import Path

import pytest

SERVER_START_BACKSTOP_S = 120.0
POLL_S = 0.05


def read_server_info(info_file: str | Path) -> dict | None:
    """The published info, or None while the file is absent or half-written."""
    try:
        text = Path(info_file).read_text()
    except FileNotFoundError:
        return None
    try:
        info = json.loads(text)
    except json.JSONDecodeError:
        return None
    return info if isinstance(info, dict) and "port" in info else None


def wait_for_server_info(
    info_file: str | Path,
    thread: threading.Thread,
    *,
    backstop_s: float = SERVER_START_BACKSTOP_S,
    poll_s: float = POLL_S,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Poll until `info_file` parses, for as long as `thread` is alive."""
    deadline = clock() + backstop_s
    while True:
        info = read_server_info(info_file)
        if info is not None:
            return info
        if not thread.is_alive():
            pytest.fail("Server thread exited before publishing its info file")
        if clock() >= deadline:
            pytest.fail(
                f"Server thread still alive but unpublished after {backstop_s}s"
            )
        sleep(poll_s)
