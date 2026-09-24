"""F264 R4 G5 — mutation red-proofs of steering consumption at the safe point, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_steering_consumption.py", "tests/orchestration/test_steering.py"]
LOOP = "packages/orchestration/pingpong_loop.py"
ST = "packages/orchestration/steering.py"
MUTATIONS = {
    "m1_never_consumed": (
        LOOP,
        "            steering_text = _steering_text_for_round(job_id, task_id, round_num)\n",
        '            steering_text = ""\n',
    ),
    "m2_segment_never_registered": (
        LOOP,
        "    if steering_text:\n",
        "    if False:\n",
    ),
    "m3_consumed_again_every_round": (
        ST,
        'json_bytes(marker), create_only=True,\n',
        'json_bytes(marker), create_only=False,\n',
    ),
    "m4_round_recorded_one_early": (
        ST,
        '                "round_number": int(round_number),\n',
        '                "round_number": int(round_number) - 1,\n',
    ),
    "m5_marker_seal_unchecked": (
        ST,
        '                or body.get("record_sha256") != _seal(body)\n',
        "",
    ),
    "m6_only_new_messages_carried": (
        ST,
        "    return records\n\n\ndef list_steering_consumptions(",
        "    new_ids = {m['message_id'] for m in consumed_now}\n"
        "    return [r for r in records if r['message_id'] in new_ids]\n\n\n"
        "def list_steering_consumptions(",
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
