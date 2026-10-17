"""Audit P1-4: one budget authority for a whole order, and every planning call on its ledger.

Fake planner at the provider seam, fake builder and reviewer, the data root under `tmp_path`.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from apps.cli.grouped import main
from tests.orchestration.scale_harness import FakePlannerService, commit_repository

ROLES = ("--builder-provider", "fake", "--reviewer-provider", "fake")
BROAD_ORDER = "Improve error handling everywhere in the project."


@pytest.fixture
def planner(monkeypatch, tmp_path) -> FakePlannerService:
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    return FakePlannerService(target="src/app.py").install(monkeypatch)


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    target = commit_repository(tmp_path / "work", {
        "src/app.py": "x = 1\n", "src/util.py": "y = 2\n", "tests/test_app.py": "def test_a():\n    pass\n",
        "README.md": "# w\n", "pkg/a.py": "a = 1\n", "pkg/b.py": "b = 1\n", "pkg/c.py": "c = 1\n",
        "pkg/d.py": "d = 1\n", "pkg/e.py": "e = 1\n", "pkg/f.py": "f = 1\n", "pkg/g.py": "g = 1\n"})
    monkeypatch.chdir(target)
    return target


def _do(capsys, order: str, *extra: str) -> dict:
    try:
        main(["do", order, "--repo", ".", *ROLES, "--json", "--no-ui", *extra])
    except SystemExit:
        pass
    return json.loads(capsys.readouterr().out)


def _step(data: dict, name: str) -> dict:
    return next(s for s in data["steps"] if s["name"] == name)


def test_every_planner_call_of_a_full_walk_is_on_the_orders_ledger(repo, planner, capsys):
    data = _do(capsys, BROAD_ORDER, "--plan-only", "--run-unattended")

    ledger = data["order_budget"]
    assert ledger["planner_calls"] == planner.count() > 0
    assert ledger["planner_calls_by_reason"] == {
        {"JobIntake": "intake", "TaskPlan": "task_plan", "MissionPlanDraft": "mission_plan",
         "StudyCategoryNarration": "study_narration"}[schema]: n
        for schema, n in planner.by_schema().items()}
    for entry in ledger["calls"]:
        assert entry["role"] == "planner" and entry["outcome"] == "ok" and entry["attempt"] in (0, 1)
        assert entry["tokens_estimated"] is True and entry["seconds"] >= 0


def test_a_bounded_walk_makes_no_planner_call_and_the_ledger_says_so(repo, planner, capsys):
    data = _do(capsys, "Fix the typo in README.md", "--plan-only")

    assert planner.count() == 0
    assert data["order_budget"]["planner_calls"] == 0 and data["order_budget"]["calls"] == []


def test_planning_calls_beyond_the_orders_call_cap_are_refused_and_the_walk_fails_honestly(
        repo, planner, capsys):
    data = _do(capsys, BROAD_ORDER, "--plan-only", "--max-provider-calls", "2")

    ledger = data["order_budget"]
    assert ledger["planner_calls"] == 2 == planner.count()
    assert ledger["refused_calls"] >= 1
    assert any(e["outcome"].startswith("refused") for e in ledger["calls"])
    shape = _step(data, "shape")
    assert shape["status"] == "failed" and "cap of 2 provider calls is spent" in shape["detail"]
    assert data["job_ids"] == []


def test_the_second_job_of_a_chain_gets_what_the_first_left_not_the_whole_cap(
        repo, planner, capsys, monkeypatch):
    from packages.orchestration.order_ledger import OrderCallLedger
    from packages.orchestration.pingpong_job import load_job_plan

    # The fake builder and reviewer report no provider calls; give the first job a measured spend.
    monkeypatch.setattr(OrderCallLedger, "record_job", lambda self, job: self.jobs.__setitem__(
        str(job.job_id), {"calls": 7, "tokens": 0, "cost_usd": None, "measured": True}))

    data = _do(capsys, "Write docs/alpha.md and docs/beta.md", "--no-llm", "--force-mission",
               "--commit-auto", "--max-provider-calls", "40")

    first, second = data["job_ids"]
    caps = [load_job_plan(j).budgets["max_provider_calls"] for j in (first, second)]
    assert caps == [40, 33]


def test_a_provider_failure_is_recorded_per_attempt_and_stops_honestly_without_unbounded_retries(
        repo, monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    failing = FakePlannerService(error=TimeoutError("planner timed out")).install(monkeypatch)

    data = _do(capsys, BROAD_ORDER, "--plan-only")

    ledger = data["order_budget"]
    # two failures in a row end planner use: the study asks twice, nothing after it is asked at all
    assert failing.count() == ledger["planner_calls"] == 2
    assert [e["outcome"] for e in ledger["calls"][:2]] == ["error: TimeoutError"] * 2
    assert all(e["outcome"].startswith("refused: the planner failed 2 calls in a row")
               for e in ledger["calls"][2:])
    shape = _step(data, "shape")      # a failed task plan is a failed shape, never a silent substitute
    assert shape["status"] == "failed" and "failed 2 calls in a row" in shape["detail"]


def test_without_a_cap_the_ledger_records_and_limits_nothing(repo, planner, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    data = _do(capsys, "Write docs/alpha.md and docs/beta.md", "--no-llm", "--force-mission",
               "--commit-auto")

    assert data["order_budget"]["caps"] is None
    assert all(not (load_job_plan(j).budgets or {}).get("max_provider_calls") for j in data["job_ids"])


def test_a_job_the_walk_leaves_waiting_keeps_the_orders_leftover_for_its_later_run(
        repo, planner, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    data = _do(capsys, "Write docs/alpha.md and docs/beta.md", "--no-llm", "--force-mission",
               "--max-provider-calls", "40")

    first, second = data["job_ids"]
    assert data["waiting_job_ids"] == [second]
    assert load_job_plan(second).budgets["max_provider_calls"] == 40
