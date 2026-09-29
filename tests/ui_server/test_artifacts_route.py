"""Route tests for /api/jobs/<job_id>/artifacts (F041 T001, DECISION F041 D1).

A real server on a free port, a real token and a real request, as the tour route's own tests
reach theirs. The route may have ONE property: it answers `artifact_preview.artifacts_view` for
the job, with the README already sanitized on the server, so the browser never receives markup
the attack corpus has not been through.
"""

from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from uuid import uuid4

import pytest

from packages.orchestration.artifact_preview import artifacts_view
from packages.orchestration.data_paths import job_evidence_dir
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from tests.ui_server.server_start import wait_for_server_info

#: The view's key set, literal on purpose: the route must not be able to change it.
ARTIFACTS_VIEW_KEYS = {"readme", "images", "error"}


def _make_job() -> JobPlan:
    job = JobPlan(
        job_title="f041-artifacts-endpoint-job",
        user_prompt="Test the artifacts endpoint",
        tasks=[TaskEntry(title="write a readme")],
    )
    save_job_plan(job)
    return job


class TestArtifactsRoute:
    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = _make_job()
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path

    def _start_server(self):
        """Start the server in a background thread, return (port, token)."""
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

        t = threading.Thread(target=run, daemon=True)
        t.start()
        info = wait_for_server_info(info_file, t)
        return info["port"], token

    def _get(self, path: str):
        port, token = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", path.format(port=port, token=token))
        resp = conn.getresponse()
        status, content_type, body = resp.status, resp.getheader("Content-Type"), resp.read()
        conn.close()
        return status, content_type, body

    def test_the_route_answers_the_sanitized_view(self):
        evidence = job_evidence_dir(self.job_id)
        (evidence / "captures").mkdir(parents=True)
        readme = "# Result\n\n<img src=x onerror=alert(1)>\n"
        (evidence / "README.md").write_text(readme)
        (evidence / "captures" / "home.png").write_bytes(b"png")
        status, content_type, body = self._get(
            f"/api/jobs/{self.job_id}/artifacts?token={{token}}")
        assert status == 200
        assert content_type == "application/json"
        data = json.loads(body)
        assert data == artifacts_view(self.job_id)
        assert data == {
            "readme": {
                "root": "evidence", "path": "README.md",
                "html": "<h1>Result</h1><p>&lt;img src=x onerror=alert(1)&gt;</p>",
                "truncated": False, "source_bytes": len(readme.encode("utf-8")),
            },
            "images": [{"root": "evidence", "path": "captures/home.png", "bytes": 3,
                        "content_type": "image/png"}],
            "error": "",
        }

    def test_the_route_answers_the_empty_view_for_a_job_with_no_artifacts(self):
        status, _, body = self._get(f"/api/jobs/{self.job_id}/artifacts?token={{token}}")
        assert status == 200
        data = json.loads(body)
        assert set(data) == ARTIFACTS_VIEW_KEYS
        assert data == {"readme": None, "images": [], "error": ""}

    def test_the_route_answers_404_for_an_unknown_job(self):
        status, _, body = self._get(f"/api/jobs/{uuid4()}/artifacts?token={{token}}")
        assert status == 404
        assert json.loads(body)["error"] == "job not found"

    def test_a_neighbouring_endpoint_is_still_unhandled(self):
        # Registering "artifacts" must not widen the dispatch; the fall-through's error string
        # differs from the loader's, so this cannot pass by finding the job missing instead.
        status, _, body = self._get(f"/api/jobs/{self.job_id}/artifact?token={{token}}")
        assert status != 200
        assert json.loads(body)["error"] == "not found"

    def test_the_route_refuses_an_invalid_token(self):
        status, _, body = self._get(f"/api/jobs/{self.job_id}/artifacts?token=wrong")
        assert status == 403
        assert json.loads(body)["error"] == "invalid token"
