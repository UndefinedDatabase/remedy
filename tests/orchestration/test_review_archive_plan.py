"""F1 (round 18) — ONE typed ArchivePlanV1 drives the package.

The package used to be built from the typed ReviewSubject on one side and an independent
`find -type f` list on the other. `find -type f` skips symlinks, so a safe authoritative symlink
was absent from the archive while the Content Proof and the ZIP verification both said PASS. The
ArchivePlan gives every ReviewSubject file exactly one disposition, so the subject and the archive
cannot disagree.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.archive_plan import (
    MEMBER_REGULAR,
    MEMBER_SYMLINK,
    MODE_EXECUTABLE,
    MODE_REGULAR,
    build_archive_plan,
)
from packages.orchestration.review_subject import resolve_review_subject


def _sh(r, c):
    subprocess.run(c, shell=True, cwd=r, check=True, capture_output=True)


def _rev(r, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=r, capture_output=True,
                          text=True).stdout.strip()


def _plan(repo, subject, context, *, authority=None):
    # Round 19: authority is passed EXPLICITLY. Default to every subject path (the pre-round-19
    # disposition tests only care about member/tombstone/block, not the authoritative flag).
    if authority is None:
        authority = {f.path for f in subject.files}
    return build_archive_plan(
        repo_root=repo, subject=subject, repo_context_rel=context,
        evidence_root=None, evidence_rel=[], authoritative_paths=authority)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo base > base.txt && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature")
    return r, base


def _m(plan, path):
    return next((m for m in plan.all_members() if m.archive_path == path), None)


# --------------------------------------------------------------------------- symlinks


class TestTheAuthoritativeSymlinkIsPlanned:
    def test_the_reproduced_case_a_dirty_symlink_is_a_member(self, repo):
        """`find -type f` would have skipped it; the plan carries it from the subject."""
        r, base = repo
        (r / "target.txt").write_text("t")
        os.symlink("target.txt", str(r / "link.txt"))
        subject = resolve_review_subject(r, base)
        # the bundle context (as `find -type f` would give it) does NOT contain link.txt
        context = ["target.txt", "base.txt"]
        plan = _plan(r, subject, context)
        m = _m(plan, "link.txt")
        assert m is not None and m.kind == MEMBER_SYMLINK
        assert m.authoritative is True
        assert m.expected_link_target == "target.txt"

    def test_a_committed_symlink_is_a_member(self, repo):
        r, base = repo
        (r / "target.txt").write_text("t")
        os.symlink("target.txt", str(r / "link.txt"))
        _sh(r, "git add -A && git commit -qm 'add link'")
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, ["target.txt", "base.txt"])
        m = _m(plan, "link.txt")
        assert m is not None and m.kind == MEMBER_SYMLINK and m.authoritative

    def test_an_external_authoritative_symlink_blocks(self, repo, tmp_path):
        r, base = repo
        os.symlink("/etc/passwd", str(r / "evil.txt"))
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, ["base.txt"])
        assert plan.blocked
        assert any("outside the repository" in b.reason for b in plan.blocked_records)


# --------------------------------------------------------------------------- dispositions


class TestEveryFileGetsOneDisposition:
    def test_every_nondeleted_subject_path_has_one_member(self, repo):
        r, base = repo
        (r / "a.py").write_text("a")
        (r / "b.py").write_text("b")
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, ["a.py", "b.py", "base.txt"])
        for f in subject.files:
            if f.status != "deleted":
                assert _m(plan, f.path) is not None, f.path

    def test_a_deleted_path_is_a_tombstone_and_no_member(self, repo):
        r, base = repo
        (r / "base.txt").unlink()
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, [])
        assert any(t.path == "base.txt" for t in plan.tombstones)
        assert _m(plan, "base.txt") is None

    def test_a_policy_excluded_changed_path_blocks(self, repo):
        """A changed `.env` is BLOCK_SENSITIVE by the bundle policy (round 19), never packaged."""
        r, base = repo
        (r / ".env").write_text("SECRET=1")
        _sh(r, "git add -A && git commit -qm env")
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, [])
        assert plan.blocked
        assert any(b.path == ".env" and "sensitive" in b.reason for b in plan.blocked_records)

    def test_no_subject_path_is_absent_from_the_plan(self, repo):
        r, base = repo
        (r / "a.py").write_text("a")
        os.symlink("a.py", str(r / "l.py"))
        subject = resolve_review_subject(r, base)
        planned = {m.archive_path for m in _plan(r, subject, ["a.py", "base.txt"]).all_members()}
        planned |= {t.path for t in _plan(r, subject, ["a.py", "base.txt"]).tombstones}
        for f in subject.files:
            assert f.path in planned, f.path


# --------------------------------------------------------------------------- modes


class TestPlannedModes:
    def test_an_executable_file_plans_0755(self, repo):
        r, base = repo
        _sh(r, "echo '#!/bin/sh' > tool.sh && chmod +x tool.sh && git add -A "
               "&& git commit -qm tool")
        subject = resolve_review_subject(r, base)
        m = _m(_plan(r, subject, ["tool.sh", "base.txt"]), "tool.sh")
        assert m.kind == MEMBER_REGULAR and m.mode == MODE_EXECUTABLE

    def test_a_plain_file_plans_0644(self, repo):
        r, base = repo
        _sh(r, "echo x > plain.txt && git add -A && git commit -qm plain")
        subject = resolve_review_subject(r, base)
        m = _m(_plan(r, subject, ["plain.txt", "base.txt"]), "plain.txt")
        assert m.kind == MEMBER_REGULAR and m.mode == MODE_REGULAR


# --------------------------------------------------------------------------- blocked kinds


class TestUnpackageableKindsBlock:
    def test_a_special_file_blocks(self, repo):
        r, base = repo
        os.mkfifo(str(r / "base.txt")) if False else None
        # a tracked file replaced by a fifo (the reachable special-file case)
        (r / "base.txt").unlink()
        os.mkfifo(str(r / "base.txt"))
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, [])
        assert plan.blocked
