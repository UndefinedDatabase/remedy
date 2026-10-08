"""The `remedy serve start` supervisor (F200, DECISIONs F200 D1 and D2).

Each test runs the supervisor in a thread of this process against its own data
root and ends it through the supervisor's stop event, never through a signal: the
supervisor's process id file names THIS process, and a SIGTERM would end the run.
The socket is a real unix socket, and the requests are real HTTP requests on it.
"""
from __future__ import annotations

import json
import os
import socket
import stat
import subprocess
import sys
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration import safe_points
from packages.orchestration import serve_daemon as SD
from packages.orchestration import serve_runs as SR
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.serve_paths import serve_paths

REPO = Path(__file__).resolve().parents[2]
#: `run_supervisor`'s own sentinel, re-exported so this module's tests can tell "pass no
#: `api_port` keyword at all" apart from "pass `None`" the same way `_Running` below does.
_UNSET_API_PORT = SD._UNSET_API_PORT


@pytest.fixture
def root(tmp_path_factory, monkeypatch):
    """A short data root, so the socket path stays far below the length limit."""
    base = tmp_path_factory.mktemp("sv")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(base))
    return base


class _Running:
    """A supervisor running in a thread until `close` sets its stop event.

    `api_port` left at its own unset sentinel means the keyword is never passed to
    `run_supervisor`, so it reads `serve.api_port` from the configuration itself, the way a
    real start does; passing `0` or `None` here passes it through unchanged.
    """

    def __init__(self, root: Path, run_argv=None, api_port=_UNSET_API_PORT) -> None:
        self.stop = threading.Event()
        self.ready = threading.Event()
        self.errors: list[Exception] = []
        self.state: SD.SupervisorState | None = None

        def ready(state: SD.SupervisorState) -> None:
            self.state = state
            self.ready.set()

        def run() -> None:
            kwargs = {}
            if run_argv is not None:
                kwargs["run_argv"] = run_argv
            if api_port is not _UNSET_API_PORT:
                kwargs["api_port"] = api_port
            try:
                SD.run_supervisor(root, stop=self.stop, on_ready=ready, **kwargs)
            except (SD.ServeError, OSError) as exc:
                self.errors.append(exc)
                self.ready.set()

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        assert self.ready.wait(10), "the supervisor never became ready"
        assert not self.errors, self.errors

    def close(self) -> None:
        self.stop.set()
        self.thread.join(10)
        assert not self.thread.is_alive(), "the supervisor did not end"


@pytest.fixture
def running(root):
    supervisor = _Running(root)
    yield supervisor
    supervisor.close()


@pytest.fixture
def running_with_api(root):
    """A supervisor whose public HTTP API listener is bound to a free port (S6a)."""
    supervisor = _Running(root, api_port=0)
    yield supervisor
    supervisor.close()


def _job() -> str:
    job = JobPlan(job_title="serve-test-job", user_prompt="Serve test prompt",
                  tasks=[TaskEntry(title="Write a README")])
    save_job_plan(job)
    return str(job.job_id)


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def _tcp_answers(port: int) -> bool:
    """True when a process accepts a TCP connection on 127.0.0.1 at PORT."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1.0)
        try:
            sock.connect(("127.0.0.1", port))
        except OSError:
            return False
    return True


def _api_request(port: int, method: str, path: str,
                  headers: dict[str, str] | None = None) -> tuple[int, dict]:
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request(method, path, headers=headers or {})
        resp = conn.getresponse()
        raw = resp.read()
        status = resp.status
    finally:
        conn.close()
    return status, json.loads(raw) if raw else {}


def _bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_a_running_supervisor_answers_and_reports_itself(root, running):
    paths = serve_paths(root)
    assert SD.socket_answers(paths.socket)
    assert SD.supervisor_state(root) == SD.SupervisorState(
        running=True, pid=running.state.pid, socket=paths.socket)
    assert SD.read_pid(paths) == running.state.pid


def test_its_directory_socket_and_token_are_readable_by_their_owner_only(root, running):
    paths = serve_paths(root)
    assert _mode(paths.root) == 0o700
    assert _mode(paths.socket) == 0o600
    assert _mode(paths.token_file) == 0o600
    assert stat.S_ISSOCK(paths.socket.stat().st_mode)


def test_a_stop_envelope_on_the_socket_is_recorded_with_the_command_lines_source(root, running):
    job_id = _job()
    status, body = SD.post_command(root, job_id, {
        "command": "job.stop", "client_nonce": "serve-stop-1", "args": {"reason": "via serve"}})
    assert status == 200, body
    signal = json.loads(safe_points.stop_request_path(job_id).read_bytes())
    assert signal["request_id"] == body["request_id"]
    assert signal["source"] == SD.SOCKET_EFFECT_SOURCE == "cli"
    assert signal["reason"] == "via serve"


def test_a_pause_envelope_on_the_socket_is_recorded_with_the_command_lines_source(root, running):
    from packages.orchestration.pause_control import pause_requested

    job_id = _job()
    status, body = SD.post_command(root, job_id, {
        "command": "job.pause", "client_nonce": "serve-pause-1", "args": {"reason": "hold"}})
    assert status == 200, body
    assert body["outcome"] == "requested"
    signal = pause_requested(job_id)
    assert (signal.request_id, signal.source, signal.reason) == (body["request_id"], "cli", "hold")


def test_only_the_socket_handler_records_a_source_the_client_names():
    from packages.orchestration.ui_server import COMMAND_EFFECT_SOURCE, _RemedyHandler

    cockpit, socket_handler = _RemedyHandler, SD.socket_handler_class("t")
    assert cockpit._effect_source_from(cockpit, {"source": "x"}) == COMMAND_EFFECT_SOURCE
    assert socket_handler._effect_source_from(socket_handler, {"source": "x"}) == "x"
    assert socket_handler._effect_source_from(socket_handler, {"source": ""}) == "cli"
    assert socket_handler._effect_source_from(socket_handler, None) == "cli"


def test_a_repeated_nonce_is_answered_from_the_record_as_the_door_answers_it(root, running):
    job_id = _job()
    envelope = {"command": "job.stop", "client_nonce": "serve-twice"}
    assert SD.post_command(root, job_id, envelope) == SD.post_command(root, job_id, envelope)


def test_a_command_the_door_does_not_expose_is_refused_as_the_door_refuses_it(root, running):
    from packages.orchestration.ui_server import COMMAND_NOT_EXPOSED_MESSAGE

    status, body = SD.post_command(root, _job(), {"command": "do.run", "client_nonce": "n-1"})
    assert (status, body) == (400, {"error": COMMAND_NOT_EXPOSED_MESSAGE, "field": "command"})


_RUN_CHILD = """\
import sys, time
from pathlib import Path
release = Path(sys.argv[2])
deadline = time.monotonic() + 60
while not release.exists() and time.monotonic() < deadline:
    time.sleep(0.01)
sys.exit(4)
"""


@pytest.fixture
def running_with_runs(root):
    release = root / "release"
    supervisor = _Running(root, run_argv=lambda job_id: [
        sys.executable, "-c", _RUN_CHILD, job_id, str(release)])
    yield supervisor, release
    release.touch()
    paths = serve_paths(root)
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline and any(
            (SR.read_run_record(paths, p.stem) or SR.RunRecord("", 0, "", "", "")).exit_code is None
            for p in paths.runs_dir.glob("*.json")):
        time.sleep(0.02)
    supervisor.close()


def _ended(root: Path, job_id: str) -> SR.RunRecord:
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        record = SR.read_run_record(serve_paths(root), job_id)
        if record is not None and record.exit_code is not None:
            return record
        time.sleep(0.02)
    raise AssertionError(f"the run of {job_id} never recorded its end")


def test_only_the_socket_handler_with_a_launcher_accepts_job_run(root):
    from packages.orchestration.ui_server import _RemedyHandler

    def bare(cls):
        """An instance that never ran the HTTP handler's constructor."""
        return cls.__new__(cls)

    with_runs = bare(SD.socket_handler_class("t", SR.RunLauncher(serve_paths(root))))
    without = bare(SD.socket_handler_class("t"))
    assert bare(_RemedyHandler)._command_is_ui_exposed("job.run") is False
    assert without._command_is_ui_exposed("job.run") is False
    assert with_runs._command_is_ui_exposed("job.run") is True
    assert with_runs._command_is_ui_exposed("job.stop") is True
    assert with_runs._command_is_ui_exposed("do.run") is False


def test_a_run_envelope_starts_the_jobs_run_and_answers_with_its_record(root, running_with_runs):
    supervisor, release = running_with_runs
    job_id = _job()
    status, body = SD.post_command(root, job_id, {"command": "job.run", "client_nonce": "run-1"})
    assert status == 200, body
    record = SR.read_run_record(serve_paths(root), job_id)
    assert body == {"command": "job.run", "outcome": "accepted", **record.to_json()}
    release.touch()
    assert _ended(root, job_id).exit_code == 4
    audit = (root / "control" / "jobs" / job_id / "commands_audit.jsonl").read_bytes()
    assert [json.loads(line)["outcome"] for line in audit.splitlines()] == ["accepted"]


def test_a_second_run_of_a_job_still_running_is_refused_with_its_reason(root, running_with_runs):
    job_id = _job()
    first = SD.post_command(root, job_id, {"command": "job.run", "client_nonce": "run-a"})
    status, body = SD.post_command(root, job_id, {"command": "job.run", "client_nonce": "run-b"})
    assert status == 409
    assert body["code"] == "job_already_running"
    assert str(first[1]["pid"]) in body["error"]
    audit = (root / "control" / "jobs" / job_id / "commands_audit.jsonl").read_bytes()
    assert [json.loads(line)["outcome"] for line in audit.splitlines()] == [
        "accepted", "rejected_state"]


def test_a_repeated_run_nonce_answers_the_first_run_and_starts_no_second(root, running_with_runs):
    job_id = _job()
    envelope = {"command": "job.run", "client_nonce": "run-same"}
    first = SD.post_command(root, job_id, envelope)
    assert SD.post_command(root, job_id, envelope) == first
    assert SR.read_run_record(serve_paths(root), job_id).pid == first[1]["pid"]


def test_a_request_without_the_token_is_refused(root, running):
    conn = SD.UnixHTTPConnection(serve_paths(root).socket)
    try:
        conn.request("POST", f"/api/jobs/{_job()}/commands",
                     body=json.dumps({"command": "job.stop", "client_nonce": "n-2"}),
                     headers={"Content-Type": "application/json"})
        assert conn.getresponse().status == 403
    finally:
        conn.close()


def test_a_second_supervisor_on_the_same_root_is_refused(root, running):
    with pytest.raises(SD.ServeError) as caught:
        SD.run_supervisor(root, stop=threading.Event())
    assert caught.value.token == "serve_already_running"
    assert str(running.state.pid) in str(caught.value)


def test_ending_removes_the_socket_the_process_id_and_the_token(root):
    paths = serve_paths(root)
    supervisor = _Running(root)
    supervisor.close()
    assert not paths.socket.exists()
    assert not paths.pid_file.exists()
    assert not paths.token_file.exists()
    assert SD.supervisor_state(root) == SD.SupervisorState(
        running=False, pid=None, socket=paths.socket)


def test_a_socket_file_nobody_answers_is_replaced(root):
    paths = serve_paths(root)
    paths.root.mkdir(parents=True)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as stale:
        stale.bind(str(paths.socket))
    assert paths.socket.exists() and not SD.socket_answers(paths.socket)
    supervisor = _Running(root)
    try:
        assert SD.socket_answers(paths.socket)
    finally:
        supervisor.close()


def test_a_data_root_too_deep_for_a_socket_is_refused_before_anything_is_written(tmp_path):
    deep = tmp_path / ("d" * 120)
    with pytest.raises(SD.ServeError) as caught:
        SD.run_supervisor(deep, stop=threading.Event())
    assert caught.value.token == "serve_socket_path_too_long"
    assert "REMEDY_DATA_DIR" in str(caught.value)
    assert not deep.exists()


def test_stopping_with_no_supervisor_reports_that_nothing_ran(root):
    assert SD.stop_supervisor(root) is False


# -- S6a: the public HTTP API on 127.0.0.1 at `serve.api_port` (DECISION F253 D6) -----------


def test_the_api_port_is_bound_and_named_by_ready_state_and_status(root, running_with_api):
    paths = serve_paths(root)
    bound = running_with_api.state.api_port
    assert isinstance(bound, int) and bound > 0
    assert SD.supervisor_state(root).api_port == bound
    assert paths.api_port_file.read_text(encoding="utf-8").strip() == str(bound)
    assert _mode(paths.api_port_file) == 0o600


def test_the_api_listener_binds_127_0_0_1_only(root, monkeypatch):
    captured: dict[str, tuple[str, int]] = {}
    real_cls = SD.ThreadingHTTPServer

    class _CapturingServer(real_cls):
        def __init__(self, address, handler):
            captured["address"] = address
            super().__init__(address, handler)

    monkeypatch.setattr(SD, "ThreadingHTTPServer", _CapturingServer)
    supervisor = _Running(root, api_port=0)
    try:
        assert captured["address"][0] == "127.0.0.1"
    finally:
        supervisor.close()


def test_the_api_port_answers_the_interface_route_with_the_sockets_own_token(
        root, running_with_api):
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    status, body = _api_request(running_with_api.state.api_port, "GET", "/api/v1/interface",
                                 headers=_bearer(token))
    assert status == 200, body
    env = dict(os.environ)
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "client", "interface", "--json"],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert body == json.loads(result.stdout)


def test_the_api_port_without_the_token_is_401(root, running_with_api):
    status, body = _api_request(running_with_api.state.api_port, "GET", "/api/v1/interface")
    assert status == 401
    assert body["error"] == "api_token_invalid"


@pytest.mark.parametrize("method,path", [
    ("GET", "/api/state"),
    ("GET", "/"),
    ("POST", "/api/jobs/any-job/commands"),
])
def test_the_api_port_answers_every_cockpit_only_path_404(root, running_with_api, method, path):
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    status, body = _api_request(running_with_api.state.api_port, method, path,
                                 headers=_bearer(token))
    assert status == 404
    assert body["error"] == "api_route_not_found"


def test_ending_removes_the_api_port_file_and_the_port_no_longer_answers(root):
    supervisor = _Running(root, api_port=0)
    port = supervisor.state.api_port
    supervisor.close()
    assert not serve_paths(root).api_port_file.exists()
    assert not _tcp_answers(port)


def test_with_api_port_none_no_port_file_exists_and_api_port_is_null(root):
    supervisor = _Running(root, api_port=None)
    try:
        assert supervisor.state.api_port is None
        assert not serve_paths(root).api_port_file.exists()
        assert SD.supervisor_state(root).api_port is None
    finally:
        supervisor.close()


def test_a_port_already_bound_refuses_the_start_and_leaves_nothing_behind(root):
    blocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    blocker.bind(("127.0.0.1", 0))
    blocker.listen(1)
    taken_port = blocker.getsockname()[1]
    try:
        with pytest.raises(SD.ServeError) as caught:
            SD.run_supervisor(root, stop=threading.Event(), api_port=taken_port)
        assert caught.value.token == "serve_api_port_unavailable"
        assert str(taken_port) in str(caught.value)
    finally:
        blocker.close()
    paths = serve_paths(root)
    assert not paths.socket.exists()
    assert not paths.pid_file.exists()
    assert not paths.token_file.exists()
    assert not paths.api_port_file.exists()


def test_run_supervisor_without_the_keyword_reads_serve_api_port_from_configuration(
        root, monkeypatch):
    import packages.orchestration.config as cfg

    class _FakeConfig:
        def get(self, key: str) -> int:
            assert key == "serve.api_port"
            return 0

    monkeypatch.setattr(cfg, "get_config", lambda: _FakeConfig())
    supervisor = _Running(root)
    try:
        assert isinstance(supervisor.state.api_port, int) and supervisor.state.api_port > 0
    finally:
        supervisor.close()
