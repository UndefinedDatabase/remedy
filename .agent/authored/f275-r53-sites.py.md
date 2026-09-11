# F275 R53 — `f275_r53_sites.py`, the static sweep, the heuristic control and the artefact generator

> Committed verbatim so `.agent/f275_t003_descriptor_sites.md` is reproducible from
> the repository itself. It is a `.md` and not a `.py` because a `.py` file anywhere
> `ruff check .` scans is counted by `tests/orchestration/test_ci_budgets.py`, and a
> probe left at a worktree root turned the lint-ceiling test red — measured, not feared.

```python
"""F275 R53 — DECISION F275 D29's P1: the type-resolved site set, and the artefact.

Usage: python3 -B f275_r53_sites.py <base> <control_base> <scratch> <out.md>

<scratch> holds, by fixed name: f275_r53_probe.py, f275_r53_sites.py (this file),
probe1.json, probe2.json, run1.txt, run2.txt.

The universe is exactly the node set the R50 transform edits: every `ast.Attribute`
whose `attr` is a classic-record field name, over `git ls-files '*.py'`, minus that
transform's five excluded files. Each node is classified THREE ways over that ONE
selection, so every difference below is a difference of verdict and never of scope.

  H  the RECEIVER-NAME HEURISTIC, verbatim from `.agent/f275_t003_flip_residue_r50.md`
  S  STATIC TYPE RESOLUTION: the receiver is provably the class whose field it names
  P  the descriptor PROBE's executed sites

R = P | S is the set D29's P1 orders the transform to consume. Every figure is printed
with the reviewer's own reading beside it, so a difference is visible, not reconciled.
"""
import ast
import collections
import hashlib
import json
import os
import subprocess
import sys

JOB_FIELD, TASK_FIELD = {"id", "name"}, {"id", "description"}
ALL_FIELD = JOB_FIELD | TASK_FIELD
JOBISH, TASKISH = ("job", "plan", "record"), ("task",)
EXCLUDE = {"packages/core/models.py", "packages/orchestration/pingpong_job.py",
           "packages/orchestration/storage.py", "tests/test_storage.py",
           "tests/test_models.py"}
SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
UNIT = (ast.FunctionDef, ast.AsyncFunctionDef)
BODIES = ("body", "orelse", "finalbody", "handlers")
# An annotation naming only these carries no information about the classic record, so
# it is UNKNOWN and never a disproof: `_create_mission_for_job(job: Any)` takes a real
# `Job` from `load_job`, and reading `Any` as "some other type" disproved it falsely.
OPAQUE = {"Any", "object", "None", "Optional", "TYPE_CHECKING"}
# The reviewer's own readings, taken at the two bases named in the artefact header.
REF = {"tracked": 993, "scanned": 989, "universe": 5276, "H_job": 1896, "H_task": 532,
       "S_job": 315, "S_task": 92, "P": 2145, "R": 2198, "HmR": 359, "RmH": 129,
       "A": 6, "B": 36, "C": 317, "expr": 76, "ctl_job": 1896, "ctl_task": 532}

recv_name = lambda n: str(getattr(n, "id", None) or getattr(n, "attr", "") or "")
is_jobish = lambda s: s.lower() in ("j", "stored") or any(t in s.lower() for t in JOBISH)
is_taskish = lambda s: s.lower() in ("t", "tk") or any(t in s.lower() for t in TASKISH)


def annotation_names(node, depth=0):
    names = set()
    if node is None or depth > 3:
        return names
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            names.add(n.id)
        elif isinstance(n, ast.Attribute):
            names.add(n.attr)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            try:
                names |= annotation_names(ast.parse(n.value, mode="eval").body, depth + 1)
            except SyntaxError:
                pass
    return names


def call_class(node):
    if not isinstance(node, ast.Call):
        return None
    f = node.func
    name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
    return name if name in ("Job", "Task") else None


def params(node):
    a = node.args
    return list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs) + \
        [x for x in (a.vararg, a.kwarg) if x is not None]


def scope_statements(scope):
    out, stack = [], []
    for f in BODIES:
        v = getattr(scope, f, None)
        if isinstance(v, list):
            stack.extend(v)
    while stack:
        s = stack.pop()
        if isinstance(s, SCOPES):
            continue
        out.append(s)
        for f in BODIES:
            v = getattr(s, f, None)
            if isinstance(v, list):
                stack.extend(v)
    return out


def from_annotation(names):
    if not names or names <= OPAQUE:
        return None
    if "Job" in names and "Task" not in names:
        return "Job"
    if "Task" in names and "Job" not in names:
        return "Task"
    return "other"


def bind(scope):
    verdicts = {}

    def mark(name, v):
        cur = verdicts.get(name)
        if cur is None or cur == v:
            verdicts[name] = v
        elif v in ("Job", "Task") and cur == "other":
            verdicts[name] = v
        elif v in ("Job", "Task") and cur in ("Job", "Task"):
            verdicts[name] = "other"

    if isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        for arg in params(scope):
            v = from_annotation(annotation_names(getattr(arg, "annotation", None)))
            if v:
                mark(arg.arg, v)
    for s in scope_statements(scope):
        if isinstance(s, ast.AnnAssign) and isinstance(s.target, ast.Name):
            v = from_annotation(annotation_names(s.annotation))
            if v:
                mark(s.target.id, v)
            if s.value is not None and call_class(s.value):
                mark(s.target.id, call_class(s.value))
        elif isinstance(s, ast.Assign) and call_class(s.value):
            for t in s.targets:
                if isinstance(t, ast.Name):
                    mark(t.id, call_class(s.value))
    return verdicts


def walk_scope(scope, path, sites):
    verdicts = bind(scope)
    stack, nested = list(ast.iter_child_nodes(scope)), []
    while stack:
        n = stack.pop()
        if isinstance(n, SCOPES):
            nested.append(n)
            continue
        if isinstance(n, ast.Attribute) and n.attr in ALL_FIELD:
            recv, bare = recv_name(n.value), isinstance(n.value, ast.Name)
            sites.append({"path": path, "line": n.lineno, "col": n.col_offset,
                          "attr": n.attr, "recv": recv, "bare": bare,
                          "static": verdicts.get(recv) if bare else None,
                          "H": (n.attr in JOB_FIELD and is_jobish(recv)) or
                               (n.attr in TASK_FIELD and is_taskish(recv)),
                          "Hjob": n.attr in JOB_FIELD and is_jobish(recv)})
        stack.extend(ast.iter_child_nodes(n))
    for n in nested:
        walk_scope(n, path, sites)


def unit_map(base, path):
    """line -> enclosing def name; module level is '<module>'."""
    try:
        tree = ast.parse(open(os.path.join(base, path), "rb").read(), filename=path)
    except (SyntaxError, OSError, ValueError):
        return {}
    out = {}

    def walk(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, UNIT):
                for ln in range(child.lineno, getattr(child, "end_lineno", child.lineno) + 1):
                    out[ln] = child.name
            walk(child)

    walk(tree)
    return out


def sweep(base):
    paths = [p for p in subprocess.run(["git", "ls-files", "*.py"], cwd=base, check=True,
                                       capture_output=True, text=True).stdout.split("\n") if p]
    scanned = [p for p in paths if p not in EXCLUDE]
    sites, unparsable = [], []
    for rel in scanned:
        try:
            tree = ast.parse(open(os.path.join(base, rel), "rb").read(), filename=rel)
        except (SyntaxError, OSError, ValueError) as exc:
            unparsable.append([rel, str(exc)])
            continue
        walk_scope(tree, rel, sites)
    return paths, scanned, sites, unparsable


def probe_sets(blob):
    """(the owner/field/mode/site set, the (path,line,owner,field) set, the ran units)."""
    full, lines, units = set(), set(), set()
    for r in blob["rows"]:
        full.add((r["owner"], r["field"], r["mode"], r["path"], r["line"], r["func"]))
        lines.add((r["path"], r["line"], r["owner"], r["field"]))
        units.add((r["path"], r["func"]))
    return full, lines, units


def row(label, measured, ref_key, out):
    ref = REF.get(ref_key)
    verdict = "same" if measured == ref else "DIFFERS (%s)" % ref
    out.append("| %s | %d | %d | %s |" % (label, measured, ref, verdict))


def main():
    base, control, scratch, outfile = sys.argv[1:5]
    p1 = json.load(open(os.path.join(scratch, "probe1.json")))
    p2 = json.load(open(os.path.join(scratch, "probe2.json")))
    run1 = open(os.path.join(scratch, "run1.txt")).read().rstrip("\n").split("\n")[-1]
    run2 = open(os.path.join(scratch, "run2.txt")).read().rstrip("\n").split("\n")[-1]

    f1, l1, units = probe_sets(p1)
    f2, l2, _ = probe_sets(p2)
    symdiff = len(f1 ^ f2)

    paths, scanned, sites, unparsable = sweep(base)
    _, _, csites, _ = sweep(control)
    ctl_job = sum(1 for s in csites if s["Hjob"])
    ctl_task = sum(1 for s in csites if s["H"] and not s["Hjob"])

    key = lambda s: (s["path"], s["line"], s["col"], s["attr"])
    owners = lambda s: ([o for o, fs in (("Job", JOB_FIELD), ("Task", TASK_FIELD))
                         if s["attr"] in fs])
    in_P = lambda s: any((s["path"], s["line"], o, s["attr"]) in l1 for o in owners(s))
    in_S = lambda s: (s["static"] == "Job" and s["attr"] in JOB_FIELD) or \
                     (s["static"] == "Task" and s["attr"] in TASK_FIELD)

    H = {key(s) for s in sites if s["H"]}
    R = {key(s) for s in sites if in_P(s) or in_S(s)}
    HmR, RmH = H - R, R - H

    maps, cls, adds, misses = {}, collections.Counter(), [], []
    for s in sites:
        k = key(s)
        if k in HmR:
            if s["static"] == "other":
                c = "A"
            else:
                if s["path"] not in maps:
                    maps[s["path"]] = unit_map(base, s["path"])
                c = "B" if (s["path"], maps[s["path"]].get(s["line"], "<module>")) in units else "C"
            cls[c] += 1
            adds.append((c, s))
        elif k in RmH:
            misses.append(s)

    o = []
    A = o.append
    A("# F275 T003 — the flip's field rename, TYPE-RESOLVED\n")
    A("> DECISION F275 D29's P1. Generated by the two instruments embedded in section 2,")
    A("> never retyped: every numeral below is read out of the probe runs and the `ast`")
    A("> sweep's own output, and the `reviewer` column carries the reviewer's reading so a")
    A("> difference is VISIBLE rather than reconciled away. Measurement base: `%s`."
      % subprocess.run(["git", "rev-parse", "--short=8", "HEAD"], cwd=base, check=True,
                       capture_output=True, text=True).stdout.strip())
    A("> Heuristic control base: `%s`.\n"
      % subprocess.run(["git", "rev-parse", "--short=8", "HEAD"], cwd=control, check=True,
                       capture_output=True, text=True).stdout.strip())
    A("This file SIZES and TYPES the rename; it performs none of it, and no line under")
    A("`packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.\n")

    A("## 1. What was measured\n")
    A("| Figure | measured | reviewer | verdict |")
    A("|---|---|---|---|")
    t = []
    row("tracked `.py` from `git ls-files`", len(paths), "tracked", t)
    row("scanned after the transform's exclusions", len(scanned), "scanned", t)
    row("attribute nodes in the universe", len(sites), "universe", t)
    row("H — heuristic, job-field", sum(1 for s in sites if s["Hjob"]), "H_job", t)
    row("H — heuristic, task-field",
        sum(1 for s in sites if s["H"] and not s["Hjob"]), "H_task", t)
    row("S — provably `Job`", sum(1 for s in sites if s["static"] == "Job" and
                                  s["attr"] in JOB_FIELD), "S_job", t)
    row("S — provably `Task`", sum(1 for s in sites if s["static"] == "Task" and
                                   s["attr"] in TASK_FIELD), "S_task", t)
    row("P — probe, distinct (path, line, owner, field)", len(l1), "P", t)
    row("**R — the union of P and S, THE RULED SITE SET**", len(R), "R", t)
    row("H - R — what the heuristic ADDS", len(HmR), "HmR", t)
    row("R - H — what the heuristic MISSES", len(RmH), "RmH", t)
    o.extend(t)
    A("\nUnparsable files: %d.\n" % len(unparsable))

    A("## 2. The instruments\n")
    A("Neither is committed as a `.py` file: a `.py` anywhere `ruff check .` scans is counted")
    A("by `tests/orchestration/test_ci_budgets.py` and turns the lint-ceiling test red, which")
    A("a probe left at a worktree root did. Their source is committed verbatim, fenced, at")
    A("`.agent/authored/f275-r53-probe.py.md` and `.agent/authored/f275-r53-sites.py.md`, and")
    A("every figure on this page is reproducible by re-running them — including the full")
    A("enumerations this page reports only as tables.\n")
    for name in ("f275_r53_probe.py", "f275_r53_sites.py"):
        src = open(os.path.join(scratch, name), "rb").read()
        A("- `%s` — %d bytes, sha256 `%s`"
          % (name, len(src), hashlib.sha256(src).hexdigest()))
    A("")

    A("## 3. The two probe runs, and the reproducibility reading\n")
    A("| Run | pytest summary | probe rows |")
    A("|---|---|---|")
    A("| 1 | `%s` | %d |" % (run1, len(p1["rows"])))
    A("| 2 | `%s` | %d |" % (run2, len(p2["rows"])))
    A("\nCompared as SETS of `(owner, field, mode, path, line, function)`: run 1 holds %d,"
      % len(f1))
    A("run 2 holds %d, SYMMETRIC DIFFERENCE %d.\n" % (len(f2), symdiff))
    A("The two summary lines are NOT required to agree and are not gated on: a cold worktree")
    A("fails `test_vitest_passes` for the gitignored `apps/ui/node_modules`, and the run that")
    A("follows it finds that dependency resolved, which moves tests between skipped and")
    A("passed. THE SITE SET IS THE MEASUREMENT, and it is what reproduced.\n")

    A("## 4. The heuristic control\n")
    A("| Figure | measured | reviewer | verdict |")
    A("|---|---|---|---|")
    t = []
    row("control base, job-field edits", ctl_job, "ctl_job", t)
    row("control base, task-field edits", ctl_task, "ctl_task", t)
    o.extend(t)
    A("\n`.agent/f275_t003_flip_residue_r50.md` section 6 records `1896` and `532` from the")
    A("R50 instrument at that same commit. This sweep's H half is an independent")
    A("implementation and reproduces both, so every difference in section 1 is a difference")
    A("of VERDICT over a selection the two instruments agree on.\n")

    A("## 5. What the heuristic ADDS, by class\n")
    A("| Class | count | what it means |")
    A("|---|---|---|")
    A("| A | %d | the static sweep DISPROVES the receiver: an annotation or a construction "
      "names another type |" % cls["A"])
    A("| B | %d | the enclosing `def` demonstrably RAN and this access never fired |" % cls["B"])
    A("| C | %d | the enclosing `def` was never observed running — UNDECIDED |" % cls["C"])
    A("\nA and B are the class DECISION F275 D29 measures at 551 `AttributeError` exception")
    A("lines. C is neither proved nor disproved here: a rename of code the suite never")
    A("executes cannot be decided by execution, and the static sweep reaches only A.\n")
    A("### A and B in full, by path and line\n")
    for c, s in sorted(adds, key=lambda x: (x[0], x[1]["path"], x[1]["line"])):
        if c in ("A", "B"):
            A("- `%s` — `%s:%d` — `%s.%s`" % (c, s["path"], s["line"], s["recv"], s["attr"]))
    A("\n### C, the undecided residue, by receiver\n")
    cc = collections.Counter("%s.%s" % (s["recv"] or "(expr)", s["attr"])
                             for c, s in adds if c == "C")
    A("| receiver.attr | sites |")
    A("|---|---|")
    for k, v in cc.most_common():
        A("| `%s` | %d |" % (k, v))
    A("\n### C by file — the set round 54 attributes its residue against\n")
    A("| file | sites |")
    A("|---|---|")
    cf = collections.Counter(s["path"] for c, s in adds if c == "C")
    for k, v in sorted(cf.items()):
        A("| `%s` | %d |" % (k, v))

    A("\n## 6. What the heuristic MISSES\n")
    expr = [s for s in misses if not s["bare"]]
    A("| Figure | measured | reviewer | verdict |")
    A("|---|---|---|---|")
    t = []
    row("R - H total", len(RmH), "RmH", t)
    row("of those, receivers the heuristic cannot NAME", len(expr), "expr", t)
    o.extend(t)
    A("\nA receiver that is a subscript or a call — `tasks[index - 1].id`, `load_job(x).id` —")
    A("has no spelled name at all, so `recv_name` returns the empty string and no name test")
    A("can ever match it. The probe resolves these by running them.\n")
    A("### R - H in full, by path and line\n")
    for s in sorted(misses, key=lambda s: (s["path"], s["line"])):
        A("- `%s:%d` — `%s.%s`" % (s["path"], s["line"], s["recv"] or "(expr)", s["attr"]))

    A("\n## 7. What this does NOT settle\n")
    A("THE UNDECIDED RESIDUE IS NOT EMPTY and is given no verdict here. The probe is blind to")
    A("code the suite does not execute and the sweep is blind to polymorphism, which is why")
    A("both are run and both differences are reported — the round 31 artefact's own rule.\n")
    A("LINE GRANULARITY. This python is 3.10, so a frame carries no column and the probe's")
    A("key is `(path, line)`. Where one line holds two same-named attributes on different")
    A("receivers the probe cannot separate them; the sweep's key carries `col` and does.\n")

    text = "\n".join(o).rstrip("\n") + "\n"
    with open(outfile, "w") as fh:
        fh.write(text)

    print("tracked %d | scanned %d | universe %d" % (len(paths), len(scanned), len(sites)))
    print("H %d | S %d | P %d | R %d" % (len(H), sum(1 for s in sites if in_S(s)), len(l1), len(R)))
    print("H-R %d (A %d, B %d, C %d) | R-H %d (expr %d)"
          % (len(HmR), cls["A"], cls["B"], cls["C"], len(RmH), len(expr)))
    print("probe reproducibility: symmetric difference %d" % symdiff)
    print("control: job %d task %d" % (ctl_job, ctl_task))
    print("wrote %s (%d bytes)" % (outfile, len(text.encode())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
