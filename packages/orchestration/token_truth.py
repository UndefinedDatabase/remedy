"""Token Truth — honest token accounting separating actual from estimated usage.

Aggregates per-task token evidence into one job-level report that never passes a
character-heuristic estimate off as a measured value. Pure orchestration logic:
no provider calls, no target-repo mutation, no job state mutation. The report is
built only from files already on disk, so the same evidence dir always yields the
same report.

When a provider exposes real usage counters, the ``actual_*`` fields are filled
and ``actual_available`` is true. When it does not (e.g. claude-cli, which never
surfaces token usage), the ``actual_*`` fields stay null and ``missing_reason``
records why — estimates live only in the ``estimated_*`` fields, clearly labeled
low-confidence character heuristics.

Reads (all optional — missing inputs degrade gracefully):
    task_runs/<task_id>/token_accounting.json   (estimated values)
    task_runs/<task_id>/provider_evidence.json  (actual provider usage, provider)
    prompt_trace_summary.json                   (prompt trace count, informational)

Public API:
    build_token_truth(evidence_dir) -> dict
    write_token_truth(evidence_dir, written) -> None
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from packages.common.strict_json import StrictJsonError, strict_loads

SCHEMA_VERSION = "1.0.0"

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")

_DEFAULT_PROVIDER = "claude-cli"
_MEASUREMENT_SOURCE_HEURISTIC = "character_heuristic"
_MEASUREMENT_SOURCE_ACTUAL = "provider_actuals"
_MEASUREMENT_SOURCE_MIXED = "mixed_provider_actuals_and_heuristic"
_MEASUREMENT_CONFIDENCE = "low"
_MISSING_REASON = "actual token usage unavailable from claude-cli output"

# Round 33 F3: the CANONICAL token-truth schema constants — the SINGLE source of truth shared with the
# validator (token_authority imports these), so the producer's own output always validates and the
# enums can never drift. These are EXACTLY the values build_token_truth emits.
TOKEN_TRUTH_SCHEMA_VERSION = SCHEMA_VERSION
MEASUREMENT_CONFIDENCES = frozenset({"low", "mixed", "high"})
MEASUREMENT_SOURCES = frozenset({
    _MEASUREMENT_SOURCE_HEURISTIC, _MEASUREMENT_SOURCE_ACTUAL, _MEASUREMENT_SOURCE_MIXED})
#: The exact (confidence -> source) pairing the producer emits; any other combination is incoherent.
CONFIDENCE_SOURCE_PAIRS = frozenset({
    ("low", _MEASUREMENT_SOURCE_HEURISTIC),
    ("high", _MEASUREMENT_SOURCE_ACTUAL),
    ("mixed", _MEASUREMENT_SOURCE_MIXED)})

# Provider-evidence usage field aliases → normalized actual_* field.
# Both flat keys and keys under a nested "usage" object are honored.
_ACTUAL_ALIASES = {
    "actual_prompt_tokens": ("actual_prompt_tokens", "prompt_tokens", "input_tokens"),
    "actual_completion_tokens": (
        "actual_completion_tokens", "completion_tokens", "output_tokens",
    ),
    "actual_total_tokens": ("actual_total_tokens", "total_tokens"),
    "actual_cache_creation_tokens": (
        "actual_cache_creation_tokens", "cache_creation_tokens",
        "cache_creation_input_tokens",
    ),
    "actual_cache_read_tokens": (
        "actual_cache_read_tokens", "cache_read_tokens", "cache_read_input_tokens",
    ),
}


class TokenEvidenceError(Exception):
    """Round 34 F2: a per-task token_accounting/provider_evidence field is malformed (wrong type,
    boolean-as-int, negative, non-finite cost, or a violated cross-field relationship). The producer
    RAISES rather than coercing/clamping it into a plausible value, so a bounded producer error becomes
    ``token_truth_authority = PRODUCER_ERROR`` and ``package_status = BLOCKED_EVIDENCE``."""


def _is_int(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _strict_count(container: dict, key: str, ctx: str, *, default: int = 0) -> int:
    """A consumed COUNT/token field: absent → ``default``; present → a real nonnegative integer
    (never a bool, float, or string). Anything else raises ``TokenEvidenceError``."""
    if key not in container:
        return default
    v = container[key]
    if not _is_int(v) or v < 0:
        raise TokenEvidenceError(f"{ctx}.{key} is not a nonnegative integer: {v!r}")
    return v


def _strict_cost(container: dict, key: str, ctx: str) -> float | None:
    """A consumed COST field: absent/null → None; present → a finite nonnegative number (never bool)."""
    if key not in container or container[key] is None:
        return None
    v = container[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise TokenEvidenceError(f"{ctx}.{key} is not a finite nonnegative number: {v!r}")
    if v != v or v in (float("inf"), float("-inf")) or v < 0:
        raise TokenEvidenceError(f"{ctx}.{key} is not a finite nonnegative number: {v!r}")
    return float(v)


def _read_json(path: Path) -> dict | None:
    """Round 36 F3: strict typed JSON decode. ``FileNotFoundError`` → ``None`` (genuinely absent).
    Any other read error → ``TokenEvidenceError`` (present-invalid). A non-object root (null, list,
    string, number, Boolean) → ``TokenEvidenceError``."""
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise TokenEvidenceError(f"cannot read {path}: {exc}") from None
    try:
        data = strict_loads(raw, where=str(path))
    except StrictJsonError as exc:
        raise TokenEvidenceError(f"malformed JSON in {path}: {exc}") from None
    if not isinstance(data, dict):
        raise TokenEvidenceError(
            f"{path} has a {type(data).__name__} root, not an object")
    return data


def _task_ids(base: Path) -> list[str]:
    """Return sorted, safe task IDs that have a task_runs/<id>/ directory."""
    runs = base / "task_runs"
    if not runs.is_dir():
        return []
    return sorted(
        child.name
        for child in runs.iterdir()
        if child.is_dir() and _SAFE_TASK_ID_RE.fullmatch(child.name)
    )


def _strict_string(container: dict, key: str, ctx: str, *, default: str = "") -> str:
    """A trust-bearing string field: absent/null → ``default``; present → must be a real string."""
    if key not in container or container[key] is None:
        return default
    v = container[key]
    if not isinstance(v, str):
        raise TokenEvidenceError(f"{ctx}.{key} is not a string: {v!r}")
    return v


def _strict_nullable_string(container: dict, key: str, ctx: str) -> str | None:
    """A nullable string field: absent/null → ``None``; present → must be a real string."""
    if key not in container or container[key] is None:
        return None
    v = container[key]
    if not isinstance(v, str):
        raise TokenEvidenceError(f"{ctx}.{key} is not a string: {v!r}")
    return v


def _strict_string_list(container: dict, key: str, ctx: str) -> list[str] | None:
    """A nullable list-of-strings field."""
    if key not in container or container[key] is None:
        return None
    v = container[key]
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise TokenEvidenceError(f"{ctx}.{key} is not a list of strings: {v!r}")
    return v


def _extract_actual(provider_evidence: Any, ctx: str = "provider_evidence") -> dict[str, int] | None:
    """Pull normalized actual usage counters from provider evidence.

    Looks at the top level and at a nested ``usage`` object. Returns a mapping of ``actual_*`` field
    name → nonnegative int for every counter found, or None when the provider exposed no usage data at
    all (the common claude-cli case). Round 34 F2: a PRESENT usage counter is STRICTLY validated — a
    real nonnegative integer (never a bool, float, string or negative). A malformed counter (e.g. a
    negative cache-creation token) raises ``TokenEvidenceError`` rather than being coerced with
    ``int()`` into a plausible value. When all three of prompt/completion/total are present they must
    agree (total == prompt + completion)."""
    if not isinstance(provider_evidence, dict):
        return None

    sources: list[dict[str, Any]] = [provider_evidence]
    usage = provider_evidence.get("usage")
    if isinstance(usage, dict):
        sources.append(usage)

    found: dict[str, int] = {}
    for field, aliases in _ACTUAL_ALIASES.items():
        for src in sources:
            hit = None
            for alias in aliases:
                if alias in src:
                    hit = alias
                    break
            if hit is not None:
                v = src[hit]
                if not _is_int(v) or v < 0:
                    raise TokenEvidenceError(
                        f"{ctx}.{hit} is not a nonnegative integer token count: {v!r}")
                found[field] = found.get(field, 0) + v
                break

    if not found:
        return None
    ap = found.get("actual_prompt_tokens")
    cp = found.get("actual_completion_tokens")
    at = found.get("actual_total_tokens")
    if ap is not None and cp is not None and at is not None and at != ap + cp:
        raise TokenEvidenceError(
            f"{ctx} actual_total_tokens ({at}) != actual_prompt_tokens + actual_completion_tokens "
            f"({ap} + {cp})")
    # Round 35 F3: derive actual_total from prompt + completion when absent — prevents emitting a
    # high-confidence report with actual_total_tokens=None while prompt and completion are present.
    if ap is not None and cp is not None and at is None:
        found["actual_total_tokens"] = ap + cp
    return found


def build_token_truth(evidence_dir: str) -> dict[str, Any]:
    """Build honest token accounting separating actual from estimated usage."""
    base = Path(evidence_dir) if evidence_dir else Path(".")
    task_ids = _task_ids(base)

    provider = ""
    model = ""

    per_task: dict[str, Any] = {}
    builder_total = 0
    reviewer_total = 0
    repair_total = 0

    actual_totals: dict[str, int] = {}
    any_actual = False
    actual_task_count = 0
    total_cost_usd = 0.0
    any_cost = False

    builder_configured_model = ""
    reviewer_configured_model = ""
    builder_actual_model = None
    reviewer_actual_model = None
    actual_model_verified = False
    agg_provider_call_count = 0
    agg_actual_call_count = 0
    agg_cost_call_count = 0
    cli_version = None
    actual_missing_reasons: list[str] = []

    for tid in task_ids:
        _acc_ctx = f"task_runs/{tid}/token_accounting.json"
        acc = _read_json(base / "task_runs" / tid / "token_accounting.json") or {}
        builder = _strict_count(acc, "builder_prompt_tokens_estimated", _acc_ctx)
        reviewer = _strict_count(acc, "reviewer_prompt_tokens_estimated", _acc_ctx)
        repair = _strict_count(acc, "repair_prompt_tokens_estimated", _acc_ctx)
        builder_total += builder
        reviewer_total += reviewer
        repair_total += repair

        _pe_ctx = f"task_runs/{tid}/provider_evidence.json"
        pe = _read_json(base / "task_runs" / tid / "provider_evidence.json")
        if pe is not None:
            if not provider:
                provider = (_strict_string(pe, "builder_provider", _pe_ctx)
                            or _strict_string(pe, "provider", _pe_ctx))
            if not model:
                model = (_strict_string(pe, "model", _pe_ctx)
                         or _strict_string(pe, "builder_model", _pe_ctx))
            if not builder_configured_model:
                builder_configured_model = _strict_string(pe, "builder_configured_model", _pe_ctx)
            if not reviewer_configured_model:
                reviewer_configured_model = _strict_string(pe, "reviewer_configured_model", _pe_ctx)
            if "actual_model_verified" in pe and not isinstance(pe["actual_model_verified"], bool):
                raise TokenEvidenceError(f"{_pe_ctx}.actual_model_verified is not a boolean")
            if pe.get("actual_model_verified"):
                _bam = _strict_nullable_string(pe, "builder_actual_model", _pe_ctx)
                _ram = _strict_nullable_string(pe, "reviewer_actual_model", _pe_ctx)
                if _bam:
                    builder_actual_model = _bam
                    actual_model_verified = True
                if _ram:
                    reviewer_actual_model = _ram
                    actual_model_verified = True
            _cv = _strict_nullable_string(pe, "cli_version", _pe_ctx)
            if _cv and not cli_version:
                cli_version = _cv
            _amr_raw = pe.get("actual_missing_reasons")
            if _amr_raw is not None:
                if not isinstance(_amr_raw, list) or not all(isinstance(x, str) for x in _amr_raw):
                    raise TokenEvidenceError(
                        f"{_pe_ctx}.actual_missing_reasons is not a list of strings: {_amr_raw!r}")
                for amr in _amr_raw:
                    if amr and amr not in actual_missing_reasons:
                        actual_missing_reasons.append(amr)
            _usage_raw = pe.get("usage")
            if _usage_raw is not None and not isinstance(_usage_raw, dict):
                raise TokenEvidenceError(
                    f"{_pe_ctx}.usage is not an object: {type(_usage_raw).__name__}")

        task_actual = _extract_actual(pe, _pe_ctx)
        task_has_actual = (task_actual is not None and
                          ("actual_prompt_tokens" in task_actual
                           or "actual_completion_tokens" in task_actual))
        exec_mode = _strict_string(pe, "execution_mode", _pe_ctx) if pe is not None else ""
        task_cost = _strict_cost(pe, "total_cost_usd", _pe_ctx) if pe is not None else None
        if exec_mode == "manual_operator_repair":
            task_actual = None
            task_has_actual = False
        if task_has_actual:
            any_actual = True
            actual_task_count += 1
            for field, val in task_actual.items():
                actual_totals[field] = actual_totals.get(field, 0) + val
            if task_cost is not None:
                total_cost_usd += task_cost
                any_cost = True

        if pe is not None:
            has_call_counts = "provider_call_count" in pe
            if has_call_counts:
                # F2 (round 34): call counts are VALIDATED, never clamped. Malformed evidence that
                # claims more measured/cost calls than real provider calls is a bounded producer error.
                task_pc = _strict_count(pe, "provider_call_count", _pe_ctx)
                task_ac = _strict_count(pe, "actual_call_count", _pe_ctx)
                task_cc = _strict_count(pe, "cost_call_count", _pe_ctx)
                if task_ac > task_pc:
                    raise TokenEvidenceError(
                        f"{_pe_ctx}: actual_call_count ({task_ac}) > provider_call_count ({task_pc})")
                if task_cc > task_ac:
                    raise TokenEvidenceError(
                        f"{_pe_ctx}: cost_call_count ({task_cc}) > actual_call_count ({task_ac})")
                # A partial-coverage state (some but not all costed calls) legitimately carries a
                # cost_call_count > 0 with a withheld (null) total_cost_usd — the total is only
                # published when coverage is complete, so no cross-check is enforced here.
                agg_provider_call_count += task_pc
                agg_actual_call_count += task_ac
                agg_cost_call_count += task_cc
            elif exec_mode != "manual_operator_repair":
                agg_provider_call_count += 1
                if task_has_actual:
                    agg_actual_call_count += 1
                    if task_cost is not None:
                        agg_cost_call_count += 1

        task_role = _strict_string(acc, "role", _acc_ctx, default="unknown") if acc else "unknown"
        task_configured_model = _strict_string(acc, "configured_model", _acc_ctx) if acc else ""
        task_actual_model = None
        if pe is not None:
            ta_model = (_strict_nullable_string(pe, "builder_actual_model", _pe_ctx)
                        or _strict_nullable_string(pe, "actual_model", _pe_ctx))
            if ta_model and pe.get("actual_model_verified"):
                task_actual_model = ta_model

        per_task[tid] = {
            "role": task_role,
            "configured_model": task_configured_model or builder_configured_model or model,
            "actual_model": task_actual_model,
            "actual_model_verified": bool(task_actual_model),
            "builder_estimated": builder,
            "reviewer_estimated": reviewer,
            "repair_estimated": repair,
            "actual_available": task_has_actual,
            "estimation_method": _MEASUREMENT_SOURCE_HEURISTIC if not task_has_actual else None,
        }

    estimated_prompt_tokens = builder_total + reviewer_total + repair_total
    estimated_completion_tokens = 0
    estimated_total_tokens = estimated_prompt_tokens + estimated_completion_tokens

    # prompt_trace_count is informational only. The authoritative
    # provider_call_count comes from aggregated provider_evidence attempt
    # counts (retries, parse retries, and repair calls included) — a prompt
    # trace is written per composed prompt, not per real provider attempt.
    trace = _read_json(base / "prompt_trace_summary.json")
    prompt_trace_count = 0
    if trace is not None:
        prompt_trace_count = _strict_count(trace, "total_prompts", "prompt_trace_summary.json")

    agg_actual_coverage_complete = (
        agg_actual_call_count == agg_provider_call_count
    ) if agg_provider_call_count else False
    # Cost coverage is complete only when EVERY real provider call reported
    # cost — measured against provider calls, not just calls with actuals.
    agg_cost_coverage_complete = (
        agg_cost_call_count == agg_provider_call_count
    ) if agg_provider_call_count else False

    if actual_task_count and actual_task_count == len(task_ids) and agg_actual_coverage_complete:
        measurement_confidence = "high"
        measurement_source = _MEASUREMENT_SOURCE_ACTUAL
    elif actual_task_count:
        measurement_confidence = "mixed"
        measurement_source = _MEASUREMENT_SOURCE_MIXED
    else:
        measurement_confidence = _MEASUREMENT_CONFIDENCE
        measurement_source = _MEASUREMENT_SOURCE_HEURISTIC

    # total_cost_usd is non-null only when both actual coverage and cost
    # coverage are complete — a partial sum is never labeled as the total.
    _coverage_ok = agg_actual_coverage_complete and agg_cost_coverage_complete
    effective_cost = round(total_cost_usd, 6) if (any_cost and _coverage_ok) else None

    if agg_cost_coverage_complete:
        cost_coverage_reason = None
    elif not agg_provider_call_count:
        cost_coverage_reason = "no_real_provider_calls"
    else:
        _missing_actuals = agg_actual_call_count < agg_provider_call_count
        _missing_cost = agg_cost_call_count < agg_actual_call_count
        if _missing_actuals and _missing_cost:
            cost_coverage_reason = "missing_actuals_and_provider_cost"
        elif _missing_actuals:
            cost_coverage_reason = "missing_actuals"
        else:
            cost_coverage_reason = "missing_provider_cost"

    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "source": "evidence_aggregation",
        "provider": provider or _DEFAULT_PROVIDER,
        "model": model,
        "builder_configured_model": builder_configured_model,
        "reviewer_configured_model": reviewer_configured_model,
        "builder_actual_model": builder_actual_model,
        "reviewer_actual_model": reviewer_actual_model,
        "actual_model_verified": actual_model_verified,
        "actual_available": any_actual,
        "actual_prompt_tokens": actual_totals.get("actual_prompt_tokens") if any_actual else None,
        "actual_completion_tokens": actual_totals.get("actual_completion_tokens") if any_actual else None,
        "actual_total_tokens": actual_totals.get("actual_total_tokens") if any_actual else None,
        "actual_cache_creation_tokens": actual_totals.get("actual_cache_creation_tokens") if any_actual else None,
        "actual_cache_read_tokens": actual_totals.get("actual_cache_read_tokens") if any_actual else None,
        "estimated_prompt_tokens": estimated_prompt_tokens,
        "estimated_completion_tokens": estimated_completion_tokens,
        "estimated_total_tokens": estimated_total_tokens,
        "measurement_source": measurement_source,
        "measurement_confidence": measurement_confidence,
        "total_cost_usd": effective_cost,
        "cost_coverage_complete": agg_cost_coverage_complete,
        "cost_coverage_reason": cost_coverage_reason,
        "missing_reason": None if any_actual else _MISSING_REASON,
        "actual_missing_reasons": actual_missing_reasons if actual_missing_reasons else None,
        "per_task": per_task,
        "builder_estimated_total": builder_total,
        "reviewer_estimated_total": reviewer_total,
        "repair_estimated_total": repair_total,
        "provider_call_count": agg_provider_call_count,
        "prompt_trace_count": prompt_trace_count,
        "actual_call_count": agg_actual_call_count,
        "actual_coverage_complete": agg_actual_coverage_complete,
        "cost_call_count": agg_cost_call_count,
        "cli_version": cli_version,
    }
    # Round 35 F3: the producer self-validates — a successful build_token_truth never returns an
    # invalid TokenTruthV1. Lazy import to avoid circular dependency (token_authority imports from
    # this module).
    from packages.orchestration.token_authority import validate_token_truth
    problems = validate_token_truth(report)
    if problems:
        raise TokenEvidenceError(
            f"producer emitted an invalid TokenTruthV1: {'; '.join(problems[:5])}")
    return report


def write_token_truth(evidence_dir: str, written: dict[str, str]) -> None:
    """Build and write ``token_truth.json`` to the evidence dir.

    No-op without an evidence dir. Registers the output path in ``written``.
    """
    if not evidence_dir:
        return

    report = build_token_truth(evidence_dir)

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "token_truth.json"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    written["token_truth.json"] = str(json_path)
