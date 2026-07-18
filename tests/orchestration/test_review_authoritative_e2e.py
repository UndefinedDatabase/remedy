"""F9 (round 21) — ONE real authoritative end-to-end package test.

committed Subject → strict ContentProof → Final-Verifier/Change-Provenance authority → Evidence
staging → build_review_manifest → ArchivePlan → Expectation → Root Manifest → real
make_review_zip.sh → READY_FOR_REVIEW ZIP → ZIP-only hash-chain verification.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

_REQUIRED_SCRIPTS = ("make_review_zip.sh", "build_review_manifest.py", "build_review_zip.py",
                     "build_observability_index.py", "select_review_evidence.py",
                     "stage_review_evidence.py")
_REQUIRED_MODULES = (
    "packages/orchestration/__init__.py", "packages/orchestration/data_paths.py",
    "packages/orchestration/evidence_index.py", "packages/orchestration/review_zip.py",
    "packages/orchestration/archive_plan.py", "packages/orchestration/review_subject.py",
    "packages/orchestration/evidence_inventory.py", "packages/common/__init__.py",
    "packages/common/secure_fs.py",
)


def _run(cmd, cwd, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180,
                          env={**os.environ, **(env or {})})


def _git(repo, *args, env=None):
    e = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
         "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t", **(env or {})}
    return _run(["git", *args], repo, e)


def _build_repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for name in _REQUIRED_SCRIPTS:
        shutil.copy2(REPO_ROOT / "scripts" / name, repo / "scripts" / name)
    # The full package tree is resolved from the real repo via PYTHONPATH (see _run), so the
    # temp repo carries only scripts + the reviewed source — no partial `packages/` to shadow it.
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("# base\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    base = _git(repo, "rev-parse", "HEAD").stdout.strip()
    # feature commit: one source + one test file
    (repo / "src").mkdir()
    (repo / "src" / "app.py").write_text("def add(a, b):\n    return a + b\n")
    (repo / "tests_pkg").mkdir()
    (repo / "tests_pkg" / "test_app.py").write_text("def test_add():\n    assert True\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "feature")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    return repo, base, head


def _write_evidence(repo, base, head, ev):
    """Build a faithful evidence dir (OUTSIDE the git repo so it never pollutes the dirty set):
    real resolved Subject + aligned strict Proof + gates."""
    import sys
    sys.path.insert(0, str(REPO_ROOT))
    from packages.orchestration.repair_attest import is_attestable_source
    from packages.orchestration.review_subject import resolve_review_subject

    subject = resolve_review_subject(str(repo), base)
    authority = sorted({f.path for f in subject.files if is_attestable_source(f.path)})

    (ev / "task_runs" / "t1").mkdir(parents=True)
    (ev / "review_subject.json").write_text(json.dumps(subject.to_json(), indent=2, sort_keys=True))
    file_hashes = {p: hashlib.sha256((repo / p).read_bytes()).hexdigest() for p in authority}
    (ev / "current_change_content_proof.json").write_text(json.dumps({
        "schema_version": "1.1.0", "base_commit": base, "head_commit": head,
        "file_hashes": file_hashes, "file_count": len(file_hashes),
        "tombstones": {}, "tombstone_count": 0}, indent=2, sort_keys=True))
    (ev / "final_verifier_report.json").write_text(json.dumps({
        "verdict": "PASS_WITH_RISKS", "authoritative_changed_files": authority,
        "review_subject_uncovered_files": []}, indent=2, sort_keys=True))
    (ev / "change_provenance_gate.json").write_text(json.dumps({
        "status": "PASS", "covered_files": authority, "uncovered_files": [],
        "source_files": authority}, indent=2, sort_keys=True))
    (ev / "review_commit_chain.json").write_text(json.dumps({
        "chain_v": 1, "base_commit": base, "head_commit": head, "commits": []}, sort_keys=True))
    (ev / "fresh_evidence_gate.json").write_text(json.dumps({
        "evidence_freshness": {"is_fresh": True}}, indent=2, sort_keys=True))
    # root + task artifacts so the manifest treats the run as valid
    (ev / "job_flow.json").write_text('{"job_id":"e2e","final_audit":{"status":"pass"}}')
    for f in ("manifest.json", "agent_run_trace.jsonl", "agent_run_trace_summary.json",
              "prompt_trace_summary.json", "command_transcript.json"):
        (ev / f).write_text("{}")
    for f in ("prompt_trace.jsonl", "prompt_trace_summary.json", "review.json", "repair_loop.json",
              "token_accounting.json", "provider_evidence.json"):
        (ev / "task_runs" / "t1" / f).write_text("{}")
    return ev, subject, authority


class TestAuthoritativeEndToEnd:
    def test_committed_subject_to_ready_zip_with_raw_byte_chain(self, tmp_path):
        repo, base, head = _build_repo(tmp_path)
        ev, subject, authority = _write_evidence(repo, base, head, tmp_path / "evidence")
        proc = _run(["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
                    repo, {"REMEDY_REVIEW_BASE": base, "PYTHONPATH": str(REPO_ROOT)})
        assert proc.returncode == 0, proc.stdout + proc.stderr
        zips = sorted(repo.glob("remedy-review-*.zip"))
        assert zips, proc.stdout
        z = zips[-1]

        # F6/F7 — the filename status equals the packaged manifest status.
        assert "READY_FOR_REVIEW" in z.name, proc.stdout

        with zipfile.ZipFile(z) as zf:
            names = set(zf.namelist())
            for n in ("evidence/current/review_subject.json",
                      "evidence/current/current_change_content_proof.json",
                      "evidence/current/review_commit_chain.json",
                      "evidence/current/review_archive_plan.json",
                      "evidence/current/review_zip_expectation.json",
                      ".review_zip_manifest.json"):
                assert n in names, n
            subject_b = zf.read("evidence/current/review_subject.json")
            proof_b = zf.read("evidence/current/current_change_content_proof.json")
            chain_b = zf.read("evidence/current/review_commit_chain.json")
            plan = json.loads(zf.read("evidence/current/review_archive_plan.json"))
            expect = json.loads(zf.read("evidence/current/review_zip_expectation.json"))
            manifest = json.loads(zf.read(".review_zip_manifest.json"))

        subject_sha = hashlib.sha256(subject_b).hexdigest()
        chain_sha = hashlib.sha256(chain_b).hexdigest()
        proof_sha = hashlib.sha256(proof_b).hexdigest()
        chain = manifest["package_hash_chain"]

        # F2 — plan/expectation/manifest subject sha ALL equal the packaged Subject bytes' sha.
        assert plan["review_subject_sha256"] == subject_sha
        assert expect["review_subject_sha256"] == subject_sha
        assert chain["review_subject_sha256"] == subject_sha
        # F4 — commit-chain sha equals the packaged bytes.
        assert chain["commit_chain_sha256"] == chain_sha
        # F2 — content-proof sha equals the packaged bytes.
        assert chain["content_proof_sha256"] == proof_sha
        # F6/F7 — the manifest's own package status is READY.
        assert manifest["package_status"] == "READY_FOR_REVIEW"
        # authority equality reflected in the plan
        auth_members = sorted(m["archive_path"] for m in plan["repository_members"]
                              if m["authoritative"])
        assert auth_members == authority
