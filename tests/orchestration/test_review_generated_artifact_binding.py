"""F4/F6 (round 20) — generated artifacts are bound by their in-memory bytes, never reopened.

The plan, expectation and manifest are passed to the builder as immutable bytes; a file forged on
disk with the same name is irrelevant, and the reopen verifier binds each generated member to the
exact bytes written. The manifest is read no-follow, so a symlinked manifest is refused.
"""
from __future__ import annotations

import hashlib
import zipfile

import pytest

from packages.orchestration.archive_plan import (
    ArchiveMemberV1,
    ArchivePlanV1,
    MEMBER_REGULAR,
    MODE_REGULAR,
    SOURCE_REPOSITORY,
)
from packages.orchestration.review_zip import (
    ReviewZipError,
    _read_manifest_no_follow,
    build_review_zip_from_snapshot,
    snapshot_plan_members,
    verify_review_zip,
)


def _plan(root, rel):
    return ArchivePlanV1(repository_members=(
        ArchiveMemberV1(archive_path=rel, kind=MEMBER_REGULAR, mode=MODE_REGULAR,
                        authoritative=False, source_root=str(root), source_rel=rel,
                        source_class=SOURCE_REPOSITORY),))


def test_generated_bytes_are_packaged_verbatim_from_memory(tmp_path):
    root = tmp_path / "r"
    root.mkdir()
    (root / "a.txt").write_text("x")
    snapshot = snapshot_plan_members(_plan(root, "a.txt"))
    plan_bytes = b'{"plan_v": 1}\n'
    gen = {"evidence/current/review_archive_plan.json": (plan_bytes, 0o644)}
    out = tmp_path / "z.zip"
    result = build_review_zip_from_snapshot(out_path=out, snapshot=snapshot, generated_members=gen)
    assert verify_review_zip(out, result) == []
    with zipfile.ZipFile(out) as zf:
        got = zf.read("evidence/current/review_archive_plan.json")
    assert got == plan_bytes
    assert result["model"]["evidence/current/review_archive_plan.json"]["sha256"] == \
        hashlib.sha256(plan_bytes).hexdigest()


def test_a_disk_file_with_the_generated_name_is_never_read(tmp_path):
    root = tmp_path / "r"
    root.mkdir()
    (root / "a.txt").write_text("x")
    # A file on disk at the generated arcname holding a forged secret — must be irrelevant.
    (root / "review_archive_plan.json").write_text('{"SECRET": "/home/alice/leak"}')
    snapshot = snapshot_plan_members(_plan(root, "a.txt"))
    good_bytes = b'{"plan_v": 1}\n'
    out = tmp_path / "z.zip"
    result = build_review_zip_from_snapshot(
        out_path=out, snapshot=snapshot,
        generated_members={"review_archive_plan.json": (good_bytes, 0o644)})
    with zipfile.ZipFile(out) as zf:
        assert zf.read("review_archive_plan.json") == good_bytes
        assert b"SECRET" not in zf.read("review_archive_plan.json")


def test_a_generated_member_over_the_cap_blocks(tmp_path, monkeypatch):
    from packages.orchestration import archive_plan
    root = tmp_path / "r"
    root.mkdir()
    (root / "a.txt").write_text("x")
    snapshot = snapshot_plan_members(_plan(root, "a.txt"))
    monkeypatch.setattr(archive_plan, "MAX_GENERATED_MEMBER_BYTES", 4)
    with pytest.raises(ReviewZipError):
        build_review_zip_from_snapshot(out_path=tmp_path / "z.zip", snapshot=snapshot,
                                       generated_members={"big.json": (b"x" * 100, 0o644)})


class TestManifestNoFollow:
    def test_a_symlinked_manifest_is_refused(self, tmp_path):
        import os
        outside = tmp_path / "SECRET"
        outside.write_text("SUPERSECRET")
        manifest = tmp_path / ".review_zip_manifest.json"
        os.symlink(str(outside), str(manifest))
        with pytest.raises(ReviewZipError):
            _read_manifest_no_follow(str(manifest))

    def test_a_regular_manifest_reads(self, tmp_path):
        manifest = tmp_path / ".review_zip_manifest.json"
        manifest.write_text('{"ok": true}')
        assert _read_manifest_no_follow(str(manifest)) == b'{"ok": true}'
