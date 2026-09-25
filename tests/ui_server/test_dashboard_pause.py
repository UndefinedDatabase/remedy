"""F025 R5, DECISION F025 D3 clause 1 — the dashboard's `pause` object (U1).

`_build_dashboard` gains `pause`: `record` (the job's own pause record while
its state is `paused`, else `{}`), `requested` (a job-scope pause pending, no
safe point has served yet — `pause_control.pause_requested` is not None),
`paused_task_ids` (the paused tasks that are still pending, in plan order —
a done task's pause is omitted) and `error` (`""`, or the text of a
`PauseControlError` or `StopControlError` met while reading, in which case
the other three keep their empty values). It never raises for them. Reads a
real control root through `pause_control`, exactly as the CLI and the write
door do (`packages/orchestration/pause_control.py`).
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest

from packages.core.models import RunState
from packages.orchestration import pause_control as pc
from packages.orchestration.pingpong_job import JOB_PAUSED, JobPlan, TaskEntry


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


def _job(**overrides) -> JobPlan:
    defaults: dict = dict(
        job_id=str(uuid4()),
        job_title="pause-dashboard-job",
        user_prompt="test prompt",
        tasks=[TaskEntry(title="task 1")],
        state=RunState.RUNNING,
        metadata={"target_repo": "."},
    )
    defaults.update(overrides)
    return JobPlan(**defaults)


def _pause_section(job) -> dict:
    from packages.orchestration.ui_server import _build_dashboard
    with patch("packages.orchestration.ui_server._load_events", return_value=[]):
        return _build_dashboard(job)["pause"]


class TestTheRecord:
    def test_reads_the_jobs_own_pause_record_while_parked(self, data_root):
        record = {"scope": "job", "request_id": "req-1", "reason": "operator"}
        job = _job(state=JOB_PAUSED, pause=dict(record))

        section = _pause_section(job)
        assert section["record"] == record
        assert section["error"] == ""

    def test_is_empty_when_the_job_is_not_paused(self, data_root):
        job = _job(state=RunState.RUNNING, pause={})

        section = _pause_section(job)
        assert section["record"] == {}


class TestRequested:
    def test_true_when_a_job_pause_is_pending(self, data_root):
        job = _job()
        pc.request_pause(job.job_id, "operator pause", "cli")

        section = _pause_section(job)
        assert section["requested"] is True

    def test_false_when_nothing_is_pending(self, data_root):
        job = _job()

        section = _pause_section(job)
        assert section["requested"] is False


class TestPausedTaskIds:
    def test_omits_a_done_task_and_keeps_plan_order(self, data_root):
        t1 = TaskEntry(title="task 1", status="pending")
        t2 = TaskEntry(title="task 2", status="completed")
        t3 = TaskEntry(title="task 3", status="pending")
        job = _job(tasks=[t1, t2, t3])

        # Pause task 3 first, then task 1 and the (already done) task 2 — the
        # dashboard must report them in PLAN order, not request order, and
        # must never name task 2, whose task is done.
        pc.request_task_pause(job.job_id, t3.task_id)
        pc.request_task_pause(job.job_id, t1.task_id)
        pc.request_task_pause(job.job_id, t2.task_id)

        section = _pause_section(job)
        assert section["paused_task_ids"] == [t1.task_id, t3.task_id]

    def test_is_empty_with_nothing_paused(self, data_root):
        job = _job()

        section = _pause_section(job)
        assert section["paused_task_ids"] == []


class TestError:
    def test_a_pause_control_error_is_reported_without_raising(self, data_root, monkeypatch):
        def raising_pause_requested(job_id, **kwargs):
            raise pc.PauseControlError("simulated control-root failure")

        monkeypatch.setattr(pc, "pause_requested", raising_pause_requested)
        job = _job(state=JOB_PAUSED, pause={"scope": "job", "request_id": "req-1"})

        section = _pause_section(job)
        assert section["error"] == "simulated control-root failure"
        assert section["record"] == {}
        assert section["requested"] is False
        assert section["paused_task_ids"] == []

    def test_a_stop_control_error_is_reported_without_raising(self, data_root, monkeypatch):
        from packages.orchestration.safe_points import StopControlError

        def raising_paused_tasks(job_id, **kwargs):
            raise StopControlError("simulated control-root failure")

        monkeypatch.setattr(pc, "paused_tasks", raising_paused_tasks)
        job = _job()

        section = _pause_section(job)
        assert section["error"] == "simulated control-root failure"
        assert section["record"] == {}
        assert section["requested"] is False
        assert section["paused_task_ids"] == []
