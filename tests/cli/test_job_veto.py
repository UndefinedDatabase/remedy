"""F027 T003, DECISION F027 D5 — `remedy job veto-task`.

Modelled on `test_job_pause.py` and `test_job_plan_cmd.py`: the CLI handler is
proved through the real argv dispatcher, over a job whose tasks carry Task Plan
metadata built with `test_dag_schedule.flight_task`, so this file's own reading
of "unreachable" cannot drift from `dag_schedule.blocked_downstream`. The
command effect itself — `task_veto.veto_task_command` — is proved in
`tests/orchestration/test_task_veto.py`; this file proves the CLI's wrapping:
the task-argument resolution, the exit code each refusal maps to, and the
JSON envelope.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import pingpong_job as pj
from packages.orchestration import task_veto as tv
from tests.orchestration.test_dag_schedule import flight_task


def _secret_shaped_reason() -> str:
    """Built at run time from parts, so no secret-shaped literal sits in the source."""
    parts = ["sk", "-", "ant", "-"] + ["a"] * 24
    return "".join(parts)


def _read_events(job_id: str) -> list[dict]:
    from packages.orchestration.data_paths import run_log_dir

    out: list[dict] = []
    job_runs = run_log_dir(job_id)
    if not job_runs.is_dir():
        return out
    for jsonl in sorted(job_runs.glob("*.jsonl")):
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def job(data_root) -> pj.JobPlan:
    """T1 -> T2, both pending, the job itself running — a job a veto can act on."""
    tasks = [flight_task("T1"), flight_task("T2", "T1")]
    job = pj.JobPlan(job_title="CLI veto test", tasks=tasks, state=RunState.RUNNING)
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


class TestVetoByTaskIdAndByPlanId:
    def test_veto_by_the_tasks_own_id(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", "known-bad approach"], capsys)
        assert code == 0
        assert f"Task {t1} vetoed" in out
        assert "request:" in out
        t2 = _task_id(job, "T2")
        assert f"no longer reachable: {t2}" in out

    def test_veto_by_the_plan_id(self, job, capsys):
        """`_resolve_task_arg` resolves the planned id `T1` to the real task id — the
        exact resolution `job edit-task` already relies on."""
        code, out = _run(
            ["job", "veto-task", str(job.job_id), "T1", "--reason", "known-bad approach"], capsys)
        assert code == 0
        t1 = _task_id(job, "T1")
        assert f"Task {t1} vetoed" in out

    def test_a_veto_with_nothing_downstream_prints_none_lost(self, job, capsys):
        t2 = _task_id(job, "T2")
        code, out = _run(
            ["job", "veto-task", str(job.job_id), t2, "--reason", "known-bad approach"], capsys)
        assert code == 0
        assert "no other task is lost." in out


class TestVetoJSON:
    def test_json_emits_the_answers_own_keys(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", "known-bad approach",
             "--json"], capsys)
        assert code == 0
        body = json.loads(out)
        assert body["ok"] is True
        assert body["job_id"] == str(job.job_id)
        assert body["outcome"] == "vetoed"
        assert body["task_id"] == t1
        assert body["reason"] == "known-bad approach"
        assert body["actor"] == "cli"
        t2 = _task_id(job, "T2")
        assert body["unreachable"] == [t2]
        assert isinstance(body["request_id"], str) and body["request_id"]


class TestVetoRefusalExitCodes:
    """Each refusal's exit code, per DECISION F027 D5: 2 for a usage refusal, 3 for a
    not-ready refusal, 1 — `fail()`'s own default — for a job that does not exist."""

    def test_a_blank_reason_is_refused_and_writes_nothing(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", "", "--json"], capsys)
        assert code == 2
        body = json.loads(out)
        assert body["ok"] is False
        assert body["error"] == "reason_required"
        assert tv.vetoed_tasks(str(job.job_id)) == ()
        assert _read_events(str(job.job_id)) == []

    def test_a_too_long_reason_is_refused(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, _ = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", "x" * 501], capsys)
        assert code == 2

    def test_a_secret_shaped_reason_is_refused(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", _secret_shaped_reason(),
             "--json"],
            capsys)
        assert code == 2
        assert json.loads(out)["error"] == "reason_invalid"

    def test_an_unknown_task_is_refused(self, job, capsys):
        code, out = _run(
            ["job", "veto-task", str(job.job_id), "no-such-task", "--reason", "x", "--json"],
            capsys)
        assert code == 2
        assert json.loads(out)["error"] == "unknown_task"

    def test_a_terminal_job_is_not_vetoable(self, data_root, capsys):
        tasks = [flight_task("T1")]
        job = pj.JobPlan(job_title="done job", tasks=tasks, state=RunState.COMPLETED)
        pj.save_job_plan(job)
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", "x", "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "job_not_vetoable"

    def test_a_passed_task_is_not_vetoable(self, data_root, capsys):
        from packages.orchestration.pingpong_job import TASK_PASSED

        tasks = [flight_task("T1", status=RunState.PENDING)]
        tasks[0].status = TASK_PASSED
        job = pj.JobPlan(job_title="passed task job", tasks=tasks, state=RunState.RUNNING)
        pj.save_job_plan(job)
        t1 = _task_id(job, "T1")
        code, out = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", "x", "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "task_not_vetoable"

    def test_an_already_vetoed_task_is_refused(self, job, capsys):
        t1 = _task_id(job, "T1")
        code, _ = _run(["job", "veto-task", str(job.job_id), t1, "--reason", "first"], capsys)
        assert code == 0
        code, out = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", "second", "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "task_already_vetoed"

    def test_a_job_that_does_not_exist_exits_one(self, data_root, capsys):
        code, out = _run(
            ["job", "veto-task", "0123456789abcdef", "T1", "--reason", "x", "--json"], capsys)
        assert code == 1
        assert json.loads(out)["error"] == "invalid_job_id"


class TestVetoedEventCarriesTheReasonVerbatim:
    def test_the_task_vetoed_event_holds_the_reason_verbatim(self, job, capsys):
        t1 = _task_id(job, "T1")
        reason = "the approach re-implements a library we already depend on"
        code, _ = _run(
            ["job", "veto-task", str(job.job_id), t1, "--reason", reason], capsys)
        assert code == 0
        events = [e for e in _read_events(str(job.job_id)) if e.get("event") == "task_vetoed"]
        assert len(events) == 1
        assert events[0]["metadata"]["reason"] == reason
        assert events[0]["task_id"] == t1
