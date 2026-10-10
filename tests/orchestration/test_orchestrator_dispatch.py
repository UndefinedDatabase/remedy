"""The orchestrator loop's dispatch path, `orchestrator_dispatch.dispatch_milestone_job`.

R-1233: a dispatched job whose plan gate is open is approved, audited, before it runs. F301 T003,
DECISION F301 D1 (9): when the mission's upkeep job is due, it runs in place of the dispatch,
serving no milestone, and the model's dispatch is made at the next move.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from packages.core.models import RunState
from packages.orchestration import mission_contract
from packages.orchestration import orchestrator_loop as loop
from packages.orchestration.data_paths import job_dir
from packages.orchestration.mission_state import create_mission, link_job_to_mission, load_mission
from packages.orchestration.mission_upkeep import UPKEEP_METADATA_KEY, read_upkeep_ledger
from packages.orchestration.orchestrator_loop import JobExecution, blocked_completion, execute_move
from packages.orchestration.orchestrator_move_schema import MOVE_DISPATCH_JOB
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan, save_job_plan

PROJECT = "b" * 32
MOVE = SimpleNamespace(kind=MOVE_DISPATCH_JOB, payload={"milestone_id": "M1", "step": "build M1"})


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    """One data root for jobs, missions, projects and run events alike."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    return tmp_path


class _Recorder:
    """Records what the dispatch path asked of the executor and of the milestone helpers."""

    def __init__(self) -> None:
        self.executed: list = []
        self.created: list = []
        self.milestone_calls: list[str] = []
        self.approvals_asked: list[str] = []

    def execute(self, job):
        self.executed.append(job)
        return JobExecution(terminal_status="all_green", job_status="completed")

    def dispatch(self, project_id, mission_id, step, *, root=None, now=None):
        job = JobPlan(job_title=step, state=RunState.PLANNED)
        save_job_plan(job)
        self.created.append(job)
        return job


def _spy(monkeypatch, module, name: str, calls: list[str]) -> None:
    """Replace ``module.name`` with a wrapper that records the call and then makes it."""
    original = getattr(module, name)

    def spy(*args, **kwargs):
        calls.append(name)
        return original(*args, **kwargs)

    monkeypatch.setattr(module, name, spy)


@pytest.fixture()
def recorder(monkeypatch) -> _Recorder:
    """The milestone helpers the dispatch path reads at call time, each recording its calls."""
    seen = _Recorder()
    approve = loop._auto_approve_if_gated
    monkeypatch.setattr(loop, "_auto_approve_if_gated",
                        lambda job: seen.approvals_asked.append(str(job.job_id)) or approve(job))
    _spy(monkeypatch, loop, "attach_milestone_dod", seen.milestone_calls)
    for name in ("merge_contract_slice_into_dod", "grant_contract_job_repository", "record_job_milestone",
                 "record_contract_results"):
        _spy(monkeypatch, mission_contract, name, seen.milestone_calls)
    return seen


def _five_done(root, *, finding: bool = True) -> str:
    mission = create_mission(PROJECT, "Keep the importer working", root=root)
    for index in range(5):
        job = JobPlan(job_title=f"job {index}", state=RunState.COMPLETED)
        save_job_plan(job)
        if index == 0 and finding:
            (job_dir(str(job.job_id)) / "final_job_review.json").write_text(json.dumps({"findings": [{
                "id": "F-TASK-001", "severity": "repairable", "category": "task_verdict",
                "message": "T001 did not pass review", "task_id": "T001"}]}), encoding="utf-8")
        link_job_to_mission(PROJECT, mission.id, str(job.job_id), "initial" if index == 0 else "follow_up",
                            root=root)
    return mission.id


class TestTheAuditedApprovalOfADispatchedJob:
    """R-1233: no test saw the dispatch path skip the approval of a job whose plan gate is open."""

    def test_a_job_waiting_at_its_plan_gate_is_approved_audited_before_it_runs(self, data_root, recorder):
        from packages.orchestration.timeline import load_run_events

        mission = create_mission(PROJECT, "Ship the tool", root=data_root)
        gated = JobPlan(job_title="t", task_plan={"_approval": "pending"})
        gated.tasks.append(TaskEntry(title="t1"))
        save_job_plan(gated)
        events_when_run: list[list[str]] = []

        def execute(job):
            events_when_run.append([e.get("event") for e in load_run_events(data_root, str(job.job_id))])
            return JobExecution(terminal_status="all_green", job_status="completed")

        outcome = execute_move(PROJECT, mission.id, MOVE, root=data_root,
                               dispatch=lambda *a, **k: gated, execute=execute)

        assert outcome.status == "dispatched"
        assert "(plan auto-approved, audited)" in outcome.detail
        assert events_when_run and "plan_approved" in events_when_run[0]


class TestTheUpkeepJobInPlaceOfADispatch:
    def test_when_due_the_upkeep_job_runs_and_serves_no_milestone(self, data_root, recorder):
        mission_id = _five_done(data_root)

        outcome = execute_move(PROJECT, mission_id, MOVE, root=data_root,
                               dispatch=recorder.dispatch, execute=recorder.execute)

        assert outcome.status == "upkeep_dispatched" and not outcome.terminal
        [job] = recorder.executed
        assert str(job.job_id) == outcome.job_id and UPKEEP_METADATA_KEY in job.metadata
        assert recorder.created == [] and recorder.milestone_calls == []
        assert recorder.approvals_asked == [outcome.job_id]
        assert mission_contract.JOB_MILESTONE_KEY not in load_job_plan(outcome.job_id).metadata
        assert load_mission(PROJECT, mission_id, data_root).job_ids()[-1] == outcome.job_id
        assert "in place of M1's step after 5 completed jobs" in outcome.detail
        assert "gate=" not in outcome.detail and blocked_completion(MOVE, outcome) == ("M1", "")
        assert [line["kind"] for line in read_upkeep_ledger(PROJECT, data_root)][-1] == "upkeep_planned"

    def test_the_next_dispatch_is_the_models_own(self, data_root, recorder):
        mission_id = _five_done(data_root)
        execute_move(PROJECT, mission_id, MOVE, root=data_root, dispatch=recorder.dispatch,
                     execute=recorder.execute)

        outcome = execute_move(PROJECT, mission_id, MOVE, root=data_root, dispatch=recorder.dispatch,
                               execute=recorder.execute)

        assert outcome.status == "dispatched" and len(recorder.created) == 1
        assert outcome.job_id == str(recorder.created[0].job_id)

    def test_when_due_with_nothing_to_carry_the_dispatch_is_made_and_that_is_recorded(self, data_root, recorder):
        mission_id = _five_done(data_root, finding=False)

        outcome = execute_move(PROJECT, mission_id, MOVE, root=data_root, dispatch=recorder.dispatch,
                               execute=recorder.execute)

        assert outcome.status == "dispatched" and len(recorder.created) == 1
        assert [line["kind"] for line in read_upkeep_ledger(PROJECT, data_root)][-1] == "upkeep_not_needed"

    def test_before_it_is_due_nothing_changes(self, data_root, recorder):
        mission = create_mission(PROJECT, "Keep the importer working", root=data_root)

        outcome = execute_move(PROJECT, mission.id, MOVE, root=data_root, dispatch=recorder.dispatch,
                               execute=recorder.execute)

        assert outcome.status == "dispatched" and "record_contract_results" in recorder.milestone_calls
        assert read_upkeep_ledger(PROJECT, data_root) == []


class TestADispatchOverSeveralProjects:
    """DECISION F205 D5: the loop's job runs in the project and repository of the chain's last job."""

    def test_the_dispatched_job_runs_in_the_last_jobs_repository(self, data_root, recorder):
        other = "c" * 32
        mission = create_mission(PROJECT, "Two repositories", project_ids=(PROJECT, other),
                                 root=data_root)
        for index, (project, repo) in enumerate(((PROJECT, "/repos/toolbox"), (other, "/repos/brain"))):
            job = JobPlan(job_title=f"job {index}", state=RunState.COMPLETED, project_id=project,
                          repo_path=repo)
            save_job_plan(job)
            link_job_to_mission(PROJECT, mission.id, str(job.job_id),
                                "initial" if index == 0 else "follow_up", root=data_root)

        outcome = execute_move(PROJECT, mission.id, MOVE, root=data_root, execute=recorder.execute)

        assert outcome.status == "dispatched"
        [job] = recorder.executed
        assert (job.project_id, job.repo_path) == (other, "/repos/brain")
        assert load_mission(PROJECT, mission.id, data_root).job_links[-1].project_id == other
