"""F8 (round 21) — root-of-trust schemas accept only exact supported versions."""
from __future__ import annotations

import pytest

from packages.orchestration.review_subject import (
    ContentProofError,
    decode_content_proof_v1,
    validate_content_proof_schema,
)


def _proof(**over):
    d = {"schema_version": "1.1.0", "base_commit": "a" * 40, "head_commit": "b" * 40,
         "file_hashes": {"src/app.py": "c" * 64}, "file_count": 1,
         "tombstones": {}, "tombstone_count": 0}
    d.update(over)
    return d


@pytest.mark.parametrize("bad", ["1.evil", "1.", "1", "1.2.0", "2.0.0", "1.1.0-rc1", ""])
def test_an_unsupported_content_proof_version_blocks(bad):
    with pytest.raises(ContentProofError):
        decode_content_proof_v1(_proof(schema_version=bad))


def test_the_exact_supported_version_passes():
    assert validate_content_proof_schema(_proof(schema_version="1.1.0")) == []
