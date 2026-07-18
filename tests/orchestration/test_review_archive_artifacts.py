"""F2 (round 19) — the ArchivePlan and its verification report are packaged and referenced.

A ZIP-only reviewer could not verify the model the members were built from, because neither the
typed plan nor a verification report was in the archive. Both are now packaged under
evidence/current/ as verified members, and the manifest names them.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

_SPEC = importlib.util.spec_from_file_location(
    "_bz2", REPO_ROOT / "scripts" / "build_review_zip.py")
_bz = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_bz)

from packages.orchestration.archive_plan import (  # noqa: E402
    ArchiveMemberV1,
    ArchivePlanV1,
    MEMBER_REGULAR,
    MEMBER_SYMLINK,
    MODE_REGULAR,
    MODE_SYMLINK,
    SOURCE_REPOSITORY,
)

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


class TestArtifactsPackaged:
    def test_the_directed_chain_artifacts_are_members_and_referenced(self, tmp_path):
        repo = _isolated_repo(tmp_path)
        ev = _synthetic_evidence(repo)
        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
            cwd=repo, capture_output=True, text=True, timeout=180)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        zips = sorted(repo.glob("remedy-review-*.zip"))
        assert zips, proc.stdout
        with zipfile.ZipFile(zips[-1]) as zf:
            names = set(zf.namelist())
            # Round 20: the directed chain — plan + expectation packaged (no self-hashing report).
            assert "evidence/current/review_archive_plan.json" in names
            assert "evidence/current/review_zip_expectation.json" in names
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
            chain = manifest["package_hash_chain"]
            plan_bytes = zf.read("evidence/current/review_archive_plan.json")
            expect_bytes = zf.read("evidence/current/review_zip_expectation.json")
            assert chain["review_archive_plan_sha256"] == hashlib.sha256(plan_bytes).hexdigest()
            assert chain["review_zip_expectation_sha256"] == \
                hashlib.sha256(expect_bytes).hexdigest()
            # the expectation names the plan by hash (directed chain, no self-hash)
            expect = json.loads(expect_bytes)
            assert expect["review_archive_plan_sha256"] == \
                chain["review_archive_plan_sha256"]
            # the packaged plan lists every SOURCE member with an expected hash
            plan = json.loads(plan_bytes)
            for m in plan["repository_members"] + plan["evidence_members"]:
                if m["kind"] == "regular":
                    assert m["content_sha256"], m["archive_path"]
