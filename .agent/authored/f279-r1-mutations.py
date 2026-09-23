"""F279 R1 G5 — mutation red-proofs of the pinned-toolchain guards, run inside a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C6 commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_toolchain_pins.py", "tests/orchestration/test_ci_workflow.py"]
PSUTIL_ENTRY_START = "psutil==7.2.2 \\\n"
MUTATIONS = {
    "m1_unhashed_install": (
        ".github/workflows/ci.yml",
        "run: python3 -m pip install --require-hashes -r constraints.txt\n",
        "run: python3 -m pip install -r constraints.txt\n",
    ),
    "m2_cache_key_dropped": (
        ".github/workflows/ci.yml",
        "          cache-dependency-path: constraints.txt\n",
        "",
    ),
    "m3_ruff_pin_moved": (
        "pyproject.toml",
        '"ruff==0.15.17"',
        '"ruff==0.15.16"',
    ),
    "m4_psutil_unbounded": (
        "pyproject.toml",
        '"psutil>=5.9,<8"',
        '"psutil>=5.9"',
    ),
    "m5_ruff_hashes_stripped": (
        "constraints.txt",
        None,  # computed below: every hash line of the ruff entry
        None,
    ),
    "m6_psutil_unpinned": (
        "constraints.txt",
        None,  # computed below: the whole psutil entry
        "",
    ),
}


def entry(text: str, start: str) -> str:
    """The pin line `start` plus every indented hash line after it."""
    begin = text.index(start)
    end = begin + len(start)
    while text.startswith("    --hash=", end):
        end = text.index("\n", end) + 1
    return text[begin:end]


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or " passed" in ln or " failed" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


constraints = (WT / "constraints.txt").read_text(encoding="utf-8")
ruff_entry = entry(constraints, "ruff==0.15.17 \\\n")
MUTATIONS["m5_ruff_hashes_stripped"] = ("constraints.txt", ruff_entry, "ruff==0.15.17\n")
MUTATIONS["m6_psutil_unpinned"] = ("constraints.txt", entry(constraints, PSUTIL_ENTRY_START), "")

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
