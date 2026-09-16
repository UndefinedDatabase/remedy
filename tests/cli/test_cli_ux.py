"""CLI UX tests — default help, advanced commands, next_commands, provider/token evidence."""
from __future__ import annotations

import json
from dataclasses import replace

import pytest

from apps.cli.command_catalog import GROUPS, GroupDef, get_commands_for_group, get_group, resolve_group
from apps.cli.grouped import main as grouped_main

# ---------------------------------------------------------------------------
# User-facing groups that MUST appear in default help
# ---------------------------------------------------------------------------

_USER_FACING_GROUPS = {"do", "job", "project", "ui", "doctor", "config", "worker", "memory"}

# Internal groups that MUST NOT appear in default help
_INTERNAL_GROUPS = {
    "snapshot", "integrity",
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
# 4b. A hidden group is in no help at all and stays callable (amend0905-vocab D4)
# ---------------------------------------------------------------------------

def _listed_groups(out: str) -> list[str]:
    """The first column of every box row of a root help page, the options excluded."""
    names = [line[1:].split()[0] for line in out.splitlines()
             if line.startswith("\u2502") and line[1:-1].strip()]
    return [name for name in names if not name.startswith("-")]


def _hide(monkeypatch, *group_ids: str) -> None:
    for group_id in group_ids:
        monkeypatch.setitem(GROUPS, group_id, replace(GROUPS[group_id], hidden=True))


class TestHiddenGroup:
    def test_a_group_is_not_hidden_unless_it_says_so(self):
        assert GroupDef("x", "X", "An x.").hidden is False
        assert GroupDef("x", "X", "An x.", False, True).hidden is True

    def test_a_hidden_group_is_absent_from_the_default_help(self, capsys, monkeypatch):
        _hide(monkeypatch, "runtime")
        grouped_main(["--help"])
        listed = _listed_groups(capsys.readouterr().out)
        assert "runtime" not in listed
        assert "stats" in listed

    def test_a_hidden_group_is_absent_from_all_commands(self, capsys, monkeypatch):
        _hide(monkeypatch, "runtime", "ci")
        grouped_main(["--all-commands"])
        listed = _listed_groups(capsys.readouterr().out)
        assert "runtime" not in listed and "ci" not in listed
        assert "stats" in listed and "dev" in listed

    def test_a_hidden_groups_own_help_still_lists_its_commands(self, capsys, monkeypatch):
        _hide(monkeypatch, "runtime")
        grouped_main(["runtime", "--help"])
        out = capsys.readouterr().out
        assert "Usage: remedy runtime" in out
        assert set(_listed_groups(out)) == {c.subcommand for c in get_commands_for_group("runtime")}

    def test_a_hidden_groups_command_still_dispatches(self, monkeypatch):
        import apps.cli.grouped as grouped

        _hide(monkeypatch, "ci")
        calls = []
        monkeypatch.setattr(grouped, "_get_dispatch_table", lambda: {"ci.run": calls.append})
        grouped_main(["ci", "run", "--json"])
        assert [args._command_id for args in calls] == ["ci.run"]


# ---------------------------------------------------------------------------
# 4c. `settings` is an alias of `config`: one GroupDef, two words (amend0831 D-D)
# ---------------------------------------------------------------------------

class TestSettingsAlias:
    def test_one_group_def_carries_both_words(self):
        assert "settings" not in GROUPS
        assert GROUPS["config"].aliases == ("settings",)
        assert GroupDef("x", "X", "An x.").aliases == ()

    def test_the_resolver_maps_every_word_to_its_group(self):
        assert [resolve_group(w) for w in ("settings", "config", "no-such-group")] == ["config", "config", None]
        assert get_group("settings") is GROUPS["config"]
        assert get_commands_for_group("settings") == get_commands_for_group("config")

    def test_no_alias_shadows_a_group_or_another_alias(self):
        words = [word for group_def in GROUPS.values() for word in group_def.aliases]
        assert len(words) == len(set(words)) and set(words).isdisjoint(GROUPS)

    def test_settings_help_names_config(self, capsys):
        grouped_main(["settings", "--help"])
        out = capsys.readouterr().out
        assert "Usage: remedy settings" in out and " Also reachable as: remedy config\n" in out
        assert set(_listed_groups(out)) == {c.subcommand for c in get_commands_for_group("config")}

    def test_config_help_names_settings(self, capsys):
        grouped_main(["config", "--help"])
        out = capsys.readouterr().out
        assert "Usage: remedy config" in out and " Also reachable as: remedy settings\n" in out

    def test_bare_settings_prints_the_group_help_naming_config(self, capsys):
        grouped_main(["settings"])
        assert " Also reachable as: remedy config\n" in capsys.readouterr().out

    def test_every_config_command_parses_to_the_same_id_under_both_words(self):
        from apps.cli.grouped import build_parser

        parser = build_parser()
        for cmd in get_commands_for_group("config"):
            fillers = ["x"] * sum(1 for a in cmd.args if not a.is_option and a.required)
            for word in ("config", "settings"):
                args, _unknown = parser.parse_known_args([word, cmd.subcommand, *fillers])
                assert args._command_id == cmd.command_id

    def test_settings_dispatches_exactly_the_config_handler(self, monkeypatch):
        import apps.cli.grouped as grouped

        calls = []
        monkeypatch.setattr(grouped, "_get_dispatch_table", lambda: {"config.list": calls.append})
        grouped_main(["settings", "list", "--json"])
        grouped_main(["config", "list", "--json"])
        assert [args._command_id for args in calls] == ["config.list", "config.list"]
        assert not [cid for cid in grouped._get_dispatch_table() if cid.startswith("settings.")]

    def test_settings_and_config_print_the_same_bytes(self, capsys):
        grouped_main(["settings", "list", "--json"])
        via_alias = capsys.readouterr().out
        grouped_main(["config", "list", "--json"])
        assert via_alias == capsys.readouterr().out and via_alias

    def test_an_unknown_settings_subcommand_is_an_error(self, capsys):
        with pytest.raises(SystemExit) as exc:
            grouped_main(["settings", "no-such-command"])
        assert exc.value.code == 2
        assert "Unknown command 'no-such-command'" in capsys.readouterr().err

    def test_an_alias_of_a_group_with_a_default_command_injects_it(self, monkeypatch):
        import apps.cli.grouped as grouped

        monkeypatch.setitem(GROUPS, "status", replace(GROUPS["status"], aliases=("overview",)))
        calls = []
        monkeypatch.setattr(grouped, "_get_dispatch_table", lambda: {"status.run": calls.append})
        grouped_main(["overview", "--json"])
        assert [args._command_id for args in calls] == ["status.run"]


# ---------------------------------------------------------------------------
# 5. Default happy path includes do commands
# ---------------------------------------------------------------------------

class TestHappyPath:
    def test_happy_path_in_help(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        assert "do run" in out
        assert "job show" in out


# ---------------------------------------------------------------------------
# 6. Default help does not show internal command names
# ---------------------------------------------------------------------------

class TestNoInternalInDefault:
    def test_no_internal_names(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        for name in ["execution", "snapshot", "integrity"]:
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
        assert result.run_id in nc["report"]

    def test_no_git_in_next_commands(self, tmp_path, monkeypatch):
        _, data = _make_run(tmp_path, monkeypatch)
        nc_str = json.dumps(data.get("next_commands", {}))
        assert "git commit" not in nc_str
        assert "git push" not in nc_str


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


# ---------------------------------------------------------------------------
# Quick start tests
# ---------------------------------------------------------------------------

class TestQuickStart:
    def test_quick_start_has_auto_job_id(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        assert "JOB_ID" in out

    def test_quick_start_has_tee(self, capsys):
        grouped_main([])
        out = capsys.readouterr().out
        assert "tee" in out

    def test_quick_start_no_manual_job_id(self):
        import re

        from apps.cli.grouped import _QUICK_START
        assert "<job_id>" not in _QUICK_START
        assert re.findall(r"<[a-z_-]+>", _QUICK_START) == ["<goal>"]

    def test_quick_start_flags_are_declared_by_their_commands(self):
        """Every flag of a quick-start step is one its command declares.

        The advertised-command flag sweep stops at the quote closing `"<goal>"`, so it never
        reads the flags after the goal; this test reads each step to the pipe.
        """
        import re

        from apps.cli.command_catalog import CATALOG
        from apps.cli.grouped import _QUICK_START

        declared = {(c.group_id, c.subcommand): {a.name for a in c.args} for c in CATALOG}
        steps = 0
        for line in _QUICK_START.splitlines():
            m = re.search(r"remedy ([a-z][a-z0-9-]*) ([a-z][a-z0-9-]*)(.*)", line)
            if not m:
                continue
            pair = (m.group(1), m.group(2))
            assert pair in declared, line
            flags = re.findall(r"(?<![\w-])--[a-z][a-z0-9-]*", m.group(3).split("|", 1)[0])
            assert [f for f in flags if f not in declared[pair]] == [], line
            steps += 1
        assert steps == 2


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
        from apps.cli.commands.do_cmd import _cmd_run_show
        _cmd_run_show(result.run_id, json_output=False)
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
        from apps.cli.commands.do_cmd import _cmd_run_show
        _cmd_run_show(result.run_id, json_output=False)
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
        from apps.cli.commands.do_cmd import _cmd_run_show
        _cmd_run_show(result.run_id, json_output=False)
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
        from apps.cli.commands.do_cmd import _cmd_run_show
        _cmd_run_show(result.run_id, json_output=False)
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
        from apps.cli.commands.do_cmd import _cmd_run_show
        _cmd_run_show(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "Remedy Run" in out
        assert "Worker:" in out
        assert "Reviewer:" in out
        assert "Status:" in out


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

    def test_run_group_holds_exactly_show_and_list(self):
        """DECISION amend0905-vocab D4: `run show <id> | list`, and nothing else under `run`."""
        assert sorted(c.subcommand for c in get_commands_for_group("run")) == ["list", "show"]
        assert GROUPS["run"].user_facing is True
        assert GROUPS["run"].hidden is False

    def test_run_commands_have_handlers(self):
        """Nothing else in the suite checks that a catalog id reaches a handler."""
        from apps.cli.commands import collect_all_handlers

        handlers = collect_all_handlers()
        assert "run.show" in handlers
        assert "run.list" in handlers

    def test_all_groups_still_in_catalog(self):
        """Every group DECISION amend0905-vocab D4 keeps is still in the catalog.

        The floor this replaces promised that no group is deleted, only hidden; D4 deletes every group it
        does not name, so the promise holds for its named groups only. `run` joins when F261 creates it.
        """
        kept = {
            "do", "mission", "job", "decision", "status", "stats", "teacher", "memory", "ui", "config",
            "doctor", "project", "init", "worker", "runtime",
            "brain", "event", "patch", "test", "blocker", "change", "file", "snapshot", "self", "ci",
            "integrity", "dev",
            "run",
            "roadmap",
        }
        assert sorted(kept - set(GROUPS)) == []


# ---------------------------------------------------------------------------
# The `run` group's two commands (F261, DECISION amend0905-vocab D4)
# ---------------------------------------------------------------------------

class TestRunList:
    def _one_run(self, tmp_path, monkeypatch, goal):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        demo = tmp_path / "repo"
        demo.mkdir(exist_ok=True)
        (demo / "README.md").write_text("# Test\n")
        p = FakeProvider()
        return run_pingpong(goal, str(demo), builder_provider=p, reviewer_provider=p)

    def test_no_flag_prints_list_runs_verbatim(self, tmp_path, monkeypatch, capsys):
        """`run list --json` prints the bytes `do report list --json` printed."""
        self._one_run(tmp_path, monkeypatch, "Fix")
        from apps.cli.commands.do_cmd import _cmd_run_list
        from packages.orchestration.pingpong_loop import list_runs

        _cmd_run_list(json_output=True)
        assert capsys.readouterr().out == json.dumps(list_runs(), indent=2) + "\n"

    def test_limit_flag_is_honoured(self, tmp_path, monkeypatch, capsys):
        """The five flags the catalog attaches are real, not decoration."""
        self._one_run(tmp_path, monkeypatch, "One")
        self._one_run(tmp_path, monkeypatch, "Two")
        from apps.cli.commands.do_cmd import _cmd_run_list

        _cmd_run_list(json_output=True, limit="1")
        assert len(json.loads(capsys.readouterr().out)) == 1

    def test_unknown_sort_field_exits_without_a_traceback(self, tmp_path, monkeypatch, capsys):
        self._one_run(tmp_path, monkeypatch, "Fix")
        from apps.cli.commands.do_cmd import _cmd_run_list

        with pytest.raises(SystemExit) as exc:
            _cmd_run_list(json_output=True, sort="nope")
        assert exc.value.code == 1
        assert "unknown --sort field" in capsys.readouterr().err

    def test_empty_store_prints_the_empty_message(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "empty"))
        from apps.cli.commands.do_cmd import _cmd_run_list

        _cmd_run_list(json_output=True)
        assert capsys.readouterr().out == "No ping-pong runs found.\n"


class TestRunShow:
    def test_missing_run_exits_one(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "empty"))
        from apps.cli.commands.do_cmd import _cmd_run_show

        with pytest.raises(SystemExit) as exc:
            _cmd_run_show("no-such-run", json_output=True)
        assert exc.value.code == 1
        assert capsys.readouterr().err == "Error: run 'no-such-run' not found.\n"
