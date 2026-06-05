"""Runtime subprocess tests for propose CLI through grouped entrypoint.

These tests exercise the real CLI boundary: argument parsing, handler dispatch,
and JSON output, via subprocess with temp REMEDY_DATA_DIR.
"""

from __future__ import annotations

import json
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
    save_proposed_tasks,
)
from packages.orchestration.storage import save_job


JOB_UUID = str(uuid4())


@pytest.fixture
def data_root(tmp_path):
    """Create temp data root with a real Job."""
    root = tmp_path / "data"
    jobs_dir = root / "jobs"
    jobs_dir.mkdir(parents=True)
    job = Job(id=UUID(JOB_UUID), name="runtime-test")
    save_job(job, root)
    return root


def _run_cli(*args: str, data_root: Path, timeout: int = 10) -> subprocess.CompletedProcess:
    env = {"REMEDY_DATA_DIR": str(data_root), "PATH": ""}
    return subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped"] + list(args),
        capture_output=True,
        text=True,
        timeout=timeout,
        env={**__import__("os").environ, **env},
    )


class TestSubprocessList:
    def test_list_empty(self, data_root):
        r = _run_cli("propose", "list", JOB_UUID, "--json", data_root=data_root)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["count"] == 0

    def test_list_with_tasks(self, data_root):
        add_proposed_task(JOB_UUID, ProposedTask(title="Test task"), root=data_root)
        r = _run_cli("propose", "list", JOB_UUID, "--json", data_root=data_root)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["count"] == 1


class TestSubprocessEvaluate:
    def test_evaluate_all(self, data_root):
        add_proposed_task(JOB_UUID, ProposedTask(title="Eval me", risk="medium"), root=data_root)
        r = _run_cli("propose", "evaluate", JOB_UUID, "--json", data_root=data_root)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["evaluated_count"] == 1


class TestSubprocessApproveRejectDefer:
    def test_approve(self, data_root):
        t = ProposedTask(title="Approve me", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_UUID, t, root=data_root)
        r = _run_cli("propose", "approve", JOB_UUID, t.id, "--json", data_root=data_root)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["approved"] is True

    def test_reject(self, data_root):
        t = ProposedTask(title="Reject me", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_UUID, t, root=data_root)
        r = _run_cli("propose", "reject", JOB_UUID, t.id, "--json", data_root=data_root)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["rejected"] is True

    def test_defer(self, data_root):
        t = ProposedTask(title="Defer me", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_UUID, t, root=data_root)
        r = _run_cli("propose", "defer", JOB_UUID, t.id, "--json", data_root=data_root)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["deferred"] is True


class TestSubprocessMaterialize:
    def test_materialize_creates_job_task(self, data_root):
        t = ProposedTask(title="Materialize", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        add_proposed_task(JOB_UUID, t, root=data_root)
        r = _run_cli("propose", "materialize", JOB_UUID, "--task-id", t.id, "--json", data_root=data_root)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["materialized_count"] == 1
        job = Job.model_validate_json((data_root / "jobs" / f"{JOB_UUID}.json").read_text())
        assert len(job.tasks) == 1


class TestSubprocessErrors:
    def test_missing_job_mutation_fails(self, data_root):
        fake_uuid = str(uuid4())
        r = _run_cli("propose", "approve", fake_uuid, "nope", "--json", data_root=data_root)
        assert r.returncode != 0
        data = json.loads(r.stdout)
        assert "error" in data

    def test_corrupt_store_safe(self, data_root):
        pt_dir = data_root / "proposed_tasks"
        pt_dir.mkdir(parents=True, exist_ok=True)
        (pt_dir / f"{JOB_UUID}.json").write_text("corrupt")
        r = _run_cli("propose", "list", JOB_UUID, "--json", data_root=data_root)
        assert r.returncode != 0
        data = json.loads(r.stdout)
        assert data.get("degraded") is True

    def test_no_traceback_in_output(self, data_root):
        r = _run_cli("propose", "show", JOB_UUID, "nonexistent", "--json", data_root=data_root)
        assert "Traceback" not in r.stdout
        assert "Traceback" not in r.stderr


class TestSubprocessFullFlow:
    def test_end_to_end(self, data_root):
        t = ProposedTask(title="E2E task", risk="medium")
        add_proposed_task(JOB_UUID, t, root=data_root)

        r = _run_cli("propose", "list", JOB_UUID, "--json", data_root=data_root)
        assert json.loads(r.stdout)["count"] == 1

        r = _run_cli("propose", "evaluate", JOB_UUID, "--json", data_root=data_root)
        assert r.returncode == 0

        r = _run_cli("propose", "approve", JOB_UUID, t.id, "--json", data_root=data_root)
        assert json.loads(r.stdout)["approved"] is True

        r = _run_cli("propose", "materialize", JOB_UUID, "--task-id", t.id, "--json", data_root=data_root)
        assert json.loads(r.stdout)["materialized_count"] == 1

        job = Job.model_validate_json((data_root / "jobs" / f"{JOB_UUID}.json").read_text())
        assert len(job.tasks) == 1

        runs_dir = data_root / "runs" / JOB_UUID
        if runs_dir.exists():
            events = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
            assert "proposed_task_evaluated" in events
            assert "proposed_task_approved" in events
            assert "proposed_task_materialized" in events
