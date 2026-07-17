"""F12 (round 19) — the bounded archive contract: per-member, aggregate, ratio, and count caps.

Round 18 read every member fully into RAM with no per-member, aggregate, member-count or
expansion-ratio limit, so a hostile input could exhaust memory. The build and the reopen now bound
every dangerous allocation.
"""
from __future__ import annotations

from packages.orchestration import archive_plan
from packages.orchestration.archive_plan import (
    ArchiveMemberV1,
    ArchivePlanV1,
    MEMBER_REGULAR,
    MODE_REGULAR,
    SOURCE_REPOSITORY,
    build_archive_plan,
)
from packages.orchestration.review_subject import ReviewSubjectV1
from packages.orchestration.review_zip import build_review_zip_from_plan, verify_review_zip


def _member(root, rel):
    return ArchiveMemberV1(archive_path=rel, kind=MEMBER_REGULAR, mode=MODE_REGULAR,
                           authoritative=False, source_root=str(root), source_rel=rel,
                           source_class=SOURCE_REPOSITORY)


def _plan(root, rels):
    return ArchivePlanV1(repository_members=tuple(_member(root, r) for r in rels))


def _build(tmp_path, root, rels):
    (root / "m.json").write_text("{}")
    out = tmp_path / "a.zip"
    plan = _plan(root, rels)
    result = build_review_zip_from_plan(out_path=out, plan=plan, manifest_rel="m.json",
                                        manifest_disk=str(root / "m.json"))
    return out, result


class TestMemberCountLimit:
    def test_repository_member_count_over_the_cap_blocks(self, tmp_path, monkeypatch):
        root = tmp_path / "r"
        root.mkdir()
        (root / "a.txt").write_text("a")
        (root / "b.txt").write_text("b")
        monkeypatch.setattr(archive_plan, "MAX_REPOSITORY_MEMBERS", 1)
        plan = build_archive_plan(repo_root=root, subject=ReviewSubjectV1(),
                                  repo_context_rel=["a.txt", "b.txt"], evidence_root=None,
                                  evidence_rel=[], authoritative_paths=set())
        assert plan.blocked
        assert any("exceeds" in b.reason for b in plan.blocked_records)


class TestReadCapsOnVerify:
    def test_a_sane_archive_verifies_clean(self, tmp_path):
        root = tmp_path / "r"
        root.mkdir()
        (root / "s.txt").write_text("small\n")
        out, result = _build(tmp_path, root, ["s.txt"])
        assert verify_review_zip(out, result) == []

    def test_a_member_over_the_per_member_cap_blocks(self, tmp_path, monkeypatch):
        root = tmp_path / "r"
        root.mkdir()
        (root / "s.txt").write_text("hello world this is more than five bytes\n")
        out, result = _build(tmp_path, root, ["s.txt"])
        # Shrink the cap AFTER the build so only the reopen enforces it.
        monkeypatch.setattr(archive_plan, "MAX_MEMBER_BYTES", 5)
        assert any("exceeds the per-member cap" in p for p in verify_review_zip(out, result))

    def test_a_decompression_bomb_ratio_blocks(self, tmp_path):
        root = tmp_path / "r"
        root.mkdir()
        # >1 MiB of a single byte deflates ~1000x — above the ratio cap and the 1 MiB floor.
        (root / "bomb.txt").write_text("a" * (1024 * 1024 + 32))
        out, result = _build(tmp_path, root, ["bomb.txt"])
        assert any("decompression" in p for p in verify_review_zip(out, result))

    def test_aggregate_cap_blocks(self, tmp_path, monkeypatch):
        root = tmp_path / "r"
        root.mkdir()
        (root / "a.txt").write_text("aaaa")
        (root / "b.txt").write_text("bbbb")
        out, result = _build(tmp_path, root, ["a.txt", "b.txt"])
        monkeypatch.setattr(archive_plan, "MAX_TOTAL_UNCOMPRESSED_BYTES", 3)
        assert any("aggregate cap" in p for p in verify_review_zip(out, result))
