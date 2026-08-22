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

    def test_well_formed_command_is_dispatched_and_accepted(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token))
        assert status == 200
        assert body["outcome"] == "accepted"
        assert body["command"] == "job.stop"

    def test_absent_args_is_valid_and_reaches_the_effect(self):
        """Absent `args` is a SHAPE success: it reaches the effect, which declines.

        DECISION F009 D21: no `decision_id` names no answerable decision, so the
        effect RUNS and REFUSES, which is 409 and `rejected_state` — not the 400
        a shape error would give and not the 501 this pin asserted while the
        dispatch was a placeholder.
        """
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=json.dumps({"command": "decision.resolve", "client_nonce": "n-2"}),
            headers=self._auth_headers(token))
        assert status == 409, body
        assert body["error"] == "decision is not open", body
        assert self._audit_records()[-1]["outcome"] == "rejected_state"

    def test_present_args_object_is_valid_and_is_accepted(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(args={"reason": "operator asked"}),
            headers=self._auth_headers(token))
        assert status == 200
        assert body["command"] == "job.stop"

    # -- D.6: the UI-exposed subset (DECISION F009 D4 and D12) --------------

    def test_every_exposed_command_reaches_the_answer_its_effect_gives(self):
        """The set itself is the contract, not the two literals above.

        BOTH exposed ids now dispatch. `job.stop` answers 200. A
        `decision.resolve` built by `_valid_body` carries no `args`, so it names
        no answerable decision and its effect RUNS and DECLINES: DECISION F009
        D21's 409, whose body carries `error` and not `command` because every
        refusal on this door goes out through the same safe-error shape.
        """
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

        port, token = self._start_server()
        for index, command_id in enumerate(sorted(UI_EXPOSED_COMMANDS)):
            status, body = self._request(
                port, "POST", self._commands_path(),
                body=self._valid_body(
                    command=command_id, client_nonce=f"nonce-exposed-{index}"),
                headers=self._auth_headers(token))
            if command_id == "job.stop":
                assert status == 200, command_id
                assert body["command"] == command_id
            else:
                assert status == 409, command_id
                assert body["error"] == "decision is not open", command_id

    def test_a_decision_resolve_naming_an_open_decision_is_answered_and_saved(self):
        """DECISION F009 D21's success path, read back off disk.

        The two writes D21 rules to be ONE effect are both checked: the record is
        `answered` in memory only if `answer_task_decision` ran, and it is that
        way in a job RELOADED from storage only if `save_job` ran too. The
        `answer_source` assertion is DECISION F009 D22 made testable — `human`,
        never this door's own name, because the escalation assumption log counts
        that field into exactly two buckets and "ui" is in neither.
        """
        from datetime import datetime, timezone

        from packages.orchestration.command_nonce import lookup_nonce_result
        from packages.orchestration.escalation import (
            enqueue_task_decision,
            find_task_decision,
        )
        from packages.orchestration.storage import load_job, save_job

        record = enqueue_task_decision(
            self.job, task_id=self.job.tasks[0].id,
            question="Which database should the task use?",
            now=datetime.now(timezone.utc))
        save_job(self.job)
        decision_id = record["decision_id"]

        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(
                command="decision.resolve", client_nonce="nonce-resolve",
                args={"decision_id": decision_id, "answer": "postgres"}),
            headers=self._auth_headers(token))

        assert status == 200, body
        assert body["outcome"] == "accepted", body
        assert body["decision_id"] == decision_id, body
        answered = find_task_decision(load_job(self.job.id), decision_id)
        assert answered["status"] == "answered", answered
        assert answered["answer"] == "postgres", answered
        assert answered["answer_source"] == "human", answered
        assert self._audit_records()[-1]["outcome"] == "accepted"
        # D18's third write. With the effect and the audit line above, all three
        # writes D18 orders for an ACCEPTED command are now asserted for
        # `decision.resolve`, as they already were for `job.stop`.
        assert lookup_nonce_result(
            self.job_id, "nonce-resolve",
            control_root_path=self.tmp_path / "control") == {"status": 200,
                                                             "body": body}

    def test_an_exposed_id_with_no_dispatch_branch_is_the_501_guard(self, monkeypatch):
        """DECISION F009 D22's guard, and the only test that reaches it.

        Reachable only by exposing an id this door does not dispatch, which is
        exactly the mistake the guard exists to catch: without it such a request
        falls off the end of the handler with no response written at all.
        """
        from apps.cli import command_catalog

        monkeypatch.setattr(
            command_catalog, "UI_EXPOSED_COMMANDS",
            frozenset(["job.stop", "decision.resolve", UNEXPOSED_CATALOG_COMMAND]))
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(
                command=UNEXPOSED_CATALOG_COMMAND, client_nonce="nonce-guard"),
            headers=self._auth_headers(token))
        assert status == 501, body
        # The MESSAGE is what tells the guard apart from the placeholder it
        # replaced: the deleted seam answered 501 for this request too, so a test
        # that pinned only the status would pass against either door.
        assert body["error"] == "command is exposed but not dispatched", body
        assert "command" not in body, body
        assert self._audit_records()[-1]["outcome"] == "not_implemented"

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
            assert status == 200, index
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
            assert self._post_command(port, token, f"nonce-a-{index}")[0] == 200
        assert self._post_command(port, token, "nonce-a-over")[0] == 429
        status, _ = self._post_command(
            port, token, "nonce-b-0", job_id=str(other.id))
        assert status == 200

    def test_a_shape_error_does_not_spend_budget(self, command_rate_limit):
        """DECISION F009 D13, from the outside: a 400 costs the client nothing."""
        limit = command_rate_limit(1)
        port, token = self._start_server()
        for _ in range(limit + 3):
            status, _ = self._request(
                port, "POST", self._commands_path(), body="{not json",
                headers=self._auth_headers(token))
            assert status == 400
        assert self._post_command(port, token, "nonce-after-shape")[0] == 200
        assert self._post_command(port, token, "nonce-spent")[0] == 429

    def test_an_unexposed_command_does_not_spend_budget(self, command_rate_limit):
        """The same property for the subset check, which is decided just before."""
        limit = command_rate_limit(1)
        port, token = self._start_server()
        for _ in range(limit + 3):
            status, _ = self._post_command(
                port, token, "nonce-unexposed", command=UNEXPOSED_CATALOG_COMMAND)
            assert status == 400
        assert self._post_command(port, token, "nonce-after-subset")[0] == 200
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
        assert self._post_command(port, token, "nonce-typo")[0] == 200

    # -- D.8: every attempt is audited (DECISION F009 D6 and D14) -----------

    def _audit_path(self, job_id=None) -> Path:
        from packages.orchestration.command_audit import AUDIT_FILENAME
        return (self.tmp_path / "control" / "jobs"
                / (job_id or self.job_id) / AUDIT_FILENAME)

    def _audit_records(self, job_id=None) -> list[dict]:
        path = self._audit_path(job_id)
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_bytes().splitlines()]

    def _seed_control_dir(self, port, token) -> None:
        """One credentialed attempt, so the job's control directory exists.

        DECISION F009 D14 audits a pre-credential refusal only into a directory that is
        ALREADY there, so a test about such a refusal has to establish one first — and it
        has to do it the way production does, through the door.
        """
        assert self._post_command(port, token, "nonce-seed")[0] == 200
        assert self._audit_path().exists()

    def test_a_dispatched_command_is_audited_as_accepted(self):
        port, token = self._start_server()
        assert self._post_command(port, token, "nonce-seam")[0] == 200

        records = self._audit_records()
        assert len(records) == 1
        assert records[0]["outcome"] == "accepted"
        assert records[0]["command"] == "job.stop"
        assert records[0]["nonce"] == "nonce-seam"

    def test_a_wrong_bearer_is_audited_as_rejected_token(self):
        port, token = self._start_server()
        self._seed_control_dir(port, token)

        status, _ = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, bearer="Bearer not-the-token"))

        assert status == 403
        assert [r["outcome"] for r in self._audit_records()] == [
            "accepted", "rejected_token"]

    def test_a_wrong_csrf_header_is_audited_as_rejected_csrf(self):
        port, token = self._start_server()
        self._seed_control_dir(port, token)

        status, _ = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, csrf="not-the-token"))

        assert status == 403
        assert [r["outcome"] for r in self._audit_records()][-1] == "rejected_csrf"

    def test_an_unresolvable_job_is_audited_as_rejected_job(self):
        port, token = self._start_server()
        other = str(uuid4())

        status, _ = self._request(
            port, "POST", self._commands_path(job_id=other),
            body=self._valid_body(), headers=self._auth_headers(token))

        assert status == 404
        records = self._audit_records(other)
        assert [r["outcome"] for r in records] == ["rejected_job"]
        assert self._audit_records() == [], "the record belongs to the job that was asked for"

    def test_a_shape_error_is_audited_as_rejected_shape(self):
        port, token = self._start_server()

        status, _ = self._request(
            port, "POST", self._commands_path(), body="{not json",
            headers=self._auth_headers(token))

        assert status == 400
        records = self._audit_records()
        assert [r["outcome"] for r in records] == ["rejected_shape"]
        # The body never parsed, so there is no command to name — and none is invented.
        assert records[0]["command"] == ""
        assert records[0]["nonce"] == ""

    def test_an_unexposed_command_is_audited_as_rejected_command(self):
        port, token = self._start_server()

        status, _ = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command=UNEXPOSED_CATALOG_COMMAND),
            headers=self._auth_headers(token))

        assert status == 400
        records = self._audit_records()
        assert [r["outcome"] for r in records] == ["rejected_command"]
        assert records[0]["command"] == UNEXPOSED_CATALOG_COMMAND

    def test_a_rate_limited_attempt_is_audited_as_rejected_rate(self, command_rate_limit):
        limit = command_rate_limit(1)
        port, token = self._start_server()
        for index in range(limit):
            assert self._post_command(port, token, f"nonce-{index}")[0] == 200

        status, _ = self._post_command(port, token, "nonce-over")

        assert status == 429
        records = self._audit_records()
        assert [r["outcome"] for r in records] == ["accepted", "rejected_rate"]
        assert records[-1]["command"] == "job.stop"
        assert records[-1]["nonce"] == "nonce-over"

    def test_every_outcome_the_door_writes_is_in_the_ruled_vocabulary(
            self, command_rate_limit):
        """One walk of every refusal, held against DECISION F009 D14's closed set."""
        from packages.orchestration.command_audit import OUTCOMES
        limit = command_rate_limit(2)
        port, token = self._start_server()
        assert self._post_command(port, token, "nonce-seam")[0] == 200
        self._request(port, "POST", self._commands_path(), body=self._valid_body(),
                      headers=self._auth_headers(token, bearer="Bearer wrong"))
        self._request(port, "POST", self._commands_path(), body=self._valid_body(),
                      headers=self._auth_headers(token, csrf="wrong"))
        self._request(port, "POST", self._commands_path(), body="{not json",
                      headers=self._auth_headers(token))
        self._post_command(port, token, "n", command=UNEXPOSED_CATALOG_COMMAND)
        for index in range(limit + 1):
            self._post_command(port, token, f"nonce-burn-{index}")

        outcomes = [r["outcome"] for r in self._audit_records()]
        assert set(outcomes) <= set(OUTCOMES), sorted(set(outcomes) - set(OUTCOMES))
        assert "accepted" in outcomes, "the dispatched job.stop was never accepted"
        assert set(outcomes) == {
            "accepted", "rejected_token", "rejected_csrf", "rejected_shape",
            "rejected_command", "rejected_rate"}

    def test_a_wrong_credential_on_a_job_with_no_control_dir_leaves_no_file(self):
        """D14's stated cost, pinned: no directory means no record, and still a 403."""
        port, token = self._start_server()
        assert not self._audit_path().exists()
        assert not (self.tmp_path / "control").exists()

        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token, bearer="Bearer not-the-token"))

        assert status == 403
        assert body["error"] == "invalid token"
        assert not (self.tmp_path / "control").exists(), (
            "an unauthenticated caller created a control directory")

    def test_the_raw_token_never_reaches_the_audit_file(self):
        port, token = self._start_server()
        self._seed_control_dir(port, token)

        self._request(port, "POST", self._commands_path(), body=self._valid_body(),
                      headers=self._auth_headers(token, bearer="Bearer not-the-token"))

        written = self._audit_path().read_bytes()
        assert token.encode() not in written
        assert b"not-the-token" not in written
        assert len(self._audit_records()) == 2, "the rejected attempt WAS recorded"

    def test_an_audit_writer_that_raises_changes_neither_status_nor_body(
            self, monkeypatch):
        """DECISION F009 D14, clause four: a full disk must not turn a 403 into a 500."""
        port, token = self._start_server()
        without = {}
        for label, headers in (
                ("token", self._auth_headers(token, bearer="Bearer wrong")),
                ("csrf", self._auth_headers(token, csrf="wrong")),
                ("seam", self._auth_headers(token))):
            without[label] = self._request(
                port, "POST", self._commands_path(), body=self._valid_body(),
                headers=headers)

        from packages.orchestration import command_audit
        from packages.orchestration.safe_points import StopControlError

        calls = []
        # One per call site below, so the whole caught set is exercised, not just OSError:
        # a full disk, a containment refusal and an unserialisable payload alike.
        failures = [OSError("no space left on device"),
                    StopControlError("stop-control containment could not be guaranteed"),
                    TypeError("object is not JSON serializable")]

        def explode(*_args, **kwargs):
            calls.append(kwargs.get("outcome"))
            raise failures[len(calls) - 1]

        monkeypatch.setattr(command_audit, "audit_command_attempt", explode)
        records_before = len(self._audit_records())

        with_raise = {}
        for label, headers in (
                ("token", self._auth_headers(token, bearer="Bearer wrong")),
                ("csrf", self._auth_headers(token, csrf="wrong")),
                ("seam", self._auth_headers(token))):
            with_raise[label] = self._request(
                port, "POST", self._commands_path(), body=self._valid_body(),
                headers=headers)

        # The mutation must REACH the door, or the comparison above proves nothing.
        # The third call is a REPLAY, not an acceptance: both loops submit the same
        # default nonce, so the first loop published it and the second one hits it.
        assert calls == ["rejected_token", "rejected_csrf", "replayed"], calls
        assert len(self._audit_records()) == records_before, (
            "the raising writer still wrote a record")
        assert with_raise == without, f"the raising writer changed a response: {with_raise}"
        assert without["token"][0] == 403
        assert without["seam"][0] == 200

    # -- D.9: the replayed nonce (DECISION F009 D8 and D15) -----------------

    def _seed_nonce(self, nonce, body, status):
        """Publish one result under `nonce`, the way the door itself will after T003.

        The door publishes for itself from R19 onward, but only for the ids it
        dispatches. This helper seeds a result directly so that a replay test can
        name the stored body it expects, byte for byte, instead of depending on
        whatever the effect of the moment happens to return.
        """
        from packages.orchestration.command_nonce import publish_nonce_result
        published = publish_nonce_result(
            self.job_id, nonce, body, status=status,
            control_root_path=self.tmp_path / "control")
        assert published == {"status": status, "body": body}
        return published

    def _raw_request(self, port, path, body, headers):
        """One POST whose response BYTES are returned unparsed, for a byte comparison."""
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request("POST", path, body=body, headers=headers)
            resp = conn.getresponse()
            return resp.status, resp.read()
        finally:
            conn.close()

    def test_a_replayed_nonce_answers_from_the_store_byte_for_byte(self):
        """D8's contract on the wire: the SAME answer, not merely an equivalent one."""
        stored = {"effect": "already-run", "command": "job.stop", "run_id": "r-7"}
        self._seed_nonce("nonce-replayed", stored, 200)
        port, token = self._start_server()

        status, raw = self._raw_request(
            port, self._commands_path(),
            self._valid_body(client_nonce="nonce-replayed"),
            self._auth_headers(token))

        assert status == 200
        assert raw == json.dumps(stored).encode()

    def test_an_unseeded_nonce_is_dispatched_rather_than_replayed(self):
        """The lookup must MISS by default, or the door would answer from an empty store."""
        port, token = self._start_server()
        status, body = self._post_command(port, token, "nonce-unseeded")
        assert status == 200
        assert body["outcome"] == "accepted"

    def test_a_replay_is_not_the_acceptance_it_repeats(self):
        """Proved by the response: the seam's own answer is not what a replay returns."""
        stored = {"effect": "already-run", "command": "job.stop"}
        self._seed_nonce("nonce-not-the-seam", stored, 200)
        port, token = self._start_server()

        seam = self._post_command(port, token, "nonce-fresh")
        replay = self._post_command(port, token, "nonce-not-the-seam")

        assert seam[0] == 200
        assert seam[1]["outcome"] == "accepted"
        assert seam[1]["command"] == "job.stop"
        assert replay == (200, stored)
        assert replay != seam

    def test_a_replay_spends_no_rate_budget(self, command_rate_limit):
        """DECISION F009 D15: a replay accepts nothing new, so it is charged nothing.

        The budget is counted from the OUTSIDE afterwards — the replays are only free if
        the full minute budget is still there to be exhausted once they are done.
        """
        limit = command_rate_limit(2)
        self._seed_nonce("nonce-free", {"effect": "already-run"}, 200)
        port, token = self._start_server()

        for _ in range(limit + 4):
            assert self._post_command(port, token, "nonce-free")[0] == 200

        accepted = 0
        for index in range(limit + 2):
            status, _ = self._post_command(port, token, f"nonce-spend-{index}")
            if status == 200:
                accepted += 1
            else:
                assert status == 429, index
        assert accepted == limit, "the replays spent budget the client never used"

    @pytest.mark.parametrize("nonce", ["../escape", "with/slash", "has space", "a" * 65])
    def test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field(self, nonce):
        """It becomes a path component, so the character class is a SHAPE error."""
        port, token = self._start_server()

        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(client_nonce=nonce),
            headers=self._auth_headers(token))

        assert status == 400
        assert body["field"] == "client_nonce"
        assert [r["outcome"] for r in self._audit_records()] == ["rejected_shape"]
        assert not (self.tmp_path / "control" / "jobs" / self.job_id
                    / "commands_nonce").exists()

    # -- E: an accepted command announces itself (DECISION F009 D23) --------

    def _run_events(self):
        """Every run-log event for this job, read the way the stream reads them."""
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events
        return load_run_events(resolve_data_root(), self.job_id)

    def _accepted_events(self):
        from packages.orchestration.ui_server import COMMAND_ACCEPTED_EVENT
        return [e for e in self._run_events()
                if e.get("event") == COMMAND_ACCEPTED_EVENT]

    def test_an_accepted_command_reaches_the_sse_frame_it_announces(self):
        """The ledger event AND the frame the stream builds out of it.

        `_safe_event_summary` is the one writer both event transports share, so
        a field it drops never reaches a client however faithfully the ledger
        recorded it. `outcome` survives only because `RunLogWriter.log` takes it
        as a NAMED parameter: the same value passed as plain metadata would sit
        one level down and arrive on the wire as the empty string.
        """
        from packages.orchestration.ui_server import (
            COMMAND_ACCEPTED_EVENT,
            _safe_event_summary,
            sse_event_frame,
        )

        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(client_nonce="nonce-sse-accept"),
            headers=self._auth_headers(token))
        assert status == 200, body

        events = self._run_events()
        matches = [(seq, e) for seq, e in enumerate(events)
                   if e.get("event") == COMMAND_ACCEPTED_EVENT]
        assert len(matches) == 1, events
        seq, event = matches[0]
        assert event["outcome"] == "accepted", event
        assert event["metadata"]["command"] == "job.stop", event

        frame = sse_event_frame(seq, _safe_event_summary(seq, event))
        payload = json.loads(frame.decode().split("data: ", 1)[1])
        assert payload["event"] == COMMAND_ACCEPTED_EVENT, payload
        assert payload["outcome"] == "accepted", payload
        assert payload["seq"] == seq, payload
        # The args never reach the stream: the safe summary is a fixed envelope,
        # and D6 keeps this door's own attribution in the audit file.
        assert "command" not in payload, payload

    def test_a_refused_command_announces_nothing(self):
        """The discriminator. A `decision.resolve` with no args is D21's 409.

        Its effect RAN and DECLINED, so the door leaves on a refusal path this
        round must keep silent — without this test the emission could sit on
        every exit of the handler and still look correct.
        """
        port, token = self._start_server()
        status, _ = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command="decision.resolve",
                                  client_nonce="nonce-sse-refused"),
            headers=self._auth_headers(token))
        assert status == 409
        assert self._accepted_events() == []

    def test_a_replay_announces_nothing_a_second_time(self):
        """A replay REPEATS an acceptance rather than being one (R-0636's rule).

        The UI would otherwise see two frames for one effect and count a retry
        after a timeout as a second write.
        """
        port, token = self._start_server()
        for _ in range(2):
            status, _ = self._request(
                port, "POST", self._commands_path(),
                body=self._valid_body(client_nonce="nonce-sse-replay"),
                headers=self._auth_headers(token))
            assert status == 200
        assert len(self._accepted_events()) == 1

    def test_an_event_writer_that_raises_changes_neither_status_nor_body(
            self, monkeypatch):
        """DECISION F009 D23 clause two, proved rather than asserted.

        The effect is already durable when this write runs, so a full disk must
        not turn an accepted command into a 500 reporting it as refused.
        """
        from packages.orchestration import timeline

        calls = []

        def _raise_no_space(*_args, **_kwargs):
            calls.append(1)
            raise OSError("no space left on device")

        monkeypatch.setattr(timeline, "append_run_event", _raise_no_space)
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(client_nonce="nonce-sse-raises"),
            headers=self._auth_headers(token))
        assert status == 200, body
        assert body["outcome"] == "accepted", body
        # The counter is what makes this a test of the SOFT FAILURE rather than
        # of a door that never emits: a handler with no call site at all would
        # satisfy every line above it.
        assert calls == [1], calls
        assert self._accepted_events() == []

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

    #: How long a thread waits for a flag it expects, or for one it expects NOT to see.
    #: A second is six orders of magnitude more than an unlocked entry needs — a caller
    #: that is not excluded reaches the critical section in microseconds — so the gap
    #: between "excluded" and "not excluded" is not a race this value could decide wrongly.
    MUTEX_WAIT_SECONDS = 1.0

    def test_the_lock_actually_excludes_a_second_caller(self):
        """Mutual exclusion OBSERVED, through the `now` injection the function already has.

        Finding R-0634: the eight-thread test below names this lock and cannot detect it —
        with `_COMMAND_RATE_LOCK` removed it stayed green ten times out of ten, because
        nothing in it ever holds the critical section long enough for a second thread to
        collide. This test makes the injected clock the suspension point instead: `now()`
        is called INSIDE the critical section, so a `now` that blocks there holds the lock
        while a second thread tries to enter. No production hook is added for it.
        """
        from packages.orchestration.ui_server import accept_command_under_rate_limit
        fingerprint, job = self._fingerprint(), str(uuid4())
        a_inside = threading.Event()
        b_attempting = threading.Event()
        b_entered = threading.Event()
        seen: dict[str, bool] = {}

        def now_a() -> float:
            # Called with the lock HELD. Everything below happens inside it.
            a_inside.set()
            seen["b_attempted"] = b_attempting.wait(self.MUTEX_WAIT_SECONDS)
            seen["b_entered_while_a_held"] = b_entered.wait(self.MUTEX_WAIT_SECONDS)
            return 5000.0

        def now_b() -> float:
            b_entered.set()
            return 5000.0

        def call_b() -> None:
            b_attempting.set()
            accept_command_under_rate_limit(fingerprint, job, 5, now=now_b)

        thread_a = threading.Thread(
            target=accept_command_under_rate_limit,
            args=(fingerprint, job, 5), kwargs={"now": now_a})
        thread_a.start()
        assert a_inside.wait(10), "thread A never reached the critical section"
        thread_b = threading.Thread(target=call_b)
        thread_b.start()
        thread_a.join(timeout=10)
        thread_b.join(timeout=10)

        assert seen.get("b_attempted") is True, (
            "thread B never attempted entry, so this test proved nothing")
        assert seen.get("b_entered_while_a_held") is False, (
            "thread B entered the critical section while thread A held it — no exclusion")
        assert b_entered.wait(10), (
            "thread B never entered at all, even after A released — the run was degenerate")
        assert not thread_a.is_alive() and not thread_b.is_alive()

    def test_concurrent_callers_never_oversubscribe_one_budget(self):
        """A smoke check on the AGGREGATE: eighty attempts against a budget of twenty.

        It does not observe the lock — see `test_the_lock_actually_excludes_a_second_caller`
        for that (finding R-0634). What it does cover is the arithmetic under real
        concurrency: the accepted total is exactly the budget, never more and never fewer.
        """
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
