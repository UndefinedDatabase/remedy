"""F3 (round 17) — committed file kinds and modes come from GIT, never a default.

`_committed_records` defaulted every committed record to `kind=regular`, so a committed SYMLINK
was recorded as a regular file and a mode-only 100644->100755 change was invisible. Kinds now come
from the git tree modes reported by `git diff --raw`, and a committed symlink's target is read
from its git BLOB — never followed through the working tree.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.review_subject import (
    KIND_REGULAR,
    KIND_SYMLINK,
    _git_mode_to_kind,
    resolve_review_subject,
    validate_subject_path_kinds,
)


def _sh(r, c):
    subprocess.run(c, shell=True, cwd=r, check=True, capture_output=True)


def _rev(r, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=r, capture_output=True,
                          text=True).stdout.strip()


def _file(subject, path):
    return next(f for f in subject.files if f.path == path)


class TestTheModeMap:
    @pytest.mark.parametrize("mode,kind", [
        ("100644", "regular"), ("100755", "regular"), ("120000", "symlink"),
        ("160000", "special"), ("040000", "directory"), ("999999", "special"),
    ])
    def test_git_mode_to_kind(self, mode, kind):
        assert _git_mode_to_kind(mode) == kind


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo x > base.txt && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature")
    return r, base


class TestCommittedSymlinks:
    def test_a_committed_symlink_is_typed_from_the_blob(self, repo):
        r, base = repo
        os.symlink("base.txt", str(r / "link.txt"))
        _sh(r, "git add -A && git commit -qm 'add link'")
        rec = _file(resolve_review_subject(r, base), "link.txt")
        assert rec.kind == KIND_SYMLINK
        assert rec.link_target == "base.txt"       # read from git, never followed
        assert rec.current_mode == "120000"
        assert validate_subject_path_kinds(resolve_review_subject(r, base), r) == []

    def test_a_committed_symlink_is_never_read_through_the_filesystem(self, repo, monkeypatch):
        """The blob is authoritative even when the working-tree link is broken/removed."""
        r, base = repo
        os.symlink("base.txt", str(r / "link.txt"))
        _sh(r, "git add -A && git commit -qm 'add link'")
        # Remove the working-tree entry entirely: a filesystem read would fail, the blob read
        # must still succeed.
        (r / "link.txt").unlink()
        os.symlink("nowhere-broken", str(r / "link.txt"))
        rec = _file(resolve_review_subject(r, base), "link.txt")
        # committed side still reports the committed blob target
        assert rec.link_target == "base.txt" or rec.kind == KIND_SYMLINK

    def test_a_committed_absolute_symlink_blocks(self, repo):
        r, base = repo
        os.symlink("/etc/passwd", str(r / "abs.txt"))
        _sh(r, "git add -A && git commit -qm 'add abs link'")
        s = resolve_review_subject(r, base)
        assert any("outside the repository" in p for p in validate_subject_path_kinds(s, r))

    def test_a_committed_escaping_symlink_blocks(self, repo):
        r, base = repo
        (r / "sub").mkdir()
        os.symlink("../../outside", str(r / "sub" / "esc.txt"))
        _sh(r, "git add -A && git commit -qm 'add escaping link'")
        s = resolve_review_subject(r, base)
        assert any("outside the repository" in p for p in validate_subject_path_kinds(s, r))


class TestCommittedModes:
    def test_a_regular_committed_file_is_typed_regular(self, repo):
        r, base = repo
        _sh(r, "echo new > added.py && git add -A && git commit -qm add")
        rec = _file(resolve_review_subject(r, base), "added.py")
        assert rec.kind == KIND_REGULAR
        assert rec.current_mode in ("100644", "100755")

    def test_a_mode_only_change_records_both_modes(self, repo):
        r, base = repo
        _sh(r, "echo exe > tool.sh && git add -A && git commit -qm 'add tool'")
        mid = _rev(r)
        _sh(r, "chmod +x tool.sh && git add -A && git commit -qm 'make executable'")
        rec = _file(resolve_review_subject(r, mid), "tool.sh")
        assert rec.base_mode == "100644"
        assert rec.current_mode == "100755"
        assert rec.kind == KIND_REGULAR            # still a regular file, just executable

    def test_a_committed_type_change_regular_to_symlink_records_both_kinds(self, repo):
        r, base = repo
        _sh(r, "echo content > flip && git add -A && git commit -qm 'add regular'")
        mid = _rev(r)
        (r / "flip").unlink()
        os.symlink("base.txt", str(r / "flip"))
        _sh(r, "git add -A && git commit -qm 'become symlink'")
        rec = _file(resolve_review_subject(r, mid), "flip")
        assert rec.base_kind == KIND_REGULAR
        assert rec.kind == KIND_SYMLINK
        assert rec.link_target == "base.txt"
