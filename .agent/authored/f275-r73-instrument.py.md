# F275 R73 — instrument A, the receiver-expression widening, verbatim

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
"""F275 R73 — instrument A: the receiver-expression widening, read against the SHIPPED stage.

Round 72 widened the owner check from 999 refusals to 324 and gated that widening by a
per-site decision-map diff rather than by its own counts. This does the same for RULE H, and
its anchor is not a mode flag but the COMMITTED round 72 carrier: the instrument extracts
both stages from git and runs them side by side, so the comparison is against the artefact
round 72 shipped rather than against this round's account of it.

The reading this round turns on is NOT the size of the gain. It is that the gain is small:
RULE H reaches the receiver shapes round 72 refused outright — `job.tasks[0].id`,
`result.job.id`, `load_job(...).id` — and buys confirmations without finding a single new
contradiction. That is the evidence DECISION F275 D45's other route needs, and instrument B
supplies the rest.

Usage: python3 -B <this file> <repo-root> <base-sha>
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
SCRATCH = ROOT / ".remedy-wt" / "r73_i_wt"
RULED = ROOT / ".remedy-wt" / "r69_rekeyed.json"
OWNERS = ROOT / ".remedy-wt" / "r69_rekeyed_owners.json"

R72_CARRIER = "d60a0cd4:.agent/authored/f275-r72-owner-stage.py.md"
R72_PATH = ROOT / ".remedy-wt" / "r73_stage_r72.py"
R73_PATH = ROOT / ".remedy-wt" / "f275-r73-owner-stage.py"

CONF = "CONFIRMED: the owner verdict matches the receiver's record"
CONTRA = "CONTRADICTED: the receiver holds another record entirely"
NOTBOUND = "REFUSED to decide: receiver's class not statically bound"
NOTNAME = "REFUSED to decide: receiver is not a bare name"
NOEXPR = "REFUSED to decide: receiver expression does not resolve"
NOID = "REFUSED to decide: annotation carries no class identity"
REFUSED = "REFUSED, the stated blind spot"


def run(args):
    return subprocess.run(args, capture_output=True, text=True, cwd=str(ROOT))


def extract(rev_path, dest):
    blob = subprocess.run(["git", "show", rev_path], capture_output=True,
                          cwd=str(ROOT)).stdout
    ls = blob.decode("utf-8").splitlines(keepends=True)
    o = [i for i, l in enumerate(ls) if l.rstrip("\n") == "```python"]
    c = [i for i, l in enumerate(ls) if l.rstrip("\n") == "```"]
    src = "".join(ls[o[0] + 1:c[0]])
    pathlib.Path(dest).write_text(src, encoding="utf-8")
    return len(blob), len(o), len(c), hashlib.sha256(src.encode()).hexdigest()


def stage(script, dump, extra=()):
    p = run([sys.executable, "-B", str(script), str(SCRATCH), str(RULED), str(OWNERS),
             "--report-only", "--dump", str(dump)] + list(extra))
    return p.stdout


def counts(out):
    d = {}
    for line in out.splitlines():
        m = re.match(r"\s+(\d+)\s\s(.+)$", line)
        if m:
            d[m.group(2).strip()] = int(m.group(1))
        m2 = re.match(r"(DECIDED|REFUSED, the stated blind spot|CONTRADICTED)\s*:\s*(\d+)",
                      line)
        if m2:
            d[m2.group(1)] = int(m2.group(2))
    return d


def rows(out):
    return sorted(re.findall(r"\s+(\S+):(\d+) col (\d+) \.(\w+)\s+receiver", out))


run(["git", "worktree", "remove", "--force", str(SCRATCH)])
run(["git", "worktree", "prune"])
if run(["git", "worktree", "add", "--detach", str(SCRATCH), BASE]).returncode != 0:
    print("FATAL: could not create the scratch worktree")
    sys.exit(2)

print("=== 1. THE ANCHOR — both stages come out of git, not out of scratch ===")
n, o, c, dg = extract(R72_CARRIER, R72_PATH)
print("      the COMMITTED round 72 carrier : %d bytes, fences %d/%d" % (n, o, c))
print("      its extracted source           : sha256 %s" % dg)
print("      the round 73 stage under test  : sha256 %s"
      % hashlib.sha256(R73_PATH.read_bytes()).hexdigest())

D72 = ROOT / ".remedy-wt" / "r73_map72.json"
D73 = ROOT / ".remedy-wt" / "r73_map73.json"
DN = ROOT / ".remedy-wt" / "r73_mapnarrow.json"
out72 = stage(R72_PATH, D72)
out73 = stage(R73_PATH, D73)
outn = stage(R73_PATH, DN, ["--narrow"])
c72, c73, cn = counts(out72), counts(out73), counts(outn)

print("")
print("=== 2. `--narrow` STILL REPRODUCES THE ROUND 71 READER ===")
keys = [CONF, CONTRA, NOTBOUND, NOTNAME, NOID, "DECIDED", REFUSED]
R71 = {CONF: 1195, CONTRA: 4, NOTBOUND: 787, NOTNAME: 113, NOID: 99,
       "DECIDED": 1199, REFUSED: 999}
print("      %-46s %10s %10s" % ("", "round 71", "--narrow"))
for k in keys:
    print("      %-46s %10d %10d" % (k[:46], R71[k], cn.get(k, 0)))
print("      every class EQUAL to the round 71 figures      : %s"
      % all(R71[k] == cn.get(k, 0) for k in keys))

print("")
print("=== 3. THE SHIPPED STAGE AGAINST THIS ONE ===")
print("      %-46s %8s %8s %8s" % ("", "R72", "R73", "delta"))
n_sites = len(json.load(open(RULED))["R"])
print("      %-46s %8d %8d %+8d" % ("ruled sites", n_sites, n_sites, 0))
for label, key in [("CONFIRMED", CONF), ("CONTRADICTED", "CONTRADICTED"),
                   ("DECIDED", "DECIDED"), ("REFUSED, the stated blind spot", REFUSED),
                   ("  of which: class not statically bound", NOTBOUND),
                   ("  of which: receiver not a bare name / expr", None),
                   ("  of which: annotation carries no class id", NOID)]:
    if key is None:
        a, b = c72.get(NOTNAME, 0), c73.get(NOEXPR, 0)
    else:
        a, b = c72.get(key, 0), c73.get(key, 0)
    print("      %-46s %8d %8d %+8d" % (label, a, b, b - a))

print("")
print("=== 4. THE SOUNDNESS CONTROL — the two PER-SITE decision maps, diffed ===")
m72, m73 = json.loads(D72.read_text()), json.loads(D73.read_text())
dropped = sorted(k for k in m72 if k not in m73)
changed = sorted(k for k in m72 if k in m73 and m72[k][0] != m73[k][0])
print("      sites the shipped stage DECIDED                  : %d" % len(m72))
print("      sites this stage DECIDED                         : %d" % len(m73))
print("      of the shipped stage's decisions, now undecided  : %d" % len(dropped))
print("      of the shipped stage's decisions, now DIFFERENT  : %d" % len(changed))
for k in changed:
    print("        CHANGED: %s  %s -> %s" % (k, m72[k][0], m73[k][0]))
print("      EVERY SITE THE SHIPPED STAGE DECIDED IS UNCHANGED: %s"
      % (not dropped and not changed))
newly = [k for k in m73 if k not in m72]
print("      sites newly decided                              : %d" % len(newly))
import collections  # noqa: E402
print("      newly decided, by verdict                        : %s"
      % dict(collections.Counter(m73[k][0] for k in newly)))

print("")
print("=== 5. THE READING THAT MATTERS — the gain finds no new defect ===")
print("      CONTRADICTED, shipped stage                      : %d"
      % c72.get("CONTRADICTED", 0))
print("      CONTRADICTED, this stage                         : %d"
      % c73.get("CONTRADICTED", 0))
print("      the contradicted SITE LISTS are identical        : %s"
      % (rows(out72) == rows(out73)))
print("      so the widening buys confirmations and no defect : %s"
      % (rows(out72) == rows(out73) and len(newly) > 0))

print("")
print("=== 6. THE SCRATCH IS GONE ===")
run(["git", "worktree", "remove", "--force", str(SCRATCH)])
run(["git", "worktree", "prune"])
print("      git worktree list -> %s"
      % run(["git", "worktree", "list"]).stdout.split("\n")[0])
print("      git status --porcelain -> %r" % run(["git", "status", "--porcelain"]).stdout)
```
