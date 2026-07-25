"""Token/cost actuals parser for the claude CLI.

Parses the JSON emitted by ``claude --output-format json`` into a structured
``UsageActuals`` record. This is the source of *measured* token/cost data —
callers fall back to a heuristic estimate when parsing fails (returns None).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class UsageActuals:
    """Measured token/cost usage parsed from a claude CLI result.

    input_tokens:    Prompt tokens (non-cached) reported in the usage block.
    output_tokens:   Generated tokens reported in the usage block.
    cache_read:      Tokens read from the prompt cache (0 if not reported).
    cache_creation:  Tokens written to the prompt cache (0 if not reported).
    total_cost_usd:  Total cost in USD for the turn (None if not reported).
    num_turns:       Number of agent turns (0 if not reported).
    duration_ms:     Wall-clock duration in milliseconds (0 if not reported).
    session_id:      CLI session identifier ("" if not reported).
    cli_version:     CLI version string if present, for drift detection.
    """

    input_tokens: int
    output_tokens: int
    cache_read: int
    cache_creation: int
    total_cost_usd: float | None
    num_turns: int
    duration_ms: int
    session_id: str
    cli_version: str | None = None


def parse_cli_result(stdout: str) -> UsageActuals | None:
    """Parse claude CLI JSON output.

    Returns None on parse failure (caller falls back to heuristic). Never raises.
    Use ``parse_cli_result_detailed`` when the failure reason matters.
    """
    actuals, _reason = parse_cli_result_detailed(stdout)
    return actuals


def parse_cli_result_detailed(stdout: str) -> tuple[UsageActuals | None, str]:
    """Parse claude CLI JSON output with a failure reason.

    Returns ``(UsageActuals, "ok")`` on success.  On failure returns
    ``(None, reason)`` where *reason* is one of:

    - ``"empty_input"``   — empty or whitespace-only stdout
    - ``"parse_failed"``  — stdout is not valid JSON
    - ``"is_error"``      — CLI reported ``is_error: true``
    - ``"usage_missing"`` — valid JSON but no usable ``usage`` block
    """
    if not stdout or not stdout.strip():
        return None, "empty_input"

    env = parse_cli_envelope(stdout)
    if not env.is_json:
        return None, "parse_failed"
    # Accepted F003 semantics: is_error hides Usage from this legacy entry point.
    # The structured path uses ``parse_cli_envelope`` directly to retain Usage.
    if env.is_error:
        return None, "is_error"
    if env.usage_actuals is None:
        return None, env.usage_reason
    return env.usage_actuals, "ok"


#: Claude Code result subtype signalling native structured-output retry
#: exhaustion — a schema/validation (parse) failure, not a transport error.
STRUCTURED_RETRY_EXHAUSTED_SUBTYPE = "error_max_structured_output_retries"


def _usage_from_payload(payload: dict) -> tuple[UsageActuals | None, str]:
    """Extract UsageActuals from an envelope dict, independent of is_error.

    Returns ``(UsageActuals, "ok")`` or ``(None, reason)``. A failed structured
    call still consumed tokens, so Usage is read whenever the block is valid —
    the caller decides whether the call succeeded.
    """
    usage = payload.get("usage")
    if not isinstance(usage, dict):
        return None, "usage_missing"
    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    if input_tokens is None or output_tokens is None:
        return None, "usage_missing"

    raw_cost = payload.get("total_cost_usd")
    if raw_cost is not None and not isinstance(raw_cost, bool):
        try:
            cost: float | None = float(raw_cost)
        except (ValueError, TypeError):
            cost = None
    else:
        cost = None

    try:
        return UsageActuals(
            input_tokens=int(input_tokens),
            output_tokens=int(output_tokens),
            cache_read=int(usage.get("cache_read_input_tokens", 0) or 0),
            cache_creation=int(usage.get("cache_creation_input_tokens", 0) or 0),
            total_cost_usd=cost,
            num_turns=int(payload.get("num_turns", 0) or 0),
            duration_ms=int(payload.get("duration_ms", 0) or 0),
            session_id=str(payload.get("session_id", "") or ""),
            cli_version=payload.get("cli_version"),
        ), "ok"
    except (ValueError, TypeError):
        return None, "parse_failed"


@dataclass
class CliEnvelope:
    """A once-parsed Claude CLI JSON result envelope.

    Parsing the envelope in ONE place lets the JSON and stream paths agree on the
    provider value, the Usage/cost, and the error classification instead of
    re-parsing the same JSON independently.
    """

    is_json: bool
    subtype: str = ""
    is_error: bool = False
    #: The native structured-output object (``structured_output``), or None.
    structured_output: Any = None
    has_structured_output: bool = False
    #: Legacy string ``result`` field ("" if absent / non-string).
    result_text: str = ""
    usage_actuals: UsageActuals | None = None
    usage_reason: str = "usage_missing"
    errors: list = field(default_factory=list)

    @property
    def structured_retry_exhausted(self) -> bool:
        return self.subtype == STRUCTURED_RETRY_EXHAUSTED_SUBTYPE


def parse_cli_envelope(stdout: str) -> CliEnvelope:
    """Parse a claude CLI JSON envelope once into a typed record. Never raises."""
    if not stdout or not stdout.strip():
        return CliEnvelope(is_json=False)
    try:
        payload = json.loads(stdout)
    except (ValueError, TypeError):
        return CliEnvelope(is_json=False)
    if not isinstance(payload, dict):
        return CliEnvelope(is_json=False)

    usage, usage_reason = _usage_from_payload(payload)
    so = payload.get("structured_output")
    has_so = "structured_output" in payload and so is not None
    result_field = payload.get("result")
    result_text = result_field if isinstance(result_field, str) else ""
    errs = payload.get("errors")
    return CliEnvelope(
        is_json=True,
        subtype=str(payload.get("subtype", "") or ""),
        is_error=bool(payload.get("is_error", False)),
        structured_output=so if has_so else None,
        has_structured_output=has_so,
        result_text=result_text,
        usage_actuals=usage,
        usage_reason=usage_reason,
        errors=list(errs) if isinstance(errs, list) else [],
    )
