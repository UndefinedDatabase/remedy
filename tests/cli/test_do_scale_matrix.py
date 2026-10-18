"""The versioned scale matrix (tests/orchestration/scale_matrix.py) as pytest cases.

Each case builds a disposable git repository of its size class, walks the order through the real
`remedy do` with a counting fake planner and the fake builder and reviewer, and checks the
expectations the matrix states: the lane, the number of jobs and tasks, the planner calls, the
requested outputs kept and the unsafe shapes absent.
"""
from __future__ import annotations

import pytest

from tests.orchestration.scale_matrix import CASES, MATRIX_VERSION, check_expectations, run_matrix


def test_the_matrix_is_versioned_and_covers_every_class_of_the_audit():
    assert MATRIX_VERSION == 5
    classes = {case["klass"] for case in CASES}
    assert classes >= {"tiny", "small", "medium", "large", "polyglot", "monorepo", "ambiguous",
                       "wrong-path", "deliverable", "failure", "incident", "verification", "lab",
                       "multi-file", "plan-only", "file-roles", "independent", "verify-only"}
    assert len({case["id"] for case in CASES}) == len(CASES)


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_the_case_meets_its_expectations(case, tmp_path):
    [record] = run_matrix(tmp_path, [case["id"]])

    assert check_expectations(case, record) == [], record


def test_a_tiny_order_costs_the_same_in_a_repository_of_ten_thousand_files(tmp_path):
    tiny, large = (run_matrix(tmp_path, [case_id])[0] for case_id in ("tiny-readme", "large-readme-edit"))

    for key in ("lane", "planner_calls", "jobs", "tasks", "builder_calls", "reviewer_calls"):
        assert tiny[key] == large[key], (key, tiny, large)
