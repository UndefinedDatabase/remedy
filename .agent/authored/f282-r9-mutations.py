"""F282 R9 G5 — red proofs of R-1028's and R-0950's repairs, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
A FROM/TO mutation asserts its FROM occurs EXACTLY ONCE before it is applied; a REVERT puts the
named file back to its bytes at the named commit. Every file is restored byte-for-byte after each
probe, and an unmutated control runs first and last. pytest runs under `python3 -B` (checklist
item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/runtimes/test_runtime_cleanup_scope.py", "tests/orchestration/test_run_manifest_logical_identity.py"]
CLEANUP = "tests/runtimes/runtime_cleanup.py"
IDENTITY = "tests/orchestration/test_run_manifest_logical_identity.py"
MUTATIONS = {
    "m1_a_root_matches_as_a_substring_again": (
        CLEANUP,
        '    return re.search(re.escape(root.rstrip(os.sep)) + r"(?=[/\\s]|$)", text) is not None\n',
        "    return root in text\n"),
    "m2_the_cwd_branch_matches_as_a_substring_again": (
        CLEANUP, "                    if names_path(proc.cwd(), root):\n",
        "                    if root in proc.cwd():\n"),
    "m3_the_real_runs_see_the_live_checkout_again": (
        IDENTITY, '@pytest.mark.usefixtures("frozen_remedy_identity")\n', ""),
}
REVERTS = {
    "r1_cleanup_before_this_round": ("5c43004f", CLEANUP),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfEs", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith(("FAILED", "ERROR", "SKIPPED")) or ln.endswith("s") and (" passed" in ln or " failed" in ln
                                                                                     or " error" in ln)]
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
