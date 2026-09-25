#!/usr/bin/env python3
"""F025 R4 G5 — red-prove tests/cli/test_job_pause.py and
tests/ui_server/test_pause_door_live.py against the job.pause/job.unpause
wiring this round gave the shared effects (packages/orchestration/
pause_control.py), the write door (packages/orchestration/ui_server.py) and
the CLI (apps/cli/commands/job_pause_cmd.py).

Usage: python3 -B f025-r4-mutations.py <worktree-path>

For each mutation, edits its NAMED production file INSIDE the worktree
(asserting its FROM text occurs exactly once), purges __pycache__, runs
`python3 -B -m pytest -q -p no:cacheprovider` over BOTH
tests/cli/test_job_pause.py and tests/ui_server/test_pause_door_live.py from
the worktree's root, restores the original bytes, and prints one line: label,
real exit code, failed count, failing node ids. An unmutated control run
brackets the eight mutations, first and last. Ends with "restored
byte-identical: True" per target file and
"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>".

Both live door tests start a real `start_ui_server`, which pre-renders the
React shell at STARTUP and auto-builds it via npm when apps/ui/dist/ is
missing or stale relative to apps/ui/src/ — and a fresh `git worktree add`
checkout makes every src file's mtime "now", always newer than the primary
checkout's already-built dist, so that staleness check would fire here even
though nothing in apps/ui/src actually changed. Never running npm from this
tool: apps/ui/node_modules is symlinked in (G5's own instruction, removed
afterwards) and apps/ui/dist is COPIED in — not symlinked, so its mtime is
this tool's own copy time rather than the primary's older build time, and
bumped 60s into the future besides, so it is never mistaken for stale — and
REMEDY_UI_NO_AUTO_BUILD=1 is set for every test run as a third, independent
guard.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

PC_REL = "packages/orchestration/pause_control.py"
UI_REL = "packages/orchestration/ui_server.py"
JPC_REL = "apps/cli/commands/job_pause_cmd.py"
TEST_RELS = [
    "tests/cli/test_job_pause.py",
    "tests/ui_server/test_pause_door_live.py",
]

PRIMARY_CHECKOUT = Path("/home/decodeux/Repos/remedy")

# m1 — the door's pause ignores `args.task` and always pauses the job.
M1_FROM = """        args = payload.get("args")
        task = args.get("task") if isinstance(args, dict) else None
        reason = args.get("reason") if isinstance(args, dict) else ""
        result = pause_job_command(
            job, task_id=task if isinstance(task, str) and task else None,
            reason=reason if isinstance(reason, str) else "",
            source=COMMAND_EFFECT_SOURCE)"""
M1_TO = """        args = payload.get("args")
        task = args.get("task") if isinstance(args, dict) else None
        reason = args.get("reason") if isinstance(args, dict) else ""
        result = pause_job_command(
            job, task_id=None,  # MUTATED m1: args.task ignored
            reason=reason if isinstance(reason, str) else "",
            source=COMMAND_EFFECT_SOURCE)"""

# m2 — the terminal-state refusal is removed from `pause_job_command`
# (scoped to that function alone: the FROM text's tail, "already = any(",
# occurs only in pause_job_command — unpause_job_command's identical-looking
# check is followed by "pause = release_task_pause" instead).
M2_FROM = """    state = _job_state_str(job)
    if state in _TERMINAL_STATES:
        body: dict[str, Any] = {"outcome": "refused", "reason": state,
                                "scope": "task" if task_id else "job"}
        if task_id:
            body["task_id"] = task_id
        return body

    if task_id:
        refusal = _refuse_unknown_task(task_id, job)
        if refusal is not None:
            return refusal
        already = any("""
M2_TO = """    state = _job_state_str(job)  # MUTATED m2: terminal-state refusal removed

    if task_id:
        refusal = _refuse_unknown_task(task_id, job)
        if refusal is not None:
            return refusal
        already = any("""

# m3 — a task id the plan does not hold is accepted (`_refuse_unknown_task`
# is the ONE check both pause_job_command and unpause_job_command call).
M3_FROM = """    if task_id in _job_task_ids(job):
        return None
    return {"outcome": "refused", "reason": f"unknown task {task_id!r}",
           "scope": "task", "task_id": task_id}"""
M3_TO = """    return None  # MUTATED m3: every task id accepted"""

# m4 — `unpause_job_command` on a parked job answers `not_paused`.
M4_FROM = """    if state == _PARKED_STATE:
        return {"outcome": "parked", "scope": "job",
                "next": f"remedy job run {job.job_id}"}

    pending = withdraw_pause(job.job_id, control_root_path=control_root_path)"""
M4_TO = """    if False:  # MUTATED m4: parked-job check removed
        return {"outcome": "parked", "scope": "job",
                "next": f"remedy job run {job.job_id}"}

    pending = withdraw_pause(job.job_id, control_root_path=control_root_path)"""

# m5 — `task_paused` is written on every call, not only when the entry is
# created.
M5_FROM = """        if not already:
            _write_task_paused_event(job, pause)
        return {"outcome": "paused", "request_id": pause.request_id, "scope": "task","""
M5_TO = """        _write_task_paused_event(job, pause)  # MUTATED m5: written on every call
        return {"outcome": "paused", "request_id": pause.request_id, "scope": "task","""

# m6 — `task_resumed` is never written.
M6_FROM = """        _write_task_resumed_event(job, pause)
        return {"outcome": "released", "request_id": pause.request_id, "scope": "task","""
M6_TO = """        pass  # MUTATED m6: task_resumed never written
        return {"outcome": "released", "request_id": pause.request_id, "scope": "task","""

# m7 — the door answers a `refused` outcome 500 `rejected_effect` instead of
# 409 `rejected_state` (scoped to the job.pause clause: the FROM text's own
# call to `_dispatch_job_pause` occurs only there).
M7_FROM = """            try:
                accepted_body = self._dispatch_job_pause(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(409, COMMAND_PAUSE_STATE_MESSAGE))
                return"""
M7_TO = """            try:
                accepted_body = self._dispatch_job_pause(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":  # MUTATED m7
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return"""

# m8 — the CLI exits 0 on a `refused` outcome (scoped to `_cmd_job_pause`: the
# FROM text's own "job_not_pausable" token occurs only there — its
# `_cmd_job_unpause` sibling uses "job_not_unpausable").
M8_FROM = """    if result["outcome"] == "refused":
        detail = result["reason"]
        subject = f"task {task_id!r}" if task_id else f"job {job_id}"
        fail("job_not_pausable", f"{subject} was not paused — {detail}",
             json_output=json_output, job_id=job_id,
             **{k: v for k, v in result.items() if k != "outcome"})
        return"""
M8_TO = """    if result["outcome"] == "refused":
        pass  # MUTATED m8: CLI exits 0 on a refused outcome"""

# (label, description, target-file-relative-path, FROM, TO)
MUTATIONS = [
    ("m1", "the door's pause ignores args.task and always pauses the job",
     UI_REL, M1_FROM, M1_TO),
    ("m2", "the terminal-state refusal is removed from pause_job_command",
     PC_REL, M2_FROM, M2_TO),
    ("m3", "a task id the plan does not hold is accepted", PC_REL, M3_FROM, M3_TO),
    ("m4", "unpause_job_command on a parked job answers not_paused", PC_REL, M4_FROM, M4_TO),
    ("m5", "task_paused is written on every call, not only when the entry is created",
     PC_REL, M5_FROM, M5_TO),
    ("m6", "task_resumed is never written", PC_REL, M6_FROM, M6_TO),
    ("m7", "the door answers a refused outcome 500 rejected_effect instead of "
     "409 rejected_state", UI_REL, M7_FROM, M7_TO),
    ("m8", "the CLI exits 0 on a refused outcome", JPC_REL, M8_FROM, M8_TO),
]

TARGET_RELS = [PC_REL, UI_REL, JPC_REL]


def purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        for f in sorted(cache_dir.rglob("*"), reverse=True):
            f.unlink() if f.is_file() else f.rmdir()
        cache_dir.rmdir()


def run_pytest(worktree: Path) -> tuple[int, str]:
    # REMEDY_UI_NO_AUTO_BUILD is the third, independent guard against npm ever
    # running from inside this tool (see the module docstring).
    env = dict(os.environ, REMEDY_UI_NO_AUTO_BUILD="1")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", "-rf", *TEST_RELS],
        cwd=str(worktree), capture_output=True, text=True, env=env)
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
        print("usage: f025-r4-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    originals = {rel: (worktree / rel).read_bytes() for rel in TARGET_RELS}
    all_caught = True
    restores_ok = True

    node_modules_src = PRIMARY_CHECKOUT / "apps" / "ui" / "node_modules"
    node_modules_link = worktree / "apps" / "ui" / "node_modules"
    linked = False
    if node_modules_src.is_dir() and not node_modules_link.exists():
        node_modules_link.symlink_to(node_modules_src, target_is_directory=True)
        linked = True
        print(f"{node_modules_link}: symlinked from the primary checkout")

    # COPIED, not symlinked: a copy's mtime is this tool's own, always newer than
    # the freshly checked-out apps/ui/src/ this worktree carries, so the door's
    # own staleness check never has a reason to rebuild (see the module docstring).
    dist_src = PRIMARY_CHECKOUT / "apps" / "ui" / "dist"
    dist_dst = worktree / "apps" / "ui" / "dist"
    if dist_src.is_dir() and (dist_src / "index.html").is_file() and not dist_dst.exists():
        shutil.copytree(dist_src, dist_dst)
        future = time.time() + 60
        for f in dist_dst.rglob("*"):
            if f.is_file():
                os.utime(f, (future, future))
        print(f"{dist_dst}: copied from the primary checkout, mtimes bumped +60s")

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

    if linked:
        if node_modules_link.is_symlink():
            node_modules_link.unlink()
        elif node_modules_link.is_dir():
            shutil.rmtree(node_modules_link)          # defensive: never leave it behind
        print(f"{node_modules_link}: removed")

    overall = all_caught and restores_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
