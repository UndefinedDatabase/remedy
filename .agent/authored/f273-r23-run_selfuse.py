"""F273 R23 C2: closure precondition 6 and R-0807's real-run reading.

Generates and runs one self-use item exactly as F271's closure did, then
mirrors the finished job into the token ledger through the seam `remedy job
run` uses, and compares the ledger's rows for the job with the provider calls
its run records list.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from packages.orchestration.job_evidence import (
    _resolve_job_ledger_project_id,
    mirror_job_run_into_ledger,
)
from packages.orchestration.pingpong_loop import load_run
from packages.orchestration.self_use_findings import describe_self_use_run_defects
from packages.orchestration.self_use_generator import generate_and_append_if_empty
from packages.orchestration.self_use_runner import run_next_self_use_item
from packages.orchestration.token_ledger import (
    open_ledger,
    query_cost,
    token_ledger_path_for,
    verify_ledger,
)

OUT = Path(".agent/selfuse_f273")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    generated = generate_and_append_if_empty()
    print("generate_and_append_if_empty ->", generated.id if generated else None)
    entry, job_file, result = run_next_self_use_item(OUT, ".")
    defects = describe_self_use_run_defects(result)
    cfg = result.execution_config

    (OUT / "entry_and_job_file.txt").write_text(
        f"Entry ID: {entry.id}\n"
        f"Entry Title: {entry.title}\n"
        f"Entry Provenance: {entry.provenance}\n"
        f"Entry Consumed By: {entry.consumed_by}\n"
        f"Job File Path: {job_file}\n",
        encoding="utf-8",
    )
    (OUT / "execution_config.txt").write_text(
        f"Builder: {cfg.builder if cfg else ''}\n"
        f"Builder Model: {cfg.builder_model if cfg else ''}\n"
        f"Reviewer: {cfg.reviewer if cfg else ''}\n"
        f"Reviewer Model: {cfg.reviewer_model if cfg else ''}\n"
        f"Repair Rounds Allowed: {cfg.repair_rounds_allowed if cfg else ''}\n"
        f"Max Rounds: {cfg.max_rounds if cfg else ''}\n"
        f"Isolation: {result.isolation_mode}\n",
        encoding="utf-8",
    )
    lines = [
        f"Job ID: {result.job_id}",
        f"Job Title: {result.job_title}",
        f"Job State: {result.state}",
        f"Isolation Mode: {result.isolation_mode}",
        f"Worktree Path: {result.worktree_path}",
        f"Worktree Cleanup Status: {result.worktree_cleanup_status}",
        f"Error: {result.error}",
        "",
        "Execution:",
        f"- Builder: {cfg.builder if cfg else ''}",
        f"- Reviewer: {cfg.reviewer if cfg else ''}",
        f"- Repair Rounds: {result.repair_rounds_allowed}",
        f"- Created: {result.created_at}",
        f"- Finished: {result.finished_at}",
        "",
        "Task Summary:",
    ]
    for task in result.tasks:
        lines += [
            "",
            f"Task {task.task_id}: {task.title}",
            f"- Status: {task.status}",
            f"- Reviewer Verdict: {task.reviewer_verdict}",
            f"- Final Status: {task.final_status}",
            f"- Repair Rounds Used: {task.repair_rounds_used}",
            f"- Repair Rounds Allowed: {task.repair_rounds_allowed}",
            f"- Error: {task.error}",
        ]
    (OUT / "full_transcript.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    state = [
        f"Job State: {result.state}",
        f"Stop Reason: {result.stop_reason}",
        f"Stop Source: {result.stop_source}",
        f"Stop Request ID: {result.stop_request_id}",
        f"Stopped At: {result.stopped_at}",
        "",
        "Task States:",
    ] + [
        f"  {t.task_id}: {t.final_status or t.status} (verdict: {t.reviewer_verdict})"
        for t in result.tasks
    ]
    (OUT / "result_state.txt").write_text("\n".join(state) + "\n", encoding="utf-8")
    body = ["From describe_self_use_run_defects():", ""]
    body += [f"{i}. {d}" for i, d in enumerate(defects, 1)] or ["(empty tuple)"]
    (OUT / "run_defects.txt").write_text("\n".join(body) + "\n", encoding="utf-8")

    # R-0807: the run records' own list of provider calls, task by task.
    calls = []
    for task in result.tasks:
        run = load_run(task.run_id) if task.run_id else None
        attempts = ((run or {}).get("provider_evidence") or {}).get("provider_attempts") or []
        calls += [(task.task_id, a.get("seq"), a.get("round"), a.get("role")) for a in attempts]
    mirror = mirror_job_run_into_ledger(result.job_id)
    project = _resolve_job_ledger_project_id(result)
    ledger = token_ledger_path_for(project) if project else None
    rows = []
    if ledger is not None and ledger.exists():
        conn = open_ledger(ledger)
        try:
            rows = [tuple(r) for r in conn.execute(
                "SELECT call_id, task_id, role FROM calls WHERE job_id = ? ORDER BY call_id",
                (result.job_id,))]
        finally:
            conn.close()
    report = query_cost(project_id=project, job_id=result.job_id, by="role") if project else None
    drift = verify_ledger(mirror["out_dir"], project_id=project) if project and mirror["out_dir"] else None
    measured = [
        f"Job ID: {result.job_id}",
        f"Mirror: {json.dumps(mirror, sort_keys=True)}",
        f"Ledger project: {project}",
        f"Ledger path: {ledger}",
        f"Provider calls in the run records: {len(calls)}",
    ] + [f"  call {c[0]} seq={c[1]} round={c[2]} role={c[3]}" for c in calls] + [
        f"Ledger rows for the job: {len(rows)}",
    ] + [f"  row {r[0]} task={r[1]} role={r[2]}" for r in rows] + [
        "Rows by role (query_cost by=role): "
        + (json.dumps([(r.bucket, r.calls) for r in report.rows]) if report else "None"),
        f"Total calls (query_cost): {report.total.calls if report else None}",
        "verify_ledger: " + (json.dumps({
            "checked": drift.checked, "missing_rows": drift.missing_rows,
            "orphan_rows": drift.orphan_rows, "drifted_rows": drift.drifted_rows,
            "unreadable": drift.unreadable, "has_drift": drift.has_drift,
        }) if drift else "None"),
        f"rows == calls: {len(rows) == len(calls)}",
    ]
    (OUT / "ledger_rows.txt").write_text("\n".join(measured) + "\n", encoding="utf-8")

    print(json.dumps({
        "entry": entry.id, "job_file": str(job_file), "job_id": result.job_id,
        "state": result.state, "defects": list(defects),
        "calls": len(calls), "rows": len(rows),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
