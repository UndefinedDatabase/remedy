"""F282 R5 G5 — red proofs of R-0999, R-1015, R-1034 and R-1000, in a DISPOSABLE worktree.

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
TESTS = ["tests/orchestration/test_repair_loop.py", "tests/orchestration/test_self_use_generator.py",
         "tests/docs/test_retired_promote_word.py", "tests/test_command_catalog.py",
         "tests/test_no_orphan_modules.py"]
LOOP = "packages/orchestration/pingpong_loop.py"
GEN = "packages/orchestration/self_use_generator.py"
CAT = "apps/cli/command_catalog.py"
ORPH = "tests/test_no_orphan_modules.py"
MUTATIONS = {
    "m1_an_empty_diff_gives_no_finding": (
        LOOP,
        "                reviewer_out.findings = [empty_change_finding(reviewer_out.summary)]\n",
        "                pass\n"),
    "m2_the_generator_copies_a_retired_word": (
        GEN,
        "        if _is_repairable(paragraph) and not RETIRED_WORD.search(paragraph):\n",
        "        if _is_repairable(paragraph):\n"),
    "m3_the_generator_pattern_drifts": (
        GEN, 'RETIRED_WORD = re.compile(r"promot", re.IGNORECASE)\n',
        'RETIRED_WORD = re.compile(r"promote", re.IGNORECASE)\n'),
    "m4_ui_stop_read_only_again": (
        CAT, '        action_class="local_state_change",\n        args=(_JSON_OPT,),\n        supports_json=True,\n    ),\n    CommandEntry(\n        command_id="ui.open",',
        '        action_class="read_only",\n        args=(_JSON_OPT,),\n        supports_json=True,\n    ),\n    CommandEntry(\n        command_id="ui.open",'),
    "m5_a_product_tree_reserved": (
        ORPH, '    "scripts/bench_sample_project/",\n)\n',
        '    "scripts/bench_sample_project/",\n    "packages/core/",\n)\n'),
}
REVERTS = {
    "r1_loop_before_this_round": ("17caab1d", LOOP),
    "r2_generator_before_this_round": ("17caab1d", GEN),
    "r3_catalog_before_this_round": ("17caab1d", CAT),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith(("FAILED", "ERROR")) or ln.endswith("s") and (" passed" in ln or " failed" in ln)]
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
