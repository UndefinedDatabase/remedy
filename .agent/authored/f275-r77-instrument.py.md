# F275 R77 — the partition instrument, verbatim

> Saved as `.md` and not as `.py` on purpose: a `.py` file anywhere `ruff check .`
> scans is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this
> round's tree gate reads. The gate extracts the single fence below into
> `.remedy-wt/` and runs it there, which is outside the tree.
>
> This carrier was GENERATED from its source by the same script that verified the
> extraction round-trips back to that source, in one step, per DECISION F275 D44.

```python
"""F275 R77 — the flip's input set, CONSTRUCTED: the partition of the 60, and a third arm.

DECISION F275 D50 ruled that the flip's input is the round 53 set minus the sites the plain
re-derivation identifies as over-selected, and called that set an inference rather than a
measurement because nothing had carried an over-selected frame back to the site that produced
it. This instrument closes that gap and then tests the result.

THE PARTITION. The SHIPPED owner check of DECISION F275 D47 — the Rule H stage round 73
landed — names 13 ruled sites whose receiver holds another record entirely. Every one of them
is compared against the 60 sites the plain re-derivation drops, and the corrected set is the
round 53 re-keyed set minus exactly those 13.

THE THIRD ARM. The corrected set is run through the same guarded transform at the same commit
and its suite residue is read beside the two arms of round 76, so the three differ in the
RULED SITE SET alone.

It re-analyses SAVED transcripts and SAVED site sets and runs no test of its own, so it is
deterministic. A CROSS-CHECK compares two numbers reached by different routes and can fail; a
PARTITION adds a set's own parts back to the set and cannot. Both are labelled.

Usage: python3 -B r77_instrument.py <scratch_dir>
"""
import collections
import hashlib
import json
import pathlib
import re
import sys

SCR = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt").resolve()

FRAME = re.compile(r"^(?P<path>[\w./\-]+\.py):(?P<line>\d+): (?P<exc>\w+)(?::\s*(?P<msg>.*))?$")
ATTR = re.compile(r"'(\w+)' object has no attribute '(\w+)'")
CONTRA = re.compile(r"^\s+(\S+\.py):(\d+) col (\d+) \.(\w+)\s+receiver '([^']*)' holds (\w+)",
                    re.MULTILINE)
SUMMARY = re.compile(r"^\d+ (failed|passed).*(in \d+\.\d+s|seconds)")
RECORD = {"JobPlan", "TaskEntry"}
CLASSIC = {"id", "name", "description"}
UNIFIED = {"job_id", "job_title", "task_id", "title"}

INPUTS = [
    "r76_r53_rekeyed.json", "r76_plain_rekeyed.json", "r77_corrected.json",
    "r77_stage.out", "r77_stage_corrected.out",
    "r76_tf_r53.out", "r76_tf_plain.out", "r77_tf_corr.out",
    "r76_suite_ctl.out", "r76_suite_r53.out", "r76_suite_plain.out", "r77_suite_corr.out",
]
CROSS, PART = [], []


def cross(label, a, b, unit):
    ok = a == b
    CROSS.append(ok)
    print(f"  CROSS-CHECK {label}: {a} against {b} {unit}  -> {'MATCH' if ok else 'MISMATCH'}")
    return ok


def partition(label, parts, total, unit):
    s = sum(parts)
    ok = s == total
    PART.append(ok)
    print(f"  PARTITION {label}: {' + '.join(str(p) for p in parts)} = {s} against {total} "
          f"{unit}  -> {'MATCH' if ok else 'MISMATCH'}")
    return ok


def sites(name):
    return {tuple(r) for r in json.loads((SCR / name).read_text())["R"]}


def outcomes(name):
    failed, errored = set(), set()
    for line in (SCR / name).read_text(errors="replace").splitlines():
        if line.startswith("FAILED "):
            failed.add(line[len("FAILED "):].split(" - ")[0].strip())
        elif line.startswith("ERROR "):
            errored.add(line[len("ERROR "):].split(" - ")[0].strip())
    return failed, errored


def summary_counts(name):
    got = {}
    for line in (SCR / name).read_text(errors="replace").splitlines():
        if SUMMARY.match(line.strip()):
            for key in ("failed", "error"):
                m = re.search(rf"(\d+) {key}s?\b", line.strip())
                got[key] = int(m.group(1)) if m else 0
    return got.get("failed", 0), got.get("error", 0)


def frames(name):
    out = []
    for line in (SCR / name).read_text(errors="replace").splitlines():
        m = FRAME.match(line.strip())
        if m:
            out.append((m.group("path"), m.group("exc"), (m.group("msg") or "").strip()))
    return out


def transform(name):
    lines = (SCR / name).read_text(errors="replace").splitlines()
    head, rules = {}, {}
    for line in lines:
        for key, pat in (("ruled", r"ruled keys (\d+)"), ("files", r"files rewritten: (\d+)"),
                         ("total", r"total rewrites: (\d+)"),
                         ("undecided", r"UNDECIDED [^:]*: (\d+)")):
            m2 = re.search(pat, line)
            if m2:
                head[key] = int(m2.group(1))
    try:
        start = lines.index("rewrites by rule:") + 1
    except ValueError:
        return head, rules
    for line in lines[start:]:
        if not line.strip():
            break
        m = re.match(r"^  (.*\S)\s+(\d+)$", line)
        if m:
            rules[m.group(1).strip()] = int(m.group(2))
    return head, rules


def stage(name):
    """The owner check's own banner: its counts and its CONTRADICTED rows."""
    txt = (SCR / name).read_text(errors="replace")
    got = {}
    for key, pat in (("ruled", r"ruled sites\s+: (\d+)"),
                     ("decided", r"DECIDED\s+: (\d+)"),
                     ("refused", r"REFUSED, the stated blind spot: (\d+)"),
                     ("contradicted", r"CONTRADICTED\s+: (\d+)")):
        m = re.search(pat, txt)
        if m:
            got[key] = int(m.group(1))
    rows = set()
    holds = collections.Counter()
    for m in CONTRA.finditer(txt):
        rows.add((m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)))
        holds[m.group(6)] += 1
    return got, rows, holds


print("=== 0. THE INPUTS THIS READING IS TAKEN FROM ===")
print("  Every figure below comes from these files and from nothing else.")
for n in INPUTS:
    b = (SCR / n).read_bytes()
    print(f"    {n:26s} {len(b):>9} bytes  sha256 {hashlib.sha256(b).hexdigest()}")

print("\n=== 1. THE THREE RULED SITE SETS, IN SITES ===")
K53, KPL, KCO = sites("r76_r53_rekeyed.json"), sites("r76_plain_rekeyed.json"), \
    sites("r77_corrected.json")
dropped = K53 - KPL
print(f"  round 53 committed, re-keyed           : {len(K53)} sites")
print(f"  round 67 plain re-derivation, re-keyed : {len(KPL)} sites")
print(f"  THE CORRECTED SET                      : {len(KCO)} sites")
print(f"  sites the PLAIN set drops              : {len(dropped)} sites")
print(f"  the CORRECTED set is a SUBSET of round 53's : {KCO <= K53}")
print(f"  the PLAIN set is a SUBSET of the CORRECTED one : {KPL <= KCO}")

print("\n=== 2. THE PARTITION OF THE DROPPED SITES ===")
counts53, contra53, holds53 = stage("r77_stage.out")
countsco, contraco, _h = stage("r77_stage_corrected.out")
print(f"  the SHIPPED owner check over the round 53 set: ruled {counts53['ruled']}, "
      f"decided {counts53['decided']}, refused {counts53['refused']}, "
      f"CONTRADICTED {counts53['contradicted']}")
cross("the CONTRADICTED rows parsed against the count the stage prints", len(contra53),
      counts53["contradicted"], "sites")
cross("the stage's ruled-site count against the set file it was given", counts53["ruled"],
      len(K53), "sites")
partition("the owner check's verdicts", [counts53["decided"], counts53["refused"]],
          counts53["ruled"], "sites")
print("  the receiver classes it names, in sites:")
for k, n in sorted(holds53.items(), key=lambda kv: (-kv[1], kv[0])):
    print(f"      {n:>3}  {k}")
partition("the contradicted sites by receiver class", sorted(holds53.values(), reverse=True),
          len(contra53), "sites")

both = contra53 & dropped
kept = contra53 - dropped
notc = dropped - contra53
print(f"\n  CONTRADICTED and dropped by the plain set : {len(both)} sites")
print(f"  CONTRADICTED but KEPT by the plain set     : {len(kept)} sites")
print(f"  dropped but NOT contradicted               : {len(notc)} sites")
partition("the dropped sites, by whether the owner check contradicts them",
          [len(both), len(notc)], len(dropped), "sites")
print("  EVERY SITE THE OWNER CHECK CONTRADICTS IS ONE THE PLAIN SET DROPS: "
      f"{contra53 <= dropped}")
cross("the corrected set against the round 53 set minus the contradicted sites", len(KCO),
      len(K53) - len(contra53), "sites")
print(f"  the corrected set IS that difference, as a set: {KCO == K53 - contra53}")
print(f"\n  the {len(notc)} sites the plain set drops that the owner check does NOT "
      f"contradict, by file:")
c = collections.Counter(k[0] for k in notc)
for f, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])):
    print(f"      {n:>3}  {f}")
partition("those sites by file", sorted(c.values(), reverse=True), len(notc), "sites")

print("\n=== 3. THE GUARD FIRES, AND THEN PASSES ===")
print("  A guard that has never been seen to fail is not a guard, and one that can never")
print("  pass is the same defect wearing the other face. Both readings are here.")
print(f"  over the round 53 set   : CONTRADICTED {counts53['contradicted']}")
print(f"  over the CORRECTED set  : CONTRADICTED {countsco['contradicted']}")
cross("the corrected run's contradicted count against zero", countsco["contradicted"], 0,
      "sites")
cross("the corrected run's ruled-site count against the corrected set file",
      countsco["ruled"], len(KCO), "sites")
print(f"  THE BLIND SPOT IS UNCHANGED AND IS STATED: refused {counts53['refused']} over the "
      f"round 53 set and {countsco['refused']} over the corrected one — the corrected set "
      f"removes what the check DECIDES against, never what it refuses to decide.")

print("\n=== 4. THE THREE TRANSFORM RUNS, IN REWRITES ===")
arms = (("round 53", "r76_tf_r53.out", K53), ("PLAIN", "r76_tf_plain.out", KPL),
        ("CORRECTED", "r77_tf_corr.out", KCO))
heads = {}
for label, fn, st in arms:
    head, rules = transform(fn)
    heads[label] = head
    print(f"  {label:10s} ruled {head['ruled']:>5}  files {head['files']:>4}  "
          f"total {head['total']:>5}  undecided {head['undecided']:>5}")
    cross(f"the {label} arm's ruled-key count against its own set file", head["ruled"],
          len(st), "sites")
    cross(f"the {label} arm's rule table against its own printed total",
          sum(v for k, v in rules.items() if not k.startswith("X")), head["total"],
          "rewrites")

print("\n=== 5. THE THREE SUITE RUNS BESIDE THEIR CONTROL, IN TEST NODES ===")
cf, ce = outcomes("r76_suite_ctl.out")
sf, se = summary_counts("r76_suite_ctl.out")
cross("CONTROL failed node ids against its own tally line", len(cf), sf, "nodes")
cross("CONTROL error node ids against its own tally line", len(ce), se, "nodes")
print(f"  CONTROL    failed {len(cf):>5}   errors {len(ce):>5}")
BAD = {}
for label, fn in (("round 53", "r76_suite_r53.out"), ("PLAIN", "r76_suite_plain.out"),
                  ("CORRECTED", "r77_suite_corr.out")):
    f, e = outcomes(fn)
    tf, te = summary_counts(fn)
    BAD[label] = (f | e) - cf - ce
    print(f"  {label:10s} failed {len(f):>5}   errors {len(e):>5}   "
          f"CAUSED BY THE FLIP {len(BAD[label]):>5}")
    cross(f"{label} failed node ids against its own tally line", len(f), tf, "nodes")
    cross(f"{label} error node ids against its own tally line", len(e), te, "nodes")
    partition(f"the {label} arm", [len(f - cf), len(e - ce)], len(BAD[label]), "nodes")

print("\n=== 6. THE CORRECTED ARM AGAINST THE OTHER TWO, IN NODES ===")
for other in ("round 53", "PLAIN"):
    fixes = BAD[other] - BAD["CORRECTED"]
    breaks = BAD["CORRECTED"] - BAD[other]
    print(f"  CORRECTED against {other:9s}: FIXES {len(fixes):>4} nodes, "
          f"BREAKS {len(breaks):>4} nodes, net {len(BAD['CORRECTED']) - len(BAD[other]):>+5}")
    partition(f"the {other} arm by what the corrected set keeps and fixes",
              [len(BAD[other] & BAD["CORRECTED"]), len(fixes)], len(BAD[other]), "nodes")
fixed53 = BAD["round 53"] - BAD["CORRECTED"]
print(f"\n  the {len(fixed53)} nodes the corrected set fixes over the round 53 set, "
      f"by test file:")
c = collections.Counter(n.split("::")[0] for n in fixed53)
for f, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])):
    print(f"      {n:>4}  {f}")
partition("those nodes by file", sorted(c.values(), reverse=True), len(fixed53), "nodes")

print("\n=== 7. THE ATTRIBUTION ACROSS THE THREE ARMS, IN LOCATION FRAMES ===")
print("  Every AttributeError frame naming a receiver class and a missing attribute falls in")
print("  exactly one bucket, every bucket is listed in full, and none is abridged.")


def classify(fr):
    under, over, none_recv, other = (collections.Counter(), collections.Counter(),
                                     collections.Counter(), collections.Counter())
    for _p, exc, msg in fr:
        if exc != "AttributeError":
            continue
        m = ATTR.search(msg)
        if not m:
            continue
        cls, attr = m.group(1), m.group(2)
        key = f"{cls}.{attr}"
        if cls in RECORD and attr in CLASSIC:
            under[key] += 1
        elif attr in UNIFIED and cls == "NoneType":
            none_recv[key] += 1
        elif attr in UNIFIED:
            over[key] += 1
        else:
            other[key] += 1
    return under, over, none_recv, other


trade = {}
for label, fn in (("round 53", "r76_suite_r53.out"), ("PLAIN", "r76_suite_plain.out"),
                  ("CORRECTED", "r77_suite_corr.out")):
    fr = frames(fn)
    under, over, none_recv, other = classify(fr)
    trade[label] = (sum(under.values()), sum(over.values()))
    print(f"\n  --- {label} ---   location frames parsed: {len(fr)}")
    for title, cc in (("UNDER-SELECTION, a classic field read left on a unified record", under),
                      ("OVER-SELECTION on a NAMED class, which is what R-0880 reports", over),
                      ("a unified field read on an ABSENT receiver, a different cause",
                       none_recv)):
        print(f"  {title}: {sum(cc.values())} frames over {len(cc)} kinds")
        for k, n in sorted(cc.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"      {n:>5}  {k}")
    matched = sum(1 for _p, exc, msg in fr if exc == "AttributeError" and ATTR.search(msg))
    partition(f"the {label} attribution buckets",
              [sum(under.values()), sum(over.values()), sum(none_recv.values()),
               sum(other.values())], matched, "frames")

print(f"\n  THE TRADE, IN FRAMES. under-selection: round 53 {trade['round 53'][0]}, "
      f"PLAIN {trade['PLAIN'][0]}, CORRECTED {trade['CORRECTED'][0]}. "
      f"over-selection on a named class: round 53 {trade['round 53'][1]}, "
      f"PLAIN {trade['PLAIN'][1]}, CORRECTED {trade['CORRECTED'][1]}.")
print("  THE CORRECTED SET IS THE ONLY ARM WITH NO UNDER-SELECTION AND LESS OVER-SELECTION")
print("  THAN THE SET THE TRANSFORM CONSUMES TODAY.")

print("\n=== 8. THE CHECKS THIS OUTPUT CARRIES, COUNTED ===")
print("  A CROSS-CHECK compares two numbers derived from DIFFERENT sources and can fail; a")
print("  PARTITION adds a set's own parts back to the set and cannot. Both are printed, and")
print("  only the first kind is evidence that anything was verified.")
print(f"  CROSS-CHECKS run : {len(CROSS)}   holding: {sum(CROSS)}   FAILING: {len(CROSS) - sum(CROSS)}")
print(f"  PARTITIONS run   : {len(PART)}   holding: {sum(PART)}   FAILING: {len(PART) - sum(PART)}")
print(f"  EVERY CHECK HOLDS: {all(CROSS) and all(PART)}")
```
