"""F3 (round 22) — strict EvidenceSnapshotInventoryV1 + exact bijection with Source-Evidence Plan
members."""
from __future__ import annotations

import hashlib

from packages.orchestration.archive_plan import (
    MEMBER_REGULAR,
    MODE_REGULAR,
    SOURCE_EVIDENCE,
    SOURCE_GENERATED_MANIFEST,
    ArchiveMemberV1,
    ArchivePlanV1,
)
from packages.orchestration.evidence_inventory import (
    INVENTORY_BOUNDARY,
    INVENTORY_VERSION,
    validate_snapshot_inventory,
)

SHA = hashlib.sha256(b"{}\n").hexdigest()


def _member(rel, sha=SHA, cls=SOURCE_EVIDENCE, mode=MODE_REGULAR):
    return ArchiveMemberV1(archive_path=f"evidence/current/{rel}", kind=MEMBER_REGULAR, mode=mode,
                           authoritative=False, source_root="/x", source_rel=rel,
                           source_class=cls, expected_sha256=sha)


def _plan(*members):
    return ArchivePlanV1(evidence_members=tuple(members))


def _entry(rel, sha=SHA, mode=0o644, size=3, kind="regular", cls=SOURCE_EVIDENCE):
    return {"relative_path": rel, "kind": kind, "mode": mode, "size": size, "sha256": sha,
            "source_class": cls}


def _inv(members):
    return {"inventory_v": INVENTORY_VERSION, "boundary": INVENTORY_BOUNDARY,
            "member_count": len(members), "members": members}


def _v(inv, plan, **kw):
    return validate_snapshot_inventory(inv, plan, prefix="evidence/current", **kw)


def test_a_valid_bijection_passes():
    assert _v(_inv([_entry("a.json")]), _plan(_member("a.json"))) == []


def test_forged_inventory_hash_blocks():
    bad = _entry("a.json", sha="0" * 64)
    assert any("disagrees" in p for p in _v(_inv([bad]), _plan(_member("a.json"))))


def test_missing_plan_member_blocks():
    assert any("missing Source-Evidence" in p
               for p in _v(_inv([]), _plan(_member("a.json"))))


def test_extra_inventory_member_blocks():
    probs = _v(_inv([_entry("a.json"), _entry("b.json")]), _plan(_member("a.json")))
    assert any("not a Plan evidence member" in p for p in probs)


def test_duplicate_inventory_path_blocks():
    assert any("more than once" in p
               for p in _v(_inv([_entry("a.json"), _entry("a.json")]), _plan(_member("a.json"))))


def test_wrong_member_count_blocks():
    inv = _inv([_entry("a.json")])
    inv["member_count"] = 9
    assert any("member_count" in p for p in _v(inv, _plan(_member("a.json"))))


def test_wrong_boundary_blocks():
    inv = _inv([_entry("a.json")])
    inv["boundary"] = "nope"
    assert any("boundary" in p for p in _v(inv, _plan(_member("a.json"))))


def test_wrong_version_blocks():
    inv = _inv([_entry("a.json")])
    inv["inventory_v"] = 99
    assert any("version" in p for p in _v(inv, _plan(_member("a.json"))))


def test_wrong_kind_blocks():
    assert any("kind" in p for p in _v(_inv([_entry("a.json", kind="symlink")]),
                                       _plan(_member("a.json"))))


def test_wrong_mode_blocks():
    assert any("mode" in p for p in _v(_inv([_entry("a.json", mode=0o600)]),
                                       _plan(_member("a.json"))))


def test_wrong_size_blocks():
    assert any("size" in p for p in _v(_inv([_entry("a.json", size=-1)]),
                                       _plan(_member("a.json"))))


def test_wrong_source_class_blocks():
    assert any("source_class" in p for p in _v(_inv([_entry("a.json", cls="repository")]),
                                               _plan(_member("a.json"))))


def test_unknown_field_blocks():
    e = _entry("a.json")
    e["EVIL"] = 1
    assert any("wrong field set" in p for p in _v(_inv([e]), _plan(_member("a.json"))))


def test_generated_members_are_outside_the_boundary():
    # a generated_manifest member is never expected in the inventory
    plan = _plan(_member("a.json"),
                 _member("review_archive_plan.json", cls=SOURCE_GENERATED_MANIFEST))
    assert _v(_inv([_entry("a.json")]), plan) == []


def test_obs_index_and_inventory_are_outside_boundary():
    plan = _plan(_member("a.json"), _member("self_run_observability_index.json"),
                 _member("evidence_snapshot_inventory.json"))
    outside = {"evidence/current/self_run_observability_index.json",
               "evidence/current/evidence_snapshot_inventory.json"}
    assert _v(_inv([_entry("a.json")]), plan, generated_outside_boundary=outside) == []
