"""DECISION amend1016p D1 and D2 — an order's deliverables apart from its constraints, and the
planner's constraint-only milestones and checking-only tasks left out (the README incident of
2026-10-16, preserved under universe's local evidence)."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.job_plan import plan_job_llm
from packages.orchestration.mission_compiler import compile_mission_plan
from packages.orchestration.order_scope import split_order_scope

#: The incident order exactly as the Orb sent it (its body, after the order file's header).
INCIDENT_ORDER = (
    "Ändere ausschließlich README.md im Projekt remedy-lab. Ergänze am Ende einen Abschnitt "
    "„Testbetrieb“ mit zwei kurzen deutschen Sätzen, die erklären, dass dieses Repository zum Testen "
    "von Codeänderungen dient. Verändere keine anderen Dateien. Führe npm test aus. Übernimm keine "
    "Änderungen automatisch.")

SCOPE_TABLE = [
    # (id, order, deliverables, constraints, simple)
    ("the incident order", INCIDENT_ORDER, 1, 4, True),
    ("one file with test and approval constraints",
     "Add a usage section to README.md. Change only README.md. Run npm test and make sure the "
     "tests pass. Do not apply the change automatically.", 1, 3, True),
    ("one file, genuinely complex",
     "In app.py add a REST endpoint for users, add authentication middleware, migrate the database "
     "schema and write tests for all of it.", 1, 0, False),
    ("a fence beside real work",
     "Fix the parser in parse.py, add tests and change no other files. Also update the docs.",
     2, 0, False),
    ("several independent deliverables",
     "Add a section to README.md. Write a changelog entry. Add a CI workflow.", 3, 0, False),
    ("a test-only order", "Run npm test and report the result.", 1, 0, True),
    ("a reporting deliverable",
     "Write a report of the npm test results to TEST_REPORT.md. Change no other files.", 1, 1, True),
    ("a list", "Do these:\n- add a license\n- add CI", 2, 0, True),
    ("a list of three", "Do these:\n- add a license\n- add CI\n- add a badge", 3, 0, False),
]


@pytest.mark.parametrize(("order", "deliverables", "constraints", "simple"),
                         [row[1:] for row in SCOPE_TABLE], ids=[row[0] for row in SCOPE_TABLE])
def test_an_order_is_sorted_into_deliverables_and_constraints(order, deliverables, constraints, simple):
    scope = split_order_scope(order)
    assert (len(scope.deliverables), len(scope.constraints), scope.simple) == (
        deliverables, constraints, simple), scope


def test_the_incident_order_has_one_deliverable_and_its_four_constraints():
    scope = split_order_scope(INCIDENT_ORDER)
    assert scope.deliverables == (
        "Ergänze am Ende einen Abschnitt „Testbetrieb“ mit zwei kurzen deutschen Sätzen, die "
        "erklären, dass dieses Repository zum Testen von Codeänderungen dient.",)
    assert "Führe npm test aus." in scope.constraints


def test_header_constraints_count_as_constraints_and_never_as_parts():
    order = ("Add a usage section to README.md\n\nConstraints the plan must honour:\n"
             "- run npm test\n- change no other files")
    scope = split_order_scope(order)
    assert scope.simple and scope.deliverables == ("Add a usage section to README.md",)
    assert scope.constraints[-2:] == ("run npm test", "change no other files")


# --- D2: the full lane leaves constraint-only milestones and checking-only tasks out -----------

def _incident_mission_answer() -> str:
    """What the planner answered for the incident order: the README milestone and a test one."""
    return json.dumps({"schema_v": "mission_plan_draft_v1", "risks": [], "assumptions": [],
                       "milestones": [
        {"id": "M001", "goal": "README.md ends with a 'Testbetrieb' section containing two short "
         "German sentences, and no other file is modified.", "depends_on": [], "rationale": "",
         "jobs_draft": [{"title": "Append the section", "goal": "Append it to README.md",
                         "est_band": "S"}]},
        {"id": "M002", "goal": "npm test has been executed in the remedy-lab project and its "
         "output is captured, with no automatic apply.", "depends_on": ["M001"], "rationale": "",
         "jobs_draft": [{"title": "Run npm test", "goal": "Run npm test and capture its output",
                         "est_band": "S"}]}]})


def test_the_incident_plan_keeps_only_the_readme_milestone():
    result = compile_mission_plan(INCIDENT_ORDER, lambda prompt, attempt: _incident_mission_answer())
    assert result.source == "llm"
    assert [m.id for m in result.plan.milestones] == ["M001"]
    assert result.plan.milestones[0].depends_on == []


def test_a_test_only_order_keeps_its_test_milestone():
    answer = json.dumps({"schema_v": "mission_plan_draft_v1", "milestones": [
        {"id": "M001", "goal": "npm test has been executed and its result is reported.",
         "depends_on": [], "jobs_draft": [{"title": "Run the tests", "goal": "Run npm test",
                                           "est_band": "S"}]}]})
    result = compile_mission_plan("Run npm test and report the result.", lambda p, a: answer)
    assert [m.id for m in result.plan.milestones] == ["M001"]


def _task(ident: str, title: str, goal: str, deps: list[str]) -> dict:
    return {"id": ident, "title": title, "goal": goal, "acceptance": [f"{title} done"],
            "depends_on": deps, "est_tokens_band": "S", "files_hint": []}


def test_checking_artifact_tasks_are_left_out_unless_the_job_asks_for_them():
    answer = json.dumps({"schema_v": "task_plan_v1", "risks": [], "tasks": [
        _task("T001", "Create pre-run file manifest", "Record hashes of all top-level files", []),
        _task("T002", "Append the Testbetrieb section", "Append the section to README.md", ["T001"]),
        _task("T003", "Generate modification report", "Confirm only README.md was modified", ["T002"]),
    ]})
    plain = {"goal": "README.md ends with a Testbetrieb section", "constraints": []}
    result = plan_job_llm(plain, lambda p, a: answer)
    assert [t.title for t in result.plan.tasks] == ["Append the Testbetrieb section"]
    assert result.plan.tasks[0].depends_on == []

    audit = {"goal": "Write a modification report of the repository with checksums", "constraints": []}
    kept = plan_job_llm(audit, lambda p, a: answer)
    assert len(kept.plan.tasks) >= 2 and any("report" in t.title.lower() for t in kept.plan.tasks)


# --- 2026-10-17 audit P1-3/P1-4: a file name is not a request; layout is not a part ---------------

from packages.orchestration.order_scope import (  # noqa: E402
    is_binding_plan_item,
    is_test_path,
    requests_test_files,
    work_milestones,
)

TYPO_ORDER = "Fix the typo in README.md. Change no other files."


@pytest.mark.parametrize("item", [
    "Create checksums.json with the hashes of all tracked files",
    "Write change_report.md describing the changes",
    "Save a comparison copy as README.before.md and a modification report",
    "Erstelle pruefsummen.json mit den Prüfsummen aller Dateien",
])
def test_an_unrequested_checking_artifact_binds_even_when_it_names_a_file(item):
    assert is_binding_plan_item(item, order=TYPO_ORDER)


def test_a_requested_report_file_is_work_and_the_fix_itself_is_never_binding():
    assert not is_binding_plan_item("Write TEST_REPORT.md", order="Write a report of the test "
                                    "results to TEST_REPORT.md.")
    assert not is_binding_plan_item("Fix the typo in README.md", order=TYPO_ORDER)


class _Draft:
    def __init__(self, ident: str, goal: str, outlines: list[dict] | None = None):
        self._d = {"id": ident, "goal": goal, "depends_on": [], "rationale": "",
                   "jobs_draft": outlines or []}

    def model_dump(self) -> dict:
        return {**self._d, "jobs_draft": list(self._d["jobs_draft"])}


def test_a_plan_of_only_checking_artifacts_is_not_kept_as_the_original():
    drafts = [_Draft("M001", "Create checksums.json for all files"),
              _Draft("M002", "Write change_report.md")]
    assert work_milestones(drafts, TYPO_ORDER) == []


def test_an_outline_that_only_makes_a_checking_artifact_is_dropped_without_a_fallback():
    outlines = [{"title": "Write change_report.md", "goal": "Report on the change", "est_band": "S"}]
    [kept] = work_milestones([_Draft("M001", "README.md has no typo", outlines)], TYPO_ORDER)
    assert kept["jobs_draft"] == []


@pytest.mark.parametrize("order", [
    "Fix a bug in src/add.py and add a regression test.",
    "Add tests for the parser in parse.py.",
    "Ergänze einen Regressionstest für add.py.",
])
def test_writing_a_test_is_a_requested_deliverable(order):
    assert requests_test_files(order)


@pytest.mark.parametrize("order", [
    "Fix a bug in src/add.py. Run the tests.",
    "Add a section to README.md describing how to run tests.",
    "Make sure the tests pass.",
])
def test_running_tests_is_a_constraint_not_a_deliverable(order):
    assert not requests_test_files(order)


def test_test_paths_are_recognised_across_languages():
    for path in ("tests/test_add.py", "src/add.test.ts", "pkg/add_test.go", "spec/add_spec.rb",
                 "test/baseline.test.js", "src/__tests__/a.ts"):
        assert is_test_path(path), path
    assert not is_test_path("src/add.py") and not is_test_path("docs/latest.md")


def test_layout_never_changes_the_parts_of_an_order():
    prose = split_order_scope("Fix the typo in README.md and run npm test")
    semicolon = split_order_scope("Fix the typo in README.md; run npm test")
    bullet = split_order_scope("- Fix the typo in README.md\n- run npm test")
    assert [len(s.deliverables) for s in (prose, semicolon, bullet)] == [1, 1, 1]
    quoted = split_order_scope('Change the heading to "Hello; world". Fix README.md.')
    assert len(quoted.deliverables) == 2
