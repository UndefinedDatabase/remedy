"""F282 R6 G5 — red proofs of R-1004 and R-1045, in a DISPOSABLE worktree.

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
TESTS = ["tests/regression/test_data_root_guard.py", "tests/orchestration/test_toolchain_pins.py",
         "tests/orchestration/test_toolchain.py"]
CONF = "tests/conftest.py"
MUTATIONS = {
    "m1_the_walk_is_unbounded_again": (
        CONF, "        if depth + 1 >= DATA_ROOT_GUARD_DEPTH:\n", "        if False:\n"),
    "m2_one_level_only": (
        CONF, "DATA_ROOT_GUARD_DEPTH = 2\n", "DATA_ROOT_GUARD_DEPTH = 1\n"),
    "m3_uv_unpinned": (
        "pyproject.toml", '"coverage", "uv==0.12.18"]', '"coverage", "uv"]'),
}
REVERTS = {
    "r1_conftest_before_this_round": ("62c02240", CONF),
    "r2_constraints_before_this_round": ("62c02240", "constraints.txt"),
    "r3_pyproject_before_this_round": ("62c02240", "pyproject.toml"),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith(("FAILED", "ERROR")) or ln.endswith("s") and (" passed" in ln or " failed" in ln
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
