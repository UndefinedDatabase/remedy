"""F038 T002 and DECISION F038 D7 — `send_card_through_door`'s refusals, before any
connection opens, and its audit line when a confirmed card reaches the cockpit. Modelled on
`TestSteerTaskDoor` in `tests/ui_server/test_steer_task_door.py`: its
`_start_ui_server_for_job` and its job fixture are this file's own model. Every card here is
built by `parse_chat_intent` and `build_action_card`, never by hand.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from packages.orchestration.chat_door import ChatDoorAnswer, send_card_through_door
from packages.orchestration.chat_intent import (
    ChatIntentError,
    build_action_card,
    parse_chat_intent,
)
from packages.orchestration.command_audit import AUDIT_FILENAME
from packages.orchestration.pause_control import pause_requested
from tests.ui_server.server_start import wait_for_server_info


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Mirrors `test_steer_task_door.py`'s own copy exactly (finding R-0701)."""
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


class TestChatDoorSend:
    """What `send_card_through_door` answers and writes through the write door."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        from packages.core.models import RunState
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan
        from tests.orchestration.test_dag_schedule import flight_task

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = JobPlan(job_title="chat-door-job", tasks=[flight_task("T1")],
                           state=RunState.RUNNING)
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path
        self.audit_path = tmp_path / "control" / "jobs" / self.job_id / AUDIT_FILENAME
        self.port, self.token = _start_ui_server_for_job(self.job_id, tmp_path)

    def _task_id(self) -> str:
        return self.job.tasks[0].task_id

    def _audit_lines(self) -> list[dict]:
        return [json.loads(line) for line in self.audit_path.read_bytes().splitlines()]

    def _pause_card(self):
        return build_action_card(parse_chat_intent("pause"), job_id=self.job_id)

    def _send(self, card, *, nonce, port=None, token=None, job_id=None) -> ChatDoorAnswer:
        return send_card_through_door(
            card, job_id=self.job_id if job_id is None else job_id,
            client_nonce=nonce,
            port=self.port if port is None else port,
            token=self.token if token is None else token)

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
        answer = self._send(self._pause_card(), nonce="nonce-wrong-token",
                            token="not-the-real-token")

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

    def test_a_port_of_zero_raises(self):
        with pytest.raises(ChatIntentError, match="port"):
            self._send(self._pause_card(), nonce="nonce-port-0", port=0)
        assert not self.audit_path.exists()

    def test_a_port_of_70000_raises(self):
        with pytest.raises(ChatIntentError, match="port"):
            self._send(self._pause_card(), nonce="nonce-port-big", port=70000)
        assert not self.audit_path.exists()

    def test_a_port_of_true_raises(self):
        with pytest.raises(ChatIntentError, match="port"):
            self._send(self._pause_card(), nonce="nonce-port-bool", port=True)
        assert not self.audit_path.exists()

    def test_an_empty_token_raises(self):
        with pytest.raises(ChatIntentError, match="token"):
            self._send(self._pause_card(), nonce="nonce-empty-token", token="")
        assert not self.audit_path.exists()
