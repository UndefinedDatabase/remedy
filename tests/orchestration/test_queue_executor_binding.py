"""F048 T003c — the opt-in executor binding, end to end.

An idle multi-cycle run may take the next entry from its project's queue and turn it into
a NORMAL job. Three properties matter, and each has a test:

  * OFF BY DEFAULT. Without the opt-in nothing is claimed, nothing is created, and the
    loop's result is shaped exactly as it was before the queue existed.
  * The queued goal becomes a normal PLANNED job — the same thing `job create` +
    `job plan` produce — and the entry is marked done with that job's id.
  * APPROVAL IS UNCHANGED. The binding stops at PLANNED: no task is executed, and nothing
    behaves as though --yes had been passed.

A failing pull is not allowed to strand an entry: the entry ends `failed`, with the
reason, rather than `claimed` by a consumer that has moved on.
"""
from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from packages.core.models import Job, RunState
from packages.orchestration import job_queue as queue
from packages.orchestration.config import reset_config
from packages.orchestration.long_run_executor import (
    QUEUE_PULL_FAILED,
    QUEUE_PULL_PLANNED,
    CycleLimits,
    queue_binding_enabled,
    run_cycles,
)
from packages.orchestration.storage import load_job

PROJECT = "proj-binding"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Nothing here touches the repository's real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir(parents=True)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    reset_config()
    yield data_dir
    reset_config()


@pytest.fixture
def binding_on(monkeypatch):
    monkeypatch.setenv("REMEDY_QUEUE_EXECUTOR_BINDING", "true")
    reset_config()
    assert queue_binding_enabled() is True


def _idle_job() -> Job:
    """A job with no tasks: the loop finds nothing ready and ends idle."""
    return Job(name="host job", user_prompt="host job", state=RunState.PENDING,
               project_id=PROJECT)


def _never_called(context):  # pragma: no cover - a called provider is the failure
    raise AssertionError("the binding must not make provider calls")


def _run_idle(job: Job):
    return run_cycles(job, CycleLimits(max_cycles=1), _never_called,
                      record_evidence=False, record_checkpoint=False)


class TestOffByDefault:
    def test_nothing_is_claimed_without_the_opt_in(self, isolate_data_root):
        entry = queue.enqueue(PROJECT, "queued goal", 0)

        result = _run_idle(_idle_job())

        assert queue_binding_enabled() is False
        assert result.queue_pull is None
        assert "queue_pull" not in result.to_json()
        assert queue.load_entry(PROJECT, entry.id).status == queue.STATUS_QUEUED
        assert queue.claim_holder(PROJECT, entry.id) == ""

    def test_an_enabled_binding_with_an_empty_queue_does_nothing(self, binding_on):
        result = _run_idle(_idle_job())

        assert result.queue_pull is None
        assert "queue_pull" not in result.to_json()

    def test_a_job_without_a_project_never_pulls(self, binding_on):
        queue.enqueue(PROJECT, "queued goal", 0)

        result = _run_idle(Job(name="unscoped", user_prompt="unscoped",
                               state=RunState.PENDING))

        assert result.queue_pull is None


class TestEndToEnd:
    def test_a_queued_goal_becomes_a_planned_job_and_completes_its_entry(self, binding_on):
        entry = queue.enqueue(PROJECT, "write the queue docs", 3)

        result = _run_idle(_idle_job())

        assert result.queue_pull is not None
        assert result.queue_pull.status == QUEUE_PULL_PLANNED
        assert result.queue_pull.entry_id == entry.id

        # The entry is done, and it names the job it became.
        after = queue.load_entry(PROJECT, entry.id)
        assert after.status == queue.STATUS_DONE
        assert after.result_job_id == result.queue_pull.job_id
        assert queue.claim_holder(PROJECT, entry.id) == ""

        # The job exists, is a normal job for this project, and has a plan.
        queued_job = load_job(UUID(result.queue_pull.job_id))
        assert queued_job.project_id == PROJECT
        assert queued_job.user_prompt == "write the queue docs"
        assert queued_job.tasks, "a pulled goal must arrive planned, not empty"
        assert queued_job.state == RunState.PLANNED
        assert queued_job.metadata["queue_entry_id"] == entry.id

        # And the result is serialisable with the pull visible.
        assert result.to_json()["queue_pull"]["status"] == QUEUE_PULL_PLANNED

    def test_the_highest_priority_entry_is_the_one_pulled(self, binding_on):
        queue.enqueue(PROJECT, "low goal", 0)
        high = queue.enqueue(PROJECT, "high goal", 9)

        result = _run_idle(_idle_job())

        assert result.queue_pull is not None
        assert result.queue_pull.entry_id == high.id
        assert queue.load_entry(PROJECT, high.id).status == queue.STATUS_DONE

    def test_one_idle_run_takes_exactly_one_entry(self, binding_on):
        first = queue.enqueue(PROJECT, "first goal", 5)
        second = queue.enqueue(PROJECT, "second goal", 1)

        result = _run_idle(_idle_job())

        assert result.queue_pull is not None
        assert result.queue_pull.entry_id == first.id
        assert queue.load_entry(PROJECT, second.id).status == queue.STATUS_QUEUED

    def test_a_goal_file_reference_is_read_into_the_job(self, binding_on, tmp_path):
        goal_file = tmp_path / "goal.md"
        goal_file.write_text("Ship the executor binding.\n", encoding="utf-8")
        entry = queue.enqueue(PROJECT, goal_path=str(goal_file))

        result = _run_idle(_idle_job())

        assert result.queue_pull is not None
        assert result.queue_pull.status == QUEUE_PULL_PLANNED
        queued_job = load_job(UUID(result.queue_pull.job_id))
        assert queued_job.user_prompt == "Ship the executor binding."
        assert queue.load_entry(PROJECT, entry.id).status == queue.STATUS_DONE


class TestApprovalIsUnchanged:
    def test_the_pulled_job_stops_at_planned_and_runs_nothing(self, binding_on):
        """PLANNED, not RUNNING and not COMPLETED: the operator's gate is still ahead."""
        queue.enqueue(PROJECT, "do something significant", 0)

        result = _run_idle(_idle_job())

        assert result.queue_pull is not None
        queued_job = load_job(UUID(result.queue_pull.job_id))
        assert queued_job.state == RunState.PLANNED
        assert all(task.status == RunState.PENDING for task in queued_job.tasks)
        # _never_called would have raised; asserting it plainly documents the rule.
        assert queued_job.artifacts, "planning output is the only thing produced"


class TestFailurePath:
    def test_an_unreadable_goal_file_fails_the_entry_instead_of_stranding_it(
            self, binding_on, tmp_path):
        entry = queue.enqueue(PROJECT, goal_path=str(tmp_path / "missing.md"))

        result = _run_idle(_idle_job())

        assert result.queue_pull is not None
        assert result.queue_pull.status == QUEUE_PULL_FAILED
        assert "could not be read" in result.queue_pull.reason

        after = queue.load_entry(PROJECT, entry.id)
        assert after.status == queue.STATUS_FAILED
        assert "could not be read" in after.failure_reason
        assert queue.claim_holder(PROJECT, entry.id) == ""
