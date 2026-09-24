"""F282 R3 G5 — red proofs of R-1040 and R-1005, in a DISPOSABLE worktree.

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
TESTS = ["tests/orchestration/test_job_budgets.py", "tests/orchestration/test_predictive_budget.py"]
JOB = "apps/cli/commands/job.py"
RM = "packages/orchestration/run_manifest.py"
MUTATIONS = {
    "m1_an_empty_ledger_answer_replaces_the_cost": (
        JOB, "                if _priced or _unpriced:\n", "                if True:\n"),
    "m2_the_decoder_cannot_read_its_own_z": (
        RM,
        '            parsed = _dt.fromisoformat(dl[:-1] + "+00:00" if dl.endswith("Z") else dl)\n',
        "            parsed = _dt.fromisoformat(dl)\n"),
    "m3_the_builder_binds_the_raw_budgets": (
        RM, "        budgets_snapshot = _decode_budgets_field(budgets_snapshot)\n", ""),
}
REVERTS = {
    "r1_job_py_before_this_round": ("59fa1bd8", JOB),
    "r2_run_manifest_before_this_round": ("59fa1bd8", RM),
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
