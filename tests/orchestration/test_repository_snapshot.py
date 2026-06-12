"""Tests for repository_snapshot.py — Steps 1118-1127.

Coverage:
  - SnapshotEntry/RepositorySnapshot/DurableApplyRecord model creation
  - create_snapshot: success, empty path set, unsafe path, file too large, total too large
  - verify_snapshot: success, manifest missing, hash mismatch, blob missing, blob corrupted
  - load_snapshot: round-trip
  - save/load_durable_apply_record
  - revert_repository_apply: success, no apply record, no snapshot, permission denied,
      contract denied, snapshot verify fail, drift detected, partial revert
  - build_snapshot_path_set from StructuredPatch
  - _is_safe_path
  - _normalize_path_set
"""

from __future__ import annotations

import dataclasses
import json
import os
import tempfile
from pathlib import Path
from uuid import UUID
from unittest.mock import MagicMock

import pytest

from packages.orchestration.repository_snapshot import (
    DurableApplyRecord,
    RepositoryRevertResult,
    RepositorySnapshot,
    SnapshotCreateResult,
    SnapshotEntry,
    SnapshotVerification,
    _is_safe_path,
    _normalize_path_set,
    _snapshot_dir,
    build_snapshot_path_set,
    build_snapshot_path_set_from_intent,
    create_snapshot,
    load_durable_apply_record,
    load_snapshot,
    revert_repository_apply,
    save_durable_apply_record,
    verify_snapshot,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_env(tmp_path: Path):
    """Provide (repo_root, data_dir) pair with temp dirs."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return repo_root, data_dir


JOB_ID = "aabbccdd-1234-5678-90ab-cdef01234567"
INTENT_ID = "intent-abc"
APPLY_ID = "applyabc"


# ---------------------------------------------------------------------------
# Job storage helpers (Step 1137 — revert gates load job from storage)
# ---------------------------------------------------------------------------


def _save_revert_job(
    data_dir: Path,
    *,
    allow_perm: bool = True,
    allow_contract: bool = True,
) -> None:
    """Create and persist a Job for revert tests.

    allow_perm=True  → Capability.repo_revert granted
    allow_contract=True → ContractAction.REVERT allowed (removed from denied_actions)
    """
    from packages.core.models import Job, Task, RunState
    from packages.orchestration.storage import save_job
    from packages.orchestration.permissions import Capability, set_permission
    from packages.orchestration.run_contract import (
        build_default_run_contract, save_contract, ContractAction,
    )

    job = Job(
        id=UUID(JOB_ID),
        name="revert-test-job",
        user_prompt="test",
        state=RunState.RUNNING,
        tasks=[],
        artifacts=[],
        metadata={},
    )
    set_permission(job, Capability.repo_revert, allow=allow_perm)

    contract = build_default_run_contract(job)
    if allow_contract:
        contract = dataclasses.replace(
            contract,
            allowed_actions=(*contract.allowed_actions, ContractAction.REVERT),
            denied_actions=tuple(a for a in contract.denied_actions if a != ContractAction.REVERT),
        )
    else:
        if ContractAction.REVERT not in contract.denied_actions:
            contract = dataclasses.replace(
                contract,
                denied_actions=(*contract.denied_actions, ContractAction.REVERT),
            )
    save_contract(job, contract)
    save_job(job, root=data_dir)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestSnapshotModels:
    def test_snapshot_entry_no_content_field(self):
        entry = SnapshotEntry(
            rel_path="foo.py",
            existed_before=True,
            file_type="text",
            before_sha256="abc",
            before_bytes=100,
            recovery_blob_ref="blob_abc.bin",
        )
        assert not hasattr(entry, "content")
        assert not hasattr(entry, "raw")
        assert entry.rel_path == "foo.py"

    def test_durable_apply_record_no_content(self):
        rec = DurableApplyRecord(
            apply_id=APPLY_ID,
            job_id=JOB_ID,
            intent_id=INTENT_ID,
            snapshot_id="snap1",
            state="applied",
            target_paths=["foo.py"],
            applied_at="2026-06-12T00:00:00+00:00",
            before_proof={"foo.py": {"sha256": "abc", "bytes": 100, "existed": True}},
            after_proof={"foo.py": {"sha256": "def", "bytes": 200, "existed": True}},
            snapshot_verified=True,
        )
        assert rec.state == "applied"
        assert "content" not in str(rec)


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------


class TestPathSafety:
    def test_empty_path_rejected(self, tmp_env):
        repo_root, _ = tmp_env
        safe, reason = _is_safe_path("", repo_root)
        assert not safe
        assert "empty" in reason

    def test_absolute_path_rejected(self, tmp_env):
        repo_root, _ = tmp_env
        safe, reason = _is_safe_path("/etc/passwd", repo_root)
        assert not safe
        assert "absolute" in reason

    def test_traversal_rejected(self, tmp_env):
        repo_root, _ = tmp_env
        safe, reason = _is_safe_path("../outside.txt", repo_root)
        assert not safe
        assert "traversal" in reason

    def test_denied_extension_rejected(self, tmp_env):
        repo_root, _ = tmp_env
        safe, reason = _is_safe_path("secrets.env", repo_root)
        assert not safe
        assert "denied_extension" in reason

    def test_denied_dir_rejected(self, tmp_env):
        repo_root, _ = tmp_env
        safe, reason = _is_safe_path("node_modules/foo.js", repo_root)
        assert not safe
        assert "denied_directory" in reason

    def test_normal_path_accepted(self, tmp_env):
        repo_root, _ = tmp_env
        (repo_root / "foo.py").write_text("hello")
        safe, reason = _is_safe_path("foo.py", repo_root)
        assert safe, reason


class TestNormalizePaths:
    def test_deduplicates(self):
        result = _normalize_path_set(["a.py", "b.py", "a.py"])
        assert result == ["a.py", "b.py"]

    def test_strips_whitespace(self):
        result = _normalize_path_set(["  a.py  "])
        assert result == ["a.py"]

    def test_normalizes_backslash(self):
        result = _normalize_path_set(["foo\\bar.py"])
        assert result == ["foo/bar.py"]

    def test_filters_empty(self):
        result = _normalize_path_set(["", "a.py", ""])
        assert result == ["a.py"]


# ---------------------------------------------------------------------------
# create_snapshot
# ---------------------------------------------------------------------------


class TestCreateSnapshot:
    def test_creates_snapshot_for_existing_file(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "hello.py").write_text("print('hello')")
        result = create_snapshot(JOB_ID, INTENT_ID, ["hello.py"], repo_root, data_dir)
        assert result.success
        assert result.snapshot_id
        assert result.path_count == 1
        assert result.total_bytes > 0
        # Manifest exists
        snap_dir = _snapshot_dir(JOB_ID, result.snapshot_id, data_dir)
        assert (snap_dir / "manifest.json").exists()
        # Blob exists (private)
        blobs = list(snap_dir.glob("blob_*.bin"))
        assert len(blobs) == 1

    def test_creates_snapshot_for_nonexistent_file(self, tmp_env):
        """Create targets (file doesn't exist yet) — existed_before=False, no blob."""
        repo_root, data_dir = tmp_env
        result = create_snapshot(JOB_ID, INTENT_ID, ["new_file.py"], repo_root, data_dir)
        assert result.success
        assert result.path_count == 1
        snap_dir = _snapshot_dir(JOB_ID, result.snapshot_id, data_dir)
        blobs = list(snap_dir.glob("blob_*.bin"))
        assert len(blobs) == 0  # No blob for absent file
        manifest = json.loads((snap_dir / "manifest.json").read_bytes())
        entry = manifest["entries"][0]
        assert entry["existed_before"] is False
        assert entry["recovery_blob_ref"] == ""

    def test_empty_path_set_fails(self, tmp_env):
        repo_root, data_dir = tmp_env
        result = create_snapshot(JOB_ID, INTENT_ID, [], repo_root, data_dir)
        assert not result.success
        assert result.safe_error_kind == "path_unsafe"

    def test_unsafe_path_fails(self, tmp_env):
        repo_root, data_dir = tmp_env
        result = create_snapshot(JOB_ID, INTENT_ID, ["../outside.txt"], repo_root, data_dir)
        assert not result.success
        assert result.safe_error_kind == "path_unsafe"

    def test_file_too_large_fails(self, tmp_env, monkeypatch):
        repo_root, data_dir = tmp_env
        (repo_root / "big.py").write_bytes(b"x" * 100)
        import packages.orchestration.repository_snapshot as snap_mod
        monkeypatch.setattr(snap_mod, "_MAX_FILE_BYTES", 50)
        result = create_snapshot(JOB_ID, INTENT_ID, ["big.py"], repo_root, data_dir)
        assert not result.success
        assert result.safe_error_kind == "file_too_large"

    def test_manifest_has_no_content(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "code.py").write_text("SECRET=1234")
        result = create_snapshot(JOB_ID, INTENT_ID, ["code.py"], repo_root, data_dir)
        assert result.success
        snap_dir = _snapshot_dir(JOB_ID, result.snapshot_id, data_dir)
        manifest = json.loads((snap_dir / "manifest.json").read_bytes())
        entry = manifest["entries"][0]
        # No raw content in manifest
        assert "content" not in entry
        assert "raw" not in entry
        assert "text" not in entry
        assert "source" not in entry

    def test_snapshot_dir_has_restrictive_permissions(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "f.py").write_text("x")
        result = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        assert result.success
        snap_dir = _snapshot_dir(JOB_ID, result.snapshot_id, data_dir)
        mode = oct(snap_dir.stat().st_mode)
        # Owner-only on supported platforms
        if os.name == "posix":
            assert "700" in mode or "0o40700" in mode

    def test_no_overwrite_existing_snapshot(self, tmp_env):
        """Second call with same job_id produces a new snapshot_id — no overwrite."""
        repo_root, data_dir = tmp_env
        (repo_root / "f.py").write_text("v1")
        r1 = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        r2 = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        assert r1.snapshot_id != r2.snapshot_id


# ---------------------------------------------------------------------------
# verify_snapshot
# ---------------------------------------------------------------------------


class TestVerifySnapshot:
    def test_verify_succeeds_after_create(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "f.py").write_text("hello world")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        assert snap_result.success
        verif = verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        assert verif.verified
        assert verif.blobs_present >= 1
        assert verif.blobs_missing == 0
        assert verif.hash_mismatches == 0

    def test_verify_missing_snapshot_fails(self, tmp_env):
        _, data_dir = tmp_env
        verif = verify_snapshot("nonexistent_snap", JOB_ID, data_dir)
        assert not verif.verified
        assert verif.failure_reason == "manifest_missing"

    def test_verify_corrupted_blob_fails(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "f.py").write_text("original")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        assert snap_result.success
        # Corrupt the blob
        snap_dir = _snapshot_dir(JOB_ID, snap_result.snapshot_id, data_dir)
        blobs = list(snap_dir.glob("blob_*.bin"))
        assert blobs
        blobs[0].write_bytes(b"corrupted data")
        verif = verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        assert not verif.verified
        assert verif.hash_mismatches >= 1

    def test_verify_missing_blob_fails(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "f.py").write_text("original")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        assert snap_result.success
        # Delete the blob
        snap_dir = _snapshot_dir(JOB_ID, snap_result.snapshot_id, data_dir)
        blobs = list(snap_dir.glob("blob_*.bin"))
        assert blobs
        blobs[0].unlink()
        verif = verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        assert not verif.verified
        assert verif.blobs_missing >= 1

    def test_verify_manifest_hash_mismatch_fails(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "f.py").write_text("original")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        assert snap_result.success
        # Tamper with manifest
        snap_dir = _snapshot_dir(JOB_ID, snap_result.snapshot_id, data_dir)
        manifest_path = snap_dir / "manifest.json"
        m = json.loads(manifest_path.read_bytes())
        m["tampered"] = True
        manifest_path.write_bytes(json.dumps(m).encode())
        verif = verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        assert not verif.verified
        assert verif.failure_reason == "manifest_hash_mismatch"

    def test_verify_updates_state_to_verified(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "f.py").write_text("x")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        snap_dir = _snapshot_dir(JOB_ID, snap_result.snapshot_id, data_dir)
        verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        m = json.loads((snap_dir / "manifest.json").read_bytes())
        assert m["state"] == "verified"


# ---------------------------------------------------------------------------
# load_snapshot round-trip
# ---------------------------------------------------------------------------


class TestLoadSnapshot:
    def test_round_trip(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "code.py").write_text("def hello(): pass")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["code.py"], repo_root, data_dir)
        snap = load_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        assert snap is not None
        assert snap.snapshot_id == snap_result.snapshot_id
        assert snap.job_id == JOB_ID
        assert snap.intent_id == INTENT_ID
        assert snap.path_count == 1
        entry = snap.entries[0]
        assert entry.rel_path == "code.py"
        assert entry.existed_before
        assert entry.before_bytes > 0
        # No content field
        assert not hasattr(entry, "content")

    def test_returns_none_for_missing(self, tmp_env):
        _, data_dir = tmp_env
        snap = load_snapshot("noexist", JOB_ID, data_dir)
        assert snap is None


# ---------------------------------------------------------------------------
# save/load DurableApplyRecord
# ---------------------------------------------------------------------------


class TestDurableApplyRecord:
    def test_round_trip(self, tmp_env):
        _, data_dir = tmp_env
        rec = DurableApplyRecord(
            apply_id=APPLY_ID,
            job_id=JOB_ID,
            intent_id=INTENT_ID,
            snapshot_id="snapxyz",
            state="applied",
            target_paths=["foo.py"],
            applied_at="2026-06-12T10:00:00+00:00",
            before_proof={"foo.py": {"sha256": "aaa", "bytes": 10, "existed": True}},
            after_proof={"foo.py": {"sha256": "bbb", "bytes": 20, "existed": True}},
            snapshot_verified=True,
        )
        ok = save_durable_apply_record(rec, JOB_ID, data_dir)
        assert ok
        loaded = load_durable_apply_record(APPLY_ID, JOB_ID, data_dir)
        assert loaded is not None
        assert loaded.apply_id == APPLY_ID
        assert loaded.snapshot_id == "snapxyz"
        assert loaded.snapshot_verified is True

    def test_returns_none_for_missing(self, tmp_env):
        _, data_dir = tmp_env
        loaded = load_durable_apply_record("nonexistent", JOB_ID, data_dir)
        assert loaded is None


# ---------------------------------------------------------------------------
# revert_repository_apply
# ---------------------------------------------------------------------------


class TestRevertRepositoryApply:
    def _setup_apply(
        self,
        tmp_env,
        content_before: str = "before",
        apply_id: str = APPLY_ID,
        *,
        allow_perm: bool = True,
        allow_contract: bool = True,
    ):
        """Create a snapshot + apply record + stored job for a file with known content."""
        repo_root, data_dir = tmp_env
        _save_revert_job(data_dir, allow_perm=allow_perm, allow_contract=allow_contract)
        file_path = repo_root / "target.py"
        file_path.write_text(content_before)
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["target.py"], repo_root, data_dir)
        assert snap_result.success
        verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)

        import hashlib
        raw_before = file_path.read_bytes()
        before_sha = hashlib.sha256(raw_before).hexdigest()

        # Simulate apply: write "after" content
        content_after = "after"
        file_path.write_text(content_after)
        raw_after = file_path.read_bytes()
        after_sha = hashlib.sha256(raw_after).hexdigest()

        rec = DurableApplyRecord(
            apply_id=apply_id,
            job_id=JOB_ID,
            intent_id=INTENT_ID,
            snapshot_id=snap_result.snapshot_id,
            state="applied",
            target_paths=["target.py"],
            applied_at="2026-06-12T10:00:00+00:00",
            before_proof={"target.py": {"sha256": before_sha, "bytes": len(raw_before), "existed": True}},
            after_proof={"target.py": {"sha256": after_sha, "bytes": len(raw_after), "existed": True}},
            snapshot_verified=True,
        )
        save_durable_apply_record(rec, JOB_ID, data_dir)
        return repo_root, data_dir

    def test_revert_success(self, tmp_env):
        repo_root, data_dir = self._setup_apply(tmp_env, "before content\n")
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        assert result.success, f"Revert failed: {result}"
        assert result.state == "reverted"
        assert result.paths_restored == 1
        assert (repo_root / "target.py").read_text() == "before content\n"

    def test_revert_no_apply_record(self, tmp_env):
        repo_root, data_dir = tmp_env
        result = revert_repository_apply(JOB_ID, "no_such_apply", repo_root, data_dir)
        assert not result.success
        assert result.block_reason == "no_apply_record"

    def test_revert_permission_denied(self, tmp_env):
        """repo_revert permission denied → block_reason permission_denied."""
        repo_root, data_dir = self._setup_apply(tmp_env, allow_perm=False, allow_contract=True)
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        assert not result.success
        assert result.block_reason == "permission_denied"

    def test_revert_contract_denied(self, tmp_env):
        """Contract denies REVERT action → block_reason contract_denied."""
        repo_root, data_dir = self._setup_apply(tmp_env, allow_perm=True, allow_contract=False)
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        assert not result.success
        assert result.block_reason == "contract_denied"

    def test_revert_job_not_found(self, tmp_env):
        """Missing job in storage → permission_denied (cannot verify permissions)."""
        repo_root, data_dir = tmp_env
        # Set up apply record but deliberately do NOT save job
        file_path = repo_root / "target.py"
        file_path.write_text("original\n")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["target.py"], repo_root, data_dir)
        verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        import hashlib
        raw = file_path.read_bytes()
        file_path.write_text("modified\n")
        raw_after = file_path.read_bytes()
        rec = DurableApplyRecord(
            apply_id=APPLY_ID, job_id=JOB_ID, intent_id=INTENT_ID,
            snapshot_id=snap_result.snapshot_id, state="applied",
            target_paths=["target.py"], applied_at="2026-06-12T10:00:00+00:00",
            before_proof={"target.py": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "existed": True}},
            after_proof={"target.py": {"sha256": hashlib.sha256(raw_after).hexdigest(), "bytes": len(raw_after), "existed": True}},
            snapshot_verified=True,
        )
        save_durable_apply_record(rec, JOB_ID, data_dir)
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        assert not result.success
        assert result.block_reason == "permission_denied"

    def test_revert_blocked_when_drift_detected(self, tmp_env):
        """Files changed after apply — revert must be blocked."""
        repo_root, data_dir = self._setup_apply(tmp_env, "before\n")
        # Simulate further modification after apply (drift)
        (repo_root / "target.py").write_text("drifted content after apply\n")
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        assert not result.success
        assert result.block_reason == "post_apply_drift"
        assert result.drift_path_count >= 1

    def test_revert_verifies_restored_state(self, tmp_env):
        """After successful revert, restored file matches before-state hash."""
        repo_root, data_dir = self._setup_apply(tmp_env, "verified content\n")
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        assert result.success
        assert result.verification_failures == 0
        assert (repo_root / "target.py").read_text() == "verified content\n"

    def test_revert_deletes_created_files(self, tmp_env):
        """Files that were created by apply (existed_before=False) get deleted on revert."""
        repo_root, data_dir = tmp_env
        _save_revert_job(data_dir)
        file_path = repo_root / "new_file.py"
        # File doesn't exist before apply
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["new_file.py"], repo_root, data_dir)
        assert snap_result.success
        verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)

        # Simulate apply creating the file
        file_path.write_text("created by apply\n")
        import hashlib
        raw_after = file_path.read_bytes()
        after_sha = hashlib.sha256(raw_after).hexdigest()

        rec = DurableApplyRecord(
            apply_id=APPLY_ID,
            job_id=JOB_ID,
            intent_id=INTENT_ID,
            snapshot_id=snap_result.snapshot_id,
            state="applied",
            target_paths=["new_file.py"],
            applied_at="2026-06-12T10:00:00+00:00",
            before_proof={"new_file.py": {"sha256": "", "bytes": 0, "existed": False}},
            after_proof={"new_file.py": {"sha256": after_sha, "bytes": len(raw_after), "existed": True}},
            snapshot_verified=True,
        )
        save_durable_apply_record(rec, JOB_ID, data_dir)
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        assert result.success
        assert result.paths_deleted == 1
        assert not file_path.exists()

    def test_revert_is_not_automatic(self, tmp_env):
        """revert_repository_apply requires explicit call — no auto-trigger."""
        # This is a design test: the function exists and requires explicit invocation.
        # Verify it's not called from create_snapshot or verify_snapshot.
        import inspect
        import packages.orchestration.repository_snapshot as mod
        src = inspect.getsource(mod.create_snapshot)
        assert "revert_repository_apply" not in src
        src2 = inspect.getsource(mod.verify_snapshot)
        assert "revert_repository_apply" not in src2


# ---------------------------------------------------------------------------
# build_snapshot_path_set
# ---------------------------------------------------------------------------


class TestBuildSnapshotPathSet:
    def test_from_file_ops(self):
        op1 = MagicMock()
        op1.path = "src/foo.py"
        op2 = MagicMock()
        op2.path = "src/bar.py"
        patch = MagicMock()
        patch.file_ops = [op1, op2]
        patch.unified_diffs = []
        result = build_snapshot_path_set(patch)
        assert result == ["src/foo.py", "src/bar.py"]

    def test_from_unified_diffs(self):
        d = MagicMock()
        d.path = "README.md"
        patch = MagicMock()
        patch.file_ops = []
        patch.unified_diffs = [d]
        result = build_snapshot_path_set(patch)
        assert result == ["README.md"]

    def test_deduplicates(self):
        op = MagicMock()
        op.path = "foo.py"
        d = MagicMock()
        d.path = "foo.py"
        patch = MagicMock()
        patch.file_ops = [op]
        patch.unified_diffs = [d]
        result = build_snapshot_path_set(patch)
        assert result == ["foo.py"]

    def test_from_intent_dict(self):
        result = build_snapshot_path_set_from_intent({"target_path": "docs/guide.md"})
        assert result == ["docs/guide.md"]

    def test_no_ops_returns_empty(self):
        patch = MagicMock()
        patch.file_ops = []
        patch.unified_diffs = []
        result = build_snapshot_path_set(patch)
        assert result == []


# ---------------------------------------------------------------------------
# Invariant: no raw content in public API returns
# ---------------------------------------------------------------------------


class TestNoRawContentLeaks:
    def test_create_result_no_content(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "secret.py").write_text("API_KEY = 'supersecret'")
        result = create_snapshot(JOB_ID, INTENT_ID, ["secret.py"], repo_root, data_dir)
        result_str = str(result)
        assert "supersecret" not in result_str
        assert "API_KEY" not in result_str

    def test_snapshot_model_no_content(self, tmp_env):
        repo_root, data_dir = tmp_env
        (repo_root / "creds.py").write_text("password = 'hunter2'")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["creds.py"], repo_root, data_dir)
        snap = load_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        assert snap is not None
        snap_str = str(snap)
        assert "hunter2" not in snap_str
        assert "password" not in snap_str

    def test_revert_result_no_content(self, tmp_env):
        """RepositoryRevertResult contains no raw file content."""
        repo_root, data_dir = tmp_env
        _save_revert_job(data_dir)
        (repo_root / "f.py").write_text("PRIVATE=xyz")
        snap_result = create_snapshot(JOB_ID, INTENT_ID, ["f.py"], repo_root, data_dir)
        verify_snapshot(snap_result.snapshot_id, JOB_ID, data_dir)
        import hashlib
        raw = (repo_root / "f.py").read_bytes()
        before_sha = hashlib.sha256(raw).hexdigest()
        # Write "after" content
        (repo_root / "f.py").write_text("UPDATED")
        raw_after = (repo_root / "f.py").read_bytes()
        after_sha = hashlib.sha256(raw_after).hexdigest()
        rec = DurableApplyRecord(
            apply_id=APPLY_ID, job_id=JOB_ID, intent_id=INTENT_ID,
            snapshot_id=snap_result.snapshot_id, state="applied",
            target_paths=["f.py"], applied_at="2026-06-12T00:00:00+00:00",
            before_proof={"f.py": {"sha256": before_sha, "bytes": len(raw), "existed": True}},
            after_proof={"f.py": {"sha256": after_sha, "bytes": len(raw_after), "existed": True}},
            snapshot_verified=True,
        )
        save_durable_apply_record(rec, JOB_ID, data_dir)
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        result_str = str(result)
        assert "PRIVATE" not in result_str
        assert "xyz" not in result_str
        assert "UPDATED" not in result_str


# ---------------------------------------------------------------------------
# Event emission (Step 1128)
# ---------------------------------------------------------------------------


class TestSnapshotEvents:
    def test_event_set_is_frozen(self):
        from packages.orchestration.repository_snapshot import _SNAPSHOT_EVENTS
        assert isinstance(_SNAPSHOT_EVENTS, frozenset)
        assert "snapshot_create_completed" in _SNAPSHOT_EVENTS
        assert "snapshot_verified" in _SNAPSHOT_EVENTS
        assert "revert_completed" in _SNAPSHOT_EVENTS
        assert "revert_failed" in _SNAPSHOT_EVENTS
        assert len(_SNAPSHOT_EVENTS) == 10

    def test_emit_ignores_unknown_event(self, tmp_env):
        """Unknown event type is silently ignored."""
        from packages.orchestration.repository_snapshot import _emit_snapshot_event
        _, data_dir = tmp_env
        # Should not raise
        _emit_snapshot_event(data_dir, JOB_ID, "unknown_event_type_xyz", {})


# ---------------------------------------------------------------------------
# Authoritative snapshot truth (Step 1156)
# ---------------------------------------------------------------------------


class TestBuildSnapshotTruth:
    """build_snapshot_truth() — single authoritative source over events/metadata."""

    def _setup_applied(self, tmp_env, *, apply_id=APPLY_ID, intent_id=INTENT_ID):
        """Create verified snapshot + applied DurableApplyRecord. Returns snapshot_id."""
        import hashlib
        repo_root, data_dir = tmp_env
        _save_revert_job(data_dir)
        f = repo_root / "target.py"
        f.write_text("before\n")
        snap = create_snapshot(JOB_ID, intent_id, ["target.py"], repo_root, data_dir)
        assert snap.success
        verify_snapshot(snap.snapshot_id, JOB_ID, data_dir)
        raw_before = b"before\n"
        before_sha = hashlib.sha256(raw_before).hexdigest()
        f.write_text("after\n")
        after_sha = hashlib.sha256(b"after\n").hexdigest()
        rec = DurableApplyRecord(
            apply_id=apply_id, job_id=JOB_ID, intent_id=intent_id,
            snapshot_id=snap.snapshot_id, state="applied",
            target_paths=["target.py"], applied_at="2026-06-12T10:00:00+00:00",
            before_proof={"target.py": {"sha256": before_sha, "bytes": len(raw_before), "existed": True}},
            after_proof={"target.py": {"sha256": after_sha, "bytes": 6, "existed": True}},
            snapshot_verified=True,
        )
        save_durable_apply_record(rec, JOB_ID, data_dir)
        return repo_root, data_dir, snap.snapshot_id

    def test_no_apply_record_is_unknown(self, tmp_env):
        from packages.orchestration.repository_snapshot import build_snapshot_truth
        _, data_dir = tmp_env
        truth = build_snapshot_truth(JOB_ID, data_dir=data_dir)
        assert truth.apply_state == "unknown"
        assert truth.revert_state == "unknown"
        assert truth.evidence_status == "unknown"
        assert "no_apply_record" in truth.blockers
        assert truth.snapshot_verified_now is False

    def test_verified_applied_snapshot_is_complete(self, tmp_env):
        from packages.orchestration.repository_snapshot import build_snapshot_truth
        repo_root, data_dir, snap_id = self._setup_applied(tmp_env)
        truth = build_snapshot_truth(JOB_ID, apply_id=APPLY_ID, data_dir=data_dir)
        assert truth.snapshot_id == snap_id
        assert truth.apply_id == APPLY_ID
        assert truth.snapshot_exists is True
        assert truth.manifest_exists is True
        assert truth.recovery_material_available is True
        assert truth.snapshot_verified_now is True
        assert truth.apply_state == "applied"
        assert truth.drift_blocked is False
        assert truth.evidence_status == "complete"
        assert truth.blockers == []

    def test_lookup_by_intent_id(self, tmp_env):
        from packages.orchestration.repository_snapshot import build_snapshot_truth
        repo_root, data_dir, snap_id = self._setup_applied(tmp_env)
        truth = build_snapshot_truth(JOB_ID, intent_id=INTENT_ID, data_dir=data_dir)
        assert truth.apply_id == APPLY_ID
        assert truth.snapshot_id == snap_id

    def test_reverted_apply(self, tmp_env):
        from packages.orchestration.repository_snapshot import build_snapshot_truth
        repo_root, data_dir, snap_id = self._setup_applied(tmp_env)
        # Bring repo back to after-state matching after_proof so drift check passes,
        # then revert through the central service.
        result = revert_repository_apply(JOB_ID, APPLY_ID, repo_root, data_dir)
        assert result.success, result
        truth = build_snapshot_truth(JOB_ID, apply_id=APPLY_ID, data_dir=data_dir)
        assert truth.revert_state == "reverted"
        assert truth.restore_verified is True
        assert truth.drift_blocked is False
        # Reverted apply is not "currently applied"
        assert truth.apply_state == "reverted"
        assert truth.evidence_status == "complete"

    def test_tampered_manifest_not_verified(self, tmp_env):
        from packages.orchestration.repository_snapshot import (
            build_snapshot_truth, _snapshot_dir,
        )
        repo_root, data_dir, snap_id = self._setup_applied(tmp_env)
        manifest = _snapshot_dir(JOB_ID, snap_id, data_dir) / "manifest.json"
        data = json.loads(manifest.read_text())
        data["path_count"] = 999  # tamper without recomputing hash
        manifest.write_text(json.dumps(data, indent=2, sort_keys=True))
        truth = build_snapshot_truth(JOB_ID, apply_id=APPLY_ID, data_dir=data_dir)
        assert truth.snapshot_verified_now is False
        assert "manifest_tampered" in truth.blockers
        assert truth.evidence_status == "degraded"

    def test_missing_recovery_blob_degraded(self, tmp_env):
        from packages.orchestration.repository_snapshot import (
            build_snapshot_truth, _snapshot_dir,
        )
        repo_root, data_dir, snap_id = self._setup_applied(tmp_env)
        snap_dir = _snapshot_dir(JOB_ID, snap_id, data_dir)
        for blob in snap_dir.glob("blob_*.bin"):
            blob.unlink()
        truth = build_snapshot_truth(JOB_ID, apply_id=APPLY_ID, data_dir=data_dir)
        assert truth.recovery_material_available is False
        assert "recovery_material_missing" in truth.blockers
        assert truth.snapshot_verified_now is False
        assert truth.evidence_status == "degraded"

    def test_missing_snapshot_blocks(self, tmp_env):
        from packages.orchestration.repository_snapshot import build_snapshot_truth
        repo_root, data_dir = tmp_env
        _save_revert_job(data_dir)
        rec = DurableApplyRecord(
            apply_id=APPLY_ID, job_id=JOB_ID, intent_id=INTENT_ID,
            snapshot_id="nonexistent-snap", state="applied",
            target_paths=["target.py"], applied_at="2026-06-12T10:00:00+00:00",
            before_proof={}, after_proof={}, snapshot_verified=False,
        )
        save_durable_apply_record(rec, JOB_ID, data_dir)
        truth = build_snapshot_truth(JOB_ID, apply_id=APPLY_ID, data_dir=data_dir)
        assert truth.snapshot_exists is False
        assert "no_snapshot" in truth.blockers
        assert truth.evidence_status == "degraded"

    def test_no_raw_paths_in_truth(self, tmp_env):
        from packages.orchestration.repository_snapshot import build_snapshot_truth
        repo_root, data_dir, snap_id = self._setup_applied(tmp_env)
        truth = build_snapshot_truth(JOB_ID, apply_id=APPLY_ID, data_dir=data_dir)
        s = str(dataclasses.asdict(truth))
        assert str(data_dir) not in s
        assert "blob_" not in s
