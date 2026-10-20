"""`budget_stop`: one stop, one question: the blockers, the doubling and the resume (F310, DECISION F310 D5)."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from packages.orchestration import public_api
from packages.orchestration.api_clients import ApiClient, client_budget_answer_refusal
from packages.orchestration.budget_decision import answer_budget_decision
from packages.orchestration.budget_stop import (
    budget_stop_blockers,
    budget_stop_walk_note,
    doubled_limit_answers,
    raise_remainder_for_final_job,
    resume_after_budget_extend,
)
from packages.orchestration.decision_queue import budget_decision_id, list_decisions
from packages.orchestration.execution_config import ExecutionConfig
from packages.orchestration.mission_contract import ContractCriterion, MissionContract, write_mission_contract
from packages.orchestration.mission_state import create_mission, link_job_to_mission
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.serve_runs import RunRecord, RunRefused, run_record_payload
from tests.orchestration.test_budget_profiles import isolated_configuration  # noqa: F401 (autouse fixture)

NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
PROJECT = "p-f310"
FIRST = NOW - timedelta(hours=2)


@pytest.fixture(autouse=True)
def _data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))


def _stopped_job(limit: str, *, budgets: dict | None = None, actuals: dict | None = None) -> JobPlan:
    """A local job (the profile's 1,500,000 tokens, 200 calls, 480 minutes) a budget stopped on LIMIT."""
    job = JobPlan(job_title="budget-stop", tasks=[TaskEntry(title="d")],
                  execution_config=ExecutionConfig(builder="pi", reviewer="pi"))
    job.stop_source, job.stop_request_id = "budget", "req1"
    job.stop_reason, job.stopped_at = f"budget_exhausted:{limit}", NOW.isoformat()
    job.budgets = budgets
    if actuals is not None:
        job.first_running_at = FIRST.isoformat()
        job.budget_actuals = {
            "schema_version": "3.0.0", "started_at": FIRST.isoformat(), "waited_s": 0,
            "active_until": (FIRST + timedelta(minutes=1)).isoformat(),
            "actual_sources": ["pingpong_live"], "measured_cost_usd": None,
            "priced_call_count": 0, "unpriced_call_count": 0, **actuals}
    return job


def _calls_and_tokens(calls: int, tokens: int) -> dict:
    return {"provider_call_count": calls, "actual_call_count": calls,
            "unmeasured_call_count": 0, "total_tokens": tokens}


def _criteria(*specs: tuple[str, str, bool, str]) -> MissionContract:
    return MissionContract(criteria=tuple(
        ContractCriterion(id=ident, text=text, origin="planner", blocking=blocking, status=status)
        for ident, text, blocking, status in specs))


def _linked_job(contract: MissionContract | None) -> JobPlan:
    job = JobPlan(job_title="in-a-mission", tasks=[TaskEntry(title="d")])
    save_job_plan(job)
    if contract is not None:
        mission = create_mission(PROJECT, "Ship the tool")
        write_mission_contract(PROJECT, mission.id, contract)
        link_job_to_mission(PROJECT, mission.id, str(job.job_id), "initial")
    return job


# --- budget_stop_blockers ------------------------------------------------------------------------

def test_a_job_of_a_mission_names_each_blocking_criterion_by_id_and_text():
    job = _linked_job(_criteria(("C001", "the suite passes", True, "open"),
                                ("C002", "the docs name every command", True, "unmet"),
                                ("C003", "the code is pleasant", False, "open"),
                                ("C004", "it ships", True, "met")))
    assert budget_stop_blockers(job) == ["C001: the suite passes", "C002: the docs name every command"]


def test_a_job_of_no_mission_and_a_mission_with_no_blocker_name_none():
    assert budget_stop_blockers(_linked_job(None)) == []
    assert budget_stop_blockers(_linked_job(_criteria(("C001", "it ships", True, "met")))) == []


# --- doubled_limit_answers -----------------------------------------------------------------------

def test_a_stop_on_the_profiles_wall_clock_doubles_the_profiles_value():
    assert doubled_limit_answers(_stopped_job("max_wall_clock_minutes")) == ["max_wall_clock_minutes=960"]


def test_a_wall_clock_of_nine_minutes_doubles_to_at_least_sixty():
    job = _stopped_job("max_wall_clock_minutes", budgets={"max_wall_clock_minutes": 9})
    assert doubled_limit_answers(job) == ["max_wall_clock_minutes=60"]


def test_a_stop_on_calls_doubles_the_token_limit_too_when_the_saved_actuals_reached_it():
    job = _stopped_job("max_provider_calls", budgets={"max_total_tokens": 1000, "max_provider_calls": 5},
                       actuals=_calls_and_tokens(5, 1000))
    assert doubled_limit_answers(job, now=NOW) == ["max_total_tokens=2000", "max_provider_calls=10"]


def test_a_limit_the_actuals_did_not_reach_is_not_doubled():
    job = _stopped_job("max_provider_calls", budgets={"max_total_tokens": 1000, "max_provider_calls": 5},
                       actuals=_calls_and_tokens(5, 999))
    assert doubled_limit_answers(job, now=NOW) == ["max_provider_calls=10"]


def test_a_job_that_waited_does_not_double_a_wall_clock_its_work_stayed_under():
    # R-1373: the record began two hours before its last active moment and waited 7,000 s of that,
    # so its work is 200 s, under the 540 s of nine minutes; only the calls were exhausted.
    job = _stopped_job("max_provider_calls", budgets={"max_wall_clock_minutes": 9, "max_provider_calls": 3},
                       actuals={**_calls_and_tokens(3, 100), "waited_s": 7000,
                                "active_until": NOW.isoformat()})
    assert doubled_limit_answers(job, now=NOW) == ["max_provider_calls=6"]


def test_a_deadline_stop_and_a_disk_floor_stop_double_nothing():
    assert doubled_limit_answers(_stopped_job("deadline")) == []
    assert doubled_limit_answers(_stopped_job("min_free_disk_bytes")) == []


# --- answer_budget_decision ----------------------------------------------------------------------

def _extend(job: JobPlan, *answers: str) -> dict:
    return answer_budget_decision(job, budget_decision_id(job.stop_request_id), "extend",
                                  list(answers), now=NOW)


def test_extend_with_no_answer_doubles_what_the_stop_exhausted():
    job = _stopped_job("max_wall_clock_minutes", budgets={"max_wall_clock_minutes": 9})
    result = _extend(job)
    assert result["outcome"] == "extended"
    assert result["raised"] == {"max_wall_clock_minutes": 60}
    assert job.budgets["max_wall_clock_minutes"] == 60


def test_an_answer_below_the_value_the_run_read_is_refused():
    result = _extend(_stopped_job("max_wall_clock_minutes"), "max_wall_clock_minutes=60")
    assert (result["outcome"], result["code"]) == ("refused", "budget_limit_not_raised")


def test_an_answer_above_the_value_the_run_read_holds_and_writes_only_that_limit():
    job = _stopped_job("max_wall_clock_minutes")
    result = _extend(job, "max_wall_clock_minutes=1000")
    assert result["outcome"] == "extended"
    assert {name: value for name, value in job.budgets.items() if value is not None} == {
        "max_wall_clock_minutes": 1000}


def test_a_deadline_stop_with_no_answer_is_still_refused():
    result = _extend(_stopped_job("deadline"))
    assert (result["outcome"], result["code"]) == ("refused", "missing_argument")


# --- list_decisions ------------------------------------------------------------------------------

def test_the_budget_decision_carries_the_blockers_of_the_jobs_mission():
    job = _linked_job(_criteria(("C001", "the suite passes", True, "open")))
    job.stop_source, job.stop_reason, job.stop_request_id = "budget", "budget_exhausted:max_cost_usd", "req9"
    job.stopped_at = NOW.isoformat()
    event = {"event": "job_stopped", "timestamp": NOW.isoformat(),
             "metadata": {"source": "budget", "request_id": "req9", "reason": job.stop_reason,
                          "exhausted_limit": "max_cost_usd"}}
    [decision] = [d for d in list_decisions(job, [event]) if d.type == "token_budget"]
    assert decision.payload == {"options": ["extend", "abandon"], "blockers": ["C001: the suite passes"]}


# --- through the public API ----------------------------------------------------------------------

JOB = "0b8c1f3e-1111-4222-8333-444455556666"
DECISION_PATH = f"/api/v1/jobs/{JOB}/decisions/"
ENDED = RunRecord(job_id=JOB, pid=4242, started_at="2026-01-01T00:00:00Z", out_log="/data/out",
                  err_log="/data/err", exit_code=0, ended_at="2026-01-01T00:00:01Z")


def _post(decision: str, envelope: dict, start_run, client=None):
    asked: list = []

    def run_command(key, argv):
        asked.append(argv)
        return envelope

    body = json.dumps({"reason": "extend"}).encode()
    return public_api.answer_public_api_post(
        DECISION_PATH + decision, body, run_command, client=client, start_run=start_run), asked


def _starter(outcome: object = None):
    calls: list = []

    def start(job, options):
        calls.append((job, tuple(options)))
        if isinstance(outcome, Exception):
            raise outcome
        return ENDED

    return calls, start


def test_an_extended_answer_starts_the_run_by_the_full_id_and_names_it():
    calls, start = _starter()
    (status, body, _headers), _asked = _post(
        "budget:req1", {"ok": True, "outcome": "extended", "raised": {}}, start)
    assert status == 200
    assert body["resumed"] == run_record_payload(serve_paths(), ENDED)
    assert calls == [(JOB, ())]


def test_a_refused_start_is_named_beside_an_answer_that_stands():
    calls, start = _starter(RunRefused("job_already_running", "a run of this job is live"))
    (status, body, _headers), _asked = _post(
        "budget:req1", {"ok": True, "outcome": "extended"}, start)
    assert status == 200 and body["ok"] is True and body["resumed"] is None
    assert body["resume_refused"] == {"error": "job_already_running", "message": "a run of this job is live"}
    assert len(calls) == 1


def test_a_start_that_fails_on_the_disk_is_named_too():
    _calls, start = _starter(OSError("no space"))
    (_status, body, _headers), _asked = _post("budget:req1", {"ok": True, "outcome": "extended"}, start)
    assert body["resumed"] is None and body["resume_refused"]["error"] == "api_command_failed"


@pytest.mark.parametrize(("twin", "envelope"), [
    ("decision.resolve", {"ok": True, "outcome": "abandoned"}),
    ("decision.resolve", {"ok": True, "outcome": "resolved"}),
    ("decision.resolve", {"ok": False, "error": "decision_not_found", "outcome": "extended"}),
    ("job.apply", {"ok": True, "outcome": "extended"}),
])
def test_an_answer_of_another_kind_starts_nothing(twin, envelope):
    calls, start = _starter()
    assert resume_after_budget_extend(twin, {"job": JOB}, envelope, start) is envelope
    assert calls == []
    assert resume_after_budget_extend("decision.resolve", {"job": JOB}, {"ok": True, "outcome": "extended"},
                                      None) == {"ok": True, "outcome": "extended"}


def test_a_stop_answered_over_the_api_with_a_resolved_decision_starts_nothing():
    calls, start = _starter()
    (status, body, _headers), _asked = _post("sr:abc", {"ok": True, "outcome": "resolved"}, start)
    assert (status, "resumed" in body, calls) == (200, False, [])


def test_a_client_is_judged_on_the_doubled_value_when_it_sends_no_answer():
    job = _stopped_job("max_total_tokens", budgets={"max_total_tokens": 600})
    save_job_plan(job)
    client = ApiClient(name="bot", token="t" * 32, projects=("p",), max_total_tokens=1000,
                       max_provider_calls=None, may_apply=False)
    refusal = client_budget_answer_refusal(client, [], job=str(job.job_id))
    assert refusal is not None and "at most 1000" in refusal and "gives 1200" in refusal
    assert client_budget_answer_refusal(client, []) is None
    assert client_budget_answer_refusal(client, [], job="ffffffff") is None


# --- the walk's note and the remainder at a final stop (DECISION F310 D6) -------------------------

def test_a_walk_note_for_an_open_budget_stop_names_its_one_question_and_adds_one_next_line():
    ctx = SimpleNamespace(next_lines=[])
    job = _linked_job(_criteria(("C001", "the suite passes", True, "open")))
    job.stop_source, job.stop_request_id = "budget", "req1"
    note = budget_stop_walk_note(ctx, job)
    decision_id = budget_decision_id("req1")
    assert ctx.next_lines == [f"remedy decision resolve {job.job_id} {decision_id} --reason extend"]
    assert f"budget decision {decision_id} is its one open question, answered extend or abandon" in note
    assert note.endswith(", and it names the mission's open blocking criteria")


def test_a_walk_note_without_a_budget_stop_is_empty_and_adds_nothing():
    ctx = SimpleNamespace(next_lines=[])
    assert budget_stop_walk_note(ctx, _linked_job(None)) == ""
    assert ctx.next_lines == []


def test_a_job_that_is_not_cancelled_raises_no_remainder_decision():
    job = _linked_job(_criteria(("C001", "the suite passes", True, "open")))
    job.stop_source, job.stop_request_id = "budget", "req1"
    assert raise_remainder_for_final_job(job) is None


def test_a_cancelled_job_lists_only_its_missions_open_remainder_decision():
    from packages.core.models import RunState
    from packages.orchestration.escalation import enqueue_task_decision
    from packages.orchestration.pingpong_job import load_job_plan

    job = _linked_job(_criteria(("C001", "the suite passes", True, "open")))
    enqueue_task_decision(job, task_id=job.tasks[0].task_id, question="Which database?",
                          options=("a", "b"), safe_default="", impact="", now=NOW)
    job.state = RunState.CANCELLED
    save_job_plan(job)
    remainder_id = raise_remainder_for_final_job(load_job_plan(job.job_id))
    assert remainder_id
    listed = list_decisions(load_job_plan(job.job_id), [])
    assert [d.id for d in listed] == [remainder_id]
