"""Builder prompt evaluation harness.

Measures structured-patch quality across prompt variants and response categories.
All records contain safe metadata only — no raw provider output, no raw source,
no raw prompts.

Public API::

    run_fixture_eval(variant, cases) -> EvalReport
    run_single_eval(variant, builder_output) -> EvalRecord
    aggregate_records(records) -> EvalMetrics
    export_eval_report_json(report) -> dict
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from packages.orchestration.builder_models import (
    BuilderOutput,
    BuilderPatchResult,
    parse_builder_patch,
)


@dataclass
class EvalRecord:
    """Single evaluation record — safe metadata only."""

    version: int = 1
    eval_id: str = ""
    fixture_name: str = ""
    provider: str = "fixture"
    model: str = "mock"
    prompt_variant: str = "default"
    structured_patch_attempted: bool = False
    parse_success: bool = False
    parse_error_kind: str = ""
    stop_reason: str = ""
    unsafe_rejected: bool = False
    target_path_count: int = 0
    operation_count: int = 0
    estimated_tokens: int = 0
    latency_ms: int = 0
    output_hash: str = ""
    output_length: int = 0
    redaction: str = "safe_metadata_only"


@dataclass
class EvalMetrics:
    """Aggregated metrics across eval records."""

    total_cases: int = 0
    parse_success_count: int = 0
    parse_success_rate: float = 0.0
    failure_counts_by_error_kind: dict[str, int] = field(default_factory=dict)
    unsafe_rejection_count: int = 0
    average_estimated_tokens: float = 0.0
    average_latency_ms: float = 0.0
    stop_reason_counts: dict[str, int] = field(default_factory=dict)


@dataclass
class EvalReport:
    """Full eval report — aggregated metrics + individual records."""

    version: int = 1
    prompt_variant: str = "default"
    provider: str = "fixture"
    model: str = "mock"
    metrics: EvalMetrics = field(default_factory=EvalMetrics)
    records: list[EvalRecord] = field(default_factory=list)
    recommendation: str = ""
    redaction: str = "safe_metadata_only"


@dataclass
class EvalCase:
    """A single test case for builder evaluation."""

    name: str
    builder_output: BuilderOutput
    category: str = "unknown"


def run_single_eval(
    variant: str,
    builder_output: BuilderOutput,
    *,
    fixture_name: str = "",
    provider: str = "fixture",
    model: str = "mock",
) -> EvalRecord:
    """Evaluate a single builder output. Returns safe metadata record."""
    eval_id = uuid4().hex[:12]
    start = time.monotonic()

    has_patch = bool(builder_output.structured_patch_text)
    result: BuilderPatchResult = parse_builder_patch(builder_output)

    latency_ms = int((time.monotonic() - start) * 1000)

    stop_reason = ""
    if not result.parse_success and result.error_kind:
        from packages.orchestration.builder_bridge import _map_error_kind_to_stop_reason

        stop_reason = _map_error_kind_to_stop_reason(result.error_kind)

    return EvalRecord(
        eval_id=eval_id,
        fixture_name=fixture_name,
        provider=provider,
        model=model,
        prompt_variant=variant,
        structured_patch_attempted=has_patch,
        parse_success=result.parse_success,
        parse_error_kind=result.error_kind,
        stop_reason=stop_reason,
        unsafe_rejected=result.error_kind in (
            "unsafe_shell_command", "validation_failed",
        ),
        target_path_count=len(result.target_paths),
        operation_count=len(result.target_paths),
        estimated_tokens=result.output_length // 4,
        latency_ms=latency_ms,
        output_hash=result.output_hash,
        output_length=result.output_length,
    )


def aggregate_records(records: list[EvalRecord]) -> EvalMetrics:
    """Aggregate eval records into metrics."""
    if not records:
        return EvalMetrics()

    total = len(records)
    success = sum(1 for r in records if r.parse_success)

    error_counts: dict[str, int] = {}
    stop_counts: dict[str, int] = {}
    total_tokens = 0
    total_latency = 0
    unsafe = 0

    for r in records:
        if r.parse_error_kind:
            error_counts[r.parse_error_kind] = error_counts.get(r.parse_error_kind, 0) + 1
        if r.stop_reason:
            stop_counts[r.stop_reason] = stop_counts.get(r.stop_reason, 0) + 1
        if r.unsafe_rejected:
            unsafe += 1
        total_tokens += r.estimated_tokens
        total_latency += r.latency_ms

    return EvalMetrics(
        total_cases=total,
        parse_success_count=success,
        parse_success_rate=success / total if total > 0 else 0.0,
        failure_counts_by_error_kind=error_counts,
        unsafe_rejection_count=unsafe,
        average_estimated_tokens=total_tokens / total if total > 0 else 0.0,
        average_latency_ms=total_latency / total if total > 0 else 0.0,
        stop_reason_counts=stop_counts,
    )


def run_fixture_eval(
    variant: str,
    cases: list[EvalCase],
    *,
    provider: str = "fixture",
    model: str = "mock",
) -> EvalReport:
    """Run evaluation across all fixture cases for a given prompt variant."""
    records = []
    for case in cases:
        record = run_single_eval(
            variant,
            case.builder_output,
            fixture_name=case.name,
            provider=provider,
            model=model,
        )
        records.append(record)

    metrics = aggregate_records(records)

    recommendation = "needs_real_ollama_eval"
    if metrics.total_cases > 0 and metrics.parse_success_rate >= 0.5:
        recommendation = f"best_for_fixture (success_rate={metrics.parse_success_rate:.0%})"

    return EvalReport(
        prompt_variant=variant,
        provider=provider,
        model=model,
        metrics=metrics,
        records=records,
        recommendation=recommendation,
    )


def standard_eval_cases() -> list[EvalCase]:
    """Standard eval cases covering all builder response categories.

    Categories: success (valid file_op, valid diff, wrapper text),
    failure (prose, malformed JSON, no text, empty),
    rejected (unsafe path, shell command).
    """
    import json

    return [
        EvalCase(
            name="valid_file_op",
            category="success",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text=json.dumps(
                    {"file_ops": [{"path": "app.py", "action": "modify", "content": "x = 1\n"}]}
                ),
            ),
        ),
        EvalCase(
            name="valid_unified_diff",
            category="success",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text=(
                    "--- a/calc.py\n+++ b/calc.py\n@@ -1,2 +1,2 @@\n"
                    " def add(a, b):\n-    return a - b\n+    return a + b\n"
                ),
            ),
        ),
        EvalCase(
            name="prose_only",
            category="failure",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text="I think we should modify the add function to return a + b instead.",
            ),
        ),
        EvalCase(
            name="malformed_json",
            category="failure",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text='{"file_ops": [{"path": "a.py", "action": "create", "content":',
            ),
        ),
        EvalCase(
            name="wrapper_text",
            category="success",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text=(
                    'Here is the fix:\n```json\n'
                    + json.dumps({"file_ops": [{"path": "a.py", "action": "create", "content": "x\n"}]})
                    + '\n```\n'
                ),
            ),
        ),
        EvalCase(
            name="unsafe_path",
            category="rejected",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text=json.dumps(
                    {"file_ops": [{"path": "/etc/passwd", "action": "modify", "content": "x\n"}]}
                ),
            ),
        ),
        EvalCase(
            name="shell_command",
            category="rejected",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text="rm -rf /tmp/foo",
            ),
        ),
        EvalCase(
            name="no_patch_text",
            category="failure",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text=None,
            ),
        ),
        EvalCase(
            name="empty_string",
            category="failure",
            builder_output=BuilderOutput(
                summary="Test", proposed_changes=["Change"],
                structured_patch_text="",
            ),
        ),
    ]


def export_eval_report_json(report: EvalReport) -> dict[str, Any]:
    """Export eval report as safe JSON dict."""
    return {
        "version": report.version,
        "prompt_variant": report.prompt_variant,
        "provider": report.provider,
        "model": report.model,
        "redaction": report.redaction,
        "metrics": {
            "total_cases": report.metrics.total_cases,
            "parse_success_count": report.metrics.parse_success_count,
            "parse_success_rate": round(report.metrics.parse_success_rate, 4),
            "failure_counts_by_error_kind": report.metrics.failure_counts_by_error_kind,
            "unsafe_rejection_count": report.metrics.unsafe_rejection_count,
            "average_estimated_tokens": round(report.metrics.average_estimated_tokens, 1),
            "average_latency_ms": round(report.metrics.average_latency_ms, 1),
            "stop_reason_counts": report.metrics.stop_reason_counts,
        },
        "recommendation": report.recommendation,
        "records": [
            {
                "eval_id": r.eval_id,
                "fixture_name": r.fixture_name,
                "prompt_variant": r.prompt_variant,
                "parse_success": r.parse_success,
                "parse_error_kind": r.parse_error_kind,
                "stop_reason": r.stop_reason,
                "unsafe_rejected": r.unsafe_rejected,
                "target_path_count": r.target_path_count,
                "output_hash": r.output_hash,
                "output_length": r.output_length,
                "redaction": r.redaction,
            }
            for r in report.records
        ],
    }
