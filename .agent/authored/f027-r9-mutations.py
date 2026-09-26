#!/usr/bin/env python3
"""F027 R9 G5 — the red proofs for the diamond end-to-end and the R-1070 repair
(DECISION F027 D9).

Takes a worktree path. Runs an unmutated PYTEST control over the worktree's
`tests/ui_server/test_task_veto_e2e_live.py` and
`tests/ui_contracts/test_veto_controls_contract.py`, from the worktree's root, first and
last. For each of the six ordered mutations below: edits the named file INSIDE the
worktree (asserting its FROM text occurs exactly once), purges the worktree's
`__pycache__` directories, runs the same two files again, restores the bytes
BYTE-IDENTICAL, and prints the mutation's label, the run's real exit code, the failed
count and the failing test node ids. Ends with `restored byte-identical: <bool>` per
touched file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f027-r9-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
UI_SERVER = "packages/orchestration/ui_server.py"
VETO_PROPOSAL = "packages/orchestration/veto_proposal.py"
DETAIL_POPOVER = "apps/ui/src/components/detail/DetailPopover.tsx"

PYTEST_NODE_IDS = [
    "tests/ui_server/test_task_veto_e2e_live.py",
    "tests/ui_contracts/test_veto_controls_contract.py",
]

# The six ordered mutations: an exact FROM string, replaced by an exact TO string. FROM
# must occur exactly once in the pristine file.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 the linear runner dispatches a task unreachable behind a veto",
        PINGPONG_JOB,
        '            _veto_ids_so_far = [t.task_id for t in job.tasks if t.status == TASK_VETOED]\n'
        '            if _veto_ids_so_far:\n'
        '                from packages.orchestration import task_veto as _tv\n'
        '                if task.task_id in _tv.veto_unreachable(job.tasks, _veto_ids_so_far):\n'
        '                    continue                   # unreachable behind a veto: never dispatched\n',
        '            _veto_ids_so_far = [t.task_id for t in job.tasks if t.status == TASK_VETOED]\n'
        '            if _veto_ids_so_far:\n'
        '                from packages.orchestration import task_veto as _tv\n'
        '                if False and task.task_id in _tv.veto_unreachable(job.tasks, _veto_ids_so_far):\n'
        '                    continue  # MUTATED (m1): unreachable-behind-a-veto guard disabled\n',
    ),
    (
        "m2 format_job_report_text drops the Vetoed by line",
        PINGPONG_JOB,
        '        veto_info = veto_map.get(t.task_id)\n'
        '        if veto_info is not None:\n'
        '            lines.append(\n'
        '                f"      Vetoed by {veto_info.get(\'actor\', \'\')}: {veto_info.get(\'reason\', \'\')}"\n'
        '            )\n',
        '        veto_info = veto_map.get(t.task_id)\n'
        '        if False:  # MUTATED (m2): Vetoed by line dropped\n'
        '            lines.append(\n'
        '                f"      Vetoed by {veto_info.get(\'actor\', \'\')}: {veto_info.get(\'reason\', \'\')}"\n'
        '            )\n',
    ),
    (
        "m3 _build_veto_section reports no veto entry",
        UI_SERVER,
        '        return {\n'
        '            "tasks": tasks_out,\n'
        '            "vetoable_task_ids": vetoable_task_ids,\n'
        '            "unreachable_task_ids": unreachable_task_ids,\n'
        '            "error": "",\n'
        '        }\n',
        '        return {\n'
        '            "tasks": [],  # MUTATED (m3): no veto entry reported\n'
        '            "vetoable_task_ids": vetoable_task_ids,\n'
        '            "unreachable_task_ids": unreachable_task_ids,\n'
        '            "error": "",\n'
        '        }\n',
    ),
    (
        "m4 the runner's terminal accounting treats an answered veto as unanswered",
        PINGPONG_JOB,
        '                    if _vid_answer is None:\n'
        '                        _veto_terminal_settled = False\n'
        '                        continue\n',
        '                    if True:  # MUTATED (m4): an answered veto reads as unanswered\n'
        '                        _veto_terminal_settled = False\n'
        '                        continue\n',
    ),
    (
        "m5 answering replan_follow_up creates no follow-up job",
        VETO_PROPOSAL,
        '    if answer.option != _tv.REPLAN_FOLLOW_UP or not answer.follow_up_job_id:\n'
        '        return\n',
        '    return  # MUTATED (m5): never creates the follow-up job\n',
    ),
    (
        "m6 the Veto section's lead-in renders before the length check again",
        DETAIL_POPOVER,
        '          {vetoEntry.unreachableTaskIds.length === 0 ? (\n'
        '            <p>No other task depended on it.</p>\n'
        '          ) : (\n'
        '            <>\n'
        '              <p>Will not run because of this veto:</p>\n'
        '              <p>\n'
        '                {vetoEntry.unreachableTaskIds.map((id, i) => (\n'
        '                  <span key={id}>\n'
        '                    {i > 0 && ", "}\n'
        '                    <TaskLink taskId={id} title={taskTitleOf(dashboard, id)} onSelectTask={onSelectTask} />\n'
        '                  </span>\n'
        '                ))}\n'
        '              </p>\n'
        '            </>\n'
        '          )}\n',
        '          <p>Will not run because of this veto:</p>\n'
        '          {vetoEntry.unreachableTaskIds.length === 0 ? (\n'
        '            <p>No other task depended on it.</p>\n'
        '          ) : (\n'
        '            <p>\n'
        '              {vetoEntry.unreachableTaskIds.map((id, i) => (\n'
        '                <span key={id}>\n'
        '                  {i > 0 && ", "}\n'
        '                  <TaskLink taskId={id} title={taskTitleOf(dashboard, id)} onSelectTask={onSelectTask} />\n'
        '                </span>\n'
        '              ))}\n'
        '            </p>\n'
        '          )}\n',
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_pytest(worktree: Path) -> tuple[int, str]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PYTEST_NODE_IDS],
        cwd=str(worktree), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count_and_ids(output: str) -> tuple[int, list[str]]:
    ids = sorted(set(re.findall(r"^FAILED (\S+)", output, re.MULTILINE)))
    match = re.search(r"(\d+) failed", output)
    count = int(match.group(1)) if match else 0
    return count, ids


def _apply_edit(path: Path, from_text: str, to_text: str, label: str) -> bytes | None:
    """Applies one edit, asserting FROM occurs exactly once. Returns the ORIGINAL bytes on
    success (for the caller to restore), or None (with a printed reason) if it refused."""
    original = path.read_bytes()
    text = original.decode("utf-8")
    occurrences = text.count(from_text)
    if occurrences != 1:
        print(f"{label}: FROM text occurs {occurrences} times (expected 1) — aborting")
        return None
    mutated = text.replace(from_text, to_text, 1)
    path.write_bytes(mutated.encode("utf-8"))
    return original


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f027-r9-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in MUTATIONS})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    all_ok = True

    print("=" * 78)
    print("--- pytest control run (unmutated, before) ---")
    code, output = _run_pytest(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    if code != 0:
        print("PYTEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        return 1

    for label, rel_path, from_text, to_text in MUTATIONS:
        path = root / rel_path
        original = originals[rel_path]
        applied = _apply_edit(path, from_text, to_text, label)
        if applied is None:
            all_ok = False
            continue
        try:
            code, output = _run_pytest(root)
            failed_count, failing_ids = _failed_count_and_ids(output)
            caught = code != 0 and failed_count > 0
            all_ok = all_ok and caught
            tag = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_node_ids={failing_ids}{tag}")
            if not caught:
                print(output[-2000:])
        finally:
            path.write_bytes(original)

    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    print("--- pytest control run (unmutated, after) ---")
    code, output = _run_pytest(root)
    control_after_ok = code == 0
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")

    result = all_ok and all_restored and control_after_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
