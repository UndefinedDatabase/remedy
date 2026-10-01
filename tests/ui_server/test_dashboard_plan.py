"""F292 T001 — the plan read (DECISION F292 D1 (1)): `plan_editing.plan_view`, served by
the dashboard's `plan` section and by `remedy job plan-show --json`, so the plan view and
the command line read one answer — the plan's version, its approval, whether it is open for
editing and why not, and each planned task with its dependencies, its acceptance and the
task entry that runs it.
"""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from packages.core.models import RunState
from packages.orchestration.job_plan import map_task_plan_to_tasks
from packages.orchestration.mission_compiler import PLAN_VERSION_KEY
from packages.orchestration.pingpong_job import JobPlan, load_job_plan, save_job_plan
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables
from packages.orchestration.ui_server import _build_dashboard, _build_plan_section

SECTION_KEYS = {"available", "version", "approval", "editable", "not_editable_because",
                "tasks", "error"}
TASK_KEYS = {"id", "title", "goal", "depends_on", "est_tokens_band", "files_hint",
             "acceptance", "job_task_id", "status", "spec_version"}


def _task(tid: str, deps: list[str], acceptance: list[str] | None = None) -> dict:
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": acceptance or [f"{tid} works"], "depends_on": deps,
        "est_tokens_band": "S", "files_hint": [f"src/{tid.lower()}.py"],
    }


_TASKS = [
    _task("T1", []),
    _task("T2", ["T1"], ["parser reads a file", "parser reports errors"]),
    _task("T3", ["T2", "T1"]),
]


@pytest.fixture(autouse=True)
def _data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))


def _save_job(*, approval: str = "pending", state: RunState = RunState.PLANNED) -> JobPlan:
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
    body = plan.model_dump()
    body["_approval"] = approval
    body["_normalization"] = []
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F292 plan read", task_plan=body, tasks=mapped, state=state)
    save_job_plan(job)
    return job


def _entry_for(job: JobPlan, planned_id: str):
    for t in job.tasks:
        if (t.inputs.get("plan") or {}).get("planned_id") == planned_id:
            return t
    raise AssertionError(f"no task for planned id {planned_id!r}")


def _cli_json(argv: list[str], capsys) -> tuple[int, dict]:
    from apps.cli.grouped import main

    try:
        code = main([*argv, "--json"])
    except SystemExit as exc:
        code = exc.code
    return code or 0, json.loads(capsys.readouterr().out)


class TestTheSectionIsTheCommandLinesRead:
    """Acceptance: the plan view's version, approval and tasks equal `remedy job plan-show
    --json` for the same job."""

    def test_after_an_edit_the_section_equals_plan_show_json(self, capsys):
        job = _save_job()
        job_id = str(job.job_id)
        code, edited = _cli_json(["job", "plan-edit-task", job_id, "T2", "--title", "Parse",
                                  "--plan-version", "1"], capsys)
        assert code == 0, edited
        code, shown = _cli_json(["job", "plan-show", job_id], capsys)
        assert code == 0, shown
        section = _build_plan_section(load_job_plan(job_id))
        assert set(section) == SECTION_KEYS
        assert (section["available"], section["error"]) == (True, "")
        for key in ("version", "approval", "editable", "not_editable_because", "tasks"):
            assert section[key] == shown[key], key
        assert (section["version"], section["tasks"][1]["title"]) == (2, "Parse")

    def test_the_dashboard_serves_the_section_under_plan(self):
        job = _save_job()
        with patch("packages.orchestration.ui_server._load_events", return_value=[]):
            dashboard = _build_dashboard(job)
        assert dashboard["plan"] == _build_plan_section(job)
        assert dashboard["plan"]["available"] is True


class TestTheEditWindow:

    def test_a_pending_plan_of_a_planned_job_is_open_for_editing(self):
        section = _build_plan_section(_save_job())
        assert (section["version"], section["approval"]) == (1, "pending")
        assert (section["editable"], section["not_editable_because"]) == (True, None)

    def test_an_approved_plan_is_closed_with_the_reason(self):
        section = _build_plan_section(_save_job(approval="approved"))
        assert section["editable"] is False
        assert section["not_editable_because"] == (
            "the plan is approved; a plan is edited only while its approval is open")

    def test_a_started_job_is_closed_with_the_reason(self):
        section = _build_plan_section(_save_job(state=RunState.RUNNING))
        assert section["editable"] is False
        assert section["not_editable_because"] == (
            "the job is running; a plan is edited only before its job starts")


class TestEachPlannedTask:

    def test_each_task_carries_its_fields_dependencies_acceptance_and_entry(self):
        job = _save_job()
        tasks = _build_plan_section(job)["tasks"]
        assert [t["id"] for t in tasks] == ["T1", "T2", "T3"]
        assert all(set(t) == TASK_KEYS for t in tasks)
        t3 = tasks[2]
        assert t3["depends_on"] == ["T2", "T1"]
        assert tasks[1]["acceptance"] == ["parser reads a file", "parser reports errors"]
        assert (t3["title"], t3["goal"], t3["est_tokens_band"], t3["files_hint"]) == (
            "Build T3", "goal of T3", "S", ["src/t3.py"])
        entry = _entry_for(job, "T3")
        assert (t3["job_task_id"], t3["status"], t3["spec_version"]) == (
            entry.task_id, "pending", 1)

    def test_a_planned_task_no_entry_maps_reads_no_id_no_status_and_version_1(self):
        job = _save_job()
        job.tasks = [t for t in job.tasks
                     if (t.inputs.get("plan") or {}).get("planned_id") != "T2"]
        t2 = _build_plan_section(job)["tasks"][1]
        assert (t2["id"], t2["job_task_id"], t2["status"], t2["spec_version"]) == (
            "T2", "", "", 1)

    def test_when_two_entries_name_one_planned_task_the_first_is_served(self):
        job = _save_job()
        first = _entry_for(job, "T2")
        second = dataclasses.replace(first, task_id="later-entry", spec_version=4)
        job.tasks = [*job.tasks, second]
        t2 = _build_plan_section(job)["tasks"][1]
        assert (t2["job_task_id"], t2["spec_version"]) == (first.task_id, 1)


class TestAPlanThatCannotBeServed:

    def test_a_job_with_no_stored_plan_reads_the_empty_section(self):
        job = JobPlan(job_title="no plan", state=RunState.PLANNED)
        assert _build_plan_section(job) == {
            "available": False, "version": 0, "approval": None, "editable": False,
            "not_editable_because": None, "tasks": [], "error": ""}

    def test_a_malformed_version_is_reported_as_error_and_never_raised(self):
        job = _save_job()
        job.task_plan[PLAN_VERSION_KEY] = "not a number"
        section = _build_plan_section(job)
        assert (section["available"], section["tasks"]) == (False, [])
        assert "not a number" in section["error"]

    def test_two_empty_sections_share_no_list(self):
        job = JobPlan(job_title="no plan", state=RunState.PLANNED)
        first = _build_plan_section(job)
        first["tasks"].append("x")
        assert _build_plan_section(job)["tasks"] == []
