"""F014 — LLM-generated Flight Plan.

Turns a job's intake into a validated, DAG-structured FlightPlan via an
LLM call (with one parse retry), then maps it onto core Task objects.
Deterministic planner remains the --no-llm/provider-down fallback.
"""
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from packages.core.models import AcceptanceCheck, RunState, Task
from packages.orchestration.schemas.models import FlightPlan
from packages.orchestration.structured_outputs import StructuredOutcome, run_structured_call


@dataclass
class FlightPlanResult:
    """Result of plan_job_llm."""

    plan: FlightPlan | None
    source: str
    error_hint: str = ""
    calls: int = 0
    call_log: list[dict[str, Any]] | None = None


_PLAN_PROMPT_TEMPLATE = """\
You are a project planner. Given the intake below, produce a flight plan:
a DAG of tasks with goals, acceptance criteria, dependencies, and token
band estimates.

## Intake
{intake_json}

## Rules
- Each task needs a unique id (e.g. "T001", "T002").
- depends_on lists task ids that must complete first.
- est_tokens_band is one of: S, M, L, XL.
- acceptance must have at least one non-empty criterion per task.
- No cycles in dependencies.
- Maximum 25 tasks.
- If clarifications were present in the intake, carry them into
  clarifications_resolved with your chosen answer.

Return ONLY a JSON object matching the flight_plan_v1 schema.
"""


def _build_plan_prompt(intake_dict: dict[str, Any]) -> str:
    return _PLAN_PROMPT_TEMPLATE.format(
        intake_json=json.dumps(intake_dict, indent=2))


def plan_job_llm(
    intake: dict[str, Any],
    call_fn: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
) -> FlightPlanResult:
    """Generate a FlightPlan from a job's intake via LLM.

    Uses run_structured_call for schema validation + one parse retry.
    Returns a FlightPlanResult; on failure, plan is None and error_hint
    describes the failure class.
    """
    prompt = _build_plan_prompt(intake)
    try:
        outcome: StructuredOutcome = run_structured_call(
            FlightPlan,
            prompt,
            call_fn,
            on_call=on_call,
            allow_parse_retry=True,
        )
    except Exception as exc:
        return FlightPlanResult(
            plan=None, source="llm", error_hint=f"provider error: {exc}")

    if not outcome.ok:
        return FlightPlanResult(
            plan=None,
            source="llm",
            error_hint=outcome.hint,
            calls=outcome.calls,
            call_log=outcome.call_log,
        )

    assert isinstance(outcome.value, FlightPlan)
    return FlightPlanResult(
        plan=outcome.value,
        source="llm",
        calls=outcome.calls,
        call_log=outcome.call_log,
    )


def map_flight_plan_to_tasks(plan: FlightPlan) -> list[Task]:
    """Convert FlightPlan tasks to core Task objects, preserving order.

    Flight plan metadata is stored in task.inputs["flight"] so the
    runner and evidence pipeline can trace provenance without modifying
    the core Task model.
    """
    tasks: list[Task] = []
    for pt in plan.tasks:
        task = Task(
            description=f"{pt.title}: {pt.goal}",
            acceptance_checks=[
                AcceptanceCheck(description=ac) for ac in pt.acceptance
            ],
            inputs={
                "flight": {
                    "planned_id": pt.id,
                    "title": pt.title,
                    "depends_on": list(pt.depends_on),
                    "est_tokens_band": pt.est_tokens_band,
                    "files_hint": list(pt.files_hint),
                },
            },
            status=RunState.PENDING,
        )
        tasks.append(task)
    return tasks


def apply_plan_budgets(
    job_budgets: dict[str, Any] | None,
    plan_budgets: dict[str, int | str | None] | None,
) -> dict[str, Any] | None:
    """Merge plan-suggested budgets into job budgets (CLI/config wins).

    Returns the merged dict, or None if both inputs are None.
    Plan budgets fill only UNSET fields — explicit user values are never
    overwritten.
    """
    if plan_budgets is None:
        return job_budgets
    if job_budgets is None:
        return dict(plan_budgets)
    merged = dict(job_budgets)
    for key, val in plan_budgets.items():
        if key not in merged or merged[key] is None:
            merged[key] = val
    return merged


def apply_plan_fences(
    job_fences: dict[str, list[str]] | None,
    plan_fences: dict[str, list[str]] | None,
) -> dict[str, list[str]] | None:
    """Merge plan-suggested fences into job fences (CLI/config wins).

    Returns the merged dict, or None if both inputs are None.
    Plan fences fill only UNSET fields — explicit user values are never
    overwritten.
    """
    if plan_fences is None:
        return job_fences
    if job_fences is None:
        return dict(plan_fences)
    merged = dict(job_fences)
    for key, val in plan_fences.items():
        if key not in merged or not merged[key]:
            merged[key] = val
    return merged
