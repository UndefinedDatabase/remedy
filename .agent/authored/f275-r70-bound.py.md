# F275 R70 — the static-bound probe for finding `R-0880`, verbatim

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
"""F275 R70 — finding `R-0880`'s FIRST obligation: bound the over-selection STATICALLY.

`R-0880` says the ruled site set rules reads whose RECEIVER is not a job or a task record at
all, and that the flip would rename them inside the one commit this feature cannot split. Its
fix clause binds two things on the round that takes it, and this is the first: bound the class
STATICALLY by reading every ruled site's owner verdict against the LIVE RECORD CLASSES,
"because a dry run can only ever show the sites the suite executes and 12 located frames is a
floor rather than a count".

The method, stated so it can be argued with. A dry run finds sites by EXECUTING them. This
finds them by resolving, for every ruled site, what class the receiver holds — using the
three bindings that carry a class statically and refusing where none of them does:
  (a) an annotated binding in the enclosing scope, `x: Mission = ...` or a parameter
      `def f(x: Mission)`, including the string form;
  (b) a direct construction in the enclosing scope, `x = Mission(...)`;
  (c) a `for x in <name>` whose iterable is itself resolved by (a) or (b) as a list of a
      class, via `list[Mission]` / `List[Mission]`.
Anything else is REFUSED and counted, so the output is a bound with a stated blind spot and
not a claim about every site.

Usage: python3 -B r70_r880.py <repo-root>
"""
import ast
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")

_tracked = []


def subprocess_tracked(root):
    import subprocess
    if not _tracked:
        out = subprocess.run(["git", "ls-files", "*.py"], cwd=str(root),
                             capture_output=True, text=True).stdout
        _tracked.extend(p for p in out.split() if p)
    return _tracked

R = [tuple(x) for x in json.loads((ROOT / ".remedy-wt/r53_R.json").read_text())["R"]]
OWN = {}
for k, v in json.loads((ROOT / ".remedy-wt/r55_owners.json").read_text()).items():
    p, l, c, a = k.rsplit("|", 3)
    OWN[(p, int(l), int(c), a)] = v

# ---- 1. the live record classes, and which of them the flip is FOR ---------------------
JOB_RECORDS = {"Job", "JobPlan"}
TASK_RECORDS = {"Task", "TaskEntry"}
# an annotation that carries NO class identity: resolving a receiver to one of these is a
# refusal, not a finding. `Any` is the one that matters — it is the most common annotation
# on a job parameter in this repository and reading it as a record produced 99 false
# positives on this probe's first run.
NOT_A_RECORD = {"Any", "object", "dict", "Dict", "Mapping", "MutableMapping", "list",
                "List", "Sequence", "Iterable", "Optional", "Union", "str", "int",
                "bool", "float", "None", "NoneType", "Callable", "Tuple", "tuple", "set",
                "Set", "TypeVar", "Self"}

# THE WHOLE REPOSITORY, not only the files holding ruled sites: the records the flip is FOR
# are defined in files the flip EXCLUDES, so scanning only ruled-site files finds none of
# them, which is what this probe's first run did.
classes = {}          # class name -> (path, fields)
for path in subprocess_tracked(ROOT):
    try:
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
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
                classes.setdefault(n.name, (path, fields))

other = {c: v for c, v in classes.items() if c not in JOB_RECORDS | TASK_RECORDS}
print("=== 1. LIVE CLASSES CARRYING id / name / description ===")
print(f"  tracked .py files scanned: {len(subprocess_tracked(ROOT))}")
print(f"  classes found            : {len(classes)}")
print(f"  job or task records      : "
      f"{sorted(set(classes) & (JOB_RECORDS | TASK_RECORDS))}")
print(f"  OTHER records, the risk  : {len(other)}")
print()


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


def scope_bindings(fn):
    """name -> class, for the three binding shapes this method admits."""
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
            it = n.iter
            base = getattr(it, "id", None) or getattr(it, "attr", None)
            if base in out:
                out[n.target.id] = out[base]
    return out


# ---- 2. resolve every ruled site's receiver ---------------------------------------------
verdict = collections.Counter()
rows = []
for path in sorted({k[0] for k in R}):
    try:
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        continue
    scopes = [n for n in ast.walk(tree)
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module))]
    binds = {}
    for s in scopes:
        for name, cls in scope_bindings(s).items():
            lo = getattr(s, "lineno", 0)
            hi = getattr(s, "end_lineno", 10 ** 9) or 10 ** 9
            binds.setdefault((name, lo, hi), cls)
    pos = {(n.lineno, n.col_offset, n.attr): n for n in ast.walk(tree)
           if isinstance(n, ast.Attribute)}
    for key in [k for k in R if k[0] == path]:
        node = pos.get((key[1], key[2], key[3]))
        if node is None:
            verdict["site does not resolve at this tree (R-0879's 54)"] += 1
            continue
        recv = getattr(node.value, "id", None)
        if recv is None:
            verdict["receiver is not a bare name — REFUSED"] += 1
            continue
        cand = [c for (n2, lo, hi), c in binds.items()
                if n2 == recv and lo <= key[1] <= hi]
        if not cand:
            verdict["receiver's class not statically bound — REFUSED"] += 1
            continue
        cls = cand[-1]
        owner = OWN.get(key)
        if cls in NOT_A_RECORD:
            verdict["receiver annotated with no class identity — REFUSED"] += 1
            continue
        if cls not in classes:
            verdict["receiver's class is not a live record class — REFUSED"] += 1
            continue
        if cls in JOB_RECORDS and owner == "Job":
            verdict["agrees: job record, owner Job"] += 1
        elif cls in TASK_RECORDS and owner == "Task":
            verdict["agrees: task record, owner Task"] += 1
        elif cls in JOB_RECORDS | TASK_RECORDS:
            verdict["record is job/task but the owner verdict DISAGREES"] += 1
            rows.append((path, key[1], key[2], key[3], recv, cls, owner))
        else:
            verdict["OVER-SELECTED: receiver is another record entirely"] += 1
            rows.append((path, key[1], key[2], key[3], recv, cls, owner))

print("=== 2. EVERY RULED SITE, AGAINST THE CLASS ITS RECEIVER HOLDS ===")
for k, n in sorted(verdict.items(), key=lambda kv: -kv[1]):
    print(f"  {n:5d}  {k}")
print(f"  {sum(verdict.values()):5d}  TOTAL")
print()

print("=== 3. THE BOUND — SITES WHOSE RECEIVER IS NOT THE RECORD THE OWNER CLAIMS ===")
by_cls = collections.Counter(r[5] for r in rows)
for c, n in by_cls.most_common():
    where = classes.get(c, ("?",))[0]
    print(f"  {n:4d}  {c:28s} defined in {where}")
print(f"  {len(rows):4d}  TOTAL statically confirmed over-selected sites")
print()

print("=== 4. THE FIRST TWENTY, NAMED ===")
for r in sorted(rows)[:20]:
    print(f"    {r[0]}:{r[1]} col {r[2]} .{r[3]}  receiver {r[4]!r} holds {r[5]}"
          f"  owner verdict {r[6]}")
```
