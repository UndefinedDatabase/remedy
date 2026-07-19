"""Round 31 F2 — the authoritative token-truth validator and token-status regeneration.

``token_truth.json`` is a trust-bearing artifact: ``final_verifier._token_status`` derives the entire
``token_status`` from it, which then drives ``token_measurement`` and the review gate. So a token truth
that is claimed present must be a valid, nonempty, typed object with coherent counts/costs/coverage —
an empty/whitespace/malformed/wrong-root/enum-violating record must not silently produce a
zeroed-out "clean" status. This module is the single validator, consumed by the manual-completion
validator (and available to the producer), so packaging and the verifier share one notion of a valid
token truth.

Pure; no provider, no filesystem, no network.
"""
from __future__ import annotations

from typing import Any

#: The only token-truth schema version this build reads.
SUPPORTED_TOKEN_TRUTH_VERSIONS = frozenset({"1.0.0"})
#: Supported measurement-confidence enum.
MEASUREMENT_CONFIDENCE = frozenset({"high", "mixed", "low"})
#: Supported measurement-source enum.
MEASUREMENT_SOURCE = frozenset({"provider_api", "character_heuristic"})

#: Integer count fields — must be real ints (never bool) and nonnegative.
_COUNT_FIELDS = (
    "estimated_prompt_tokens", "estimated_completion_tokens", "estimated_total_tokens",
    "builder_estimated_total", "reviewer_estimated_total", "repair_estimated_total",
    "provider_call_count", "prompt_trace_count", "actual_call_count", "cost_call_count",
)
#: Nullable nonnegative integer fields (present when measured, else null).
_NULLABLE_COUNT_FIELDS = (
    "actual_prompt_tokens", "actual_completion_tokens", "actual_total_tokens",
)


def _is_real_int(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _is_finite_number(v: Any) -> bool:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return False
    return v == v and v not in (float("inf"), float("-inf"))   # reject NaN / Infinity


def validate_token_truth(truth: Any) -> list[str]:
    """Return a list of bounded problems for a token-truth object. Empty means valid. Never raises."""
    p: list[str] = []
    if not isinstance(truth, dict):
        return ["token_truth.json is not a JSON object"]
    if not truth:
        return ["token_truth.json is empty"]
    if truth.get("schema_version") not in SUPPORTED_TOKEN_TRUTH_VERSIONS:
        p.append(f"token_truth.schema_version {truth.get('schema_version')!r} is not supported "
                 f"{sorted(SUPPORTED_TOKEN_TRUTH_VERSIONS)}")

    conf = truth.get("measurement_confidence")
    if conf not in MEASUREMENT_CONFIDENCE:
        p.append(f"token_truth.measurement_confidence {conf!r} is not in {sorted(MEASUREMENT_CONFIDENCE)}")
    src = truth.get("measurement_source")
    if src not in MEASUREMENT_SOURCE:
        p.append(f"token_truth.measurement_source {src!r} is not in {sorted(MEASUREMENT_SOURCE)}")

    if not isinstance(truth.get("actual_available"), bool):
        p.append("token_truth.actual_available is not a boolean")

    for f in _COUNT_FIELDS:
        v = truth.get(f)
        if not _is_real_int(v) or v < 0:
            p.append(f"token_truth.{f} is not a nonnegative integer")
    for f in _NULLABLE_COUNT_FIELDS:
        v = truth.get(f)
        if v is not None and (not _is_real_int(v) or v < 0):
            p.append(f"token_truth.{f} is not a nonnegative integer or null")

    cost = truth.get("total_cost_usd")
    if cost is not None and (not _is_finite_number(cost) or cost < 0):
        p.append("token_truth.total_cost_usd is not a finite nonnegative number or null")

    # Coherence — availability, call counts and actual token totals must agree.
    actual_available = truth.get("actual_available") is True
    acc = truth.get("actual_call_count")
    pcc = truth.get("provider_call_count")
    if actual_available and _is_real_int(acc) and acc == 0:
        p.append("token_truth.actual_available is true but actual_call_count is 0")
    if not actual_available:
        for f in ("actual_prompt_tokens", "actual_completion_tokens", "actual_total_tokens"):
            if truth.get(f) is not None:
                p.append(f"token_truth.{f} is present but actual_available is false")
    if _is_real_int(pcc) and pcc == 0 and _is_real_int(acc) and acc > 0:
        p.append("token_truth.actual_call_count > 0 but provider_call_count is 0")

    ap, cp_, at = (truth.get("actual_prompt_tokens"), truth.get("actual_completion_tokens"),
                   truth.get("actual_total_tokens"))
    if all(_is_real_int(x) for x in (ap, cp_, at)) and at != ap + cp_:
        p.append("token_truth.actual_total_tokens != actual_prompt_tokens + actual_completion_tokens")

    return p
