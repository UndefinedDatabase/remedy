"""F285 R4 red proofs: python3 -B mutations.py <worktree>. Mutates, runs pytest, restores, reports.

Every mutation's FROM must occur exactly once in its file; the file is restored byte-identical
after each run. Each removes the token-start bound from one `sk-` pattern the landed self-use
diff bounded, and runs the stream-evidence tests. Unmutated controls run first and last.
"""
import re
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_stream_evidence.py"]
SRC = "packages/orchestration/stream_evidence.py"

MUTATIONS = [
    ("m1", "the sk- pattern loses its token-start bound", SRC,
     '    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_\\-]{20,}"),\n',
     '    re.compile(r"sk-[A-Za-z0-9_\\-]{20,}"),\n'),
    ("m2", "the sk-ant- pattern loses its token-start bound", SRC,
     '    re.compile(r"(?<![A-Za-z0-9])sk-ant-[A-Za-z0-9_\\-]{10,}"),\n',
     '    re.compile(r"sk-ant-[A-Za-z0-9_\\-]{10,}"),\n'),
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
