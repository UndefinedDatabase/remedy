"""F268 T002 — tasks bounded by deliverables, and the one validator (DECISION F268 D6, R-0808).

Pure unit tests over `packages/orchestration/task_deliverables.py`: no repository,
no data root, no provider.
"""
from __future__ import annotations

import pytest

from packages.orchestration.pingpong_job import TaskEntry
from packages.orchestration.schemas.models import _MAX_TASK_PLAN_TASKS
from packages.orchestration.task_deliverables import (
    INSPECTION_VERBS,
    DeliverablePlanError,
    deliverable_check_task,
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
    tasks = _flat(deterministic_job_plans(order)) + [deliverable_check_task("README.md", order)]

    for task in tasks:
        items = [line for line in task.acceptance.splitlines() if line.strip()]
        assert 1 <= len(items) <= ceiling


def test_the_validator_accepts_a_clean_deterministic_plan():
    order = "Write " + " ".join(TEN_FILES)
    tasks = _flat(deterministic_job_plans(order)) + [deliverable_check_task(TEN_FILES[0], order)]

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
