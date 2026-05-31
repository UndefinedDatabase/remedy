"""
Repair Context v1 — safe failure summary for the next builder pass.

When tests fail after a patch apply, this module produces a structured
repair context that the next builder pass can consume. No raw stdout/stderr
or tracebacks appear in public surfaces.

Public API::

    build_repair_context(job_id, test_run_event, events) -> dict
"""

from __future__ import annotations

from typing import Any
from uuid import UUID


def build_repair_context(
    job_id: UUID,
    test_run_event: dict[str, Any],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a safe repair context from a failed test run.

    Returns a dict suitable for logging as ``repair_context_created`` event
    metadata — never contains raw stdout/stderr or tracebacks.
    """
    meta = test_run_event.get("metadata", {})
    exit_code = meta.get("exit_code", -1)

    # Determine failure kind
    failure_kind = "unknown"
    if exit_code == 1:
        failure_kind = "assertion"
    elif exit_code == 2:
        failure_kind = "syntax"
    elif exit_code == 5:
        failure_kind = "no_tests_collected"
    elif exit_code != 0:
        failure_kind = "command_failed"
    if meta.get("timeout", False):
        failure_kind = "timeout"

    # Find related apply event
    related_apply_id = ""
    for e in reversed(events):
        if e.get("event") == "source_patch_applied":
            related_apply_id = e.get("metadata", {}).get("apply_id", "")
            break

    # Find test_run_id
    test_run_id = meta.get("test_run_id", test_run_event.get("id", ""))

    # Affected files — from the related apply
    affected_files: list[str] = []
    for e in reversed(events):
        if e.get("event") == "source_patch_applied":
            am = e.get("metadata", {})
            # files_modified/files_created may be int (count) or list (paths)
            fm = am.get("files_modified", [])
            fc = am.get("files_created", [])
            if isinstance(fm, list):
                affected_files = fm[:20]
            if isinstance(fc, list):
                affected_files += fc[:10]
            # Also check target_paths from patch intent
            if not affected_files:
                tp = am.get("target_paths", [])
                if isinstance(tp, list):
                    affected_files = tp[:20]
            break

    # Safe summary — no raw output
    safe_summary = f"Test {failure_kind}: exit code {exit_code}"
    if affected_files:
        safe_summary += f", {len(affected_files)} affected file(s)"

    return {
        "version": 1,
        "job_id": str(job_id),
        "test_run_id": str(test_run_id),
        "related_apply_id": str(related_apply_id),
        "status": "failed",
        "safe_summary": safe_summary[:200],
        "failure_kind": failure_kind,
        "affected_files": affected_files[:20],
        "estimated_tokens": len(safe_summary) + len(affected_files) * 30,
        "truncated": len(affected_files) > 20,
    }
