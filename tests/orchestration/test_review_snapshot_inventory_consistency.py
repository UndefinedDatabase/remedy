"""F10 (round 21) — every snapshot-inventory entry matches its Plan Evidence member's hash and
mode; generated members are outside the inventory boundary."""
from __future__ import annotations

import hashlib

from packages.orchestration.archive_plan import (
    ArchiveMemberV1,
    ArchivePlanV1,
    MEMBER_REGULAR,
    MODE_REGULAR,
    SOURCE_EVIDENCE,
)
from packages.orchestration.evidence_inventory import (
    INVENTORY_VERSION,
    validate_snapshot_inventory,
)


def _plan_with_evidence(sha):
    return ArchivePlanV1(evidence_members=(ArchiveMemberV1(
        archive_path="evidence/current/job_flow.json", kind=MEMBER_REGULAR, mode=MODE_REGULAR,
        authoritative=False, source_root="/x", source_rel="job_flow.json",
        source_class=SOURCE_EVIDENCE, expected_sha256=sha),))


def _inventory(sha, mode=0o644):
    return {"inventory_v": INVENTORY_VERSION, "boundary": "source-evidence-at-snapshot",
            "member_count": 1,
            "members": [{"relative_path": "job_flow.json", "kind": "regular", "mode": mode,
                         "size": 3, "sha256": sha, "source_class": SOURCE_EVIDENCE}]}


def test_a_consistent_inventory_passes():
    sha = hashlib.sha256(b"{}\n").hexdigest()
    assert validate_snapshot_inventory(_inventory(sha), _plan_with_evidence(sha),
                                       prefix="evidence/current") == []


def test_a_hash_mismatch_is_reported():
    good = hashlib.sha256(b"a").hexdigest()
    bad = hashlib.sha256(b"b").hexdigest()
    probs = validate_snapshot_inventory(_inventory(bad), _plan_with_evidence(good),
                                        prefix="evidence/current")
    assert any("sha256 disagrees" in p for p in probs)


def test_a_mode_mismatch_is_reported():
    sha = hashlib.sha256(b"x").hexdigest()
    probs = validate_snapshot_inventory(_inventory(sha, mode=0o755), _plan_with_evidence(sha),
                                        prefix="evidence/current")
    assert any("mode disagrees" in p for p in probs)


def test_an_entry_with_no_plan_member_is_reported():
    sha = hashlib.sha256(b"x").hexdigest()
    probs = validate_snapshot_inventory(_inventory(sha), ArchivePlanV1(),
                                        prefix="evidence/current")
    assert any("not a Plan evidence member" in p for p in probs)


def test_a_bad_version_is_reported():
    sha = hashlib.sha256(b"x").hexdigest()
    inv = _inventory(sha)
    inv["inventory_v"] = 99
    probs = validate_snapshot_inventory(inv, _plan_with_evidence(sha), prefix="evidence/current")
    assert any("version" in p for p in probs)
