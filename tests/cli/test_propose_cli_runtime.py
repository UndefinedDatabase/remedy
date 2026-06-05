"""Runtime subprocess tests for propose CLI through grouped entrypoint."""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.core.models import Job
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    ProposedTaskStatus,
    add_proposed_task,
)
from tests.cli.runtime_helpers import create_test_env, run_grouped_cli, run_json, read_events, assert_no_leftover_locks


@pytest.fixture
def env(tmp_path):
    root, jid = create_test_env(tmp_path)
    yield root, jid
    assert_no_leftover_locks(root)


class TestSubprocessList:
    def test_list_empty(self, env):
        root, jid = env
        data = run_json(["propose", "list", jid, "--json"], root)
        assert data["count"] == 0

    def test_list_with_tasks(self, env):
        root, jid = env
        add_proposed_task(jid, ProposedTask(title="Test"), root=root)
        data = run_json(["propose", "list", jid, "--json"], root)
        assert data["count"] == 1


class TestSubprocessEvaluate:
    def test_evaluate_all(self, env):
        root, jid = env
        add_proposed_task(jid, ProposedTask(title="Eval me", risk="medium"), root=root)
        data = run_json(["propose", "evaluate", jid, "--json"], root)
        assert data["evaluated_count"] == 1


class TestSubprocessTransitions:
    def test_approve(self, env):
        root, jid = env
        t = ProposedTask(title="Approve", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(jid, t, root=root)
        data = run_json(["propose", "approve", jid, t.id, "--json"], root)
        assert data["approved"] is True

    def test_reject(self, env):
        root, jid = env
        t = ProposedTask(title="Reject", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(jid, t, root=root)
        data = run_json(["propose", "reject", jid, t.id, "--json"], root)
        assert data["rejected"] is True

    def test_defer(self, env):
        root, jid = env
        t = ProposedTask(title="Defer", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(jid, t, root=root)
        data = run_json(["propose", "defer", jid, t.id, "--json"], root)
        assert data["deferred"] is True


class TestSubprocessMaterialize:
    def test_materialize_creates_job_task(self, env):
        root, jid = env
        t = ProposedTask(title="Mat", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        add_proposed_task(jid, t, root=root)
        data = run_json(["propose", "materialize", jid, "--task-id", t.id, "--json"], root)
        assert data["materialized_count"] == 1
        job = Job.model_validate_json((root / "jobs" / f"{jid}.json").read_text())
        assert len(job.tasks) == 1


class TestSubprocessErrors:
    def test_missing_job_fails(self, env):
        root, _ = env
        fake = str(uuid4())
        r = run_grouped_cli(["propose", "approve", fake, "nope", "--json"], root)
        assert r.returncode != 0
        assert "error" in json.loads(r.stdout)

    def test_corrupt_store_safe(self, env):
        root, jid = env
        pt_dir = root / "proposed_tasks"
        pt_dir.mkdir(parents=True, exist_ok=True)
        (pt_dir / f"{jid}.json").write_text("corrupt")
        r = run_grouped_cli(["propose", "list", jid, "--json"], root)
        assert r.returncode != 0
        assert json.loads(r.stdout).get("degraded") is True

    def test_no_traceback(self, env):
        root, jid = env
        r = run_grouped_cli(["propose", "show", jid, "nonexistent", "--json"], root)
        assert "Traceback" not in r.stdout
        assert "Traceback" not in r.stderr


class TestSubprocessFullFlow:
    def test_end_to_end(self, env):
        root, jid = env
        t = ProposedTask(title="E2E", risk="medium")
        add_proposed_task(jid, t, root=root)

        assert run_json(["propose", "list", jid, "--json"], root)["count"] == 1
        run_json(["propose", "evaluate", jid, "--json"], root)
        assert run_json(["propose", "approve", jid, t.id, "--json"], root)["approved"] is True
        assert run_json(["propose", "materialize", jid, "--task-id", t.id, "--json"], root)["materialized_count"] == 1

        job = Job.model_validate_json((root / "jobs" / f"{jid}.json").read_text())
        assert len(job.tasks) == 1

        events = read_events(root, jid)
        assert "proposed_task_evaluated" in events
        assert "proposed_task_approved" in events
        assert "proposed_task_materialized" in events
