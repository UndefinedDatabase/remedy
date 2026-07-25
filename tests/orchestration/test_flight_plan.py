"""Tests for flight plan LLM generation + task mapping (F014 T002/T003)."""

from __future__ import annotations

import json

from packages.core.models import RunState
from packages.orchestration.flight_plan import (
    apply_plan_budgets,
    apply_plan_fences,
    map_flight_plan_to_tasks,
    plan_job_llm,
)
from packages.orchestration.schemas.models import FlightPlan


def _fake_intake() -> dict:
    return {
        "schema_v": "ji1",
        "goal": "Add a login page",
        "context_refs": ["src/auth.py"],
        "constraints": ["No new dependencies"],
        "acceptance_hints": ["Login form renders"],
        "truncated_input": False,
        "clarifications": [],
        "dropped_clarifications": 0,
    }


def _valid_plan_json(n_tasks: int = 3) -> str:
    tasks = []
    for i in range(n_tasks):
        tid = f"T{i + 1:03d}"
        deps = [f"T{i:03d}"] if i > 0 else []
        tasks.append({
            "id": tid,
            "title": f"Task {i + 1}",
            "goal": f"Do thing {i + 1}",
            "acceptance": [f"Thing {i + 1} done"],
            "depends_on": deps,
            "est_tokens_band": "M",
            "files_hint": [f"src/file{i + 1}.py"],
        })
    return json.dumps({
        "schema_v": "flight_plan_v1",
        "tasks": tasks,
        "risks": ["timeline risk"],
    })


def _fake_provider(response_text: str):
    def _call(prompt: str, attempt: int) -> str:
        return response_text
    return _call


class TestPlanJobLlm:

    def test_three_task_plan_succeeds(self):
        result = plan_job_llm(_fake_intake(), _fake_provider(_valid_plan_json(3)))
        assert result.plan is not None
        assert len(result.plan.tasks) == 3
        assert result.source == "llm"
        assert result.error_hint == ""
        assert result.calls == 1

    def test_provider_exception_returns_error(self):
        def _exploding(prompt: str, attempt: int) -> str:
            raise ConnectionError("network down")

        result = plan_job_llm(_fake_intake(), _exploding)
        assert result.plan is None
        assert "provider error" in result.error_hint

    def test_cyclic_plan_returns_parse_error(self):
        cyclic = json.dumps({
            "schema_v": "flight_plan_v1",
            "tasks": [
                {"id": "T1", "title": "A", "goal": "A", "acceptance": ["ok"],
                 "depends_on": ["T2"], "est_tokens_band": "S", "files_hint": []},
                {"id": "T2", "title": "B", "goal": "B", "acceptance": ["ok"],
                 "depends_on": ["T1"], "est_tokens_band": "S", "files_hint": []},
            ],
            "risks": [],
        })
        result = plan_job_llm(_fake_intake(), _fake_provider(cyclic))
        assert result.plan is None
        assert result.error_hint != ""

    def test_invalid_json_retries_then_fails(self):
        calls = []

        def _bad_then_bad(prompt: str, attempt: int) -> str:
            calls.append(attempt)
            return "not json at all"

        result = plan_job_llm(_fake_intake(), _bad_then_bad)
        assert result.plan is None
        assert len(calls) == 2  # initial + one retry


class TestMapFlightPlanToTasks:

    def test_three_tasks_in_order(self):
        fp = FlightPlan(**json.loads(_valid_plan_json(3)))
        tasks = map_flight_plan_to_tasks(fp)
        assert len(tasks) == 3
        for i, task in enumerate(tasks):
            assert task.status == RunState.PENDING
            flight = task.inputs["flight"]
            assert flight["planned_id"] == f"T{i + 1:03d}"
            assert flight["title"] == f"Task {i + 1}"
            assert f"Thing {i + 1} done" in task.acceptance_checks[0].description

    def test_description_combines_title_and_goal(self):
        fp = FlightPlan(**json.loads(_valid_plan_json(1)))
        tasks = map_flight_plan_to_tasks(fp)
        assert "Task 1" in tasks[0].description
        assert "Do thing 1" in tasks[0].description

    def test_depends_on_preserved(self):
        fp = FlightPlan(**json.loads(_valid_plan_json(3)))
        tasks = map_flight_plan_to_tasks(fp)
        assert tasks[0].inputs["flight"]["depends_on"] == []
        assert tasks[1].inputs["flight"]["depends_on"] == ["T001"]
        assert tasks[2].inputs["flight"]["depends_on"] == ["T002"]


class TestBudgetPrecedence:

    def test_config_set_budget_survives(self):
        job_budgets = {"max_total_tokens": 100000, "max_provider_calls": 50}
        plan_budgets = {"max_total_tokens": 200000, "max_wall_clock_minutes": 30}
        merged = apply_plan_budgets(job_budgets, plan_budgets)
        assert merged["max_total_tokens"] == 100000  # user wins
        assert merged["max_provider_calls"] == 50    # user kept
        assert merged["max_wall_clock_minutes"] == 30  # plan fills gap

    def test_plan_budget_fills_unset(self):
        merged = apply_plan_budgets(None, {"max_total_tokens": 50000})
        assert merged == {"max_total_tokens": 50000}

    def test_no_budgets_returns_none(self):
        assert apply_plan_budgets(None, None) is None

    def test_only_job_budgets(self):
        merged = apply_plan_budgets({"max_total_tokens": 10}, None)
        assert merged == {"max_total_tokens": 10}


class TestFencePrecedence:

    def test_config_set_fences_survive(self):
        job_fences = {"allow": ["src/**"]}
        plan_fences = {"allow": ["lib/**"], "deny": ["tests/**"]}
        merged = apply_plan_fences(job_fences, plan_fences)
        assert merged["allow"] == ["src/**"]  # user wins
        assert merged["deny"] == ["tests/**"]  # plan fills gap

    def test_plan_fences_fill_unset(self):
        merged = apply_plan_fences(None, {"allow": ["src/**"]})
        assert merged == {"allow": ["src/**"]}

    def test_no_fences_returns_none(self):
        assert apply_plan_fences(None, None) is None
