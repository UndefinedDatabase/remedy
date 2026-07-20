"""F5 (round 17) — dirty deletions and renames carry FULL base-side proofs.

A dirty deletion used to record `base_sha256: null` — no tombstone, so nothing said what was
removed. A dirty (staged) rename lost its old path and base hash entirely. Both are now resolved
against the declared HEAD with git BLOB reads (never the working tree): a deletion records the
HEAD blob it removed, a rename records old path + both hashes + both kinds.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.review_subject import (
    KIND_REGULAR,
    STATUS_DELETED,
    STATUS_RENAMED,
    resolve_review_subject,
)


def _sh(r, c):
    subprocess.run(c, shell=True, cwd=r, check=True, capture_output=True)


def _rev(r, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=r, capture_output=True,
                          text=True).stdout.strip()


def _file(subject, path):
    return next(f for f in subject.files if f.path == path)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    (r / "keep.py").write_text("keep\n")
    (r / "gone.py").write_text("gone\n")
    # old.py is substantial so a one-line edit keeps git's rename detection above threshold.
    (r / "old.py").write_text("\n".join(f"line {i}" for i in range(40)) + "\n")
    _sh(r, "git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature && echo work > work.py && git add -A "
           "&& git commit -qm work")
    return r, base


class TestDirtyDeletionsCarryATombstone:
    def test_the_reproduced_case(self, repo):
        """A dirty deletion of a HEAD file records the blob it removed."""
        r, base = repo
        (r / "gone.py").unlink()
        rec = _file(resolve_review_subject(r, base), "gone.py")
        assert rec.status == STATUS_DELETED
        assert rec.base_sha256 is not None and len(rec.base_sha256) == 64
        assert rec.current_sha256 is None
        assert rec.base_kind == KIND_REGULAR

    def test_a_null_base_hash_for_a_head_file_would_be_a_bug(self, repo):
        r, base = repo
        (r / "keep.py").unlink()
        rec = _file(resolve_review_subject(r, base), "keep.py")
        assert rec.base_sha256, "a deletion of a file present at HEAD must carry its tombstone"

    def test_the_tombstone_is_the_head_blob_content(self, repo):
        import hashlib

        r, base = repo
        expected = hashlib.sha256((r / "gone.py").read_bytes()).hexdigest()
        (r / "gone.py").unlink()
        rec = _file(resolve_review_subject(r, base), "gone.py")
        assert rec.base_sha256 == expected


class TestDirtyRenames:
    def test_a_staged_rename_records_old_and_new_paths(self, repo):
        r, base = repo
        _sh(r, "git mv old.py new.py")
        s = resolve_review_subject(r, base)
        rec = _file(s, "new.py")
        assert rec.status == STATUS_RENAMED
        assert rec.old_path == "old.py"
        assert rec.base_sha256 is not None       # what old.py was
        assert rec.current_sha256 is not None     # what new.py is

    def test_a_rename_plus_edit_carries_both_hashes(self, repo):
        r, base = repo
        _sh(r, "git mv old.py new.py")
        # append one line: git still detects the rename (>50% similar), and both hashes differ.
        with open(r / "new.py", "a") as fh:
            fh.write("one appended line\n")
        _sh(r, "git add new.py")
        rec = _file(resolve_review_subject(r, base), "new.py")
        assert rec.old_path == "old.py", "a lightly-edited rename must stay a rename"
        assert rec.base_sha256 != rec.current_sha256

    def test_a_committed_rename_plus_dirty_edit_stays_a_rename(self, repo):
        r, base = repo
        _sh(r, "git mv old.py renamed.py && git commit -qm 'rename'")
        (r / "renamed.py").write_text("dirty edit\n")
        rec = _file(resolve_review_subject(r, base), "renamed.py")
        # committed rename provides old_path + base; the dirty edit updates current
        assert rec.old_path == "old.py"
        assert rec.base_sha256 is not None
        assert "dirty edit" not in (rec.link_target or "")

    def test_a_delete_of_a_file_modified_in_committed_history(self, repo):
        r, base = repo
        _sh(r, "echo changed > gone.py && git add -A && git commit -qm 'edit gone'")
        (r / "gone.py").unlink()
        rec = _file(resolve_review_subject(r, base), "gone.py")
        assert rec.status == STATUS_DELETED
        assert rec.base_sha256 is not None

    def test_hostile_path_names_survive(self, repo):
        r, base = repo
        weird = "a b\tc'd.py"
        (r / weird).write_text("weird\n")
        _sh(r, "git add -A")
        rec = _file(resolve_review_subject(r, base), weird)
        assert rec.path == weird
        assert rec.current_sha256 is not None
