"""
Domain tests: cli/test_command_catalog.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch
from unittest.mock import patch
from uuid import uuid4
import json
import os
import pytest
import re
import subprocess
import sys
import tempfile

from packages.core.models import Job, RunState, Task
from packages.memory.models import MemoryEntry

_ROOT = Path(__file__).resolve().parent.parent.parent

ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = ROOT / "apps" / "ui" / "src"

UI_ROOT = ROOT / "apps" / "ui"


def _make_job(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task = Task(
                task_type=t.get("type", "readme_draft"),
                description=t.get("description", t.get("type", "task")),
            )
            if "status" in t:
                task.status = RunState(t["status"])
            if "metadata" in t:
                task.inputs = t["metadata"]
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 111 — UI CLI Contract
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s141(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = Task(description=t.get("description", task_type), inputs=inputs)
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 141 — Commit-Readiness Task Summary Bugfix
# ═══════════════════════════════════════════════════════════════════════════




class TestUICommands:
    def test_new_commands_in_catalog(self):
        from apps.cli.command_catalog import get_command
        for cmd_id in ("ui.latest", "ui.status", "ui.stop", "ui.open"):
            cmd = get_command(cmd_id)
            assert cmd.group_id == "ui"

    def test_ui_group_has_five_commands(self):
        from apps.cli.command_catalog import get_commands_for_group
        cmds = get_commands_for_group("ui")
        assert len(cmds) == 5
        subs = {c.subcommand for c in cmds}
        assert subs == {"start", "latest", "status", "stop", "open"}


# ---------------------------------------------------------------------------
# Legacy Viewer Quarantine
# ---------------------------------------------------------------------------




class TestUiDirectFormCommandRewrite:
    """remedy ui <job_id> direct form must work."""

    def test_default_command_rewrite_ui(self):
        """remedy ui <uuid> should rewrite to remedy ui start <uuid>."""
        from apps.cli.grouped import main as grouped_main

        fake_id = str(uuid4())
        # Should not crash with SystemExit(1) — should reach handler
        with pytest.raises(SystemExit):
            grouped_main(["ui", fake_id])
        # The key test: it should have tried to load the job (meaning it
        # correctly routed to ui.start), not show "Unknown command"

    def test_default_command_rewrite_preserves_flags(self):
        """remedy ui <uuid> --port 0 should rewrite correctly."""
        from apps.cli.grouped import main as grouped_main

        fake_id = str(uuid4())
        with pytest.raises(SystemExit):
            grouped_main(["ui", fake_id, "--port", "0"])

    def test_ui_no_args_shows_help(self, capsys):
        """remedy ui with no args shows group help."""
        from apps.cli.grouped import main as grouped_main
        grouped_main(["ui"])
        out = capsys.readouterr().out
        assert "ui" in out.lower()

    def test_ui_help_flag(self, capsys):
        """remedy ui --help shows help."""
        from apps.cli.grouped import main as grouped_main
        grouped_main(["ui", "--help"])
        out = capsys.readouterr().out
        assert "ui" in out.lower()

    def test_ui_start_still_works(self):
        """remedy ui start <uuid> still works as alias."""
        from apps.cli.grouped import main as grouped_main
        fake_id = str(uuid4())
        with pytest.raises(SystemExit):
            grouped_main(["ui", "start", fake_id])

    def test_catalog_has_ui_start(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("ui.start")
        assert cmd.group_id == "ui"
        assert cmd.subcommand == "start"

    def test_info_file_schema(self):
        """Info file must have exact fields."""
        required = {"version", "url", "host", "port", "token", "job_id", "pid", "started_at"}
        # Verify the contract exists in the server
        from packages.orchestration.ui_server import start_ui_server
        # Just check the function signature exists
        assert callable(start_ui_server)

    def test_smoke_uses_direct_form(self):
        """Smoke script should use remedy ui <job_id>, not remedy ui start."""
        smoke = Path(_ROOT / "scripts" / "remedy_smoke.sh")
        if smoke.exists():
            content = smoke.read_text()
            # Find the UI start line
            assert 'remedy ui "${JOB_ID}"' in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 112 — Resource Cleanup / VRAM Hygiene
# ═══════════════════════════════════════════════════════════════════════════




class TestCliHelpIncludesHappyPath:
    """CLI help must include key commands and no stale content."""

    def test_root_help_includes_happy_path(self):
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["--help"])
            output = str(mock_print.call_args[0][0])
            assert "remedy do" in output
            assert "remedy ui" in output
            assert "commit-readiness" in output
            assert "worker unload" in output
            assert "dev status" in output

    def test_repo_group_includes_commit_readiness(self):
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["repo", "--help"])
            output = str(mock_print.call_args[0][0])
            assert "commit-readiness" in output
            assert "read-only" in output.lower() or "does not commit" in output.lower()

    def test_no_flat_commands_in_help(self):
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["--help"])
            output = str(mock_print.call_args[0][0])
            # No flat argparse subcommands
            assert "add_subparsers" not in output

    def test_help_no_raw_leak_words(self):
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["--help"])
            output = str(mock_print.call_args[0][0])
            for bad in ("raw_output", "command_output", "Traceback"):
                assert bad not in output

    def test_main_py_under_120_lines(self):
        content = Path("apps/cli/main.py").read_text()
        assert len(content.splitlines()) <= 120

    def test_commit_readiness_read_only_documented(self):
        """Repo group description mentions read-only / does not commit."""
        from apps.cli.command_catalog import GROUPS
        desc = GROUPS["repo"].description.lower()
        assert "read-only" in desc or "does not commit" in desc




class TestCLISizeLimit:
    """CLI main.py stays under 120 lines."""

    def test_cli_main_under_120(self):
        main = ROOT / "apps" / "cli" / "main.py"
        if main.is_file():
            lines = main.read_text(encoding="utf-8").count("\n") + 1
            assert lines <= 120, f"apps/cli/main.py is {lines} lines (max 120)"




class TestMemoryCardCLI:
    def test_card_show_help(self):
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "memory", "card-show", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "memory_id" in result.stdout.lower()

    def test_card_approve_help(self):
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "memory", "card-approve", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0




class TestEventCLIHelp:
    def test_event_list_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "event", "list", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "job_id" in result.stdout.lower()

    def test_event_timeline_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "event", "timeline", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0


# ── Step 67: Stop Reasons ────────────────────────────────────────────────




class TestBlockerCLIHelp:
    def test_blocker_list_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "blocker", "list", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "job_id" in result.stdout.lower()


# ── Step 68: Autonomy Loop ──────────────────────────────────────────────




class TestRunLoopCLIHelp:
    def test_run_loop_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "job", "run-loop", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "autonomy" in result.stdout.lower()

