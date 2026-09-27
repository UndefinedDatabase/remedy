"""F029 R4 S3 — DECISION F029 D4 (4): each dashboard task item gains `attempt`
and `attempts`, placed directly before `origin`, which stays the LAST key
(unchanged from DECISION F028 D6 (1)'s `test_dashboard_task_origin.py`, which
this file is built as).

`fold_subtree_rerun` (F029 T002) is pure, so a rerun's attempt fan is produced
directly rather than through a real git worktree and preparation — the same
economy `test_subtree_rerun_prepare.py::TestFoldSubtreeRerun` already banks on.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from packages.core.models import RunState
from packages.orchestration import subtree_rerun as SR
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    map_task_plan_to_tasks,
    plan_content_hash,
)
from packages.orchestration.pingpong_job import (
    TASK_APPLIED,
    JobPlan,
    save_job_plan,
)
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables
from packages.orchestration.ui_server import _build_dashboard


def _task(tid: str, depends_on: list | None = None) -> dict:
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": [f"{tid} works"], "depends_on": depends_on or [],
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


def _dashboard(job: JobPlan) -> dict:
    with patch("packages.orchestration.ui_server._load_events", return_value=[]):
        return _build_dashboard(job)


def _items_by_planned(job: JobPlan, dashboard: dict) -> dict:
    by_id = {item["id"]: item for item in dashboard["tasks"]}
    return {
        (t.inputs.get("plan") or {}).get("planned_id"): by_id[str(t.task_id)]
        for t in job.tasks if by_id.get(str(t.task_id)) is not None
    }


def _reset_for(task_id: str) -> dict:
    return {
        "root_task_id": task_id,
        "subtree": [task_id],
        "base_commit": "base123",
        "reset_commit": "reset456",
        "paths": ["a.py"],
        "exact": True,
        "proof": {"paths_checked": 1, "paths_equal": True, "tree_equals_base": True},
        "pre_task_tree_equal": None,
    }


def test_after_a_preparation_t002_carries_its_old_attempt_and_t001_carries_none(root):
    job = _save_job(root, [_task("T1"), _task("T2", depends_on=["T1"])])
    t1, t2 = job.tasks
    t2.status = TASK_APPLIED
    t2.run_id = "run-old-1"
    t2.worktree_commit = "c" * 40

    SR.fold_subtree_rerun(
        job, _reset_for(t2.task_id), rerun_id="rerun-1", model_override="", actor="tester",
        now=datetime(2026, 9, 27, tzinfo=timezone.utc), moved_streams={},
    )

    dashboard = _dashboard(job)
    items = _items_by_planned(job, dashboard)

    assert items["T2"]["attempt"] == 2
    assert len(items["T2"]["attempts"]) == 1
    assert items["T2"]["attempts"][0]["run_id"] == "run-old-1"
    assert items["T1"]["attempt"] == 1
    assert items["T1"]["attempts"] == []
    assert list(items["T2"].keys())[-1] == "origin"
    assert list(items["T1"].keys())[-1] == "origin"


def test_a_never_run_tasks_item_names_attempt_one_and_no_attempts(root):
    job = _save_job(root, [_task("T1")])

    dashboard = _dashboard(job)
    items = _items_by_planned(job, dashboard)

    assert items["T1"]["attempt"] == 1
    assert items["T1"]["attempts"] == []
