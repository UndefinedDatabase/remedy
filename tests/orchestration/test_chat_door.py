"""F038 T002 and DECISION F038 D7 — `send_card_through_door`'s refusals, before any
connection opens, and its audit line when a confirmed card reaches the write door. Since
DECISION amend1015f D20 the door is the `remedy serve start` supervisor's, so each test runs a
real supervisor in a thread on a short data root and the card goes over its unix socket. Every
card here is built by `parse_chat_intent` and `build_action_card`, never by hand.
"""

from __future__ import annotations

import json

import pytest

from packages.orchestration.chat_door import ChatDoorAnswer, send_card_through_door
from packages.orchestration.chat_intent import (
    ChatIntentError,
    build_action_card,
    parse_chat_intent,
)
from packages.orchestration.command_audit import AUDIT_FILENAME
from packages.orchestration.pause_control import pause_requested
from packages.orchestration.serve_paths import serve_paths
from tests.ui_server.door_host import SupervisorThread


class TestChatDoorSend:
    """What `send_card_through_door` answers and writes through the write door."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path_factory, monkeypatch):
        from packages.core.models import RunState
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan
        from tests.orchestration.test_dag_schedule import flight_task

        tmp_path = tmp_path_factory.mktemp("cd")
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = JobPlan(job_title="chat-door-job", tasks=[flight_task("T1")],
                           state=RunState.RUNNING)
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path
        self.audit_path = tmp_path / "control" / "jobs" / self.job_id / AUDIT_FILENAME
        self.supervisor = SupervisorThread(tmp_path)
        yield
        self.supervisor.close()

    def _task_id(self) -> str:
        return self.job.tasks[0].task_id

    def _audit_lines(self) -> list[dict]:
        return [json.loads(line) for line in self.audit_path.read_bytes().splitlines()]

    def _pause_card(self):
        return build_action_card(parse_chat_intent("pause"), job_id=self.job_id)

    def _send(self, card, *, nonce, job_id=None) -> ChatDoorAnswer:
        return send_card_through_door(
            card, job_id=self.job_id if job_id is None else job_id, client_nonce=nonce)

    def test_before_any_send_the_audit_file_is_absent(self):
        assert not self.audit_path.exists()

    def test_a_pause_card_is_accepted_and_audited(self):
        answer = self._send(self._pause_card(), nonce="nonce-pause")

        assert answer.status == 200
        assert answer.accepted is True
        assert answer.body["command"] == "job.pause"
        lines = self._audit_lines()
        assert len(lines) == 1
        assert (lines[0]["command"], lines[0]["nonce"], lines[0]["outcome"]) == (
            "job.pause", "nonce-pause", "accepted")
        assert pause_requested(self.job_id) is not None

    def test_the_same_card_and_nonce_sent_twice_replays(self):
        card = self._pause_card()
        first = self._send(card, nonce="nonce-replay")
        second = self._send(card, nonce="nonce-replay")

        assert (first.status, first.body) == (second.status, second.body)
        outcomes = [line["outcome"] for line in self._audit_lines()]
        assert outcomes == ["accepted", "replayed"]

    def test_a_focused_note_is_a_steer_naming_the_task(self):
        t1 = self._task_id()
        card = build_action_card(
            parse_chat_intent("tell the builder: use X", focused_task_id=t1),
            job_id=self.job_id)
        answer = self._send(card, nonce="nonce-steer")

        assert answer.status == 200
        assert answer.body["command"] == "job.steer"
        assert answer.body["task_id"] == t1

    def test_an_unfocused_note_is_a_chat_send(self):
        card = build_action_card(
            parse_chat_intent("note: keep it small"), job_id=self.job_id)
        answer = self._send(card, nonce="nonce-note")

        assert answer.status == 200
        assert answer.body["command"] == "chat.send"

    def test_a_wrong_token_is_403_and_not_accepted(self):
        # The supervisor holds its token in memory; a token file that no longer matches it is
        # what a client with a stale or forged token sends.
        serve_paths(self.tmp_path).token_file.write_text("not-the-real-token", encoding="utf-8")
        answer = self._send(self._pause_card(), nonce="nonce-wrong-token")

        assert answer.status == 403
        assert answer.accepted is False

    def test_an_unconfirmable_card_raises_and_writes_nothing(self):
        card = build_action_card(parse_chat_intent("veto it"), job_id=self.job_id)
        assert not card.confirmable

        with pytest.raises(ChatIntentError):
            self._send(card, nonce="nonce-veto")
        assert not self.audit_path.exists()

    def test_an_unsafe_job_id_raises_before_any_send(self):
        with pytest.raises(ChatIntentError, match="job_id"):
            self._send(self._pause_card(), nonce="nonce-bad-job", job_id="../x")
        assert not self.audit_path.exists()

    def test_with_no_supervisor_the_send_raises_os_error_and_writes_nothing(self):
        self.supervisor.close()
        with pytest.raises(OSError):
            self._send(self._pause_card(), nonce="nonce-no-supervisor")
        assert not self.audit_path.exists()
