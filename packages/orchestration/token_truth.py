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
    prompt_trace_summary.json                   (provider call count)

Public API:
    build_token_truth(evidence_dir) -> dict
    write_token_truth(evidence_dir, written) -> None
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")

_DEFAULT_PROVIDER = "claude-cli"
_MEASUREMENT_SOURCE = "character_heuristic"
_MEASUREMENT_CONFIDENCE = "low"
_MISSING_REASON = "actual token usage unavailable from claude-cli output"

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


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


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


def _as_int(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else 0


def _extract_actual(provider_evidence: Any) -> dict[str, int] | None:
    """Pull normalized actual usage counters from provider evidence.

    Looks at the top level and at a nested ``usage`` object. Returns a mapping of
    ``actual_*`` field name → int for every counter found, or None when the
    provider exposed no usage data at all (the common claude-cli case).
    """
    if not isinstance(provider_evidence, dict):
        return None

    sources: list[dict[str, Any]] = [provider_evidence]
    usage = provider_evidence.get("usage")
    if isinstance(usage, dict):
        sources.append(usage)

    found: dict[str, int] = {}
    for field, aliases in _ACTUAL_ALIASES.items():
        for src in sources:
            present = False
            for alias in aliases:
                if alias in src and isinstance(src[alias], (int, float)) and not isinstance(src[alias], bool):
                    found[field] = found.get(field, 0) + int(src[alias])
                    present = True
                    break
            if present:
                break

    return found or None


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

    for tid in task_ids:
        acc = _read_json(base / "task_runs" / tid / "token_accounting.json")
        acc = acc if isinstance(acc, dict) else {}
        builder = _as_int(acc.get("builder_prompt_tokens_estimated"))
        reviewer = _as_int(acc.get("reviewer_prompt_tokens_estimated"))
        repair = _as_int(acc.get("repair_prompt_tokens_estimated"))
        builder_total += builder
        reviewer_total += reviewer
        repair_total += repair

        pe = _read_json(base / "task_runs" / tid / "provider_evidence.json")
        if isinstance(pe, dict):
            if not provider:
                provider = str(pe.get("builder_provider") or pe.get("provider") or "")
            if not model:
                model = str(pe.get("model") or pe.get("builder_model") or "")
        task_actual = _extract_actual(pe)
        task_has_actual = task_actual is not None
        if task_has_actual:
            any_actual = True
            for field, val in task_actual.items():
                actual_totals[field] = actual_totals.get(field, 0) + val

        per_task[tid] = {
            "builder_estimated": builder,
            "reviewer_estimated": reviewer,
            "repair_estimated": repair,
            "actual_available": task_has_actual,
        }

    estimated_prompt_tokens = builder_total + reviewer_total + repair_total
    estimated_completion_tokens = 0
    estimated_total_tokens = estimated_prompt_tokens + estimated_completion_tokens

    trace = _read_json(base / "prompt_trace_summary.json")
    provider_call_count = 0
    if isinstance(trace, dict):
        provider_call_count = _as_int(trace.get("total_prompts"))

    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "source": "evidence_aggregation",
        "provider": provider or _DEFAULT_PROVIDER,
        "model": model,
        "actual_available": any_actual,
        "actual_prompt_tokens": actual_totals.get("actual_prompt_tokens") if any_actual else None,
        "actual_completion_tokens": actual_totals.get("actual_completion_tokens") if any_actual else None,
        "actual_total_tokens": actual_totals.get("actual_total_tokens") if any_actual else None,
        "actual_cache_creation_tokens": actual_totals.get("actual_cache_creation_tokens") if any_actual else None,
        "actual_cache_read_tokens": actual_totals.get("actual_cache_read_tokens") if any_actual else None,
        "estimated_prompt_tokens": estimated_prompt_tokens,
        "estimated_completion_tokens": estimated_completion_tokens,
        "estimated_total_tokens": estimated_total_tokens,
        "measurement_source": _MEASUREMENT_SOURCE,
        "measurement_confidence": _MEASUREMENT_CONFIDENCE,
        "missing_reason": None if any_actual else _MISSING_REASON,
        "per_task": per_task,
        "builder_estimated_total": builder_total,
        "reviewer_estimated_total": reviewer_total,
        "repair_estimated_total": repair_total,
        "provider_call_count": provider_call_count,
    }
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
