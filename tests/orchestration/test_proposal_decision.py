"""Contract tests for proposal decision integration (F280 T001).

Tests the proposal decision type:
- Branch 9 of list_decisions derives proposal decisions from proposed tasks
- CLI subprocess round-trip for decision resolve proposal:<id> --reason approve|reject|defer
"""

from __future__ import annotations

import json

import pytest

from apps.cli.commands.decision import _cmd_decision_resolve
from packages.orchestration.decision_queue import DECISION_TYPES, list_decisions
from packages.orchestration.pingpong_job import JobPlan
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    ProposedTaskStatus,
    add_proposed_task,
)

JOB_ID = "12345678-1234-5678-1234-567812345678"


@pytest.fixture
def tmp_store(monkeypatch, tmp_path):
    """Temporary proposed task store with a valid job record."""
    monkeypatch.setattr(
        "packages.orchestration.proposed_tasks._STORE_DIR",
        tmp_path / "proposed_tasks"
    )
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    # Create a valid job record so resolve_job_id can find it
    job_dir = tmp_path / "jobs" / JOB_ID
    job_dir.mkdir(parents=True, exist_ok=True)
    job_data = {
        "job_id": JOB_ID,
        "job_title": "test-job",
        "created_at": "2026-09-17T00:00:00Z",
        "tasks": [],
        "status": "pending",
        "artifacts": [],
        "budget": {"max_steps": 10, "max_tokens": 0, "max_cost_usd": 0.0},
        "metadata": {},
    }
    (job_dir / "job.json").write_text(json.dumps(job_data, indent=2))

    return tmp_path


class TestProposalDecisionType:
    """Verify proposal is in DECISION_TYPES."""

    def test_proposal_in_decision_types(self):
        assert "proposal" in DECISION_TYPES


class TestProposalDecisionListDerivation:
    """Test that branch 9 of list_decisions derives proposal decisions."""

    def test_unresolved_task_yields_proposal_decision(self, tmp_store):
        """An unresolved task surfaces a proposal decision."""
        from packages.orchestration.proposed_tasks import ProposedTaskStatus

        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Review findings", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        decisions = list_decisions(job, [])
        proposal_decisions = [d for d in decisions if d.type == "proposal"]

        assert len(proposal_decisions) == 1
        assert proposal_decisions[0].id == f"proposal:{t.id}"
        assert proposal_decisions[0].status == "open"
        assert proposal_decisions[0].severity == "blocker"

    def test_approved_not_materialized_task_yields_decision(self, tmp_store):
        """An approved but not-materialized task surfaces a decision."""
        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(
            title="Approved task",
            status=ProposedTaskStatus.APPROVED_FOR_BUILD
        )
        add_proposed_task(JOB_ID, t, root=tmp_store)

        decisions = list_decisions(job, [])
        proposal_decisions = [d for d in decisions if d.type == "proposal"]

        assert len(proposal_decisions) == 1
        assert proposal_decisions[0].status == "open"

    def test_rejected_task_yields_no_decision(self, tmp_store):
        """A rejected task does not surface a decision."""
        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(
            title="Rejected",
            status=ProposedTaskStatus.REJECTED
        )
        add_proposed_task(JOB_ID, t, root=tmp_store)

        decisions = list_decisions(job, [])
        proposal_decisions = [d for d in decisions if d.type == "proposal"]

        assert len(proposal_decisions) == 0

    def test_unresolved_task_next_actions(self, tmp_store):
        """Unresolved task decision offers all three actions."""
        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Unresolved", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        decisions = list_decisions(job, [])
        proposal_decisions = [d for d in decisions if d.type == "proposal"]

        assert len(proposal_decisions[0].next_actions) == 3
        assert any("approve" in a for a in proposal_decisions[0].next_actions)
        assert any("reject" in a for a in proposal_decisions[0].next_actions)
        assert any("defer" in a for a in proposal_decisions[0].next_actions)

    def test_approved_not_materialized_next_actions(self, tmp_store):
        """Approved-not-materialized decision offers only approve (materialize)."""
        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(
            title="Approved",
            status=ProposedTaskStatus.APPROVED_FOR_BUILD
        )
        add_proposed_task(JOB_ID, t, root=tmp_store)

        decisions = list_decisions(job, [])
        proposal_decisions = [d for d in decisions if d.type == "proposal"]

        assert len(proposal_decisions[0].next_actions) == 1
        assert "approve" in proposal_decisions[0].next_actions[0]


class TestProposalDecisionCLI:
    """Test CLI subprocess round-trip for proposal decision resolution."""

    def test_approve_unresolved_materializes(self, tmp_store):
        """Approve on unresolved task transitions to approved and materializes."""
        from packages.orchestration.proposed_tasks import get_proposed_task

        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Unresolved task", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        _cmd_decision_resolve(JOB_ID, f"proposal:{t.id}", reason="approve")

        # Verify task is materialized
        updated = get_proposed_task(JOB_ID, t.id, root=tmp_store)
        assert updated is not None
        assert updated.is_materialized

    def test_approve_approved_not_materialized_materializes(self, tmp_store):
        """Approve on approved-not-materialized task materializes it."""
        from packages.orchestration.proposed_tasks import get_proposed_task

        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(
            title="Approved task",
            status=ProposedTaskStatus.APPROVED_FOR_BUILD
        )
        add_proposed_task(JOB_ID, t, root=tmp_store)

        _cmd_decision_resolve(JOB_ID, f"proposal:{t.id}", reason="approve")

        # Verify task is materialized
        updated = get_proposed_task(JOB_ID, t.id, root=tmp_store)
        assert updated is not None
        assert updated.is_materialized

    def test_approve_rejected_task_exits_cleanly(self, tmp_store, capsys):
        """Approve on rejected task exits with named error, not ValueError."""
        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Rejected task", status=ProposedTaskStatus.REJECTED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        with pytest.raises(SystemExit) as exc_info:
            _cmd_decision_resolve(JOB_ID, f"proposal:{t.id}", reason="approve")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "rejected" in captured.err
        assert "ValueError" not in captured.err

    def test_approve_deferred_task_exits_cleanly(self, tmp_store, capsys):
        """Approve on deferred task exits with named error, not ValueError."""
        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Deferred task", status=ProposedTaskStatus.DEFERRED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        with pytest.raises(SystemExit) as exc_info:
            _cmd_decision_resolve(JOB_ID, f"proposal:{t.id}", reason="approve")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "deferred" in captured.err

    def test_reject_unresolved_transitions(self, tmp_store):
        """Reject on unresolved task transitions to rejected."""
        from packages.orchestration.proposed_tasks import get_proposed_task

        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Unresolved task", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        _cmd_decision_resolve(JOB_ID, f"proposal:{t.id}", reason="reject")

        # Verify task is rejected
        updated = get_proposed_task(JOB_ID, t.id, root=tmp_store)
        assert updated is not None
        assert updated.status == ProposedTaskStatus.REJECTED

    def test_reject_terminal_task_exits_cleanly(self, tmp_store, capsys):
        """Reject on terminal task exits with named error."""
        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Already rejected", status=ProposedTaskStatus.REJECTED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        with pytest.raises(SystemExit) as exc_info:
            _cmd_decision_resolve(JOB_ID, f"proposal:{t.id}", reason="reject")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "terminal" in captured.err

    def test_defer_unresolved_transitions(self, tmp_store):
        """Defer on unresolved task transitions to deferred."""
        from packages.orchestration.proposed_tasks import get_proposed_task

        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Unresolved task", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        _cmd_decision_resolve(JOB_ID, f"proposal:{t.id}", reason="defer")

        # Verify task is deferred
        updated = get_proposed_task(JOB_ID, t.id, root=tmp_store)
        assert updated is not None
        assert updated.status == ProposedTaskStatus.DEFERRED

    def test_defer_terminal_task_exits_cleanly(self, tmp_store, capsys):
        """Defer on terminal task exits with named error."""
        job = JobPlan(job_id=JOB_ID)
        t = ProposedTask(title="Already deferred", status=ProposedTaskStatus.DEFERRED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        with pytest.raises(SystemExit) as exc_info:
            _cmd_decision_resolve(JOB_ID, f"proposal:{t.id}", reason="defer")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "terminal" in captured.err
