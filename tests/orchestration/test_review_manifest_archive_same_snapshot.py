"""F2 (round 22) — the manifest and the archive consume ONE immutable staged byte map; the final
status is decided from exactly the packaged gate bytes, and a gate mutation blocks."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_e2e = importlib.util.spec_from_file_location(
    "_e2e_h", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e2e)
_e2e.loader.exec_module(_E2E)

_bzs = importlib.util.spec_from_file_location("_bz_snap", REPO_ROOT / "scripts" / "build_review_zip.py")
_bz = importlib.util.module_from_spec(_bzs)
_bzs.loader.exec_module(_bz)

from packages.orchestration.archive_plan import (  # noqa: E402
    ArchiveMemberV1, ArchivePlanV1, MEMBER_REGULAR, MODE_REGULAR, SOURCE_EVIDENCE,
)
from packages.orchestration.review_zip import ReviewZipError, snapshot_plan_members  # noqa: E402


def test_a_blocked_final_verifier_cannot_produce_ready(tmp_path):
    repo, base, head = _E2E._build_repo(tmp_path)
    ev, subject, authority = _E2E._write_evidence(repo, base, head, tmp_path / "evidence")
    # flip the packaged final_verifier to BLOCKED
    fv = json.loads((ev / "final_verifier_report.json").read_text())
    fv["verdict"] = "BLOCKED"
    fv["unresolved_findings"] = ["REAL_BLOCK"]
    (ev / "final_verifier_report.json").write_text(json.dumps(fv, indent=2, sort_keys=True))
    proc = _E2E._run(["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
                     repo, {"REMEDY_REVIEW_BASE": base, "PYTHONPATH": str(REPO_ROOT)})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    z = sorted(repo.glob("remedy-review-*.zip"))[-1]
    assert "BLOCKED_EVIDENCE" in z.name, proc.stdout
    with zipfile.ZipFile(z) as zf:
        man = json.loads(zf.read(".review_zip_manifest.json"))
        packaged_fv = json.loads(zf.read("evidence/current/final_verifier_report.json"))
    # status is BLOCKED and it was decided from EXACTLY the packaged (BLOCKED) gate bytes
    assert man["package_status"] == "BLOCKED_EVIDENCE"
    assert packaged_fv["verdict"] == "BLOCKED"
    assert man["ready_gate_matrix"]["ok"] is False


def test_a_staged_gate_mutation_between_decode_and_snapshot_blocks(tmp_path):
    cur = tmp_path / "staging" / "evidence" / "current"
    cur.mkdir(parents=True)
    (cur / "final_verifier_report.json").write_bytes(b'{"verdict": "PASS_WITH_RISKS"}\n')
    staged = _bz._StagedArtifacts(str(tmp_path / "staging"), "evidence/current")
    staged.load("final_verifier_report.json")
    arc = "evidence/current/final_verifier_report.json"
    plan = ArchivePlanV1(evidence_members=(ArchiveMemberV1(
        archive_path=arc, kind=MEMBER_REGULAR, mode=MODE_REGULAR, authoritative=False,
        source_root=str(tmp_path / "staging"), source_rel=arc, source_class=SOURCE_EVIDENCE),))
    plan = _bz._bind_staged_expected_hashes(plan, staged.by_arcname)
    # mutate after decode
    (tmp_path / "staging" / arc).write_bytes(b'{"verdict": "BLOCKED"}\n')
    with pytest.raises(ReviewZipError):
        snapshot_plan_members(plan)
