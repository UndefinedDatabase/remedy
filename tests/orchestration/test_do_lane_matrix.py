"""The routing matrix of the 2026-10-17 scale audit, as a versioned table (MATRIX_VERSION).

Each row is an order over a repository's tracked files and the lane its facts must give. The
expectations are the audit's semantic judgements: `bounded` is one job and one task with no
planner call, `full` is investigation and planning (an attended plan), `hold` is a question asked
before anything is planned. The table also pins what the lane must NOT depend on: punctuation,
layout, language and the transport.
"""
from __future__ import annotations

import pytest

from packages.orchestration.do_lane import (
    DO_LANE_BOUNDED,
    DO_LANE_FULL,
    DO_LANE_HOLD,
    select_do_lane,
)

MATRIX_VERSION = 1

CODE = ["README.md", "package.json", "src/calc.js", "src/add.py", "tests/test_add.py", "src/app.ts",
        "src/main.ts", "src/database.py", "src/auth.ts", "CHANGELOG.md"]
TWO_READMES = [*CODE, "docs/README.md"]
ONLY_NESTED_READMES = ["src/add.py", "docs/README.md", "web/README.md"]

B, F, H = DO_LANE_BOUNDED, DO_LANE_FULL, DO_LANE_HOLD

MATRIX = [
    # (id, order, tracked, lane, deliverable)
    ("readme minimal", "Add a usage section to README.md.", CODE, B, "README.md"),
    ("readme with a test constraint", "Add a usage section to README.md. Run npm test.", CODE, B,
     "README.md"),
    ("readme with a semicolon", "Edit README.md; run npm test", CODE, B, "README.md"),
    ("readme numbered", "1. Add a usage section to README.md.", CODE, B, "README.md"),
    ("readme in a markdown list", "Do this:\n- fix the typo in README.md", CODE, B, "README.md"),
    ("readme heading", "# Task\nFix the typo in README.md", CODE, B, "README.md"),
    ("one-file auth rewrite", "Rewrite the complete authentication system in src/app.ts.", CODE, F, ""),
    ("one-file security change", "Rewrite the security layer of src/database.py to encrypt all "
     "stored credentials.", CODE, F, ""),
    ("one-file protocol migration", "Migrate the wire protocol of all services via src/main.ts.", CODE,
     F, ""),
    ("one-file auth change by path", "Change src/auth.ts so that it works better.", CODE, F, ""),
    ("one-file data migration", "Drop and recreate all tables in src/database.py and migrate "
     "existing user data.", CODE, F, ""),
    ("bug fix with a regression test", "Fix a bug in src/add.py and add a regression test.", CODE, B,
     "src/add.py"),
    ("bug fix with an explicit test file",
     "Fix a bug in src/add.py and add a regression test in tests/test_add.py.", CODE, B, "src/add.py"),
    ("a file only in a test run", "Fix the typo in README.md. Run pytest tests/test_add.py.", CODE, B,
     "README.md"),
    ("a file only in a header constraint",
     "Fix the typo in README.md\n\nConstraints the plan must honour:\n- run tests/test_add.py\n"
     "- change no other files", CODE, B, "README.md"),
    ("bug fix, tests only run", "Fix a bug in src/add.py. Run the tests.", CODE, B, "src/add.py"),
    ("feature in two files", "Add a feature to src/add.py and src/calc.js.", CODE, B, "src/add.py"),
    ("typo without a suffix", "Fix the typo in the readme", CODE, B, "README.md"),
    ("typo in German", "Korrigiere den Tippfehler in README.md", CODE, B, "README.md"),
    ("heading in German", "Ändere in README.md die Überschrift auf 'Hallo'.", CODE, B, "README.md"),
    ("no specific target", "Improve error handling everywhere.", CODE, F, ""),
    ("tests only", "Write tests for the calculator.", CODE, F, ""),
    ("one file and a review", "Fix the typo in README.md and review the diff.", CODE, B, "README.md"),
    ("report file asked for", "Write a report to REPORT.md.", CODE, B, "REPORT.md"),
    ("a semicolon inside a quote", 'Change the heading in README.md to "Hello; world".', CODE, B,
     "README.md"),
    ("cross-app change without a file", "Change the API contract and update both the web app and "
     "the mobile app.", CODE, F, ""),
    ("a file the repository does not have", "Edit DOES_NOT_EXIST.md", CODE, H, ""),
    ("the same file when the order creates it", "Create DOES_NOT_EXIST.md with a short intro.", CODE, B,
     "DOES_NOT_EXIST.md"),
    ("root README beside docs README", "Change only README.md: fix the typo.", TWO_READMES, B,
     "README.md"),
    ("nested README named by path", "Fix the typo in docs/README.md.", TWO_READMES, B, "docs/README.md"),
    ("a bare README that two nested files share", "Fix the typo in README.md.", ONLY_NESTED_READMES, H,
     ""),
    ("a documentation target mentions auth", "Fix the typo in the authentication section of "
     "README.md.", CODE, B, "README.md"),
]


@pytest.mark.parametrize(("order", "tracked", "lane", "deliverable"), [row[1:] for row in MATRIX],
                         ids=[row[0] for row in MATRIX])
def test_the_audit_matrix_routes_as_the_audit_expects(order, tracked, lane, deliverable):
    decision = select_do_lane(order, tracked_files=tracked)
    assert (decision.lane, decision.deliverable) == (lane, deliverable), decision.reason
    assert decision.reason


def test_a_hold_is_a_question_naming_the_candidates():
    decision = select_do_lane("Fix the typo in README.md.", tracked_files=ONLY_NESTED_READMES)
    assert decision.hold and "docs/README.md" in decision.reason and "web/README.md" in decision.reason


def test_a_requested_test_is_part_of_the_one_job_and_a_test_run_is_not():
    assert select_do_lane("Fix src/add.py and add a regression test.", tracked_files=CODE).with_tests
    assert not select_do_lane("Fix src/add.py. Run the tests.", tracked_files=CODE).with_tests
    assert not select_do_lane("Add a section to README.md describing how to run tests.",
                              tracked_files=CODE).with_tests


#: Groups of orders that say the same thing; each group must walk one lane.
PARAPHRASES = [
    ["Fix the typo in README.md",
     "Fix the typo in README.md.",
     "  Fix   the typo in\nREADME.md  ",
     "- Fix the typo in README.md",
     "1) Fix the typo in README.md",
     "## Task\n\nFix the typo in README.md",
     "Fix the typo in README.md; change no other files",
     "Fix the typo in README.md. Change no other files. Run npm test.",
     "Korrigiere den Tippfehler in README.md",
     "Korrigiere den Tippfehler in README.md. Ändere keine anderen Dateien. Führe npm test aus."],
    ["Rewrite the authentication in src/app.ts",
     "Rewrite the authentication in src/app.ts.",
     "- Rewrite the authentication in src/app.ts",
     "Schreibe die Authentifizierung in src/app.ts neu; ändere nur src/app.ts"],
    ["Add a paragraph and fix the title",
     "Add a paragraph; fix the title",
     "- Add a paragraph\n- fix the title"],
]


@pytest.mark.parametrize("group", PARAPHRASES, ids=["typo", "auth", "two actions"])
def test_equivalent_orders_walk_the_same_lane(group):
    tracked = CODE if "README" not in group[0] or "title" not in group[0] else ["README.md"]
    lanes = {select_do_lane(order, tracked_files=tracked).lane for order in group}
    assert len(lanes) == 1, lanes


def test_a_force_job_override_says_what_routing_alone_chose():
    order = "Rewrite the complete authentication system in src/app.ts."
    decision = select_do_lane(order, tracked_files=CODE, force_job=True)
    assert decision.bounded and "--force-job" in decision.reason and "full lane" in decision.reason
    assert decision.deliverable == ""


@pytest.mark.parametrize("order, tracked", [
    ("Fix the typo in README.md", ONLY_NESTED_READMES),       # which of two nested files?
    ("Fix the typo in docs/missing.md", CODE),                 # a named file nothing tracks
])
def test_force_job_never_answers_an_unresolved_file_question(order, tracked):
    decision = select_do_lane(order, tracked_files=tracked, force_job=True)
    assert decision.hold and decision.lane == H and not decision.bounded
    assert decision.deliverable == ""
    assert decision.reason == select_do_lane(order, tracked_files=tracked).reason


def test_several_projects_and_force_mission_stay_in_the_full_lane():
    assert select_do_lane("Fix README.md", tracked_files=CODE, projects=2).lane == F
    assert select_do_lane("Fix README.md", tracked_files=CODE, force_mission=True).lane == F
