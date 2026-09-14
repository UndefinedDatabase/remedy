# F275 R73 — instrument B, the residual as a risk, verbatim

> Saved as `.md` and not as `.py` on purpose: a `.py` file anywhere `ruff check .`
> scans is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this
> round's tree gate reads. The gate extracts the single fence below into
> `.remedy-wt/` and runs it there, which is outside the tree.
>
> This carrier was GENERATED from its source by the same script that verified the
> extraction round-trips back to that source, in one step. Round 69 landed a carrier
> generated before its source was edited and never regenerated; that is the defect
> this procedure exists to make unreachable.

```python
"""F275 R73 — instrument B: is the owner check's residual a RISK, or only a blind spot?

DECISION F275 D45 gave the flip round two routes: shrink the refusal set, or rule the residual
acceptable in a dated decision that states the count. Round 72 took the first and instrument A
shows the second round of shrinking buys 47 confirmations and no new defect. So the residual
has to be RULED, and a ruling needs a measurement of what it is accepting.

THE RESIDUAL IS NOT THE RISK. The flip round runs the full suite, and the transform renames
`.id` to `.job_id`; applied to a receiver that is not a job record, that read raises
AttributeError on any line the suite executes. So the sites that can hurt are the ones the
guard cannot decide AND the suite does not run. This instrument measures both halves.

  (1) COVERAGE. An instrumented run of the whole suite, read back against the exact lines of
      the production sites the shipped guard refuses.
  (2) THE PROBE. At two of those sites, in the same disposable worktree, the attribute is
      renamed to one nothing defines — which is what a wrong guess by the flip looks like —
      and the suite is run again. The reading is the set of failures NOT in the control, and
      the test ids that appear in it, because a count can be explained by the environment and
      an attributed name cannot.

A FRESH WORKTREE'S FIRST SUITE RUN IS NOT A USABLE BASELINE, and this instrument was wrong
about that before it was right. A worktree carries no `apps/ui/node_modules` and no built
dist, so the FIRST run fails a varying subset of the command-channel door tests and builds
what the later runs then find in place. Measured across two invocations the first run's
failure set was ten and then nine, with different members. So the first run here is a WARM-UP
whose failures are reported and NOT used, the second run is the control the mutations are
subtracted against, and every run is instrumented the same way. Both are printed, because the
instability is itself a fact the flip round needs: it will read this suite's failures.

Everything destructive happens inside a worktree this script creates and removes, per
docs/agents/self_drive_protocol.md G5 and §4 item 10.

Usage: python3 -B <this file> <repo-root> <base-sha>
"""
import collections
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
WT = ROOT / ".remedy-wt" / "r73_risk_wt"
RULED = ROOT / ".remedy-wt" / "r69_rekeyed.json"
MAP = ROOT / ".remedy-wt" / "r73_map72.json"     # written by instrument A
PROBES = [("packages/orchestration/ui_view_model.py", 292),
          ("packages/orchestration/autorun.py", 320)]


def run(args, cwd=None):
    return subprocess.run(args, capture_output=True, text=True, cwd=str(cwd or ROOT))


def suite(cwd, cov=False):
    args = [sys.executable, "-m", "pytest", "-n", "auto", "-q", "-p", "no:cacheprovider"]
    if cov:
        args += ["--cov=packages", "--cov=apps", "--cov-report="]
    p = run(args, cwd=cwd)
    body = [l for l in p.stdout.strip().splitlines() if l.strip()]
    last = body[-1] if body else "(no output)"
    failed = sorted(l.split(" ")[1] for l in p.stdout.splitlines()
                    if l.startswith("FAILED"))
    return p.returncode, last, failed


run(["git", "worktree", "remove", "--force", str(WT)])
run(["git", "worktree", "prune"])
if run(["git", "worktree", "add", "--detach", str(WT), BASE]).returncode != 0:
    print("FATAL: could not create the scratch worktree")
    sys.exit(2)

decided = set(json.loads(MAP.read_text()))
R = [tuple(x) for x in json.load(open(RULED))["R"]]
refused = [k for k in R if "|".join(str(x) for x in k) not in decided]
prod = [k for k in refused if not k[0].startswith("tests/")]
tests = [k for k in refused if k[0].startswith("tests/")]

print("=== 1. WHAT THE SHIPPED GUARD REFUSES, SPLIT BY TREE ===")
print("      refused sites                                    : %d" % len(refused))
print("      of them, in test files                           : %d" % len(tests))
print("      of them, in production files                     : %d" % len(prod))
print("      distinct production files                        : %d"
      % len({k[0] for k in prod}))
print("      A wrong rename inside a test file breaks the test that contains it, so the")
print("      suite catches those by construction. The production sites are what parts 4")
print("      and 5 measure.")

print("")
print("=== 2. THE WARM-UP, WHOSE FAILURES ARE REPORTED AND NOT USED ===")
rc0, last0, warm0 = suite(WT, cov=True)
print("      exit %d" % rc0)
print("      %s" % last0)
print("      warm-up failures: %d" % len(warm0))
for f in warm0:
    print("        %s" % f)

print("")
print("=== 3. THE CONTROL — the SECOND run, which the mutations are subtracted against ===")
rc, last, control = suite(WT, cov=True)
print("      exit %d" % rc)
print("      %s" % last)
print("      control failures: %d" % len(control))
for f in control:
    print("        %s" % f)
print("      warm-up failures the control no longer reproduces: %d"
      % len(set(warm0) - set(control)))
print("      control failures the warm-up did not have          : %d"
      % len(set(control) - set(warm0)))
print("      These are the worktree's own environment, not regressions. They are")
print("      subtracted, not explained away, and part 5 reports only failures absent")
print("      from THIS set.")

print("")
print("=== 4. ARE THE REFUSED PRODUCTION SITES EXECUTED BY THOSE RUNS? ===")
sys.path.insert(0, str(WT))
import coverage  # noqa: E402
data = coverage.CoverageData(str(WT / ".coverage"))
data.read()
root = str(WT)
executed = collections.defaultdict(set)
for path in data.measured_files():
    rel = path[len(root) + 1:] if path.startswith(root) else path
    ls = data.lines(path)
    if ls:
        executed[rel] |= set(ls)
    else:
        for a, b in (data.arcs(path) or []):
            for v in (a, b):
                if v and v > 0:
                    executed[rel].add(v)
hit = [k for k in prod if k[1] in executed.get(k[0], ())]
miss = [k for k in prod if k[1] not in executed.get(k[0], ())]
print("      files carrying coverage data                     : %d" % len(executed))
print("      refused production sites EXECUTED by the suite    : %d" % len(hit))
print("      refused production sites NOT executed             : %d" % len(miss))
for k in miss:
    print("        UNEXECUTED: %s:%d" % (k[0], k[1]))
print("      THE UNEXECUTED SET IS THE RISK SET, and it holds  : %d" % len(miss))

print("")
print("=== 5. THE PROBE — a wrong rename, at a refused site, against that control ===")
for path, line in PROBES:
    f = WT / path
    src = f.read_text(encoding="utf-8")
    ls = src.splitlines(keepends=True)
    before = ls[line - 1]
    ls[line - 1] = before.replace(".id", ".job_id_PROBE", 1)
    f.write_text("".join(ls), encoding="utf-8")
    rc2, last2, failed2 = suite(WT, cov=True)
    f.write_text(src, encoding="utf-8")
    new = sorted(set(failed2) - set(control))
    print("      %s:%d" % (path, line))
    print("        before : %s" % before.strip()[:96])
    print("        after  : %s" % ls[line - 1].strip()[:96])
    print("        exit %d ; %s" % (rc2, last2))
    print("        failures NOT in the control                   : %d" % len(new))
    for x in new[:8]:
        print("          %s" % x)
    print("        reverted byte-identically                     : %s"
          % (f.read_text(encoding="utf-8") == src))
    print("        THE READING: control exit %d against mutated exit %d, %d new failures"
          % (rc, rc2, len(new)))

run(["git", "worktree", "remove", "--force", str(WT)])
run(["git", "worktree", "prune"])
print("")
print("=== 6. THE SCRATCH IS GONE ===")
print("      git worktree list -> %s"
      % run(["git", "worktree", "list"]).stdout.split("\n")[0])
print("      git status --porcelain -> %r" % run(["git", "status", "--porcelain"]).stdout)
```
