"""F282 R11 G5 — red proofs of the closure suite's one repair, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's repair commit.
A FROM/TO mutation asserts its FROM occurs EXACTLY ONCE before it is applied. Every file is restored
byte-for-byte after each probe, and an unmutated control runs first and last. pytest runs under
`python3 -B` (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TEST = "tests/orchestration/test_review_zip_hygiene.py"
NODE = f"{TEST}::TestThePackerRefusesRootLeftovers::test_the_packages_own_output_directory_is_not_its_own_detritus"
MUTATIONS = {
    "m1_both_runs_read_one_second": (
        TEST, '        second = package("20260924-000002")\n', '        second = package("20260924-000001")\n'),
    "m2_the_shim_is_not_on_path": (
        TEST, "\n                     \"PATH\": f\"{shim}{os.pathsep}{os.environ['PATH']}\"},\n", "},\n"),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfEs", NODE],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith(("FAILED", "ERROR", "SKIPPED")) or ln.endswith("s") and (" passed" in ln or " failed" in ln)]
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
