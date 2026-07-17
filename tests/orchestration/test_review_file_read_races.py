"""F3 (round 18) — file reads are atomically no-follow.

The vulnerable shape was `lstat(path)` then `open(path)`/`read_bytes(path)` by NAME: an attacker
swaps `path` to an external symlink in the window and the second call follows it, so outside bytes
are hashed or archived. `read_verified_file_at` (and `read_verified_relative`) operate on a name
relative to a HELD anchored parent fd, open the regular case with O_NOFOLLOW, and re-fstat the open
descriptor's (dev, inode) against the pre-open lstat — a swap changes the inode and is refused.

These tests can't win a real kernel race deterministically, so they simulate the swap by making the
path ALREADY be an external symlink at the moment the reader runs with a regular expectation: the
reader must refuse and read no outside bytes. The atomic-window property is proven structurally —
the read never reopens by ordinary path after the check.
"""
from __future__ import annotations

import os

import pytest

from packages.common.secure_fs import (
    SecureFsError,
    read_verified_file_at,
    read_verified_relative,
)


@pytest.fixture
def world(tmp_path):
    repo = tmp_path / "repo"
    (repo / "sub").mkdir(parents=True)
    outside = tmp_path / "outside.txt"
    outside.write_text("OUTSIDE SECRET")
    return repo, outside


def _fds():
    return len(os.listdir("/proc/self/fd"))


class TestRegularExpectationRefusesASymlink:
    def test_a_regular_read_of_an_external_symlink_reads_no_outside_bytes(self, world):
        repo, outside = world
        os.symlink(str(outside), str(repo / "sub" / "f.txt"))
        with pytest.raises(SecureFsError) as exc:
            read_verified_relative(repo, "sub/f.txt", expected_kind="regular")
        assert "OUTSIDE SECRET" not in str(exc.value)

    def test_a_regular_read_of_an_absolute_symlink_is_refused(self, world):
        repo, _o = world
        os.symlink("/etc/passwd", str(repo / "sub" / "f.txt"))
        with pytest.raises(SecureFsError):
            read_verified_relative(repo, "sub/f.txt", expected_kind="regular")

    def test_the_regular_reader_never_returns_the_target_bytes(self, world):
        repo, outside = world
        os.symlink(str(outside), str(repo / "sub" / "f.txt"))
        try:
            vf = read_verified_relative(repo, "sub/f.txt", expected_kind="regular")
            assert vf.data != b"OUTSIDE SECRET"
        except SecureFsError:
            pass


class TestSymlinkExpectationReadsTargetTextOnly:
    def test_a_symlink_read_returns_the_link_text_not_the_target_bytes(self, world):
        repo, outside = world
        os.symlink(str(outside), str(repo / "sub" / "l.txt"))
        vf = read_verified_relative(repo, "sub/l.txt", expected_kind="symlink")
        assert vf.kind == "symlink"
        assert vf.data == str(outside).encode()      # the link TEXT
        assert vf.data != b"OUTSIDE SECRET"           # never the target content

    def test_a_symlink_read_of_a_regular_file_is_refused(self, world):
        repo, _o = world
        (repo / "sub" / "r.txt").write_text("plain")
        with pytest.raises(SecureFsError):
            read_verified_relative(repo, "sub/r.txt", expected_kind="symlink")


class TestNoDescriptorLeak:
    def test_fd_count_is_stable_across_reads_and_refusals(self, world):
        repo, outside = world
        (repo / "sub" / "ok.txt").write_text("fine")
        os.symlink(str(outside), str(repo / "sub" / "bad.txt"))
        before = _fds()
        for _ in range(20):
            read_verified_relative(repo, "sub/ok.txt", expected_kind="regular")
            try:
                read_verified_relative(repo, "sub/bad.txt", expected_kind="regular")
            except SecureFsError:
                pass
            try:
                read_verified_relative(repo, "sub/missing.txt", expected_kind="regular")
            except SecureFsError:
                pass
        assert _fds() == before


class TestTheAtWorksThroughAHeldFd:
    def test_read_verified_file_at_uses_the_parent_fd(self, world):
        repo, _o = world
        (repo / "sub" / "f.txt").write_text("held")
        parent = os.open(str(repo / "sub"), os.O_RDONLY)
        try:
            vf = read_verified_file_at(parent, "f.txt", expected_kind="regular")
            assert vf.data == b"held"
        finally:
            os.close(parent)

    def test_the_at_reader_refuses_a_symlink_component_by_name(self, world):
        """A basename that is itself a symlink to outside is refused, target unread."""
        repo, outside = world
        os.symlink(str(outside), str(repo / "sub" / "link"))
        parent = os.open(str(repo / "sub"), os.O_RDONLY)
        try:
            with pytest.raises(SecureFsError):
                read_verified_file_at(parent, "link", expected_kind="regular")
        finally:
            os.close(parent)
