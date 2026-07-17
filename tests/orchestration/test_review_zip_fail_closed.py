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


class TestLoaderFailsClosed:
    def test_no_path_is_the_legacy_empty_subject(self):
        subj = _bz._load_subject("")
        assert subj.files == ()

    def test_a_supplied_but_missing_path_blocks(self, tmp_path):
        with pytest.raises(ArchivePlanError):
            _bz._load_subject(str(tmp_path / "nope.json"))

    def test_invalid_json_blocks(self, tmp_path):
        p = tmp_path / "s.json"
        p.write_text("{not json")
        with pytest.raises(ArchivePlanError):
            _bz._load_subject(str(p))

    def test_a_schema_failing_subject_blocks(self, tmp_path):
        p = tmp_path / "s.json"
        # unknown field + a forged path => strict schema rejects, never an empty downgrade
        p.write_text(json.dumps({"subject_v": 1, "EVIL": "/home/alice", "files": []}))
        with pytest.raises((ReviewSubjectError, ArchivePlanError)):
            _bz._load_subject(str(p))

    def test_a_valid_subject_decodes(self, tmp_path):
        p = tmp_path / "s.json"
        p.write_text(json.dumps(_valid_subject_json()))
        subj = _bz._load_subject(str(p))
        assert [f.path for f in subj.files] == ["a.py"]


class TestAuthoritySet:
    def test_authority_is_file_hashes_plus_tombstones(self, tmp_path):
        p = tmp_path / "cp.json"
        p.write_text(json.dumps({"file_hashes": {"a.py": "x", "b.py": "y"},
                                 "tombstones": {"gone.py": "z"}}))
        assert _bz._authority_set(str(p)) == {"a.py", "b.py", "gone.py"}

    def test_absent_content_proof_is_empty_authority(self, tmp_path):
        assert _bz._authority_set(str(tmp_path / "missing.json")) == set()
