"""F284 R1 red proofs: python3 -B mutations.py <worktree>. Mutates, runs pytest, restores, reports.

Every mutation's FROM must occur exactly once in its file; the file is restored byte-identical
after each run. m1-m4 run the R-1046 tests; m5 creates an EMPTY apps/ui/node_modules (the state
R-0499's red runs passed through) and runs the vitest node, which must skip with the repair and
fail with the old directory gate. Unmutated controls run first and last.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
R1046_TESTS = ["tests/orchestration/test_teacher_model.py", "tests/orchestration/test_lessons.py"]
VITEST_NODE = ["tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes"]

MUTATIONS = [
    ("m1", "ask_teacher reads no override", "packages/orchestration/teacher_model.py",
     "    overrides = teacher_role_overrides()\n", "    overrides = None\n", R1046_TESTS),
    ("m2", "the transport ignores the override", "packages/orchestration/teacher_model.py",
     "    transport = resolve_teacher_transport(overrides)\n",
     "    transport = resolve_teacher_transport()\n", R1046_TESTS),
    ("m3", "the lessons path hands in no override", "packages/orchestration/pingpong_job.py",
     "config_file=teacher_role_overrides(),", "config_file=None,", R1046_TESTS),
    ("m4", "the helper never reads the key", "packages/orchestration/teacher_model.py",
     '    return {"model": str(model)} if model else None\n', "    return None\n", R1046_TESTS),
    ("m5", "the vitest gate reads the directory again", "tests/orchestration/test_test_runner.py",
     'not (_ROOT / "apps" / "ui" / "node_modules" / ".bin" / "vitest").is_file(),',
     'not (_ROOT / "apps" / "ui" / "node_modules").is_dir(),', VITEST_NODE),
]


def run(tests):
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *tests],
                       cwd=WT, capture_output=True, text=True)
    lines = [ln for ln in r.stdout.splitlines() if re.search(r"\d+ (passed|failed|skipped)", ln)]
    return r.returncode, (lines[-1] if lines else r.stdout[-300:])


def empty_node_modules(present: bool):
    nm = WT / "apps/ui/node_modules"
    if present:
        assert not nm.exists(), "node_modules already exists in the worktree"
        nm.mkdir()
    elif nm.exists():
        shutil.rmtree(nm)


def controls(label):
    code, summary = run(R1046_TESTS)
    print(f"control {label} R-1046 tests: exit {code}: {summary}")
    empty_node_modules(True)
    try:
        vcode, vsummary = run(VITEST_NODE)
    finally:
        empty_node_modules(False)
    print(f"control {label} vitest node over an empty node_modules: exit {vcode}: {vsummary}")
    return code == 0 and vcode == 0 and "1 skipped" in vsummary


ok = controls("first")
for mid, what, rel, frm, to, tests in MUTATIONS:
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
        if mid == "m5":
            empty_node_modules(True)
        code, summary = run(tests)
    finally:
        if mid == "m5":
            empty_node_modules(False)
        path.write_bytes(original)
    restored = path.read_bytes() == original
    print(f"{mid}: exit {code}: {summary}; restored byte-identical: {restored}")
    ok = ok and code == 1 and "failed" in summary and restored
ok = controls("last") and ok
print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {ok}")
