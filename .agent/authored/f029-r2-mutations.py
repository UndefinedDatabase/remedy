"""F029 R2 G5 — mutation-and-restore tool for round 2's subtree-rerun changes.

Usage: python3 -B .agent/authored/f029-r2-mutations.py <worktree_path>

For each mutation below, edits the named module INSIDE the given worktree
(never the primary checkout), asserting its FROM text occurs exactly once in
that file, purges the worktree's ``__pycache__`` directories, runs
``tests/orchestration/test_subtree_rerun.py`` and
``tests/orchestration/test_subtree_rerun_prepare.py`` from the worktree's
root, restores the original bytes, and prints one line per mutation naming
its label, the real exit code, the failed count and the failing node ids.
Runs an unmutated control first and last, then reports whether every
mutated file was restored byte-identical and whether every mutation was
caught.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

SR_MODULE_REL = "packages/orchestration/subtree_rerun.py"
PJ_MODULE_REL = "packages/orchestration/pingpong_job.py"
TEST_RELS = [
    "tests/orchestration/test_subtree_rerun.py",
    "tests/orchestration/test_subtree_rerun_prepare.py",
]

# (label, module, from_text, to_text)
MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1 step d compares the live head with job.worktree_head again, as before S1",
     SR_MODULE_REL,
     'if not live_head or live_head != job.worktree_head:',
     'if live_head != job.worktree_head:'),

    ("m2 S4 does not raise attempt",
     SR_MODULE_REL,
     '            task.attempt += 1\n',
     '            pass\n'),

    ("m3 S4 appends no attempt record",
     SR_MODULE_REL,
     '            task.attempts.append({\n',
     '            [].append({\n'),

    ("m4 S4 keeps worktree_commit",
     SR_MODULE_REL,
     '        task.worktree_commit = ""\n',
     '        pass\n'),

    ("m5 S4 leaves a skipped task outside the subtree as it is",
     SR_MODULE_REL,
     '        if task.task_id not in subtree_id_set and task.status == TASK_SKIPPED:\n',
     '        if False and task.task_id not in subtree_id_set '
     'and task.status == TASK_SKIPPED:\n'),

    ("m6 S4 leaves a completed job completed",
     SR_MODULE_REL,
     '    if job.state == JOB_COMPLETED:\n'
     '        job.state = JOB_PAUSED\n'
     '        job.finished_at = ""\n',
     '    if False:\n'
     '        job.state = JOB_PAUSED\n'
     '        job.finished_at = ""\n'),

    ("m7 the run_pingpong( call passes builder_model alone",
     PJ_MODULE_REL,
     '                    builder_model=(task.model_override or builder_model),\n',
     '                    builder_model=builder_model,\n'),

    ("m8 S5 releases the lock on a refusal instead of removing a worktree it created",
     SR_MODULE_REL,
     '            if handle.created:\n'
     '                W.remove(handle, keep_branch=True)\n'
     '            else:\n'
     '                W.release_lock(handle)\n'
     '            raise\n',
     '            W.release_lock(handle)\n'
     '            raise\n'),

    ("m9 S5 does not set the job_initial_tree_ref again",
     SR_MODULE_REL,
     '        if W.resolve_checkpoint_ref(job.repo_path, ref) != job.job_initial_tree:\n'
     '            W.set_checkpoint_ref(job.repo_path, ref, job.job_initial_tree)\n',
     '        if False:\n'
     '            W.set_checkpoint_ref(job.repo_path, ref, job.job_initial_tree)\n'),

    ("m10 S5 moves no stream directory",
     SR_MODULE_REL,
     '            os.replace(stream_dir, dest)\n'
     '            moved_streams[task_id] = dest_rel\n',
     '            moved_streams[task_id] = dest_rel\n'),

    ("m11 the export drops the attempts key",
     PJ_MODULE_REL,
     '                "attempts": t.attempts,\n',
     ''),

    ("m12 S4 leaves worktree_cleanup_status as it was",
     SR_MODULE_REL,
     '    job.worktree_cleanup_status = "retained"\n'
     '    job.worktree_cleanup_error = ""\n',
     '    job.worktree_cleanup_error = ""\n'),
]


def _purge_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        shutil.rmtree(path, ignore_errors=True)


def _run_tests(worktree: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_RELS],
        cwd=str(worktree), capture_output=True, text=True, timeout=300,
    )
    output = proc.stdout + proc.stderr
    failed_match = re.search(r"(\d+) failed", output)
    failed = int(failed_match.group(1)) if failed_match else 0
    failing_ids = re.findall(r"^FAILED (\S+)", output, re.MULTILINE)
    return proc.returncode, failed, failing_ids


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    originals = {
        rel: (worktree / rel).read_bytes() for rel in {SR_MODULE_REL, PJ_MODULE_REL}
    }

    print(f"worktree: {worktree}")

    exit_code, failed, failing_ids = _run_tests(worktree)
    print(f"control (before): exit={exit_code} failed={failed} failing={failing_ids}")
    all_caught = exit_code == 0 and failed == 0

    for label, rel, from_text, to_text in MUTATIONS:
        module_path = worktree / rel
        original = originals[rel]
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

    identical = True
    for rel, original in originals.items():
        restored = (worktree / rel).read_bytes()
        ok = restored == original
        print(f"restored byte-identical ({rel}): {ok}")
        identical = identical and ok
    print(f"restored byte-identical: {identical}")
    if not identical:
        all_caught = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
