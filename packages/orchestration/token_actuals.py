"""Token/cost actuals parser for the claude CLI.

Parses the JSON emitted by ``claude --output-format json`` into a structured
``UsageActuals`` record. This is the source of *measured* token/cost data —
callers fall back to a heuristic estimate when parsing fails (returns None).
"""

from __future__ import annotations

import json
from dataclasses import dataclass


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

    try:
        payload = json.loads(stdout)
    except (ValueError, TypeError):
        return None, "parse_failed"

    if not isinstance(payload, dict):
        return None, "parse_failed"

    if payload.get("is_error"):
        return None, "is_error"

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
