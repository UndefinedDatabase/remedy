"""CLI UX tests — default help, advanced commands, next_commands, provider/token evidence."""
from __future__ import annotations

import json

from apps.cli.command_catalog import GROUPS
from apps.cli.grouped import main as grouped_main

# ---------------------------------------------------------------------------
# User-facing groups that MUST appear in default help
# ---------------------------------------------------------------------------

_USER_FACING_GROUPS = {"do", "job", "project", "ui", "doctor", "config", "worker", "memory"}

# Internal groups that MUST NOT appear in default help
_INTERNAL_GROUPS = {
    "tournament", "local-candidate", "candidate-quality", "route-policy",
    "token", "context-pack", "self-repair", "execution", "builder",
    "dogfood", "snapshot", "contract", "integrity",
}


# ---------------------------------------------------------------------------
# Helper: create a fake run and export JSON
# ---------------------------------------------------------------------------

def _make_run(tmp_path, monkeypatch, *, test_command="", repo_arg=None):
    """Create a FakeProvider run and return (result, export_data)."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong
    from packages.orchestration.pingpong_provider import FakeProvider
    p = FakeProvider()
    demo = tmp_path / "repo"
    demo.mkdir(exist_ok=True)
    (demo / "README.md").write_text("# Test\n")
    (demo / "main.py").write_text("print('hello')\n")
    result = run_pingpong(
        "Fix README", str(demo) if repo_arg is None else repo_arg,
        builder_provider=p, reviewer_provider=p,
        test_command=test_command,
    )
    data = export_pingpong_json(result)
    return result, data


# ---------------------------------------------------------------------------
# 1-2. Default help hides advanced, shows only user-facing
# ---------------------------------------------------------------------------

class TestDefaultHelp:
    def test_default_help_shows_user_facing(self, capsys):
        grouped_main(["--help"])
        out = capsys.readouterr().out
        for group_id in _USER_FACING_GROUPS:
            assert group_id in out, f"{group_id} should be in default help"

    def test_default_help_hides_internal(self, capsys):
        grouped_main(["--help"])
        out = capsys.readouterr().out
        for group_id in _INTERNAL_GROUPS:
            lines = [l.strip() for l in out.split("\n") if l.strip().startswith(group_id)]
            assert not lines, f"{group_id} should not be in default help commands"

    def test_no_args_shows_default_help(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        assert "do" in out
        assert "Commands" in out
        for group_id in _INTERNAL_GROUPS:
            lines = [l.strip() for l in out.split("\n") if l.strip().startswith(group_id)]
            assert not lines


# ---------------------------------------------------------------------------
# 3. Advanced command listing shows all commands
# ---------------------------------------------------------------------------

class TestAdvancedHelp:
    def test_all_commands_shows_internal(self, capsys):
        grouped_main(["--all-commands"])
        out = capsys.readouterr().out
        for group_id in _INTERNAL_GROUPS:
            assert group_id in out, f"{group_id} should appear in --all-commands"

    def test_all_commands_shows_user_facing_too(self, capsys):
        grouped_main(["--all-commands"])
        out = capsys.readouterr().out
        for group_id in _USER_FACING_GROUPS:
            assert group_id in out


# ---------------------------------------------------------------------------
# 4. Hidden commands remain callable
# ---------------------------------------------------------------------------

class TestHiddenCallable:
    def test_hidden_group_callable(self):
        for group_id in _INTERNAL_GROUPS:
            assert group_id in GROUPS, f"{group_id} should still be in GROUPS"


# ---------------------------------------------------------------------------
# 5. Default happy path includes do commands
# ---------------------------------------------------------------------------

class TestHappyPath:
    def test_happy_path_in_help(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        assert "do run" in out
        assert "do report" in out
        assert "do promote" in out
        assert "--dry-run" in out
        assert "--approve" in out


# ---------------------------------------------------------------------------
# 6. Default help does not show internal command names
# ---------------------------------------------------------------------------

class TestNoInternalInDefault:
    def test_no_internal_names(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        for name in ["self-repair", "execution", "dogfood", "snapshot",
                      "contract", "integrity", "builder-routing"]:
            lines = [l.strip() for l in out.split("\n") if l.strip().startswith(name)]
            assert not lines, f"{name} should not appear in default help"


# ---------------------------------------------------------------------------
# 7-9. next_commands in do run JSON output
# ---------------------------------------------------------------------------

class TestNextCommands:
    def test_next_commands_in_json(self, tmp_path, monkeypatch):
        result, data = _make_run(tmp_path, monkeypatch)
        nc = data.get("next_commands", {})
        assert "report" in nc
        assert "promote_dry_run" in nc
        assert "promote_approve" in nc
        assert result.run_id in nc["report"]
        assert result.run_id in nc["promote_approve"]

    def test_no_git_in_next_commands(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        nc_str = json.dumps(data.get("next_commands", {}))
        assert "git commit" not in nc_str
        assert "git push" not in nc_str

    def test_next_commands_preserve_repo(self, tmp_path, monkeypatch):
        """next_commands preserve original repo argument."""
        demo = tmp_path / "repo"
        demo.mkdir(exist_ok=True)
        (demo / "README.md").write_text("# Test\n")
        result, data = _make_run(tmp_path, monkeypatch, repo_arg=str(demo))
        nc = data["next_commands"]
        assert str(demo) in nc["promote_approve"] or "." in nc["promote_approve"]

    def test_next_commands_with_test_command(self, tmp_path, monkeypatch):
        """When test command used, next_commands include promote with test."""
        _, data = _make_run(tmp_path, monkeypatch, test_command="python3 -m pytest tests/ -q")
        nc = data["next_commands"]
        assert "promote_approve_with_test_json" in nc
        assert "pytest" in nc["promote_approve_with_test_json"]

    def test_next_commands_shell_quote_test(self, tmp_path, monkeypatch):
        """Test command is shell-quoted in next_commands."""
        _, data = _make_run(tmp_path, monkeypatch, test_command="echo 'hello world'")
        nc = data["next_commands"]
        # Should be quoted safely (no raw unquoted spaces)
        assert "promote_approve_with_test" in nc


# ---------------------------------------------------------------------------
# 10-14. Provider evidence and token accounting
# ---------------------------------------------------------------------------

class TestProviderEvidence:
    def test_provider_evidence_in_json(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        pe = data.get("provider_evidence", {})
        assert "builder_provider" in pe
        assert "reviewer_provider" in pe

    def test_provider_evidence_has_kind(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        pe = data["provider_evidence"]
        assert "builder_provider_kind" in pe
        assert "reviewer_provider_kind" in pe

    def test_provider_evidence_has_write_mode(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        pe = data["provider_evidence"]
        assert "builder_write_mode" in pe
        assert "reviewer_write_mode" in pe

    def test_reviewer_write_mode_none(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        pe = data["provider_evidence"]
        assert pe["reviewer_write_mode"] == "none"
        assert pe["reviewer_can_write_staging"] is False

    def test_provider_evidence_no_raw_prompt(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        pe_str = json.dumps(data["provider_evidence"])
        assert "You are a Builder" not in pe_str
        assert "You are a code Reviewer" not in pe_str


class TestTokenAccounting:
    def test_token_accounting_in_json(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data.get("token_accounting", {})
        assert "kind" in ta
        assert ta["kind"] in ("estimated", "actual")
        assert "actual_tokens_available" in ta

    def test_builder_prompt_estimate(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data["token_accounting"]
        assert "builder_prompt_tokens_estimated" in ta
        assert ta["builder_prompt_tokens_estimated"] > 0

    def test_reviewer_prompt_estimate(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data["token_accounting"]
        assert "reviewer_prompt_tokens_estimated" in ta
        assert ta["reviewer_prompt_tokens_estimated"] > 0

    def test_repair_prompt_estimate_field(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data["token_accounting"]
        assert "repair_prompt_tokens_estimated" in ta

    def test_context_token_estimate(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data["token_accounting"]
        assert "context_tokens_estimated" in ta
        assert ta["context_tokens_estimated"] > 0

    def test_full_repo_token_estimate(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data["token_accounting"]
        assert "full_repo_tokens_estimated" in ta
        assert ta["full_repo_tokens_estimated"] > 0

    def test_estimated_savings(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data["token_accounting"]
        assert "estimated_context_savings_tokens" in ta
        assert "estimated_context_savings_ratio" in ta

    def test_context_strategy(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data["token_accounting"]
        assert ta["context_strategy"] == "bounded_task_context"

    def test_fake_provider_not_actual(self, tmp_path, monkeypatch):
        """FakeProvider synthetic tokens are not treated as actual."""
        _, data = _make_run(tmp_path, monkeypatch)
        ta = data["token_accounting"]
        assert ta["kind"] == "estimated"
        assert ta["actual_tokens_available"] is False
        assert "builder_tokens_actual" not in ta

    def test_claude_cli_zero_is_estimated(self, tmp_path, monkeypatch):
        """Claude CLI tokens_used=0 means unavailable, not actual zero."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        # Simulate claude-cli returning 0 tokens
        result.builder_provider = "claude-cli"
        for rd in result.rounds:
            if rd.builder_output:
                rd.builder_output.tokens_used = 0
            if rd.reviewer_output:
                rd.reviewer_output.tokens_used = 0
        data = export_pingpong_json(result)
        ta = data["token_accounting"]
        assert ta["kind"] == "estimated"
        assert ta["actual_tokens_available"] is False
        assert "token_note" in ta

    def test_estimated_when_no_tokens(self, tmp_path, monkeypatch):
        """When provider returns 0 tokens, kind is estimated."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        for rd in result.rounds:
            if rd.builder_output:
                rd.builder_output.tokens_used = 0
            if rd.reviewer_output:
                rd.reviewer_output.tokens_used = 0
        data = export_pingpong_json(result)
        ta = data["token_accounting"]
        assert ta["kind"] == "estimated"
        assert ta["actual_tokens_available"] is False
        assert "builder_tokens_actual" not in ta
        assert "token_note" in ta


# ---------------------------------------------------------------------------
# Full repo estimate tests
# ---------------------------------------------------------------------------

class TestFullRepoEstimate:
    def test_excludes_git_dir(self, tmp_path):
        """Full repo estimate excludes .git directory."""
        from packages.orchestration.pingpong_loop import _estimate_full_repo_tokens
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("print('hello')\n")
        git_dir = repo / ".git"
        git_dir.mkdir()
        (git_dir / "HEAD").write_text("ref: refs/heads/main\n")
        est = _estimate_full_repo_tokens(str(repo))
        assert est["full_repo_files_estimated"] == 1  # only main.py

    def test_excludes_node_modules(self, tmp_path):
        from packages.orchestration.pingpong_loop import _estimate_full_repo_tokens
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "app.js").write_text("console.log('hi');\n")
        nm = repo / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("module.exports = {};\n")
        est = _estimate_full_repo_tokens(str(repo))
        assert est["full_repo_files_estimated"] == 1

    def test_excludes_env_files(self, tmp_path):
        from packages.orchestration.pingpong_loop import _estimate_full_repo_tokens
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "app.py").write_text("x = 1\n")
        (repo / ".env").write_text("SECRET=abc\n")
        (repo / ".env.local").write_text("KEY=xyz\n")
        est = _estimate_full_repo_tokens(str(repo))
        assert est["full_repo_files_estimated"] == 1
        assert est["full_repo_files_skipped"] == 2

    def test_excludes_binary_extensions(self, tmp_path):
        from packages.orchestration.pingpong_loop import _estimate_full_repo_tokens
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("x = 1\n")
        (repo / "image.png").write_bytes(b"\x89PNG\r\n")
        (repo / "archive.zip").write_bytes(b"PK\x03\x04")
        est = _estimate_full_repo_tokens(str(repo))
        assert est["full_repo_files_estimated"] == 1
        assert est["full_repo_files_skipped"] >= 2

    def test_deterministic(self, tmp_path):
        """Full repo estimate is deterministic — same result twice."""
        from packages.orchestration.pingpong_loop import _estimate_full_repo_tokens
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "a.py").write_text("x = 1\n")
        (repo / "b.py").write_text("y = 2\n")
        est1 = _estimate_full_repo_tokens(str(repo))
        est2 = _estimate_full_repo_tokens(str(repo))
        assert est1 == est2

    def test_no_file_contents_leaked(self, tmp_path):
        """Full repo estimate returns only counts, no file contents."""
        from packages.orchestration.pingpong_loop import _estimate_full_repo_tokens
        repo = tmp_path / "repo"
        repo.mkdir()
        secret_content = "SUPER_SECRET_VALUE_12345"
        (repo / "config.py").write_text(secret_content)
        est = _estimate_full_repo_tokens(str(repo))
        est_str = json.dumps(est)
        assert secret_content not in est_str

    def test_includes_cap_bytes(self, tmp_path):
        from packages.orchestration.pingpong_loop import _estimate_full_repo_tokens
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "a.py").write_text("x = 1\n")
        est = _estimate_full_repo_tokens(str(repo))
        assert "full_repo_estimate_cap_bytes_per_file" in est
        assert est["full_repo_estimate_cap_bytes_per_file"] > 0

    def test_excludes_data_and_cache_dirs(self, tmp_path):
        from packages.orchestration.pingpong_loop import _estimate_full_repo_tokens
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("x = 1\n")
        for d in [".data", ".cache", "__pycache__", ".pytest_cache"]:
            dp = repo / d
            dp.mkdir()
            (dp / "stuff.txt").write_text("data\n")
        est = _estimate_full_repo_tokens(str(repo))
        assert est["full_repo_files_estimated"] == 1


# ---------------------------------------------------------------------------
# Shell flow tests
# ---------------------------------------------------------------------------

class TestShellFlow:
    def test_shell_flow_has_run_id(self, tmp_path, monkeypatch):
        result, data = _make_run(tmp_path, monkeypatch)
        nc = data["next_commands"]
        assert "shell_flow" in nc
        assert result.run_id in nc["shell_flow"]

    def test_shell_flow_no_git(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        flow = data["next_commands"]["shell_flow"]
        assert "git commit" not in flow
        assert "git push" not in flow

    def test_shell_flow_has_dry_run(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        flow = data["next_commands"]["shell_flow"]
        assert "--dry-run" in flow

    def test_shell_flow_has_approve(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        flow = data["next_commands"]["shell_flow"]
        assert "--approve" in flow


# ---------------------------------------------------------------------------
# Quick start tests
# ---------------------------------------------------------------------------

class TestQuickStart:
    def test_quick_start_has_auto_run_id(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        assert "RUN_ID" in out

    def test_quick_start_has_tee(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        assert "tee" in out

    def test_quick_start_no_manual_run_id(self):
        from apps.cli.grouped import _QUICK_START
        assert "<run_id>" not in _QUICK_START


# ---------------------------------------------------------------------------
# Text report token proof
# ---------------------------------------------------------------------------

class TestTextReportTokenProof:
    def test_text_report_shows_provider_evidence(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        from apps.cli.commands.do_cmd import _cmd_do_report
        _cmd_do_report(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "Worker:" in out
        assert "Reviewer:" in out
        assert "write mode:" in out

    def test_text_report_shows_token_accounting(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        from apps.cli.commands.do_cmd import _cmd_do_report
        _cmd_do_report(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "Token accounting:" in out
        assert "Context sent:" in out

    def test_text_report_shows_savings(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        # Add enough files so full repo > context
        for i in range(20):
            (demo / f"mod_{i}.py").write_text(f"# Module {i}\n" + "x = 1\n" * 50)
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        from apps.cli.commands.do_cmd import _cmd_do_report
        _cmd_do_report(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "Full repo estimate:" in out
        assert "Estimated saved:" in out

    def test_text_report_no_raw_prompts(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        from apps.cli.commands.do_cmd import _cmd_do_report
        _cmd_do_report(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "You are a Builder" not in out
        assert "You are a code Reviewer" not in out
        # No absolute staging paths
        assert "/tmp/remedy-pingpong-" not in out


# ---------------------------------------------------------------------------
# Concise text report (existing)
# ---------------------------------------------------------------------------

class TestConciseTextReport:
    def test_text_report_concise(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix README", str(demo), builder_provider=p, reviewer_provider=p)
        from apps.cli.commands.do_cmd import _cmd_do_report
        _cmd_do_report(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "Remedy Run" in out
        assert "Worker:" in out
        assert "Reviewer:" in out
        assert "Status:" in out

    def test_text_report_shows_promotion(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_promote import promote_run
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p, repair_rounds=2)
        promote_run(result.run_id, target_repo=str(demo), approve=True)
        from apps.cli.commands.do_cmd import _cmd_do_report
        _cmd_do_report(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "Promotion: promoted" in out

    def test_text_report_shows_next_steps(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p, repair_rounds=2)
        from apps.cli.commands.do_cmd import _cmd_do_report
        _cmd_do_report(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "Next steps:" in out
        assert "--dry-run" in out
        assert "--approve" in out


# ---------------------------------------------------------------------------
# Existing flows still work (smoke)
# ---------------------------------------------------------------------------

class TestExistingFlowsSmoke:
    def test_staged_run_still_passes(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p, repair_rounds=2)
        assert result.final_status == "staged_review_passed"

    def test_promote_safety_still_works(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_promote import promote_run
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p, repair_rounds=2)
        dr = promote_run(result.run_id, target_repo=str(demo), dry_run=True)
        assert dr.status == "dry_run"
        ap = promote_run(result.run_id, target_repo=str(demo), approve=True)
        assert ap.status == "promoted"

    def test_json_still_parseable(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        text = json.dumps(data)
        parsed = json.loads(text)
        assert "run_id" in parsed
        assert "next_commands" in parsed
        assert "provider_evidence" in parsed
        assert "token_accounting" in parsed


# ---------------------------------------------------------------------------
# GroupDef.user_facing field integrity
# ---------------------------------------------------------------------------

class TestGroupDefIntegrity:
    def test_user_facing_groups_exist(self):
        for gid in _USER_FACING_GROUPS:
            assert gid in GROUPS
            assert GROUPS[gid].user_facing is True

    def test_internal_groups_marked(self):
        for gid in _INTERNAL_GROUPS:
            assert gid in GROUPS
            assert GROUPS[gid].user_facing is False

    def test_all_groups_still_in_catalog(self):
        assert len(GROUPS) >= 40
