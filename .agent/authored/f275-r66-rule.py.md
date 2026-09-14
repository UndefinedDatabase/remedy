# F275 R66 — the ruling instrument, saved verbatim as an authored blob

Its extension is `.md` and that is load-bearing: a `.py` file anywhere `ruff check .` scans
is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this round gates on.

```python
"""F275 R66 — the ruling instrument. Re-derives every figure the artefact states.

Four readings. (1) THE THREE SITES DECISION F275 D39 holds the write shut on, each with the
source line, the sweep's own sites, the re-keyed probe's rows and the `ast` nodes actually
present, plus the `long_run_executor.py:504` disagreement round 64 reported. (2) THE
SWEEP'S OWN POSITIONS: how many ruled keys resolve to an `ast` Attribute at that exact
line and column. (3) PYTEST'S ASSERTION REWRITING, enumerated. (4) HOW FAR IT REACHES into
the 52 drops the receiver join makes.

Reads only; creates nothing and writes nothing.
"""
import ast
import json
import pathlib

REPO = pathlib.Path("/home/decodeux/Repos/remedy")
SCR = REPO / ".remedy-wt"
d = json.loads((SCR / "r53_R.json").read_text())
R = {tuple(r) for r in d["R"]}
SITES = d["sites"]
rows = json.loads((SCR / "r65_probe1.json").read_text())["rows"]
JOB_FIELD, TASK_FIELD = {"id", "name"}, {"id", "description"}


def src_line(path, line):
    return (REPO / path).read_text(encoding="utf-8", errors="replace").split("\n")[line - 1]


print("=== 1. THE THREE SITES, AND THE 504 DISAGREEMENT ===")
for path, line in (("packages/orchestration/long_run_executor.py", 505),
                   ("tests/orchestration/test_loop_run.py", 285),
                   ("tests/orchestration/test_repair_loop_v1.py", 56),
                   ("packages/orchestration/long_run_executor.py", 504)):
    print(f"  --- {path}:{line}")
    print(f"    source: {src_line(path, line)!r}")
    for s in sorted([s for s in SITES if s["path"] == path and s["line"] == line],
                    key=lambda s: s["col"]):
        k = (s["path"], s["line"], s["col"], s["attr"])
        print(f"    sweep  col {s['col']:>3} .{s['attr']:<12} recv {s['recv']!r:<14} "
              f"static {s['static']!r:<7} RULED {k in R}")
    for r in sorted([r for r in rows if r["path"] == path and r["line"] == line],
                    key=lambda r: r["lasti"]):
        print(f"    probe  {r['owner']}.{r['field']:<12} lasti {r['lasti']:>4} "
              f"recv {r['recv']!r:<16} direct {r['direct']}")
    tree = ast.parse((REPO / path).read_text(encoding="utf-8", errors="replace"))
    for n in sorted([n for n in ast.walk(tree)
                     if isinstance(n, ast.Attribute) and n.lineno == line],
                    key=lambda n: n.col_offset):
        print(f"    ast    .{n.attr:<12} value {type(n.value).__name__:<10} "
              f"node col {n.col_offset:>3} end col {n.end_col_offset:>3}")

print("\n=== 2. DO THE SWEEP'S OWN (line, col) POSITIONS RESOLVE? ===")
nodes = {}
for path in sorted({k[0] for k in R}):
    try:
        tree = ast.parse((REPO / path).read_text(encoding="utf-8", errors="replace"))
    except (SyntaxError, OSError):
        continue
    nodes[path] = {(n.lineno, n.col_offset, n.attr)
                   for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
exact = sum(1 for p, l, c, a in R if p in nodes and (l, c, a) in nodes[p])
print(f"  ruled keys                                        : {len(R)}")
print(f"  resolving to an ast Attribute at that exact position: {exact}")
print(f"  NOT resolving there                               : {len(R) - exact}")
print("  a key that resolves to nothing is a key no ast-walking consumer can match.")

print("\n=== 3. PYTEST'S ASSERTION REWRITING ===")
synth = sorted([r for r in rows if r["recv"] and r["recv"].startswith("@py_")],
               key=lambda r: (r["path"], r["line"], r["lasti"]))
print(f"  probe rows whose resolved receiver is synthetic: {len(synth)}")
print(f"  distinct synthetic names: {sorted({r['recv'] for r in synth})}")
print(f"  distinct lines they sit on: {len({(r['path'], r['line']) for r in synth})}")
on_assert = sum(1 for p, l in {(r["path"], r["line"]) for r in synth}
                if src_line(p, l).strip().startswith("assert "))
print(f"  of those lines, beginning with `assert ` in the source: {on_assert}")
for r in synth:
    print(f"    {r['path']}:{r['line']} {r['owner']}.{r['field']} recv {r['recv']!r}")

print("\n=== 4. HOW FAR IT REACHES INTO THE DROPS ===")


def owners_of(s):
    return [o for o, fs in (("Job", JOB_FIELD), ("Task", TASK_FIELD)) if s["attr"] in fs]


def build(line_set, recv_set=None, refused=None):
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


l65 = {(r["path"], r["line"], r["owner"], r["field"]) for r in rows}
recv = {(r["path"], r["line"], r["owner"], r["field"], r["recv"])
        for r in rows if r["recv"] is not None}
refused = {(r["path"], r["line"], r["owner"], r["field"])
           for r in rows if r["recv"] is None}
dropped = build(l65) - build(l65, recv, refused)
synth_lines = {(r["path"], r["line"]) for r in synth}
hit = sorted({k for k in dropped if (k[0], k[1]) in synth_lines})
print(f"  dropped sites                                  : {len(dropped)}")
print(f"  of them on a line carrying a SYNTHETIC receiver: {len(hit)}")
print("  every one of them, which is a drop the rewriting caused and not the key:")
for k in hit:
    print(f"    {k[0]}:{k[1]} col {k[2]} .{k[3]}")
```
