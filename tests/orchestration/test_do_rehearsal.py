"""F055 R2 T002 — the rehearsal's own record and its readable summary (DECISION F055 D2).

`build_job_rehearsal` and `render_rehearsal_summary` are PURE, so this file exercises their
shape directly against a `JobPlan` built in the test, and proves the golden summary byte for
byte. `write_job_rehearsal` is proven once, end to end, through a real job evidence folder
(R-1316's neighbour: a rehearsal's own guarantees need an instrument that actually writes).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.do_rehearsal import (
    build_job_rehearsal,
    job_waits_after_rehearsal,
    rehearsal_staleness_warning,
    render_rehearsal_summary,
    write_job_rehearsal,
)
from packages.orchestration.dod_schema import DoD, DoDCheck
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan
from packages.orchestration.scope_fences import FenceSpec

GOLDEN = Path(__file__).resolve().parent / "fixtures" / "rehearsal" / "golden" / "rehearsal.md"

REPO_HEAD = "deadbeefcafef00dfacade0123456789abcdef0"
REHEARSED_AT = "2026-10-14T00:00:00+00:00"


def _two_task_job(repo_path: str = "/tmp/rehearsal-fixture") -> JobPlan:
    """One task with a priced plan band and a fence conflict, one with no band — a task plan
    of one risk and one normalization entry."""
    priced = TaskEntry(
        task_id="T001", title="Write the thing",
        inputs={"plan": {"planned_id": "T001", "title": "Write the thing", "depends_on": [],
                          "est_tokens_band": "M", "files_hint": []}},
        files_hint=["src/app.py", ".git/config"])
    unpriced = TaskEntry(task_id="T002", title="Polish it", inputs={}, files_hint=[])
    return JobPlan(
        job_id="job-rehearsal-fixture", repo_path=repo_path, tasks=[priced, unpriced],
        task_plan={
            "risks": ["the fixture might drift"],
            "_normalization": [{"kind": "merge", "source_ids": ["T001", "T002"],
                                 "result_ids": ["T001"], "reason": "too small to split"}],
        })


def _two_checks_dod() -> DoD:
    """One compiled, blocking check and one standard, non-blocking one."""
    return DoD(schema_v="dod_v1", compiled=True, origin="provider", checks=[
        DoDCheck(id="tests-pass", kind="custom_cmd", spec={"argv": ["true"]}, blocking=True,
                 source="compiled"),
        DoDCheck(id="lint-clean", kind="custom_cmd", spec={"argv": ["true"]}, blocking=False,
                 source="standard"),
    ])


def _priced_config() -> PredictiveBudgetConfig:
    return PredictiveBudgetConfig(price_basis_usd_per_1k_tokens=2.5)


def _trace_entries() -> list[dict]:
    return [
        {"role": "intake", "prompt_chars": 500, "prompt_tokens_estimated": 125},
        {"role": "task_plan", "prompt_chars": 1500, "prompt_tokens_estimated": 375},
    ]


def _fixture_record() -> dict:
    return build_job_rehearsal(
        _two_task_job(), trace_entries=_trace_entries(), dod=_two_checks_dod(),
        predictive_config=_priced_config(), fence_spec=FenceSpec(), fence_error="",
        repo_head=REPO_HEAD, rehearsed_at=REHEARSED_AT)


# ── (a) the golden summary ───────────────────────────────────────────────────


def test_render_rehearsal_summary_matches_the_golden_file():
    summary = render_rehearsal_summary(_fixture_record())
    assert summary == GOLDEN.read_text(encoding="utf-8")


# ── (b) the planner's cost ───────────────────────────────────────────────────


def test_planner_cost_sums_both_trace_entries_and_claims_no_dollar_figure():
    cost = _fixture_record()["planner_cost"]
    assert cost["calls"] == 2
    assert cost["roles"] == ["intake", "task_plan"]
    assert cost["prompt_chars"] == 2000
    assert cost["prompt_tokens_estimated"] == 500
    assert "$" not in cost["basis"]
    assert "no cost in dollars is claimed" in cost["basis"]


# ── (c) per-task and whole-job pricing ───────────────────────────────────────


def test_the_priced_tasks_band_prices_and_the_unpriced_one_is_not_available():
    record = _fixture_record()
    first, second = record["tasks"]
    assert first["task_id"] == "T001"
    assert first["band_usd_low"] is not None
    assert first["band_usd_high"] is not None
    assert second["task_id"] == "T002"
    assert second["band_usd_low"] is None
    assert second["band_usd_high"] is None
    assert record["estimate_total"]["band_usd_low"] is None
    assert record["estimate_total"]["band_usd_high"] is None


def test_a_fully_priced_whole_job_reads_the_usd_form():
    """Amendment 1: the unit only appears once both bounds are measured; unavailable reads
    with no unit at all."""
    priced = TaskEntry(
        task_id="T001", title="Write the thing",
        inputs={"plan": {"planned_id": "T001", "title": "Write the thing", "depends_on": [],
                          "est_tokens_band": "M", "files_hint": []}},
        files_hint=[])
    job = JobPlan(job_id="job-priced-fixture", repo_path="/tmp/rehearsal-fixture",
                  tasks=[priced], task_plan=None)
    record = build_job_rehearsal(
        job, trace_entries=_trace_entries(), dod=_two_checks_dod(),
        predictive_config=_priced_config(), fence_spec=FenceSpec(), fence_error="",
        repo_head=REPO_HEAD, rehearsed_at=REHEARSED_AT)
    total = record["estimate_total"]
    assert total["band_usd_low"] is not None
    assert total["band_usd_high"] is not None
    summary = render_rehearsal_summary(record)
    assert f"Whole job: {total['band_usd_low']:.4f}–{total['band_usd_high']:.4f} USD. Basis: " in summary
    assert "Whole job: not available" not in summary


# ── (d) the fence simulation ─────────────────────────────────────────────────


def test_the_fence_simulation_writes_one_path_and_blocks_the_other():
    fences = _fixture_record()["fences"]
    assert fences["scope_undeclared"] is False
    assert fences["would_write"] == ["src/app.py"]
    assert len(fences["would_block"]) == 1
    assert fences["would_block"][0]["path"] == ".git/config"
    assert fences["would_block"][0]["reason"]


# ── (e) no files_hint anywhere ───────────────────────────────────────────────


def test_no_files_hint_anywhere_gives_scope_undeclared():
    job = _two_task_job()
    for task in job.tasks:
        task.files_hint = []
    record = build_job_rehearsal(
        job, trace_entries=_trace_entries(), dod=_two_checks_dod(),
        predictive_config=_priced_config(), fence_spec=FenceSpec(), fence_error="",
        repo_head=REPO_HEAD, rehearsed_at=REHEARSED_AT)
    assert record["fences"] == {
        "scope_undeclared": True, "would_write": [], "would_block": [], "error": ""}
    assert "Scope undeclared" in render_rehearsal_summary(record)


# ── (f) a fence config error ─────────────────────────────────────────────────


def test_a_fence_error_gives_the_sentence_and_no_list():
    record = build_job_rehearsal(
        _two_task_job(), trace_entries=_trace_entries(), dod=_two_checks_dod(),
        predictive_config=_priced_config(), fence_spec=FenceSpec(),
        fence_error="F017: malformed glob", repo_head=REPO_HEAD, rehearsed_at=REHEARSED_AT)
    assert record["fences"] == {
        "scope_undeclared": False, "would_write": [], "would_block": [],
        "error": "F017: malformed glob"}
    summary = render_rehearsal_summary(record)
    assert "The fences could not be read: F017: malformed glob" in summary
    assert "would write" not in summary
    assert "would be blocked" not in summary


# ── (g) no DoD ────────────────────────────────────────────────────────────────


def test_no_dod_gives_its_sentence():
    record = build_job_rehearsal(
        _two_task_job(), trace_entries=_trace_entries(), dod=None,
        predictive_config=_priced_config(), fence_spec=FenceSpec(), fence_error="",
        repo_head=REPO_HEAD, rehearsed_at=REHEARSED_AT)
    assert record["dod"] == {
        "present": False, "compiled": None, "checks": [], "not_compiled": []}
    summary = render_rehearsal_summary(record)
    assert "No definition of done is recorded for this job." in summary
    assert "| Check | Kind | Blocking | Source |" not in summary


# ── (h) no trace entry ───────────────────────────────────────────────────────


def test_no_trace_entry_gives_the_deterministic_sentence():
    record = build_job_rehearsal(
        _two_task_job(), trace_entries=[], dod=_two_checks_dod(),
        predictive_config=_priced_config(), fence_spec=FenceSpec(), fence_error="",
        repo_head=REPO_HEAD, rehearsed_at=REHEARSED_AT)
    assert record["planner_cost"]["calls"] == 0
    assert record["planner_cost"]["basis"] == (
        "No planning call was made for this job: its plan is deterministic.")


# ── (i) no task plan from the planner ────────────────────────────────────────


def test_a_job_without_a_task_plan_gives_the_risks_sentence_for_it():
    job = _two_task_job()
    job.task_plan = None
    record = build_job_rehearsal(
        job, trace_entries=_trace_entries(), dod=_two_checks_dod(),
        predictive_config=_priced_config(), fence_spec=FenceSpec(), fence_error="",
        repo_head=REPO_HEAD, rehearsed_at=REHEARSED_AT)
    assert record["risks"] is None
    assert record["normalization"] == []
    summary = render_rehearsal_summary(record)
    assert ("No task plan from the planner: the plan is deterministic and names no risk."
            in summary)


# ── (j) write_job_rehearsal, end to end ──────────────────────────────────────


def test_write_job_rehearsal_writes_both_files_and_updates_the_job(tmp_path, monkeypatch):
    from packages.orchestration.data_paths import job_evidence_dir
    from packages.orchestration.pingpong_job import save_job_plan

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    repo = tmp_path / "target"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=str(repo), check=True)
    subprocess.run(["git", "config", "user.email", "t@e.com"], cwd=str(repo), check=True)
    subprocess.run(["git", "config", "user.name", "T"], cwd=str(repo), check=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=str(repo), check=True)
    (repo / "README.md").write_text("# target\n")
    subprocess.run(["git", "add", "-A"], cwd=str(repo), check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=str(repo), check=True)
    real_head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(repo), capture_output=True, text=True,
        check=True).stdout.strip()

    job = _two_task_job(repo_path=str(repo))
    save_job_plan(job)

    summary_path = write_job_rehearsal(job)

    evidence_dir = job_evidence_dir(str(job.job_id))
    assert summary_path == evidence_dir / "rehearsal.md"
    json_path = evidence_dir / "rehearsal.json"
    assert json_path.is_file()
    assert summary_path.is_file()

    record = json.loads(json_path.read_text(encoding="utf-8"))
    assert record["repo_head"] == real_head
    assert summary_path.read_text(encoding="utf-8") == render_rehearsal_summary(record)

    reloaded = load_job_plan(str(job.job_id))
    assert reloaded.metadata["rehearsal"]["repo_head"] == real_head
    assert reloaded.metadata["rehearsal"]["record"] == "rehearsal.json"
    assert reloaded.metadata["rehearsal"]["rehearsed_at"]


# ── (k) rehearsal_staleness_warning and job_waits_after_rehearsal (DECISION F055 D3) ──


def _git_repo_with_one_commit(path: Path) -> str:
    """Init a tiny git repo at `path` with one commit; returns its HEAD."""
    subprocess.run(["git", "init", "-q"], cwd=str(path), check=True)
    subprocess.run(["git", "config", "user.email", "t@e.com"], cwd=str(path), check=True)
    subprocess.run(["git", "config", "user.name", "T"], cwd=str(path), check=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=str(path), check=True)
    (path / "README.md").write_text("# target\n")
    subprocess.run(["git", "add", "-A"], cwd=str(path), check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=str(path), check=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(path), capture_output=True, text=True,
        check=True).stdout.strip()


def test_no_rehearsal_record_gives_no_warning(tmp_path):
    job = JobPlan(job_id="job-a", repo_path=str(tmp_path))
    assert rehearsal_staleness_warning(job) is None


def test_a_record_with_no_recorded_head_gives_no_warning(tmp_path):
    job = JobPlan(job_id="job-b", repo_path=str(tmp_path),
                  metadata={"rehearsal": {"repo_head": ""}})
    assert rehearsal_staleness_warning(job) is None


def test_equal_heads_give_no_warning(tmp_path):
    head = _git_repo_with_one_commit(tmp_path)
    job = JobPlan(job_id="job-c", repo_path=str(tmp_path),
                  metadata={"rehearsal": {"repo_head": head}})
    assert rehearsal_staleness_warning(job) is None


def test_an_unreadable_current_head_gives_no_warning():
    job = JobPlan(job_id="job-d", repo_path="/nonexistent/path/for/f055-rehearsal",
                  metadata={"rehearsal": {"repo_head": REPO_HEAD}})
    assert rehearsal_staleness_warning(job) is None


def test_a_moved_head_gives_the_warning_sentence(tmp_path):
    old_head = _git_repo_with_one_commit(tmp_path)
    (tmp_path / "more.txt").write_text("more\n")
    subprocess.run(["git", "add", "-A"], cwd=str(tmp_path), check=True)
    subprocess.run(["git", "commit", "-qm", "moved"], cwd=str(tmp_path), check=True)
    job = JobPlan(job_id="job-e", repo_path=str(tmp_path),
                  metadata={"rehearsal": {"repo_head": old_head}})

    warning = rehearsal_staleness_warning(job)

    now = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(tmp_path),
                         capture_output=True, text=True, check=True).stdout.strip()
    assert warning == (
        f"Warning: job job-e was rehearsed at commit {old_head[:12]}, and its "
        f"repository is now at commit {now[:12]}; the plan may be stale, so check it "
        f"before you run it.")


def test_job_waits_after_rehearsal_true_only_while_planned_with_a_record():
    from packages.orchestration.pingpong_job import JOB_COMPLETED

    planned_with_record = JobPlan(job_id="job-f", metadata={"rehearsal": {"repo_head": "x"}})
    assert job_waits_after_rehearsal(planned_with_record) is True

    planned_without_record = JobPlan(job_id="job-g")
    assert job_waits_after_rehearsal(planned_without_record) is False

    completed_with_record = JobPlan(
        job_id="job-h", state=JOB_COMPLETED, metadata={"rehearsal": {"repo_head": "x"}})
    assert job_waits_after_rehearsal(completed_with_record) is False
