"""Test group command handlers — Steps 1099-1100."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    import argparse


def _cmd_run_tests(
    job_id_str: str,
    *,
    task_id: str = "",
    intent_id: str = "",
    apply_id: str = "",
    timeout_seconds: float | None = None,
    as_json: bool = False,
) -> None:
    """Route remedy test run through the central Test Execution Service."""
    from packages.orchestration.test_execution_service import (
        TestExecutionRequest,
        execute_test_run,
    )

    request = TestExecutionRequest(
        job_id=job_id_str,
        source="cli_v1",
        task_id=task_id or "",
        intent_id=intent_id or "",
        apply_id=apply_id or "",
        requested_timeout_seconds=timeout_seconds,
    )
    result = execute_test_run(request)

    if as_json:
        from dataclasses import asdict
        print(_json.dumps(asdict(result)))
        if result.status not in ("passed",):
            sys.exit(1)
        return

    # Text output — no raw output printed
    out = sys.stdout if result.status == "passed" else sys.stderr
    _print_result_text(result, out=out)
    if result.status not in ("passed",):
        sys.exit(1)


def _print_result_text(result: object, *, out=None) -> None:
    """Print human-readable result. No raw output."""
    import sys as _sys

    from packages.orchestration.test_execution_service import TestExecutionResult
    r: TestExecutionResult = result  # type: ignore[assignment]
    if out is None:
        out = _sys.stdout

    status_sym = {
        "passed": "PASSED",
        "failed": "FAILED",
        "timeout": "TIMEOUT",
        "blocked": "BLOCKED",
        "environment_failure": "ENVIRONMENT FAILURE",
    }.get(r.status, r.status.upper())

    print(f"Test run: {status_sym}", file=out)
    if r.test_run_id:
        print(f"  run_id:   {r.test_run_id}", file=out)
    if r.command_safe:
        print(f"  command:  {r.command_safe}", file=out)
    if r.duration_ms:
        print(f"  duration: {r.duration_ms}ms", file=out)
    if r.exit_code is not None:
        print(f"  exit:     {r.exit_code}", file=out)
    if r.safe_summary:
        print(f"  summary:  {r.safe_summary}", file=out)
    if r.usage_after:
        u = r.usage_after
        print(
            f"  usage:    test_runs={u.get('test_runs_used', '?')}  "
            f"runtime={u.get('runtime_seconds_used', '?'):.1f}s",
            file=out,
        )
    if r.failure_artifact_id:
        print(f"  failure_artifact: {r.failure_artifact_id}", file=out)
    if r.next_safe_action:
        print(f"  next: {r.next_safe_action}", file=out)
    if r.status == "blocked" and r.contract_guidance:
        print(f"  grant:  {r.contract_guidance}", file=out)


def _cmd_discover_commands(job_id_str: str, *, as_json: bool) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        from packages.orchestration.storage import load_job
        job = load_job(job_id)
    except Exception as exc:
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


def _cmd_test_status(job_id_str: str, *, as_json: bool = False) -> None:
    """Show lease state, latest test run, and usage for a job. Read-only."""
    import json as _json
    from uuid import UUID

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.run_contract import ensure_contract, export_usage_json, load_usage
    from packages.orchestration.storage import JobNotFoundError, load_job

    try:
        job_id = UUID(job_id_str)
    except ValueError:
        if as_json:
            print(_json.dumps({"error": "invalid_job_id", "job_id": job_id_str}))
        else:
            print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)

    try:
        job = load_job(job_id)
    except JobNotFoundError:
        if as_json:
            print(_json.dumps({"error": "job_not_found", "job_id": job_id_str}))
        else:
            print(f"Error: job {job_id_str!r} not found.", file=sys.stderr)
        sys.exit(1)

    data_dir = resolve_data_root()
    workspace = data_dir / "workspaces" / str(job_id)
    lease_path = workspace / "test_execution.lock"

    # Check lease without acquiring it (non-blocking probe)
    lease_active = False
    if lease_path.exists():
        import fcntl
        try:
            with open(lease_path) as lf:
                fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(lf, fcntl.LOCK_UN)
        except OSError:
            lease_active = True

    contract = ensure_contract(job)
    usage = load_usage(job)
    usage_dict = export_usage_json(usage)

    # Latest test run (safe fields only, no raw output)
    test_runs: list[dict] = job.metadata.get("test_runs", [])
    latest = test_runs[-1] if test_runs else None
    latest_safe: dict = {}
    if latest:
        latest_safe = {
            "test_run_id": latest.get("test_run_id", ""),
            "status": latest.get("status", ""),
            "exit_code": latest.get("exit_code"),
            "duration_ms": latest.get("duration_ms", 0),
            "command_safe": latest.get("command_safe", ""),
            "created_at": latest.get("created_at", ""),
            "output_truncated": latest.get("output_truncated", False),
        }

    out_dict = {
        "job_id": str(job_id),
        "lease_active": lease_active,
        "lease_scope": "job",
        "contract_id": contract.contract_id,
        "usage": usage_dict,
        "run_count": len(test_runs),
        "latest_run": latest_safe,
    }

    if as_json:
        print(_json.dumps(out_dict))
        return

    print(f"Test status for job {job_id_str}")
    print(f"  lease_active:  {lease_active}")
    print(f"  contract_id:   {contract.contract_id}")
    print(f"  runs_used:     {usage_dict.get('test_runs_used', 0)} / {contract.max_test_runs}")
    print(f"  runtime_used:  {usage_dict.get('runtime_seconds_used', 0.0):.1f}s")
    if latest_safe:
        print(f"  latest_run:    {latest_safe['test_run_id']}  status={latest_safe['status']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "test.discover": lambda args: _cmd_discover_commands(args.job_id, as_json=args.json),
    "test.run": lambda args: _cmd_run_tests(
        args.job_id,
        task_id=getattr(args, "task_id", "") or "",
        intent_id=getattr(args, "intent_id", "") or "",
        apply_id=getattr(args, "apply_id", "") or "",
        timeout_seconds=float(ts) if (ts := (getattr(args, "timeout_seconds", None) or "")) else None,
        as_json=getattr(args, "json", False),
    ),
    "test.status": lambda args: _cmd_test_status(args.job_id, as_json=getattr(args, "json", False)),
}
