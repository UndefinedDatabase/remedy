"""F006 correction, Finding 2 — EVERY exit after worktree creation cleans up.

Before this fix an early provider failure called ``_discard_staging()``, which
``rmtree``s the directory: git kept a deleted-but-registered (prunable) worktree
and the run's fcntl lock stayed held, so the same run id could never be claimed
again. Every path below must instead leave: no registered worktree, no held lock,
an unchanged main checkout, and an honest cleanup status.

Temporary git repositories and fake providers only. No provider call is made.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.orchestration import pingpong_loop as PL
from packages.orchestration import worktrees as W
from packages.orchestration.pingpong_loop import load_run, run_pingpong
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
    (r / "a.txt").write_text("v1\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


def _status(repo: Path) -> str:
    return _git(repo, "status", "--porcelain")


class _OkProvider:
    def build(self, prompt, **kw):
        return BuilderOutput(summary="noop", files_changed=[], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _capture_worktree(monkeypatch) -> dict:
    """Record the handle the loop creates, so a test can inspect it afterwards."""
    seen: dict = {}
    real_create = W.create

    def spy(job_id, r):
        h = real_create(job_id, r)
        seen["handle"] = h
        seen["path"] = Path(h.path)
        return h

    monkeypatch.setattr(W, "create", spy)
    return seen


def _assert_workspace_released(repo: Path, seen: dict, run_id: str) -> None:
    """No physical worktree, no registration, no lock — and main untouched."""
    assert not seen["path"].exists(), "physical worktree still on disk"
    assert len(W.list_worktrees(repo)) == 1, "a prunable worktree is still registered"
    assert _status(repo) == "", "main checkout was mutated"
    # The lock must be claimable again by anyone, including this process.
    h = W.create(run_id, repo)
    try:
        assert h.branch == f"remedy/{run_id}"
    finally:
        W.remove(h)


class TestEarlyProviderFailures:
    def test_builder_provider_construction_failure_releases_the_worktree(
        self, repo, monkeypatch,
    ):
        seen = _capture_worktree(monkeypatch)

        def boom(name, *, role, **kw):
            raise RuntimeError(f"provider {name!r} unavailable")

        monkeypatch.setattr(PL, "_create_provider_with_cwd", boom)
        res = run_pingpong("goal", str(repo), builder_name="claude-cli",
                           reviewer_name="claude-cli", max_rounds=1)

        assert res.final_status == "provider_unavailable"
        _assert_workspace_released(repo, seen, res.run_id)

    def test_reviewer_provider_construction_failure_releases_the_worktree(
        self, repo, monkeypatch,
    ):
        seen = _capture_worktree(monkeypatch)

        def only_reviewer_fails(name, *, role, **kw):
            if role == "reviewer":
                raise RuntimeError("reviewer unavailable")
            return _OkProvider()

        monkeypatch.setattr(PL, "_create_provider_with_cwd", only_reviewer_fails)
        res = run_pingpong("goal", str(repo), builder_name="claude-cli",
                           reviewer_name="claude-cli", max_rounds=1)

        assert res.final_status == "provider_unavailable"
        _assert_workspace_released(repo, seen, res.run_id)

    def test_early_failure_persists_an_honest_record(self, repo, monkeypatch):
        _capture_worktree(monkeypatch)

        def boom(name, *, role, **kw):
            raise RuntimeError("nope")

        monkeypatch.setattr(PL, "_create_provider_with_cwd", boom)
        res = run_pingpong("goal", str(repo), builder_name="claude-cli",
                           reviewer_name="claude-cli", max_rounds=1)

        wt = load_run(res.run_id)["worktree"]
        assert wt["isolation_mode"] == "worktree"
        assert wt["cleanup_status"] == "clean"
        assert wt["cleanup_error"] == ""
        assert wt["branch"] == f"remedy/{res.run_id}"

    def test_early_failure_may_keep_the_result_branch(self, repo, monkeypatch):
        _capture_worktree(monkeypatch)

        def boom(name, *, role, **kw):
            raise RuntimeError("nope")

        monkeypatch.setattr(PL, "_create_provider_with_cwd", boom)
        res = run_pingpong("goal", str(repo), builder_name="claude-cli",
                           reviewer_name="claude-cli", max_rounds=1)

        assert W._branch_exists(repo, res.worktree_branch)   # hand-off survives
        assert _git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip() != res.worktree_branch


class TestExceptionPaths:
    def test_context_construction_failure_releases_the_worktree(self, repo, monkeypatch):
        seen = _capture_worktree(monkeypatch)

        def boom(*a, **kw):
            raise RuntimeError("context exploded")

        monkeypatch.setattr(PL, "build_repo_context", boom)
        prov = _OkProvider()
        with pytest.raises(RuntimeError, match="context exploded"):
            run_pingpong("goal", str(repo), builder_provider=prov,
                         reviewer_provider=prov, builder_name="fake",
                         reviewer_name="fake", max_rounds=1)

        run_id = seen["handle"].job_id
        _assert_workspace_released(repo, seen, run_id)
        assert load_run(run_id)["worktree"]["cleanup_status"] == "clean"

    def test_builder_exception_before_any_change_releases_the_worktree(
        self, repo, monkeypatch,
    ):
        seen = _capture_worktree(monkeypatch)

        class _Exploding(_OkProvider):
            def build(self, prompt, **kw):
                raise RuntimeError("builder exploded")

        prov = _Exploding()
        with pytest.raises(RuntimeError, match="builder exploded"):
            run_pingpong("goal", str(repo), builder_provider=prov,
                         reviewer_provider=prov, builder_name="fake",
                         reviewer_name="fake", max_rounds=1)

        run_id = seen["handle"].job_id
        _assert_workspace_released(repo, seen, run_id)
        rec = load_run(run_id)
        assert rec["final_status"] == "run_error"
        assert "builder exploded" in rec["error"]
        assert rec["worktree"]["cleanup_status"] == "clean"

    def test_reviewer_exception_releases_the_worktree(self, repo, monkeypatch):
        seen = _capture_worktree(monkeypatch)

        class _Exploding(_OkProvider):
            def review(self, prompt, **kw):
                raise RuntimeError("reviewer exploded")

        prov = _Exploding()
        with pytest.raises(RuntimeError, match="reviewer exploded"):
            run_pingpong("goal", str(repo), builder_provider=prov,
                         reviewer_provider=prov, builder_name="fake",
                         reviewer_name="fake", max_rounds=1)

        _assert_workspace_released(repo, seen, seen["handle"].job_id)

    def test_test_command_exception_releases_the_worktree(self, repo, monkeypatch):
        seen = _capture_worktree(monkeypatch)

        def boom(*a, **kw):
            raise RuntimeError("test runner exploded")

        monkeypatch.setattr(PL, "_run_test_command", boom)
        prov = _OkProvider()
        with pytest.raises(RuntimeError, match="test runner exploded"):
            run_pingpong("goal", str(repo), builder_provider=prov,
                         reviewer_provider=prov, builder_name="fake",
                         reviewer_name="fake", max_rounds=1,
                         test_command="true")

        _assert_workspace_released(repo, seen, seen["handle"].job_id)


class TestNormalPaths:
    def test_success_releases_the_worktree_and_keeps_the_branch(self, repo, monkeypatch):
        seen = _capture_worktree(monkeypatch)
        prov = _OkProvider()
        res = run_pingpong("goal", str(repo), builder_provider=prov,
                           reviewer_provider=prov, builder_name="fake",
                           reviewer_name="fake", max_rounds=1)
        assert res.worktree_cleanup_status == "clean"
        assert W._branch_exists(repo, res.worktree_branch)
        _assert_workspace_released(repo, seen, res.run_id)

    def test_blocked_result_releases_the_worktree(self, repo, monkeypatch):
        seen = _capture_worktree(monkeypatch)

        class _Blocking(_OkProvider):
            def review(self, prompt, **kw):
                return ReviewerOutput(verdict="blocked", confidence="high",
                                      summary="no", provider="fake")

        prov = _Blocking()
        res = run_pingpong("goal", str(repo), builder_provider=prov,
                           reviewer_provider=prov, builder_name="fake",
                           reviewer_name="fake", max_rounds=1)
        assert res.final_status in ("staged_blocked", "repair_exhausted")
        assert res.worktree_cleanup_status == "clean"
        _assert_workspace_released(repo, seen, res.run_id)


class TestCleanupHonesty:
    def test_cleanup_failure_is_reported_not_hidden(self, repo, monkeypatch):
        _capture_worktree(monkeypatch)

        def failing_remove(handle, *, keep_branch=True):
            raise W.WorktreeError("git refused to remove the worktree")

        monkeypatch.setattr(W, "remove", failing_remove)
        prov = _OkProvider()
        res = run_pingpong("goal", str(repo), builder_provider=prov,
                           reviewer_provider=prov, builder_name="fake",
                           reviewer_name="fake", max_rounds=1)

        wt = load_run(res.run_id)["worktree"]
        assert wt["cleanup_status"] == "failed"        # never a false "clean"
        assert "git refused" in wt["cleanup_error"]

    def test_a_completed_run_never_leaves_a_prunable_registration(self, repo, monkeypatch):
        seen = _capture_worktree(monkeypatch)
        prov = _OkProvider()
        run_pingpong("goal", str(repo), builder_provider=prov, reviewer_provider=prov,
                     builder_name="fake", reviewer_name="fake", max_rounds=1)
        porcelain = _git(repo, "worktree", "list", "--porcelain")
        assert "prunable" not in porcelain
        assert str(seen["path"]) not in porcelain

    def test_a_failed_run_never_touches_another_jobs_retained_worktree(
        self, repo, monkeypatch,
    ):
        # Job A deliberately retains its worktree (still in flight).
        kept = W.create("keptjob", repo)
        (Path(kept.path) / "a.txt").write_text("job A work\n")

        _capture_worktree(monkeypatch)

        def boom(name, *, role, **kw):
            raise RuntimeError("nope")

        monkeypatch.setattr(PL, "_create_provider_with_cwd", boom)
        run_pingpong("goal", str(repo), builder_name="claude-cli",
                     reviewer_name="claude-cli", max_rounds=1)

        # Job A's worktree, content and lock are untouched by job B's failure.
        assert Path(kept.path).is_dir()
        assert (Path(kept.path) / "a.txt").read_text() == "job A work\n"
        with pytest.raises(W.WorktreeLockError):
            W.create("keptjob", repo)
        W.remove(kept)
