"""F030 T002 — `remedy job steer`, DECISION F030 D2.

Modelled on `test_job_veto.py` and `test_chat_cmd.py`: the CLI handler is proved through the
real argv dispatcher, over a job whose tasks carry Task Plan metadata built with
`test_dag_schedule.flight_task`, so the task-argument resolution matches `job veto-task`'s own.
The command effect itself — `steering.steer_task_command` — is proved in
`tests/orchestration/test_steer_task.py`; this file proves the CLI's wrapping: the task
resolution, the exit code each refusal maps to, the JSON envelope, and that `remedy chat show`
names the task a note went to.
"""
from __future__ import annotations

import json

import pytest

from packages.core.models import RunState
from packages.orchestration import pingpong_job as pj
from tests.orchestration.test_dag_schedule import flight_task


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


@pytest.fixture
def job() -> pj.JobPlan:
    tasks = [flight_task("T1"), flight_task("T2", "T1")]
    job = pj.JobPlan(job_title="CLI steer test", tasks=tasks, state=RunState.RUNNING)
    pj.save_job_plan(job)
    return job


def _task_id(job: pj.JobPlan, planned_id: str) -> str:
    for t in job.tasks:
        if (t.inputs.get("plan") or {}).get("planned_id") == planned_id:
            return t.task_id
    raise AssertionError(f"no task for planned id {planned_id!r}")


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return (code or 0), capsys.readouterr().out


class TestSteerTextAndJSON:
    def test_the_text_form_records_the_note_and_names_the_task(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "steer", str(job.job_id), "--task", t1, "Keep it small."], capsys)
        assert code == 0
        assert f"Note sm-0001 recorded for task {t1} of job {job.job_id}." in out
        assert "next round" in out

    def test_the_json_form_emits_the_answers_own_keys(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "steer", str(job.job_id), "--task", t1, "Keep it small.", "--json"], capsys)
        assert code == 0
        body = json.loads(out)
        assert body["ok"] is True
        assert body["job_id"] == str(job.job_id)
        assert body["outcome"] == "accepted"
        assert body["task_id"] == t1
        assert body["message_id"] == "sm-0001"
        assert body["request_id"] == "sm-0001"

    def test_a_planned_id_resolves_to_its_task(self, job, capsys):
        """`_resolve_task_arg` resolves the planned id `T1` to the real task id — the exact
        resolution `job veto-task` already relies on."""
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "steer", str(job.job_id), "--task", "T1", "Keep it small."], capsys)
        assert code == 0
        assert f"for task {t1} of job {job.job_id}." in out


class TestSteerRefusalExitCodes:
    """Each refusal's exit code, per DECISION F030 D2: 2 for a usage refusal, 3 for a
    not-ready refusal."""

    def test_an_unknown_task_exits_2(self, job, capsys):
        code, out = _run(
            ["job", "steer", str(job.job_id), "--task", "no-such-task", "hello", "--json"],
            capsys)
        assert code == 2
        assert json.loads(out)["error"] == "unknown_task"

    def test_an_empty_text_exits_2_and_writes_nothing(self, job, capsys):
        from packages.orchestration import steering as ST

        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "steer", str(job.job_id), "--task", t1, "   ", "--json"], capsys)
        assert code == 2
        assert json.loads(out)["error"] == "invalid_message"
        assert ST.list_steering_messages(str(job.job_id)) == []

    def test_a_passed_task_exits_3(self, job, capsys):
        from packages.orchestration.pingpong_job import TASK_PASSED

        t1 = _task_id(job, "T1")
        for t in job.tasks:
            if t.task_id == t1:
                t.status = TASK_PASSED
        pj.save_job_plan(job)
        code, out = _run(
            ["job", "steer", str(job.job_id), "--task", t1, "hello", "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "task_not_steerable"

    def test_an_ended_job_exits_3(self, job, capsys):
        job.state = RunState.COMPLETED
        pj.save_job_plan(job)
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "steer", str(job.job_id), "--task", t1, "hello", "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "job_not_steerable"

    def test_a_job_that_does_not_exist_exits_1(self, capsys):
        code, out = _run(
            ["job", "steer", "0123456789abcdef", "--task", "T1", "hello", "--json"], capsys)
        assert code == 1
        assert json.loads(out)["error"] == "invalid_job_id"


class TestChatShowNamesTheTask:
    def test_text_names_the_task_a_note_went_to(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, _ = _run(["job", "steer", str(job.job_id), "--task", t1, "Keep it small."], capsys)
        assert code == 0
        code, out = _run(["chat", "show", str(job.job_id)], capsys)
        assert code == 0
        assert f"via cli to task {t1}: Keep it small." in out
        assert f"waiting — task {t1} has not started a round since it arrived" in out

    def test_json_names_the_task_as_addressed_to(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, _ = _run(["job", "steer", str(job.job_id), "--task", t1, "Keep it small."], capsys)
        assert code == 0
        code, out = _run(["chat", "show", str(job.job_id), "--json"], capsys)
        assert code == 0
        [message] = json.loads(out)["messages"]
        assert message["addressed_to"] == t1
        assert message["status"] == "waiting"

    def test_a_finished_tasks_note_reads_not_taken_in_while_the_job_runs(self, job, capsys):
        from packages.orchestration.pingpong_job import TASK_PASSED

        t1 = _task_id(job, "T1")
        code, _ = _run(["job", "steer", str(job.job_id), "--task", t1, "Keep it small."], capsys)
        assert code == 0
        reloaded = pj.load_job_plan(job.job_id)
        for t in reloaded.tasks:
            if t.task_id == t1:
                t.status = TASK_PASSED
        pj.save_job_plan(reloaded)
        code, out = _run(["chat", "show", str(job.job_id)], capsys)
        assert code == 0
        assert f"not taken in — task {t1} finished without starting another round" in out
