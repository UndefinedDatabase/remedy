# F275 R67 — the plain-run instrument, saved verbatim as an authored blob

Its extension is `.md` and that is load-bearing: a `.py` file anywhere `ruff check .` scans
is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this round gates on.

```python
"""F275 R67 — what the PLAIN run changes, measured against the rewritten one.

Five readings. (1) THE TWO PLAIN RUNS and their reproducibility as SETS. (2) THE SYNTHETIC
NAMES, which DECISION F275 D40 part four predicts go to zero, beside the rewritten run's 24
as the control. (3) THE RESOLUTION, plain against rewritten. (4) THE REBUILD, under the
same committed join as round 65, controlled the same way. (5) IS EVERY DROP JUSTIFIED — the
same classification round 65 ran, over the plain set.

Reads only; creates nothing and writes nothing.
"""
import collections
import json
import pathlib

SCR = pathlib.Path("/home/decodeux/Repos/remedy/.remedy-wt")
JOB_FIELD, TASK_FIELD = {"id", "name"}, {"id", "description"}
d = json.loads((SCR / "r53_R.json").read_text())
SITES = d["sites"]
R_53 = {tuple(r) for r in d["R"]}
BYK = {(s["path"], s["line"], s["col"], s["attr"]): s for s in SITES}
rw = json.loads((SCR / "r65_probe1.json").read_text())["rows"]
p1 = json.loads((SCR / "r67_probe1.json").read_text())
p2 = json.loads((SCR / "r67_probe2.json").read_text())
r53probe = json.loads((SCR / "kept_r53_probe_sites_run1.json").read_text())

print("=== 1. THE TWO PLAIN RUNS ===")
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

print("\n=== 2. THE SYNTHETIC NAMES ===")
rows = p1["rows"]
sy_rw = [r for r in rw if r["recv"] and r["recv"].startswith("@py_")]
sy_pl = [r for r in rows if r["recv"] and r["recv"].startswith("@py_")]
print(f"  CONTROL, the rewritten run: {len(sy_rw)} rows on "
      f"{len({(r['path'], r['line']) for r in sy_rw})} lines")
print(f"  the PLAIN run             : {len(sy_pl)} rows")
print("  a run that had none to begin with would prove nothing, which is why both are here.")

print("\n=== 3. THE RESOLUTION, PLAIN AGAINST REWRITTEN ===")
for label, rs in (("rewritten", rw), ("plain    ", rows)):
    res = sum(1 for r in rs if r["recv"] is not None)
    print(f"  {label}: rows {len(rs)}  RESOLVED {res}  REFUSED {len(rs) - res}")
print("  the lines the rewritten run resolved to a synthetic name, as the plain run sees them:")
sy_lines = {(r["path"], r["line"]) for r in sy_rw}
now = collections.Counter()
for r in rows:
    if (r["path"], r["line"]) in sy_lines:
        now["resolved" if r["recv"] is not None else "REFUSED"] += 1
for k in sorted(now):
    print(f"    {k}: {now[k]}")


def owners_of(s):
    return [o for o, fs in (("Job", JOB_FIELD), ("Task", TASK_FIELD)) if s["attr"] in fs]


def build(line_set, recv_set=None, refused=None):
    def in_P(s):
        if recv_set is None:
            return any((s["path"], s["line"], o, s["attr"]) in line_set for o in owners_of(s))
        for o in owners_of(s):
            if (s["path"], s["line"], o, s["attr"], s.get("recv")) in recv_set:
                return True
            if (s["path"], s["line"], o, s["attr"]) in refused:
                return True
        return False

    def in_S(s):
        return ((s["static"] == "Job" and s["attr"] in JOB_FIELD)
                or (s["static"] == "Task" and s["attr"] in TASK_FIELD))

    return {(s["path"], s["line"], s["col"], s["attr"]) for s in SITES if in_P(s) or in_S(s)}


def sets_of(rs):
    return ({(r["path"], r["line"], r["owner"], r["field"]) for r in rs},
            {(r["path"], r["line"], r["owner"], r["field"], r["recv"])
             for r in rs if r["recv"] is not None},
            {(r["path"], r["line"], r["owner"], r["field"])
             for r in rs if r["recv"] is None})


print("\n=== 4. THE REBUILD, UNDER THE SAME CONTROL ===")
l53 = {(r["path"], r["line"], r["owner"], r["field"]) for r in r53probe["rows"]}
R_ctl = build(l53)
print(f"  CONTROL: round 53 probe under the LINE join -> {len(R_ctl)}   "
      f"SET-EQUAL to round 53's R: {R_ctl == R_53}")
lw, rvw, rfw = sets_of(rw)
lp, rvp, rfp = sets_of(rows)
R_line_rw, R_recv_rw = build(lw), build(lw, rvw, rfw)
R_line_pl, R_recv_pl = build(lp), build(lp, rvp, rfp)
print(f"  rewritten probe: LINE {len(R_line_rw)}  RECEIVER {len(R_recv_rw)}  "
      f"drops {len(R_line_rw - R_recv_rw)}")
print(f"  plain probe    : LINE {len(R_line_pl)}  RECEIVER {len(R_recv_pl)}  "
      f"drops {len(R_line_pl - R_recv_pl)}")
print(f"  the two LINE joins agree: {R_line_rw == R_line_pl}")
recovered = (R_line_pl & R_recv_pl) - R_recv_rw
print(f"  sites the PLAIN receiver join keeps that the REWRITTEN one dropped: "
      f"{len(recovered)}")
print(f"  sites the PLAIN receiver join drops that the REWRITTEN one kept: "
      f"{len(R_recv_rw - R_recv_pl)}")
for k in sorted(R_recv_rw - R_recv_pl):
    print(f"    {k[0]}:{k[1]} col {k[2]} .{k[3]}")

print("\n=== 5. IS EVERY DROP JUSTIFIED, OVER THE PLAIN SET? ===")
dropped = R_line_pl - R_recv_pl
byline = collections.defaultdict(list)
for k in R_53:
    byline[(k[0], k[1])].append(k)
owners_json = {}
for kk, owner in json.loads((SCR / "r55_owners.json").read_text()).items():
    p, ln, col, attr = kk.rsplit("|", 3)
    owners_json[(p, int(ln), int(col), attr)] = owner
members = set()
for ln, ks in byline.items():
    g = collections.defaultdict(set)
    for k in ks:
        g[(owners_json.get(k), k[3])].add(BYK[k]["recv"] or "(expr)")
    for (o, a), names in g.items():
        if len(names) > 1:
            members |= {k for k in ks if owners_json.get(k) == o and k[3] == a}
empty = {k for k in dropped if BYK[k].get("recv") == ""}
sy_now = {(r["path"], r["line"]) for r in sy_pl}
print(f"  dropped total                                   : {len(dropped)}")
print(f"  on one of the 39 at-risk lines D36 bounded      : {len(dropped & members)}")
print(f"  the sweep recorded NO receiver for it at all    : {len(empty)}")
print(f"  both of the above                               : {len(dropped & members & empty)}")
print(f"  on a line still carrying a SYNTHETIC receiver   : "
      f"{len({k for k in dropped if (k[0], k[1]) in sy_now})}")
rest = dropped - members - empty
print(f"  NEITHER, so justified by nothing stated so far  : {len(rest)}")
for k in sorted(rest):
    print(f"    {k[0]}:{k[1]} col {k[2]} .{k[3]}  sweep receiver {BYK[k]['recv']!r}")
```
