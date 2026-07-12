"""F006 integrity — checkpoints survive GC, the hand-off is exactly the reviewed
work, promotion preserves file modes, and temporary cleanup never lies.

* Finding 1 — active tree checkpoints are protected by private Remedy refs.
* Finding 2 — the root diff must equal the union of the applied task manifests.
* Finding 3 — promotion reproduces the reviewed git file mode, not just the bytes.
* Finding 4 — temporary promotion cleanup is checked and reported honestly.

Temporary git repositories, fake providers and monkeypatching only. No provider
call is ever made.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import job_promote as JP
from packages.orchestration import pingpong_job as PJ
from packages.orchestration import worktrees as W
from packages.orchestration.artifact_contract_gate import check_worktree_artifacts
from packages.orchestration.job_evidence import export_job_evidence
from packages.orchestration.job_promote import promote_job
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    job_worktree_id,
    load_job_plan,
    parse_job_file,
    resume_job_plan,
    run_job,
)
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    (r / "base.txt").write_text("base\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


ONE_TASK = "# One\n\n## Task 1 — write\n\nWrite one.txt.\n"
TWO_TASKS = (
    "# Two\n\n## Task 1 — prior\n\nWrite prior.txt.\n\n"
    "## Task 2 — finish\n\nWrite finished.txt.\n"
)


class _Builder:
    """Fake Builder: writes the files for the current task; records review input."""

    def __init__(self, holder: dict, per_call: list[dict], seen: dict | None = None):
        self._holder = holder
        self._per_call = per_call
        self.calls = 0
        self.seen = seen if seen is not None else {}

    def build(self, prompt, **kw):
        ws = Path(self._holder["path"])
        files = self._per_call[min(self.calls, len(self._per_call) - 1)]
        self.calls += 1
        for name, content in files.items():
            (ws / name).write_text(content)
        return BuilderOutput(summary="wrote", files_changed=list(files), provider="fake")

    def review(self, prompt, **kw):
        self.seen["reviewer_prompt"] = prompt
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _spy(monkeypatch, holder):
    real = W.create

    def create(job_id, r):
        h = real(job_id, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", create)


def _run(repo, monkeypatch, per_call, text=ONE_TASK, seen=None, **kw):
    job = parse_job_file(text, str(repo))
    holder: dict = {}
    _spy(monkeypatch, holder)
    prov = _Builder(holder, per_call, seen)
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1, **kw)
    return done, holder


# ---------------------------------------------------------------------------
# Finding 1 — checkpoint refs keep active trees alive through gc/prune
# ---------------------------------------------------------------------------

class TestCheckpointRefsSurviveGc:
    def _crashed_two_task_job(self, repo, monkeypatch):
        """Task 1 accepted prior.txt; task 2 started, wrote partial.txt, died."""
        job, holder = _run(repo, monkeypatch, [{"prior.txt": "prior\n"}],
                           text=TWO_TASKS, max_tasks=1)
        assert job.status == "paused"
        assert job.tasks[0].status == PJ.TASK_APPLIED

        handle = W.recover(job_worktree_id(job.job_id), repo)
        job = load_job_plan(job.job_id)
        task2 = job.tasks[1]
        task2.status = PJ.TASK_RUNNING
        task2.task_start_tree = W.write_tree(handle)          # uncommitted job state
        task2.task_start_tree_ref = W.checkpoint_ref(
            job_worktree_id(job.job_id), "start", task2.task_id)
        W.set_checkpoint_ref(repo, task2.task_start_tree_ref, task2.task_start_tree)
        task2.task_attempt_state = "active"
        job.status = PJ.JOB_RUNNING
        PJ._persist_job(job)

        (Path(handle.path) / "partial.txt").write_text("partial\n")
        W.release_lock(handle)                                # the process dies
        return job, handle

    def test_the_task_start_tree_survives_git_gc_prune(self, repo, monkeypatch):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        tree = load_job_plan(job.job_id).tasks[1].task_start_tree

        _git(repo, "gc", "--prune=now", "--quiet")            # aggressive collection

        assert W.object_exists(repo, tree)                    # the ref kept it alive
        assert W.resolve_checkpoint_ref(
            repo, job.tasks[1].task_start_tree_ref) == tree

    def test_resume_after_gc_reviews_pre_crash_and_post_resume_files(
        self, repo, monkeypatch,
    ):
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir

        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        _git(repo, "gc", "--prune=now", "--quiet")

        holder = {"path": handle.path}
        seen: dict = {}
        prov = _Builder(holder, [{"finished.txt": "done\n"}], seen)
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)

        assert done.status == JOB_COMPLETED
        t2 = done.tasks[1]
        assert "partial.txt" in seen["reviewer_prompt"]
        assert "finished.txt" in seen["reviewer_prompt"]
        diff = (_pingpong_runs_dir() / t2.run_id / "result.diff").read_text()
        assert "partial.txt" in diff and "finished.txt" in diff
        assert "prior.txt" not in diff              # task 1's work is not re-reported
        assert sorted(t2.safe_diff_files) == ["finished.txt", "partial.txt"]

    def test_a_deleted_checkpoint_ref_blocks_instead_of_re_snapshotting(
        self, repo, monkeypatch,
    ):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        W.delete_checkpoint_ref(repo, job.tasks[1].task_start_tree_ref)

        holder = {"path": handle.path}
        prov = _Builder(holder, [{"finished.txt": "done\n"}])
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)

        assert done.status == JOB_BLOCKED
        assert "checkpoint_ref_missing" in done.error
        # The work is kept, the lock is free, no hidden fresh baseline was taken.
        assert (Path(handle.path) / "partial.txt").read_text() == "partial\n"
        assert done.worktree_cleanup_status == "retained"
        rec = W.recover(job_worktree_id(job.job_id), repo)
        assert rec is not None
        W.release_lock(rec)

    def test_a_ref_pointing_at_the_wrong_tree_blocks(self, repo, monkeypatch):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        rec = W.recover(job_worktree_id(job.job_id), repo)
        other_tree = W.write_tree(rec)                    # a DIFFERENT tree
        W.release_lock(rec)
        W.set_checkpoint_ref(repo, job.tasks[1].task_start_tree_ref, other_tree)

        holder = {"path": handle.path}
        prov = _Builder(holder, [{"finished.txt": "done\n"}])
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)
        assert done.status == JOB_BLOCKED
        assert "checkpoint_ref_mismatch" in done.error

    def test_a_completed_job_drops_its_checkpoint_refs(self, repo, monkeypatch):
        job, _ = _run(repo, monkeypatch, [{"one.txt": "hello\n"}])
        assert job.status == JOB_COMPLETED and job.worktree_cleanup_status == "clean"

        assert W.resolve_checkpoint_ref(repo, job.job_initial_tree_ref) == ""
        for t in job.tasks:
            assert W.resolve_checkpoint_ref(repo, t.task_start_tree_ref) == ""
        # The result branch is NOT a checkpoint ref and is untouched.
        assert W._branch_exists(repo, job.worktree_branch)

    def test_a_retained_job_keeps_its_checkpoint_refs(self, repo, monkeypatch):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        reloaded = load_job_plan(job.job_id)
        assert W.resolve_checkpoint_ref(
            repo, reloaded.job_initial_tree_ref) == reloaded.job_initial_tree
        assert W.resolve_checkpoint_ref(
            repo, reloaded.tasks[1].task_start_tree_ref
        ) == reloaded.tasks[1].task_start_tree

    def test_checkpoint_refs_live_in_the_private_namespace_only(self, repo, monkeypatch):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        refs = _git(repo, "for-each-ref", "--format=%(refname)").split()
        checkpoints = [r for r in refs if "checkpoints" in r]
        assert checkpoints
        assert all(r.startswith("refs/remedy/checkpoints/") for r in checkpoints)
        with pytest.raises(W.WorktreeError):
            W.set_checkpoint_ref(repo, "refs/heads/main", job.job_initial_tree)


# ---------------------------------------------------------------------------
# Finding 2 — the root hand-off must be exactly the reviewed task work
# ---------------------------------------------------------------------------

def _rogue_hook(monkeypatch, holder: dict, name: str = "rogue.txt"):
    """A finalization hook that sneaks an unreviewed file into the worktree."""
    real = PJ._check_handoff_coverage

    def hooked(job, handle):
        (Path(holder["path"]) / name).write_text("never reviewed\n")
        return real(job, handle)

    monkeypatch.setattr(PJ, "_check_handoff_coverage", hooked)
