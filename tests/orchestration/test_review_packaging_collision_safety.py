"""F3 (round 29) — packaging never deletes or overwrites a TRACKED project file that collides with
one of its own output paths. make_review_zip.sh refuses (exit 3) and leaves the tracked file
byte-identical, rather than silently reserving/deleting it as scratch state."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MAKE = REPO_ROOT / "scripts" / "make_review_zip.sh"

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None or shutil.which("bash") is None,
    reason="git and bash required")

_HELPERS = ("select_review_evidence.py", "stage_review_evidence.py",
            "build_observability_index.py", "build_review_manifest.py", "build_review_zip.py")


def _mini_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    shutil.copy2(MAKE, repo / "scripts" / "make_review_zip.sh")
    for h in _HELPERS:
        shutil.copy2(MAKE.parent / h, repo / "scripts" / h)
    (repo / "README.md").write_text("# tmp\n")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True, capture_output=True)
    return repo


def _run(repo: Path):
    return subprocess.run(
        ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(repo / "nonexistent-ev")],
        cwd=repo, capture_output=True, text=True, timeout=120,
        # A CLOSED environment: no HOME, so the packaging script cannot resolve its default archive
        # target. REMEDY_REVIEW_DIR="." names this mini repository explicitly instead.
        env={"PYTHONPATH": str(REPO_ROOT), "PATH": __import__("os").environ["PATH"],
             "REMEDY_REVIEW_DIR": "."})


class TestTrackedOutputCollisionRefused:
    def test_tracked_root_manifest_is_never_overwritten(self, tmp_path):
        repo = _mini_repo(tmp_path)
        sacred = repo / ".review_zip_manifest.json"
        original = b'{"this":"is a tracked project file, not scratch state"}\n'
        sacred.write_bytes(original)
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "track manifest"], cwd=repo, check=True,
                       capture_output=True)

        proc = _run(repo)
        assert proc.returncode == 3, proc.stdout + proc.stderr
        assert "refusing to" in (proc.stdout + proc.stderr)
        # The tracked file is byte-identical — packaging did not touch it.
        assert sacred.read_bytes() == original

    def test_untracked_leftover_manifest_is_not_a_collision(self, tmp_path):
        # An UNTRACKED leftover manifest is safe scratch state; the guard does not refuse on it.
        repo = _mini_repo(tmp_path)
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True, capture_output=True)
        (repo / ".review_zip_manifest.json").write_bytes(b"{}\n")
        proc = _run(repo)
        # It fails later (no evidence), but NOT with the collision refusal (exit 3).
        assert proc.returncode != 3
        assert "refusing to" not in (proc.stdout + proc.stderr)
