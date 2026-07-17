"""F6 (round 20) — the manifest is read through the anchored no-follow reader, and it is packaged
from in-memory bytes, so a manifest path that is a symlink to an external secret is refused.
"""
from __future__ import annotations

import os

import pytest

from packages.orchestration.review_zip import ReviewZipError, _read_manifest_no_follow


def test_a_symlinked_manifest_to_outside_bytes_blocks(tmp_path):
    secret = tmp_path / "SECRET"
    secret.write_text("SUPERSECRET-external")
    manifest = tmp_path / ".review_zip_manifest.json"
    os.symlink(str(secret), str(manifest))
    with pytest.raises(ReviewZipError):
        _read_manifest_no_follow(str(manifest))


def test_a_relative_symlink_manifest_blocks(tmp_path):
    (tmp_path / "real.json").write_text('{"x": 1}')
    manifest = tmp_path / ".review_zip_manifest.json"
    os.symlink("real.json", str(manifest))
    with pytest.raises(ReviewZipError):
        _read_manifest_no_follow(str(manifest))


def test_a_regular_manifest_reads_its_exact_bytes(tmp_path):
    manifest = tmp_path / ".review_zip_manifest.json"
    manifest.write_bytes(b'{"package_status": "READY_FOR_REVIEW"}')
    assert _read_manifest_no_follow(str(manifest)) == b'{"package_status": "READY_FOR_REVIEW"}'
