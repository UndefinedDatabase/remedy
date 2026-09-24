"""F282 R4 G5 — red proofs of R-1007 and of R-1016/R-1027/R-1035, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
A FROM/TO mutation asserts its FROM occurs EXACTLY ONCE before it is applied; a REVERT puts the
named file back to its bytes at the named commit. Every file is restored byte-for-byte after
each probe, and an unmutated control runs first and last. pytest runs under `python3 -B`, so no
bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_predictive_budget.py", "tests/orchestration/test_self_use_runner.py",
         "tests/orchestration/test_claude_cli_failure_detail.py"]
LOOP = "packages/orchestration/pingpong_loop.py"
JOB = "packages/orchestration/pingpong_job.py"
RUNNER = "packages/orchestration/self_use_runner.py"
MUTATIONS = {
    "m1_a_timeout_reads_unavailable": (
        LOOP,
        '    return "provider_timeout" if is_timeout_error(error) else "provider_unavailable"\n',
        '    return "provider_unavailable"\n'),
    "m2_a_timeout_records_no_detail": (
        JOB,
        '    if getattr(result, "final_status", "") not in ("provider_unavailable", "provider_timeout"):\n',
        '    if getattr(result, "final_status", "") != "provider_unavailable":\n'),
    "m3_the_stop_forgets_the_verdict": (
        JOB,
        "                     if rd.reviewer_output), task.reviewer_verdict)\n",
        "                     if rd.reviewer_output and rd is result.rounds[-1]), task.reviewer_verdict)\n"),
    "m4_the_default_cap_ties_the_loop": (
        RUNNER,
        "        max_provider_calls = max(_MAX_PROVIDER_CALLS, loop_calls + 1)\n",
        "        max_provider_calls = _MAX_PROVIDER_CALLS\n"),
    "m5_a_passed_cap_is_raised_too": (
        RUNNER,
        "    if calls_defaulted:\n",
        "    if True:\n"),
}
REVERTS = {
    "r1_loop_before_this_round": ("a5715ae8", LOOP),
    "r2_job_before_this_round": ("a5715ae8", JOB),
    "r3_runner_before_this_round": ("a5715ae8", RUNNER),
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
for name, (rev, rel) in REVERTS.items():
    path = WT / rel
    good = path.read_bytes()
    old = subprocess.run(["git", "-C", str(WT), "show", f"{rev}:{rel}"], capture_output=True, check=True)
    path.write_bytes(old.stdout)
    run(name)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
run("control_after")
