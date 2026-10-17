"""Operator amendment amend1014-do-golden-path-now D1 — the lane classifier of `remedy do`, as a table.

DECISION amend1016p D1: the transport never decides (an order file and a typed order get the same
lane), the constraints never count as parts, and a named file alone is not enough."""
from __future__ import annotations

import pytest

from packages.orchestration.do_context import DoContext
from packages.orchestration.do_lane import (
    DO_LANE_BOUNDED,
    DO_LANE_FULL,
    DO_TINY_REPO_MAX_FILES,
    is_tiny_repo,
    select_do_lane,
    settle_do_lane,
)

#: The order of 2026-10-16 that became two jobs and six tasks, as the Orb sent it.
APP_INCIDENT_ORDER = (
    "Ändere ausschließlich README.md im Projekt remedy-lab. Ergänze am Ende einen Abschnitt "
    "„Testbetrieb“ mit zwei kurzen deutschen Sätzen, die erklären, dass dieses Repository zum Testen "
    "von Codeänderungen dient. Verändere keine anderen Dateien. Führe npm test aus. Übernimm keine "
    "Änderungen automatisch.")
LAB = ["README.md", "package.json", "src/calc.js", "src/format.js", "test/baseline.test.js", ".gitignore"]

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
    ("the same words as prose in a one-file repo", "Add a paragraph and fix the title", ["README.md"],
     {}, DO_LANE_FULL),
    ("several projects", INCIDENT_ORDER, ["README.md"], {"projects": 2}, DO_LANE_FULL),
    ("the app's incident order", APP_INCIDENT_ORDER, LAB, {}, DO_LANE_BOUNDED),
    ("one file with test and approval constraints",
     "Add a usage section to README.md. Change only README.md. Run npm test. Do not apply it "
     "automatically.", LAB, {}, DO_LANE_BOUNDED),
    ("one file with complex requirements",
     "In src/calc.js add input validation, add a subtract function, migrate the exports to ESM and "
     "write tests for all of it.", LAB, {}, DO_LANE_FULL),
    ("several independent deliverables in one file's name",
     "Add a section to README.md. Write a changelog entry. Add a CI workflow.", LAB, {}, DO_LANE_FULL),
    ("a test-only order", "Run npm test and report the result.", LAB, {}, DO_LANE_FULL),
    ("a reporting deliverable", "Write a report of the npm test results to TEST_REPORT.md.", LAB, {},
     DO_LANE_BOUNDED),
    ("an ambiguous target", "Fix the bug.", LAB, {}, DO_LANE_FULL),
    ("the app's order with --force-mission", APP_INCIDENT_ORDER, LAB, {"force_mission": True},
     DO_LANE_FULL),
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
    assert select_do_lane(long_one, tracked_files=["a", "b", "README.md"]).bounded
    assert not select_do_lane("Edit alpha.md beta.md", tracked_files=["alpha.md"]).bounded


def test_a_repository_is_tiny_up_to_the_threshold_and_an_empty_one_is_not():
    assert is_tiny_repo(["README.md"])
    assert is_tiny_repo(["f"] * DO_TINY_REPO_MAX_FILES)
    assert not is_tiny_repo(["f"] * (DO_TINY_REPO_MAX_FILES + 1))
    assert not is_tiny_repo([])


def test_an_order_file_and_a_typed_order_walk_the_same_lane(tmp_path):
    """The order the HTTP API wrote to an order file and the same words typed on the command line."""
    import subprocess

    repo = tmp_path / "lab"
    repo.mkdir()
    for name in LAB:
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text("x\n")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.email=t@example.com", "-c", "user.name=t",
                    "commit", "-qm", "lab"], check=True)
    typed = DoContext(order=APP_INCIDENT_ORDER, repo_root=str(repo))
    filed = DoContext(order=APP_INCIDENT_ORDER, repo_root=str(repo),
                      order_source_path=str(tmp_path / "order.md"))
    assert settle_do_lane(typed) == settle_do_lane(filed)
    assert settle_do_lane(filed).bounded and settle_do_lane(filed).deliverable == "README.md"
