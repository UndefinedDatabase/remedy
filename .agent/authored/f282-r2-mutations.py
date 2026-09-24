"""F282 R2 G5 — red proofs in a DISPOSABLE worktree: R-1041's lint rule, and the amend0923 repairs.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
A FROM/TO mutation asserts its FROM occurs EXACTLY ONCE before it is applied; a REVERT puts the
named files back to their bytes at the named commit. Every file is restored byte-for-byte after
each probe, and an unmutated control runs first and last for each test selection. pytest runs
under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
LINT_TESTS = ["tests/orchestration/test_block_lint.py"]
SELF_USE_TESTS = ["tests/orchestration/test_self_use_runner.py", "tests/orchestration/test_job_task_runner.py",
                  "tests/orchestration/test_provider_evidence_integration.py",
                  "tests/docs/test_toolchain_refresh_order.py"]
BL = "packages/orchestration/block_lint.py"
MUTATIONS = {
    "m1_payloads_never_read": (
        LINT_TESTS, BL,
        "    registered, resolved = _ledger_payload_ids(ctx)\n",
        "    registered, resolved = set(), set()\n",
    ),
    "m2_every_diff_section_counted": (
        LINT_TESTS, BL,
        '            in_ledger = line[4:].strip() == f"b/{LEDGER_PATH}"\n',
        "            in_ledger = True\n",
    ),
    "m3_every_whole_payload_counted": (
        LINT_TESTS, BL,
        '            elif name.startswith("ledger"):\n',
        "            else:\n",
    ),
}
REVERTS = {
    "r1_block_lint_before_this_round": (LINT_TESTS, "5f9e4725", [BL]),
    "r2_self_use_runner_before_amend0923": (
        SELF_USE_TESTS, "d80f12c1",
        ["packages/orchestration/self_use_runner.py", "packages/orchestration/pingpong_job.py",
         "docs/orders/toolchain-refresh.md"]),
}


def run(label: str, tests: list[str]) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *tests],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines() if " passed" in ln or " failed" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


run("control_before_lint", LINT_TESTS)
run("control_before_self_use", SELF_USE_TESTS)
for name, (tests, rel, frm, to) in MUTATIONS.items():
    path = WT / rel
    good = path.read_bytes()
    text = good.decode("utf-8")
    print(f"{name} FROM count in {rel}: {text.count(frm)}")
    if text.count(frm) != 1:
        sys.exit(f"{name}: FROM must occur exactly once; stopping")
    path.write_text(text.replace(frm, to, 1), encoding="utf-8")
    run(name, tests)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
for name, (tests, rev, rels) in REVERTS.items():
    goods = {rel: (WT / rel).read_bytes() for rel in rels}
    for rel in rels:
        old = subprocess.run(["git", "-C", str(WT), "show", f"{rev}:{rel}"], capture_output=True, check=True)
        (WT / rel).write_bytes(old.stdout)
    run(name, tests)
    for rel, good in goods.items():
        (WT / rel).write_bytes(good)
        print(f"{name} {rel} restored byte-identical: {(WT / rel).read_bytes() == good}")
run("control_after_lint", LINT_TESTS)
run("control_after_self_use", SELF_USE_TESTS)
