"""F4 (round 17) — the content-proof check is typed and NO-FOLLOW.

`_check_bundle_integrity` used `os.path.isfile` + `open`, both of which FOLLOW symlinks: an allowed
contained symlink was hashed as its TARGET's bytes (content from outside the packaged set), and a
regular file swapped for a symlink after the proof was written would still verify against the
target. Each path is now inspected with `lstat` and hashed by its declared kind — a regular file
its own bytes, a symlink its literal target text, never the target.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

import scripts.build_review_manifest as brm


def _proof(root: Path, files: dict, subject_files: list):
    """Write current_change_content_proof.json + review_subject.json into an evidence dir."""
    ev = root / "ev"
    ev.mkdir()
    (ev / "current_change_content_proof.json").write_text(json.dumps({"file_hashes": files}))
    (ev / "review_subject.json").write_text(json.dumps(
        {"subject_v": 1, "base_commit": "", "head_commit": "", "base_is_ancestor": False,
         "commits": [], "files": subject_files}))
    return str(ev)


class TestTypedNoFollowContentProof:
    def test_a_safe_dirty_symlink_is_hashed_as_its_target_text(self, tmp_path):
        root = tmp_path / "src"
        root.mkdir()
        (root / "real.py").write_text("REAL CONTENT")
        os.symlink("real.py", str(root / "link.py"))
        link_hash = hashlib.sha256(b"real.py").hexdigest()
        ev = _proof(root, {"link.py": link_hash},
                    [{"path": "link.py", "status": "dirty", "base_sha256": None,
                      "current_sha256": link_hash, "kind": "symlink",
                      "link_target": "real.py"}])
        result = brm._check_bundle_integrity(ev, str(root))
        assert result["verdict"] == "PASS", result
        assert result["current_content_hash_mismatches"] == []

    def test_the_symlink_target_bytes_are_never_hashed(self, tmp_path):
        """If the check followed the link it would hash 'REAL CONTENT'; it must not."""
        root = tmp_path / "src"
        root.mkdir()
        (root / "real.py").write_text("REAL CONTENT")
        os.symlink("real.py", str(root / "link.py"))
        target_bytes_hash = hashlib.sha256(b"REAL CONTENT").hexdigest()
        ev = _proof(root, {"link.py": target_bytes_hash},
                    [{"path": "link.py", "status": "dirty", "base_sha256": None,
                      "current_sha256": target_bytes_hash, "kind": "symlink",
                      "link_target": "real.py"}])
        result = brm._check_bundle_integrity(ev, str(root))
        # The proof (wrongly) claims the TARGET bytes; the no-follow check hashes the link text,
        # so this must MISMATCH rather than silently pass by following.
        assert result["verdict"] == "BLOCKED"

    def test_a_regular_file_swapped_for_a_symlink_after_proof_blocks(self, tmp_path):
        root = tmp_path / "src"
        root.mkdir()
        (root / "outside.txt").write_text("secret outside")
        # proof was written for a REGULAR file
        reg_hash = hashlib.sha256(b"the regular content").hexdigest()
        ev = _proof(root, {"f.py": reg_hash},
                    [{"path": "f.py", "status": "dirty", "base_sha256": None,
                      "current_sha256": reg_hash, "kind": "regular"}])
        # but on disk it is now a symlink to outside content
        os.symlink("outside.txt", str(root / "f.py"))
        result = brm._check_bundle_integrity(ev, str(root))
        assert result["verdict"] == "BLOCKED"
        assert any(m.get("actual") == "not-a-regular-file"
                   for m in result["current_content_hash_mismatches"])

    def test_a_forged_link_target_blocks(self, tmp_path):
        root = tmp_path / "src"
        root.mkdir()
        (root / "real.py").write_text("x")
        os.symlink("real.py", str(root / "link.py"))
        link_hash = hashlib.sha256(b"real.py").hexdigest()
        ev = _proof(root, {"link.py": link_hash},
                    [{"path": "link.py", "status": "dirty", "base_sha256": None,
                      "current_sha256": link_hash, "kind": "symlink",
                      "link_target": "SOMETHING_ELSE.py"}])
        result = brm._check_bundle_integrity(ev, str(root))
        assert result["verdict"] == "BLOCKED"

    def test_a_regular_file_verifies_by_its_own_bytes(self, tmp_path):
        root = tmp_path / "src"
        root.mkdir()
        (root / "f.py").write_text("hello")
        h = hashlib.sha256(b"hello").hexdigest()
        ev = _proof(root, {"f.py": h},
                    [{"path": "f.py", "status": "dirty", "base_sha256": None,
                      "current_sha256": h, "kind": "regular"}])
        assert brm._check_bundle_integrity(ev, str(root))["verdict"] == "PASS"

    def test_a_missing_declared_path_is_a_missing_proof(self, tmp_path):
        root = tmp_path / "src"
        root.mkdir()
        h = hashlib.sha256(b"x").hexdigest()
        ev = _proof(root, {"gone.py": h},
                    [{"path": "gone.py", "status": "dirty", "base_sha256": None,
                      "current_sha256": h, "kind": "regular"}])
        result = brm._check_bundle_integrity(ev, str(root))
        assert "gone.py" in result["current_content_hash_missing_proofs"]
