"""`budget_clock`: the working wall clock of a job, which counts work and records every wait (F310, DECISION F310 D4)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

import packages.orchestration.pi_provider as PP
from packages.orchestration.budget_clock import (
    BudgetClockError,
    job_work_start,
    resume_job_clock,
)
from packages.orchestration.budget_guard import (
    BudgetCounterError,
    counters_from_persisted,
    decode_persisted_budget_actuals,
)
from packages.orchestration.execution_config import ExecutionConfig
from tests.orchestration.test_budget_profiles import (  # noqa: F401 (the autouse fixture isolates configuration)
    _git_repo_with_a_task,
    isolated_configuration,
)

T0 = datetime(2026, 7, 1, 11, 0, tzinfo=timezone.utc)
_BASE = {
    "provider_call_count": 4, "actual_call_count": 3, "unmeasured_call_count": 1,
    "total_tokens": 4200, "actual_sources": ["pingpong_live"],
}


@pytest.fixture(autouse=True)
def _no_leftover_job_clock():
    PP._JOB_TIME_LEFT.set(None)
    yield
    PP._JOB_TIME_LEFT.set(None)


def _v1(first):
    return {**_BASE, "schema_version": "1.0.0", "started_at": first.isoformat()}


def _v2(first, *, cost=1.5, priced=2, unpriced=1):
    return {**_v1(first), "schema_version": "2.0.0", "measured_cost_usd": cost,
            "priced_call_count": priced, "unpriced_call_count": unpriced}


def _v3(first, *, waited, active):
    return {**_v2(first), "schema_version": "3.0.0", "waited_s": waited,
            "active_until": active.isoformat()}


def _job(first, record=None, stopped_at=""):
    return SimpleNamespace(first_running_at=first.isoformat() if first else "",
                           budget_actuals=record, stopped_at=stopped_at)


def _decoded(job):
    if not job.budget_actuals:
        return {}
    return decode_persisted_budget_actuals(job.budget_actuals, first_running_at=job.first_running_at)


# --- resume_job_clock ---------------------------------------------------------------------------

def test_a_first_run_starts_now_and_leaves_the_record_alone():
    now = T0 + timedelta(hours=1)
    record = {"untouched": True}
    job = SimpleNamespace(first_running_at="", budget_actuals=record, stopped_at="")
    assert resume_job_clock(job, {}, now=now) == (now, 0.0)
    assert job.budget_actuals is record and record == {"untouched": True}
    assert resume_job_clock(_job(None), {}, now=now) == (now, 0.0)


def test_a_version_three_record_counts_the_gap_since_it_was_last_active():
    active = T0 + timedelta(minutes=5)
    now = active + timedelta(hours=2)
    job = _job(T0, _v3(T0, waited=60, active=active))
    assert resume_job_clock(job, _decoded(job), now=now) == (T0, 7260.0)
    again = decode_persisted_budget_actuals(job.budget_actuals, first_running_at=T0.isoformat())
    assert job.budget_actuals["schema_version"] == "3.0.0"
    assert (again["waited_s"], again["active_until"]) == (7260.0, now)


def test_a_version_two_record_counts_the_gap_from_the_stop_and_keeps_its_money():
    now = T0 + timedelta(hours=3)
    job = _job(T0, _v2(T0), stopped_at=(T0 + timedelta(hours=1)).isoformat())
    assert resume_job_clock(job, _decoded(job), now=now) == (T0, 7200.0)
    again = decode_persisted_budget_actuals(job.budget_actuals, first_running_at=T0.isoformat())
    assert again["schema_version"] == "3.0.0"
    assert (again["measured_cost_usd"], again["priced_call_count"], again["unpriced_call_count"]) == (1.5, 2, 1)
    assert (again["waited_s"], again["active_until"]) == (7200.0, now)


def test_a_version_one_record_upgrades_with_unpriced_money():
    now = T0 + timedelta(hours=2)
    job = _job(T0, _v1(T0), stopped_at=(T0 + timedelta(hours=1)).isoformat())
    assert resume_job_clock(job, _decoded(job), now=now) == (T0, 3600.0)
    again = decode_persisted_budget_actuals(job.budget_actuals, first_running_at=T0.isoformat())
    assert (again["measured_cost_usd"], again["priced_call_count"], again["unpriced_call_count"]) == (None, 0, 0)
    assert again["waited_s"] == 3600.0


def test_a_version_two_record_without_a_stop_counts_nothing():
    now = T0 + timedelta(hours=2)
    job = _job(T0, _v2(T0))
    assert resume_job_clock(job, _decoded(job), now=now) == (T0, 0.0)
    assert job.budget_actuals["waited_s"] == 0.0


def test_an_unreadable_first_run_is_refused_by_name():
    with pytest.raises(BudgetClockError, match="cannot parse 'not-a-time'"):
        resume_job_clock(SimpleNamespace(first_running_at="not-a-time", budget_actuals=None,
                                         stopped_at=""), {}, now=T0)
    naive = "2026-07-01T11:00:00"
    with pytest.raises(BudgetClockError, match="timezone-naive value '2026-07-01T11:00:00'"):
        resume_job_clock(SimpleNamespace(first_running_at=naive, budget_actuals=None,
                                         stopped_at=""), {}, now=T0)


# --- the decoder --------------------------------------------------------------------------------

def test_a_version_three_record_decodes_its_clock():
    active = T0 + timedelta(minutes=5)
    decoded = decode_persisted_budget_actuals(_v3(T0, waited=90, active=active))
    assert (decoded["waited_s"], decoded["active_until"]) == (90.0, active)


@pytest.mark.parametrize(("field", "value", "message"), [
    ("waited_s", -1, "persisted waited_s"),
    ("waited_s", True, "persisted waited_s"),
    ("waited_s", float("inf"), "persisted waited_s"),
    ("waited_s", "5", "persisted waited_s"),
    ("active_until", "2026-07-01T11:05:00", "persisted active_until"),
    ("active_until", "2026-07-01T10:59:00+00:00", "persisted active_until"),
    ("active_until", "yesterday", "persisted active_until"),
])
def test_a_corrupt_clock_field_is_refused(field, value, message):
    record = {**_v3(T0, waited=90, active=T0 + timedelta(minutes=5)), field: value}
    with pytest.raises(BudgetCounterError, match=message):
        decode_persisted_budget_actuals(record)


def test_a_version_three_record_without_active_until_is_refused():
    record = _v3(T0, waited=90, active=T0)
    del record["active_until"]
    with pytest.raises(BudgetCounterError, match="active_until"):
        decode_persisted_budget_actuals(record)


def test_a_version_two_record_decodes_nothing_waited():
    decoded = decode_persisted_budget_actuals(_v2(T0))
    assert (decoded["waited_s"], decoded["active_until"]) == (0.0, None)


def test_the_counters_subtract_the_seconds_waited():
    decoded = decode_persisted_budget_actuals(_v3(T0, waited=600, active=T0 + timedelta(minutes=5)))
    counters = counters_from_persisted(decoded, now=T0 + timedelta(hours=1))
    assert counters.elapsed_seconds == 3000.0


# --- job_work_start -----------------------------------------------------------------------------

def test_the_working_start_is_the_first_run_plus_the_seconds_waited():
    assert job_work_start(_job(T0, {"waited_s": 90})) == T0 + timedelta(seconds=90)
    assert job_work_start(_job(T0, {"waited_s": 2.5})) == T0 + timedelta(seconds=2.5)


@pytest.mark.parametrize("record", [None, {}, {"waited_s": True}, {"waited_s": -3},
                                    {"waited_s": float("nan")}, {"waited_s": "9"}])
def test_the_working_start_ignores_a_waiting_it_cannot_read(record):
    assert job_work_start(_job(T0, record)) == T0


def test_there_is_no_working_start_before_the_first_run():
    assert job_work_start(_job(None)) is None


def test_an_unreadable_first_run_has_no_working_start():
    with pytest.raises(ValueError):
        job_work_start(SimpleNamespace(first_running_at="soon", budget_actuals=None))


# --- through run_job and the Pi call ------------------------------------------------------------

def _resumed_job(tmp_path, *, last_active_ago):
    """A local job whose first run was nine hours ago and which was last active `last_active_ago` ago."""
    now = datetime.now(timezone.utc)
    first = now - timedelta(hours=9)
    job = _git_repo_with_a_task(tmp_path)
    job.execution_config = ExecutionConfig(builder="pi", reviewer="pi")
    job.first_running_at = first.isoformat()
    job.budget_actuals = _v3(first, waited=0, active=now - last_active_ago)
    return job


def _run(job):
    from packages.orchestration.pingpong_job import _persist_job, run_job
    from packages.orchestration.pingpong_provider import FakeProvider

    _persist_job(job)
    return run_job(job.job_id, builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                   reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99))


def test_a_job_that_waited_most_of_nine_hours_is_not_stopped_by_the_wall_clock(tmp_path):
    result = _run(_resumed_job(tmp_path, last_active_ago=timedelta(hours=8, minutes=55)))
    assert "max_wall_clock_minutes" not in result.stop_reason, result.stop_reason
    assert result.budget_actuals["schema_version"] == "3.0.0"
    assert result.budget_actuals["waited_s"] >= 31800


def test_a_job_that_was_active_a_minute_ago_is_stopped_by_the_wall_clock(tmp_path):
    result = _run(_resumed_job(tmp_path, last_active_ago=timedelta(minutes=1)))
    assert result.state == "stopped"
    assert "max_wall_clock_minutes" in result.stop_reason, result.stop_reason


def test_the_pi_call_reads_the_time_left_by_work_alone(tmp_path):
    for n, (ago, has_time) in enumerate(((timedelta(hours=8, minutes=55), True),
                                         (timedelta(minutes=1), False))):
        job = _resumed_job(tmp_path / str(n), last_active_ago=ago)
        _, waited = resume_job_clock(job, _decoded(job))
        assert waited >= ago.total_seconds()
        PP.bind_job_clock(job)
        left = PP.effective_pi_timeout(600)[1]["job_left_sec"]
        assert (left > 0) is has_time, left
