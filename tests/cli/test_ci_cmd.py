"""Contract tests for the `remedy ci` CLI seam.

The seam is thin by design, so these pin the three things that can rot: the
catalog entry and its handler agree, the summary reports every stage including
the ones CI never runs, and the argv a stage builds really reaches
`scripts/remedy_pytest_runner.py` as a subprocess.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from apps.cli.command_catalog import GROUPS, get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.commands.ci_cmd import repo_root_for_ci, summarize_ci_results
from packages.orchestration.ci_run import StageResult, stage_command
from packages.orchestration.ci_stages import ci_stage_by_name

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_ci_group_and_entry_declare_that_the_command_executes():
    assert "ci" in GROUPS
    assert GROUPS["ci"].user_facing is False
    cmd = get_command("ci.run")
    assert cmd.group_id == "ci"
    assert cmd.subcommand == "run"
    assert cmd.action_class == "test_execution"
    assert cmd.may_execute_commands is True


def test_ci_run_handler_is_reachable_from_the_cli():
    assert "ci.run" in collect_all_handlers()


def test_repo_root_is_the_repository_root():
    assert repo_root_for_ci() == REPO_ROOT
    assert (repo_root_for_ci() / "scripts" / "remedy_pytest_runner.py").is_file()


def test_summary_reports_a_skipped_stage_instead_of_dropping_it():
    note = "not run by CI — run it manually with: pytest -m real_ollama"
    results = (
        StageResult(stage="fast", ran=True, exit_code=0, duration_s=1.0, note=""),
        StageResult(stage="excluded", ran=False, exit_code=None, duration_s=0.0, note=note),
    )
    table = summarize_ci_results(results)
    assert "excluded" in table
    assert "skipped" in table
    assert "passed" in table
    assert "run it manually" in table


def test_summary_names_the_failing_exit_code():
    results = (StageResult(stage="fast", ran=True, exit_code=2, duration_s=0.5, note=""),)
    assert "failed(2)" in summarize_ci_results(results)


@pytest.mark.subprocess
def test_a_stage_argv_really_reaches_the_pytest_runner():
    """Launch a real stage argv through the runner script, not a stub.

    The tests above prove the wiring without spawning anything; this one proves
    the seam a user actually hits.
    """
    command = stage_command(ci_stage_by_name("fast"), REPO_ROOT)
    assert command[1].endswith("scripts/remedy_pytest_runner.py")
    assert command[2] == "--"
    probe = [*command[:3], "--collect-only", "-q", "tests/cli/test_ci_cmd.py"]
    completed = subprocess.run(
        probe, cwd=REPO_ROOT, capture_output=True, text=True, timeout=300, check=False
    )
    assert completed.returncode == 0, completed.stdout[-2000:] + completed.stderr[-2000:]
