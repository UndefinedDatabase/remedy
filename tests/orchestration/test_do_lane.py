"""Operator amendment amend1014-do-golden-path-now D1 — the lane classifier of `remedy do`, as a table."""
from __future__ import annotations

import pytest

from packages.orchestration.do_lane import (
    DO_LANE_BOUNDED,
    DO_LANE_FULL,
    DO_TINY_REPO_MAX_FILES,
    is_tiny_repo,
    select_do_lane,
)

INCIDENT_ORDER = (
    "Add one concise project-description paragraph below the existing heading in README.md. "
    "Change no other files.")

LANE_TABLE = [
    # (id, order, tracked files, options, expected lane)
    ("the incident order", INCIDENT_ORDER, ["README.md"], {}, DO_LANE_BOUNDED),
    ("one named file in a big repo", "Write a CONTRIBUTING.md", [f"f{n}.py" for n in range(80)],
     {}, DO_LANE_BOUNDED),
    ("a plain order in a one-file repo", "Add a short project description", ["README.md"],
     {}, DO_LANE_BOUNDED),
    ("a plain order in a big repo", "Add a short project description",
     ["README.md", "a.py", "b.py"], {}, DO_LANE_FULL),
    ("two named files", "Write CONTRIBUTING.md and CHANGELOG.md", ["README.md"], {}, DO_LANE_FULL),
    ("a list order in a one-file repo", "Do these:\n- add a license\n- add CI", ["README.md"],
     {}, DO_LANE_FULL),
    ("three sentences in a one-file repo", "Add a paragraph. Fix the title. Add a badge.",
     ["README.md"], {}, DO_LANE_FULL),
    ("a semicolon list in a one-file repo", "Add a paragraph; fix the title", ["README.md"],
     {}, DO_LANE_FULL),
    ("several projects", INCIDENT_ORDER, ["README.md"], {"projects": 2}, DO_LANE_FULL),
    ("an order file", INCIDENT_ORDER, ["README.md"], {"from_order_file": True}, DO_LANE_FULL),
    ("--force-mission", INCIDENT_ORDER, ["README.md"], {"force_mission": True}, DO_LANE_FULL),
    ("--force-job on a vague order", "Improve things", ["a.py", "b.py"], {"force_job": True},
     DO_LANE_BOUNDED),
    ("an empty repository and a vague order", "Improve things", [], {}, DO_LANE_FULL),
]


@pytest.mark.parametrize(("order", "tracked", "options", "expected"),
                         [row[1:] for row in LANE_TABLE], ids=[row[0] for row in LANE_TABLE])
def test_the_lane_of_an_order_is_decided_by_its_facts(order, tracked, options, expected):
    decision = select_do_lane(order, tracked_files=tracked, **options)
    assert decision.lane == expected, decision.reason
    assert decision.reason


def test_the_bounded_lane_names_the_one_file_it_serves():
    assert select_do_lane(INCIDENT_ORDER, tracked_files=["README.md"]).deliverable == "README.md"
    plain = select_do_lane("Add a short project description", tracked_files=["docs/intro.md"])
    assert plain.deliverable == "docs/intro.md"


def test_a_word_count_alone_never_picks_the_lane():
    """A long order naming one file is bounded, a short one naming two is not."""
    long_one = "Please " + "carefully " * 60 + "update README.md"
    assert select_do_lane(long_one, tracked_files=["a", "b", "c"]).bounded
    assert not select_do_lane("Edit alpha.md beta.md", tracked_files=["alpha.md"]).bounded


def test_a_repository_is_tiny_up_to_the_threshold_and_an_empty_one_is_not():
    assert is_tiny_repo(["README.md"])
    assert is_tiny_repo(["f"] * DO_TINY_REPO_MAX_FILES)
    assert not is_tiny_repo(["f"] * (DO_TINY_REPO_MAX_FILES + 1))
    assert not is_tiny_repo([])
