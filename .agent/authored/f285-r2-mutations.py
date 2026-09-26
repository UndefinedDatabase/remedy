"""F285 R2 red proofs: python3 -B mutations.py <worktree>. Mutates, runs pytest, restores, reports.

Every mutation's FROM must occur exactly once in its file; the file is restored byte-identical
after each run. Each breaks one part of R-1055's repair and runs the relaunch, session-resume and
prompt-trace tests. Unmutated controls run first and last.
"""
import re
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_relaunch_session_resume.py", "tests/orchestration/test_session_resume.py",
         "tests/orchestration/test_prompt_trace.py"]
LOOP = "packages/orchestration/pingpong_loop.py"

MUTATIONS = [
    ("m1", "run_job offers the relaunch no session", "packages/orchestration/pingpong_job.py",
     "                resume_sessions = parked_session_refs(load_run(task.run_id))\n",
     "                resume_sessions = {}\n"),
    ("m2", "the builder's first call ignores the offer", LOOP,
     '                builder_call_resume = resume_sessions["builder"]\n',
     "                builder_call_resume = builder_resume_ref\n"),
    ("m3", "the reviewer's first call ignores the offer", LOOP,
     '                reviewer_call_resume = resume_sessions["reviewer"]\n',
     "                reviewer_call_resume = reviewer_resume_ref\n"),
    ("m4", "the run record drops the session", LOOP,
     '        "session_id": str(actuals.get("session_id") or ""),\n',
     '        "session_id": "",\n'),
    ("m5", "the fallback fires on the prompt gate again", LOOP,
     "            if builder_call_resume and builder_out.error:\n",
     "            if builder_resume_ref and builder_out.error:\n"),
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
