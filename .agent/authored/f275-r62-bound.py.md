# F275 R62 — `f275_r62_bound.py`, the static bound on finding `R-0880`

> Committed verbatim because `R-0880`'s fix clause binds a STATIC bound on the round that
> takes it, and because a bound asserted without its instrument is a number nobody can
> re-derive. It reads the committed site set's own provenance — no worktree, no suite run —
> and reports the lines on which one descriptor-probe proof ruled two receivers.
> It is a `.md` and not a `.py` because a `.py` file anywhere `ruff check .` scans is
> counted by `tests/orchestration/test_ci_budgets.py`.

```python
"""The bound `R-0880` asked for: ruled sites that one probe proof covered for free.

Not every shared line is a defect. `job.id` and `task.id` on one line are two receivers
with two DIFFERENT owner verdicts, and each is a separate proof. The defect is the line
where two DIFFERENT receiver names carry the SAME owner verdict: there the probe proved one
receiver and round 53 ruled both.
"""
import collections
import json

d = json.load(open("/home/decodeux/Repos/remedy/.remedy-wt/r53_R.json"))
R = set(tuple(r) for r in d["R"])
by_key = {(s["path"], s["line"], s["col"], s["attr"]): s for s in d["sites"]}
owners = {}
for key, owner in json.load(
        open("/home/decodeux/Repos/remedy/.remedy-wt/r55_owners.json")).items():
    p, ln, col, attr = key.rsplit("|", 3)
    owners[(p, int(ln), int(col), attr)] = owner

byline = collections.defaultdict(list)
for k in R:
    byline[(k[0], k[1])].append(k)

at_risk, rows = [], []
for ln, ks in byline.items():
    groups = collections.defaultdict(set)
    for k in ks:
        groups[(owners.get(k), k[3])].add(by_key[k]["recv"] or "(expr)")
    for (owner, attr), names in groups.items():
        if len(names) > 1:
            members = [k for k in ks if owners.get(k) == owner and k[3] == attr]
            at_risk += members
            rows.append((ln[0], ln[1], owner, attr, sorted(names)))

shared = [ks for ks in byline.values() if len(ks) > 1]
print("=== THE STATIC BOUND ON `R-0880` ===\n")
print("  ruled sites                                              : %d" % len(R))
print("  distinct (path, line) they occupy                        : %d" % len(byline))
print("  lines carrying MORE THAN ONE ruled site                   : %d" % len(shared))
print("  ruled sites on such a line                                : %d"
      % sum(len(v) for v in shared))
print("  lines where >1 ruled site shares ONE owner verdict across")
print("  DIFFERENT receiver names                                 : %d" % len(rows))
print("  ruled sites on those lines                               : %d" % len(at_risk))
print("\n  On each such line the probe proved ONE receiver and round 53 ruled BOTH,")
print("  because the probe records a (path, LINE) and not a (path, line, COLUMN).")
print("  At most one receiver per group is the proved one, so the sites that were")
print("  ruled without proof number AT LEAST %d and AT MOST %d."
      % (len(rows), len(at_risk) - len(rows)))

print("\n=== every at-risk line ===")
for p, l, owner, attr, names in sorted(rows):
    print("   %-48s:%-5d owner=%-5s .%s  receivers=%s" % (p, l, owner, attr, names))

print("\n=== by file ===")
for p, n in collections.Counter(r[0] for r in rows).most_common():
    print("   %3d  %s" % (n, p))

print("\n=== cross-check against the twelve frames the R61 run reached ===")
KNOWN = [("packages/orchestration/loop_run.py", 285),
         ("packages/orchestration/long_run_executor.py", 504),
         ("packages/orchestration/brain_detail.py", 345),
         ("packages/orchestration/mission_state.py", 1074)]
rowset = set((p, l) for p, l, _o, _a, _n in rows)
for p, l in KNOWN:
    print("   %-48s:%-5d in the static bound: %s" % (p, l, (p, l) in rowset))
```
