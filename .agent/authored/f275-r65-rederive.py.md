# F275 R65 — the re-derivation instrument, saved verbatim as an authored blob

Its extension is `.md` and that is load-bearing: a `.py` file anywhere `ruff check .` scans
is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this round gates on.

```python
"""F275 R65 — the re-derivation instrument. Re-derives every figure the artefact states.

Five readings under five banners. (1) THE TWO RUNS and their reproducibility as SETS, under
both the round 53 key and the round 65 key. (2) WHAT THE RESOLUTION DID — resolved against
refused, and the refusals characterised. (3) THE AMBIGUITY THE OLD KEY HID, enumerated.
(4) THE CONTROL: rebuilding the ruled set from ROUND 53's own probe output under the LINE
join must reproduce round 53's `R` exactly, which is what makes this rebuild a faithful
copy of the committed builder's join rather than a new one. (5) THE RE-DERIVATION: the same
rebuild under the round 65 probe, LINE join against RECEIVER join, a one-variable
difference on one run.

Reads only; creates nothing and writes nothing.
"""
import collections
import json
import pathlib

SCR = pathlib.Path("/home/decodeux/Repos/remedy/.remedy-wt")
JOB_FIELD = {"id", "name"}
TASK_FIELD = {"id", "description"}

d = json.loads((SCR / "r53_R.json").read_text())
SITES = d["sites"]
R_53 = {tuple(r) for r in d["R"]}
p1 = json.loads((SCR / "r65_probe1.json").read_text())
p2 = json.loads((SCR / "r65_probe2.json").read_text())
r53probe = json.loads((SCR / "kept_r53_probe_sites_run1.json").read_text())

print("=== 1. THE TWO RUNS ===")
for name, p in (("run 1", p1), ("run 2", p2)):
    print(f"  {name}: probe rows {len(p['rows'])}   pytest exitstatus {p['exitstatus']}")


def keys(p, wide):
    out = set()
    for r in p["rows"]:
        k = (r["owner"], r["field"], r["mode"], r["path"], r["line"], r["func"])
        out.add(k + (r["lasti"], r["recv"]) if wide else k)
    return out


for label, wide in (("the ROUND 53 key", False), ("the ROUND 65 key", True)):
    a, b = keys(p1, wide), keys(p2, wide)
    print(f"  as {label}: run1 {len(a)}  run2 {len(b)}  symmetric difference {len(a ^ b)}")

print("\n=== 2. WHAT THE RECEIVER RESOLUTION DID ===")
rows = p1["rows"]
res = sum(1 for r in rows if r["recv"] is not None)
print(f"  rows {len(rows)}   receiver RESOLVED {res}   REFUSED {len(rows) - res}")
for direct, n in sorted(collections.Counter(
        r["direct"] for r in rows if r["recv"] is None).items()):
    print(f"    refused with direct={direct}: {n}")
print("  the five receivers seen most often:")
for name, n in collections.Counter(
        r["recv"] for r in rows if r["recv"]).most_common(5):
    print(f"    {n:>5}  {name}")

print("\n=== 3. THE AMBIGUITY THE OLD KEY HID ===")
by_old = collections.defaultdict(set)
for r in rows:
    by_old[(r["owner"], r["field"], r["mode"], r["path"], r["line"], r["func"])].add(
        r["recv"])
multi = {k: v for k, v in by_old.items() if len({x for x in v if x}) > 1}
print(f"  distinct round 53 keys in run 1: {len(by_old)}")
print(f"  of them, covering MORE THAN ONE resolved receiver: {len(multi)}")
for k, v in sorted(multi.items()):
    print(f"    {k[3]}:{k[4]} {k[0]}.{k[1]} {k[2]} -> {sorted(x for x in v if x)}")


def owners_of(s):
    return [o for o, fs in (("Job", JOB_FIELD), ("Task", TASK_FIELD)) if s["attr"] in fs]


def build(line_set, recv_set=None, refused=None):
    """The committed builder's own join. `recv_set` is None for the LINE join.

    Where the probe REFUSED a receiver on a line, a site on that line keeps its old
    standing: a refusal is an absence of evidence and not evidence of absence, and turning
    one into a strike is finding `R-0879` arriving from the other side.
    """
    def in_P(s):
        if recv_set is None:
            return any((s["path"], s["line"], o, s["attr"]) in line_set
                       for o in owners_of(s))
        for o in owners_of(s):
            if (s["path"], s["line"], o, s["attr"], s.get("recv")) in recv_set:
                return True
            if (s["path"], s["line"], o, s["attr"]) in refused:
                return True
        return False

    def in_S(s):
        return ((s["static"] == "Job" and s["attr"] in JOB_FIELD)
                or (s["static"] == "Task" and s["attr"] in TASK_FIELD))

    return {(s["path"], s["line"], s["col"], s["attr"])
            for s in SITES if in_P(s) or in_S(s)}


print("\n=== 4. THE CONTROL ===")
l53 = {(r["path"], r["line"], r["owner"], r["field"]) for r in r53probe["rows"]}
R_ctl = build(l53)
print(f"  round 53 probe rows {len(r53probe['rows'])}   its line keys {len(l53)}")
print(f"  rebuilt under the LINE join: {len(R_ctl)}   round 53's own R: {len(R_53)}")
print(f"  SET-EQUAL to round 53's R: {R_ctl == R_53}")
print("  a rebuild that did not reproduce the committed set would make every number")
print("  in banner 5 a number about a different join.")

print("\n=== 5. THE RE-DERIVATION ===")
l65 = {(r["path"], r["line"], r["owner"], r["field"]) for r in rows}
recv = {(r["path"], r["line"], r["owner"], r["field"], r["recv"])
        for r in rows if r["recv"] is not None}
refused = {(r["path"], r["line"], r["owner"], r["field"])
           for r in rows if r["recv"] is None}
R_line, R_recv = build(l65), build(l65, recv, refused)
print(f"  round 65 probe, LINE join     : {len(R_line)}")
print(f"  round 65 probe, RECEIVER join : {len(R_recv)}")
print(f"  line-join drift from round 53's set: {len(R_ctl ^ R_line)}  "
      "(the tree moved between the two commits; NOT the re-keying)")
print(f"  the RECEIVER join DROPS {len(R_line - R_recv)} and ADDS {len(R_recv - R_line)}")

byk = {(s["path"], s["line"], s["col"], s["attr"]): s for s in SITES}
dropped = R_line - R_recv
print("  the dropped sites by file, most first:")
# `dropped` is a set, so `Counter.most_common` breaks ties in an order that varies per
# process. Sorting on (-count, path) makes the listing the same listing twice.
_by_file = collections.Counter(k[0] for k in dropped)
for path, n in sorted(_by_file.items(), key=lambda kv: (-kv[1], kv[0]))[:8]:
    print(f"    {n:>4}  {path}")
print(f"  of the dropped, receiver recorded as the empty string: "
      f"{sum(1 for k in dropped if byk[k].get('recv') == '')}")
print(f"  of the dropped, under packages/: "
      f"{sum(1 for k in dropped if k[0].startswith('packages/'))}")

print("\n=== 5b. AGAINST THE 39 AT-RISK LINES OF DECISION F275 D36 ===")
owners_json = {}
for kk, owner in json.loads((SCR / "r55_owners.json").read_text()).items():
    p, ln, col, attr = kk.rsplit("|", 3)
    owners_json[(p, int(ln), int(col), attr)] = owner
byline = collections.defaultdict(list)
for k in R_53:
    byline[(k[0], k[1])].append(k)
at_risk = []
for ln, ks in byline.items():
    groups = collections.defaultdict(set)
    for k in ks:
        groups[(owners_json.get(k), k[3])].add(byk[k]["recv"] or "(expr)")
    for (owner, attr), names in groups.items():
        if len(names) > 1:
            at_risk.append((ln, [k for k in ks
                                 if owners_json.get(k) == owner and k[3] == attr]))
at_risk.sort()
members = {k for _l, ms in at_risk for k in ms}
reached = {(p, l) for p, l, _o, _f in l65}
print(f"  at-risk lines {len(at_risk)}   ruled sites on them {len(members)}")
print(f"  of those sites, DROPPED by the receiver join: {len(members & dropped)}")
print(f"  of those sites, still in the receiver-join set: {len(members & R_recv)}")
print(f"  of those sites, no longer in EITHER round 65 set: "
      f"{len(members - R_line - R_recv)}")
print(f"  at-risk lines the suite REACHED: "
      f"{sum(1 for ln, _m in at_risk if ln in reached)}   never reached: "
      f"{sum(1 for ln, _m in at_risk if ln not in reached)}")

print("\n=== 6. IS EVERY DROP JUSTIFIED? ===")
empty = {k for k in dropped if byk[k].get("recv") == ""}
print(f"  dropped total                                   : {len(dropped)}")
print(f"  on one of the 39 at-risk lines D36 bounded      : {len(dropped & members)}")
print(f"  the sweep recorded NO receiver for it at all    : {len(empty)}")
print(f"  both of the above                               : {len(dropped & members & empty)}")
print(f"  NEITHER, so justified by nothing stated so far  : "
      f"{len(dropped - members - empty)}")
print("  every site of that last class, which is what a per-site ruling still owes:")
for k in sorted(dropped - members - empty):
    print(f"    {k[0]}:{k[1]} col {k[2]} .{k[3]}  sweep receiver "
          f"{byk[k]['recv']!r}")
```
