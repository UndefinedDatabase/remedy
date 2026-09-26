"""F285 R1 red proofs: python3 -B mutations.py <worktree>. Mutates, runs pytest, restores, reports.

Every mutation's FROM must occur exactly once in its file; the file is restored byte-identical
after each run. m1-m3 break R-1058's repair and run the generator and findings tests; m4-m5 break
R-1057's and run the runner tests. Unmutated controls run first and last.
"""
import re
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_self_use_generator.py", "tests/orchestration/test_self_use_findings.py",
         "tests/orchestration/test_self_use_runner.py"]

MUTATIONS = [
    ("m1", "the ledger note is offered again", "packages/orchestration/self_use_generator.py",
     '        "- no file under `.agent/` changes.\\n"\n',
     '        "- or the reviewer records why it cannot be — either way the ledger gains a line.\\n"\n'),
    ("m2", "the builder is not told to leave the record alone",
     "packages/orchestration/self_use_generator.py",
     '        "at. Do not edit any file under `.agent/`: `.agent/live_review.md` is "\n',
     '        "at. `.agent/live_review.md` is "\n'),
    ("m3", "a pass confined to .agent/ is not named", "packages/orchestration/self_use_findings.py",
     "        if not any(not path.startswith(_RECORD_DIR) for path in changed):\n",
     "        if False:\n"),
    ("m4", "the stopped job's applied manifests are not read",
     "packages/orchestration/self_use_findings.py",
     '        if manifest is not None and manifest.status == "applied":\n',
     "        if False:\n"),
    ("m5", "the cost cap is one dollar again", "packages/orchestration/self_use_runner.py",
     "_MAX_COST_USD = 6.00\n", "_MAX_COST_USD = 1.00\n"),
]


def run(tests):
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *tests],
                       cwd=WT, capture_output=True, text=True)
    lines = [ln for ln in r.stdout.splitlines() if re.search(r"\d+ (passed|failed|skipped)", ln)]
    return r.returncode, (lines[-1] if lines else r.stdout[-300:])


def control(label):
    code, summary = run(TESTS)
    print(f"control {label}: exit {code}: {summary}")
    return code == 0


ok = control("first")
for mid, what, rel, frm, to in MUTATIONS:
    path = WT / rel
    original = path.read_bytes()
    text = original.decode("utf-8")
    count = text.count(frm)
    print(f"{mid} ({what}): FROM occurs {count}x in {rel}")
    if count != 1:
        ok = False
        continue
    path.write_text(text.replace(frm, to), encoding="utf-8")
    try:
        code, summary = run(TESTS)
    finally:
        path.write_bytes(original)
    restored = path.read_bytes() == original
    print(f"{mid}: exit {code}: {summary}; restored byte-identical: {restored}")
    ok = ok and code == 1 and "failed" in summary and restored
ok = control("last") and ok
print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {ok}")
