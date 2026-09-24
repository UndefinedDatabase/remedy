"""F015 R4 G5 — mutation red-proofs of execution fidelity, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_plan_edit_execution.py",
         "tests/orchestration/test_plan_editing.py", "tests/orchestration/test_job_plan.py"]
PE = "packages/orchestration/plan_editing.py"
JP = "packages/orchestration/job_plan.py"
PJ = "packages/orchestration/pingpong_job.py"
MUTATIONS = {
    "m1_a_task_may_precede_its_dependency": (
        PE,
        "        if later:\n",
        "        if False:\n",
    ),
    "m2_the_human_approval_records_no_hash": (
        PE,
        "            body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)\n",
        "            pass\n",
    ),
    "m3_a_rejection_records_a_hash": (
        PE,
        '        if reason == "approve":\n',
        "        if True:\n",
    ),
    "m4_the_unattended_approval_records_no_hash": (
        JP,
        "    body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)\n",
        "    pass\n",
    ),
    "m5_the_hash_covers_the_bookkeeping": (
        JP,
        '    return compute_content_hash({k: v for k, v in body.items() if not k.startswith("_")})\n',
        "    return compute_content_hash(body)\n",
    ),
    "m6_the_task_list_is_not_compared": (
        JP,
        "    if planned != ids:\n",
        "    if False:\n",
    ),
    "m7_a_plan_approved_before_the_hash_is_refused": (
        JP,
        "    if not recorded:\n",
        "    if False:\n",
    ),
    "m8_the_start_never_checks_the_plan": (
        PJ,
        "    if _plan_mismatch is not None:\n",
        "    if False:\n",
    ),
    "m9_a_revision_names_no_edit": (
        PE,
        "                            edits=new_body[EDIT_LOG_KEY])\n",
        "                            edits=None)\n",
    ),
    "m10_an_edited_plan_is_used_as_generated": (
        JP,
        '        lines.append("Normalization changed nothing." if edits\n',
        '        lines.append("Normalization changed nothing." if False\n',
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
