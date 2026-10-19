"""F1 (round 19) — authority is passed EXPLICITLY (the Content-Proof set), never inferred.

The ArchivePlan used to mark all 21 ReviewSubject files authoritative, re-authorizing the three
`.agent` operator-state files and disagreeing with the 18-file Content-Proof authority set. A
member is authoritative iff its path is in the explicit authority set, while development-only
`.agent` state is excluded regardless of subject membership.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.archive_plan import (
    DISP_EXCLUDE_SAFE_CONTEXT,
    SOURCE_REPOSITORY,
    build_archive_plan,
)
from packages.orchestration.review_subject import resolve_review_subject


def _sh(r, c):
    subprocess.run(c, shell=True, cwd=r, check=True, capture_output=True)


def _rev(r, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=r, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo base > base.txt && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature")
    return r, base


def _member(plan, path):
    return next((m for m in plan.all_members() if m.archive_path == path), None)


def _plan(r, subject, authority, context):
    return build_archive_plan(
        repo_root=r, subject=subject, repo_context_rel=context, evidence_root=None,
        evidence_rel=[], authoritative_paths=set(authority))


class TestAuthorityIsExplicit:
    def test_a_source_file_in_the_authority_set_is_authoritative(self, repo):
        r, base = repo
        (r / "src.py").write_text("x = 1\n")
        _sh(r, "git add -A && git commit -qm src")
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, {"src.py"}, ["src.py", "base.txt"])
        m = _member(plan, "src.py")
        assert m is not None and m.authoritative is True
        assert m.source_class == SOURCE_REPOSITORY

    def test_a_subject_file_not_in_the_authority_set_is_not_authoritative(self, repo):
        r, base = repo
        (r / "a.py").write_text("a\n")
        (r / "b.py").write_text("b\n")
        _sh(r, "git add -A && git commit -qm two")
        subject = resolve_review_subject(r, base)
        # Only a.py is authoritative; b.py is in the subject but NOT the authority set.
        plan = _plan(r, subject, {"a.py"}, ["a.py", "b.py", "base.txt"])
        assert _member(plan, "a.py").authoritative is True
        assert _member(plan, "b.py").authoritative is False

    def test_agent_operator_state_is_excluded_even_if_claimed_as_authority(self, repo):
        r, base = repo
        (r / ".agent").mkdir()
        (r / ".agent" / "plan.md").write_text("# plan\n")
        _sh(r, "git add -A && git commit -qm agent")
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, {".agent/plan.md"}, [".agent/plan.md", "base.txt"])

        assert _member(plan, ".agent/plan.md") is None
        excluded = {record.path: record.disposition for record in plan.excluded_records}
        assert excluded[".agent/plan.md"] == DISP_EXCLUDE_SAFE_CONTEXT

    def test_authority_set_hash_is_recorded(self, repo):
        r, base = repo
        (r / "s.py").write_text("s\n")
        _sh(r, "git add -A && git commit -qm s")
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject, {"s.py"}, ["s.py", "base.txt"])
        assert len(plan.authority_set_sha256) == 64
        assert len(plan.review_subject_sha256) == 64
        # Distinct authority sets produce distinct authority hashes.
        other = _plan(r, subject, set(), ["s.py", "base.txt"])
        assert other.authority_set_sha256 != plan.authority_set_sha256
