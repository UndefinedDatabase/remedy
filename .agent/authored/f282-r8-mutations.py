"""F282 R8 G5 — red proofs of R-0866's repair, in a DISPOSABLE worktree.

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
TESTS = ["tests/orchestration/test_self_dogfood_execution.py", "tests/cli/test_self_dogfood_execution_cli.py"]
SE = "packages/orchestration/self_dogfood_execution.py"
MUTATIONS = {
    "m1_start_parks_again": (
        SE,
        "    _transition(attempt, AttemptState.REQUEST_PREPARED)\n"
        "    _stop_at_removed_candidate_route(attempt)\n",
        "    _transition(attempt, AttemptState.REQUEST_PREPARED)\n"
        "    _transition(attempt, AttemptState.AWAITING_EXTERNAL_CANDIDATE)\n"
        "    attempt.stop_reason = StopReason.AWAITING_EXTERNAL_CANDIDATE\n"
        '    attempt.next_safe_action = "remedy self status --json"\n'),
    "m2_reconcile_leaves_the_parked_attempt": (
        SE, "    if a.state == AttemptState.AWAITING_EXTERNAL_CANDIDATE and not a.patch_intent_id:\n",
        "    if False:\n"),
    "m3_reconcile_ends_an_attempt_with_an_intent": (
        SE, " and not a.patch_intent_id:\n", ":\n"),
    "m4_start_prepares_a_second_attempt": (
        SE,
        '    if existing and (existing.get("state") in _ACTIVE or existing.get("stop_reason")\n'
        "                     == StopReason.EXTERNAL_CANDIDATE_ROUTE_REMOVED):\n",
        '    if existing and existing.get("state") in _ACTIVE:\n'),
    "m5_next_action_loops_on_reconcile": (
        SE,
        "    if a.stop_reason == StopReason.EXTERNAL_CANDIDATE_ROUTE_REMOVED:\n"
        '        return f"remedy self status --attempt-id {a.attempt_id} --json"\n',
        ""),
}
REVERTS = {
    "r1_module_before_this_round": ("7932b7c1", SE),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfEs", *TESTS],
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
for name, (rev, rel) in REVERTS.items():
    path = WT / rel
    good = path.read_bytes()
    old = subprocess.run(["git", "-C", str(WT), "show", f"{rev}:{rel}"], capture_output=True, check=True)
    path.write_bytes(old.stdout)
    run(name)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
run("control_after")
