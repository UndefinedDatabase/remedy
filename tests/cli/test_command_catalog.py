"""
Domain tests: cli/test_command_catalog.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest

from packages.core.models import RunState
from packages.orchestration.pingpong_job import JobPlan, TaskEntry

_ROOT = Path(__file__).resolve().parent.parent.parent

ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = ROOT / "apps" / "ui" / "src"

UI_ROOT = ROOT / "apps" / "ui"


def _make_job(*, tasks=None, name="test"):
    job = JobPlan(job_title=name)
    if tasks:
        for t in tasks:
            task = TaskEntry(
                title=t.get("description", t.get("type", "task")),
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
    job = JobPlan(job_title=name)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = TaskEntry(title=t.get("description", task_type), inputs=inputs)
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 141 — Commit-Readiness Task Summary Bugfix
# ═══════════════════════════════════════════════════════════════════════════




class TestUICommands:
    """amend1015f D22: `ui` keeps only `start` and `stop`, as warning aliases of `serve`."""

    def test_the_ui_group_holds_only_the_two_aliases(self):
        from apps.cli.command_catalog import get_commands_for_group
        cmds = get_commands_for_group("ui")
        assert {c.subcommand: c.related for c in cmds} == {
            "start": ("serve.start",), "stop": ("serve.stop",)}

    def test_latest_status_and_open_are_gone_with_a_history_line(self):
        from apps.cli.command_catalog import CATALOG, RETIRED_COMMANDS
        ids = {c.command_id for c in CATALOG}
        assert not ids & {"ui.latest", "ui.status", "ui.open"}
        assert not ids & set(RETIRED_COMMANDS)
        for cid in ("ui.latest", "ui.status", "ui.open"):
            assert "Removed 2026-10-15" in RETIRED_COMMANDS[cid]


# ---------------------------------------------------------------------------
# Legacy Viewer Quarantine
# ---------------------------------------------------------------------------




class TestUiDirectFormCommandRewrite:
    """`remedy ui <job_id>` and `remedy ui start|stop` reach the serve handlers with a warning
    (amend1015f D22); no test starts a real supervisor."""

    @pytest.fixture
    def serve_calls(self, monkeypatch):
        from apps.cli.commands import serve_cmd
        calls: list[str] = []
        for word in ("start", "stop"):
            monkeypatch.setitem(serve_cmd.COMMAND_HANDLERS, f"serve.{word}",
                                lambda args, _w=word: calls.append(_w))
        return calls

    def test_default_command_rewrite_ui(self, serve_calls, capsys):
        """remedy ui <uuid> rewrites to remedy ui start <uuid>, which runs serve start."""
        from apps.cli.grouped import main as grouped_main

        grouped_main(["ui", str(uuid4())])
        assert serve_calls == ["start"]
        assert "`remedy ui start` is deprecated" in capsys.readouterr().err

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

    def test_ui_start_and_stop_run_serve_and_warn(self, serve_calls, capsys):
        from apps.cli.grouped import main as grouped_main
        grouped_main(["ui", "start", str(uuid4()), "--json"])
        grouped_main(["ui", "stop", "--json"])
        assert serve_calls == ["start", "stop"]
        err = capsys.readouterr().err
        assert "use `remedy serve start` instead" in err.lower()
        assert "use `remedy serve stop` instead" in err.lower()

    def test_catalog_has_ui_start(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("ui.start")
        assert cmd.group_id == "ui"
        assert cmd.subcommand == "start"


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
            # Root help shows group names (not subcommands)
            assert "do" in output
            # amend1015f D22: `ui` left the default help with the old cockpit.
            assert "job" in output
            assert "worker" in output
            assert "doctor" in output

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
