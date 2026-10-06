"""F028 R2 — the linear runner's fold of a confirmed task injection (DECISION F028 D2 (3)).

The fold at all four points, the task the loop has not yet reached running in the same run
(the live list a growing ``job.tasks`` feeds ``enumerate`` over), a fold after the loop
parking the job PAUSED with the injected task pending, an injection folded once and never
again, a corrupt control area blocking the job, and an inert fold recording its reason.

Built on the fixtures and fake builders of ``tests/orchestration/test_task_veto_runner.py``:
planned jobs as ``test_task_edit_runtime.py``'s own ``_save_job`` builds them, and runs go
through the real ``run_job`` with ``pingpong_provider.FakeProvider`` or a small custom fake.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.core.models import JobBudgets
from packages.orchestration import budget_guard, safe_points
from packages.orchestration import pingpong_job as pj
from packages.orchestration import task_injection as ti
from packages.orchestration.budget_guard import BudgetCounters
from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PAUSED,
    load_job_plan,
    run_job,
    save_job_plan,
)
from packages.orchestration.pingpong_provider import BuilderOutput, FakeProvider, ReviewerOutput
from packages.orchestration.run_report import render_report
from tests.orchestration.test_task_edit_runtime import _by_planned, _save_job, _task


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
    return data


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A plain (non-git) directory: the copy-mode job's target."""
    r = tmp_path / "repo"
    r.mkdir()
    (r / "docs").mkdir()
    (r / "docs" / "README.md").write_text("# Docs\n")
    return r


def _control() -> Path:
    return safe_points.control_root()


def _pass_provider() -> FakeProvider:
    return FakeProvider(pass_on_round=1, fail_on_round=99)


class _RefusingProvider:
    """A provider that must never be called: `build`/`review` fail the test outright."""

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return False

    def build(self, prompt, **kw):
        raise AssertionError("the builder must not run: nothing should be dispatched")

    def review(self, prompt, **kw):
        raise AssertionError("the reviewer must not run: nothing should be dispatched")


# ---------------------------------------------------------------------------
# A permissive budget triple: no cost limit, so an injection is never a shortfall
# ---------------------------------------------------------------------------


def _no_limit_budgets() -> JobBudgets:
    return JobBudgets()


def _zero_counters() -> BudgetCounters:
    return BudgetCounters(
        provider_calls=0, measured_call_count=0, unmeasured_call_count=0,
        measured_token_total=0, actual_sources=(), measured_cost_usd=None,
        priced_call_count=0)


def _no_price_config() -> PredictiveBudgetConfig:
    return PredictiveBudgetConfig(
        price_basis_usd_per_1k_tokens=None,
        class_default_tokens={"low": 8000, "medium": 32000, "high": 120000})


def _draft_json() -> str:
    return json.dumps({
        "schema_v": "task_injection_draft_v1",
        "title": "Add the thing",
        "goal": "do the thing",
        "acceptance": ["it happens"],
        "est_tokens_band": "S",
        "files_hint": [],
        "rationale": "because the operator asked",
    })


class _FakeCall:
    def __init__(self, replies: list[str]) -> None:
        self._replies = list(replies)
        self.calls = 0

    def __call__(self, prompt: str, attempt: int) -> str:
        self.calls += 1
        return self._replies.pop(0)


def _draft_and_confirm(job, *, control_root_path: Path, actor: str = "alice") -> dict:
    """Draft one injection against *job* and confirm it, answering the confirmation."""
    call = _FakeCall([_draft_json()])
    draft = ti.draft_task_injection(
        job, "add a widget", call_fn=call, budgets=_no_limit_budgets(),
        counters=_zero_counters(), config=_no_price_config(), actor=actor,
        control_root_path=control_root_path)
    assert draft["outcome"] == "drafted", draft
    confirmed = ti.confirm_task_injection(
        job, draft["confirm_token"], actor=actor, control_root_path=control_root_path)
    assert confirmed["outcome"] == "confirmed", confirmed
    return confirmed


# ---------------------------------------------------------------------------
# Confirmed before the run: the injected task runs in the same run
# ---------------------------------------------------------------------------


class TestConfirmedBeforeTheRun:
    def test_the_injected_task_runs_in_the_same_run_and_the_job_completes(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)

        confirmed = _draft_and_confirm(job, control_root_path=_control())

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_COMPLETED
        assert len(done.tasks) == 2
        _, injected = _by_planned(done, confirmed["task_id"])
        assert injected.status == pj.TASK_APPLIED
        assert injected.inputs["plan"]["origin"] == ti.ORIGIN_HUMAN_INJECTED
        recorded = done.metadata["task_injections"][confirmed["draft_id"]]
        assert recorded["task_id"] == injected.task_id

    def test_render_report_holds_the_clause_on_the_injected_tasks_line_once(
            self, root, repo):
        """DECISION F028 D8's S2 half: the fold's `origin` reaches the report."""
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)

        confirmed = _draft_and_confirm(job, control_root_path=_control())

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        _, injected = _by_planned(done, confirmed["task_id"])
        report = render_report(done)
        clause = " — added by you while the job ran"
        matching = [line for line in report.splitlines() if clause in line]
        assert len(matching) == 1, (
            f"expected the clause exactly once, found {len(matching)}: {matching}")
        assert matching[0].startswith(f"- `{injected.task_id[:8]}`")


# ---------------------------------------------------------------------------
# Confirmed while the job's LAST task runs
# ---------------------------------------------------------------------------


# A FakeProvider, so the loop writes the file its build names: a job task that changed no
# file is blocked (R-1117).
class _InjectingBuilder(FakeProvider):
    """During the LAST original task's OWN build call, drafts and confirms an injection."""

    def __init__(self, job_id: str, inject_on_build: int):
        super().__init__(pass_on_round=1, fail_on_round=99)
        self._job_id = job_id
        self._inject_on_build = inject_on_build
        self.build_calls = 0

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return False

    def build(self, prompt, **kw):
        self.build_calls += 1
        if self.build_calls == self._inject_on_build:
            job = load_job_plan(self._job_id)
            _draft_and_confirm(job, control_root_path=_control())
        return BuilderOutput(summary="ok", files_changed=["docs/README.md"], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


class TestConfirmedWhileTheLastTaskRuns:
    def test_the_injected_task_runs_in_the_same_run_and_the_job_completes(self, root, repo):
        tasks = [_task("A", []), _task("B", ["A"])]
        job_id = _save_job(root, tasks, repo_path=str(repo))
        builder = _InjectingBuilder(job_id, inject_on_build=2)      # B is the 2nd build call

        done = run_job(job_id, builder_provider=builder, reviewer_provider=builder,
                       max_rounds=1, repair_rounds=0)

        assert done.state == JOB_COMPLETED
        assert len(done.tasks) == 3
        a = _by_planned(done, "A")[1]
        b = _by_planned(done, "B")[1]
        assert a.status == pj.TASK_APPLIED and b.status == pj.TASK_APPLIED
        [draft_id] = list(done.metadata["task_injections"])
        recorded = done.metadata["task_injections"][draft_id]
        _, injected = _by_planned(done, recorded["planned_id"])
        assert injected.status == pj.TASK_APPLIED
        assert injected.inputs["plan"]["origin"] == ti.ORIGIN_HUMAN_INJECTED


# ---------------------------------------------------------------------------
# Confirmed exactly at point (d): the fold after the loop parks the job PAUSED
# ---------------------------------------------------------------------------


class TestConfirmedExactlyAtPointD:
    def test_the_job_parks_paused_and_a_second_run_completes_it(
            self, root, repo, monkeypatch):
        tasks = [_task("A", [])]
        job_id = _save_job(root, tasks, repo_path=str(repo))

        real_fold = pj._fold_task_injections
        calls = {"n": 0}

        def wrapper(job, control_root_path):
            calls["n"] += 1
            if calls["n"] == 4:                       # point (d): after the loop
                fresh = load_job_plan(job_id, root)
                _draft_and_confirm(fresh, control_root_path=control_root_path)
            return real_fold(job, control_root_path)

        monkeypatch.setattr(pj, "_fold_task_injections", wrapper)

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert calls["n"] == 4
        assert done.state == JOB_PAUSED
        assert len(done.tasks) == 2
        a = _by_planned(done, "A")[1]
        assert a.status == pj.TASK_APPLIED
        [draft_id] = list(done.metadata["task_injections"])
        planned_id = done.metadata["task_injections"][draft_id]["planned_id"]
        injected = _by_planned(done, planned_id)[1]
        assert injected.status == pj.TASK_PENDING

        completed = run_job(job_id, builder_provider=_pass_provider(),
                            reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)
        assert completed.state == JOB_COMPLETED
        assert _by_planned(completed, planned_id)[1].status == pj.TASK_APPLIED


# ---------------------------------------------------------------------------
# An injection folded once is never folded twice across two runs
# ---------------------------------------------------------------------------


class TestInjectionFoldedOnlyOnceAcrossRuns:
    def test_a_second_run_never_refolds_the_same_confirmation(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)
        _draft_and_confirm(job, control_root_path=_control())

        first = run_job(job_id, builder_provider=_pass_provider(),
                        reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)
        assert first.state == JOB_COMPLETED
        assert len(first.tasks) == 2
        recorded = dict(first.metadata["task_injections"])

        second = run_job(job_id, builder_provider=_RefusingProvider(),
                         reviewer_provider=_RefusingProvider(), max_rounds=1, repair_rounds=0)
        assert second.state == JOB_COMPLETED
        assert len(second.tasks) == 2
        assert second.metadata["task_injections"] == recorded


# ---------------------------------------------------------------------------
# A corrupt confirmed-injection file blocks the job
# ---------------------------------------------------------------------------


class TestCorruptConfirmedInjectionFile:
    def test_blocks_with_task_injection_control_error_and_dispatches_nothing(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))

        d = _control() / "jobs" / job_id / ti.INJECTED_TASKS_DIRNAME
        d.mkdir(parents=True)
        (d / "deadbeefdeadbeefdeadbeefdeadbeef.json").write_text("not json")

        done = run_job(job_id, builder_provider=_RefusingProvider(),
                       reviewer_provider=_RefusingProvider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_BLOCKED
        assert done.error.startswith("task_injection_control_error:")
        a = done.tasks[0]
        assert a.status == pj.TASK_PENDING
        assert not a.run_id


# ---------------------------------------------------------------------------
# An inert fold: a confirmed injection the apply refuses
# ---------------------------------------------------------------------------


class TestInertInjectionFold:
    def test_records_the_refusal_reason_and_dispatches_nothing_new(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))

        bad_record = {
            "injected_task_v": 1, "job_id": job_id, "draft_id": "baddraft00000001",
            "task": {"id": "INJ1", "title": "t", "goal": "g", "acceptance": ["a"],
                    "depends_on": ["GHOST"], "est_tokens_band": "S", "files_hint": []},
            "placement": {"depends_on": ["GHOST"], "basis": "stated", "position": 1,
                         "rationale": "r"},
            "task_rationale": "r", "text": "t", "drafted_by": "alice", "actor": "alice",
            "confirmed_at": "2026-01-01T00:00:00+00:00",
        }
        assert ti._publish_confirmed_injection(
            job_id, bad_record["draft_id"], bad_record, control_root_path=_control())

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_COMPLETED
        assert len(done.tasks) == 1
        entry = done.metadata["task_injections"]["baddraft00000001"]
        assert "inert" in entry and entry["folded_at"]


# ---------------------------------------------------------------------------
# R-1077 — a confirmed injection missing a field the apply reads blocks the job loudly
# ---------------------------------------------------------------------------


class TestConfirmedInjectionMissingAFieldBlocksTheJob:
    def test_missing_text_blocks_with_task_injection_control_error(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))

        bad_record = {
            "draft_id": "baddraft00000002",
            "task": {"id": "INJ1", "title": "t", "goal": "g", "acceptance": ["a"],
                    "depends_on": [], "est_tokens_band": "S", "files_hint": []},
            "placement": {"depends_on": [], "basis": "frontier_default", "position": 1,
                         "rationale": "r"},
            "task_rationale": "r", "actor": "alice",
            "confirmed_at": "2026-01-01T00:00:00+00:00",
        }                                                      # deliberately missing "text"
        assert ti._publish_confirmed_injection(
            job_id, bad_record["draft_id"], bad_record, control_root_path=_control())

        done = run_job(job_id, builder_provider=_RefusingProvider(),
                       reviewer_provider=_RefusingProvider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_BLOCKED
        assert done.error.startswith("task_injection_control_error:")
        a = done.tasks[0]
        assert a.status == pj.TASK_PENDING
        assert not a.run_id


# ---------------------------------------------------------------------------
# DECISION F028 D3 (2) — an extension folded before the run reaches the very next safe point
# ---------------------------------------------------------------------------


def _shortfall_counters() -> BudgetCounters:
    return BudgetCounters(
        provider_calls=1, measured_call_count=1, unmeasured_call_count=0,
        measured_token_total=1000, actual_sources=("pingpong_actuals",),
        measured_cost_usd=0.90, priced_call_count=1)


def _priced_config() -> PredictiveBudgetConfig:
    return PredictiveBudgetConfig(
        price_basis_usd_per_1k_tokens=0.01,
        class_default_tokens={"low": 8000, "medium": 32000, "high": 120000})


class TestBudgetExtensionReachesThePredictiveCheck:
    def test_the_extended_limit_reaches_every_predictive_call_and_the_job_records_it(
            self, root, repo, monkeypatch):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)
        job.budgets = {"max_cost_usd": 1.00}
        save_job_plan(job, root)

        call = _FakeCall([json.dumps({
            "schema_v": "task_injection_draft_v1", "title": "Add the thing",
            "goal": "do the thing", "acceptance": ["it happens"], "est_tokens_band": "M",
            "files_hint": [], "rationale": "because the operator asked",
        })])
        draft = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(max_cost_usd=1.00),
            counters=_shortfall_counters(), config=_priced_config(), actor="alice",
            control_root_path=_control())
        assert draft["outcome"] == "shortfall"

        answered = ti.answer_injection_shortfall(
            job, draft["draft_id"], "extend_budget", actor="alice",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_shortfall_counters(),
            config=_priced_config(), control_root_path=_control())
        assert answered["outcome"] == "drafted"
        assert answered["budget_extend_to_usd"] == 1.22

        confirmed = ti.confirm_task_injection(
            job, answered["confirm_token"], actor="alice", control_root_path=_control())
        assert confirmed["outcome"] == "confirmed"

        seen_limits: list[float | None] = []
        real_predict = budget_guard.predict_next_task_cost

        def _recording_predict(budgets, counters, *, band, config):
            seen_limits.append(budgets.max_cost_usd if budgets is not None else None)
            return real_predict(budgets, counters, band=band, config=config)

        monkeypatch.setattr(budget_guard, "predict_next_task_cost", _recording_predict)

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_COMPLETED
        assert len(done.tasks) == 2
        assert seen_limits, "the predictive check never ran"
        assert all(limit == 1.22 for limit in seen_limits)
        assert done.budgets["max_cost_usd"] == 1.22


# ---------------------------------------------------------------------------
# DECISION F028 D5 (2) — the fold writes one `task_injected` event per record, after
# `_persist_job`
# ---------------------------------------------------------------------------


def _injected_events(job_id: str) -> list[dict]:
    from packages.orchestration.data_paths import run_log_dir

    job_runs = run_log_dir(job_id)
    out: list[dict] = []
    if job_runs.is_dir():
        for jsonl in sorted(job_runs.glob("*.jsonl")):
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    out.append(json.loads(line))
    return [e for e in out if e.get("event") == "task_injected"]


class TestTaskInjectedEvent:
    def test_an_applied_fold_writes_one_event_naming_the_new_entrys_task_id(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)
        confirmed = _draft_and_confirm(job, control_root_path=_control())

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_COMPLETED
        recorded = done.metadata["task_injections"][confirmed["draft_id"]]
        [event] = _injected_events(job_id)
        assert event["outcome"] == "applied"
        assert event["task_id"] == recorded["task_id"]

    def test_an_inert_fold_writes_one_event_naming_its_reason(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))

        bad_record = {
            "injected_task_v": 1, "job_id": job_id, "draft_id": "baddraft00000003",
            "task": {"id": "INJ1", "title": "t", "goal": "g", "acceptance": ["a"],
                    "depends_on": ["GHOST"], "est_tokens_band": "S", "files_hint": []},
            "placement": {"depends_on": ["GHOST"], "basis": "stated", "position": 1,
                         "rationale": "r"},
            "task_rationale": "r", "text": "t", "drafted_by": "alice", "actor": "alice",
            "confirmed_at": "2026-01-01T00:00:00+00:00",
        }
        assert ti._publish_confirmed_injection(
            job_id, bad_record["draft_id"], bad_record, control_root_path=_control())

        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert done.state == JOB_COMPLETED
        [event] = _injected_events(job_id)
        assert event["outcome"] == "inert"
        assert event["task_id"] == ""
        recorded = done.metadata["task_injections"]["baddraft00000003"]
        assert event["metadata"]["reason"] == recorded["inert"]

    def test_a_second_run_writes_no_further_event(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)
        _draft_and_confirm(job, control_root_path=_control())

        first = run_job(job_id, builder_provider=_pass_provider(),
                        reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)
        assert first.state == JOB_COMPLETED
        assert len(_injected_events(job_id)) == 1

        second = run_job(job_id, builder_provider=_RefusingProvider(),
                         reviewer_provider=_RefusingProvider(), max_rounds=1, repair_rounds=0)
        assert second.state == JOB_COMPLETED
        assert len(_injected_events(job_id)) == 1
