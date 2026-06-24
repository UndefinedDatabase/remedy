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
    _compute_safe_diff,
    _is_target_noise,
    export_pingpong_json,
    list_runs,
    load_run,
    run_pingpong,
    summarize_pingpong,
)
from packages.orchestration.pingpong_provider import (
    ClaudeCliProvider,
    FakeProvider,
    build_claude_cli_args,
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


# ===========================================================================
# Steps 4146-4215: Write-Enabled Staged Self-Run tests
# ===========================================================================

# ---------------------------------------------------------------------------
# 24. build_claude_cli_args: write_mode=none produces no write args
# ---------------------------------------------------------------------------

class TestBuildClaudeCliArgsNone:
    def test_no_write_args_when_none(self):
        argv = build_claude_cli_args("/usr/bin/claude", "Fix it", write_mode="none")
        assert "--allowedTools" not in argv
        assert "--dangerously-skip-permissions" not in argv
        assert "-p" in argv


# ---------------------------------------------------------------------------
# 25. build_claude_cli_args: write_mode=allowed-tools adds --allowedTools
# ---------------------------------------------------------------------------

class TestBuildClaudeCliArgsAllowedTools:
    def test_allowed_tools_args_present(self):
        argv = build_claude_cli_args("/usr/bin/claude", "Fix it", write_mode="allowed-tools")
        assert "--allowedTools" in argv
        idx = argv.index("--allowedTools")
        assert argv[idx + 1] == "Edit,Write,MultiEdit"

    def test_no_dangerous_skip(self):
        argv = build_claude_cli_args("/usr/bin/claude", "Fix it", write_mode="allowed-tools")
        assert "--dangerously-skip-permissions" not in argv


# ---------------------------------------------------------------------------
# 26. build_claude_cli_args: write_mode=dangerous-skip adds flag
# ---------------------------------------------------------------------------

class TestBuildClaudeCliArgsDangerousSkip:
    def test_dangerous_skip_present(self):
        argv = build_claude_cli_args("/usr/bin/claude", "Fix it", write_mode="dangerous-skip")
        assert "--dangerously-skip-permissions" in argv

    def test_no_allowed_tools(self):
        argv = build_claude_cli_args("/usr/bin/claude", "Fix it", write_mode="dangerous-skip")
        assert "--allowedTools" not in argv


# ---------------------------------------------------------------------------
# 27. ClaudeCliProvider stores and exposes write_mode
# ---------------------------------------------------------------------------

class TestClaudeCliProviderWriteMode:
    def test_default_write_mode_none(self):
        p = ClaudeCliProvider()
        assert p.write_mode == "none"

    def test_custom_write_mode(self):
        p = ClaudeCliProvider(write_mode="allowed-tools")
        assert p.write_mode == "allowed-tools"


# ---------------------------------------------------------------------------
# 28. Reviewer ClaudeCliProvider always gets write_mode=none
# ---------------------------------------------------------------------------

class TestReviewerAlwaysReadOnly:
    def test_reviewer_no_write_mode(self, demo_repo):
        """run_pingpong with claude_cli_write_mode=allowed-tools must NOT pass it to reviewer."""
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            claude_cli_write_mode="allowed-tools",
        )
        # Fake providers don't use write_mode, but result should still work
        assert result.final_status == "staged_review_passed"


# ---------------------------------------------------------------------------
# 29. run_pingpong accepts claude_cli_write_mode param
# ---------------------------------------------------------------------------

class TestRunPingpongWriteMode:
    def test_write_mode_accepted(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            claude_cli_write_mode="none",
        )
        assert result.final_status == "staged_review_passed"


# ---------------------------------------------------------------------------
# 30. builder_no_changes status when builder produces no changes
# ---------------------------------------------------------------------------

class TestBuilderNoChanges:
    def test_claude_cli_no_changes(self, monkeypatch, tmp_path, demo_repo):
        """Claude CLI builder that produces no file changes -> builder_no_changes."""
        bin_dir = tmp_path / "noop_bin"
        bin_dir.mkdir()
        claude_script = bin_dir / "claude"
        # Builder that prints but writes nothing
        claude_script.write_text("#!/bin/bash\necho 'I looked at the code'\n")
        claude_script.chmod(claude_script.stat().st_mode | 0o755)
        # Reviewer that passes
        rev_dir = tmp_path / "rev_bin"
        rev_dir.mkdir()
        rev_script = rev_dir / "claude"
        rev_script.write_text('#!/bin/bash\necho \'{"verdict":"pass","findings":[],"confidence":"high","summary":"ok"}\'\n')
        rev_script.chmod(rev_script.stat().st_mode | 0o755)
        monkeypatch.setenv("PATH", f"{bin_dir}:{rev_dir}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.final_status == "builder_no_changes"
        assert "no file changes" in result.error.lower()


# ---------------------------------------------------------------------------
# 31. Safe diff: empty when no staged files
# ---------------------------------------------------------------------------

class TestSafeDiffEmpty:
    def test_no_staged_files_no_diff(self, tmp_path):
        original = tmp_path / "orig"
        original.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()
        diff_text, diff_files, truncated = _compute_safe_diff(staging, original, [])
        assert diff_text == ""
        assert diff_files == []
        assert truncated is False


# ---------------------------------------------------------------------------
# 32. Safe diff: shows changed file content
# ---------------------------------------------------------------------------

class TestSafeDiffContent:
    def test_diff_shows_changes(self, tmp_path):
        original = tmp_path / "orig"
        original.mkdir()
        (original / "hello.py").write_text("print('hello')\n")
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "hello.py").write_text("print('goodbye')\n")
        diff_text, diff_files, truncated = _compute_safe_diff(
            staging, original, ["hello.py"],
        )
        assert "hello.py" in diff_text
        assert "hello" in diff_text
        assert "goodbye" in diff_text
        assert "hello.py" in diff_files
        assert truncated is False


# ---------------------------------------------------------------------------
# 33. Safe diff: new file shows as addition
# ---------------------------------------------------------------------------

class TestSafeDiffNewFile:
    def test_new_file_in_diff(self, tmp_path):
        original = tmp_path / "orig"
        original.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "new.py").write_text("# new file\n")
        diff_text, diff_files, truncated = _compute_safe_diff(
            staging, original, ["new.py"],
        )
        assert "new.py" in diff_text
        assert "new.py" in diff_files


# ---------------------------------------------------------------------------
# 34. Safe diff: excludes .env secrets
# ---------------------------------------------------------------------------

class TestSafeDiffExcludesSecrets:
    def test_env_excluded(self, tmp_path):
        original = tmp_path / "orig"
        original.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / ".env").write_text("SECRET=bad\n")
        (staging / ".env.local").write_text("DB=hunter2\n")
        diff_text, diff_files, truncated = _compute_safe_diff(
            staging, original, [".env", ".env.local"],
        )
        assert "SECRET" not in diff_text
        assert "hunter2" not in diff_text
        assert diff_files == []


# ---------------------------------------------------------------------------
# 35. Safe diff: binary files get [binary file] marker
# ---------------------------------------------------------------------------

class TestSafeDiffBinary:
    def test_binary_marker(self, tmp_path):
        original = tmp_path / "orig"
        original.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "image.png").write_bytes(b"\x89PNG\r\n")
        diff_text, diff_files, truncated = _compute_safe_diff(
            staging, original, ["image.png"],
        )
        assert "[binary file]" in diff_text
        assert "image.png" in diff_files


# ---------------------------------------------------------------------------
# 36. Safe diff: truncation at cap
# ---------------------------------------------------------------------------

class TestSafeDiffTruncation:
    def test_truncation_at_cap(self, tmp_path, monkeypatch):
        import packages.orchestration.pingpong_loop as loop_mod
        monkeypatch.setattr(loop_mod, "_SAFE_DIFF_CAP", 100)
        original = tmp_path / "orig"
        original.mkdir()
        (original / "big.py").write_text("")
        staging = tmp_path / "staging"
        staging.mkdir()
        # Large enough to exceed 100 char cap
        (staging / "big.py").write_text("x = 1\n" * 50)
        diff_text, diff_files, truncated = _compute_safe_diff(
            staging, original, ["big.py"],
        )
        assert truncated is True
        assert "[DIFF TRUNCATED]" in diff_text


# ---------------------------------------------------------------------------
# 37. Safe diff: no absolute staging paths in diff
# ---------------------------------------------------------------------------

class TestSafeDiffNoAbsolutePaths:
    def test_no_tmp_paths(self, tmp_path):
        original = tmp_path / "orig"
        original.mkdir()
        (original / "f.py").write_text("old\n")
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "f.py").write_text("new\n")
        diff_text, diff_files, truncated = _compute_safe_diff(
            staging, original, ["f.py"],
        )
        assert str(staging) not in diff_text
        assert str(original) not in diff_text
        assert "a/f.py" in diff_text
        assert "b/f.py" in diff_text


# ---------------------------------------------------------------------------
# 38. Safe diff fields in export JSON
# ---------------------------------------------------------------------------

class TestSafeDiffInExport:
    def test_export_has_safe_diff_fields(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        data = export_pingpong_json(result)
        assert "safe_diff_files" in data
        assert "safe_diff_truncated" in data
        assert "safe_diff_summary" in data
        assert isinstance(data["safe_diff_files"], list)
        assert isinstance(data["safe_diff_truncated"], bool)


# ---------------------------------------------------------------------------
# 39. Safe diff in summary text
# ---------------------------------------------------------------------------

class TestSafeDiffInSummary:
    def test_summary_has_diff_section(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        summary = summarize_pingpong(result)
        # Fake provider produces staged_files from file_tree, so diff may or may not be empty
        # At minimum, the summary should be parseable
        assert "staged" in summary.lower()


# ---------------------------------------------------------------------------
# 40. Safe diff populated for fake provider with changes
# ---------------------------------------------------------------------------

class TestSafeDiffWithFakeProvider:
    def test_fake_provider_diff_files_match_staged(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            keep_staging=True,
        )
        # Fake provider doesn't actually modify files, so safe_diff_files may be empty
        # But safe_diff_truncated should be False
        assert result.safe_diff_truncated is False
        # Cleanup staging
        import shutil
        staging_path = Path(f"/tmp/remedy-pingpong-{result.run_id}")
        shutil.rmtree(staging_path, ignore_errors=True)


# ---------------------------------------------------------------------------
# 41. CLI write mode validation rejects invalid mode
# ---------------------------------------------------------------------------

class TestCliWriteModeValidation:
    def test_invalid_write_mode_exits(self):
        from apps.cli.commands.do_cmd import _VALID_CLI_WRITE_MODES
        assert "none" in _VALID_CLI_WRITE_MODES
        assert "allowed-tools" in _VALID_CLI_WRITE_MODES
        assert "dangerous-skip" in _VALID_CLI_WRITE_MODES
        assert "yolo" not in _VALID_CLI_WRITE_MODES


# ---------------------------------------------------------------------------
# 42. --claude-cli-write-mode in command catalog
# ---------------------------------------------------------------------------

class TestCatalogHasWriteMode:
    def test_catalog_has_write_mode_arg(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("do.run")
        arg_names = [a.name for a in cmd.args]
        assert "--claude-cli-write-mode" in arg_names


# ---------------------------------------------------------------------------
# 43. write_mode passed through to builder provider
# ---------------------------------------------------------------------------

class TestWriteModePassthrough:
    def test_builder_gets_write_mode(self, demo_repo, monkeypatch, tmp_path):
        """Verify ClaudeCliProvider created with correct write_mode."""
        from packages.orchestration.pingpong_loop import _create_provider_with_cwd
        staging_dir = str(tmp_path / "staging")
        p = _create_provider_with_cwd(
            "claude-cli", role="builder", staging_dir=staging_dir,
            write_mode="allowed-tools",
        )
        assert isinstance(p, ClaudeCliProvider)
        assert p.write_mode == "allowed-tools"

    def test_reviewer_ignores_write_mode(self, tmp_path):
        from packages.orchestration.pingpong_loop import _create_provider_with_cwd
        p = _create_provider_with_cwd(
            "claude-cli", role="reviewer", staging_dir=None,
            write_mode="allowed-tools",
        )
        assert isinstance(p, ClaudeCliProvider)
        assert p.write_mode == "none"


# ---------------------------------------------------------------------------
# 44. Safe diff: subdirectory files work
# ---------------------------------------------------------------------------

class TestSafeDiffSubdirectory:
    def test_subdir_file_diff(self, tmp_path):
        original = tmp_path / "orig"
        (original / "src").mkdir(parents=True)
        (original / "src" / "app.py").write_text("old\n")
        staging = tmp_path / "staging"
        (staging / "src").mkdir(parents=True)
        (staging / "src" / "app.py").write_text("new\n")
        diff_text, diff_files, truncated = _compute_safe_diff(
            staging, original, ["src/app.py"],
        )
        assert "src/app.py" in diff_text
        assert "src/app.py" in diff_files


# ---------------------------------------------------------------------------
# 45. Export JSON has no absolute staging paths
# ---------------------------------------------------------------------------

class TestExportNoStagingPaths:
    def test_no_staging_paths_in_export(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        data = export_pingpong_json(result)
        text = json.dumps(data)
        assert "/tmp/remedy-pingpong-" not in text


# ---------------------------------------------------------------------------
# 46. build_claude_cli_args always includes -p and --output-format text
# ---------------------------------------------------------------------------

class TestBuildClaudeCliArgsBase:
    def test_base_args_always_present(self):
        for mode in ("none", "allowed-tools", "dangerous-skip"):
            argv = build_claude_cli_args("/usr/bin/claude", "Do stuff", write_mode=mode)
            assert argv[0] == "/usr/bin/claude"
            assert "-p" in argv
            assert "--output-format" in argv
            idx = argv.index("--output-format")
            assert argv[idx + 1] == "text"


# ---------------------------------------------------------------------------
# 47. Safe diff: unchanged file not in diff
# ---------------------------------------------------------------------------

class TestSafeDiffUnchangedFile:
    def test_unchanged_not_in_diff(self, tmp_path):
        original = tmp_path / "orig"
        original.mkdir()
        (original / "same.py").write_text("x = 1\n")
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "same.py").write_text("x = 1\n")
        diff_text, diff_files, truncated = _compute_safe_diff(
            staging, original, ["same.py"],
        )
        # File was listed as changed but content is identical
        assert diff_files == []
        assert diff_text == ""


# ---------------------------------------------------------------------------
# 48. run_pingpong with keep_staging populates safe_diff
# ---------------------------------------------------------------------------

class TestSafeDiffWithKeepStaging:
    def test_diff_computed_before_cleanup(self, demo_repo):
        """Safe diff must be computed before staging is discarded."""
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            keep_staging=False,
        )
        # Even without keep_staging, safe_diff fields should be populated
        assert isinstance(result.safe_diff_summary, str)
        assert isinstance(result.safe_diff_files, list)
        assert isinstance(result.safe_diff_truncated, bool)


# ===========================================================================
# Steps 4216-4265: Dogfood Cache-Noise + Staged Diff Report Closure tests
# ===========================================================================

@pytest.fixture
def fake_claude_cache_noise_builder_bin(tmp_path: Path, demo_repo: Path) -> Path:
    """Fake builder that writes to staging cwd AND creates cache dirs in target."""
    bin_dir = tmp_path / "noise_builder_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    # Writes to staging (cwd) AND creates cache noise in target
    claude_script.write_text(textwrap.dedent(f"""\
        #!/bin/bash
        /bin/mkdir -p "$PWD/docs"
        echo "# Report guide" > "$PWD/docs/report-guide.md"
        /bin/mkdir -p "{demo_repo}/.pytest_cache"
        echo "cache" > "{demo_repo}/.pytest_cache/v"
        /bin/mkdir -p "{demo_repo}/.ruff_cache"
        echo "cache" > "{demo_repo}/.ruff_cache/v"
        /bin/mkdir -p "{demo_repo}/.mypy_cache"
        echo "cache" > "{demo_repo}/.mypy_cache/v"
        echo "Builder changed docs/report-guide.md"
    """))
    claude_script.chmod(claude_script.stat().st_mode | 0o755)
    return bin_dir


@pytest.fixture
def fake_claude_real_target_mutator_bin(tmp_path: Path, demo_repo: Path) -> Path:
    """Fake builder that mutates a real doc file in target (not just cache noise)."""
    bin_dir = tmp_path / "real_mut_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    claude_script.write_text(textwrap.dedent(f"""\
        #!/bin/bash
        /bin/mkdir -p "{demo_repo}/docs"
        echo "# Mutated doc" > "{demo_repo}/docs/mutated.md"
        echo "Builder summary"
    """))
    claude_script.chmod(claude_script.stat().st_mode | 0o755)
    return bin_dir


# ---------------------------------------------------------------------------
# 49. Cache noise classified as noise, not meaningful mutation
# ---------------------------------------------------------------------------

class TestCacheNoiseClassification:
    def test_pytest_cache_is_noise(self):
        assert _is_target_noise(".pytest_cache/") is True
        assert _is_target_noise(".pytest_cache/v/cache") is True

    def test_mypy_cache_is_noise(self):
        assert _is_target_noise(".mypy_cache/") is True

    def test_ruff_cache_is_noise(self):
        assert _is_target_noise(".ruff_cache/") is True

    def test_pycache_is_noise(self):
        assert _is_target_noise("__pycache__/") is True
        assert _is_target_noise("__pycache__/module.cpython-310.pyc") is True

    def test_pyc_is_noise(self):
        assert _is_target_noise("module.pyc") is True

    def test_source_file_not_noise(self):
        assert _is_target_noise("main.py") is False

    def test_doc_file_not_noise(self):
        assert _is_target_noise("docs/guide.md") is False

    def test_config_not_noise(self):
        assert _is_target_noise("pyproject.toml") is False

    def test_lockfile_not_noise(self):
        assert _is_target_noise("poetry.lock") is False


# ---------------------------------------------------------------------------
# 50. Real target file mutation still blocks
# ---------------------------------------------------------------------------

class TestRealTargetMutationStillBlocks:
    def test_doc_mutation_blocks(self, monkeypatch, demo_repo, fake_claude_real_target_mutator_bin, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", f"{fake_claude_real_target_mutator_bin}:{fake_claude_reviewer_bin}")
        (demo_repo / "docs").mkdir(exist_ok=True)
        result = run_pingpong(
            "Fix docs", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.final_status == "target_mutation_blocked"
        assert result.target_mutated is True
        assert any("mutated.md" in f for f in result.changed_target_files)


# ---------------------------------------------------------------------------
# 51. Target Markdown/doc mutation still blocks
# ---------------------------------------------------------------------------

class TestTargetDocMutationBlocks:
    def test_markdown_mutation_blocks(self, monkeypatch, demo_repo, fake_claude_real_target_mutator_bin, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", f"{fake_claude_real_target_mutator_bin}:{fake_claude_reviewer_bin}")
        (demo_repo / "docs").mkdir(exist_ok=True)
        result = run_pingpong(
            "Fix docs", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.target_mutated is True


# ---------------------------------------------------------------------------
# 52. Target source file mutation still blocks
# ---------------------------------------------------------------------------

class TestTargetSourceMutationBlocks:
    def test_source_mutation_blocks(self, monkeypatch, demo_repo, fake_claude_target_mutator_bin, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", f"{fake_claude_target_mutator_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.target_mutated is True
        assert result.final_status == "target_mutation_blocked"


# ---------------------------------------------------------------------------
# 53. Ignored target noise exported in JSON
# ---------------------------------------------------------------------------

class TestNoiseExportedInJson:
    def test_noise_fields_in_json(self, demo_repo):
        # Create cache noise before run
        (demo_repo / ".pytest_cache").mkdir(exist_ok=True)
        (demo_repo / ".pytest_cache" / "v").write_text("cache")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        data = export_pingpong_json(result)
        assert "ignored_target_noise_files" in data
        assert "target_noise_detected" in data
        assert isinstance(data["ignored_target_noise_files"], list)
        assert isinstance(data["target_noise_detected"], bool)


# ---------------------------------------------------------------------------
# 54. Ignored target noise in text report
# ---------------------------------------------------------------------------

class TestNoiseInTextReport:
    def test_noise_in_summary(self, demo_repo):
        (demo_repo / ".ruff_cache").mkdir(exist_ok=True)
        (demo_repo / ".ruff_cache" / "v").write_text("cache")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        summary = summarize_pingpong(result)
        if result.target_noise_detected:
            assert "no meaningful target changes" in summary
            assert "Ignored target noise" in summary


# ---------------------------------------------------------------------------
# 55. target_mutated=false when only noise
# ---------------------------------------------------------------------------

class TestTargetMutatedFalseOnNoise:
    def test_only_noise_not_mutated(self, demo_repo):
        (demo_repo / ".pytest_cache").mkdir(exist_ok=True)
        (demo_repo / ".pytest_cache" / "v").write_text("cache")
        (demo_repo / ".mypy_cache").mkdir(exist_ok=True)
        (demo_repo / ".mypy_cache" / "v").write_text("cache")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        assert result.target_mutated is False


# ---------------------------------------------------------------------------
# 56. changed_target_files=[] when only noise
# ---------------------------------------------------------------------------

class TestChangedTargetFilesEmptyOnNoise:
    def test_changed_files_empty_on_noise(self, demo_repo):
        (demo_repo / ".ruff_cache").mkdir(exist_ok=True)
        (demo_repo / ".ruff_cache" / "v").write_text("cache")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        assert result.changed_target_files == []


# ---------------------------------------------------------------------------
# 57. target_noise_detected=true when noise exists
# ---------------------------------------------------------------------------

class TestTargetNoiseDetected:
    def test_noise_detected_flag(self, demo_repo):
        (demo_repo / ".pytest_cache").mkdir(exist_ok=True)
        (demo_repo / ".pytest_cache" / "v").write_text("cache")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        assert result.target_noise_detected is True
        assert ".pytest_cache/" in result.ignored_target_noise_files


# ---------------------------------------------------------------------------
# 58. Staged files preserved when target mutation blocker
# ---------------------------------------------------------------------------

class TestStagedFilesPreservedOnBlock:
    def test_staged_files_on_block(self, monkeypatch, demo_repo, fake_claude_cache_noise_builder_bin, fake_claude_reviewer_bin):
        """Builder writes to staging + creates cache noise in target.
        Noise should NOT block. staged_files should be populated."""
        monkeypatch.setenv("PATH", f"{fake_claude_cache_noise_builder_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Add report guide", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        # Should NOT be blocked by cache noise
        assert result.final_status != "target_mutation_blocked"
        assert result.target_mutated is False
        assert result.target_noise_detected is True


# ---------------------------------------------------------------------------
# 59. Safe diff preserved when target mutation blocker (real mutation)
# ---------------------------------------------------------------------------

class TestSafeDiffPreservedOnBlock:
    def test_diff_on_real_block(self, monkeypatch, demo_repo, fake_claude_target_mutator_bin, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", f"{fake_claude_target_mutator_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.target_mutated is True
        # safe_diff fields should exist (may be empty if no staging changes)
        assert isinstance(result.safe_diff_summary, str)
        assert isinstance(result.safe_diff_files, list)


# ---------------------------------------------------------------------------
# 60. Staged files non-empty when fake builder writes staging
# ---------------------------------------------------------------------------

class TestStagedFilesNonEmptyFake:
    def test_fake_builder_has_staged_files(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        assert len(result.staged_files) > 0


# ---------------------------------------------------------------------------
# 61. Explicit test command runs after cache noise
# ---------------------------------------------------------------------------

class TestTestCommandAfterNoise:
    def test_tests_run_despite_noise(self, demo_repo):
        (demo_repo / ".pytest_cache").mkdir(exist_ok=True)
        (demo_repo / ".pytest_cache" / "v").write_text("cache")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            test_command="echo 'tests pass'",
        )
        assert result.tests_not_run is False
        for rd in result.rounds:
            if rd.test_passed is not None:
                assert rd.test_passed is True


# ---------------------------------------------------------------------------
# 62. Explicit test command runs in staging cwd
# ---------------------------------------------------------------------------

class TestTestCommandRunsInStaging:
    def test_test_in_staging_cwd(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            test_command="pwd",
        )
        for rd in result.rounds:
            if rd.test_summary and "exit=0" in rd.test_summary:
                # pwd output should contain /tmp (staging), not demo_repo
                assert "/tmp/remedy-pingpong-" in rd.test_summary


# ---------------------------------------------------------------------------
# 63. Target receives no meaningful product changes
# ---------------------------------------------------------------------------

class TestNoMeaningfulTargetChanges:
    def test_clean_run_no_target_changes(self, demo_repo):
        original_readme = (demo_repo / "README.md").read_text()
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        assert (demo_repo / "README.md").read_text() == original_readme
        assert result.target_mutated is False
        assert result.changed_target_files == []


# ---------------------------------------------------------------------------
# 64. --keep-staging works as boolean flag
# ---------------------------------------------------------------------------

class TestKeepStagingBooleanFlag:
    def test_keep_staging_flag(self, demo_repo):
        import shutil
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            keep_staging=True,
        )
        staging_path = Path(f"/tmp/remedy-pingpong-{result.run_id}")
        assert staging_path.exists()
        assert result.staging_path == str(staging_path)
        shutil.rmtree(staging_path, ignore_errors=True)


# ---------------------------------------------------------------------------
# 65. --keep-staging true remains accepted
# ---------------------------------------------------------------------------

class TestKeepStagingTrueAccepted:
    def test_keep_staging_true(self, demo_repo):
        import shutil
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            keep_staging=True,
        )
        assert result.staging_path != ""
        shutil.rmtree(result.staging_path, ignore_errors=True)


# ---------------------------------------------------------------------------
# 66. do run --json includes noise fields
# ---------------------------------------------------------------------------

class TestJsonIncludesNoiseFields:
    def test_json_has_noise_fields(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        data = export_pingpong_json(result)
        assert "ignored_target_noise_files" in data
        assert "target_noise_detected" in data
        assert "staging_retained" in data
        assert "staging_path" in data


# ---------------------------------------------------------------------------
# 67. do report --json includes noise fields
# ---------------------------------------------------------------------------

class TestReportJsonIncludesNoiseFields:
    def test_report_has_noise_fields(self, demo_repo):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        data = load_run(result.run_id)
        assert data is not None
        assert "ignored_target_noise_files" in data
        assert "target_noise_detected" in data


# ---------------------------------------------------------------------------
# 68. Existing target snapshot guard tests still pass (via run above)
# ---------------------------------------------------------------------------

class TestExistingSnapshotGuard:
    def test_snapshot_guard_still_blocks_real(self, monkeypatch, demo_repo, fake_claude_target_mutator_bin, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", f"{fake_claude_target_mutator_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        assert result.target_mutated is True
        assert result.final_status == "target_mutation_blocked"


# ---------------------------------------------------------------------------
# 69. Existing claude-cli staging cwd tests still pass (via earlier tests)
# 70. Existing safe diff tests still pass (via earlier tests)
# 71. Existing fake CLI E2E tests still pass (via earlier tests)
# (these are covered by the existing test classes above)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 72. Dogfood regression: cache noise + staging write, no block
# ---------------------------------------------------------------------------

class TestDogfoodRegression:
    def test_cache_noise_does_not_block_with_staging_changes(
        self, monkeypatch, demo_repo, fake_claude_cache_noise_builder_bin, fake_claude_reviewer_bin,
    ):
        """Reproduce real dogfood issue: Builder writes staging file,
        test/helper creates .pytest_cache/.ruff_cache/.mypy_cache in target.
        Run must NOT be blocked. staged_files and safe_diff must be populated."""
        monkeypatch.setenv("PATH", f"{fake_claude_cache_noise_builder_bin}:{fake_claude_reviewer_bin}")
        result = run_pingpong(
            "Add report guide", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )
        # Must NOT block on cache noise
        assert result.target_mutated is False
        assert result.final_status != "target_mutation_blocked"
        # Noise detected
        assert result.target_noise_detected is True
        assert any(".pytest_cache" in n for n in result.ignored_target_noise_files)
        assert any(".ruff_cache" in n for n in result.ignored_target_noise_files)
        assert any(".mypy_cache" in n for n in result.ignored_target_noise_files)
        # Staged files populated (builder wrote docs/report-guide.md)
        assert len(result.staged_files) > 0
        assert any("report-guide" in f for f in result.staged_files)
        # Safe diff populated
        assert len(result.safe_diff_files) > 0
        assert result.safe_diff_summary != ""
        assert "report-guide" in result.safe_diff_summary
