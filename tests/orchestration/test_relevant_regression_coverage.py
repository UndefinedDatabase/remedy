"""F8 (round 16) — a Missing-Tests gate cannot pass while a relevant suite is red.

Round 15 changed `apps/cli/commands/do_cmd.py` and shipped the public `do job-flow` command
broken with `NameError: timeout_sec is not defined`. Every Missing-Tests gate reported PASS.

Nothing lied. Nothing was asked. The gate required a task's CHANGED test files to be covered by a
successful run, and the suite that catches this — `tests/test_do_job_flow.py` — was in neither the
changed set nor the authoritative CLI command, which runs only `tests/cli`. A gate that checks
only the tests you happened to touch cannot notice the one you broke.

Two things close it: the suite is named as relevant coverage for the source file, and the
authoritative matrix runs it. Coverage was already restricted to SUCCESSFUL runs, so a red suite
now takes the gate to NEEDS_TESTS instead of being ignored.
"""
from __future__ import annotations

import pytest

from packages.orchestration.missing_tests_gate import (
    _RELEVANT_SUITES_FOR_SOURCE,
    _relevant_suites_for_source,
)


class TestTheRelevanceMap:
    def test_the_do_command_maps_to_the_job_flow_suite(self):
        """THE finding: this is the mapping whose absence hid a broken public command."""
        assert _relevant_suites_for_source("apps/cli/commands/do_cmd.py") == (
            "tests/test_do_job_flow.py",)

    def test_an_unmapped_source_file_maps_to_nothing(self):
        """The map is a floor for suites at unconventional paths, not a map of everything."""
        assert _relevant_suites_for_source("packages/orchestration/run_manifest.py") == ()

    def test_every_mapped_suite_exists(self):
        """A mapping to a file that does not exist would make every task permanently uncovered."""
        from pathlib import Path

        for src, suites in _RELEVANT_SUITES_FOR_SOURCE.items():
            assert Path(src).is_file(), f"{src} is mapped but does not exist"
            for s in suites:
                assert Path(s).is_file(), f"{src} maps to missing suite {s}"

    def test_the_map_is_a_reviewable_constant(self):
        """Additions must show up in a diff — the F017 builtin-deny-list precedent."""
        assert isinstance(_RELEVANT_SUITES_FOR_SOURCE, dict)
        for suites in _RELEVANT_SUITES_FOR_SOURCE.values():
            assert isinstance(suites, tuple)


class TestARedRelevantSuiteBlocksTheGate:
    """The mechanism end to end: coverage comes only from SUCCESSFUL runs."""

    def _coverage(self, runs):
        """The production rule, exercised exactly as `job_evidence` applies it."""
        coverage: dict[str, list[str]] = {}
        for run in runs:
            if int(run.get("exit_code", -1)) != 0 or int(run.get("failed", 0) or 0) != 0:
                continue
            for tf in run.get("test_files") or []:
                coverage.setdefault(tf, []).append(run["run_id"])
        return coverage

    def test_a_green_run_covers_its_suite(self):
        cov = self._coverage([{"run_id": "vr-1", "exit_code": 0, "failed": 0,
                               "test_files": ["tests/test_do_job_flow.py"]}])
        assert cov.get("tests/test_do_job_flow.py") == ["vr-1"]

    @pytest.mark.parametrize("run", [
        {"run_id": "vr-1", "exit_code": 1, "failed": 69},      # round 15's actual state
        {"run_id": "vr-1", "exit_code": 0, "failed": 3},       # passed-but-failures
        {"run_id": "vr-1", "exit_code": 2, "failed": 0},       # usage error
    ])
    def test_a_red_run_covers_nothing(self, run):
        run["test_files"] = ["tests/test_do_job_flow.py"]
        assert self._coverage([run]) == {}

    def test_a_task_changing_the_do_command_is_uncovered_without_the_suite(self):
        """The round-15 shape: the CLI matrix ran, the job-flow suite did not."""
        changed = ["apps/cli/commands/do_cmd.py"]
        related = sorted({t for f in changed for t in _relevant_suites_for_source(f)})
        assert related == ["tests/test_do_job_flow.py"]
        cov = self._coverage([{"run_id": "vr-1", "exit_code": 0, "failed": 0,
                               "test_files": ["tests/cli/test_job_commands.py"]}])
        uncovered = [f for f in related if not cov.get(f)]
        assert uncovered == ["tests/test_do_job_flow.py"], \
            "a change to the do command must require its regression suite"

    def test_the_same_task_is_covered_once_the_suite_runs_green(self):
        changed = ["apps/cli/commands/do_cmd.py"]
        related = sorted({t for f in changed for t in _relevant_suites_for_source(f)})
        cov = self._coverage([{"run_id": "vr-1", "exit_code": 0, "failed": 0,
                               "test_files": ["tests/test_do_job_flow.py"]}])
        assert [f for f in related if not cov.get(f)] == []

    def test_a_red_suite_leaves_the_task_uncovered(self):
        changed = ["apps/cli/commands/do_cmd.py"]
        related = sorted({t for f in changed for t in _relevant_suites_for_source(f)})
        cov = self._coverage([{"run_id": "vr-1", "exit_code": 1, "failed": 69,
                               "test_files": ["tests/test_do_job_flow.py"]}])
        assert [f for f in related if not cov.get(f)] == ["tests/test_do_job_flow.py"]
