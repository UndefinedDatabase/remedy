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

# Round 33 F3: the schema constants are imported from the PRODUCER (token_truth), never duplicated, so
# the producer's own output always validates and the enums cannot drift.
from packages.orchestration.token_truth import (
    CONFIDENCE_SOURCE_PAIRS,
    TOKEN_TRUTH_SCHEMA_VERSION,
)
from packages.orchestration.token_truth import (
    MEASUREMENT_CONFIDENCES as MEASUREMENT_CONFIDENCE,
)
from packages.orchestration.token_truth import (
    MEASUREMENT_SOURCES as MEASUREMENT_SOURCE,
)

#: The only token-truth schema version this build reads (shared with the producer).
SUPPORTED_TOKEN_TRUTH_VERSIONS = frozenset({TOKEN_TRUTH_SCHEMA_VERSION})

#: Non-nullable integer count fields — real ints (never bool), nonnegative.
_COUNT_FIELDS = (
    "estimated_prompt_tokens", "estimated_completion_tokens", "estimated_total_tokens",
    "builder_estimated_total", "reviewer_estimated_total", "repair_estimated_total",
    "provider_call_count", "prompt_trace_count", "actual_call_count", "cost_call_count",
)
#: Nullable nonnegative integer fields (present when measured, else null) — includes cache counts.
_NULLABLE_COUNT_FIELDS = (
    "actual_prompt_tokens", "actual_completion_tokens", "actual_total_tokens",
    "actual_cache_creation_tokens", "actual_cache_read_tokens",
)
#: String fields (may be empty). ``model`` etc. are informational identities.
_STRING_FIELDS = ("source", "provider", "model",
                  "builder_configured_model", "reviewer_configured_model")
#: Nullable string fields.
_NULLABLE_STRING_FIELDS = ("builder_actual_model", "reviewer_actual_model",
                           "cost_coverage_reason", "missing_reason", "cli_version")
#: The EXACT closed TokenTruthV1 output field set — an unknown or missing field blocks.
_TOKEN_TRUTH_FIELDS = frozenset({
    "schema_version", "source", "provider", "model",
    "builder_configured_model", "reviewer_configured_model",
    "builder_actual_model", "reviewer_actual_model", "actual_model_verified",
    "actual_available", "actual_prompt_tokens", "actual_completion_tokens", "actual_total_tokens",
    "actual_cache_creation_tokens", "actual_cache_read_tokens",
    "estimated_prompt_tokens", "estimated_completion_tokens", "estimated_total_tokens",
    "measurement_source", "measurement_confidence", "total_cost_usd",
    "cost_coverage_complete", "cost_coverage_reason", "missing_reason", "actual_missing_reasons",
    "per_task", "builder_estimated_total", "reviewer_estimated_total", "repair_estimated_total",
    "provider_call_count", "prompt_trace_count", "actual_call_count", "actual_coverage_complete",
    "cost_call_count", "cli_version",
})
#: The EXACT closed per_task record field set.
_PER_TASK_FIELDS = frozenset({
    "role", "configured_model", "actual_model", "actual_model_verified",
    "builder_estimated", "reviewer_estimated", "repair_estimated",
    "actual_available", "estimation_method",
})


def _is_real_int(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _is_finite_number(v: Any) -> bool:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return False
    return v == v and v not in (float("inf"), float("-inf"))   # reject NaN / Infinity


def _validate_per_task(truth: dict, p: list[str]) -> None:
    """Every per_task record is a closed, typed object; the per-task estimate sums agree with the
    aggregate ``*_estimated_total`` fields."""
    per_task = truth.get("per_task")
    if not isinstance(per_task, dict):
        p.append("token_truth.per_task is not an object")
        return
    sums = {"builder_estimated": 0, "reviewer_estimated": 0, "repair_estimated": 0}
    ok_sums = True
    for tid, rec in per_task.items():
        if not isinstance(rec, dict):
            p.append(f"token_truth.per_task[{tid!r}] is not an object")
            ok_sums = False
            continue
        extra = set(rec) - _PER_TASK_FIELDS
        missing = _PER_TASK_FIELDS - set(rec)
        if extra:
            p.append(f"token_truth.per_task[{tid!r}] has unknown fields {sorted(extra)}")
        if missing:
            p.append(f"token_truth.per_task[{tid!r}] is missing fields {sorted(missing)}")
        for f in ("builder_estimated", "reviewer_estimated", "repair_estimated"):
            v = rec.get(f)
            if not _is_real_int(v) or v < 0:
                p.append(f"token_truth.per_task[{tid!r}].{f} is not a nonnegative integer")
                ok_sums = False
            else:
                sums[f] += v
        if not isinstance(rec.get("actual_available"), bool):
            p.append(f"token_truth.per_task[{tid!r}].actual_available is not a boolean")
        if not isinstance(rec.get("actual_model_verified"), bool):
            p.append(f"token_truth.per_task[{tid!r}].actual_model_verified is not a boolean")
        if not (isinstance(rec.get("role"), str) and isinstance(rec.get("configured_model"), str)):
            p.append(f"token_truth.per_task[{tid!r}] role/configured_model are not strings")
        am = rec.get("actual_model")
        if am is not None and not isinstance(am, str):
            p.append(f"token_truth.per_task[{tid!r}].actual_model is not a string or null")
        em = rec.get("estimation_method")
        if em is not None and not isinstance(em, str):
            p.append(f"token_truth.per_task[{tid!r}].estimation_method is not a string or null")
    if ok_sums:
        for f, total_key in (("builder_estimated", "builder_estimated_total"),
                             ("reviewer_estimated", "reviewer_estimated_total"),
                             ("repair_estimated", "repair_estimated_total")):
            agg = truth.get(total_key)
            if _is_real_int(agg) and agg != sums[f]:
                p.append(f"token_truth.{total_key} ({agg}) != sum of per_task.{f} ({sums[f]})")


def validate_token_truth(truth: Any) -> list[str]:
    """Round 34 F2 — validate the COMPLETE, closed TokenTruthV1 output: exact field set, every field
    typed, and every state invariant. Empty list means valid; never raises. A malformed or internally
    incoherent report (one the strict producer would never emit) is blocked here, so packaging and the
    verifier share one notion of a valid token truth."""
    p: list[str] = []
    if not isinstance(truth, dict):
        return ["token_truth.json is not a JSON object"]
    if not truth:
        return ["token_truth.json is empty"]

    # Closed field set — an unknown or missing field blocks (the schema is exact, not a superset).
    extra = set(truth) - _TOKEN_TRUTH_FIELDS
    missing = _TOKEN_TRUTH_FIELDS - set(truth)
    if extra:
        p.append(f"token_truth has unknown fields {sorted(extra)}")
    if missing:
        p.append(f"token_truth is missing required fields {sorted(missing)}")

    if truth.get("schema_version") not in SUPPORTED_TOKEN_TRUTH_VERSIONS:
        p.append(f"token_truth.schema_version {truth.get('schema_version')!r} is not supported "
                 f"{sorted(SUPPORTED_TOKEN_TRUTH_VERSIONS)}")

    conf = truth.get("measurement_confidence")
    if conf not in MEASUREMENT_CONFIDENCE:
        p.append(f"token_truth.measurement_confidence {conf!r} is not in {sorted(MEASUREMENT_CONFIDENCE)}")
    src = truth.get("measurement_source")
    if src not in MEASUREMENT_SOURCE:
        p.append(f"token_truth.measurement_source {src!r} is not in {sorted(MEASUREMENT_SOURCE)}")
    if conf in MEASUREMENT_CONFIDENCE and src in MEASUREMENT_SOURCE \
            and (conf, src) not in CONFIDENCE_SOURCE_PAIRS:
        p.append(f"token_truth.measurement_confidence {conf!r} / measurement_source {src!r} is not a "
                 f"valid combination")

    for f in ("actual_available", "actual_model_verified",
              "cost_coverage_complete", "actual_coverage_complete"):
        if not isinstance(truth.get(f), bool):
            p.append(f"token_truth.{f} is not a boolean")
    for f in _STRING_FIELDS:
        if not isinstance(truth.get(f), str):
            p.append(f"token_truth.{f} is not a string")
    for f in _NULLABLE_STRING_FIELDS:
        v = truth.get(f)
        if v is not None and not isinstance(v, str):
            p.append(f"token_truth.{f} is not a string or null")
    amr = truth.get("actual_missing_reasons")
    if amr is not None and not (isinstance(amr, list) and all(isinstance(x, str) for x in amr)):
        p.append("token_truth.actual_missing_reasons is not a list of strings or null")

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

    # ---- State invariants (only when the underlying fields are the right type) ----
    ep, ec, et = (truth.get("estimated_prompt_tokens"), truth.get("estimated_completion_tokens"),
                  truth.get("estimated_total_tokens"))
    be, re_, rp = (truth.get("builder_estimated_total"), truth.get("reviewer_estimated_total"),
                   truth.get("repair_estimated_total"))
    if all(_is_real_int(x) for x in (ep, ec, et)) and et != ep + ec:
        p.append("token_truth.estimated_total_tokens != estimated_prompt + estimated_completion")
    if all(_is_real_int(x) for x in (ep, be, re_, rp)) and ep != be + re_ + rp:
        p.append("token_truth.estimated_prompt_tokens != builder + reviewer + repair estimated totals")

    ap, cp_, at = (truth.get("actual_prompt_tokens"), truth.get("actual_completion_tokens"),
                   truth.get("actual_total_tokens"))
    if all(_is_real_int(x) for x in (ap, cp_, at)) and at != ap + cp_:
        p.append("token_truth.actual_total_tokens != actual_prompt_tokens + actual_completion_tokens")

    pcc, acc, ccc = (truth.get("provider_call_count"), truth.get("actual_call_count"),
                     truth.get("cost_call_count"))
    if _is_real_int(pcc) and _is_real_int(acc) and acc > pcc:
        p.append("token_truth.actual_call_count > provider_call_count")
    if _is_real_int(acc) and _is_real_int(ccc) and ccc > acc:
        p.append("token_truth.cost_call_count > actual_call_count")

    actual_available = truth.get("actual_available") is True
    acov = truth.get("actual_coverage_complete")
    ccov = truth.get("cost_coverage_complete")
    if _is_real_int(pcc) and _is_real_int(acc) and isinstance(acov, bool):
        if acov != (pcc > 0 and acc == pcc):
            p.append("token_truth.actual_coverage_complete disagrees with the call counts")
    if _is_real_int(pcc) and _is_real_int(ccc) and isinstance(ccov, bool):
        if ccov != (pcc > 0 and ccc == pcc):
            p.append("token_truth.cost_coverage_complete disagrees with the call counts")

    if actual_available and _is_real_int(acc) and acc == 0:
        p.append("token_truth.actual_available is true but actual_call_count is 0")
    if not actual_available:
        for f in ("actual_prompt_tokens", "actual_completion_tokens", "actual_total_tokens"):
            if truth.get(f) is not None:
                p.append(f"token_truth.{f} is present but actual_available is false")

    # Confidence ↔ coverage.
    if conf == "high":
        if acov is not True:
            p.append("token_truth.measurement_confidence 'high' requires complete actual coverage")
        if any(truth.get(f) is None for f in
               ("actual_prompt_tokens", "actual_completion_tokens", "actual_total_tokens")):
            p.append("token_truth.measurement_confidence 'high' requires complete actual token totals")
    if conf == "low" and (actual_available or (_is_real_int(acc) and acc > 0)):
        p.append("token_truth.measurement_confidence 'low' but actual usage is present")
    if conf == "mixed" and not actual_available:
        p.append("token_truth.measurement_confidence 'mixed' but no actual usage is present")

    # Cost coherence.
    if ccov is True and cost is None:
        p.append("token_truth.cost_coverage_complete is true but total_cost_usd is null")
    if cost is not None and _is_real_int(ccc) and ccc == 0:
        p.append("token_truth.total_cost_usd is present but cost_call_count is 0")
    reason = truth.get("cost_coverage_reason")
    if isinstance(ccov, bool):
        if ccov and reason is not None:
            p.append("token_truth.cost_coverage_reason must be null when cost coverage is complete")
        if not ccov and not (isinstance(reason, str) and reason):
            p.append("token_truth.cost_coverage_reason must be a nonempty string when cost coverage "
                     "is incomplete")

    # Model identity ↔ verification.
    verified = truth.get("actual_model_verified") is True
    bam, ram = truth.get("builder_actual_model"), truth.get("reviewer_actual_model")
    if verified and not ((isinstance(bam, str) and bam) or (isinstance(ram, str) and ram)):
        p.append("token_truth.actual_model_verified is true but no actual model identity is present")
    if not verified and (bam or ram):
        p.append("token_truth.actual model identity present but actual_model_verified is false")

    # missing_reason ↔ availability.
    missing_reason = truth.get("missing_reason")
    if actual_available and missing_reason is not None:
        p.append("token_truth.missing_reason must be null when actual usage is available")
    if not actual_available and not (isinstance(missing_reason, str) and missing_reason):
        p.append("token_truth.missing_reason must be a nonempty string when actual usage is absent")

    _validate_per_task(truth, p)
    return p
