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
from packages.orchestration.pingpong_job import JOB_COMPLETED, JobPlan, TaskEntry, save_job_plan
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
                  headers: dict[str, str] | None = None,
                  body: bytes | None = None, timeout: float = 10) -> tuple[int, dict]:
    conn = HTTPConnection("127.0.0.1", port, timeout=timeout)
    try:
        conn.request(method, path, body=body, headers=headers or {})
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


def test_ending_stops_the_thread_that_served_the_api_port(root):
    """R-1191: closing the listener is not enough; the thread serving it ends with the supervisor."""
    before = set(threading.enumerate())
    supervisor = _Running(root, api_port=0)
    try:
        serving = [t for t in threading.enumerate()
                   if t not in before and t.name == "remedy-serve-api" and t.is_alive()]
        assert serving, "no thread named remedy-serve-api serves the port"
    finally:
        supervisor.close()
    assert [t for t in serving if t.is_alive()] == []


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


# -- S4a: a write under /api/v1 runs its twin command as a child (DECISION F253 D9) ----------


def _job_with_open_decision() -> tuple[str, str]:
    """A saved job holding one open task decision, asked with the same question as any other."""
    from datetime import datetime, timezone

    from packages.orchestration.escalation import enqueue_task_decision

    job = JobPlan(job_title="serve-decision-job", user_prompt="Serve decision prompt",
                  tasks=[TaskEntry(title="Pick a database")])
    record = enqueue_task_decision(job, task_id=job.tasks[0].task_id,
                                   question="Which database?", options=("postgres", "sqlite"),
                                   now=datetime.now(timezone.utc))
    save_job_plan(job)
    return str(job.job_id), record["decision_id"]


def _stored_decision(job_id: str, decision_id: str) -> dict:
    from packages.orchestration.escalation import find_task_decision
    from packages.orchestration.pingpong_job import require_job_plan

    return find_task_decision(require_job_plan(job_id), decision_id)


def _resolve_command_envelope(root: Path, job_id: str, decision_id: str) -> dict:
    """What `remedy decision resolve <job> <decision> --reason Postgres --json` prints, run as a
    subprocess against ROOT; a refusal exits nonzero and still prints its envelope."""
    env = {**os.environ, "REMEDY_DATA_DIR": str(root), SR.DIRECT_ENV: "1"}
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "decision", "resolve", job_id, decision_id,
         "--reason", "Postgres", "--json"],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=60)
    return json.loads(result.stdout.strip().splitlines()[-1])


def _post_reason(port: int, token: str, job_id: str, decision_id: str):
    return _api_request(port, "POST", f"/api/v1/jobs/{job_id}/decisions/{decision_id}",
                        headers=_bearer(token), body=json.dumps({"reason": "Postgres"}).encode())


def test_a_post_on_the_api_port_answers_what_the_resolve_command_prints(root, running_with_api):
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    port = running_with_api.state.api_port
    posted_job, posted_decision = _job_with_open_decision()
    run_job, run_decision = _job_with_open_decision()
    open_job, open_decision = _job_with_open_decision()

    status, body = _post_reason(port, token, posted_job, posted_decision)
    assert status == 200, body
    command = _resolve_command_envelope(root, run_job, run_decision)
    assert (body["job_id"], body["decision_id"]) == (posted_job, posted_decision)
    assert (command["job_id"], command["decision_id"]) == (run_job, run_decision)
    aside = ("job_id", "decision_id", "next_command")
    assert ({k: v for k, v in body.items() if k not in aside}
            == {k: v for k, v in command.items() if k not in aside})
    assert _stored_decision(posted_job, posted_decision)["answer"] == "Postgres"

    status, refused = _post_reason(port, token, posted_job, posted_decision)
    assert (status, refused["error"]) == (409, "decision_already_answered")
    again = _resolve_command_envelope(root, run_job, run_decision)
    assert again["error"] == "decision_already_answered"
    assert refused["message"].replace(posted_decision, "<decision>") == \
        again["message"].replace(run_decision, "<decision>")

    status, unknown = _api_request(
        port, "POST", f"/api/v1/jobs/not-a-job/decisions/{open_decision}",
        headers=_bearer(token), body=b"{}")
    assert (status, unknown["error"]) == (404, "invalid_job_id")
    assert unknown == _resolve_command_envelope(root, "not-a-job", open_decision)

    status, denied = _api_request(
        port, "POST", f"/api/v1/jobs/{open_job}/decisions/{open_decision}",
        body=json.dumps({"reason": "Postgres"}).encode())
    assert (status, denied["error"]) == (401, "api_token_invalid")
    assert _stored_decision(open_job, open_decision)["status"] == "open"

    ledger = Path(root) / "api" / "calls.jsonl"
    posts = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()
             if json.loads(line)["method"] == "POST"]
    assert [(r["path"], r["status"]) for r in posts] == [
        (f"/api/v1/jobs/{posted_job}/decisions/{posted_decision}", 200),
        (f"/api/v1/jobs/{posted_job}/decisions/{posted_decision}", 409),
        (f"/api/v1/jobs/not-a-job/decisions/{open_decision}", 404),
        (f"/api/v1/jobs/{open_job}/decisions/{open_decision}", 401),
    ]


def test_the_same_post_on_the_supervisors_socket_answers_200_too(root, running):
    from packages.orchestration.serve_daemon import UnixHTTPConnection

    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    job_id, decision_id = _job_with_open_decision()
    conn = UnixHTTPConnection(serve_paths(root).socket, timeout=30)
    try:
        conn.request("POST", f"/api/v1/jobs/{job_id}/decisions/{decision_id}",
                     body=json.dumps({"reason": "Postgres"}).encode(), headers=_bearer(token))
        response = conn.getresponse()
        body = json.loads(response.read())
    finally:
        conn.close()
    assert response.status == 200, body
    assert (body["job_id"], body["decision_id"], body["outcome"]) == (
        job_id, decision_id, "answered")
    assert _stored_decision(job_id, decision_id)["answer"] == "Postgres"


def test_a_post_with_a_query_string_is_400_and_runs_nothing(root, running_with_api):
    """R-1194: no write route takes a query string (DECISION F253 D9)."""
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    job_id, decision_id = _job_with_open_decision()
    status, body = _api_request(
        running_with_api.state.api_port, "POST",
        f"/api/v1/jobs/{job_id}/decisions/{decision_id}?reason=Postgres",
        headers=_bearer(token), body=json.dumps({"reason": "Postgres"}).encode())
    assert (status, body["error"]) == (400, "api_query_invalid")
    assert _stored_decision(job_id, decision_id)["status"] == "open"


def test_a_post_declaring_a_body_above_the_ceiling_is_400_and_runs_nothing(
        root, running_with_api):
    """R-1194: a body above `COMMAND_REQUEST_MAX_BYTES` is refused before it is read."""
    from packages.orchestration.ui_server import COMMAND_REQUEST_MAX_BYTES

    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    job_id, decision_id = _job_with_open_decision()
    status, body = _api_request(
        running_with_api.state.api_port, "POST", f"/api/v1/jobs/{job_id}/decisions/{decision_id}",
        headers={**_bearer(token), "Content-Length": str(COMMAND_REQUEST_MAX_BYTES + 1)},
        body=json.dumps({"reason": "Postgres"}).encode())
    assert (status, body["error"]) == (400, "api_body_invalid")
    assert _stored_decision(job_id, decision_id)["status"] == "open"


def test_a_post_whose_path_value_decodes_to_a_nul_is_400_and_ledgered(root, running_with_api):
    """R-1195: `%00` decodes to a NUL, which no child's argument list can hold; the supervisor
    answers and ledgers the refusal instead of failing the request."""
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    job_id, decision_id = _job_with_open_decision()
    path = f"/api/v1/jobs/{job_id}/decisions/{decision_id}%00"
    status, body = _api_request(running_with_api.state.api_port, "POST", path,
                                headers=_bearer(token), body=b"{}")
    assert (status, body["error"]) == (400, "api_path_invalid")
    assert _stored_decision(job_id, decision_id)["status"] == "open"
    ledger = Path(root) / "api" / "calls.jsonl"
    records = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    assert (records[-1]["method"], records[-1]["path"], records[-1]["status"]) == (
        "POST", path, 400)


# -- S4b: declining a result over HTTP (DECISION F253 D11) --------------------------------------


def _saved_job(*, completed: bool) -> str:
    from packages.orchestration.pingpong_job import JOB_COMPLETED

    job = JobPlan(job_title="serve-decline-job", user_prompt="Serve decline prompt",
                  tasks=[TaskEntry(title="Write a page")])
    if completed:
        job.state = JOB_COMPLETED
    save_job_plan(job)
    return str(job.job_id)


def _decline_command_envelope(root: Path, job_id: str, reason: str) -> dict:
    """What `remedy job decline <job> --reason <reason> --source api --json` prints, run as a
    subprocess against ROOT; a refusal exits nonzero and still prints its envelope."""
    env = {**os.environ, "REMEDY_DATA_DIR": str(root), SR.DIRECT_ENV: "1"}
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "job", "decline", job_id, "--reason", reason,
         "--source", "api", "--json"],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=60)
    return json.loads(result.stdout.strip().splitlines()[-1])


def _post_decline(port: int, token: str, job_id: str, body: dict):
    return _api_request(port, "POST", f"/api/v1/jobs/{job_id}/decline",
                        headers=_bearer(token), body=json.dumps(body).encode())


def test_a_decline_post_answers_what_the_decline_command_prints(root, running_with_api):
    from packages.orchestration.job_apply import job_result_decline
    from packages.orchestration.pingpong_job import require_job_plan

    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    port = running_with_api.state.api_port
    posted, run = _saved_job(completed=True), _saved_job(completed=True)

    status, body = _post_decline(port, token, posted, {"reason": "not wanted"})
    assert status == 200, body
    command = _decline_command_envelope(root, run, "not wanted")
    aside = ("job_id", "declined_at")
    assert ({k: v for k, v in body.items() if k not in aside}
            == {k: v for k, v in command.items() if k not in aside})
    assert (body["job_id"], body["source"], body["already_declined"]) == (posted, "api", False)
    assert job_result_decline(require_job_plan(posted))["source"] == "api"

    status, again = _post_decline(port, token, posted, {"reason": "other reason"})
    assert status == 200 and again["already_declined"] is True
    assert (again["reason"], again["declined_at"]) == ("not wanted", body["declined_at"])


def test_a_decline_post_refuses_as_the_command_does(root, running_with_api):
    from packages.orchestration.job_apply import job_result_decline
    from packages.orchestration.pingpong_job import require_job_plan

    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    port = running_with_api.state.api_port
    planned, completed = _saved_job(completed=False), _saved_job(completed=True)

    status, body = _post_decline(port, token, planned, {"reason": "too early"})
    assert (status, body["error"]) == (409, "job_not_declinable")
    assert body == _decline_command_envelope(root, planned, "too early")

    status, body = _post_decline(port, token, completed, {})
    assert (status, body["error"]) == (400, "missing_argument")
    assert body == _decline_command_envelope(root, completed, "")
    assert job_result_decline(require_job_plan(completed)) is None


def test_a_client_token_on_the_port_reads_a_route_and_is_refused_a_write_outside_its_policy(
        root, running_with_api):
    """R-1213: the door another user of the machine reaches Remedy by takes a client's token."""
    from packages.orchestration.job_apply import job_result_decline
    from packages.orchestration.pingpong_job import require_job_plan

    api_dir = Path(root) / "api"
    api_dir.mkdir(mode=0o700, exist_ok=True)
    client_token = "client-token-" + "x" * 32
    clients_file = api_dir / "clients.json"
    clients_file.write_text(json.dumps({"clients": [{
        "name": "other-user", "token": client_token, "projects": ["no-such-project"],
        "max_total_tokens": None, "max_provider_calls": None, "may_apply": False}]}),
        encoding="utf-8")
    clients_file.chmod(0o600)
    assert _mode(clients_file) == 0o600 and len(client_token) >= 32
    port = running_with_api.state.api_port
    job_id = _saved_job(completed=True)

    status, body = _api_request(port, "GET", "/api/v1/interface", headers=_bearer(client_token))
    assert status == 200, body

    status, refused = _post_decline(port, client_token, job_id, {"reason": "not mine"})
    assert (status, refused["error"]) == (403, "api_client_policy_refused")
    assert job_result_decline(require_job_plan(job_id)) is None

    ledger = api_dir / "calls.jsonl"
    posts = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()
             if json.loads(line)["method"] == "POST"]
    assert [(r["client"], r["path"], r["status"], r["error"]) for r in posts] == [
        ("other-user", f"/api/v1/jobs/{job_id}/decline", 403, "api_client_policy_refused")]


def test_the_supervisors_listener_source_imports_no_ssl_and_binds_127_0_0_1_only():
    """R-1214, R-1218: no TLS and no remote bind (the feature file's binding); read from the
    source. No module of the API's path imports `ssl`, wherever in the module the import stands;
    the listener is the one in `serve_daemon.py`."""
    import ast

    api_path = ("serve_daemon.py", "public_api.py", "public_api_writes.py", "ui_server.py",
                "serve_runs.py", "serve_paths.py", "api_clients.py")
    imported: list[str] = []
    listeners: list[ast.Call] = []
    for filename in api_path:
        module = REPO / "packages" / "orchestration" / filename
        assert module.is_file(), f"{filename} is not where the API's path puts it"
        tree = ast.parse(module.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported += [f"{filename}: {alias.name}" for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported.append(f"{filename}: {node.module or ''}")
            elif isinstance(node, ast.Call) and filename == "serve_daemon.py":
                func = node.func
                name = func.id if isinstance(func, ast.Name) else (
                    func.attr if isinstance(func, ast.Attribute) else "")
                if name == "ThreadingHTTPServer":
                    listeners.append(node)
    assert not [m for m in imported
                if m.split(": ", 1)[1] == "ssl" or m.split(": ", 1)[1].startswith("ssl.")]
    assert listeners, "no call of ThreadingHTTPServer found in serve_daemon.py"
    for call in listeners:
        address = call.args[0] if call.args else None
        assert isinstance(address, ast.Tuple) and address.elts, ast.dump(call)
        host = address.elts[0]
        assert isinstance(host, ast.Constant) and host.value == "127.0.0.1", ast.dump(call)


# -- S4c: approving an apply over HTTP (DECISION F253 D12) -------------------------------------


def _completed_job_in_a_repository(root: Path, tmp_path: Path) -> tuple[str, Path]:
    """A job `remedy do` completed with the fake builder and reviewer, run as a child against
    ROOT inside a scratch repository: the job's id and the repository."""
    from tests.cli.test_machine_client_paths import UNATTENDED, _client

    repo, order_file, env = _client(tmp_path)
    env = {**env, "REMEDY_DATA_DIR": str(root), SR.DIRECT_ENV: "1", "PYTHONPATH": str(REPO)}
    done = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "do", str(order_file), *UNATTENDED, "--json"],
        cwd=str(repo), env=env, capture_output=True, text=True, timeout=300)
    envelope = json.loads(done.stdout.strip().splitlines()[-1])
    assert envelope["ok"], envelope
    [job_id] = envelope["job_ids"]
    return job_id, repo


def _apply_command_envelope(root: Path, job_id: str, repo: Path, *flags: str) -> dict:
    """What `remedy job apply <job> --repo <repo> --approve <flags> --json` prints, run as a
    subprocess against ROOT; a refusal exits nonzero and still prints its envelope."""
    env = {**os.environ, "REMEDY_DATA_DIR": str(root), SR.DIRECT_ENV: "1"}
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "job", "apply", job_id, "--repo", str(repo),
         "--approve", *flags, "--json"],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=120)
    return json.loads(result.stdout.strip().splitlines()[-1])


def _post_apply(port: int, token: str, job: str, body: dict):
    return _api_request(port, "POST", f"/api/v1/jobs/{job}/apply", headers=_bearer(token),
                        body=json.dumps(body).encode(), timeout=120)


def test_an_apply_post_lands_one_commit_in_the_jobs_own_repository(
        root, running_with_api, tmp_path, monkeypatch):
    from tests.cli.test_machine_client_contract import _GIT_IDENTITY

    for name, value in _GIT_IDENTITY.items():
        monkeypatch.setenv(name, value)
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    job_id, repo = _completed_job_in_a_repository(root, tmp_path)
    before = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                            capture_output=True, text=True).stdout.strip()

    status, body = _post_apply(running_with_api.state.api_port, token, job_id[:8],
                               {"commit_auto": True})
    assert status == 200, body
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()
    parent = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD~1"], check=True,
                            capture_output=True, text=True).stdout.strip()
    assert (body["ok"], body["status"], body["job_id"]) == (True, "applied", job_id)
    assert body["commit_sha"] == head and parent == before


def test_an_apply_post_answers_what_the_apply_command_prints(
        root, running_with_api, tmp_path, monkeypatch):
    """R-1217: the success answer of the route equals `remedy job apply --json`'s envelope for a
    second job made alike in a repository of its own, but for the keys that name the job, its
    commit, an apply record's id or a time."""
    from tests.cli.test_machine_client_contract import _GIT_IDENTITY

    for name, value in _GIT_IDENTITY.items():
        monkeypatch.setenv(name, value)
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    (tmp_path / "posted").mkdir()
    (tmp_path / "run").mkdir()
    posted, _posted_repo = _completed_job_in_a_repository(root, tmp_path / "posted")
    run, run_repo = _completed_job_in_a_repository(root, tmp_path / "run")

    status, body = _post_apply(running_with_api.state.api_port, token, posted,
                               {"commit_auto": True})
    assert status == 200, body
    command = _apply_command_envelope(root, run, run_repo, "--commit-auto")
    assert body["ok"] is True and command["ok"] is True, (body, command)
    assert set(body) == set(command), sorted(set(body) ^ set(command))
    aside = (
        "commit_sha",       # its commit: the commit each repository's own apply made
        "finished_at",      # a time
        "job_apply_id",     # an apply record's id
        "job_id",           # the job
        "started_at",       # a time
        "task_summaries",   # names the job's tasks and runs by id; compared below without them
    )
    differing = {k: (body[k], command[k]) for k in body if k not in aside and body[k] != command[k]}
    assert not differing, "\n".join(f"{k}: {a!r} | {b!r}" for k, (a, b) in differing.items())

    def without_ids(summaries: list[dict]) -> list[dict]:
        return [{k: v for k, v in item.items() if k not in ("run_id", "task_id")}
                for item in summaries]

    assert without_ids(body["task_summaries"]) == without_ids(command["task_summaries"])
    assert (body["job_id"], command["job_id"]) == (posted, run)
    assert len(body["commit_sha"]) == len(command["commit_sha"]) == 40


def _register_project(root: Path, repo: Path) -> str:
    """Register REPO as a project on ROOT via `remedy init --json`; the project's slug."""
    env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    result = subprocess.run([sys.executable, "-m", "apps.cli.main", "init", "--json"],
                            cwd=str(repo), env=env, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)["summary"]["slug"]


def _post_order(port: int, token: str, body: dict):
    return _api_request(port, "POST", "/api/v1/orders", headers=_bearer(token),
                        body=json.dumps(body).encode(), timeout=120)


def test_an_order_create_post_starts_a_real_order_and_polling_reaches_its_end(
        root, running_with_api, tmp_path):
    """S5b, DECISION F253 D14: a real order, through the fake builder and reviewer, started by
    `POST /api/v1/orders` and followed to its end by `GET /api/v1/orders/{order}`."""
    from tests.cli.test_client_order_cmd import _PAST_DEADLINE, _git_repo

    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    port = running_with_api.state.api_port
    repo = _git_repo(tmp_path / "order-create-repo")
    slug = _register_project(root, repo)

    order_text = (f"---\nproject: {slug}\nmax-cost-usd: 1\n---\n"
                 "Add a line saying hello to README.md\n")
    body = {"order": order_text, "no_llm": True, "builder_provider": "fake",
            "reviewer_provider": "fake", "deadline": _PAST_DEADLINE}
    status, created = _post_order(port, token, body)
    assert status == 202, created
    assert created["state"] == "running"
    order_id = created["order_id"]

    polled = created
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline and polled["state"] == "running":
        time.sleep(0.2)
        status, polled = _api_request(
            port, "GET", f"/api/v1/orders/{order_id}", headers=_bearer(token))
        assert status == 200, polled
    assert polled["state"] == "ended", "the order never ended within 120 seconds"
    assert polled["answer"]["mission_id"]
    assert polled["answer"]["job_ids"]

    ledger = Path(root) / "api" / "calls.jsonl"
    records = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    posts = [r for r in records if r["method"] == "POST" and r["path"] == "/api/v1/orders"]
    gets = [r for r in records
            if r["method"] == "GET" and r["path"] == f"/api/v1/orders/{order_id}"]
    assert posts and posts[-1]["status"] == 202
    assert gets and gets[-1]["status"] == 200


def test_an_order_create_post_without_a_project_is_409_and_starts_nothing(root, running_with_api):
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    port = running_with_api.state.api_port
    orders_dir = serve_paths(root).orders_dir
    before = sorted(p.name for p in orders_dir.iterdir()) if orders_dir.exists() else []

    body = {"order": "No header at all, just text that is long enough to be an order.\n",
            "no_llm": True}
    status, answer = _post_order(port, token, body)

    assert (status, answer["error"]) == (409, "api_order_project_unknown")
    after = sorted(p.name for p in orders_dir.iterdir()) if orders_dir.exists() else []
    assert after == before


def _project_repo_with_passing_test(path: Path) -> Path:
    """A git repository at PATH holding `README.md` and a passing test under `tests`, committed,
    the way `probe_two_orders.py`'s own `repo` function makes one (DECISION F253 D15 (2))."""
    path.mkdir()
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "init", "-q", str(path)], check=True, env=env)
    (path / "README.md").write_text("# Scratch\n", encoding="utf-8")
    (path / "tests").mkdir()
    (path / "tests" / "test_ok.py").write_text(
        "def test_ok():\n    assert True\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", str(path), "commit", "-q", "-m", "init"], check=True, env=env)
    return path


def test_two_order_create_posts_sent_at_once_both_run_and_every_record_reads_back_whole(
        root, running_with_api, tmp_path):
    """DECISION F253 D15 (2): two `POST /api/v1/orders` for one registered project, sent from two
    threads a `threading.Barrier` releases together, each `no_llm` with both providers `fake` and
    no deadline. The supervisor keeps no waiting line (DECISION F200 D1 (4)) and refuses neither
    order for the other, so both answer 202 with different order ids and both reach `ended`; the
    digest then lists both missions and both jobs `completed`, with `degraded` false and
    `skipped_files` empty, and no `.json` or `.jsonl` record under the data root is damaged."""
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    port = running_with_api.state.api_port
    repo = _project_repo_with_passing_test(tmp_path / "order-two-repo")
    slug = _register_project(root, repo)

    bodies = [
        {"order": (f"---\nproject: {slug}\nmax-cost-usd: 1\n---\n"
                   f"Add a line saying hello number {i} to README.md\n"),
         "no_llm": True, "builder_provider": "fake", "reviewer_provider": "fake"}
        for i in range(2)
    ]
    barrier = threading.Barrier(2)
    results: list[tuple[int, dict] | None] = [None, None]
    errors: list[Exception] = []

    def send(index: int) -> None:
        try:
            barrier.wait(timeout=10)
            results[index] = _post_order(port, token, bodies[index])
        except (OSError, threading.BrokenBarrierError) as exc:
            errors.append(exc)

    threads = [threading.Thread(target=send, args=(i,)) for i in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(30)
    assert not errors, errors
    assert all(result is not None for result in results)

    order_ids = []
    for status, created in results:
        assert status == 202, created
        assert created["state"] == "running"
        order_ids.append(created["order_id"])
    assert order_ids[0] != order_ids[1]

    answers = {}
    for order_id in order_ids:
        polled = None
        deadline = time.monotonic() + 180
        while time.monotonic() < deadline:
            status, polled = _api_request(
                port, "GET", f"/api/v1/orders/{order_id}", headers=_bearer(token))
            assert status == 200, polled
            if polled["state"] != "running":
                break
            time.sleep(0.2)
        assert polled["state"] == "ended", f"order {order_id} never ended within 180 seconds"
        assert polled["exit_code"] == 0, polled
        assert polled["answer"]["ok"] is True, polled
        assert polled["answer"]["mission_id"]
        assert polled["answer"]["job_ids"]
        answers[order_id] = polled["answer"]

    assert len({answer["mission_id"] for answer in answers.values()}) == 2

    status, digest = _api_request(port, "GET", "/api/v1/digest", headers=_bearer(token))
    assert status == 200, digest
    assert digest["degraded"] is False
    assert digest["skipped_files"] == []
    project = next(p for p in digest["projects"] if p["slug"] == slug)
    mission_ids = {mission["mission_id"] for mission in project["missions"]}
    assert mission_ids == {answer["mission_id"] for answer in answers.values()}

    all_job_ids = {job_id for answer in answers.values() for job_id in answer["job_ids"]}
    jobs_by_id = {job["job_id"]: job for job in digest["jobs"]}
    for job_id in all_job_ids:
        assert jobs_by_id[job_id]["state"] == JOB_COMPLETED

    bad: list[tuple[str, str]] = []
    for f in root.rglob("*.json"):
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            bad.append((str(f.relative_to(root)), str(exc)[:80]))
    for f in root.rglob("*.jsonl"):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines()):
            if line.strip():
                try:
                    json.loads(line)
                except ValueError as exc:
                    bad.append((f"{f.relative_to(root)}:{n + 1}", str(exc)[:80]))
    assert not bad, bad


# -- S7a: POST /api/v1/jobs/{job}/run starts a run through the supervisor (DECISION F253 D18) --

#: A stand-in for `remedy job run`: it writes the arguments it got after its release file's path
#: (the job id, the options, `--json`) as JSON to the file at argv[1], then waits for the release
#: file at argv[2] and exits 5. No provider is ever called.
_RUN_ARGS_CHILD = """\
import json, sys, time
from pathlib import Path
Path(sys.argv[1]).write_text(json.dumps(sys.argv[3:]), encoding="utf-8")
release = Path(sys.argv[2])
deadline = time.monotonic() + 60
while not release.exists() and time.monotonic() < deadline:
    time.sleep(0.01)
sys.exit(5)
"""


@pytest.fixture
def running_with_run_route(root):
    """A supervisor with a public port whose runs are `_RUN_ARGS_CHILD`; every child is released
    and has recorded its end before the supervisor ends."""
    release = root / "release"
    supervisor = _Running(root, api_port=0, run_argv=lambda job_id: [
        sys.executable, "-c", _RUN_ARGS_CHILD, str(root / f"args-{job_id}.json"), str(release),
        job_id])
    yield supervisor, release
    release.touch()
    paths = serve_paths(root)
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline and any(
            (SR.read_run_record(paths, p.stem) or SR.RunRecord("", 0, "", "", "")).exit_code is None
            for p in paths.runs_dir.glob("*.json")):
        time.sleep(0.02)
    supervisor.close()


def _written_args(root: Path, job_id: str) -> list[str]:
    path = root / f"args-{job_id}.json"
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline and not path.is_file():
        time.sleep(0.02)
    return json.loads(path.read_text(encoding="utf-8"))


def test_a_run_post_on_the_port_starts_the_run_and_the_socket_starts_another(
        root, running_with_run_route):
    """DECISION F253 D18: the port and the socket answer the route from one launcher."""
    supervisor, release = running_with_run_route
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    port = supervisor.state.api_port
    job_id, other_id = _job(), _job()
    body = json.dumps({"builder_provider": "fake", "reviewer_provider": "fake"}).encode()

    status, started = _api_request(
        port, "POST", f"/api/v1/jobs/{job_id}/run", headers=_bearer(token), body=body)
    assert status == 202, started
    assert started["job_id"] == job_id and isinstance(started["pid"], int)
    assert (started["exit_code"], started["ended_at"]) == (None, None)
    assert _written_args(root, job_id) == [
        job_id, "--builder-provider=fake", "--reviewer-provider=fake", "--json"]

    status, refused = _api_request(
        port, "POST", f"/api/v1/jobs/{job_id}/run", headers=_bearer(token), body=body)
    assert (status, refused["error"]) == (409, "job_already_running")

    conn = SD.UnixHTTPConnection(serve_paths(root).socket, timeout=30)
    try:
        conn.request("POST", f"/api/v1/jobs/{other_id}/run", body=b"{}", headers=_bearer(token))
        response = conn.getresponse()
        on_socket = json.loads(response.read())
    finally:
        conn.close()
    assert response.status == 202, on_socket
    assert on_socket["job_id"] == other_id
    assert _written_args(root, other_id) == [other_id, "--json"]

    release.touch()
    ended = _ended(root, job_id)
    assert (ended.exit_code, ended.pid) == (5, started["pid"])
    assert ended.ended_at is not None
    assert _ended(root, other_id).exit_code == 5


def test_an_apply_post_refuses_as_the_command_does_or_before_it(root, running_with_api, tmp_path):
    token = serve_paths(root).token_file.read_text(encoding="utf-8").strip()
    port = running_with_api.state.api_port

    planned = JobPlan(job_title="serve-apply-job", user_prompt="Serve apply prompt",
                      tasks=[TaskEntry(title="Write a page")], repo_path=str(tmp_path))
    save_job_plan(planned)
    status, body = _post_apply(port, token, str(planned.job_id), {"commit_auto": True})
    assert (status, body["ok"], body["error"]) == (409, False, "job_not_ready")
    command = _apply_command_envelope(root, str(planned.job_id), tmp_path, "--commit-auto")
    aside = ("job_apply_id", "started_at", "finished_at")
    assert ({k: v for k, v in body.items() if k not in aside}
            == {k: v for k, v in command.items() if k not in aside})

    status, body = _post_apply(port, token, "0123abcd", {})
    assert (status, body["error"]) == (404, "job_not_found")

    unknown = _saved_job(completed=True)
    path = f"/api/v1/jobs/{unknown}/apply"
    status, body = _api_request(port, "POST", path, headers=_bearer(token), body=b"{}")
    assert (status, body["error"]) == (409, "api_job_repository_unknown")
    ledger = Path(root) / "api" / "calls.jsonl"
    records = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    assert (records[-1]["method"], records[-1]["path"], records[-1]["status"]) == (
        "POST", path, 409)
