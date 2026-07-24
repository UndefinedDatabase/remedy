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

from packages.orchestration.schemas import JOB_INTAKE_SCHEMA_V, JobIntake, to_json_schema
from packages.orchestration.structured_outputs import StructuredOutcome, run_structured_call

MAX_CLARIFICATIONS = 5
_MAX_PROMPT_MISSION_CHARS = 8000
_TRUNCATION_MARKER = "\n[...mission truncated...]"

_INTAKE_PROMPT_TEMPLATE = """\
Analyze this mission and produce a structured job intake.

Mission:
{mission}

Rules:
- goal: one clear sentence stating the objective
- context_refs: file paths, URLs, or identifiers mentioned
- constraints: explicit limitations or requirements
- acceptance_hints: how to verify completion
- truncated_input: true only if the mission text is visibly cut off
- clarifications: open questions with default answers and impact"""

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


def _build_intake_prompt(mission: str) -> str:
    """Build the intake prompt from mission text."""
    prompt_mission, _ = _truncate_mission(mission)
    return _INTAKE_PROMPT_TEMPLATE.format(mission=prompt_mission)


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
    )
    return IntakeResult(value=value, source="heuristic")


def run_intake(
    mission: str,
    call_fn: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
) -> IntakeResult:
    """LLM-backed intake with heuristic fallback on failure."""
    try:
        outcome: StructuredOutcome = run_structured_call(
            JobIntake,
            _build_intake_prompt(mission),
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
    return IntakeResult(
        value=value,
        source="llm",
        calls=outcome.calls,
        schema_v=outcome.schema_v,
        call_log=outcome.call_log,
    )


def make_provider_call_fn() -> Callable[[str, int], str] | None:
    """Build an Ollama-backed call_fn for intake, or None if unavailable.

    Reuses the same host/model config surface as OllamaPlanner (env vars,
    config file) but sends the intake prompt directly — no planner-specific
    system prompt wrapping. Uses Ollama's native ``format=`` for schema
    enforcement.
    """
    try:
        import ollama
    except ImportError:
        return None

    try:
        import os

        from packages.orchestration.config import get_config

        cfg = get_config()
        host = (
            os.environ.get("REMEDY_OLLAMA_HOST")
            or cfg.get("ollama.host")
            or "http://localhost:11434"
        )
        model = (
            os.environ.get("REMEDY_OLLAMA_PLANNER_MODEL")
            or os.environ.get("REMEDY_OLLAMA_MODEL")
            or cfg.get("ollama.planner.model")
            or "qwen3-coder-next"
        )
        client = ollama.Client(host=host, timeout=15.0)
        schema = to_json_schema(JobIntake)
        client.list()
    except Exception:
        return None

    def _call(prompt: str, attempt: int) -> str:
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            format=schema,
        )
        return response.message.content

    return _call
