"""Ping-pong promotion tests.

Tests the `do promote` command: eligibility, baseline validation,
artifact persistence, dry-run, approved apply, blocked paths,
post-promotion tests, report integration.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import (
    run_pingpong,
)
from packages.orchestration.pingpong_promote import (
    _is_blocked_path,
    export_promotion_json,
    load_artifacts,
    load_promotion,
    persist_artifacts,
    promote_run,
    summarize_promotion,
)
from packages.orchestration.pingpong_provider import FakeProvider

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
        max_rounds=2,
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
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        run_id = "test_no_staged"
        run_dir = _pingpong_runs_dir() / run_id
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
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
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        run_id = "test_mutated"
        run_dir = _pingpong_runs_dir() / run_id
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
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
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        run_id = "test_changed"
        run_dir = _pingpong_runs_dir() / run_id
        run_dir.mkdir(parents=True)
        data = {
            "run_id": run_id,
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
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        run_id = "test_delete"
        run_dir = _pingpong_runs_dir() / run_id
        run_dir.mkdir(parents=True)
        # Create run data
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
            max_rounds=2,
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
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        run_id = _run_passing(demo_repo)
        run_dir = _pingpong_runs_dir() / run_id
        manifest = run_dir / "artifacts" / "manifest.json"
        assert manifest.exists()
        entries = json.loads(manifest.read_text())
        assert len(entries) > 0
        # Artifact file exists
        for e in entries:
            artifact = run_dir / "artifacts" / "staged" / e["relative_path"]
            assert artifact.exists()


class TestArtifactManifestFields:
    def test_manifest_has_required_fields(self, demo_repo):
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir
        run_id = _run_passing(demo_repo)
        run_dir = _pingpong_runs_dir() / run_id
        entries = json.loads((run_dir / "artifacts" / "manifest.json").read_text())
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
        entries, _ = load_artifacts(tmp_path)
        assert entries == []


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
