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
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import JobPlan, TaskEntry
from tests.ui_server.server_start import wait_for_server_info

# Pinned as a literal for the reason its sibling gives: a test that imports the
# constant it checks cannot catch a rename of the header the browser must send.
CSRF_HEADER = "X-Remedy-CSRF"


def _make_job() -> JobPlan:
    return JobPlan(
        job_title="test-command-dispatch-job",
        user_prompt="Test prompt for the command dispatch effects",
        tasks=[TaskEntry(title="Write a README")],
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

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return wait_for_server_info(info_file, t)["port"], token


class TestJobStopDispatchEffects:
    """Integration tests that start a real server and then read what it wrote."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        self.job = _make_job()
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
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


class TestTaskPlanApprovalDispatchEffects:
    """What an accepted `plan:` decision DID, read off disk (DECISION F031 D24).

    Its sibling `test_command_channel.py` pins what the door ANSWERS for the
    same requests. This class exists because a 200 proves only that the door
    chose a status: whether `resolve_task_plan_approval` ran, and how many
    times the answer was persisted, is visible nowhere on the wire.
    """

    @pytest.fixture(autouse=True)
    def _setup_pending_plan(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        self.job = _make_job()
        self.job.task_plan = {"_approval": "pending"}
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path

    def _approve(self, port, token, nonce, answers=None):
        args = {"decision_id": "plan:approval", "answer": "approve"}
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

    def test_an_accepted_plan_approval_really_resolved_the_plan(self):
        """The effect ran: the plan is `approved` in a job RELOADED from storage."""
        from packages.orchestration.pingpong_job import load_job_plan

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(port, token, "nonce-fp-effect")

        assert status == 200, body
        reloaded = load_job_plan(self.job.job_id)
        assert reloaded.task_plan["_approval"] == "approved", reloaded.task_plan

    def test_a_supplied_clarification_answer_is_recorded_as_human(self):
        """DECISION F031 D26's whole point, read off disk rather than the wire.

        A 200 proves only that the door took the request. What makes the form
        real is that the operator's own words reach the stored record and that
        `answered_by` says `human` — the field the assumption log reports, and
        the one that stays `default` if the door drops the answers it was sent.
        """
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

        self.job.task_plan = {"_approval": "pending", "clarifications_resolved": [
            {"id": "q1", "question": "Which store?", "default_answer": "sqlite"}]}
        save_job_plan(self.job)
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(port, token, "nonce-fp-answered",
                                     answers={"q1": "use PostgreSQL"})

        assert status == 200, body
        resolved = load_job_plan(self.job.job_id).task_plan["clarifications_resolved"]
        assert resolved[0]["answer"] == "use PostgreSQL", resolved
        assert resolved[0]["answered_by"] == "human", resolved

    def test_the_accepted_plan_approval_saves_the_job_exactly_once(self, monkeypatch):
        """The only guard on the door's DELIBERATE omission of its own `save_job`.

        `resolve_task_plan_approval` saves on both of its arms, so the door
        does not save again — and a reader who finds that absence surprising is
        one edit away from "fixing" it into a double write. Counting the calls
        is what makes the omission a decision rather than an oversight.
        """
        from packages.orchestration import pingpong_job

        real_save_job = pingpong_job.save_job_plan
        saves = []

        def counting_save_job(job, *args, **kwargs):
            saves.append(str(job.job_id))
            return real_save_job(job, *args, **kwargs)

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        monkeypatch.setattr(pingpong_job, "save_job_plan", counting_save_job)
        status, body = self._approve(port, token, "nonce-fp-save-once")

        assert status == 200, body
        assert saves == [self.job_id], saves

    def _save_a_real_plan(self):
        """A plan the edit backend can edit: two tasks, the second waiting for the first."""
        from packages.orchestration.job_plan import map_task_plan_to_tasks
        from packages.orchestration.pingpong_job import save_job_plan
        from packages.orchestration.schemas.models import TaskPlan

        plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": [
            {"id": "T1", "title": "Build parser", "goal": "g", "acceptance": ["parses"],
             "depends_on": [], "est_tokens_band": "S", "files_hint": ["src/p.py"]},
            {"id": "T2", "title": "Build report", "goal": "g", "acceptance": ["reports"],
             "depends_on": ["T1"], "est_tokens_band": "S", "files_hint": ["src/r.py"]},
        ]})
        body = plan.model_dump()
        body["_approval"] = "pending"
        self.job.task_plan = body
        self.job.tasks = map_task_plan_to_tasks(plan)
        save_job_plan(self.job)

    def test_an_edit_landing_after_the_door_loaded_the_job_is_approved_not_lost(
            self, monkeypatch):
        """DECISION F015 D2: the door consumes the approval against the record as it is NOW."""
        from packages.orchestration import job_plan
        from packages.orchestration.pingpong_job import load_job_plan
        from packages.orchestration.plan_editing import edit_plan

        self._save_a_real_plan()
        real_questions = job_plan.open_clarification_questions

        def questions_after_a_concurrent_edit(clarifications):
            edit_plan(self.job_id, "plan_delete_task", {"task_id": "T2"}, expected_version=1,
                      actor="cli")
            return real_questions(clarifications)

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        monkeypatch.setattr(job_plan, "open_clarification_questions",
                            questions_after_a_concurrent_edit)
        status, body = self._approve(port, token, "nonce-fp-race")

        assert status == 200, body
        stored = load_job_plan(self.job.job_id).task_plan
        assert stored["_approval"] == "approved", stored
        assert [t["id"] for t in stored["tasks"]] == ["T1"], stored
        assert stored["_version"] == 2, stored

    def test_an_approval_closed_after_the_door_loaded_the_job_declines_409(self, monkeypatch):
        """The door read `pending`, then another door approved: nothing is approved twice."""
        from packages.orchestration import job_plan
        from packages.orchestration.pingpong_job import load_job_plan
        from packages.orchestration.plan_editing import consume_plan_approval

        self._save_a_real_plan()
        real_questions = job_plan.open_clarification_questions

        def questions_after_a_concurrent_approval(clarifications):
            consume_plan_approval(load_job_plan(self.job.job_id), reason="reject", answers={},
                                  questions=[])
            return real_questions(clarifications)

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        monkeypatch.setattr(job_plan, "open_clarification_questions",
                            questions_after_a_concurrent_approval)
        status, body = self._approve(port, token, "nonce-fp-closed")

        assert status == 409, body
        assert load_job_plan(self.job.job_id).task_plan["_approval"] == "rejected"


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
        from packages.orchestration.pingpong_job import save_job_plan
        self.job = _make_job()
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
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
        from packages.orchestration.pingpong_job import load_job_plan

        return load_job_plan(self.job.job_id).metadata.get(HUNK_DECISIONS_METADATA_KEY)

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


class TestChatSendDispatchEffects:
    """DECISION F264 D2: what an accepted `chat.send` wrote — the sealed steering record, the
    run-log event that certifies it, the audit line and the nonce publication — and that a
    refused or failed one wrote no record at all."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        self.job = _make_job()
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path
        self.control = tmp_path / "control"

    def _send(self, port, token, nonce, **args):
        payload = {"command": "chat.send", "client_nonce": nonce, "args": args}
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

    def _records(self):
        from packages.orchestration.steering import list_steering_messages
        return list_steering_messages(self.job_id, self.tmp_path)

    def _steering_events(self):
        from packages.orchestration.timeline import load_run_events
        return [e for e in load_run_events(self.tmp_path, self.job_id)
                if e.get("event") == "steering_message_received"]

    def test_an_accepted_message_is_sealed_certified_and_published(self):
        from packages.orchestration.command_nonce import lookup_nonce_result

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._send(port, token, "nonce-chat", message="  Keep it small.  ")

        assert status == 200, body
        assert body == {"command": "chat.send", "outcome": "accepted",
                        "request_id": "sm-0001", "message_id": "sm-0001"}
        [record] = self._records()
        assert record["text"] == "Keep it small."
        assert record["channel"] == "cockpit"
        [event] = self._steering_events()
        assert (event.get("metadata") or {})["record_sha256"] == record["record_sha256"]
        assert self._audit_outcomes() == ["accepted"]
        assert lookup_nonce_result(self.job_id, "nonce-chat",
                                   control_root_path=self.control) == {"status": 200, "body": body}

    def test_a_retry_of_the_same_nonce_records_the_message_once(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        first = self._send(port, token, "nonce-chat-twice", message="Once.")
        second = self._send(port, token, "nonce-chat-twice", message="Once.")

        assert first == second
        assert [r["message_id"] for r in self._records()] == ["sm-0001"]
        assert self._audit_outcomes() == ["accepted", "replayed"]

    def test_a_blank_message_is_400_on_its_field_and_writes_nothing(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._send(port, token, "nonce-chat-blank", message="   ")

        assert status == 400, body
        assert body == {"error": "the message is empty", "field": "message"}
        assert self._records() == []
        assert self._audit_outcomes() == ["rejected_shape"]

    def test_an_ended_job_is_409_audited_rejected_state_and_writes_nothing(self):
        from packages.core.models import RunState
        from packages.orchestration.pingpong_job import save_job_plan

        self.job.state = RunState.COMPLETED
        save_job_plan(self.job)
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._send(port, token, "nonce-chat-ended", message="Too late.")

        assert status == 409, body
        assert body["error"] == "job has ended and takes no message", body
        assert self._records() == []
        assert self._audit_outcomes() == ["rejected_state"]

    def test_a_record_that_cannot_be_written_is_500_and_certifies_nothing(self, monkeypatch):
        from packages.orchestration import steering

        def refuse(*_args, **_kwargs):
            raise steering.SecureFsError("disk full at /secret/path")

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        monkeypatch.setattr(steering, "write_file_atomically", refuse)
        status, body = self._send(port, token, "nonce-chat-fails", message="Hello.")

        assert status == 500, body
        assert "secret" not in json.dumps(body), "the exception text reached the wire"
        assert self._steering_events() == []
        assert self._audit_outcomes() == ["rejected_effect"]


def _plan_task(tid: str, deps: list[str], acceptance: list[str] | None = None) -> dict:
    return {"id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
            "acceptance": acceptance or [f"{tid} works"], "depends_on": deps,
            "est_tokens_band": "S", "files_hint": [f"src/{tid.lower()}.py"]}


class TestPlanEditDispatchEffects:
    """What an accepted `job.plan-*` edit DID, read off disk (DECISION F015 D3).

    The door maps each edit to `plan_editing.edit_plan`, so these tests prove the mapping —
    the argument object, the version, the editor's fingerprint, the refusal statuses and the
    replay — and leave the edits' own rules to `tests/orchestration/test_plan_editing.py`.
    """

    @pytest.fixture(autouse=True)
    def _setup_plan(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import RunState
        from packages.orchestration.job_plan import map_task_plan_to_tasks
        from packages.orchestration.pingpong_job import save_job_plan
        from packages.orchestration.schemas.models import TaskPlan

        plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": [
            _plan_task("T1", []),
            _plan_task("T2", ["T1"], ["parser reads", "parser reports", "parser is fast"]),
            _plan_task("T3", ["T2"]),
        ]})
        body = plan.model_dump()
        body["_approval"] = "pending"
        self.job = _make_job()
        self.job.task_plan = body
        self.job.tasks = map_task_plan_to_tasks(plan)
        self.job.state = RunState.PLANNED
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path
        self.control = tmp_path / "control"

    def _post(self, port, token, nonce, command, args):
        payload = {"command": command, "client_nonce": nonce, "args": args}
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

    def _stored(self):
        from packages.orchestration.pingpong_job import load_job_plan
        return load_job_plan(self.job_id).task_plan

    def _record_bytes(self):
        from packages.orchestration.data_paths import job_record_path
        return job_record_path(self.job_id).read_bytes()

    @pytest.mark.parametrize(("command", "args", "expected_ids"), [
        ("job.plan-edit-task", {"task_id": "T3", "fields": {"title": "Wire T3"}},
         ["T1", "T2", "T3"]),
        ("job.plan-delete-task", {"task_id": "T2"}, ["T1", "T3"]),
        ("job.plan-reorder", {"order": ["T1", "T3", "T2"]}, ["T1", "T3", "T2"]),
        ("job.plan-merge-tasks", {"task_ids": ["T2", "T3"]}, ["T1", "T2"]),
        ("job.plan-split-task", {"task_id": "T2", "partition": [[0], [1, 2]]},
         ["T1", "T2a", "T2b", "T3"]),
        ("job.plan-edit-acceptance", {"task_id": "T2", "op": "remove", "index": 1},
         ["T1", "T2", "T3"]),
    ])
    def test_each_edit_is_applied_versioned_and_attributed_to_the_token(
            self, command, args, expected_ids):
        from packages.orchestration.ui_server import token_fingerprint

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-" + command.replace(".", "-"), command,
                                  {**args, "expected_version": 1})

        assert status == 200, body
        assert (body["outcome"], body["version"], body["tasks"]) == ("accepted", 2, expected_ids)
        stored = self._stored()
        assert [t["id"] for t in stored["tasks"]] == expected_ids
        [entry] = stored["_edits"]
        assert entry["actor"] == token_fingerprint(token)
        assert "expected_version" not in entry["args"]
        assert self._audit_outcomes() == ["accepted"]

    def test_an_edit_naming_no_version_is_a_shape_error_on_that_field(self):
        before = self._record_bytes()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        for nonce, version in (("nonce-none", None), ("nonce-bool", True), ("nonce-zero", 0)):
            args = {"task_id": "T3"}
            if version is not None:
                args["expected_version"] = version
            status, body = self._post(port, token, nonce, "job.plan-delete-task", args)
            assert (status, body["field"]) == (400, "expected_version"), body
        assert self._record_bytes() == before
        assert self._audit_outcomes() == ["rejected_shape"] * 3

    def test_a_stale_version_is_a_conflict_naming_the_current_one(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        self._post(port, token, "nonce-first", "job.plan-delete-task",
                   {"task_id": "T3", "expected_version": 1})
        before = self._record_bytes()
        status, body = self._post(port, token, "nonce-stale", "job.plan-delete-task",
                                  {"task_id": "T2", "expected_version": 1})

        assert status == 409, body
        assert body == {"error": "the plan changed since this edit was made", "current_version": 2}
        assert self._record_bytes() == before
        assert self._audit_outcomes() == ["accepted", "rejected_state"]

    @pytest.mark.parametrize(("args", "status", "says", "outcome"), [
        ({"task_id": "T9"}, 400, "T9", "rejected_shape"),
        ({}, 400, "task_id", "rejected_shape"),
    ])
    def test_refused_arguments_are_a_shape_error_on_args_with_the_reason(
            self, args, status, says, outcome):
        before = self._record_bytes()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        code, body = self._post(port, token, "nonce-args", "job.plan-delete-task",
                                {**args, "expected_version": 1})
        assert (code, body["field"]) == (status, "args"), body
        assert says in body["detail"]
        assert self._record_bytes() == before
        assert self._audit_outcomes() == [outcome]

    def test_an_edit_the_planners_checks_refuse_is_409_with_the_violation(self):
        before = self._record_bytes()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-invalid", "job.plan-merge-tasks",
                                  {"task_ids": ["T1", "T3"], "expected_version": 1})
        assert status == 409, body
        assert body["error"] == "the edited plan fails the planner's checks"
        assert "cycle" in body["detail"]
        assert self._record_bytes() == before
        assert self._audit_outcomes() == ["rejected_state"]

    def test_an_approved_plan_refuses_an_edit_with_its_state(self):
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

        job = load_job_plan(self.job_id)
        job.task_plan["_approval"] = "approved"
        save_job_plan(job)
        before = self._record_bytes()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-closed", "job.plan-delete-task",
                                  {"task_id": "T3", "expected_version": 1})
        assert status == 409, body
        assert body["error"] == "the plan is not open for editing"
        assert "the plan is approved" in body["detail"]
        assert self._record_bytes() == before

    def test_a_retried_nonce_replays_the_edit_and_never_applies_it_twice(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        args = {"task_id": "T3", "expected_version": 1}
        first = self._post(port, token, "nonce-retry", "job.plan-delete-task", args)
        second = self._post(port, token, "nonce-retry", "job.plan-delete-task", args)

        assert first == second and first[0] == 200
        assert self._stored()["_version"] == 2 and len(self._stored()["_edits"]) == 1
        assert self._audit_outcomes() == ["accepted", "replayed"]
