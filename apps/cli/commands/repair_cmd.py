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

    try:
        result = start_repair_loop_v0(
            args.job_id,
            args.failure_artifact_id,
            create_patch_intent=create_intent,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps(export_repair_loop_json(result), indent=2))
    else:
        print(summarize_repair_loop(result))


def _cmd_failure_show(args: Any) -> None:
    """Show a test failure artifact."""
    from packages.orchestration.storage import load_job
    from packages.orchestration.test_failure_artifact import (
        TestFailureArtifact,
        export_failure_artifact_json,
        summarize_failure_artifact,
    )

    try:
        job = load_job(args.job_id)
    except Exception:
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


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "repair.start": _cmd_repair_start,
    "repair.failure-show": _cmd_failure_show,
}
