"""F3/F5 (round 20) — the immutable snapshot is the single byte source.

Once phase 1 has snapshotted a member's bytes, mutating the source on disk cannot change the
packaged bytes, and a source whose bytes disagree with the plan's expected hash is refused.
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
    SOURCE_EVIDENCE,
    SOURCE_REPOSITORY,
)
from packages.orchestration.review_zip import (
    ReviewZipError,
    build_review_zip_from_snapshot,
    snapshot_plan_members,
    verify_review_zip,
)


def _member(root, rel, *, expected=None, source_class=SOURCE_REPOSITORY, auth=False):
    return ArchiveMemberV1(archive_path=rel, kind=MEMBER_REGULAR, mode=MODE_REGULAR,
                           authoritative=auth, source_root=str(root), source_rel=rel,
                           source_class=source_class, expected_sha256=expected)


def test_source_mutated_after_snapshot_does_not_change_the_package(tmp_path):
    root = tmp_path / "r"
    root.mkdir()
    (root / "a.txt").write_text("ORIGINAL")
    plan = ArchivePlanV1(repository_members=(_member(root, "a.txt"),))
    snapshot = snapshot_plan_members(plan)
    # Mutate the source AFTER the snapshot.
    (root / "a.txt").write_text("TAMPERED-LONGER-BYTES")
    out = tmp_path / "z.zip"
    result = build_review_zip_from_snapshot(out_path=out, snapshot=snapshot, generated_members={})
    assert verify_review_zip(out, result) == []
    with zipfile.ZipFile(out) as zf:
        assert zf.read("a.txt") == b"ORIGINAL"      # the immutable snapshot bytes, not the tamper


def test_a_source_that_disagrees_with_the_expected_hash_is_refused(tmp_path):
    root = tmp_path / "r"
    root.mkdir()
    (root / "a.txt").write_text("real bytes")
    wrong = hashlib.sha256(b"other bytes").hexdigest()
    plan = ArchivePlanV1(repository_members=(_member(root, "a.txt", expected=wrong),))
    with pytest.raises(ReviewZipError) as ei:
        snapshot_plan_members(plan)
    assert "declared" in str(ei.value)


def test_an_evidence_member_expected_hash_is_bound(tmp_path):
    root = tmp_path / "ev"
    root.mkdir()
    (root / "final_verifier_report.json").write_text('{"ok": true}')
    good = hashlib.sha256((root / "final_verifier_report.json").read_bytes()).hexdigest()
    plan = ArchivePlanV1(evidence_members=(
        _member(root, "final_verifier_report.json", expected=good, source_class=SOURCE_EVIDENCE),))
    snapshot = snapshot_plan_members(plan)
    assert snapshot["final_verifier_report.json"].sha256 == good
    # a forged evidence member (expected hash of clean bytes, disk holds forged bytes) is refused
    (root / "final_verifier_report.json").write_text('{"ok": false, "forged": true}')
    plan_forged = ArchivePlanV1(evidence_members=(
        _member(root, "final_verifier_report.json", expected=good, source_class=SOURCE_EVIDENCE),))
    with pytest.raises(ReviewZipError):
        snapshot_plan_members(plan_forged)
