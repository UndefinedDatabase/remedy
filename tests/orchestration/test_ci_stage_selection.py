"""Selection tests for the F083 CI stage table, measured against a fixture tree.

`test_ci_stages.py` reads the table structurally and defers the question this
file answers: whether each stage's marker expression SELECTS what its
description claims. The subject is a FIXTURE tree whose markers are known by
construction, so every assertion pins an EXPRESSION rather than the live suite —
pinning live collected counts would go red whenever an unrelated commit added a
test, the carried finding R-0205 this feature owns. The one live-suite test
asserts a PROPERTY and never a count: that no test here escapes the stage set.

Every property below that reasons about the UNION or the OVERLAP of the stages
scopes itself to the MARKER-selected stages — `runs_in_ci and not
stage.test_paths`. A path-bearing stage such as `budgets` selects by path and
carries the marker expression `not real_ollama`, so folding it into a marker
union would report every uncovered test in the repository as covered. That is a
false green of exactly the kind this feature exists to detect.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.ci_stages import CI_STAGES, ci_stage_by_name

REPO_ROOT = Path(__file__).resolve().parents[2]
LIVE_MODULES = {"test_live_only.py", "test_live_integration.py"}

#: One fixture module per marker combination the stage set distinguishes.
FIXTURE_MODULES: dict[str, tuple[str, ...]] = {
    "test_plain.py": (),
    "test_slow_only.py": ("slow",),
    "test_integration_only.py": ("integration",),
    "test_subprocess_only.py": ("subprocess",),
    "test_ui_only.py": ("ui_contract",),
    "test_smoke_only.py": ("smoke",),
    "test_live_only.py": ("real_ollama",),
    "test_subprocess_and_smoke.py": ("subprocess", "smoke"),
    "test_live_integration.py": ("integration", "real_ollama"),
}
FIXTURE_MARKERS = ("slow", "integration", "subprocess", "ui_contract", "smoke", "real_ollama")


@pytest.fixture(scope="module")
def fixture_tree(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A tiny pytest tree whose markers are known by construction, not measured."""
    tree = tmp_path_factory.mktemp("ci_stage_selection")
    ini = ["[pytest]", "markers ="] + [f"    {name}: fixture marker" for name in FIXTURE_MARKERS]
    (tree / "pytest.ini").write_text("\n".join(ini) + "\n")
    for filename, markers in FIXTURE_MODULES.items():
        lines = ["import pytest", ""] + [f"@pytest.mark.{m}" for m in markers]
        (tree / filename).write_text("\n".join([*lines, "def test_case():", "    pass", ""]))
    return tree


def collect_in_tree(tree: Path, marker_expression: str) -> set[str]:
    """The fixture modules `marker_expression` selects, by filename.

    Collection runs in a CHILD process against the tree's own config, so the
    repository's `pyproject.toml` and conftest cannot colour the result.
    """
    argv = [sys.executable, "-m", "pytest", str(tree), "-c", str(tree / "pytest.ini"),
            "--collect-only", "-q", "-p", "no:cacheprovider", "-m", marker_expression]
    done = subprocess.run(argv, cwd=tree, capture_output=True, text=True, timeout=120, check=False)
    assert done.returncode in (0, 5), done.stdout[-2000:] + done.stderr[-2000:]
    return {line.split("::")[0] for line in done.stdout.splitlines() if "::" in line}


def selection_for(tree: Path, stage_name: str) -> set[str]:
    """What the named stage's own expression selects out of the fixture tree."""
    return collect_in_tree(tree, ci_stage_by_name(stage_name).marker_expression)


def test_fast_selects_only_the_module_carrying_no_marker_at_all(fixture_tree: Path):
    assert selection_for(fixture_tree, "fast") == {"test_plain.py"}


def test_standard_selects_integration_and_subprocess_but_never_live(fixture_tree: Path):
    assert selection_for(fixture_tree, "standard") == {
        "test_integration_only.py", "test_subprocess_only.py", "test_subprocess_and_smoke.py"}


def test_ui_selects_the_ui_contract_module_alone(fixture_tree: Path):
    assert selection_for(fixture_tree, "ui") == {"test_ui_only.py"}


def test_smoke_selects_both_smoke_modules_including_the_overlapping_one(fixture_tree: Path):
    assert selection_for(fixture_tree, "smoke") == {"test_smoke_only.py", "test_subprocess_and_smoke.py"}


def test_excluded_selects_every_live_provider_module_and_only_those(fixture_tree: Path):
    assert selection_for(fixture_tree, "excluded") == LIVE_MODULES


def marker_selected_stages() -> tuple[str, ...]:
    """The stages CI runs that select by MARKER alone — see the module docstring."""
    return tuple(s.name for s in CI_STAGES if s.runs_in_ci and not s.test_paths)


def test_no_ci_stage_ever_selects_a_live_provider_module(fixture_tree: Path):
    """The exclusion is the honesty claim of the whole table (DECISION F083 D2)."""
    for name in marker_selected_stages():
        assert selection_for(fixture_tree, name) & LIVE_MODULES == set(), name


def test_exactly_one_fixture_module_lands_in_two_ci_stages(fixture_tree: Path):
    """The inventory measured exactly one overlapping pair; this names it."""
    counts: dict[str, int] = {}
    for name in marker_selected_stages():
        for filename in selection_for(fixture_tree, name):
            counts[filename] = counts.get(filename, 0) + 1
    assert [name for name, seen in counts.items() if seen > 1] == ["test_subprocess_and_smoke.py"]


def test_a_slow_only_module_is_selected_by_no_ci_stage(fixture_tree: Path):
    """The table's one blind spot, pinned rather than rediscovered later.

    `fast` excludes `slow` and no other marker-selected stage claims it, so a
    test marked ONLY `slow` would be run by nothing. The live guard below is what
    keeps that hypothetical: no such test exists today.
    """
    for name in marker_selected_stages():
        assert "test_slow_only.py" not in selection_for(fixture_tree, name), name


@pytest.mark.subprocess
def test_no_test_in_this_repository_escapes_the_marker_selected_stages():
    """The union claim in the `ci_stages` docstring, measured as a property.

    Asserts the COMPLEMENT of the marker expressions collects nothing, so it
    stays green as the suite grows and reddens only when a test no stage runs
    appears. Path-bearing stages are excluded from the union for the reason the
    module docstring gives: `not real_ollama` inside a union would report every
    uncovered test as covered. `excluded` STAYS in the union even though CI never
    runs it — it is the term that accounts for the live-provider tests, and
    dropping it would make every one of them look like an escapee.
    """
    union = " or ".join(
        f"({stage.marker_expression})" for stage in CI_STAGES if not stage.test_paths)
    argv = [sys.executable, "-m", "pytest", "--collect-only", "-q",
            "-p", "no:cacheprovider", "-m", f"not ({union})"]
    done = subprocess.run(argv, cwd=REPO_ROOT, capture_output=True, text=True, timeout=600, check=False)
    assert done.returncode == 5, done.stdout[-3000:] + done.stderr[-2000:]
    assert "no tests collected" in done.stdout
