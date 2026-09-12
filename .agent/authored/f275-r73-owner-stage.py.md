# F275 R73 — the owner-check stage, third edition, verbatim

> Saved as `.md` and not as `.py` on purpose: a `.py` file anywhere `ruff check .`
> scans is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this
> round's tree gate reads. The gate extracts the single fence below into
> `.remedy-wt/` and runs it there, which is outside the tree.
>
> This carrier was GENERATED from its source by the same script that verified the
> extraction round-trips back to that source, in one step. Round 69 landed a carrier
> generated before its source was edited and never regenerated; that is the defect
> this procedure exists to make unreachable.

```python
"""F275 R73 — the OWNER-CHECK stage, third edition: RULE H reaches receiver EXPRESSIONS.

WHAT THIS EDITION ADDS, and it is deliberately the last of its kind. Rules A through G below
all resolve a NAME; the stage then refused outright any receiver that was not a bare name,
which left `job.tasks[0].id`, `result.job.id` and `load_job(...).id` in the blind spot as a
CLASS rather than as a difficulty. RULE H walks the receiver expression instead of demanding
it be a name, refusing on ambiguity like every rule before it and bounding its own recursion.

IT BUYS 47 CONFIRMATIONS AND NOT ONE NEW CONTRADICTION, which is the reading the round that
shipped it cares about: further resolver work is past the point where it finds defects, so
DECISION F275 D45's remaining route is to RULE the residual rather than to chase it. The
figures are in this round's artefact and its instrument re-derives them.

The rest of this docstring is round 72's and is unchanged, because the rules it describes are.

--- the OWNER-CHECK stage, second edition: the same guard with a smaller blind spot.

DECISION F275 D45 made the refusal set a PRECONDITION on the flip round: the flip may
not be taken until that set has been shrunk or the residual ruled acceptable on the
record. This file is the shrink. The guard's CONTRACT is unchanged — exit 0 means the
ruled set may be consumed, exit 5 means it may not, and a site the code CONTRADICTS
stops the run and is named. What changes is only how many receivers the static pass can
resolve, and therefore how much of the ruled set the guard can see.

SIX RESOLUTION RULES ARE ADDED TO THE R71 METHOD AND EVERY ONE OF THEM REFUSES ON
AMBIGUITY. That is the design constraint, not an implementation detail: a resolver that
guesses turns a silent blind spot into a confident wrong answer, which is strictly worse,
because the blind spot is counted and printed on every run while a wrong answer is not.
Wherever a rule can yield two different live record classes for one name it yields
NOTHING and the site stays in the refusal set.

  A  CROSS-FILE RETURN TYPES. A function whose return annotation resolves to a live
     record class binds its callers' targets. The table is keyed by function NAME across
     the whole tree, because that is how an import reaches a call site, and any name that
     two files annotate with two different record classes is dropped from the table.
  B  EVERY-RETURN-IS-ONE-CONSTRUCTOR. A function with no return annotation whose every
     `return` statement returns `Cls(...)` for a single live record class binds by that
     class. A function with no returns, or with two, is not in the table.
  C  FIELD ELEMENT TYPES. `for t in job.tasks` binds `t` when `job` is already bound to a
     class whose own `tasks` field is annotated `list[Task]`. The field is resolved on the
     RECEIVER'S OWN class and never by field name globally — `Job.tasks`, `_FakeJob.tasks`
     and `Case.tasks` are three different fields that share a spelling.
  D  WIDER ANNOTATIONS. PEP 604 unions (`Job | None`) and mapping subscripts
     (`dict[str, Job]`) carry a class identity the R71 reader dropped. A union naming two
     live record classes resolves to neither.
  E  `with ... as x` AND THE WALRUS. Both are assignments the R71 reader did not visit.
  F  ALIASES. `y = x` binds `y` to whatever `x` holds in the same scope, computed to a
     fixed point so a chain of aliases resolves.
  G  FILE-WIDE AGREEMENT, and only where it is unanimous. Where no enclosing scope binds a
     receiver, but EVERY scope in the file that binds that name binds it to the SAME live
     record class, the site resolves to that class. This is the one rule that reaches
     across scopes, and the unanimity requirement is what makes it a rule rather than the
     leak described below: a test file that writes `job = _make_job()` in thirty methods
     says the same thing thirty times, while the file that produced this round's worst
     false positive binds `t` to two different records in two functions and is therefore
     refused. Without this rule the scoping repair below costs 327 sites the R71 reader
     decided correctly; with it that cost is paid only where the file itself disagrees.

AND ONE SCOPING REPAIR THE RULES ABOVE MAKE LOAD-BEARING. A scope that walks its nested
definitions republishes their locals as its own, and because a module's span covers every
line of its file, such a binding then answers for a name in an unrelated function. The R71
reader has that leak and is saved from it only by binding too little for it to matter;
these rules bind enough that it would produce WRONG answers rather than none. So a scope
walks its own body only, and a name is answered by the innermost scope that really binds it.

THE BLIND SPOT IS STILL PRINTED AS A COUNT ON EVERY RUN, for the reason D45 gives: a
guard whose reach is smaller than its subject must say so where it is used and not only
where it was ruled. Shrinking the residual does not retire that obligation.

`--narrow` RESTORES THE R71 READER EXACTLY, and exists so the widening can be gated rather
than asserted. The instrument runs this file in both modes, proves the narrow mode
reproduces the committed R71 stage's own banner class for class, and then diffs the two
PER-SITE decision maps `--dump` writes. Without that flag the comparison would rest on two
banners of counts, which cannot tell a site that changed its mind from two sites that
swapped.

Usage: python3 -B <this file> <worktree> <ruled.json> <owners.json>
                 [--report-only] [--narrow] [--dump <path>]
"""
import ast
import collections
import json
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1])
RULED_JSON, OWNERS_JSON = sys.argv[2], sys.argv[3]
FLAGS = sys.argv[4:]
REPORT_ONLY = "--report-only" in FLAGS
NARROW = "--narrow" in FLAGS
DUMP = FLAGS[FLAGS.index("--dump") + 1] if "--dump" in FLAGS else None

JOB_RECORDS = {"Job", "JobPlan"}
TASK_RECORDS = {"Task", "TaskEntry"}
NOT_A_RECORD = {"Any", "object", "dict", "Dict", "Mapping", "MutableMapping", "list",
                "List", "Sequence", "Iterable", "Optional", "Union", "str", "int",
                "bool", "float", "None", "NoneType", "Callable", "Tuple", "tuple", "set",
                "Set", "TypeVar", "Self"}
ELEMENT_CONTAINERS = {"list", "List", "Sequence", "Iterable", "set", "Set", "frozenset",
                      "tuple", "Tuple", "Collection", "MutableSequence"}

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
    """The class identity an annotation carries, or None.

    RULE D widens the R71 reader in two places and both refuse on ambiguity: a PEP 604
    union drops its None arm and resolves only if ONE arm is left with a name, and a
    subscript with a tuple slice reads the LAST element, which is the value type of every
    mapping spelling in this repository. Under `--narrow` neither widening is applied.
    """
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.strip("'\" ")
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Subscript):
        sl = node.slice
        if isinstance(sl, ast.Tuple):
            if NARROW:
                return None
            return annotation_name(sl.elts[-1]) if sl.elts else None
        return annotation_name(sl)
    if not NARROW and isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        arms = [annotation_name(node.left), annotation_name(node.right)]
        arms = [a for a in arms if a is not None and a != "None"]
        return arms[0] if len(arms) == 1 else None
    return None


def element_name(node):
    """The ELEMENT class of a container annotation — `list[Task]` gives `Task`."""
    if isinstance(node, ast.Subscript):
        base = getattr(node.value, "id", None) or getattr(node.value, "attr", None)
        if base in ELEMENT_CONTAINERS:
            sl = node.slice
            if isinstance(sl, ast.Tuple):
                names = {annotation_name(e) for e in sl.elts}
                names.discard(None)
                return names.pop() if len(names) == 1 else None
            return annotation_name(sl)
    return None


TREES = {}
for path in tracked():
    try:
        TREES[path] = ast.parse((WT / path).read_text(encoding="utf-8"))
    except (SyntaxError, OSError, UnicodeDecodeError):
        continue

# the live record classes, over the WHOLE tree: the records the flip is for are defined in
# files the flip excludes, so scanning only the ruled-site files finds none of them.
classes = {}
class_fields = {}
for path, tree in TREES.items():
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            fields = {}
            for st in n.body:
                if isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name):
                    fields[st.target.id] = st.annotation
                elif isinstance(st, ast.Assign):
                    for t in st.targets:
                        if isinstance(t, ast.Name):
                            fields.setdefault(t.id, None)
            if set(fields) & {"id", "name", "description"}:
                classes.setdefault(n.name, path)
                class_fields.setdefault(n.name, fields)


def returns_of(fn):
    """The returned expressions of a function, not descending into nested definitions."""
    out, stack = [], list(fn.body)
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(n, ast.Return) and n.value is not None:
            out.append(n.value)
        stack.extend(ast.iter_child_nodes(n))
    return out


# --- RULES A and B: the function-return table, keyed by name, ambiguity dropped ---
_ret = collections.defaultdict(set)
if not NARROW:
    for path, tree in TREES.items():
        for n in ast.walk(tree):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            cls = annotation_name(n.returns) if n.returns is not None else None
            if cls in classes:                                      # RULE A
                _ret[n.name].add(cls)
                continue
            if n.returns is not None:
                continue
            ctors, ok = set(), True                                 # RULE B
            rs = returns_of(n)
            if not rs:
                continue
            for r in rs:
                c = None
                if isinstance(r, ast.Call):
                    c = getattr(r.func, "id", None) or getattr(r.func, "attr", None)
                if c in classes:
                    ctors.add(c)
                else:
                    ok = False
            if ok and len(ctors) == 1:
                _ret[n.name].add(ctors.pop())

RETURNS = {k: next(iter(v)) for k, v in _ret.items() if len(v) == 1}
AMBIGUOUS = {k for k, v in _ret.items() if len(v) > 1}


def called_name(value):
    """The callee name of a call expression, seeing through `await`."""
    if not NARROW and isinstance(value, ast.Await):
        value = value.value
    if isinstance(value, ast.Call):
        f = value.func
        return getattr(f, "id", None) or getattr(f, "attr", None)
    return None


def value_class(value, out):
    """The record class an expression yields, under the rules, or None."""
    name = called_name(value)
    if name is not None:
        if name in classes:
            return name
        if NARROW:
            return None
        if name in AMBIGUOUS:
            return None
        return RETURNS.get(name)
    if not NARROW and isinstance(value, ast.Name):                  # RULE F
        return out.get(value.id)
    return None


def iter_element_class(it, out):
    """The element class of an iterable expression — RULE C."""
    if isinstance(it, ast.Attribute):
        base = getattr(it.value, "id", None)
        owner = out.get(base) if base else None
        ann = class_fields.get(owner, {}).get(it.attr) if owner else None
        return element_name(ann) if ann is not None else None
    return None


def own_nodes(scope):
    """Every node of a scope's own body, NOT descending into a nested definition."""
    out, stack = [], list(getattr(scope, "body", []))
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        out.append(n)
        stack.extend(ast.iter_child_nodes(n))
    return out


def scope_bindings(fn):
    out = {}
    args = getattr(fn, "args", None)
    if args:
        for a in list(args.args) + list(args.kwonlyargs) + list(args.posonlyargs):
            if a.annotation is not None:
                c = annotation_name(a.annotation)
                if c:
                    out[a.arg] = c
    if NARROW:
        # the R71 reader exactly: one pass, walking nested definitions, `for` only, and
        # an iterable resolved by `.id` OR `.attr` against names already bound.
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
    body = own_nodes(fn)
    # passes to a fixed point, so an alias or a field iteration that reads a binding made
    # later in the same scope still resolves; each pass adds only bindings the one before
    # made available, and the loop stops as soon as a pass changes nothing.
    for _ in range(3):
        before = dict(out)
        for n in body:
            if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
                c = annotation_name(n.annotation)
                if c:
                    out[n.target.id] = c
            elif isinstance(n, ast.Assign):
                c = value_class(n.value, out)
                if c:
                    for t in n.targets:
                        if isinstance(t, ast.Name):
                            out[t.id] = c
            elif isinstance(n, ast.NamedExpr) and isinstance(n.target, ast.Name):
                c = value_class(n.value, out)                       # RULE E
                if c:
                    out[n.target.id] = c
            elif isinstance(n, (ast.With, ast.AsyncWith)):
                for item in n.items:                                # RULE E
                    v = item.optional_vars
                    if isinstance(v, ast.Name):
                        c = value_class(item.context_expr, out)
                        if c:
                            out[v.id] = c
            elif isinstance(n, (ast.For, ast.AsyncFor, ast.comprehension)):
                if isinstance(n.target, ast.Name):
                    base = getattr(n.iter, "id", None)
                    if base in out:
                        out[n.target.id] = out[base]
                    else:
                        c = iter_element_class(n.iter, out)          # RULE C
                        if c:
                            out[n.target.id] = c
        if out == before:
            break
    return out


verdict = collections.Counter()
contradicted = []
decisions = {}
for path in sorted({k[0] for k in R}):
    tree = TREES.get(path)
    if tree is None:
        verdict["file unreadable at this tree"] += len([k for k in R if k[0] == path])
        continue
    binds = {}
    for s in [n for n in ast.walk(tree)
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module))]:
        lo = getattr(s, "lineno", 0)
        hi = getattr(s, "end_lineno", 10 ** 9) or 10 ** 9
        for name, cls in scope_bindings(s).items():
            binds.setdefault((name, lo, hi), cls)
    # RULE G: a name every binding scope in this file agrees about. Disagreement — the
    # same name standing for two records in two functions — yields nothing.
    agree = {}
    if not NARROW:
        per_name = collections.defaultdict(set)
        for (name, _lo, _hi), cls in binds.items():
            per_name[name].add(cls)
        agree = {n: next(iter(v)) for n, v in per_name.items() if len(v) == 1}
    # RULE H needs the RAW annotation, not the class name it reduces to, because
    # `list[Task]` and `Task` reduce alike and only the first can be subscripted.
    binds_ann = {}
    if not NARROW:
        for s in [n for n in ast.walk(tree)
                  if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module))]:
            lo = getattr(s, "lineno", 0)
            hi = getattr(s, "end_lineno", 10 ** 9) or 10 ** 9
            for n in own_nodes(s):
                if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
                    binds_ann.setdefault((n.target.id, lo, hi), n.annotation)
            args = getattr(s, "args", None)
            if args:
                for a in (list(args.args) + list(args.kwonlyargs)
                          + list(args.posonlyargs)):
                    if a.annotation is not None:
                        binds_ann.setdefault((a.arg, lo, hi), a.annotation)
    pos = {(n.lineno, n.col_offset, n.attr): n for n in ast.walk(tree)
           if isinstance(n, ast.Attribute)}
    for key in [k for k in R if k[0] == path]:
        node = pos.get((key[1], key[2], key[3]))
        if node is None:
            verdict["site does not resolve at this tree (R-0879's guard owns this)"] += 1
            continue
        def name_class(nm):
            c = [x for (n2, lo, hi), x in binds.items()
                 if n2 == nm and lo <= key[1] <= hi]
            if not c and nm in agree:
                c = [agree[nm]]                                     # RULE G
            return c[-1] if c else None

        def expr_class(e, depth=0):
            """RULE H — the class a RECEIVER EXPRESSION yields, or None.

            The R72 reader resolved only a bare name and refused every other receiver
            shape outright, which left `job.tasks[0].id`, `result.job.id` and
            `load_job(...).id` in the blind spot as a class rather than as a difficulty.
            Each of those shapes is one step away from something already resolvable, so
            this rule walks the receiver expression instead of demanding it be a name.
            It refuses on ambiguity like every rule before it, and it bounds its own
            recursion: an expression nested deeper than a handful of steps is refused
            rather than explored, because a resolver that never gives up is a resolver
            whose wrong answers are unbounded too.
            """
            if depth > 4:
                return None
            if isinstance(e, ast.Name):
                return name_class(e.id)
            if isinstance(e, ast.Attribute):
                owner = expr_class(e.value, depth + 1)
                if owner is None:
                    return None
                ann = class_fields.get(owner, {}).get(e.attr)
                return annotation_name(ann) if ann is not None else None
            if isinstance(e, ast.Subscript):
                base = expr_class_container(e.value, depth + 1)
                return base
            if isinstance(e, (ast.Call, ast.Await)):
                nm = called_name(e)
                if nm is None:
                    return None
                if nm in classes:
                    return nm
                if nm in AMBIGUOUS:
                    return None
                return RETURNS.get(nm)
            return None

        def expr_class_container(e, depth=0):
            """The ELEMENT class of an expression that denotes a container."""
            if depth > 4:
                return None
            if isinstance(e, ast.Name):
                c = [x for (n2, lo, hi), x in binds_ann.items()
                     if n2 == e.id and lo <= key[1] <= hi]
                return element_name(c[-1]) if c else None
            if isinstance(e, ast.Attribute):
                owner = expr_class(e.value, depth + 1)
                if owner is None:
                    return None
                ann = class_fields.get(owner, {}).get(e.attr)
                return element_name(ann) if ann is not None else None
            return None

        if NARROW:
            recv = getattr(node.value, "id", None)
            if recv is None:
                verdict["REFUSED to decide: receiver is not a bare name"] += 1
                continue
            cls = name_class(recv)
            if cls is None:
                verdict["REFUSED to decide: receiver's class not statically bound"] += 1
                continue
        else:
            recv = ast.unparse(node.value)
            cls = expr_class(node.value)
            if cls is None:
                if isinstance(node.value, ast.Name):
                    verdict["REFUSED to decide: receiver's class not statically bound"] += 1
                else:
                    verdict["REFUSED to decide: receiver expression does not resolve"] += 1
                continue
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
            decisions["|".join(str(x) for x in key)] = ["CONFIRMED", cls, owner]
        else:
            verdict["CONTRADICTED: the receiver holds another record entirely"] += 1
            contradicted.append((key[0], key[1], key[2], key[3], recv, cls, owner))
            decisions["|".join(str(x) for x in key)] = ["CONTRADICTED", cls, owner]

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

if DUMP:
    pathlib.Path(DUMP).write_text(json.dumps(decisions, sort_keys=True), encoding="utf-8")

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
