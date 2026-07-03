"""Evidence execution mode taxonomy v1.

Every task's evidence must declare *how* the task was actually executed, based on
real evidence signals (prompt traces, provider call counts, provider identity) —
not on what was configured or intended.

This prevents "phantom provider" evidence, where a task claims to be backed by a
real provider but no prompts were ever sent and no provider calls were made.

Execution modes:
    provider_backed          — real provider ran (prompts sent, provider calls made)
    fake_provider_test       — a fake/stub/mock provider was used (test only)
    manual_operator_repair   — prompts recorded but no provider call (operator edited by hand)
    operator_built_no_provider — no prompts, no provider calls (pure operator work)
    unknown                  — signals inconsistent / cannot be classified

Public API:
    ExecutionMode — str Enum
    classify_execution_mode(prompt_count, provider_call_count, builder_provider,
                            reviewer_provider) -> ExecutionMode
    build_task_execution_evidence(task_id, mode, builder_provider, reviewer_provider,
                                  builder_identity, reviewer_identity, ...) -> dict
"""
from __future__ import annotations

from enum import Enum
from typing import Any

# Substrings that mark a provider name/identity as a non-real (fake) provider.
_FAKE_PROVIDER_MARKERS = ("fake", "stub", "mock")


class ExecutionMode(str, Enum):
    """How a task was actually executed, per real evidence signals."""

    PROVIDER_BACKED = "provider_backed"
    FAKE_PROVIDER_TEST = "fake_provider_test"
    MANUAL_OPERATOR_REPAIR = "manual_operator_repair"
    OPERATOR_BUILT_NO_PROVIDER = "operator_built_no_provider"
    UNKNOWN = "unknown"


def _is_fake_provider(name: Any) -> bool:
    """True if a provider name/identity looks like a fake/stub/mock provider."""
    if not name:
        return False
    lowered = str(name).lower()
    return any(marker in lowered for marker in _FAKE_PROVIDER_MARKERS)


def classify_execution_mode(
    prompt_count: int,
    provider_call_count: int,
    builder_provider: Any = None,
    reviewer_provider: Any = None,
) -> ExecutionMode:
    """Classify the true execution mode from real evidence signals.

    Precedence:
        1. Fake builder/reviewer provider -> fake_provider_test
        2. prompts > 0 and provider calls > 0 -> provider_backed
        3. prompts == 0 and provider calls == 0 -> operator_built_no_provider
        4. prompts > 0 and provider calls == 0 -> manual_operator_repair
        5. otherwise (calls > 0 but no prompts) -> unknown (inconsistent)
    """
    prompts = max(0, int(prompt_count or 0))
    calls = max(0, int(provider_call_count or 0))

    if _is_fake_provider(builder_provider) or _is_fake_provider(reviewer_provider):
        return ExecutionMode.FAKE_PROVIDER_TEST

    if prompts > 0 and calls > 0:
        return ExecutionMode.PROVIDER_BACKED

    if prompts == 0 and calls == 0:
        return ExecutionMode.OPERATOR_BUILT_NO_PROVIDER

    if prompts > 0 and calls == 0:
        return ExecutionMode.MANUAL_OPERATOR_REPAIR

    return ExecutionMode.UNKNOWN


def build_task_execution_evidence(
    task_id: str,
    mode: ExecutionMode | str,
    builder_provider: Any = None,
    reviewer_provider: Any = None,
    builder_identity: Any = None,
    reviewer_identity: Any = None,
    *,
    prompt_trace_available: bool = False,
    provider_call_count: int = 0,
    actual_provider_available: bool = False,
    actual_model_available: bool = False,
    actual_token_usage_available: bool = False,
) -> dict[str, Any]:
    """Build a structured, self-describing task execution evidence dict.

    ``mode`` may be an ``ExecutionMode`` or its string value; the returned
    ``execution_mode`` is always the canonical string value.
    """
    if isinstance(mode, ExecutionMode):
        mode_value = mode.value
    else:
        mode_value = ExecutionMode(str(mode)).value

    return {
        "task_id": str(task_id),
        "execution_mode": mode_value,
        "builder_provider": builder_provider,
        "reviewer_provider": reviewer_provider,
        "builder_identity": builder_identity,
        "reviewer_identity": reviewer_identity,
        "prompt_trace_available": bool(prompt_trace_available),
        "provider_call_count": max(0, int(provider_call_count or 0)),
        "actual_provider_available": bool(actual_provider_available),
        "actual_model_available": bool(actual_model_available),
        "actual_token_usage_available": bool(actual_token_usage_available),
    }
