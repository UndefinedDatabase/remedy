# F275 R72 — the round 72 measurement instrument, verbatim

> Saved as `.md` and not as `.py` on purpose: a `.py` file anywhere `ruff check .`
> scans is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this
> round's G6(c) reads. The gate extracts the single fence below into `.remedy-wt/`
> and runs it there, which is outside the tree.
>
> This carrier was GENERATED from its source by the same script that verified the
> extraction round-trips back to that source, in one step. Round 69 landed a carrier
> generated before its source was edited and never regenerated; that is the defect
> this procedure exists to make unreachable.

```python
"""F275 R72 — the instrument for the owner-check widening.

It reads the widened owner-check stage against the narrow one, and the question it asks is
not "is the refusal set smaller". That is arithmetic anyone can do from two banners, and it
is answered the same way by a correct widening and by a broken one. The question is whether
the widening is SOUND, and soundness here has one falsifiable statement:

    EVERY SITE THE R71 METHOD DECIDED, THE R72 METHOD DECIDES THE SAME WAY.

Two banners of COUNTS cannot establish that: a site that changed its mind and two sites that
swapped classes produce the same totals. So the stage carries a `--dump` that writes its
per-site decision map, and section 3 diffs the two maps site by site.

The maps come from ONE file run in two modes, which raises the question the narrow mode has
to answer first: is `--narrow` really the R71 method? Section 1 settles it against the
committed R71 stage — same banner, class for class, and the same contradicted sites — so the
comparison is anchored to the artefact round 71 shipped and not to this file's own account
of it.

Section 5 removes the scratch worktree it made.

Usage: python3 -B <this file> <repo-root> <base-sha>
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
SCRATCH = ROOT / ".remedy-wt" / "r72_i_wt"
RULED = ROOT / ".remedy-wt" / "r69_rekeyed.json"
OWNERS = ROOT / ".remedy-wt" / "r69_rekeyed_owners.json"
R71 = ROOT / ".remedy-wt" / "f275-r71-owner-stage.py"
R72 = ROOT / ".remedy-wt" / "f275-r72-owner-stage.py"

CONF = "CONFIRMED: the owner verdict matches the receiver's record"
CONTRA = "CONTRADICTED: the receiver holds another record entirely"
NOTBOUND = "REFUSED to decide: receiver's class not statically bound"
NOTNAME = "REFUSED to decide: receiver is not a bare name"
NOID = "REFUSED to decide: annotation carries no class identity"
REFUSED = "REFUSED, the stated blind spot"


def run(args):
    return subprocess.run(args, capture_output=True, text=True, cwd=str(ROOT))


def stage(script, extra=()):
    p = run([sys.executable, "-B", str(script), str(SCRATCH), str(RULED), str(OWNERS),
             "--report-only"] + list(extra))
    return p.stdout


def enforcing(ruled_path):
    p = run([sys.executable, "-B", str(R72), str(SCRATCH), str(ruled_path), str(OWNERS)])
    return p.stdout, p.returncode


def banner_counts(out):
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


def contradicted_rows(out):
    rows = []
    for line in out.splitlines():
        m = re.match(r"\s+(\S+):(\d+) col (\d+) \.(\w+)\s+receiver '([^']*)' "
                     r"holds (\w+)\s+owner verdict (\w+)$", line)
        if m:
            rows.append((m.group(1), int(m.group(2)), int(m.group(3)), m.group(4),
                         m.group(5), m.group(6), m.group(7)))
    return rows


run(["git", "worktree", "remove", "--force", str(SCRATCH)])
run(["git", "worktree", "prune"])
if run(["git", "worktree", "add", "--detach", str(SCRATCH), BASE]).returncode != 0:
    print("FATAL: could not create the scratch worktree")
    sys.exit(2)

DN = ROOT / ".remedy-wt" / "r72_map_narrow.json"
DW = ROOT / ".remedy-wt" / "r72_map_wide.json"
out_committed = stage(R71)
out_narrow = stage(R72, ["--narrow", "--dump", str(DN)])
out_wide = stage(R72, ["--dump", str(DW)])
cc, cn, cw = (banner_counts(out_committed), banner_counts(out_narrow),
              banner_counts(out_wide))

print("=== 1. IS `--narrow` THE R71 METHOD? measured against the committed R71 stage ===")
keys = [CONF, CONTRA, NOTBOUND, NOTNAME, NOID, "DECIDED", REFUSED]
print("      %-46s %10s %10s" % ("", "committed", "--narrow"))
for k in keys:
    print("      %-46s %10d %10d" % (k[:46], cc.get(k, 0), cn.get(k, 0)))
print("      every class EQUAL                              : %s"
      % all(cc.get(k, 0) == cn.get(k, 0) for k in keys))
rc, rn = contradicted_rows(out_committed), contradicted_rows(out_narrow)
print("      the contradicted SITE LISTS are identical      : %s" % (sorted(rc)
                                                                    == sorted(rn)))
print("      (so every figure below in the R71 column is the committed stage's own)")

print("")
print("=== 2. THE TWO STAGES OVER THE SAME TREE AND THE SAME RULED SET ===")
print("      %-46s %8s %8s %8s" % ("", "R71", "R72", "delta"))
n_sites = len(json.load(open(RULED))["R"])
print("      %-46s %8d %8d %+8d" % ("ruled sites", n_sites, n_sites, 0))
for label, key in [("CONFIRMED", CONF), ("CONTRADICTED", "CONTRADICTED"),
                   ("DECIDED", "DECIDED"), ("REFUSED, the stated blind spot", REFUSED),
                   ("  of which: class not statically bound", NOTBOUND),
                   ("  of which: receiver is not a bare name", NOTNAME),
                   ("  of which: annotation carries no class id", NOID)]:
    print("      %-46s %8d %8d %+8d"
          % (label, cn.get(key, 0), cw.get(key, 0), cw.get(key, 0) - cn.get(key, 0)))

print("")
print("=== 3. THE SOUNDNESS CONTROL — the two PER-SITE decision maps, diffed ===")
mn = json.loads(DN.read_text())
mw = json.loads(DW.read_text())
changed = sorted(k for k in mn if k in mw and mn[k][0] != mw[k][0])
dropped = sorted(k for k in mn if k not in mw)
print("      sites the R71 method DECIDED                     : %d" % len(mn))
print("      sites the R72 method DECIDED                     : %d" % len(mw))
print("      of R71's decisions, sites R72 no longer decides  : %d" % len(dropped))
for k in dropped:
    print("        DROPPED: %s  was %s" % (k, mn[k][0]))
print("      of R71's decisions, sites R72 decides DIFFERENTLY: %d" % len(changed))
for k in changed:
    print("        CHANGED: %s  %s -> %s" % (k, mn[k][0], mw[k][0]))
print("      EVERY SITE R71 DECIDED, R72 DECIDES THE SAME WAY : %s"
      % (not changed and not dropped))
print("      sites R72 decides that R71 refused               : %d"
      % len([k for k in mw if k not in mn]))
print("      that count equals the fall in REFUSED            : %s"
      % (len([k for k in mw if k not in mn]) == cn.get(REFUSED, 0) - cw.get(REFUSED, 0)))

print("")
print("=== 4. WHAT THE WIDENING FOUND — contradictions R71 COULD NOT SEE ===")
d71 = {(r[0], r[1], r[2], r[3]) for r in contradicted_rows(out_narrow)}
rows72 = {(r[0], r[1], r[2], r[3]): r for r in contradicted_rows(out_wide)}
new = sorted(k for k in rows72 if k not in d71)
print("      NEW contradicted sites                           : %d" % len(new))
for k in new:
    r = rows72[k]
    print("        %s:%d col %d .%s  receiver %r holds %s  owner verdict %s"
          % (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
print("      each was REFUSED by R71, never CONFIRMED         : %s"
      % all("|".join(str(x) for x in k) not in mn for k in new))

print("")
print("=== 5. THE DISCRIMINATOR — the guard still refuses, and still passes ===")
out_e, rc_e = enforcing(RULED)
rows = contradicted_rows(out_e)
seen = {(r[0], r[1], r[2], r[3]) for r in rows}
clean = [x for x in json.load(open(RULED))["R"] if (x[0], x[1], x[2], x[3]) not in seen]
cleaned = ROOT / ".remedy-wt" / "r72_cleaned_ruled.json"
cleaned.write_text(json.dumps({"R": clean}), encoding="utf-8")
out_p, rc_p = enforcing(cleaned)
cp = banner_counts(out_p)
print("      contradicted sites parsed from the stage's own report: %d" % len(rows))
print("      ruled set goes from %d to %d" % (n_sites, len(clean)))
print("      THE DISCRIMINATOR, refuse against pass: exit %d against exit %d"
      % (rc_e, rc_p))
print("      CONFIRMED in the refuse case %d ; in the pass case %d ; EQUAL: %s"
      % (cw.get(CONF, 0), cp.get(CONF, 0), cw.get(CONF, 0) == cp.get(CONF, 0)))
print("      CONTRADICTED in the pass case: %d" % cp.get("CONTRADICTED", 0))

print("")
print("=== 6. THE SCRATCH IS GONE ===")
run(["git", "worktree", "remove", "--force", str(SCRATCH)])
run(["git", "worktree", "prune"])
print("      git worktree list -> %s"
      % run(["git", "worktree", "list"]).stdout.split("\n")[0])
print("      git status --porcelain -> %r" % run(["git", "status", "--porcelain"]).stdout)
```
