"""F6/F7 — strict external schema for the manifest, snapshot, stop metadata and calls.

No synthetic legacy snapshot fallback (F6); every external field is strictly validated with no
silent normalization (F7).
"""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    ManifestError,
    decode_run_manifest_v1,
    validate_input_snapshot,
    validate_run_manifest,
)


# --------------------------------------------------------------------------- F6


class TestNoSyntheticLegacySnapshot:
    def test_manifest_without_episode_snapshot_is_rejected(self):
        d = T._mk(episode_id="ep1").to_json()
        d.pop("episode_snapshot")
        d["snapshot"] = {"remedy_git_sha": "a" * 40}     # a bare legacy snapshot
        with pytest.raises(ManifestError):
            decode_run_manifest_v1(d)


# --------------------------------------------------------------------------- F7 manifest


class TestManifestSchema:
    def _mk(self, **over):
        return dataclasses.replace(T._mk(episode_id="ep1"), **over)

    def test_naive_timestamp_is_rejected(self):
        m = self._mk(created_at="2026-07-15T00:00:00")     # no timezone
        assert any("UTC-aware" in p for p in validate_run_manifest(m))

    def test_bad_job_input_sha_is_rejected(self):
        assert any("job_input_sha256" in p
                   for p in validate_run_manifest(self._mk(job_input_sha256="nope")))

    def test_unsafe_stop_request_id_is_rejected(self):
        m = self._mk(status="stopped", stop_request_id="../../escape")
        assert any("stop_request_id" in p for p in validate_run_manifest(m))

    def test_stopped_requires_a_request_id(self):
        m = self._mk(status="stopped", stop_request_id="")
        assert any("stop_request_id" in p for p in validate_run_manifest(m))

    def test_non_stopped_must_not_carry_a_request_id(self):
        m = self._mk(status="completed", stop_request_id="abc123")
        assert any("stop_request_id" in p for p in validate_run_manifest(m))

    def test_malformed_artifact_sha_is_rejected(self):
        from packages.orchestration.call_identity import CallIdentity
        from packages.orchestration.run_manifest import FinalizedCall
        bad = FinalizedCall(
            identity=CallIdentity(job_id="j", task_id="T001", run_id="r", sequence=1,
                                  role="builder", round=1, kind="attempt", call_id="c1",
                                  episode_id="ep1"),
            fingerprint="abcd", prepared_input={}, fingerprint_source="provider_transport",
            ok=True, artifact="calls/0001-builder-round01-attempt.json",
            artifact_sha256="not-a-sha")
        m = self._mk(calls=(bad,))
        assert any("artifact_sha256" in p for p in validate_run_manifest(m))


# --------------------------------------------------------------------------- F7 snapshot


class TestInputSnapshotSchema:
    def test_clean_snapshot_validates(self):
        assert validate_input_snapshot(T._snap()) == []

    def test_bad_worktree_status_is_rejected(self):
        s = dataclasses.replace(T._snap(), remedy_worktree={
            "status": "weird", "digest": "aa" * 32, "problems": [], "dirty": False})
        assert any("status" in p for p in validate_input_snapshot(s))

    def test_ok_worktree_with_null_dirty_is_rejected(self):
        s = dataclasses.replace(T._snap(), remedy_worktree={
            "status": "ok", "digest": "aa" * 32, "problems": []})   # no dirty
        assert any("dirty" in p for p in validate_input_snapshot(s))

    def test_duplicate_config_keys_are_rejected(self):
        s = dataclasses.replace(T._snap(), config=[
            {"key": "k", "value": "1", "source": "default"},
            {"key": "k", "value": "2", "source": "default"}])
        assert any("config" in p for p in validate_input_snapshot(s))

    def test_non_remedy_env_key_is_rejected(self):
        s = dataclasses.replace(T._snap(), environment=[{"key": "HOME", "value": "/x"}])
        assert any("non-REMEDY_" in p for p in validate_input_snapshot(s))

    def test_bad_job_file_sha_is_rejected(self):
        s = dataclasses.replace(T._snap(), job_file_sha256="short")
        assert any("job_file_sha256" in p for p in validate_input_snapshot(s))
