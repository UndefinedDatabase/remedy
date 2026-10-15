"""F042 T001, DECISION F042 D1 — a project's ledger cost of one UTC day.

The old cockpit's project list and per-project summary were deleted with the old face (amend1015f
D27); `project_cost_of_day` stays because the client digest reads it. Its four cases are pinned
here against the ledger reader it composes, never against a figure this file invents: two
registered projects, `alpha` and `beta`, each with ledger calls at FIXED times around one UTC day.
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone

import pytest

from packages.orchestration.project_cockpit import project_cost_of_day
from packages.orchestration.project_registry import register_project_repo
from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    CallRecord,
    query_cost,
    record_call,
)

NOW = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)


def _git_folder(path):
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    return path


def _call(project, call_id, ts_utc, cost_usd, basis):
    assert record_call(CallRecord(call_id=call_id, ts_utc=ts_utc, cost_usd=cost_usd, cost_basis=basis),
                       project_id=project.id)


@pytest.fixture
def world(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    alpha = register_project_repo("alpha", _git_folder(tmp_path / "alpha"))
    beta = register_project_repo("beta", _git_folder(tmp_path / "beta"))
    _call(alpha, "a-today", "2026-09-01T08:30:00+00:00", 0.25, COST_BASIS_PROVIDER_REPORTED)
    _call(alpha, "a-yesterday", "2026-08-31T23:59:59+00:00", 1.0, COST_BASIS_PROVIDER_REPORTED)
    _call(alpha, "a-tomorrow", "2026-09-02T00:00:00+00:00", 2.0, COST_BASIS_PROVIDER_REPORTED)
    _call(beta, "b-priced", "2026-09-01T09:30:00+00:00", 0.5, COST_BASIS_PROVIDER_REPORTED)
    _call(beta, "b-unpriced", "2026-09-01T09:31:00+00:00", None, COST_BASIS_UNKNOWN)
    return {"tmp": tmp_path, "alpha": alpha, "beta": beta}


class TestProjectCostOfDay:
    def test_cost_today_is_the_ledgers_utc_day_and_names_its_basis(self, world):
        alpha = project_cost_of_day(world["alpha"].id, NOW)
        assert alpha == {"day": "2026-09-01", "value_usd": 0.25, "basis": "actual", "harness_invocations": 1}
        report = query_cost(project_id=world["alpha"].id, since="2026-09-01", until="2026-09-02")
        assert (alpha["value_usd"], alpha["harness_invocations"]) == (report.total.cost_usd, report.total.calls)

    def test_an_unpriced_call_makes_cost_today_a_lower_bound(self, world):
        assert project_cost_of_day(world["beta"].id, NOW) == {
            "day": "2026-09-01", "value_usd": 0.5, "basis": "lower_bound", "harness_invocations": 2}

    def test_no_ledger_is_an_absent_cost_never_a_zero(self, world, tmp_path):
        gamma = register_project_repo("gamma", _git_folder(tmp_path / "gamma"))
        assert project_cost_of_day(gamma.id, NOW) == {
            "day": "2026-09-01", "value_usd": None, "basis": "absent", "harness_invocations": 0}

    def test_the_day_is_the_utc_day_of_the_moment_asked(self, world):
        late = datetime(2026, 9, 2, 0, 30, tzinfo=timezone.utc)
        assert project_cost_of_day(world["alpha"].id, late) == {
            "day": "2026-09-02", "value_usd": 2.0, "basis": "actual", "harness_invocations": 1}
