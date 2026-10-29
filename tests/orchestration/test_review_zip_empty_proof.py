"""F335 (operator order beweis): a job that stopped before any change landed leaves an empty
content proof; the review zip is built without it instead of failing on its schema."""

from packages.orchestration.content_proof_empty import content_proof_is_empty

EMPTY = {"schema_version": "1.1.0", "base_commit": "", "head_commit": "", "file_hashes": {},
         "file_count": 0, "tombstones": {}, "tombstone_count": 0}


def test_the_proof_of_a_job_without_a_landed_change_is_empty():
    assert content_proof_is_empty(EMPTY)


def test_a_proof_with_commits_or_files_is_never_empty():
    assert not content_proof_is_empty({**EMPTY, "base_commit": "a" * 40, "head_commit": "b" * 40})
    assert not content_proof_is_empty({**EMPTY, "file_hashes": {"x.py": "c" * 64}, "file_count": 1})
    assert not content_proof_is_empty({**EMPTY, "tombstones": {"y.py": "d" * 64}})
    assert not content_proof_is_empty(None)
