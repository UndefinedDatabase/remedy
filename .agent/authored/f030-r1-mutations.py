"""F030 R1 G5 — the red-proof tool for task-addressed steering notes (DECISION F030 D1).

Takes a worktree path (argv[1]). For each mutation below: edits the named file inside that
worktree (asserting its FROM text occurs exactly once), purges the worktree's __pycache__
directories, runs the pinned steering suite from the worktree's root, records the exit code and
every failing node id, restores the file's original bytes, and verifies the restoration is
byte-identical. Runs an unmutated control first and last. Prints one line per mutation plus a
final verdict line.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TEST_ARGS = [
    "tests/orchestration/test_steering_notes.py",
    "tests/orchestration/test_steering.py",
    "tests/orchestration/test_steering_consumption.py",
    "tests/orchestration/test_steering_mission.py",
]

# label, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1 drain consumes a note addressed to another task",
     "packages/orchestration/steering.py",
     "            if addressed_to and addressed_to != str(task_id):\n"
     "                continue  # addressed to another task: stays pending, no marker, no event\n",
     "            if False:\n"
     "                continue  # addressed to another task: stays pending, no marker, no event\n"),

    ("m2 drain returns the notes with the job-wide records",
     "packages/orchestration/steering.py",
     "    return job_wide_records\n",
     "    return records\n"),

    ("m3 a note amends the mission's contract as a job-wide message does",
     "packages/orchestration/steering.py",
     "            if addressed_to:\n"
     "                amendment = None\n"
     "                mission_id = \"\"\n"
     "            else:\n",
     "            if False:\n"
     "                amendment = None\n"
     "                mission_id = \"\"\n"
     "            else:\n"),

    ("m4 the notes are numbered from 0",
     "packages/orchestration/steering.py",
     "enumerate(records, start=1)",
     "enumerate(records, start=0)"),

    ("m5 a job-wide record always carries \"task_id\": \"\"",
     "packages/orchestration/steering.py",
     "            if task_id:\n"
     "                body[\"task_id\"] = task_id\n",
     "            body[\"task_id\"] = task_id\n"),

    ("m6 compose_builder_prompt never registers builder_operator_notes",
     "packages/orchestration/pingpong_loop.py",
     "    if operator_notes_text:\n"
     "        specs.append((\n"
     "            \"builder_operator_notes\", SegmentStabilityRank.STEERING, [operator_notes_text],\n"
     "        ))\n",
     "    if False:\n"
     "        specs.append((\n"
     "            \"builder_operator_notes\", SegmentStabilityRank.STEERING, [operator_notes_text],\n"
     "        ))\n"),

    ("m7 builder_operator_notes is registered after builder_directive",
     "packages/orchestration/pingpong_loop.py",
     "    if steering_text:\n"
     "        specs.append((\"builder_steering\", SegmentStabilityRank.STEERING, [steering_text]))\n"
     "    # F030 T001: a task-addressed operator note, VERBATIM like the steering segment above, and\n"
     "    # registered only when there are any so the golden shapes keep their manifest.\n"
     "    if operator_notes_text:\n"
     "        specs.append((\n"
     "            \"builder_operator_notes\", SegmentStabilityRank.STEERING, [operator_notes_text],\n"
     "        ))\n"
     "    specs.append((\n"
     "        \"builder_directive\", SegmentStabilityRank.STEERING,\n"
     "        [\"\\nProvide your changes and a summary of what you did.\"],\n"
     "    ))\n",
     "    if steering_text:\n"
     "        specs.append((\"builder_steering\", SegmentStabilityRank.STEERING, [steering_text]))\n"
     "    specs.append((\n"
     "        \"builder_directive\", SegmentStabilityRank.STEERING,\n"
     "        [\"\\nProvide your changes and a summary of what you did.\"],\n"
     "    ))\n"
     "    # F030 T001: a task-addressed operator note, VERBATIM like the steering segment above, and\n"
     "    # registered only when there are any so the golden shapes keep their manifest.\n"
     "    if operator_notes_text:\n"
     "        specs.append((\n"
     "            \"builder_operator_notes\", SegmentStabilityRank.STEERING, [operator_notes_text],\n"
     "        ))\n"),

    ("m8 SAFE POINT 1 passes \"\" as operator_notes_text",
     "packages/orchestration/pingpong_loop.py",
     "                operator_notes_text=operator_notes_text,\n",
     "                operator_notes_text=\"\",\n"),

    ("m9 the report lists a consumed note",
     "packages/orchestration/pingpong_job.py",
     "            if _st.note_task_id(r) == task.task_id and r[\"message_id\"] not in markers\n",
     "            if _st.note_task_id(r) == task.task_id\n"),

    ("m10 the report lists a note of a pending task",
     "packages/orchestration/pingpong_job.py",
     "        if task.status in (TASK_PENDING, TASK_RUNNING):\n"
     "            continue\n",
     "        if task.status in (TASK_RUNNING,):\n"
     "            continue\n"),

    ("m11 the text report leaves out the Steering not consumed: line",
     "packages/orchestration/pingpong_job.py",
     "        for note in steering_map.get(t.task_id, []):\n",
     "        for note in []:\n"),
]


def _purge_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    child.unlink()
            for child in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
                if child.is_dir():
                    child.rmdir()
            path.rmdir()


def _run_suite(root: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_ARGS],
        cwd=root, capture_output=True, text=True,
    )
    out = proc.stdout + proc.stderr
    failing = re.findall(r"^FAILED\s+(\S+)", out, flags=re.MULTILINE)
    match = re.search(r"(\d+) failed", out)
    failed_count = int(match.group(1)) if match else len(failing)
    return proc.returncode, failed_count, failing


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    all_caught = True

    label, exit_code, failed_count, failing = (
        "control (start)", *_run_suite(worktree))
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={failing}")
    if exit_code != 0:
        print("CONTROL RUN IS NOT GREEN — aborting.")
        return 1

    restored_all = True
    for label, rel_path, from_text, to_text in MUTATIONS:
        target = worktree / rel_path
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(from_text)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times in {rel_path} (expected 1) — SKIPPED")
            all_caught = False
            continue
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed_count, failing = _run_suite(worktree)
        finally:
            target.write_bytes(original)
        restored = target.read_bytes() == original
        restored_all = restored_all and restored
        caught = exit_code != 0 and failed_count > 0 and bool(failing)
        all_caught = all_caught and caught
        print(f"{label}: exit={exit_code} failed={failed_count} nodes={failing} "
              f"caught={caught} restored={restored}")

    label, exit_code, failed_count, failing = (
        "control (end)", *_run_suite(worktree))
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={failing}")
    if exit_code != 0:
        all_caught = False

    print(f"restored byte-identical: {restored_all}")
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught and restored_all}")
    return 0 if (all_caught and restored_all) else 1


if __name__ == "__main__":
    raise SystemExit(main())
