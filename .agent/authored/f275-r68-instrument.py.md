# F275 R68 — the instrument, verbatim

> Saved as `.md` and not as `.py` on purpose: a `.py` file anywhere `ruff check .`
> scans is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this
> round's G6(c) reads. The gate extracts the single fence below into `.remedy-wt/`
> and runs it there, which is outside the tree.

```python
"""F275 R68 — does the transform's own consumption lose the 54 non-resolving ruled keys?

DECISION F275 D41 holds the flip's write shut on exactly one open question, and this
instrument answers it end to end. Six readings, each printed under its own banner, and the
fourth is a control-and-treatment pair rather than a single run, because a count taken
against one ruled set says nothing about what a DIFFERENT ruled set would have cost.

It writes nothing outside two disposable `git worktree`s under the gitignored `.remedy-wt/`,
both removed and pruned before it returns (docs/agents/self_drive_protocol.md G5).

Usage: python3 -B <this file> <repo-root> <sweep-sha> <tip-sha>
"""
import ast
import collections
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(sys.argv[1]).resolve()
SWEEP, TIP = sys.argv[2], sys.argv[3]
SCRATCH = REPO / ".remedy-wt"

R53_JSON = SCRATCH / "r53_R.json"
O55_JSON = SCRATCH / "r55_owners.json"
R61_JSON = SCRATCH / "r61_ruled.json"
O61_JSON = SCRATCH / "r61_ruled_owners.json"
STATUS_JSON = SCRATCH / "r61_status.json"
TRANSFORM = SCRATCH / "r61_flip_transform.py"

R53 = set(map(tuple, json.loads(R53_JSON.read_text())["R"]))
R61 = set(map(tuple, json.loads(R61_JSON.read_text())["R"]))
O55 = json.loads(O55_JSON.read_text())
O61 = json.loads(O61_JSON.read_text())

_pos = {}


def positions(sha, path):
    """Every ast.Attribute position of `path` at `sha`, read without touching the tree."""
    if (sha, path) not in _pos:
        out = subprocess.run(["git", "show", f"{sha}:{path}"], cwd=str(REPO),
                             capture_output=True, text=True)
        _pos[(sha, path)] = None if out.returncode else {
            (n.lineno, n.col_offset, n.attr)
            for n in ast.walk(ast.parse(out.stdout)) if isinstance(n, ast.Attribute)}
    return _pos[(sha, path)]


def nodes(sha, path):
    out = subprocess.run(["git", "show", f"{sha}:{path}"], cwd=str(REPO),
                         capture_output=True, text=True)
    return [n for n in ast.walk(ast.parse(out.stdout)) if isinstance(n, ast.Attribute)]


def unresolved(S, sha):
    return {k for k in S if (k[1], k[2], k[3]) not in (positions(sha, k[0]) or set())}


print("=== 1. THE ROUND 53 COMMITTED SET, AT THE COMMIT THAT LANDED IT ===")
bad_sweep, bad_tip = unresolved(R53, SWEEP), unresolved(R53, TIP)
print(f"  at the sweep commit {SWEEP}: resolve {len(R53) - len(bad_sweep)}"
      f"  do NOT resolve {len(bad_sweep)}")
print(f"  at the tip {TIP}         : resolve {len(R53) - len(bad_tip)}"
      f"  do NOT resolve {len(bad_tip)}")
for p, n in collections.Counter(k[0] for k in bad_tip).most_common():
    print(f"      {n:3d}  {p}")
moved = subprocess.run(["git", "log", "--oneline", "--format=%h %s", f"{SWEEP}..{TIP}",
                        "--"] + sorted({k[0] for k in bad_tip}),
                       cwd=str(REPO), capture_output=True, text=True).stdout.strip()
print("  commits that moved those files between the two:")
for line in moved.split("\n"):
    print(f"      {line}")
print()

print("=== 2. THE SHAPE OF THE 54 ===")
off, agree, disagree, ruled_at_node = collections.Counter(), 0, 0, 0
SITES = {(s["path"], s["line"], s["col"], s["attr"]): s
         for s in json.loads(R53_JSON.read_text())["sites"]}
for k in sorted(bad_tip):
    path, line, col, attr = k
    cands = sorted({n.lineno for n in nodes(TIP, path)
                    if n.col_offset == col and n.attr == attr},
                   key=lambda L: (abs(L - line), L))
    if not cands:
        off["no node at that column with that attr, any line"] += 1
        continue
    nl = cands[0]
    off[nl - line] += 1
    node = next(n for n in nodes(TIP, path)
                if n.lineno == nl and n.col_offset == col and n.attr == attr)
    actual = getattr(node.value, "id", None) or getattr(node.value, "attr", None)
    rec = SITES[k]["recv"] if k in SITES else None
    if rec == actual:
        agree += 1
    else:
        disagree += 1
    if (path, nl, col, attr) in R53:
        ruled_at_node += 1
for d, n in sorted(off.items(), key=lambda kv: str(kv[0])):
    lab = f"node line - recorded line = {d:+d}" if isinstance(d, int) else d
    print(f"  {n:3d}  {lab}")
print(f"  the sweep's recorded receiver agrees at the shifted node: {agree}"
      f"   disagrees: {disagree}")
print(f"  shifted node is ITSELF a round 53 ruled key             : {ruled_at_node}")
print(f"  every one of the 54 is in the static sweep's own `sites`: "
      f"{all(k in SITES for k in bad_tip)}")
print()

print("=== 3. THE SET THE TRANSFORM ACTUALLY CONSUMES ===")
print(f"  round 61 set at the tip: resolve {len(R61) - len(unresolved(R61, TIP))}"
      f"  do NOT resolve {len(unresolved(R61, TIP))}")
only53, only61 = R53 - R61, R61 - R53
print(f"  53-only keys {len(only53)}   61-only keys {len(only61)}"
      f"   shared {len(R53 & R61)}")
shifted = {(p, l - 1, c, a) for (p, l, c, a) in only53}
print(f"  every 53-only key's one-line-earlier node is in the 61 set: "
      f"{shifted == only61}")
shared_o = set(O55) & set(O61)
print(f"  owner verdicts disagreeing on the {len(shared_o)} shared owner keys: "
      f"{sum(1 for k in shared_o if O55[k] != O61[k])}")
print()

print("=== 4. THE BEHAVIOURAL PAIR, ONE VARIABLE ===")


def run(tag, wt, ruled, owners):
    if wt.exists():
        subprocess.run(["git", "worktree", "remove", "--force", str(wt)],
                       cwd=str(REPO), capture_output=True, text=True)
    subprocess.run(["git", "worktree", "add", "--detach", str(wt), TIP],
                   cwd=str(REPO), capture_output=True, text=True, check=True)
    out = subprocess.run([sys.executable, "-B", str(TRANSFORM), str(wt),
                          str(ruled), str(owners), str(STATUS_JSON)],
                         cwd=str(REPO), capture_output=True, text=True)
    got = {}
    for line in out.stdout.split("\n"):
        s = line.strip()
        if s.startswith("T2 job field"):
            got["T2"] = int(s.split()[-1])
        elif s.startswith("T3 task field"):
            got["T3"] = int(s.split()[-1])
        elif s.startswith("total rewrites:"):
            got["total"] = int(s.split()[-1])
        elif s.startswith("UNDECIDED"):
            got["undecided"] = int(s.split("sites:")[1].split("|")[0])
    print(f"  {tag:26s} T2 {got['T2']}  T3 {got['T3']}"
          f"  total {got['total']}  undecided {got['undecided']}"
          f"  exit {out.returncode}")
    return got


A = SCRATCH / "r68_wt_a"
B = SCRATCH / "r68_wt_b"
t = run("TREATMENT, round 61 set", A, R61_JSON, O61_JSON)
c = run("CONTROL,   round 53 set", B, R53_JSON, O55_JSON)
print(f"  difference                 T2 {t['T2'] - c['T2']:+d}"
      f"  T3 {t['T3'] - c['T3']:+d}"
      f"  total {t['total'] - c['total']:+d}"
      f"  undecided {t['undecided'] - c['undecided']:+d}")
print()

print("=== 5. WHERE THE 54 RENAMES LAND ===")
files = [p for p in subprocess.run(["git", "ls-files", "*.py"], cwd=str(A),
                                   capture_output=True, text=True).stdout.split() if p]
srcline = collections.defaultdict(set)
for p, l, cc, a in only61:
    srcline[p].add(l)
diffs, unexplained = collections.defaultdict(list), 0
for rel in files:
    la = (A / rel).read_text(encoding="utf-8").split("\n")
    lb = (B / rel).read_text(encoding="utf-8").split("\n")
    if la == lb:
        continue
    for i, (x, y) in enumerate(zip(la, lb), start=1):
        if x != y:
            diffs[rel].append((i, x.strip(), y.strip()))
            if not any(abs(i - s) <= 2 for s in srcline.get(rel, ())):
                unexplained += 1
for rel in sorted(diffs):
    print(f"  {len(diffs[rel]):3d} differing lines  {rel}"
          f"   ({len([k for k in only61 if k[0] == rel])} fixed keys)")
print(f"  files compared {len(files)}   files differing {len(diffs)}"
      f"   differing lines {sum(len(v) for v in diffs.values())}")
print(f"  differing lines NOT within 2 lines of a fixed key: {unexplained}")
for rel in sorted(diffs):
    for i, x, y in diffs[rel][:2]:
        print(f"      {rel}:{i}  treatment {x!r}")
        print(f"      {' ' * len(rel)}   {' ' * len(str(i))} control   {y!r}")
print()

print("=== 6. THE SITE DECISION F275 D40 PART THREE CITED BY NAME ===")
LRE = "packages/orchestration/long_run_executor.py"
for sha, lo, hi in ((SWEEP, 503, 506), (TIP, 502, 505)):
    text = subprocess.run(["git", "show", f"{sha}:{LRE}"], cwd=str(REPO),
                          capture_output=True, text=True).stdout.split("\n")
    print(f"  at {sha}:")
    for n in range(lo, hi + 1):
        print(f"      {n}: {text[n - 1]}")
    got = sorted((x.lineno, x.col_offset, x.attr,
                  getattr(x.value, 'id', None) or getattr(x.value, 'attr', None))
                 for x in nodes(sha, LRE) if lo <= x.lineno <= hi)
    for ln, co, at, rv in got:
        print(f"      node line {ln} col {co} .{at}  receiver {rv!r}")
    print(f"      round 53 keys there: "
          f"{sorted(k[1:] for k in R53 if k[0] == LRE and lo <= k[1] <= hi)}")
    print(f"      round 61 keys there: "
          f"{sorted(k[1:] for k in R61 if k[0] == LRE and lo <= k[1] <= hi)}")
print()

for wt in (A, B):
    subprocess.run(["git", "worktree", "remove", "--force", str(wt)],
                   cwd=str(REPO), capture_output=True, text=True)
    if wt.exists():
        shutil.rmtree(wt, ignore_errors=True)
subprocess.run(["git", "worktree", "prune"], cwd=str(REPO), capture_output=True, text=True)
wl = subprocess.run(["git", "worktree", "list"], cwd=str(REPO),
                    capture_output=True, text=True).stdout.strip()
print("=== 7. THE SCRATCH IS GONE ===")
print(f"  git worktree list -> {wl}")
print(f"  git status --porcelain -> "
      f"{subprocess.run(['git', 'status', '--porcelain'], cwd=str(REPO), capture_output=True, text=True).stdout!r}")
```
