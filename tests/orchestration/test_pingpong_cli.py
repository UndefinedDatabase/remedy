"""Ping-pong CLI safety closure E2E tests.

Tests the ClaudeCliProvider staging-cwd binding, target snapshot guard,
external run storage, no-test behavior, JSON/report UX, and all provider
error paths — using fake/mock providers (no real Claude calls, no network).
"""
from __future__ import annotations

import json
import stat
import textwrap
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import (
    export_pingpong_json,
    list_runs,
    load_run,
    run_pingpong,
    summarize_pingpong,
)
from packages.orchestration.pingpong_provider import (
    ClaudeCliProvider,
    FakeProvider,
    create_provider,
)

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


@pytest.fixture
def fake_claude_builder_bin(tmp_path: Path) -> Path:
    """Fake `claude` that writes a file to cwd (to prove cwd binding)."""
    bin_dir = tmp_path / "builder_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    claude_script.write_text(textwrap.dedent("""\
        #!/bin/bash
        echo "hello from builder" > "$PWD/BUILDER_WAS_HERE.txt"
        echo "Builder made changes"
        echo "- docs/README.md updated"
    """))
    claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


@pytest.fixture
def fake_claude_reviewer_bin(tmp_path: Path) -> Path:
    """Fake `claude` that returns reviewer JSON."""
    bin_dir = tmp_path / "reviewer_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    claude_script.write_text(textwrap.dedent("""\
        #!/bin/bash
        echo '{"verdict": "pass", "findings": [], "confidence": "high", "summary": "All good"}'
    """))
    claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


@pytest.fixture
def fake_claude_target_mutator_bin(tmp_path: Path, demo_repo: Path) -> Path:
    """Fake `claude` that writes directly to the target repo (the bug)."""
    bin_dir = tmp_path / "mutator_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    # This script writes to the ACTUAL target repo path, simulating the blocker bug
    claude_script.write_text(textwrap.dedent(f"""\
        #!/bin/bash
        echo "mutating target" > "{demo_repo}/CLI_MUTATED_TARGET.txt"
        echo "Builder did things"
    """))
    claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


@pytest.fixture
def fake_claude_failing_bin(tmp_path: Path) -> Path:
    """Fake `claude` that exits non-zero."""
    bin_dir = tmp_path / "fail_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    claude_script.write_text(textwrap.dedent("""\
        #!/bin/bash
        echo "Error: auth failed" >&2
        exit 1
    """))
    claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


@pytest.fixture
def fake_claude_reviewer_mutator_bin(tmp_path: Path, demo_repo: Path) -> Path:
    """Fake reviewer `claude` that mutates target."""
    bin_dir = tmp_path / "rev_mut_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    claude_script.write_text(textwrap.dedent(f"""\
        #!/bin/bash
        echo "reviewer mutating target" > "{demo_repo}/REVIEWER_MUTATED.txt"
        echo '{{"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"}}'
    """))
    claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


# ---------------------------------------------------------------------------
# 1. claude-cli Builder runs in staging cwd
# ---------------------------------------------------------------------------

class TestBuilderStagingCwd:
    def test_builder_writes_to_staging_not_target(self, monkeypatch, demo_repo, fake_claude_builder_bin, fake_claude_reviewer_bin):
        """Fake claude writes BUILDER_WAS_HERE.txt to cwd. Must appear in staging, not target."""
        monkeypatch.setenv("PATH", f"{fake_claude_builder_bin}:{fake_claude_reviewer_bin}")
        original_files = set(p.name for p in demo_repo.iterdir())
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        # Target must NOT have BUILDER_WAS_HERE.txt
        assert not (demo_repo / "BUILDER_WAS_HERE.txt").exists(), "Builder wrote to target repo!"
        # Target files unchanged
        assert "BUILDER_WAS_HERE.txt" not in set(p.name for p in demo_repo.iterdir())
        # Staged files should include it
        assert "BUILDER_WAS_HERE.txt" in result.staged_files
        assert result.target_mutated is False


# ---------------------------------------------------------------------------
# 2. Fake claude cwd write modifies staging, not target
# ---------------------------------------------------------------------------

class TestFakeClaudeCwdWrite:
    def test_cwd_write_goes_to_staging(self, monkeypatch, demo_repo, fake_claude_builder_bin, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", f"{fake_claude_builder_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.target_mutated is False
        assert result.changed_target_files == []


# ---------------------------------------------------------------------------
# 3. Target mutation reproduction caught by snapshot guard
# ---------------------------------------------------------------------------

class TestTargetMutationReproduction:
    def test_target_mutation_caught(self, monkeypatch, demo_repo, fake_claude_target_mutator_bin, fake_claude_reviewer_bin):
        """Exact reproduction of primary-review bug: fake claude writes CLI_MUTATED_TARGET.txt to target."""
        monkeypatch.setenv("PATH", f"{fake_claude_target_mutator_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.final_status == "target_mutation_blocked"
        assert result.target_mutated is True
        assert any("CLI_MUTATED_TARGET.txt" in f for f in result.changed_target_files)


# ---------------------------------------------------------------------------
# 4. If target mutates, final status is target_mutation_blocked, not pass
# ---------------------------------------------------------------------------

class TestTargetMutationStatus:
    def test_status_is_blocked_not_pass(self, monkeypatch, demo_repo, fake_claude_target_mutator_bin, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", f"{fake_claude_target_mutator_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.final_status != "staged_review_passed"
        assert result.final_status == "target_mutation_blocked"


# ---------------------------------------------------------------------------
# 5. changed_target_files is non-empty when target mutation detected
# ---------------------------------------------------------------------------

class TestChangedTargetFilesNonEmpty:
    def test_changed_target_files_populated(self, monkeypatch, demo_repo, fake_claude_target_mutator_bin, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", f"{fake_claude_target_mutator_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert len(result.changed_target_files) > 0


# ---------------------------------------------------------------------------
# 6. Reviewer cannot mutate target
# ---------------------------------------------------------------------------

class TestReviewerCannotMutateTarget:
    def test_reviewer_target_mutation_blocked(self, monkeypatch, demo_repo, fake_claude_builder_bin, fake_claude_reviewer_mutator_bin):
        monkeypatch.setenv("PATH", str(fake_claude_builder_bin))
        # Builder uses builder_bin, reviewer uses mutator_bin (explicit provider)
        builder_prov = ClaudeCliProvider(cwd=None)  # Will get staging cwd from loop
        reviewer_prov = ClaudeCliProvider()
        reviewer_prov._claude_path = str(fake_claude_reviewer_mutator_bin / "claude")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli",
            reviewer_provider=reviewer_prov,
            max_rounds=1,
        )
        assert result.target_mutated is True
        assert result.final_status == "target_mutation_blocked"
        assert any("REVIEWER_MUTATED" in f for f in result.changed_target_files)


# ---------------------------------------------------------------------------
# 7. Reviewer mutation of staging detected
# ---------------------------------------------------------------------------

class TestReviewerStagingMutation:
    def test_fake_reviewer_no_staging_mutation(self, demo_repo):
        """FakeProvider reviewer does not mutate staging."""
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert "Reviewer mutated staging" not in (result.error or "")


# ---------------------------------------------------------------------------
# 8. Ping-pong run storage is outside target repo
# ---------------------------------------------------------------------------

class TestExternalRunStorage:
    def test_storage_outside_target(self, demo_repo, isolate_data_root):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        # Must NOT exist in target repo
        assert not (demo_repo / ".data" / "pingpong_runs").exists()
        # Must exist in remedy data root
        stored = isolate_data_root / "pingpong_runs" / result.run_id / "result.json"
        assert stored.exists()


# ---------------------------------------------------------------------------
# 9. do run --json does not create target .data/pingpong_runs
# ---------------------------------------------------------------------------

class TestNoTargetDataDir:
    def test_no_target_data_dir_created(self, demo_repo):
        run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert not (demo_repo / ".data").exists()


# ---------------------------------------------------------------------------
# 10. do report <run_id> --json loads from Remedy data root
# ---------------------------------------------------------------------------

class TestReportLoadsFromDataRoot:
    def test_load_run_from_data_root(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = load_run(result.run_id)
        assert data is not None
        assert data["run_id"] == result.run_id


# ---------------------------------------------------------------------------
# 11. do report list --json loads from Remedy data root
# ---------------------------------------------------------------------------

class TestReportListFromDataRoot:
    def test_list_runs_from_data_root(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        runs = list_runs()
        assert any(r["run_id"] == result.run_id for r in runs)


# ---------------------------------------------------------------------------
# 12. No test command does not claim tests passed
# ---------------------------------------------------------------------------

class TestNoTestCommand:
    def test_no_test_command_no_pass(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.tests_not_run is True
        for rd in result.rounds:
            assert rd.test_passed is None
            assert rd.test_summary == "tests_not_run"

    def test_no_test_command_json_has_tests_not_run(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = export_pingpong_json(result)
        assert data["tests_not_run"] is True


# ---------------------------------------------------------------------------
# 13. Explicit --test-command runs in staging
# ---------------------------------------------------------------------------

class TestExplicitTestCommand:
    def test_passing_test_command(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            test_command="echo 'tests pass'",
        )
        assert result.tests_not_run is False
        for rd in result.rounds:
            assert rd.test_passed is True
            assert "exit=0" in rd.test_summary

    def test_failing_test_command(self, demo_repo):
        provider = FakeProvider(pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
            test_command="false",
            max_rounds=1,
        )
        assert result.final_status == "test_failed"
        rd = result.rounds[0]
        assert rd.test_passed is False


# ---------------------------------------------------------------------------
# 14. Target repo receives no .pytest_cache or __pycache__
# ---------------------------------------------------------------------------

class TestNoTargetArtifacts:
    def test_no_pytest_cache_in_target(self, demo_repo):
        run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert not (demo_repo / ".pytest_cache").exists()
        assert not (demo_repo / "__pycache__").exists()


# ---------------------------------------------------------------------------
# 15. do run --json is parseable and includes report commands
# ---------------------------------------------------------------------------

class TestJsonOutput:
    def test_json_parseable_with_report_commands(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = export_pingpong_json(result)
        text = json.dumps(data)
        parsed = json.loads(text)
        assert "run_id" in parsed
        assert "final_status" in parsed
        assert "report_command" in parsed
        assert "report_json_command" in parsed
        assert "report_path" in parsed
        assert "target_mutated" in parsed
        assert "changed_target_files" in parsed
        assert "staged_files" in parsed
        assert "tests_not_run" in parsed
        assert result.run_id in parsed["report_command"]
        assert "--json" in parsed["report_json_command"]


# ---------------------------------------------------------------------------
# 16. do report --json is parseable
# ---------------------------------------------------------------------------

class TestReportJsonParseable:
    def test_report_json_valid(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = load_run(result.run_id)
        assert data is not None
        text = json.dumps(data)
        parsed = json.loads(text)
        assert parsed["run_id"] == result.run_id


# ---------------------------------------------------------------------------
# 17. Missing claude-cli blocks honestly
# ---------------------------------------------------------------------------

class TestMissingClaudeCli:
    def test_build_error_when_no_claude(self, monkeypatch):
        monkeypatch.setenv("PATH", "/nonexistent")
        provider = ClaudeCliProvider()
        out = provider.build("test prompt")
        assert out.error
        assert "not found" in out.error.lower() or "provider_error" in out.error

    def test_review_error_when_no_claude(self, monkeypatch):
        monkeypatch.setenv("PATH", "/nonexistent")
        provider = ClaudeCliProvider()
        out = provider.review("test prompt")
        assert out.error


# ---------------------------------------------------------------------------
# 18. Non-zero claude-cli blocks honestly
# ---------------------------------------------------------------------------

class TestNonZeroClaudeCli:
    def test_build_captures_error(self, monkeypatch, fake_claude_failing_bin):
        monkeypatch.setenv("PATH", str(fake_claude_failing_bin))
        provider = ClaudeCliProvider()
        out = provider.build("Fix something")
        assert out.error
        assert "provider_error" in out.error

    def test_review_captures_error(self, monkeypatch, fake_claude_failing_bin):
        monkeypatch.setenv("PATH", str(fake_claude_failing_bin))
        provider = ClaudeCliProvider()
        out = provider.review("Review something")
        assert out.error


# ---------------------------------------------------------------------------
# 19. Timeout claude-cli blocks honestly
# ---------------------------------------------------------------------------

class TestTimeoutClaudeCli:
    def test_build_timeout(self, monkeypatch, tmp_path):
        bin_dir = tmp_path / "slow_bin"
        bin_dir.mkdir()
        claude_script = bin_dir / "claude"
        claude_script.write_text("#!/bin/bash\nsleep 30\n")
        claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
        monkeypatch.setenv("PATH", str(bin_dir))
        provider = ClaudeCliProvider()
        out = provider.build("test", timeout_sec=1)
        assert out.error
        assert "timeout" in out.error.lower() or "provider_error" in out.error


# ---------------------------------------------------------------------------
# 20. Malformed reviewer JSON blocks honestly
# ---------------------------------------------------------------------------

class TestMalformedReviewerOutput:
    def test_malformed_review_blocks(self, demo_repo):
        provider = FakeProvider(malformed_review=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        assert result.final_status == "review_failed"
        assert "malformed" in result.error.lower()


# ---------------------------------------------------------------------------
# 21. Context still excludes secrets
# ---------------------------------------------------------------------------

class TestContextSafety:
    def test_no_env_secrets_in_context(self, demo_repo):
        from packages.orchestration.pingpong_loop import build_repo_context
        context, categories = build_repo_context(str(demo_repo), "Fix something")
        assert "secret123" not in context
        assert "API_KEY" not in context
        assert ".env" not in context.split("\n")


# ---------------------------------------------------------------------------
# 22. Fake-provider E2E still passes
# ---------------------------------------------------------------------------

class TestFakeProviderE2E:
    def test_fake_provider_full_loop(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.final_status == "staged_review_passed"
        assert len(result.rounds) >= 2
        assert result.target_mutated is False
        assert result.changed_target_files == []
        assert len(result.staged_files) > 0

    def test_summary_references_do_report(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        summary = summarize_pingpong(result)
        assert "remedy do report" in summary
        assert result.run_id in summary
        assert "remedy job report" not in summary


# ---------------------------------------------------------------------------
# 23. Existing staged fulfillment tests contract
# ---------------------------------------------------------------------------

class TestStagedFulfillmentContract:
    def test_staged_mode_no_target_mutation(self, demo_repo):
        original_readme = (demo_repo / "README.md").read_text()
        run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert (demo_repo / "README.md").read_text() == original_readme

    def test_run_has_id_and_timestamps(self, demo_repo):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.run_id
        assert len(result.run_id) == 16
        assert result.started_at
        assert result.finished_at


# ---------------------------------------------------------------------------
# REGRESSION: exact primary-review bug reproduction
# ---------------------------------------------------------------------------

class TestPrimaryReviewBugReproduction:
    def test_fake_claude_cwd_write_to_target_blocked(self, monkeypatch, demo_repo, fake_claude_target_mutator_bin, fake_claude_reviewer_bin):
        """Reproduce: fake claude writes CLI_MUTATED_TARGET.txt to target.
        Old code: final_status=staged_review_passed, target_mutated=false.
        New code: final_status=target_mutation_blocked, target_mutated=true.
        """
        monkeypatch.setenv("PATH", f"{fake_claude_target_mutator_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        # The file was written to target by the malicious fake claude
        assert (demo_repo / "CLI_MUTATED_TARGET.txt").exists()
        # But Remedy caught it
        assert result.target_mutated is True
        assert result.final_status == "target_mutation_blocked"
        assert "CLI_MUTATED_TARGET.txt" in str(result.changed_target_files)
        # Must NOT claim pass
        assert result.final_status != "staged_review_passed"


# ---------------------------------------------------------------------------
# Provider factory
# ---------------------------------------------------------------------------

class TestProviderFactory:
    def test_create_fake(self):
        p = create_provider("fake")
        assert p.name == "fake"

    def test_create_claude_cli(self):
        p = create_provider("claude-cli")
        assert p.name == "claude-cli"

    def test_unknown_raises(self):
        with pytest.raises(RuntimeError, match="Unknown provider"):
            create_provider("nonexistent")


# ---------------------------------------------------------------------------
# Keep staging
# ---------------------------------------------------------------------------

class TestKeepStaging:
    def test_keep_staging_preserves_dir(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            keep_staging=True,
        )
        staging_path = Path(f"/tmp/remedy-pingpong-{result.run_id}")
        assert staging_path.exists()
        # Cleanup
        import shutil
        shutil.rmtree(staging_path, ignore_errors=True)
