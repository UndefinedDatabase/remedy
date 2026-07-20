"""F4 (round 23) — inventory size is bound EXACTLY to the plan member's snapshot byte length."""
from __future__ import annotations

import hashlib

from packages.orchestration.archive_plan import (
    ArchiveMemberV1, ArchivePlanV1, MEMBER_REGULAR, MODE_REGULAR, SOURCE_EVIDENCE,
)
from packages.orchestration.evidence_inventory import (
    INVENTORY_BOUNDARY, INVENTORY_VERSION, validate_snapshot_inventory,
)

SHA = hashlib.sha256(b"abc").hexdigest()


def _plan(size):
    return ArchivePlanV1(evidence_members=(ArchiveMemberV1(
        archive_path="evidence/current/a.json", kind=MEMBER_REGULAR, mode=MODE_REGULAR,
        authoritative=False, source_root="/x", source_rel="a.json", source_class=SOURCE_EVIDENCE,
        expected_sha256=SHA, expected_size=size),))


def _inv(size):
    return {"inventory_v": INVENTORY_VERSION, "boundary": INVENTORY_BOUNDARY, "member_count": 1,
            "members": [{"relative_path": "a.json", "kind": "regular", "mode": 0o644,
                         "size": size, "sha256": SHA, "source_class": SOURCE_EVIDENCE}]}


def _v(inv, plan):
    return validate_snapshot_inventory(inv, plan, prefix="evidence/current")


def test_matching_size_passes():
    assert _v(_inv(3), _plan(3)) == []


def test_size_mismatch_blocks():
    assert any("size" in p and "disagrees" in p for p in _v(_inv(999999999), _plan(3)))


def test_the_expected_size_is_the_byte_length():
    # ArchiveMemberV1 carries expected_size; the inventory must equal it.
    assert any("size" in p for p in _v(_inv(4), _plan(3)))
