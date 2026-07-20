"""F8 (round 19) — the typed, no-follow Evidence inventory blocks unsafe members.

`find -type f | cp` skipped symlinks and followed them into outside bytes. The inventory walks the
tree with anchored O_NOFOLLOW reads: a symlink/FIFO anywhere BLOCKS (never skipped, never
followed), and regular members are staged from the exact verified bytes.
"""
from __future__ import annotations

import os

import pytest

from packages.orchestration.evidence_inventory import (
    EvidenceInventoryError,
    list_regular_tree,
    stage_evidence_tree,
)


@pytest.fixture
def evidence(tmp_path):
    src = tmp_path / "ev"
    (src / "task_runs" / "t1").mkdir(parents=True)
    (src / "job_flow.json").write_text('{"job_id":"j"}')
    (src / "task_runs" / "t1" / "review.json").write_text("[]")
    return src


class TestRegularStaging:
    def test_regular_tree_is_staged_from_the_same_bytes(self, evidence, tmp_path):
        dst = tmp_path / "staged"
        staged = stage_evidence_tree(evidence, dst)
        assert staged == ["job_flow.json", "task_runs/t1/review.json"]
        assert (dst / "job_flow.json").read_text() == '{"job_id":"j"}'
        assert (dst / "task_runs" / "t1" / "review.json").read_text() == "[]"

    def test_listing_prefixes_the_tree(self, evidence, tmp_path):
        dst = tmp_path / "staged"
        stage_evidence_tree(evidence, dst)
        rels = list_regular_tree(dst, prefix="evidence/current")
        assert rels == ["evidence/current/job_flow.json",
                        "evidence/current/task_runs/t1/review.json"]

    def test_pyc_is_skipped(self, evidence, tmp_path):
        (evidence / "junk.pyc").write_bytes(b"\x00")
        dst = tmp_path / "staged"
        staged = stage_evidence_tree(evidence, dst)
        assert "junk.pyc" not in staged


class TestUnsafeMembersBlock:
    def test_a_symlink_member_blocks(self, evidence, tmp_path):
        os.symlink("/etc/passwd", str(evidence / "token.json"))
        with pytest.raises(EvidenceInventoryError) as ei:
            stage_evidence_tree(evidence, tmp_path / "staged")
        assert "not a regular file or directory" in str(ei.value)

    def test_a_symlink_is_not_silently_followed_into_outside_bytes(self, evidence, tmp_path):
        secret = tmp_path / "SECRET"
        secret.write_text("SUPERSECRET")
        os.symlink(str(secret), str(evidence / "leak.json"))
        dst = tmp_path / "staged"
        with pytest.raises(EvidenceInventoryError):
            stage_evidence_tree(evidence, dst)
        # nothing containing the secret was written
        assert not (dst / "leak.json").exists()

    def test_a_fifo_member_blocks(self, evidence, tmp_path):
        os.mkfifo(str(evidence / "pipe"))
        with pytest.raises(EvidenceInventoryError):
            stage_evidence_tree(evidence, tmp_path / "staged")

    def test_a_symlinked_directory_component_blocks(self, evidence, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        (outside / "x.json").write_text("{}")
        os.symlink(str(outside), str(evidence / "linkdir"))
        with pytest.raises(EvidenceInventoryError):
            stage_evidence_tree(evidence, tmp_path / "staged")

    def test_listing_a_tree_with_a_symlink_blocks(self, evidence):
        os.symlink("job_flow.json", str(evidence / "alias.json"))
        with pytest.raises(EvidenceInventoryError):
            list_regular_tree(evidence)
