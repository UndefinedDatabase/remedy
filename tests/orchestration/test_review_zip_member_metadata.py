"""F2/F6 (round 18) — ZIP member TYPE and MODE are preserved and verified.

The builder hardcoded every regular member to 0o644, losing executable and mode-only changes;
post-build verification checked bodies but never the member type or mode, so a regular entry
containing the correct link text passed as a symlink. The builder now writes each member's real
unix type and permission bits, and the verifier holds the reopened archive to them.
"""
from __future__ import annotations

import os
import zipfile

from packages.orchestration.archive_plan import (
    MODE_EXECUTABLE,
    MODE_REGULAR,
    ArchiveMemberV1,
    ArchivePlanV1,
)
from packages.orchestration.review_zip import (
    build_review_zip_from_plan,
    verify_review_zip,
)

_S_IFREG = 0o100000
_S_IFLNK = 0o120000


def _build(tmp_path, files, symlinks=None):
    """files: {rel: (bytes, mode)}, symlinks: {rel: target}."""
    root = tmp_path / "root"
    root.mkdir()
    members = []
    for rel, (data, mode) in files.items():
        p = root / rel
        p.write_bytes(data)
        os.chmod(p, mode)
        members.append(ArchiveMemberV1(archive_path=rel, kind="regular", mode=mode,
                                       authoritative=False, source_root=str(root),
                                       source_rel=rel))
    for rel, target in (symlinks or {}).items():
        os.symlink(target, str(root / rel))
        members.append(ArchiveMemberV1(archive_path=rel, kind="symlink", mode=0o777,
                                       authoritative=False, source_root=str(root),
                                       source_rel=rel))
    manifest = tmp_path / ".review_zip_manifest.json"
    manifest.write_text("{}")
    out = tmp_path / "o.zip"
    plan = ArchivePlanV1(repository_members=tuple(members))
    result = build_review_zip_from_plan(out_path=out, plan=plan,
                                        manifest_rel=".review_zip_manifest.json",
                                        manifest_disk=manifest)
    return out, result


def _perm(info):
    return (info.external_attr >> 16) & 0o7777


def _ftype(info):
    return (info.external_attr >> 16) & 0o170000


# --------------------------------------------------------------------------- modes


class TestModePreservation:
    def test_an_executable_stays_0755(self, tmp_path):
        out, _ = _build(tmp_path, {"tool.sh": (b"#!/bin/sh\n", 0o755)})
        with zipfile.ZipFile(out) as zf:
            info = zf.getinfo("tool.sh")
            assert _perm(info) == MODE_EXECUTABLE
            assert _ftype(info) == _S_IFREG

    def test_a_plain_file_stays_0644(self, tmp_path):
        out, _ = _build(tmp_path, {"f.txt": (b"x", 0o644)})
        with zipfile.ZipFile(out) as zf:
            assert _perm(zf.getinfo("f.txt")) == MODE_REGULAR

    def test_a_symlink_carries_the_symlink_file_type(self, tmp_path):
        out, _ = _build(tmp_path, {"real.txt": (b"r", 0o644)}, {"l.txt": "real.txt"})
        with zipfile.ZipFile(out) as zf:
            assert _ftype(zf.getinfo("l.txt")) == _S_IFLNK

    def test_the_timestamp_is_deterministic(self, tmp_path):
        out, _ = _build(tmp_path, {"f.txt": (b"x", 0o644)})
        with zipfile.ZipFile(out) as zf:
            assert zf.getinfo("f.txt").date_time == (1980, 1, 1, 0, 0, 0)


# --------------------------------------------------------------------------- verification


class TestPostBuildTypeAndModeVerification:
    def test_a_faithful_archive_verifies(self, tmp_path):
        out, result = _build(tmp_path, {"a.sh": (b"x", 0o755), "b.txt": (b"y", 0o644)},
                             {"l": "b.txt"})
        assert verify_review_zip(out, result) == []

    def test_a_regular_member_cannot_satisfy_a_symlink_record(self, tmp_path):
        out, result = _build(tmp_path, {"real.txt": (b"r", 0o644)}, {"l": "real.txt"})
        # rebuild with l as a REGULAR member whose body is the target text
        buf = {}
        with zipfile.ZipFile(out) as zf:
            for n in zf.namelist():
                buf[n] = zf.read(n)
        with zipfile.ZipFile(out, "w") as zf:
            for n, data in buf.items():
                info = zipfile.ZipInfo(n, (1980, 1, 1, 0, 0, 0))
                info.external_attr = (_S_IFREG | 0o644) << 16
                zf.writestr(info, data)
        probs = verify_review_zip(out, result)
        assert any("not a symlink type" in p for p in probs), probs

    def test_a_symlink_member_cannot_satisfy_a_regular_record(self, tmp_path):
        out, result = _build(tmp_path, {"f.txt": (b"content", 0o644)})
        buf = {}
        with zipfile.ZipFile(out) as zf:
            for n in zf.namelist():
                buf[n] = zf.read(n)
        with zipfile.ZipFile(out, "w") as zf:
            for n, data in buf.items():
                info = zipfile.ZipInfo(n, (1980, 1, 1, 0, 0, 0))
                ftype = _S_IFLNK if n == "f.txt" else _S_IFREG
                info.external_attr = (ftype | 0o777) << 16
                zf.writestr(info, data)
        probs = verify_review_zip(out, result)
        assert any("not a regular-file type" in p for p in probs), probs

    def test_a_forged_mode_blocks(self, tmp_path):
        out, result = _build(tmp_path, {"tool.sh": (b"x", 0o755)})
        buf = {}
        with zipfile.ZipFile(out) as zf:
            for n in zf.namelist():
                buf[n] = zf.read(n)
        with zipfile.ZipFile(out, "w") as zf:
            for n, data in buf.items():
                info = zipfile.ZipInfo(n, (1980, 1, 1, 0, 0, 0))
                perm = 0o644 if n == "tool.sh" else 0o644     # 0755 forged down to 0644
                info.external_attr = (_S_IFREG | perm) << 16
                zf.writestr(info, data)
        probs = verify_review_zip(out, result)
        assert any("mode" in p for p in probs), probs

    def test_a_non_deterministic_timestamp_blocks(self, tmp_path):
        out, result = _build(tmp_path, {"f.txt": (b"x", 0o644)})
        buf = {}
        with zipfile.ZipFile(out) as zf:
            for n in zf.namelist():
                buf[n] = zf.read(n)
        with zipfile.ZipFile(out, "w") as zf:
            for n, data in buf.items():
                info = zipfile.ZipInfo(n, (2020, 6, 6, 6, 6, 6))
                info.external_attr = (_S_IFREG | 0o644) << 16
                zf.writestr(info, data)
        probs = verify_review_zip(out, result)
        assert any("non-deterministic timestamp" in p for p in probs), probs

    def test_a_directory_entry_blocks(self, tmp_path):
        out, result = _build(tmp_path, {"f.txt": (b"x", 0o644)})
        with zipfile.ZipFile(out, "a") as zf:
            info = zipfile.ZipInfo("adir/", (1980, 1, 1, 0, 0, 0))
            info.external_attr = (0o040000 | 0o755) << 16
            zf.writestr(info, b"")
        probs = verify_review_zip(out, result)
        assert any("directory" in p or "unexpected member" in p for p in probs), probs
