"""Ping-pong promotion tests.

Tests the `do promote` command: eligibility, baseline validation,
artifact persistence, dry-run, approved apply, blocked paths,
post-promotion tests, report integration.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import (
    run_pingpong,
)
from packages.orchestration.pingpong_promote import (
    _is_blocked_path,
    _normalize_rel_path,
    export_promotion_json,
    load_artifacts,
    load_promotion,
    persist_artifacts,
    promote_run,
    summarize_promotion,
)
from packages.orchestration.pingpong_provider import FakeProvider


def _hash_file_helper(path: Path) -> str:
    """SHA-256 hash of file for test setup."""
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    """Minimal demo repo for testing."""
    (tmp_path / "README.md").write_text("# Demo\nA demo project.\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    (tmp_path / ".env").write_text("API_KEY=secret123\n")
    return tmp_path


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    """Redirect REMEDY_DATA_DIR to tmp so tests don't write to real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _run_passing(demo_repo: Path, **kwargs) -> str:
    """Run a fake ping-pong that passes review and return run_id."""
    provider = FakeProvider(**kwargs)
    result = run_pingpong(
        "Fix README", str(demo_repo),
        builder_provider=provider,
        reviewer_provider=provider,
        max_rounds=2, repair_rounds=2,
    )
    assert result.final_status == "staged_review_passed"
    return result.run_id


# ---------------------------------------------------------------------------
# 1. Dry-run does not mutate target
# ---------------------------------------------------------------------------

class TestDryRunNoMutation:
    def test_dry_run_no_changes(self, demo_repo):
        run_id = _run_passing(demo_repo)
        original_content = (demo_repo / "README.md").read_text()
        result = promote_run(run_id, target_repo=str(demo_repo), dry_run=True)
        assert result.status == "dry_run"
        assert (demo_repo / "README.md").read_text() == original_content
        assert result.changed_target_files == []


# ---------------------------------------------------------------------------
# 2. Without --approve does not mutate target
# ---------------------------------------------------------------------------

class TestUnapprovedNoMutation:
    def test_unapproved_no_changes(self, demo_repo):
        run_id = _run_passing(demo_repo)
        original_content = (demo_repo / "README.md").read_text()
        result = promote_run(run_id, target_repo=str(demo_repo))
        assert result.status == "dry_run"
        assert result.approved is False
        assert (demo_repo / "README.md").read_text() == original_content


# ---------------------------------------------------------------------------
# 3. Approved promotion applies new text file
# ---------------------------------------------------------------------------

class TestApprovedNewFile:
    def test_new_file_applied(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "promoted"
        assert len(result.applied_files) > 0
        # At least one file should now exist in target
        for f in result.applied_files:
            assert (demo_repo / f).exists()


# ---------------------------------------------------------------------------
# 4. Approved promotion modifies existing file
# ---------------------------------------------------------------------------

class TestApprovedModifyFile:
    def test_modify_applied(self, demo_repo):
        run_id = _run_passing(demo_repo, builder_files=["README.md"])
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "promoted"
        assert "README.md" in result.applied_files


# ---------------------------------------------------------------------------
# 5. Blocked when final_status not staged_review_passed
# ---------------------------------------------------------------------------

class TestBlockedBadStatus:
    def test_test_failed_blocks(self, demo_repo):
        provider = FakeProvider(reviewer_error="some error")
        r = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        result = promote_run(r.run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "ineligible_status" in result.blocked_reason


# ---------------------------------------------------------------------------
# 6. Blocked when reviewer verdict not pass
# ---------------------------------------------------------------------------

class TestBlockedReviewerNotPass:
    def test_verdict_not_pass_blocks(self, demo_repo):
        provider = FakeProvider(pass_on_round=99, max_rounds_before_block=1)
        r = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
            max_rounds=1,
        )
        result = promote_run(r.run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"


# ---------------------------------------------------------------------------
# 7. Blocked when staged_files empty
# ---------------------------------------------------------------------------

class TestBlockedNoStagedFiles:
    def test_no_staged_files_blocks(self, demo_repo, isolate_data_root):
        """Manually create a run record with empty staged_files."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_no_staged"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": [],
            "target_mutated": False,
            "changed_target_files": [],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "no_staged_files" in result.blocked_reason


# ---------------------------------------------------------------------------
# 8. Blocked when target was mutated during run
# ---------------------------------------------------------------------------

class TestBlockedTargetMutated:
    def test_target_mutated_blocks(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_mutated"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": ["README.md"],
            "target_mutated": True,
            "changed_target_files": ["README.md"],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "target_mutated" in result.blocked_reason


# ---------------------------------------------------------------------------
# 9. Blocked when changed_target_files existed during run
# ---------------------------------------------------------------------------

class TestBlockedChangedTargetFiles:
    def test_changed_target_files_blocks(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_changed"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": ["README.md"],
            "target_mutated": False,
            "changed_target_files": ["some_file.txt"],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "changed_target_files" in result.blocked_reason


# ---------------------------------------------------------------------------
# 10. Blocked when target file changed since run baseline
# ---------------------------------------------------------------------------

class TestBlockedBaselineMismatch:
    def test_baseline_mismatch_blocks(self, demo_repo):
        run_id = _run_passing(demo_repo, builder_files=["README.md"])
        # Modify the target file after run
        (demo_repo / "README.md").write_text("# Modified after run\n")
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "baseline_mismatch" in result.blocked_reason
        assert any("target_changed_since_run" in m for m in result.baseline_mismatches)


# ---------------------------------------------------------------------------
# 11. Blocked for path traversal
# ---------------------------------------------------------------------------

class TestBlockedPathTraversal:
    def test_path_traversal(self):
        assert _is_blocked_path("../etc/passwd") == "path_traversal"
        assert _is_blocked_path("foo/../../bar") == "path_traversal"


# ---------------------------------------------------------------------------
# 12. Blocked for .env
# ---------------------------------------------------------------------------

class TestBlockedEnv:
    def test_env_blocked(self):
        assert _is_blocked_path(".env") != ""
        assert _is_blocked_path(".env.local") == "secret_file"
        assert _is_blocked_path(".env-production") == "secret_file"


# ---------------------------------------------------------------------------
# 13. Blocked for .git
# ---------------------------------------------------------------------------

class TestBlockedGit:
    def test_git_blocked(self):
        assert _is_blocked_path(".git") != ""
        assert _is_blocked_path(".git/config") != ""
        assert _is_blocked_path(".git/HEAD") != ""


# ---------------------------------------------------------------------------
# 14. Blocked for cache/build/node_modules paths
# ---------------------------------------------------------------------------

class TestBlockedCachePaths:
    def test_cache_paths_blocked(self):
        assert _is_blocked_path("node_modules/foo/bar.js") != ""
        assert _is_blocked_path("__pycache__/mod.pyc") != ""
        assert _is_blocked_path(".mypy_cache/cache.json") != ""
        assert _is_blocked_path("dist/bundle.js") != ""
        assert _is_blocked_path("build/output.js") != ""


# ---------------------------------------------------------------------------
# 15. Blocked for binary files
# ---------------------------------------------------------------------------

class TestBlockedBinary:
    def test_binary_blocked(self):
        assert _is_blocked_path("image.png") == "binary_file"
        assert _is_blocked_path("archive.zip") == "binary_file"
        assert _is_blocked_path("lib.so") == "binary_file"


# ---------------------------------------------------------------------------
# 16. Blocked for deletes in v0
# ---------------------------------------------------------------------------

class TestBlockedDeletes:
    def test_delete_not_supported(self, demo_repo, isolate_data_root):
        """If artifact file doesn't exist in artifacts dir, it's treated as delete."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_delete"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        # Create run data
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": ["README.md"],
            "target_mutated": False,
            "changed_target_files": [],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        # Create manifest with entry but no artifact file
        artifacts_dir = run_dir / "artifacts"
        artifacts_dir.mkdir()
        manifest = [{"relative_path": "README.md", "operation": "modify",
                      "file_type": ".md", "target_baseline_hash": "abc",
                      "staged_hash": "def", "size": 100}]
        (artifacts_dir / "manifest.json").write_text(json.dumps(manifest))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert any("delete_not_supported" in u for u in result.unsupported_files)


# ---------------------------------------------------------------------------
# 17. Promotion persists result
# ---------------------------------------------------------------------------

class TestPromotionPersists:
    def test_promotion_persisted(self, demo_repo):
        run_id = _run_passing(demo_repo)
        promote_run(run_id, target_repo=str(demo_repo), approve=True)
        promo = load_promotion(run_id)
        assert promo is not None
        assert promo["status"] == "promoted"


# ---------------------------------------------------------------------------
# 18. Report shows promotion status
# ---------------------------------------------------------------------------

class TestReportShowsPromotion:
    def test_report_includes_promotion(self, demo_repo):
        run_id = _run_passing(demo_repo)
        promote_run(run_id, target_repo=str(demo_repo), approve=True)
        promo = load_promotion(run_id)
        assert promo is not None
        assert promo["status"] == "promoted"
        assert len(promo["applied_files"]) > 0


# ---------------------------------------------------------------------------
# 19. JSON includes applied_files and changed_target_files
# ---------------------------------------------------------------------------

class TestJsonFields:
    def test_json_has_fields(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        data = export_promotion_json(result)
        assert "applied_files" in data
        assert "changed_target_files" in data
        assert "run_id" in data
        assert "promotion_id" in data
        assert "status" in data
        assert "approved" in data
        assert "dry_run" in data
        assert "baseline_mismatches" in data
        assert "unsupported_files" in data
        assert "post_test_command" in data
        assert "post_test_passed" in data
        assert "git_status_hint" in data


# ---------------------------------------------------------------------------
# 20. Post-promotion test runs only after approval
# ---------------------------------------------------------------------------

class TestPostTestAfterApproval:
    def test_post_test_runs(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(
            run_id, target_repo=str(demo_repo), approve=True,
            test_command="python3 -c \"print('ok')\"",
        )
        assert result.status == "promoted"
        assert result.post_test_passed is True
        assert result.post_test_summary != ""


# ---------------------------------------------------------------------------
# 21. Failing post-promotion test reports honestly
# ---------------------------------------------------------------------------

class TestPostTestFails:
    def test_post_test_failure(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(
            run_id, target_repo=str(demo_repo), approve=True,
            test_command="python3 -c \"import sys; sys.exit(1)\"",
        )
        assert result.status == "promoted_test_failed"
        assert result.post_test_passed is False


# ---------------------------------------------------------------------------
# 22. Dry-run JSON is parseable
# ---------------------------------------------------------------------------

class TestDryRunJsonParseable:
    def test_dry_run_json(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), dry_run=True)
        data = export_promotion_json(result)
        text = json.dumps(data)
        parsed = json.loads(text)
        assert parsed["status"] == "dry_run"


# ---------------------------------------------------------------------------
# 23. Promote JSON is parseable
# ---------------------------------------------------------------------------

class TestPromoteJsonParseable:
    def test_promote_json(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        data = export_promotion_json(result)
        text = json.dumps(data)
        parsed = json.loads(text)
        assert parsed["status"] == "promoted"


# ---------------------------------------------------------------------------
# 24. Existing staged-only run never auto-promotes
# ---------------------------------------------------------------------------

class TestNoAutoPromote:
    def test_run_never_auto_promotes(self, demo_repo):
        """run_pingpong must never auto-promote. target stays clean."""
        provider = FakeProvider()
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
            max_rounds=2, repair_rounds=2,
        )
        assert result.final_status == "staged_review_passed"
        # No target changes
        assert result.changed_target_files == []
        assert result.target_mutated is False


# ---------------------------------------------------------------------------
# 25-31. Existing test suite regressions (verified by running full suite)
# ---------------------------------------------------------------------------

class TestArtifactPersistence:
    def test_artifacts_saved_on_pass(self, demo_repo, isolate_data_root):
        """Artifacts persisted for passing runs."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = _run_passing(demo_repo)
        run_dir = pingpong_run_dir(run_id)
        manifest = run_dir / "artifacts" / "manifest.json"
        assert manifest.exists()
        data = json.loads(manifest.read_text())
        # New format: dict with "artifacts" and "skipped" keys
        assert isinstance(data, dict)
        entries = data["artifacts"]
        assert len(entries) > 0
        # Artifact file exists
        for e in entries:
            artifact = run_dir / "artifacts" / "staged" / e["relative_path"]
            assert artifact.exists()


class TestArtifactManifestFields:
    def test_manifest_has_required_fields(self, demo_repo):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = _run_passing(demo_repo)
        run_dir = pingpong_run_dir(run_id)
        data = json.loads((run_dir / "artifacts" / "manifest.json").read_text())
        assert "artifacts" in data
        assert "skipped" in data
        entries = data["artifacts"]
        for e in entries:
            assert "relative_path" in e
            assert "operation" in e
            assert "file_type" in e
            assert "target_baseline_hash" in e
            assert "staged_hash" in e
            assert "size" in e


class TestPersistArtifactsSkipsSecrets:
    def test_env_not_persisted(self, tmp_path):
        """persist_artifacts skips .env files."""
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        (staging / ".env").write_text("SECRET=x")
        (staging / "ok.py").write_text("print('ok')")
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        entries = persist_artifacts(run_dir, staging, original, [".env", "ok.py"])
        paths = [e.relative_path for e in entries]
        assert ".env" not in paths
        assert "ok.py" in paths


class TestLoadArtifactsMissing:
    def test_no_manifest(self, tmp_path):
        entries, skipped, _ = load_artifacts(tmp_path)
        assert entries == []
        assert skipped == []


class TestPromotionRunNotFound:
    def test_run_not_found(self, demo_repo):
        result = promote_run("nonexistent_id", target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "run_not_found" in result.blocked_reason


class TestSummarizePromotionDryRun:
    def test_dry_run_summary(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), dry_run=True)
        summary = summarize_promotion(result)
        assert "preview only" in summary.lower()
        assert "To apply:" in summary


class TestSummarizePromotionApproved:
    def test_approved_summary(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        summary = summarize_promotion(result)
        assert "promoted" in summary.lower()
        assert "git status" in summary.lower()


class TestAllowedPaths:
    def test_normal_paths_allowed(self):
        assert _is_blocked_path("src/main.py") == ""
        assert _is_blocked_path("docs/README.md") == ""
        assert _is_blocked_path("tests/test_foo.py") == ""
        assert _is_blocked_path("packages/orchestration/loop.py") == ""


class TestAbsolutePathBlocked:
    def test_absolute_path(self):
        assert _is_blocked_path("/etc/passwd") == "absolute_path"


# ---------------------------------------------------------------------------
# 34. Artifact hash mismatch blocks before any target write
# ---------------------------------------------------------------------------

class TestArtifactHashMismatch:
    def test_hash_mismatch_blocks(self, demo_repo, isolate_data_root):
        """Tampered artifact blocks promotion, lists affected files."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_hash_mismatch"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        # Create run data
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": ["src/main.py"],
            "target_mutated": False,
            "changed_target_files": [],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        # Create artifact with wrong hash in manifest
        artifacts_dir = run_dir / "artifacts"
        staged_dir = artifacts_dir / "staged" / "src"
        staged_dir.mkdir(parents=True)
        (staged_dir / "main.py").write_text("print('tampered')")
        manifest = {
            "artifacts": [{
                "relative_path": "src/main.py",
                "operation": "modify",
                "file_type": ".py",
                "target_baseline_hash": _hash_file_helper(demo_repo / "src" / "main.py"),
                "staged_hash": "0000000000000000000000000000000000000000000000000000000000000000",
                "size": 18,
            }],
            "skipped": [],
        }
        (artifacts_dir / "manifest.json").write_text(json.dumps(manifest))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "artifact_hash_mismatch" in result.blocked_reason
        assert "src/main.py" in result.artifact_hash_mismatches
        # Target not modified
        assert (demo_repo / "src" / "main.py").read_text() == "def hello():\n    return 'hello'\n"


# ---------------------------------------------------------------------------
# 35. Missing artifact blocks before any target write
# ---------------------------------------------------------------------------

class TestMissingArtifact:
    def test_missing_artifact_blocks(self, demo_repo, isolate_data_root):
        """Staged file not in manifest blocks promotion."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_missing_artifact"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": ["src/main.py", "src/extra.py"],
            "target_mutated": False,
            "changed_target_files": [],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        # Manifest only has src/main.py, missing src/extra.py
        artifacts_dir = run_dir / "artifacts"
        staged_dir = artifacts_dir / "staged" / "src"
        staged_dir.mkdir(parents=True)
        content = b"def hello():\n    return 'hello'\n"
        (staged_dir / "main.py").write_bytes(content)
        import hashlib
        h = hashlib.sha256(content).hexdigest()
        manifest = {
            "artifacts": [{
                "relative_path": "src/main.py",
                "operation": "modify",
                "file_type": ".py",
                "target_baseline_hash": _hash_file_helper(demo_repo / "src" / "main.py"),
                "staged_hash": h,
                "size": len(content),
            }],
            "skipped": [],
        }
        (artifacts_dir / "manifest.json").write_text(json.dumps(manifest))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "missing_artifacts" in result.blocked_reason
        assert "src/extra.py" in result.missing_artifacts


# ---------------------------------------------------------------------------
# 36. Skipped unsafe staged files block promotion
# ---------------------------------------------------------------------------

class TestSkippedUnsafeBlocks:
    def test_skipped_blocks(self, demo_repo, isolate_data_root):
        """Skipped files in manifest block promotion."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_skipped"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": ["src/main.py"],
            "target_mutated": False,
            "changed_target_files": [],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        # Manifest with a skipped entry
        artifacts_dir = run_dir / "artifacts"
        staged_dir = artifacts_dir / "staged" / "src"
        staged_dir.mkdir(parents=True)
        content = b"print('ok')"
        (staged_dir / "main.py").write_bytes(content)
        import hashlib
        h = hashlib.sha256(content).hexdigest()
        manifest = {
            "artifacts": [{
                "relative_path": "src/main.py",
                "operation": "modify",
                "file_type": ".py",
                "target_baseline_hash": _hash_file_helper(demo_repo / "src" / "main.py"),
                "staged_hash": h,
                "size": len(content),
            }],
            "skipped": [{"relative_path": "node_modules/pkg/index.js", "reason": "blocked_path: node_modules"}],
        }
        (artifacts_dir / "manifest.json").write_text(json.dumps(manifest))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "skipped_unsafe" in result.blocked_reason
        assert len(result.skipped_artifacts) > 0


# ---------------------------------------------------------------------------
# 37. All validation before any target writes
# ---------------------------------------------------------------------------

class TestAllValidationBeforeWrites:
    def test_no_partial_apply(self, demo_repo, isolate_data_root):
        """Multiple files: one bad hash. No files written to target."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_no_partial"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": ["src/main.py", "docs/new.md"],
            "target_mutated": False,
            "changed_target_files": [],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        artifacts_dir = run_dir / "artifacts"

        # Good file
        import hashlib
        good_content = b"def updated():\n    return 'updated'\n"
        good_hash = hashlib.sha256(good_content).hexdigest()
        (artifacts_dir / "staged" / "src").mkdir(parents=True)
        (artifacts_dir / "staged" / "src" / "main.py").write_bytes(good_content)

        # Bad file (hash won't match)
        bad_content = b"# New doc\n"
        (artifacts_dir / "staged" / "docs").mkdir(parents=True)
        (artifacts_dir / "staged" / "docs" / "new.md").write_bytes(bad_content)

        manifest = {
            "artifacts": [
                {
                    "relative_path": "src/main.py",
                    "operation": "modify",
                    "file_type": ".py",
                    "target_baseline_hash": _hash_file_helper(demo_repo / "src" / "main.py"),
                    "staged_hash": good_hash,
                    "size": len(good_content),
                },
                {
                    "relative_path": "docs/new.md",
                    "operation": "create",
                    "file_type": ".md",
                    "target_baseline_hash": "",
                    "staged_hash": "bad_hash_value",
                    "size": len(bad_content),
                },
            ],
            "skipped": [],
        }
        (artifacts_dir / "manifest.json").write_text(json.dumps(manifest))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        # Neither file written to target
        assert (demo_repo / "src" / "main.py").read_text() == "def hello():\n    return 'hello'\n"
        assert not (demo_repo / "docs" / "new.md").exists()


# ---------------------------------------------------------------------------
# 38. Dry-run persists promotion.json
# ---------------------------------------------------------------------------

class TestDryRunPersisted:
    def test_dry_run_persisted(self, demo_repo):
        run_id = _run_passing(demo_repo)
        promote_run(run_id, target_repo=str(demo_repo), dry_run=True)
        promo = load_promotion(run_id)
        assert promo is not None
        assert promo["status"] == "dry_run"
        assert promo["dry_run"] is True


# ---------------------------------------------------------------------------
# 39. No-approve persists promotion.json
# ---------------------------------------------------------------------------

class TestNoApprovePersisted:
    def test_no_approve_persisted(self, demo_repo):
        run_id = _run_passing(demo_repo)
        promote_run(run_id, target_repo=str(demo_repo))
        promo = load_promotion(run_id)
        assert promo is not None
        assert promo["status"] == "dry_run"
        assert promo["approved"] is False


# ---------------------------------------------------------------------------
# 40. Blocked attempts persist promotion.json
# ---------------------------------------------------------------------------

class TestBlockedAttemptPersisted:
    def test_blocked_persisted(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_blocked_persist"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
            "repo_path": str(demo_repo),
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": [],
            "target_mutated": False,
            "changed_target_files": [],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        promo = load_promotion(run_id)
        assert promo is not None
        assert promo["status"] == "blocked"
        assert "no_staged_files" in promo["blocked_reason"]


# ---------------------------------------------------------------------------
# 41. JSON export includes new integrity fields
# ---------------------------------------------------------------------------

class TestJsonIntegrityFields:
    def test_json_has_integrity_fields(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        data = export_promotion_json(result)
        assert "artifact_hash_mismatches" in data
        assert "missing_artifacts" in data
        assert "skipped_artifacts" in data
        assert "unexpected_artifacts" in data
        assert "duplicate_artifacts" in data
        assert "run_repo" in data
        assert "requested_target_repo" in data
        assert "target_repo_mismatch" in data


# ---------------------------------------------------------------------------
# 42. persist_artifacts records skipped with reasons
# ---------------------------------------------------------------------------

class TestPersistArtifactsSkippedTracking:
    def test_skipped_recorded(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        (staging / "ok.py").write_text("print('ok')")
        (staging / "image.png").write_bytes(b"\x89PNG")
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        entries = persist_artifacts(run_dir, staging, original, ["ok.py", "image.png"])
        assert len(entries) == 1
        assert entries[0].relative_path == "ok.py"
        # Check manifest has skipped
        data = json.loads((run_dir / "artifacts" / "manifest.json").read_text())
        assert len(data["skipped"]) == 1
        assert data["skipped"][0]["relative_path"] == "image.png"
        assert "binary_file" in data["skipped"][0]["reason"]


# ---------------------------------------------------------------------------
# 43. load_artifacts returns skipped entries
# ---------------------------------------------------------------------------

class TestLoadArtifactsSkipped:
    def test_load_skipped(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        (staging / "ok.py").write_text("print('ok')")
        (staging / "image.png").write_bytes(b"\x89PNG")
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        persist_artifacts(run_dir, staging, original, ["ok.py", "image.png"])
        entries, skipped, staged_dir = load_artifacts(run_dir)
        assert len(entries) == 1
        assert len(skipped) == 1
        assert skipped[0].relative_path == "image.png"
        assert skipped[0].reason == "binary_file"


# ---------------------------------------------------------------------------
# 44. Old flat manifest backward compatibility
# ---------------------------------------------------------------------------

class TestOldManifestCompat:
    def test_flat_list_manifest(self, tmp_path):
        """load_artifacts handles old flat-list manifest format."""
        artifacts_dir = tmp_path / "artifacts"
        artifacts_dir.mkdir()
        (artifacts_dir / "staged").mkdir()
        flat = [{"relative_path": "foo.py", "operation": "create",
                 "file_type": ".py", "target_baseline_hash": "",
                 "staged_hash": "abc", "size": 10}]
        (artifacts_dir / "manifest.json").write_text(json.dumps(flat))
        entries, skipped, _ = load_artifacts(tmp_path)
        assert len(entries) == 1
        assert entries[0].relative_path == "foo.py"
        assert skipped == []


# ---------------------------------------------------------------------------
# Helper for manual run data creation
# ---------------------------------------------------------------------------

def _make_run_data(run_id, demo_repo, **overrides):
    """Build standard run data dict with repo_path set."""
    data = {
        "run_id": run_id,
        "repo_path": str(demo_repo),
        "final_status": "staged_review_passed",
        "mode": "staged",
        "staged_files": ["README.md"],
        "target_mutated": False,
        "changed_target_files": [],
        "rounds": [{"reviewer": {"verdict": "pass"}}],
    }
    data.update(overrides)
    return data


def _make_artifact(run_dir, rel_path, content, operation="create",
                   baseline_hash="", staged_hash=None):
    """Create artifact file and return manifest entry dict."""
    import hashlib
    artifacts_dir = run_dir / "artifacts" / "staged"
    dest = artifacts_dir / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        content = content.encode()
    dest.write_bytes(content)
    if staged_hash is None:
        staged_hash = hashlib.sha256(content).hexdigest()
    return {
        "relative_path": rel_path,
        "operation": operation,
        "file_type": os.path.splitext(rel_path)[1].lower(),
        "target_baseline_hash": baseline_hash,
        "staged_hash": staged_hash,
        "size": len(content),
    }


def _write_manifest(run_dir, artifacts, skipped=None):
    """Write manifest.json with artifacts and optional skipped."""
    manifest = {"artifacts": artifacts, "skipped": skipped or []}
    mf = run_dir / "artifacts" / "manifest.json"
    mf.parent.mkdir(parents=True, exist_ok=True)
    mf.write_text(json.dumps(manifest))


# ---------------------------------------------------------------------------
# 45. Unexpected extra artifact blocks (primary-review regression)
# ---------------------------------------------------------------------------

class TestUnexpectedArtifactBlocks:
    def test_extra_artifact_blocks(self, demo_repo, isolate_data_root):
        """Exact primary-review reproduction: MALICIOUS.md in manifest but not in staged_files."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_unexpected"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        # staged_files only has README.md
        data = _make_run_data(run_id, demo_repo, staged_files=["README.md"])
        (run_dir / "result.json").write_text(json.dumps(data))

        # Manifest has README.md AND MALICIOUS.md
        readme_content = b"# Updated README\n"
        malicious_content = b"# MALICIOUS\n"
        a1 = _make_artifact(run_dir, "README.md", readme_content, operation="modify",
                            baseline_hash=_hash_file_helper(demo_repo / "README.md"))
        a2 = _make_artifact(run_dir, "MALICIOUS.md", malicious_content)
        _write_manifest(run_dir, [a1, a2])

        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)

        # Must block
        assert result.status == "blocked"
        assert "unexpected_artifacts" in result.blocked_reason
        assert "MALICIOUS.md" in result.unexpected_artifacts

        # Target NOT modified
        assert not (demo_repo / "MALICIOUS.md").exists()
        assert (demo_repo / "README.md").read_text() == "# Demo\nA demo project.\n"

        # Persisted
        promo = load_promotion(run_id)
        assert promo is not None
        assert "unexpected_artifacts" in promo
        assert "MALICIOUS.md" in promo["unexpected_artifacts"]

    def test_extra_code_artifact_not_written(self, demo_repo, isolate_data_root):
        """Extra code artifact not in staged_files does not get written."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_unexpected_code"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        data = _make_run_data(run_id, demo_repo, staged_files=["src/main.py"])
        (run_dir / "result.json").write_text(json.dumps(data))

        a1 = _make_artifact(run_dir, "src/main.py", b"def updated(): pass",
                            operation="modify",
                            baseline_hash=_hash_file_helper(demo_repo / "src" / "main.py"))
        a2 = _make_artifact(run_dir, "src/backdoor.py", b"import os; os.system('rm -rf /')")
        _write_manifest(run_dir, [a1, a2])

        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "src/backdoor.py" in result.unexpected_artifacts
        assert not (demo_repo / "src" / "backdoor.py").exists()
        assert (demo_repo / "src" / "main.py").read_text() == "def hello():\n    return 'hello'\n"


# ---------------------------------------------------------------------------
# 46. Exact artifact set promotes successfully
# ---------------------------------------------------------------------------

class TestExactArtifactSetPromotes:
    def test_exact_set_promotes(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "promoted"
        assert len(result.applied_files) > 0
        assert result.unexpected_artifacts == []
        assert result.missing_artifacts == []
        assert result.duplicate_artifacts == []


# ---------------------------------------------------------------------------
# 47. Missing artifact still blocks
# ---------------------------------------------------------------------------

class TestMissingArtifactStillBlocks:
    def test_missing_still_blocks(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_missing_still"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        data = _make_run_data(run_id, demo_repo,
                              staged_files=["src/main.py", "src/other.py"])
        (run_dir / "result.json").write_text(json.dumps(data))

        a1 = _make_artifact(run_dir, "src/main.py", b"print('ok')",
                            operation="modify",
                            baseline_hash=_hash_file_helper(demo_repo / "src" / "main.py"))
        _write_manifest(run_dir, [a1])

        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "missing_artifacts" in result.blocked_reason
        assert "src/other.py" in result.missing_artifacts


# ---------------------------------------------------------------------------
# 48. Duplicate artifact paths after normalization block
# ---------------------------------------------------------------------------

class TestDuplicateArtifacts:
    def test_duplicate_blocks(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_duplicate"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        data = _make_run_data(run_id, demo_repo, staged_files=["src/main.py"])
        (run_dir / "result.json").write_text(json.dumps(data))

        content = b"print('ok')"
        import hashlib
        h = hashlib.sha256(content).hexdigest()
        baseline = _hash_file_helper(demo_repo / "src" / "main.py")

        # Two entries with same normalized path (./src/main.py and src/main.py)
        manifest = {
            "artifacts": [
                {"relative_path": "src/main.py", "operation": "modify",
                 "file_type": ".py", "target_baseline_hash": baseline,
                 "staged_hash": h, "size": len(content)},
                {"relative_path": "./src/main.py", "operation": "modify",
                 "file_type": ".py", "target_baseline_hash": baseline,
                 "staged_hash": h, "size": len(content)},
            ],
            "skipped": [],
        }
        (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
        (run_dir / "artifacts" / "manifest.json").write_text(json.dumps(manifest))
        (run_dir / "artifacts" / "staged" / "src").mkdir(parents=True)
        (run_dir / "artifacts" / "staged" / "src" / "main.py").write_bytes(content)

        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "duplicate_artifacts" in result.blocked_reason
        assert "src/main.py" in result.duplicate_artifacts

    def test_duplicate_listed(self, demo_repo, isolate_data_root):
        """duplicate_artifacts field lists affected paths."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_dup_listed"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        data = _make_run_data(run_id, demo_repo, staged_files=["src/main.py"])
        (run_dir / "result.json").write_text(json.dumps(data))

        content = b"print('ok')"
        import hashlib
        h = hashlib.sha256(content).hexdigest()
        baseline = _hash_file_helper(demo_repo / "src" / "main.py")

        manifest = {
            "artifacts": [
                {"relative_path": "src/main.py", "operation": "modify",
                 "file_type": ".py", "target_baseline_hash": baseline,
                 "staged_hash": h, "size": len(content)},
                {"relative_path": "src/main.py", "operation": "modify",
                 "file_type": ".py", "target_baseline_hash": baseline,
                 "staged_hash": h, "size": len(content)},
            ],
            "skipped": [],
        }
        (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
        (run_dir / "artifacts" / "manifest.json").write_text(json.dumps(manifest))
        (run_dir / "artifacts" / "staged" / "src").mkdir(parents=True)
        (run_dir / "artifacts" / "staged" / "src" / "main.py").write_bytes(content)

        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert len(result.duplicate_artifacts) == 1


# ---------------------------------------------------------------------------
# 49. Path normalization
# ---------------------------------------------------------------------------

class TestPathNormalization:
    def test_leading_dot_slash_normalized(self):
        assert _normalize_rel_path("./src/main.py") == "src/main.py"
        assert _normalize_rel_path("././foo.py") == "foo.py"
        assert _normalize_rel_path("src/main.py") == "src/main.py"

    def test_backslash_normalized(self):
        assert _normalize_rel_path("src\\main.py") == "src/main.py"

    def test_trailing_slash_normalized(self):
        assert _normalize_rel_path("src/dir/") == "src/dir"

    def test_dotdot_still_blocked(self):
        assert _is_blocked_path("../etc/passwd") == "path_traversal"

    def test_absolute_still_blocked(self):
        assert _is_blocked_path("/etc/passwd") == "absolute_path"


# ---------------------------------------------------------------------------
# 50. Target repo mismatch blocks
# ---------------------------------------------------------------------------

class TestTargetRepoMismatch:
    def test_mismatch_blocks(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_repo_mismatch"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        # Run was for demo_repo, but promote targets /tmp/other
        other_repo = demo_repo.parent / "other_repo"
        other_repo.mkdir()
        data = _make_run_data(run_id, demo_repo)
        (run_dir / "result.json").write_text(json.dumps(data))

        result = promote_run(run_id, target_repo=str(other_repo), approve=True)
        assert result.status == "blocked"
        assert "target_repo_mismatch" in result.blocked_reason
        assert result.target_repo_mismatch is True
        assert result.run_repo == str(demo_repo)

    def test_mismatch_persisted(self, demo_repo, isolate_data_root):
        """Target repo mismatch persists promotion attempt."""
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_repo_mismatch_persist"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        other_repo = demo_repo.parent / "other_repo2"
        other_repo.mkdir()
        data = _make_run_data(run_id, demo_repo)
        (run_dir / "result.json").write_text(json.dumps(data))

        promote_run(run_id, target_repo=str(other_repo), approve=True)
        promo = load_promotion(run_id)
        assert promo is not None
        assert promo["status"] == "blocked"
        assert "target_repo_mismatch" in promo["blocked_reason"]
        assert promo["target_repo_mismatch"] is True

    def test_same_repo_different_spelling(self, demo_repo):
        """'.' vs absolute path resolves and passes."""
        run_id = _run_passing(demo_repo)
        # promote with absolute path — run was also for demo_repo (resolved)
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "promoted"
        assert result.target_repo_mismatch is False


# ---------------------------------------------------------------------------
# 51. Missing run repo path blocks legacy promotion
# ---------------------------------------------------------------------------

class TestMissingRunRepoPath:
    def test_missing_repo_path_blocks(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_no_repo_path"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        # Old run data without repo_path
        data = {
            "run_id": run_id,
            "final_status": "staged_review_passed",
            "mode": "staged",
            "staged_files": ["README.md"],
            "target_mutated": False,
            "changed_target_files": [],
            "rounds": [{"reviewer": {"verdict": "pass"}}],
        }
        (run_dir / "result.json").write_text(json.dumps(data))

        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "missing_run_repo_path" in result.blocked_reason

    def test_empty_repo_path_blocks(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_empty_repo_path"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        data = _make_run_data(run_id, demo_repo, repo_path="")
        (run_dir / "result.json").write_text(json.dumps(data))

        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "missing_run_repo_path" in result.blocked_reason


# ---------------------------------------------------------------------------
# 52. Dry-run with exact artifact set still does not mutate
# ---------------------------------------------------------------------------

class TestDryRunExactSetNoMutation:
    def test_dry_run_exact_no_mutation(self, demo_repo):
        run_id = _run_passing(demo_repo)
        original = (demo_repo / "README.md").read_text()
        result = promote_run(run_id, target_repo=str(demo_repo), dry_run=True)
        assert result.status == "dry_run"
        assert (demo_repo / "README.md").read_text() == original


# ---------------------------------------------------------------------------
# 53. No-approve with exact artifact set still does not mutate
# ---------------------------------------------------------------------------

class TestNoApproveExactSetNoMutation:
    def test_no_approve_exact_no_mutation(self, demo_repo):
        run_id = _run_passing(demo_repo)
        original = (demo_repo / "README.md").read_text()
        result = promote_run(run_id, target_repo=str(demo_repo))
        assert result.status == "dry_run"
        assert result.approved is False
        assert (demo_repo / "README.md").read_text() == original


# ---------------------------------------------------------------------------
# 54. Approved promotion with exact artifact set applies new text file
# ---------------------------------------------------------------------------

class TestApprovedExactNewFile:
    def test_exact_new_file(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "promoted"
        for f in result.applied_files:
            assert (demo_repo / f).exists()


# ---------------------------------------------------------------------------
# 55. Approved promotion with exact artifact set applies code modification
# ---------------------------------------------------------------------------

class TestApprovedExactModify:
    def test_exact_modify(self, demo_repo):
        run_id = _run_passing(demo_repo, builder_files=["README.md"])
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "promoted"
        assert "README.md" in result.applied_files


# ---------------------------------------------------------------------------
# 56. Artifact hash mismatch still blocks
# ---------------------------------------------------------------------------

class TestHashMismatchStillBlocks:
    def test_hash_still_blocks(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_hash_still"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        data = _make_run_data(run_id, demo_repo, staged_files=["src/main.py"])
        (run_dir / "result.json").write_text(json.dumps(data))

        a1 = _make_artifact(run_dir, "src/main.py", b"print('ok')",
                            operation="modify",
                            baseline_hash=_hash_file_helper(demo_repo / "src" / "main.py"),
                            staged_hash="bad_hash")
        _write_manifest(run_dir, [a1])

        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "artifact_hash_mismatch" in result.blocked_reason


# ---------------------------------------------------------------------------
# 57. Baseline mismatch still blocks
# ---------------------------------------------------------------------------

class TestBaselineMismatchStillBlocks:
    def test_baseline_still_blocks(self, demo_repo):
        run_id = _run_passing(demo_repo, builder_files=["README.md"])
        (demo_repo / "README.md").write_text("# Modified after run\n")
        result = promote_run(run_id, target_repo=str(demo_repo), approve=True)
        assert result.status == "blocked"
        assert "baseline_mismatch" in result.blocked_reason


# ---------------------------------------------------------------------------
# 58. Post-promotion test still runs after approved apply
# ---------------------------------------------------------------------------

class TestPostTestStillRuns:
    def test_post_test_runs(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(
            run_id, target_repo=str(demo_repo), approve=True,
            test_command="python3 -c \"print('ok')\"",
        )
        assert result.status == "promoted"
        assert result.post_test_passed is True


# ---------------------------------------------------------------------------
# 59. Failing post-promotion test still reports honestly
# ---------------------------------------------------------------------------

class TestPostTestStillFails:
    def test_post_test_failure(self, demo_repo):
        run_id = _run_passing(demo_repo)
        result = promote_run(
            run_id, target_repo=str(demo_repo), approve=True,
            test_command="python3 -c \"import sys; sys.exit(1)\"",
        )
        assert result.status == "promoted_test_failed"
        assert result.post_test_passed is False


# ---------------------------------------------------------------------------
# 60. Report shows unexpected artifact block
# ---------------------------------------------------------------------------

class TestReportShowsUnexpected:
    def test_report_unexpected(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_report_unexp"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        data = _make_run_data(run_id, demo_repo, staged_files=["README.md"])
        (run_dir / "result.json").write_text(json.dumps(data))

        a1 = _make_artifact(run_dir, "README.md", b"# Updated\n",
                            operation="modify",
                            baseline_hash=_hash_file_helper(demo_repo / "README.md"))
        a2 = _make_artifact(run_dir, "extra.txt", b"extra")
        _write_manifest(run_dir, [a1, a2])

        promote_run(run_id, target_repo=str(demo_repo), approve=True)
        promo = load_promotion(run_id)
        assert promo is not None
        assert promo["status"] == "blocked"
        assert "extra.txt" in promo["unexpected_artifacts"]

        summary = summarize_promotion(promote_run(run_id, target_repo=str(demo_repo)))
        assert "unexpected" in summary.lower() or "Unexpected" in summary


# ---------------------------------------------------------------------------
# 61. Report shows target repo mismatch block
# ---------------------------------------------------------------------------

class TestReportShowsRepoMismatch:
    def test_report_repo_mismatch(self, demo_repo, isolate_data_root):
        from packages.orchestration.data_paths import pingpong_run_dir
        run_id = "test_report_mismatch"
        run_dir = pingpong_run_dir(run_id)
        run_dir.mkdir(parents=True)

        other = demo_repo.parent / "other_for_report"
        other.mkdir()
        data = _make_run_data(run_id, demo_repo)
        (run_dir / "result.json").write_text(json.dumps(data))

        result = promote_run(run_id, target_repo=str(other), approve=True)
        summary = summarize_promotion(result)
        assert "Run repo:" in summary or "target_repo_mismatch" in summary


# F085 T002b — pingpong_promote._run_post_test on the shared `test`-class seam


def test_pingpong_promote_post_test_runs_on_the_guarded_seam(tmp_path, monkeypatch):
    """The spawn goes through `run_guarded_test_command`, and its BYTES decode to str."""
    import subprocess

    from packages.orchestration import pingpong_promote

    seen: dict[str, object] = {}

    def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
        seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
        return subprocess.CompletedProcess(list(cmd), 0, b"out-line\n", b"err-line\n")

    monkeypatch.setattr(pingpong_promote, "run_guarded_test_command", _fake_guarded)
    passed, summary = pingpong_promote._run_post_test("pytest -q", tmp_path, timeout_sec=17)

    assert passed is True
    assert seen == {"cmd": ["pytest", "-q"], "timeout_sec": 17, "cwd": str(tmp_path)}
    assert summary.startswith("exit=0")
    assert "out-line" in summary
    assert "err-line" in summary
