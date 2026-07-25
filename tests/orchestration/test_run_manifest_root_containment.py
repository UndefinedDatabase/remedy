"""F3 — every recovery/write helper CONTAINS the evidence directory inside its trusted root."""
from __future__ import annotations

import os

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MANIFEST_INDEX_FILENAME,
    ManifestError,
    write_run_manifest,
)
from packages.orchestration.run_manifest import (
    rebuild_manifest_mirror_and_index_from_canonical_episodes as _rebuild,
)


def _rebuildable_tree(ev):
    ev.mkdir(parents=True, exist_ok=True)
    from packages.orchestration.run_manifest import (
        COVERAGE_COMPLETE,
        CallCoverage,
        RunManifestV1,
        job_input_definition_sha256,
    )
    m = RunManifestV1(
        job_id="j", episode_id="ep1", created_at="2026-07-15T00:01:00+00:00",
        status="completed", episode_snapshot=T._wrap(episode_id="ep1"),
        job_input_sha256=job_input_definition_sha256(T._snap().job_input),
        calls=(), coverage=CallCoverage(status=COVERAGE_COMPLETE),
        call_expectation=T._zero_call_proof())
    write_run_manifest(ev, m, root=ev)
    (ev / MANIFEST_INDEX_FILENAME).unlink()
    return ev


class TestRootContainment:
    def test_evidence_dir_outside_root_is_refused(self, tmp_path):
        trusted = tmp_path / "trusted"; trusted.mkdir()
        outside = tmp_path / "outside"; outside.mkdir()
        with pytest.raises(ManifestError, match="outside the trusted root"):
            _rebuild(outside, root=trusted, job_id="j")
        assert os.listdir(outside) == [], "wrote outside the trusted root"

    def test_sibling_is_refused(self, tmp_path):
        trusted = tmp_path / "trusted"; trusted.mkdir()
        with pytest.raises(ManifestError):
            _rebuild(tmp_path / "sibling", root=trusted, job_id="j")
        assert not (tmp_path / "sibling").exists()

    def test_traversal_is_refused(self, tmp_path):
        trusted = tmp_path / "trusted"; trusted.mkdir()
        with pytest.raises(ManifestError):
            _rebuild(trusted / ".." / "escape", root=trusted, job_id="j")
        assert not (tmp_path / "escape").exists()

    def test_symlink_inside_root_pointing_outside_is_refused(self, tmp_path):
        trusted = tmp_path / "trusted"; trusted.mkdir()
        outside = tmp_path / "outside"; outside.mkdir()
        os.symlink(str(outside), str(trusted / "ev"))
        with pytest.raises(ManifestError):
            _rebuild(trusted / "ev", root=trusted, job_id="j")
        assert os.listdir(outside) == []

    def test_missing_root_is_refused(self, tmp_path):
        with pytest.raises(ManifestError, match="trusted evidence root"):
            _rebuild(tmp_path / "ev", root="", job_id="j")

    def test_safe_nested_evidence_dir_succeeds(self, tmp_path):
        trusted = tmp_path / "trusted"; trusted.mkdir()
        ev = _rebuildable_tree(trusted / "nested" / "ev")
        latest = _rebuild(ev, root=trusted, job_id="j")
        assert latest == "ep1"
        assert (ev / MANIFEST_INDEX_FILENAME).is_file()
