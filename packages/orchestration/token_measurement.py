"""The single source of truth for the pure token-measurement derivation.

Round 29 F1: the review gate must be able to reconstruct a packaged final-verifier
``token_measurement`` block byte-for-semantic-byte from its ``token_status``. Keeping a second,
hand-maintained projection-field list in the gate let the two drift — an impossible combination
(high confidence with a null summary, a low-confidence report carrying a fabricated non-null summary,
an arbitrary matching measurement_note) could pass. So the derivation lives here, is imported by both
``final_verifier`` (the producer) and ``build_review_manifest`` (the gate validator), and neither
keeps its own copy.

The function is PURE: it reads only ``token_status`` and returns a fresh dict. No filesystem, no
provider, no side effect — safe to import from anywhere.
"""
from __future__ import annotations

from typing import Any

#: Informational note surfaced when token counts are pure character heuristics. It is advisory only —
#: a low-confidence measurement never blocks promotion.
LOW_CONFIDENCE_TOKEN_NOTE = (
    "Token counts are low-confidence character heuristics; no provider exposed "
    "measured usage. Informational only — does not affect the verdict."
)

#: The fields the high/mixed-confidence ``actual_summary`` copies straight from ``token_status``.
_SUMMARY_FIELDS = (
    "measurement_confidence", "measurement_source", "actual_prompt_tokens",
    "actual_completion_tokens", "actual_total_tokens", "total_cost_usd", "cost_call_count",
    "cost_coverage_complete", "cost_coverage_reason", "provider_call_count", "actual_call_count",
    "actual_coverage_complete", "actual_missing_reasons", "cli_version", "configured_models",
    "actual_models", "actual_model_verified",
)

def token_measurement_summary(token_status: dict[str, Any]) -> dict[str, Any]:
    """Derive a measurement-confidence view over the token_truth-backed status.

    - ``high``/``mixed`` confidence: attach the exact non-null actual token/cost summary.
    - ``low`` confidence (or empty confidence with no actual measurement): attach the informational
      note only; the summary is null.

    Never returns anything that alters the verdict — this is reporting only. The output key order is
    the historical producer order so a re-derivation is byte-identical to the packaged block.
    """
    if not isinstance(token_status, dict):
        token_status = {}
    confidence = str(token_status.get("measurement_confidence", "") or "")
    note: str | None = None
    actual_summary: dict[str, Any] | None = None

    if confidence in ("high", "mixed"):
        actual_summary = {f: token_status.get(f) for f in _SUMMARY_FIELDS}
    elif confidence == "low" or (
        not confidence and not token_status.get("actual_available")
    ):
        note = LOW_CONFIDENCE_TOKEN_NOTE

    # F003: the measurement summary always preserves coverage/cost/model fields from token_truth —
    # unknown stays None, never zero/false.
    return {
        "measurement_confidence": confidence,
        "measurement_source": token_status.get("measurement_source"),
        "measurement_note": note,
        "actual_summary": actual_summary,
        "provider_call_count": token_status.get("provider_call_count"),
        "actual_call_count": token_status.get("actual_call_count"),
        "actual_coverage_complete": token_status.get("actual_coverage_complete"),
        "actual_missing_reasons": token_status.get("actual_missing_reasons"),
        "cost_call_count": token_status.get("cost_call_count"),
        "cost_coverage_complete": token_status.get("cost_coverage_complete"),
        "cost_coverage_reason": token_status.get("cost_coverage_reason"),
        "total_cost_usd": token_status.get("total_cost_usd"),
        "cli_version": token_status.get("cli_version"),
        "configured_models": token_status.get("configured_models"),
        "actual_models": token_status.get("actual_models"),
        "actual_model_verified": token_status.get("actual_model_verified"),
    }
