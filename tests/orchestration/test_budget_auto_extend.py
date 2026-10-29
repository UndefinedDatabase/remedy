"""F328 (operator order beweis): an unattended job raises its call or token cap once by itself."""
from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

from packages.core.models import JobBudgets
from packages.orchestration.budget_auto_extend import (
    AUTO_EXTEND_ASSUMPTION,
    JOB_AUTO_EXTEND_KEY,
    JOB_AUTO_EXTENDED_KEY,
    should_stop_or_extend,
)
from packages.orchestration.budget_guard import BudgetCounters
from packages.orchestration.client_story import story_assumptions
from packages.orchestration.job_unattended import JOB_ASSUMPTIONS_KEY
from packages.orchestration.order_jobs import JOB_UNATTENDED_KEY

NOW = datetime(2026, 10, 29, 12, 0, tzinfo=timezone.utc)
#: WHY a list: the tests read which jobs the extension saved instead of writing a record.
_saved: list = []


def _job(**metadata):
    # WHY a namespace: the extension reads only `metadata` and `budgets`, as a JobPlan carries them.
    return SimpleNamespace(job_id="job-f328", metadata={JOB_UNATTENDED_KEY: True, **metadata},
                           budgets={"max_provider_calls": 4, "max_wall_clock_minutes": 30})


def _calls(n: int) -> BudgetCounters:
    return BudgetCounters(provider_calls=n, measured_call_count=n, actual_sources=("pingpong_actuals",))


def test_the_first_call_cap_of_an_unattended_job_doubles_once_and_is_an_assumption(tmp_path):
    job, budgets = _job(), JobBudgets(max_provider_calls=4)
    result = should_stop_or_extend(job.job_id, job=job, budgets=budgets, counters=_calls(4), now=NOW,
                                   control_root_path=tmp_path, persist=_saved.append)
    assert not result.should_stop
    assert budgets.max_provider_calls == 8 and job.budgets["max_provider_calls"] == 8
    assert job.budgets["max_wall_clock_minutes"] == 30
    assert job.metadata[JOB_AUTO_EXTENDED_KEY] == {"at": NOW.isoformat(), "max_provider_calls": 8}
    [entry] = story_assumptions(job)
    assert entry["assumed"] == AUTO_EXTEND_ASSUMPTION == "Remedy hat das Budget einmal selbst erhöht, weil niemand da war"
    assert "provider calls" in entry["question"]
    assert _saved[-1] is job


def test_the_second_touch_stops_with_the_budget_question(tmp_path):
    job, budgets = _job(), JobBudgets(max_provider_calls=4)
    should_stop_or_extend(job.job_id, job=job, budgets=budgets, counters=_calls(4), now=NOW,
                          control_root_path=tmp_path, persist=_saved.append)
    second = should_stop_or_extend(job.job_id, job=job, budgets=budgets, counters=_calls(8), now=NOW,
                                   control_root_path=tmp_path, persist=_saved.append)
    assert second.should_stop and second.source == "budget"
    assert second.reason == "budget_exhausted:max_provider_calls"
    assert budgets.max_provider_calls == 8 and len(job.metadata[JOB_ASSUMPTIONS_KEY]) == 1


def test_a_token_cap_is_extended_too(tmp_path):
    job, budgets = _job(), JobBudgets(max_total_tokens=1000)
    counters = BudgetCounters(provider_calls=1, measured_token_total=1000, measured_call_count=1,
                              actual_sources=("pingpong_actuals",))
    assert not should_stop_or_extend(job.job_id, job=job, budgets=budgets, counters=counters, now=NOW,
                                     control_root_path=tmp_path, persist=_saved.append).should_stop
    assert budgets.max_total_tokens == 2000


def test_the_time_cap_is_never_extended(tmp_path):
    job, budgets = _job(), JobBudgets(max_wall_clock_minutes=1)
    counters = BudgetCounters(elapsed_seconds=120.0, actual_sources=("pingpong_actuals",))
    result = should_stop_or_extend(job.job_id, job=job, budgets=budgets, counters=counters, now=NOW,
                                   control_root_path=tmp_path, persist=_saved.append)
    assert result.should_stop and result.source == "budget"
    assert budgets.max_wall_clock_minutes == 1 and JOB_AUTO_EXTENDED_KEY not in job.metadata


def test_auto_extend_false_and_an_attended_job_stop_at_the_first_cap(tmp_path):
    for job in (_job(**{JOB_AUTO_EXTEND_KEY: False}), _job(**{JOB_UNATTENDED_KEY: False})):
        budgets = JobBudgets(max_provider_calls=4)
        result = should_stop_or_extend(job.job_id, job=job, budgets=budgets, counters=_calls(4), now=NOW,
                                       control_root_path=tmp_path, persist=_saved.append)
        assert result.should_stop and budgets.max_provider_calls == 4
        assert story_assumptions(job) == []


def test_a_walk_without_auto_extend_stores_it_on_its_job(monkeypatch):
    from packages.orchestration import do_targets, pingpong_job

    saved = []
    monkeypatch.setattr(pingpong_job, "save_job_plan", saved.append)
    monkeypatch.setattr(do_targets, "do_job_title", lambda *args, **kwargs: "Titel")
    target = SimpleNamespace(project=SimpleNamespace(slug="p"))
    for auto_extend, stored in ((False, False), (True, None)):
        job = SimpleNamespace(job_id="j", metadata={}, job_title="", tasks=[])
        do_targets.name_do_job(job, "o", "o", target, several=False, unattended=True, auto_extend=auto_extend)
        assert job.metadata.get(JOB_AUTO_EXTEND_KEY) is stored and job.metadata[JOB_UNATTENDED_KEY] is True
    assert len(saved) == 2
