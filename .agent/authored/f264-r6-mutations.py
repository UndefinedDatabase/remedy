"""F264 R6 G5 — mutation red-proofs of the steering acknowledgement, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_steering.py", "tests/orchestration/test_steering_mission.py",
         "tests/cli/test_chat_cmd.py", "tests/ui_server/test_sse_stream.py"]
ST = "packages/orchestration/steering.py"
MUTATIONS = {
    "m1_event_carries_no_restatement": (
        ST,
        '                          "understood": marker["understood"]},\n',
        "                          },\n",
    ),
    "m2_restatement_names_no_round": (
        ST,
        '    said = f"the builder follows “{text}” from round {round_number} of task {task_id} on"\n',
        '    said = f"the builder follows “{text}”"\n',
    ),
    "m3_mission_half_unnamed": (
        ST,
        "    if amendment:\n        said +=",
        "    if False:\n        said +=",
    ),
    "m4_ended_job_shown_as_waiting": (
        ST,
        "(STATUS_NOT_TAKEN_IN if ended else STATUS_WAITING)",
        "STATUS_WAITING",
    ),
    "m5_stream_drops_the_acknowledgement": (
        "packages/orchestration/ui_server.py",
        '    if kind == "steering_message_consumed":\n',
        "    if False:\n",
    ),
    "m6_task_read_from_metadata_only": (
        ST,
        '"task_id": str(event.get("task_id") or meta.get("task_id", "")),',
        '"task_id": str(meta.get("task_id", "")),',
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
