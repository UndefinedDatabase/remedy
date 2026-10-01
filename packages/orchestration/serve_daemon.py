"""The `remedy serve start` supervisor (F200, DECISION F200 D1).

One supervisor runs per data root, in the foreground of whatever started it: a
terminal, a systemd unit or a container. It listens on the unix socket
`serve_paths` names and answers it with the cockpit's own request handler, so the
socket carries exactly the F009 command envelope through exactly the cockpit
door's checks, and no second write protocol exists. The one difference is the
`source` the door records an effect with, `SOCKET_EFFECT_SOURCE`, which is the
word the command line writes when it runs the same command direct.

Who may talk to it is decided by the file system: the `serve` directory is
readable by its owner only, and so are the socket and the token file inside it.
The door still demands the token, as the cockpit's door does, so a client reads
it from the token file. A supervisor counts as running exactly when its socket
answers a connection; the process id file is read only to stop it.
"""
from __future__ import annotations

import json
import os
import secrets
import signal
import socket
import socketserver
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from http.client import HTTPConnection
from pathlib import Path
from typing import Any

from packages.orchestration.serve_paths import ServePaths, serve_paths, socket_path_problem

#: The `source` an effect that arrives over the socket is recorded with: the word
#: `remedy job stop`, `remedy job pause` and `remedy job unpause` write direct.
SOCKET_EFFECT_SOURCE = "cli"


class ServeError(Exception):
    """Why the supervisor cannot start or stop, with the error token the CLI reports."""

    def __init__(self, token: str, message: str) -> None:
        super().__init__(message)
        self.token = token


@dataclass(frozen=True)
class SupervisorState:
    """What `remedy serve status` reports for one data root."""

    running: bool
    pid: int | None
    socket: Path

    def to_json(self) -> dict[str, Any]:
        return {"running": self.running, "pid": self.pid, "socket": str(self.socket)}


class _SocketServer(socketserver.ThreadingUnixStreamServer):
    daemon_threads = True


class UnixHTTPConnection(HTTPConnection):
    """An HTTP connection to a unix socket path instead of a host and port."""

    def __init__(self, path: Path, timeout: float = 10.0) -> None:
        super().__init__("localhost", timeout=timeout)
        self._socket_path = str(path)

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            sock.connect(self._socket_path)
        except OSError:
            sock.close()
            raise
        self.sock = sock


def socket_handler_class(token: str) -> type:
    """The cockpit's request handler, bound for the supervisor's socket."""
    from packages.orchestration.ui_server import _RemedyHandler

    return type("_SocketHandler", (_RemedyHandler,), {
        "server_token": token,
        "target_job_id": "",
        "app_html": "",
        "preview_worker": None,
        "effect_source": SOCKET_EFFECT_SOURCE,
        "client_names_source": True,
    })


def socket_answers(path: Path, timeout: float = 1.0) -> bool:
    """True when a process accepts a connection on the unix socket at PATH."""
    if not path.exists():
        return False
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect(str(path))
        except OSError:
            return False
    return True


def read_pid(paths: ServePaths) -> int | None:
    """The process id the supervisor wrote, or None when there is no readable one."""
    try:
        pid = int(paths.pid_file.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None
    return pid if pid > 0 else None


def supervisor_state(root: Path | None = None) -> SupervisorState:
    """Whether a supervisor answers on ROOT's socket, and its process id if so."""
    paths = serve_paths(root)
    running = socket_answers(paths.socket)
    return SupervisorState(running=running, pid=read_pid(paths) if running else None,
                           socket=paths.socket)


def _write_private(path: Path, text: str) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.fchmod(fd, 0o600)
        os.write(fd, text.encode("utf-8"))
    finally:
        os.close(fd)


def _install_stop_signals(stop: threading.Event) -> Callable[[], None]:
    """Let SIGTERM and SIGINT set STOP; return the function that restores the old handlers."""
    if threading.current_thread() is not threading.main_thread():
        return lambda: None
    previous = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT)}
    for sig in previous:
        signal.signal(sig, lambda _signum, _frame: stop.set())

    def restore() -> None:
        for sig, handler in previous.items():
            signal.signal(sig, handler)

    return restore


def run_supervisor(
    root: Path | None = None,
    *,
    stop: threading.Event | None = None,
    on_ready: Callable[[SupervisorState], None] | None = None,
) -> None:
    """Answer ROOT's socket until STOP is set, or until SIGTERM or SIGINT arrives.

    Refuses a data root whose socket path is too long and a socket another
    supervisor already answers; a socket file nobody answers is what a killed
    supervisor leaves behind, and it is replaced. The socket, the process id file
    and the token file are removed when the supervisor ends.
    """
    paths = serve_paths(root)
    problem = socket_path_problem(paths.socket)
    if problem:
        raise ServeError("serve_socket_path_too_long", problem)
    paths.root.mkdir(parents=True, exist_ok=True)
    os.chmod(paths.root, 0o700)
    if socket_answers(paths.socket):
        raise ServeError("serve_already_running",
                         f"a serve supervisor already answers on {paths.socket} "
                         f"(process {read_pid(paths)})")
    paths.socket.unlink(missing_ok=True)
    token = secrets.token_urlsafe(24)
    _write_private(paths.token_file, token)
    stop = stop if stop is not None else threading.Event()
    server = _SocketServer(str(paths.socket), socket_handler_class(token))
    try:
        os.chmod(paths.socket, 0o600)
        _write_private(paths.pid_file, str(os.getpid()))
        restore = _install_stop_signals(stop)
        thread = threading.Thread(target=server.serve_forever, name="remedy-serve", daemon=True)
        thread.start()
        try:
            if on_ready is not None:
                on_ready(SupervisorState(running=True, pid=os.getpid(), socket=paths.socket))
            while not stop.wait(0.2):
                pass
        finally:
            server.shutdown()
            thread.join()
            restore()
    finally:
        server.server_close()
        for path in (paths.socket, paths.pid_file, paths.token_file):
            path.unlink(missing_ok=True)


def stop_supervisor(root: Path | None = None, *, timeout: float = 10.0) -> bool:
    """Send SIGTERM to the supervisor answering ROOT's socket and wait for it to end.

    False when no supervisor answers; a supervisor that still answers after
    TIMEOUT seconds raises.
    """
    paths = serve_paths(root)
    if not socket_answers(paths.socket):
        return False
    pid = read_pid(paths)
    if pid is None:
        raise ServeError("serve_pid_unknown",
                         f"a supervisor answers on {paths.socket} but {paths.pid_file} "
                         f"holds no process id")
    os.kill(pid, signal.SIGTERM)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not socket_answers(paths.socket):
            return True
        time.sleep(0.05)
    raise ServeError("serve_stop_timeout",
                     f"the supervisor (process {pid}) still answers on {paths.socket} "
                     f"after {timeout:g} seconds")


def post_command(root: Path | None, job_id: str, envelope: dict[str, Any],
                 *, timeout: float = 30.0) -> tuple[int, dict[str, Any]]:
    """Send one F009 command envelope for JOB_ID to ROOT's supervisor; (status, body)."""
    from packages.orchestration.ui_server import COMMAND_CSRF_HEADER

    paths = serve_paths(root)
    token = paths.token_file.read_text(encoding="utf-8").strip()
    conn = UnixHTTPConnection(paths.socket, timeout=timeout)
    try:
        conn.request("POST", f"/api/jobs/{job_id}/commands", body=json.dumps(envelope),
                     headers={"Authorization": f"Bearer {token}", COMMAND_CSRF_HEADER: token,
                              "Content-Type": "application/json"})
        response = conn.getresponse()
        return response.status, json.loads(response.read())
    finally:
        conn.close()
