"""Contract tests for proposal decision integration (F280 T001).

Tests the proposal decision type:
- Branch 9 of list_decisions derives proposal decisions from proposed tasks
"""

from __future__ import annotations

import pytest

from packages.orchestration.decision_queue import DECISION_TYPES, list_decisions
from packages.orchestration.pingpong_job import JobPlan
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    ProposedTaskStatus,
    add_proposed_task,
)


JOB_ID = "test-job-f280"


@pytest.fixture
def tmp_store(monkeypatch, tmp_path):
    """Temporary proposed task store."""
    monkeypatch.setattr(
        "packages.orchestration.proposed_tasks._STORE_DIR",
        tmp_path / "proposed_tasks"
    )
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
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
