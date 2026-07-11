"""Validation primitive for enforced structured outputs (F005).

A single, deterministic entry point turns a raw provider response into either a
validated model or a classified ``parse`` failure carrying a concise hint. The
hint is what a caller may include in its single parse retry — nothing more.

The rules this module enforces (the loop wiring lives with each provider path):
  * invalid data is error class ``parse`` — never anything else;
  * the hint is short and mentions the failing fields, so a retry is cheap;
  * an unsupported ``schema_v`` is just another validation failure.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, ValidationError

#: The one error class F005 uses for a bad structured response.
PARSE_ERROR_CLASS = "parse"

#: Keep retry hints cheap: at most this many field errors, each clipped.
_MAX_HINT_ERRORS = 3
_MAX_HINT_CHARS = 240


@dataclass
class ValidationResult:
    """Outcome of validating one structured response."""

    ok: bool
    value: BaseModel | None = None
    error_class: str = ""
    hint: str = ""
    #: Set when the response was not even JSON (vs. valid JSON that failed the model).
    json_error: bool = False
    errors: list[dict[str, Any]] = field(default_factory=list)


def to_json_schema(model_cls: type[BaseModel]) -> dict[str, Any]:
    """Return the JSON schema a provider call should send for ``model_cls``."""
    return model_cls.model_json_schema()


def to_json_schema_str(model_cls: type[BaseModel]) -> str:
    """Compact JSON-schema string for the wire and for size snapshots."""
    return json.dumps(to_json_schema(model_cls), separators=(",", ":"), sort_keys=True)


def _extract_json_object(raw: str) -> tuple[Any, str]:
    """Best-effort single-object extraction: strip fences, take outermost {...}.

    Returns ``(obj, "")`` on success or ``(None, reason)`` on failure. This is
    lenient about surrounding prose but never "repairs" the JSON itself — a
    malformed object is a parse failure, not something to guess at.
    """
    text = raw.strip()
    if text.startswith("```"):
        newline = text.find("\n")
        if newline != -1:
            text = text[newline + 1 :]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
        text = text.strip()

    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None, "no JSON object found in response"
    try:
        return json.loads(text[start : end + 1]), ""
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc.msg} at pos {exc.pos}"


def _hint_from_errors(errors: list[dict[str, Any]]) -> str:
    """Concise, field-oriented hint from pydantic validation errors."""
    parts: list[str] = []
    for err in errors[:_MAX_HINT_ERRORS]:
        loc = ".".join(str(p) for p in err.get("loc", ())) or "(root)"
        msg = str(err.get("msg", "invalid"))
        parts.append(f"{loc}: {msg}")
    hint = "; ".join(parts)
    if len(errors) > _MAX_HINT_ERRORS:
        hint += f"; (+{len(errors) - _MAX_HINT_ERRORS} more)"
    return hint[:_MAX_HINT_CHARS]


def validate_response(model_cls: type[BaseModel], raw: Any) -> ValidationResult:
    """Validate a raw provider response against ``model_cls``.

    ``raw`` may be a JSON string (possibly fenced / wrapped in prose) or an
    already-parsed object. Any failure is classified as ``parse`` with a concise
    hint suitable for a single retry.
    """
    if isinstance(raw, str):
        obj, reason = _extract_json_object(raw)
        if reason:
            return ValidationResult(
                ok=False, error_class=PARSE_ERROR_CLASS, hint=reason, json_error=True,
            )
    else:
        obj = raw

    try:
        value = model_cls.model_validate(obj)
    except ValidationError as exc:
        errs = exc.errors()
        return ValidationResult(
            ok=False,
            error_class=PARSE_ERROR_CLASS,
            hint=_hint_from_errors(errs),
            errors=errs,
        )
    return ValidationResult(ok=True, value=value)
