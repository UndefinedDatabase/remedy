"""F264 R5 G5 — mutation red-proofs of the mission amendment on consumption, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_steering_mission.py", "tests/orchestration/test_steering.py",
         "tests/orchestration/test_steering_consumption.py"]
ST = "packages/orchestration/steering.py"
MUTATIONS = {
    "m1_mission_never_amended": (
        ST,
        '            amendment_id = _amend_mission(mission, record["text"], root, now) if mission else ""\n',
        '            amendment_id = ""\n',
    ),
    "m2_consumed_message_amended_again": (
        ST,
        "            if (folder / f\"{record['message_id']}.json\").exists():\n                continue\n",
        "",
    ),
    "m3_marker_names_no_amendment": (
        ST,
        '                "amendment_id": amendment_id,\n',
        '                "amendment_id": "",\n',
    ),
    "m4_failed_amendment_swallowed": (
        ST,
        "    contract = amend_mission_contract(mission.project_id, mission.id, text, root=root, now=now)\n",
        "    try:\n"
        "        contract = amend_mission_contract(mission.project_id, mission.id, text, root=root, now=now)\n"
        "    except OSError:\n"
        "        return \"\"\n",
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
