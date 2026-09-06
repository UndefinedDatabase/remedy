"""F006 primary path — the REAL planned-job runner must use a job-owned worktree.

Drives the actual `parse_job_file()` → `run_job()` path (and the real CLI job-run
entry point) against a temporary git repository with fake providers. A git job that
produces ``isolation_mode = copy`` is a failure, not a fallback.

No provider call is ever made.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.orchestration import pingpong_job as PJ
from packages.orchestration import worktrees as W
from packages.orchestration.data_paths import task_job_dir
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    job_worktree_id,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_loop import load_run
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


JOB_TEXT = """# Two-task job

## Task 1 — create one.txt

Create `one.txt`.

## Task 2 — read one.txt and create two.txt

Read `one.txt` and create `two.txt` from it.
"""


class _SequentialBuilder:
    """Fake Builder. Task 1 writes one.txt; Task 2 READS it and writes two.txt.

    Task 2 can only succeed if it is running in the same workspace Task 1 changed —
    which is the whole point of a job-owned worktree.
    """

    def __init__(self, cwd_holder: dict, seen: dict):
        self._cwd = cwd_holder
        self._seen = seen
        self.calls = 0

    def build(self, prompt, **kw):
        ws = Path(self._cwd["path"])
        self.calls += 1
        self._seen[f"cwd{self.calls}"] = str(ws)
        if self.calls == 1:
            (ws / "one.txt").write_text("from task one\n")
            return BuilderOutput(summary="wrote one.txt", files_changed=["one.txt"],
                                 provider="fake")
        prior = (ws / "one.txt").read_text()          # <- task 1's accepted change
        self._seen["task2_read"] = prior
        (ws / "two.txt").write_text(f"task two saw: {prior}")
        return BuilderOutput(summary="wrote two.txt", files_changed=["two.txt"],
                             provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _run_two_task_job(repo: Path, monkeypatch, seen: dict, **kw):
    job = parse_job_file(JOB_TEXT, str(repo))
    holder: dict = {}

    real_create = W.create

    def spy(job_id, r):
        h = real_create(job_id, r)
        holder["path"] = h.path
        seen["created_ids"] = seen.get("created_ids", []) + [job_id]
        return h

    monkeypatch.setattr(W, "create", spy)
    prov = _SequentialBuilder(holder, seen)
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1, **kw)
    seen["provider"] = prov
    seen["worktree_path"] = holder.get("path", "")
    return done


class TestGitJobUsesAWorktree:
    def test_git_job_runs_in_worktree_mode_never_copy(self, repo, monkeypatch):
        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)

        assert job.status == JOB_COMPLETED
        assert job.isolation_mode == "worktree"       # a copy here is a FAILURE
        assert job.worktree_branch == f"remedy/{job_worktree_id(job.job_id)}"
        assert job.worktree_path == f".remedy-wt/{job_worktree_id(job.job_id)}"
        for task in job.tasks:
            run = load_run(task.run_id)
            assert run["isolation_mode"] == "worktree"
            assert run["worktree"]["isolation_mode"] == "worktree"

    def test_no_full_repository_copy_is_made_for_a_git_target(self, repo, monkeypatch):
        def forbidden(*a, **kw):
            raise AssertionError("the full-copy helper must not run for a git job")

        monkeypatch.setattr(PJ, "_create_job_workspace_copy", forbidden)
        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)
        assert job.status == JOB_COMPLETED
        assert "job_workspaces" not in job.job_workspace_path

    def test_exactly_one_worktree_is_created_for_the_whole_job(self, repo, monkeypatch):
        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)
        assert seen["created_ids"] == [job_worktree_id(job.job_id)]   # not per task

    def test_provider_cwd_is_inside_the_worktree(self, repo, monkeypatch):
        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)
        for key in ("cwd1", "cwd2"):
            assert ".remedy-wt/" in seen[key]
            assert seen[key].endswith(job_worktree_id(job.job_id))


class TestSequentialTasksShareTheWorkspace:
    def test_task_two_sees_task_ones_accepted_change(self, repo, monkeypatch):
        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)
        assert seen["task2_read"] == "from task one\n"
        assert job.status == JOB_COMPLETED
        assert [t.status for t in job.tasks] == [PJ.TASK_APPLIED, PJ.TASK_APPLIED]

    def test_each_task_has_an_exact_task_local_diff(self, repo, monkeypatch):
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)

        d1 = (_pingpong_runs_dir() / job.tasks[0].run_id / "result.diff").read_text()
        d2 = (_pingpong_runs_dir() / job.tasks[1].run_id / "result.diff").read_text()

        assert "one.txt" in d1 and "two.txt" not in d1        # only task 1's change
        assert "two.txt" in d2 and "one.txt" not in d2        # only task 2's change
        assert job.tasks[0].safe_diff_files == ["one.txt"]
        assert job.tasks[1].safe_diff_files == ["two.txt"]

    def test_the_final_job_diff_contains_both_tasks(self, repo, monkeypatch):
        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)
        job_diff = (task_job_dir(job.job_id) / "result.diff").read_text()
        assert "one.txt" in job_diff and "two.txt" in job_diff
        assert job.result_diff_sha256 and job.result_diff_size_bytes > 0


class TestJobWorkspaceLifecycle:
    def test_main_checkout_is_byte_identical_before_and_after(self, repo, monkeypatch):
        before_status = _git(repo, "status", "--porcelain")
        before_head = _git(repo, "rev-parse", "HEAD").strip()
        seen: dict = {}
        _run_two_task_job(repo, monkeypatch, seen)

        assert _git(repo, "status", "--porcelain") == before_status == ""
        assert _git(repo, "rev-parse", "HEAD").strip() == before_head
        assert (repo / "base.txt").read_text() == "base\n"
        assert not (repo / "one.txt").exists()      # never leaked into the checkout

    def test_success_removes_the_worktree_and_keeps_the_branch(self, repo, monkeypatch):
        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)

        assert job.worktree_cleanup_status == "clean"
        assert not Path(seen["worktree_path"]).exists()
        assert len(W.list_worktrees(repo)) == 1
        assert W._branch_exists(repo, job.worktree_branch)     # the hand-off
        # No automatic merge and no automatic commit onto the checked-out branch.
        assert _git(repo, "rev-parse", "HEAD").strip() == _git(
            repo, "rev-parse", job.worktree_base_commit).strip()

    def test_a_blocked_job_retains_the_worktree_and_releases_the_lock(
        self, repo, monkeypatch,
    ):
        job = parse_job_file(JOB_TEXT, str(repo))
        holder: dict = {}
        real_create = W.create

        def spy(job_id, r):
            h = real_create(job_id, r)
            holder["path"] = h.path
            return h

        monkeypatch.setattr(W, "create", spy)

        class _Blocking(_SequentialBuilder):
            def review(self, prompt, **kw):
                return ReviewerOutput(verdict="blocked", confidence="high",
                                      summary="no", provider="fake")

        prov = _Blocking(holder, {})
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)

        assert done.status == JOB_BLOCKED
        assert done.worktree_cleanup_status == "retained"     # never "clean"
        assert Path(holder["path"]).is_dir()                  # work is kept
        assert (Path(holder["path"]) / "one.txt").read_text() == "from task one\n"
        # The lock is free: a later resume/recovery can claim the SAME worktree.
        rec = W.recover(job_worktree_id(done.job_id), repo)
        assert rec is not None and rec.branch == done.worktree_branch
        W.remove(rec)
        assert _git(repo, "status", "--porcelain") == ""

    def test_paused_job_is_resumable_and_second_run_reuses_the_worktree(
        self, repo, monkeypatch,
    ):
        seen: dict = {}
        job = parse_job_file(JOB_TEXT, str(repo))
        holder: dict = {}
        real_create = W.create

        def spy(job_id, r):
            h = real_create(job_id, r)
            holder["path"] = h.path
            return h

        monkeypatch.setattr(W, "create", spy)
        prov = _SequentialBuilder(holder, seen)

        paused = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                         builder_name="fake", reviewer_name="fake", max_rounds=1,
                         max_tasks=1)
        assert paused.status == "paused"
        assert paused.worktree_cleanup_status == "retained"
        assert Path(holder["path"]).is_dir()

        # Second run: same worktree, same branch — task 2 sees task 1's change.
        prov2 = _SequentialBuilder(holder, seen)
        prov2.calls = 1                        # continue as the second task
        done = run_job(job.job_id, builder_provider=prov2, reviewer_provider=prov2,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)
        assert done.status == JOB_COMPLETED
        assert seen["task2_read"] == "from task one\n"
        assert done.worktree_branch == paused.worktree_branch
        assert done.worktree_cleanup_status == "clean"
        assert not Path(holder["path"]).exists()
        assert W._branch_exists(repo, done.worktree_branch)


class TestNonGitTargetStillCopies:
    def test_non_git_target_uses_the_copy_fallback(self, tmp_path, monkeypatch):
        plain = tmp_path / "plain"
        plain.mkdir()
        (plain / "base.txt").write_text("base\n")

        job = parse_job_file("# J\n\n## Task 1 — write\n\nWrite one.txt.\n", str(plain))

        class _Simple:
            def build(self, prompt, **kw):
                return BuilderOutput(summary="noop", files_changed=[], provider="fake")

            def review(self, prompt, **kw):
                return ReviewerOutput(verdict="pass", confidence="high",
                                      summary="ok", provider="fake")

        prov = _Simple()
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)
        assert done.isolation_mode == "copy"
        assert "job_workspaces" in done.job_workspace_path
        assert load_job_plan(done.job_id).isolation_mode == "copy"


class TestEvidenceUsesTheWorktreeResult:
    def test_job_evidence_export_carries_the_worktree_task_runs(
        self, repo, monkeypatch, tmp_path,
    ):
        import json

        from packages.orchestration.job_evidence import _write_task_run_evidence

        seen: dict = {}
        job = _run_two_task_job(repo, monkeypatch, seen)

        out = tmp_path / "export"
        written: dict[str, str] = {}
        for t in job.tasks:
            class _T:
                task_id = t.task_id
                run_id = t.run_id
                status = t.status
            _write_task_run_evidence(_T(), str(out), written)

        for t in job.tasks:
            doc = json.loads((out / "task_runs" / t.task_id / "worktree.json").read_text())
            assert doc["isolation_mode"] == "worktree"
            assert doc["result_diff"]["sha256"]
            assert (out / "task_runs" / t.task_id / "result.diff").is_file()
