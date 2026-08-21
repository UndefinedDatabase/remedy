"""
Domain tests: ui_server/test_server_concurrency.py

The cockpit server must serve two requests at once. F008 streams a long-lived
SSE response from this same process, so a server that handles one request at a
time would block every other cockpit request for the life of one stream.
DECISION F008 D1 makes that a prerequisite of T001 rather than part of it.
"""

from __future__ import annotations

import json
import secrets
import threading
import time
import urllib.request
from pathlib import Path

import pytest

from packages.core.models import Job, Task


def _make_job(**overrides: object) -> Job:
    defaults = dict(
        name="test-concurrency-job",
        user_prompt="Test prompt for concurrency",
        tasks=[Task(type="write_readme", description="Write a README")],
    )
    defaults.update(overrides)
    return Job(**defaults)


class TestServerServesConcurrentRequests:
    """A blocking server cannot host an SSE stream — proven, not assumed."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job

        self.job = _make_job()
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path

    def _start_server(self) -> tuple[int, str]:
        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = secrets.token_urlsafe(16)

        def run():
            try:
                start_ui_server(
                    self.job_id,
                    host="127.0.0.1",
                    port=0,
                    token=token,
                    open_browser=False,
                    info_file=info_file,
                )
            except (SystemExit, KeyboardInterrupt):
                pass

        threading.Thread(target=run, daemon=True).start()

        for _ in range(50):
            if Path(info_file).exists():
                return json.loads(Path(info_file).read_text())["port"], token
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

    def test_two_requests_are_in_flight_at_once(self, monkeypatch):
        # A barrier, not a stopwatch: both requests must be inside the handler
        # simultaneously or the barrier breaks. That is a fact about
        # concurrency rather than a threshold about speed, so it cannot flake
        # on a slow runner.
        from packages.orchestration import ui_server as mod

        port, token = self._start_server()
        barrier = threading.Barrier(2, timeout=8)
        build_dashboard = mod._build_dashboard

        def gated(job):
            barrier.wait()
            return build_dashboard(job)

        monkeypatch.setattr(mod, "_build_dashboard", gated)

        url = f"http://127.0.0.1:{port}/api/state?job_id={self.job_id}&token={token}"
        outcomes: list[object] = []

        def hit():
            try:
                with urllib.request.urlopen(url, timeout=20) as resp:
                    outcomes.append(resp.status)
            except Exception as exc:  # noqa: BLE001 — the failure mode is the evidence
                outcomes.append(type(exc).__name__)

        threads = [threading.Thread(target=hit) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=25)

        assert outcomes == [200, 200], (
            f"both concurrent requests must be served, got {outcomes} — "
            "a single-threaded server breaks the barrier instead"
        )
