"""F006 T001 — worktree manager: create/snapshot/diff/remove/recover + locking.

Temporary git repositories only. No provider is ever invoked.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.orchestration import worktrees as W
from packages.orchestration.worktrees import (
    WorktreeConflictError,
    WorktreeError,
    WorktreeLockError,
)


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True)
    return proc.stdout


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


# ---------------------------------------------------------------------------
# create / snapshot / diff / remove
# ---------------------------------------------------------------------------

class TestCreate:
    def test_create_makes_worktree_and_branch(self, repo):
        h = W.create("job1", repo)
        try:
            assert h.created is True
            assert h.branch == "remedy/job1"
            assert h.relative_path == ".remedy-wt/job1"
            assert Path(h.path).is_dir()
            assert (Path(h.path) / "a.txt").read_text() == "v1\n"
            assert h.base_commit and h.head_commit == h.base_commit
        finally:
            W.remove(h)

    def test_main_checkout_stays_clean(self, repo):
        before = _status(repo)
        h = W.create("job1", repo)
        try:
            (Path(h.path) / "a.txt").write_text("changed\n")
            (Path(h.path) / "new.txt").write_text("new\n")
            assert _status(repo) == before == ""
        finally:
            W.remove(h)
        assert _status(repo) == before

    def test_repeated_create_for_same_job_reattaches(self, repo):
        h1 = W.create("job1", repo)
        path1, branch1 = h1.path, h1.branch
        W.release_lock(h1)                     # simulate the first claim ending
        h2 = W.create("job1", repo)
        try:
            assert h2.created is False         # re-attached, not recreated
            assert h2.path == path1 and h2.branch == branch1
        finally:
            W.remove(h2)

    def test_evidence_record_has_no_absolute_path(self, repo):
        h = W.create("job1", repo)
        try:
            ev = h.to_evidence()
            assert ev["worktree_path"] == ".remedy-wt/job1"
            assert ev["worktree_branch"] == "remedy/job1"
            assert ev["base_commit"] and ev["worktree_head"]
            assert not any(str(v).startswith("/") for v in ev.values())
        finally:
            W.remove(h)


class TestSnapshotAndDiff:
    def test_snapshot_returns_head(self, repo):
        h = W.create("job1", repo)
        try:
            assert W.snapshot(h) == _git(repo, "rev-parse", "HEAD").strip()
        finally:
            W.remove(h)

    def test_diff_covers_edits_and_new_files(self, repo):
        h = W.create("job1", repo)
        try:
            (Path(h.path) / "a.txt").write_text("v2\n")
            (Path(h.path) / "new.txt").write_text("hello\n")
            text = W.diff(h)
            assert "a/a.txt" in text and "+v2" in text
            assert "new.txt" in text and "+hello" in text
            # repository-relative paths only
            assert str(h.path) not in text
        finally:
            W.remove(h)

    def test_diff_is_deterministic(self, repo):
        h = W.create("job1", repo)
        try:
            (Path(h.path) / "a.txt").write_text("v2\n")
            assert W.diff(h) == W.diff(h)
        finally:
            W.remove(h)

    def test_write_result_diff_records_hash_and_size(self, repo, tmp_path):
        import hashlib
        h = W.create("job1", repo)
        try:
            (Path(h.path) / "a.txt").write_text("v2\n")
            out = tmp_path / "ev" / "result.diff"
            info = W.write_result_diff(h, out)
            data = out.read_bytes()
            assert info["sha256"] == hashlib.sha256(data).hexdigest()
            assert info["size_bytes"] == len(data)
            assert info["empty"] is False
        finally:
            W.remove(h)


class TestRemove:
    def test_remove_keeps_branch_by_default(self, repo):
        h = W.create("job1", repo)
        (Path(h.path) / "a.txt").write_text("v2\n")
        res = W.remove(h)
        assert res["worktree_removed"] is True
        assert res["branch_kept"] is True
        assert res["cleanup_status"] == "clean"
        assert not Path(h.path).exists()
        assert W._branch_exists(repo, "remedy/job1")          # hand-off survives
        assert len(W.list_worktrees(repo)) == 1               # only the main one

    def test_remove_can_drop_the_branch_explicitly(self, repo):
        h = W.create("job1", repo)
        res = W.remove(h, keep_branch=False)
        assert res["branch_kept"] is False
        assert not W._branch_exists(repo, "remedy/job1")

    def test_remove_never_merges_into_main(self, repo):
        main_before = _git(repo, "rev-parse", "HEAD").strip()
        h = W.create("job1", repo)
        (Path(h.path) / "a.txt").write_text("v2\n")
        _git(Path(h.path), "add", "-A")
        _git(Path(h.path), "commit", "-qm", "work")
        W.remove(h)
        assert _git(repo, "rev-parse", "HEAD").strip() == main_before
        assert (repo / "a.txt").read_text() == "v1\n"


# ---------------------------------------------------------------------------
# Conflicts, locking, unsafe input
# ---------------------------------------------------------------------------

class TestConflicts:
    def test_branch_collision_with_foreign_branch_is_refused(self, repo):
        # remedy/job1 exists but is checked out for a DIFFERENT worktree path.
        h_other = W.create("job2", repo)
        try:
            # Force job2's worktree onto job1's branch, then claim job1.
            _git(Path(h_other.path), "checkout", "-q", "-b", "remedy/job1")
            with pytest.raises(WorktreeConflictError):
                W.create("job1", repo)
        finally:
            _git(Path(h_other.path), "checkout", "-q", "remedy/job2")
            W.remove(h_other)

    def test_stale_directory_is_reported_not_silently_reused(self, repo):
        path = W.worktree_path_for(repo, "job1")
        path.mkdir(parents=True)
        (path / "junk.txt").write_text("left behind\n")
        with pytest.raises(WorktreeConflictError):
            W.create("job1", repo)

    def test_worktree_on_wrong_branch_is_refused(self, repo):
        h = W.create("job1", repo)
        try:
            _git(Path(h.path), "checkout", "-q", "-b", "someone-elses")
            W.release_lock(h)
            with pytest.raises(WorktreeConflictError):
                W.create("job1", repo)
        finally:
            _git(Path(h.path), "checkout", "-q", "remedy/job1")
            W.remove(h)


class TestLocking:
    def test_lock_collision_blocks_a_duplicate_claim(self, repo):
        h = W.create("job1", repo)
        try:
            with pytest.raises(WorktreeLockError):
                W.create("job1", repo)          # same process, lock still held
        finally:
            W.remove(h)

    def test_lock_lives_under_the_project_data_area(self, repo):
        h = W.create("job1", repo)
        try:
            lock = Path(h.lock_path)
            assert lock.name == "job1.lock"
            assert lock.parent.name == "locks"
            assert lock.parent.parent.name == W.project_id(repo)
        finally:
            W.remove(h)

    def test_lock_is_released_after_remove(self, repo):
        h = W.create("job1", repo)
        W.remove(h)
        again = W.create("job1", repo)          # must be claimable again
        try:
            assert again.branch == "remedy/job1"
        finally:
            W.remove(again)

    def test_project_id_is_stable_and_per_repository(self, repo, tmp_path):
        other = tmp_path / "other"
        other.mkdir()
        assert W.project_id(repo) == W.project_id(repo)
        assert W.project_id(repo) != W.project_id(other)


class TestUnsafeInput:
    @pytest.mark.parametrize("bad", [
        "../escape", "a/b", "..", "", "-leading-dash", "x" * 65, "job;rm -rf /",
    ])
    def test_unsafe_job_ids_are_rejected(self, bad):
        with pytest.raises(WorktreeError):
            W.validate_job_id(bad)

    def test_path_traversal_never_escapes_the_worktree_dir(self, repo):
        with pytest.raises(WorktreeError):
            W.worktree_path_for(repo, "../../etc")
        with pytest.raises(WorktreeError):
            W.create("../../etc", repo)

    def test_branch_name_is_namespaced(self):
        assert W.branch_for("abc") == "remedy/abc"
        with pytest.raises(WorktreeError):
            W.branch_for("../x")


# ---------------------------------------------------------------------------
# Recovery after an interrupted run
# ---------------------------------------------------------------------------

class TestRecover:
    def test_recover_returns_none_when_nothing_exists(self, repo):
        assert W.recover("nojob", repo) is None

    def test_interrupted_run_is_recoverable_and_keeps_its_diff(self, repo):
        h = W.create("job1", repo)
        (Path(h.path) / "a.txt").write_text("interrupted work\n")
        expected = W.diff(h)
        # Simulate a crash: the process dies WITHOUT remove(); only the lock dies.
        W.release_lock(h)

        rec = W.recover("job1", repo)
        assert rec is not None
        try:
            assert rec.branch == "remedy/job1"          # never a different branch
            assert rec.path == h.path
            assert W.diff(rec) == expected              # the work survived
        finally:
            W.remove(rec)

    def test_recovery_keeps_the_result_branch_after_cleanup(self, repo):
        h = W.create("job1", repo)
        (Path(h.path) / "a.txt").write_text("work\n")
        _git(Path(h.path), "add", "-A")
        _git(Path(h.path), "commit", "-qm", "wip")
        W.release_lock(h)

        rec = W.recover("job1", repo)
        assert rec is not None
        res = W.remove(rec, keep_branch=True)
        assert res["branch_kept"] is True
        assert W._branch_exists(repo, "remedy/job1")
        assert not Path(h.path).exists()
        assert len(W.list_worktrees(repo)) == 1

    def test_recover_finds_a_branch_left_after_physical_cleanup(self, repo):
        h = W.create("job1", repo)
        W.remove(h, keep_branch=True)              # worktree gone, branch kept
        rec = W.recover("job1", repo)
        assert rec is not None and rec.branch == "remedy/job1"
        W.release_lock(rec)

    def test_recover_reconciles_a_stale_directory(self, repo):
        h = W.create("job1", repo)
        path = Path(h.path)
        W.release_lock(h)
        # Kill the registration but leave the directory (a crashed cleanup).
        _git(repo, "worktree", "remove", "--force", str(path))
        path.mkdir(parents=True, exist_ok=True)
        (path / "leftover.txt").write_text("x\n")

        rec = W.recover("job1", repo)
        assert rec is not None
        try:
            assert rec.branch == "remedy/job1"
        finally:
            W.remove(rec)
        assert not path.exists()
