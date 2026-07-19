"""F1/F2 (round 33) — the publication lifecycle is atomic and no-clobber, and Git-status determination
is fail-closed. Exactly one concurrent publisher wins the same final path; the loser returns a
controlled collision and no successful result is silently overwritten; a Git failure is never read as
"untracked"."""
from __future__ import annotations

import os
import shutil
import subprocess
import threading
from pathlib import Path

import pytest

from packages.orchestration.safe_publish import (
    PublishCollisionError, git_tracked_status, publish_atomically,
)

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git required")


def _repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True, capture_output=True)
    return repo


def _src(repo, content=b"zipbytes"):
    import tempfile
    fd, p = tempfile.mkstemp(prefix=".part", dir=str(repo))
    os.write(fd, content)
    os.close(fd)
    return p


class TestAtomicPublish:
    def test_single_publish_moves_and_cleans_source(self, tmp_path):
        repo = _repo(tmp_path)
        src = _src(repo, b"complete-zip")
        final = str(repo / "remedy-review-x.zip")
        publish_atomically(src, final, str(repo))
        assert Path(final).read_bytes() == b"complete-zip"
        assert not os.path.exists(src)                     # private temp cleaned

    def test_concurrent_publishers_exactly_one_wins(self, tmp_path):
        repo = _repo(tmp_path)
        final = str(repo / "remedy-review-race.zip")
        results = {}
        barrier = threading.Barrier(8)

        def worker(i):
            src = _src(repo, f"content-{i}".encode())
            barrier.wait()
            try:
                publish_atomically(src, final, str(repo))
                results[i] = "ok"
            except PublishCollisionError:
                results[i] = "collision"
            # loser's source must be cleaned
            assert not os.path.exists(src)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        wins = [i for i, r in results.items() if r == "ok"]
        losers = [i for i, r in results.items() if r == "collision"]
        assert len(wins) == 1, results
        assert len(losers) == 7, results
        # The winner's bytes are intact and never overwritten by a loser.
        assert Path(final).read_bytes() == f"content-{wins[0]}".encode()

    def test_tracked_final_preserved_and_blocks(self, tmp_path):
        repo = _repo(tmp_path)
        final = repo / "out.zip"
        final.write_bytes(b"tracked")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "c"], cwd=repo, check=True, capture_output=True)
        src = _src(repo, b"new")
        with pytest.raises(PublishCollisionError):
            publish_atomically(src, str(final), str(repo))
        assert final.read_bytes() == b"tracked"            # byte-identical
        assert not os.path.exists(src)                     # source cleaned

    def test_foreign_existing_final_preserved_and_blocks(self, tmp_path):
        repo = _repo(tmp_path)
        final = repo / "remedy-review-foreign.zip"
        final.write_bytes(b"foreign")
        src = _src(repo, b"new")
        with pytest.raises(PublishCollisionError):
            publish_atomically(src, str(final), str(repo))
        assert final.read_bytes() == b"foreign"

    def test_builder_no_longer_unlinks_out_path(self):
        import inspect
        from packages.orchestration import review_zip
        src = inspect.getsource(review_zip.build_review_zip_from_snapshot)
        assert "out_path.unlink()" not in src


class TestGitTrackedStatusFailClosed:
    def test_tracked(self, tmp_path):
        repo = _repo(tmp_path)
        f = repo / "f.txt"; f.write_text("x")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "c"], cwd=repo, check=True, capture_output=True)
        assert git_tracked_status(str(f), str(repo))[0] == "TRACKED"

    def test_untracked_absent(self, tmp_path):
        repo = _repo(tmp_path)
        assert git_tracked_status(str(repo / "nope.zip"), str(repo))[0] == "UNTRACKED"

    def test_git_exit_128_blocks(self, tmp_path):
        # repo_root is not a git repository → git exits 128; must be GIT_FAILED, never UNTRACKED.
        notrepo = tmp_path / "plain"; notrepo.mkdir()
        status, diag = git_tracked_status(str(notrepo / "x.zip"), str(notrepo))
        assert status == "GIT_FAILED" and diag
        with pytest.raises(PublishCollisionError):
            publish_atomically(_src(tmp_path), str(notrepo / "x.zip"), str(notrepo))

    def test_git_unavailable_blocks(self, tmp_path, monkeypatch):
        repo = _repo(tmp_path)
        import packages.orchestration.safe_publish as sp

        def boom(*a, **k):
            raise FileNotFoundError("git")
        monkeypatch.setattr(sp.subprocess, "run", boom)
        assert git_tracked_status(str(repo / "x.zip"), str(repo))[0] == "GIT_UNAVAILABLE"

    def test_git_timeout_blocks(self, tmp_path, monkeypatch):
        repo = _repo(tmp_path)
        import packages.orchestration.safe_publish as sp

        def slow(*a, **k):
            raise subprocess.TimeoutExpired(cmd="git", timeout=10)
        monkeypatch.setattr(sp.subprocess, "run", slow)
        assert git_tracked_status(str(repo / "x.zip"), str(repo))[0] == "GIT_TIMED_OUT"
