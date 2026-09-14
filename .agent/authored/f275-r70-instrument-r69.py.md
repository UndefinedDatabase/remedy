# F275 R70 — the round 69 measurement instrument, CORRECTED, verbatim

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
"""F275 R69 — finding `R-0879`, both halves, each with the control that makes it a reading.

`R-0879` asks for two things and this instrument runs both, each beside the case that must
fail. THE REPAIR: re-key the ruled site set off line numbers, so a set survives the commits
that move the code it names. THE REFUSAL: stop a run whose ruled set has gone stale, rather
than quietly editing less of the tree than the set says. A guard that only ever passes is
not evidence, so each half is run twice — once where it must hold and once where it must
break.

Five banners. Every worktree it makes is disposable, lives under the gitignored
`.remedy-wt/`, and is removed before the last banner reads `git worktree list` back
(docs/agents/self_drive_protocol.md G5). Nothing outside `.remedy-wt/` is ever written.

Usage: python3 -B <this file> <repo-root> <sweep-sha> <tip-sha>
"""
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(sys.argv[1]).resolve()
SWEEP, TIP = sys.argv[2], sys.argv[3]
S = REPO / ".remedy-wt"

# Built from a character code rather than written out, so this file contains no literal
# markdown fence and can therefore itself be carried inside one. Round 69 landed an
# instrument blob that was generated before two banners were added and never regenerated;
# a literal fence here is what would have made regenerating it impossible.
FENCE = chr(96) * 3
FENCE_OPEN = FENCE + "python\n"

REKEY = S / "f275-r69-rekey.py"
GUARDED = S / "f275-r69-transform-guarded.py"
R53, O55 = S / "r53_R.json", S / "r55_owners.json"
STATUS = S / "r61_status.json"
R61 = S / "r61_ruled.json"

# the scope whose rename must trip the re-key refusal; unique in its file, which is what
# makes the mutation a named target rather than a description (item 25 of §3)
TARGET_FILE = "packages/orchestration/ui_server.py"
TARGET_DEF = "def _handle_command_submission("


def wt(name, sha):
    p = S / name
    if p.exists():
        subprocess.run(["git", "worktree", "remove", "--force", str(p)],
                       cwd=str(REPO), capture_output=True)
    subprocess.run(["git", "worktree", "add", "--detach", str(p), sha],
                   cwd=str(REPO), capture_output=True, check=True)
    return p


def drop(p):
    subprocess.run(["git", "worktree", "remove", "--force", str(p)],
                   cwd=str(REPO), capture_output=True)
    if p.exists():
        shutil.rmtree(p, ignore_errors=True)


def rekey(old, new, out):
    r = subprocess.run([sys.executable, "-B", str(REKEY), str(old), str(new),
                        str(R53), str(O55), str(out)],
                       cwd=str(REPO), capture_output=True, text=True)
    return r


def show(r, keep=("ruled sites in R", "recovered by", "CONTROL, recovered",
                  "UNRESOLVED", "owners carried", "THE PRECONDITION REFUSES")):
    for line in r.stdout.split("\n"):
        if any(k in line for k in keep):
            print(f"      {line.strip()}")


print("=== 0. WHAT IS ALREADY LANDED, AND WHAT IS NOT ===")
landed = REPO / ".agent/authored/f275-r59-rekey.py.md"
doc = landed.read_text()
inner = doc.split(FENCE_OPEN, 1)[1].rsplit(FENCE, 1)[0]
print(f"      the re-key stage was landed at round 59: {landed.exists()}")
print(f"      the stage run below is byte-identical to that landed blob: "
      f"{inner == REKEY.read_text()}")
tracked = subprocess.run(["git", "ls-files"], cwd=str(REPO),
                         capture_output=True, text=True).stdout.split()
print(f"      tracked files whose name holds 'flip_transform': "
      f"{[t for t in tracked if 'flip_transform' in t]}")
print()

print("=== 1. THE REPAIR, AT THE TREE THE TRANSFORM WOULD RUN ON ===")
old, new = wt("r69_i_old", SWEEP), wt("r69_i_new", TIP)
out1 = S / "r69_i_rekeyed.json"
r = rekey(old, new, out1)
show(r)
print(f"      exit {r.returncode}")
got = set(map(tuple, json.loads(out1.read_text())["R"]))
ref = set(map(tuple, json.loads(R61.read_text())["R"]))
print(f"      SET-EQUAL to the set the transform has consumed since round 61: {got == ref}")
print()

print("=== 2. THE REPAIR'S RED CONTROL — ONE SCOPE RENAMED, IN THE SAME WORKTREE ===")
p = new / TARGET_FILE
src = p.read_text(encoding="utf-8")
print(f"      occurrences of the target def in {TARGET_FILE}: {src.count(TARGET_DEF)}")
p.write_text(src.replace(TARGET_DEF, TARGET_DEF[:-1] + "_RENAMED("), encoding="utf-8")
out2 = S / "r69_i_mutated.json"
if out2.exists():
    out2.unlink()
r = rekey(old, new, out2)
show(r)
print(f"      exit {r.returncode}")
print(f"      an output set was written anyway: {out2.exists()}")
for line in r.stdout.split("\n"):
    if line.strip().startswith(("20 ", "packages/")) or "ui_server" in line:
        print(f"      {line.strip()}")
        break
drop(old)
drop(new)
print()

print("=== 3. THE REFUSAL, WHERE THE SET IS WHOLE ===")
a = wt("r69_i_a", TIP)
r = subprocess.run([sys.executable, "-B", str(GUARDED), str(a), str(out1),
                    str(S / "r69_i_rekeyed_owners.json"), str(STATUS)],
                   cwd=str(REPO), capture_output=True, text=True)
for line in r.stdout.split("\n"):
    if line.startswith(("PRECONDITION:", "files rewritten:", "total rewrites:")):
        print(f"      {line.strip()}")
print(f"      exit {r.returncode}")
dirty_a = [x for x in subprocess.run(["git", "status", "--porcelain"], cwd=str(a),
                                     capture_output=True, text=True).stdout.split("\n") if x]
print(f"      files the run modified in its worktree: {len(dirty_a)}")
drop(a)
print()

print("=== 4. THE REFUSAL'S RED CONTROL — THE STALE SET, WHICH ROUND 68 MEASURED ===")
b = wt("r69_i_b", TIP)
r = subprocess.run([sys.executable, "-B", str(GUARDED), str(b), str(R53), str(O55),
                    str(STATUS)], cwd=str(REPO), capture_output=True, text=True)
for line in r.stdout.split("\n"):
    if line.startswith(("PRECONDITION:", "THE TRANSFORM REFUSES", "files rewritten:")):
        print(f"      {line.strip()}")
    elif line.strip() and line.startswith("   ") and ".py" in line and "(" not in line:
        print(f"      {line.strip()}")
print(f"      exit {r.returncode}")
dirty_b = [x for x in subprocess.run(["git", "status", "--porcelain"], cwd=str(b),
                                     capture_output=True, text=True).stdout.split("\n") if x]
print(f"      files the run modified in its worktree: {len(dirty_b)}")
print(f"      the discriminator, PASS against REFUSE: {len(dirty_a)} modified against "
      f"{len(dirty_b)}")
drop(b)
print()

print("=== 5. THE TWO PARTS THIS ROUND LANDS REJOIN TO WHAT IT RAN ===")
join = ""
for n in (1, 2):
    d = (S / f"f275-r69-transform-guarded.part{n}.py.md").read_text()
    join += d.split(FENCE_OPEN, 1)[1].rsplit(FENCE, 1)[0]
print(f"      part 1 + part 2 == the transform run in banners 3 and 4: "
      f"{join == GUARDED.read_text()}")
print(f"      joined source lines: {join.count(chr(10))}")
print()

print("=== 6. THE SCRATCH IS GONE ===")
subprocess.run(["git", "worktree", "prune"], cwd=str(REPO), capture_output=True)
print(f"      git worktree list -> {subprocess.run(['git', 'worktree', 'list'], cwd=str(REPO), capture_output=True, text=True).stdout.strip()}")
print(f"      git status --porcelain -> {subprocess.run(['git', 'status', '--porcelain'], cwd=str(REPO), capture_output=True, text=True).stdout!r}")
```
