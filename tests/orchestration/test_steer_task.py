"""F030 T002 — `steering.steer_task_command`, DECISION F030 D2.

The one function `job.steer` on both doors calls: refuses an unusable text, an ended job, an
unknown task and a task that will not run again, in that order, and otherwise records the note
addressed to the task. `steering_overview`'s `addressed_to` and `not_taken_in` reading — over
a task known to have finished while the job itself still runs — is proved here too.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from packages.core.models import RunState
from packages.orchestration import pingpong_job as pj
from packages.orchestration import steering as ST
from packages.orchestration import task_veto as tv
from tests.orchestration.test_dag_schedule import flight_task

NOW = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def root(tmp_path):
    return tmp_path / "remedy_data"


def _job(tasks, state: RunState = RunState.RUNNING) -> pj.JobPlan:
    return pj.JobPlan(job_title="steer test", tasks=tasks, state=state)


class TestSteerableStatusesPinned:
    def test_steerable_statuses_equal_the_vetoable_set(self):
        """S1: pinned by a test rather than imported, so `steering.py` reaches no veto code."""
        assert ST.STEERABLE_TASK_STATUSES == frozenset(tv.VETOABLE_TASK_STATUSES)


class TestRefusalOrder:
    def test_an_unusable_text_refuses_first_and_nothing_is_written(self, root):
        job = _job([flight_task("T1")])
        t1 = job.tasks[0].task_id
        result = ST.steer_task_command(job, t1, "   ", channel="cli", root=root, now=NOW)
        assert result == {"outcome": "refused", "code": "invalid_message",
                          "detail": "the message is empty", "task_id": t1}
        assert ST.list_steering_messages(job.job_id, root) == []

    def test_an_ended_job_naming_an_unknown_task_refuses_job_not_steerable(self, root):
        """The refusal order: the job's own state is checked before the task is looked up."""
        job = _job([flight_task("T1")], state=RunState.COMPLETED)
        result = ST.steer_task_command(job, "no-such-task", "hello", channel="cli", root=root,
                                       now=NOW)
        assert result["code"] == "job_not_steerable"
        assert result["detail"] == f"job {job.job_id} has ended (completed); no run will read a note"
        assert ST.list_steering_messages(job.job_id, root) == []

    def test_an_unknown_task_of_a_running_job_refuses_unknown_task(self, root):
        job = _job([flight_task("T1")])
        result = ST.steer_task_command(job, "no-such-task", "hello", channel="cli", root=root,
                                       now=NOW)
        assert result["code"] == "unknown_task"
        assert "no-such-task" in result["detail"]
        assert ST.list_steering_messages(job.job_id, root) == []

    def test_over_ten_tasks_names_the_first_ten_and_counts_the_rest(self, root):
        tasks = [flight_task(f"T{i}") for i in range(1, 12)]
        job = _job(tasks)
        result = ST.steer_task_command(job, "no-such-task", "hello", channel="cli", root=root,
                                       now=NOW)
        assert result["code"] == "unknown_task"
        ids = [t.task_id for t in tasks]
        assert result["detail"] == (
            f"there is no task 'no-such-task' in job {job.job_id}; its tasks are: "
            f"{', '.join(ids[:10])} and 1 more")

    def test_a_task_that_will_not_run_again_refuses_task_not_steerable(self, root):
        task = flight_task("T1")
        task.status = pj.TASK_PASSED
        job = _job([task])
        t1 = job.tasks[0].task_id
        result = ST.steer_task_command(job, t1, "hello", channel="cli", root=root, now=NOW)
        assert result == {"outcome": "refused", "code": "task_not_steerable",
                          "detail": f"task {t1} is passed; a note reaches only a task that "
                                    f"can still run",
                          "task_id": t1}
        assert ST.list_steering_messages(job.job_id, root) == []


class TestAcceptance:
    @pytest.mark.parametrize("status", ["pending", "running", "blocked", "failed", "skipped"])
    def test_each_steerable_status_accepts_and_the_record_carries_the_task_and_channel(
            self, root, status):
        task = flight_task("T1")
        task.status = status
        job = _job([task])
        t1 = job.tasks[0].task_id
        result = ST.steer_task_command(job, t1, "Use pnpm.", channel="cockpit", root=root,
                                       now=NOW)
        assert result["outcome"] == "accepted"
        assert result["task_id"] == t1
        assert result["message_id"] == result["request_id"]
        [record] = ST.list_steering_messages(job.job_id, root)
        assert record["message_id"] == result["message_id"]
        assert record["task_id"] == t1
        assert record["channel"] == "cockpit"
        assert record["text"] == "Use pnpm."
        assert result["received_at"] == record["received_at"]
        assert result["record_sha256"] == record["record_sha256"]

    @pytest.mark.parametrize("status", ["passed", "applied_to_job_workspace", "split", "vetoed"])
    def test_a_status_outside_the_steerable_set_refuses_and_writes_nothing(self, root, status):
        task = flight_task("T1")
        task.status = status
        job = _job([task])
        t1 = job.tasks[0].task_id
        result = ST.steer_task_command(job, t1, "Use pnpm.", channel="cli", root=root, now=NOW)
        assert result == {"outcome": "refused", "code": "task_not_steerable",
                          "detail": f"task {t1} is {status}; a note reaches only a task that "
                                    f"can still run",
                          "task_id": t1}
        assert ST.list_steering_messages(job.job_id, root) == []


class TestOverviewAddressedToAndNotTakenIn:
    def test_addressed_to_and_not_taken_in_for_a_finished_task_while_the_job_still_runs(
            self, root):
        task1 = flight_task("T1")
        task2 = flight_task("T2")
        job = _job([task1, task2])
        t1, t2 = job.tasks[0].task_id, job.tasks[1].task_id
        ST.steer_task_command(job, t1, "note for T1", channel="cli", root=root, now=NOW)
        ST.record_steering_message(job.job_id, "job-wide note", job_state="running",
                                   channel="cli", root=root, now=NOW)
        rows = ST.steering_overview(job.job_id, "running", root,
                                    task_statuses={t1: "passed", t2: "pending"})
        by_id = {r["message_id"]: r for r in rows}
        assert by_id["sm-0001"]["addressed_to"] == t1
        assert by_id["sm-0001"]["status"] == "not_taken_in"
        # A job-wide row reads exactly as it did before this reading existed.
        assert by_id["sm-0002"]["addressed_to"] == ""
        assert by_id["sm-0002"]["status"] == "waiting"

    def test_an_addressed_note_whose_task_can_still_run_waits_like_today(self, root):
        task1 = flight_task("T1")
        job = _job([task1])
        t1 = job.tasks[0].task_id
        ST.steer_task_command(job, t1, "note for T1", channel="cli", root=root, now=NOW)
        rows = ST.steering_overview(job.job_id, "running", root, task_statuses={t1: "pending"})
        assert rows[0]["status"] == "waiting"
        assert rows[0]["addressed_to"] == t1

    def test_with_no_task_statuses_an_addressed_note_reads_waiting_while_the_job_runs(self, root):
        task1 = flight_task("T1")
        job = _job([task1])
        t1 = job.tasks[0].task_id
        ST.steer_task_command(job, t1, "note for T1", channel="cli", root=root, now=NOW)
        rows = ST.steering_overview(job.job_id, "running", root)
        assert rows[0]["status"] == "waiting"
        assert rows[0]["addressed_to"] == t1
