"""Runtime subprocess tests for propose CLI through grouped entrypoint.

Each test gets its own UUID and data root. No shared state.
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
)
from packages.orchestration.storage import save_job


@pytest.fixture
def env(tmp_path):
    """Create isolated data root with unique Job."""
    root = tmp_path / "data"
    job_id = str(uuid4())
    job = Job(id=UUID(job_id), name="runtime-test")
    save_job(job, root)
    return root, job_id


def _run(args: list[str], root: Path) -> subprocess.CompletedProcess:
    full_env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    return subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped"] + args,
        capture_output=True, text=True, timeout=10, env=full_env,
    )


class TestSubprocessList:
    def test_list_empty(self, env):
        root, jid = env
        r = _run(["propose", "list", jid, "--json"], root)
        assert r.returncode == 0
        assert json.loads(r.stdout)["count"] == 0

    def test_list_with_tasks(self, env):
        root, jid = env
        add_proposed_task(jid, ProposedTask(title="Test"), root=root)
        r = _run(["propose", "list", jid, "--json"], root)
        assert json.loads(r.stdout)["count"] == 1


class TestSubprocessEvaluate:
    def test_evaluate_all(self, env):
        root, jid = env
        add_proposed_task(jid, ProposedTask(title="Eval me", risk="medium"), root=root)
        r = _run(["propose", "evaluate", jid, "--json"], root)
        assert r.returncode == 0
        assert json.loads(r.stdout)["evaluated_count"] == 1


class TestSubprocessTransitions:
    def test_approve(self, env):
        root, jid = env
        t = ProposedTask(title="Approve", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(jid, t, root=root)
        r = _run(["propose", "approve", jid, t.id, "--json"], root)
        assert json.loads(r.stdout)["approved"] is True

    def test_reject(self, env):
        root, jid = env
        t = ProposedTask(title="Reject", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(jid, t, root=root)
        r = _run(["propose", "reject", jid, t.id, "--json"], root)
        assert json.loads(r.stdout)["rejected"] is True

    def test_defer(self, env):
        root, jid = env
        t = ProposedTask(title="Defer", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(jid, t, root=root)
        r = _run(["propose", "defer", jid, t.id, "--json"], root)
        assert json.loads(r.stdout)["deferred"] is True


class TestSubprocessMaterialize:
    def test_materialize_creates_job_task(self, env):
        root, jid = env
        t = ProposedTask(title="Mat", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        add_proposed_task(jid, t, root=root)
        r = _run(["propose", "materialize", jid, "--task-id", t.id, "--json"], root)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["materialized_count"] == 1
        job = Job.model_validate_json((root / "jobs" / f"{jid}.json").read_text())
        assert len(job.tasks) == 1


class TestSubprocessErrors:
    def test_missing_job_fails(self, env):
        root, _ = env
        fake = str(uuid4())
        r = _run(["propose", "approve", fake, "nope", "--json"], root)
        assert r.returncode != 0
        assert "error" in json.loads(r.stdout)

    def test_corrupt_store_safe(self, env):
        root, jid = env
        pt_dir = root / "proposed_tasks"
        pt_dir.mkdir(parents=True, exist_ok=True)
        (pt_dir / f"{jid}.json").write_text("corrupt")
        r = _run(["propose", "list", jid, "--json"], root)
        assert r.returncode != 0
        assert json.loads(r.stdout).get("degraded") is True

    def test_no_traceback(self, env):
        root, jid = env
        r = _run(["propose", "show", jid, "nonexistent", "--json"], root)
        assert "Traceback" not in r.stdout
        assert "Traceback" not in r.stderr


class TestSubprocessFullFlow:
    def test_end_to_end(self, env):
        root, jid = env
        t = ProposedTask(title="E2E", risk="medium")
        add_proposed_task(jid, t, root=root)

        r = _run(["propose", "list", jid, "--json"], root)
        assert json.loads(r.stdout)["count"] == 1

        r = _run(["propose", "evaluate", jid, "--json"], root)
        assert r.returncode == 0

        r = _run(["propose", "approve", jid, t.id, "--json"], root)
        assert json.loads(r.stdout)["approved"] is True

        r = _run(["propose", "materialize", jid, "--task-id", t.id, "--json"], root)
        assert json.loads(r.stdout)["materialized_count"] == 1

        job = Job.model_validate_json((root / "jobs" / f"{jid}.json").read_text())
        assert len(job.tasks) == 1

        runs_dir = root / "runs" / jid
        if runs_dir.exists():
            events = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
            assert "proposed_task_evaluated" in events
            assert "proposed_task_approved" in events
            assert "proposed_task_materialized" in events
