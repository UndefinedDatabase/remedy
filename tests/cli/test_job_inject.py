"""F028 T003, DECISION F028 D4 — `remedy job inject`, `job inject-confirm` and
`job inject-answer`.

Modelled on `test_job_veto.py`: the CLI handlers are proved through the real argv
dispatcher, over a running job carrying both a runtime task list (`test_dag_schedule
.flight_task`, so `--after` resolution is proved against the real `job_plan_cmd
._resolve_task_arg`) and a matching stored task plan (so `task_injection
.draft_task_injection` has a plan to place against). `task_injection.injection_call_fn`
is monkeypatched everywhere a planner call would otherwise be attempted, and
`task_injection.injection_budget_inputs` wherever a budget shortfall matters — the
module functions themselves (`draft_task_injection`, `confirm_task_injection`,
`answer_injection_shortfall`) are proved directly in `test_task_injection.py`; this file
proves the CLI's wrapping: argument resolution, printed/JSON output, and exit codes.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.core.models import JobBudgets, RunState
from packages.orchestration import pingpong_job as pj
from packages.orchestration import task_injection as ti
from packages.orchestration.budget_guard import BudgetCounters
from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.schemas.models import PlannedTask, TaskPlan
from tests.orchestration.test_dag_schedule import flight_task

CLASS_DEFAULTS = {"low": 8000, "medium": 32000, "high": 120000}


class _FakeCall:
    """A queue of raw replies; each call pops the next. Mirrors
    `test_task_injection.py::_FakeCall` exactly."""

    def __init__(self, replies: list[str]) -> None:
        self._replies = list(replies)
        self.calls = 0

    def __call__(self, prompt: str, attempt: int) -> str:
        self.calls += 1
        return self._replies.pop(0)


def _draft_json(*, title: str = "Add the thing", goal: str = "do the thing",
                acceptance: tuple[str, ...] = ("acceptance one",), est_tokens_band: str = "S",
                files_hint: tuple[str, ...] = (), rationale: str = "because") -> str:
    return json.dumps({
        "schema_v": "task_injection_draft_v1",
        "title": title,
        "goal": goal,
        "acceptance": list(acceptance),
        "est_tokens_band": est_tokens_band,
        "files_hint": list(files_hint),
        "rationale": rationale,
    })


def _counters(spent: float | None) -> BudgetCounters:
    return BudgetCounters(
        provider_calls=1, measured_call_count=1, unmeasured_call_count=0,
        measured_token_total=1000, actual_sources=("pingpong_actuals",),
        measured_cost_usd=spent, priced_call_count=1)


def _config(price_basis: float | None = 0.01) -> PredictiveBudgetConfig:
    return PredictiveBudgetConfig(price_basis_usd_per_1k_tokens=price_basis,
                                  class_default_tokens=dict(CLASS_DEFAULTS))


def _shortfall_budget_inputs(job):
    """A limit no band M draft can fit under, however this job's real budgets read."""
    return JobBudgets(max_cost_usd=0.01), _counters(0.0), _config()


def _plan_task(task_id: str, depends_on: tuple[str, ...] = ()) -> PlannedTask:
    return PlannedTask(id=task_id, title=f"title {task_id}", goal=f"goal {task_id}",
                       acceptance=[f"do {task_id}"], est_tokens_band="S",
                       depends_on=list(depends_on))


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def job(data_root) -> pj.JobPlan:
    """T1 -> T2, both pending, the job running, with a matching stored task plan — a
    job `job inject` can draft into and `--after` can resolve against."""
    tasks = [flight_task("T1"), flight_task("T2", "T1")]
    task_plan = TaskPlan(
        schema_v="task_plan_v1",
        tasks=[_plan_task("T1"), _plan_task("T2", depends_on=("T1",))],
    ).model_dump()
    job = pj.JobPlan(job_title="CLI inject test", tasks=tasks, state=RunState.RUNNING,
                     task_plan=task_plan)
    pj.save_job_plan(job)
    return job


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return (code or 0), capsys.readouterr().out


def _draft(job, capsys, monkeypatch, *, text: str = "add a widget",
          band: str = "S", after: str | None = None) -> dict:
    """Draft through the CLI, returning the parsed JSON envelope."""
    call = _FakeCall([_draft_json(est_tokens_band=band)])
    monkeypatch.setattr(ti, "injection_call_fn", lambda: call)
    argv = ["job", "inject", str(job.job_id), text, "--json"]
    if after is not None:
        argv = ["job", "inject", str(job.job_id), text, "--after", after, "--json"]
    code, out = _run(argv, capsys)
    assert code == 0, out
    return json.loads(out)


def _draft_shortfall(job, capsys, monkeypatch) -> dict:
    call = _FakeCall([_draft_json(est_tokens_band="M")])
    monkeypatch.setattr(ti, "injection_call_fn", lambda: call)
    monkeypatch.setattr(ti, "injection_budget_inputs", _shortfall_budget_inputs)
    code, out = _run(
        ["job", "inject", str(job.job_id), "add a widget", "--json"], capsys)
    assert code == 0, out
    body = json.loads(out)
    assert body["outcome"] == "shortfall"
    return body


class TestInjectDraft:
    def test_human_output_holds_the_confirm_line_with_its_token(self, job, capsys, monkeypatch):
        call = _FakeCall([_draft_json()])
        monkeypatch.setattr(ti, "injection_call_fn", lambda: call)

        code, out = _run(["job", "inject", str(job.job_id), "add a widget"], capsys)

        assert code == 0
        assert f"remedy job inject-confirm {job.job_id}" in out

    def test_json_envelope_carries_the_draft(self, job, capsys, monkeypatch):
        body = _draft(job, capsys, monkeypatch)
        assert body["ok"] is True
        assert body["outcome"] == "drafted"
        assert body["confirm_token"] == body["draft_id"]
        assert body["task"]["title"] == "Add the thing"

    def test_after_by_planned_id_and_by_entry_id_give_the_same_depends_on(
            self, job, capsys, monkeypatch):
        t1_entry = next(t for t in job.tasks if t.inputs["plan"]["planned_id"] == "T1")

        by_planned_id = _draft(job, capsys, monkeypatch, text="widget one", after="T1")
        assert by_planned_id["placement"]["depends_on"] == ["T1"]

        by_entry_id = _draft(
            job, capsys, monkeypatch, text="widget two", after=t1_entry.task_id)
        assert by_entry_id["placement"]["depends_on"] == ["T1"]


class TestInjectYes:
    def test_yes_confirms_at_once_with_confirmed_unseen_true(self, job, capsys, monkeypatch):
        call = _FakeCall([_draft_json()])
        monkeypatch.setattr(ti, "injection_call_fn", lambda: call)

        code, out = _run(
            ["job", "inject", str(job.job_id), "add a widget", "--yes", "--json"], capsys)

        assert code == 0
        body = json.loads(out)
        assert body["ok"] is True
        assert body["draft"]["outcome"] == "drafted"
        assert body["confirmation"]["outcome"] == "confirmed"

        [record] = ti.confirmed_injections(str(job.job_id))
        assert record["confirmed_unseen"] is True

    def test_yes_over_a_shortfall_exits_3_with_the_seed_printed_and_nothing_confirmed(
            self, job, capsys, monkeypatch):
        call = _FakeCall([_draft_json(est_tokens_band="M")])
        monkeypatch.setattr(ti, "injection_call_fn", lambda: call)
        monkeypatch.setattr(ti, "injection_budget_inputs", _shortfall_budget_inputs)

        code, out = _run(
            ["job", "inject", str(job.job_id), "add a widget", "--yes"], capsys)

        assert code == 3
        assert "cost limit" in out
        assert ti.confirmed_injections(str(job.job_id)) == ()

    def test_yes_json_over_a_shortfall_prints_exactly_one_json_document(
            self, job, capsys, monkeypatch):
        """R-1078's repair: `--yes --json` over a shortfall must never emit `emit_ok`'s
        envelope before `fail`'s — a caller parsing `--json` output as one document must
        not choke on a second."""
        call = _FakeCall([_draft_json(est_tokens_band="M")])
        monkeypatch.setattr(ti, "injection_call_fn", lambda: call)
        monkeypatch.setattr(ti, "injection_budget_inputs", _shortfall_budget_inputs)

        code, out = _run(
            ["job", "inject", str(job.job_id), "add a widget", "--yes", "--json"], capsys)

        assert code == 3
        body = json.loads(out)                     # raises if stdout is not ONE document
        assert body["ok"] is False
        assert body["error"] == "draft_needs_decision"
        assert "draft_id" in body
        assert "decision_seed" in body
        assert "budget_check" in body
        assert ti.confirmed_injections(str(job.job_id)) == ()


class TestInjectConfirm:
    def test_confirms_a_drafted_injection(self, job, capsys, monkeypatch):
        draft = _draft(job, capsys, monkeypatch)

        code, out = _run(
            ["job", "inject-confirm", str(job.job_id), draft["confirm_token"], "--json"],
            capsys)

        assert code == 0
        body = json.loads(out)
        assert body["outcome"] == "confirmed"
        assert body["task_id"] == draft["task"]["id"]

    def test_an_unknown_token_answers_draft_unknown_exit_3(self, job, capsys):
        code, out = _run(
            ["job", "inject-confirm", str(job.job_id), "deadbeefdeadbeef", "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "draft_unknown"


class TestInjectAnswer:
    @pytest.mark.parametrize("option", ["drop", "shrink_task", "extend_budget"])
    def test_each_option_answers_and_exits_zero(self, job, capsys, monkeypatch, option):
        shortfall = _draft_shortfall(job, capsys, monkeypatch)

        code, out = _run(
            ["job", "inject-answer", str(job.job_id), shortfall["draft_id"],
             "--option", option, "--json"], capsys)

        assert code == 0, out
        body = json.loads(out)
        assert body["outcome"] in ("dropped", "drafted", "shortfall")

    def test_unknown_option_exits_2(self, job, capsys, monkeypatch):
        shortfall = _draft_shortfall(job, capsys, monkeypatch)

        code, out = _run(
            ["job", "inject-answer", str(job.job_id), shortfall["draft_id"],
             "--option", "bogus", "--json"], capsys)

        assert code == 2
        assert json.loads(out)["error"] == "unknown_option"


class TestInjectExitCodes:
    """One exit code per class (DECISION F028 D4)."""

    def test_text_invalid_exits_2(self, job, capsys):
        parts = ["sk", "-", "ant", "-"] + ["a"] * 24
        secret_shaped = "".join(parts)

        code, out = _run(
            ["job", "inject", str(job.job_id), secret_shaped, "--json"], capsys)

        assert code == 2
        assert json.loads(out)["error"] == "text_invalid"

    def test_planner_unavailable_exits_3(self, job, capsys, monkeypatch):
        monkeypatch.setattr(ti, "injection_call_fn", lambda: None)

        code, out = _run(
            ["job", "inject", str(job.job_id), "add a widget", "--json"], capsys)

        assert code == 3
        assert json.loads(out)["error"] == "planner_unavailable"

    def test_draft_unknown_exits_3(self, job, capsys):
        code, out = _run(
            ["job", "inject-confirm", str(job.job_id), "deadbeefdeadbeef", "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "draft_unknown"

    def test_draft_unparseable_exits_1(self, job, capsys, monkeypatch):
        call = _FakeCall(["not json", "still not json"])
        monkeypatch.setattr(ti, "injection_call_fn", lambda: call)

        code, out = _run(
            ["job", "inject", str(job.job_id), "add a widget", "--json"], capsys)

        assert code == 1
        assert json.loads(out)["error"] == "draft_unparseable"

    def test_a_missing_job_exits_1(self, capsys):
        code, out = _run(
            ["job", "inject", "0123456789abcdef", "add a widget", "--json"], capsys)
        assert code == 1
        assert json.loads(out)["error"] == "invalid_job_id"
