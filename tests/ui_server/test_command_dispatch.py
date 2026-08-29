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

    def _approve(self, port, token, nonce, answers=None):
        args = {"decision_id": "fp:approval", "answer": "approve"}
        if answers is not None:
            args["answers"] = answers
        payload = {"command": "decision.resolve", "client_nonce": nonce,
                   "args": args}
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

    def test_a_supplied_clarification_answer_is_recorded_as_human(self):
        """DECISION F031 D26's whole point, read off disk rather than the wire.

        A 200 proves only that the door took the request. What makes the form
        real is that the operator's own words reach the stored record and that
        `answered_by` says `human` — the field the assumption log reports, and
        the one that stays `default` if the door drops the answers it was sent.
        """
        from packages.orchestration.storage import load_job, save_job

        self.job.flight_plan = {"_approval": "pending", "clarifications_resolved": [
            {"id": "q1", "question": "Which store?", "default_answer": "sqlite"}]}
        save_job(self.job)
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(port, token, "nonce-fp-answered",
                                     answers={"q1": "use PostgreSQL"})

        assert status == 200, body
        resolved = load_job(self.job.id).flight_plan["clarifications_resolved"]
        assert resolved[0]["answer"] == "use PostgreSQL", resolved
        assert resolved[0]["answered_by"] == "human", resolved

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


#: A three-hunk diff, built with the `difflib` recipe `tests/cli/test_patch_cmd.py` and
#: `tests/orchestration/test_hunk_decision_record.py` both use. The three edits are spaced
#: further apart than twice `difflib`'s context, so they really arrive as three hunks and a
#: decision can leave one of them PENDING — which is what makes the body's three counts
#: distinguishable from one another.
_ORIGINAL = "\n".join(f"line {number:02d}" for number in range(1, 31)) + "\n"
_EDITED = (_ORIGINAL
           .replace("line 03\n", "line 03 CHANGED\n")
           .replace("line 15\n", "line 15 CHANGED\n")
           .replace("line 27\n", "line 27 CHANGED\n"))


def _three_hunk_diff() -> str:
    import difflib

    return "".join(difflib.unified_diff(
        _ORIGINAL.splitlines(True), _EDITED.splitlines(True),
        fromfile="a/f.txt", tofile="b/f.txt"))


def _hunk_ids(diff_text: str) -> list[str]:
    from packages.orchestration.diff_parser import parse_unified_diff_to_view

    view = parse_unified_diff_to_view(diff_text)
    return [h["id"] for h in view["files"][0]["hunks"]]


class TestApproveHunksDispatchEffects:
    """What an accepted `patch.approve-hunks` DID, read off disk (DECISION F033 D4).

    Its sibling `test_command_channel.py` pins what the door ANSWERS. This class
    exists for the reason the two classes above exist: a 200 proves only that the
    door chose a status, and whether the decision reached `job.metadata` and
    survived a `save_job` is visible nowhere on the wire.

    The door RECORDS and never applies, so every assertion below is about
    `job.metadata` and none is about the repository.
    """

    @pytest.fixture(autouse=True)
    def _setup_job_with_a_diff(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        self.job = _make_job()
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path
        self.control = tmp_path / "control"
        self.diff_text = _three_hunk_diff()
        self.hunk_ids = _hunk_ids(self.diff_text)
        assert len(self.hunk_ids) == 3, self.hunk_ids

    def _with_evidence(self):
        """An evidence directory holding the job-level diff, named by an INDEX record.

        The index is keyed by the job's CANONICAL id, which is what the door resolves
        with (finding R-0744), so this fixture is also the premise of that fix.
        """
        from packages.orchestration.data_paths import job_evidence_index_dir
        from packages.orchestration.diff_view_source import DIFF_JOB_ARTIFACT_NAME

        evidence_dir = self.tmp_path / "evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        (evidence_dir / DIFF_JOB_ARTIFACT_NAME).write_text(
            self.diff_text, encoding="utf-8")
        index_dir = job_evidence_index_dir()
        index_dir.mkdir(parents=True, exist_ok=True)
        (index_dir / f"{self.job_id}.json").write_text(
            json.dumps({"job_id": self.job_id,
                        "evidence_dir_local": str(evidence_dir)}),
            encoding="utf-8")
        return evidence_dir

    def _approve(self, port, token, nonce, **args):
        payload = {"command": "patch.approve-hunks", "client_nonce": nonce,
                   "args": args}
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

    def _recorded(self):
        """Every recorded decision on a job RELOADED from storage, so `save_job` is
        part of what each assertion below is testing."""
        from packages.orchestration.hunk_decision_record import (
            HUNK_DECISIONS_METADATA_KEY,
        )
        from packages.orchestration.storage import load_job

        return load_job(self.job.id).metadata.get(HUNK_DECISIONS_METADATA_KEY)

    def test_an_accepted_submission_records_the_decision_and_persists_it(self):
        """The effect ran AND `save_job` returned — proved by loading the job back."""
        from packages.orchestration.diff_view_source import DIFF_JOB_ARTIFACT_NAME

        self._with_evidence()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(
            port, token, "nonce-hunks-effect",
            approved=[self.hunk_ids[0]],
            rejected=[{"id": self.hunk_ids[1], "reason": "out of scope"}])

        assert status == 200, body
        attempt_key = f"job:{DIFF_JOB_ARTIFACT_NAME}"
        records = self._recorded()
        assert list(records) == [attempt_key], records
        assert [row["state"] for row in records[attempt_key]["hunks"]] == [
            "approved", "rejected", "pending"]
        assert self._audit_outcomes() == ["accepted"]

    def test_the_accepted_body_carries_the_attempt_key_and_the_three_counts(self):
        """The counts come from the LEDGER, so a pending hunk is reported as pending."""
        from packages.orchestration.diff_view_source import DIFF_JOB_ARTIFACT_NAME

        self._with_evidence()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(
            port, token, "nonce-hunks-body",
            approved=[self.hunk_ids[0]],
            rejected=[{"id": self.hunk_ids[1], "reason": "out of scope"}])

        assert status == 200, body
        assert body == {"command": "patch.approve-hunks", "outcome": "accepted",
                        "attempt_key": f"job:{DIFF_JOB_ARTIFACT_NAME}",
                        "approved": 1, "rejected": 1, "pending": 1}, body

    def test_the_rejected_wire_form_reaches_the_recorder_with_its_reason_verbatim(self):
        """`rejected[{id, reason}]` is the form `docs/roadmap/features/T5_F033.md` writes,
        and the door passes it STRAIGHT THROUGH — so the operator's words, whitespace and
        any `=` of their own included, arrive on the job unaltered."""
        from packages.orchestration.diff_view_source import DIFF_JOB_ARTIFACT_NAME

        reason = "  DSN=postgres://x is out of scope  "
        self._with_evidence()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(
            port, token, "nonce-hunks-reason",
            rejected=[{"id": self.hunk_ids[2], "reason": reason}])

        assert status == 200, body
        rows = self._recorded()[f"job:{DIFF_JOB_ARTIFACT_NAME}"]["hunks"]
        rejected = [row for row in rows if row["state"] == "rejected"]
        assert [row["id"] for row in rejected] == [self.hunk_ids[2]], rows
        assert rejected[0]["reason"] == reason, rejected

    def test_a_refused_decision_is_409_audited_rejected_state_and_writes_nothing(self):
        """DECISION F009 D21 clause three: the effect RAN and DECLINED. An id no hunk
        answers to is the core's `unknown_hunk`, and a refused decision is not a
        decision — nothing at all reaches `job.metadata`."""
        self._with_evidence()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(port, token, "nonce-hunks-refused",
                                     approved=["not-a-hunk-id"])

        assert status == 409, body
        assert body["error"] == "hunk decision was refused", body
        assert "not-a-hunk-id" not in json.dumps(body), body
        assert self._recorded() is None, self._recorded()
        assert self._audit_outcomes() == ["rejected_state"]

    def test_an_unresolvable_evidence_directory_takes_the_same_409_path(self):
        """A NAMED ABSENCE IS NOT A FAILURE, which is why this is 409 and not 500: no
        index record and no CWD-relative directory means the envelope reports the diff
        missing, the recorder refuses over it, and the effect declined rather than
        raised. THE DISCRIMINATOR is the status — a door that let the absence reach
        `_safe_error(500, ...)` would report the operator's own missing evidence as a
        server fault."""
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(port, token, "nonce-hunks-no-diff",
                                     approved=["h1"])

        assert status == 409, body
        assert body["error"] == "hunk decision was refused", body
        assert self._recorded() is None
        assert self._audit_outcomes() == ["rejected_state"]
