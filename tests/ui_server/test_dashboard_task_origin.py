"""F028 R6 S1 — DECISION F028 D6 (1): each dashboard task item's LAST key,
`origin`, carries `inputs["plan"]["origin"]` when that value is a non-empty
string, and `""` otherwise — an injected task's item names
`task_injection.ORIGIN_HUMAN_INJECTED`, a planned task's item (whose plan
carries no `origin` key at all) and a task with no plan inputs whatsoever
both name `""`.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from packages.core.models import RunState
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    map_task_plan_to_tasks,
    plan_content_hash,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables
from packages.orchestration.task_injection import ORIGIN_HUMAN_INJECTED
from packages.orchestration.ui_server import _build_dashboard


def _task(tid: str) -> dict:
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": [f"{tid} works"], "depends_on": [],
        "est_tokens_band": "S", "files_hint": [f"src/{tid.lower()}.py"],
    }


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
    return data


def _save_job(root: Path, tasks: list) -> JobPlan:
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = "approved"
    body["_normalization"] = []
    body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="t", task_plan=body, tasks=mapped, state=RunState.PLANNED)
    save_job_plan(job, root)
    return job


def _items_by_planned(job: JobPlan, dashboard: dict) -> dict:
    by_id = {item["id"]: item for item in dashboard["tasks"]}
    return {
        (t.inputs.get("plan") or {}).get("planned_id"): by_id[str(t.task_id)]
        for t in job.tasks if by_id.get(str(t.task_id)) is not None
    }


def _dashboard(job: JobPlan) -> dict:
    with patch("packages.orchestration.ui_server._load_events", return_value=[]):
        return _build_dashboard(job)


def test_a_planned_tasks_item_names_the_empty_string(root):
    job = _save_job(root, [_task("T1")])

    dashboard = _dashboard(job)
    items = _items_by_planned(job, dashboard)
    assert items["T1"]["origin"] == ""
    assert list(items["T1"].keys())[-1] == "origin"


def test_an_injected_tasks_item_names_human_injected(root):
    job = _save_job(root, [_task("T1")])
    entry = job.tasks[0]
    entry.inputs["plan"]["origin"] = ORIGIN_HUMAN_INJECTED

    dashboard = _dashboard(job)
    items = _items_by_planned(job, dashboard)
    assert items["T1"]["origin"] == ORIGIN_HUMAN_INJECTED


def test_a_task_with_no_plan_inputs_at_all_names_the_empty_string(root):
    job = _save_job(root, [_task("T1")])
    bare = TaskEntry(title="a task with no plan inputs", inputs={})
    job.tasks.append(bare)

    dashboard = _dashboard(job)
    by_id = {item["id"]: item for item in dashboard["tasks"]}
    assert by_id[str(bare.task_id)]["origin"] == ""
