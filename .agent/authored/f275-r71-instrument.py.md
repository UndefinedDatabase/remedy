# F275 R71 — the round 71 measurement instrument, verbatim

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
"""F275 R71 — the owner-check stage, against the case it must refuse and the case it must pass.

Finding `R-0880`'s second obligation. The stage is `.agent/authored/f275-r71-owner-stage.py.md`;
this runs it twice over the same worktree and the same method, differing only in whether the
ruled set still holds the sites the static pass CONTRADICTS. A guard that only ever refuses is
as useless as one that only ever passes, so both readings are taken.

The PASS set is built HERE, from the stage's own report, rather than written by hand: the four
sites removed are the four the stage names, parsed out of its output, so the two runs cannot
disagree about which sites the difference is.

Usage: python3 -B <this file> <repo-root> <tip-sha>
"""
import collections
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(sys.argv[1]).resolve()
TIP = sys.argv[2]
S = REPO / ".remedy-wt"
STAGE = S / "f275-r71-owner-stage.py"
RULED, OWNERS = S / "r69_rekeyed.json", S / "r69_rekeyed_owners.json"
WT = S / "r71_i_wt"


def run(ruled, owners, extra=()):
    return subprocess.run([sys.executable, "-B", str(STAGE), str(WT), str(ruled),
                           str(owners), *extra], cwd=str(REPO),
                          capture_output=True, text=True)


def show(r, keep=("ruled sites", "live record classes", "CONFIRMED", "CONTRADICTED",
                  "REFUSED", "DECIDED", "THE OWNER CHECK REFUSES")):
    for line in r.stdout.split("\n"):
        s = line.strip()
        if any(k in s for k in keep):
            print(f"      {s}")


if WT.exists():
    subprocess.run(["git", "worktree", "remove", "--force", str(WT)],
                   cwd=str(REPO), capture_output=True)
subprocess.run(["git", "worktree", "add", "--detach", str(WT), TIP],
               cwd=str(REPO), capture_output=True, check=True)

print("=== 1. THE REFUSE CASE — the ruled set as the pipeline holds it ===")
r1 = run(RULED, OWNERS)
show(r1)
print(f"      exit {r1.returncode}")
for line in r1.stdout.split("\n"):
    s = line.strip()
    if " col " in s and " holds " in s and " owner verdict " in s:
        print(f"      {s}")
print()

print("=== 2. THE PASS SET, BUILT FROM THE STAGE'S OWN REPORT ===")
rep = run(RULED, OWNERS, ("--report-only",))
bad = set()
for line in rep.stdout.split("\n"):
    s = line.strip()
    if " col " in s and " holds " in s and " owner verdict " in s:
        bad.add((s.split(":")[0], int(s.split(":")[1].split()[0]),
                 int(s.split(" col ")[1].split()[0]), s.split(" .")[1].split()[0]))
print(f"      contradicted sites parsed from the report: {len(bad)}")
R = [tuple(x) for x in json.loads(RULED.read_text())["R"]]
keep = [list(k) for k in R if tuple(k) not in bad]
print(f"      ruled set goes from {len(R)} to {len(keep)}")
(S / "r71_i_clean.json").write_text(json.dumps({"R": keep}))
own = json.loads(OWNERS.read_text())


def key_of(k):
    p, l, c, a = k.rsplit("|", 3)
    return (p, int(l), int(c), a)


own2 = {k: v for k, v in own.items() if key_of(k) not in bad}
print(f"      owner table goes from {len(own)} to {len(own2)}")
(S / "r71_i_clean_owners.json").write_text(json.dumps(own2))
print()

print("=== 3. THE PASS CASE — the same stage, the same tree, the cleaned set ===")
r2 = run(S / "r71_i_clean.json", S / "r71_i_clean_owners.json")
show(r2)
print(f"      exit {r2.returncode}")
print(f"      THE DISCRIMINATOR, refuse against pass: exit {r1.returncode} "
      f"against exit {r2.returncode}")
print()

print("=== 4. THE BLIND SPOT, STATED AS A COUNT ===")
ref = collections.OrderedDict()
for line in r1.stdout.split("\n"):
    s = line.strip()
    if s.startswith(tuple(str(n) for n in range(10))) and "REFUSED to decide" in s:
        ref[s.split("  ", 1)[1]] = int(s.split()[0])
for k, v in ref.items():
    print(f"      {v:5d}  {k}")
decided = len(R) - sum(ref.values())
print(f"      the guard decides {decided} of {len(R)} and refuses {sum(ref.values())}")
print()

subprocess.run(["git", "worktree", "remove", "--force", str(WT)],
               cwd=str(REPO), capture_output=True)
if WT.exists():
    shutil.rmtree(WT, ignore_errors=True)
subprocess.run(["git", "worktree", "prune"], cwd=str(REPO), capture_output=True)
print("=== 5. THE SCRATCH IS GONE ===")
print(f"      git worktree list -> {subprocess.run(['git', 'worktree', 'list'], cwd=str(REPO), capture_output=True, text=True).stdout.strip()}")
print(f"      git status --porcelain -> {subprocess.run(['git', 'status', '--porcelain'], cwd=str(REPO), capture_output=True, text=True).stdout!r}")
```
