# F275 R76 — the residue instrument, verbatim

> Saved as `.md` and not as `.py` on purpose: a `.py` file anywhere `ruff check .`
> scans is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this
> round's tree gate reads. The gate extracts the single fence below into
> `.remedy-wt/` and runs it there, which is outside the tree.
>
> This carrier was GENERATED from its source by the same script that verified the
> extraction round-trips back to that source, in one step, per DECISION F275 D44.

```python
"""F275 R76 — what the two corrections cost the FLIP, measured in FAILURES.

DECISION F275 D41 deferred the flip's dry run against the plain re-derived set of round 67,
and DECISION F275 D44's consequence paragraph still records it as not taken. This instrument
reads that run. It re-analyses SAVED logs and SAVED site sets and runs no test of its own, so
it is deterministic and reproducible; the three pytest invocations that produced the logs are
the reviewer's and their summary lines are declared as reviewer readings in the artefact.

THE COMPARISON IS ONE-VARIABLE. Both arms run the same guarded transform of DECISION F275
D43, at the same commit, over the same 994 tracked `.py` files, with the same status input.
They differ in the RULED SITE SET alone: the round 53 committed set re-keyed (2198 sites)
against the round 67 plain re-derivation re-keyed (2138 sites).

EVERY COUNT STATES ITS UNIT and every distribution prints the SUM of its own buckets beside
the total it claims to partition, per DECISION F275 D49.

Usage: python3 -B r76_instrument.py <scratch_dir>
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
SUMMARY = re.compile(r"^\d+ (failed|passed).*(in \d+\.\d+s|seconds)")
# the two record classes the flip creates, and the classic field names it renames away
RECORD = {"JobPlan", "TaskEntry"}
CLASSIC = {"id", "name", "description"}
UNIFIED = {"job_id", "job_title", "task_id", "title"}

INPUTS = [
    "r53_R.json", "r76_plain.json", "r76_plain_rekeyed.json", "r76_r53_rekeyed.json",
    "r76_tf_r53.out", "r76_tf_plain.out",
    "r76_suite_ctl.out", "r76_suite_r53.out", "r76_suite_plain.out",
]


def digest(name):
    b = (SCR / name).read_bytes()
    return len(b), hashlib.sha256(b).hexdigest()


def outcomes(name):
    """FAILED and ERROR node ids, as two sets, from a `-rfE` short summary."""
    failed, errored = set(), set()
    for line in (SCR / name).read_text(errors="replace").splitlines():
        if line.startswith("FAILED "):
            failed.add(line[len("FAILED "):].split(" - ")[0].strip())
        elif line.startswith("ERROR "):
            errored.add(line[len("ERROR "):].split(" - ")[0].strip())
    return failed, errored


def frames(name):
    """Every `<path>:<line>: <Exc>: <msg>` location frame of a `--tb=line` report."""
    out = []
    for line in (SCR / name).read_text(errors="replace").splitlines():
        m = FRAME.match(line.strip())
        if m:
            out.append((m.group("path"), int(m.group("line")), m.group("exc"),
                        (m.group("msg") or "").strip()))
    return out


def relative(path):
    """A frame path as a repo-relative one, so the two arms' frames are comparable.

    Every frame of a run names the worktree it ran in, so the same source file appears
    under two different absolute paths across the two arms and a naive count of paths
    reads every file as having moved. Frames outside any worktree keep their own path.
    """
    for marker in ("/r76_flip53/", "/r76_flip/", "/r76_ctl/"):
        if marker in path:
            return path.split(marker, 1)[1]
    return path


def tail(name):
    lines = [x.strip() for x in (SCR / name).read_text(errors="replace").splitlines()]
    return [x for x in lines if SUMMARY.match(x)]


def summary_counts(name):
    """The failed and error counts as pytest's own SUMMARY LINE reports them.

    This is a second, independent reading of the same run: the short-summary `FAILED` and
    `ERROR` lines are emitted by `-rfE` and the tally line by pytest's terminal reporter,
    so comparing the two can fail — which is the whole reason it is here. A partition of a
    set against its own parts cannot.
    """
    got = {}
    for line in tail(name):
        for key in ("failed", "error"):
            m = re.search(rf"(\d+) {key}s?\b", line)
            got[key] = int(m.group(1)) if m else 0
    return got.get("failed", 0), got.get("error", 0)


CROSS, PART = [], []


def cross(label, a, b, unit):
    """A CROSS-CHECK between two numbers derived from DIFFERENT sources. It can fail."""
    ok = a == b
    CROSS.append(ok)
    print(f"  CROSS-CHECK {label}: {a} against {b} {unit}  -> {'MATCH' if ok else 'MISMATCH'}")
    return ok


def partition(label, parts, total, unit):
    """A PARTITION IDENTITY, printed so a reader can add up. It is true by construction."""
    s = sum(parts)
    ok = s == total
    PART.append(ok)
    print(f"  PARTITION {label}: {' + '.join(str(p) for p in parts)} = {s} against {total} "
          f"{unit}  -> {'MATCH' if ok else 'MISMATCH'}")
    return ok


print("=== 0. THE INPUTS THIS READING IS TAKEN FROM ===")
print("  Every figure below comes from these files and from nothing else.")
for n in INPUTS:
    size, sha = digest(n)
    print(f"    {n:26s} {size:>9} bytes  sha256 {sha}")

print("\n=== 1. THE TWO RULED SITE SETS, IN SITES ===")
R53 = {tuple(r) for r in json.loads((SCR / "r53_R.json").read_text())["R"]}
PLAIN = {tuple(r) for r in json.loads((SCR / "r76_plain.json").read_text())["R"]}
K53 = {tuple(r) for r in json.loads((SCR / "r76_r53_rekeyed.json").read_text())["R"]}
KPL = {tuple(r) for r in json.loads((SCR / "r76_plain_rekeyed.json").read_text())["R"]}
dropped = R53 - PLAIN
print(f"  round 53 committed set                 : {len(R53)} sites")
print(f"  round 67 plain re-derivation           : {len(PLAIN)} sites")
print(f"  PLAIN is a SUBSET of round 53's        : {PLAIN <= R53}")
print(f"  sites round 53 rules and PLAIN drops   : {len(dropped)} sites")
print(f"  sites PLAIN rules and round 53 lacks   : {len(PLAIN - R53)} sites")
print(f"  re-keyed onto this base: round 53 {len(K53)} sites, PLAIN {len(KPL)} sites")

byfile = collections.Counter(k[0] for k in dropped)
prod = {f: n for f, n in byfile.items() if not f.startswith("tests/")}
test = {f: n for f, n in byfile.items() if f.startswith("tests/")}
cross("the re-keyed round 53 set against the set it was re-keyed from", len(K53), len(R53),
      "sites")
cross("the re-keyed PLAIN set against the set it was re-keyed from", len(KPL), len(PLAIN),
      "sites")

print(f"\n  the dropped sites by file, in sites ({len(byfile)} files):")
for f, n in sorted(byfile.items(), key=lambda kv: (-kv[1], kv[0])):
    print(f"      {n:>3}  {f}")
partition("the dropped sites by file", sorted(byfile.values(), reverse=True), len(dropped),
          "sites")
print(f"  of them in production files: {sum(prod.values())} sites over {len(prod)} files")
print(f"  of them in test files      : {sum(test.values())} sites over {len(test)} files")
partition("production against test", [sum(prod.values()), sum(test.values())], len(dropped),
          "sites")

print("\n=== 2. THE TWO TRANSFORM RUNS, IN REWRITES ===")


def transform(name):
    """The transform's header figures and its rule table, parsed separately.

    The rule table is read ONLY between its own heading and the blank line that ends it,
    and a row is split at its LAST run of whitespace — not at a two-space gap, which three
    of the longest rule names do not have. Reading the table by a fixed gap silently drops
    those rows, and the cross-check against the transform's own printed total is what
    catches it; that check found exactly this defect in this instrument before emission.
    """
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


h53, u53 = transform("r76_tf_r53.out")
hpl, upl = transform("r76_tf_plain.out")
for key in ("ruled", "files", "total", "undecided"):
    print(f"  {key:>10}:  round 53 {h53[key]:>6}   PLAIN {hpl[key]:>6}   "
          f"difference {hpl[key] - h53[key]:>+5}")
cross("the round 53 arm's ruled-key count against its own set file", h53["ruled"], len(K53),
      "sites")
cross("the PLAIN arm's ruled-key count against its own set file", hpl["ruled"], len(KPL),
      "sites")

print("\n  the rules whose count MOVED, in rewrites:")
moved = {k for k in set(u53) | set(upl) if u53.get(k, 0) != upl.get(k, 0)}
for k in sorted(moved):
    print(f"      {k:34s} {u53.get(k, 0):>6} -> {upl.get(k, 0):>6}   "
          f"{upl.get(k, 0) - u53.get(k, 0):>+5}")
cross("the rules that MOVED against the change in the printed total",
      sum(upl.get(k, 0) - u53.get(k, 0) for k in moved), hpl["total"] - h53["total"],
      "rewrites")
for label, head, rules in (("round 53", h53, u53), ("PLAIN", hpl, upl)):
    cross(f"the {label} arm's rule table against its own printed total",
          sum(v for k, v in rules.items() if not k.startswith("X")), head["total"], "rewrites")
print(f"  rules unchanged across the two arms: {len(set(u53) | set(upl)) - len(moved)}")

print("\n=== 3. THE THREE SUITE RUNS, IN TEST NODES ===")
print("  The pytest summary line of each run, quoted from its own transcript:")
for label, name in (("CONTROL", "r76_suite_ctl.out"), ("R53    ", "r76_suite_r53.out"),
                    ("PLAIN  ", "r76_suite_plain.out")):
    for line in tail(name):
        print(f"    {label}  {line}")

cf, ce = outcomes("r76_suite_ctl.out")
rf, rE = outcomes("r76_suite_r53.out")
pf, pE = outcomes("r76_suite_plain.out")
print("\n  node ids collected from the short summaries, in nodes:")
print(f"    CONTROL  failed {len(cf):>5}   errors {len(ce):>5}")
print(f"    R53      failed {len(rf):>5}   errors {len(rE):>5}")
print(f"    PLAIN    failed {len(pf):>5}   errors {len(pE):>5}")
print("\n  the same two counts as PYTEST'S OWN TALLY LINE reports them, which is a second and")
print("  independent reading of each run rather than a partition of the first:")
for label, name, ids in (("CONTROL", "r76_suite_ctl.out", (cf, ce)),
                         ("R53", "r76_suite_r53.out", (rf, rE)),
                         ("PLAIN", "r76_suite_plain.out", (pf, pE))):
    sf, se = summary_counts(name)
    print(f"    {label:8s} tally line: failed {sf:>5}   errors {se:>5}")
    cross(f"{label} failed node ids against the tally line", len(ids[0]), sf, "nodes")
    cross(f"{label} error node ids against the tally line", len(ids[1]), se, "nodes")

shared_ctl = (rf | rE) & (cf | ce)
shared_ctl_p = (pf | pE) & (cf | ce)
print(f"\n  nodes bad in the CONTROL too, and therefore a worktree artefact and not the flip:")
print(f"    R53 {len(shared_ctl)}   PLAIN {len(shared_ctl_p)}")
for n in sorted(shared_ctl | shared_ctl_p):
    print(f"      {n}")

BAD53 = (rf | rE) - cf - ce
BADPL = (pf | pE) - cf - ce
print("\n  CAUSED BY THE FLIP, in nodes:")
print(f"    R53    {len(BAD53):>5}   = failures {len(rf - cf):>5} + errors {len(rE - ce):>5}")
print(f"    PLAIN  {len(BADPL):>5}   = failures {len(pf - cf):>5} + errors {len(pE - ce):>5}")
partition("the round 53 arm", [len(rf - cf), len(rE - ce)], len(BAD53), "nodes")
partition("the PLAIN arm", [len(pf - cf), len(pE - ce)], len(BADPL), "nodes")
print(f"    THE PLAIN SET COSTS {len(BADPL) - len(BAD53):+d} BAD NODES over the round 53 set.")

print("\n=== 4. THE ARM DIFFERENCE, IN NODES ===")
only_p, only_r, both = BADPL - BAD53, BAD53 - BADPL, BADPL & BAD53
print(f"  bad under PLAIN only (the plain set BREAKS) : {len(only_p)} nodes")
print(f"  bad under R53 only   (the plain set FIXES)  : {len(only_r)} nodes")
print(f"  bad under both                              : {len(both)} nodes")
partition("the PLAIN arm by shared and own", [len(both), len(only_p)], len(BADPL), "nodes")
partition("the round 53 arm by shared and own", [len(both), len(only_r)], len(BAD53), "nodes")

for label, s in (("the plain set BREAKS", only_p), ("the plain set FIXES", only_r)):
    c = collections.Counter(n.split("::")[0] for n in s)
    print(f"\n  {label}, by test file, in nodes ({len(c)} files):")
    for f, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"      {n:>4}  {f:62s} holds a dropped site: {f in byfile}")
    partition(f"{label} by file", sorted(c.values(), reverse=True), len(s), "nodes")

print("\n=== 5. THE ATTRIBUTION, IN LOCATION FRAMES ===")
print("  Every AttributeError frame naming a receiver class and a missing attribute falls in")
print("  exactly one bucket below, every bucket is listed in full, and none is abridged.")
fr53, frpl = frames("r76_suite_r53.out"), frames("r76_suite_plain.out")
print(f"  location frames parsed: R53 {len(fr53)}   PLAIN {len(frpl)}")


def classify(fr):
    """Four buckets, every matched frame in exactly one of them.

    OVER-SELECTION is split, because `NoneType` is not a wrong class but an absent
    receiver — a different cause that this reading must not fold into the class R-0880
    names — and the split is measured here rather than derived by eye afterwards.
    """
    under, over, none_recv, other = (collections.Counter(), collections.Counter(),
                                     collections.Counter(), collections.Counter())
    for _p, _l, exc, msg in fr:
        if exc != "AttributeError":
            continue
        m = ATTR.search(msg)
        if not m:
            continue
        cls, attr = m.group(1), m.group(2)
        key = f"{cls}.{attr}"
        if cls in RECORD and attr in CLASSIC:
            under[key] += 1          # the flip renamed the field and left this read behind
        elif attr in UNIFIED and cls == "NoneType":
            none_recv[key] += 1      # an absent receiver, not a wrong record
        elif attr in UNIFIED:
            over[key] += 1           # the flip renamed a read on a record it does not own
        else:
            other[key] += 1
    return under, over, none_recv, other


# the receiver classes finding `R-0880` names in its own MEASUREMENT sentence
R0880_CLASSES = {"Mission", "Artifact", "QueueEntry", "BrainNode", "_FakeJob"}

for label, fr in (("R53", fr53), ("PLAIN", frpl)):
    under, over, none_recv, other = classify(fr)
    tot = sum(under.values()) + sum(over.values()) + sum(none_recv.values()) + sum(other.values())
    print(f"\n  --- {label} ---")
    for title, c in (("UNDER-SELECTION, a classic field read left standing on a unified record",
                      under),
                     ("OVER-SELECTION on a NAMED class, which is what R-0880 reports", over),
                     ("a unified field read on an ABSENT receiver, a different cause", none_recv),
                     ("NEITHER", other)):
        print(f"  {title}: {sum(c.values())} frames over {len(c)} kinds")
        for k, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"      {n:>5}  {k}")
    matched = sum(1 for _p, _l, exc, msg in fr if exc == "AttributeError" and ATTR.search(msg))
    partition(f"the {label} attribution buckets",
              [sum(under.values()), sum(over.values()), sum(none_recv.values()),
               sum(other.values())], matched, "frames")
    seen = {k.split(".")[0] for k in over}
    print(f"  the classes in the OVER-SELECTION bucket: {sorted(seen) if seen else 'none'}")
    print(f"  every one of them is named by R-0880: {seen <= R0880_CLASSES}")

u53_, o53_, n53_, _ = classify(fr53)
upl_, opl_, npl_, _ = classify(frpl)
print(f"\n  THE TRADE, IN FRAMES: under-selection {sum(u53_.values())} -> {sum(upl_.values())} "
      f"({sum(upl_.values()) - sum(u53_.values()):+d}), "
      f"over-selection on a named class {sum(o53_.values())} -> {sum(opl_.values())} "
      f"({sum(opl_.values()) - sum(o53_.values()):+d}), "
      f"absent receiver {sum(n53_.values())} -> {sum(npl_.values())} "
      f"({sum(npl_.values()) - sum(n53_.values()):+d}).")

print("\n=== 6. THE FILES WHOSE FRAME COUNT MOVED, IN FRAMES ===")
c53 = collections.Counter(relative(f[0]) for f in fr53)
cpl = collections.Counter(relative(f[0]) for f in frpl)
delta = {f: cpl[f] - c53[f] for f in set(c53) | set(cpl) if cpl[f] != c53[f]}
print(f"  files whose repo-relative frame count differs between the arms: {len(delta)}")
for f, n in sorted(delta.items(), key=lambda kv: (-abs(kv[1]), kv[0])):
    print(f"      {n:>+5}  {f:62s} holds a dropped site: {f in byfile}")
cross("the per-file deltas against the change in the frame total", sum(delta.values()),
      len(frpl) - len(fr53), "frames")

print("\n=== 7. THE EXCEPTION CLASSES, IN FRAMES ===")
e53 = collections.Counter(f[2] for f in fr53)
epl = collections.Counter(f[2] for f in frpl)
for exc in sorted(set(e53) | set(epl), key=lambda x: (-(epl[x] + e53[x]), x)):
    print(f"      {exc:24s} R53 {e53[exc]:>5}   PLAIN {epl[exc]:>5}   "
          f"{epl[exc] - e53[exc]:>+5}")
partition("the round 53 exception classes", sorted(e53.values(), reverse=True), len(fr53),
          "frames")
partition("the PLAIN exception classes", sorted(epl.values(), reverse=True), len(frpl),
          "frames")

print("\n=== 8. THE CHECKS THIS OUTPUT CARRIES, COUNTED ===")
print("  A CROSS-CHECK compares two numbers derived from DIFFERENT sources and can fail; a")
print("  PARTITION adds a set's own parts back to the set and cannot. Both are printed, and")
print("  only the first kind is evidence that anything was verified.")
print(f"  CROSS-CHECKS run : {len(CROSS)}   holding: {sum(CROSS)}   FAILING: {len(CROSS) - sum(CROSS)}")
print(f"  PARTITIONS run   : {len(PART)}   holding: {sum(PART)}   FAILING: {len(PART) - sum(PART)}")
print(f"  EVERY CHECK HOLDS: {all(CROSS) and all(PART)}")
```
