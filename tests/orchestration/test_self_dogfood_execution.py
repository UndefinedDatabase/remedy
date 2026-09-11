"""Self-Dogfood Execution v0 tests (Steps 1448/1449/1450/1452).

Eligibility, branch/main safety, state machine, idempotency, redaction and architecture
guards. No real provider / git / main mutation.

Remedy deliberately has no end-to-end flow test here any more: F275 T001 deleted the
Provider Trust Gate and its `provider intake-repair` command, so nothing can move an
attempt past `awaiting_external_candidate` and the round trip the old test drove no
longer exists (R-0866).
"""
from __future__ import annotations

import dataclasses
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration import self_dogfood as SD
from packages.orchestration import self_dogfood_execution as SE
from packages.orchestration.proposed_tasks import (
    ProposedTaskStatus,
    load_proposed_tasks,
    save_proposed_tasks,
    transition_status,
)
from packages.orchestration.storage import save_job


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    for f in ("live_review.md", "plan.md", "context.md"):
        (ad / f).write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_AGENT_DIR", str(ad))
    # Default: a safe (non-main) branch.
    monkeypatch.setattr(SE, "current_branch", lambda: "feature/x")
    return d


def _approved_task(data_dir, *, failure=True, repo="."):
    t = Task(description="t")
    arts = []
    if failure:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=str(t.id),
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_task_id": str(t.id), "related_files": ["docs/guide.md"],
                                "safe_summary": "doc gap"})
        arts.append(fa)
    job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=arts, metadata={"target_repo": repo})
    save_job(job, root=data_dir)
    SD.propose_self_improvement(str(job.id), top=1, data_dir=data_dir)
    tasks = load_proposed_tasks(str(job.id), data_dir)
    transition_status(tasks[0], ProposedTaskStatus.APPROVED_FOR_BUILD, by="human")
    save_proposed_tasks(str(job.id), tasks, data_dir)
    return job, tasks[0]


# ---------------------------------------------------------------------------
# Eligibility + branch safety (Steps 1432/1433)
# ---------------------------------------------------------------------------


class TestEligibility:
    def test_approved_self_task_eligible(self, env):
        job, pt = _approved_task(env)
        e = SE.evaluate_self_execution_eligibility(pt.id, str(job.id), env)
        assert e.eligible and e.item_fingerprint

    def test_missing_task(self, env):
        e = SE.evaluate_self_execution_eligibility("nope", str(uuid4()), env)
        assert not e.eligible and e.stop_reason == SE.StopReason.PROPOSED_TASK_NOT_FOUND

    def test_unapproved_blocks(self, env):
        job, _ = _approved_task(env)
        SD.propose_self_improvement(str(job.id), top=2, data_dir=env)
        tasks = load_proposed_tasks(str(job.id), env)
        unapproved = next(t for t in tasks if t.status == ProposedTaskStatus.PROPOSED)
        e = SE.evaluate_self_execution_eligibility(unapproved.id, str(job.id), env)
        assert not e.eligible and e.stop_reason == SE.StopReason.NOT_APPROVED

    def test_main_branch_blocks(self, env, monkeypatch):
        monkeypatch.setattr(SE, "current_branch", lambda: "main")
        job, pt = _approved_task(env)
        e = SE.evaluate_self_execution_eligibility(pt.id, str(job.id), env)
        assert not e.eligible and e.stop_reason == SE.StopReason.MAIN_BRANCH_UNSAFE

    def test_unknown_branch_blocks(self, env, monkeypatch):
        monkeypatch.setattr(SE, "current_branch", lambda: "")
        job, pt = _approved_task(env)
        e = SE.evaluate_self_execution_eligibility(pt.id, str(job.id), env)
        assert not e.eligible and e.stop_reason == SE.StopReason.MAIN_BRANCH_UNSAFE

    def test_contract_blocked(self, env):
        from packages.orchestration.run_contract import (
            ContractAction,
            build_default_run_contract,
            save_contract,
        )
        job, pt = _approved_task(env)
        c = build_default_run_contract(job)
        c = dataclasses.replace(c, allowed_actions=tuple(
            a for a in c.allowed_actions if a != ContractAction.SELF_EXECUTE_PREPARE))
        save_contract(job, c); save_job(job, root=env)
        e = SE.evaluate_self_execution_eligibility(pt.id, str(job.id), env)
        assert not e.eligible and e.stop_reason == SE.StopReason.CONTRACT_BLOCKED


# ---------------------------------------------------------------------------
# Start / state machine / idempotency (Steps 1434/1436/1448)
# ---------------------------------------------------------------------------


class TestStartAndIdempotency:
    def test_execute_awaits_candidate(self, env):
        job, pt = _approved_task(env)
        r = SE.start_self_execution(pt.id, str(job.id), env)
        assert r.state == SE.AttemptState.AWAITING_EXTERNAL_CANDIDATE
        assert r.request_package_id
        assert r.next_safe_action == "remedy self status --json"

    def test_execute_idempotent_resume(self, env):
        job, pt = _approved_task(env)
        r1 = SE.start_self_execution(pt.id, str(job.id), env)
        r2 = SE.start_self_execution(pt.id, str(job.id), env)
        assert r1.attempt_id == r2.attempt_id
        assert len(SE.list_attempts(env)) == 1

    def test_main_blocks_start(self, env, monkeypatch):
        monkeypatch.setattr(SE, "current_branch", lambda: "main")
        job, pt = _approved_task(env)
        r = SE.start_self_execution(pt.id, str(job.id), env)
        assert r.state == SE.AttemptState.BLOCKED
        assert r.stop_reason == SE.StopReason.MAIN_BRANCH_UNSAFE
        assert SE.list_attempts(env) == []

    def test_transition_rejects_illegal(self, env):
        a = SE.SelfImprovementAttempt(attempt_id="x", state=SE.AttemptState.PROPOSED)
        assert SE._transition(a, SE.AttemptState.COMPLETED) is False  # illegal jump
        assert a.state == SE.AttemptState.PROPOSED


# ---------------------------------------------------------------------------
# End-to-end (Step 1452)
# ---------------------------------------------------------------------------


class TestEndToEnd:
    # R-0084's mislink guard (`test_reconcile_does_not_mislink_foreign_intent`) is gone
    # with F275 T001: reconcile no longer links anything, so the property is held BY
    # CONSTRUCTION rather than by a test. See R-0866.

    def test_reconcile_idempotent_after_completed(self, env, monkeypatch, tmp_path):
        # Re-running reconcile on a completed attempt is stable (no double work).
        # (Lightweight: completed attempt persisted directly.)
        a = SE.SelfImprovementAttempt(attempt_id="done1", job_id=str(uuid4()),
                                      state=SE.AttemptState.COMPLETED, proof_status="verified",
                                      created_at=SE._now())
        SE.save_attempt(a, env)
        r = SE.reconcile_self_attempt("done1", env)
        assert r.state == SE.AttemptState.COMPLETED


# ---------------------------------------------------------------------------
# Architecture guards (Step 1450)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/self_dogfood_execution.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_network_subprocess(self):
        for ln in self._imports():
            for bad in ("subprocess", "socket", "requests", "httpx", "urllib", "selenium", "playwright"):
                assert bad not in ln
        assert "import subprocess" not in self.SRC
        assert "shell=True" not in self.SRC

    def test_no_provider_sdk(self):
        for ln in self._imports():
            low = ln.lower()
            for bad in ("ollama", "anthropic", "openai", "litellm"):
                assert bad not in low

    def test_no_apply_or_source_apply_import(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "source_apply" not in ln
            assert "test_execution_service" not in ln
        # do_continue is invoked by the human via CLI, not imported/called here.
        assert "run_do_continue" not in self.SRC

    def test_no_git_or_job_tasks_or_pr(self):
        assert "os.system" not in self.SRC
        assert ".tasks.append" not in self.SRC
        for ln in self._imports():
            assert "import git" not in ln and "from git" not in ln
        assert "gh pr" not in self.SRC.lower()

    def test_next_actions_catalog_backed(self, env):
        # The command the ATTEMPT ITSELF reports must resolve in the shipped catalog —
        # not a string this test supplies, which is what it used to assert.
        from packages.orchestration.do_run import validate_next_safe_action_command
        job, pt = _approved_task(env)
        r = SE.start_self_execution(pt.id, str(job.id), env)
        assert r.next_safe_action
        assert validate_next_safe_action_command(r.next_safe_action)
        rec = SE.reconcile_self_attempt(r.attempt_id, env)
        assert rec.next_safe_action
        assert validate_next_safe_action_command(rec.next_safe_action)


# ---------------------------------------------------------------------------
# current_branch() repo forms (R-0159) — .git directory vs worktree gitfile
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                   text=True, check=True)


class TestCurrentBranchRepoForms:
    """R-0159: a linked worktree's `.git` is a gitfile pointer, not a
    directory — current_branch() must resolve HEAD in both forms."""

    @pytest.fixture()
    def repo(self, tmp_path) -> Path:
        r = tmp_path / "repo"
        r.mkdir()
        _git(r, "init", "-q")
        _git(r, "config", "user.email", "t@e.com")
        _git(r, "config", "user.name", "T")
        _git(r, "config", "commit.gpgsign", "false")
        (r / "a.txt").write_text("v1\n")
        _git(r, "add", "-A")
        _git(r, "commit", "-qm", "init")
        _git(r, "checkout", "-qb", "feature/primary")
        return r

    def test_git_directory_form(self, repo, monkeypatch):
        monkeypatch.chdir(repo)
        assert SE.current_branch() == "feature/primary"

    def test_worktree_gitfile_form(self, repo, monkeypatch):
        wt = repo.parent / "wt"
        _git(repo, "worktree", "add", "-q", "-b", "feature/linked",
             str(wt))
        monkeypatch.chdir(wt)
        assert (wt / ".git").is_file()  # the R-0159 precondition
        assert SE.current_branch() == "feature/linked"

    def test_detached_head_unknown(self, repo, monkeypatch):
        _git(repo, "checkout", "-q", "--detach")
        monkeypatch.chdir(repo)
        assert SE.current_branch() == ""

    def test_no_repo_unknown(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert SE.current_branch() == ""
