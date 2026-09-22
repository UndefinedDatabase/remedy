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
    except Exception:  # noqa: BLE001 — provider failure falls back to the heuristic intake
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


#: The planner services ``make_structured_call_fn`` can build. ``None`` is not
#: listed because it is not a service: it means "ask the planner role", which
#: answers one of these. Spelled ONCE so the factory, the CLI flag's refusal and
#: the tests cannot come to disagree about what is legal.
PLANNER_PROVIDERS: tuple[str, ...] = ("ollama", "claude-cli")


def resolve_planner_target(
    provider: str | None = None, model: str | None = None,
) -> tuple[str, str | None]:
    """``(provider, model)`` for a planner call — the ONE place that decision is made.

    ``provider`` is an explicit choice (``--planner-provider``) and wins.
    ``None`` asks the ``planner`` role, whose built-in default is ``ollama``
    (packages/orchestration/role_config.py), so an unconfigured repository
    resolves exactly what it resolved before this function existed.

    The answered MODEL is ``None`` unless something actually named one — the
    ``model`` argument, or ``planner.model`` in the configuration. ``None`` is
    not a missing answer: it means "let the selected planner resolve its own
    default", which for Ollama still includes ``ollama.planner.model`` and the
    two ``REMEDY_OLLAMA_*`` variables its provider has always read. Answering a
    model here in that case would silently take that resolution away.

    Raises:
        ValueError: ``provider`` is neither ``None`` nor a member of
            :data:`PLANNER_PROVIDERS`. An unknown planner is a refusal, never a
            quiet fall back to the other one.
    """
    from packages.orchestration.config import get_config
    from packages.orchestration.role_config import resolve_role_config

    if provider is not None and provider not in PLANNER_PROVIDERS:
        raise ValueError(
            f"Unknown planner provider {provider!r}; "
            f"the planners are {', '.join(PLANNER_PROVIDERS)}."
        )

    cfg = get_config()
    configured_model = cfg.get("planner.model")
    resolved_model = model or (configured_model if configured_model else None)

    if provider is not None:
        return provider, resolved_model

    overrides: dict[str, str] = {}
    configured_provider = cfg.get("planner.provider")
    if configured_provider:
        overrides["provider"] = str(configured_provider)
    role_cfg = resolve_role_config("planner", config_file=overrides)
    resolved_provider = role_cfg.provider
    if resolved_provider not in PLANNER_PROVIDERS:
        raise ValueError(
            f"planner.provider is {resolved_provider!r}, which is not a planner; "
            f"the planners are {', '.join(PLANNER_PROVIDERS)}."
        )
    return resolved_provider, resolved_model


def make_structured_call_fn(
    model_cls: type[BaseModel],
    *,
    model: str | None = None,
    provider: str | None = None,
) -> Callable[[str, int], str] | None:
    """Build a planner-backed call_fn bound to ``model_cls``, or None.

    ``provider`` names the planning SERVICE: ``"ollama"``, ``"claude-cli"``, or
    ``None`` to take the ``planner`` role's own answer (operator amendment
    amend0920-selfuse-real, DECISION D1). That role's built-in default is
    ``ollama``, so ``provider=None`` on an unconfigured repository builds
    exactly the call_fn this factory built before a second planner existed.

    ``model`` overrides the planner's configured model for this call_fn only —
    the F070 orchestrator role names a top-tier model through
    ``orchestrator.model`` without changing anything for any other caller.
    Omitted, the planner resolves the model exactly as it always has.

    THE SCHEMA BOUND HERE DECIDES THE SHAPE OF EVERY RESPONSE the returned
    callable can produce, whichever planner serves: Ollama enforces it
    NATIVELY (``format=``) and the Claude CLI planner states it in the system
    text and validates the reply itself. A call_fn built for one model
    therefore must never drive a structured call for another: the provider
    would answer in the bound shape and validation would fail on every
    attempt, retry included.

    ANSWERS ``None`` WHEN THE SELECTED PLANNER IS NOT REACHABLE — an Ollama
    server that does not list, a ``claude`` CLI that is not on PATH — and the
    caller plans deterministically instead. It does NOT fall back to the other
    planner: a run that silently changes which service planned it is a run
    whose evidence lies about itself.

    Raises:
        ValueError: ``provider`` is not a member of :data:`PLANNER_PROVIDERS`.
    """
    planner_provider, planner_model = resolve_planner_target(provider, model)

    if planner_provider == "claude-cli":
        import shutil

        try:
            from packages.providers.claude_planner.provider import ClaudeCliPlanner
            planner: Any = (
                ClaudeCliPlanner(model=planner_model)
                if planner_model else ClaudeCliPlanner()
            )
        except Exception:  # noqa: BLE001 — unreachable planner is reported as absent, not a crash
            return None
        if not shutil.which("claude"):
            return None
    else:
        try:
            from packages.providers.ollama_planner.provider import OllamaPlanner
            planner = (
                OllamaPlanner(model=planner_model)
                if planner_model else OllamaPlanner()
            )
        except Exception:  # noqa: BLE001 — unreachable planner is reported as absent, not a crash
            return None

        try:
            import ollama
            ollama.Client(host=planner.host).list()
        except Exception:  # noqa: BLE001 — ollama server not reachable; report the planner as absent
            return None

    schema = to_json_schema(model_cls)

    def _call(prompt: str, attempt: int) -> str:
        return planner.raw_call(prompt, schema=schema)

    # F082 T003b (DECISION F082 D8): the model this call_fn will ACTUALLY serve
    # with, read off the instance that serves it rather than re-resolved from
    # config — a configured model is not the model that ran, the same rule
    # `token_ledger.py::call_record_from_evidence` keeps for its own column.
    # Readers use `getattr(fn, "resolved_model", None)`, so an unlabelled
    # call_fn reads as an absence and never as a default name.
    _call.resolved_model = planner.model  # type: ignore[attr-defined]
    return _call


def make_provider_call_fn() -> Callable[[str, int], str] | None:
    """Build an Ollama-backed call_fn for intake, or None if unavailable."""
    return make_structured_call_fn(JobIntake)
