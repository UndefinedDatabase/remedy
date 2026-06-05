"""Runtime subprocess tests for worker CLI through grouped entrypoint.

Proves the full backend loop from CLI boundary:
propose → evaluate → approve → materialize → enqueue → worker run → completed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Job
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    ProposedTaskStatus,
    add_proposed_task,
    approve_proposed_task,
    do_materialize,
    evaluate_proposed_task,
    propose_task_from_review_finding,
)
from packages.orchestration.storage import save_job


@pytest.fixture
def env(tmp_path):
    root = tmp_path / "data"
    jid = str(uuid4())
    job = Job(id=UUID(jid), name="worker-runtime-test")
    save_job(job, root)
    return root, jid


def _run(args: list[str], root: Path) -> subprocess.CompletedProcess:
    full_env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    return subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped"] + args,
        capture_output=True, text=True, timeout=10, env=full_env,
    )


class TestWorkerRunOnce:
    def test_fixture_worker_completes_task(self, env):
        root, jid = env
        t = propose_task_from_review_finding(jid, title="Worker task", risk="medium", root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        r = _run(["job", "enqueue", jid], root)
        assert r.returncode == 0, r.stderr

        r = _run(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        assert r.returncode == 0, r.stderr
        data = json.loads(r.stdout)
        assert data["action_taken"] == "task_completed"
        assert data["work_performed"] is True
        assert data["last_task_id"] != ""

        job = Job.model_validate_json((root / "jobs" / f"{jid}.json").read_text())
        assert any(t.status.value == "completed" for t in job.tasks)

    def test_second_run_no_pending(self, env):
        root, jid = env
        t = propose_task_from_review_finding(jid, title="Only task", risk="medium", root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        _run(["job", "enqueue", jid], root)
        _run(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)

        r = _run(["job", "enqueue", jid], root)
        r2 = _run(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        data = json.loads(r2.stdout)
        assert data["action_taken"] == "no_pending_tasks"

    def test_provider_none_no_work(self, env):
        root, jid = env
        r = _run(["job", "enqueue", jid], root)
        r2 = _run(["worker", "run", "--once", "--provider", "none", "--job", jid, "--json"], root)
        data = json.loads(r2.stdout)
        assert data["action_taken"] == "no_work_performed"

    def test_events_written(self, env):
        root, jid = env
        t = propose_task_from_review_finding(jid, title="Event task", risk="medium", root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        _run(["job", "enqueue", jid], root)
        _run(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)

        runs_dir = root / "runs" / jid
        if runs_dir.exists():
            event_files = sorted(runs_dir.glob("*.jsonl"))[:5]
            events = "".join(f.read_text() for f in event_files)
            assert "task_execution_started" in events
            assert "task_execution_completed" in events


class TestFullBackendLoop:
    def test_propose_to_worker_completion(self, env):
        root, jid = env
        t = propose_task_from_review_finding(jid, title="Full loop", risk="medium", root=root)

        r = _run(["propose", "evaluate", jid, "--json"], root)
        assert r.returncode == 0, r.stderr

        r = _run(["propose", "approve", jid, t.id, "--json"], root)
        assert r.returncode == 0, r.stderr

        r = _run(["propose", "materialize", jid, "--task-id", t.id, "--json"], root)
        assert r.returncode == 0, r.stderr

        r = _run(["job", "enqueue", jid], root)
        assert r.returncode == 0, r.stderr

        r = _run(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
        assert r.returncode == 0, r.stderr
        data = json.loads(r.stdout)
        assert data["action_taken"] == "task_completed"
        assert data["work_performed"] is True

        job = Job.model_validate_json((root / "jobs" / f"{jid}.json").read_text())
        assert len(job.tasks) == 1
        assert job.tasks[0].status.value == "completed"
        assert job.tasks[0].inputs.get("proposed_task_id") == t.id

        runs_dir = root / "runs" / jid
        if runs_dir.exists():
            event_files = sorted(runs_dir.glob("*.jsonl"))[:10]
            events = "".join(f.read_text() for f in event_files)
            assert "proposed_task_evaluated" in events
            assert "proposed_task_approved" in events
            assert "proposed_task_materialized" in events
            assert "task_execution_started" in events
            assert "task_execution_completed" in events
