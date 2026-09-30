"""Guards for the repository ceilings the `budgets` CI stage checks.

The parsing and comparison tests are pure: they hand `parse_ruff_error_count`
strings shaped like ruff's own output and never spawn anything. Exactly ONE test
really invokes the linter, and it is marked `subprocess` so the stage table can
see it for what it is. That live test runs the repository's own configuration —
no substituted flag and no `--isolated`, because a reading taken under a
different config is a reading of a different repository (finding R-0463).
"""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration import ci_budgets
from packages.orchestration.ci_budgets import (
    BUNDLE_BASELINE_CHUNKS,
    BUNDLE_SIZE_CAP_FACTOR,
    BudgetCheck,
    bundle_report,
    check_bundle_size,
    check_lint_clean,
    normalize_chunk_name,
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


def test_normalize_chunk_name_strips_the_vite_hash():
    assert normalize_chunk_name("assets/index-BKD2HAVk.js") == "assets/index.js"
    assert normalize_chunk_name("assets/diffHighlightGrammars-o9XqnLhb.js") == "assets/diffHighlightGrammars.js"


def test_normalize_chunk_name_leaves_an_unhashed_name_alone():
    assert normalize_chunk_name("index.html") == "index.html"
    assert normalize_chunk_name("story/story-player.js") == "story/story-player.js"


def test_bundle_report_sums_bytes_under_the_normalized_name():
    report = bundle_report({"assets/index-AAAA1AAA.js": 100, "assets/index-BBBB2BBB.js": 50})
    assert report.chunks == {"assets/index.js": 150}
    assert report.total_bytes == 150


def test_bundle_size_within_the_baseline_plus_ten_percent_is_ok():
    baseline_total = sum(BUNDLE_BASELINE_CHUNKS.values())
    report = bundle_report(dict(BUNDLE_BASELINE_CHUNKS))
    check = check_bundle_size(report)
    assert check.ok is True
    assert check.observed == baseline_total


def test_a_seeded_bundle_bloat_names_the_chunk_that_grew():
    bloated = dict(BUNDLE_BASELINE_CHUNKS)
    bloated["assets/index-Z9ZZZZZZ.js"] = bloated.pop("assets/index.js") + 500_000
    report = bundle_report(bloated)
    check = check_bundle_size(report)
    assert check.ok is False
    assert "assets/index.js +500000B" in check.detail


def test_bundle_size_cap_is_the_baseline_plus_ten_percent():
    baseline_total = sum(BUNDLE_BASELINE_CHUNKS.values())
    assert BUNDLE_SIZE_CAP_FACTOR == 1.10
    cap = math.ceil(baseline_total * BUNDLE_SIZE_CAP_FACTOR)
    just_over = dict(BUNDLE_BASELINE_CHUNKS)
    just_over["assets/index-Z9ZZZZZZ.js"] = just_over.pop("assets/index.js") + (cap - baseline_total) + 1
    report = bundle_report(just_over)
    check = check_bundle_size(report)
    assert check.ok is False


def test_bundle_size_at_exactly_the_rounded_cap_is_ok():
    baseline_total = sum(BUNDLE_BASELINE_CHUNKS.values())
    cap = math.ceil(baseline_total * BUNDLE_SIZE_CAP_FACTOR)
    at_cap = dict(BUNDLE_BASELINE_CHUNKS)
    at_cap["assets/index-Z9ZZZZZZ.js"] = at_cap.pop("assets/index.js") + (cap - baseline_total)
    report = bundle_report(at_cap)
    check = check_bundle_size(report)
    assert check.ok is True
    assert check.observed == cap


@pytest.mark.subprocess
def test_this_repositorys_ui_bundle_is_within_its_size_cap(tmp_path):
    """The live check: a fresh `vite build` of `apps/ui`, never into the shared
    `apps/ui/dist` (F039 D9), read as this module reads any build."""
    outdir = tmp_path / "dist"
    done = subprocess.run(
        ["node_modules/.bin/vite", "build", "--outDir", str(outdir), "--emptyOutDir"],
        cwd=str(REPO_ROOT / "apps" / "ui"),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    files = {str(p.relative_to(outdir)): p.stat().st_size for p in outdir.rglob("*") if p.is_file()}
    report = bundle_report(files)
    check = check_bundle_size(report)
    assert check.ok, check.detail
