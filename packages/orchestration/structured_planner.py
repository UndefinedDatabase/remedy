"""Structured planner path (F005 T003).

Wraps a raw-text planner call into a ``call_planner`` callable that enforces the
``PlannerPlan`` schema: it sends the JSON schema (with a compact ``schema_v``),
validates the response, and performs at most one parse retry carrying a concise
hint. A response that is still invalid after the single retry raises a
:class:`StructuredParseError` (error class ``parse``) — never an unbounded loop.

The validated ``PlannerPlan`` is mapped to the existing ``PlannerOutput`` so the
downstream planning contract in ``llm_planner`` is unchanged (anti-goal A6: no
second planner taxonomy). The legacy planner call stays reachable behind the
compatibility flag; per the feature document it is not removed until at least
five deterministic green planner runs are recorded.
"""
from __future__ import annotations

from typing import Callable

from packages.orchestration.planner_models import PlannerOutput, ProposedTask
from packages.orchestration.schemas import PARSE_ERROR_CLASS, PlannerPlan
from packages.orchestration.structured_outputs import (
    planner_structured_enabled,
    run_structured_call,
)

__all__ = [
    "StructuredParseError",
    "plan_to_planner_output",
    "make_structured_planner",
    "planner_structured_enabled",
]


class StructuredParseError(RuntimeError):
    """A planner response that stayed invalid after the single parse retry."""

    error_class = PARSE_ERROR_CLASS

    def __init__(self, hint: str, schema_v: str, calls: int) -> None:
        super().__init__(f"planner parse failure ({schema_v}): {hint}")
        self.hint = hint
        self.schema_v = schema_v
        self.calls = calls


def plan_to_planner_output(plan: PlannerPlan) -> PlannerOutput:
    """Map a validated PlannerPlan onto the existing PlannerOutput shape."""
    return PlannerOutput(
        summary=plan.summary,
        proposed_tasks=[
            ProposedTask(task_type=t.task_type, description=t.description)
            for t in plan.proposed_tasks
        ],
        acceptance_checks=list(plan.acceptance_checks),
        notes=list(plan.notes),
    )


def make_structured_planner(
    raw_call: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    native_schema: bool = False,
) -> Callable[[str], PlannerOutput]:
    """Build a ``call_planner`` that enforces the PlannerPlan schema.

    ``raw_call(prompt, attempt_index)`` returns the raw provider text.
    ``on_call(attempt, schema_v, is_parse_retry, effective_prompt)`` fires
    IMMEDIATELY BEFORE every real call, so its prompt-trace entry survives even a
    provider/network exception. ``native_schema`` is set when the
    provider enforces the schema out-of-band (Ollama ``format=``), so the prompt
    carries only a short instruction. The returned callable matches
    ``llm_planner.plan_job_with_llm``'s ``call_planner`` type.
    """

    def _call_planner(prompt: str) -> PlannerOutput:
        outcome = run_structured_call(
            PlannerPlan, prompt, raw_call,
            on_call=on_call, allow_parse_retry=True, native_schema=native_schema,
        )
        if not outcome.ok:
            raise StructuredParseError(outcome.hint, outcome.schema_v, outcome.calls)
        assert isinstance(outcome.value, PlannerPlan)
        return plan_to_planner_output(outcome.value)

    return _call_planner
