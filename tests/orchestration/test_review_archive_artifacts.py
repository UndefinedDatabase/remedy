"""F2 (round 19) — the ArchivePlan and its verification report are packaged and referenced.

A ZIP-only reviewer could not verify the model the members were built from, because neither the
typed plan nor a verification report was in the archive. Both are now packaged under
evidence/current/ as verified members, and the manifest names them.
"""
from __future__ import annotations

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
    "packages/common/secure_fs.py",
)


class TestVerificationReportContent:
    def test_report_is_derived_from_the_plan(self):
        plan = ArchivePlanV1(repository_members=(
            ArchiveMemberV1(archive_path="a.py", kind=MEMBER_REGULAR, mode=MODE_REGULAR,
                            authoritative=True, source_root="/r", source_rel="a.py",
                            source_class=SOURCE_REPOSITORY),
            ArchiveMemberV1(archive_path="l", kind=MEMBER_SYMLINK, mode=MODE_SYMLINK,
                            authoritative=False, source_root="/r", source_rel="l",
                            source_class=SOURCE_REPOSITORY),
        ), review_subject_sha256="a" * 64, authority_set_sha256="b" * 64)
        report = _bz._verification_report(plan)
        assert report["review_subject_sha256"] == "a" * 64
        assert report["authority_set_sha256"] == "b" * 64
        assert report["authoritative_member_count"] == 1
        assert report["symlink_member_count"] == 1
        assert report["expected_member_count"] == 3     # 2 members + manifest
        assert report["verdict"] == "PLAN_ENFORCED"


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
    def test_plan_and_report_are_members_and_referenced(self, tmp_path):
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
            assert "evidence/current/review_archive_plan.json" in names
            assert "evidence/current/review_zip_verification.json" in names
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
            ra = manifest["current_evidence"]["review_archive"]
            assert ra["plan"] == "evidence/current/review_archive_plan.json"
            assert ra["verification"] == "evidence/current/review_zip_verification.json"
            # the packaged plan lists itself and the report as members
            plan = json.loads(zf.read("evidence/current/review_archive_plan.json"))
            ev_paths = {m["archive_path"] for m in plan["evidence_members"]}
            assert "evidence/current/review_archive_plan.json" in ev_paths
            assert "evidence/current/review_zip_verification.json" in ev_paths
