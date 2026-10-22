"""F074 Acceptance — one project's calibration, read by all three consumers and the trust view.

`docs/roadmap/features/T3_F074.md` is done when a fixture ledger produces correct distributions, all
three consumers (flight-plan bands, predictive budget, cost preview) read the SAME calibration source,
and thin classes stay honestly on defaults. Here a real git repository is registered under the test's
own data root, its ledger and job records are written as a project's would be, and the calibration is
resolved ONCE through `resolve_predictive_budget_config`, the resolver every consumer calls; every
consumer then reads that one table, and `remedy stats calibration` shows the very measurement they
read. The per-module proofs live in `tests/orchestration/test_estimate_calibration.py` and
`tests/orchestration/test_estimate_calibration_consumers.py`.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from apps.cli.cost_preview_confirm import render_estimate_line
from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import BudgetCounters, predict_next_task_cost
from packages.orchestration.budget_resolution import PredictiveBudgetConfig, resolve_predictive_budget_config
from packages.orchestration.data_paths import job_record_path, resolve_data_root
from packages.orchestration.do_rehearsal import build_job_rehearsal
from packages.orchestration.estimate_calibration import calibration_snapshot_path
from packages.orchestration.pingpong_job import JobPlan, TaskEntry
from packages.orchestration.scope_fences import FenceSpec
from packages.orchestration.subtree_rerun import subtree_rerun_cost_estimate
from packages.orchestration.token_economy import TokenBand
from packages.orchestration.token_ledger import CallRecord, record_call

RECENT = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
FAT, THIN = "standard_build", "format"


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from packages.orchestration.project_registry import register_project_repo

    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "remedy.toml").write_text("[remedy.budget]\nprice_basis_usd_per_1k_tokens = 0.01\n", encoding="utf-8")
    return register_project_repo("Acceptance", repo)


def _seed(project) -> None:
    root = resolve_data_root()
    for task_class, count in ((FAT, 20), (THIN, 3)):
        for k in range(1, count + 1):
            job = f"jobacc{task_class}{k:02d}"
            path = job_record_path(job, root)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"tasks": [{"task_id": "T001", "task_class": task_class}]}), encoding="utf-8")
            for role, tokens in (("builder", k * 1000), ("reviewer", 500)):
                assert record_call(CallRecord(
                    call_id=f"{job}:T001:{role}", job_id=job, task_id="T001", role=role, ts_utc=RECENT,
                    tokens_in=tokens - 100, tokens_out=100), project_id=str(project.id))


def _job(repo: str) -> JobPlan:
    def task(task_id: str, task_class: str) -> TaskEntry:
        plan = {"planned_id": task_id, "title": task_id, "depends_on": [], "est_tokens_band": "M",
                "files_hint": []}
        return TaskEntry(task_id=task_id, title=f"Task {task_id}", task_class=task_class, inputs={"plan": plan})

    return JobPlan(job_id="job-acceptance", repo_path=repo, tasks=[task("T001", FAT), task("T002", THIN)])


def _read_all_three(config: PredictiveBudgetConfig, job: JobPlan) -> tuple[dict, list, str, str]:
    rehearsal = build_job_rehearsal(job, trace_entries=[], dod=None, predictive_config=config,
                                    fence_spec=FenceSpec(), fence_error="", repo_head="0" * 40, rehearsed_at=RECENT)
    predictions = [predict_next_task_cost(JobBudgets(max_cost_usd=1.0), BudgetCounters(), band=TokenBand.LOW,
                                          config=config, task_class=task_class).estimate_basis
                   for task_class in (FAT, THIN)]
    preview_fat = render_estimate_line(subtree_rerun_cost_estimate(job, ["T001"], config=config))
    preview_thin = render_estimate_line(subtree_rerun_cost_estimate(job, ["T002"], config=config))
    return rehearsal, predictions, preview_fat, preview_thin


def _stats_json(project, capsys) -> dict:
    from apps.cli.grouped import main

    try:
        main(["stats", "calibration", "--project", project.slug, "--json"])
    except SystemExit as exc:
        assert not exc.code, exc.code
    return json.loads(capsys.readouterr().out)


def test_all_three_consumers_read_one_calibration_and_the_thin_class_stays_on_its_default(project, capsys):
    _seed(project)
    repo = project.canonical_repo_path
    config = resolve_predictive_budget_config(project_root=repo)
    table = config.calibration
    assert table is not None and table.project_id == str(project.id)
    rehearsal, predictions, preview_fat, preview_thin = _read_all_three(config, _job(repo))

    # The fat class: every consumer wears the one table's label, with the one table's sample count.
    label = f"calibrated({table.calibrated_tokens(FAT).n})"
    assert label == "calibrated(20)"
    fat_row, thin_row = rehearsal["tasks"]
    assert fat_row["basis"].startswith(label + " ")
    assert predictions[0] == label
    assert f"T001 {label}" in preview_fat

    # The thin class: every consumer reads exactly what it reads with no calibration at all.
    plain = PredictiveBudgetConfig(price_basis_usd_per_1k_tokens=0.01)
    plain_rehearsal, plain_predictions, _plain_fat, plain_preview_thin = _read_all_three(plain, _job(repo))
    assert thin_row == plain_rehearsal["tasks"][1]
    assert predictions[1] == plain_predictions[1] == "class_default"
    assert preview_thin == plain_preview_thin

    # The trust view shows the very measurement the consumers read: the same saved snapshot.
    view = _stats_json(project, capsys)
    assert view["updated_at"] == table.updated_at
    assert view["calibrated_classes"] == [FAT]
    assert json.loads(calibration_snapshot_path(str(project.id)).read_text(encoding="utf-8"))["updated_at"] == (
        table.updated_at)


def test_a_project_with_no_ledger_keeps_every_estimate_on_its_default(project, capsys):
    repo = project.canonical_repo_path
    config = resolve_predictive_budget_config(project_root=repo)
    assert config.calibration is not None and not config.calibration.ledger_present
    plain = PredictiveBudgetConfig(price_basis_usd_per_1k_tokens=0.01)
    assert _read_all_three(config, _job(repo)) == _read_all_three(plain, _job(repo))
    view = _stats_json(project, capsys)
    assert (view["ledger_present"], view["calibrated_classes"], view["entries"]) == (False, [], [])
