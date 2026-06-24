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
            # Group name should not appear as a command row
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
        """Internal groups still exist in GROUPS and can be parsed."""
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
        """do run --json includes next_commands with actual run_id."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong(
            "Fix README", str(demo),
            builder_provider=p, reviewer_provider=p, max_rounds=2,
        )
        from packages.orchestration.pingpong_loop import export_pingpong_json
        data = export_pingpong_json(result)
        nc = data.get("next_commands", {})
        assert "report" in nc
        assert "promote_dry_run" in nc
        assert "promote_approve" in nc
        assert result.run_id in nc["report"]
        assert result.run_id in nc["promote_approve"]

    def test_no_git_in_next_commands(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        data = export_pingpong_json(result)
        nc_str = json.dumps(data.get("next_commands", {}))
        assert "git commit" not in nc_str
        assert "git push" not in nc_str


# ---------------------------------------------------------------------------
# 10-14. Provider evidence and token accounting
# ---------------------------------------------------------------------------

class TestProviderEvidence:
    def test_provider_evidence_in_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        data = export_pingpong_json(result)
        pe = data.get("provider_evidence", {})
        assert "builder_provider" in pe
        assert "reviewer_provider" in pe


class TestTokenAccounting:
    def test_token_accounting_in_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        data = export_pingpong_json(result)
        ta = data.get("token_accounting", {})
        assert "kind" in ta
        assert ta["kind"] in ("estimated", "actual")
        assert "actual_tokens_available" in ta

    def test_fake_provider_reports_actual(self, tmp_path, monkeypatch):
        """FakeProvider reports synthetic tokens — kind is actual."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        data = export_pingpong_json(result)
        ta = data["token_accounting"]
        # FakeProvider sets tokens_used > 0, so kind is actual
        assert ta["kind"] == "actual"
        assert ta["actual_tokens_available"] is True
        assert ta["builder_tokens_actual"] > 0

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
        # Zero out all token counts to simulate no-token provider
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
# 15-19. Concise text report
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
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
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
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)

        from apps.cli.commands.do_cmd import _cmd_do_report
        _cmd_do_report(result.run_id, json_output=False)
        out = capsys.readouterr().out
        assert "Next steps:" in out
        assert "--dry-run" in out
        assert "--approve" in out


# ---------------------------------------------------------------------------
# 20-25. Existing flows still work (smoke)
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
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
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
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        # Dry-run does not mutate
        dr = promote_run(result.run_id, target_repo=str(demo), dry_run=True)
        assert dr.status == "dry_run"
        # Approved works
        ap = promote_run(result.run_id, target_repo=str(demo), approve=True)
        assert ap.status == "promoted"

    def test_json_still_parseable(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong
        from packages.orchestration.pingpong_provider import FakeProvider
        p = FakeProvider()
        demo = tmp_path / "repo"
        demo.mkdir()
        (demo / "README.md").write_text("# Test\n")
        result = run_pingpong("Fix", str(demo), builder_provider=p, reviewer_provider=p)
        data = export_pingpong_json(result)
        text = json.dumps(data)
        parsed = json.loads(text)
        assert parsed["run_id"] == result.run_id
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
        """No groups deleted — only hidden from default help."""
        assert len(GROUPS) >= 40
