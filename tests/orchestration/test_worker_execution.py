"""Tests for worker executing real materialized Job.tasks through task_execution port."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID, uuid4

from packages.core.models import Job, RunState, Task
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    add_proposed_task,
    approve_proposed_task,
    backend_readiness,
    can_finalize,
    do_materialize,
    evaluate_proposed_task,
    propose_task_from_review_finding,
)
from packages.orchestration.storage import load_job, save_job
from packages.orchestration.worker_queue import (
    enqueue_job,
    get_next_job,
    run_worker_once,
)


def _setup(tmp_path, monkeypatch) -> tuple[Path, str]:
    root = tmp_path / "data"
    monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", root / "proposed_tasks")
    monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", root / "jobs")
    jid = str(uuid4())
    job = Job(id=UUID(jid), name="worker-test")
    save_job(job, root)
    return root, jid


class TestWorkerExecutesRealTask:
    def test_fixture_completes_one_pending_task(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Build feature", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        result = run_worker_once(root, job_id=jid, provider="fixture")
        assert result.action_taken == "task_completed"

        job = load_job(UUID(jid), root)
        completed = [t for t in job.tasks if t.status == RunState.COMPLETED]
        assert len(completed) == 1

    def test_second_run_no_pending_tasks(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Only task", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        enqueue_job(jid, root)
        result2 = run_worker_once(root, job_id=jid, provider="fixture")
        assert result2.action_taken == "no_pending_tasks"

    def test_two_tasks_one_per_run(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        for title in ("Task A", "Task B"):
            t = ProposedTask(title=title, risk="medium")
            add_proposed_task(jid, t, root=root)
            evaluate_proposed_task(jid, t.id, root=root)
            approve_proposed_task(jid, t.id, root=root)
            do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        r1 = run_worker_once(root, job_id=jid, provider="fixture")
        assert r1.action_taken == "task_completed"

        job = load_job(UUID(jid), root)
        completed = [t for t in job.tasks if t.status == RunState.COMPLETED]
        pending = [t for t in job.tasks if t.status == RunState.PENDING]
        assert len(completed) == 1
        assert len(pending) == 1

        enqueue_job(jid, root)
        r2 = run_worker_once(root, job_id=jid, provider="fixture")
        assert r2.action_taken == "task_completed"

        job = load_job(UUID(jid), root)
        assert all(t.status == RunState.COMPLETED for t in job.tasks)

    def test_provider_none_no_work(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="X", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        result = run_worker_once(root, job_id=jid, provider="none")
        assert result.action_taken == "no_work_performed"

    def test_completed_task_not_rerun(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Single", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        job = load_job(UUID(jid), root)
        assert job.tasks[0].status == RunState.COMPLETED

        enqueue_job(jid, root)
        r2 = run_worker_once(root, job_id=jid, provider="fixture")
        assert r2.action_taken == "no_pending_tasks"

        job = load_job(UUID(jid), root)
        assert len(job.tasks) == 1


class TestExecutionPersistence:
    def test_task_status_persists_after_reload(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Persist test", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        job = load_job(UUID(jid), root)
        assert job.tasks[0].status == RunState.COMPLETED
        assert job.tasks[0].inputs.get("execution_provider") == "fixture"
        assert job.tasks[0].inputs.get("execution_summary")

    def test_artifact_ids_persist(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Artifact test", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        job = load_job(UUID(jid), root)
        assert job.tasks[0].inputs.get("execution_artifact_ids")


class TestExecutionEvents:
    def test_fixture_writes_event(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Event test", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        runs_dir = root / "job_logs" / jid
        assert runs_dir.exists()
        events = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
        assert "task_execution_completed" in events
        assert "work_performed" in events


class TestQueueGateMaterialization:
    def test_approved_not_materialized_blocks_queue(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Unapproved mat", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)

        enqueue_job(jid, root)
        result = get_next_job(root)
        assert result is None

    def test_materialized_allows_queue(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Ready", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        result = get_next_job(root)
        assert result is not None


class TestFinalizeAfterExecution:
    def test_finalize_after_task_completed(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Finalize test", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        ok, reason = can_finalize(jid, pending_task_count=1, root=root)
        assert ok is False

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        ok, reason = can_finalize(jid, root=root)
        assert ok is True

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

    def test_finalize_ready_after_completion(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Complete", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        report = backend_readiness(jid, root=root)
        assert report["storage_health"]["healthy"] is True
        assert report["finalize_readiness"]["ready"] is True


class TestFullBackendLoop:
    def test_propose_to_completion(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)

        t = propose_task_from_review_finding(jid, title="Full loop task", reason="Test", risk="medium", root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        mat = do_materialize(jid, t.id, root=root)
        assert mat.materialized_task_id != ""

        enqueue_job(jid, root)
        wr = run_worker_once(root, job_id=jid, provider="fixture")
        assert wr.action_taken == "task_completed"

        job = load_job(UUID(jid), root)
        assert len(job.tasks) == 1
        assert job.tasks[0].status == RunState.COMPLETED
        assert str(job.tasks[0].id) == mat.materialized_task_id
        assert job.tasks[0].inputs.get("proposed_task_id") == t.id

        ok, _ = can_finalize(jid, root=root)
        assert ok is True

        runs_dir = root / "job_logs" / jid
        if runs_dir.exists():
            events = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
            assert "task_execution_started" in events
            assert "task_execution_completed" in events


class TestWorkerBudget:
    def test_max_steps_zero_blocks(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Budget", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        result = run_worker_once(root, job_id=jid, provider="fixture", max_steps=0)
        assert result.action_taken == "blocked"
        assert result.budget_status == "no_budget_set"

    def test_max_steps_one_allows(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Budget ok", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        result = run_worker_once(root, job_id=jid, provider="fixture", max_steps=1)
        assert result.action_taken == "task_completed"
        assert result.budget_status == "ok"


class TestWorkerResultV2:
    def test_result_has_task_id(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Result v2", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        result = run_worker_once(root, job_id=jid, provider="fixture")
        assert result.last_task_id != ""
        assert result.provider == "fixture"
        assert result.work_performed is True
        assert result.task_status == "completed"
        assert len(result.artifact_ids) > 0

    def test_no_pending_has_no_task_id(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        enqueue_job(jid, root)
        result = run_worker_once(root, job_id=jid, provider="fixture")
        assert result.last_task_id == ""
        assert result.action_taken == "no_pending_tasks"


class TestBlockedFixturePersistence:
    def test_blocked_task_persists_failed(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        from packages.core.models import RunState
        job = load_job(UUID(jid), root)
        task = Task(description="Will block", inputs={"task_type": "blocked_fixture"})
        job.tasks.append(task)
        save_job(job, root)

        enqueue_job(jid, root)
        result = run_worker_once(root, job_id=jid, provider="fixture")
        assert result.task_status == "blocked"
        assert result.blocked_reason != ""

        job = load_job(UUID(jid), root)
        assert job.tasks[0].status == RunState.FAILED
        assert job.tasks[0].inputs.get("blocked_reason") != ""

    def test_blocked_task_finalize_false(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        job = load_job(UUID(jid), root)
        task = Task(description="Blocked", inputs={"task_type": "blocked_fixture"})
        job.tasks.append(task)
        save_job(job, root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        ok, reason = can_finalize(jid, blocked_task_count=1, root=root)
        assert ok is False


class TestStartedCompletedEvents:
    def test_started_and_completed_events(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        t = ProposedTask(title="Events", risk="medium")
        add_proposed_task(jid, t, root=root)
        evaluate_proposed_task(jid, t.id, root=root)
        approve_proposed_task(jid, t.id, root=root)
        do_materialize(jid, t.id, root=root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        runs_dir = root / "job_logs" / jid
        assert runs_dir.exists()
        events = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
        assert "task_execution_started" in events
        assert "task_execution_completed" in events
        assert '"provider":"fixture"' in events or '"provider": "fixture"' in events

    def test_blocked_event_written(self, tmp_path, monkeypatch):
        root, jid = _setup(tmp_path, monkeypatch)
        job = load_job(UUID(jid), root)
        task = Task(description="Blocked event", inputs={"task_type": "blocked_fixture"})
        job.tasks.append(task)
        save_job(job, root)

        enqueue_job(jid, root)
        run_worker_once(root, job_id=jid, provider="fixture")

        runs_dir = root / "job_logs" / jid
        events = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
        assert "task_execution_started" in events
        assert "task_execution_blocked" in events
