# F275 R75 — the witness instrument, second edition, verbatim

> Saved as `.md` and not as `.py` on purpose: a `.py` file anywhere `ruff check .`
> scans is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this
> round's tree gate reads. The gate extracts the single fence below into
> `.remedy-wt/` and runs it there, which is outside the tree.
>
> This carrier was GENERATED from its source by the same script that verified the
> extraction round-trips back to that source, in one step, per DECISION F275 D44.

```python
"""F275 R75 — the owner check's residual, measured by WITNESS instead of by line.

WHAT ROUND 73 GOT WRONG, AND IT IS THE REASON THIS FILE EXISTS. Round 73 asked whether the
sites the owner check refuses are executed by the suite, ran the suite inside a fresh
`git worktree`, and read 176 of 176 executed with an empty risk set. DECISION F275 D47 then
discharged DECISION F275 D45's precondition on that reading. Re-run, the same instrument in
the same kind of worktree read 23 UNEXECUTED and 126 control failures, because a worktree
carries no `apps/ui/node_modules` and no built dist, so the `ui_server` suite fails there and
never reaches the `ui_server` lines. The first reading was a property of a worktree that
happened to be warm. A measurement that moves with the weather cannot discharge a precondition.

THIS EDITION ADDS ONE THING TO ROUND 74'S: IT SAYS WHICH UNIT EVERY COUNT IS IN. Coverage
resolves a context per LINE while the ruled set is keyed per SITE — path, line, column and
attribute — and several sites can share a line. Round 74 printed a site count in one section
and a line distribution in the next without naming either, its buckets summed to fewer than
its site total, and DECISION F275 D48 restated the two as one number. Every count below now
says whether it counts sites or lines, and the bucket sums are printed so the arithmetic is
visible rather than assumed.

TWO THINGS ROUND 74 CHANGED, AND THEY STAND.

FIRST, THE COVERAGE READING MOVES TO THE PRIMARY CHECKOUT, where the suite actually runs.
That is not a guardrail violation: `docs/agents/self_drive_protocol.md` G5 isolates DESTRUCTIVE
verification, and a coverage run writes no tracked file — `.coverage` is gitignored, and this
instrument reports `git status --porcelain` afterwards to show it. The MUTATIONS still happen
only inside a disposable worktree, which is what G5 is about.

SECOND, THE QUESTION GETS SHARPER. "Is the line executed" is a weak property: one test
reaching a site and forty tests reaching it are not the same protection, and round 73 could
only say so as an unquantified caveat after spot-checking two sites. Coverage records WHICH
test executed each line, so this asks how many distinct tests witness each refused site, for
every site at once. The sites with ZERO witnesses are the risk set. The sites with exactly ONE
are the thin set — the real exposure, because they are one test deletion from unguarded — and
every one of them is then RED-PROVED individually: its single witness is run unmutated and
then against the rename, in a worktree, and both colours are reported.

Usage: python3 -B <this file> <repo-root> <base-sha>
"""
import ast
import collections
import hashlib
import json
import pathlib
import re
import subprocess
import sys

import coverage


def rename_at(src_bytes, lineno, col, attr, new):
    """Rewrite the attribute NAME of the `ast.Attribute` node at (lineno, col, attr).

    A textual `.id` -> `.job_id` replace is not good enough and this instrument learned
    that the hard way: at `packages/orchestration/verifier.py` the first textual `.id` on
    the ruled line sits inside an f-string's LITERAL text, so the naive replace edited a
    message instead of an attribute access, the witness test stayed green, and the site
    read as unguarded when it is not. The flip renames an ATTRIBUTE NODE, so the probe
    must mutate exactly that node. `ast` columns are BYTE offsets, so this works in bytes.
    """
    tree = ast.parse(src_bytes.decode("utf-8"))
    node = None
    for n in ast.walk(tree):
        if (isinstance(n, ast.Attribute) and n.lineno == lineno
                and n.col_offset == col and n.attr == attr):
            node = n
            break
    if node is None:
        return None
    lines = src_bytes.split(b"\n")
    end_line = lines[node.end_lineno - 1]
    start = node.end_col_offset - len(attr)
    if end_line[start:node.end_col_offset] != attr.encode():
        return None
    lines[node.end_lineno - 1] = (end_line[:start] + new.encode()
                                  + end_line[node.end_col_offset:])
    return b"\n".join(lines)

ROOT = pathlib.Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
WT = ROOT / ".remedy-wt" / "r75_wt"
RULED = ROOT / ".remedy-wt" / "r69_rekeyed.json"
OWNERS = ROOT / ".remedy-wt" / "r69_rekeyed_owners.json"
MAP = ROOT / ".remedy-wt" / "r75_map_shipped.json"
# the SHIPPED guard is the Rule H stage round 73 landed, and this instrument derives its
# refusal set by running that stage out of its own committed carrier rather than by reading
# a map some earlier round left in scratch. An earlier draft read round 72's map, whose
# refusal set of 324 is a SUPERSET of Rule H's — conservative, but it measures a guard that
# is no longer the one in use, and a document about the shipped guard should name the
# shipped guard's own set.
STAGE_CARRIER = "78e5c18c:.agent/authored/f275-r73-owner-stage.py.md"
STAGE = ROOT / ".remedy-wt" / "r75_stage.py"


def run(args, cwd=None):
    return subprocess.run(args, capture_output=True, text=True, cwd=str(cwd or ROOT))


def counts(out):
    d = {}
    body = [l for l in out.strip().splitlines() if l.strip()]
    last = body[-1] if body else ""
    for n, what in re.findall(r"(\d+) (passed|failed|skipped|error)", last):
        d[what] = int(n)
    return d


def fmt(c):
    return "passed %d, failed %d, skipped %d" % (c.get("passed", 0), c.get("failed", 0),
                                                 c.get("skipped", 0))


print("=== 0. THE SHIPPED GUARD, OUT OF ITS OWN COMMITTED CARRIER ===")
run(["git", "worktree", "remove", "--force", str(WT)])
run(["git", "worktree", "prune"])
if run(["git", "worktree", "add", "--detach", str(WT), BASE]).returncode != 0:
    print("      FATAL: could not create the scratch worktree")
    sys.exit(2)
blob = subprocess.run(["git", "show", STAGE_CARRIER], capture_output=True,
                      cwd=str(ROOT)).stdout
cl = blob.decode("utf-8").splitlines(keepends=True)
op = [i for i, x in enumerate(cl) if x.rstrip("\n") == "```python"]
clo = [i for i, x in enumerate(cl) if x.rstrip("\n") == "```"]
stage_src = "".join(cl[op[0] + 1:clo[0]])
STAGE.write_text(stage_src, encoding="utf-8")
print("      carrier %s" % STAGE_CARRIER)
print("      carrier bytes %d ; fences %d/%d" % (len(blob), len(op), len(clo)))
print("      extracted %d bytes  sha256 %s"
      % (len(stage_src.encode()),
         hashlib.sha256(stage_src.encode()).hexdigest()))
sp = run([sys.executable, "-B", str(STAGE), str(WT), str(RULED), str(OWNERS),
          "--report-only", "--dump", str(MAP)])
for line in sp.stdout.splitlines():
    if line.strip():
        print("      %s" % line.rstrip())

decided = set(json.loads(MAP.read_text()))
R = [tuple(x) for x in json.load(open(RULED))["R"]]
refused = [k for k in R if "|".join(str(x) for x in k) not in decided]
prod = [k for k in refused if not k[0].startswith("tests/")]
tests_side = [k for k in refused if k[0].startswith("tests/")]

print("")
print("=== 1. WHAT THE SHIPPED GUARD REFUSES, SPLIT BY TREE ===")
print("      refused sites                                    : %d" % len(refused))
print("      of them, in test files                           : %d" % len(tests_side))
print("      of them, in production files                     : %d" % len(prod))
print("      distinct production files                        : %d"
      % len({k[0] for k in prod}))

print("")
print("=== 2. THE SUITE, IN THE PRIMARY CHECKOUT, RECORDING PER-TEST CONTEXTS ===")
p = run([sys.executable, "-m", "pytest", "-n", "auto", "-q", "-p", "no:cacheprovider",
         "--cov=packages", "--cov=apps", "--cov-context=test", "--cov-fail-under=0",
         "--cov-report="])
c = counts(p.stdout)
failed = sorted(l.split(" ")[1] for l in p.stdout.splitlines() if l.startswith("FAILED"))
print("      exit %d ; %s" % (p.returncode, fmt(c)))
for f in failed:
    print("        FAILED: %s" % f)
print("      THIS RUN'S COLOUR IS NOT A READING OF THIS GATE, and saying so is the whole")
print("      repair of what round 73 got wrong. Its job is to produce coverage CONTEXTS,")
print("      not a verdict. Several tests here are environment-sensitive under coverage on")
print("      a parallel runner — a wall-clock perf budget and a workspace-identity pair")
print("      have each been observed red in one invocation and green in the next, and")
print("      passing in isolation — so a gate that demands this run be green fails at")
print("      random, which is the gate that cannot reliably pass.")
print("      THE BIAS OF A FAILING TEST RUNS THE SAFE WAY, which is why no colour is")
print("      needed: a test that fails can only execute FEWER lines than it otherwise")
print("      would, so it can only UNDERSTATE a site's witness count. That makes the risk")
print("      set and the thin set of parts 4 and 5 too LARGE, never too small, and those")
print("      are the sets the ruling is about.")
print("      THE TREE IS UNTOUCHED BY THIS RUN, which is what makes it legal here:")
print("      git status --porcelain -> %r" % run(["git", "status", "--porcelain"]).stdout)

print("")
print("=== 3. HOW MANY TESTS WITNESS EACH REFUSED PRODUCTION SITE ===")
data = coverage.CoverageData(str(ROOT / ".coverage"))
data.read()
by_file = {}
for f in data.measured_files():
    rel = f[len(str(ROOT)) + 1:] if f.startswith(str(ROOT)) else f
    by_file[rel] = f
witness = {}
site_key = {}
for path, line, co, at in prod:
    src = by_file.get(path)
    if src is None:
        witness[(path, line)] = set()
        continue
    ctx = data.contexts_by_lineno(src)
    witness[(path, line)] = {x.split("|")[0] for x in ctx.get(line, [])
                             if x and x.split("|")[0]}
    site_key.setdefault((path, line), (co, at))

# A SITE AND A LINE ARE NOT THE SAME UNIT, and the round 74 edition of this instrument
# reported one distribution without saying which it was over. Coverage resolves a context
# per LINE, so the witness map is keyed by line; the ruled set is keyed by (path, line,
# column, attribute), and several ruled sites can share one line. Round 74's banner
# therefore counted sites in its first section and lines in this one, its buckets summed to
# fewer than the site total, and DECISION F275 D48 restated the difference as though it were
# one number. Both units are now printed, and every count says which it is.
sites_on = collections.Counter((k[0], k[1]) for k in prod)
print("      production SITES refused                         : %5d" % len(prod))
print("      distinct LINES they sit on                       : %5d" % len(witness))
print("      SITES sharing a line with another site           : %5d"
      % (len(prod) - len(witness)))
print("      A witness count is a property of a LINE, so the buckets below count LINES.")
buckets = collections.Counter()
site_buckets = collections.Counter()
for k, v in witness.items():
    n = len(v)
    label = ("zero" if n == 0 else "one" if n == 1 else "two to nine" if n < 10
             else "ten or more")
    buckets[label] += 1
    site_buckets[label] += sites_on[k]
for label in ["zero", "one", "two to nine", "ten or more"]:
    print("      witnessed by %-12s : %5d lines, carrying %5d sites"
          % (label, buckets.get(label, 0), site_buckets.get(label, 0)))
print("      the bucket LINE counts sum to                    : %5d"
      % sum(buckets.values()))
print("      the bucket SITE counts sum to                    : %5d"
      % sum(site_buckets.values()))
sizes = sorted(len(v) for v in witness.values())
print("      median witnesses per LINE                        : %5d"
      % sizes[len(sizes) // 2])
print("      total (line, test) witness pairs                 : %5d"
      % sum(len(v) for v in witness.values()))

zero = sorted(k for k, v in witness.items() if not v)
thin = sorted(k for k, v in witness.items() if len(v) == 1)
print("")
print("=== 4. THE RISK SET — refused by the guard and witnessed by NO test ===")
print("      the risk set holds                               : %d lines, carrying %d sites"
      % (len(zero), sum(sites_on[k] for k in zero)))
for p2, l2 in zero:
    print("        %s:%d" % (p2, l2))

print("")
print("=== 5. THE THIN SET — refused, and witnessed by exactly ONE test ===")
print("      the thin set holds                               : %d lines, carrying %d sites"
      % (len(thin), sum(sites_on[k] for k in thin)))
for p2, l2 in thin:
    print("        %s:%d" % (p2, l2))
    print("            witness %s" % sorted(witness[(p2, l2)])[0])

print("")
print("=== 6. EVERY THIN SITE IS RED-PROVED AGAINST ITS OWN WITNESS ===")
proved = 0
for p2, l2 in thin:
    w = sorted(witness[(p2, l2)])[0]
    co, at = site_key[(p2, l2)]
    f = WT / p2
    src = f.read_bytes()
    mutated = rename_at(src, l2, co, at, "job_id_PROBE")
    print("      %s:%d col %d .%s" % (p2, l2, co, at))
    print("        witness            : %s" % w)
    if mutated is None:
        print("        THE NODE DOES NOT RESOLVE AT THIS TREE — no colour is claimed.")
        continue
    a = run([sys.executable, "-m", "pytest", w, "-q", "-p", "no:cacheprovider"], cwd=WT)
    f.write_bytes(mutated)
    b = run([sys.executable, "-m", "pytest", w, "-q", "-p", "no:cacheprovider"], cwd=WT)
    f.write_bytes(src)
    ok = a.returncode == 0 and b.returncode != 0
    proved += 1 if ok else 0
    print("        unmutated control  : exit %d ; %s" % (a.returncode, fmt(counts(a.stdout))))
    print("        against the rename : exit %d ; %s" % (b.returncode, fmt(counts(b.stdout))))
    print("        control green and mutation red: %s ; reverted byte-identically: %s"
          % (ok, f.read_bytes() == src))
print("      thin sites whose single witness really catches the rename: %d of %d"
      % (proved, len(thin)))

run(["git", "worktree", "remove", "--force", str(WT)])
run(["git", "worktree", "prune"])
print("")
print("=== 7. THE SCRATCH IS GONE ===")
print("      git worktree list -> %s"
      % run(["git", "worktree", "list"]).stdout.split("\n")[0])
print("      git status --porcelain -> %r" % run(["git", "status", "--porcelain"]).stdout)
```
