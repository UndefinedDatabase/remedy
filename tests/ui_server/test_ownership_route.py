"""Route tests for /api/jobs/<job_id>/ownership (F035 T003, DECISION F035 D4).

Reaches the endpoint the way the digest route's own tests reach theirs — a real server on a
free port, a real token, a real HTTP request — and pins the ONE property this route is
allowed to have: it answers `ownership_phrases.ownership_view` byte-for-byte, the SAME view
`remedy job ownership` prints, so the browser and the CLI cannot say two different things
about who did what.
"""

from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from uuid import uuid4

import pytest

from packages.orchestration.ownership_phrases import ownership_view
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from tests.ui_server.server_start import wait_for_server_info

#: The view's own key set (S2), literal on purpose: the point of the assertion is that the
#: ROUTE cannot change this set, so reading it back out of the module under test would make
#: the check vacuous.
OWNERSHIP_KEYS = {"schema", "job_id", "entries", "error"}


def _make_job() -> JobPlan:
    job = JobPlan(
        job_title="f035-ownership-endpoint-job",
        user_prompt="Test the ownership endpoint",
        tasks=[TaskEntry(title="write a readme")],
    )
    job.metadata["task_vetoes"] = {
        job.tasks[0].task_id: {
            "request_id": "r1",
            "requested_at": "2026-08-29T00:00:00+00:00",
            "actor": "alice",
            "reason": "bad approach",
            "status_at_veto": "completed",
            "unreachable_task_ids": [],
        },
    }
    return job


class TestOwnershipRoute:
    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = _make_job()
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
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

        t = threading.Thread(target=run, daemon=True)
        t.start()

        info = wait_for_server_info(info_file, t)
        return info["port"], token

    def _get(self, path: str):
        port, token = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", path.format(port=port, token=token))
        resp = conn.getresponse()
        status = resp.status
        content_type = resp.getheader("Content-Type")
        body = resp.read()
        conn.close()
        return status, content_type, body

    def test_ownership_endpoint_answers_the_view_for_a_job_with_an_action(self):
        expected = ownership_view(self.job)
        status, content_type, body = self._get(
            f"/api/jobs/{self.job_id}/ownership?token={{token}}")
        assert status == 200
        assert content_type == "application/json"
        data = json.loads(body)
        assert data == expected
        assert set(data) == OWNERSHIP_KEYS
        assert data["entries"]
        assert all(e["sentence"] for e in data["entries"])

    def test_ownership_endpoint_answers_404_for_an_unknown_job(self):
        status, _, body = self._get(
            f"/api/jobs/{uuid4()}/ownership?token={{token}}")
        assert status == 404
        assert json.loads(body)["error"] == "job not found"

    def test_a_neighbouring_endpoint_is_still_unhandled(self):
        # Registering "ownership" must not widen the dispatch.  The neighbour is
        # answered by the fall-through, whose error string differs from the
        # loader's, so this cannot pass by finding the job missing instead.
        status, _, body = self._get(
            f"/api/jobs/{self.job_id}/ownerships?token={{token}}")
        assert status != 200
        assert json.loads(body)["error"] == "not found"

    def test_ownership_endpoint_refuses_an_invalid_token(self):
        status, _, body = self._get(f"/api/jobs/{self.job_id}/ownership?token=wrong")
        assert status == 403
        assert json.loads(body)["error"] == "invalid token"
