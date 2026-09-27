"""F030 T002 S4 — DECISION F030 D2: the write door's `job.steer`, modelled on
`TestVetoTaskDispatchEffects` in `test_command_dispatch.py` (DECISION F027 D5) and
`TestChatSendDispatchEffects` (DECISION F264 D2): the shape checks that run BEFORE the job's
own state can refuse anything, the 409s the effect itself gives, and the audit line for each.
The effect's own rules are proved in `tests/orchestration/test_steer_task.py`.
"""
from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import JobPlan
from tests.ui_server.server_start import wait_for_server_info

CSRF_HEADER = "X-Remedy-CSRF"


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Mirrors `test_command_dispatch.py`'s own copy exactly (finding R-0701)."""
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


class TestSteerTaskDoor:
    """What `job.steer` answers and writes through the write door (DECISION F030 D2)."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        from packages.core.models import RunState
        from packages.orchestration.pingpong_job import save_job_plan
        from tests.orchestration.test_dag_schedule import flight_task

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        tasks = [flight_task("T1"), flight_task("T2", "T1")]
        self.job = JobPlan(job_title="steer-door-job", tasks=tasks, state=RunState.RUNNING)
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path
        self.control = tmp_path / "control"

    def _task_id(self, planned_id: str) -> str:
        for t in self.job.tasks:
            if (t.inputs.get("plan") or {}).get("planned_id") == planned_id:
                return t.task_id
        raise AssertionError(f"no task for planned id {planned_id!r}")

    def _post(self, port, token, nonce, args):
        payload = {"command": "job.steer", "client_nonce": nonce, "args": args}
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

    def test_an_accepted_note_writes_a_record_with_channel_cockpit_and_the_task_id(self):
        t1 = self._task_id("T1")
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-steer",
                                  {"task_id": t1, "message": "Keep it small."})

        assert status == 200, body
        assert (body["command"], body["outcome"]) == ("job.steer", "accepted")
        assert body["task_id"] == t1
        [record] = self._records()
        assert record["task_id"] == t1
        assert record["channel"] == "cockpit"
        assert record["text"] == "Keep it small."
        assert self._audit_outcomes() == ["accepted"]

    def test_a_passed_task_is_409_naming_task_not_steerable_and_writes_nothing(self):
        from packages.orchestration.pingpong_job import TASK_PASSED

        t1 = self._task_id("T1")
        for t in self.job.tasks:
            if t.task_id == t1:
                t.status = TASK_PASSED
        from packages.orchestration.pingpong_job import save_job_plan
        save_job_plan(self.job)
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-passed",
                                  {"task_id": t1, "message": "Too late."})

        assert status == 409, body
        assert body["error"].startswith("task_not_steerable:"), body
        assert self._records() == []
        assert self._audit_outcomes() == ["rejected_state"]

    def test_an_unknown_task_is_409_naming_unknown_task(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-unknown",
                                  {"task_id": "no-such-task", "message": "hello"})

        assert status == 409, body
        assert body["error"].startswith("unknown_task:"), body
        assert self._records() == []

    def test_a_missing_task_id_is_400_before_the_job_is_read(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-no-task", {"message": "hello"})

        assert status == 400, body
        assert body["field"] == "task_id", body
        assert self._records() == []

    def test_an_empty_message_is_400_on_its_field_and_writes_nothing(self):
        t1 = self._task_id("T1")
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-empty-message",
                                  {"task_id": t1, "message": "   "})

        assert status == 400, body
        assert body["field"] == "message", body
        assert self._records() == []

    def test_an_ended_job_is_409_naming_job_not_steerable(self):
        from packages.core.models import RunState
        from packages.orchestration.pingpong_job import save_job_plan

        t1 = self._task_id("T1")
        self.job.state = RunState.COMPLETED
        save_job_plan(self.job)
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-ended",
                                  {"task_id": t1, "message": "Too late."})

        assert status == 409, body
        assert body["error"].startswith("job_not_steerable:"), body
        assert self._records() == []
        assert self._audit_outcomes() == ["rejected_state"]
