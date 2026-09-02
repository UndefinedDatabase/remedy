"""F006 T003 — isolation and parallel smoke.

Two fake-provider jobs against ONE temporary git repository. No Claude, Ollama or
Fable call is ever made; there is never an automatic merge into main.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.orchestration import worktrees as W
from packages.orchestration.pingpong_loop import run_pingpong
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
    (r / "shared.txt").write_text("base\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


def _status(repo: Path) -> str:
    return _git(repo, "status", "--porcelain")


class _WritingBuilder:
    """Fake Builder: writes its own content into the SAME filename in its cwd."""

    def __init__(self, cwd_holder, content: str):
        self._cwd = cwd_holder
        self._content = content

    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
        target = self._cwd.get("path") or ""
        # Never write outside the run's worktree: an empty path would land in the
        # operator's cwd, which is exactly the leak this feature prevents.
        assert target, "fake builder has no worktree to write into"
        (Path(target) / "shared.txt").write_text(self._content)
        return BuilderOutput(summary="wrote shared.txt",
                             files_changed=["shared.txt"], provider="fake")

    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _run_with_content(monkeypatch, repo: Path, content: str, keep: bool = False,
                      seen: list | None = None):
    """Run one fake job. The builder writes into THIS run's worktree.

    The worktree path is discovered by spying on worktrees.create(), which the
    loop calls before any provider runs.
    """
    holder: dict = {"path": ""}
    real_create = W.create

    def spy(job_id, r):
        h = real_create(job_id, r)
        holder["path"] = h.path
        if seen is not None:
            seen.append(h)
        return h

    monkeypatch.setattr(W, "create", spy)
    prov = _WritingBuilder(holder, content)
    return run_pingpong(
        "goal", str(repo), builder_provider=prov, reviewer_provider=prov,
        builder_name="fake", reviewer_name="fake", max_rounds=1,
        keep_staging=keep,
    )


class TestTwoJobsDoNotCollide:

    def test_each_run_gets_its_own_worktree_and_branch(self, repo, monkeypatch):
        seen: list = []
        r1 = _run_with_content(monkeypatch, repo, "job one\n", seen=seen)
        r2 = _run_with_content(monkeypatch, repo, "job two\n", seen=seen)

        assert r1.isolation_mode == "worktree" and r2.isolation_mode == "worktree"
        assert r1.worktree_branch != r2.worktree_branch
        assert r1.worktree_path != r2.worktree_path
        assert r1.worktree_branch.startswith("remedy/")
        assert r1.worktree_path.startswith(".remedy-wt/")
        paths = {h.path for h in seen}
        assert len(paths) == 2, "each run must get a distinct worktree"

    def test_main_checkout_identical_before_and_after_both_runs(self, repo, monkeypatch):
        before_status = _status(repo)
        before_head = _git(repo, "rev-parse", "HEAD").strip()
        before_content = (repo / "shared.txt").read_text()

        _run_with_content(monkeypatch, repo, "job one\n")
        _run_with_content(monkeypatch, repo, "job two\n")

        assert _status(repo) == before_status == ""
        assert _git(repo, "rev-parse", "HEAD").strip() == before_head
        assert (repo / "shared.txt").read_text() == before_content == "base\n"

    def test_both_jobs_may_write_the_same_filename_independently(self, repo, monkeypatch):
        r1 = _run_with_content(monkeypatch, repo, "job one\n", keep=True)
        r2 = _run_with_content(monkeypatch, repo, "job two\n", keep=True)

        # Both wrote shared.txt, in their OWN worktrees, with different content.
        assert (Path(r1.staging_path) / "shared.txt").read_text() == "job one\n"
        assert (Path(r2.staging_path) / "shared.txt").read_text() == "job two\n"
        assert r1.staging_path != r2.staging_path

    def test_each_result_diff_contains_only_its_own_change(self, repo, monkeypatch):
        r1 = _run_with_content(monkeypatch, repo, "job one\n")
        r2 = _run_with_content(monkeypatch, repo, "job two\n")

        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        d1 = (_pingpong_runs_dir() / r1.run_id / "result.diff").read_text()
        d2 = (_pingpong_runs_dir() / r2.run_id / "result.diff").read_text()

        assert "job one" in d1 and "job two" not in d1
        assert "job two" in d2 and "job one" not in d2
        assert r1.result_diff_sha256 and r1.result_diff_sha256 != r2.result_diff_sha256

    def test_no_automatic_merge_and_branches_remain(self, repo, monkeypatch):
        main_before = _git(repo, "rev-parse", "HEAD").strip()
        r1 = _run_with_content(monkeypatch, repo, "job one\n")
        r2 = _run_with_content(monkeypatch, repo, "job two\n")

        # main untouched; both result branches survive the physical cleanup.
        assert _git(repo, "rev-parse", "HEAD").strip() == main_before
        assert W._branch_exists(repo, r1.worktree_branch)
        assert W._branch_exists(repo, r2.worktree_branch)

    def test_cleanup_leaves_no_mounted_worktrees(self, repo, monkeypatch):
        _run_with_content(monkeypatch, repo, "job one\n")
        _run_with_content(monkeypatch, repo, "job two\n")
        # `git worktree list --porcelain` shows only the main checkout.
        assert len(W.list_worktrees(repo)) == 1
        assert not (repo / ".remedy-wt").exists() or not any(
            (repo / ".remedy-wt").iterdir()
        )

    def test_a_failed_job_does_not_remove_the_other_jobs_worktree(self, repo, monkeypatch):
        # Job A is kept (simulating a run still in flight / retained on failure).
        r_kept = _run_with_content(monkeypatch, repo, "job kept\n", keep=True)
        assert Path(r_kept.staging_path).is_dir()

        class _FailingBuilder(_WritingBuilder):
            def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
                return BuilderOutput(error="provider_error: boom", provider="fake")

        run_pingpong("goal", str(repo),
                     builder_provider=_FailingBuilder({}, ""),
                     reviewer_provider=_FailingBuilder({}, ""),
                     builder_name="fake", reviewer_name="fake", max_rounds=1)

        # The other job's worktree and content are untouched.
        assert Path(r_kept.staging_path).is_dir()
        assert (Path(r_kept.staging_path) / "shared.txt").read_text() == "job kept\n"

    def test_a_live_claim_blocks_a_duplicate_claim(self, repo):
        # A LIVE holder (a handle someone still owns) blocks a second claim.
        h = W.create("livejob", repo)
        try:
            with pytest.raises(W.WorktreeLockError):
                W.create("livejob", repo)
        finally:
            W.remove(h)

    def test_a_retained_run_leaves_no_orphaned_lock(self, repo, monkeypatch):
        # keep_staging retains the WORKTREE but must NOT retain the lock: once
        # run_pingpong has returned, the handle is unreachable, so a held fcntl
        # lock would make the run id permanently unclaimable by recovery.
        r = _run_with_content(monkeypatch, repo, "held\n", keep=True)
        assert r.worktree_cleanup_status == "retained"
        rec = W.recover(r.run_id, repo)
        assert rec is not None and rec.branch == r.worktree_branch
        assert (Path(rec.path) / "shared.txt").read_text() == "held\n"
        W.remove(rec)


class TestInterruptedRunRecovery:
    def test_killed_run_is_recoverable_diff_survives_branch_kept(self, repo):
        # 1. create worktree  2. modify a file  3. terminate before cleanup
        h = W.create("crashjob", repo)
        (Path(h.path) / "shared.txt").write_text("interrupted work\n")
        expected_diff = W.diff(h)
        assert "interrupted work" in expected_diff
        W.release_lock(h)                      # the process dies; no remove()

        # main checkout was never touched by the interrupted run
        assert _status(repo) == ""

        # 4. reopen through recovery
        rec = W.recover("crashjob", repo)
        assert rec is not None
        assert rec.branch == "remedy/crashjob"     # never a different branch
        # 5. the diff survives
        assert W.diff(rec) == expected_diff

        # 6. clean the physical worktree safely, 7. keep the result branch
        res = W.remove(rec, keep_branch=True)
        assert res["cleanup_status"] == "clean"
        assert not Path(h.path).exists()
        assert W._branch_exists(repo, "remedy/crashjob")
        assert len(W.list_worktrees(repo)) == 1
        assert _status(repo) == ""

    def test_recovery_clears_the_active_worktree_state(self, repo):
        h = W.create("crashjob", repo)
        W.release_lock(h)
        rec = W.recover("crashjob", repo)
        assert rec is not None
        W.remove(rec)
        # Nothing left to recover except the retained branch hand-off.
        again = W.recover("crashjob", repo)
        assert again is not None                # branch survives
        assert not Path(again.path).exists()    # but no physical worktree
        W.release_lock(again)
