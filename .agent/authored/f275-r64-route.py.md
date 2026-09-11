# F275 R64 — the route instrument, saved verbatim as an authored blob

Its extension is `.md` and that is load-bearing: a `.py` file anywhere `ruff check .` scans
is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this round gates on.

```python
"""F275 R64 — the route instrument. Re-derives every figure the round 64 artefact states.

Four readings under four banners. (1) THE RUNTIME: whether the column information
DECISION F275 D36 part three orders exists here at all. (2) THE DISCRIMINATION: whether
`f_lasti` separates two same-named attribute reads on ONE line, on the REAL pydantic model
the F275 R53 probe installs over, with the same outward frame walk that probe uses.
(3) THE RESOLUTION: whether a recorded offset maps back to its NAMED receiver by
disassembly. (4) THE COVERAGE: how far that resolution reaches over the 39 at-risk lines
DECISION F275 D36 bounds.

Installs a descriptor over `packages.core.models.Job.id` IN THIS PROCESS ONLY and writes
nothing anywhere.
"""
import ast
import collections
import dis
import json
import os
import pathlib
import sys

REPO = pathlib.Path("/home/decodeux/Repos/remedy")
SCR = REPO / ".remedy-wt"
PREFIX = str(REPO) + os.sep
sys.path.insert(0, str(REPO))

print("=== 1. THE RUNTIME ===")
print(f"python {sys.version.split()[0]}")
print(f"code objects carry co_positions (PEP 657, 3.11+): "
      f"{hasattr((lambda: None).__code__, 'co_positions')}")
print("positional attributes a frame carries: "
      f"{sorted(a for a in dir(sys._getframe()) if a in ('f_lineno', 'f_lasti'))}")

from packages.core import models  # noqa: E402

RECORDS = []


def _classify(filename):
    if isinstance(filename, str) and os.path.isabs(filename) and filename.startswith(PREFIX):
        return True, filename[len(PREFIX):]
    return False, filename


def _record(owner, field, mode):
    """The F275 R53 probe's own outward walk, with `f_lasti` added to what it keeps."""
    frame = sys._getframe(2)
    innermost, direct, chosen, f = frame, None, None, frame
    while f is not None:
        qual, rel = _classify(f.f_code.co_filename)
        if direct is None:
            direct = qual
        if qual:
            chosen = (rel, f.f_lineno, f.f_code.co_name, f.f_lasti, f.f_code)
            break
        f = f.f_back
    if chosen is None:
        _, rel = _classify(innermost.f_code.co_filename)
        chosen = (rel, innermost.f_lineno, innermost.f_code.co_name,
                  innermost.f_lasti, innermost.f_code)
    RECORDS.append((owner, field, mode, bool(direct)) + chosen)


def _make(owner, field):
    def getter(self, _o=owner, _f=field):
        _record(_o, _f, "read")
        return self.__dict__[_f]

    def setter(self, value, _o=owner, _f=field):
        _record(_o, _f, "write")
        self.__dict__[_f] = value
        self.__pydantic_fields_set__.add(_f)

    return property(getter, setter)


print("\n=== 2. THE DISCRIMINATION, on the real model ===")
print(f"Job.id is a pydantic field: {'id' in models.Job.model_fields}")
setattr(models.Job, "id", _make("Job", "id"))
job, other = models.Job(name="j"), models.Job(name="o")
RECORDS.clear()


def two_on_one_line(a, b):
    return str(a.id) == str(b.id)


two_on_one_line(job, other)
for owner, field, mode, direct, path, line, func, lasti, _c in RECORDS:
    print(f"  {owner}.{field} {mode} direct={direct} {path}:{line} {func}() f_lasti={lasti}")
k_line = {(r[4], r[5], r[6]) for r in RECORDS}
k_lasti = {(r[4], r[5], r[6], r[7]) for r in RECORDS}
print(f"  reads {len(RECORDS)}   distinct (path, line, func) {len(k_line)}"
      f"   distinct with f_lasti {len(k_lasti)}")
print(f"  the offset DISCRIMINATES where the line does not: {len(k_lasti) > len(k_line)}")

print("\n=== 3. THE RESOLUTION, offset back to receiver by disassembly ===")
LOADS = ("LOAD_FAST", "LOAD_GLOBAL", "LOAD_DEREF")
code = two_on_one_line.__code__
got = []
for r in RECORDS:
    if r[8] is not code:
        print(f"  f_lasti={r[7]} belongs to {r[8].co_name}, not the read's own frame")
        continue
    prev = [i for i in dis.get_instructions(code)
            if i.offset <= r[7] and i.opname in LOADS]
    got.append(prev[-1].argval if prev else "?")
    print(f"  f_lasti={r[7]:<4} -> receiver {got[-1]!r}")
print(f"  receivers resolved in order {got} | source order ['a', 'b'] | "
      f"MATCH {got == ['a', 'b']}")

print("\n=== 4. THE COVERAGE over the 39 at-risk lines ===")
d = json.loads((SCR / "r53_R.json").read_text())
R = {tuple(x) for x in d["R"]}
by_key = {(s["path"], s["line"], s["col"], s["attr"]): s for s in d["sites"]}
owners = {}
for key, owner in json.loads((SCR / "r55_owners.json").read_text()).items():
    p, ln, col, attr = key.rsplit("|", 3)
    owners[(p, int(ln), int(col), attr)] = owner
byline = collections.defaultdict(list)
for k in R:
    byline[(k[0], k[1])].append(k)
at_risk = []
for ln, ks in byline.items():
    groups = collections.defaultdict(set)
    for k in ks:
        groups[(owners.get(k), k[3])].add(by_key[k]["recv"] or "(expr)")
    for (owner, attr), names in groups.items():
        if len(names) > 1:
            at_risk.append((ln, attr, sorted(names),
                            [k for k in ks if owners.get(k) == owner and k[3] == attr]))
# `R` is a set, so the walk above visits lines in an order that varies per process.
# Every listing below is therefore sorted: a report a gate compares line by line has to
# be the same report twice.
at_risk.sort(key=lambda r: (r[0][0], r[0][1], r[1]))
print(f"  at-risk lines {len(at_risk)}   ruled sites on them "
      f"{sum(len(m) for *_x, m in at_risk)}")
print(f"  lines whose receiver-NAME set has more than one member: "
      f"{sum(1 for _l, _a, n, _m in at_risk if len(n) > 1)}")
print(f"  lines carrying the placeholder receiver '(expr)': "
      f"{sum(1 for _l, _a, n, _m in at_risk if '(expr)' in n)}")
shapes, hard, mismatch = collections.Counter(), [], []
for (path, line), attr, names, members in at_risk:
    tree = ast.parse((REPO / path).read_text(encoding="utf-8", errors="replace"))
    nodes = [n for n in ast.walk(tree)
             if isinstance(n, ast.Attribute) and n.lineno == line and n.attr == attr]
    if len(nodes) != len(members):
        mismatch.append((path, line, attr, len(members), len(nodes),
                         sorted(k[2] for k in members),
                         sorted(n.value.col_offset for n in nodes)))
    for n in nodes:
        kind = type(n.value).__name__
        shapes[kind] += 1
        if kind != "Name":
            hard.append((path, line, attr, kind))
print("  the receiver expression of every attribute node on those lines:")
for kind, n in shapes.most_common():
    print(f"    {n:>4}  {kind}")
print(f"  a bare Name, which one load instruction resolves: {shapes.get('Name', 0)} "
      f"of {sum(shapes.values())}")
print("  the rest, which the route must REFUSE rather than guess:")
for path, line, attr, kind in sorted(hard):
    print(f"    {path}:{line} .{attr} receiver is {kind}")
print(f"  lines where the ruled-site count and the ast node count DISAGREE: {len(mismatch)}")
for path, line, attr, ms, ns, mcols, ncols in mismatch:
    print(f"    {path}:{line} .{attr}  ruled sites {ms} ast nodes {ns}"
          f"  site cols {mcols}  node value cols {ncols}")
```
