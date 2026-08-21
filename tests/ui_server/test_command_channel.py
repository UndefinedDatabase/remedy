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

# A real catalog command_id that the write door does NOT expose, and a string
# that names no command anywhere. The door must answer both identically.
UNEXPOSED_CATALOG_COMMAND = "job.list"
UNKNOWN_COMMAND = "not.a.command.anywhere"


def _make_job() -> Job:
    return Job(
        name="test-command-channel-job",
        user_prompt="Test prompt for the command channel",
        tasks=[Task(type="write_readme", description="Write a README")],
    )


@pytest.fixture
def command_rate_limit(monkeypatch):
    """Set the write door's minute budget, and report the value the door reads.

    The configured limit is RETURNED rather than assumed, so a boundary test
    counts up to the number the server will actually enforce instead of to a
    literal that could drift away from it. The cached config is cleared on the
    way in and on the way out: it is process-global state and the server runs
    in this same process.
    """
    from packages.orchestration.config import get_config, reset_config

    def configure(limit: int) -> int:
        monkeypatch.setenv("REMEDY_UI_COMMAND_RATE_LIMIT_PER_MINUTE", str(limit))
        reset_config()
        return get_config().get("ui.command_rate_limit_per_minute")

    yield configure
    reset_config()


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
        # The default command is UI-exposed so that a body built here is valid
        # all the way to the seam; tests about the subset name their id inline.
        payload = {"command": "job.stop", "client_nonce": "nonce-0001"}
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
        assert body["command"] == "job.stop"

    def test_absent_args_is_valid_and_reaches_the_seam(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=json.dumps({"command": "decision.resolve", "client_nonce": "n-2"}),
            headers=self._auth_headers(token))
        assert status == 501
        assert body["command"] == "decision.resolve"

    def test_present_args_object_is_valid_and_reaches_the_seam(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(args={"reason": "operator asked"}),
            headers=self._auth_headers(token))
        assert status == 501
        assert body["command"] == "job.stop"

    # -- D.6: the UI-exposed subset (DECISION F009 D4 and D12) --------------

    def test_every_exposed_command_reaches_the_seam(self):
        """The set itself is the contract, not the two literals above."""
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

        port, token = self._start_server()
        for index, command_id in enumerate(sorted(UI_EXPOSED_COMMANDS)):
            status, body = self._request(
                port, "POST", self._commands_path(),
                body=self._valid_body(
                    command=command_id, client_nonce=f"nonce-exposed-{index}"),
                headers=self._auth_headers(token))
            assert status == 501, command_id
            assert body["command"] == command_id

    def test_unexposed_catalog_command_is_400_on_field_command(self):
        """`job.list` is a real catalog id that the write door does not expose."""
        from apps.cli.command_catalog import get_command

        assert get_command(UNEXPOSED_CATALOG_COMMAND).command_id == (
            UNEXPOSED_CATALOG_COMMAND)
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=UNEXPOSED_CATALOG_COMMAND),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "command"
        assert "error" in body

    def test_command_in_no_catalog_is_400_on_field_command(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=UNKNOWN_COMMAND),
            headers=self._auth_headers(token))
        assert status == 400
        assert body["field"] == "command"
        assert "error" in body

    def test_the_two_refusals_are_indistinguishable(self):
        """D12's non-disclosure, as a tested property rather than a comment.

        A caller must not be able to tell a catalog id it may not use from a
        string that names no command at all, or the write door becomes a way
        to enumerate the CLI surface.
        """
        port, token = self._start_server()
        catalog_status, catalog_body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=UNEXPOSED_CATALOG_COMMAND),
            headers=self._auth_headers(token))
        unknown_status, unknown_body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=UNKNOWN_COMMAND),
            headers=self._auth_headers(token))
        assert (catalog_status, catalog_body) == (unknown_status, unknown_body)

    def test_unexposed_command_with_a_bad_bearer_is_403_and_never_400(self):
        """The subset is policy, so it is decided after the credentials."""
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=UNEXPOSED_CATALOG_COMMAND),
            headers=self._auth_headers(token, bearer="Bearer not-the-token"))
        assert status == 403
        assert body["error"] == "invalid token"
        assert "field" not in body

    def test_unexposed_command_on_an_unresolvable_job_is_404(self):
        """And after the job, for the same reason."""
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(job_id=str(uuid4())),
            body=self._valid_body(command=UNEXPOSED_CATALOG_COMMAND),
            headers=self._auth_headers(token))
        assert status == 404
        assert body["error"] == "job not found"

    def test_empty_command_is_still_a_shape_error_not_a_subset_error(self):
        """Shape is decided before the subset, so the field message is D.4's."""
        port, token = self._start_server()
        shape_status, shape_body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=""),
            headers=self._auth_headers(token))
        subset_status, subset_body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=UNKNOWN_COMMAND),
            headers=self._auth_headers(token))
        assert shape_status == subset_status == 400
        assert shape_body["field"] == subset_body["field"] == "command"
        assert shape_body["error"] != subset_body["error"]

    # -- D.7: the rate limit (DECISION F009 D9 and D13) ---------------------

    def _post_command(self, port, token, nonce, **overrides):
        """One fully credentialed command submission, valid unless overridden."""
        return self._request(
            port, "POST", self._commands_path(overrides.pop("job_id", None)),
            body=self._valid_body(client_nonce=nonce, **overrides),
            headers=self._auth_headers(token))

    def test_the_last_command_in_budget_is_accepted_and_the_next_is_429(
            self, command_rate_limit):
        limit = command_rate_limit(3)
        port, token = self._start_server()
        for index in range(limit):
            status, _ = self._post_command(port, token, f"nonce-in-{index}")
            assert status == 501, index
        status, body = self._post_command(port, token, "nonce-over")
        assert status == 429
        assert body["error"] == "too many commands for this job"
        assert "field" not in body

    def test_a_second_job_has_its_own_budget(self, command_rate_limit):
        """The key is the PAIR, so exhausting one job leaves the other alone."""
        from packages.orchestration.storage import save_job
        limit = command_rate_limit(2)
        other = _make_job()
        save_job(other)
        port, token = self._start_server()
        for index in range(limit):
            assert self._post_command(port, token, f"nonce-a-{index}")[0] == 501
        assert self._post_command(port, token, "nonce-a-over")[0] == 429
        status, _ = self._post_command(
            port, token, "nonce-b-0", job_id=str(other.id))
        assert status == 501

    def test_a_shape_error_does_not_spend_budget(self, command_rate_limit):
        """DECISION F009 D13, from the outside: a 400 costs the client nothing."""
        limit = command_rate_limit(1)
        port, token = self._start_server()
        for _ in range(limit + 3):
            status, _ = self._request(
                port, "POST", self._commands_path(), body="{not json",
                headers=self._auth_headers(token))
            assert status == 400
        assert self._post_command(port, token, "nonce-after-shape")[0] == 501
        assert self._post_command(port, token, "nonce-spent")[0] == 429

    def test_an_unexposed_command_does_not_spend_budget(self, command_rate_limit):
        """The same property for the subset check, which is decided just before."""
        limit = command_rate_limit(1)
        port, token = self._start_server()
        for _ in range(limit + 3):
            status, _ = self._post_command(
                port, token, "nonce-unexposed", command=UNEXPOSED_CATALOG_COMMAND)
            assert status == 400
        assert self._post_command(port, token, "nonce-after-subset")[0] == 501
        assert self._post_command(port, token, "nonce-spent")[0] == 429

    def test_a_mistyped_limit_falls_back_to_the_default_and_still_limits(
            self, command_rate_limit, monkeypatch):
        """A typo in configuration must not turn every command into a 500."""
        from packages.orchestration.config import get_config, reset_config
        command_rate_limit(3)
        monkeypatch.setenv("REMEDY_UI_COMMAND_RATE_LIMIT_PER_MINUTE", "lots")
        reset_config()
        assert get_config().get("ui.command_rate_limit_per_minute") == "lots"
        port, token = self._start_server()
        assert self._post_command(port, token, "nonce-typo")[0] == 501

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


class TestUiExposedCommands:
    """The exposed subset itself — DECISION F009 D4."""

    def test_the_set_holds_exactly_the_two_ruled_ids(self):
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS
        assert sorted(UI_EXPOSED_COMMANDS) == ["decision.resolve", "job.stop"]

    def test_the_set_is_a_frozenset(self):
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS
        assert isinstance(UI_EXPOSED_COMMANDS, frozenset)

    def test_every_member_resolves_through_get_command(self):
        """The set cannot drift from the catalog it names."""
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS, get_command
        for command_id in sorted(UI_EXPOSED_COMMANDS):
            assert get_command(command_id).command_id == command_id

    def test_the_chosen_unexposed_catalog_command_is_really_both(self):
        """Guards the fixtures the door tests above are built on."""
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS, get_command
        assert get_command(UNEXPOSED_CATALOG_COMMAND)
        assert UNEXPOSED_CATALOG_COMMAND not in UI_EXPOSED_COMMANDS
        with pytest.raises(KeyError):
            get_command(UNKNOWN_COMMAND)


class TestCommandRateLimitConfigKey:
    """DECISION F009 D9's typed key, read by importing it rather than grepping."""

    def test_the_key_resolves_through_get_config(self, monkeypatch):
        from packages.orchestration.config import get_config, reset_config
        monkeypatch.delenv("REMEDY_UI_COMMAND_RATE_LIMIT_PER_MINUTE", raising=False)
        reset_config()
        try:
            assert get_config().get("ui.command_rate_limit_per_minute") == 30
        finally:
            reset_config()

    def test_the_spec_is_a_typed_int_key_with_the_conventional_env_var(self):
        from packages.orchestration.config import get_key_spec
        spec = get_key_spec("ui.command_rate_limit_per_minute")
        assert spec is not None
        assert spec.env_var == "REMEDY_UI_COMMAND_RATE_LIMIT_PER_MINUTE"
        assert spec.value_type is int
        assert spec.default == 30
        assert "F009 D9" in spec.description

    def test_the_door_reads_the_limit_from_that_key(self):
        """The name is shared, so the door and the registry cannot drift apart."""
        from packages.orchestration.ui_server import COMMAND_RATE_LIMIT_CONFIG_KEY
        assert COMMAND_RATE_LIMIT_CONFIG_KEY == "ui.command_rate_limit_per_minute"


class TestTokenFingerprint:
    """DECISION F009 D7's fingerprint, introduced where it is first used."""

    def test_the_fingerprint_never_contains_the_raw_token(self):
        from packages.orchestration.ui_server import token_fingerprint
        token = "s3cret-token-value-do-not-leak"
        assert token not in token_fingerprint(token)

    def test_the_fingerprint_is_a_prefixed_truncated_sha256(self):
        import hashlib

        from packages.orchestration.ui_server import token_fingerprint
        token = "s3cret-token-value-do-not-leak"
        expected = hashlib.sha256(token.encode("utf-8")).hexdigest()[:16]
        assert token_fingerprint(token) == "tf:" + expected

    def test_different_tokens_get_different_fingerprints(self):
        from packages.orchestration.ui_server import token_fingerprint
        assert token_fingerprint("token-a") != token_fingerprint("token-b")

    def test_a_missing_token_does_not_raise(self):
        from packages.orchestration.ui_server import token_fingerprint
        assert token_fingerprint(None).startswith("tf:")


class TestCommandRateLimiter:
    """The limiter itself, driven by an injected clock instead of a wait."""

    def _fingerprint(self) -> str:
        """A fingerprint no other test in this process can collide with.

        The limiter's window map is module-level state in a long-lived server,
        so a test that reused a fingerprint would inherit another test's spent
        budget when the whole file runs in one pytest process.
        """
        from packages.orchestration.ui_server import token_fingerprint
        return token_fingerprint(f"token-{uuid4()}")

    def test_the_budget_is_per_fingerprint(self):
        from packages.orchestration.ui_server import accept_command_under_rate_limit
        job = str(uuid4())
        spent, fresh = self._fingerprint(), self._fingerprint()
        assert accept_command_under_rate_limit(spent, job, 1) is True
        assert accept_command_under_rate_limit(spent, job, 1) is False
        assert accept_command_under_rate_limit(fresh, job, 1) is True

    def test_the_budget_is_per_job(self):
        from packages.orchestration.ui_server import accept_command_under_rate_limit
        fingerprint = self._fingerprint()
        spent, fresh = str(uuid4()), str(uuid4())
        assert accept_command_under_rate_limit(fingerprint, spent, 1) is True
        assert accept_command_under_rate_limit(fingerprint, spent, 1) is False
        assert accept_command_under_rate_limit(fingerprint, fresh, 1) is True

    def test_the_window_rolls_on_the_injected_clock(self):
        from packages.orchestration.ui_server import (
            COMMAND_RATE_WINDOW_SECONDS,
            accept_command_under_rate_limit,
        )
        clock = [1000.0]
        fingerprint, job = self._fingerprint(), str(uuid4())

        def now():
            return clock[0]

        assert accept_command_under_rate_limit(fingerprint, job, 2, now=now) is True
        assert accept_command_under_rate_limit(fingerprint, job, 2, now=now) is True
        assert accept_command_under_rate_limit(fingerprint, job, 2, now=now) is False
        clock[0] += COMMAND_RATE_WINDOW_SECONDS - 0.5
        assert accept_command_under_rate_limit(fingerprint, job, 2, now=now) is False
        clock[0] += 0.5
        assert accept_command_under_rate_limit(fingerprint, job, 2, now=now) is True

    def test_an_expired_window_is_dropped_from_the_map(self):
        """Contract D: the map holds a live working set, not a growing history."""
        from packages.orchestration.ui_server import (
            _COMMAND_RATE_WINDOWS,
            COMMAND_RATE_WINDOW_SECONDS,
            accept_command_under_rate_limit,
        )
        clock = [2000.0]
        stale, later = self._fingerprint(), self._fingerprint()
        job = str(uuid4())

        def now():
            return clock[0]

        accept_command_under_rate_limit(stale, job, 5, now=now)
        assert (stale, job) in _COMMAND_RATE_WINDOWS
        clock[0] += COMMAND_RATE_WINDOW_SECONDS
        accept_command_under_rate_limit(later, job, 5, now=now)
        assert (stale, job) not in _COMMAND_RATE_WINDOWS
        assert (later, job) in _COMMAND_RATE_WINDOWS

    def test_concurrent_callers_never_oversubscribe_one_budget(self):
        """The lock is the point: two threads must not both take the last unit."""
        from packages.orchestration.ui_server import accept_command_under_rate_limit
        fingerprint, job = self._fingerprint(), str(uuid4())
        limit = 20
        accepted = []
        lock = threading.Lock()
        start = threading.Barrier(8)

        def submit():
            start.wait()
            for _ in range(10):
                if accept_command_under_rate_limit(fingerprint, job, limit):
                    with lock:
                        accepted.append(1)

        threads = [threading.Thread(target=submit) for _ in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
        assert len(accepted) == limit


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
