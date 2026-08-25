"""The budget-aware safe point of the JOB-LESS ping-pong path (`remedy do run`).

Operator dogfooding on 2026-08-25 found every budgeted `remedy do run` dying
with ``StopControlError: invalid job id ''`` before the first provider call:
the stop check asked ``safe_points.should_stop`` with a hardcoded empty job id,
and the operator-stop layer it fronts is addressed BY job id. This path mints
no job, so there was never an id to pass. The tests below pin both halves of
the repair — the crash is gone, AND the budget still stops the run.

`validate_job_id` is deliberately NOT exercised here as a weakened rule: it
still refuses an empty id, and ``tests/orchestration/test_safe_points.py``
keeps that guarantee.
"""
from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from datetime import datetime, timezone

from packages.core.models import JobBudgets


def _run_pingpong_cli(repo, *, budgets):
    """Drive the real `remedy do run` handler and return its parsed JSON report."""
    from apps.cli.commands.do_cmd import _cmd_do_pingpong

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        _cmd_do_pingpong(
            "add a docstring",
            repo=str(repo),
            builder="fake",
            reviewer="fake",
            max_rounds=1,
            json_output=True,
            budgets=budgets,
        )
    return json.loads(buffer.getvalue())


class TestBudgetedRunReachesTheProviders:
    """(a) A budgeted run on the job-less path no longer dies at safe point 1."""

    def test_budgets_set_and_the_run_completes(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# demo\n")

        report = _run_pingpong_cli(
            repo,
            budgets=JobBudgets(max_total_tokens=100_000, max_cost_usd=2.0),
        )

        # The defect stopped the run BEFORE any round existed; a completed run
        # is the proof it is gone.
        assert report["final_status"] != "stopped"
        assert report["total_rounds"] >= 1


class TestExhaustedBudgetStillStops:
    """(b) The budget remains a real stop on this path — nothing was disarmed."""

    def test_exhausted_budget_stops_the_run(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# demo\n")

        # A deadline already in the past is exhausted at the FIRST safe point,
        # which is the earliest point a budget can speak on this path. The
        # counter-based limits cannot express "already over" — the model
        # requires them to be strictly positive.
        report = _run_pingpong_cli(
            repo,
            budgets=JobBudgets(deadline=datetime(2020, 1, 1, tzinfo=timezone.utc)),
        )

        assert report["final_status"] == "stopped"
        assert report["total_rounds"] == 0
