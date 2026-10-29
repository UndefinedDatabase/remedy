"""F335 (operator order beweis): the content proof of a job whose change never landed."""

from __future__ import annotations


def content_proof_is_empty(d: object) -> bool:
    """F335 (operator order beweis): the proof a job writes when no change of it ever landed (a job
    that stopped before its result: no commits, no file, no tombstone). It attests nothing, so the
    review zip is built without it and says what the evidence says, never fails on its schema."""
    return (isinstance(d, dict) and not d.get("base_commit") and not d.get("head_commit")
            and not d.get("file_hashes") and not d.get("tombstones"))
