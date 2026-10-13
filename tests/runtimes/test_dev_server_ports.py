"""F306 T003 — `port_listener_in_session`, the ownership check a runtime-flow
check makes before it trusts a health answer (R-1251).

Real subprocesses and real sockets only: the function enumerates the live
process table, so a fake psutil object would prove nothing about the real one.
"""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import time

import psutil

from packages.runtimes.dev_server_ports import port_listener_in_session
from tests.ports import worker_port

#: A tiny child that binds the port handed to it on argv, then sleeps.
_LISTENER = (
    "import socket, sys, time\n"
    "port = int(sys.argv[1])\n"
    "sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
    "sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n"
    "sock.bind(('127.0.0.1', port))\n"
    "sock.listen(1)\n"
    "sys.stdout.write('listening\\n')\n"
    "sys.stdout.flush()\n"
    "time.sleep(30)\n"
)

#: A child with a session of its own that binds nothing.
_IDLE = "import time\ntime.sleep(30)\n"


def _spawn(script: str, *args: str) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, "-c", script, *args], start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def _stop(proc: subprocess.Popen) -> None:
    proc.terminate()
    try:
        proc.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5.0)


def _wait_connectable(port: int, deadline: float) -> None:
    while time.monotonic() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.2)
            try:
                probe.connect(("127.0.0.1", port))
            except OSError:
                time.sleep(0.05)
                continue
            return
    raise AssertionError(f"nothing ever listened on {port}")


class TestPortListenerInSession:
    def test_a_child_in_its_own_session_reads_true_for_its_group(self):
        port = worker_port(6)
        child = _spawn(_LISTENER, str(port))
        try:
            _wait_connectable(port, time.monotonic() + 10.0)
            session_id = os.getpgid(child.pid)
            assert port_listener_in_session(port, session_id) is True
        finally:
            _stop(child)

    def test_a_listener_in_a_different_session_reads_false(self):
        port = worker_port(7)
        # a process with a session of its own, so its pgid differs from ours
        # and from the port's real holder (this test process)
        child = _spawn(_IDLE)
        try:
            child_session = os.getpgid(child.pid)
            assert child_session != os.getpgid(os.getpid())
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("127.0.0.1", port))
                sock.listen(1)
                assert port_listener_in_session(port, child_session) is False
        finally:
            _stop(child)

    def test_a_psutil_failure_of_the_whole_read_answers_none(self, monkeypatch):
        def _boom(*_a, **_kw):
            raise psutil.AccessDenied()

        monkeypatch.setattr(psutil, "process_iter", _boom)
        session_id = os.getpgid(os.getpid())
        assert port_listener_in_session(worker_port(8), session_id) is None

    def test_a_denied_connections_read_in_the_session_answers_none(self, monkeypatch):
        """A member of the session IS there, but its sockets cannot be read: this
        must never be mistaken for proof that the port is foreign (R-1251)."""
        def _denied(self, *_a, **_kw):
            raise psutil.AccessDenied(pid=self.pid)

        monkeypatch.setattr(psutil.Process, "connections", _denied)
        if hasattr(psutil.Process, "net_connections"):
            monkeypatch.setattr(psutil.Process, "net_connections", _denied)

        child = _spawn(_IDLE)
        try:
            session_id = os.getpgid(child.pid)
            assert port_listener_in_session(worker_port(9), session_id) is None
        finally:
            _stop(child)
