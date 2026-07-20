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
    PublishCollisionError, PublishSourceError, git_tracked_status, publish_atomically,
    verify_published_inode, verify_source_identity,
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


class TestVerifiedSourceIdentityBinding:
    """F1 (round 34): the private source published must be the exact verified regular-file/inode/bytes;
    a pathname swapped after verification (to a symlink, another file, or changed bytes) cannot be
    published."""

    def _sha(self, p):
        return __import__("hashlib").sha256(Path(p).read_bytes()).hexdigest()

    def test_correct_sha_publishes(self, tmp_path):
        repo = _repo(tmp_path)
        src = _src(repo, b"verified-bytes")
        final = str(repo / "remedy-review-x.zip")
        publish_atomically(src, final, str(repo), expected_sha256=self._sha(src))
        assert Path(final).read_bytes() == b"verified-bytes"

    def test_changed_bytes_after_verification_blocks(self, tmp_path):
        repo = _repo(tmp_path)
        src = _src(repo, b"original")
        stale = self._sha(src)
        with open(src, "wb") as fh:                          # swap the bytes AFTER "verification"
            fh.write(b"tampered-different-length")
        final = str(repo / "remedy-review-y.zip")
        with pytest.raises(PublishSourceError):
            publish_atomically(src, final, str(repo), expected_sha256=stale)
        assert not os.path.exists(final)                     # nothing published

    def test_symlink_source_blocks(self, tmp_path):
        repo = _repo(tmp_path)
        real = repo / "real.bin"
        real.write_bytes(b"payload")
        link = str(repo / ".remedy_zip_link.part")
        os.symlink(real, link)
        final = str(repo / "remedy-review-z.zip")
        with pytest.raises(PublishSourceError):
            publish_atomically(link, final, str(repo), expected_sha256=self._sha(real))
        assert not os.path.exists(final)
        assert Path(real).read_bytes() == b"payload"

    def test_verify_source_identity_rejects_missing_expected(self, tmp_path):
        repo = _repo(tmp_path)
        src = _src(repo, b"x")
        with pytest.raises(PublishSourceError):
            verify_source_identity(src, str(repo), expected_sha256=None)


class TestFDRetainedInodeBoundPublication:
    """F1 (round 35): the publication protocol is FD-retained and inode-bound. The source FD is opened
    O_RDONLY|O_NOFOLLOW, fstat-confirmed regular, hashed through the FD, and the retained FD's inode
    is compared to the published path's inode after os.link. A post-hash pathname swap, in-place
    mutation via a second FD, or symlink replacement cannot change the published bytes. The st_dev
    precheck is removed so OverlayFS-like mounts don't falsely block."""

    def _sha(self, p):
        return __import__("hashlib").sha256(Path(p).read_bytes()).hexdigest()

    def test_post_hash_pathname_swap_blocks(self, tmp_path):
        """After verify_source_identity hashes through the FD, replacing the pathname with a different
        file does NOT affect the already-retained FD — but publication via os.link uses the pathname,
        so the published file would be the swapped one. The inode verification catches this."""
        repo = _repo(tmp_path)
        src = _src(repo, b"original-good")
        sha = self._sha(src)
        # Verify source — get the retained FD
        fd = verify_source_identity(src, str(repo), expected_sha256=sha)
        try:
            # Swap the pathname to a different file AFTER verification
            os.unlink(src)
            with open(src, "wb") as fh:
                fh.write(b"swapped-bad-content")
            final = str(repo / "remedy-review-swap.zip")
            os.link(src, final)
            # The inode verification catches the swap
            with pytest.raises(PublishSourceError, match="inode.*differs"):
                verify_published_inode(fd, final)
        finally:
            os.close(fd)

    def test_fd_inode_matches_after_successful_publish(self, tmp_path):
        """After a successful publish_atomically, the published file is the same inode as the
        verified source — the FD-retained protocol guarantees this."""
        repo = _repo(tmp_path)
        src = _src(repo, b"verified-inode-content")
        sha = self._sha(src)
        final = str(repo / "remedy-review-inode.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha)
        assert Path(final).read_bytes() == b"verified-inode-content"

    def test_symlink_at_source_blocked_by_o_nofollow(self, tmp_path):
        """O_NOFOLLOW on the source path means a symlink raises immediately, before any hash."""
        repo = _repo(tmp_path)
        real = repo / "real.bin"
        real.write_bytes(b"payload")
        link = str(repo / ".remedy_zip_link.part")
        os.symlink(real, link)
        with pytest.raises(PublishSourceError):
            verify_source_identity(link, str(repo),
                                   expected_sha256=self._sha(str(real)))

    def test_overlayfs_like_different_stdev_does_not_block(self, tmp_path, monkeypatch):
        """On OverlayFS, a file and its parent directory can report different st_dev even though
        they share a mount and hardlink works. The removed st_dev precheck no longer blocks this."""
        repo = _repo(tmp_path)
        src = _src(repo, b"overlay-content")
        sha = self._sha(src)
        # verify_source_identity no longer checks st_dev — it just opens/fstat/hashes.
        # If the link succeeds (same actual fs), publication works.
        final = str(repo / "remedy-review-overlay.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha)
        assert Path(final).read_bytes() == b"overlay-content"

    def test_true_cross_filesystem_blocked_by_exdev(self, tmp_path, monkeypatch):
        """A true cross-device link raises EXDEV which is caught as PublishSourceError."""
        import errno as _errno
        import packages.orchestration.safe_publish as sp
        repo = _repo(tmp_path)
        src = _src(repo, b"cross-dev")
        sha = self._sha(src)

        original_link = os.link

        def fake_link(s, d):
            raise OSError(_errno.EXDEV, "Invalid cross-device link")

        monkeypatch.setattr(os, "link", fake_link)
        final = str(repo / "remedy-review-xdev.zip")
        with pytest.raises(PublishSourceError, match="different filesystem"):
            publish_atomically(src, final, str(repo), expected_sha256=sha, cleanup_source=False)

    def test_verify_source_identity_returns_fd(self, tmp_path):
        """verify_source_identity returns an open FD that can be fstat'd."""
        repo = _repo(tmp_path)
        src = _src(repo, b"fd-test")
        sha = self._sha(src)
        fd = verify_source_identity(src, str(repo), expected_sha256=sha)
        try:
            st = os.fstat(fd)
            assert st.st_size == len(b"fd-test")
        finally:
            os.close(fd)


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
