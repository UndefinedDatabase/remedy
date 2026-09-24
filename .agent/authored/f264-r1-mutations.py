"""F264 R1 G5 — mutation red-proofs of the steering record and `remedy chat`, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_steering.py", "tests/cli/test_chat_cmd.py"]
ST = "packages/orchestration/steering.py"
MUTATIONS = {
    "m1_an_ended_job_accepts": (
        ST,
        "    if job_is_terminal(job_state):\n",
        "    if False:\n",
    ),
    "m2_a_record_is_overwritten": (
        ST,
        "json_bytes(body), create_only=True,\n",
        "json_bytes(body), create_only=False,\n",
    ),
    "m3_seal_unchecked": (
        ST,
        '    if body.get("record_sha256") != _seal(body):\n',
        "    if False:\n",
    ),
    "m4_records_listed_by_name": (
        ST,
        "    return sorted(found)\n",
        "    return sorted(found, key=lambda item: item[1].name)\n",
    ),
    "m5_limit_off_by_one": (
        ST,
        "    if len(cleaned) > STEERING_MAX_CHARS:\n",
        "    if len(cleaned) > STEERING_MAX_CHARS + 1:\n",
    ),
    "m6_event_carries_no_seal": (
        ST,
        '                  "record_sha256": body["record_sha256"]},\n',
        "                  },\n",
    ),
    "m7_file_name_unchecked": (
        ST,
        '    if body.get("message_id") != Path(path).stem:\n',
        "    if False:\n",
    ),
    "m8_cli_records_the_wrong_channel": (
        "apps/cli/commands/chat_cmd.py",
        'job_state=state, channel="cli")\n',
        'job_state=state, channel="cockpit")\n',
    ),
    "m9_bare_group_form_not_routed": (
        "apps/cli/grouped.py",
        '    "chat": "send"}\n',
        "    }\n",
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
