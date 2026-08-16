"""Remedy's own CI stages — the five marker selections DECISION F083 D2 ruled.

The stage set is DATA and it lives in exactly one place, so the local `remedy
ci` entrypoint and the hosted workflow files cannot drift into two opinions
about what CI means (T2_F083: "one source of truth for what CI means"). This
module RUNS NOTHING: it holds the selections, the reason each exists, and the
pytest argv a caller hands to the existing subprocess runner
(`scripts/remedy_pytest_runner.py`, which owns the process-group cleanup, the
output caps and the timeout). Wiring that runner, the summary table and the CLI
seam are later rounds; putting them here would make importing the stage table
able to start a test run.

The selections are MEASURED, not guessed: `.agent/f083_inventory.md` Q4
collected all five against the whole suite, their union was the whole suite with
nothing uncovered, and exactly one pair overlapped.

Remedy deliberately does NOT make `safety` and `architecture` stages of their
own (DECISION F083 D2.2) — measured, both are subsets of the selections below
and `safety` straddles two of them, so promoting either would introduce overlaps
this set does not have. They stay markers for ad-hoc selection.

Remedy deliberately does NOT store a collected COUNT per stage: a count is true
for one commit and wrong for the next, and a table carrying stale numbers is
worse than one carrying none.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CiStage:
    """One CI stage: what it selects, why it exists, and whether CI runs it."""

    name: str
    description: str
    marker_expression: str
    runs_in_ci: bool
    manual_command: str
    #: Wall-clock budget for this stage in seconds; 0 for a stage CI never runs.
    timeout_sec: int


#: The stage set DECISION F083 D2.1 ruled, in the order CI runs them.
CI_STAGES: tuple[CiStage, ...] = (
    CiStage(
        name="fast",
        description="Pure unit work: no integration state, no subprocess, no UI contract, no live provider.",
        marker_expression="not integration and not subprocess and not real_ollama and not ui_contract and not smoke and not slow",
        runs_in_ci=True,
        manual_command="",
        timeout_sec=900,
    ),
    CiStage(
        name="standard",
        description="Integration and subprocess tests on the fake provider.",
        marker_expression="(integration or subprocess) and not real_ollama",
        runs_in_ci=True,
        manual_command="",
        timeout_sec=2100,
    ),
    CiStage(
        name="ui",
        description="Python-verifiable frontend and UI contracts.",
        marker_expression="ui_contract and not real_ollama",
        runs_in_ci=True,
        manual_command="",
        timeout_sec=300,
    ),
    CiStage(
        name="smoke",
        description="Smoke contracts for the scripts and the infrastructure.",
        marker_expression="smoke and not real_ollama",
        runs_in_ci=True,
        manual_command="",
        timeout_sec=300,
    ),
    CiStage(
        name="excluded",
        description="Live-provider tests. CI never runs them; they are listed so the coverage claim stays honest.",
        marker_expression="real_ollama",
        runs_in_ci=False,
        manual_command="python3 -m pytest -m real_ollama -q  # needs a running Ollama server",
        timeout_sec=0,
    ),
)


def ci_stage_names() -> tuple[str, ...]:
    """The stage names, in the order CI runs them."""
    return tuple(stage.name for stage in CI_STAGES)


def ci_stage_by_name(name: str) -> CiStage:
    """The stage called `name`; KeyError naming every known stage otherwise."""
    for stage in CI_STAGES:
        if stage.name == name:
            return stage
    known = ", ".join(ci_stage_names())
    raise KeyError(f"unknown CI stage {name!r}; known stages: {known}")


def pytest_argv_for_stage(stage: CiStage) -> list[str]:
    """The pytest arguments that select `stage`. Builds argv; runs nothing."""
    return ["-m", stage.marker_expression, "-q"]
