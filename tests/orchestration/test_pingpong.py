"""Ping-pong loop E2E tests with fake provider.

Tests the Builder ↔ Reviewer repair cycle using deterministic fake providers.
No real Claude calls. No network. No target repo mutation.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import (
    build_repo_context,
    export_pingpong_json,
    run_pingpong,
    summarize_pingpong,
)
from packages.orchestration.pingpong_provider import (
    ClaudeProvider,
    FakeProvider,
    create_provider,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    """Redirect REMEDY_DATA_DIR to tmp so tests don't write to real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    """Create a minimal demo repo for testing."""
    (tmp_path / "README.md").write_text("# Demo\nA demo project.\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "README.md").write_text("# Docs\nDocumentation here.\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    # Secret file — must NOT appear in context
    (tmp_path / ".env").write_text("API_KEY=secret123\n")
    (tmp_path / ".env.local").write_text("DB_PASSWORD=hunter2\n")
    return tmp_path


# ---------------------------------------------------------------------------
# 1. remedy do creates a durable job/run
# ---------------------------------------------------------------------------

class TestPingPongCreatesRun:
    def test_run_returns_result_with_id(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.run_id
        assert len(result.run_id) == 16
        assert result.goal == "Fix README"

    def test_run_result_has_timestamps(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.started_at
        assert result.finished_at


# ---------------------------------------------------------------------------
# 2. Staged mode does not mutate target repo
# ---------------------------------------------------------------------------

class TestStagedModeNoTargetMutation:
    def test_target_files_unchanged(self, demo_repo: Path):
        original_readme = (demo_repo / "README.md").read_text()
        original_docs = (demo_repo / "docs" / "README.md").read_text()
        run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert (demo_repo / "README.md").read_text() == original_readme
        assert (demo_repo / "docs" / "README.md").read_text() == original_docs

    def test_changed_target_files_empty(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.changed_target_files == []

    def test_target_not_mutated(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.target_mutated is False

    def test_no_pytest_cache_in_target(self, demo_repo: Path):
        run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert not (demo_repo / ".pytest_cache").exists()
        assert not (demo_repo / "__pycache__").exists()


# ---------------------------------------------------------------------------
# 3-4. Fake Builder changes staging, Fake Reviewer returns findings
# ---------------------------------------------------------------------------

class TestFakeBuilderAndReviewer:
    def test_builder_produces_output(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.rounds
        rd = result.rounds[0]
        assert rd.builder_output is not None
        assert rd.builder_output.summary
        assert rd.builder_output.files_changed

    def test_reviewer_returns_findings_round_1(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        rd = result.rounds[0]
        assert rd.reviewer_output is not None
        assert rd.reviewer_output.verdict == "needs_repair"
        assert len(rd.reviewer_output.findings) > 0

    def test_staged_files_populated(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert len(result.staged_files) > 0


# ---------------------------------------------------------------------------
# 5-7. Findings → Repair → Pass cycle
# ---------------------------------------------------------------------------

class TestRepairLoop:
    def test_findings_become_repair_input(self, demo_repo: Path):
        """Round 1 findings lead to round 2 repair."""
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake", repair_rounds=2)
        assert len(result.rounds) >= 2
        # Round 2 builder should have received findings
        rd2 = result.rounds[1]
        assert rd2.builder_output is not None
        assert "Repair" in rd2.builder_output.summary or "round 2" in rd2.builder_output.summary.lower()

    def test_reviewer_passes_after_repair(self, demo_repo: Path):
        """Fake provider passes on round 2 by default."""
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake", repair_rounds=2)
        assert len(result.rounds) >= 2
        last = result.rounds[-1]
        assert last.reviewer_output is not None
        assert last.reviewer_output.verdict == "pass"

    def test_final_status_is_staged_review_passed(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake", repair_rounds=2)
        assert result.final_status == "staged_review_passed"


# ---------------------------------------------------------------------------
# 8. Final report shows both rounds
# ---------------------------------------------------------------------------

class TestReportShowsRounds:
    def test_report_json_has_rounds(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake", repair_rounds=2)
        data = export_pingpong_json(result)
        assert data["total_rounds"] >= 2
        assert len(data["rounds"]) >= 2
        assert data["rounds"][0]["round"] == 1
        assert data["rounds"][1]["round"] == 2

    def test_summary_shows_rounds(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake", repair_rounds=2)
        summary = summarize_pingpong(result)
        assert "Round 1" in summary
        assert "Round 2" in summary
        assert "staged_review_passed" in summary


# ---------------------------------------------------------------------------
# 9. Max rounds blocks honestly
# ---------------------------------------------------------------------------

class TestMaxRounds:
    def test_max_rounds_reached(self, demo_repo: Path):
        provider = FakeProvider(pass_on_round=99)  # Never passes
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
            max_rounds=2, repair_rounds=5,
        )
        assert result.final_status == "max_rounds_reached"
        assert len(result.rounds) == 2


# ---------------------------------------------------------------------------
# 10. Provider unavailable blocks honestly
# ---------------------------------------------------------------------------

class TestProviderUnavailable:
    def test_builder_error_blocks(self, demo_repo: Path):
        provider = FakeProvider(builder_error="provider_unavailable: API key missing")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        assert result.final_status == "provider_unavailable"
        assert "API key" in result.error or "provider" in result.error

    def test_unknown_provider_fails(self):
        with pytest.raises(RuntimeError, match="Unknown provider"):
            create_provider("nonexistent_provider")

    def test_claude_without_api_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        provider = ClaudeProvider()
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
            provider._get_client()


# ---------------------------------------------------------------------------
# 11. Malformed reviewer JSON blocks honestly
# ---------------------------------------------------------------------------

class TestMalformedReviewerOutput:
    def test_malformed_review_blocks(self, demo_repo: Path):
        provider = FakeProvider(malformed_review=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider,
            reviewer_provider=provider,
        )
        assert result.final_status == "review_failed"
        assert "malformed" in result.error.lower()


# ---------------------------------------------------------------------------
# 12-13. Tests run in staging, target has no artifacts
# ---------------------------------------------------------------------------

class TestStagingTestExecution:
    def test_test_result_in_round(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        for rd in result.rounds:
            # Without --test-command, test_passed is None and summary is "tests_not_run"
            assert rd.test_passed is None
            assert rd.test_summary == "tests_not_run"


# ---------------------------------------------------------------------------
# 14-15. changed_target_files=[] and staged_files non-empty
# ---------------------------------------------------------------------------

class TestFileTracking:
    def test_changed_target_files_empty_staged_mode(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert result.changed_target_files == []

    def test_staged_files_nonempty(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert len(result.staged_files) > 0


# ---------------------------------------------------------------------------
# 16. CLI output tells user remedy report
# ---------------------------------------------------------------------------

class TestCLIOutput:
    def test_summary_mentions_mode(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        summary = summarize_pingpong(result)
        assert "staged" in summary.lower()

    def test_json_export_has_required_fields(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = export_pingpong_json(result)
        required = [
            "run_id", "goal", "mode", "builder_provider", "reviewer_provider",
            "max_rounds", "total_rounds", "final_status", "staged_files",
            "changed_target_files", "target_mutated", "rounds",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# 17. No secrets from .env* enter context pack
# ---------------------------------------------------------------------------

class TestContextSafety:
    def test_no_env_secrets_in_context(self, demo_repo: Path):
        context, categories = build_repo_context(str(demo_repo), "Fix something")
        assert "secret123" not in context
        assert "hunter2" not in context
        assert "API_KEY" not in context
        assert "DB_PASSWORD" not in context

    def test_env_files_excluded_from_tree(self, demo_repo: Path):
        context, categories = build_repo_context(str(demo_repo), "Fix something")
        assert ".env" not in context.split("\n")
        assert ".env.local" not in context.split("\n")

    def test_context_includes_goal(self, demo_repo: Path):
        context, categories = build_repo_context(str(demo_repo), "Fix the README")
        assert "Fix the README" in context
        assert "goal" in categories

    def test_context_includes_file_tree(self, demo_repo: Path):
        context, categories = build_repo_context(str(demo_repo), "Fix something")
        assert "file_tree" in categories
        assert "README.md" in context

    def test_context_bounded(self, demo_repo: Path):
        context, categories = build_repo_context(str(demo_repo), "Fix something")
        assert len(context) < 200000  # Bounded


# ---------------------------------------------------------------------------
# Provider factory
# ---------------------------------------------------------------------------

class TestProviderFactory:
    def test_create_fake(self):
        p = create_provider("fake")
        assert p.name == "fake"

    def test_create_claude(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
        p = create_provider("claude")
        assert p.name == "claude"


# ---------------------------------------------------------------------------
# Export safety
# ---------------------------------------------------------------------------

class TestExportSafety:
    def test_no_raw_prompts_in_export(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = export_pingpong_json(result)
        text = json.dumps(data)
        # No builder system prompt should appear
        assert "You are a Builder" not in text
        assert "You are a code Reviewer" not in text

    def test_no_repo_path_in_export(self, demo_repo: Path):
        result = run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        data = export_pingpong_json(result)
        # repo_path should not contain absolute staging path
        text = json.dumps(data)
        assert "/tmp/remedy-pingpong-" not in text


# F085 T002b — pingpong_loop._run_test_command on the shared `test`-class seam


def test_pingpong_loop_test_command_runs_on_the_guarded_seam(tmp_path, monkeypatch):
    """The spawn goes through `run_guarded_test_command`, and its BYTES decode to str."""
    import subprocess

    from packages.orchestration import pingpong_loop

    seen: dict[str, object] = {}

    def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
        seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
        return subprocess.CompletedProcess(list(cmd), 0, b"out-line\n", b"err-line\n")

    monkeypatch.setattr(pingpong_loop, "run_guarded_test_command", _fake_guarded)
    passed, summary = pingpong_loop._run_test_command("pytest -q", tmp_path, timeout_sec=17)

    assert passed is True
    assert seen == {"cmd": ["pytest", "-q"], "timeout_sec": 17, "cwd": str(tmp_path)}
    assert summary.startswith("exit=0")
    assert "out-line" in summary
    assert "err-line" in summary


# F112 T003b2a — compiled_context_token_budget passthrough on run_pingpong


class TestCompiledContextTokenBudget:
    """compiled_context_token_budget must reach compile_task_context's own
    token_budget kwarg only when the caller supplies it (DECISION F112 D3)."""

    def test_token_budget_reaches_compile_task_context(self, demo_repo, monkeypatch):
        from packages.orchestration import context_compiler

        captured: dict[str, object] = {}
        real_compile = context_compiler.compile_task_context

        def _spy(root, fenced_paths, repo_paths, **kwargs):
            captured.update(kwargs)
            return real_compile(root, fenced_paths, repo_paths, **kwargs)

        monkeypatch.setattr(context_compiler, "compile_task_context", _spy)

        run_pingpong(
            "Fix something", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            compiled_context_paths=["src/main.py"],
            compiled_context_candidates=["src/main.py", "README.md"],
            compiled_context_token_budget=777,
        )

        assert captured.get("token_budget") == 777

    def test_no_token_budget_kwarg_when_caller_omits_it(self, demo_repo, monkeypatch):
        from packages.orchestration import context_compiler

        captured: dict[str, object] = {}
        real_compile = context_compiler.compile_task_context

        def _spy(root, fenced_paths, repo_paths, **kwargs):
            captured.update(kwargs)
            return real_compile(root, fenced_paths, repo_paths, **kwargs)

        monkeypatch.setattr(context_compiler, "compile_task_context", _spy)

        run_pingpong(
            "Fix something", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            compiled_context_paths=["src/main.py"],
            compiled_context_candidates=["src/main.py", "README.md"],
        )

        assert "token_budget" not in captured
