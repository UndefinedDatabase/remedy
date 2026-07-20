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
    verify_published_identity, verify_source_identity,
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
    def _sha(self, data):
        return __import__("hashlib").sha256(data).hexdigest()

    def test_single_publish_moves_and_cleans_source(self, tmp_path):
        repo = _repo(tmp_path)
        content = b"complete-zip"
        src = _src(repo, content)
        final = str(repo / "remedy-review-x.zip")
        publish_atomically(src, final, str(repo), expected_sha256=self._sha(content))
        assert Path(final).read_bytes() == content
        assert not os.path.exists(src)

    def test_concurrent_publishers_exactly_one_wins(self, tmp_path):
        repo = _repo(tmp_path)
        final = str(repo / "remedy-review-race.zip")
        results = {}
        barrier = threading.Barrier(8)

        def worker(i):
            content = f"content-{i}".encode()
            src = _src(repo, content)
            barrier.wait()
            try:
                publish_atomically(src, final, str(repo), expected_sha256=self._sha(content))
                results[i] = "ok"
            except (PublishCollisionError, PublishSourceError):
                results[i] = "collision"
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
        assert Path(final).read_bytes() == f"content-{wins[0]}".encode()

    def test_tracked_final_preserved_and_blocks(self, tmp_path):
        repo = _repo(tmp_path)
        final = repo / "out.zip"
        final.write_bytes(b"tracked")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "c"], cwd=repo, check=True, capture_output=True)
        content = b"new"
        src = _src(repo, content)
        with pytest.raises(PublishCollisionError):
            publish_atomically(src, str(final), str(repo), expected_sha256=self._sha(content))
        assert final.read_bytes() == b"tracked"
        assert not os.path.exists(src)

    def test_foreign_existing_final_preserved_and_blocks(self, tmp_path):
        repo = _repo(tmp_path)
        final = repo / "remedy-review-foreign.zip"
        final.write_bytes(b"foreign")
        content = b"new"
        src = _src(repo, content)
        with pytest.raises(PublishCollisionError):
            publish_atomically(src, str(final), str(repo), expected_sha256=self._sha(content))
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


class TestByteAndInodeBoundPublication:
    """F1/F2 (round 36): the publication protocol verifies BOTH inode identity AND byte integrity.
    A same-inode in-place mutation (through a second writable FD) and a pathname replacement both
    fail AND leave no misleading final ZIP. ``expected_sha256`` is mandatory."""

    def _sha(self, data):
        return __import__("hashlib").sha256(data).hexdigest()

    def _sha_path(self, p):
        return self._sha(Path(p).read_bytes())

    def test_same_inode_inplace_mutation_blocks(self, tmp_path, monkeypatch):
        """After FD hash, a second writable FD mutates the same inode in place. The post-publication
        re-hash catches it. The final path is removed."""
        repo = _repo(tmp_path)
        content = b"GOOD_VERIFIED_BYTES"
        src = _src(repo, content)
        sha = self._sha(content)
        writable_fd = os.open(src, os.O_WRONLY)
        original_link = os.link

        def mutating_link(s, d):
            os.lseek(writable_fd, 0, os.SEEK_SET)
            os.write(writable_fd, b"EVIL_MUTATED_BYTES")
            os.fsync(writable_fd)
            return original_link(s, d)

        monkeypatch.setattr(os, "link", mutating_link)
        final = str(repo / "remedy-review-mut.zip")
        with pytest.raises(PublishSourceError, match="mutation"):
            publish_atomically(src, final, str(repo), expected_sha256=sha, cleanup_source=False)
        os.close(writable_fd)
        assert not os.path.exists(final)

    def test_pathname_replacement_blocks_and_cleans_up(self, tmp_path, monkeypatch):
        """After FD hash, the source pathname is replaced with a different regular file. The inode
        check catches it AND the evil final path is removed."""
        repo = _repo(tmp_path)
        content = b"GOOD_VERIFIED_BYTES"
        src = _src(repo, content)
        sha = self._sha(content)
        original_link = os.link

        def swapping_link(s, d):
            os.unlink(s)
            with open(s, "wb") as fh:
                fh.write(b"EVIL_SWAPPED_BYTES")
            return original_link(s, d)

        monkeypatch.setattr(os, "link", swapping_link)
        final = str(repo / "remedy-review-swap.zip")
        with pytest.raises(PublishSourceError, match="inode.*differs"):
            publish_atomically(src, final, str(repo), expected_sha256=sha, cleanup_source=False)
        assert not os.path.exists(final)

    def test_symlink_replacement_blocks(self, tmp_path, monkeypatch):
        """After FD hash, the source pathname is replaced with a symlink. O_NOFOLLOW on source
        prevents this when verify_source_identity opens, but a link to a symlink target also differs
        in inode."""
        repo = _repo(tmp_path)
        content = b"GOOD_PAYLOAD"
        src = _src(repo, content)
        sha = self._sha(content)
        target = repo / "evil_target.bin"
        target.write_bytes(b"SYMLINK_TARGET")
        original_link = os.link

        def symlink_link(s, d):
            os.unlink(s)
            os.symlink(str(target), s)
            return original_link(str(target), d)

        monkeypatch.setattr(os, "link", symlink_link)
        final = str(repo / "remedy-review-symlink.zip")
        with pytest.raises(PublishSourceError, match="inode.*differs"):
            publish_atomically(src, final, str(repo), expected_sha256=sha, cleanup_source=False)
        assert not os.path.exists(final)

    def test_foreign_preexisting_not_removed(self, tmp_path):
        """A pre-existing foreign file at the final path blocks but is never removed."""
        repo = _repo(tmp_path)
        final = repo / "remedy-review-foreign.zip"
        final.write_bytes(b"FOREIGN")
        src = _src(repo, b"new")
        with pytest.raises(PublishCollisionError):
            publish_atomically(src, str(final), str(repo), expected_sha256=self._sha(b"new"))
        assert final.read_bytes() == b"FOREIGN"

    def test_successful_bytes_hash_exactly(self, tmp_path):
        """After successful publication, the final bytes hash exactly to expected_sha256."""
        repo = _repo(tmp_path)
        content = b"verified-exact-content"
        src = _src(repo, content)
        sha = self._sha(content)
        final = str(repo / "remedy-review-exact.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha)
        assert self._sha(Path(final).read_bytes()) == sha

    def test_final_identity_belongs_to_invocation(self, tmp_path):
        """After successful publication, the final file is a hard link of the verified source."""
        repo = _repo(tmp_path)
        content = b"identity-check-content"
        src = _src(repo, content)
        sha = self._sha(content)
        src_ino = os.lstat(src).st_ino
        final = str(repo / "remedy-review-id.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha)
        assert os.lstat(final).st_ino == src_ino

    def test_concurrent_verified_publishers_exactly_one_wins(self, tmp_path):
        """Exactly one concurrent verified publisher succeeds; every concurrency test passes
        expected_sha256."""
        repo = _repo(tmp_path)
        final = str(repo / "remedy-review-crace.zip")
        content = b"concurrent-content"
        sha = self._sha(content)
        results = {}
        barrier = threading.Barrier(8)

        def worker(i):
            src = _src(repo, content)
            barrier.wait()
            try:
                publish_atomically(src, final, str(repo), expected_sha256=sha)
                results[i] = "ok"
            except PublishCollisionError:
                results[i] = "collision"

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert sum(1 for r in results.values() if r == "ok") == 1
        assert Path(final).read_bytes() == content
        assert self._sha(Path(final).read_bytes()) == sha

    def test_omitted_expected_hash_blocks(self, tmp_path):
        """A missing expected_sha256 raises PublishSourceError."""
        repo = _repo(tmp_path)
        src = _src(repo, b"no-hash")
        final = str(repo / "remedy-review-nohash.zip")
        with pytest.raises(PublishSourceError, match="no verified source"):
            publish_atomically(src, final, str(repo), expected_sha256=None)
        assert not os.path.exists(final)

    def test_overlayfs_valid_publication_succeeds(self, tmp_path):
        """OverlayFS-like mount (different st_dev for file vs parent) still succeeds."""
        repo = _repo(tmp_path)
        content = b"overlay-content"
        src = _src(repo, content)
        sha = self._sha(content)
        final = str(repo / "remedy-review-overlay.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha)
        assert Path(final).read_bytes() == content

    def test_true_cross_filesystem_blocks(self, tmp_path, monkeypatch):
        """A true cross-device link raises EXDEV → PublishSourceError."""
        import errno as _errno
        repo = _repo(tmp_path)
        content = b"cross-dev"
        src = _src(repo, content)
        sha = self._sha(content)
        original_link = os.link

        def fake_link(s, d):
            raise OSError(_errno.EXDEV, "Invalid cross-device link")

        monkeypatch.setattr(os, "link", fake_link)
        final = str(repo / "remedy-review-xdev.zip")
        with pytest.raises(PublishSourceError, match="different filesystem"):
            publish_atomically(src, final, str(repo), expected_sha256=sha, cleanup_source=False)

    def test_symlink_at_source_blocked_by_o_nofollow(self, tmp_path):
        """O_NOFOLLOW on the source path means a symlink raises immediately."""
        repo = _repo(tmp_path)
        real = repo / "real.bin"
        real.write_bytes(b"payload")
        link = str(repo / ".remedy_zip_link.part")
        os.symlink(real, link)
        with pytest.raises(PublishSourceError):
            verify_source_identity(link, str(repo),
                                   expected_sha256=self._sha(real.read_bytes()))

    def test_verify_source_identity_returns_fd(self, tmp_path):
        """verify_source_identity returns an open FD that can be fstat'd."""
        repo = _repo(tmp_path)
        content = b"fd-test"
        src = _src(repo, content)
        sha = self._sha(content)
        fd = verify_source_identity(src, str(repo), expected_sha256=sha)
        try:
            st = os.fstat(fd)
            assert st.st_size == len(content)
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
        content = b"x"
        sha = __import__("hashlib").sha256(content).hexdigest()
        with pytest.raises(PublishCollisionError):
            publish_atomically(_src(tmp_path, content), str(notrepo / "x.zip"), str(notrepo),
                               expected_sha256=sha)

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
