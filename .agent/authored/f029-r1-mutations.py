"""F029 R1 G5 — mutation-and-restore tool for packages/orchestration/subtree_rerun.py.

Usage: python3 -B .agent/authored/f029-r1-mutations.py <worktree_path>

For each mutation below, edits the module INSIDE the given worktree (never the
primary checkout), asserting its FROM text occurs exactly once in the file,
runs ``tests/orchestration/test_subtree_rerun.py`` from the worktree's root
after purging its ``__pycache__`` directories, restores the original bytes,
and prints one line per mutation naming its label, the real exit code, the
failed count and the failing node ids. Runs an unmutated control first and
last, then reports whether the restore left the file byte-identical and
whether every mutation was caught.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

MODULE_REL = "packages/orchestration/subtree_rerun.py"
TEST_REL = "tests/orchestration/test_subtree_rerun.py"

MUTATIONS: list[tuple[str, str, str]] = [
    ("m1 S2 answers the direct dependents only, with no transitive walk",
     '    while changed:\n        changed = False\n',
     '    if changed:\n        changed = False\n'),

    ("m2 S2 leaves the root out of the subtree",
     '    return [t.task_id for t in tasks if t.task_id in included]',
     '    return [t.task_id for t in tasks '
     'if t.task_id in included and t.task_id != root_task_id]'),

    ("m3 step d reads an unreadable live head ('') as matching",
     '    if live_head != job.worktree_head:',
     '    if live_head != job.worktree_head and live_head != "":'),

    ("m4 step e is skipped",
     '    if not W.worktree_matches_head(worktree_path):',
     '    if False and not W.worktree_matches_head(worktree_path):'),

    ("m5 a commit carrying no Remedy-Task trailer is classed IN the subtree",
     '        if commit["task_id"] not in subtree_id_set:\n',
     '        if commit["task_id"] not in subtree_id_set '
     'and commit["task_id"] != "":\n'),

    ("m6 step h is skipped",
     '    if interleaving:\n',
     '    if False and interleaving:\n'),

    ("m7 a path base has no entry for is left in the target tree instead of removed",
     '            if entry is None:\n'
     '                rm = subprocess.run(\n'
     '                    ["git", "update-index", "--force-remove", "--", path],\n'
     '                    cwd=str(worktree_path), env=env, capture_output=True, text=True,\n'
     '                    timeout=W.GIT_QUERY_TIMEOUT_SEC,\n'
     '                )\n'
     '                if rm.returncode != 0:\n'
     '                    raise W.WorktreeError(\n'
     '                        f"git update-index --force-remove failed for {path!r}: '
     '{rm.stderr[:200]}")\n'
     '                continue\n',
     '            if entry is None:\n'
     '                continue\n'),

    ("m8 base is the root's commit itself instead of its first parent",
     '    base = W._git(worktree_path, "rev-parse", f"{root_commit}^").strip()',
     '    base = W._git(worktree_path, "rev-parse", f"{root_commit}").strip()'),

    ("m9 S6 restores the worktree but makes no commit",
     '    reset_commit = W.commit_job_worktree(str(worktree_path), '
     'build_rerun_commit_message(job, plan))',
     '    reset_commit = W._git(worktree_path, "rev-parse", "HEAD").strip()'),

    ("m10 step g is skipped",
     '    for tid in subtree_ids:',
     '    for tid in []:'),

    ("m11 exact is always True",
     '    exact = all(commit["task_id"] in subtree_id_set for commit in commits)',
     '    exact = True'),

    ("m12 S5 leaves out the Remedy-Rerun trailer",
     '    return (subject + body\n'
     '            + f"{W.REMEDY_JOB_TRAILER}: {job.job_id}\\n"\n'
     '            + f"{RERUN_TRAILER}: {root}\\n")\n',
     '    return (subject + body\n'
     '            + f"{W.REMEDY_JOB_TRAILER}: {job.job_id}\\n")\n'),
]


def _purge_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        shutil.rmtree(path, ignore_errors=True)


def _run_tests(worktree: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_REL],
        cwd=str(worktree), capture_output=True, text=True, timeout=300,
    )
    output = proc.stdout + proc.stderr
    failed_match = re.search(r"(\d+) failed", output)
    failed = int(failed_match.group(1)) if failed_match else 0
    failing_ids = re.findall(r"^FAILED (\S+)", output, re.MULTILINE)
    return proc.returncode, failed, failing_ids


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    module_path = worktree / MODULE_REL
    original = module_path.read_bytes()

    print(f"worktree: {worktree}")

    exit_code, failed, failing_ids = _run_tests(worktree)
    print(f"control (before): exit={exit_code} failed={failed} failing={failing_ids}")
    all_caught = exit_code == 0 and failed == 0

    for label, from_text, to_text in MUTATIONS:
        text = original.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            print(f"{label}: SKIPPED — FROM text occurs {occurrences} times, expected 1")
            all_caught = False
            continue
        mutated = text.replace(from_text, to_text, 1)
        module_path.write_text(mutated, encoding="utf-8")

        exit_code, failed, failing_ids = _run_tests(worktree)
        caught = exit_code != 0 and failed > 0
        print(f"{label}: exit={exit_code} failed={failed} failing={failing_ids} caught={caught}")
        if not caught:
            all_caught = False

        module_path.write_bytes(original)

    exit_code, failed, failing_ids = _run_tests(worktree)
    print(f"control (after): exit={exit_code} failed={failed} failing={failing_ids}")
    if not (exit_code == 0 and failed == 0):
        all_caught = False

    restored = module_path.read_bytes()
    identical = restored == original
    print(f"restored byte-identical: {identical}")
    if not identical:
        all_caught = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
