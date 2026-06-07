"""Runtime subprocess tests for worker CLI through grouped entrypoint.

IMPORTANT: This file must NOT import packages.orchestration.proposed_tasks
or any module that uses fcntl.flock. All setup via runtime_helpers JSON writes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.cli.runtime_helpers import (
    assert_no_leftover_locks,
    create_test_env,
    create_proposed_task,
    run_grouped_cli,
    run_json,
    read_events,
)


@pytest.fixture
def env(tmp_path):
    root, jid = create_test_env(tmp_path)
    yield root, jid
    assert_no_leftover_locks(root)


def _prepare_via_cli(root: Path, jid: str) -> str:
    """Create, evaluate, approve, materialize one task via CLI subprocess."""
    tid = create_proposed_task(root, jid, title="Worker task", risk="medium")
    run_json(["propose", "evaluate", jid, "--json"], root)
    run_json(["propose", "approve", jid, tid, "--json"], root)
    run_json(["propose", "materialize", jid, "--task-id", tid, "--json"], root)
    return tid


class TestWorkerRunOnce:
    def test_fixture_worker_completes_task(self, env):
        root, jid = env
        _prepare_via_cli(root, jid)
        run_grouped_cli(["job", "enqueue", jid], root)
        data = run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        assert data["action_taken"] == "task_completed"
        assert data["work_performed"] is True
        assert data["last_task_id"] != ""
        job_data = json.loads((root / "jobs" / f"{jid}.json").read_text())
        assert any(t.get("status") == "completed" for t in job_data["tasks"])

    def test_second_run_no_pending(self, env):
        root, jid = env
        _prepare_via_cli(root, jid)
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
        _prepare_via_cli(root, jid)
        run_grouped_cli(["job", "enqueue", jid], root)
        run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        events = read_events(root, jid)
        assert "task_execution_started" in events
        assert "task_execution_completed" in events

    def test_budget_max_steps_zero_blocks(self, env):
        root, jid = env
        _prepare_via_cli(root, jid)
        run_grouped_cli(["job", "enqueue", jid], root)
        data = run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--max-steps", "0", "--json"], root)
        assert data["budget_status"] == "no_budget_set"
        assert data["action_taken"] == "blocked"


class TestFullBackendLoop:
    def test_propose_to_worker_completion(self, env):
        root, jid = env
        tid = create_proposed_task(root, jid, title="Full loop", risk="medium")

        run_json(["propose", "evaluate", jid, "--json"], root)
        run_json(["propose", "approve", jid, tid, "--json"], root)
        run_json(["propose", "materialize", jid, "--task-id", tid, "--json"], root)
        run_grouped_cli(["job", "enqueue", jid], root)
        data = run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)

        assert data["action_taken"] == "task_completed"
        assert data["work_performed"] is True

        job_data = json.loads((root / "jobs" / f"{jid}.json").read_text())
        assert len(job_data["tasks"]) == 1
        assert job_data["tasks"][0]["status"] == "completed"

        events = read_events(root, jid)
        assert "proposed_task_evaluated" in events
        assert "proposed_task_approved" in events
        assert "proposed_task_materialized" in events
        assert "task_execution_started" in events
        assert "task_execution_completed" in events
