# F275 R70 — the round 70 measurement instrument, verbatim

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
"""F275 R70 — the round 69 defect reproduced and repaired, and `R-0880`'s first obligation.

Two jobs, and the first is the round's own repair. Round 69 landed an artefact together with
an instrument blob that cannot reproduce five of the lines that artefact quotes, because the
blob was generated BEFORE two banners were added to its source and never regenerated. The
artefact was right and the blob was stale. Banners 1 and 2 below show both halves of that:
the LANDED round 69 blob failing the sweep, and the corrected blob passing it. A repair that
only showed the fix would not show that the defect was real.

The second job is finding `R-0880`'s FIRST obligation — bound the over-selection STATICALLY,
"because a dry run can only ever show the sites the suite executes". Banner 3 runs that probe
and reports its blind spot as loudly as its result.

Every worktree this makes is disposable, lives under the gitignored `.remedy-wt/`, and is
removed before the last banner reads `git worktree list` back.

Usage: python3 -B <this file> <repo-root> <sweep-sha> <tip-sha> <r69-instrument-sha>
"""
import pathlib
import subprocess
import sys

REPO = pathlib.Path(sys.argv[1]).resolve()
SWEEP, TIP, R69SHA = sys.argv[2], sys.argv[3], sys.argv[4]
S = REPO / ".remedy-wt"

FENCE = chr(96) * 3
FENCE_OPEN = FENCE + "python\n"

R69_ARTEFACT = ".agent/f275_t003_rekey_r69.md"
R69_INSTRUMENT = ".agent/authored/f275-r69-instrument.py.md"
CORRECTED = S / "f275-r70-instrument-r69.py.md"
BOUND = S / "f275-r70-bound.py"


def blob(sha, path):
    return subprocess.run(["git", "show", f"{sha}:{path}"], cwd=str(REPO),
                          capture_output=True, text=True).stdout


def fence_of(text):
    return text.split(FENCE_OPEN, 1)[1].rsplit(FENCE, 1)[0]


def run_instrument(src, tag):
    p = S / f"r70_extract_{tag}.py"
    p.write_text(src)
    r = subprocess.run([sys.executable, "-B", str(p), str(REPO), SWEEP, TIP],
                       cwd=str(REPO), capture_output=True, text=True)
    return r


def sweep(artefact, out):
    """Every indented non-blank artefact line, against the output, as a monotone matching."""
    o = [l.strip() for l in out.split("\n") if l.strip()]
    q = [l.strip() for l in artefact.split("\n") if l[:1] in (" ", "\t") and l.strip()]
    absent = [l for l in q if l not in o]
    pos, matched, unordered = -1, [], []
    for line in q:
        nxt = next((i for i in range(pos + 1, len(o)) if o[i] == line), None)
        if nxt is None:
            unordered.append(line)
        else:
            matched.append(nxt)
            pos = nxt
    return q, absent, matched, unordered


art = blob(TIP, R69_ARTEFACT)

print("=== 1. THE DEFECT, REPRODUCED AGAINST THE BLOB ROUND 69 LANDED ===")
stale = fence_of(blob(R69SHA, R69_INSTRUMENT))
print(f"      landed instrument fence: {len(stale.encode())} B, "
      f"{stale.count(chr(10))} lines")
r = run_instrument(stale, "stale")
print(f"      it runs: exit {r.returncode}, stderr {len(r.stderr)} B")
q, absent, matched, unordered = sweep(art, r.stdout)
print(f"      artefact lines quoted: {len(q)}")
print(f"      lines it CANNOT produce: {len(absent)}")
for line in absent:
    print(f"        {line}")
print(f"      unmatchable in order   : {len(unordered)}")
print()

print("=== 2. THE REPAIR, AGAINST THE CORRECTED BLOB ===")
fixed = fence_of(CORRECTED.read_text())
print(f"      corrected fence: {len(fixed.encode())} B, {fixed.count(chr(10))} lines")
r2 = run_instrument(fixed, "fixed")
print(f"      it runs: exit {r2.returncode}, stderr {len(r2.stderr)} B")
q2, absent2, matched2, unordered2 = sweep(art, r2.stdout)
print(f"      artefact lines quoted: {len(q2)}")
print(f"      lines it CANNOT produce: {len(absent2)}")
print(f"      unmatchable in order   : {len(unordered2)}")
print(f"      matched indices strictly increase: "
      f"{all(matched2[i] < matched2[i + 1] for i in range(len(matched2) - 1))}")
print(f"      THE DISCRIMINATOR, stale against corrected: "
      f"{len(absent)} absent against {len(absent2)}")
print()

print("=== 3. FINDING R-0880, FIRST OBLIGATION — THE STATIC BOUND ===")
r3 = subprocess.run([sys.executable, "-B", str(BOUND), str(REPO)],
                    cwd=str(REPO), capture_output=True, text=True)
for line in r3.stdout.split("\n"):
    if line.strip():
        print(f"      {line}")
print(f"      bound probe exit {r3.returncode}, stderr {len(r3.stderr)} B")
print()

print("=== 4. THE SCRATCH IS GONE ===")
subprocess.run(["git", "worktree", "prune"], cwd=str(REPO), capture_output=True)
wl = subprocess.run(["git", "worktree", "list"], cwd=str(REPO),
                    capture_output=True, text=True).stdout.strip()
st = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO),
                    capture_output=True, text=True).stdout
print(f"      git worktree list -> {wl}")
print(f"      git status --porcelain -> {st!r}")
```
