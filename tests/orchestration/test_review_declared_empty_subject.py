"""F3 (round 21) — a DECLARED subject requires a strict Proof even with zero files."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location("_bz_des", REPO_ROOT / "scripts" / "build_review_zip.py")
_bz = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_bz)

from packages.orchestration.archive_plan import ArchivePlanError  # noqa: E402
from packages.orchestration.review_subject import ReviewSubjectV1  # noqa: E402


def _declared_empty_subject_bytes():
    # a subject with a declared base/head but ZERO files (a revert / net-zero change)
    return json.dumps({"subject_v": 1, "base_commit": "a" * 40, "head_commit": "b" * 40,
                       "base_is_ancestor": True, "commits": [], "files": []}).encode()


def test_declared_empty_subject_is_declared():
    subj = _bz._decode_subject(_declared_empty_subject_bytes())
    assert subj.files == () and subj.declared is True


def test_declared_empty_subject_without_proof_blocks():
    subj = _bz._decode_subject(_declared_empty_subject_bytes())
    assert subj.declared
    with pytest.raises(ArchivePlanError):
        _bz._decode_content_proof(None, subject_declared=subj.declared)


def test_declared_empty_subject_with_empty_strict_proof_passes():
    subj = _bz._decode_subject(_declared_empty_subject_bytes())
    proof_bytes = json.dumps({"schema_version": "1.1.0", "base_commit": "a" * 40,
                              "head_commit": "b" * 40, "file_hashes": {}, "file_count": 0,
                              "tombstones": {}, "tombstone_count": 0}).encode()
    cp = _bz._decode_content_proof(proof_bytes, subject_declared=subj.declared)
    assert cp is not None and cp.authority_paths() == set()


def test_an_undeclared_empty_subject_needs_no_proof():
    subj = ReviewSubjectV1()
    assert subj.declared is False
    assert _bz._decode_content_proof(None, subject_declared=subj.declared) is None
