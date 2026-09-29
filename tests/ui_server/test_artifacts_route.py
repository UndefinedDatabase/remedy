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


class _ServerHarness:
    """A real server for one saved job, and a GET helper."""

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


class TestArtifactsRoute(_ServerHarness):
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


class TestArtifactFileRoute(_ServerHarness):
    """/api/jobs/<id>/artifacts/file (DECISION F041 D2): the bytes, and the headers that keep
    a served file from ever running as a page."""

    #: The headers every served artifact carries, literal on purpose.
    ARTIFACT_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'none'; sandbox",
        "Cache-Control": "no-store",
    }

    def _fetch(self, query: str):
        port, token = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/jobs/{self.job_id}/artifacts/file?token={token}&{query}")
        resp = conn.getresponse()
        headers, body = dict(resp.getheaders()), resp.read()
        conn.close()
        return resp.status, headers, body

    def test_a_screenshot_is_served_with_its_type_and_the_headers(self):
        captures = job_evidence_dir(self.job_id) / "captures"
        captures.mkdir(parents=True)
        (captures / "home.png").write_bytes(b"\x89PNG-bytes")
        status, headers, body = self._fetch("root=evidence&path=captures/home.png")
        assert status == 200
        assert body == b"\x89PNG-bytes"
        assert headers["Content-Type"] == "image/png"
        assert headers["Content-Length"] == str(len(body))
        for name, value in self.ARTIFACT_HEADERS.items():
            assert headers[name] == value

    def test_the_readme_is_served_as_plain_text_never_as_html(self):
        evidence = job_evidence_dir(self.job_id)
        evidence.mkdir(parents=True)
        (evidence / "README.md").write_text("<script>alert(1)</script>\n")
        status, headers, body = self._fetch("root=evidence&path=README.md")
        assert status == 200
        assert body == b"<script>alert(1)</script>\n"
        assert headers["Content-Type"] == "text/plain; charset=utf-8"
        for name, value in self.ARTIFACT_HEADERS.items():
            assert headers[name] == value

    @pytest.mark.parametrize(("query", "status", "error"), [
        ("root=evidence&path=captures/missing.png", 404, "artifact not found"),
        ("root=evidence&path=captures/../README.md", 400, "invalid artifact request"),
        ("root=evidence&path=..%2F..%2Fsecret.png", 400, "invalid artifact request"),
        ("root=repo&path=README.md", 400, "invalid artifact request"),
        ("path=README.md", 400, "invalid artifact request"),
    ])
    def test_a_refused_request_answers_json_and_no_bytes(self, query, status, error):
        (job_evidence_dir(self.job_id) / "captures").mkdir(parents=True)
        got, headers, body = self._fetch(query)
        assert got == status
        assert headers["Content-Type"] == "application/json"
        assert json.loads(body) == {"error": error}

    def test_the_file_route_answers_404_for_an_unknown_job(self):
        status, _, body = self._get(
            f"/api/jobs/{uuid4()}/artifacts/file?token={{token}}&root=evidence&path=README.md")
        assert status == 404
        assert json.loads(body)["error"] == "job not found"


class TestStaticAssetContainment(_ServerHarness):
    """R-1105: `/assets/` serves only from inside the built `dist`, by a path test."""

    def test_a_sibling_whose_name_starts_with_dist_is_not_served(self, monkeypatch):
        from packages.orchestration import ui_server

        dist = self.tmp_path / "ui" / "dist"
        (dist / "assets").mkdir(parents=True)
        (dist / "index.html").write_text("<html></html>")
        (dist / "assets" / "app.js").write_text("ok")
        (self.tmp_path / "ui" / "dist-old").mkdir()
        (self.tmp_path / "ui" / "dist-old" / "secret.js").write_text("secret")
        monkeypatch.setattr(ui_server, "_get_frontend_dist", lambda: dist)
        port, _ = self._start_server()
        answers = {}
        for path in ("/assets/app.js", "/assets/../../dist-old/secret.js"):
            conn = HTTPConnection("127.0.0.1", port, timeout=5)
            conn.request("GET", path)
            resp = conn.getresponse()
            answers[path] = (resp.status, resp.read())
            conn.close()
        assert answers["/assets/app.js"] == (200, b"ok")
        assert answers["/assets/../../dist-old/secret.js"][0] == 403
