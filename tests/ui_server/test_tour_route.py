"""Route tests for /api/jobs/<job_id>/tour (F036 T003, DECISION F036 D5).

Reaches the endpoint the way the ownership route's own tests reach theirs — a real server on
a free port, a real token, a real HTTP request — and pins the ONE property this route is
allowed to have: it answers `result_tour.tour_view` byte-for-byte, the SAME view the command
line's `tour` section shows, so the browser and the CLI cannot say two different things about
a job's tour.
"""

from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from uuid import uuid4

import pytest

from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.result_tour import tour_path, tour_view, write_result_tour
from tests.ui_server.server_start import wait_for_server_info

#: The view's own key set (S1), literal on purpose: the point of the assertion is that the
#: ROUTE cannot change this set, so reading it back out of the module under test would make
#: the check vacuous.
TOUR_VIEW_KEYS = {"stored", "version", "tour", "error"}


def _make_job() -> JobPlan:
    job = JobPlan(
        job_title="f036-tour-endpoint-job",
        user_prompt="Test the tour endpoint",
        tasks=[TaskEntry(title="write a readme")],
    )
    save_job_plan(job)
    return job


class TestTourRoute:
    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = _make_job()
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

    def test_tour_endpoint_answers_the_view_for_a_job_with_a_stored_tour(self):
        write_result_tour(self.job, call_fn=None)
        expected = tour_view(self.job)
        status, content_type, body = self._get(
            f"/api/jobs/{self.job_id}/tour?token={{token}}")
        assert status == 200
        assert content_type == "application/json"
        data = json.loads(body)
        assert data == expected
        assert set(data) == TOUR_VIEW_KEYS
        assert data["stored"] is True

    def test_tour_endpoint_answers_the_view_for_a_job_with_none_stored(self):
        expected = tour_view(self.job)
        status, content_type, body = self._get(
            f"/api/jobs/{self.job_id}/tour?token={{token}}")
        assert status == 200
        assert content_type == "application/json"
        data = json.loads(body)
        assert data == expected
        assert set(data) == TOUR_VIEW_KEYS
        assert data["stored"] is False
        assert data["version"] == 0
        assert data["error"] == ""

    def test_tour_endpoint_answers_200_with_the_error_for_an_unreadable_stored_tour(self):
        path = tour_path(self.job_id, 1)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("not json", encoding="utf-8")

        status, _, body = self._get(f"/api/jobs/{self.job_id}/tour?token={{token}}")
        assert status == 200
        data = json.loads(body)
        assert set(data) == TOUR_VIEW_KEYS
        assert data["stored"] is False
        assert data["error"] != ""

    def test_tour_endpoint_answers_404_for_an_unknown_job(self):
        status, _, body = self._get(
            f"/api/jobs/{uuid4()}/tour?token={{token}}")
        assert status == 404
        assert json.loads(body)["error"] == "job not found"

    def test_a_neighbouring_endpoint_is_still_unhandled(self):
        # Registering "tour" must not widen the dispatch.  The neighbour is
        # answered by the fall-through, whose error string differs from the
        # loader's, so this cannot pass by finding the job missing instead.
        status, _, body = self._get(
            f"/api/jobs/{self.job_id}/tours?token={{token}}")
        assert status != 200
        assert json.loads(body)["error"] == "not found"

    def test_tour_endpoint_refuses_an_invalid_token(self):
        status, _, body = self._get(f"/api/jobs/{self.job_id}/tour?token=wrong")
        assert status == 403
        assert json.loads(body)["error"] == "invalid token"
