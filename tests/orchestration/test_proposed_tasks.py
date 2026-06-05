"""Tests for proposed task domain model, store, evaluator, and transitions."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.proposed_tasks import (
    ProposedTask,
    ProposedTaskSource,
    ProposedTaskStatus,
    ProposedTaskStoreError,
    InvalidTransitionError,
    UNRESOLVED_STATUSES,
    TERMINAL_STATUSES,
    transition_status,
    save_proposed_tasks,
    load_proposed_tasks,
    load_proposed_tasks_safe,
    add_proposed_task,
    get_proposed_task,
    update_proposed_task,
    count_unresolved,
    count_unresolved_safe,
    list_by_status,
    propose_task_from_review_finding,
    propose_from_recommendation,
    propose_rework,
    evaluate_proposed_task,
    evaluate_all_proposed,
    approve_proposed_task,
    reject_proposed_task,
    defer_proposed_task,
    emit_proposed_task_event,
    can_finalize,
    materialize_approved_task,
    do_materialize,
    list_approved_not_materialized,
    reconcile_materialized,
    backend_readiness,
    overnight_readiness,
    EvaluationResult,
)


@pytest.fixture
def tmp_store(tmp_path, monkeypatch):
    """Redirect proposed task store to tmp dir."""
    monkeypatch.setattr(
        "packages.orchestration.proposed_tasks._STORE_DIR",
        tmp_path / "proposed_tasks",
    )
    return tmp_path


JOB_ID = "test-job-001"
REAL_JOB_UUID = "12345678-1234-1234-1234-123456789012"


def _create_real_job(root: Path, job_id: str = REAL_JOB_UUID) -> None:
    """Create a minimal Job file in the given data root."""
    from packages.core.models import Job
    from packages.orchestration.storage import save_job
    from uuid import UUID
    job = Job(id=UUID(job_id), name="test-job")
    save_job(job, root)


class TestProposedTaskModel:
    def test_default_status_is_proposed(self):
        t = ProposedTask(title="Fix bug")
        assert t.status == ProposedTaskStatus.PROPOSED

    def test_is_unresolved_for_proposed(self):
        t = ProposedTask(title="Fix bug")
        assert t.is_unresolved()

    def test_is_not_unresolved_for_approved(self):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        assert not t.is_unresolved()

    def test_is_terminal_for_rejected(self):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.REJECTED)
        assert t.is_terminal()

    def test_is_not_terminal_for_evaluated(self):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.EVALUATED)
        assert not t.is_terminal()

    def test_unresolved_statuses_correct(self):
        assert ProposedTaskStatus.PROPOSED in UNRESOLVED_STATUSES
        assert ProposedTaskStatus.EVALUATED in UNRESOLVED_STATUSES
        assert len(UNRESOLVED_STATUSES) == 2

    def test_terminal_statuses_correct(self):
        assert ProposedTaskStatus.APPROVED_FOR_BUILD in TERMINAL_STATUSES
        assert ProposedTaskStatus.REJECTED in TERMINAL_STATUSES
        assert ProposedTaskStatus.DEFERRED in TERMINAL_STATUSES
        assert len(TERMINAL_STATUSES) == 3

    def test_serialization_roundtrip(self):
        t = ProposedTask(title="Fix bug", reason="Found in review", source=ProposedTaskSource.REVIEWER)
        data = t.model_dump(mode="json")
        t2 = ProposedTask.model_validate(data)
        assert t2.title == "Fix bug"
        assert t2.source == ProposedTaskSource.REVIEWER


class TestTransitions:
    def test_proposed_to_evaluated(self):
        t = ProposedTask(title="Fix bug")
        transition_status(t, ProposedTaskStatus.EVALUATED, by="deterministic")
        assert t.status == ProposedTaskStatus.EVALUATED
        assert t.evaluated_by == "deterministic"
        assert t.evaluated_at is not None

    def test_proposed_to_approved(self):
        t = ProposedTask(title="Fix bug")
        transition_status(t, ProposedTaskStatus.APPROVED_FOR_BUILD, by="user")
        assert t.status == ProposedTaskStatus.APPROVED_FOR_BUILD
        assert t.resolved_at is not None

    def test_proposed_to_rejected(self):
        t = ProposedTask(title="Fix bug")
        transition_status(t, ProposedTaskStatus.REJECTED)
        assert t.status == ProposedTaskStatus.REJECTED
        assert t.resolved_at is not None

    def test_evaluated_to_approved(self):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.EVALUATED)
        transition_status(t, ProposedTaskStatus.APPROVED_FOR_BUILD)
        assert t.status == ProposedTaskStatus.APPROVED_FOR_BUILD

    def test_invalid_transition_raises(self):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.REJECTED)
        with pytest.raises(InvalidTransitionError):
            transition_status(t, ProposedTaskStatus.APPROVED_FOR_BUILD)

    def test_approved_is_terminal(self):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        with pytest.raises(InvalidTransitionError):
            transition_status(t, ProposedTaskStatus.REJECTED)

    def test_reject_approved_fails(self):
        t = ProposedTask(title="X", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        with pytest.raises(InvalidTransitionError):
            transition_status(t, ProposedTaskStatus.REJECTED)

    def test_defer_approved_fails(self):
        t = ProposedTask(title="X", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        with pytest.raises(InvalidTransitionError):
            transition_status(t, ProposedTaskStatus.DEFERRED)

    def test_approve_rejected_fails(self):
        t = ProposedTask(title="X", status=ProposedTaskStatus.REJECTED)
        with pytest.raises(InvalidTransitionError):
            transition_status(t, ProposedTaskStatus.APPROVED_FOR_BUILD)

    def test_evaluated_at_set_on_evaluate(self):
        t = ProposedTask(title="X")
        transition_status(t, ProposedTaskStatus.EVALUATED, by="user")
        assert t.evaluated_at is not None
        assert t.evaluated_by == "user"

    def test_resolved_at_set_on_terminal(self):
        t = ProposedTask(title="X")
        transition_status(t, ProposedTaskStatus.DEFERRED)
        assert t.resolved_at is not None


class TestStore:
    def test_save_and_load(self, tmp_store):
        tasks = [ProposedTask(title="A"), ProposedTask(title="B")]
        save_proposed_tasks(JOB_ID, tasks)
        loaded = load_proposed_tasks(JOB_ID)
        assert len(loaded) == 2
        assert loaded[0].title == "A"
        assert loaded[1].title == "B"

    def test_load_nonexistent_returns_empty(self, tmp_store):
        assert load_proposed_tasks("nonexistent") == []

    def test_add_and_get(self, tmp_store):
        t = ProposedTask(title="Fix bug", job_id=JOB_ID)
        add_proposed_task(JOB_ID, t)
        found = get_proposed_task(JOB_ID, t.id)
        assert found is not None
        assert found.title == "Fix bug"

    def test_update(self, tmp_store):
        t = ProposedTask(title="Fix bug")
        add_proposed_task(JOB_ID, t)
        t.title = "Fix critical bug"
        result = update_proposed_task(JOB_ID, t)
        assert result is True
        loaded = get_proposed_task(JOB_ID, t.id)
        assert loaded.title == "Fix critical bug"

    def test_count_unresolved(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        add_proposed_task(JOB_ID, ProposedTask(title="B", status=ProposedTaskStatus.APPROVED_FOR_BUILD))
        add_proposed_task(JOB_ID, ProposedTask(title="C", status=ProposedTaskStatus.EVALUATED))
        assert count_unresolved(JOB_ID) == 2  # A (proposed) + C (evaluated)

    def test_list_by_status(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        add_proposed_task(JOB_ID, ProposedTask(title="B", status=ProposedTaskStatus.REJECTED))
        result = list_by_status(JOB_ID, ProposedTaskStatus.PROPOSED)
        assert len(result) == 1
        assert result[0].title == "A"

    def test_save_writes_valid_json(self, tmp_store):
        tasks = [ProposedTask(title="A")]
        save_proposed_tasks(JOB_ID, tasks)
        path = tmp_store / "proposed_tasks" / f"{JOB_ID}.json"
        data = json.loads(path.read_text())
        assert isinstance(data, list)
        assert len(data) == 1

    def test_sequential_updates_preserve_data(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        add_proposed_task(JOB_ID, ProposedTask(title="B"))
        loaded = load_proposed_tasks(JOB_ID)
        assert len(loaded) == 2

    def test_data_dir_root_param(self, tmp_path):
        root = tmp_path / "custom_root"
        tasks = [ProposedTask(title="A")]
        save_proposed_tasks(JOB_ID, tasks, root=root)
        loaded = load_proposed_tasks(JOB_ID, root=root)
        assert len(loaded) == 1
        assert (root / "proposed_tasks" / f"{JOB_ID}.json").exists()

    def test_root_param_isolated_from_default(self, tmp_store, tmp_path):
        root = tmp_path / "isolated"
        add_proposed_task(JOB_ID, ProposedTask(title="in-default"))
        add_proposed_task(JOB_ID, ProposedTask(title="in-root"), root=root)
        assert len(load_proposed_tasks(JOB_ID)) == 1
        assert load_proposed_tasks(JOB_ID)[0].title == "in-default"
        assert len(load_proposed_tasks(JOB_ID, root=root)) == 1
        assert load_proposed_tasks(JOB_ID, root=root)[0].title == "in-root"


class TestCorruptStore:
    def test_corrupt_json_raises_store_error(self, tmp_store):
        path = tmp_store / "proposed_tasks"
        path.mkdir(parents=True, exist_ok=True)
        (path / f"{JOB_ID}.json").write_text("{not valid json")
        with pytest.raises(ProposedTaskStoreError):
            load_proposed_tasks(JOB_ID)

    def test_corrupt_json_safe_returns_degraded(self, tmp_store):
        path = tmp_store / "proposed_tasks"
        path.mkdir(parents=True, exist_ok=True)
        (path / f"{JOB_ID}.json").write_text("<<<garbage>>>")
        tasks, degraded = load_proposed_tasks_safe(JOB_ID)
        assert degraded is True
        assert tasks == []

    def test_corrupt_count_unresolved_raises(self, tmp_store):
        path = tmp_store / "proposed_tasks"
        path.mkdir(parents=True, exist_ok=True)
        (path / f"{JOB_ID}.json").write_text("not json")
        with pytest.raises(ProposedTaskStoreError):
            count_unresolved(JOB_ID)

    def test_corrupt_count_unresolved_safe_returns_degraded(self, tmp_store):
        path = tmp_store / "proposed_tasks"
        path.mkdir(parents=True, exist_ok=True)
        (path / f"{JOB_ID}.json").write_text("not json")
        count, degraded = count_unresolved_safe(JOB_ID)
        assert degraded is True
        assert count == -1

    def test_nonexistent_is_not_degraded(self, tmp_store):
        tasks, degraded = load_proposed_tasks_safe("no-such-job")
        assert degraded is False
        assert tasks == []


class TestReviewBridge:
    def test_propose_from_review_finding(self, tmp_store):
        t = propose_task_from_review_finding(JOB_ID, title="Add tests", reason="Coverage low")
        assert t.status == ProposedTaskStatus.PROPOSED
        assert t.source == ProposedTaskSource.REVIEWER
        loaded = load_proposed_tasks(JOB_ID)
        assert len(loaded) == 1

    def test_propose_from_recommendation_dict(self, tmp_store):
        rec = {
            "id": "rec-001",
            "title": "Add edge case tests",
            "description": "Test negative inputs",
            "task_type": "test_improvement",
            "reason": "Coverage gap",
            "risk": "low",
            "priority": "medium",
        }
        t = propose_from_recommendation(JOB_ID, rec)
        assert t.title == "Add edge case tests"
        assert t.origin_recommendation_id == "rec-001"

    def test_propose_rework(self, tmp_store):
        t = propose_rework(JOB_ID, failed_task_id="task-001", title="Fix test failure")
        assert t.source == ProposedTaskSource.ORCHESTRATOR
        assert t.task_type == "rework"
        assert t.priority == "high"


class TestEvaluator:
    def test_evaluate_high_risk_needs_human(self, tmp_store):
        t = ProposedTask(title="Risky change", risk="high")
        add_proposed_task(JOB_ID, t)
        result = evaluate_proposed_task(JOB_ID, t.id)
        assert result.status == ProposedTaskStatus.EVALUATED
        assert "high risk" in result.evaluation_notes

    def test_evaluate_duplicate_rejected(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="Fix bug", status=ProposedTaskStatus.APPROVED_FOR_BUILD))
        t = ProposedTask(title="Fix bug")
        add_proposed_task(JOB_ID, t)
        result = evaluate_proposed_task(JOB_ID, t.id)
        assert result.status == ProposedTaskStatus.REJECTED
        assert "duplicate" in result.evaluation_notes

    def test_evaluate_low_risk_no_approval_auto_approves(self, tmp_store):
        t = ProposedTask(title="Minor fix", risk="low", approval_required=False)
        add_proposed_task(JOB_ID, t)
        result = evaluate_proposed_task(JOB_ID, t.id)
        assert result.status == ProposedTaskStatus.APPROVED_FOR_BUILD

    def test_evaluate_default_awaits_human(self, tmp_store):
        t = ProposedTask(title="Normal task", risk="medium")
        add_proposed_task(JOB_ID, t)
        result = evaluate_proposed_task(JOB_ID, t.id)
        assert result.status == ProposedTaskStatus.EVALUATED
        assert "awaiting human" in result.evaluation_notes

    def test_evaluate_all_proposed(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A", risk="medium"))
        add_proposed_task(JOB_ID, ProposedTask(title="B", risk="medium"))
        tasks = evaluate_all_proposed(JOB_ID)
        assert all(t.status == ProposedTaskStatus.EVALUATED for t in tasks)

    def test_evaluate_skips_already_evaluated(self, tmp_store):
        t = ProposedTask(title="Already done", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_ID, t)
        result = evaluate_proposed_task(JOB_ID, t.id)
        assert result.status == ProposedTaskStatus.EVALUATED  # unchanged


class TestApproveRejectDefer:
    def test_approve(self, tmp_store):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_ID, t)
        result = approve_proposed_task(JOB_ID, t.id)
        assert result.status == ProposedTaskStatus.APPROVED_FOR_BUILD

    def test_reject_with_reason(self, tmp_store):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_ID, t)
        result = reject_proposed_task(JOB_ID, t.id, reason="Not needed")
        assert result.status == ProposedTaskStatus.REJECTED
        assert result.evaluation_notes == "Not needed"

    def test_defer(self, tmp_store):
        t = ProposedTask(title="Fix bug", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_ID, t)
        result = defer_proposed_task(JOB_ID, t.id)
        assert result.status == ProposedTaskStatus.DEFERRED

    def test_approve_nonexistent_returns_none(self, tmp_store):
        assert approve_proposed_task(JOB_ID, "nonexistent") is None

    def test_reject_approved_raises(self, tmp_store):
        t = ProposedTask(title="X", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        add_proposed_task(JOB_ID, t)
        with pytest.raises(InvalidTransitionError):
            reject_proposed_task(JOB_ID, t.id)

    def test_defer_approved_raises(self, tmp_store):
        t = ProposedTask(title="X", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        add_proposed_task(JOB_ID, t)
        with pytest.raises(InvalidTransitionError):
            defer_proposed_task(JOB_ID, t.id)

    def test_reason_bounded(self, tmp_store):
        t = ProposedTask(title="X", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_ID, t)
        long_reason = "x" * 500
        result = reject_proposed_task(JOB_ID, t.id, reason=long_reason)
        assert len(result.evaluation_notes) <= 200


class TestCanFinalize:
    def test_can_finalize_clean(self, tmp_store):
        ok, reason = can_finalize(JOB_ID)
        assert ok is True
        assert reason == "ready"

    def test_blocked_by_unresolved(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        ok, reason = can_finalize(JOB_ID)
        assert ok is False
        assert "unresolved" in reason

    def test_blocked_by_pending_tasks(self, tmp_store):
        ok, reason = can_finalize(JOB_ID, pending_task_count=1)
        assert ok is False
        assert "pending" in reason

    def test_blocked_by_blocked_tasks(self, tmp_store):
        ok, reason = can_finalize(JOB_ID, blocked_task_count=1)
        assert ok is False
        assert "blocked" in reason

    def test_blocked_by_approvals(self, tmp_store):
        ok, reason = can_finalize(JOB_ID, pending_approvals=1)
        assert ok is False
        assert "approval" in reason

    def test_blocked_by_corrupt_store(self, tmp_store):
        path = tmp_store / "proposed_tasks"
        path.mkdir(parents=True, exist_ok=True)
        (path / f"{JOB_ID}.json").write_text("corrupt")
        ok, reason = can_finalize(JOB_ID)
        assert ok is False
        assert "degraded" in reason

    def test_approved_not_materialized_blocks(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A", status=ProposedTaskStatus.APPROVED_FOR_BUILD))
        ok, reason = can_finalize(JOB_ID)
        assert ok is False
        assert "not materialized" in reason

    def test_approved_materialized_does_not_block(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A", status=ProposedTaskStatus.APPROVED_FOR_BUILD, materialized_task_id="real-task-1"))
        ok, _ = can_finalize(JOB_ID)
        assert ok is True

    def test_rejected_does_not_block(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A", status=ProposedTaskStatus.REJECTED))
        ok, _ = can_finalize(JOB_ID)
        assert ok is True

    def test_deferred_does_not_block(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A", status=ProposedTaskStatus.DEFERRED))
        ok, _ = can_finalize(JOB_ID)
        assert ok is True


class TestEventAudit:
    def test_emit_with_none_writer_is_noop(self):
        t = ProposedTask(title="Fix bug")
        emit_proposed_task_event(None, "proposed_task_created", t)  # should not raise

    def test_emit_calls_writer_log(self, tmp_store):
        calls = []

        class FakeWriter:
            def log(self, event, **kwargs):
                calls.append((event, kwargs))

        t = ProposedTask(title="Fix bug", source=ProposedTaskSource.REVIEWER)
        emit_proposed_task_event(FakeWriter(), "proposed_task_created", t)
        assert len(calls) == 1
        assert calls[0][0] == "proposed_task_created"
        assert calls[0][1]["proposed_task_id"] == t.id

    def test_event_payload_safe(self, tmp_store):
        calls = []

        class FakeWriter:
            def log(self, event, **kwargs):
                calls.append((event, kwargs))

        t = ProposedTask(title="X" * 200, evaluation_notes="N" * 500, source=ProposedTaskSource.REVIEWER)
        emit_proposed_task_event(FakeWriter(), "proposed_task_evaluated", t)
        assert len(calls[0][1]["title"]) <= 80
        assert len(calls[0][1]["evaluation_notes"]) <= 200


class TestWorkerQueueGate:
    def test_unresolved_blocks_queue(self, tmp_path):
        from packages.orchestration.worker_queue import enqueue_job, get_next_job
        root = tmp_path / "data"
        queue_dir = root / "queue"
        queue_dir.mkdir(parents=True)

        enqueue_job("blocked-job", root)
        add_proposed_task("blocked-job", ProposedTask(title="Pending"), root=root)

        result = get_next_job(root)
        assert result is None

    def test_approved_does_not_block_queue(self, tmp_path):
        from packages.orchestration.worker_queue import enqueue_job, get_next_job
        root = tmp_path / "data"
        queue_dir = root / "queue"
        queue_dir.mkdir(parents=True)

        enqueue_job("ok-job", root)
        add_proposed_task("ok-job", ProposedTask(title="Done", status=ProposedTaskStatus.APPROVED_FOR_BUILD, materialized_task_id="real-task"), root=root)

        result = get_next_job(root)
        assert result is not None
        assert result.job_id == "ok-job"

    def test_corrupt_store_blocks_queue(self, tmp_path):
        from packages.orchestration.worker_queue import enqueue_job, get_next_job
        root = tmp_path / "data"
        queue_dir = root / "queue"
        queue_dir.mkdir(parents=True)

        enqueue_job("corrupt-job", root)
        pt_dir = root / "proposed_tasks"
        pt_dir.mkdir(parents=True)
        (pt_dir / "corrupt-job.json").write_text("not json")

        result = get_next_job(root)
        assert result is None


class TestMaterialization:
    def test_materialize_approved(self, tmp_store):
        t = ProposedTask(title="Build feature", status=ProposedTaskStatus.APPROVED_FOR_BUILD, task_type="feature", source=ProposedTaskSource.REVIEWER, risk="low")
        result = materialize_approved_task(t)
        assert result["description"] == "Build feature"
        assert result["status"] == "pending"
        assert result["inputs"]["proposed_task_id"] == t.id
        assert result["inputs"]["task_type"] == "feature"

    def test_materialize_non_approved_raises(self):
        t = ProposedTask(title="X", status=ProposedTaskStatus.EVALUATED)
        with pytest.raises(ValueError, match="not approved_for_build"):
            materialize_approved_task(t)

    def test_list_approved_not_materialized(self, tmp_store):
        t1 = ProposedTask(title="A", status=ProposedTaskStatus.APPROVED_FOR_BUILD, materialized_task_id="real-1")
        t2 = ProposedTask(title="B", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        t3 = ProposedTask(title="C", status=ProposedTaskStatus.REJECTED)
        add_proposed_task(JOB_ID, t1)
        add_proposed_task(JOB_ID, t2)
        add_proposed_task(JOB_ID, t3)
        not_materialized = list_approved_not_materialized(JOB_ID)
        assert len(not_materialized) == 1
        assert not_materialized[0].id == t2.id

    def test_do_materialize_creates_real_job_task(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        t = ProposedTask(title="Materialize me", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        add_proposed_task(REAL_JOB_UUID, t)
        result = do_materialize(REAL_JOB_UUID, t.id)
        assert result is not None
        assert result.materialized_task_id != ""
        assert result.materialized_at is not None
        from packages.orchestration.storage import load_job
        from uuid import UUID
        job = load_job(UUID(REAL_JOB_UUID))
        assert any(str(task.id) == result.materialized_task_id for task in job.tasks)

    def test_do_materialize_rejects_non_approved(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        t = ProposedTask(title="Not ready", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(REAL_JOB_UUID, t)
        with pytest.raises(ValueError, match="not approved_for_build"):
            do_materialize(REAL_JOB_UUID, t.id)

    def test_do_materialize_rejects_already_materialized(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        t = ProposedTask(title="Done", status=ProposedTaskStatus.APPROVED_FOR_BUILD, materialized_task_id="existing")
        add_proposed_task(REAL_JOB_UUID, t)
        with pytest.raises(ValueError, match="Already materialized"):
            do_materialize(REAL_JOB_UUID, t.id)

    def test_do_materialize_missing_job_fails(self, tmp_store):
        t = ProposedTask(title="No job", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
        add_proposed_task(JOB_ID, t)
        with pytest.raises(Exception):
            do_materialize(JOB_ID, t.id)

    def test_materialize_non_approved_raises(self):
        t = ProposedTask(title="X", status=ProposedTaskStatus.EVALUATED)
        with pytest.raises(ValueError, match="not approved_for_build"):
            materialize_approved_task(t)


class TestEndToEndFlow:
    def test_full_proposed_task_lifecycle(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)

        t = propose_task_from_review_finding(REAL_JOB_UUID, title="New feature", reason="Reviewer found gap", risk="medium")
        assert t.status == ProposedTaskStatus.PROPOSED
        assert count_unresolved(REAL_JOB_UUID) == 1

        ok, _ = can_finalize(REAL_JOB_UUID)
        assert ok is False

        evaluated = evaluate_proposed_task(REAL_JOB_UUID, t.id)
        assert evaluated.status == ProposedTaskStatus.EVALUATED

        approved = approve_proposed_task(REAL_JOB_UUID, t.id)
        assert approved.status == ProposedTaskStatus.APPROVED_FOR_BUILD
        assert count_unresolved(REAL_JOB_UUID) == 0

        ok, reason = can_finalize(REAL_JOB_UUID)
        assert ok is False
        assert "not materialized" in reason

        do_materialize(REAL_JOB_UUID, t.id)
        ok, reason = can_finalize(REAL_JOB_UUID)
        assert ok is True

    def test_reject_flow(self, tmp_store):
        t = propose_task_from_review_finding(JOB_ID, title="Bad idea", risk="low")
        evaluate_proposed_task(JOB_ID, t.id)
        rejected = reject_proposed_task(JOB_ID, t.id, reason="Not needed")
        assert rejected.status == ProposedTaskStatus.REJECTED
        assert count_unresolved(JOB_ID) == 0

    def test_defer_flow(self, tmp_store):
        t = propose_task_from_review_finding(JOB_ID, title="Later", risk="low")
        evaluate_proposed_task(JOB_ID, t.id)
        deferred = defer_proposed_task(JOB_ID, t.id, reason="Next sprint")
        assert deferred.status == ProposedTaskStatus.DEFERRED
        assert count_unresolved(JOB_ID) == 0

    def test_full_lifecycle_with_materialize(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        t = propose_task_from_review_finding(REAL_JOB_UUID, title="Build it", risk="medium")
        evaluate_proposed_task(REAL_JOB_UUID, t.id)
        approve_proposed_task(REAL_JOB_UUID, t.id)
        materialized = do_materialize(REAL_JOB_UUID, t.id)
        assert materialized.materialized_task_id != ""
        assert materialized.materialized_at is not None
        assert list_approved_not_materialized(REAL_JOB_UUID) == []
        ok, _ = can_finalize(REAL_JOB_UUID)
        assert ok is True
        from packages.orchestration.storage import load_job
        from uuid import UUID
        job = load_job(UUID(REAL_JOB_UUID))
        assert len(job.tasks) == 1
        assert str(job.tasks[0].id) == materialized.materialized_task_id


class TestFileLocking:
    def test_sequential_adds_preserve_data(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        add_proposed_task(JOB_ID, ProposedTask(title="B"))
        add_proposed_task(JOB_ID, ProposedTask(title="C"))
        loaded = load_proposed_tasks(JOB_ID)
        assert len(loaded) == 3

    def test_update_then_add_preserves_both(self, tmp_store):
        t = ProposedTask(title="Original")
        add_proposed_task(JOB_ID, t)
        t.title = "Updated"
        update_proposed_task(JOB_ID, t)
        add_proposed_task(JOB_ID, ProposedTask(title="New"))
        loaded = load_proposed_tasks(JOB_ID)
        assert len(loaded) == 2
        assert loaded[0].title == "Updated"
        assert loaded[1].title == "New"

    def test_approve_then_materialize_preserves_state(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        t = ProposedTask(title="Build", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(REAL_JOB_UUID, t)
        approve_proposed_task(REAL_JOB_UUID, t.id)
        do_materialize(REAL_JOB_UUID, t.id)
        loaded = load_proposed_tasks(REAL_JOB_UUID)
        assert loaded[0].status == ProposedTaskStatus.APPROVED_FOR_BUILD
        assert loaded[0].materialized_task_id != ""

    def test_lock_file_created_and_cleaned(self, tmp_store):
        from packages.orchestration.proposed_tasks import _file_lock, _lock_path
        with _file_lock(JOB_ID):
            lock = _lock_path(JOB_ID)
            assert lock.exists()


class TestStoreRootResolution:
    def test_env_data_dir_used(self, tmp_path, monkeypatch):
        data_root = tmp_path / "env_data"
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", None)
        add_proposed_task(JOB_ID, ProposedTask(title="Via env"))
        loaded = load_proposed_tasks(JOB_ID)
        assert len(loaded) == 1
        assert (data_root / "proposed_tasks" / f"{JOB_ID}.json").exists()

    def test_root_param_overrides_env(self, tmp_path, monkeypatch):
        env_root = tmp_path / "env"
        explicit_root = tmp_path / "explicit"
        monkeypatch.setenv("REMEDY_DATA_DIR", str(env_root))
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", None)
        add_proposed_task(JOB_ID, ProposedTask(title="Explicit"), root=explicit_root)
        assert load_proposed_tasks(JOB_ID, root=explicit_root)[0].title == "Explicit"
        assert load_proposed_tasks(JOB_ID) == []


class TestReconciliation:
    def test_consistent(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        report = reconcile_materialized(REAL_JOB_UUID)
        assert report["consistent"] is True

    def test_missing_job_task(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        t = ProposedTask(title="Ghost", status=ProposedTaskStatus.APPROVED_FOR_BUILD, materialized_task_id="nonexistent-task-id")
        add_proposed_task(REAL_JOB_UUID, t)
        report = reconcile_materialized(REAL_JOB_UUID)
        assert report["consistent"] is False
        assert t.id in report["missing_job_task"]

    def test_corrupt_store(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        pt_dir = tmp_path / "proposed_tasks"
        pt_dir.mkdir(parents=True, exist_ok=True)
        (pt_dir / f"{REAL_JOB_UUID}.json").write_text("corrupt")
        report = reconcile_materialized(REAL_JOB_UUID)
        assert report["consistent"] is False
        assert report["proposals_degraded"] is True


class TestBackendReadiness:
    def test_healthy_job_no_work(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        report = backend_readiness(REAL_JOB_UUID)
        assert report["storage_health"]["healthy"] is True
        assert report["build_readiness"]["ready"] is False
        assert "no_pending_work" in report["build_readiness"]["blockers"]

    def test_not_ready_with_unresolved(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        add_proposed_task(REAL_JOB_UUID, ProposedTask(title="Pending"))
        report = backend_readiness(REAL_JOB_UUID)
        assert report["build_readiness"]["ready"] is False
        assert any("unresolved" in b for b in report["build_readiness"]["blockers"])

    def test_not_ready_missing_job(self, tmp_store):
        report = backend_readiness("00000000-0000-0000-0000-000000000099")
        assert report["storage_health"]["healthy"] is False
        assert "job_not_found" in report["storage_health"]["blockers"]

    def test_not_ready_corrupt_store(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        pt_dir = tmp_path / "proposed_tasks"
        pt_dir.mkdir(parents=True, exist_ok=True)
        (pt_dir / f"{REAL_JOB_UUID}.json").write_text("corrupt")
        report = backend_readiness(REAL_JOB_UUID)
        assert report["storage_health"]["healthy"] is False
        assert "proposal_store_degraded" in report["storage_health"]["blockers"]

    def test_materialized_pending_task(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        t = propose_task_from_review_finding(REAL_JOB_UUID, title="Work", risk="medium")
        evaluate_proposed_task(REAL_JOB_UUID, t.id)
        approve_proposed_task(REAL_JOB_UUID, t.id)
        do_materialize(REAL_JOB_UUID, t.id)
        report = backend_readiness(REAL_JOB_UUID)
        assert report["storage_health"]["healthy"] is True
        assert report["build_readiness"]["ready"] is True
        assert report["build_readiness"]["pending_tasks"] == 1
        assert report["finalize_readiness"]["ready"] is False


class TestOvernightReadiness:
    def test_never_ready_yet(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        _create_real_job(tmp_path)
        report = overnight_readiness(REAL_JOB_UUID)
        assert report["ready"] is False
        assert "no_overnight_mode_implemented" in report["blockers"]
        assert report["max_safe_autonomy_level"] == 0
