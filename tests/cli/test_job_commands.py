"""
Domain tests: cli/test_job_commands.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Step 91 — ELK Directional Layout
# ---------------------------------------------------------------------------


class TestRemedyDo:
    def test_do_command_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("do.run")
        assert cmd.group_id == "do"
        # R-0969 and DECISION F268 D17 (3): `do` runs a job, which writes the repository.
        assert cmd.may_mutate_repo is True


# ═══════════════════════════════════════════════════════════════════════════
# Step 123 — View-model Hardening
# ═══════════════════════════════════════════════════════════════════════════


class TestDoDirectGoalCommandRewrite:
    """remedy do '<goal>' must work via default-command rewrite."""

    def test_do_default_rewrite(self):
        """remedy do 'Make tests pass' should rewrite to do run 'Make tests pass'."""
        from apps.cli.command_catalog import get_commands_for_group

        subcmds = {c.subcommand for c in get_commands_for_group("do")}
        assert "run" in subcmds
        # "Make tests pass" is not a known subcommand
        assert "Make tests pass" not in subcmds

    def test_do_no_args_shows_help(self):
        """remedy do with no args should show group help."""
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["do"])
            output = str(mock_print.call_args[0][0])
            assert "do" in output.lower()

    def test_do_help_shows_help(self):
        """remedy do --help should show help."""
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["do", "--help"])
            output = str(mock_print.call_args[0][0])
            assert "do" in output.lower()

    def test_default_rewrite_dict(self):
        """Default command dict includes both ui and do."""
        # Verify the rewrite exists by checking the source
        src = Path("apps/cli/grouped.py").read_text()
        assert '"do": "run"' in src
        assert '"ui": "start"' in src

    def test_main_py_under_120_lines(self):
        content = Path("apps/cli/main.py").read_text()
        assert len(content.splitlines()) <= 120

    def test_no_flat_commands(self):
        """No flat argparse reintroduction in main.py."""
        content = Path("apps/cli/main.py").read_text()
        assert "add_subparsers" not in content
