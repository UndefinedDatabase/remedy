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

from packages.orchestration.ci_budgets import (
    LINT_ERROR_CEILING,
    BudgetCheck,
    check_lint_ceiling,
    parse_ruff_error_count,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_the_ceiling_is_the_ratcheted_number_decision_d5_froze():
    assert LINT_ERROR_CEILING == 26


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


def test_a_count_below_the_ceiling_is_ok():
    check = check_lint_ceiling(25)
    assert isinstance(check, BudgetCheck)
    assert check.ok is True
    assert (check.observed, check.ceiling) == (25, LINT_ERROR_CEILING)


def test_a_count_exactly_at_the_ceiling_is_ok_because_the_ceiling_is_inclusive():
    check = check_lint_ceiling(LINT_ERROR_CEILING)
    assert check.ok is True


def test_a_count_above_the_ceiling_fails_and_says_not_to_raise_the_ceiling():
    check = check_lint_ceiling(27)
    assert check.ok is False
    assert "27" in check.detail
    assert "do not raise the ceiling" in check.detail


@pytest.mark.subprocess
def test_this_repository_really_is_at_or_below_the_lint_ceiling():
    """The live ratchet: ruff's own reading of this repository, its own config.

    If this goes red the finding is the NEW errors, not the ceiling. Lowering
    the count is the fix; editing `LINT_ERROR_CEILING` upward is forbidden by
    DECISION F083 D5.
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
    check = check_lint_ceiling(observed)
    assert check.ok, check.detail
