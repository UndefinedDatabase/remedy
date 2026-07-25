"""Enforced structured-output call engine (F005).

One deterministic helper drives a structured provider call: it appends the JSON
schema instruction, validates the response against the model, and on a bad
response performs AT MOST ONE parse retry carrying only a concise validation
hint. There is never an unbounded repair loop.

The engine is provider-agnostic — it is driven by an injected ``call_fn`` — so
every scenario can be exercised with fake providers and recorded outputs, with
no provider tokens spent.

Reviewer vs planner ownership of the retry:
  * The planner has no existing retry, so it uses this engine directly and the
    engine owns the single retry.
  * The reviewer's single parse retry already lives in the ping-pong loop (so the
    retry is recorded as its own provider attempt and token/call accounting stays
    correct). The reviewer path therefore uses :func:`build_schema_prompt` and
    :func:`schemas.validate_response` for one call at a time and lets the loop do
    the one retry — it does NOT double-retry here.
"""
from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel

from packages.orchestration.schemas import (
    PARSE_ERROR_CLASS,
    ValidationResult,
    schema_v_of,
    to_json_schema_str,
    validate_response,
)

#: Compatibility flags. Structured mode is ON by default; the legacy free-text
#: path is reachable only by explicitly opting out. Schema mode never silently
#: falls back to free-text parsing.
_REVIEWER_FREETEXT_ENV = "REMEDY_REVIEWER_FREETEXT"
_PLANNER_FREETEXT_ENV = "REMEDY_PLANNER_FREETEXT"


def _flag_on(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def reviewer_structured_enabled() -> bool:
    """True unless the reviewer legacy free-text compatibility flag is set."""
    return not _flag_on(_REVIEWER_FREETEXT_ENV)


def planner_structured_enabled() -> bool:
    """True unless the planner legacy compatibility flag is set."""
    return not _flag_on(_PLANNER_FREETEXT_ENV)


#: Short instruction used when the provider enforces the schema NATIVELY (e.g.
#: Claude CLI ``--json-schema``). The full schema is NOT duplicated into the
#: prompt in that case — the provider already has it.
NATIVE_SCHEMA_INSTRUCTION = "Return ONLY the schema-compliant JSON result."


def native_schema_prompt(base_prompt: str, hint: str = "") -> str:
    """Prompt for native-schema mode: base + a short instruction, no schema prose."""
    prompt = f"{base_prompt}\n\n{NATIVE_SCHEMA_INSTRUCTION}"
    if hint:
        prompt += (
            f"\n\nYour previous response was invalid: {hint}\n"
            "Return ONLY the corrected JSON object."
        )
    return prompt


def schema_instruction(model_cls: type[BaseModel]) -> str:
    """Compact instruction block appended to a structured provider prompt."""
    schema_v = schema_v_of(model_cls)
    return (
        "Return ONLY one JSON object, no markdown and no prose, valid against "
        f"this JSON schema (schema_v={schema_v}):\n{to_json_schema_str(model_cls)}"
    )


def build_schema_prompt(model_cls: type[BaseModel], base_prompt: str, hint: str = "") -> str:
    """Base prompt + schema instruction, optionally carrying a concise retry hint."""
    prompt = f"{base_prompt}\n\n{schema_instruction(model_cls)}"
    if hint:
        prompt += (
            f"\n\nYour previous response was invalid: {hint}\n"
            "Return ONLY the corrected JSON object."
        )
    return prompt


@dataclass
class StructuredOutcome:
    """Result of a structured call, including its single optional parse retry."""

    ok: bool
    value: BaseModel | None
    error_class: str
    hint: str
    schema_v: str
    calls: int
    parse_retried: bool
    last_text: str
    #: One entry per underlying provider call, in order (for accounting).
    call_log: list[dict[str, Any]] = field(default_factory=list)


def run_structured_call(
    model_cls: type[BaseModel],
    base_prompt: str,
    call_fn: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    allow_parse_retry: bool = True,
    native_schema: bool = False,
) -> StructuredOutcome:
    """Drive a structured call with AT MOST one parse retry.

    The single-retry maximum is a hard safety rule, not a caller convention:
    ``allow_parse_retry`` is a boolean, so no caller can request more than one
    retry and three-or-more calls are impossible through this helper. A truthy
    non-bool is clamped to one retry; a falsey value disables the retry entirely.

    ``call_fn(prompt, attempt_index)`` returns the raw provider text.

    ``on_call(attempt, schema_v, is_parse_retry, effective_prompt)`` — when given —
    runs IMMEDIATELY BEFORE every real ``call_fn()`` invocation, so a caller
    records exactly one prompt-trace entry per ACTUAL provider call. Because it
    fires first, the trace survives a provider/network exception raised by
    ``call_fn`` (F005: every real call logs its ``schema_v``).

    ``native_schema`` selects the prompt shape: when the provider enforces the
    schema out-of-band (Ollama ``format=`` / Claude ``--json-schema``) the prompt
    carries only a short instruction, not a duplicated full schema.

    Any invalid response is classified as ``parse``; the last attempt's hint is
    returned.
    """
    schema_v = schema_v_of(model_cls)
    hint = ""
    last_text = ""
    call_log: list[dict[str, Any]] = []
    # Hard ceiling: 1 call, or 2 when a retry is allowed. Never more.
    total = 2 if allow_parse_retry else 1

    for attempt in range(total):
        carry = hint if attempt else ""
        if native_schema:
            prompt = native_schema_prompt(base_prompt, carry)
        else:
            prompt = build_schema_prompt(model_cls, base_prompt, carry)
        if on_call is not None:
            on_call(attempt + 1, schema_v, attempt > 0, prompt)
        last_text = call_fn(prompt, attempt)
        res: ValidationResult = validate_response(model_cls, last_text)
        call_log.append({
            "attempt": attempt + 1,
            "schema_v": schema_v,
            "ok": res.ok,
            "is_parse_retry": attempt > 0,
        })
        if res.ok:
            return StructuredOutcome(
                ok=True, value=res.value, error_class="", hint="", schema_v=schema_v,
                calls=attempt + 1, parse_retried=attempt > 0, last_text=last_text,
                call_log=call_log,
            )
        hint = res.hint

    return StructuredOutcome(
        ok=False, value=None, error_class=PARSE_ERROR_CLASS, hint=hint,
        schema_v=schema_v, calls=total, parse_retried=total > 1, last_text=last_text,
        call_log=call_log,
    )
