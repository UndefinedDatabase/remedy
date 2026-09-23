"""F263 R7 G3 — red proofs of the one-implementation guard, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C3 commit,
which adds `tests/orchestration/test_human_change_one_path.py`. Each mutation takes one of the
three entrances off the one path, or adds a second spelling of absorption; its FROM text is
asserted to occur EXACTLY ONCE before it is applied, every file is restored byte-for-byte after
each, and an unmutated control runs first and last. pytest runs under `python3 -B` (checklist
item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_human_change_one_path.py"]
MUTATIONS = {
    "m1_the_command_spells_its_own_absorption": (
        "apps/cli/commands/absorb_cmd.py",
        '            outcomes.append(HC.absorb_job(job, detected_by="absorb"))\n',
        '            outcomes.append(HC.absorb(job.job_id, job.repo_path, None,\n'
        '                                      detected_by="absorb", rebase=print))\n',
    ),
    "m2_the_safe_point_leaves_the_path": (
        "packages/orchestration/pingpong_job.py",
        '        HC.absorb_job(job, detected_by=f"run:{point}")\n',
        "        HC.capture_target_state(job.repo_path)\n",
    ),
    "m3_the_apply_leaves_the_path": (
        "packages/orchestration/job_apply.py",
        '            HC.absorb_job(job, detected_by="apply")\n',
        "            pass\n",
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or ln.endswith("s") and (" passed" in ln or " failed" in ln)]
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
