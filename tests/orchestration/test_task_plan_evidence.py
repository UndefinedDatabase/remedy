"""Tests for the task plan evidence module."""
from __future__ import annotations

from packages.orchestration.task_plan_evidence import build_task_plan_evidence

SAMPLE_TASKS = [
    {"id": "T001", "summary": "Add role config", "dependencies": [], "expected_files": ["role_config.py"], "expected_tests": ["test defaults"]},
    {"id": "T002", "summary": "Add CLI flags", "dependencies": ["T001"], "expected_files": ["do_cmd.py", "role_config.py"], "expected_tests": ["test flag parsing"]},
    {"id": "T003", "summary": "Add evidence", "dependencies": ["T001"], "expected_files": ["evidence.py"], "expected_tests": ["test schema"]},
]


def _build(**overrides):
    defaults = {"goal": "Implement role system", "step_range": "5001-5030", "tasks": SAMPLE_TASKS}
    defaults.update(overrides)
    return build_task_plan_evidence(**defaults)


def test_schema_version():
    result = _build()
    assert result["schema_version"] == 1


def test_package_goal_recorded():
    result = _build(goal="Build new widget")
    assert result["package_goal"] == "Build new widget"


def test_step_range_recorded():
    result = _build(step_range="6001-6050")
    assert result["step_range"] == "6001-6050"


def test_task_list_with_ids():
    result = _build()
    ids = [t["id"] for t in result["tasks"]]
    assert ids == ["T001", "T002", "T003"]


def test_task_dependencies_recorded():
    result = _build()
    graph = result["task_dependency_graph"]
    assert graph["T001"] == []
    assert graph["T002"] == ["T001"]
    assert graph["T003"] == ["T001"]


def test_expected_changed_areas_deduped():
    result = _build()
    areas = result["expected_changed_areas"]
    assert areas == ["role_config.py", "do_cmd.py", "evidence.py"]
    assert len(areas) == len(set(areas))


def test_risk_tags_recorded():
    result = _build(risks=["concurrency", "schema migration"])
    assert result["risk_tags"] == ["concurrency", "schema migration"]
    assert result["open_risks"] == ["concurrency", "schema migration"]


def test_default_completion_criteria():
    result = _build()
    assert "all tasks pass review" in result["completion_criteria"]
    assert "all tests pass" in result["completion_criteria"]
    assert "no blocked gates" in result["completion_criteria"]


def test_custom_completion_criteria():
    custom = ["manual QA pass", "perf benchmark green"]
    result = _build(completion_criteria=custom)
    assert result["completion_criteria"] == custom
    assert "all tasks pass review" not in result["completion_criteria"]


def test_task_count_matches():
    result = _build()
    assert result["task_count"] == len(result["tasks"])
    assert result["task_count"] == 3
