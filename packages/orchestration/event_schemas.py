"""
Event Metadata Schema Registry — exact per-event-type metadata schemas.

Different run-log event types have different exact metadata schemas.
This module is the single source of truth for what keys each event type
must have. No extra keys, no missing keys.

Public API::

    EVENT_METADATA_SCHEMAS: dict[str, frozenset[str]]
    validate_event_metadata(event_name, metadata) -> list[str]
    get_event_schema(event_name) -> frozenset[str] | None
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Schema registry — frozenset of required metadata keys per event type
# ---------------------------------------------------------------------------

EVENT_METADATA_SCHEMAS: dict[str, frozenset[str]] = {
    "agent_loop_started": frozenset({
        "cycle", "max_cycles", "decision", "stage", "reason",
        "task_count", "pending_task_count", "pending_approval_count",
        "applied_count", "test_run_count",
    }),
    "agent_loop_cycle_started": frozenset({
        "cycle", "max_cycles", "decision", "stage", "reason",
        "task_count", "pending_task_count", "pending_approval_count",
        "applied_count", "test_run_count",
    }),
    "agent_loop_completed": frozenset({
        "cycle", "max_cycles", "decision", "stage", "reason",
        "task_count", "pending_task_count", "pending_approval_count",
        "applied_count", "test_run_count",
    }),
    "agent_loop_cycle_decision": frozenset({
        "cycle", "decision", "reason", "next_action", "blocked_by",
        "token_mode", "selected_worker", "readiness_level",
    }),
    "agent_loop_stopped": frozenset({
        "final_decision", "stop_reason", "cycles_run",
        "unresolved_blocker_count",
    }),
    "context_budget_optimized": frozenset({
        "mode", "budget", "estimated_tokens", "token_savings",
        "recommended_worker", "included_section_count",
        "excluded_section_count",
    }),
    "token_policy_applied": frozenset({
        "mode", "max_context_tokens", "estimated_context_tokens",
        "local_first", "remote_model_requires_approval",
        "selected_worker",
    }),
}

# Strings that must never appear in any event metadata value
FORBIDDEN_STRINGS = frozenset({
    "stdout", "stderr", "raw_output", "command_output",
    "Traceback", "diff_preview", "approval_reason",
})


def get_event_schema(event_name: str) -> frozenset[str] | None:
    """Return the exact metadata schema for an event type, or None if unregistered."""
    return EVENT_METADATA_SCHEMAS.get(event_name)


def validate_event_metadata(event_name: str, metadata: dict[str, Any]) -> list[str]:
    """Validate metadata against the registered schema.

    Returns a list of error strings. Empty list means valid.
    Does NOT raise — caller decides what to do with errors.
    """
    schema = EVENT_METADATA_SCHEMAS.get(event_name)
    if schema is None:
        return []  # unregistered event types are not validated

    errors: list[str] = []
    got = frozenset(metadata.keys())

    extra = got - schema
    if extra:
        errors.append(f"{event_name}: extra keys {sorted(extra)}")

    missing = schema - got
    if missing:
        errors.append(f"{event_name}: missing keys {sorted(missing)}")

    return errors
