"""F324 — a job started unattended stays unattended, through run, resume, retry and continue."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.orchestration.job_burn import job_approved_unattended
from packages.orchestration.job_plan import AUTO_APPROVAL_MODE
from packages.orchestration.job_unattended import (
    ORDER_REPAIR_ROUNDS_SOURCE,
    UNATTENDED_RUN_APPROVAL_REASON,
    approve_unattended_plan,
    job_has_caps,
    job_runs_unattended,
    record_walk_job_choices,
    set_job_unattended,
)
from packages.orchestration.order_jobs import JOB_UNATTENDED_KEY


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _bare_job(**metadata):
    return SimpleNamespace(metadata=dict(metadata), repair_rounds_allowed=2, repair_rounds_source="default",
                           budgets=None, task_plan=None)


def test_a_walk_stores_its_unattended_choice_and_its_repair_rounds_on_the_job() -> None:
    job = _bare_job()
    record_walk_job_choices(job, unattended=True, repair_rounds=4)
    assert job.metadata[JOB_UNATTENDED_KEY] is True and job_runs_unattended(job) is True
    assert (job.repair_rounds_allowed, job.repair_rounds_source) == (4, ORDER_REPAIR_ROUNDS_SOURCE)
    attended = _bare_job()
    record_walk_job_choices(attended, unattended=False, repair_rounds=None)
    assert job_runs_unattended(attended) is None
    assert (attended.repair_rounds_allowed, attended.repair_rounds_source) == (2, "default")


def test_a_run_switches_the_stored_choice_only_when_it_names_one() -> None:
    job = _bare_job(**{JOB_UNATTENDED_KEY: True})
    assert set_job_unattended(job, None) is False and job_runs_unattended(job) is True
    assert set_job_unattended(job, True) is False
    assert set_job_unattended(job, False) is True and job_runs_unattended(job) is False


def test_the_stored_choice_wins_over_the_plans_audit() -> None:
    audited = {"_approval_audit": {"mode": AUTO_APPROVAL_MODE}}
    assert job_approved_unattended(SimpleNamespace(metadata={}, task_plan=audited)) is True
    assert job_approved_unattended(SimpleNamespace(metadata={JOB_UNATTENDED_KEY: False}, task_plan=audited)) is False
    assert job_approved_unattended(SimpleNamespace(metadata={JOB_UNATTENDED_KEY: True}, task_plan={})) is True


def _saved_job(tmp_path: Path, approval: str, unattended: bool | None):
    from packages.orchestration.pingpong_job import parse_job_file, save_job_plan

    repo = tmp_path / "repo"
    repo.mkdir(exist_ok=True)
    job = parse_job_file("# Job: Demo\n\n## Task 1\nFix README.\n\nAcceptance:\n- fixed\n", str(repo))
    job.task_plan = {"tasks": [{"title": "Fix README"}], "_approval": approval}
    if unattended is not None:
        job.metadata[JOB_UNATTENDED_KEY] = unattended
    save_job_plan(job)
    return job


def test_an_unattended_job_approves_the_plan_it_waits_on(tmp_path: Path) -> None:
    # The night of 2026-10-28: a retry over HTTP of a job its order had started unattended
    # stopped again at the plan approval and waited for a person.
    from packages.orchestration.job_plan import task_plan_blocks_execution
    from packages.orchestration.pingpong_job import load_job_plan

    job = _saved_job(tmp_path, "pending", True)
    assert approve_unattended_plan(job) is True
    loaded = load_job_plan(str(job.job_id))
    assert loaded is not None and task_plan_blocks_execution(loaded) is None
    assert loaded.task_plan["_approval_audit"] == {"mode": AUTO_APPROVAL_MODE,
                                                   "reason": UNATTENDED_RUN_APPROVAL_REASON}
    assert approve_unattended_plan(loaded) is False    # nothing left to approve


def test_an_asking_or_rejected_job_is_never_approved_by_its_run(tmp_path: Path) -> None:
    assert approve_unattended_plan(_saved_job(tmp_path, "pending", None)) is False
    assert approve_unattended_plan(_saved_job(tmp_path, "pending", False)) is False
    assert approve_unattended_plan(_saved_job(tmp_path, "rejected", True)) is False


def test_job_caps_are_the_jobs_own_limits() -> None:
    assert job_has_caps(SimpleNamespace(budgets=None)) is False
    assert job_has_caps(SimpleNamespace(budgets={"max_total_tokens": None})) is False
    assert job_has_caps(SimpleNamespace(budgets={"max_cost_usd": 1.5})) is True


def test_job_run_takes_unattended_or_no_unattended_and_do_takes_repair_rounds() -> None:
    from apps.cli.grouped import build_parser

    parser = build_parser()
    assert parser.parse_args(["job", "run", "j1"]).unattended is None
    assert parser.parse_args(["job", "run", "j1", "--unattended"]).unattended is True
    assert parser.parse_args(["job", "run", "j1", "--no-unattended"]).unattended is False
    with pytest.raises(SystemExit):
        parser.parse_args(["job", "run", "j1", "--unattended", "--no-unattended"])
    assert parser.parse_args(["do", "run", "--repair-rounds", "3", "--", "order.md"]).repair_rounds == 3
