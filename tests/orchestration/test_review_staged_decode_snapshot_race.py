"""F5 (round 21) — decode-bytes and package-bytes are provably identical.

A staged artifact changed between the decode read and the snapshot read is refused: the plan carries
the decode-time sha, and snapshot_plan_members must reproduce those exact bytes to package them.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location("_bz_race", REPO_ROOT / "scripts" / "build_review_zip.py")
_bz = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_bz)

from packages.orchestration.archive_plan import (  # noqa: E402
    ArchiveMemberV1,
    ArchivePlanV1,
    MEMBER_REGULAR,
    MODE_REGULAR,
    SOURCE_EVIDENCE,
)
from packages.orchestration.review_zip import ReviewZipError, snapshot_plan_members  # noqa: E402


def _staged(tmp_path, name, body):
    cur = tmp_path / "staging" / "evidence" / "current"
    cur.mkdir(parents=True, exist_ok=True)
    (cur / name).write_bytes(body)
    return tmp_path / "staging"


@pytest.mark.parametrize("name", ["review_subject.json", "current_change_content_proof.json",
                                  "final_verifier_report.json", "review_commit_chain.json"])
def test_a_staged_artifact_mutated_between_decode_and_snapshot_blocks(tmp_path, name):
    root = _staged(tmp_path, name, b'{"original": true}\n')
    staged = _bz._StagedArtifacts(str(root), "evidence/current")
    # decode-time read records the sha of the ORIGINAL bytes
    raw, sha = staged.load(name)
    assert raw is not None

    arc = f"evidence/current/{name}"
    plan = ArchivePlanV1(evidence_members=(ArchiveMemberV1(
        archive_path=arc, kind=MEMBER_REGULAR, mode=MODE_REGULAR, authoritative=False,
        source_root=str(root), source_rel=arc, source_class=SOURCE_EVIDENCE),))
    plan = _bz._bind_staged_expected_hashes(plan, staged.by_arcname)
    assert plan.evidence_members[0].expected_sha256 == sha

    # MUTATE the staged file after decode
    (root / arc).write_bytes(b'{"tampered": true, "extra": "bytes"}\n')
    with pytest.raises(ReviewZipError):
        snapshot_plan_members(plan)


def test_an_unchanged_staged_artifact_snapshots_cleanly(tmp_path):
    root = _staged(tmp_path, "review_subject.json", b'{"x": 1}\n')
    staged = _bz._StagedArtifacts(str(root), "evidence/current")
    staged.load("review_subject.json")
    arc = "evidence/current/review_subject.json"
    plan = ArchivePlanV1(evidence_members=(ArchiveMemberV1(
        archive_path=arc, kind=MEMBER_REGULAR, mode=MODE_REGULAR, authoritative=False,
        source_root=str(root), source_rel=arc, source_class=SOURCE_EVIDENCE),))
    plan = _bz._bind_staged_expected_hashes(plan, staged.by_arcname)
    snap = snapshot_plan_members(plan)
    assert snap[arc].sha256 == staged.by_arcname[arc][1]
