"""Tests for FlightPlan schema + DAG validation (F014 T001)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from packages.orchestration.schemas.models import (
    _LARGE_PLAN_THRESHOLD,
    FLIGHT_PLAN_SCHEMA_V,
    FlightPlan,
    FlightPlanClarification,
    PlannedTask,
)


def _task(tid: str = "T1", **overrides) -> dict:
    base = {
        "id": tid,
        "title": f"Task {tid}",
        "goal": f"Do {tid}",
        "acceptance": [f"{tid} done"],
        "depends_on": [],
        "est_tokens_band": "M",
        "files_hint": [],
    }
    base.update(overrides)
    return base


def _plan(**overrides) -> dict:
    base = {
        "schema_v": "flight_plan_v1",
        "tasks": [_task()],
        "risks": [],
    }
    base.update(overrides)
    return base


class TestFlightPlanRoundTrip:

    def test_minimal_plan_roundtrips(self):
        fp = FlightPlan(**_plan())
        assert fp.schema_v == "flight_plan_v1"
        assert fp.SCHEMA_V == FLIGHT_PLAN_SCHEMA_V
        assert len(fp.tasks) == 1
        assert fp.tasks[0].id == "T1"
        d = fp.model_dump()
        fp2 = FlightPlan(**d)
        assert fp2.tasks[0].goal == fp.tasks[0].goal

    def test_full_plan_with_all_fields(self):
        fp = FlightPlan(**_plan(
            tasks=[
                _task("T1"),
                _task("T2", depends_on=["T1"]),
            ],
            risks=["timeline risk"],
            clarifications_resolved=[{
                "question": "Which DB?",
                "default_answer": "postgres",
                "impact": "driver choice",
                "answer": "postgres",
            }],
            budgets={"max_total_tokens": 50000},
            fences={"allow": ["src/**"]},
        ))
        assert len(fp.tasks) == 2
        assert fp.tasks[1].depends_on == ["T1"]
        assert len(fp.clarifications_resolved) == 1
        assert fp.budgets == {"max_total_tokens": 50000}
        assert fp.fences == {"allow": ["src/**"]}


class TestDAGValidation:

    def test_duplicate_task_id_rejected(self):
        with pytest.raises(ValidationError, match="duplicate task id"):
            FlightPlan(**_plan(tasks=[_task("T1"), _task("T1")]))

    def test_unknown_dependency_rejected(self):
        with pytest.raises(ValidationError, match="unknown id"):
            FlightPlan(**_plan(tasks=[
                _task("T1", depends_on=["T99"]),
            ]))

    def test_cycle_rejected(self):
        with pytest.raises(ValidationError, match="cycle"):
            FlightPlan(**_plan(tasks=[
                _task("T1", depends_on=["T2"]),
                _task("T2", depends_on=["T1"]),
            ]))

    def test_self_cycle_rejected(self):
        with pytest.raises(ValidationError, match="cycle"):
            FlightPlan(**_plan(tasks=[
                _task("T1", depends_on=["T1"]),
            ]))

    def test_three_node_cycle_rejected(self):
        with pytest.raises(ValidationError, match="cycle"):
            FlightPlan(**_plan(tasks=[
                _task("T1", depends_on=["T3"]),
                _task("T2", depends_on=["T1"]),
                _task("T3", depends_on=["T2"]),
            ]))

    def test_diamond_dag_accepted(self):
        fp = FlightPlan(**_plan(tasks=[
            _task("T1"),
            _task("T2", depends_on=["T1"]),
            _task("T3", depends_on=["T1"]),
            _task("T4", depends_on=["T2", "T3"]),
        ]))
        assert len(fp.tasks) == 4


class TestTaskCap:

    def test_26_tasks_rejected(self):
        tasks = [_task(f"T{i:02d}") for i in range(26)]
        with pytest.raises(ValidationError, match="cap"):
            FlightPlan(**_plan(tasks=tasks))

    def test_25_tasks_accepted(self):
        tasks = [_task(f"T{i:02d}") for i in range(25)]
        fp = FlightPlan(**_plan(tasks=tasks))
        assert len(fp.tasks) == 25

    def test_13_tasks_sets_large_plan_flag(self):
        n = _LARGE_PLAN_THRESHOLD + 1
        tasks = [_task(f"T{i:02d}") for i in range(n)]
        fp = FlightPlan(**_plan(tasks=tasks))
        assert fp.large_plan is True

    def test_12_tasks_no_large_plan_flag(self):
        tasks = [_task(f"T{i:02d}") for i in range(_LARGE_PLAN_THRESHOLD)]
        fp = FlightPlan(**_plan(tasks=tasks))
        assert fp.large_plan is False


class TestFieldValidation:

    def test_empty_acceptance_rejected(self):
        with pytest.raises(ValidationError):
            FlightPlan(**_plan(tasks=[_task("T1", acceptance=[])]))

    def test_whitespace_only_acceptance_rejected(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            FlightPlan(**_plan(tasks=[_task("T1", acceptance=["  "])]))

    def test_invalid_band_rejected(self):
        with pytest.raises(ValidationError):
            FlightPlan(**_plan(tasks=[
                _task("T1", est_tokens_band="XXL"),
            ]))

    def test_valid_bands_accepted(self):
        for band in ("S", "M", "L", "XL"):
            fp = FlightPlan(**_plan(tasks=[
                _task("T1", est_tokens_band=band),
            ]))
            assert fp.tasks[0].est_tokens_band == band

    def test_wrong_schema_v_rejected(self):
        with pytest.raises(ValidationError):
            FlightPlan(**_plan(schema_v="pp1"))

    def test_empty_tasks_rejected(self):
        with pytest.raises(ValidationError):
            FlightPlan(**_plan(tasks=[]))

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            FlightPlan(**_plan(secret="hack"))


class TestPlannedTaskModel:

    def test_roundtrip(self):
        t = PlannedTask(**_task("T1"))
        assert t.id == "T1"
        assert t.est_tokens_band == "M"

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            PlannedTask(**_task("T1", bonus="nope"))


class TestClarificationModel:

    def test_roundtrip(self):
        c = FlightPlanClarification(
            question="Q?", default_answer="A", impact="I", answer="A")
        assert c.question == "Q?"
        assert c.answer == "A"

    def test_missing_answer_rejected(self):
        with pytest.raises(ValidationError):
            FlightPlanClarification(
                question="Q?", default_answer="A", impact="I")
