"""F133 T003 — `remedy stats trust`, the model trust view.

A real git repository is registered under the test's own data root, its cost ledger, job records
and provider evidence are written as a project's would be, and the command runs as a user runs it,
through the grouped CLI.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from apps.cli.command_catalog import get_command
from apps.cli.commands import collect_all_handlers
from packages.orchestration.data_paths import job_evidence_dir, job_record_path, resolve_data_root
from packages.orchestration.model_trust_score import model_trust_snapshot_path
from packages.orchestration.token_ledger import CallRecord, record_call

RECENT = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
OLD = (datetime.now(timezone.utc) - timedelta(days=100)).isoformat()


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return code or 0, capsys.readouterr().out


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from packages.orchestration.project_registry import register_project_repo

    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    repo = tmp_path / "trusted"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return register_project_repo("Trusted", repo)


def _task(project, job: str, task: str, *, status: str, repair_rounds: int, role: str, model: str,
          cost: float | None, ts: str = RECENT, seq: int = 1, is_parse_retry: bool = False) -> None:
    root = resolve_data_root()
    path = job_record_path(job, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"tasks": [
        {"task_id": task, "status": status, "repair_rounds_used": repair_rounds}]}), encoding="utf-8")
    ev_dir = job_evidence_dir(job, root) / "task_runs" / task
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "provider_evidence.json").write_text(json.dumps({"provider_attempts": [
        {"seq": seq, "round": 1, "role": role, "model": model, "is_parse_retry": is_parse_retry}]}),
        encoding="utf-8")
    assert record_call(CallRecord(
        call_id=f"{job}:{task}:{seq}", job_id=job, task_id=task, role=role, model=None, ts_utc=ts,
        tokens_in=100, tokens_out=10, cost_usd=cost,
        cost_basis="unknown" if cost is None else "provider_reported"), project_id=str(project.id))


def _seed(project) -> None:
    for k in range(1, 21):
        _task(project, f"jobstrong{k:02d}", "T001", status="passed", repair_rounds=0, role="builder",
              model="claude-strong-v1", cost=0.02)
    for k in range(1, 4):
        _task(project, f"jobthin{k:02d}", "T001", status="passed", repair_rounds=1, role="builder",
              model="claude-thin-v1", cost=0.01)


def test_the_command_is_catalogued_read_only_and_handled():
    entry = get_command("stats.trust")
    assert entry.action_class == "read_only" and entry.supports_json
    assert "stats.trust" in collect_all_handlers()


def test_the_text_shows_each_row_with_its_columns_dashes_and_thin_marker(project, capsys):
    _seed(project)
    code, out = _run(["stats", "trust", "--project", project.slug], capsys)
    assert code == 0, out
    lines = out.splitlines()
    assert lines[0] == (f"Model trust of project {project.id}, measured from its cost ledger, job "
                        "records and provider evidence")
    assert lines[1].startswith("Window: the last 90 days, tasks whose latest call is at or after ")
    assert lines[1].endswith("Floor: 20 settled tasks per model and role.")
    assert lines[2].startswith("Measured at ")
    header = lines[3].split()
    assert header == ["role", "model", "tasks", "pass", "quota", "repair/task", "format", "err",
                      "cost/pass", "Δ", "pass", "quota"]
    rows = lines[4:6]
    joined = "\n".join(rows)
    assert "claude-strong-v1" in joined and "claude-thin-v1" in joined
    assert "3/20 thin" in joined  # the thin model's 3 settled tasks against the floor of 20
    strong_row = next(r for r in rows if "claude-strong-v1" in r)
    assert "20" in strong_row and "thin" not in strong_row
    assert "new" in joined
    assert lines[-2] == "Unattributed calls: 0. Unsettled tasks: 0."
    # `claude-strong-v1` (20 settled tasks) is the only non-thin, eligible row; `claude-thin-v1`'s
    # 3 settled tasks are below the floor, so there are fewer than two eligible rows to compare.
    assert lines[-1] == ("No recommendation for builder: fewer than two models have 20 settled "
                         "tasks in the last 90 days.")


def test_the_json_carries_the_table_the_prior_table_and_the_changes(project, capsys):
    _seed(project)
    code, out = _run(["stats", "trust", "--project", project.slug, "--json"], capsys)
    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] is True and body["version"] == 1
    assert {"table", "prior", "changes"} <= body.keys()
    assert body["table"]["project_id"] == str(project.id)
    assert body["prior"]["project_id"] == str(project.id)
    models = {row["model"] for row in body["table"]["rows"]}
    assert {"claude-strong-v1", "claude-thin-v1"} <= models
    changes = {c["model"]: c for c in body["changes"]}
    assert changes["claude-strong-v1"]["new"] is True
    assert changes["claude-strong-v1"]["pass_quota_change"] is None


def test_role_keeps_only_that_roles_rows(project, capsys):
    _seed(project)
    _task(project, "jobreviewer01", "T001", status="passed", repair_rounds=0, role="reviewer",
          model="claude-reviewer-v1", cost=0.01)
    code, out = _run(["stats", "trust", "--project", project.slug, "--role", "reviewer", "--json"], capsys)
    assert code == 0, out
    body = json.loads(out)
    assert {row["role"] for row in body["table"]["rows"]} == {"reviewer"}
    assert {c["role"] for c in body["changes"]} == {"reviewer"}


def test_role_keeps_only_that_roles_rows_in_the_text_view(project, capsys):
    """R-1429 survivor (6): `--role` must filter the TEXT view too, not only `--json`."""
    _seed(project)
    _task(project, "jobreviewer02", "T001", status="passed", repair_rounds=0, role="reviewer",
          model="claude-reviewer-v1", cost=0.01)
    code, out = _run(["stats", "trust", "--project", project.slug, "--role", "reviewer"], capsys)
    assert code == 0, out
    assert "claude-reviewer-v1" in out
    assert "claude-strong-v1" not in out
    assert "claude-thin-v1" not in out


def test_the_prior_window_shows_the_change_and_new_for_an_absent_row(project, capsys):
    window_days = 90
    now = datetime.now(timezone.utc)
    prior_ts = (now - timedelta(days=window_days + 10)).isoformat()
    # A model present in BOTH the current and the prior window: its pass quota changes.
    _task(project, "jobprior01", "T001", status="passed", repair_rounds=0, role="builder",
          model="claude-both-v1", cost=0.01, ts=prior_ts)
    _task(project, "jobnow01", "T001", status="failed", repair_rounds=0, role="builder",
          model="claude-both-v1", cost=0.01)
    # A model present only now: "new".
    _task(project, "jobnew01", "T001", status="passed", repair_rounds=0, role="builder",
          model="claude-only-now-v1", cost=0.01)
    code, out = _run(["stats", "trust", "--project", project.slug, "--json"], capsys)
    assert code == 0, out
    body = json.loads(out)
    changes = {c["model"]: c for c in body["changes"]}
    assert changes["claude-only-now-v1"]["new"] is True
    assert changes["claude-both-v1"]["new"] is False
    assert changes["claude-both-v1"]["pass_quota_change"] == pytest.approx(0.0 - 1.0)


def test_a_project_with_no_ledger_says_so(project, capsys):
    code, out = _run(["stats", "trust", "--project", project.slug], capsys)
    assert code == 0, out
    assert out.splitlines()[1] == "This project has no cost ledger yet, so no model has a trust row."
    assert not model_trust_snapshot_path(str(project.id)).exists()


def test_no_project_is_refused(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    monkeypatch.chdir(tmp_path)
    code, out = _run(["stats", "trust", "--json"], capsys)
    assert code == 1
    assert json.loads(out)["error"] == "no_project"


def test_a_malformed_setting_is_refused_as_a_usage_error(project, capsys):
    Path(project.canonical_repo_path, "remedy.toml").write_text(
        "[remedy.model_routing]\ntrust_sample_floor = -4\n", encoding="utf-8")
    code, out = _run(["stats", "trust", "--project", project.slug, "--json"], capsys)
    assert code == 2
    assert json.loads(out)["error"] == "invalid_trust_setting"


def _row(*, pass_quota_value, pass_quota_n=10, cost_value=0.01, cost_basis="provider_reported",
         cost_n=10, role="builder", model="m"):
    from packages.orchestration.model_trust_score import ModelTrustRow, TrustMetric

    return ModelTrustRow(
        role=role, model=model, pass_quota=TrustMetric(value=pass_quota_value, n=pass_quota_n),
        repair_need=TrustMetric(value=0.0, n=pass_quota_n),
        format_error_rate=TrustMetric(value=0.0, n=pass_quota_n),
        cost_per_pass=TrustMetric(value=cost_value, n=cost_n), cost_basis=cost_basis,
        settled_tasks=pass_quota_n, thin=False)


def _table(*rows):
    from packages.orchestration.model_trust_score import ModelTrustTable

    return ModelTrustTable(
        project_id="p", updated_at="2026-01-01T00:00:00+00:00", window_days=90, sample_floor=20,
        window_start="2025-10-03T00:00:00+00:00", ledger_present=True, rows=rows,
        unattributed_calls=0, unsettled_tasks=0)


def test_a_row_with_no_settled_task_prints_a_dash_never_0_percent_for_its_pass_quota():
    """R-1429 survivor (5): a missing pass quota prints a dash, never `0%`."""
    from apps.cli.commands.stats_trust_cmd import DASH, trust_rows

    row = _row(pass_quota_value=None, pass_quota_n=0, cost_value=None, cost_n=0,
               cost_basis="unknown")
    rendered = trust_rows(_table(row), _table())
    assert rendered[0][3] == DASH
    assert "0%" not in rendered[0][3]


def test_the_cost_cell_names_its_passes():
    """R-1431: the cost cell names the passes its figure rests on."""
    from apps.cli.commands.stats_trust_cmd import _format_cost

    row = _row(pass_quota_value=1.0, pass_quota_n=15, cost_value=0.0123,
                cost_basis="provider_reported", cost_n=15)
    assert _format_cost(row) == "$0.0123 (provider_reported, 15 passes)"


def test_a_falling_pass_quota_prints_a_minus_sign_and_a_rising_one_a_plus_sign():
    """R-1429 survivor (7): the change against the prior window keeps its sign."""
    from apps.cli.commands.stats_trust_cmd import _format_change

    falling = _format_change(_row(pass_quota_value=0.5), _table(_row(pass_quota_value=0.8)))
    rising = _format_change(_row(pass_quota_value=0.8), _table(_row(pass_quota_value=0.5)))
    assert falling.startswith("-") and falling.endswith("pp")
    assert rising.startswith("+") and rising.endswith("pp")


def test_the_leader_wording_is_the_whole_line():
    """DECISION F133 D3 (1), wording 1, asserted whole — not a fragment."""
    from apps.cli.commands.stats_trust_cmd import _format_recommendation
    from packages.orchestration.model_trust_score import TRUST_RECOMMENDATION_LEADER, TrustRecommendation

    rec = TrustRecommendation(
        role="builder", leader="claude-strong-v1", leader_pass_quota=0.90, leader_settled_tasks=25,
        runner_up="claude-weak-v1", runner_up_pass_quota=0.70, reason=TRUST_RECOMMENDATION_LEADER)
    assert _format_recommendation(rec, window_days=90, sample_floor=20) == (
        "Recommendation for builder: consider routing it to claude-strong-v1, whose pass quota is "
        "90% over 25 settled tasks against 70% for claude-weak-v1, in the last 90 days. Adopt it "
        "through config and an ADR, as the promotion rule of docs/agents/model_routing_policy.md "
        "requires; trust never changes a route by itself.")


def test_the_too_few_eligible_wording_is_the_whole_line():
    """DECISION F133 D3 (1), wording 2, asserted whole — not a fragment."""
    from apps.cli.commands.stats_trust_cmd import _format_recommendation
    from packages.orchestration.model_trust_score import (
        TRUST_RECOMMENDATION_TOO_FEW_ELIGIBLE,
        TrustRecommendation,
    )

    rec = TrustRecommendation(
        role="reviewer", leader=None, leader_pass_quota=None, leader_settled_tasks=None,
        runner_up=None, runner_up_pass_quota=None, reason=TRUST_RECOMMENDATION_TOO_FEW_ELIGIBLE)
    assert _format_recommendation(rec, window_days=90, sample_floor=20) == (
        "No recommendation for reviewer: fewer than two models have 20 settled tasks in the last "
        "90 days.")


def test_the_no_margin_wording_is_the_whole_line():
    """DECISION F133 D3 (1), wording 3, asserted whole — not a fragment."""
    from apps.cli.commands.stats_trust_cmd import _format_recommendation
    from packages.orchestration.model_trust_score import TRUST_RECOMMENDATION_NO_MARGIN, TrustRecommendation

    rec = TrustRecommendation(
        role="builder", leader=None, leader_pass_quota=None, leader_settled_tasks=None,
        runner_up=None, runner_up_pass_quota=None, reason=TRUST_RECOMMENDATION_NO_MARGIN)
    assert _format_recommendation(rec, window_days=90, sample_floor=20) == (
        "No recommendation for builder: no model leads the next by 10 points in the last 90 days.")


def test_role_filter_keeps_only_that_roles_recommendation_in_the_text_view():
    """R-1433 survivor (3): `--role` must keep the TEXT view's recommendation line to one role,
    not every role the matrix has an eligible leader for."""
    from apps.cli.commands.stats_trust_cmd import render_trust_text

    builder_a = _row(pass_quota_value=0.9, role="builder", model="builder-leader")
    builder_b = _row(pass_quota_value=0.5, role="builder", model="builder-runner")
    reviewer_a = _row(pass_quota_value=0.9, role="reviewer", model="reviewer-leader")
    reviewer_b = _row(pass_quota_value=0.5, role="reviewer", model="reviewer-runner")
    table = _table(builder_a, builder_b, reviewer_a, reviewer_b)
    text = render_trust_text(table, _table(), max_age_seconds=3600,
                             now=datetime(2026, 1, 2, tzinfo=timezone.utc), role="builder")
    assert "Recommendation for builder" in text
    assert "for reviewer" not in text


def test_the_json_carries_the_recommendation_per_role(project, capsys):
    """DECISION F133 D3 (1): the JSON's `recommendations` names the leader and the runner-up."""
    _seed(project)
    for k in range(1, 11):
        _task(project, f"jobweakpass{k:02d}", "T001", status="passed", repair_rounds=0,
              role="builder", model="claude-weak-v1", cost=0.015)
    for k in range(1, 11):
        _task(project, f"jobweakfail{k:02d}", "T001", status="failed", repair_rounds=0,
              role="builder", model="claude-weak-v1", cost=0.015)
    code, out = _run(["stats", "trust", "--project", project.slug, "--json"], capsys)
    assert code == 0, out
    body = json.loads(out)
    recs = {r["role"]: r for r in body["recommendations"]}
    assert recs.keys() == {"builder"}
    rec = recs["builder"]
    assert rec["reason"] == "leader"
    assert rec["leader"] == "claude-strong-v1" and rec["runner_up"] == "claude-weak-v1"
    assert rec["leader_pass_quota"] == pytest.approx(1.0)
    assert rec["runner_up_pass_quota"] == pytest.approx(0.5)
    assert rec["leader_settled_tasks"] == 20
