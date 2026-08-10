"""Job intake module (F013 T002).

Turns a free-text mission into a validated ``JobIntake``. Two paths:

- ``run_intake``: LLM-backed structured call via ``run_structured_call``.
  On parse failure or provider error, falls to ``heuristic_intake``.
- ``heuristic_intake``: deterministic fallback (no provider needed).

Clarification truncation (A9): more than five → keep the first five, record
the drop count in ``dropped_clarifications``. The schema allows unlimited;
truncation is module-level behavior.
"""
from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel

from packages.orchestration.prompt_segments import (
    ComposedPrompt,
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)
from packages.orchestration.prompt_trace import build_trace_entry
from packages.orchestration.schemas import JOB_INTAKE_SCHEMA_V, JobIntake, to_json_schema
from packages.orchestration.structured_outputs import StructuredOutcome, run_structured_call

MAX_CLARIFICATIONS = 5
_MAX_PROMPT_MISSION_CHARS = 8000
_TRUNCATION_MARKER = "\n[...mission truncated...]"

#: Rank-0 SYSTEM segment: the one-line task statement, first in every
#: composition so the cacheable prefix starts at byte 0.
_INTAKE_SYSTEM_SEGMENT = "Analyze this mission and produce a structured job intake."

#: Rank-4 TASK segment, the only volatile part: `{mission}` is the caller's
#: mission text after `_truncate_mission`.
_INTAKE_MISSION_TEMPLATE = """\
Mission:
{mission}"""

#: Rank-1 CONVENTIONS segment: the output-field rules. Never varies per
#: call, so composing it ahead of the mission keeps it inside the prefix.
_INTAKE_RULES_SEGMENT = """\
Rules:
- goal: one clear sentence stating the objective
- context_refs: file paths, URLs, or identifiers mentioned
- constraints: explicit limitations or requirements
- acceptance_hints: how to verify completion
- truncated_input: true only if the mission text is visibly cut off
- clarifications: open questions with default answers and impact
- mission_candidate: true only if this goal plainly outlives a single job
  (ongoing upkeep, a multi-stage effort, a standing commitment). It creates
  nothing on its own — it only offers the choice to a human."""

_PATH_PATTERN = re.compile(
    r'(?:[\w.-]+/)+[\w.-]+'
    r'|'
    r'[\w][\w.-]*\.(?:py|md|js|ts|tsx|txt|yaml|yml|json|toml|html|css'
    r'|go|rs|java|rb|sh|sql|xml|csv|cfg|ini|env)\b',
)


@dataclass
class IntakeResult:
    """Result of intake processing."""

    value: JobIntake
    source: str
    error_hint: str = ""
    calls: int = 0
    schema_v: str = JOB_INTAKE_SCHEMA_V
    call_log: list[dict[str, Any]] = field(default_factory=list)


def _truncate_mission(mission: str) -> tuple[str, bool]:
    """Truncate oversized mission text for the prompt."""
    if len(mission) <= _MAX_PROMPT_MISSION_CHARS:
        return mission, False
    return mission[:_MAX_PROMPT_MISSION_CHARS] + _TRUNCATION_MARKER, True


# Rank order puts the never-changing rules block AHEAD of the mission text, so
# the cacheable prefix runs to the end of the rules instead of stopping at the
# first mission character (F105 T003 site 1). The segment BYTES are unchanged
# from the pre-migration template — only their ORDER differs, which is the
# "modulo ordering" content-equality the F105 feature file requires.
def compose_intake_prompt(mission: str) -> ComposedPrompt:
    """Compose the intake prompt from registered segments, with its manifest."""
    prompt_mission, _ = _truncate_mission(mission)
    registry = PromptSegmentRegistry()
    registry.register(
        "intake_system", SegmentStabilityRank.SYSTEM, _INTAKE_SYSTEM_SEGMENT
    )
    registry.register(
        "intake_rules", SegmentStabilityRank.CONVENTIONS, _INTAKE_RULES_SEGMENT
    )
    registry.register(
        "intake_mission",
        SegmentStabilityRank.TASK,
        _INTAKE_MISSION_TEMPLATE.format(mission=prompt_mission),
    )
    return compose_prompt_segments(registry.registered_segments())


def _build_intake_prompt(mission: str) -> str:
    """Build the intake prompt from mission text."""
    return compose_intake_prompt(mission).text


# The recorder lives beside the composer, in this module, so the manifest and
# the prompt it describes cannot drift apart: whoever changes intake composition
# sees the evidence writer in the same file (F105 T003 site 1).
def make_intake_call_recorder(
    traces: list[Any],
    composed: ComposedPrompt,
    *,
    provider: str = "",
    provider_kind: str = "",
) -> Callable[[int, str, bool, str], None]:
    """Build the ``on_call`` recorder ``run_intake`` expects.

    Every provider invocation appends one prompt trace entry to ``traces``,
    carrying ``composed``'s segment manifest so call evidence records which
    named segments produced the prompt.
    """
    def _record(
        attempt: int, schema_v: str, is_parse_retry: bool, effective_prompt: str,
    ) -> None:
        kind = "intake-retry" if is_parse_retry else "intake"
        traces.append(build_trace_entry(
            prompt_text=effective_prompt,
            role="intake",
            provider=provider,
            provider_kind=provider_kind,
            prompt_kind=kind,
            schema_v=schema_v,
            phase=kind,
            transport_attempt=attempt,
            is_transport_retry=False,
            composed_prompt=composed,
        ))

    return _record


def _first_sentence(text: str) -> str:
    """Extract the first sentence from text."""
    text = text.strip()
    for sep in (". ", ".\n", "\n"):
        idx = text.find(sep)
        if idx != -1:
            candidate = text[: idx + (1 if sep.startswith(".") else 0)].strip()
            if candidate:
                return candidate
    return text[:200].strip()


def _extract_context_refs(text: str) -> list[str]:
    """Extract file-path-like tokens from text."""
    seen: set[str] = set()
    refs: list[str] = []
    for m in _PATH_PATTERN.finditer(text):
        ref = m.group()
        if ref not in seen:
            seen.add(ref)
            refs.append(ref)
    return refs


#: Phrases that mark a goal as outliving one job (F056).  Deliberately
#: PHRASES, not single words: "keep" alone appears in half of all goals, while
#: "keep it green" is a standing commitment.  A false positive costs one extra
#: line in the approval payload; the offer still defaults to NO, and nothing is
#: created without a human yes — so the list may be generous, but the ACTION
#: never is.
_MISSION_CANDIDATE_MARKERS = (
    "ongoing", "long-term", "long term", "over time", "from now on",
    "continuously", "continuous", "keep it working", "keep it green",
    "keep working", "keep them working", "keep passing", "stay green",
    "every day", "every week", "every month", "daily", "weekly", "monthly",
    "maintain", "monitor", "watch for", "step by step", "multi-step",
    "in stages", "in phases", "phase 1", "phase one", "milestone",
    "over the next", "until it is", "until they are",
)


def mission_candidate_hint(mission: str) -> bool:
    """Does this goal smell like it outlives a single job? (F056)

    A HINT, never a decision.  A true answer only surfaces the "run as
    mission?" item in the plan-approval payload, where it defaults to NO.  No
    caller of this function creates anything.
    """
    text = str(mission).lower()
    return any(marker in text for marker in _MISSION_CANDIDATE_MARKERS)


def _truncate_clarifications(intake: JobIntake) -> JobIntake:
    """Keep at most MAX_CLARIFICATIONS, recording the drop count."""
    if len(intake.clarifications) <= MAX_CLARIFICATIONS:
        return intake
    dropped = len(intake.clarifications) - MAX_CLARIFICATIONS
    data = intake.model_dump()
    data["clarifications"] = data["clarifications"][:MAX_CLARIFICATIONS]
    data["dropped_clarifications"] = dropped
    return JobIntake.model_validate(data)


def heuristic_intake(mission: str) -> IntakeResult:
    """Deterministic fallback — no provider needed."""
    _, was_truncated = _truncate_mission(mission)
    value = JobIntake(
        schema_v="ji1",
        goal=_first_sentence(mission),
        context_refs=_extract_context_refs(mission),
        truncated_input=was_truncated,
        mission_candidate=mission_candidate_hint(mission),
    )
    return IntakeResult(value=value, source="heuristic")


def run_intake(
    mission: str,
    call_fn: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    composed: ComposedPrompt | None = None,
) -> IntakeResult:
    """LLM-backed intake with heuristic fallback on failure.

    ``composed`` lets a caller that ALREADY composed this prompt — the CLI, for
    its trace manifest — hand those exact bytes over, so one composition feeds
    both the provider and the evidence row and a manifest can no longer
    describe bytes that were never sent (R-0256). Omitted, this function
    composes for itself as it always has. The expression stays the ARGUMENT
    inside the ``try``: a raising composer becomes the heuristic fallback,
    never an escape (R-0257).
    """
    try:
        outcome: StructuredOutcome = run_structured_call(
            JobIntake,
            composed.text if composed is not None else _build_intake_prompt(mission),
            call_fn,
            on_call=on_call,
            allow_parse_retry=True,
        )
    except Exception:
        result = heuristic_intake(mission)
        result.error_hint = "provider error"
        return result

    if not outcome.ok:
        result = heuristic_intake(mission)
        result.error_hint = outcome.hint
        result.calls = outcome.calls
        result.call_log = outcome.call_log
        return result

    assert isinstance(outcome.value, JobIntake)
    value = _truncate_clarifications(outcome.value)
    _, was_truncated = _truncate_mission(mission)
    if was_truncated and not value.truncated_input:
        data = value.model_dump()
        data["truncated_input"] = True
        value = JobIntake.model_validate(data)
    return IntakeResult(
        value=value,
        source="llm",
        calls=outcome.calls,
        schema_v=outcome.schema_v,
        call_log=outcome.call_log,
    )


def make_structured_call_fn(
    model_cls: type[BaseModel],
    *,
    model: str | None = None,
) -> Callable[[str, int], str] | None:
    """Build an Ollama-backed call_fn bound to ``model_cls``, or None.

    ``model`` overrides the planner's configured model for this call_fn only —
    the F070 orchestrator role names a top-tier model through
    ``orchestrator.model`` without changing anything for any other caller.
    Omitted, the planner resolves the model exactly as it always has.

    Ollama enforces the schema NATIVELY (``format=``), so the schema bound
    here decides the SHAPE of every response the returned callable can
    produce — the prompt cannot override it. A call_fn built for one model
    therefore must never drive a structured call for another: the provider
    would answer in the bound shape and validation would fail on every
    attempt, retry included.

    Delegates to OllamaPlanner.raw_call so all Ollama config (host, model,
    temperature, num_predict) is resolved in one place.
    """
    try:
        from packages.providers.ollama_planner.provider import OllamaPlanner
        planner = OllamaPlanner(model=model) if model else OllamaPlanner()
    except Exception:
        return None

    try:
        import ollama
        ollama.Client(host=planner.host).list()
    except Exception:
        return None

    schema = to_json_schema(model_cls)

    def _call(prompt: str, attempt: int) -> str:
        return planner.raw_call(prompt, schema=schema)

    return _call


def make_provider_call_fn() -> Callable[[str, int], str] | None:
    """Build an Ollama-backed call_fn for intake, or None if unavailable."""
    return make_structured_call_fn(JobIntake)
