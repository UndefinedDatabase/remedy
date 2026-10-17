"""F268 T002 — tasks bounded by deliverables, and the one validator (DECISION F268 D6, R-0808).

Pure unit tests over `packages/orchestration/task_deliverables.py`: no repository,
no data root, no provider.
"""
from __future__ import annotations

import pytest

from packages.orchestration.pingpong_job import TaskEntry
from packages.orchestration.schemas.models import _MAX_TASK_PLAN_TASKS, TaskPlan
from packages.orchestration.task_deliverables import (
    EXTENSIONLESS_DELIVERABLE_NAMES,
    INSPECTION_VERBS,
    DeliverablePlanError,
    deterministic_job_plans,
    extract_order_deliverables,
    record_llm_task_deliverables,
    task_deliverable,
    validate_deliverable_plan,
)

TEN_FILES = [f"docs/part_{n:02d}.md" for n in range(10)]


def _flat(plans: list[list[TaskEntry]]) -> list[TaskEntry]:
    return [task for plan in plans for task in plan]


def test_a_one_sentence_order_without_a_path_is_one_task():
    order = "Improve the error messages the importer prints"

    [tasks] = deterministic_job_plans(order)

    assert len(tasks) == 1
    assert task_deliverable(tasks[0]) == order


def test_an_order_naming_ten_files_is_ten_tasks_in_order_each_delivering_its_file():
    order = "Write " + ", ".join(TEN_FILES) + "."

    [tasks] = deterministic_job_plans(order)

    assert [t.inputs["deliverable"] for t in tasks] == TEN_FILES


def test_a_file_named_twice_is_one_deliverable():
    order = "Update src/app.py and tests/test_app.py, then src/app.py once more"

    assert extract_order_deliverables(order) == ["src/app.py", "tests/test_app.py"]


@pytest.mark.parametrize("name", EXTENSIONLESS_DELIVERABLE_NAMES)
def test_an_extensionless_file_name_is_a_deliverable(name):
    # R-0966: the dot-extension pattern alone read this order as one vague deliverable.
    order = f"Fix the {name}."

    assert extract_order_deliverables(order) == [name]


def test_extensionless_names_keep_their_directory_and_order_beside_paths():
    order = "Add docker/Dockerfile, then update src/app.py and the Makefile"

    assert extract_order_deliverables(order) == ["docker/Dockerfile", "src/app.py", "Makefile"]


@pytest.mark.parametrize("order", [
    "Fetch https://example.com/download?file=report.pdf and write notes.md",
    "Follow www.example.com/page then write notes.md",
    "See https://example.com/docs and write notes.md",
])
def test_no_token_inside_a_url_is_a_deliverable(order):
    # R-0966: the query string's file and the scheme-less host each read as a path.
    assert extract_order_deliverables(order) == ["notes.md"]


def test_more_files_than_one_job_holds_become_two_jobs_and_none_is_dropped():
    files = [f"pkg/mod_{n:02d}.py" for n in range(26)]
    order = "Create " + " ".join(files)

    plans = deterministic_job_plans(order)

    assert [len(p) for p in plans] == [_MAX_TASK_PLAN_TASKS, 26 - _MAX_TASK_PLAN_TASKS]
    assert [task_deliverable(t) for t in _flat(plans)] == files


def test_every_deterministic_task_holds_at_most_the_configured_acceptance_count():
    from packages.orchestration.job_plan import granularity_config

    ceiling = granularity_config().max_acceptance
    order = "Write " + " ".join(TEN_FILES)
    tasks = _flat(deterministic_job_plans(order))

    for task in tasks:
        items = [line for line in task.acceptance.splitlines() if line.strip()]
        assert 1 <= len(items) <= ceiling


def test_the_validator_accepts_a_clean_deterministic_plan():
    order = "Write " + " ".join(TEN_FILES)
    tasks = _flat(deterministic_job_plans(order))

    validate_deliverable_plan(tasks)


def test_the_validator_rejects_a_task_with_no_deliverable():
    tasks = [TaskEntry(title="Write the changelog")]

    with pytest.raises(DeliverablePlanError, match="names no deliverable"):
        validate_deliverable_plan(tasks)


@pytest.mark.parametrize("verb", INSPECTION_VERBS)
def test_the_validator_rejects_a_task_titled_with_an_inspection_verb(verb):
    task = TaskEntry(title=f"{verb.capitalize()} the repository layout",
                     inputs={"deliverable": "notes.md"})

    with pytest.raises(DeliverablePlanError, match="is inspection"):
        validate_deliverable_plan([task])


def test_the_validator_rejects_an_empty_plan():
    with pytest.raises(DeliverablePlanError, match="holds no task"):
        validate_deliverable_plan([])


def test_an_llm_task_delivers_its_first_files_hint_else_its_first_acceptance_line():
    hinted = TaskEntry(title="Add the parser: parse input",
                       acceptance="parser handles empty input",
                       inputs={"plan": {"files_hint": ["src/parser.py", "src/lexer.py"]}})
    unhinted = TaskEntry(title="Document the flags: help text",
                         acceptance="\n  \nevery flag has help text\nexamples added")
    bare = TaskEntry(title="Do something")

    record_llm_task_deliverables([hinted, unhinted, bare])

    assert [task_deliverable(t) for t in (hinted, unhinted, bare)] == [
        "src/parser.py", "every flag has help text", ""]


# ── Operator amendment amend1014-do-golden-path-now D2: one concrete deliverable is one task ──

def _task(ident, title, goal, *, files=(), depends=()):
    return {"id": ident, "title": title, "goal": goal, "acceptance": [f"{title} is done"],
            "depends_on": list(depends), "est_tokens_band": "S", "files_hint": list(files)}


def _plan(*tasks) -> TaskPlan:
    return TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": list(tasks)})


def _captured_plan(files=("README.md",)) -> TaskPlan:
    """The incident's plan: Verify README.md, then Draft paragraph, then Insert paragraph."""
    return _plan(
        _task("T1", "Verify README.md", "Confirm README.md exists and locate its heading.",
              files=files),
        _task("T2", "Draft paragraph", "Draft one concise project-description paragraph.",
              files=files, depends=["T1"]),
        _task("T3", "Insert paragraph", "Insert the paragraph below the heading of README.md.",
              files=files, depends=["T2"]))


@pytest.mark.parametrize("files", [("README.md",), ()], ids=["with files_hint", "named in text only"])
def test_the_captured_incident_plan_becomes_one_mutating_task(files):
    from packages.orchestration.do_sequence import _deliverable_task_plan
    from packages.orchestration.task_deliverables import task_deliverable

    plan = _captured_plan(files)
    if not files:
        plan = _plan(
            _task("T1", "Verify README.md", "Confirm README.md exists and locate its heading."),
            _task("T2", "Draft paragraph", "Draft the paragraph for README.md.", depends=["T1"]),
            _task("T3", "Insert paragraph", "Insert the paragraph into README.md.",
                  depends=["T2"]))

    normalized, tasks = _deliverable_task_plan(plan)

    [task] = tasks
    assert task.title.startswith("Insert paragraph")
    assert task_deliverable(tasks[0]) == "README.md"
    [planned] = normalized.tasks
    for step in ("Verify README.md", "Draft paragraph", "Insert paragraph"):
        assert step in planned.goal
    assert planned.depends_on == []


def test_a_plan_of_only_inspection_is_still_rejected():
    from packages.orchestration.do_sequence import OrderJobPlanError, _deliverable_task_plan

    plan = _plan(_task("T1", "Verify README.md", "Look.", files=["README.md"]),
                 _task("T2", "Locate the heading", "Look again.", files=["README.md"],
                       depends=["T1"]))
    with pytest.raises(OrderJobPlanError):
        _deliverable_task_plan(plan)


@pytest.mark.parametrize("title", ["Verify README.md", "Confirm the heading", "Locate the heading",
                                   "Find the section", "Identify the file"])
def test_the_observed_inspection_verbs_are_not_tasks(title):
    from packages.orchestration.pingpong_job import TaskEntry
    from packages.orchestration.task_deliverables import (
        DeliverablePlanError,
        validate_deliverable_plan,
    )

    with pytest.raises(DeliverablePlanError):
        validate_deliverable_plan([TaskEntry(title=title, inputs={"deliverable": "README.md"})])


def test_tasks_over_different_files_are_never_merged():
    from packages.orchestration.task_deliverables import coalesce_deliverable_tasks

    plan = _plan(_task("T1", "Add intro", "x", files=["README.md"]),
                 _task("T2", "Add changelog", "y", files=["CHANGELOG.md"]))
    assert coalesce_deliverable_tasks(plan) is None


def test_a_task_between_two_of_a_files_tasks_keeps_the_plan_as_planned():
    """Merging T1 and T3 would make the merged task wait for T2, which waits for T1: a cycle."""
    from packages.orchestration.task_deliverables import coalesce_deliverable_tasks

    plan = _plan(_task("T1", "Add intro", "x", files=["README.md"]),
                 _task("T2", "Add changelog", "y", files=["CHANGELOG.md"], depends=["T1"]),
                 _task("T3", "Add badges", "z", files=["README.md"], depends=["T2"]))
    assert coalesce_deliverable_tasks(plan) is None


def test_two_files_keep_two_tasks_and_each_file_one():
    from packages.orchestration.do_sequence import _deliverable_task_plan

    plan = _plan(
        _task("T1", "Draft intro", "x", files=["README.md"]),
        _task("T2", "Insert intro", "x2", files=["README.md"], depends=["T1"]),
        _task("T3", "Draft log", "y", files=["CHANGELOG.md"]),
        _task("T4", "Insert log", "y2", files=["CHANGELOG.md"], depends=["T3"]))
    _normalized, tasks = _deliverable_task_plan(plan)
    assert [t.title.split(":")[0] for t in tasks] == ["Insert intro", "Insert log"]


def test_a_requested_test_is_named_as_a_deliverable_of_the_same_task():
    # Lab calc order of 2026-10-17 17:13: "deliverable: src/calc.js" plus a side sentence made the
    # builder fix only calc.js; the reviewer failed it and the repair round ran out of budget.
    from packages.orchestration.task_deliverables import deliverable_task

    order = "add(a, b) in src/calc.js rechnet falsch. Repariere sie und ergänze einen Regressionstest in test/calc.test.js."
    task = deliverable_task("src/calc.js", order, with_tests=True)
    assert task.title == "Deliver src/calc.js and its test test/calc.test.js"
    assert "TWO things" in task.body and "Do not finish until both are written" in task.body
    assert task.acceptance.endswith("the test the order asks for exists and passes (test/calc.test.js)")
    assert deliverable_task("README.md", "Fix README.md.").title == "Deliver README.md"
