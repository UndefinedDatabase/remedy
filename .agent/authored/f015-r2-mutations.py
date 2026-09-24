"""F015 R2 G5 — mutation red-proofs of the approval under the lock and the job plan-* CLI, in a
DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_plan_editing.py", "tests/cli/test_job_plan_cmd.py",
         "tests/ui_server/test_command_dispatch.py"]
PE = "packages/orchestration/plan_editing.py"
CMD = "apps/cli/commands/job_plan_cmd.py"
DEC = "apps/cli/commands/decision.py"
UI = "packages/orchestration/ui_server.py"
MUTATIONS = {
    "m1_the_door_copy_is_approved": (
        PE,
        "        job.task_plan = body\n",
        "        pass\n",
    ),
    "m2_a_closed_approval_is_consumed_again": (
        PE,
        '        if not isinstance(body, dict) or body.get("_approval") != "pending":\n',
        "        if not isinstance(body, dict):\n",
    ),
    "m3_the_cli_door_approves_its_own_copy": (
        DEC,
        "    from packages.orchestration.plan_editing import PlanEditRefused, consume_plan_approval\n",
        "    from packages.orchestration.job_plan import resolve_task_plan_approval as consume_plan_approval\n"
        "    from packages.orchestration.plan_editing import PlanEditRefused\n",
    ),
    "m4_the_ui_door_approves_its_own_copy": (
        UI,
        "                PlanEditRefused,\n                consume_plan_approval,\n            )\n",
        "                PlanEditRefused,\n            )\n"
        "            from packages.orchestration.job_plan import (\n"
        "                resolve_task_plan_approval as consume_plan_approval,\n            )\n",
    ),
    "m5_not_ready_refusals_exit_one": (
        CMD,
        "        if exc.code in _NOT_READY_REFUSALS:\n",
        "        if False:\n",
    ),
    "m6_usage_refusals_exit_one": (
        CMD,
        "        if exc.code in _USAGE_REFUSALS:\n",
        "        if False:\n",
    ),
    "m7_plan_show_calls_every_plan_editable": (
        CMD,
        "    refusal = edit_window_refusal(job, body)\n",
        "    refusal = None\n",
    ),
    "m8_reorder_reads_no_sequence": (
        CMD,
        '        "order": _ids(getattr(args, "sequence", ""))}),\n',
        '        "order": _ids(getattr(args, "order", ""))}),\n',
    ),
    "m9_split_hands_over_no_groups": (
        CMD,
        '    groups = [_indexes(group, json_output=json_output) for group in getattr(args, "group", None) or []]\n',
        "    groups = []\n",
    ),
    "m10_band_is_not_the_backends_field": (
        CMD,
        '                          ("band", "est_tokens_band"), ("files_hint", "files_hint")):\n',
        '                          ("band", "band"), ("files_hint", "files_hint")):\n',
    ),
    "m11_a_missing_version_is_not_named": (
        CMD,
        "    if raw is None:\n",
        "    if False:\n",
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
