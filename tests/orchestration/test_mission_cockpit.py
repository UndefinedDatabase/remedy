"""Tests for `packages.orchestration.mission_cockpit` (F305 T001, DECISIONS F305 D1 and D2; R-1248).

Each test sets `REMEDY_DATA_DIR` to a fresh folder and registers real projects over real git
folders, so the missions, the jobs, the registry and the ledgers are the ones the cockpit reads.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.orchestration.mission_cockpit import (
    MISSION_COCKPIT_VERSION,
    mission_orders_view,
    project_missions_view,
)
from packages.orchestration.mission_state import (
    MISSING_JOB_LABEL,
    MissionOrder,
    create_mission,
    link_job_to_mission,
)
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.project_registry import register_project_repo
from packages.orchestration.repo_mission import accept_order, accept_order_in_each, link_order_job

CHIP_KEYS = {"job_id", "project_id", "slug", "repo_name", "title", "state"}
NO_TOKENS = {"input": None, "output": None, "cache_read": None, "cache_creation": None}


def _repo(path: Path) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.email=a@b", "-c", "user.name=n",
                    "commit", "-q", "--allow-empty", "-m", "x"], check=True)
    return path


def _job(project, title: str) -> JobPlan:
    job = JobPlan(job_title=title, project_id=str(project.id), repo_path=project.canonical_repo_path)
    save_job_plan(job)
    return job


def _ledger_call(project_id, call_id: str, job_id: str, **tokens) -> None:
    from packages.orchestration.token_ledger import CallRecord, record_call

    assert record_call(CallRecord(call_id=call_id, job_id=job_id,
                                  ts_utc="2026-10-12T09:00:00+00:00", **tokens),
                       project_id=project_id)


@pytest.fixture
def world(tmp_path, monkeypatch):
    """An order over two repositories: two jobs in alpha's mission, one in beta's."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    alpha = register_project_repo("alpha", _repo(tmp_path / "alpha"))
    beta = register_project_repo("beta", _repo(tmp_path / "beta"))
    accepted = accept_order_in_each(
        [(alpha, alpha.canonical_repo_path), (beta, beta.canonical_repo_path)],
        MissionOrder(text="Add a health route\nto both services"))
    jobs = {"a1": _job(alpha, "alpha first"), "a2": _job(alpha, "alpha second"),
            "b1": _job(beta, "beta only")}
    for key, project in (("a1", alpha), ("b1", beta), ("a2", alpha)):
        mission_id, order_id = accepted[str(project.id)]
        link_order_job(str(project.id), mission_id, order_id, str(jobs[key].job_id))
    return {"alpha": alpha, "beta": beta, "accepted": accepted, "jobs": jobs}


def _orders(world, name):
    project = world[name]
    status, body = mission_orders_view(project, world["accepted"][str(project.id)][0])
    assert status == 200, body
    return body


def test_an_order_over_two_repositories_shows_three_chips_naming_two_projects(world):
    jobs = world["jobs"]
    for side in ("alpha", "beta"):
        [order] = _orders(world, side)["orders"]
        chain = order["chain"]
        assert [chip["job_id"] for chip in chain] == [
            str(jobs["a1"].job_id), str(jobs["b1"].job_id), str(jobs["a2"].job_id)]
        assert [chip["slug"] for chip in chain] == ["alpha", "beta", "alpha"]
        assert {chip["project_id"] for chip in chain} == {
            str(world["alpha"].id), str(world["beta"].id)}


def test_a_chip_carries_references_and_titles_only(world):
    [order] = _orders(world, "alpha")["orders"]
    for chip in order["chain"]:
        assert set(chip) == CHIP_KEYS
        assert "/" not in chip["repo_name"]
    beta_chip = order["chain"][1]
    assert (beta_chip["repo_name"], beta_chip["title"], beta_chip["state"]) == (
        "beta", "beta only", world["jobs"]["b1"].state.value)


def test_an_order_row_names_its_title_and_batch(world):
    body = _orders(world, "alpha")
    [order] = body["orders"]
    assert order["title"] == "Add a health route"
    assert order["job_count"] == 2
    assert order["order_id"] == world["accepted"][str(world["alpha"].id)][1]
    assert order["correlation_id"] and order["sealed"] is False
    assert (body["version"], body["slug"], body["earlier_orders"], body["degraded"]) == (
        MISSION_COCKPIT_VERSION, "alpha", 0, False)


def test_the_missions_view_has_one_card_per_repository_mission(world):
    view = project_missions_view(world["alpha"])
    [card] = view["missions"]
    assert card == {"mission_id": world["accepted"][str(world["alpha"].id)][0],
                    "goal": "Maintain alpha", "status": "active", "created_at": card["created_at"],
                    "order_count": 1, "job_count": 2}
    assert (view["version"], view["slug"], view["degraded"], view["skipped_count"]) == (
        MISSION_COCKPIT_VERSION, "alpha", False, 0)


def test_an_orders_usage_sums_the_calls_and_tokens_of_its_own_projects_jobs(world):
    jobs, alpha, beta = world["jobs"], world["alpha"], world["beta"]
    _ledger_call(alpha.id, "c1", str(jobs["a1"].job_id), tokens_in=100, tokens_out=20, cache_read=7)
    _ledger_call(alpha.id, "c2", str(jobs["a2"].job_id), tokens_in=50, tokens_out=5)
    _ledger_call(beta.id, "c3", str(jobs["b1"].job_id), tokens_in=999, tokens_out=999)
    [order] = _orders(world, "alpha")["orders"]
    assert order["usage"] == {"calls": 2, "tokens": {
        "input": 150, "output": 25, "cache_read": 7, "cache_creation": None}}
    [beta_order] = _orders(world, "beta")["orders"]
    assert beta_order["usage"]["calls"] == 1


def test_an_order_whose_jobs_made_no_recorded_call_reads_zero_calls(world):
    [order] = _orders(world, "alpha")["orders"]
    assert order["usage"] == {"calls": 0, "tokens": NO_TOKENS}


def test_an_unreadable_ledger_nulls_the_usage_and_marks_the_answer_degraded(world):
    from packages.orchestration.token_ledger import token_ledger_path_for

    ledger = token_ledger_path_for(world["alpha"].id)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_bytes(b"this is not an SQLite database, and it is long enough to be read")
    body = _orders(world, "alpha")
    assert body["degraded"] is True
    assert body["orders"][0]["usage"] == {"calls": None, "tokens": NO_TOKENS}


@pytest.mark.parametrize("mission_id", ["no-such-mission", "../escape", ""])
def test_a_mission_the_project_does_not_hold_is_404(world, mission_id):
    assert mission_orders_view(world["alpha"], mission_id) == (404, {"error": "mission not found"})


def test_another_projects_mission_is_404_under_this_project(world):
    beta_mission = world["accepted"][str(world["beta"].id)][0]
    assert mission_orders_view(world["alpha"], beta_mission) == (404, {"error": "mission not found"})


def test_only_the_newest_orders_are_answered_and_the_rest_counted(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    solo = register_project_repo("solo", _repo(tmp_path / "solo"))
    for index in range(27):
        mission, _batch = accept_order(solo, solo.canonical_repo_path, MissionOrder(text=f"order {index}"))
    status, body = mission_orders_view(solo, mission.id)
    assert status == 200
    assert [order["title"] for order in body["orders"]] == [f"order {n}" for n in range(26, 1, -1)]
    assert body["earlier_orders"] == 2


def test_a_mission_written_before_orders_keeps_each_links_project(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    lead = register_project_repo("lead", _repo(tmp_path / "lead"))
    other = register_project_repo("other", _repo(tmp_path / "other"))
    mission = create_mission(str(lead.id), "span two", project_ids=(str(lead.id), str(other.id)))
    first, second = _job(lead, "lead job"), _job(other, "other job")
    link_job_to_mission(str(lead.id), mission.id, str(first.job_id), "initial")
    link_job_to_mission(str(lead.id), mission.id, str(second.job_id), "follow_up")
    status, body = mission_orders_view(lead, mission.id)
    assert status == 200
    [row] = body["orders"]
    assert [(chip["slug"], chip["title"]) for chip in row["chain"]] == [
        ("lead", "lead job"), ("other", "other job")]
    assert row["job_count"] == 2 and row["order_id"] == ""


def test_a_job_gone_from_the_store_reads_the_missing_label(world):
    from packages.orchestration.data_paths import job_record_path

    job_record_path(str(world["jobs"]["b1"].job_id)).unlink()
    [order] = _orders(world, "alpha")["orders"]
    gone = order["chain"][1]
    assert (gone["state"], gone["title"], gone["repo_name"], gone["slug"]) == (
        MISSING_JOB_LABEL, "", "", "beta")


def test_a_link_whose_id_is_no_job_id_reads_the_missing_label(world):
    alpha = world["alpha"]
    mission_id, order_id = world["accepted"][str(alpha.id)]
    link_order_job(str(alpha.id), mission_id, order_id, "not-a-job")
    [order] = _orders(world, "alpha")["orders"]
    [stray] = [chip for chip in order["chain"] if chip["job_id"] == "not-a-job"]
    assert (stray["state"], stray["title"], stray["slug"]) == (MISSING_JOB_LABEL, "", "alpha")
