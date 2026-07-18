"""F6/F7 (round 21) — the final package status/filename come from the VERIFIED build model, not a
post-build reread of the mutable disk manifest."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MAKE = REPO_ROOT / "scripts" / "make_review_zip.sh"

_SCRIPTS = ("make_review_zip.sh", "build_review_manifest.py", "build_review_zip.py",
            "build_observability_index.py", "select_review_evidence.py",
            "stage_review_evidence.py")


def _repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for n in _SCRIPTS:
        shutil.copy2(REPO_ROOT / "scripts" / n, repo / "scripts" / n)
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
    (repo / "README.md").write_text("# t\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True, capture_output=True,
                   env=env)
    return repo


class TestStatusComesFromTheVerifiedModel:
    def test_the_shell_reads_status_from_the_build_result(self):
        src = MAKE.read_text()
        # The status block uses BUILD_RESULT (stdout), not a post-build json.load of the manifest.
        assert "BUILD_RESULT" in src
        block = src.split("Package status comes from the VERIFIED build result")[1]
        block = block.split("Terminal status block")[0]
        assert "json.load(open('$MANIFEST'))" not in block

    def test_build_zip_emits_the_verified_status(self):
        src = (REPO_ROOT / "scripts" / "build_review_zip.py").read_text()
        assert "verified_status" in src
        for key in ("package_status", "evidence_authoritative", "review_subject_alignment",
                    "manifest_sha256"):
            assert key in src

    def test_filename_status_equals_packaged_manifest_status(self, tmp_path):
        repo = _repo(tmp_path)
        proc = subprocess.run(["bash", "scripts/make_review_zip.sh"], cwd=repo,
                              capture_output=True, text=True, timeout=180,
                              env={**os.environ, "PYTHONPATH": str(REPO_ROOT)})
        assert proc.returncode == 0, proc.stdout + proc.stderr
        m = re.search(r"^PACKAGE_STATUS=(\S+)$", proc.stdout, re.M)
        assert m, proc.stdout
        status = m.group(1)
        z = sorted(repo.glob("remedy-review-*.zip"))[-1]
        assert status in z.name
        with zipfile.ZipFile(z) as zf:
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
        # the filename status and the packaged manifest status are ONE verified fact
        assert manifest["package_status"] == status
