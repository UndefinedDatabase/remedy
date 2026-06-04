"""Tests for proposed task domain model, store, evaluator, and transitions."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.proposed_tasks import (
    ProposedTask,
    ProposedTaskSource,
    ProposedTaskStatus,
    InvalidTransitionError,
    UNRESOLVED_STATUSES,
    TERMINAL_STATUSES,
    transition_status,
    save_proposed_tasks,
    load_proposed_tasks,
    add_proposed_task,
    get_proposed_task,
    update_proposed_task,
    count_unresolved,
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
