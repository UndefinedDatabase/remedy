"""F026 R3 T003 first half — the dashboard's `task_specs` section (DECISION F026 D3
clause 1): for every task entry mapped from the job's stored plan, its planned id, its
spec version, the runtime edit state (or `""` with the refusal's detail), the plan
task's current fields, and its archived versions.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from packages.core.models import RunState
from packages.orchestration import pause_control as pc
from packages.orchestration import safe_points as sp
from packages.orchestration import task_edit_runtime as ter
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    map_task_plan_to_tasks,
    plan_content_hash,
)
from packages.orchestration.pingpong_job import (
    TASK_BLOCKED,
    JobPlan,
    save_job_plan,
)
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables
from packages.orchestration.ui_server import _build_dashboard, _build_task_spec_section


def _task(tid: str, deps: list[str] | None = None, acceptance: list[str] | None = None) -> dict:
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": acceptance or [f"{tid} works"], "depends_on": deps or [],
        "est_tokens_band": "S", "files_hint": [f"src/{tid.lower()}.py"],
    }


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
    return data


def _save_job(root: Path, tasks: list[dict], *, state: RunState = RunState.PLANNED,
             approval: str = "approved") -> JobPlan:
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = approval
    body["_normalization"] = []
    if approval == "approved":
        body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="t", task_plan=body, tasks=mapped, state=state)
    save_job_plan(job, root)
    return job


def _by_planned(job: JobPlan, planned_id: str):
    for i, t in enumerate(job.tasks):
        if (t.inputs.get("plan") or {}).get("planned_id") == planned_id:
            return i, t
    raise AssertionError(f"no task for planned id {planned_id!r}")


def _section(job: JobPlan) -> dict:
    with patch("packages.orchestration.ui_server._load_events", return_value=[]):
        return _build_dashboard(job)["task_specs"]


class TestNeverEdited:
    def test_a_never_edited_task_reads_version_1_no_versions_waiting(self, root):
        job = _save_job(root, [_task("T1")])
        _, entry = _by_planned(job, "T1")

        section = _build_task_spec_section(job)

        assert section["error"] == ""
        spec = section["tasks"][str(entry.task_id)]
        assert spec["planned_id"] == "T1"
        assert spec["spec_version"] == 1
        assert spec["edit_state"] == "waiting"
        assert spec["not_editable_because"] == ""
        assert spec["versions"] == []
        assert spec["current"]["title"] == "Build T1"
        assert spec["current"]["goal"] == "goal of T1"
        assert spec["current"]["acceptance"] == ["T1 works"]
        assert spec["current"]["est_tokens_band"] == "S"
        assert spec["current"]["files_hint"] == ["src/t1.py"]


class TestAfterOneEdit:
    def test_version_2_and_one_archived_version_with_the_old_fields(self, root):
        job = _save_job(root, [_task("T1")])
        _, entry = _by_planned(job, "T1")

        ter.edit_task_at_runtime(
            job.job_id, entry.task_id, {"title": "Build T1, renamed"},
            expected_spec_version=1, actor="tf:test", root=root)

        from packages.orchestration.pingpong_job import load_job_plan
        reloaded = load_job_plan(job.job_id, root)

        section = _build_task_spec_section(reloaded)
        spec = section["tasks"][str(entry.task_id)]
        assert spec["spec_version"] == 2
        assert spec["current"]["title"] == "Build T1, renamed"
        assert len(spec["versions"]) == 1
        old = spec["versions"][0]
        assert old["title"] == "Build T1"
        assert old["spec_version"] == 1
        assert old["state"] == "waiting"
        assert old["archived_at"] != ""


class TestBlockedTask:
    def test_a_blocked_task_reads_failed(self, root):
        job = _save_job(root, [_task("T1")])
        _, entry = _by_planned(job, "T1")
        entry.status = TASK_BLOCKED
        save_job_plan(job, root)

        from packages.orchestration.pingpong_job import load_job_plan
        reloaded = load_job_plan(job.job_id, root)

        section = _build_task_spec_section(reloaded)
        assert section["tasks"][str(entry.task_id)]["edit_state"] == "failed"


class TestRunningJob:
    def test_a_running_job_reads_empty_with_a_detail_naming_running(self, root):
        job = _save_job(root, [_task("T1")], state=RunState.RUNNING)
        _, entry = _by_planned(job, "T1")

        section = _build_task_spec_section(job)
        spec = section["tasks"][str(entry.task_id)]
        assert spec["edit_state"] == ""
        assert "running" in spec["not_editable_because"]


class TestNoPlan:
    def test_a_job_without_a_plan_reads_no_tasks(self, root):
        job = JobPlan(job_title="t", task_plan=None, tasks=[], state=RunState.PLANNED)
        save_job_plan(job, root)

        section = _build_task_spec_section(job)
        assert section == {"tasks": {}, "error": ""}


class TestCorruptPauseFile:
    def test_a_corrupt_task_pause_file_reads_no_tasks_and_a_nonempty_error(self, root):
        job = _save_job(root, [_task("T1")])
        _, entry = _by_planned(job, "T1")

        pc.request_task_pause(job.job_id, entry.task_id)
        name = pc._task_pause_filename(entry.task_id)
        path = sp.control_root() / "jobs" / job.job_id / "paused_tasks" / name
        path.write_text("not json")

        section = _build_task_spec_section(job)
        assert section["tasks"] == {}
        assert section["error"] != ""


class TestDashboardCarriesTheKey:
    def test_build_dashboard_carries_the_key(self, root):
        job = _save_job(root, [_task("T1")])

        section = _section(job)
        assert "tasks" in section
        assert "error" in section
