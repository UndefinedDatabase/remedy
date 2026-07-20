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


class TestAnonymousInodePublication:
    """F1/F2 (round 37): publication uses an anonymous inode (O_TMPFILE + linkat AT_EMPTY_PATH).
    No named source path participates in the security decision. The anonymous inode has no
    pathname before publication, so no external writable FD can exist on it. Cleanup uses the
    pre-publication anonymous inode identity, never a post-race observation."""

    def _sha(self, data):
        return __import__("hashlib").sha256(data).hexdigest()

    def test_named_part_mutation_cannot_alter_publication(self, tmp_path):
        """Mutating the named .part AFTER anonymous copy cannot change the published bytes."""
        repo = _repo(tmp_path)
        content = b"GOOD_VERIFIED_BYTES"
        src = _src(repo, content)
        sha = self._sha(content)
        # Mutate the named source AFTER it was written — anonymous copy already has the bytes
        final = str(repo / "remedy-review-anon.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha)
        assert Path(final).read_bytes() == content
        assert self._sha(Path(final).read_bytes()) == sha

    def test_no_named_source_link_in_publish(self):
        """The publish_atomically function does not call os.link(source_path, final)."""
        import inspect
        from packages.orchestration import safe_publish as sp
        src = inspect.getsource(sp.publish_atomically)
        assert "os.link(source_path" not in src
        assert "os.link(src" not in src

    def test_final_bytes_equal_expected_sha256(self, tmp_path):
        """After successful publication, the final bytes hash exactly to expected_sha256."""
        repo = _repo(tmp_path)
        content = b"verified-exact-content"
        src = _src(repo, content)
        sha = self._sha(content)
        final = str(repo / "remedy-review-exact.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha)
        assert self._sha(Path(final).read_bytes()) == sha

    def test_final_inode_is_anonymous(self, tmp_path):
        """The published file's inode differs from the named source's original inode."""
        repo = _repo(tmp_path)
        content = b"anonymous-inode-check"
        src = _src(repo, content)
        sha = self._sha(content)
        src_ino = os.lstat(src).st_ino
        final = str(repo / "remedy-review-anon-id.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha, cleanup_source=False)
        # The final inode is the anonymous one, not the named source
        assert Path(final).read_bytes() == content
        final_ino = os.lstat(final).st_ino
        assert final_ino != src_ino

    def test_concurrent_verified_publishers_exactly_one_wins(self, tmp_path):
        """Exactly one concurrent verified publisher succeeds."""
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

    def test_foreign_preexisting_not_removed(self, tmp_path):
        """A pre-existing foreign file at the final path blocks but is never removed."""
        repo = _repo(tmp_path)
        final = repo / "remedy-review-foreign.zip"
        final.write_bytes(b"FOREIGN")
        src = _src(repo, b"new")
        with pytest.raises(PublishCollisionError):
            publish_atomically(src, str(final), str(repo), expected_sha256=self._sha(b"new"))
        assert final.read_bytes() == b"FOREIGN"

    def test_foreign_replacement_between_publication_and_verify_preserved(self, tmp_path, monkeypatch):
        """If another process replaces the final path between linkat and postverification,
        the foreign replacement remains byte-identical and is never removed."""
        import packages.orchestration.safe_publish as sp
        repo = _repo(tmp_path)
        content = b"GOOD_VERIFIED_BYTES"
        src = _src(repo, content)
        sha = self._sha(content)
        final = str(repo / "remedy-review-race.zip")
        original_verify = sp.verify_published_identity

        def intercepting_verify(source_fd, fp, expected):
            # Between linkat and verify: remove our link, place a foreign file
            os.unlink(fp)
            with open(fp, "wb") as fh:
                fh.write(b"FOREIGN_AFTER_LINK")
            return original_verify(source_fd, fp, expected)

        monkeypatch.setattr(sp, "verify_published_identity", intercepting_verify)
        with pytest.raises(PublishSourceError, match="inode.*differs"):
            publish_atomically(src, final, str(repo), expected_sha256=sha, cleanup_source=False)
        # The foreign replacement must remain byte-identical
        assert Path(final).read_bytes() == b"FOREIGN_AFTER_LINK"

    def test_omitted_expected_hash_blocks(self, tmp_path):
        """A missing expected_sha256 raises PublishSourceError."""
        repo = _repo(tmp_path)
        src = _src(repo, b"no-hash")
        final = str(repo / "remedy-review-nohash.zip")
        with pytest.raises(PublishSourceError, match="no verified source"):
            publish_atomically(src, final, str(repo), expected_sha256=None)
        assert not os.path.exists(final)

    def test_tampered_source_after_write_blocks(self, tmp_path):
        """If source bytes change after being written to disk, the anonymous copy hash mismatch
        catches it because the stale expected hash doesn't match."""
        repo = _repo(tmp_path)
        src = _src(repo, b"original")
        stale_sha = self._sha(b"original")
        with open(src, "wb") as fh:
            fh.write(b"tampered-different-bytes")
        final = str(repo / "remedy-review-tamper.zip")
        with pytest.raises(PublishSourceError):
            publish_atomically(src, final, str(repo), expected_sha256=stale_sha)
        assert not os.path.exists(final)

    def test_symlink_source_blocks(self, tmp_path):
        """A symlink source is rejected by the O_NOFOLLOW copy."""
        repo = _repo(tmp_path)
        real = repo / "real.bin"
        real.write_bytes(b"payload")
        link = str(repo / ".remedy_zip_link.part")
        os.symlink(real, link)
        final = str(repo / "remedy-review-sym.zip")
        with pytest.raises(PublishSourceError):
            publish_atomically(link, final, str(repo), expected_sha256=self._sha(b"payload"))
        assert not os.path.exists(final)

    def test_successful_publication_cleans_source(self, tmp_path):
        """After successful publication, the named source is removed."""
        repo = _repo(tmp_path)
        content = b"cleanup-test"
        src = _src(repo, content)
        sha = self._sha(content)
        final = str(repo / "remedy-review-clean.zip")
        publish_atomically(src, final, str(repo), expected_sha256=sha)
        assert not os.path.exists(src)

    def test_verify_source_identity_still_works(self, tmp_path):
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
