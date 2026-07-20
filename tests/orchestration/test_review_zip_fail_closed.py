"""F10 (round 19) — a supplied-but-invalid ReviewSubject BLOCKS; it never becomes an empty subject.

build_review_zip.py used to catch every decode error and silently substitute an empty ReviewSubject,
so a corrupt/forged subject produced a context-only package that still reported success. The loader
now fails closed: only an ENTIRELY ABSENT `--subject-json` yields the legacy empty subject.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "_bz", Path(__file__).resolve().parents[2] / "scripts" / "build_review_zip.py")
_bz = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_bz)

from packages.orchestration.archive_plan import ArchivePlanError  # noqa: E402
from packages.orchestration.review_subject import ReviewSubjectError  # noqa: E402


def _valid_subject_json():
    return {
        "subject_v": 1, "base_commit": "", "head_commit": "", "base_is_ancestor": False,
        "commits": [], "files": [
            {"path": "a.py", "status": "added", "kind": "regular", "base_sha256": None,
             "current_sha256": "b" * 64, "current_mode": "100644"},
        ],
    }


class TestDecoderFailsClosed:
    def test_no_bytes_is_the_legacy_empty_subject(self):
        subj = _bz._decode_subject(None)
        assert subj.files == ()

    def test_invalid_json_blocks(self):
        with pytest.raises(ArchivePlanError):
            _bz._decode_subject(b"{not json")

    def test_a_schema_failing_subject_blocks(self):
        raw = json.dumps({"subject_v": 1, "EVIL": "/home/alice", "files": []}).encode()
        with pytest.raises((ReviewSubjectError, ArchivePlanError)):
            _bz._decode_subject(raw)

    def test_a_valid_subject_decodes(self):
        raw = json.dumps(_valid_subject_json()).encode()
        subj = _bz._decode_subject(raw)
        assert [f.path for f in subj.files] == ["a.py"]


class TestContentProofMandatory:
    def test_declared_subject_with_missing_proof_blocks(self):
        # F2/F3 (round 20/21): no fail-open empty authority when a Subject is declared.
        with pytest.raises(ArchivePlanError):
            _bz._decode_content_proof(None, subject_declared=True)

    def test_no_subject_no_proof_is_empty(self):
        assert _bz._decode_content_proof(None, subject_declared=False) is None

    def test_invalid_proof_json_blocks(self):
        with pytest.raises(ArchivePlanError):
            _bz._decode_content_proof(b"{not json", subject_declared=True)
