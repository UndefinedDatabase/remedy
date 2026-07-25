"""F5 (round 19) — a regular member is a STABLE same-inode read; a torn read is discarded.

A file modified in place during a multi-chunk read returned mixed old/new bytes with no error. The
anchored reader re-fstats the OPEN descriptor after the read and refuses the bytes if identity,
type, mode, size or mtime/ctime drifted.
"""
from __future__ import annotations

import os

import pytest

from packages.common import secure_fs


class _Err(RuntimeError):
    pass


def _read(root, rel):
    return secure_fs.read_verified_relative(root, rel, expected_kind="regular",
                                            error_cls=_Err, noun="file")


def test_a_stable_file_reads_its_own_bytes(tmp_path):
    (tmp_path / "a.txt").write_text("stable content\n")
    vf = _read(str(tmp_path), "a.txt")
    assert vf.data == b"stable content\n"


def test_a_file_rewritten_between_stat_and_read_is_refused(tmp_path, monkeypatch):
    """Force a modification to land after the pre-open stat by hooking os.read once."""
    p = tmp_path / "big.txt"
    p.write_text("A" * 4096)

    real_read = os.read
    tripped = {"done": False}

    def _hooked(fd, n):
        if not tripped["done"]:
            tripped["done"] = True
            # rewrite the file's bytes AND bump its size/mtime while the read is in flight
            with open(p, "wb") as fh:
                fh.write(b"B" * 8192)
        return real_read(fd, n)

    monkeypatch.setattr(os, "read", _hooked)
    with pytest.raises(_Err) as ei:
        _read(str(tmp_path), "big.txt")
    assert "torn read" in str(ei.value) or "changed while it was being read" in str(ei.value)


def test_a_regular_swapped_to_a_symlink_is_refused(tmp_path):
    (tmp_path / "real.txt").write_text("x")
    outside = tmp_path / "OUT"
    outside.write_text("SECRET")
    # A symlink cannot satisfy a regular read.
    (tmp_path / "real.txt").unlink()
    os.symlink(str(outside), str(tmp_path / "real.txt"))
    with pytest.raises(_Err):
        _read(str(tmp_path), "real.txt")
