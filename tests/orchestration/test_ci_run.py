"""Guards for the F083 CI stage runner.

No test here spawns pytest: the command runner is injected, so these prove the
WIRING — which argv a stage produces, what a red stage does to the aggregate,
what an excluded stage reports — without paying a suite run to learn it.
"""
from __future__ import annotations

from pathlib import Path

from packages.orchestration.ci_run import (
    PYTEST_RUNNER_SCRIPT,
    StageResult,
    ci_exit_code,
    run_ci_stage,
    stage_command,
)
from packages.orchestration.ci_stages import ci_stage_by_name, pytest_argv_for_stage

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_the_runner_script_this_module_targets_exists():
    assert (REPO_ROOT / PYTEST_RUNNER_SCRIPT).is_file()


def test_stage_command_goes_through_the_runner_and_carries_the_selection():
    stage = ci_stage_by_name("smoke")
    command = stage_command(stage, REPO_ROOT)
    assert command[1] == str(REPO_ROOT / PYTEST_RUNNER_SCRIPT)
    assert command[2] == "--"
    assert command[3:] == pytest_argv_for_stage(stage)
    assert "pytest" not in command[1:2]


def test_running_a_stage_records_the_exit_code_and_a_duration():
    ticks = iter([10.0, 12.5])
    result = run_ci_stage(
        ci_stage_by_name("fast"),
        REPO_ROOT,
        run_command=lambda command: 0,
        monotonic=lambda: next(ticks),
    )
    assert result.ran is True
    assert result.exit_code == 0
    assert result.duration_s == 2.5
    assert result.note == ""


def test_a_timeout_exit_code_is_named_in_the_note():
    result = run_ci_stage(
        ci_stage_by_name("fast"),
        REPO_ROOT,
        run_command=lambda command: 124,
        monotonic=lambda: 0.0,
    )
    assert result.exit_code == 124
    assert "timed out" in result.note


def test_an_excluded_stage_is_not_run_and_names_its_manual_command():
    calls = []
    stage = ci_stage_by_name("excluded")
    result = run_ci_stage(
        stage,
        REPO_ROOT,
        run_command=lambda command: calls.append(command) or 0,
        monotonic=lambda: 0.0,
    )
    assert calls == []
    assert result.ran is False
    assert result.exit_code is None
    assert stage.manual_command in result.note


def test_ci_exit_code_is_red_when_any_stage_that_ran_is_red():
    green = StageResult("fast", True, 0, 1.0, "")
    red = StageResult("standard", True, 1, 1.0, "")
    skipped = StageResult("excluded", False, None, 0.0, "not run by CI")
    assert ci_exit_code((green, skipped)) == 0
    assert ci_exit_code((green, red)) == 1
