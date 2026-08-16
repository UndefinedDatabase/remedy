"""Structural guards for the F083 CI stage table.

These tests read the table and nothing else: nothing is collected and no count
of the live suite is asserted. Whether each stage SELECTS the right subset is a
different question, measured against a fixture tree in test_ci_stage_selection.py — a test
pinning live collected counts would go red whenever an unrelated commit added a
test, which is the carried finding R-0205 this feature owns.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import pytest

from packages.orchestration.ci_stages import (
    CI_STAGES,
    ci_stage_by_name,
    ci_stage_names,
    pytest_argv_for_stage,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
BOOLEAN_WORDS = {"not", "and", "or"}


def test_stage_names_are_decision_d2_in_run_order():
    assert ci_stage_names() == ("fast", "standard", "ui", "smoke", "budgets", "excluded")
    assert len(set(ci_stage_names())) == len(CI_STAGES)


def test_every_stage_carries_a_description_and_an_expression():
    for stage in CI_STAGES:
        assert stage.description.strip(), stage.name
        assert stage.marker_expression.strip(), stage.name


def test_only_excluded_stays_out_of_ci_and_names_its_manual_command():
    out_of_ci = [stage for stage in CI_STAGES if not stage.runs_in_ci]
    assert [stage.name for stage in out_of_ci] == ["excluded"]
    assert out_of_ci[0].manual_command.strip()


def test_stages_ci_runs_carry_no_manual_command():
    for stage in CI_STAGES:
        if stage.runs_in_ci:
            assert stage.manual_command == "", stage.name


def test_every_marker_named_in_an_expression_is_declared_in_pyproject():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text()
    declared = set(re.findall(r'^\s*"([a-z_]+):', pyproject, re.M))
    for stage in CI_STAGES:
        used = set(re.findall(r"[a-z_]+", stage.marker_expression)) - BOOLEAN_WORDS
        assert used <= declared, (stage.name, sorted(used - declared))


def test_pytest_argv_selects_the_expression_and_nothing_else():
    """Both argv shapes are pinned: a path-less stage, and a path-bearing one.

    A path-less stage's argv ENDS at `-q`; a stage carrying `test_paths` appends
    exactly those paths, in table order, after it. Pinning only the first shape
    would let a path silently vanish from the command that selects it.
    """
    path_less = ci_stage_by_name("smoke")
    assert path_less.test_paths == ()
    assert pytest_argv_for_stage(path_less) == ["-m", path_less.marker_expression, "-q"]

    path_bearing = ci_stage_by_name("budgets")
    assert path_bearing.test_paths
    assert pytest_argv_for_stage(path_bearing) == [
        "-m", path_bearing.marker_expression, "-q", *path_bearing.test_paths]


def test_every_test_path_a_stage_names_resolves_on_disk():
    """A stage whose path has moved runs NOTHING and exits 4 (finding R-0438).

    pytest reports a missing path as an error, not as a failure, so a stage
    pointed at a vanished file is a silently vacuous gate. This test is what
    turns that into a red one.
    """
    for stage in CI_STAGES:
        for relative in stage.test_paths:
            assert (REPO_ROOT / relative).is_file(), (stage.name, relative)


def test_unknown_stage_name_raises_naming_every_known_stage():
    with pytest.raises(KeyError) as excinfo:
        ci_stage_by_name("determinism")
    for name in ci_stage_names():
        assert name in str(excinfo.value)


#: The slowest wall second each stage was MEASURED at, three samples per stage:
#: `.agent/f083_inventory.md` `## Q10` for `fast`, `ui` and `smoke`, `## Q11` for
#: `standard`, whose three uncapped samples span 916.36 s to 935.14 s, and
#: `## Q12` for `budgets`, whose three samples span 1.25 s to 1.32 s.
MEASURED_MAX_WALL_S = {
    "fast": 397.45, "standard": 935.14, "ui": 8.09, "smoke": 11.07, "budgets": 1.32}

#: The budget rule: twice the measured maximum, rounded UP to a whole multiple of
#: this many seconds. Doubling absorbs a slow machine; the rounding keeps the
#: table readable. Changing a budget means re-measuring, not re-guessing.
BUDGET_HEADROOM_FACTOR = 2
BUDGET_ROUNDING_S = 300


def test_every_stage_ci_runs_carries_a_budget_and_excluded_carries_none():
    for stage in CI_STAGES:
        if stage.runs_in_ci:
            assert stage.timeout_sec > 0, stage.name
        else:
            assert stage.timeout_sec == 0, stage.name


def test_each_budget_is_the_documented_multiple_of_the_measured_maximum():
    for stage in CI_STAGES:
        if not stage.runs_in_ci:
            continue
        measured = MEASURED_MAX_WALL_S[stage.name]
        expected = math.ceil(
            BUDGET_HEADROOM_FACTOR * measured / BUDGET_ROUNDING_S
        ) * BUDGET_ROUNDING_S
        assert stage.timeout_sec == expected, stage.name


def test_the_standard_budget_clears_the_runners_default_that_killed_it():
    assert ci_stage_by_name("standard").timeout_sec > 600
    assert ci_stage_by_name("standard").timeout_sec > MEASURED_MAX_WALL_S["standard"]
