"""F4 (round 15) — deletions and renames are provable parts of a committed review subject.

The round-14 proof hashed files that still exist. So a committed deletion sat in the review
subject and in no proof set:

    base contains base.txt
    feature commit deletes base.txt
    review subject files  = [base.txt]
    current content proof = no base.txt entry

"No entry" is indistinguishable from "never looked", and a removed file is emphatically part of a
change. A deleted path now carries a TOMBSTONE — the hash it had at the base — and the packager
counts that as authoritative coverage rather than reporting a false missing proof.

Paths come from ONE canonical NUL-delimited git command, so a name containing a space, a quote or
a newline survives intact; parsing git's human-formatted status text would corrupt exactly those.
"""
from __future__ import annotations

import hashlib
import subprocess

import pytest

from packages.orchestration.review_subject import (
    STATUS_ADDED,
    STATUS_DELETED,
    STATUS_MODIFIED,
    STATUS_RENAMED,
    resolve_review_subject,
)


def _sh(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


def _rev(repo, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=repo, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    (r / "base.txt").write_text("base content\n")
    (r / "old.txt").write_text("moved content\n")
    (r / "keep.txt").write_text("untouched\n")
    _sh(r, "git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature")
    _sh(r, "git rm -q base.txt && git mv old.txt new.txt")
    (r / "added.txt").write_text("brand new\n")
    _sh(r, "git add -A && git commit -qm 'delete, rename, add'")
    return r, base


def _by(subject):
    return {f.path: f for f in subject.files}


# --------------------------------------------------------------------------- deletion


class TestACommittedDeletionIsProven:
    def test_the_reproduced_case(self, repo):
        """base.txt was deleted; it must still appear, with a proof."""
        r, base = repo
        s = resolve_review_subject(r, base)
        assert "base.txt" in s.paths()
        f = _by(s)["base.txt"]
        assert f.status == STATUS_DELETED
        assert f.current_sha256 is None, "a deleted file has no current content — that is the fact"
        assert f.base_sha256, "the tombstone must record what the file WAS"

    def test_the_tombstone_is_the_files_real_pre_deletion_hash(self, repo):
        r, base = repo
        want = hashlib.sha256(b"base content\n").hexdigest()
        assert _by(resolve_review_subject(r, base))["base.txt"].base_sha256 == want

    def test_the_deleted_file_is_really_gone_from_the_worktree(self, repo):
        r, base = repo
        assert not (r / "base.txt").exists()
        assert "base.txt" in resolve_review_subject(r, base).paths()

    def test_a_deletion_serializes_with_a_null_current_hash(self, repo):
        r, base = repo
        rec = next(f for f in resolve_review_subject(r, base).to_json()["files"]
                   if f["path"] == "base.txt")
        assert rec["status"] == STATUS_DELETED
        assert rec["current_sha256"] is None
        assert rec["base_sha256"]


# --------------------------------------------------------------------------- rename


class TestARenameCarriesBothPaths:
    def test_a_rename_records_old_and_new(self, repo):
        r, base = repo
        f = _by(resolve_review_subject(r, base))["new.txt"]
        assert f.status == STATUS_RENAMED
        assert f.old_path == "old.txt"

    def test_a_rename_carries_both_hashes(self, repo):
        r, base = repo
        f = _by(resolve_review_subject(r, base))["new.txt"]
        want = hashlib.sha256(b"moved content\n").hexdigest()
        assert f.base_sha256 == want            # what it was, at the old path
        assert f.current_sha256 == want         # and what it is, at the new one

    def test_a_rename_with_an_edit_shows_different_hashes(self, tmp_path):
        r = tmp_path / "edited"
        r.mkdir()
        _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
        (r / "a.txt").write_text("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nbbbbbbbbbbbbbbbbbbbbbbbb\n")
        _sh(r, "git add -A && git commit -qm base")
        base = _rev(r)
        _sh(r, "git checkout -q -b f && git mv a.txt b.txt")
        (r / "b.txt").write_text("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nCHANGED\n")
        _sh(r, "git add -A && git commit -qm 'rename+edit'")
        f = _by(resolve_review_subject(r, base))["b.txt"]
        assert f.status == STATUS_RENAMED and f.old_path == "a.txt"
        assert f.base_sha256 != f.current_sha256


# --------------------------------------------------------------------------- the whole set


class TestTheFullDeltaIsTyped:
    def test_every_status_is_represented(self, repo):
        r, base = repo
        got = {f.path: f.status for f in resolve_review_subject(r, base).files}
        assert got == {"base.txt": STATUS_DELETED, "new.txt": STATUS_RENAMED,
                       "added.txt": STATUS_ADDED}

    def test_an_untouched_file_is_not_in_the_subject(self, repo):
        r, base = repo
        assert "keep.txt" not in resolve_review_subject(r, base).paths()

    def test_an_added_file_has_no_base_hash(self, repo):
        r, base = repo
        f = _by(resolve_review_subject(r, base))["added.txt"]
        assert f.status == STATUS_ADDED and f.base_sha256 is None and f.current_sha256

    def test_a_modified_file_carries_both_hashes(self, tmp_path):
        r = tmp_path / "mod"
        r.mkdir()
        _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
        (r / "m.txt").write_text("one\n")
        _sh(r, "git add -A && git commit -qm base")
        base = _rev(r)
        _sh(r, "git checkout -q -b f")
        (r / "m.txt").write_text("two\n")
        _sh(r, "git add -A && git commit -qm edit")
        f = _by(resolve_review_subject(r, base))["m.txt"]
        assert f.status == STATUS_MODIFIED
        assert f.base_sha256 == hashlib.sha256(b"one\n").hexdigest()
        assert f.current_sha256 == hashlib.sha256(b"two\n").hexdigest()


# --------------------------------------------------------------------------- NUL safety


class TestPathsSurviveHostileNames:
    def test_a_path_with_a_space_survives(self, tmp_path):
        r = tmp_path / "spacey"
        r.mkdir()
        _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
        (r / "a file.txt").write_text("x\n")
        _sh(r, "git add -A && git commit -qm base")
        base = _rev(r)
        _sh(r, "git checkout -q -b f && git rm -q 'a file.txt'")
        _sh(r, "git commit -qm 'delete spacey'")
        s = resolve_review_subject(r, base)
        assert s.paths() == ["a file.txt"]
        assert _by(s)["a file.txt"].status == STATUS_DELETED

    def test_a_path_with_a_quote_survives(self, tmp_path):
        r = tmp_path / "quoted"
        r.mkdir()
        _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
        name = 'we"ird.txt'
        (r / name).write_text("x\n")
        _sh(r, "git add -A && git commit -qm base")
        base = _rev(r)
        _sh(r, "git checkout -q -b f")
        (r / name).write_text("y\n")
        _sh(r, "git add -A && git commit -qm edit")
        # A human-formatted `git status` would hand this back wrapped in quotes and escaped.
        assert resolve_review_subject(r, base).paths() == [name]
