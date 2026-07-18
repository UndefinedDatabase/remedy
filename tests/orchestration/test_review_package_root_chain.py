"""F4/F10 (round 20) — the directed package hash chain is complete and recomputes from ZIP bytes.

An end-to-end build produces plan -> expectation -> manifest, each carrying the previous artifact's
sha256, and every one of those hashes recomputes from the ZIP-only bytes. No artifact hashes itself.
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
    "packages/common/secure_fs.py", "packages/common/strict_json.py",
)


def _isolated_repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for name in _REQUIRED_SCRIPTS:
        shutil.copy2(REPO_ROOT / "scripts" / name, repo / "scripts" / name)
    for rel in _REQUIRED_MODULES:
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / rel, dst)
    (repo / "README.md").write_text("# t\n")
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True, capture_output=True,
                   env=env)
    return repo


def _synthetic_evidence(repo):
    ev = repo / "evdir"
    (ev / "task_runs" / "t1").mkdir(parents=True)
    (ev / "job_flow.json").write_text('{"job_id":"j","final_audit":{"status":"pass"}}')
    for f in ("manifest.json", "agent_run_trace.jsonl", "agent_run_trace_summary.json",
              "prompt_trace_summary.json", "command_transcript.json"):
        (ev / f).write_text("{}")
    for f in ("prompt_trace.jsonl", "prompt_trace_summary.json", "review.json", "repair_loop.json",
              "token_accounting.json", "provider_evidence.json"):
        (ev / "task_runs" / "t1" / f).write_text("{}")
    return ev


def test_the_directed_chain_recomputes_from_zip_only_bytes(tmp_path):
    repo = _isolated_repo(tmp_path)
    ev = _synthetic_evidence(repo)
    proc = subprocess.run(["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
                          cwd=repo, capture_output=True, text=True, timeout=180)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    z = sorted(repo.glob("remedy-review-*.zip"))[-1]
    with zipfile.ZipFile(z) as zf:
        plan_b = zf.read("evidence/current/review_archive_plan.json")
        expect_b = zf.read("evidence/current/review_zip_expectation.json")
        manifest_b = zf.read(".review_zip_manifest.json")

    sha_plan = hashlib.sha256(plan_b).hexdigest()
    sha_expect = hashlib.sha256(expect_b).hexdigest()
    expect = json.loads(expect_b)
    manifest = json.loads(manifest_b)
    chain = manifest["package_hash_chain"]

    # expectation carries the plan sha; manifest carries plan + expectation shas — the directed chain
    assert expect["review_archive_plan_sha256"] == sha_plan
    assert chain["review_archive_plan_sha256"] == sha_plan
    assert chain["review_zip_expectation_sha256"] == sha_expect
    # nothing hashes itself: the manifest does not contain its own sha
    assert sha_plan != sha_expect
    for v in chain.values():
        if isinstance(v, str):
            assert v != hashlib.sha256(manifest_b).hexdigest()

    # every source member hash in the plan recomputes from the packaged member bytes
    plan = json.loads(plan_b)
    with zipfile.ZipFile(z) as zf:
        for m in plan["repository_members"] + plan["evidence_members"]:
            if m["kind"] != "regular":
                continue
            data = zf.read(m["archive_path"])
            assert hashlib.sha256(data).hexdigest() == m["content_sha256"], m["archive_path"]
