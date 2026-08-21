"""
Domain tests: ui_server/test_command_channel.py

Contract tests for F009 T001 — the single write channel. They pin the
observable behaviour of POST `/api/jobs/<job_id>/commands`: which requests the
door rejects, with which status, and which field name a shape error reports.
They also guard the half of DECISION F009 D3 that touches the existing GET
door, so a constant-time comparison cannot silently break read access.
"""

from __future__ import annotations

import json
import threading
import time
from http.client import HTTPConnection
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

import pytest

from packages.core.models import Job, Task

# The wire spelling is pinned here on purpose: a test that imports the constant
# it is checking cannot catch a rename of the header the browser has to send.
CSRF_HEADER = "X-Remedy-CSRF"

COMMAND_REQUEST_MAX_BYTES = 64 * 1024


def _make_job() -> Job:
    return Job(
        name="test-command-channel-job",
        user_prompt="Test prompt for the command channel",
        tasks=[Task(type="write_readme", description="Write a README")],
    )


class TestCommandChannelDoor:
    """Integration tests that start a real server on a free port."""

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

    # -- request helpers ---------------------------------------------------

    def _request(self, port, method, path, body=None, headers=None):
        """Issue one request on a fresh connection, return (status, parsed body)."""
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            resp = conn.getresponse()
            raw = resp.read()
            status = resp.status
        finally:
            conn.close()
        try:
            return status, json.loads(raw)
        except ValueError:
            return status, {}

    def _commands_path(self, job_id=None):
        return f"/api/jobs/{job_id or self.job_id}/commands"

    def _auth_headers(self, token, *, bearer=None, csrf=None):
        """Full, valid credentials unless a caller overrides one of them."""
        headers = {}
        bearer_value = f"Bearer {token}" if bearer is None else bearer
        if bearer_value is not False:
            headers["Authorization"] = bearer_value
        csrf_value = token if csrf is None else csrf
        if csrf_value is not False:
            headers[CSRF_HEADER] = csrf_value
        headers["Content-Type"] = "application/json"
        return headers

    def _valid_body(self, **overrides):
        payload = {"command": "pause_job", "client_nonce": "nonce-0001"}
        payload.update(overrides)
        return json.dumps(payload)

    # -- C: only the commands route accepts a mutating method --------------

    def test_post_to_non_commands_path_is_405(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", "/api/state", body="{}",
            headers=self._auth_headers(token))
        assert status == 405
        assert body["error"] == "method not allowed"

    def test_post_to_job_dashboard_is_405(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", f"/api/jobs/{self.job_id}/dashboard", body="{}",
            headers=self._auth_headers(token))
        assert status == 405
        assert body["error"] == "method not allowed"

    def test_put_is_405_even_on_the_commands_path(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "PUT", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token))
        assert status == 405
        assert body["error"] == "method not allowed"

    def test_delete_is_405_even_on_the_commands_path(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "DELETE", self._commands_path(),
            headers=self._auth_headers(token))
        assert status == 405
        assert body["error"] == "method not allowed"

    # -- D.1: the bearer token ---------------------------------------------

    def test_missing_bearer_is_403(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, bearer=False))
        assert status == 403
        assert body["error"] == "invalid token"

    def test_malformed_bearer_is_403(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, bearer=token))
        assert status == 403
        assert body["error"] == "invalid token"

    def test_bearer_without_a_token_is_403(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, bearer="Bearer"))
        assert status == 403
        assert body["error"] == "invalid token"

    def test_wrong_bearer_is_403(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, bearer="Bearer not-the-token"))
        assert status == 403
        assert body["error"] == "invalid token"

    def test_non_ascii_bearer_is_403_and_does_not_raise(self):
        """The TypeError trap of D3, on the POST side of the same helper."""
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, bearer="Bearer tökén-ünicöde"))
        assert status == 403
        assert body["error"] == "invalid token"

    # -- D.2: the CSRF header (DECISION F009 D11) ---------------------------

    def test_missing_csrf_header_is_403(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, csrf=False))
        assert status == 403
        assert body["error"] == "invalid csrf token"

    def test_wrong_csrf_header_is_403(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, csrf="not-the-token"))
        assert status == 403
        assert body["error"] == "invalid csrf token"

    def test_csrf_is_checked_after_the_bearer(self):
        """A caller with neither credential learns nothing about the CSRF rule."""
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, bearer=False, csrf=False))
        assert status == 403
        assert body["error"] == "invalid token"

    # -- D.3: the job id ----------------------------------------------------

    def test_unresolvable_job_id_is_404(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(job_id=str(uuid4())),
            body=self._valid_body(), headers=self._auth_headers(token))
        assert status == 404
        assert body["error"] == "job not found"

    def test_unresolvable_job_id_matches_the_get_door(self):
        port, token = self._start_server()
        missing = str(uuid4())
        post_status, post_body = self._request(
            port, "POST", self._commands_path(job_id=missing),
            body=self._valid_body(), headers=self._auth_headers(token))
        get_status, get_body = self._request(
            port, "GET", f"/api/jobs/{missing}/dashboard?token={token}")
        assert (post_status, post_body) == (get_status, get_body)

    def test_job_id_is_checked_after_the_credentials(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(job_id=str(uuid4())),
            body=self._valid_body(),
            headers=self._auth_headers(token, bearer=False))
        assert status == 403
        assert body["error"] == "invalid token"

    # -- D.4: request shape, each error naming its field --------------------

    def test_absent_body_is_400_on_field_body(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "body"
        assert "error" in body

    def test_oversize_body_is_400_on_field_body(self):
        port, token = self._start_server()
        oversize = json.dumps({
            "command": "pause_job",
            "client_nonce": "nonce-0001",
            "args": {"filler": "x" * (COMMAND_REQUEST_MAX_BYTES + 1)},
        })
        assert len(oversize) > COMMAND_REQUEST_MAX_BYTES
        status, body = self._request(
            port, "POST", self._commands_path(), body=oversize,
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "body"
        assert "error" in body

    def test_invalid_json_body_is_400_on_field_body(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body="{not json",
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "body"
        assert "error" in body

    def test_non_object_body_is_400_on_field_body(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body="[1, 2, 3]",
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "body"
        assert "error" in body

    def test_missing_command_is_400_on_field_command(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=json.dumps({"client_nonce": "nonce-0001"}),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "command"
        assert "error" in body

    def test_non_string_command_is_400_on_field_command(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=17),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "command"

    def test_empty_command_is_400_on_field_command(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=""),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "command"

    def test_missing_client_nonce_is_400_on_field_client_nonce(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=json.dumps({"command": "pause_job"}),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "client_nonce"
        assert "error" in body

    def test_empty_client_nonce_is_400_on_field_client_nonce(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(client_nonce=""),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "client_nonce"

    def test_non_object_args_is_400_on_field_args(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(args="not-an-object"),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "args"
        assert "error" in body

    # -- D.5: the R7 seam ---------------------------------------------------

    def test_well_formed_command_reaches_the_501_seam(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token))
        assert status == 501
        assert body["error"] == "command channel not yet accepting commands"
        assert body["command"] == "pause_job"

    def test_absent_args_is_valid_and_reaches_the_seam(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=json.dumps({"command": "resume_job", "client_nonce": "n-2"}),
            headers=self._auth_headers(token))
        assert status == 501
        assert body["command"] == "resume_job"

    def test_present_args_object_is_valid_and_reaches_the_seam(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(args={"reason": "operator asked"}),
            headers=self._auth_headers(token))
        assert status == 501
        assert body["command"] == "pause_job"

    # -- B: the GET door still behaves as it did ----------------------------

    def test_get_door_still_answers_200_for_the_correct_token(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "GET", f"/api/jobs/{self.job_id}/dashboard?token={token}")
        assert status == 200
        assert body["job_id"] == self.job_id

    def test_get_door_still_answers_403_for_a_wrong_token(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "GET", "/api/state?token=wrong")
        assert status == 403
        assert body["error"] == "invalid token"

    def test_get_door_answers_403_for_a_non_ascii_token(self):
        """Regression for D3: `compare_digest` raises TypeError on a non-ASCII str.

        The query token is attacker-controlled, so a comparison that raises
        would turn a rejected request into a 500 — or into no response at all.
        """
        port, token = self._start_server()
        status, body = self._request(
            port, "GET", "/api/state?token=" + quote("tökén-ünicöde"))
        assert status == 403
        assert body["error"] == "invalid token"


class TestServerTokenMatches:
    """Unit coverage for the constant-time helper of contract A."""

    def test_equal_tokens_match(self):
        from packages.orchestration.ui_server import server_token_matches
        assert server_token_matches("abc123", "abc123") is True

    def test_different_tokens_do_not_match(self):
        from packages.orchestration.ui_server import server_token_matches
        assert server_token_matches("abc123", "abc124") is False

    def test_missing_supplied_token_does_not_raise(self):
        from packages.orchestration.ui_server import server_token_matches
        assert server_token_matches(None, "abc123") is False

    def test_non_ascii_token_does_not_raise(self):
        from packages.orchestration.ui_server import server_token_matches
        assert server_token_matches("tökén", "abc123") is False

    def test_equal_non_ascii_tokens_match(self):
        from packages.orchestration.ui_server import server_token_matches
        assert server_token_matches("tökén", "tökén") is True
