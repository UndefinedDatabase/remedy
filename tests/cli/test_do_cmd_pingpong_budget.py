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


class TestStartupHeaderNamesTheModel:
    """The bare `remedy do run` path says which model will answer it.

    Operator dogfooding on 2026-08-25 ran two real claude-cli jobs on this path
    and was never told which model served them: the path passes no model, so
    the `claude` CLI silently used the operator's own default. The header now
    says so. Each answer below is pinned against what the provider really does,
    so the line cannot drift into a comfortable fiction.
    """

    def test_claude_cli_reports_the_inherited_cli_default(self):
        from apps.cli.commands.do_cmd import pingpong_effective_model
        from packages.orchestration.pingpong_provider import build_claude_cli_args

        # The claim is "no --model passed", so prove the argument is absent.
        argv = build_claude_cli_args("/usr/bin/claude", "prompt", model="")
        assert "--model" not in argv

        assert pingpong_effective_model("claude-cli") == "CLI default (no --model passed)"

    def test_direct_api_reports_the_provider_s_own_default(self):
        from apps.cli.commands.do_cmd import pingpong_effective_model
        from packages.orchestration import pingpong_provider

        reported = pingpong_effective_model("claude")
        assert pingpong_provider._DEFAULT_CLAUDE_MODEL in reported

    def test_fake_reports_that_no_model_is_called(self):
        from apps.cli.commands.do_cmd import pingpong_effective_model

        assert pingpong_effective_model("fake") == "none (fake provider makes no model call)"

    def test_header_prints_a_model_line_for_each_role(self, tmp_path, monkeypatch, capsys):
        from apps.cli.commands.do_cmd import _cmd_do_pingpong

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# demo\n")

        _cmd_do_pingpong("add a docstring", repo=str(repo), max_rounds=1)
        out = capsys.readouterr().out

        assert "Builder model: none (fake provider makes no model call)" in out
        assert "Reviewer model: none (fake provider makes no model call)" in out
