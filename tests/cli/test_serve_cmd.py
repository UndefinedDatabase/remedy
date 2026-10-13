"""`remedy serve start`, `remedy serve status` and `remedy serve stop` (F200, DECISION F200 D1).

The lifecycle test starts the supervisor as its own process, the way an operator,
a systemd unit or a container does, and stops it with `remedy serve stop`; its
`finally` kills the process if any step before that failed, so no run leaves a
supervisor behind.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from packages.orchestration.crash_report import crash_reports_dir
from packages.orchestration.serve_daemon import socket_answers
from packages.orchestration.serve_paths import serve_paths

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture
def root(tmp_path_factory, monkeypatch):
    base = tmp_path_factory.mktemp("sc")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(base))
    return base


def _remedy(root: Path, *argv: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    return subprocess.run([sys.executable, "-m", "apps.cli.main", *argv], cwd=REPO, env=env,
                          capture_output=True, text=True, timeout=60)


def _envelope(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.count("\n") == 1, proc.stdout
    return json.loads(proc.stdout)


def test_status_with_no_supervisor_reports_not_running(root):
    proc = _remedy(root, "serve", "status", "--json")
    assert proc.returncode == 0, proc.stderr
    body = _envelope(proc)
    assert (body["ok"], body["running"], body["pid"]) == (True, False, None)
    assert body["socket"] == str(serve_paths(root).socket)
    assert body["api_port"] is None


def test_stop_with_no_supervisor_stops_nothing_and_succeeds(root):
    proc = _remedy(root, "serve", "stop")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "No serve supervisor is running for this data root.\n"


def test_start_status_stop_runs_one_supervisor_and_cleans_up_after_it(root):
    paths = serve_paths(root)
    env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    server = subprocess.Popen([sys.executable, "-m", "apps.cli.main", "serve", "start", "--json"],
                              cwd=REPO, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
    try:
        ready = json.loads(server.stdout.readline())
        assert (ready["ok"], ready["running"], ready["pid"]) == (True, True, server.pid)
        assert ready["socket"] == str(paths.socket)
        assert socket_answers(paths.socket)

        status = _envelope(_remedy(root, "serve", "status", "--json"))
        assert (status["running"], status["pid"]) == (True, server.pid)

        again = _remedy(root, "serve", "start", "--json")
        assert again.returncode == 1
        assert _envelope(again)["error"] == "serve_already_running"

        stop = _remedy(root, "serve", "stop", "--json")
        assert stop.returncode == 0, stop.stderr
        assert _envelope(stop)["stopped"] is True
        assert server.wait(timeout=20) == 0
    finally:
        if server.poll() is None:
            server.kill()
            server.wait(timeout=20)
        server.stdout.close()
        server.stderr.close()
    deadline = time.monotonic() + 5
    while paths.socket.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert not paths.socket.exists()
    assert not paths.pid_file.exists()
    assert not paths.token_file.exists()


def test_serve_start_installs_the_thread_crash_hook_and_restores_the_previous_one(
    root, monkeypatch,
):
    import packages.orchestration.serve_daemon as serve_daemon
    from apps.cli.commands.serve_cmd import _cmd_serve_start

    seen: list[threading.ExceptHookArgs] = []
    monkeypatch.setattr(threading, "excepthook", seen.append)
    recorder = threading.excepthook

    def boom() -> None:
        raise RuntimeError("boom")

    def supervisor_with_a_crashing_thread(*, on_ready) -> None:
        worker = threading.Thread(target=boom, name="remedy-serve-test")
        worker.start()
        worker.join()

    monkeypatch.setattr(serve_daemon, "run_supervisor", supervisor_with_a_crashing_thread)
    _cmd_serve_start(json_output=True)
    assert len(seen) == 1
    assert threading.excepthook == recorder
    reports = list(crash_reports_dir().glob("*.md"))
    assert len(reports) == 1
    text = reports[0].read_text(encoding="utf-8")
    assert "- command: serve.start (thread remedy-serve-test)" in text
    assert "RuntimeError: boom" in text
