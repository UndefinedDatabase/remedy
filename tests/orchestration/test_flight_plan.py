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


class TestRenderPlanMd:

    def test_deterministic_output(self):
        from packages.orchestration.flight_plan import render_plan_md

        fp = FlightPlan(**json.loads(_valid_plan_json(3)))
        r1 = render_plan_md(fp)
        r2 = render_plan_md(fp)
        assert r1 == r2
        assert "# Flight Plan" in r1
        assert "T001" in r1
        assert "T002" in r1
        assert "T003" in r1

    def test_contains_acceptance_and_bands(self):
        from packages.orchestration.flight_plan import render_plan_md

        fp = FlightPlan(**json.loads(_valid_plan_json(2)))
        md = render_plan_md(fp)
        assert "Thing 1 done" in md
        assert "**Band:** M" in md

    def test_large_plan_note(self):
        from packages.orchestration.flight_plan import render_plan_md
        from packages.orchestration.schemas.models import _LARGE_PLAN_THRESHOLD

        n = _LARGE_PLAN_THRESHOLD + 1
        tasks = []
        for i in range(n):
            tasks.append({
                "id": f"T{i:03d}", "title": f"T{i}", "goal": f"G{i}",
                "acceptance": ["ok"], "depends_on": [],
                "est_tokens_band": "S", "files_hint": [],
            })
        fp = FlightPlan(schema_v="flight_plan_v1", tasks=tasks, risks=[])
        md = render_plan_md(fp)
        assert "Consider splitting" in md

    def test_risks_rendered(self):
        from packages.orchestration.flight_plan import render_plan_md

        fp = FlightPlan(**json.loads(_valid_plan_json(1)))
        md = render_plan_md(fp)
        assert "timeline risk" in md

    def test_write_plan_md(self, tmp_path):
        from packages.orchestration.flight_plan import write_plan_md

        fp = FlightPlan(**json.loads(_valid_plan_json(2)))
        path = write_plan_md(fp, tmp_path)
        assert path.name == "plan.md"
        assert path.exists()
        assert "Flight Plan" in path.read_text()

    def test_write_plan_md_versioned(self, tmp_path):
        from packages.orchestration.flight_plan import write_plan_md

        fp = FlightPlan(**json.loads(_valid_plan_json(1)))
        p1 = write_plan_md(fp, tmp_path, version=1)
        p2 = write_plan_md(fp, tmp_path, version=2)
        assert p1.name == "plan.md"
        assert p2.name == "plan_v2.md"
        assert p1.exists()
        assert p2.exists()


class TestNormalizationSection:
    """F016: the approver always sees what normalization did."""

    def test_empty_record_says_no_transformations(self):
        from packages.orchestration.flight_plan import render_plan_md

        fp = FlightPlan(**json.loads(_valid_plan_json(2)))
        md = render_plan_md(fp)
        assert "## Normalization" in md
        assert "No transformations" in md

    def test_record_entries_are_rendered(self):
        from packages.orchestration.flight_plan import render_plan_md

        fp = FlightPlan(**json.loads(_valid_plan_json(2)))
        md = render_plan_md(fp, [{
            "kind": "split",
            "source_ids": ["T001"],
            "result_ids": ["T001a", "T001b"],
            "reason": "too many acceptance criteria",
        }])
        assert "**split** T001 → T001a, T001b" in md
        assert "too many acceptance criteria" in md

    def test_write_plan_md_threads_the_record(self, tmp_path):
        from packages.orchestration.flight_plan import write_plan_md

        fp = FlightPlan(**json.loads(_valid_plan_json(1)))
        path = write_plan_md(fp, tmp_path, transformations=[{
            "kind": "merge",
            "source_ids": ["T001", "T002"],
            "result_ids": ["T001"],
            "reason": "trivial neighbors",
        }])
        assert "**merge** T001, T002 → T001" in path.read_text()


class TestPlanJobLlmNormalization:
    """F016 runs at exactly one insertion point: plan_job_llm."""

    def _xl_plan_json(self) -> str:
        return json.dumps({
            "schema_v": "flight_plan_v1",
            "tasks": [{
                "id": "T001",
                "title": "Big task",
                "goal": "Do a lot",
                "acceptance": ["parser core", "runner loop", "docs page",
                               "cli flag"],
                "depends_on": [],
                "est_tokens_band": "XL",
                "files_hint": ["src/parser.py", "src/runner.py",
                               "docs/page.md", "cli/flag.py"],
            }],
            "risks": [],
        })

    def test_plan_is_normalized_and_the_record_is_carried(self):
        result = plan_job_llm(
            _fake_intake(), _fake_provider(self._xl_plan_json()))

        assert result.plan is not None
        assert [t.id for t in result.plan.tasks] == [
            "T001a", "T001b", "T001c", "T001d"]
        assert [e["kind"] for e in result.transformations] == ["split"]

    def test_disabled_config_passes_the_plan_through(self):
        from packages.orchestration.task_granularity import GranularityConfig

        result = plan_job_llm(
            _fake_intake(), _fake_provider(self._xl_plan_json()),
            granularity=GranularityConfig(enabled=False))

        assert result.plan is not None
        assert [t.id for t in result.plan.tasks] == ["T001"]
        assert result.transformations == []

    def test_a_broken_threshold_never_loses_the_plan(self, monkeypatch):
        import packages.orchestration.flight_plan as FP

        def _boom() -> None:
            raise ValueError("split_band must be one of S, M, L, XL")

        monkeypatch.setattr(FP, "granularity_config", _boom)
        result = plan_job_llm(
            _fake_intake(), _fake_provider(self._xl_plan_json()))

        assert result.plan is not None
        assert [t.id for t in result.plan.tasks] == ["T001"]
        assert [e["kind"] for e in result.transformations] == ["aborted"]
        assert "split_band" in result.transformations[0]["reason"]


class TestReplan:

    def test_replan_appends_version(self, tmp_path):
        from packages.orchestration.flight_plan import replan

        fp1 = FlightPlan(**json.loads(_valid_plan_json(2)))
        fp1_dict = fp1.model_dump()
        fp2 = FlightPlan(**json.loads(_valid_plan_json(3)))

        updated, version = replan(fp1_dict, fp2, tmp_path)
        assert version == 2
        assert updated["_version"] == 2
        assert len(updated["_versions"]) == 1
        assert (tmp_path / "plan_v2.md").exists()

    def test_replan_keeps_old_file(self, tmp_path):
        from packages.orchestration.flight_plan import replan, write_plan_md

        fp1 = FlightPlan(**json.loads(_valid_plan_json(2)))
        write_plan_md(fp1, tmp_path, version=1)
        fp1_dict = fp1.model_dump()

        fp2 = FlightPlan(**json.loads(_valid_plan_json(3)))
        replan(fp1_dict, fp2, tmp_path)

        assert (tmp_path / "plan.md").exists()
        assert (tmp_path / "plan_v2.md").exists()

    def test_replan_after_completed_task_rejected(self, tmp_path):
        import pytest

        from packages.orchestration.flight_plan import ReplanRejectedError, replan

        fp1 = FlightPlan(**json.loads(_valid_plan_json(2)))
        fp2 = FlightPlan(**json.loads(_valid_plan_json(1)))

        with pytest.raises(ReplanRejectedError, match="Cannot replan"):
            replan(fp1.model_dump(), fp2, tmp_path, any_task_completed=True)
