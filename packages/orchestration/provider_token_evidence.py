"""ProviderTokenEvidenceV1 — closed versioned input schema for provider evidence.

The SINGLE source of truth for what constitutes valid provider_evidence.json.
Every trust-bearing claim must either survive into canonical TokenTruthV1 or
cause a producer error. No field is silently discarded, no count is inferred.

Public API:
    PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION
    SUPPORTED_EXECUTION_MODES
    ALLOWED_FIELDS
    validate_provider_token_evidence(pe, ctx) -> None  (raises TokenEvidenceError)
"""
from __future__ import annotations

from typing import Any

PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION = "1.0.0"

SUPPORTED_EXECUTION_MODES = frozenset({
    "provider_backed",
    "manual_operator_repair",
})

ALLOWED_FIELDS = frozenset({
    # --- identity & version ---
    "schema_version",
    "task_id",
    "execution_mode",
    # --- call counts (trust-bearing) ---
    "provider_call_count",
    "actual_call_count",
    "cost_call_count",
    # --- cost (trust-bearing) ---
    "total_cost_usd",
    "cost_coverage_reason",
    "cost_coverage_complete",
    # --- provider identity ---
    "builder_provider",
    "reviewer_provider",
    "provider",
    "builder_provider_kind",
    "reviewer_provider_kind",
    # --- model identity ---
    "model",
    "builder_model",
    "builder_configured_model",
    "reviewer_configured_model",
    "builder_actual_model",
    "reviewer_actual_model",
    "actual_model_verified",
    "model_flag_supported",
    # --- actual token counters ---
    "usage",
    "actual_prompt_tokens",
    "actual_completion_tokens",
    "actual_total_tokens",
    "actual_cache_creation_tokens",
    "actual_cache_read_tokens",
    "actual_available",
    "actual_coverage_complete",
    "actual_missing_reasons",
    # --- write mode metadata ---
    "builder_write_mode",
    "reviewer_write_mode",
    "builder_can_write_staging",
    "reviewer_can_write_staging",
    # --- per-call attempt records ---
    "provider_attempts",
    "stream_artifact_refs",
    "stream_evidence_present",
    # --- session & parse metadata ---
    "session_id",
    "parse_source",
    "cli_version",
    "cli_versions",
    # --- prompt trace metadata ---
    "prompt_trace_available",
    "prompt_trace_status",
    "actual_provider_available",
    # --- completion layering (manual repair) ---
    "completion_execution_mode",
    "completion_provider_call_count",
    "supersedes_prior_execution",
    "prior_execution",
})

REQUIRED_FIELDS_PROVIDER_BACKED = frozenset({
    "schema_version",
    "execution_mode",
    "provider_call_count",
    "actual_call_count",
    "cost_call_count",
})

REQUIRED_FIELDS_MANUAL = frozenset({
    "schema_version",
    "execution_mode",
    "provider_call_count",
})


def _is_int(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def validate_provider_token_evidence(pe: dict, ctx: str) -> None:
    """Validate the closed ProviderTokenEvidenceV1 schema.

    Raises ``TokenEvidenceError`` for any schema violation. Must be called
    BEFORE the semantic cross-field validator (``validate_provider_evidence``).
    """
    from packages.orchestration.token_truth import TokenEvidenceError

    if not isinstance(pe, dict):
        raise TokenEvidenceError(f"{ctx}: provider evidence is not an object")

    sv = pe.get("schema_version")
    if sv is None:
        raise TokenEvidenceError(
            f"{ctx}: schema_version is missing; "
            f"expected {PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION!r}")
    if not isinstance(sv, str):
        raise TokenEvidenceError(
            f"{ctx}: schema_version is not a string: {sv!r}")
    if sv != PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION:
        raise TokenEvidenceError(
            f"{ctx}: unsupported schema_version {sv!r}; "
            f"expected {PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION!r}")

    unknown = set(pe.keys()) - ALLOWED_FIELDS
    if unknown:
        raise TokenEvidenceError(
            f"{ctx}: unknown fields {sorted(unknown)}; "
            f"ProviderTokenEvidenceV1 has a closed schema")

    em = pe.get("execution_mode")
    if em is None:
        raise TokenEvidenceError(f"{ctx}: execution_mode is missing")
    if not isinstance(em, str):
        raise TokenEvidenceError(f"{ctx}: execution_mode is not a string: {em!r}")
    if em not in SUPPORTED_EXECUTION_MODES:
        raise TokenEvidenceError(
            f"{ctx}: unsupported execution_mode {em!r}; "
            f"supported: {sorted(SUPPORTED_EXECUTION_MODES)}")

    if em == "provider_backed":
        for req in sorted(REQUIRED_FIELDS_PROVIDER_BACKED):
            if req not in pe:
                raise TokenEvidenceError(
                    f"{ctx}: required field {req!r} is missing for "
                    f"execution_mode='provider_backed'")
    elif em == "manual_operator_repair":
        for req in sorted(REQUIRED_FIELDS_MANUAL):
            if req not in pe:
                raise TokenEvidenceError(
                    f"{ctx}: required field {req!r} is missing for "
                    f"execution_mode='manual_operator_repair'")
        pc = pe.get("provider_call_count")
        if not (_is_int(pc) and pc == 0):
            raise TokenEvidenceError(
                f"{ctx}: manual_operator_repair requires provider_call_count=0, "
                f"got {pc!r}")
        ac = pe.get("actual_call_count")
        if ac is not None and not (_is_int(ac) and ac == 0):
            raise TokenEvidenceError(
                f"{ctx}: manual_operator_repair requires actual_call_count=0 or absent, "
                f"got {ac!r}")
        cc = pe.get("cost_call_count")
        if cc is not None and not (_is_int(cc) and cc == 0):
            raise TokenEvidenceError(
                f"{ctx}: manual_operator_repair requires cost_call_count=0 or absent, "
                f"got {cc!r}")
        for model_field in ("builder_actual_model", "reviewer_actual_model",
                            "actual_model_verified"):
            if pe.get(model_field) is not None and pe.get(model_field) is not False:
                raise TokenEvidenceError(
                    f"{ctx}: manual_operator_repair must not claim {model_field}={pe[model_field]!r}")
        usage_fields = ("actual_prompt_tokens", "actual_completion_tokens",
                        "actual_total_tokens", "actual_cache_creation_tokens",
                        "actual_cache_read_tokens")
        for uf in usage_fields:
            if pe.get(uf) is not None:
                raise TokenEvidenceError(
                    f"{ctx}: manual_operator_repair must not claim {uf}={pe[uf]!r}")
        if isinstance(pe.get("usage"), dict) and pe["usage"]:
            raise TokenEvidenceError(
                f"{ctx}: manual_operator_repair must not carry usage counters")
