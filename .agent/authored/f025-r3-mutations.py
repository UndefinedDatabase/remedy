#!/usr/bin/env python3
"""F025 R3 G5 — red-prove tests/orchestration/test_pause_resume_cycles.py and
tests/orchestration/test_pause_resume.py against the pause wiring this round
gave the cycle executor (packages/orchestration/long_run_executor.py) and the
shared park/lift functions and R-1049/R-1050 fixes (packages/orchestration/
pingpong_job.py).

Usage: python3 -B f025-r3-mutations.py <worktree-path>

For each mutation, edits its NAMED production file INSIDE the worktree
(asserting its FROM text occurs exactly once), purges __pycache__, runs
`python3 -B -m pytest -q -p no:cacheprovider` over BOTH
tests/orchestration/test_pause_resume_cycles.py and
tests/orchestration/test_pause_resume.py from the worktree's root, restores
the original bytes, and prints one line: label, real exit code, failed count,
failing node ids. An unmutated control run brackets the eleven mutations,
first and last. Ends with "restored byte-identical: True" per target file and
"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>".
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

LRE_REL = "packages/orchestration/long_run_executor.py"
PJ_REL = "packages/orchestration/pingpong_job.py"
TEST_RELS = [
    "tests/orchestration/test_pause_resume_cycles.py",
    "tests/orchestration/test_pause_resume.py",
]

# m1 — the executor reads (and acts on) the job pause BEFORE `_should_stop`:
# a pending job pause now wins the safe point even when a stop is ALSO
# pending, instead of a stop always winning (DECISION F025 D1).
M1_FROM = """        if stop.should_stop:
            terminal = _terminal_from_stop(stop.reason, stop.source)
            stop_reason = stop.reason
            _supersede_pending_job_pause_on_stop(job, control_root_path)
            break"""
M1_TO = """        from packages.orchestration import pause_control as _pc_m1  # MUTATED m1
        if stop.should_stop and _pc_m1.pause_requested(
                str(job.job_id), control_root_path=control_root_path) is None:
            terminal = _terminal_from_stop(stop.reason, stop.source)
            stop_reason = stop.reason
            _supersede_pending_job_pause_on_stop(job, control_root_path)
            break"""

# m2 — `ready_tasks` ignores `paused_ids` entirely.
M2_FROM = """    withheld_seeds = set(blocked_ids) | set(awaiting_ids) | paused_pending"""
M2_TO = """    withheld_seeds = set(blocked_ids) | set(awaiting_ids)  # MUTATED m2: paused_ids ignored"""

# m3 — `ready_tasks` withholds the paused seeds but not their dependents.
M3_FROM = """    if withheld_seeds:
        withheld = withheld_seeds | blocked_downstream(job.tasks, withheld_seeds)
        ready = [task_id for task_id in ready if task_id not in withheld]
    return ready[:batch_size]"""
M3_TO = """    if withheld_seeds:
        _downstream_seeds = set(blocked_ids) | set(awaiting_ids)  # MUTATED m3: paused excluded
        withheld = withheld_seeds | blocked_downstream(job.tasks, _downstream_seeds)
        ready = [task_id for task_id in ready if task_id not in withheld]
    return ready[:batch_size]"""

# m4 — `paused_by_operator` is added to `REPORTED_TERMINALS`.
M4_FROM = """REPORTED_TERMINALS: frozenset[str] = frozenset({
    TERMINAL_ALL_GREEN,
    TERMINAL_STOPPED_BY_OPERATOR,
    TERMINAL_BUDGET_EXHAUSTED,
    TERMINAL_DEADLINE_REACHED,
    TERMINAL_BLOCKED,
})"""
M4_TO = """REPORTED_TERMINALS: frozenset[str] = frozenset({
    TERMINAL_ALL_GREEN,
    TERMINAL_STOPPED_BY_OPERATOR,
    TERMINAL_BUDGET_EXHAUSTED,
    TERMINAL_DEADLINE_REACHED,
    TERMINAL_BLOCKED,
    TERMINAL_PAUSED_BY_OPERATOR,  # MUTATED m4
})"""

# m5 — the relaunch runs while the mask still withholds every pending task.
M5_FROM = """        if _relaunch_pause is not None or _relaunch_withheld:
            # Still pending (job scope) or still withheld (task scope): STAYS
            # parked — no event, no save, zero task steps (E4).
            return CycleLoopResult(
                job=job, terminal_status=TERMINAL_PAUSED_BY_OPERATOR,
                job_status=TERMINAL_JOB_STATUS[TERMINAL_PAUSED_BY_OPERATOR])"""
M5_TO = """        if _relaunch_pause is not None:  # MUTATED m5: mask withholding never re-parks
            return CycleLoopResult(
                job=job, terminal_status=TERMINAL_PAUSED_BY_OPERATOR,
                job_status=TERMINAL_JOB_STATUS[TERMINAL_PAUSED_BY_OPERATOR])"""

# m6 — the relaunch never lifts the pause.
M6_FROM = """        _lift_job_pause(job)
        save_fn(job)

    while True:"""
M6_TO = """        pass  # MUTATED m6: the relaunch never lifts the pause
        save_fn(job)

    while True:"""

# m7 — the job pause is not read before a task pick INSIDE a cycle (only at
# the batch boundary).
M7_FROM = """                job_pause = _job_pause_or_raise(job, control_root_path)
                if job_pause is not None:
                    break                  # E2: end the batch; the next safe point parks
                paused_entries = _paused_entries_or_raise(job, control_root_path)"""
M7_TO = """                job_pause = None  # MUTATED m7: never read before a task pick
                paused_entries = _paused_entries_or_raise(job, control_root_path)"""

# m8 — a `PauseControlError` in the executor is swallowed and the task step
# runs (the corrupt `paused_tasks` entry is read as "no paused tasks").
M8_FROM = """    try:
        return _pc.paused_tasks(str(job.job_id), control_root_path=control_root_path)
    except _pc.PauseControlError as exc:
        raise _PauseControlErrorObserved(str(exc)) from exc"""
M8_TO = """    try:
        return _pc.paused_tasks(str(job.job_id), control_root_path=control_root_path)
    except _pc.PauseControlError:
        return ()  # MUTATED m8: swallowed, the task step runs"""

# m9 — the park settles a job-scope request although the `job_paused` write
# failed (R-1050's own gate dropped).
M9_FROM = """    # --- 4. scope `job` only: settle the request as served, event permitting --
    if signal.scope == "job" and _ledger_readable and event_written:"""
M9_TO = """    # --- 4. MUTATED m9: settles even when the job_paused write failed --------
    if signal.scope == "job" and _ledger_readable:"""

# m10 — the park drops `event_error` instead of recording it.
M10_FROM = """    except (OSError, RuntimeError, ValueError, TypeError) as exc:
        from packages.orchestration.failure_postmortem import safe_text

        job.pause["event_error"] = safe_text(
            f"job_paused_event_failed: {type(exc).__name__}: {exc}")[:500]
        return False"""
M10_TO = """    except (OSError, RuntimeError, ValueError, TypeError):
        return False  # MUTATED m10: event_error dropped"""

# m11 — a settle raising `PauseControlError` inside a served stop propagates
# out of the stop instead of being logged and swallowed.
M11_FROM = """    except (_pc.PauseControlError, StopControlError) as exc:
        import logging as _logging
        _logging.getLogger(__name__).warning(
            "pause settle failed while finalizing a stop for job %r: %s: %s",
            job.job_id, type(exc).__name__, exc,
        )"""
M11_TO = """    except ValueError:  # MUTATED m11: PauseControlError no longer caught here
        pass"""

# (label, description, target-file-relative-path, FROM, TO)
MUTATIONS = [
    ("m1", "the executor reads (and acts on) the job pause before _should_stop",
     LRE_REL, M1_FROM, M1_TO),
    ("m2", "ready_tasks ignores paused_ids", LRE_REL, M2_FROM, M2_TO),
    ("m3", "ready_tasks withholds the paused seeds but not their dependents",
     LRE_REL, M3_FROM, M3_TO),
    ("m4", "paused_by_operator is added to REPORTED_TERMINALS", LRE_REL, M4_FROM, M4_TO),
    ("m5", "the relaunch runs while the mask still withholds every pending task",
     LRE_REL, M5_FROM, M5_TO),
    ("m6", "the relaunch never lifts the pause", LRE_REL, M6_FROM, M6_TO),
    ("m7", "the job pause is not read before a task pick inside a cycle",
     LRE_REL, M7_FROM, M7_TO),
    ("m8", "a PauseControlError in the executor is swallowed and the task step runs",
     LRE_REL, M8_FROM, M8_TO),
    ("m9", "the park settles a job-scope request although the job_paused write failed",
     PJ_REL, M9_FROM, M9_TO),
    ("m10", "the park drops event_error instead of recording it", PJ_REL, M10_FROM, M10_TO),
    ("m11", "a settle raising PauseControlError inside a served stop propagates out of the stop",
     PJ_REL, M11_FROM, M11_TO),
]

TARGET_RELS = [LRE_REL, PJ_REL]


def purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        for f in sorted(cache_dir.rglob("*"), reverse=True):
            f.unlink() if f.is_file() else f.rmdir()
        cache_dir.rmdir()


def run_pytest(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", "-rf", *TEST_RELS],
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
        print("usage: f025-r3-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    originals = {rel: (worktree / rel).read_bytes() for rel in TARGET_RELS}
    all_caught = True
    restores_ok = True

    purge_pycache(worktree)
    code, out = run_pytest(worktree)
    failed, ids = parse_summary(out)
    print(report("control (before)", "unmutated control run", code, failed, ids))
    if code != 0 or failed != 0:
        all_caught = False

    for label, desc, target_rel, from_text, to_text in MUTATIONS:
        target = worktree / target_rel
        original = originals[target_rel]
        text = original.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            print(f"{label}: {desc} -- ABORT: FROM occurs {occurrences} times "
                 f"in {target_rel}, expected 1")
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
        print(f"{label}: restored byte-identical: {restored} ({target_rel})")
        restores_ok = restores_ok and restored

    purge_pycache(worktree)
    code, out = run_pytest(worktree)
    failed, ids = parse_summary(out)
    print(report("control (after)", "unmutated control run", code, failed, ids))
    if code != 0 or failed != 0:
        all_caught = False

    for rel in TARGET_RELS:
        target = worktree / rel
        final_restored = target.read_bytes() == originals[rel]
        print(f"{rel}: restored byte-identical: {final_restored}")
        restores_ok = restores_ok and final_restored

    overall = all_caught and restores_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
