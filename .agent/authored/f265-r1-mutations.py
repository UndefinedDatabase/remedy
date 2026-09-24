"""F265 R1 G5 — mutation red-proofs of the lesson generator and its hook, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_lessons.py"]
LS = "packages/orchestration/lessons.py"
PJ = "packages/orchestration/pingpong_job.py"
MUTATIONS = {
    "m1_ungrounded_constructs_taught": (
        LS,
        '        if any(construct["name"] in line for line in added):\n',
        "        if True:\n",
    ),
    "m2_removed_lines_count_as_added": (
        LS,
        '            if line.startswith("+") and not line.startswith("+++")]\n',
        '            if line[:1] in "+-" and not line.startswith(("+++", "---"))]\n',
    ),
    "m3_a_stored_lesson_is_regenerated": (
        LS,
        "    if existing is not None:\n",
        "    if False:\n",
    ),
    "m4_a_spent_pot_still_calls": (
        LS,
        "    if pot.exhausted:\n",
        "    if False:\n",
    ),
    "m5_the_pot_counts_every_role": (
        LS,
        "    row = next((r for r in report.rows if r.bucket == TEACHER_ROLE), None)\n",
        "    row = report.total if report.total.calls else None\n",
    ),
    "m6_an_oversize_diff_is_sent": (
        LS,
        "    if len(diff) > LESSON_MAX_DIFF_CHARS:\n",
        "    if False:\n",
    ),
    "m7_no_ledger_still_calls": (
        LS,
        "    if project_id is None and ledger_path is None:\n",
        "    if False:\n",
    ),
    "m8_the_seal_is_unchecked": (
        LS,
        '    if body.get("record_sha256") != _seal(body):\n',
        "    if False:\n",
    ),
    "m9_the_row_is_not_keyed_on_the_run": (
        LS,
        "        project_id=project_id, call_id=f\"teacher:lesson:{body['run_id']}\")\n",
        "        project_id=project_id)\n",
    ),
    "m10_lessons_ignore_the_switch": (
        PJ,
        "        if not lessons.lessons_enabled():\n",
        "        if False:\n",
    ),
    "m11_the_hook_is_never_called": (
        PJ,
        "            _teach_task_lesson(job, task)\n",
        "",
    ),
    "m12_the_hook_names_the_task_as_the_run": (
        PJ,
        "            run_id=task.run_id, job_id=str(job.job_id), task_id=task.task_id,\n",
        "            run_id=task.task_id, job_id=str(job.job_id), task_id=task.task_id,\n",
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or " passed" in ln or " failed" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


run("control_before")
for name, (rel, frm, to) in MUTATIONS.items():
    path = WT / rel
    good = path.read_bytes()
    text = good.decode("utf-8")
    print(f"{name} FROM count in {rel}: {text.count(frm)}")
    if text.count(frm) != 1:
        sys.exit(f"{name}: FROM must occur exactly once; stopping")
    path.write_text(text.replace(frm, to, 1), encoding="utf-8")
    run(name)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
run("control_after")
