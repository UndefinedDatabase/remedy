"""Contract tests for proposal decision integration (F280 T001).

Tests the proposal decision type:
- Branch 9 of list_decisions derives proposal decisions from proposed tasks
- decision.resolve proposal: command accepts approve/reject/defer
- decision_inbox recognizes proposal decisions as answerable
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.decision_queue import DECISION_TYPES, list_decisions
from packages.orchestration.pingpong_job import JobPlan
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    ProposedTaskSource,
    ProposedTaskStatus,
    add_and_evaluate_proposed_task,
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

        job = JobPlan(job_id=JOB_ID, name="test")
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
        job = JobPlan(job_id=JOB_ID, name="test")
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
        job = JobPlan(job_id=JOB_ID, name="test")
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
        job = JobPlan(job_id=JOB_ID, name="test")
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
        job = JobPlan(job_id=JOB_ID, name="test")
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
    """Test the CLI round trip for decision resolve proposal:*."""

    def test_cli_approve_unresolved_task(self, tmp_store, tmp_path):
        """CLI: remedy decision resolve <job> proposal:* --reason approve."""
        import os

        # Create a test job
        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(job_id=JOB_ID, name="test")
        save_job_plan(job, root=tmp_store)

        # Add an unresolved task
        t = ProposedTask(title="To approve", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        # Call the CLI
        env = os.environ.copy()
        env["REMEDY_DATA_DIR"] = str(tmp_store)
        result = subprocess.run(
            [
                "python3", "-m", "apps.cli",
                "decision", "resolve", JOB_ID,
                f"proposal:{t.id}",
                "--reason", "approve"
            ],
            cwd=str(Path(__file__).parent.parent.parent),
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "approved and materialized" in result.stdout

    def test_cli_reject_unresolved_task(self, tmp_store, tmp_path):
        """CLI: remedy decision resolve <job> proposal:* --reason reject."""
        import os

        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(job_id=JOB_ID, name="test")
        save_job_plan(job, root=tmp_store)

        t = ProposedTask(title="To reject", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        env = os.environ.copy()
        env["REMEDY_DATA_DIR"] = str(tmp_store)
        result = subprocess.run(
            [
                "python3", "-m", "apps.cli",
                "decision", "resolve", JOB_ID,
                f"proposal:{t.id}",
                "--reason", "reject"
            ],
            cwd=str(Path(__file__).parent.parent.parent),
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "rejected" in result.stdout

    def test_cli_defer_unresolved_task(self, tmp_store, tmp_path):
        """CLI: remedy decision resolve <job> proposal:* --reason defer."""
        import os

        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(job_id=JOB_ID, name="test")
        save_job_plan(job, root=tmp_store)

        t = ProposedTask(title="To defer", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        env = os.environ.copy()
        env["REMEDY_DATA_DIR"] = str(tmp_store)
        result = subprocess.run(
            [
                "python3", "-m", "apps.cli",
                "decision", "resolve", JOB_ID,
                f"proposal:{t.id}",
                "--reason", "defer"
            ],
            cwd=str(Path(__file__).parent.parent.parent),
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "deferred" in result.stdout

    def test_cli_invalid_reason_rejected(self, tmp_store):
        """CLI rejects invalid --reason values."""
        import os

        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(job_id=JOB_ID, name="test")
        save_job_plan(job, root=tmp_store)

        t = ProposedTask(title="Test", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        env = os.environ.copy()
        env["REMEDY_DATA_DIR"] = str(tmp_store)
        result = subprocess.run(
            [
                "python3", "-m", "apps.cli",
                "decision", "resolve", JOB_ID,
                f"proposal:{t.id}",
                "--reason", "invalid"
            ],
            cwd=str(Path(__file__).parent.parent.parent),
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 1
        assert "must be 'approve', 'reject', or 'defer'" in result.stderr


class TestProposalDecisionInbox:
    """Test that proposal decisions integrate with decision_inbox."""

    def test_proposal_answerable_when_unresolved(self, tmp_store):
        """Unresolved proposal is answerable by decision.resolve."""
        from packages.orchestration.decision_inbox import (
            _answerable_by_decision_resolve
        )

        job = JobPlan(job_id=JOB_ID, name="test")
        t = ProposedTask(title="Unresolved", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        answerable = _answerable_by_decision_resolve(job, f"proposal:{t.id}")
        assert answerable is True

    def test_proposal_answerable_when_approved_not_materialized(self, tmp_store):
        """Approved-not-materialized proposal is answerable."""
        from packages.orchestration.decision_inbox import (
            _answerable_by_decision_resolve
        )

        job = JobPlan(job_id=JOB_ID, name="test")
        t = ProposedTask(
            title="Approved",
            status=ProposedTaskStatus.APPROVED_FOR_BUILD
        )
        add_proposed_task(JOB_ID, t, root=tmp_store)

        answerable = _answerable_by_decision_resolve(job, f"proposal:{t.id}")
        assert answerable is True

    def test_proposal_not_answerable_when_rejected(self, tmp_store):
        """Rejected proposal is not answerable."""
        from packages.orchestration.decision_inbox import (
            _answerable_by_decision_resolve
        )

        job = JobPlan(job_id=JOB_ID, name="test")
        t = ProposedTask(title="Rejected", status=ProposedTaskStatus.REJECTED)
        add_proposed_task(JOB_ID, t, root=tmp_store)

        answerable = _answerable_by_decision_resolve(job, f"proposal:{t.id}")
        assert answerable is False

    def test_proposal_not_answerable_when_nonexistent(self, tmp_store):
        """Nonexistent proposal task ID is not answerable."""
        from packages.orchestration.decision_inbox import (
            _answerable_by_decision_resolve
        )

        job = JobPlan(job_id=JOB_ID, name="test")
        answerable = _answerable_by_decision_resolve(job, "proposal:nonexistent")
        assert answerable is False
