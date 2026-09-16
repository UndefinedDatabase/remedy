"""CLI handlers for Real Test Execution + Snapshot/Rollback Proof v1 (Step 1887).

`test result/list/integrity` are read-only over safe test records; `snapshot create/show` record
honest proofs. Test EXECUTION itself stays on the existing `test run`
(the contract-gated safe runner). No raw output, no shell, no arbitrary commands, no auto-revert.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _cmd_test_result(args: Any) -> None:
    from packages.orchestration.real_test_execution import get_test_run
    rec = get_test_run(str(args.test_run_id))
    if rec is None:
        print("Error: test run not found", file=sys.stderr)
        sys.exit(1)
    if getattr(args, "json", False):
        print(json.dumps(rec, indent=2))
        return
    print(f"Test run {rec.get('test_run_id')}: status={rec.get('status')} exit={rec.get('exit_code')}")


def _cmd_test_list(args: Any) -> None:
    from packages.orchestration.real_test_execution import list_test_runs
    runs = list_test_runs(str(args.job_id))
    out = {"job_id": str(args.job_id), "run_count": len(runs),
           "runs": [{"test_run_id": r.get("test_run_id"), "status": r.get("status"),
                     "exit_code": r.get("exit_code"), "created_at": r.get("created_at")}
                    for r in runs]}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    if not out["runs"]:
        print(f"No test runs for {str(args.job_id)[:8]}.")
        return
    for r in out["runs"]:
        print(f"  {r['test_run_id']}  status={r['status']}  exit={r['exit_code']}  created={r['created_at']}")


def _cmd_test_integrity(args: Any) -> None:
    from packages.orchestration.real_test_execution import test_execution_integrity
    data = test_execution_integrity()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Test execution integrity: passed={data['passed']} violations={data['violation_count']}")


def _cmd_snapshot_create(args: Any) -> None:
    from packages.orchestration.real_test_execution import (
        create_snapshot_proof,
        export_snapshot_proof_json,
    )
    proof = create_snapshot_proof(str(args.job_id))
    data = export_snapshot_proof_json(proof)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Snapshot proof {data['snapshot_id']} (strategy={data['strategy']})")
    print(f"  restore_available: {data['restore_available']} (metadata snapshot is NOT a rollback restore)")


def _cmd_snapshot_show(args: Any) -> None:
    from packages.orchestration.real_test_execution import get_snapshot_proof
    rec = get_snapshot_proof(str(args.snapshot_id))
    if rec is None:
        print("Error: snapshot proof not found", file=sys.stderr)
        sys.exit(1)
    if getattr(args, "json", False):
        print(json.dumps(rec, indent=2))
        return
    print(f"Snapshot {rec.get('snapshot_id')}: restore_available={rec.get('restore_available')}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "test.result": _cmd_test_result,
    "test.list": _cmd_test_list,
    "test.integrity": _cmd_test_integrity,
    "snapshot.create": _cmd_snapshot_create,
    "snapshot.show": _cmd_snapshot_show,
}
