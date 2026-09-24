"""F015 R1 G5 — mutation red-proofs of the plan-editing backend, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_plan_editing.py"]
PE = "packages/orchestration/plan_editing.py"
MUTATIONS = {
    "m1_delete_drops_the_inherited_dependencies": (
        PE,
        "            for new_dep in (gone.depends_on if dep == gone.id else [dep]):\n",
        "            for new_dep in ([] if dep == gone.id else [dep]):\n",
    ),
    "m2_the_schema_and_dag_are_not_rechecked": (
        PE,
        "        new_plan = TaskPlan.model_validate(data)\n",
        "        new_plan = TaskPlan.model_construct(**data)\n",
    ),
    "m3_the_deliverable_check_is_skipped": (
        PE,
        "        validate_deliverable_plan(_mapped_tasks(new_plan))\n",
        "        _mapped_tasks(new_plan)\n",
    ),
    "m4_an_approved_plan_stays_editable": (
        PE,
        '    if approval != "pending":\n',
        '    if approval not in ("pending", "approved"):\n',
    ),
    "m5_a_started_job_stays_editable": (
        PE,
        "    if job.state != RunState.PLANNED:\n",
        "    if job.state == RunState.FAILED:\n",
    ),
    "m6_a_stale_version_is_written": (
        PE,
        "        if expected_version != version:\n",
        "        if expected_version > version:\n",
    ),
    "m7_the_task_list_is_not_regenerated": (
        PE,
        "        job.tasks = _mapped_tasks(new_plan)\n",
        "        job.tasks = job.tasks\n",
    ),
    "m8_the_log_keeps_only_the_last_edit": (
        PE,
        "        new_body[EDIT_LOG_KEY] = [*body.get(EDIT_LOG_KEY, []), entry]\n",
        "        new_body[EDIT_LOG_KEY] = [entry]\n",
    ),
    "m9_the_version_is_not_bumped": (
        PE,
        "        new_body[PLAN_VERSION_KEY] = version + 1\n",
        "        new_body[PLAN_VERSION_KEY] = version\n",
    ),
    "m10_the_lock_is_never_taken": (
        PE,
        "                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)\n",
        "                pass\n",
    ),
    "m11_split_dependents_wait_for_the_chain_start": (
        PE,
        "    replacements = {task.id: children[-1].id}\n",
        "    replacements = {task.id: children[0].id}\n",
    ),
    "m12_merge_leaves_dependents_on_a_dropped_task": (
        PE,
        "    replacements = {t.id: merged.id for t in group[1:]}\n",
        "    replacements = {}\n",
    ),
    "m13_a_no_op_edit_is_written": (
        PE,
        "    if after == [t.model_dump() for t in plan.tasks]:\n",
        "    if False:\n",
    ),
    "m14_the_evidence_export_omits_the_log": (
        PE,
        '        "edits": new_body[EDIT_LOG_KEY],\n',
        '        "edits": [],\n',
    ),
    "m15_replay_never_checks_the_logged_result": (
        PE,
        '        if [t.model_dump() for t in plan.tasks] != entry["after"]:\n',
        "        if False:\n",
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
