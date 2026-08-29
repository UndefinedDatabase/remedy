"""Route tests for /api/jobs/<job_id>/digest (F040 T001).

Reaches the endpoint the way the other ui_server tests reach theirs — a real
server on a free port, a real token, a real HTTP request — and pins the ONE
property this route is allowed to have: it composes NOTHING.  The body it
answers must be byte-for-byte the dict ``build_job_digest`` returns for the same
job, so a route that filtered, defaulted, renamed or re-versioned the envelope
would become a second home for a composition F040 deliberately made single.
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
from packages.orchestration.job_digest import JOB_DIGEST_VERSION, build_job_digest
from packages.orchestration.ui_server import _load_events

#: The envelope's top-level contract, from ``job_digest.build_job_digest``.  A
#: literal here on purpose: the point of the assertion is that the ROUTE cannot
#: change this set, so reading it back out of the module under test would make
#: the check vacuous.
DIGEST_KEYS = {
    "version",
    "job_id",
    "state",
    "headline",
    "cost",
    "ownership",
    "decisions",
    "primary_action",
}


def _make_job() -> Job:
    # A real plan of work — one task — and no target_repo in metadata, so the
    # decision queue derives a card and the digest's decision and action
    # sections are non-trivial rather than every-field-absent.
    return Job(
        name="f040-digest-endpoint-job",
        user_prompt="Test the digest endpoint",
        tasks=[Task(description="write a readme")],
    )


class TestDigestRoute:
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
        content_type = resp.getheader("Content-Type")
        body = resp.read()
        conn.close()
        return status, content_type, body

    def test_digest_endpoint_answers_json_for_a_job_with_a_plan(self):
        status, content_type, body = self._get(
            f"/api/jobs/{self.job_id}/digest?token={{token}}")
        assert status == 200
        assert content_type == "application/json"
        assert json.loads(body)["job_id"] == self.job_id

    def test_digest_endpoint_is_a_pass_through_of_the_composition(self):
        # THE assertion that makes "the route adds no behaviour" enforceable:
        # the whole decoded body, compared against the composition computed here
        # for the same job.  Any key the route added, dropped, defaulted or
        # reshaped shows up as an inequality.
        expected = build_job_digest(self.job, _load_events(self.job))
        status, _, body = self._get(
            f"/api/jobs/{self.job_id}/digest?token={{token}}")
        assert status == 200
        assert json.loads(body) == expected

    def test_digest_body_carries_exactly_the_envelope_key_set(self):
        status, _, body = self._get(
            f"/api/jobs/{self.job_id}/digest?token={{token}}")
        assert status == 200
        data = json.loads(body)
        assert set(data) == DIGEST_KEYS
        assert len(DIGEST_KEYS) == 8

    def test_digest_version_is_the_modules_own_and_never_a_literal(self):
        # Imported, not written as 1: a version bump in job_digest.py that
        # forgot this consumer would otherwise pass here forever.
        status, _, body = self._get(
            f"/api/jobs/{self.job_id}/digest?token={{token}}")
        assert status == 200
        assert json.loads(body)["version"] == JOB_DIGEST_VERSION

    def test_digest_endpoint_answers_404_for_an_unknown_job(self):
        # MEASURED against `_load_job`, not assumed: a well-formed UUID that
        # names no stored job is answered by the loader before any handler runs,
        # and the loader's answer for it is 404 "job not found".
        status, _, body = self._get(
            f"/api/jobs/{uuid4()}/digest?token={{token}}")
        assert status == 404
        assert json.loads(body)["error"] == "job not found"

    def test_a_neighbouring_endpoint_is_still_unhandled(self):
        # Registering "digest" must not widen the dispatch.  The neighbour is
        # answered by the fall-through, whose error string differs from the
        # loader's, so this cannot pass by finding the job missing instead.
        status, _, body = self._get(
            f"/api/jobs/{self.job_id}/digests?token={{token}}")
        assert status != 200
        assert json.loads(body)["error"] == "not found"

    def test_digest_endpoint_refuses_an_invalid_token(self):
        status, _, body = self._get(f"/api/jobs/{self.job_id}/digest?token=wrong")
        assert status == 403
        assert json.loads(body)["error"] == "invalid token"
