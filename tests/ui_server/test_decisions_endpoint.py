"""Route tests for /api/jobs/<job_id>/decisions (F031 T001).

Reaches the endpoint the way the other ui_server tests reach theirs: a real
server on a free port, a real token, and a real HTTP request.
"""

from __future__ import annotations

import json
import threading
import time
from http.client import HTTPConnection
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Job, Task


def _make_job() -> Job:
    # No target_repo in metadata, so the decision queue derives at least one
    # card ("no target repository attached") and the inbox is never empty.
    return Job(
        name="f031-decisions-endpoint-job",
        user_prompt="Test the decisions endpoint",
        tasks=[Task(description="write a readme")],
    )


class TestDecisionsEndpoint:
    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = _make_job()
        from packages.orchestration.storage import save_job
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path

    def _start_server(self, **kwargs):
        """Start the server in a background thread, return (port, token)."""
        import secrets as _s

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = _s.token_urlsafe(16)

        def run():
            try:
                start_ui_server(
                    self.job_id,
                    host="127.0.0.1",
                    port=0,
                    token=token,
                    open_browser=False,
                    info_file=info_file,
                    **kwargs,
                )
            except (SystemExit, KeyboardInterrupt):
                pass

        threading.Thread(target=run, daemon=True).start()

        for _ in range(50):
            if Path(info_file).exists():
                info = json.loads(Path(info_file).read_text())
                return info["port"], token
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

    def _get(self, path: str):
        port, token = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", path.format(port=port, token=token))
        resp = conn.getresponse()
        status = resp.status
        body = resp.read()
        conn.close()
        return status, body

    def test_decisions_endpoint_returns_the_inbox_document(self):
        status, body = self._get(
            f"/api/jobs/{self.job_id}/decisions?token={{token}}")
        assert status == 200
        data = json.loads(body)
        assert set(data) == {"version", "job_id", "decisions"}
        assert data["version"] == 1
        assert data["job_id"] == self.job_id

    def test_decision_card_carries_age_and_blocked_count(self):
        status, body = self._get(
            f"/api/jobs/{self.job_id}/decisions?token={{token}}")
        assert status == 200
        data = json.loads(body)
        assert data["decisions"], "fixture job produced no decision card"
        card = data["decisions"][0]
        assert "age_seconds" in card
        assert "blocked_count" in card
        assert isinstance(card["blocked_count"], int)

    def test_decisions_endpoint_refuses_an_invalid_token(self):
        status, body = self._get(f"/api/jobs/{self.job_id}/decisions?token=wrong")
        assert status == 403
        assert json.loads(body)["error"] == "invalid token"

    def test_decisions_endpoint_answers_404_for_an_unknown_job(self):
        status, body = self._get(
            f"/api/jobs/{uuid4()}/decisions?token={{token}}")
        assert status == 404
        assert "error" in json.loads(body)
