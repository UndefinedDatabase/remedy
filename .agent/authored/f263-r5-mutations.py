"""F263 R5 G5 — red proofs of in-run absorption, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path> <base-sha>. The worktree must be at the round's
test commit. `old_runner` first puts `packages/orchestration/pingpong_job.py` back to its bytes at
<base-sha> — the runner that BLOCKS on drift — so the demo case shows the old behaviour before
the new one (T2_F263.md, Orchestrator brief). Each mutation's FROM text is then asserted to
occur EXACTLY ONCE before it is applied, every file is restored byte-for-byte after each, and an
unmutated control runs first and last. pytest runs under `python3 -B` (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
TESTS = ["tests/orchestration/test_human_change_in_run.py",
         "tests/cli/test_do_evidence_package.py"]
PJ = "packages/orchestration/pingpong_job.py"
MUTATIONS = {
    "m1_the_drift_guard_back_for_git_jobs": (
        PJ,
        "        absorbs = job_handle is not None\n",
        "        absorbs = False\n",
    ),
    "m2_run_safe_points_do_not_check": (
        PJ,
        "                    stop_check=_run_stop_check,\n",
        "                    stop_check=_stop_check,\n",
    ),
    "m3_checks_not_counted": (
        PJ,
        '    checks["count"] += 1\n',
        "",
    ),
    "m4_a_failed_check_does_not_block_before_apply": (
        PJ,
        "                _absorb_block = _absorb_here(\"pre_apply\")\n"
        "                if _absorb_block:\n",
        "                _absorb_block = _absorb_here(\"pre_apply\")\n"
        "                if False:\n",
    ),
    "m5_an_old_job_gets_no_last_known_state": (
        PJ,
        "        if absorbs and not job.target_last_known:\n"
        "            _record_target_last_known(job)\n",
        "",
    ),
    "m6_no_guard_record_for_a_git_job": (
        PJ,
        "            job.target_guard = TargetGuard()\n",
        "            pass\n",
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or ln.endswith("s") and (" passed" in ln or " failed" in ln)
            or "target_repo_mutated" in ln and ln.startswith("E ")]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


run("control_before")
path = WT / PJ
good = path.read_bytes()
old = subprocess.run(["git", "-C", str(WT), "show", f"{BASE}:{PJ}"], capture_output=True,
                     check=True).stdout
path.write_bytes(old)
run("old_runner")
path.write_bytes(good)
print(f"old_runner restored byte-identical: {path.read_bytes() == good}")
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
