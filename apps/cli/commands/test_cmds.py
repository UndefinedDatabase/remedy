"""Test group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.core.models import RunState
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.storage import JobNotFoundError, load_job, save_job

if TYPE_CHECKING:
    import argparse


def _cmd_run_tests_local(job_id_str: str) -> None:
    from pathlib import Path

    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.permissions import Capability
    from packages.orchestration.permissions import is_allowed as _perm_allowed
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.test_runner import run_tests_local

    if not _perm_allowed(job, Capability.repo_test_run):
        print(
            "Error: permission repo_test_run is required.\n"
            f"Grant it with: remedy job permit {job.id} repo_test_run allow",
            file=sys.stderr,
        )
        sys.exit(1)

    target_repo_str = job.metadata.get("target_repo")
    if not target_repo_str:
        print(
            "Error: no target_repo attached to this job.\n"
            f"Attach one with: remedy job attach-repo {job.id} <repo_path>",
            file=sys.stderr,
        )
        sys.exit(1)

    data_dir = resolve_data_root()
    workspace_root = data_dir / "workspaces" / str(job_id)
    record = run_tests_local(job, workspace_root)

    log = RunLogWriter(job_id=job.id)

    if record.status == "blocked":
        log.log("test_run_completed", **{
            "test_run_id": record.test_run_id, "command": record.command,
            "status": record.status, "exit_code": record.exit_code,
            "duration_ms": record.duration_ms, "output_line_count": record.output_line_count,
            "output_bytes": record.output_bytes, "command_source_type": record.command_source_type,
            "command_source_path": record.command_source_path,
            "command_purpose": record.command_purpose,
            "command_confidence": record.command_confidence,
        })
        print(f"Error: test run blocked — {record.blocked_reason}", file=sys.stderr)
        sys.exit(1)

    log.log("test_run_completed", **{
        "test_run_id": record.test_run_id, "command": record.command,
        "status": record.status, "exit_code": record.exit_code,
        "duration_ms": record.duration_ms, "output_line_count": record.output_line_count,
        "output_bytes": record.output_bytes, "command_source_type": record.command_source_type,
        "command_source_path": record.command_source_path,
        "command_purpose": record.command_purpose,
        "command_confidence": record.command_confidence,
    })

    if "test_runs" not in job.metadata:
        job.metadata["test_runs"] = []
    job.metadata["test_runs"].append({
        "test_run_id": record.test_run_id, "command": record.command,
        "status": record.status, "exit_code": record.exit_code,
        "duration_ms": record.duration_ms, "output_path": record.output_path,
        "output_line_count": record.output_line_count, "output_bytes": record.output_bytes,
        "created_at": record.created_at,
    })
    save_job(job)

    status_sym = "PASSED" if record.status == "passed" else (
        "FAILED" if record.status == "failed" else record.status.upper()
    )
    output_info = f"output={record.output_path}" if record.output_path else "no output file"
    print(
        f"Job {job.id} | test_run_id={record.test_run_id}"
        f"  status={record.status}  cmd={record.command}"
        f"  exit={record.exit_code}  dur={record.duration_ms}ms"
        f"  {output_info}  log={log.path}"
    )
    print(f"Test run: {status_sym}")
    print("Note: raw stdout/stderr are in the workspace test_runs/ directory only.")

    if record.status not in ("passed",):
        sys.exit(1)


def _cmd_discover_commands(job_id_str: str, *, as_json: bool) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    target_repo_str = job.metadata.get("target_repo")
    if not target_repo_str:
        if as_json:
            print(_json.dumps({"job_id": str(job_id), "candidates": [], "error": "no_target_repo"}))
        else:
            print("Error: no target_repo attached.", file=sys.stderr)
        sys.exit(1)

    from pathlib import Path as _Path
    from packages.orchestration.command_discovery import discover_commands

    repo_root = _Path(target_repo_str).resolve()
    candidates = discover_commands(job, repo_root)

    if as_json:
        from collections import Counter as _Counter
        from packages.orchestration.command_discovery import select_best_test_candidate

        selected = select_best_test_candidate(candidates)
        by_purpose = dict(_Counter(c.purpose for c in candidates))
        by_source = dict(_Counter(c.source_type for c in candidates))
        by_risk = dict(_Counter(c.risk for c in candidates))
        output = {
            "version": 1,
            "job_id": str(job_id),
            "repo_root": str(repo_root),
            "candidates": [
                {
                    "id": c.id, "purpose": c.purpose, "argv": list(c.argv),
                    "display": c.display, "source_type": c.source_type,
                    "source_path": c.source_path, "confidence": c.confidence,
                    "risk": c.risk, "reason": c.reason,
                    "requires_permission": c.requires_permission,
                }
                for c in candidates
            ],
            "selected_test_candidate": {
                "id": selected.id, "purpose": selected.purpose,
                "argv": list(selected.argv), "display": selected.display,
                "source_type": selected.source_type, "source_path": selected.source_path,
                "confidence": selected.confidence, "risk": selected.risk,
            } if selected is not None else None,
            "counts": {
                "by_purpose": by_purpose, "by_source": by_source,
                "by_risk": by_risk, "total": len(candidates),
            },
        }
        print(_json.dumps(output))
        return

    if not candidates:
        print("No command candidates discovered.")
        return

    print(f"Discovered {len(candidates)} command candidate(s) in {repo_root}:")
    for c in candidates:
        risk_label = f"  risk={c.risk}" if c.risk != "low" else ""
        print(
            f"  [{c.purpose:6s}] {c.display:<30s} "
            f"source={c.source_type}:{c.source_path}  "
            f"conf={c.confidence}{risk_label}"
        )


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "test.discover": lambda args: _cmd_discover_commands(args.job_id, as_json=args.json),
    "test.run": lambda args: _cmd_run_tests_local(args.job_id),
}
