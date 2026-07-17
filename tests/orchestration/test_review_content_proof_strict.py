"""F2 (round 20) — the strict ContentProofV1 decoder is the ONE authority source.

A missing/invalid/schema-failing proof BLOCKS; the authority set is never derived from an
un-validated proof, and it can never silently become empty when a Subject is declared.
"""
from __future__ import annotations

import pytest

from packages.orchestration.review_subject import (
    ContentProofError,
    decode_content_proof_v1,
    validate_content_proof_schema,
)


def _proof(**over):
    d = {
        "schema_version": "1.1.0",
        "base_commit": "a" * 40, "head_commit": "b" * 40,
        "file_hashes": {"src/app.py": "c" * 64, "tests/test_app.py": "d" * 64},
        "file_count": 2,
        "tombstones": {"old.py": "e" * 64},
        "tombstone_count": 1,
    }
    d.update(over)
    return d


class TestValidProof:
    def test_a_clean_proof_decodes(self):
        cp = decode_content_proof_v1(_proof())
        assert cp.authority_paths() == {"src/app.py", "tests/test_app.py", "old.py"}
        assert cp.base_commit == "a" * 40


class TestStrictRejection:
    def test_unknown_field_blocks(self):
        assert any("unknown field" in p for p in validate_content_proof_schema(_proof(EVIL="x")))

    def test_missing_field_blocks(self):
        d = _proof()
        del d["tombstone_count"]
        assert any("missing required field" in p for p in validate_content_proof_schema(d))

    def test_bad_schema_version_blocks(self):
        with pytest.raises(ContentProofError):
            decode_content_proof_v1(_proof(schema_version="9.9"))

    def test_non_hex_hash_blocks(self):
        with pytest.raises(ContentProofError):
            decode_content_proof_v1(_proof(file_hashes={"a.py": "nothex"}, file_count=1))

    def test_file_count_mismatch_blocks(self):
        with pytest.raises(ContentProofError):
            decode_content_proof_v1(_proof(file_count=99))

    def test_tombstone_count_mismatch_blocks(self):
        with pytest.raises(ContentProofError):
            decode_content_proof_v1(_proof(tombstone_count=99))

    def test_path_in_both_maps_blocks(self):
        d = _proof(file_hashes={"dup.py": "c" * 64}, file_count=1,
                   tombstones={"dup.py": "e" * 64}, tombstone_count=1)
        assert any("both file_hashes and tombstones" in p
                   for p in validate_content_proof_schema(d))

    def test_agent_operator_state_path_blocks(self):
        d = _proof(file_hashes={".agent/plan.md": "c" * 64}, file_count=1)
        assert any("non-authoritative path" in p for p in validate_content_proof_schema(d))

    def test_unsafe_path_blocks(self):
        d = _proof(file_hashes={"../escape.py": "c" * 64}, file_count=1)
        assert any("not a safe relative path" in p for p in validate_content_proof_schema(d))

    def test_a_sensitive_path_blocks(self):
        d = _proof(file_hashes={"secrets/.env": "c" * 64}, file_count=1)
        assert any("non-authoritative path" in p for p in validate_content_proof_schema(d))
