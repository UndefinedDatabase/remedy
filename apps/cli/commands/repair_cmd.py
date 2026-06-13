"""CLI handlers for ``remedy repair`` commands — test failure repair loop."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    import argparse


def _cmd_repair_start(args: Any) -> None:
    """Start repair loop v0 for a test failure."""
    from packages.orchestration.repair_loop import (
        export_repair_loop_json,
        start_repair_loop_v0,
        summarize_repair_loop,
    )

    create_intent = str(getattr(args, "fixture_patch_intent", "false")).lower() in (
        "true", "1", "yes",
    )

    from packages.orchestration.storage import JobNotFoundError, JobStoreError

    try:
        result = start_repair_loop_v0(
            args.job_id,
            args.failure_artifact_id,
            create_patch_intent=create_intent,
        )
    except (JobNotFoundError, JobStoreError) as exc:
        print(f"Error: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps(export_repair_loop_json(result), indent=2))
    else:
        print(summarize_repair_loop(result))


def _cmd_failure_show(args: Any) -> None:
    """Show a test failure artifact."""
    from packages.orchestration.storage import JobNotFoundError, JobStoreError, load_job
    from packages.orchestration.test_failure_artifact import (
        TestFailureArtifact,
        export_failure_artifact_json,
        summarize_failure_artifact,
    )

    try:
        job = load_job(args.job_id)
    except (JobNotFoundError, JobStoreError):
        print(f"Error: job {args.job_id[:8]} not found", file=sys.stderr)
        sys.exit(1)

    failure_art = None
    for art in job.artifacts:
        if str(art.id) == args.failure_artifact_id and art.metadata.get("test_failure"):
            failure_art = art
            break

    if not failure_art:
        print(
            f"Error: failure artifact {args.failure_artifact_id[:8]} not found",
            file=sys.stderr,
        )
        sys.exit(1)

    meta = failure_art.metadata
    failure = TestFailureArtifact(
        artifact_id=args.failure_artifact_id,
        job_id=args.job_id,
        task_id=meta.get("related_task_id", ""),
        related_intent_id=meta.get("related_intent_id", ""),
        related_apply_id=meta.get("related_apply_id", ""),
        related_test_run_id=meta.get("related_test_run_id", ""),
        failing_phase=meta.get("failing_phase", "test"),
        command_safe=meta.get("command_safe", ""),
        exit_code=meta.get("exit_code"),
        safe_summary=meta.get("safe_summary", ""),
        output_ref=meta.get("output_ref", ""),
        failure_kind=meta.get("failure_kind", "unknown"),
    )

    if getattr(args, "json", False):
        print(json.dumps(export_failure_artifact_json(failure), indent=2))
    else:
        print(summarize_failure_artifact(failure))


def _cmd_repair_propose(args: Any) -> None:
    """Propose a bounded, approval-gated repair (v1). Creates a Patch Intent only."""
    from packages.orchestration.repair_loop import (
        export_repair_attempt_json,
        run_repair_attempt,
        summarize_repair_attempt,
    )
    from packages.orchestration.storage import JobNotFoundError, JobStoreError

    fixture = str(getattr(args, "fixture_builder", "false")).lower() in ("true", "1", "yes")
    source_fixture = str(getattr(args, "fixture_source_builder", "false")).lower() in ("true", "1", "yes")
    # Source fixture builder implies the fixture builder path.
    if source_fixture:
        fixture = True

    try:
        result = run_repair_attempt(
            args.job_id,
            args.failure_artifact_id,
            fixture_builder=fixture,
            source_fixture_builder=source_fixture,
        )
    except (JobNotFoundError, JobStoreError) as exc:
        print(f"Error: {type(exc).__name__}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps(export_repair_attempt_json(result), indent=2))
    else:
        print(summarize_repair_attempt(result))


def _cmd_repair_status(args: Any) -> None:
    """Show repair attempts and approval state (read-only)."""
    from packages.orchestration.approval_queue import get_patch_intent
    from packages.orchestration.repair_loop import load_repair_attempts
    from packages.orchestration.storage import JobNotFoundError, JobStoreError, load_job

    try:
        job = load_job(args.job_id)
    except (JobNotFoundError, JobStoreError):
        print(f"Error: job {str(args.job_id)[:8]} not found", file=sys.stderr)
        sys.exit(1)

    filter_fa = getattr(args, "failure_artifact_id", None)
    attempts = load_repair_attempts(job)
    rows = []
    for attempt in attempts.values():
        if filter_fa and attempt.failure_artifact_id != filter_fa:
            continue
        approval_state = ""
        if attempt.repair_intent_id:
            intent = get_patch_intent(job, attempt.repair_intent_id)
            approval_state = intent.get("state", "") if intent else "unresolved"
        rows.append({
            "attempt_id": attempt.attempt_id,
            "failure_artifact_id": attempt.failure_artifact_id,
            "repair_task_id": attempt.repair_task_id,
            "repair_intent_id": attempt.repair_intent_id,
            "status": attempt.status,
            "stop_reason": attempt.stop_reason,
            "approval_state": approval_state,
            "repair_kind": attempt.repair_kind,
            "expected_effect": attempt.expected_effect,
            "resolved_failure": attempt.resolved_failure,
            "updated_at": attempt.updated_at,
        })

    if getattr(args, "json", False):
        print(json.dumps({"version": 1, "job_id": str(args.job_id), "attempts": rows}, indent=2))
        return

    if not rows:
        print(f"No repair attempts for job {str(args.job_id)[:8]}.")
        return
    print(f"Repair attempts: {str(args.job_id)[:8]}")
    for r in rows:
        line = f"  [{r['status']}] {r['attempt_id'][:8]} failure={r['failure_artifact_id'][:8]}"
        if r["repair_intent_id"]:
            line += f" intent={r['repair_intent_id']} approval={r['approval_state']}"
        elif r["repair_task_id"]:
            line += f" fix_task={r['repair_task_id'][:8]}"
        print(line)


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "repair.start": _cmd_repair_start,
    "repair.failure-show": _cmd_failure_show,
    "repair.propose": _cmd_repair_propose,
    "repair.status": _cmd_repair_status,
}
