"""F4 (round 32) — the shared no-clobber publication boundary. A packaging output may be written only
to a safe, non-colliding path; a tracked / symlink / directory / FIFO / device / foreign pre-existing
file is refused and every pre-existing byte is preserved. Direct Python and the shell share this check.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.safe_publish import (
    PublishCollisionError, assert_publishable, atomic_reserve,
)

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git required")


def _repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True, capture_output=True)
    return repo


class TestAssertPublishable:
    def test_nonexistent_path_is_ok(self, tmp_path):
        repo = _repo(tmp_path)
        assert_publishable(str(repo / "remedy-review-x.zip"), str(repo))   # no raise

    def test_tracked_file_refused_and_preserved(self, tmp_path):
        repo = _repo(tmp_path)
        p = repo / "out.zip"
        p.write_bytes(b"tracked bytes")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "c"], cwd=repo, check=True, capture_output=True)
        with pytest.raises(PublishCollisionError):
            assert_publishable(str(p), str(repo))
        assert p.read_bytes() == b"tracked bytes"

    def test_foreign_existing_file_refused_and_preserved(self, tmp_path):
        repo = _repo(tmp_path)
        p = repo / "remedy-review-old.zip"
        p.write_bytes(b"foreign")
        with pytest.raises(PublishCollisionError):
            assert_publishable(str(p), str(repo))
        assert p.read_bytes() == b"foreign"

    def test_owned_existing_path_allowed(self, tmp_path):
        repo = _repo(tmp_path)
        p = repo / "remedy-review-mine.zip"
        p.write_bytes(b"mine")
        assert_publishable(str(p), str(repo), owned_paths=frozenset({"remedy-review-mine.zip"}))

    def test_symlink_refused(self, tmp_path):
        repo = _repo(tmp_path)
        target = repo / "t"; target.write_bytes(b"x")
        link = repo / "remedy-review-link.zip"
        os.symlink(target, link)
        with pytest.raises(PublishCollisionError):
            assert_publishable(str(link), str(repo))

    def test_directory_refused(self, tmp_path):
        repo = _repo(tmp_path)
        d = repo / "remedy-review-dir.zip"; d.mkdir()
        with pytest.raises(PublishCollisionError):
            assert_publishable(str(d), str(repo))

    def test_fifo_refused(self, tmp_path):
        repo = _repo(tmp_path)
        fifo = repo / "remedy-review-fifo.zip"
        os.mkfifo(fifo)
        with pytest.raises(PublishCollisionError):
            assert_publishable(str(fifo), str(repo))

    def test_atomic_reserve_no_double_win(self, tmp_path):
        repo = _repo(tmp_path)
        p = str(repo / "remedy-review-reserve.zip")
        fd = atomic_reserve(p)
        os.close(fd)
        with pytest.raises(PublishCollisionError):
            atomic_reserve(p)   # second concurrent reservation cannot win


class TestShellFinalPathNoClobber:
    def test_shell_refuses_tracked_final_path(self, tmp_path):
        # A tracked file at the final status-bearing name must be refused by the shell before mv.
        from packages.orchestration.safe_publish import assert_publishable as ap
        repo = _repo(tmp_path)
        final = repo / "remedy-review-20260101-000000-READY_FOR_REVIEW.zip"
        final.write_bytes(b"tracked final")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "c"], cwd=repo, check=True, capture_output=True)
        with pytest.raises(PublishCollisionError):
            ap(str(final), str(repo), owned_paths=frozenset({str(final)}))
        assert final.read_bytes() == b"tracked final"
