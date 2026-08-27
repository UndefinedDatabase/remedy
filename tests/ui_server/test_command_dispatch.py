"""
Domain tests: ui_server/test_command_dispatch.py

Effect tests for F009 T003 — what an ACCEPTED command actually DID. Its sibling
`test_command_channel.py` pins what the door ANSWERS; this file pins the three
writes DECISION F009 D18 orders behind that answer: the effect, the `accepted`
audit line and the nonce publication. Remedy deliberately keeps the two files
apart — a status can be right while the effect never ran, and only a test that
reads the job's control directory can tell those two cases apart.
"""

from __future__ import annotations

import json
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.core.models import Job, Task

# Pinned as a literal for the reason its sibling gives: a test that imports the
# constant it checks cannot catch a rename of the header the browser must send.
CSRF_HEADER = "X-Remedy-CSRF"


def _make_job() -> Job:
    return Job(
        name="test-command-dispatch-job",
        user_prompt="Test prompt for the command dispatch effects",
        tasks=[Task(type="write_readme", description="Write a README")],
    )


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Start a real UI server for `job_id` in a thread and return `(port, token)`.

    Module-level because both dispatch-effect classes below need it identically
    (finding R-0701). Two copies of a server-start helper drift, and the failure
    mode is quiet: a timeout raised in one copy makes one class flaky on a slow
    runner while its sibling stays green, and the divergence reads as an
    environment problem rather than as a duplicate.
    """
    import secrets

    from packages.orchestration.ui_server import start_ui_server

    info_file = str(tmp_path / "server_info.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    threading.Thread(target=run, daemon=True).start()
    for _ in range(50):
        if Path(info_file).exists():
            return json.loads(Path(info_file).read_text())["port"], token
        time.sleep(0.1)
    pytest.fail("Server did not start in time")


class TestJobStopDispatchEffects:
    """Integration tests that start a real server and then read what it wrote."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        self.job = _make_job()
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path
        self.control = tmp_path / "control"

    def _post(self, port, token, nonce, **overrides):
        """One fully credentialed `job.stop` submission, valid unless overridden."""
        payload = {"command": "job.stop", "client_nonce": nonce}
        payload.update(overrides)
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request("POST", f"/api/jobs/{self.job_id}/commands",
                         body=json.dumps(payload),
                         headers={"Authorization": f"Bearer {token}",
                                  CSRF_HEADER: token,
                                  "Content-Type": "application/json"})
            resp = conn.getresponse()
            return resp.status, json.loads(resp.read())
        finally:
            conn.close()

    def _audit_outcomes(self):
        from packages.orchestration.command_audit import AUDIT_FILENAME
        path = self.control / "jobs" / self.job_id / AUDIT_FILENAME
        return [json.loads(line)["outcome"] for line in path.read_bytes().splitlines()]

    def test_the_dispatch_publishes_the_stop_request_the_body_names(self):
        """D5's effect really ran: the request_id on the wire is the one on disk."""
        from packages.orchestration import safe_points

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-effect",
                                  args={"reason": "operator asked"})

        assert status == 200, body
        path = safe_points.stop_request_path(self.job_id, control_root_path=self.control)
        assert path.exists(), "the door answered accepted but requested no stop"
        signal = json.loads(path.read_bytes())
        assert signal["request_id"] == body["request_id"], (signal, body)
        assert signal["source"] == "ui", signal
        assert signal["reason"] == "operator asked", signal

    def test_the_nonce_record_holds_the_body_the_client_received(self):
        """D8's replay is byte-exact only if the store holds what was sent."""
        from packages.orchestration.command_nonce import lookup_nonce_result

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-published")

        assert status == 200, body
        assert lookup_nonce_result(
            self.job_id, "nonce-published",
            control_root_path=self.control) == {"status": 200, "body": body}

    def test_a_retry_of_the_same_nonce_is_audited_replayed(self):
        """Finding R-0636: a replay REPEATS an acceptance rather than being one."""
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        first = self._post(port, token, "nonce-twice")
        second = self._post(port, token, "nonce-twice")

        assert first == second
        assert self._audit_outcomes() == ["accepted", "replayed"]

    def test_an_effect_that_raises_is_500_and_audited_rejected_effect(self, monkeypatch):
        """DECISION F009 D18 clause four, and the only test that reaches the token."""
        from packages.orchestration import safe_points

        def explode(*_args, **_kwargs):
            raise safe_points.StopControlError("containment could not be guaranteed")

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        monkeypatch.setattr(safe_points, "request_stop", explode)
        status, body = self._post(port, token, "nonce-raises")

        assert status == 500, body
        assert "containment" not in json.dumps(body), "the exception text reached the wire"
        assert self._audit_outcomes() == ["rejected_effect"]


class TestFlightPlanApprovalDispatchEffects:
    """What an accepted `fp:` decision DID, read off disk (DECISION F031 D24).

    Its sibling `test_command_channel.py` pins what the door ANSWERS for the
    same requests. This class exists because a 200 proves only that the door
    chose a status: whether `resolve_flight_plan_approval` ran, and how many
    times the answer was persisted, is visible nowhere on the wire.
    """

    @pytest.fixture(autouse=True)
    def _setup_pending_plan(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        self.job = _make_job()
        self.job.flight_plan = {"_approval": "pending"}
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path

    def _approve(self, port, token, nonce):
        payload = {"command": "decision.resolve", "client_nonce": nonce,
                   "args": {"decision_id": "fp:approval", "answer": "approve"}}
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request("POST", f"/api/jobs/{self.job_id}/commands",
                         body=json.dumps(payload),
                         headers={"Authorization": f"Bearer {token}",
                                  CSRF_HEADER: token,
                                  "Content-Type": "application/json"})
            resp = conn.getresponse()
            return resp.status, json.loads(resp.read())
        finally:
            conn.close()

    def test_an_accepted_fp_approval_really_resolved_the_plan(self):
        """The effect ran: the plan is `approved` in a job RELOADED from storage."""
        from packages.orchestration.storage import load_job

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(port, token, "nonce-fp-effect")

        assert status == 200, body
        reloaded = load_job(self.job.id)
        assert reloaded.flight_plan["_approval"] == "approved", reloaded.flight_plan

    def test_the_accepted_fp_approval_saves_the_job_exactly_once(self, monkeypatch):
        """The only guard on the door's DELIBERATE omission of its own `save_job`.

        `resolve_flight_plan_approval` saves on both of its arms, so the door
        does not save again — and a reader who finds that absence surprising is
        one edit away from "fixing" it into a double write. Counting the calls
        is what makes the omission a decision rather than an oversight.
        """
        from packages.orchestration import storage

        real_save_job = storage.save_job
        saves = []

        def counting_save_job(job, *args, **kwargs):
            saves.append(str(job.id))
            return real_save_job(job, *args, **kwargs)

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        monkeypatch.setattr(storage, "save_job", counting_save_job)
        status, body = self._approve(port, token, "nonce-fp-save-once")

        assert status == 200, body
        assert saves == [self.job_id], saves
