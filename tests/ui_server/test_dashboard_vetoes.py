"""F027 R7, DECISION F027 D7 (1) — the dashboard's `vetoes` section.

`_build_dashboard` gains `vetoes`: `tasks` (one entry per veto entry in plan order —
task id, reason verbatim, actor, request time, request id, status at the veto, that
veto's own unreachable set and its recorded answer's option or ""), `vetoable_task_ids`
(the tasks `task_veto.veto_refusal` admits for the job's current state),
`unreachable_task_ids` (`task_veto.veto_unreachable` over every vetoed task) and `error`
(`""`, or the text of a `TaskVetoError` met while reading, in which case the other three
keep their empty values). It never raises for them, and reads a real control root through
`task_veto`, exactly as `test_dashboard_pause.py` does for `pause_control`.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import task_veto as tv
from packages.orchestration.pingpong_job import JobPlan
from tests.orchestration.test_dag_schedule import flight_task
from tests.orchestration.test_dag_schedule import ids as dag_ids


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


def _job(tasks, **overrides) -> JobPlan:
    defaults: dict = dict(
        job_id="f027-r7-dash-job",
        job_title="veto-dashboard-job",
        user_prompt="test prompt",
        tasks=tasks,
        state=RunState.RUNNING,
        metadata={"target_repo": "."},
    )
    defaults.update(overrides)
    return JobPlan(**defaults)


def _vetoes_section(job) -> dict:
    from unittest.mock import patch

    from packages.orchestration.ui_server import _build_dashboard
    with patch("packages.orchestration.ui_server._load_events", return_value=[]):
        return _build_dashboard(job)["vetoes"]


class TestNoVeto:
    def test_empty_lists_and_no_error(self, data_root):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)

        section = _vetoes_section(job)
        assert section == {
            "tasks": [],
            "vetoable_task_ids": dag_ids(tasks, "A", "B"),
            "unreachable_task_ids": [],
            "error": "",
        }


class TestOneVeto:
    def test_the_reason_verbatim_and_the_unreachable_set(self, data_root):
        tasks = [flight_task("A"), flight_task("B", "A"), flight_task("C", "A"),
                 flight_task("D", "B", "C")]
        job = _job(tasks)
        a_id, b_id, c_id, d_id = dag_ids(tasks, "A", "B", "C", "D")

        result = tv.veto_task_command(job, task_id=b_id, reason="known-bad approach for B",
                                      actor="alice")
        assert result["outcome"] == "vetoed"

        section = _vetoes_section(job)
        assert section["error"] == ""
        assert len(section["tasks"]) == 1
        entry = section["tasks"][0]
        assert entry["task_id"] == b_id
        assert entry["reason"] == "known-bad approach for B"
        assert entry["actor"] == "alice"
        assert entry["request_id"] == result["request_id"]
        assert entry["status_at_veto"] == "pending"
        assert entry["unreachable_task_ids"] == [d_id]
        assert entry["answer"] == ""
        assert section["unreachable_task_ids"] == [d_id]
        assert b_id not in section["vetoable_task_ids"]
        assert a_id in section["vetoable_task_ids"]
        assert c_id in section["vetoable_task_ids"]


class TestAnAnsweredVeto:
    def test_the_answer_s_option_is_reported(self, data_root):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        a_id, b_id = dag_ids(tasks, "A", "B")

        result = tv.veto_task_command(job, task_id=a_id, reason="stop A", actor="alice")
        assert result["outcome"] == "vetoed"
        answer, created = tv.record_veto_answer(
            job.job_id, result["request_id"], a_id, tv.ACCEPT_REDUCED_SCOPE, "alice", "")
        assert created is True

        section = _vetoes_section(job)
        assert len(section["tasks"]) == 1
        assert section["tasks"][0]["answer"] == tv.ACCEPT_REDUCED_SCOPE


class TestFinishedJobVetoableListEmpty:
    def test_a_completed_job_admits_no_new_veto(self, data_root):
        tasks = [flight_task("A", status=RunState.COMPLETED)]
        job = _job(tasks, state=RunState.COMPLETED)

        section = _vetoes_section(job)
        assert section["vetoable_task_ids"] == []
        assert section["tasks"] == []
        assert section["error"] == ""


class TestCorruptVetoFile:
    def test_a_task_veto_error_empties_every_list_and_sets_error(self, data_root):
        tasks = [flight_task("A")]
        job = _job(tasks)

        vdir = tv._sp.control_root() / "jobs" / job.job_id / tv.VETOED_TASKS_DIRNAME
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / tv._veto_filename("bogus")).write_text("not json")

        section = _vetoes_section(job)
        assert section["tasks"] == []
        assert section["vetoable_task_ids"] == []
        assert section["unreachable_task_ids"] == []
        assert section["error"] != ""
