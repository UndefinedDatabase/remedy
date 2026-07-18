"""F2 (round 21) — the plan's review_subject_sha256 is the RAW packaged bytes' sha, passed in
explicitly, never a hash of a reserialized projection."""
from __future__ import annotations

import hashlib

from packages.orchestration.archive_plan import build_archive_plan
from packages.orchestration.review_subject import ReviewSubjectV1


def test_plan_uses_the_raw_subject_sha_when_supplied():
    raw = b'{"subject_v": 1, "files": []}\n'
    raw_sha = hashlib.sha256(raw).hexdigest()
    plan = build_archive_plan(
        repo_root=".", subject=ReviewSubjectV1(), repo_context_rel=[], evidence_root=None,
        evidence_rel=[], authoritative_paths=set(), review_subject_raw_sha256=raw_sha)
    assert plan.review_subject_sha256 == raw_sha


def test_a_reserialized_hash_is_not_used_when_a_raw_sha_is_given():
    # A reserialized subject.to_json() hash differs from the raw file bytes; the raw one must win.
    import json
    reserialized = hashlib.sha256(
        json.dumps(ReviewSubjectV1().to_json(), sort_keys=True).encode()).hexdigest()
    raw_sha = "a" * 64
    plan = build_archive_plan(
        repo_root=".", subject=ReviewSubjectV1(), repo_context_rel=[], evidence_root=None,
        evidence_rel=[], authoritative_paths=set(), review_subject_raw_sha256=raw_sha)
    assert plan.review_subject_sha256 == raw_sha != reserialized
