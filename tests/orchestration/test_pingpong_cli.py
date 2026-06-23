"""Ping-pong CLI provider + durable storage + test-command E2E tests.

Tests the ClaudeCliProvider path, durable run persistence, test-command
execution, do.report command, and JSON mode correctness — all using
fake/mock providers (no real Claude calls, no network).
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


@pytest.fixture
def fake_claude_bin(tmp_path: Path) -> Path:
    """Create a fake `claude` executable that echoes a canned response."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    claude_script.write_text(textwrap.dedent("""\
        #!/bin/bash
        echo "Builder made changes to README.md"
        echo "- docs/README.md updated"
    """))
    claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


@pytest.fixture
def fake_claude_reviewer_bin(tmp_path: Path) -> Path:
    """Create a fake `claude` that returns reviewer JSON."""
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
def fake_claude_failing_bin(tmp_path: Path) -> Path:
    """Create a fake `claude` that exits non-zero."""
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


# ---------------------------------------------------------------------------
# 1. ClaudeCliProvider: factory + name
# ---------------------------------------------------------------------------

class TestClaudeCliProviderFactory:
    def test_create_claude_cli(self):
        p = create_provider("claude-cli")
        assert p.name == "claude-cli"

    def test_unknown_provider_raises(self):
        with pytest.raises(RuntimeError, match="Unknown provider"):
            create_provider("nonexistent")


# ---------------------------------------------------------------------------
# 2. ClaudeCliProvider: CLI not found
# ---------------------------------------------------------------------------

class TestClaudeCliNotFound:
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
        assert "not found" in out.error.lower() or "provider_error" in out.error


# ---------------------------------------------------------------------------
# 3. ClaudeCliProvider: successful build
# ---------------------------------------------------------------------------

class TestClaudeCliBuild:
    def test_build_returns_output(self, monkeypatch, fake_claude_bin):
        monkeypatch.setenv("PATH", str(fake_claude_bin))
        provider = ClaudeCliProvider()
        out = provider.build("Fix the README")
        assert out.error == ""
        assert out.provider == "claude-cli"
        assert out.summary
        assert out.duration_ms >= 0

    def test_build_detects_files(self, monkeypatch, fake_claude_bin):
        monkeypatch.setenv("PATH", str(fake_claude_bin))
        provider = ClaudeCliProvider()
        out = provider.build("Fix the README")
        assert "docs/README.md" in out.files_changed


# ---------------------------------------------------------------------------
# 4. ClaudeCliProvider: successful review
# ---------------------------------------------------------------------------

class TestClaudeCliReview:
    def test_review_parses_json(self, monkeypatch, fake_claude_reviewer_bin):
        monkeypatch.setenv("PATH", str(fake_claude_reviewer_bin))
        provider = ClaudeCliProvider()
        out = provider.review("Review these changes")
        assert out.error == ""
        assert out.verdict == "pass"
        assert out.confidence == "high"
        assert out.provider == "claude-cli"


# ---------------------------------------------------------------------------
# 5. ClaudeCliProvider: CLI failure
# ---------------------------------------------------------------------------

class TestClaudeCliFailure:
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
        assert "provider_error" in out.error


# ---------------------------------------------------------------------------
# 6. Durable run storage: persist + load
# ---------------------------------------------------------------------------

class TestDurableStorage:
    def test_run_persists_result(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = load_run(str(demo_repo), result.run_id)
        assert data is not None
        assert data["run_id"] == result.run_id
        assert data["goal"] == "Fix README"
        assert data["final_status"] == result.final_status

    def test_load_nonexistent_returns_none(self, demo_repo: Path):
        data = load_run(str(demo_repo), "nonexistent_id_1234")
        assert data is None

    def test_list_runs_shows_persisted(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        runs = list_runs(str(demo_repo))
        assert any(r["run_id"] == result.run_id for r in runs)

    def test_list_runs_empty_repo(self, tmp_path: Path):
        runs = list_runs(str(tmp_path))
        assert runs == []

    def test_persisted_json_has_required_fields(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = load_run(str(demo_repo), result.run_id)
        required = [
            "run_id", "goal", "mode", "builder_provider", "reviewer_provider",
            "max_rounds", "total_rounds", "final_status", "staged_files",
            "changed_target_files", "target_mutated", "rounds",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# 7. Test command execution
# ---------------------------------------------------------------------------

class TestTestCommand:
    def test_passing_test_command(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            test_command="echo 'tests pass'",
        )
        for rd in result.rounds:
            assert rd.test_passed is True
            assert "exit=0" in rd.test_summary

    def test_failing_test_command(self, demo_repo: Path):
        provider = FakeProvider(pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
            test_command="false",
            max_rounds=1,
        )
        rd = result.rounds[0]
        assert rd.test_passed is False
        assert result.final_status == "test_failed"

    def test_invalid_test_command(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            test_command="nonexistent_binary_xyz_12345",
            max_rounds=1,
        )
        rd = result.rounds[0]
        assert rd.test_passed is False
        assert "not found" in rd.test_summary.lower()


# ---------------------------------------------------------------------------
# 8. JSON mode: no human headers
# ---------------------------------------------------------------------------

class TestJSONMode:
    def test_export_json_is_valid(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = export_pingpong_json(result)
        text = json.dumps(data)
        # Must be valid JSON
        parsed = json.loads(text)
        assert parsed["run_id"] == result.run_id

    def test_export_no_human_headers(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = export_pingpong_json(result)
        text = json.dumps(data)
        assert "Job: ping-pong run" not in text
        assert "Mode: staged" not in text


# ---------------------------------------------------------------------------
# 9. Summary references remedy do report
# ---------------------------------------------------------------------------

class TestSummaryReport:
    def test_summary_references_do_report(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        summary = summarize_pingpong(result)
        assert "remedy do report" in summary
        assert result.run_id in summary

    def test_summary_does_not_reference_job_report(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        summary = summarize_pingpong(result)
        assert "remedy job report" not in summary


# ---------------------------------------------------------------------------
# 10. Keep staging
# ---------------------------------------------------------------------------

class TestKeepStaging:
    def test_keep_staging_preserves_dir(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            keep_staging=True,
        )
        # staging_dir should appear in error/info field
        staging_dir = None
        if result.error and "staging_dir=" in result.error:
            staging_dir = result.error.split("staging_dir=")[-1].strip()
        assert staging_dir is not None
        assert Path(staging_dir).exists()
        # Cleanup
        import shutil
        shutil.rmtree(staging_dir, ignore_errors=True)

    def test_default_discards_staging(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
        )
        # No staging_dir in error
        assert "staging_dir=" not in (result.error or "")
