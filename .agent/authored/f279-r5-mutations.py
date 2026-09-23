"""F279 R5 G5 — mutation red-proofs of the block linter and its guard, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C3 commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_block_lint.py"]
LINT = "packages/orchestration/block_lint.py"
FENCE = "`" * 3
MUTATIONS = {
    "m1_a_rule_cites_a_retired_item": (
        LINT,
        '    Rule(37, "no unmeasured runs",',
        '    Rule(32, "no unmeasured runs",',
    ),
    "m2_size_limit_off_by_one": (
        LINT,
        "    return lines <= BLOCK_LINE_LIMIT, ",
        "    return lines < BLOCK_LINE_LIMIT, ",
    ),
    "m3_a_declared_new_file_is_not_exempt": (
        LINT,
        "if path not in new_files and not (ctx.repo_root / path).exists()]",
        "if not (ctx.repo_root / path).exists()]",
    ),
    "m4_a_code_fence_counts_as_a_run": (
        LINT,
        f' and line.strip() != "{FENCE}"]\n',
        "]\n",
    ),
    "m5_a_wrong_open_count_passes": (
        LINT,
        "    wrong = [n for n in stated if n != measured]\n",
        "    wrong = []\n",
    ),
    "m6_a_violation_exits_zero": (
        "apps/cli/commands/integrity_cmd.py",
        '        if violations:\n            fail("block_lint_failed",',
        '        if False:\n            fail("block_lint_failed",',
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
