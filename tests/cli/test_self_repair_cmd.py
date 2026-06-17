"""CLI subprocess tests for `remedy self-repair` commands (R-0139)."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from packages.orchestration.self_repair_proposal import (
    SelfRepairProposal,
    SelfRepairProposalStatus,
    save_self_repair_proposal,
)

_CLI = [sys.executable, "-m", "apps.cli.grouped"]


def _env(data_dir: str) -> dict[str, str]:
    return {**os.environ, "REMEDY_DATA_DIR": data_dir, "PYTHONPATH": os.getcwd()}


@pytest.mark.subprocess
class TestSelfRepairCli:

    def test_proposal_create_json(self, tmp_path):
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-create", "nonexistent-run", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["status"] == "blocked"
        assert data["proposal_id"].startswith("srp-")

    def test_proposal_create_text(self, tmp_path):
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-create", "nonexistent-run"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        assert "Proposal" in r.stdout
        assert "created" in r.stdout.lower() or "Status" in r.stdout

    def test_proposal_show_json(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-show1",
            run_id="dfr-abc",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            title="Test proposal",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-show", "srp-show1", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["proposal_id"] == "srp-show1"
        assert data["status"] == "awaiting_operator"

    def test_proposal_show_not_found(self, tmp_path):
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-show", "nonexistent", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode != 0
        data = json.loads(r.stdout)
        assert "error" in data

    def test_proposal_list_json(self, tmp_path):
        for i in range(2):
            p = SelfRepairProposal(
                proposal_id=f"srp-list{i}",
                status=SelfRepairProposalStatus.DRAFT,
                created_at=f"2026-01-0{i + 1}T00:00:00Z",
            )
            save_self_repair_proposal(p, data_dir=tmp_path)
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-list", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert len(data) == 2

    def test_proposal_list_empty(self, tmp_path):
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-list"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        assert "No self-repair proposals" in r.stdout

    def test_proposal_approve_json(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-apprcli",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            evidence_refs=["replay:test"],
            suggested_worker_prompt="Fix bug",
            acceptance_criteria=["Tests pass"],
            required_tests=["test_foo.py"],
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-approve", "srp-apprcli",
             "--operator-id", "op-1", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["status"] == "approved"

    def test_proposal_approve_fails_missing(self, tmp_path):
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-approve", "nonexistent",
             "--operator-id", "op-1", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode != 0

    def test_proposal_deny_json(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-denycli",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-deny", "srp-denycli",
             "--operator-id", "op-1", "--reason", "Not needed", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["status"] == "denied"

    def test_proposal_edit_json(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-editcli",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            suggested_worker_prompt="Original",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        r = subprocess.run(
            [*_CLI, "self-repair", "proposal-edit", "srp-editcli",
             "--operator-id", "op-1", "--text", "Updated prompt", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["status"] == "awaiting_operator"

    def test_worker_prompt_json(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-wpcli",
            status=SelfRepairProposalStatus.APPROVED,
            suggested_worker_prompt="Do the fix",
            evidence_refs=["replay:test"],
            acceptance_criteria=["Tests pass"],
            required_tests=["test_foo.py"],
            operator_decision="approved by op-1",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        r = subprocess.run(
            [*_CLI, "self-repair", "worker-prompt", "srp-wpcli", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["proposal_id"] == "srp-wpcli"
        assert data["worker_prompt"] == "Do the fix"

    def test_worker_prompt_not_approved(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-wpfail",
            status=SelfRepairProposalStatus.DRAFT,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        r = subprocess.run(
            [*_CLI, "self-repair", "worker-prompt", "srp-wpfail", "--json"],
            capture_output=True, text=True, timeout=30,
            env=_env(str(tmp_path)),
        )
        assert r.returncode != 0
