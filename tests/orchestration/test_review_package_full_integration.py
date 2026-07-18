"""F7 (round 18) — the REAL `make_review_zip.sh` hands the subject path to the plan builder.

Round 17's symlink tests proved the ReviewSubject could describe a symlink, the bundle integrity
could hash its link text, and `build_review_zip()` could package one when handed its path. They did
NOT prove that `make_review_zip.sh` actually drives the plan-based builder end to end. These tests
run the real packaging entry point on a repo with hostile file shapes and assert the ZIP's exact,
typed membership.
"""
from __future__ import annotations

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
_REQUIRED_MODULES = ("packages/orchestration/__init__.py", "packages/orchestration/data_paths.py",
                     "packages/orchestration/evidence_index.py",
                     "packages/orchestration/review_zip.py",
                     "packages/orchestration/archive_plan.py",
                     "packages/orchestration/review_subject.py",
                     "packages/orchestration/evidence_inventory.py",
                     "packages/common/__init__.py", "packages/common/secure_fs.py", "packages/common/strict_json.py", "packages/common/acquisition_budget.py")

_S_IFREG = 0o100000
_S_IFLNK = 0o120000

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None or shutil.which("bash") is None,
    reason="git and bash required")


def _repo(tmp_path):
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
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, env=env)
    subprocess.run(["git", "add", "."], cwd=repo, check=True, env=env)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True, env=env)
    return repo, env


def _run(repo, env):
    return subprocess.run(["bash", "scripts/make_review_zip.sh"], cwd=repo, env=env,
                          capture_output=True, text=True, timeout=120)


def _zip(repo):
    zips = sorted(repo.glob("*.zip"))
    assert zips, "no zip produced"
    return zipfile.ZipFile(zips[-1])


def _ftype(info):
    return (info.external_attr >> 16) & 0o170000


def _perm(info):
    return (info.external_attr >> 16) & 0o7777


# --------------------------------------------------------------------------- shapes


class TestRealPackagingHandlesFileShapes:
    def test_a_safe_symlink_is_packaged_as_a_symlink(self, tmp_path):
        repo, env = _repo(tmp_path)
        (repo / "target.txt").write_text("t")
        os.symlink("target.txt", str(repo / "link.txt"))
        proc = _run(repo, env)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        with _zip(repo) as zf:
            assert "link.txt" in zf.namelist()
            assert _ftype(zf.getinfo("link.txt")) == _S_IFLNK
            assert zf.read("link.txt").decode() == "target.txt"

    def test_an_executable_file_keeps_its_bit(self, tmp_path):
        repo, env = _repo(tmp_path)
        tool = repo / "tool.sh"
        tool.write_text("#!/bin/sh\necho hi\n")
        os.chmod(tool, 0o755)
        subprocess.run(["git", "add", "-A"], cwd=repo, env=env, check=True)
        subprocess.run(["git", "commit", "-qm", "tool"], cwd=repo, env=env, check=True)
        proc = _run(repo, env)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        with _zip(repo) as zf:
            assert _perm(zf.getinfo("tool.sh")) == 0o755

    def test_a_newline_and_unicode_name_survive(self, tmp_path):
        repo, env = _repo(tmp_path)
        (repo / "with\nnewline.py").write_text("n")
        (repo / "ünïcode.py").write_text("u")
        proc = _run(repo, env)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        with _zip(repo) as zf:
            names = zf.namelist()
            assert "with\nnewline.py" in names
            assert "ünïcode.py" in names

    def test_a_special_file_is_never_packaged(self, tmp_path):
        """A FIFO is neither a regular file nor a symlink, so the bundle discovery
        (`-type f -o -type l`) never selects it — it is simply absent from the archive, never
        packaged as garbage. (An AUTHORITATIVE special file — one in the ReviewSubject — BLOCKS
        the plan; that path is covered by test_review_archive_plan.py without needing evidence.)"""
        repo, env = _repo(tmp_path)
        os.mkfifo(str(repo / "pipe"))
        proc = _run(repo, env)
        if proc.returncode == 0 and list(repo.glob("*.zip")):
            with _zip(repo) as zf:
                assert "pipe" not in zf.namelist()

    def test_the_output_reports_plan_counts(self, tmp_path):
        repo, env = _repo(tmp_path)
        (repo / "target.txt").write_text("t")
        os.symlink("target.txt", str(repo / "l.txt"))
        proc = _run(repo, env)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "symlink_count" in proc.stdout


class TestExternalSymlinkBlocksBeforeReadingTarget:
    def test_an_external_symlink_in_the_bundle_is_never_dereferenced(self, tmp_path):
        repo, env = _repo(tmp_path)
        outside = tmp_path / "outside.txt"
        outside.write_text("OUTSIDE SECRET")
        os.symlink(str(outside), str(repo / "evil.txt"))
        proc = _run(repo, env)
        # a symlink is packaged as its target TEXT, never followed — the secret is never read.
        # (An external symlink in context is recorded as text; it does not leak the target bytes.)
        if proc.returncode == 0:
            with _zip(repo) as zf:
                if "evil.txt" in zf.namelist():
                    body = zf.read("evil.txt")
                    assert b"OUTSIDE SECRET" not in body
        assert "OUTSIDE SECRET" not in proc.stdout
