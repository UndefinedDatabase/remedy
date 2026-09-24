"""F282 R1 G5 — mutation red-proofs of R-0998's verdict reader, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_integrity_gate.py"]
IG = "packages/orchestration/integrity_gate.py"
MUTATIONS = {
    "m1_complete_never_checked": (
        IG,
        "    if _ctx_says_complete(ctx_text) and verdict not in _PASSING_GATE_VERDICTS:\n",
        "    if False:\n",
    ),
    "m2_any_verdict_passes": (
        IG,
        '_PASSING_GATE_VERDICTS = frozenset({"PASS", "PASS_WITH_RISKS"})\n',
        '_PASSING_GATE_VERDICTS = frozenset({"PASS", "PASS_WITH_RISKS", "FAIL", "absent"})\n',
    ),
    "m3_unreadable_reader_passes": (
        IG,
        "        return IntegrityCheck(\"live_review_verdict\", IntegrityStatus.FAIL,\n"
        "                              f\"ledger reader failed: {type(exc).__name__}: {exc}\"[:200])\n"
        "\n"
        "    # Check if context",
        "        return IntegrityCheck(\"live_review_verdict\", IntegrityStatus.PASS,\n"
        "                              f\"ledger reader failed: {type(exc).__name__}: {exc}\"[:200])\n"
        "\n"
        "    # Check if context",
    ),
    "m4_missing_gate_passes": (
        IG,
        '    if verdict in ("absent", "unparsed"):\n',
        "    if False:\n",
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
