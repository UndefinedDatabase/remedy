#!/usr/bin/env python3
"""F025 R2 G5 — red-prove tests/orchestration/test_pause_resume.py against the
pause wiring `run_job` gained this round in packages/orchestration/pingpong_job.py.

Usage: python3 -B f025-r2-mutations.py <worktree-path>

For each mutation, edits packages/orchestration/pingpong_job.py INSIDE the
worktree (asserting its FROM text occurs exactly once), purges __pycache__, runs
`python3 -B -m pytest -q -p no:cacheprovider` over tests/orchestration/test_pause_resume.py
from the worktree's root, restores the original bytes, and prints one line: label, real exit
code, failed count, failing node ids. An unmutated control run brackets the mutations, first
and last. Ends with "restored byte-identical: True" and
"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>".
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TARGET_REL = "packages/orchestration/pingpong_job.py"
TEST_REL = "tests/orchestration/test_pause_resume.py"

# m1 — the job pause is read BEFORE the operator stop.
M1_FROM = '''    def _stop_check(*, next_task=None, previous_summaries=()):
        counters = _build_budget_counters()'''
M1_TO = '''    def _stop_check(*, next_task=None, previous_summaries=()):
        _early_pause = _pause_park_signal(next_task=next_task)  # MUTATED: pause read first
        if _early_pause is not None:
            return _early_pause
        counters = _build_budget_counters()'''

# m2 — the park settles the request BEFORE it persists the job.
M2_FROM = '''    # --- 3. the durable checkpoint --------------------------------------------
    _persist_job(job)

    # --- 4. the event, exactly once per request id ----------------------------
    already = _job_paused_event_exists(job.job_id, signal.request_id)
    _ledger_readable = already is not None
    if _ledger_readable and not already:
        pending_count = sum(1 for t in job.tasks if t.status == TASK_PENDING)
        _append_job_paused_event(job, signal, pending_count=pending_count)

    # --- 5. scope `job` only: settle the request as served ---------------------
    if signal.scope == "job" and _ledger_readable:
        try:
            pending = _pc.pause_requested(job.job_id, control_root_path=control_root_path)
            if pending is not None and pending.request_id == signal.request_id:
                _pc.settle_pause(job.job_id, pending, "served",
                                 control_root_path=control_root_path)
        except _pc.PauseControlError:
            # S3: "a failure at (5) leaves the request pending and the job
            # parked; the next run re-parks on the same request without a
            # second event and settles it."
            pass

    return job'''
M2_TO = '''    # --- MUTATED: settle (step 5) runs BEFORE persist (step 3) -----------------
    if signal.scope == "job":
        try:
            pending = _pc.pause_requested(job.job_id, control_root_path=control_root_path)
            if pending is not None and pending.request_id == signal.request_id:
                _pc.settle_pause(job.job_id, pending, "served",
                                 control_root_path=control_root_path)
        except _pc.PauseControlError:
            pass

    # --- 3. the durable checkpoint --------------------------------------------
    _persist_job(job)

    # --- 4. the event, exactly once per request id ----------------------------
    already = _job_paused_event_exists(job.job_id, signal.request_id)
    _ledger_readable = already is not None
    if _ledger_readable and not already:
        pending_count = sum(1 for t in job.tasks if t.status == TASK_PENDING)
        _append_job_paused_event(job, signal, pending_count=pending_count)

    return job'''

# m3 — the park writes `job_paused` without checking the ledger for that request id.
M3_FROM = '''    already = _job_paused_event_exists(job.job_id, signal.request_id)
    _ledger_readable = already is not None
    if _ledger_readable and not already:
        pending_count = sum(1 for t in job.tasks if t.status == TASK_PENDING)
        _append_job_paused_event(job, signal, pending_count=pending_count)'''
M3_TO = '''    already = _job_paused_event_exists(job.job_id, signal.request_id)
    _ledger_readable = already is not None
    pending_count = sum(1 for t in job.tasks if t.status == TASK_PENDING)
    _append_job_paused_event(job, signal, pending_count=pending_count)  # MUTATED: no ledger check'''

# m4 — the park leaves the in-flight task `running`.
M4_FROM = '''    # --- 1. the in-flight task goes back to pending ------------------------------
    if task is not None and task.status not in (TASK_APPLIED, TASK_PASSED, TASK_SKIPPED):
        task.status = TASK_PENDING
        task.task_attempt_state = "active"'''
M4_TO = '''    # --- 1. MUTATED: the in-flight task is left running -------------------------
    if False:
        task.status = TASK_PENDING
        task.task_attempt_state = "active"'''

# m5 — the relaunch never lifts the pause.
M5_FROM = '''    if job.state == JOB_PAUSED and job.pause:
        _first_pending = next('''
M5_TO = '''    if job.state == JOB_PAUSED and job.pause:
        return job  # MUTATED: the relaunch never lifts a pause
        _first_pending = next('''

# m6 — the relaunch dispatches a task that is still withheld.
M6_FROM = '''        if _relaunch_signal is not None:
            # Still pending (job scope) or still withheld (task scope): STAYS
            # parked — no event, no state change, no provider call.
            return job
        _lift_job_pause(job)'''
M6_TO = '''        if _relaunch_signal is not None and False:  # MUTATED: never stays parked
            return job
        _lift_job_pause(job)'''

# m7 — the pre-task safe point ignores the task mask.
M7_FROM = '''            _stop = _stop_check(next_task=task, previous_summaries=previous_summaries)'''
M7_TO = '''            _stop = _stop_check(next_task=None, previous_summaries=previous_summaries)  # MUTATED: mask never read'''

# m8 — the in-task safe point ignores a pause of the in-flight task.
M8_FROM = '''            if _sig is not None:
                return _sig
            # F025 S2 IN-TASK reading: `pingpong_loop` calls this with no
            # arguments, so `_stop_check` above only ever sees `next_task=None`
            # (no mask read) — this is the ADDITIONAL check for `task`, the
            # closure's own in-flight task, counted pending for the mask (S2).
            return _pause_park_signal(in_flight_task=task)'''
M8_TO = '''            if _sig is not None:
                return _sig
            return None  # MUTATED: in-flight task pause never checked'''

# m9 — the relaunch re-stamps `first_running_at`.
M9_FROM = '''        _lift_job_pause(job)
        _persist_job(job)'''
M9_TO = '''        _lift_job_pause(job)
        job.first_running_at = datetime.now(timezone.utc).isoformat()  # MUTATED: re-stamped
        _persist_job(job)'''

# m10 — a `PauseControlError` at a safe point is swallowed and the task dispatched.
M10_FROM = '''        except _pc.PauseControlError as exc:
            return _PauseSignal(job_id=job.job_id,
                                reason=f"{_PAUSE_ERROR_REASON_PREFIX}{exc}",
                                is_error=True)'''
M10_TO = '''        except _pc.PauseControlError as exc:
            return None  # MUTATED: swallowed, the safe point dispatches normally'''

# m11 — a served stop leaves a pending job pause unsettled.
M11_FROM = '''    from packages.orchestration import pause_control as _pc
    try:
        _pending_job_pause = _pc.pause_requested(
            job.job_id, control_root_path=control_root_path)
        if _pending_job_pause is not None:
            _pc.settle_pause(job.job_id, _pending_job_pause, "superseded_by_stop",
                             control_root_path=control_root_path)
    except Exception:  # noqa: BLE001 — a pause-settle failure must never block a stop
        pass
    # S1: the job leaves `paused` for `stopped` here (whether it was already
    # parked, or a pause was merely pending) — the record is emptied.
    job.pause = {}'''
M11_TO = '''    # MUTATED: a pending job-scope pause is left unsettled by a stop
    job.pause = {}'''

MUTATIONS = [
    ("m1", "the job pause is read BEFORE the operator stop", M1_FROM, M1_TO),
    ("m2", "the park settles the request BEFORE it persists the job", M2_FROM, M2_TO),
    ("m3", "the park writes job_paused without checking the ledger for that request id",
     M3_FROM, M3_TO),
    ("m4", "the park leaves the in-flight task running", M4_FROM, M4_TO),
    ("m5", "the relaunch never lifts the pause", M5_FROM, M5_TO),
    ("m6", "the relaunch dispatches a task that is still withheld", M6_FROM, M6_TO),
    ("m7", "the pre-task safe point ignores the task mask", M7_FROM, M7_TO),
    ("m8", "the in-task safe point ignores a pause of the in-flight task", M8_FROM, M8_TO),
    ("m9", "the relaunch re-stamps first_running_at", M9_FROM, M9_TO),
    ("m10", "a PauseControlError at a safe point is swallowed and the task dispatched",
     M10_FROM, M10_TO),
    ("m11", "a served stop leaves a pending job pause unsettled", M11_FROM, M11_TO),
]


def purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        for f in sorted(cache_dir.rglob("*"), reverse=True):
            f.unlink() if f.is_file() else f.rmdir()
        cache_dir.rmdir()


def run_pytest(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", "-rf", TEST_REL],
        cwd=str(worktree), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def parse_summary(output: str) -> tuple[int, list[str]]:
    ids = [line[len("FAILED "):].split(" - ")[0].strip()
          for line in output.splitlines() if line.startswith("FAILED ")]
    return len(ids), ids


def report(label: str, desc: str, code: int, failed: int, ids: list[str]) -> str:
    shown = ", ".join(ids) if ids else "(none)"
    return f"{label}: {desc} -- exit={code} failed={failed} failing_node_ids=[{shown}]"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f025-r2-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    target = worktree / TARGET_REL
    original = target.read_bytes()
    all_caught = True
    restores_ok = True

    purge_pycache(worktree)
    code, out = run_pytest(worktree)
    failed, ids = parse_summary(out)
    print(report("control (before)", "unmutated control run", code, failed, ids))
    if code != 0 or failed != 0:
        all_caught = False

    for label, desc, from_text, to_text in MUTATIONS:
        text = original.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            print(f"{label}: {desc} -- ABORT: FROM occurs {occurrences} times, expected 1")
            all_caught = False
            continue
        target.write_text(text.replace(from_text, to_text, 1), encoding="utf-8")

        purge_pycache(worktree)
        code, out = run_pytest(worktree)
        failed, ids = parse_summary(out)
        print(report(label, desc, code, failed, ids))
        if not (code != 0 and failed >= 1):
            all_caught = False

        target.write_bytes(original)
        restored = target.read_bytes() == original
        print(f"{label}: restored byte-identical: {restored}")
        restores_ok = restores_ok and restored

    purge_pycache(worktree)
    code, out = run_pytest(worktree)
    failed, ids = parse_summary(out)
    print(report("control (after)", "unmutated control run", code, failed, ids))
    if code != 0 or failed != 0:
        all_caught = False

    final_restored = target.read_bytes() == original
    print(f"{TARGET_REL}: restored byte-identical: {final_restored}")
    restores_ok = restores_ok and final_restored

    overall = all_caught and restores_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
