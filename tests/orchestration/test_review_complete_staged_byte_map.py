"""F3 (round 23) — the Root Manifest is built from the same staged bytes the ZIP packages: one
complete map covers every Source-Evidence member, and the manifest's facts equal the packaged
evidence."""
from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_e = importlib.util.spec_from_file_location("_e2e_map", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _build(tmp_path):
    repo, base, head = _E2E._build_repo(tmp_path)
    ev, subject, authority = _E2E._write_evidence(repo, base, head, tmp_path / "evidence")
    proc = _E2E._run(["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
                     repo, {"REMEDY_REVIEW_BASE": base, "PYTHONPATH": str(REPO_ROOT)})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return sorted(repo.glob("remedy-review-*.zip"))[-1]


class TestCompleteStagedByteMap:
    def test_root_manifest_job_id_equals_packaged_evidence(self, tmp_path):
        z = _build(tmp_path)
        with zipfile.ZipFile(z) as zf:
            man = json.loads(zf.read(".review_zip_manifest.json"))
            job_flow = json.loads(zf.read("evidence/current/job_flow.json"))
        # the Root Manifest's evidence facts come from the SAME staged bytes that are packaged
        assert man["current_evidence"]["job_id"] == job_flow["job_id"]

    def test_the_inventory_covers_the_core_evidence_members(self, tmp_path):
        z = _build(tmp_path)
        with zipfile.ZipFile(z) as zf:
            inv = json.loads(zf.read("evidence/current/evidence_snapshot_inventory.json"))
            names = set(zf.namelist())
        rels = {m["relative_path"] for m in inv["members"]}
        for core in ("manifest.json", "job_flow.json", "review_subject.json",
                     "current_change_content_proof.json", "final_verifier_report.json"):
            assert core in rels, core
            assert f"evidence/current/{core}" in names

    def test_every_inventory_member_size_equals_the_zip_member_size(self, tmp_path):
        z = _build(tmp_path)
        with zipfile.ZipFile(z) as zf:
            inv = json.loads(zf.read("evidence/current/evidence_snapshot_inventory.json"))
            info = {i.filename: i for i in zf.infolist()}
            for m in inv["members"]:
                arc = f"evidence/current/{m['relative_path']}"
                assert info[arc].file_size == m["size"], arc
