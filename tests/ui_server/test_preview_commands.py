"""The write door's preview pair and the `preview` view (F041 T002, DECISION F041 D4).

A real server with its real preview worker; only the harness's verbs are a scripted stand-in,
put on `preview_runner` where the worker looks them up. The door answers at once with the
recorded state, and the worker's own thread carries the preview to live and back.
"""

from __future__ import annotations

import json
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration import preview_runner
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.preview_control import VerbResult
from tests.ui_server.server_start import wait_for_server_info

CSRF_HEADER = "X-Remedy-CSRF"
SERVED = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5173/", "port": 5173})
PROBED = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5173/", "port": 5173})
STOPPED = VerbResult(True, {"ok": True})


class TestPreviewCommands:
    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        project = tmp_path / "project"
        project.mkdir()
        self.job = JobPlan(job_title="f041-preview-door-job", user_prompt="preview",
                           tasks=[TaskEntry(title="t")], repo_path=str(project))
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path
        self.calls: list[tuple[str, str]] = []
        answers = {"serve": SERVED, "probe": PROBED, "stop": STOPPED}

        def runner(verb, root):
            self.calls.append((verb, str(root)))
            return answers[verb]

        monkeypatch.setattr(preview_runner, "run_runtime_verb", runner)

    def _start_server(self):
        import secrets as _s

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = _s.token_urlsafe(16)

        def run():
            try:
                start_ui_server(self.job_id, host="127.0.0.1", port=0, token=token,
                                open_browser=False, info_file=info_file)
            except (SystemExit, KeyboardInterrupt):
                pass

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        info = wait_for_server_info(info_file, thread)
        return info["port"], token

    def _request(self, port, method, path, body=None, headers=None):
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            resp = conn.getresponse()
            return resp.status, json.loads(resp.read())
        finally:
            conn.close()

    def _command(self, port, token, command, nonce):
        headers = {"Authorization": f"Bearer {token}", CSRF_HEADER: token,
                   "Content-Type": "application/json"}
        body = json.dumps({"command": command, "client_nonce": nonce})
        return self._request(port, "POST", f"/api/jobs/{self.job_id}/commands", body, headers)

    def _wait_for(self, port, token, state):
        deadline = time.monotonic() + 10
        view = {}
        while time.monotonic() < deadline:
            status, view = self._request(
                port, "GET", f"/api/jobs/{self.job_id}/preview?token={token}")
            assert status == 200
            if view["state"] == state:
                return view
            time.sleep(0.05)
        raise AssertionError(f"preview never reached {state!r}: {view}")

    def test_start_then_stop_through_the_door(self):
        port, token = self._start_server()
        status, body = self._command(port, token, "job.preview-start", "nonce-preview-1")
        assert status == 200
        assert body == {"command": "job.preview-start", "outcome": "accepted",
                        "state": "starting"}
        view = self._wait_for(port, token, "live")
        assert (view["url"], view["port"], view["reason"]) == ("http://127.0.0.1:5173/", 5173, "")
        status, body = self._command(port, token, "job.preview-stop", "nonce-preview-2")
        assert status == 200
        assert (body["command"], body["outcome"]) == ("job.preview-stop", "accepted")
        view = self._wait_for(port, token, "stopped")
        assert (view["url"], view["port"], view["reason"]) == ("", 0, "stopped on request")
        assert [verb for verb, _ in self.calls[:2]] == ["serve", "probe"]
        assert self.calls[-1] == ("stop", str(Path(self.job.repo_path)))

    def test_the_preview_view_of_a_job_never_previewed_is_stopped(self):
        port, token = self._start_server()
        status, view = self._request(port, "GET", f"/api/jobs/{self.job_id}/preview?token={token}")
        assert status == 200
        assert view == {"state": "stopped", "url": "", "port": 0, "reason": "", "updated_at": ""}
        assert self.calls == []

    def test_a_replayed_start_is_answered_from_the_first_and_runs_nothing_new(self):
        port, token = self._start_server()
        first = self._command(port, token, "job.preview-start", "nonce-preview-3")
        self._wait_for(port, token, "live")
        calls = list(self.calls)
        assert self._command(port, token, "job.preview-start", "nonce-preview-3") == first
        time.sleep(0.2)
        assert self.calls == calls
        self._command(port, token, "job.preview-stop", "nonce-preview-4")
        self._wait_for(port, token, "stopped")
