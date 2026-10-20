"""The lab stop of 2026-10-20 rebuilt: review report `rr-20261020T143546Z`, job `48ce0648d73747eb` (F310).

The figures are those findings R-1370 and R-1371 record: a job of a mission whose contract has one
blocking criterion, `execution_config` `pi` for both roles, budgets of 100,000 tokens, 5 calls and
9 minutes, stopped `budget_exhausted:max_wall_clock_minutes` with a version-2 record of 78,696 tokens
over 3 measured calls and nine minutes of work.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from packages.orchestration.budget_decision import answer_budget_decision
from packages.orchestration.budget_stop import doubled_limit_answers, raise_remainder_for_final_job
from packages.orchestration.decision_queue import budget_decision_id, list_decisions
from packages.orchestration.execution_config import ExecutionConfig
from packages.orchestration.mission_contract import (
    CONTRACT_REMAINDER_MARKER,
    ContractCriterion,
    MissionContract,
    write_mission_contract,
)
from packages.orchestration.mission_state import create_mission, link_job_to_mission
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan, save_job_plan
from tests.orchestration.test_budget_profiles import isolated_configuration  # noqa: F401 (autouse fixture)

PROJECT = "p-lab-stop"
STARTED = datetime(2026, 10, 20, 14, 0, 0, tzinfo=timezone.utc)
STOPPED = STARTED + timedelta(minutes=9)


@pytest.fixture(autouse=True)
def _data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))


def _lab_stop() -> JobPlan:
    """The saved job of a mission with one blocking criterion, stopped on its nine-minute wall clock."""
    job = JobPlan(job_title="lab-stop", tasks=[TaskEntry(title="d")],
                  execution_config=ExecutionConfig(builder="pi", reviewer="pi"))
    job.metadata = {"target_repo": "/work/target"}    # so no derived "no target repository" stop reason joins the list
    job.budgets = {"max_total_tokens": 100_000, "max_provider_calls": 5, "max_wall_clock_minutes": 9}
    job.stop_source, job.stop_request_id = "budget", "lab1"
    job.stop_reason, job.stopped_at = "budget_exhausted:max_wall_clock_minutes", STOPPED.isoformat()
    job.first_running_at = STARTED.isoformat()
    job.budget_actuals = {
        "schema_version": "2.0.0", "started_at": STARTED.isoformat(),
        "provider_call_count": 3, "actual_call_count": 3, "unmeasured_call_count": 0,
        "total_tokens": 78_696, "actual_sources": ["pingpong_live"],
        "measured_cost_usd": None, "priced_call_count": 0, "unpriced_call_count": 0}
    save_job_plan(job)
    mission = create_mission(PROJECT, "Ship the tool")
    write_mission_contract(PROJECT, mission.id, MissionContract(criteria=(
        ContractCriterion(id="C001", text="the suite passes", origin="planner", blocking=True, status="open"),)))
    link_job_to_mission(PROJECT, mission.id, str(job.job_id), "initial")
    return job


def _stop_event(job: JobPlan) -> dict:
    return {"event": "job_stopped", "timestamp": STOPPED.isoformat(),
            "metadata": {"source": "budget", "request_id": job.stop_request_id, "reason": job.stop_reason,
                         "exhausted_limit": "max_wall_clock_minutes"}}


def _open_ids(job: JobPlan) -> list[str]:
    return [d.id for d in list_decisions(job, [_stop_event(job)]) if d.status == "open"]


def test_the_lab_stop_asks_one_question_and_names_its_blocker():
    job = _lab_stop()
    [decision] = list_decisions(job, [_stop_event(job)])
    assert decision.id == budget_decision_id("lab1")
    assert decision.payload["blockers"] == ["C001: the suite passes"]


def test_the_lab_stop_doubles_only_the_wall_clock_and_an_extend_raises_it():
    job = _lab_stop()
    assert doubled_limit_answers(job, now=STOPPED) == ["max_wall_clock_minutes=60"]
    result = answer_budget_decision(job, budget_decision_id("lab1"), "extend", [], now=STOPPED)
    assert result["outcome"] == "extended"
    assert result["raised"] == {"max_wall_clock_minutes": 60}


def test_the_lab_stop_abandoned_raises_one_remainder_decision_once():
    job = _lab_stop()
    result = answer_budget_decision(job, budget_decision_id("lab1"), "abandon", [], now=STOPPED)
    assert result["outcome"] == "abandoned"
    save_job_plan(job)
    final = load_job_plan(job.job_id)

    remainder_id = raise_remainder_for_final_job(final)
    assert remainder_id
    assert raise_remainder_for_final_job(load_job_plan(job.job_id)) is None
    reloaded = load_job_plan(job.job_id)
    assert _open_ids(reloaded) == [remainder_id]
    [decision] = list_decisions(reloaded, [_stop_event(reloaded)])
    assert decision.payload["question"].startswith(CONTRACT_REMAINDER_MARKER)
