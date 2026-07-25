"""F9 (round 12) — INPUT coverage and CALL coverage are separate claims.

"We compared every call" and "we know every material input this run was given" are different
things, and a check can honestly have one without the other. An explicit `unavailable` identity is
better than an empty string — it keeps the record truthful — but it is still not a complete
deterministic input record, and it must never quietly add up to `same_inputs=true`.

So the diff reports both dimensions, `same_inputs` is True only when BOTH are complete, and the
CLI names which one is short.
"""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    GIT_UNAVAILABLE,
    UNAVAILABLE,
    diff_manifests,
)


def _cov(reference, candidate):
    return diff_manifests(reference, candidate)


class TestTheTwoDimensionsAreReportedSeparately:
    def test_a_clean_pair_is_complete_on_both(self):
        d = _cov(T._mk(), T._mk())
        assert d["coverage"]["call_status"] == COVERAGE_COMPLETE
        assert d["coverage"]["input_status"] == COVERAGE_COMPLETE
        assert d["same_inputs"] is True

    @pytest.mark.parametrize("field", [
        "remedy_git_sha", "target_base_commit", "target_head", "target_tree",
        "job_initial_tree", "job_file_sha256",
    ])
    def test_an_unavailable_material_identity_makes_input_coverage_incomplete(self, field):
        snap = dataclasses.replace(T._snap(), **{field: UNAVAILABLE})
        m = T._mk(snap=snap)
        d = _cov(m, m)
        assert d["coverage"]["input_status"] == COVERAGE_INCOMPLETE
        assert any(field in p for p in d["coverage"]["input_problems"]), \
            d["coverage"]["input_problems"]

    def test_an_unavailable_workspace_identity_makes_input_coverage_incomplete(self):
        snap = dataclasses.replace(T._snap(), episode_start_workspace_identity={
            "status": GIT_UNAVAILABLE, "head": UNAVAILABLE, "digest": "",
            "problems": ["the target is not a git repository"], "dirty": None})
        m = T._mk(snap=snap)
        d = _cov(m, m)
        assert d["coverage"]["input_status"] == COVERAGE_INCOMPLETE
        assert any("episode_start_workspace_identity" in p
                   for p in d["coverage"]["input_problems"])

    def test_incomplete_input_coverage_never_says_same_inputs(self):
        """THE point: an honest gap must never add up to determinism."""
        snap = dataclasses.replace(T._snap(), target_tree=UNAVAILABLE)
        m = T._mk(snap=snap)
        d = _cov(m, m)
        assert d["coverage"]["call_status"] == COVERAGE_COMPLETE   # calls DID compare
        assert d["coverage"]["input_status"] == COVERAGE_INCOMPLETE
        assert d["same_inputs"] is None, "an incomplete input record claimed same inputs"
        assert d["verification_complete"] is False

    def test_call_complete_plus_input_incomplete_is_never_true(self):
        snap = dataclasses.replace(T._snap(), job_initial_tree=UNAVAILABLE)
        m = T._mk(snap=snap)
        d = _cov(m, m)
        assert (d["coverage"]["call_status"], d["coverage"]["input_status"]) == \
            (COVERAGE_COMPLETE, COVERAGE_INCOMPLETE)
        assert d["same_inputs"] is not True

    def test_an_incomplete_worktree_identity_makes_input_coverage_incomplete(self):
        snap = dataclasses.replace(T._snap(), target_worktree={
            "status": "incomplete", "head": "c" * 40, "digest": "dd" * 32,
            "problems": ["a component failed"], "dirty": None})
        m = T._mk(snap=snap)
        d = _cov(m, m)
        assert d["coverage"]["input_status"] == COVERAGE_INCOMPLETE
        assert d["same_inputs"] is not True

    def test_real_drift_is_still_false_not_none(self):
        """An incomplete record must not launder real drift into "unknown"."""
        a = T._mk()
        b = T._mk(snap=dataclasses.replace(T._snap(), target_head="f" * 40))
        d = _cov(a, b)
        assert d["same_inputs"] is False
        assert d["blocking"]


# --------------------------------------------------------------------------- the payload


class TestTheCoveragePayloadNamesTheShortDimension:
    """The operator has to be able to see WHICH claim is short. (The CLI text/JSON rendering and
    the exit codes are proven end-to-end in `tests/cli/test_job_rerun_manifest.py`.)"""

    def test_the_payload_exposes_both_dimensions(self):
        snap = dataclasses.replace(T._snap(), target_tree=UNAVAILABLE)
        m = T._mk(snap=snap)
        cov = _cov(m, m)["coverage"]
        assert cov["call_status"] == COVERAGE_COMPLETE
        assert cov["input_status"] == COVERAGE_INCOMPLETE
        assert cov["input_problems"]

    def test_the_material_problem_names_the_field(self):
        snap = dataclasses.replace(T._snap(), job_initial_tree=UNAVAILABLE)
        m = T._mk(snap=snap)
        assert any("job_initial_tree" in p
                   for p in _cov(m, m)["coverage"]["input_problems"])
