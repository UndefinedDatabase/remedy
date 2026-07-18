"""F5 (round 21) — the ArchivePlan owns ONE disposition per path; a special file cannot silently
disappear."""
from __future__ import annotations

import os

import pytest

from packages.orchestration.archive_plan import (
    DISP_EXCLUDE_SAFE_CONTEXT,
    build_archive_plan,
)
from packages.orchestration.review_subject import ReviewSubjectV1


def test_a_fifo_context_path_gets_an_explicit_blocked_record(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "keep.py").write_text("x = 1\n")
    os.mkfifo(str(repo / "pipe"))
    plan = build_archive_plan(
        repo_root=repo, subject=ReviewSubjectV1(), repo_context_rel=["pipe", "keep.py"],
        evidence_root=None, evidence_rel=[], authoritative_paths=set())
    assert plan.blocked
    assert any(b.path == "pipe" and "BLOCK_UNSUPPORTED" in b.reason for b in plan.blocked_records)
    # it did NOT silently disappear
    assert not any(m.archive_path == "pipe" for m in plan.all_members())


def test_an_unchanged_sensitive_context_is_excluded_not_blocked(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "app.log").write_text("log")
    (repo / "keep.py").write_text("x = 1\n")
    plan = build_archive_plan(
        repo_root=repo, subject=ReviewSubjectV1(), repo_context_rel=["app.log", "keep.py"],
        evidence_root=None, evidence_rel=[], authoritative_paths=set())
    assert not plan.blocked
    assert any(e.path == "app.log" and e.disposition == DISP_EXCLUDE_SAFE_CONTEXT
               for e in plan.excluded_records)


def test_every_context_path_has_exactly_one_disposition(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "a.py").write_text("a")
    (repo / "s.log").write_text("s")
    os.mkfifo(str(repo / "fifo"))
    plan = build_archive_plan(
        repo_root=repo, subject=ReviewSubjectV1(), repo_context_rel=["a.py", "s.log", "fifo"],
        evidence_root=None, evidence_rel=[], authoritative_paths=set())
    dispositions = {}
    for m in plan.all_members():
        dispositions[m.archive_path] = "member"
    for e in plan.excluded_records:
        dispositions[e.path] = "excluded"
    for b in plan.blocked_records:
        dispositions[b.path] = "blocked"
    assert dispositions == {"a.py": "member", "s.log": "excluded", "fifo": "blocked"}
