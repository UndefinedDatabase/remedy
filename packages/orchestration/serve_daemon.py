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
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from packages.orchestration.serve_paths import ServePaths, serve_paths, socket_path_problem
from packages.orchestration.serve_runs import CommandRunner, RunLauncher, RunRefused, job_run_argv

#: `run_supervisor`'s own sentinel for `api_port`, distinguishing "the caller passed no
#: argument, so read `serve.api_port` from the configuration" from "the caller explicitly
#: passed `None`, so no listener binds" — the two cases a plain default of `None` cannot
#: tell apart, mirroring `self_use_runner._UNSET`.
_UNSET_API_PORT: Any = object()

#: The `source` an effect that arrives over the socket is recorded with: the word
#: `remedy job stop`, `remedy job pause` and `remedy job unpause` write direct.
SOCKET_EFFECT_SOURCE = "cli"

#: The one command the socket accepts beyond the cockpit door's own set (DECISION F200 D4).
JOB_RUN_COMMAND_ID = "job.run"


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
    #: The public HTTP API listener's bound port (S6a, DECISION F253 D6); `None` when no
    #: listener runs.
    api_port: int | None = None

    def to_json(self) -> dict[str, Any]:
        return {"running": self.running, "pid": self.pid, "socket": str(self.socket),
                "api_port": self.api_port}


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


def socket_handler_class(token: str, launcher: RunLauncher | None = None,
                         runner: CommandRunner | None = None) -> type:
    """The cockpit's request handler, bound for the supervisor's socket.

    With a LAUNCHER it also accepts `job.run` and starts the job's run through it;
    every other command takes the cockpit door's own path. With a RUNNER it also
    answers a write under `/api/v1` through it (DECISION F253 D9).
    """
    from packages.orchestration.ui_server import (
        COMMAND_EFFECT_FAILED_MESSAGE,
        _RemedyHandler,
        _safe_error,
    )

    class _SocketHandler(_RemedyHandler):
        server_token = token
        target_job_id = ""
        app_html = ""
        preview_worker = None
        effect_source = SOCKET_EFFECT_SOURCE
        client_names_source = True
        run_launcher = launcher
        command_runner = runner

        def _command_is_ui_exposed(self, command_id: str) -> bool:
            if command_id == JOB_RUN_COMMAND_ID:
                return self.run_launcher is not None
            return super()._command_is_ui_exposed(command_id)

        def _dispatch_extra_command(
                self, job: Any, payload: Any) -> tuple[int, dict[str, Any], str] | None:
            if payload["command"] != JOB_RUN_COMMAND_ID or self.run_launcher is None:
                return None
            args = payload.get("args")
            json_output = isinstance(args, dict) and args.get("json") is True
            try:
                record = self.run_launcher.start(str(job.job_id), json_output=json_output)
            except RunRefused as exc:
                return 409, {"error": str(exc), "code": exc.token}, "rejected_state"
            except OSError:
                status, body = _safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE)
                return status, body, "rejected_effect"
            return 200, {"command": JOB_RUN_COMMAND_ID, "outcome": "accepted",
                         **record.to_json()}, "accepted"

    return _SocketHandler


def public_api_handler_class(token: str, runner: CommandRunner | None = None) -> type:
    """The handler bound to the supervisor's public HTTP API listener (S6a, DECISION F253 D6).

    A subclass of `socket_handler_class(token, None, runner)` with no run launcher. Each of `do_GET`,
    `do_POST`, `do_PUT` and `do_DELETE` reads the path the way `do_POST` reads it, and passes
    a path `is_public_api_path` accepts to the inherited method, which answers it exactly as
    the socket does. Every other path, for every method, answers 404 `api_route_not_found`
    straight through `_send_json`, naming that this port serves only `/api/v1` — never through
    `_send_public_api_answer`, so a request this port does not serve writes no ledger line.
    """
    from apps.cli.json_envelope import build_error
    from packages.orchestration.public_api import PUBLIC_API_PREFIX, is_public_api_path

    base = socket_handler_class(token, None, runner)

    def _not_served(handler: Any, path: str) -> None:
        handler._send_json(404, build_error(
            "api_route_not_found",
            f"this port answers only the public HTTP API under {PUBLIC_API_PREFIX}; "
            f"'{path}' is not served here",
        ))

    class _PublicApiHandler(base):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(getattr(self, "path", ""))
            path = parsed.path.rstrip("/") or "/"
            if is_public_api_path(path):
                super().do_GET()
                return
            _not_served(self, path)

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(getattr(self, "path", ""))
            path = parsed.path.rstrip("/") or "/"
            if is_public_api_path(path):
                super().do_POST()
                return
            _not_served(self, path)

        def do_PUT(self) -> None:  # noqa: N802
            parsed = urlparse(getattr(self, "path", ""))
            path = parsed.path.rstrip("/") or "/"
            if is_public_api_path(path):
                super().do_PUT()
                return
            _not_served(self, path)

        def do_DELETE(self) -> None:  # noqa: N802
            parsed = urlparse(getattr(self, "path", ""))
            path = parsed.path.rstrip("/") or "/"
            if is_public_api_path(path):
                super().do_DELETE()
                return
            _not_served(self, path)

    return _PublicApiHandler


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


def read_api_port(paths: ServePaths) -> int | None:
    """The public HTTP API port the supervisor wrote, or None when there is no readable one."""
    try:
        port = int(paths.api_port_file.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None
    return port


def supervisor_state(root: Path | None = None) -> SupervisorState:
    """Whether a supervisor answers on ROOT's socket, its process id and API port if so."""
    paths = serve_paths(root)
    running = socket_answers(paths.socket)
    return SupervisorState(
        running=running, pid=read_pid(paths) if running else None, socket=paths.socket,
        api_port=read_api_port(paths) if running else None)


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
    run_argv: Callable[[str], list[str]] = job_run_argv,
    job_is_running: Callable[[str], bool] | None = None,
    api_port: int | None = _UNSET_API_PORT,
) -> None:
    """Answer ROOT's socket until STOP is set, or until SIGTERM or SIGINT arrives.

    Refuses a data root whose socket path is too long and a socket another
    supervisor already answers; a socket file nobody answers is what a killed
    supervisor leaves behind, and it is replaced. The socket, the process id file
    and the token file are removed when the supervisor ends. A run it started keeps
    running when it ends; RUN_ARGV builds each run's command, which tests replace.

    Before the supervisor serves any request on its socket, and before ON_READY
    is called (DECISION F200 D7), the registry is reconciled: every run this
    data root still names as open is adopted, restarted or declared lost — see
    `RunLauncher.resume_registered`, which JOB_IS_RUNNING is passed through to;
    tests replace it the way they replace RUN_ARGV.

    API_PORT left unset reads `serve.api_port` from `get_config()` (S6a, DECISION F253 D6);
    `None`, given or read, means no listener. Otherwise, after the socket server is created
    and before ON_READY, a threaded HTTP server is bound to `("127.0.0.1", API_PORT)` with
    `public_api_handler_class`, answering only `/api/v1`; an `OSError` from that bind raises
    `ServeError("serve_api_port_unavailable", ...)`, and the same `finally` blocks that remove
    the socket, the process id file and the token file still run. The bound port is written
    with `_write_private` to `paths.api_port_file`, served in its own daemon thread, passed to
    ON_READY's `SupervisorState`, and on the way out shut down, closed and removed with the
    other files.
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
    launcher = RunLauncher(paths, argv_for=run_argv)
    runner = CommandRunner(paths)
    server = _SocketServer(str(paths.socket), socket_handler_class(token, launcher, runner))
    if api_port is _UNSET_API_PORT:
        from packages.orchestration.config import get_config
        resolved_api_port = get_config().get("serve.api_port")
    else:
        resolved_api_port = api_port
    api_server: ThreadingHTTPServer | None = None
    bound_api_port: int | None = None
    try:
        os.chmod(paths.socket, 0o600)
        _write_private(paths.pid_file, str(os.getpid()))
        launcher.resume_registered(job_is_running=job_is_running)
        if resolved_api_port is not None:
            try:
                api_server = ThreadingHTTPServer(
                    ("127.0.0.1", resolved_api_port), public_api_handler_class(token, runner))
            except OSError as exc:
                raise ServeError(
                    "serve_api_port_unavailable",
                    f"the public HTTP API port {resolved_api_port} could not be bound: {exc}",
                ) from exc
            bound_api_port = api_server.server_address[1]
            _write_private(paths.api_port_file, str(bound_api_port))
        restore = _install_stop_signals(stop)
        thread = threading.Thread(target=server.serve_forever, name="remedy-serve", daemon=True)
        thread.start()
        api_thread: threading.Thread | None = None
        if api_server is not None:
            api_thread = threading.Thread(
                target=api_server.serve_forever, name="remedy-serve-api", daemon=True)
            api_thread.start()
        try:
            if on_ready is not None:
                on_ready(SupervisorState(running=True, pid=os.getpid(), socket=paths.socket,
                                         api_port=bound_api_port))
            while not stop.wait(0.2):
                pass
        finally:
            server.shutdown()
            thread.join()
            if api_server is not None and api_thread is not None:
                api_server.shutdown()
                api_thread.join()
            restore()
    finally:
        server.server_close()
        if api_server is not None:
            api_server.server_close()
        for path in (paths.socket, paths.pid_file, paths.token_file, paths.api_port_file):
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
