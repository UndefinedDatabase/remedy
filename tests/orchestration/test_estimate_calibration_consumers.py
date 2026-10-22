"""F074 T002 — the three consumers of the shared estimator read the SAME calibration.

The feature's orchestrator brief names them and asks one seam test each, proving that the label
flip is the whole integration: the flight-plan bands (a rehearsal's per-task rows and its whole-job
sum), the predictive stop arithmetic (`predict_next_task_cost`, behind `run_job`'s safe point and
`remedy job budget`), and the cost-preview line of a subtree rerun. Each shows `calibrated(n)` on the
fat class and the class default on the thin one, and a thin class reads byte for byte what it read
with no calibration at all.

Where a test goes through `resolve_predictive_budget_config`, only the project registry's resolver
is stubbed — the seam `test_predictive_budget.py` stubs for the ledger, for the same reason: the
production resolver needs a registered git repository. Everything downstream is production code.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from apps.cli.cost_preview_confirm import render_estimate_line
from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import BudgetCounters, predict_next_task_cost
from packages.orchestration.budget_resolution import PredictiveBudgetConfig, resolve_predictive_budget_config
from packages.orchestration.data_paths import job_record_path, resolve_data_root
from packages.orchestration.do_rehearsal import build_job_rehearsal
from packages.orchestration.estimate_calibration import CalibrationTable, build_calibration_table
from packages.orchestration.pingpong_job import JobPlan, TaskEntry
from packages.orchestration.pingpong_provider_fake import FakeProvider
from packages.orchestration.scope_fences import FenceSpec
from packages.orchestration.subtree_rerun import subtree_rerun_cost_estimate
from packages.orchestration.token_economy import TokenBand
from packages.orchestration.token_ledger import CallRecord, record_call, token_ledger_path_for

PROJECT = "22222222-3333-4444-5555-666666666666"
# A day ago, so the rows stay inside every window the tests read through the real clock.
RECENT = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
FAT, THIN = "standard_build", "format"


def _seed_ledger(root: Path) -> None:
    """Twenty measured standard_build tasks (whole task k*1000+500 tokens) and three format tasks."""
    for task_class, count in ((FAT, 20), (THIN, 3)):
        for k in range(1, count + 1):
            job = f"jobseed{task_class}{k:02d}"
            path = job_record_path(job, root)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"tasks": [{"task_id": "T001", "task_class": task_class}]}),
                            encoding="utf-8")
            for role, tokens in (("builder", k * 1000), ("reviewer", 500)):
                assert record_call(CallRecord(
                    call_id=f"{job}:T001:{role}", job_id=job, task_id="T001", role=role, ts_utc=RECENT,
                    tokens_in=tokens - 100, tokens_out=100), path=token_ledger_path_for(PROJECT, root))


def _table(root: Path) -> CalibrationTable:
    _seed_ledger(root)
    return build_calibration_table(PROJECT, now=datetime.now(timezone.utc), root=root)


def _config(table: CalibrationTable | None) -> PredictiveBudgetConfig:
    return PredictiveBudgetConfig(price_basis_usd_per_1k_tokens=0.01, calibration=table)


def _registered(monkeypatch, repo: Path) -> None:
    """The registry answers PROJECT for ``repo``, as `register_project_repo` would make it."""
    from packages.orchestration import project_registry

    real = project_registry.resolve_project
    monkeypatch.setattr(project_registry, "resolve_project",
                        lambda cwd: SimpleNamespace(id=PROJECT) if Path(cwd) == repo else real(cwd))


def _banded_job(repo_path: str) -> JobPlan:
    def task(task_id: str, task_class: str) -> TaskEntry:
        plan = {"planned_id": task_id, "title": task_id, "depends_on": [], "est_tokens_band": "M",
                "files_hint": []}
        return TaskEntry(task_id=task_id, title=f"Task {task_id}", task_class=task_class, inputs={"plan": plan})

    return JobPlan(job_id="job-calibrated", repo_path=repo_path, tasks=[task("T001", FAT), task("T002", THIN)])


# ── consumer 1: the flight-plan bands ───────────────────────────────────────────


def _rehearse(job: JobPlan, config: PredictiveBudgetConfig) -> dict:
    return build_job_rehearsal(job, trace_entries=[], dod=None, predictive_config=config,
                               fence_spec=FenceSpec(), fence_error="", repo_head="0" * 40,
                               rehearsed_at=RECENT)


def test_the_plan_band_rows_flip_to_calibrated_on_the_fat_class_only(tmp_path):
    job = _banded_job(str(tmp_path))
    calibrated = _rehearse(job, _config(_table(tmp_path)))
    plain = _rehearse(job, _config(None))
    fat, thin = calibrated["tasks"]
    assert fat["basis"] == ("calibrated(20) (standard_build measured P20-P80 tokens) x "
                            "price_basis_usd_per_1k_tokens=0.01")
    # The whole task's P20 and P80 are 5900 and 16100 tokens; the band vocabulary stays M.
    assert (fat["band_usd_low"], fat["band_usd_high"]) == pytest.approx((0.059, 0.161))
    assert (fat["plan_band"], fat["token_band"]) == ("M", TokenBand.MEDIUM)
    assert thin == plain["tasks"][1]
    assert thin["basis"] == "class defaults (medium/medium token bands) x price_basis_usd_per_1k_tokens=0.01"
    assert calibrated["estimate_total"]["basis"] == (
        "sum over the 2 tasks of the subtree of calibrated class ranges for T001 calibrated(20) and class "
        "defaults per plan band for the rest x price_basis_usd_per_1k_tokens=0.01")
    assert calibrated["estimate_total"]["band_usd_low"] == pytest.approx(0.059 + 0.32)


# ── consumer 2: the predictive stop arithmetic ──────────────────────────────────


def test_the_prediction_flips_to_the_fat_class_median_and_the_thin_one_is_unchanged(tmp_path):
    table = _table(tmp_path)
    budgets = JobBudgets(max_cost_usd=0.10)

    def predict(config: PredictiveBudgetConfig, task_class: str, band: str = TokenBand.LOW):
        return predict_next_task_cost(budgets, BudgetCounters(), band=band, config=config, task_class=task_class)

    fat = predict(_config(table), FAT)
    assert (fat.estimate_basis, fat.expected_tokens) == ("calibrated(20)", 11000)
    assert fat.expected_cost_usd == pytest.approx(0.11)
    assert fat.would_breach and "basis=calibrated(20)" in fat.arithmetic
    # The band no longer decides a calibrated class: an underivable band reads the same median.
    assert predict(_config(table), FAT, band=TokenBand.UNKNOWN).expected_tokens == 11000
    thin = predict(_config(table), THIN)
    assert thin == predict(_config(None), THIN)
    assert (thin.estimate_basis, thin.expected_tokens, thin.would_breach) == ("class_default", 8000, False)


_TWO_TASK_JOB = """\
# Job: Calibrated Prediction

## Task 1
Add a helper module.

Acceptance:
- module exists

## Task 2
Add a second module.

Acceptance:
- module exists
"""


def _demo_repo(tmp_path: Path, monkeypatch) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# demo\n", encoding="utf-8")
    (repo / "remedy.toml").write_text("[remedy.budget]\nprice_basis_usd_per_1k_tokens = 0.01\n", encoding="utf-8")
    _registered(monkeypatch, repo)
    return repo


def _seed_job_cost(job_id: str, cost: float) -> None:
    assert record_call(CallRecord(call_id=f"{job_id}-seed", job_id=job_id, ts_utc=RECENT, cost_usd=cost,
                                  cost_basis="provider_reported"), project_id=PROJECT)


class _CountingProvider(FakeProvider):
    def __init__(self, **kwargs):
        super().__init__(pass_on_round=1, fail_on_round=99, **kwargs)
        self.build_calls = 0

    def build(self, prompt, **kwargs):
        self.build_calls += 1
        return super().build(prompt, **kwargs)


def test_run_job_stops_on_the_calibrated_median_where_the_default_would_run(tmp_path, monkeypatch):
    # $0.90 spent of $1.00: the LOW default's 8000 tokens ($0.08) would pass, the class's measured
    # median of 11000 ($0.11) does not, so only the calibration can stop this job before its task.
    from packages.orchestration import job_evidence
    from packages.orchestration.pingpong_job import TASK_PENDING, parse_job_file, run_job

    _seed_ledger(resolve_data_root())
    repo = _demo_repo(tmp_path, monkeypatch)
    monkeypatch.setattr(job_evidence, "_resolve_job_ledger_project_id", lambda job: PROJECT)
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    _seed_job_cost(job.job_id, 0.90)
    builder = _CountingProvider()
    done = run_job(job.job_id, builder_provider=builder, reviewer_provider=_CountingProvider(),
                   repair_rounds=0, budgets={"max_cost_usd": 1.00})
    assert done.stop_reason == "predicted_budget_exhausted:max_cost_usd"
    assert builder.build_calls == 0 and all(t.status == TASK_PENDING for t in done.tasks)
    assert done.budget_prediction["estimate_basis"] == "calibrated(20)"
    assert done.budget_prediction["expected_tokens"] == 11000


def test_remedy_job_budget_prints_the_calibrated_expectation(tmp_path, monkeypatch, capsys):
    from apps.cli.commands.job import _cmd_job_budget
    from packages.orchestration.pingpong_job import parse_job_file, save_job_plan

    _seed_ledger(resolve_data_root())
    repo = _demo_repo(tmp_path, monkeypatch)
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    job.budgets = {"max_cost_usd": 2.0}
    job.first_running_at = "2026-01-01T09:00:00+00:00"
    job.budget_actuals = {
        "schema_version": "2.0.0", "provider_call_count": 1, "actual_call_count": 1,
        "unmeasured_call_count": 0, "total_tokens": 1000, "actual_sources": ["pingpong_live"],
        "started_at": job.first_running_at, "measured_cost_usd": 0.25, "priced_call_count": 1,
        "unpriced_call_count": 0}
    save_job_plan(job)
    _cmd_job_budget(job.job_id, json_output=False)
    values = dict(line.strip().split(":", 1) for line in capsys.readouterr().out.splitlines() if ":" in line)
    assert values["estimate_basis"].strip() == "calibrated(20)"
    assert values["next_task_expected"].strip() == "$0.1100"


# ── consumer 3: the cost-preview line ───────────────────────────────────────────


def test_the_cost_preview_line_flips_to_calibrated_on_the_fat_class_only(tmp_path, monkeypatch):
    _seed_ledger(resolve_data_root())
    repo = _demo_repo(tmp_path, monkeypatch)
    config = resolve_predictive_budget_config(project_root=str(repo))
    assert isinstance(config.calibration, CalibrationTable) and config.calibration.project_id == PROJECT
    job = _banded_job(str(repo))
    fat_line = render_estimate_line(subtree_rerun_cost_estimate(job, ["T001"], config=config))
    assert fat_line == (
        "estimated $0.0590-$0.1610 (basis: sum over the 1 tasks of the subtree of calibrated class ranges "
        "for T001 calibrated(20) x price_basis_usd_per_1k_tokens=0.01)")
    thin_estimate = subtree_rerun_cost_estimate(job, ["T002"], config=config)
    plain = PredictiveBudgetConfig(price_basis_usd_per_1k_tokens=0.01)
    assert thin_estimate == subtree_rerun_cost_estimate(job, ["T002"], config=plain)
    assert render_estimate_line(thin_estimate) == (
        "estimated $0.3200-$0.3200 (basis: sum over the 1 tasks of the subtree of class defaults per plan "
        "band x price_basis_usd_per_1k_tokens=0.01)")


def test_without_a_registered_project_every_estimate_keeps_its_defaults(tmp_path):
    repo = tmp_path / "unregistered"
    repo.mkdir()
    assert resolve_predictive_budget_config(project_root=str(repo)).calibration is None
    assert resolve_predictive_budget_config().calibration is None


def test_the_calibration_settings_are_read_from_config(tmp_path, monkeypatch):
    _seed_ledger(resolve_data_root())
    repo = _demo_repo(tmp_path, monkeypatch)
    (repo / "remedy.toml").write_text(
        "[remedy.budget]\nprice_basis_usd_per_1k_tokens = 0.01\ncalibration_sample_floor = 3\n"
        "calibration_window_days = 400\n", encoding="utf-8")
    table = resolve_predictive_budget_config(project_root=str(repo)).calibration
    assert (table.sample_floor, table.window_days) == (3, 400)
    assert table.calibrated_tokens(THIN).n == 3
