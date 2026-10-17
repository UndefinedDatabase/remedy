"""The order's ledger as arithmetic: shares of the caps, refusals and the walk's recorded spend."""
from __future__ import annotations

import pytest

from packages.orchestration.order_ledger import (
    OrderCallLedger,
    OrderCallRefusedError,
    bind_order_ledger,
    bound_order_ledger,
    reason_for,
)


class _Clock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


class _Job:
    def __init__(self, job_id: str, calls: int, tokens: int, cost: float | None = None):
        self.job_id = job_id
        self.budget_actuals = {
            "schema_version": "2.0.0", "provider_call_count": calls, "actual_call_count": calls,
            "unmeasured_call_count": 0, "total_tokens": tokens, "started_at": "2026-10-17T08:00:00+00:00",
            "actual_sources": ["pingpong_actuals"] if calls else [], "measured_cost_usd": cost,
            "priced_call_count": calls if cost is not None else 0,
            "unpriced_call_count": 0 if cost is not None else calls}


def _ok(prompt: str, attempt: int) -> str:
    return "x" * 40


def test_an_uncapped_order_limits_nothing_and_still_records():
    ledger = OrderCallLedger(caps=None)
    wrapped = ledger.wrap("intake", _ok)
    for _ in range(5):
        wrapped("p" * 40, 0)
    assert ledger.exhausted() == "" and ledger.remaining() is None
    assert ledger.planner_calls == 5 and ledger.entries[0]["estimated_tokens"] == 20


def test_planning_calls_count_against_the_call_cap_and_the_next_one_is_refused():
    ledger = OrderCallLedger(caps={"max_provider_calls": 2})
    wrapped = ledger.wrap("task_plan", _ok)
    wrapped("p", 0)
    wrapped("p", 1)
    with pytest.raises(OrderCallRefusedError, match="cap of 2 provider calls"):
        wrapped("p", 0)
    assert ledger.planner_calls == 2 and ledger.summary()["refused_calls"] == 1
    assert ledger.entries[-1]["outcome"].startswith("refused")


def test_a_failing_call_is_recorded_with_its_error_and_still_counts():
    ledger = OrderCallLedger(caps={"max_provider_calls": 5})

    def boom(prompt: str, attempt: int) -> str:
        raise TimeoutError("slow")

    with pytest.raises(TimeoutError):
        ledger.wrap("mission_plan", boom)("p", 0)
    assert ledger.entries[0]["outcome"] == "error: TimeoutError" and ledger.planner_calls == 1


def test_each_job_gets_the_caps_less_planning_and_the_jobs_before_it():
    ledger = OrderCallLedger(caps={"max_provider_calls": 30, "max_total_tokens": 10_000,
                                   "max_cost_usd": 1.0, "deadline": None})
    ledger.wrap("intake", _ok)("p" * 400, 0)         # 1 call, (400 + 40) // 4 = 110 estimated tokens
    ledger.record_job(_Job("j1", calls=9, tokens=3000, cost=0.25))
    left = ledger.remaining()
    assert left["max_provider_calls"] == 30 - 1 - 9
    assert left["max_total_tokens"] == 10_000 - 110 - 3000
    assert left["max_cost_usd"] == pytest.approx(0.75)
    assert left["deadline"] is None


def test_the_wall_clock_cap_is_shared_by_the_whole_order():
    clock = _Clock()
    ledger = OrderCallLedger(caps={"max_wall_clock_minutes": 10}, clock=clock)
    clock.now += 4 * 60 + 1
    assert ledger.remaining()["max_wall_clock_minutes"] == 6
    clock.now += 6 * 60
    assert "10 minute(s) of wall-clock time" in ledger.exhausted()


def test_a_spent_cap_stops_the_next_job_and_a_spent_job_is_counted_once():
    ledger = OrderCallLedger(caps={"max_provider_calls": 10})
    ledger.record_job(_Job("j1", calls=10, tokens=0))
    ledger.record_job(_Job("j1", calls=10, tokens=0))       # a resumed job's actuals replace its entry
    assert "cap of 10 provider calls is spent (10 used)" in ledger.exhausted()


def test_a_job_whose_actuals_cannot_be_decoded_counts_as_unmeasured_not_as_free_spend_of_garbage():
    job = _Job("j1", calls=1, tokens=1)
    job.budget_actuals = {"schema_version": "9"}
    ledger = OrderCallLedger(caps={"max_provider_calls": 5})
    ledger.record_job(job)
    assert ledger.jobs["j1"]["measured"] is False


def test_the_bound_ledger_is_visible_only_inside_its_block_and_reasons_name_the_schema():
    ledger = OrderCallLedger()
    assert bound_order_ledger() is None
    with bind_order_ledger(ledger):
        assert bound_order_ledger() is ledger
    assert bound_order_ledger() is None

    class TaskPlan:
        pass

    assert reason_for(TaskPlan) == "task_plan"


def test_two_failures_in_a_row_end_planner_use_and_an_answer_resets_the_count():
    ledger = OrderCallLedger(caps=None)
    answers = iter(["fail", "ok", "fail", "fail", "never"])

    def flaky(prompt: str, attempt: int) -> str:
        if next(answers) == "ok":
            return "{}"
        raise TimeoutError("slow")

    wrapped = ledger.wrap("task_plan", flaky)
    for expected_error in (TimeoutError, None, TimeoutError, TimeoutError):
        if expected_error is None:
            wrapped("p", 0)
        else:
            with pytest.raises(expected_error):
                wrapped("p", 0)
    with pytest.raises(OrderCallRefusedError, match="failed 2 calls in a row"):
        wrapped("p", 0)
    assert ledger.planner_calls == 4 and ledger.summary()["refused_calls"] == 1
