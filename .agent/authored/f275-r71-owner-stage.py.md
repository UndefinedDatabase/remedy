# F275 R71 — the owner-check stage for finding `R-0880`, verbatim

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
"""F275 R71 — the OWNER-CHECK stage. Finding `R-0880`'s second obligation.

`R-0880` asks for two things. The first — bound the over-selection STATICALLY — was measured
at round 70: over 994 tracked files and 71 record classes, 1010 ruled sites agree with a job
owner verdict, 157 with a task one, FOUR are statically confirmed to read a record that is
neither, and 973 are REFUSED by the method because no binding in scope resolves their
receiver. This is the second: give the run a refusal for a site whose owner verdict cannot be
confirmed against the receiver's own record.

THE REACH OF THIS GUARD EQUALS THE REACH OF THAT METHOD, AND THAT IS STATED RATHER THAN
HIDDEN. It fires on what the static pass CONFIRMS wrong and is silent on what the static pass
REFUSES to decide. Making it fire on the refusals instead would stop every run it is ever
given — a guard that cannot pass, which is the same defect as a guard that cannot fail, and
item 33 of `docs/agents/planner_reviewer_prompt.md` §3 names both. So the honest design is a
guard with a stated blind spot and a printed count of it, not a stricter one that is unusable.

It sits beside the re-key stage: that one refuses to EMIT a set whose keys have gone stale,
this one refuses to emit a set whose OWNER VERDICTS are contradicted by the code. Neither
edits anything. Exit 0 means the set may be consumed; exit 5 means it may not.

Usage: python3 -B <this file> <worktree> <ruled.json> <owners.json> [--report-only]
"""
import ast
import collections
import json
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1])
RULED_JSON, OWNERS_JSON = sys.argv[2], sys.argv[3]
REPORT_ONLY = "--report-only" in sys.argv[4:]

JOB_RECORDS = {"Job", "JobPlan"}
TASK_RECORDS = {"Task", "TaskEntry"}
NOT_A_RECORD = {"Any", "object", "dict", "Dict", "Mapping", "MutableMapping", "list",
                "List", "Sequence", "Iterable", "Optional", "Union", "str", "int",
                "bool", "float", "None", "NoneType", "Callable", "Tuple", "tuple", "set",
                "Set", "TypeVar", "Self"}

R = [tuple(x) for x in json.load(open(RULED_JSON))["R"]]
OWN = {}
for k, v in json.load(open(OWNERS_JSON)).items():
    p, l, c, a = k.rsplit("|", 3)
    OWN[(p, int(l), int(c), a)] = v


def tracked():
    out = subprocess.run(["git", "ls-files", "*.py"], capture_output=True, text=True,
                         cwd=str(WT)).stdout
    return [p for p in out.split() if p]


def annotation_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.strip("'\" ")
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Subscript):
        return annotation_name(node.slice)
    return None


# the live record classes, over the WHOLE tree: the records the flip is for are defined in
# files the flip excludes, so scanning only the ruled-site files finds none of them.
classes = {}
for path in tracked():
    try:
        tree = ast.parse((WT / path).read_text(encoding="utf-8"))
    except (SyntaxError, OSError, UnicodeDecodeError):
        continue
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            fields = set()
            for st in n.body:
                if isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name):
                    fields.add(st.target.id)
                elif isinstance(st, ast.Assign):
                    for t in st.targets:
                        if isinstance(t, ast.Name):
                            fields.add(t.id)
            if fields & {"id", "name", "description"}:
                classes.setdefault(n.name, path)


def scope_bindings(fn):
    out = {}
    args = getattr(fn, "args", None)
    if args:
        for a in list(args.args) + list(args.kwonlyargs) + list(args.posonlyargs):
            if a.annotation is not None:
                c = annotation_name(a.annotation)
                if c:
                    out[a.arg] = c
    for n in ast.walk(fn):
        if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            c = annotation_name(n.annotation)
            if c:
                out[n.target.id] = c
        elif isinstance(n, ast.Assign) and isinstance(n.value, ast.Call):
            f = n.value.func
            c = getattr(f, "id", None) or getattr(f, "attr", None)
            if c in classes:
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        out[t.id] = c
        elif isinstance(n, ast.For) and isinstance(n.target, ast.Name):
            base = getattr(n.iter, "id", None) or getattr(n.iter, "attr", None)
            if base in out:
                out[n.target.id] = out[base]
    return out


verdict = collections.Counter()
contradicted = []
for path in sorted({k[0] for k in R}):
    try:
        tree = ast.parse((WT / path).read_text(encoding="utf-8"))
    except (SyntaxError, OSError, UnicodeDecodeError):
        verdict["file unreadable at this tree"] += len([k for k in R if k[0] == path])
        continue
    binds = {}
    for s in [n for n in ast.walk(tree)
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module))]:
        lo = getattr(s, "lineno", 0)
        hi = getattr(s, "end_lineno", 10 ** 9) or 10 ** 9
        for name, cls in scope_bindings(s).items():
            binds.setdefault((name, lo, hi), cls)
    pos = {(n.lineno, n.col_offset, n.attr): n for n in ast.walk(tree)
           if isinstance(n, ast.Attribute)}
    for key in [k for k in R if k[0] == path]:
        node = pos.get((key[1], key[2], key[3]))
        if node is None:
            verdict["site does not resolve at this tree (R-0879's guard owns this)"] += 1
            continue
        recv = getattr(node.value, "id", None)
        if recv is None:
            verdict["REFUSED to decide: receiver is not a bare name"] += 1
            continue
        cand = [c for (n2, lo, hi), c in binds.items() if n2 == recv and lo <= key[1] <= hi]
        if not cand:
            verdict["REFUSED to decide: receiver's class not statically bound"] += 1
            continue
        cls = cand[-1]
        if cls in NOT_A_RECORD:
            verdict["REFUSED to decide: annotation carries no class identity"] += 1
            continue
        if cls not in classes:
            verdict["REFUSED to decide: class is not a live record class"] += 1
            continue
        owner = OWN.get(key)
        if (cls in JOB_RECORDS and owner == "Job") or (cls in TASK_RECORDS
                                                       and owner == "Task"):
            verdict["CONFIRMED: the owner verdict matches the receiver's record"] += 1
        else:
            verdict["CONTRADICTED: the receiver holds another record entirely"] += 1
            contradicted.append((key[0], key[1], key[2], key[3], recv, cls, owner))

decided = (verdict["CONFIRMED: the owner verdict matches the receiver's record"]
           + len(contradicted))
refused = sum(v for k, v in verdict.items() if k.startswith("REFUSED"))
print(f"ruled sites                 : {len(R)}")
print(f"live record classes         : {len(classes)}")
for k, n in sorted(verdict.items(), key=lambda kv: -kv[1]):
    print(f"  {n:5d}  {k}")
print(f"DECIDED                     : {decided}")
print(f"REFUSED, the stated blind spot: {refused}")
print(f"CONTRADICTED                : {len(contradicted)}")

if contradicted:
    print("")
    print("THE OWNER CHECK REFUSES. These ruled sites name an owner the code contradicts, "
          "and the flip is one commit that cannot be split, so a wrong rename inside it "
          "has no cheap second chance. Finding R-0880.")
    for c, n in collections.Counter(r[5] for r in contradicted).most_common():
        print(f"   {n:>4}  {c}  defined in {classes.get(c, '?')}")
    for row in sorted(contradicted):
        print(f"        {row[0]}:{row[1]} col {row[2]} .{row[3]}  receiver {row[4]!r} "
              f"holds {row[5]}  owner verdict {row[6]}")
    if not REPORT_ONLY:
        sys.exit(5)
```
