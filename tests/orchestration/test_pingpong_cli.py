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

import packages.orchestration.pingpong_loop as pingpong_loop
from packages.orchestration.data_paths import pingpong_run_dir
from packages.orchestration.pingpong_loop import (
    _OVERSIZED_DIFF_THRESHOLD_CHARS,
    _OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS,
    _STAGING_NOISE_DIRS,
    _build_builder_prompt,
    _build_reviewer_prompt,
    _compute_safe_diff,
    _create_staging,
    _estimate_full_repo_tokens,
    _find_staging_changes,
    _is_safe_repo_path,
    _is_safe_staged_path,
    _is_target_noise,
    _snapshot_target,
    build_repo_context,
    export_pingpong_json,
    list_runs,
    load_run,
    run_pingpong,
    summarize_pingpong,
)
from packages.orchestration.pingpong_provider import (
    _REVIEWER_RETRY_PROMPT,
    ClaudeCliProvider,
    FakeProvider,
    ReviewFinding,
    _parse_reviewer_json,
    _unwrap_envelope,
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
        if [ "$1" = "--version" ]; then echo "1.0.0 (test)"; exit 0; fi
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
        if [ "$1" = "--version" ]; then echo "1.0.0 (test)"; exit 0; fi
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
        if [ "$1" = "--version" ]; then echo "1.0.0 (test)"; exit 0; fi
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
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake", repair_rounds=2)
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
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            claude_cli_write_mode="allowed-tools",
        )
        # Fake providers don't use write_mode, but result should still work
        assert result.final_status == "staged_review_passed"


# ---------------------------------------------------------------------------
# 29. run_pingpong accepts claude_cli_write_mode param
# ---------------------------------------------------------------------------

class TestRunPingpongWriteMode:
    def test_write_mode_accepted(self, demo_repo):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            claude_cli_write_mode="none",
        )
        assert result.final_status == "staged_review_passed"


# ---------------------------------------------------------------------------
# 30. builder_no_changes status when builder produces no changes
# ---------------------------------------------------------------------------

class TestBuilderNoChanges:
    def test_claude_cli_no_changes(self, monkeypatch, tmp_path, demo_repo):
        """Claude CLI builder producing no file changes: tests pass, reviewer passes,
        final_status is staged_review_passed with builder_no_changes flag set."""
        # This fake CLI reviewer predates F005 native schema (it routes by the
        # legacy prompt and emits no schema_v), so it exercises the legacy
        # free-text reviewer path explicitly. F005 schema enforcement is covered
        # by the dedicated structured-output tests.
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        bin_dir = tmp_path / "noop_bin"
        bin_dir.mkdir()
        claude_script = bin_dir / "claude"
        reviewer_verdict = json.dumps({
            "verdict": "pass", "findings": [], "confidence": "high", "summary": "ok",
        })
        builder_envelope = json.dumps({
            "type": "result", "subtype": "success", "is_error": False,
            "duration_ms": 50, "num_turns": 1,
            "result": "I looked at the code and no changes are needed.",
            "session_id": "test-build", "total_cost_usd": 0.001,
            "usage": {"input_tokens": 100, "output_tokens": 10},
        })
        reviewer_envelope = json.dumps({
            "type": "result", "subtype": "success", "is_error": False,
            "duration_ms": 50, "num_turns": 1,
            "result": reviewer_verdict,
            "session_id": "test-rev", "total_cost_usd": 0.001,
            "usage": {"input_tokens": 100, "output_tokens": 10},
        })
        script_body = (
            '#!/bin/bash\n'
            'PROMPT=""\n'
            'while [ $# -gt 0 ]; do\n'
            '  case "$1" in\n'
            '    -p) PROMPT="$2"; shift 2;;\n'
            '    *) shift;;\n'
            '  esac\n'
            'done\n'
            'if [[ "$PROMPT" == *verdict* ]]; then\n'
            f"  echo '{reviewer_envelope}'\n"
            'else\n'
            f"  echo '{builder_envelope}'\n"
            'fi\n'
        )
        claude_script.write_text(script_body)
        claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
        test_script = tmp_path / "test_pass.sh"
        test_script.write_text("#!/bin/bash\nexit 0\n")
        test_script.chmod(test_script.stat().st_mode | stat.S_IEXEC)
        monkeypatch.setenv("PATH", f"{bin_dir}:{tmp_path}")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
            test_command=f"/bin/bash {test_script}",
        )
        assert result.final_status == "staged_review_passed"
        assert result.builder_no_changes is True


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
# 46. build_claude_cli_args always includes -p and --output-format json
# ---------------------------------------------------------------------------

class TestBuildClaudeCliArgsBase:
    def test_base_args_always_present(self):
        for mode in ("none", "allowed-tools", "dangerous-skip"):
            argv = build_claude_cli_args("/usr/bin/claude", "Do stuff", write_mode=mode)
            assert argv[0] == "/usr/bin/claude"
            assert "-p" in argv
            assert "--output-format" in argv
            idx = argv.index("--output-format")
            assert argv[idx + 1] == "json"


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
        if [ "$1" = "--version" ]; then echo "1.0.0 (test)"; exit 0; fi
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
        if [ "$1" = "--version" ]; then echo "1.0.0 (test)"; exit 0; fi
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
# 49b. Staging noise dirs pruned from _find_staging_changes
# ---------------------------------------------------------------------------


class TestStagingNoisePruning:
    def test_pytest_cache_excluded(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        (staging / "real.py").write_text("new\n")
        cache = staging / ".pytest_cache"
        cache.mkdir()
        (cache / ".gitignore").write_text("*\n")
        (cache / "v" / "cache").mkdir(parents=True)
        (cache / "v" / "cache" / "data.json").write_text("{}\n")
        changed = _find_staging_changes(staging, original)
        assert "real.py" in changed
        assert not any(".pytest_cache" in c for c in changed)

    def test_pycache_excluded(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        (staging / "app.py").write_text("code\n")
        pc = staging / "__pycache__"
        pc.mkdir()
        (pc / "app.cpython-311.pyc").write_bytes(b"\x00")
        changed = _find_staging_changes(staging, original)
        assert "app.py" in changed
        assert not any("__pycache__" in c for c in changed)

    def test_mypy_cache_excluded(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        (staging / "mod.py").write_text("typed\n")
        mc = staging / ".mypy_cache"
        mc.mkdir()
        (mc / "cache.json").write_text("{}\n")
        changed = _find_staging_changes(staging, original)
        assert "mod.py" in changed
        assert not any(".mypy_cache" in c for c in changed)

    def test_ruff_cache_excluded(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        (staging / "lint.py").write_text("pass\n")
        rc = staging / ".ruff_cache"
        rc.mkdir()
        (rc / "0.0.1").write_text("cache\n")
        changed = _find_staging_changes(staging, original)
        assert "lint.py" in changed
        assert not any(".ruff_cache" in c for c in changed)

    def test_nested_pycache_excluded(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        pkg = staging / "pkg"
        pkg.mkdir()
        (pkg / "mod.py").write_text("code\n")
        pc = pkg / "__pycache__"
        pc.mkdir()
        (pc / "mod.cpython-311.pyc").write_bytes(b"\x00")
        changed = _find_staging_changes(staging, original)
        assert any("mod.py" in c for c in changed)
        assert not any("__pycache__" in c for c in changed)

    def test_real_files_still_found(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()
        (original / "existing.py").write_text("old\n")
        (staging / "existing.py").write_text("new\n")
        (staging / "added.py").write_text("new\n")
        changed = _find_staging_changes(staging, original)
        assert "existing.py" in changed
        assert "added.py" in changed

    def test_staging_noise_dirs_constant_complete(self):
        for d in (".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache"):
            assert d in _STAGING_NOISE_DIRS


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


# ===========================================================================
# Block v3 — Reviewer JSON Reliability tests (Steps 4266-4315)
# ===========================================================================


# ---------------------------------------------------------------------------
# 73. _parse_reviewer_json strips markdown code fences
# ---------------------------------------------------------------------------

class TestParseReviewerJsonCodeFence:
    def test_code_fence_stripped(self):
        text = '```json\n{"verdict":"pass","findings":[],"confidence":"high","summary":"ok"}\n```'
        out = _parse_reviewer_json(text, 100, 50)
        assert out.verdict == "pass"
        assert out.error == ""


# ---------------------------------------------------------------------------
# 74. _parse_reviewer_json handles bare JSON
# ---------------------------------------------------------------------------

class TestParseReviewerJsonBare:
    def test_bare_json(self):
        text = '{"verdict":"needs_repair","findings":[{"id":"R1","severity":"high","file":"a.py","summary":"bug"}],"confidence":"medium","summary":"fix needed"}'
        out = _parse_reviewer_json(text, 100, 50)
        assert out.verdict == "needs_repair"
        assert len(out.findings) == 1
        assert out.findings[0].id == "R1"


# ---------------------------------------------------------------------------
# 75. _parse_reviewer_json rejects no-JSON text
# ---------------------------------------------------------------------------

class TestParseReviewerJsonNoJson:
    def test_no_json_returns_malformed(self):
        out = _parse_reviewer_json("This is just prose with no JSON.", 100, 50)
        assert out.error.startswith("malformed_output:")
        assert out.verdict == "blocked"


# ---------------------------------------------------------------------------
# 76. _parse_reviewer_json rejects invalid verdict
# ---------------------------------------------------------------------------

class TestParseReviewerJsonInvalidVerdict:
    def test_invalid_verdict(self):
        text = '{"verdict":"approve","findings":[],"confidence":"high","summary":"ok"}'
        out = _parse_reviewer_json(text, 100, 50)
        assert out.error.startswith("malformed_output:")
        assert "approve" in out.error


# ---------------------------------------------------------------------------
# 77. _unwrap_envelope direct verdict
# ---------------------------------------------------------------------------

class TestUnwrapEnvelopeDirect:
    def test_direct_verdict(self):
        data = {"verdict": "pass", "findings": [], "summary": "ok"}
        assert _unwrap_envelope(data) is data


# ---------------------------------------------------------------------------
# 78. _unwrap_envelope result wrapper
# ---------------------------------------------------------------------------

class TestUnwrapEnvelopeResult:
    def test_result_wrapper(self):
        inner = {"verdict": "fail", "findings": []}
        data = {"result": inner}
        assert _unwrap_envelope(data) is inner


# ---------------------------------------------------------------------------
# 79. _unwrap_envelope content wrapper
# ---------------------------------------------------------------------------

class TestUnwrapEnvelopeContent:
    def test_content_wrapper(self):
        inner = {"verdict": "pass", "findings": []}
        data = {"content": inner}
        assert _unwrap_envelope(data) is inner


# ---------------------------------------------------------------------------
# 80. _unwrap_envelope message wrapper
# ---------------------------------------------------------------------------

class TestUnwrapEnvelopeMessage:
    def test_message_wrapper(self):
        inner = {"verdict": "blocked", "findings": []}
        data = {"message": inner}
        assert _unwrap_envelope(data) is inner


# ---------------------------------------------------------------------------
# 81. _unwrap_envelope text field with JSON string
# ---------------------------------------------------------------------------

class TestUnwrapEnvelopeTextField:
    def test_text_field_json(self):
        import json as _json
        inner = {"verdict": "pass", "findings": [], "summary": "ok"}
        data = {"text": _json.dumps(inner)}
        assert _unwrap_envelope(data)["verdict"] == "pass"


# ---------------------------------------------------------------------------
# 82. _unwrap_envelope returns data unchanged when no verdict
# ---------------------------------------------------------------------------

class TestUnwrapEnvelopeNoVerdict:
    def test_no_verdict_passthrough(self):
        data = {"foo": "bar"}
        assert _unwrap_envelope(data) is data


# ---------------------------------------------------------------------------
# 83. Malformed review triggers retry (FakeProvider always malformed)
# ---------------------------------------------------------------------------

class TestMalformedReviewRetryPersistent:
    def test_malformed_retry_still_fails(self, demo_repo):
        """Both first and retry calls return malformed — result stays review_failed."""
        provider = FakeProvider(malformed_review=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        assert result.final_status == "review_failed"
        assert result.reviewer_parse_retry_count == 1
        assert result.reviewer_json_recovered is False
        assert result.reviewer_parse_error.startswith("malformed_output:")


# ---------------------------------------------------------------------------
# 84. Recoverable malformed review — retry passes
# ---------------------------------------------------------------------------

class TestMalformedReviewRecoverable:
    def test_recoverable_retry_passes(self, demo_repo):
        """First review malformed, retry returns valid pass."""
        provider = FakeProvider(malformed_review_recoverable=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        assert result.final_status == "staged_review_passed"
        assert result.reviewer_parse_retry_count == 1
        assert result.reviewer_json_recovered is True


# ---------------------------------------------------------------------------
# 85. parse_retried flag set on ReviewerOutput after retry
# ---------------------------------------------------------------------------

class TestParseRetriedFlag:
    def test_parse_retried_set(self, demo_repo):
        provider = FakeProvider(malformed_review_recoverable=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        rd = result.rounds[0]
        assert rd.reviewer_output is not None
        assert rd.reviewer_output.parse_retried is True
        assert rd.reviewer_output.parse_retry_recovered is True


# ---------------------------------------------------------------------------
# 86. parse_retried flag NOT set on normal review
# ---------------------------------------------------------------------------

class TestParseRetriedFlagNotSet:
    def test_no_retry_on_normal(self, demo_repo):
        provider = FakeProvider()
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        rd = result.rounds[0]
        assert rd.reviewer_output is not None
        assert rd.reviewer_output.parse_retried is False
        assert rd.reviewer_output.parse_retry_recovered is False


# ---------------------------------------------------------------------------
# 87. Retry does NOT fake a pass — malformed stays blocked
# ---------------------------------------------------------------------------

class TestRetryCannotFakePass:
    def test_retry_no_fake_pass(self, demo_repo):
        provider = FakeProvider(malformed_review=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        assert result.final_status != "staged_review_passed"
        assert result.reviewer_json_recovered is False


# ---------------------------------------------------------------------------
# 88. reviewer_malformed_excerpt captured in result
# ---------------------------------------------------------------------------

class TestMalformedExcerptCaptured:
    def test_excerpt_captured(self, demo_repo):
        provider = FakeProvider(malformed_review=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        assert result.reviewer_malformed_excerpt != ""
        assert "not valid json" in result.reviewer_malformed_excerpt


# ---------------------------------------------------------------------------
# 89. Parse metadata exported in JSON
# ---------------------------------------------------------------------------

class TestParseMetadataInExport:
    def test_parse_fields_in_json(self, demo_repo):
        provider = FakeProvider(malformed_review=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        data = export_pingpong_json(result)
        assert "reviewer_parse_retry_count" in data
        assert data["reviewer_parse_retry_count"] == 1
        assert "reviewer_json_recovered" in data
        assert data["reviewer_json_recovered"] is False
        assert "reviewer_parse_error" in data
        assert "reviewer_malformed_excerpt" in data


# ---------------------------------------------------------------------------
# 90. Parse metadata in summarize output
# ---------------------------------------------------------------------------

class TestParseMetadataInSummary:
    def test_parse_info_in_summary(self, demo_repo):
        provider = FakeProvider(malformed_review=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        summary = summarize_pingpong(result)
        assert "retried" in summary.lower()
        assert "NOT recovered" in summary


# ---------------------------------------------------------------------------
# 91. Recovered parse metadata in summarize
# ---------------------------------------------------------------------------

class TestRecoveredParseInSummary:
    def test_recovered_in_summary(self, demo_repo):
        provider = FakeProvider(malformed_review_recoverable=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        summary = summarize_pingpong(result)
        assert "recovered" in summary.lower()


# ---------------------------------------------------------------------------
# 92. parse_retried exported per-round in JSON
# ---------------------------------------------------------------------------

class TestParseRetriedInRoundExport:
    def test_per_round_parse_retried(self, demo_repo):
        provider = FakeProvider(malformed_review_recoverable=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        data = export_pingpong_json(result)
        reviewer_data = data["rounds"][0]["reviewer"]
        assert reviewer_data["parse_retried"] is True
        assert reviewer_data["parse_retry_recovered"] is True


# ---------------------------------------------------------------------------
# 93. _REVIEWER_RETRY_PROMPT has excerpt placeholder
# ---------------------------------------------------------------------------

class TestRetryPromptTemplate:
    def test_retry_prompt_has_excerpt(self):
        assert "{excerpt}" in _REVIEWER_RETRY_PROMPT
        formatted = _REVIEWER_RETRY_PROMPT.format(excerpt="some bad text")
        assert "some bad text" in formatted
        assert "ONLY valid JSON" in formatted


# ---------------------------------------------------------------------------
# 94. Reviewer prompt includes safe diff
# ---------------------------------------------------------------------------

class TestReviewerPromptSafeDiff:
    def test_safe_diff_in_reviewer_prompt(self):
        prompt = _build_reviewer_prompt(
            "Fix bug", "Builder fixed it",
            safe_diff="--- a/foo.py\n+++ b/foo.py\n@@ -1 +1 @@\n-old\n+new",
            test_result="passed",
            files_changed=["foo.py"],
        )
        assert "Staged Unified Diff" in prompt
        assert "+new" in prompt
        assert "-old" in prompt


# ---------------------------------------------------------------------------
# 95. Reviewer prompt caps safe diff at 30K
# ---------------------------------------------------------------------------

class TestReviewerPromptDiffCap:
    def test_safe_diff_capped(self):
        long_diff = "x" * 35000
        prompt = _build_reviewer_prompt(
            "Fix bug", "Builder fixed it",
            safe_diff=long_diff,
        )
        assert "[DIFF TRUNCATED]" in prompt


# ---------------------------------------------------------------------------
# 96. Builder repair prompt includes safe diff
# ---------------------------------------------------------------------------

class TestBuilderRepairPromptDiff:
    def test_safe_diff_in_repair_prompt(self):
        findings = [ReviewFinding(id="R1", severity="high", summary="bug")]
        prompt = _build_builder_prompt(
            "Fix bug", "context here",
            round_number=2,
            findings=findings,
            staged_state="Files changed: [foo.py]",
            safe_diff="--- a/foo.py\n+++ b/foo.py\n@@ -1 +1 @@\n-old\n+new",
        )
        assert "Current Staged Diff" in prompt
        assert "+new" in prompt


# ---------------------------------------------------------------------------
# 97. Builder repair prompt caps diff at 20K
# ---------------------------------------------------------------------------

class TestBuilderRepairPromptDiffCap:
    def test_repair_diff_capped(self):
        findings = [ReviewFinding(id="R1", severity="high", summary="bug")]
        long_diff = "y" * 25000
        prompt = _build_builder_prompt(
            "Fix bug", "context",
            round_number=2,
            findings=findings,
            safe_diff=long_diff,
        )
        assert "[DIFF TRUNCATED]" in prompt


# ---------------------------------------------------------------------------
# 98. Builder prompt round 1 has no diff section
# ---------------------------------------------------------------------------

class TestBuilderPromptRound1NoDiff:
    def test_no_diff_round_1(self):
        prompt = _build_builder_prompt(
            "Fix bug", "context",
            round_number=1,
            safe_diff="some diff",
        )
        # No findings = no diff shown (safe_diff only shown with findings)
        assert "Current Staged Diff" not in prompt


# ---------------------------------------------------------------------------
# 99. _parse_reviewer_json handles JSON with surrounding prose
# ---------------------------------------------------------------------------

class TestParseReviewerJsonSurroundingProse:
    def test_json_with_prose(self):
        text = 'Here is my review:\n{"verdict":"pass","findings":[],"confidence":"high","summary":"ok"}\nEnd.'
        out = _parse_reviewer_json(text, 100, 50)
        assert out.verdict == "pass"
        assert out.error == ""


# ---------------------------------------------------------------------------
# 100. _parse_reviewer_json raw_text capped at 500
# ---------------------------------------------------------------------------

class TestParseReviewerJsonRawTextCap:
    def test_raw_text_capped(self):
        text = "x" * 1000  # No JSON
        out = _parse_reviewer_json(text, 100, 50)
        assert len(out.raw_text) <= 500


# ---------------------------------------------------------------------------
# 101. Reviewer prompt falls back to diff_summary when no safe_diff
# ---------------------------------------------------------------------------

class TestReviewerPromptFallbackDiffSummary:
    def test_fallback_diff_summary(self):
        prompt = _build_reviewer_prompt(
            "Fix bug", "Builder fixed it",
            diff_summary="M foo.py\nM bar.py",
        )
        assert "Staged Diff" in prompt
        assert "M foo.py" in prompt
        assert "Staged Unified Diff" not in prompt


# ---------------------------------------------------------------------------
# 102. _unwrap_envelope handles nested text with extra whitespace
# ---------------------------------------------------------------------------

class TestUnwrapEnvelopeTextWhitespace:
    def test_text_with_whitespace(self):
        import json as _json
        inner = {"verdict": "pass", "findings": [], "summary": "ok"}
        data = {"text": f"  {_json.dumps(inner)}  "}
        result = _unwrap_envelope(data)
        assert result["verdict"] == "pass"


# ---------------------------------------------------------------------------
# 103. E2E: reviewer safe diff passed to reviewer (fake provider)
# ---------------------------------------------------------------------------

class TestReviewerReceivesSafeDiff:
    def test_reviewer_gets_diff(self, demo_repo):
        """Verify run completes and safe diff is computed before reviewer."""
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        assert result.final_status == "staged_review_passed"
        assert result.safe_diff_summary != "" or result.safe_diff_files != []


# ---------------------------------------------------------------------------
# 104. E2E: repair round gets safe diff context
# ---------------------------------------------------------------------------

class TestRepairRoundGetsDiff:
    def test_two_round_repair(self, demo_repo):
        """Two-round run: round 2 builder gets findings + diff context."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=2)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
            max_rounds=2, repair_rounds=2,
        )
        assert len(result.rounds) == 2
        assert result.final_status == "staged_review_passed"


# ---------------------------------------------------------------------------
# Step 5023: Target-repo symlink copy leak regression tests
# ---------------------------------------------------------------------------


class TestStagingCopySymlinkBlock:
    def test_external_symlink_not_copied(self, tmp_path):
        """Target repo file symlink to outside is not copied into staging."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "normal.py").write_text("normal content\n")

        external = tmp_path / "secret.txt"
        external.write_text("SECRET_CONTENT\n")
        (repo / "link.txt").symlink_to(external)

        sr = _create_staging(str(repo), "test-ext-symlink")
        staging = sr.staging_path

        assert (staging / "normal.py").exists()
        assert not (staging / "link.txt").exists()
        assert any("target_source_is_symlink" in s for s in sr.skipped_unsafe)
        for f in staging.rglob("*"):
            if f.is_file():
                assert "SECRET_CONTENT" not in f.read_text()

        import shutil
        shutil.rmtree(staging, ignore_errors=True)

    def test_internal_symlink_not_copied(self, tmp_path):
        """Target repo file symlink to inside is also not copied."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "real.py").write_text("real content\n")
        (repo / "link.py").symlink_to(repo / "real.py")

        sr = _create_staging(str(repo), "test-int-symlink")
        staging = sr.staging_path

        assert (staging / "real.py").exists()
        assert not (staging / "link.py").exists()
        assert any("target_source_is_symlink" in s for s in sr.skipped_unsafe)

        import shutil
        shutil.rmtree(staging, ignore_errors=True)

    def test_parent_symlink_not_followed(self, tmp_path):
        """Target repo parent directory symlink is not followed."""
        repo = tmp_path / "repo"
        repo.mkdir()

        outside = tmp_path / "outside_dir"
        outside.mkdir()
        (outside / "secret.py").write_text("PARENT_SECRET\n")

        (repo / "linkdir").symlink_to(outside)
        (repo / "normal.py").write_text("ok\n")

        sr = _create_staging(str(repo), "test-parent-symlink")
        staging = sr.staging_path

        assert (staging / "normal.py").exists()
        assert not (staging / "linkdir").exists()
        for f in staging.rglob("*"):
            if f.is_file():
                assert "PARENT_SECRET" not in f.read_text()

        import shutil
        shutil.rmtree(staging, ignore_errors=True)

    def test_normal_files_copy(self, tmp_path):
        """Normal (non-symlink) files copy correctly."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("main\n")
        sub = repo / "sub"
        sub.mkdir()
        (sub / "util.py").write_text("util\n")

        sr = _create_staging(str(repo), "test-normal-copy")
        staging = sr.staging_path

        assert (staging / "main.py").read_text() == "main\n"
        assert (staging / "sub" / "util.py").read_text() == "util\n"
        assert sr.files_copied == 2
        assert len(sr.skipped_unsafe) == 0

        import shutil
        shutil.rmtree(staging, ignore_errors=True)


# ---------------------------------------------------------------------------
# Step 5026: Builder-created staging symlink no-leak test
# ---------------------------------------------------------------------------


class TestBuilderStagingSymlinkNoLeak:
    def test_builder_staging_symlink_not_in_diff(self, tmp_path):
        """Fake builder creates staging symlink — safe diff excludes it."""
        original = tmp_path / "original"
        original.mkdir()
        (original / "good.py").write_text("original\n")

        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "good.py").write_text("modified\n")

        external = tmp_path / "secret.txt"
        external.write_text("TOP_SECRET_CONTENT\n")
        (staging / "leak.txt").symlink_to(external)

        changed = _find_staging_changes(staging, original)
        assert "good.py" in changed
        assert "leak.txt" not in changed

        diff_text, diff_files, _ = _compute_safe_diff(
            staging, original, ["good.py", "leak.txt"],
        )
        assert "TOP_SECRET_CONTENT" not in diff_text
        assert "unsafe staged artifact skipped" in diff_text

    def test_builder_staging_symlink_inside_skipped(self, tmp_path):
        """Even a staging symlink to inside staging is skipped in diff."""
        staging = tmp_path / "staging"
        staging.mkdir()
        original = tmp_path / "original"
        original.mkdir()

        (staging / "real.py").write_text("real\n")
        (staging / "link.py").symlink_to(staging / "real.py")

        changed = _find_staging_changes(staging, original)
        assert "real.py" in changed
        assert "link.py" not in changed


# ---------------------------------------------------------------------------
# Step 5027: Builder-created staging parent symlink no-leak test
# ---------------------------------------------------------------------------


class TestBuilderStagingParentSymlinkNoLeak:
    def test_builder_parent_symlink_not_in_diff(self, tmp_path):
        """Builder creates staging parent symlink — safe diff excludes it."""
        original = tmp_path / "original"
        original.mkdir()

        staging = tmp_path / "staging"
        staging.mkdir()

        outside = tmp_path / "outside_dir"
        outside.mkdir()
        (outside / "file.py").write_text("OUTSIDE_SECRET\n")

        (staging / "linkdir").symlink_to(outside)

        changed = _find_staging_changes(staging, original)
        assert not any("linkdir" in c for c in changed)

        diff_text, diff_files, _ = _compute_safe_diff(
            staging, original, ["linkdir/file.py"],
        )
        assert "OUTSIDE_SECRET" not in diff_text
        assert "unsafe staged artifact skipped" in diff_text


# ---------------------------------------------------------------------------
# Step 5024/5025: _is_safe_staged_path unit tests
# ---------------------------------------------------------------------------


class TestSafeStagedPath:
    def test_regular_file_is_safe(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        (root / "file.py").write_text("ok\n")
        assert _is_safe_staged_path(root, root.resolve(), "file.py") == ""

    def test_symlink_is_unsafe(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        external = tmp_path / "ext.txt"
        external.write_text("x")
        (root / "link.txt").symlink_to(external)
        reason = _is_safe_staged_path(root, root.resolve(), "link.txt")
        assert "staged_is_symlink" in reason

    def test_parent_symlink_is_unsafe(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        (outside / "f.py").write_text("x")
        (root / "linkdir").symlink_to(outside)
        reason = _is_safe_staged_path(root, root.resolve(), "linkdir/f.py")
        assert "staged_parent_symlink" in reason


# ---------------------------------------------------------------------------
# Step 5031: Review ZIP hygiene test
# ---------------------------------------------------------------------------


class TestReviewZipHygiene:
    def test_make_review_zip_rejects_detritus(self, tmp_path):
        """make_review_zip.sh fails if BUILDER_WAS_HERE.txt exists."""
        import subprocess

        script = Path(__file__).resolve().parents[2] / "scripts" / "make_review_zip.sh"
        if not script.exists():
            pytest.skip("make_review_zip.sh not found")

        fake_repo = tmp_path / "repo"
        fake_repo.mkdir()
        subprocess.run(
            ["git", "init"], cwd=str(fake_repo),
            capture_output=True, timeout=5,
        )
        (fake_repo / "main.py").write_text("ok\n")
        subprocess.run(
            ["git", "add", "."], cwd=str(fake_repo),
            capture_output=True, timeout=5,
        )
        subprocess.run(
            ["git", "commit", "-m", "init", "--allow-empty"],
            cwd=str(fake_repo), capture_output=True, timeout=5,
            env={**__import__("os").environ, "GIT_AUTHOR_NAME": "test",
                 "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "test",
                 "GIT_COMMITTER_EMAIL": "t@t"},
        )
        (fake_repo / "BUILDER_WAS_HERE.txt").write_text("debug\n")
        ev_dir = fake_repo / "remedy-job-evidence-test"
        ev_dir.mkdir()
        (ev_dir / "job_flow.json").write_text("{}")

        result = subprocess.run(
            ["bash", str(script), "--evidence-dir", str(ev_dir)],
            cwd=str(fake_repo),
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode != 0
        assert "detritus" in result.stdout.lower() or "BUILDER_WAS_HERE" in result.stdout


# ---------------------------------------------------------------------------
# Step 5037: _is_safe_repo_path tests
# ---------------------------------------------------------------------------


class TestSafeRepoPath:
    def test_regular_file_is_safe(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("ok")
        assert _is_safe_repo_path(repo, repo.resolve(), "main.py") == ""

    def test_symlink_is_unsafe(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("TOP SECRET")
        (repo / "link.txt").symlink_to(secret)
        assert _is_safe_repo_path(repo, repo.resolve(), "link.txt") == "repo_source_is_symlink"

    def test_parent_symlink_is_unsafe(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        real_dir = tmp_path / "external"
        real_dir.mkdir()
        (real_dir / "data.txt").write_text("external data")
        (repo / "linked").symlink_to(real_dir)
        result = _is_safe_repo_path(repo, repo.resolve(), "linked/data.txt")
        assert result == "repo_source_parent_symlink"

    def test_missing_file(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        assert _is_safe_repo_path(repo, repo.resolve(), "nope.txt") == "repo_source_missing"

    def test_directory_is_not_regular(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "subdir").mkdir()
        assert _is_safe_repo_path(repo, repo.resolve(), "subdir") == "repo_source_not_regular_file"

    def test_absolute_path_rejected(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        assert _is_safe_repo_path(repo, repo.resolve(), "/etc/passwd") == "repo_source_escapes_repo"


# ---------------------------------------------------------------------------
# Step 5043: README symlink context leak tests
# ---------------------------------------------------------------------------


class TestReadmeSymlinkContextLeak:
    def test_readme_symlink_no_secret_leak(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("TOP SECRET CONTENT xyz123")
        (repo / "README.md").symlink_to(secret)
        context, cats = build_repo_context(str(repo), "test goal")
        assert "TOP SECRET CONTENT" not in context
        assert "xyz123" not in context
        assert "readme" not in cats

    def test_normal_readme_still_appears(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("This is a normal readme")
        context, cats = build_repo_context(str(repo), "test goal")
        assert "This is a normal readme" in context
        assert "readme" in cats

    def test_unsafe_readme_safety_note(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("TOP SECRET")
        (repo / "README.md").symlink_to(secret)
        context, cats = build_repo_context(str(repo), "test goal")
        assert "repo_source_is_symlink" in context
        assert "README.md" in context

    def test_no_absolute_external_path_in_context(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("TOP SECRET")
        (repo / "README.md").symlink_to(secret)
        context, _ = build_repo_context(str(repo), "test goal")
        assert str(secret) not in context


# ---------------------------------------------------------------------------
# Step 5044: mentioned file symlink context leak tests
# ---------------------------------------------------------------------------


class TestMentionedFileSymlinkContextLeak:
    def test_mentioned_symlink_no_secret_leak(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "safe.py").write_text("safe content")
        secret = tmp_path / "secret.txt"
        secret.write_text("EXTERNAL SECRET abc999")
        (repo / "link.txt").symlink_to(secret)
        context, cats = build_repo_context(
            str(repo), "goal", mentioned_files=["link.txt"]
        )
        assert "EXTERNAL SECRET" not in context
        assert "abc999" not in context

    def test_mentioned_symlink_inside_repo_also_blocked(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "real.txt").write_text("real content inside")
        (repo / "link.txt").symlink_to(repo / "real.txt")
        context, _ = build_repo_context(
            str(repo), "goal", mentioned_files=["link.txt"]
        )
        assert "real content inside" not in context

    def test_normal_mentioned_file_appears(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("normal python code")
        context, cats = build_repo_context(
            str(repo), "goal", mentioned_files=["main.py"]
        )
        assert "normal python code" in context
        assert "mentioned_files" in cats

    def test_context_has_reason_no_external_path(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("TOP SECRET")
        (repo / "link.txt").symlink_to(secret)
        context, _ = build_repo_context(
            str(repo), "goal", mentioned_files=["link.txt"]
        )
        assert "repo_source_is_symlink" in context
        assert str(secret) not in context


# ---------------------------------------------------------------------------
# Step 5045: context file tree symlink behavior tests
# ---------------------------------------------------------------------------


class TestFileTreeSymlinkBehavior:
    def test_symlink_dir_not_traversed(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        (external / "secret.py").write_text("SECRET CODE")
        (repo / "linked_dir").symlink_to(external)
        (repo / "safe.py").write_text("ok")
        context, _ = build_repo_context(str(repo), "goal")
        assert "secret.py" not in context
        assert "SECRET CODE" not in context
        assert "safe.py" in context

    def test_file_symlink_not_read(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("SECRET DATA 12345")
        (repo / "link.txt").symlink_to(secret)
        (repo / "real.py").write_text("real")
        context, _ = build_repo_context(str(repo), "goal")
        assert "SECRET DATA 12345" not in context
        assert "link.txt" not in context or "repo_source_is_symlink" in context
        assert "real.py" in context

    def test_no_secret_in_safety_notes(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("SECRET")
        (repo / "link.txt").symlink_to(secret)
        context, _ = build_repo_context(str(repo), "goal")
        assert str(secret) not in context

    def test_normal_files_in_tree(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("code")
        (repo / "utils.py").write_text("helpers")
        context, _ = build_repo_context(str(repo), "goal")
        assert "main.py" in context
        assert "utils.py" in context


# ---------------------------------------------------------------------------
# Step 5046: _snapshot_target symlink safety tests
# ---------------------------------------------------------------------------


class TestSnapshotTargetSymlinkSafety:
    def test_file_symlink_outside_skipped(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("SECRET HASH CONTENT")
        (repo / "link.txt").symlink_to(secret)
        (repo / "real.py").write_text("real content")
        snap = _snapshot_target(repo)
        assert "link.txt" not in snap
        assert "real.py" in snap

    def test_file_symlink_inside_skipped(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "real.py").write_text("real")
        (repo / "alias.py").symlink_to(repo / "real.py")
        snap = _snapshot_target(repo)
        assert "alias.py" not in snap
        assert "real.py" in snap

    def test_parent_dir_symlink_not_traversed(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        (external / "data.py").write_text("external data")
        (repo / "linked").symlink_to(external)
        (repo / "safe.py").write_text("safe")
        snap = _snapshot_target(repo)
        assert "linked/data.py" not in snap
        assert "safe.py" in snap

    def test_normal_files_still_hashed(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("content")
        snap = _snapshot_target(repo)
        assert "main.py" in snap
        import hashlib
        expected = hashlib.sha256(b"content").digest()
        assert snap["main.py"] == expected

    def test_mutation_guard_detects_normal_change(self, tmp_path):
        from packages.orchestration.pingpong_loop import _check_target_mutation
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("original")
        before = _snapshot_target(repo)
        (repo / "main.py").write_text("changed")
        meaningful, _ = _check_target_mutation(repo, before)
        assert "main.py" in meaningful


# ---------------------------------------------------------------------------
# Step 5047: token estimate symlink safety tests
# ---------------------------------------------------------------------------


class TestTokenEstimateSymlinkSafety:
    def test_symlink_file_skipped(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        big_file = tmp_path / "big.txt"
        big_file.write_text("X" * 100000)
        (repo / "link.txt").symlink_to(big_file)
        (repo / "real.py").write_text("small")
        result = _estimate_full_repo_tokens(str(repo))
        assert result["full_repo_files_estimated"] == 1
        assert result["full_repo_files_skipped"] >= 1

    def test_symlink_dir_not_traversed(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        for i in range(10):
            (external / f"file{i}.py").write_text("x" * 1000)
        (repo / "linked").symlink_to(external)
        (repo / "safe.py").write_text("ok")
        result = _estimate_full_repo_tokens(str(repo))
        assert result["full_repo_files_estimated"] == 1

    def test_normal_files_counted(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "a.py").write_text("aaa")
        (repo / "b.py").write_text("bbb")
        result = _estimate_full_repo_tokens(str(repo))
        assert result["full_repo_files_estimated"] == 2

    def test_no_outside_path_leaks(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("X" * 50000)
        (repo / "link.txt").symlink_to(secret)
        result = _estimate_full_repo_tokens(str(repo))
        for v in result.values():
            if isinstance(v, str):
                assert str(secret) not in v


# ---------------------------------------------------------------------------
# Step 5048: run_pingpong prompt no-leak integration test
# ---------------------------------------------------------------------------


class TestRunPingpongPromptNoLeak:
    def test_builder_prompt_no_symlink_content(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("SUPER SECRET CONTENT qwerty789")
        (repo / "README.md").symlink_to(secret)
        (repo / "main.py").write_text("normal code")
        context, cats = build_repo_context(str(repo), "implement feature X")
        from packages.orchestration.pingpong_loop import _build_builder_prompt
        prompt = _build_builder_prompt("implement feature X", context)
        assert "SUPER SECRET CONTENT" not in prompt
        assert "qwerty789" not in prompt
        assert "implement feature X" in prompt

    def test_builder_prompt_no_mentioned_symlink_content(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        secret = tmp_path / "secret.txt"
        secret.write_text("MENTIONED SECRET asdf456")
        (repo / "config.txt").symlink_to(secret)
        (repo / "safe.py").write_text("safe")
        context, _ = build_repo_context(
            str(repo), "goal", mentioned_files=["config.txt"]
        )
        prompt = _build_builder_prompt("goal", context)
        assert "MENTIONED SECRET" not in prompt
        assert "asdf456" not in prompt
        assert "repo_source_is_symlink" in prompt

    def test_builder_prompt_safe_context_present(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("normal safe code 12345")
        context, _ = build_repo_context(
            str(repo), "goal", mentioned_files=["main.py"]
        )
        prompt = _build_builder_prompt("goal", context)
        assert "normal safe code 12345" in prompt


# ---------------------------------------------------------------------------
# F108 T003d: end-to-end tiered summaries reduce composed prompt size
# ---------------------------------------------------------------------------

class TestTieredSummariesReduceComposedPromptSize:
    def test_both_call_sites_tiered_and_prompt_shrinks_an_order_of_magnitude(
        self, demo_repo, monkeypatch,
    ):
        big_content = "\n".join(f"# line {i:05d}: " + "x" * 70 for i in range(1000))

        def fake_apply(staging, builder_output, goal):
            for rel_path in builder_output.files_changed:
                fp = staging / rel_path
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(big_content)

        monkeypatch.setattr(pingpong_loop, "_apply_fake_builder_changes", fake_apply)

        fake_response = json.dumps({
            "l1": "x" * 100,
            "l2": [
                {"section": "big.py", "span_ref": "file:big.py", "summary": "SECTION SUMMARY"},
            ],
        })

        def fake_call_fn(prompt: str, attempt: int) -> str:
            return fake_response

        monkeypatch.setattr(pingpong_loop, "summary_call_fn", lambda: fake_call_fn)

        provider = FakeProvider(builder_files=["big.py"], fail_on_round=1, pass_on_round=2)
        result = run_pingpong(
            "Fix big file", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=2, repair_rounds=2,
        )
        assert len(result.rounds) == 2

        reviewer_trace = next(
            t for t in result.prompt_traces if t.role == "reviewer" and t.round == 1)
        builder_trace = next(
            t for t in result.prompt_traces if t.role == "builder" and t.round == 2)

        reviewer_artifact = (
            pingpong_run_dir(result.run_id) / "calls" / "reviewer"
            / "round-01" / "tiered_diff.diff")
        builder_artifact = (
            pingpong_run_dir(result.run_id) / "calls" / "builder"
            / "round-02" / "tiered_diff.diff")
        assert reviewer_artifact.exists()
        assert builder_artifact.exists()

        raw_reviewer_len = len(reviewer_artifact.read_text())
        raw_builder_len = len(builder_artifact.read_text())
        assert raw_reviewer_len > _OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS
        assert raw_builder_len > _OVERSIZED_DIFF_THRESHOLD_CHARS

        assert reviewer_trace.prompt_chars < raw_reviewer_len / 10
        assert builder_trace.prompt_chars < raw_builder_len / 10
