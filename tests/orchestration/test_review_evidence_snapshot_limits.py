"""F9/F10 (round 20) — the Evidence snapshot is bounded DURING the walk, before the whole tree is
copied, and it records a per-member sha256.
"""
from __future__ import annotations

import os

import pytest

from packages.orchestration.evidence_inventory import (
    EvidenceInventoryError,
    stage_evidence_snapshot,
)


@pytest.fixture
def tree(tmp_path):
    src = tmp_path / "ev"
    (src / "task_runs" / "t1").mkdir(parents=True)
    for i in range(6):
        (src / f"a{i}.json").write_text("x" * 100)
    (src / "task_runs" / "t1" / "review.json").write_text("[]")
    return src


class TestSnapshotHashes:
    def test_every_member_carries_its_staged_sha(self, tree, tmp_path):
        import hashlib
        dst = tmp_path / "st"
        members = stage_evidence_snapshot(tree, dst)
        assert members
        for m in members:
            data = (dst / m.relative_path).read_bytes()
            assert m.sha256 == hashlib.sha256(data).hexdigest()
            assert m.size == len(data)


class TestLimits:
    def test_member_count_limit_blocks_during_walk(self, tree, tmp_path):
        dst = tmp_path / "st"
        with pytest.raises(EvidenceInventoryError) as ei:
            stage_evidence_snapshot(tree, dst, max_members=3)
        assert "member-count limit" in str(ei.value)
        # It stopped early — fewer than the full tree was copied.
        copied = sum(len(f) for _, _, f in os.walk(dst))
        assert copied <= 4

    def test_aggregate_byte_limit_blocks_during_walk(self, tree, tmp_path):
        dst = tmp_path / "st"
        with pytest.raises(EvidenceInventoryError) as ei:
            stage_evidence_snapshot(tree, dst, max_aggregate_bytes=250)
        assert "aggregate-byte limit" in str(ei.value)
