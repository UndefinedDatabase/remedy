"""F295 R12 — DECISION F295 D11: `answer_budget_decision`, its readers and the
resume guard's fourth guard, over a job a budget stop left `stopped` (R-1146).

Every test here builds a `JobPlan` stopped by its budget the way
`tests.orchestration.test_resume_cli._budget_stopped_job` builds one — with
`budgets`, `stop_reason`, `stop_request_id` and an explicit `stopped_at` — and
answers it against a fixed `now`, never the real clock.
"""
from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone

import pytest

from packages.orchestration.budget_decision import answer_budget_decision
from packages.orchestration.budget_resolution import BudgetConfigError, parse_budget_limit
from packages.orchestration.decision_queue import (
    budget_decision_id,
    list_decisions,
    open_budget_decision_id,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry

#: The fixed clock every test answers against — never `datetime.now()`.
NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

_DEFAULT_BUDGETS = {"deadline": "2025-12-01T00:00:00+00:00"}


def _budget_stopped_job(
    *,
    stop_reason: str = "budget_exhausted:deadline",
    budgets: dict | None = None,
    stopped_at: datetime = NOW,
    request_id: str = "req1",
) -> JobPlan:
    """A `JobPlan` stopped by its budget, with an explicit `stopped_at`."""
    job = JobPlan(job_title="budget-decision-job", tasks=[TaskEntry(title="d")])
    job.stop_source = "budget"
    job.stop_reason = stop_reason
    job.stop_request_id = request_id
    job.stopped_at = stopped_at.isoformat()
    job.budgets = dict(_DEFAULT_BUDGETS if budgets is None else budgets)
    return job


def _open_decision_id(job: JobPlan) -> str:
    return budget_decision_id(job.stop_request_id)


class TestExtendRecordsTheAnswer:
    def test_extend_raises_the_exhausted_limit_and_records_the_answer(self) -> None:
        job = _budget_stopped_job()
        decision_id = _open_decision_id(job)
        new_deadline = NOW + timedelta(days=1)

        result = answer_budget_decision(
            job, decision_id, "extend", [f"deadline={new_deadline.isoformat()}"],
            now=NOW)

        assert result["outcome"] == "extended"
        raised_deadline = datetime.fromisoformat(
            job.budgets["deadline"].replace("Z", "+00:00"))
        assert raised_deadline == new_deadline

        records = job.metadata["budget_decision_answers"]
        assert len(records) == 1
        record = records[0]
        for key in ("decision_id", "request_id", "option", "raised", "answered_at", "actor"):
            assert key in record, key
        assert record["decision_id"] == decision_id
        assert record["request_id"] == job.stop_request_id
        assert record["option"] == "extend"
        assert record["actor"] == "cli"

        assert open_budget_decision_id(job) == ""

    def test_a_stop_after_the_answer_is_open_again_under_the_same_request_id(self) -> None:
        job = _budget_stopped_job()
        decision_id = _open_decision_id(job)
        new_deadline = NOW + timedelta(days=1)

        answer_budget_decision(
            job, decision_id, "extend", [f"deadline={new_deadline.isoformat()}"],
            now=NOW)
        assert open_budget_decision_id(job) == ""

        job.stopped_at = (NOW + timedelta(hours=1)).isoformat()

        assert open_budget_decision_id(job) == decision_id

    def test_list_decisions_leaves_an_answered_budget_stop_out(self) -> None:
        job = _budget_stopped_job()
        decision_id = _open_decision_id(job)
        stop_event = {
            "event": "job_stopped",
            "timestamp": NOW.isoformat(),
            "metadata": {
                "source": "budget", "request_id": job.stop_request_id,
                "reason": job.stop_reason, "exhausted_limit": "deadline",
            },
        }

        ids_before = [d.id for d in list_decisions(job, [stop_event])]
        assert decision_id in ids_before

        new_deadline = NOW + timedelta(days=1)
        result = answer_budget_decision(
            job, decision_id, "extend", [f"deadline={new_deadline.isoformat()}"],
            now=NOW)
        assert result["outcome"] == "extended"

        ids_after = [d.id for d in list_decisions(job, [stop_event])]
        assert decision_id not in ids_after

        job.stop_request_id = "req2"
        job.stopped_at = (NOW + timedelta(hours=2)).isoformat()
        later_event = {
            "event": "job_stopped",
            "timestamp": (NOW + timedelta(hours=2)).isoformat(),
            "metadata": {
                "source": "budget", "request_id": "req2",
                "reason": job.stop_reason, "exhausted_limit": "deadline",
            },
        }
        ids_later = [d.id for d in list_decisions(job, [later_event])]
        assert any(i.startswith("budget") for i in ids_later)


def _case_unknown_decision():
    job = _budget_stopped_job()
    return job, "budget:does-not-exist", "extend", \
        ["deadline=2026-02-01T00:00:00+00:00"], "decision_not_found"


def _case_already_answered():
    job = _budget_stopped_job()
    decision_id = _open_decision_id(job)
    answer_budget_decision(
        job, decision_id, "extend", ["deadline=2026-02-01T00:00:00+00:00"], now=NOW)
    return job, decision_id, "extend", ["deadline=2026-02-02T00:00:00+00:00"], \
        "decision_already_answered"


def _case_bad_reason():
    job = _budget_stopped_job()
    return job, _open_decision_id(job), "abandon", \
        ["deadline=2026-02-01T00:00:00+00:00"], "invalid_argument"


def _case_no_answers():
    job = _budget_stopped_job()
    return job, _open_decision_id(job), "extend", [], "missing_argument"


def _case_unknown_limit():
    job = _budget_stopped_job()
    return job, _open_decision_id(job), "extend", ["nope=1"], "invalid_budget"


def _case_bad_value():
    job = _budget_stopped_job()
    return job, _open_decision_id(job), "extend", ["max_cost_usd=abc"], "invalid_budget"


def _case_malformed():
    job = _budget_stopped_job()
    return job, _open_decision_id(job), "extend", ["max_cost_usd"], "invalid_budget"


def _case_disallowed_limit_name():
    job = _budget_stopped_job()
    return job, _open_decision_id(job), "extend", ["min_free_disk_bytes=5"], "invalid_budget"


def _case_wrong_limit_raised():
    job = _budget_stopped_job(stop_reason="budget_exhausted:deadline")
    return job, _open_decision_id(job), "extend", ["max_cost_usd=2"], \
        "budget_limit_not_raised"


def _case_cost_not_raised():
    job = _budget_stopped_job(
        stop_reason="budget_exhausted:max_cost_usd", budgets={"max_cost_usd": 1.0})
    return job, _open_decision_id(job), "extend", ["max_cost_usd=1.0"], \
        "budget_limit_not_raised"


def _case_deadline_earlier_than_now():
    job = _budget_stopped_job()
    earlier = (NOW - timedelta(days=1)).isoformat()
    return job, _open_decision_id(job), "extend", [f"deadline={earlier}"], \
        "budget_limit_not_raised"


def _case_disk_floor_stop():
    job = _budget_stopped_job(stop_reason="budget_exhausted:min_free_disk_bytes")
    return job, _open_decision_id(job), "extend", ["max_cost_usd=100"], \
        "budget_limit_not_raisable"


_REFUSAL_CASES = (
    _case_unknown_decision,
    _case_already_answered,
    _case_bad_reason,
    _case_no_answers,
    _case_unknown_limit,
    _case_bad_value,
    _case_malformed,
    _case_disallowed_limit_name,
    _case_wrong_limit_raised,
    _case_cost_not_raised,
    _case_deadline_earlier_than_now,
    _case_disk_floor_stop,
)


class TestEachRefusalNamesItsTokenAndChangesNothing:
    @pytest.mark.parametrize("make_case", _REFUSAL_CASES,
                             ids=[c.__name__ for c in _REFUSAL_CASES])
    def test_each_refusal_names_its_token_and_changes_nothing(self, make_case) -> None:
        job, decision_id, reason, answers, expected_code = make_case()
        budgets_before = copy.deepcopy(job.budgets)
        metadata_before = copy.deepcopy(job.metadata)

        result = answer_budget_decision(job, decision_id, reason, answers, now=NOW)

        assert result["outcome"] == "refused"
        assert result["code"] == expected_code
        assert job.budgets == budgets_before
        assert job.metadata == metadata_before


def test_a_stop_reason_naming_no_limit_accepts_any_raise() -> None:
    job = _budget_stopped_job(stop_reason="budget_exhausted", budgets={})
    decision_id = _open_decision_id(job)

    result = answer_budget_decision(job, decision_id, "extend", ["max_cost_usd=5"], now=NOW)

    assert result["outcome"] == "extended"
    assert job.budgets["max_cost_usd"] == 5.0


def test_parse_budget_limit_parses_each_limit_and_refuses_others() -> None:
    assert parse_budget_limit("max_total_tokens", "100") == 100
    assert parse_budget_limit("max_provider_calls", "5") == 5
    assert parse_budget_limit("max_wall_clock_minutes", "30") == 30
    assert parse_budget_limit("max_cost_usd", "2.5") == 2.5
    assert parse_budget_limit("deadline", "2026-02-01T00:00:00+00:00") == datetime(
        2026, 2, 1, tzinfo=timezone.utc)

    with pytest.raises(BudgetConfigError):
        parse_budget_limit("min_free_disk_bytes", "5")
    with pytest.raises(BudgetConfigError):
        parse_budget_limit("nope", "1")
