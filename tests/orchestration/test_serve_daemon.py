"""The `remedy serve start` supervisor (F200, DECISIONs F200 D1 and D2).

Each test runs the supervisor in a thread of this process against its own data
root and ends it through the supervisor's stop event, never through a signal: the
supervisor's process id file names THIS process, and a SIGTERM would end the run.
The socket is a real unix socket, and the requests are real HTTP requests on it.
"""
from __future__ import annotations

import json
import socket
import stat
import threading
from pathlib import Path

import pytest

from packages.orchestration import safe_points
from packages.orchestration import serve_daemon as SD
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.serve_paths import serve_paths


@pytest.fixture
def root(tmp_path_factory, monkeypatch):
    """A short data root, so the socket path stays far below the length limit."""
    base = tmp_path_factory.mktemp("sv")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(base))
    return base


class _Running:
    """A supervisor running in a thread until `close` sets its stop event."""

    def __init__(self, root: Path) -> None:
        self.stop = threading.Event()
        self.ready = threading.Event()
        self.errors: list[Exception] = []
        self.state: SD.SupervisorState | None = None

        def ready(state: SD.SupervisorState) -> None:
            self.state = state
            self.ready.set()

        def run() -> None:
            try:
                SD.run_supervisor(root, stop=self.stop, on_ready=ready)
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


def _job() -> str:
    job = JobPlan(job_title="serve-test-job", user_prompt="Serve test prompt",
                  tasks=[TaskEntry(title="Write a README")])
    save_job_plan(job)
    return str(job.job_id)


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


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

    status, body = SD.post_command(root, _job(), {"command": "job.run", "client_nonce": "n-1"})
    assert (status, body) == (400, {"error": COMMAND_NOT_EXPOSED_MESSAGE, "field": "command"})


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
