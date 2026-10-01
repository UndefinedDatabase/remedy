"""F041 T003 — the preview flow proved end to end on a real small app (DECISION F041 D6).

One test, driving the whole path a person really takes: a fixture app under a real
``.remedy/config.toml``, a real UI server, the write door's ``job.preview-start``, the
worker's own thread carrying the request through the harness's real ``remedy runtime``
subprocess verbs (never a scripted stand-in, unlike `test_preview_commands.py`), the live
link answering, and the worker's own idle stop tearing the app down again once nobody is
looking — read TRUTHFULLY off the record on disk, never off a clock guess.

THE ONE RULE THIS TEST OBEYS THAT A SHORTCUT WOULD BREAK: every read of the browser's
``GET /api/jobs/<id>/preview`` counts as a view (`_build_preview_json` calls `mark_viewed`
first), so it resets the very idle clock this test is trying to observe expire. Once the
preview is confirmed live, this test never reads that route again until the record on disk
already says ``stopped`` — the wait for the idle stop reads `load_preview` straight off
disk instead, which marks nothing.
"""
from __future__ import annotations

import json
import secrets
import sys
import threading
import time
import urllib.error
import urllib.request
from http.client import HTTPConnection
from pathlib import Path

import psutil
import pytest

from packages.orchestration.config import reset_config
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.preview_control import load_preview, preview_view
from packages.orchestration.preview_runner import run_runtime_verb
from packages.runtimes.dev_server import STATE_ABSENT, STATE_VALID, load_state_result
from tests.ports import worker_port
from tests.ui_server.server_start import wait_for_server_info

pytestmark = pytest.mark.subprocess

CSRF_HEADER = "X-Remedy-CSRF"

#: A stdlib app the harness's own `remedy runtime serve` can run: it answers every GET
#: with 200 and a fixed body, bound to 127.0.0.1 at the port `.remedy/config.toml` gives it.
FIXTURE_APP_SOURCE = '''
import http.server
import os

PORT = int(os.environ["PORT"])


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"fixture app ok"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


http.server.HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
'''


def _alive(pid: int) -> bool:
    try:
        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def _fetch(url: str, timeout: float = 5.0) -> tuple[int, bytes]:
    """One GET. Never raises: a connection failure reads as status 0, empty body."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310 - loopback only
            return int(resp.status), resp.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read()
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, b""


def _start_server(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """A real UI server on port 0, in a daemon thread — `test_tour_e2e_live.py`'s own
    `_start_server` shape, copied rather than imported (this file's own copy)."""
    from packages.orchestration.ui_server import start_ui_server

    info_file = str(tmp_path / f"server_info_{secrets.token_hex(4)}.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    info = wait_for_server_info(info_file, thread)
    return info["port"], token


def _command(port: int, token: str, job_id: str, command: str, nonce: str) -> tuple[int, dict]:
    headers = {"Authorization": f"Bearer {token}", CSRF_HEADER: token,
               "Content-Type": "application/json"}
    body = json.dumps({"command": command, "client_nonce": nonce})
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("POST", f"/api/jobs/{job_id}/commands", body=body, headers=headers)
        resp = conn.getresponse()
        return resp.status, json.loads(resp.read())
    finally:
        conn.close()


def _get_preview_route(port: int, token: str, job_id: str) -> tuple[int, dict]:
    """A read through the browser's own route. COUNTS AS A VIEW — see the module docstring."""
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("GET", f"/api/jobs/{job_id}/preview?token={token}")
        resp = conn.getresponse()
        return resp.status, json.loads(resp.read())
    finally:
        conn.close()


class TestPreviewEndToEnd:
    def test_the_preview_flow_runs_end_to_end_on_a_real_fixture_app(self, tmp_path, monkeypatch):
        # (a) THE PROJECT: a real stdlib app the harness's own `remedy runtime serve` runs.
        project = tmp_path / "project"
        project.mkdir()
        (project / "server.py").write_text(FIXTURE_APP_SOURCE, encoding="utf-8")
        port = worker_port()
        config_dir = project / ".remedy"
        config_dir.mkdir()
        (config_dir / "config.toml").write_text(
            "[runtime]\n"
            f'cmd = ["{sys.executable}", "server.py"]\n'
            f"port = {port}\n"
            'health_path = "/"\n',
            encoding="utf-8",
        )

        # (b) THE SCRATCH DATA ROOT AND THE TWO-SECOND IDLE LIMIT.
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        monkeypatch.setenv("REMEDY_PREVIEW_IDLE_TTL_SECONDS", "2")
        reset_config()

        try:
            # (c) THE JOB: its repo_path names the project, saved as
            #     `test_preview_commands.py` saves one.
            job = JobPlan(job_title="f041-r6-preview-e2e", user_prompt="preview the app",
                          tasks=[TaskEntry(title="t")], repo_path=str(project))
            save_job_plan(job)
            job_id = str(job.job_id)

            # (d) THE SERVER.
            server_port, token = _start_server(job_id, tmp_path)

            # (e) OPEN: `job.preview-start` through the door, bearer token, CSRF header,
            #     a fresh nonce.
            nonce = secrets.token_hex(8)
            status, body = _command(server_port, token, job_id, "job.preview-start", nonce)
            assert status == 200
            assert body["outcome"] == "accepted"

            # (f) LIVE: poll the view every 0.5s for at most 120s. Every answer before the
            #     live one holds url "" and port 0; the live one holds the real link.
            deadline = time.monotonic() + 120
            view: dict = {}
            while time.monotonic() < deadline:
                status, view = _get_preview_route(server_port, token, job_id)
                assert status == 200
                if view["state"] == "live":
                    break
                assert view["url"] == ""
                assert view["port"] == 0
                time.sleep(0.5)
            assert view.get("state") == "live", f"preview never went live: {view}"
            live_url = f"http://127.0.0.1:{port}/"
            assert view["url"] == live_url
            assert view["port"] == port

            # (g) THE LINK: a GET of that url really answers.
            link_status, link_body = _fetch(live_url)
            assert link_status == 200
            assert b"fixture app ok" in link_body

            # (h) THE PIDS: read from the harness's own runtime record for the project,
            #     the way `remedy runtime status` finds it — both alive.
            load = load_state_result(project)
            assert load.kind == STATE_VALID, load
            app_pid = load.state.pid
            supervisor_pid = load.state.supervisor_pid
            assert _alive(app_pid), "the app is not running"
            assert _alive(supervisor_pid), "the supervisor is not running"

            # (i) IDLE: NO MORE READS OF THE VIEW THROUGH THE ROUTE — each one would count
            #     as a fresh view and reset the very clock this waits on. Read the record
            #     straight off disk instead.
            deadline = time.monotonic() + 60
            record: dict = {}
            while time.monotonic() < deadline:
                record = load_preview(job_id, data_root=data_dir)
                if record["state"] == "stopped":
                    break
                time.sleep(0.5)
            assert record.get("state") == "stopped", f"preview never idled out: {record}"
            assert record["reason"] == "stopped after 2 seconds without a viewer"

            # (j) TRUTHFUL: the view now answers stopped, with no link and that reason;
            #     within 10s neither pid is a running process; the old link no longer
            #     answers. Reading the route is safe again — `mark_viewed` no-ops off `live`.
            status, view = _get_preview_route(server_port, token, job_id)
            assert status == 200
            assert view == preview_view(job_id, data_root=data_dir)
            assert view["state"] == "stopped"
            assert view["url"] == ""
            assert view["port"] == 0
            assert view["reason"] == "stopped after 2 seconds without a viewer"

            pid_deadline = time.monotonic() + 10
            while time.monotonic() < pid_deadline and (_alive(app_pid) or _alive(supervisor_pid)):
                time.sleep(0.2)
            assert not _alive(app_pid), "the app survived its own idle stop"
            assert not _alive(supervisor_pid), "the supervisor survived its own idle stop"

            old_link_status, _old_link_body = _fetch(live_url)
            assert old_link_status != 200
        finally:
            # (k) if the project's runtime is still recorded, stop it and report the outcome.
            load = load_state_result(project)
            if load.kind != STATE_ABSENT:
                cleanup = run_runtime_verb("stop", project)
                print(f"F041 R6 C6 cleanup stop: ok={cleanup.ok} payload={cleanup.payload}")
            monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
            monkeypatch.delenv("REMEDY_PREVIEW_IDLE_TTL_SECONDS", raising=False)
            reset_config()
