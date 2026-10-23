"""F133 Acceptance — the trust home and its view, read end-to-end through the command line.

`docs/roadmap/features/T7_F133.md` is DONE when a constructed history produces a matrix with `n`
and the window on every figure, `remedy stats trust` shows that matrix and the clear leader's
recommendation naming the strong model, and the informational routing note ("trust suggests
otherwise", DECISION F133 D4) appears in `remedy job plan-show` on a contradiction fixture and
never changes the route. Every ledger row and job record here is written the way a real job's
would be, in a temporary data root, and every command runs through the grouped CLI, exactly as a
user runs it. The per-module proofs live in `tests/orchestration/test_model_trust_score.py`,
`tests/cli/test_stats_trust_cmd.py` and `tests/cli/test_job_plan_cmd.py`.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import job_evidence_dir, job_record_path, resolve_data_root
from packages.orchestration.execution_config import ExecutionConfig
from packages.orchestration.job_plan import map_task_plan_to_tasks
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables
from packages.orchestration.token_ledger import CallRecord, record_call

RECENT = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
STRONG, WEAK, THIN = "claude-strong-v1", "claude-weak-v1", "claude-thin-v1"
_PLAN_TASKS = [{"id": "T1", "title": "Build T1", "goal": "ship it", "acceptance": ["T1 works"],
                "depends_on": [], "est_tokens_band": "S", "files_hint": ["src/t1.py"]}]


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from packages.orchestration.project_registry import register_project_repo

    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return register_project_repo("F133 Acceptance", repo)


def _seed_task(project, job: str, *, status: str, model: str, cost: float) -> None:
    root = resolve_data_root()
    path = job_record_path(job, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"tasks": [
        {"task_id": "T001", "status": status, "repair_rounds_used": 0}]}), encoding="utf-8")
    ev_dir = job_evidence_dir(job, root) / "task_runs" / "T001"
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "provider_evidence.json").write_text(json.dumps({"provider_attempts": [
        {"seq": 1, "round": 1, "role": "builder", "model": model, "is_parse_retry": False}]}),
        encoding="utf-8")
    assert record_call(CallRecord(
        call_id=f"{job}:T001:1", job_id=job, task_id="T001", role="builder", model=None,
        ts_utc=RECENT, tokens_in=100, tokens_out=10, cost_usd=cost, cost_basis="provider_reported"),
        project_id=str(project.id))


def _seed(project) -> None:
    """A STRONG builder (25 passes, 100%), a WEAK one (15 pass, 5 fail — 75%), both above the
    sample floor of 20, and a THIN one (3 passes, below the floor)."""
    for k in range(1, 26):
        _seed_task(project, f"jobstrong{k:02d}", status="passed", model=STRONG, cost=0.02)
    for k in range(1, 16):
        _seed_task(project, f"jobweakpass{k:02d}", status="passed", model=WEAK, cost=0.015)
    for k in range(1, 6):
        _seed_task(project, f"jobweakfail{k:02d}", status="failed", model=WEAK, cost=0.015)
    for k in range(1, 4):
        _seed_task(project, f"jobthin{k:02d}", status="passed", model=THIN, cost=0.01)


def _cli(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return code or 0, capsys.readouterr().out


def _make_job(repo: Path, *, builder_model: str) -> str:
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _PLAN_TASKS})
    body = plan.model_dump()
    body["_approval"] = "pending"
    body["_normalization"] = []
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F133 acceptance plan", task_plan=body, tasks=mapped,
                  state=RunState.PLANNED, repo_path=str(repo),
                  execution_config=ExecutionConfig(builder_model=builder_model))
    save_job_plan(job)
    return str(job.job_id)


def test_stats_trust_names_n_and_the_window_on_every_figure_and_recommends_the_strong_model(
        project, capsys):
    _seed(project)
    code, out = _cli(["stats", "trust", "--project", project.slug], capsys)
    assert code == 0, out
    lines = out.splitlines()
    assert "Window: the last 90 days" in lines[1] and lines[1].endswith(
        "Floor: 20 settled tasks per model and role.")
    rows = lines[4:7]
    joined = "\n".join(rows)
    assert STRONG in joined and WEAK in joined and THIN in joined
    assert "3/20 thin" in joined  # the thin model's own sample size, honestly below the floor
    strong_row = next(r for r in rows if STRONG in r)
    weak_row = next(r for r in rows if WEAK in r)
    assert "25" in strong_row and "100%" in strong_row
    assert "20" in weak_row and "75%" in weak_row
    # The cost and the format-error cells each name the sample size their own figure rests on.
    assert "(provider_reported, 15 passes)" in weak_row
    assert "0% (20 calls)" in weak_row
    assert (f"Recommendation for builder: consider routing it to {STRONG}, whose pass quota is "
            f"100% over 25 settled tasks against 75% for {WEAK}, in the last 90 days. Adopt it "
            "through config and an ADR") in out

    code, out_json = _cli(["stats", "trust", "--project", project.slug, "--json"], capsys)
    assert code == 0, out_json
    body = json.loads(out_json)
    rows_by_model = {row["model"]: row for row in body["table"]["rows"]}
    assert rows_by_model[STRONG]["pass_quota"] == {"value": 1.0, "n": 25}
    assert rows_by_model[WEAK]["pass_quota"] == {"value": 0.75, "n": 20}
    assert rows_by_model[THIN]["thin"] is True and rows_by_model[THIN]["settled_tasks"] == 3
    rec = next(r for r in body["recommendations"] if r["role"] == "builder")
    assert (rec["reason"], rec["leader"], rec["runner_up"]) == ("leader", STRONG, WEAK)
    assert rec["leader_settled_tasks"] == 25


def test_job_plan_show_prints_the_note_for_the_weak_builder_and_the_job_record_is_unchanged(
        project, capsys):
    _seed(project)
    job_id = _make_job(Path(project.canonical_repo_path), builder_model=WEAK)
    record = job_record_path(job_id)
    before = record.read_bytes()
    code, out = _cli(["job", "plan-show", job_id], capsys)
    assert code == 0, out
    assert (f"Trust suggests otherwise for builder: {WEAK} is configured, with a pass quota of "
            f"75% over 20 settled tasks, while {STRONG} leads with 100% over 25 in the last 90 "
            "days. This note is informational: the route is unchanged, and a change is made "
            "through config and an ADR.") in out
    assert record.read_bytes() == before


def test_job_plan_show_prints_no_note_for_the_strong_builder(project, capsys):
    """The strong builder already leads, so the configured route and the trust leader agree."""
    _seed(project)
    job_id = _make_job(Path(project.canonical_repo_path), builder_model=STRONG)
    code, out = _cli(["job", "plan-show", job_id], capsys)
    assert code == 0, out
    assert "Trust suggests otherwise" not in out
