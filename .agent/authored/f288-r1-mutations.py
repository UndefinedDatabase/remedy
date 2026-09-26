"""F288 R1 G5 — mutation (red-proof) tool for the attempt id, the round events, the
envelope and their readers (DECISION F288 D1).

Takes a worktree path and, for each mutation below, edits the named file INSIDE
that worktree (asserting its FROM text occurs exactly once in the file at the
time of the edit — every mutation starts from the file's own pristine bytes,
restored after the previous mutation), runs the worktree's own
`tests/ui_server/test_sse_stream.py`, `tests/orchestration/test_teacher_narration.py`,
`tests/test_timeline.py`, `tests/orchestration/test_mint_call_sites.py`,
`tests/ui_contracts/test_humanize_catalog.py` and the node ids of the classes this
round added to `tests/orchestration/test_job_task_runner.py` and
`tests/orchestration/test_pingpong.py`, under pytest from the worktree's root —
after purging every `__pycache__` directory under it, so a stale bytecode file
cannot hide or fake a result — then restores the file's exact original bytes. An
unmutated CONTROL run happens first and last. Every mutation is a real behaviour
change the specification (S1 to S6) forbids, and every one of them must turn at
least one node red.

Usage:
    python3 -B f288-r1-mutations.py <worktree_path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

#: Run together for the control and for every mutation, from the worktree's root.
_TEST_PATHS = (
    "tests/ui_server/test_sse_stream.py",
    "tests/orchestration/test_teacher_narration.py",
    "tests/test_timeline.py",
    "tests/orchestration/test_mint_call_sites.py",
    "tests/ui_contracts/test_humanize_catalog.py",
    "tests/orchestration/test_job_task_runner.py::TestAttemptIdAndRoundEvents",
    "tests/orchestration/test_pingpong.py::TestRunPingpongAdoptsGivenRunId",
)

_PINGPONG_LOOP = "packages/orchestration/pingpong_loop.py"
_PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
_UI_SERVER = "packages/orchestration/ui_server.py"
_TIMELINE = "packages/orchestration/timeline.py"
_TEACHER_NARRATION = "packages/orchestration/teacher_narration.py"
_HUMANIZE_CATALOG = "apps/ui/src/api/humanizeCatalog.ts"

#: (label, relative file path, FROM text, TO text). FROM must occur exactly once
#: in the file at the time of the edit; every mutation starts from the file's own
#: pristine bytes, restored after the previous mutation.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    (
        "m1_run_pingpong_ignores_its_run_id_keyword",
        _PINGPONG_LOOP,
        "    if run_id:\n        result.run_id = run_id\n",
        "    if run_id and False:\n        result.run_id = run_id\n",
    ),
    (
        "m2_run_job_passes_no_run_id_to_run_pingpong",
        _PINGPONG_JOB,
        "                    resumed_from_run_id=task.run_id if resume_sessions else \"\",\n"
        "                    run_id=attempt_id,\n"
        "                )\n",
        "                    resumed_from_run_id=task.run_id if resume_sessions else \"\",\n"
        "                )\n",
    ),
    (
        "m3_task_run_started_carries_no_attempt_id",
        _PINGPONG_JOB,
        '            log.log("task_run_started", task_id=task.task_id, '
        "task_type=task.task_class,\n"
        "                    attempt_id=attempt_id)\n",
        '            log.log("task_run_started", task_id=task.task_id, '
        "task_type=task.task_class)\n",
    ),
    (
        "m4_task_round_tested_reads_fail_for_a_round_whose_test_did_not_run",
        _PINGPONG_JOB,
        "            if rnd.test_passed is not None:\n"
        '                log.log("task_round_tested", task_id=task.task_id,\n'
        '                        outcome="pass" if rnd.test_passed else "fail",\n'
        "                        round_number=rnd.round_number, attempt_id=attempt_id)\n",
        '            log.log("task_round_tested", task_id=task.task_id,\n'
        '                    outcome="pass" if rnd.test_passed else "fail",\n'
        "                    round_number=rnd.round_number, attempt_id=attempt_id)\n",
    ),
    (
        "m5_task_round_repaired_is_written_for_every_round",
        _PINGPONG_JOB,
        '            if rnd.kind == "repair":\n'
        '                log.log("task_round_repaired", task_id=task.task_id,\n'
        "                        outcome=_repair_result(rnd), round_number=rnd.round_number,\n"
        "                        attempt_id=attempt_id)\n",
        '            log.log("task_round_repaired", task_id=task.task_id,\n'
        "                    outcome=_repair_result(rnd), round_number=rnd.round_number,\n"
        "                    attempt_id=attempt_id)\n",
    ),
    (
        "m6_repair_result_answers_changed_for_an_errored_output",
        _PINGPONG_JOB,
        "    output = rnd.builder_output\n"
        "    if output is None or output.error:\n"
        '        return "error"\n'
        "    if output.files_changed:\n"
        '        return "changed"\n'
        '    return "unchanged"\n',
        "    output = rnd.builder_output\n"
        "    if output is None:\n"
        '        return "error"\n'
        "    if output.files_changed:\n"
        '        return "changed"\n'
        "    if output.error:\n"
        '        return "error"\n'
        '    return "unchanged"\n',
    ),
    (
        "m7_task_round_tested_is_written_before_task_round_repaired",
        _PINGPONG_JOB,
        '            if rnd.kind == "repair":\n'
        '                log.log("task_round_repaired", task_id=task.task_id,\n'
        "                        outcome=_repair_result(rnd), round_number=rnd.round_number,\n"
        "                        attempt_id=attempt_id)\n"
        "            if rnd.test_passed is not None:\n"
        '                log.log("task_round_tested", task_id=task.task_id,\n'
        '                        outcome="pass" if rnd.test_passed else "fail",\n'
        "                        round_number=rnd.round_number, attempt_id=attempt_id)\n",
        "            if rnd.test_passed is not None:\n"
        '                log.log("task_round_tested", task_id=task.task_id,\n'
        '                        outcome="pass" if rnd.test_passed else "fail",\n'
        "                        round_number=rnd.round_number, attempt_id=attempt_id)\n"
        '            if rnd.kind == "repair":\n'
        '                log.log("task_round_repaired", task_id=task.task_id,\n'
        "                        outcome=_repair_result(rnd), round_number=rnd.round_number,\n"
        "                        attempt_id=attempt_id)\n",
    ),
    (
        "m8_task_run_failed_carries_no_attempt_id",
        _PINGPONG_JOB,
        '            log.log("task_run_failed", task_id=task.task_id, outcome=outcome,\n'
        "                    attempt_id=attempt_id)\n",
        '            log.log("task_run_failed", task_id=task.task_id, outcome=outcome)\n',
    ),
    (
        "m9_the_envelope_adds_attempt_id_to_every_kind",
        _UI_SERVER,
        "    if kind in ATTEMPT_EVENT_KINDS:\n",
        "    if True:\n",
    ),
    (
        "m10_the_envelope_reads_attempt_id_from_the_top_level",
        _UI_SERVER,
        '        attempt_id = metadata.get("attempt_id") if isinstance(metadata, dict) '
        "else None\n",
        '        attempt_id = event.get("attempt_id")\n',
    ),
    (
        "m11_the_timeline_counts_task_round_completed_events_as_repairs",
        _TIMELINE,
        '        m = sum(1 for e in task_events if e.get("event") == "task_round_repaired")\n',
        '        m = sum(1 for e in task_events if e.get("event") == "task_round_completed")\n',
    ),
    (
        "m12_humanize_catalog_loses_its_task_round_tested_line",
        _HUMANIZE_CATALOG,
        '  "task_round_tested": "The tests of a task\'s round finished.",\n',
        "",
    ),
    (
        "m13_the_task_round_tested_narration_drops_outcome",
        _TEACHER_NARRATION,
        '    "task_round_tested": ("A round\'s tests finished: task {task_id}, '
        'round {round_number} "\n'
        '                          "(result: {outcome})"),\n',
        '    "task_round_tested": "A round\'s tests finished: task {task_id}, '
        'round {round_number} ",\n',
    ),
)


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir():
            for child in sorted(cache_dir.rglob("*"), reverse=True):
                if child.is_file():
                    child.unlink()
                else:
                    child.rmdir()
            cache_dir.rmdir()


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    """Run the fixed test selection from `root`. Returns (exit_code, failed_count, node_ids)."""
    _purge_pycache(root)
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", *_TEST_PATHS],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    failed_ids = [
        line[len("FAILED "):].split(" ", 1)[0]
        for line in result.stdout.splitlines()
        if line.startswith("FAILED ")
    ]
    return result.returncode, len(failed_ids), failed_ids


def main(worktree: str) -> bool:
    root = Path(worktree).resolve()
    all_ok = True

    exit_code, failed_count, node_ids = _run_tests(root)
    control_ok = exit_code == 0 and failed_count == 0
    all_ok = all_ok and control_ok
    print(f"control (before): exit={exit_code} failed={failed_count} nodes={node_ids}")

    originals: dict[str, bytes] = {}
    for _label, rel_path, _from_text, _to_text in MUTATIONS:
        if rel_path not in originals:
            originals[rel_path] = (root / rel_path).read_bytes()

    for label, rel_path, from_text, to_text in MUTATIONS:
        target = root / rel_path
        original_bytes = originals[rel_path]
        text = original_bytes.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected 1"
            )
        mutated_text = text.replace(from_text, to_text, 1)
        target.write_bytes(mutated_text.encode("utf-8"))

        exit_code, failed_count, node_ids = _run_tests(root)
        caught = exit_code != 0 and failed_count >= 1
        all_ok = all_ok and caught
        print(f"{label}: exit={exit_code} failed={failed_count} nodes={node_ids}")
        if not caught:
            print(f"  {label}: STAYED GREEN — not caught by the test selection")

        target.write_bytes(original_bytes)

    for rel_path, original_bytes in originals.items():
        restored = (root / rel_path).read_bytes() == original_bytes
        all_ok = all_ok and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    exit_code, failed_count, node_ids = _run_tests(root)
    control_ok_after = exit_code == 0 and failed_count == 0
    all_ok = all_ok and control_ok_after
    print(f"control (after): exit={exit_code} failed={failed_count} nodes={node_ids}")

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return all_ok


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: f288-r1-mutations.py <worktree_path>")
    ok = main(sys.argv[1])
    raise SystemExit(0 if ok else 1)
