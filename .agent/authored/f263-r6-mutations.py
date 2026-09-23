"""F263 R6 G5 — red proofs of absorption at apply, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path> <base-sha>. The worktree must be at the round's
product commit. `old_apply` first puts `packages/orchestration/job_apply.py` back to its bytes at
<base-sha> — the apply that absorbs nothing — so the demo case shows the old behaviour before
the new one. Each mutation's FROM text is then asserted to occur EXACTLY ONCE before it is
applied, every file is restored byte-for-byte after each, and an unmutated control runs first
and last. pytest runs under `python3 -B` (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
TESTS = ["tests/orchestration/test_human_change_at_apply.py",
         "tests/orchestration/test_job_apply.py"]
JA = "packages/orchestration/job_apply.py"
HC = "packages/orchestration/human_change.py"
MUTATIONS = {
    "m1_apply_absorbs_nothing": (
        JA,
        '            HC.absorb_job(job, detected_by="apply")\n',
        "            pass\n",
    ),
    "m2_conflicts_not_named": (
        JA,
        "        human_changed = HC.recorded_human_changes(job.job_id)\n",
        "",
    ),
    "m3_a_failed_absorption_does_not_block": (
        JA,
        '            return _block(result, f"human_change_absorb_failed: {exc}")\n',
        "            pass\n",
    ),
    "m4_the_drift_block_back": (
        JA,
        "    result.target_guard_ok = True\n",
        "    if job.target_guard and job.target_guard.target_mutated:\n"
        '        return _block(result, "target_mutated_during_job")\n'
        "    result.target_guard_ok = True\n",
    ),
    "m5_unverified_records_counted": (
        HC,
        "        if verify_human_change_record(record):\n            continue\n",
        "",
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
path = WT / JA
good = path.read_bytes()
old = subprocess.run(["git", "-C", str(WT), "show", f"{BASE}:{JA}"], capture_output=True,
                     check=True).stdout
path.write_bytes(old)
run("old_apply")
path.write_bytes(good)
print(f"old_apply restored byte-identical: {path.read_bytes() == good}")
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
