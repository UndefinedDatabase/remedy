"""Tests for remedy do --continue v1 (Steps 1164-1178)."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.approval_queue import make_intent_id, set_approval_state
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.run_contract import (
    build_default_run_contract, save_contract, ContractAction,
)
from packages.orchestration.storage import save_job


ARTIFACT_CONTENT = "Summary:\n  - safe doc\nProposed Changes:\n  - add a line\nNotes:\n  - none\n"


def make_continue_job(
    data_dir: Path,
    repo_root: Path,
    *,
    approve: bool = True,
    write_perm: bool = True,
    test_perm: bool = True,
    allow_apply: bool = True,
    stop_before_apply: bool = False,
    max_test_runs: int = 1,
    target_path: str = "docs/CHANGES.md",
    extra_intents: int = 0,
):
    """Build a continuation-ready job. Returns (job, intent_id)."""
    repo_root.mkdir(parents=True, exist_ok=True)
    task = Task(description="Continue task")
    explanations = [
        {"file": target_path, "action": "create", "risk": "low",
         "reason": "", "summary": "safe doc"}
    ]
    for n in range(extra_intents):
        explanations.append(
            {"file": f"docs/EXTRA{n}.md", "action": "create", "risk": "low",
             "reason": "", "summary": "extra"}
        )
    art = Artifact(
        name="build", content=ARTIFACT_CONTENT, kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=task.id,
        metadata={"patch_intent_explanations": explanations, "patch_intent_approvals": {}},
    )
    job = Job(
        id=uuid4(), name="cont-job", user_prompt="continue", state=RunState.RUNNING,
        tasks=[task], artifacts=[art],
        metadata={"target_repo": str(repo_root.resolve())},
    )
    intent_id = make_intent_id(art.id, 0)
    if write_perm:
        set_permission(job, Capability.repo_generated_write, allow=True)
    if test_perm:
        set_permission(job, Capability.repo_test_run, allow=True)
    if approve:
        set_approval_state(job, intent_id, "approved", decided_by="human")
        for n in range(extra_intents):
            set_approval_state(job, make_intent_id(art.id, n + 1), "approved", decided_by="human")

    contract = build_default_run_contract(job)
    allowed = list(contract.allowed_actions)
    denied = [a for a in contract.denied_actions if a != ContractAction.PATCH_APPLY]
    if allow_apply and ContractAction.PATCH_APPLY not in allowed:
        allowed.append(ContractAction.PATCH_APPLY)
    contract = dataclasses.replace(
        contract,
        allowed_actions=tuple(allowed),
        denied_actions=tuple(denied),
        stop_before_apply=stop_before_apply,
        max_test_runs=max_test_runs,
    )
    save_contract(job, contract)
    save_job(job, root=data_dir)
    return job, intent_id


@pytest.fixture()
def env(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"; data_dir.mkdir()
    repo = tmp_path / "repo"; repo.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir, repo


# ---------------------------------------------------------------------------
# Eligibility (Step 1165)
# ---------------------------------------------------------------------------


class TestEligibility:
    def _elig(self, job, data_dir, intent_id=None):
        from packages.orchestration.do_continue import evaluate_continue_eligibility
        return evaluate_continue_eligibility(str(job.id), intent_id, data_dir)

    def test_eligible_happy_path(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        e = self._elig(job, data_dir)
        assert e.eligible is True
        assert e.intent_id == iid
        assert e.blockers == []

    def test_job_not_found(self, env):
        data_dir, _ = env
        from packages.orchestration.do_continue import evaluate_continue_eligibility
        e = evaluate_continue_eligibility(str(uuid4()), None, data_dir)
        assert not e.eligible
        assert "job_not_found" in e.blockers

    def test_no_approved_intent(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, approve=False)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "no_approved_intent" in e.blockers

    def test_multiple_approved_intents(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, extra_intents=1)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "multiple_approved_intents" in e.blockers
        assert "--intent-id" in e.next_safe_action

    def test_explicit_intent_id_resolves(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, extra_intents=1)
        e = self._elig(job, data_dir, intent_id=iid)
        assert e.eligible is True
        assert e.intent_id == iid

    def test_permission_denied(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, write_perm=False)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "permission_denied" in e.blockers

    def test_contract_apply_denied(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, allow_apply=False)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "contract_apply_denied" in e.blockers

    def test_stop_before_apply_true(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, stop_before_apply=True)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "stop_before_apply_true" in e.blockers

    def test_no_target_repo(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        job.metadata["target_repo"] = ""
        save_job(job, root=data_dir)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "no_target_repo" in e.blockers

    def test_test_budget_unconfigured(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, max_test_runs=0)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "test_budget_unconfigured" in e.blockers

    def test_test_permission_missing(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, test_perm=False)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "test_permission_missing" in e.blockers

    def test_blocked_has_next_safe_action(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, approve=False)
        e = self._elig(job, data_dir)
        assert e.next_safe_action
