"""Runtime subprocess tests for worker CLI through grouped entrypoint."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID

import pytest

from packages.core.models import Job
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    approve_proposed_task,
    do_materialize,
    evaluate_proposed_task,
    propose_task_from_review_finding,
)
from tests.cli.runtime_helpers import create_test_env, run_grouped_cli, run_json, read_events, assert_no_leftover_locks


@pytest.fixture
def env(tmp_path):
    root, jid = create_test_env(tmp_path)
    yield root, jid
    assert_no_leftover_locks(root)


def _prepare_materialized_task(root: Path, jid: str) -> str:
    """Create, evaluate, approve, materialize one task. Returns proposed task id."""
    t = propose_task_from_review_finding(jid, title="Worker task", risk="medium", root=root)
    evaluate_proposed_task(jid, t.id, root=root)
    approve_proposed_task(jid, t.id, root=root)
    do_materialize(jid, t.id, root=root)
    return t.id


class TestWorkerRunOnce:
    def test_fixture_worker_completes_task(self, env):
        root, jid = env
        _prepare_materialized_task(root, jid)
        run_grouped_cli(["job", "enqueue", jid], root)
        data = run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        assert data["action_taken"] == "task_completed"
        assert data["work_performed"] is True
        assert data["last_task_id"] != ""
        job = Job.model_validate_json((root / "jobs" / f"{jid}.json").read_text())
        assert any(t.status.value == "completed" for t in job.tasks)

    def test_second_run_no_pending(self, env):
        root, jid = env
        _prepare_materialized_task(root, jid)
        run_grouped_cli(["job", "enqueue", jid], root)
        run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        run_grouped_cli(["job", "enqueue", jid], root)
        data = run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        assert data["action_taken"] == "no_pending_tasks"

    def test_provider_none_no_work(self, env):
        root, jid = env
        run_grouped_cli(["job", "enqueue", jid], root)
        data = run_json(["worker", "run", "--once", "--provider", "none", "--job", jid, "--json"], root)
        assert data["action_taken"] == "no_work_performed"

    def test_events_written(self, env):
        root, jid = env
        _prepare_materialized_task(root, jid)
        run_grouped_cli(["job", "enqueue", jid], root)
        run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        events = read_events(root, jid)
        assert "task_execution_started" in events
        assert "task_execution_completed" in events

    def test_budget_max_steps_zero_blocks(self, env):
        root, jid = env
        _prepare_materialized_task(root, jid)
        run_grouped_cli(["job", "enqueue", jid], root)
        data = run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--max-steps", "0", "--json"], root)
        assert data["budget_status"] == "no_budget_set"
        assert data["action_taken"] == "blocked"


class TestFullBackendLoop:
    def test_propose_to_worker_completion(self, env):
        root, jid = env
        t = propose_task_from_review_finding(jid, title="Full loop", risk="medium", root=root)

        run_json(["propose", "evaluate", jid, "--json"], root)
        run_json(["propose", "approve", jid, t.id, "--json"], root)
        run_json(["propose", "materialize", jid, "--task-id", t.id, "--json"], root)
        run_grouped_cli(["job", "enqueue", jid], root)
        data = run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)

        assert data["action_taken"] == "task_completed"
        assert data["work_performed"] is True

        job = Job.model_validate_json((root / "jobs" / f"{jid}.json").read_text())
        assert len(job.tasks) == 1
        assert job.tasks[0].status.value == "completed"
        assert job.tasks[0].inputs.get("proposed_task_id") == t.id

        events = read_events(root, jid)
        assert "proposed_task_evaluated" in events
        assert "proposed_task_approved" in events
        assert "proposed_task_materialized" in events
        assert "task_execution_started" in events
        assert "task_execution_completed" in events
