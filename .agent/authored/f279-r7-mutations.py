"""F279 R7 G5 — mutation red-proofs of the order tier and the order file's pins, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C3 commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_self_use_generator.py", "tests/docs/test_toolchain_refresh_order.py"]
GEN = "packages/orchestration/self_use_generator.py"
MUTATIONS = {
    "m1_no_cadence": (
        GEN,
        "    if last is not None and today - last < timedelta(days=ORDER_CADENCE_DAYS):\n",
        "    if False:\n",
    ),
    "m2_the_order_tier_never_answers": (
        GEN,
        "    if order_result is not None:\n        return order_result\n",
        "    if False:\n        return order_result\n",
    ),
    "m3_any_file_is_taken_as_a_job": (
        GEN,
        '    if not title or not re.search(r"^## Task 1\\b", text, re.M):\n',
        "    if False:\n",
    ),
    "m4_an_order_heading_reworded": (
        "docs/orders/toolchain-refresh.md",
        "## Task 2 — Read the release notes of every tool that moves\n",
        "## Task 2 — Read the notes\n",
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
