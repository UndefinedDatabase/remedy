"""F015 R3 G5 — mutation red-proofs of the write door's job plan edits, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/ui_server/test_command_dispatch.py", "tests/ui_server/test_command_channel.py"]
UI = "packages/orchestration/ui_server.py"
CAT = "apps/cli/command_catalog.py"
MUTATIONS = {
    "m1_a_door_id_runs_the_wrong_edit": (
        UI,
        '    "job.plan-delete-task": "plan_delete_task",\n',
        '    "job.plan-delete-task": "plan_edit_task",\n',
    ),
    "m2_a_missing_version_reaches_the_backend": (
        UI,
        "        if command in PLAN_EDIT_COMMAND_IDS and (\n",
        "        if False and (\n",
    ),
    "m3_the_version_rides_into_the_edit_log": (
        UI,
        '        expected_version = args.pop("expected_version")\n',
        '        expected_version = args["expected_version"]\n',
    ),
    "m4_the_editor_is_not_the_token": (
        UI,
        "            actor=token_fingerprint(self._supplied_bearer_token()))\n",
        '            actor="ui")\n',
    ),
    "m5_a_conflict_is_worded_as_a_closed_plan": (
        UI,
        '        return 409, "rejected_state", {"error": COMMAND_PLAN_CONFLICT_MESSAGE,\n',
        '        return 409, "rejected_state", {"error": COMMAND_PLAN_STATE_MESSAGE,\n',
    ),
    "m6_argument_refusals_are_not_shape_errors": (
        UI,
        '    if code in ("invalid_args", "unknown_task", "unknown_command"):\n',
        "    if False:\n",
    ),
    "m7_an_invalid_plan_hides_its_violation": (
        UI,
        '        return 409, "rejected_state", {"error": COMMAND_PLAN_INVALID_MESSAGE, "detail": detail,\n',
        '        return 409, "rejected_state", {"error": COMMAND_PLAN_INVALID_MESSAGE, "detail": "",\n',
    ),
    "m8_a_closed_plan_is_a_server_fault": (
        UI,
        '    if code in ("plan_not_editable", "no_task_plan"):\n',
        "    if False:\n",
    ),
    "m9_refusals_fall_to_the_generic_clause": (
        UI,
        "            except PlanEditRefused as exc:\n                status, outcome, body = plan_edit_refusal(\n",
        "            except KeyError as exc:\n                status, outcome, body = plan_edit_refusal(\n",
    ),
    "m10_an_edit_is_not_exposed": (
        CAT,
        '    "job.plan-edit-task",\n',
        "",
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
