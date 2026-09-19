"""Guards for the repository ceilings the `budgets` CI stage checks.

The parsing and comparison tests are pure: they hand `parse_ruff_error_count`
strings shaped like ruff's own output and never spawn anything. Exactly ONE test
really invokes the linter, and it is marked `subprocess` so the stage table can
see it for what it is. That live test runs the repository's own configuration —
no substituted flag and no `--isolated`, because a reading taken under a
different config is a reading of a different repository (finding R-0463).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration import ci_budgets
from packages.orchestration.ci_budgets import (
    BudgetCheck,
    check_lint_clean,
    parse_ruff_error_count,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_no_lint_ceiling_or_baseline_survives():
    """DECISION amend0911-feedback D7: zero findings, no number to ratchet."""
    assert not hasattr(ci_budgets, "LINT_ERROR_CEILING")
    assert not hasattr(ci_budgets, "check_lint_ceiling")


def test_parse_reads_the_count_out_of_ruffs_own_found_line():
    assert parse_ruff_error_count("some/file.py:1:1: F401 unused\nFound 26 errors.\n") == 26


def test_parse_reads_a_singular_found_line_too():
    assert parse_ruff_error_count("some/file.py:1:1: F821 undefined\nFound 1 error.\n") == 1


def test_parse_reads_a_clean_run_as_zero():
    assert parse_ruff_error_count("All checks passed!\n") == 0


def test_parse_refuses_output_it_cannot_read_rather_than_guessing_zero():
    with pytest.raises(ValueError) as excinfo:
        parse_ruff_error_count("ruff: command exploded\n")
    assert "ruff: command exploded" in str(excinfo.value)


def test_parse_refuses_empty_output():
    with pytest.raises(ValueError):
        parse_ruff_error_count("")


def test_zero_findings_is_ok():
    check = check_lint_clean(0)
    assert isinstance(check, BudgetCheck)
    assert check.ok is True
    assert check.observed == 0


def test_a_single_finding_fails_and_says_not_to_suppress_it():
    check = check_lint_clean(1)
    assert check.ok is False
    assert "1 ruff error" in check.detail
    assert "do not add a baseline, a ceiling" in check.detail


@pytest.mark.subprocess
def test_this_repository_has_no_ruff_findings():
    """The live check: ruff's own reading of this repository, its own config.

    If this goes red the fix is the findings themselves; a baseline, a ceiling,
    a `# noqa` or an ignore is forbidden by DECISION amend0911-feedback D7.
    """
    done = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "."],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    observed = parse_ruff_error_count(done.stdout)
    check = check_lint_clean(observed)
    assert check.ok, f"{check.detail}\n{done.stdout}"
