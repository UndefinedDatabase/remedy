"""F3/F5 (round 20) — every Evidence (and repository) ArchiveMember carries an expected sha in the
finalized CoreArchivePlan, so a ZIP-only reviewer can recompute every member's identity.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

from packages.orchestration.archive_plan import (
    MEMBER_REGULAR,
    MODE_REGULAR,
    SOURCE_EVIDENCE,
    SOURCE_REPOSITORY,
    ArchiveMemberV1,
    ArchivePlanV1,
)
from packages.orchestration.review_zip import snapshot_plan_members

REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location("_bz_h", REPO_ROOT / "scripts" / "build_review_zip.py")
_bz = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_bz)


def test_finalized_plan_binds_every_member_hash(tmp_path):
    repo = tmp_path / "repo"
    ev = tmp_path / "ev"
    repo.mkdir()
    ev.mkdir()
    (repo / "src.py").write_text("x = 1\n")
    (ev / "final_verifier_report.json").write_text('{"ok": true}')
    plan = ArchivePlanV1(
        repository_members=(ArchiveMemberV1(
            archive_path="src.py", kind=MEMBER_REGULAR, mode=MODE_REGULAR, authoritative=True,
            source_root=str(repo), source_rel="src.py", source_class=SOURCE_REPOSITORY),),
        evidence_members=(ArchiveMemberV1(
            archive_path="evidence/current/final_verifier_report.json", kind=MEMBER_REGULAR,
            mode=MODE_REGULAR, authoritative=False, source_root=str(ev),
            source_rel="final_verifier_report.json", source_class=SOURCE_EVIDENCE),))

    snapshot = snapshot_plan_members(plan)
    finalized = _bz._finalize_plan(plan, snapshot)
    for m in finalized.repository_members + finalized.evidence_members:
        assert m.expected_sha256 == snapshot[m.archive_path].sha256
    # and the serialized plan carries the content hash for every regular member
    j = finalized.to_json()
    for m in j["repository_members"] + j["evidence_members"]:
        assert m["content_sha256"], m["archive_path"]
