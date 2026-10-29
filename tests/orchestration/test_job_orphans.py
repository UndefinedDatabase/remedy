"""F331 (operator order beweis): no job stays `running` with nothing running it."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.core.models import JobBudgets
from packages.orchestration import (
    budget_profiles,
    job_cancel,
    order_cancel,
    pingpong_job,
    serve_runs,
)
from packages.orchestration.budget_stop import job_within_caps
from packages.orchestration.job_orphans import ORPHANED_AFTER_RESTART, settle_orphaned_running_jobs
from packages.orchestration.job_stop_text import job_stop
from packages.orchestration.order_jobs import JOB_UNATTENDED_KEY

NOW = datetime(2026, 10, 29, 18, 16, tzinfo=timezone.utc)


def _job(job_id="d1a8b318952f4b04", *, unattended=True, state="running"):
    # WHY a namespace: the settling reads and writes only these fields, as a JobPlan carries them.
    return SimpleNamespace(job_id=job_id, state=pingpong_job.JOB_RUNNING if state == "running" else state,
                           metadata={JOB_UNATTENDED_KEY: unattended}, stop_reason="", stop_source="",
                           stopped_at="", pause=None, error="", tasks=[], budgets=None, budget_actuals=None)


class _Launcher:
    def __init__(self, fail=False):
        self.started, self.fail = [], fail

    def start(self, job_id):
        if self.fail:
            raise serve_runs.RunRefused("job_already_running", "refused")
        self.started.append(job_id)


@pytest.fixture
def world(monkeypatch):
    """Jobs, which of them a process still runs, cancel requests, orders and the saved records."""
    state = SimpleNamespace(jobs=[], alive=set(), cancels=set(), orders={}, order_cancels=set(), saved=[],
                            within=True)
    monkeypatch.setattr(pingpong_job, "list_job_plans_safe", lambda: (state.jobs, False, []))
    monkeypatch.setattr(pingpong_job, "save_job_plan", state.saved.append)
    monkeypatch.setattr(job_cancel, "job_cancel_request", lambda job_id: {"r": 1} if job_id in state.cancels else None)
    monkeypatch.setattr(serve_runs, "job_runner_alive", lambda paths, job_id: job_id in state.alive)
    monkeypatch.setattr(serve_runs, "settle_orphaned_job_cancels", lambda paths: [])
    monkeypatch.setattr(serve_runs, "order_record_for_job",
                        lambda paths, job_id: state.orders.get(job_id))
    monkeypatch.setattr(order_cancel, "order_cancel_request",
                        lambda folder: {"r": 1} if folder.name in state.order_cancels else None)
    monkeypatch.setattr(budget_profiles, "effective_job_budgets",
                        lambda job: None if state.within else JobBudgets(deadline=NOW - timedelta(minutes=1)))
    return state


PATHS = SimpleNamespace(orders_dir=Path("/nonexistent/orders"))


def _settle(world, launcher=None):
    return settle_orphaned_running_jobs(PATHS, launcher or _Launcher(), now=NOW)


def test_an_unattended_job_of_a_live_order_within_its_caps_is_resumed(world):
    job = _job()
    world.jobs, world.orders = [job], {job.job_id: SimpleNamespace(order_id="o1")}
    launcher = _Launcher()
    assert _settle(world, launcher) == [{"job_id": job.job_id, "action": "resumed"}]
    assert launcher.started == [job.job_id] and world.saved == []


@pytest.mark.parametrize("case, why", [
    ("attended", "it does not run unattended, so a person decides"),
    ("no_order", "its order is no longer live"),
    ("order_cancelled", "its order is no longer live"),
    ("caps", "it has reached its caps"),
    ("start_fails", "its run could not start again (RunRefused)"),
])
def test_any_other_orphaned_job_ends_stopped_with_the_reason_and_a_sentence(world, case, why):
    job = _job(unattended=case != "attended")
    world.jobs = [job]
    if case != "no_order":
        world.orders = {job.job_id: SimpleNamespace(order_id="o1")}
    if case == "order_cancelled":
        world.order_cancels = {"o1"}
    world.within = case != "caps"
    assert _settle(world, _Launcher(fail=case == "start_fails")) == [{"job_id": job.job_id, "action": "stopped"}]
    assert (job.state, job.stop_reason, world.saved) == (pingpong_job.JOB_STOPPED, ORPHANED_AFTER_RESTART, [job])
    stop = job_stop(job)
    assert stop["reason"] == ORPHANED_AFTER_RESTART
    assert stop["text"] == (f"Remedy found job {job.job_id} running with nothing left to run it after the server "
                            f"started again, and stopped it because {why}; `remedy job resume {job.job_id}` "
                            "continues it.")


def test_a_job_a_process_runs_a_cancelled_one_and_a_finished_one_are_left_alone(world):
    alive, cancelled, done = _job("alive"), _job("cancelled"), _job("done", state="completed")
    world.jobs, world.alive, world.cancels = [alive, cancelled, done], {"alive"}, {"cancelled"}
    assert _settle(world) == [] and world.saved == []


def test_a_passed_deadline_is_outside_the_caps(world):
    world.within = True
    assert job_within_caps(_job(), now=NOW)
    world.within = False
    assert not job_within_caps(_job(), now=NOW)


def test_the_supervisor_settles_orphans_when_it_starts():
    source = (Path(__file__).resolve().parents[2] / "packages/orchestration/serve_daemon.py").read_text(encoding="utf-8")
    assert "settle_orphaned_running_jobs(paths, launcher)" in source
