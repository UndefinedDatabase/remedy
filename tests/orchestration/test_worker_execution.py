"""Tests for finalize and readiness after proposed tasks are materialized.

The worker execution path these tests once drove was deleted for finding R-0927; the
proposed-task finalize and readiness checks stay.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    add_proposed_task,
    approve_proposed_task,
    backend_readiness,
    can_finalize,
    do_materialize,
    evaluate_proposed_task,
)


def _setup(tmp_path, monkeypatch) -> tuple[Path, str]:
    root = tmp_path / "data"
    monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", root / "proposed_tasks")
    jid = str(uuid4())
    job = JobPlan(job_id=jid, job_title="worker-test")
    save_job_plan(job, root)
    return root, jid


class TestFinalizeAfterExecution:
    def test_finalize_false_with_pending_task(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Pending", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        ok, reason = can_finalize(jid, pending_task_count=1, root=root)
        assert ok is False
        assert "pending" in reason


class TestReadinessAfterExecution:
    def test_build_ready_with_pending_task(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Ready", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        report = backend_readiness(jid, root=root)
        assert report["build_readiness"]["ready"] is True
        assert report["finalize_readiness"]["ready"] is False
