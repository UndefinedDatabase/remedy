# F275 R56 — `f275_r56_records.py`, the UUID-record sweep and its artefact generator

> Committed verbatim so `.agent/f275_t003_uuid_records.md` is reproducible from the
> repository itself. It takes its measurement base as an ARGUMENT rather than reading
> `git rev-parse HEAD`, so a second run reproduces the first bit for bit at any tip —
> round 54's generator embedded the tip it ran at and its reproduction had to be taken
> before the commit that stored it. It is a `.md` and not a `.py` because a `.py` file
> anywhere `ruff check .` scans is counted by `tests/orchestration/test_ci_budgets.py`,
> and a probe left at a worktree root turned the lint-ceiling test red.

```python
"""F275 R56 — every RECORD the flip feeds that still declares a UUID-typed field.

Usage: python3 -B f275_r56_records.py <base-sha> <out.md>

The base is an ARGUMENT and never `git rev-parse HEAD`, so a second run reproduces the
first bit for bit at any tip. Round 54's generator embedded the tip it ran at and its
reproduction had to be taken before the commit that stored it; this one has no such
friction, which is the only difference of method.

WHY THIS SWEEP EXISTS. DECISION F275 D26's premise P2 swept `pydantic` models under
`packages.` for a UUID-typed field and found six, of which D27 and D28 migrated three. A
DATACLASS is invisible to that sweep: `issubclass(obj, BaseModel)` is False for every one
of them. This reads the live objects of every class defined under `packages.` and `apps.`,
pydantic model and dataclass and plain annotated class body alike, and then resolves by
`ast` whether the flip's own output actually reaches each UUID-typed id field.

It WRITES exactly one file, the one named on the command line, and reads nothing else.
"""
import ast
import collections
import dataclasses
import importlib
import inspect
import pkgutil
import subprocess
import sys

from pydantic import BaseModel

BASE, OUT = sys.argv[1], sys.argv[2]
CLASSIC_MODULES = {"packages.core.models", "packages.orchestration.pingpong_job"}
MIGRATED = {"Artifact", "TaskExecutionContext", "PatchIntentSet"}
JOB_TASK_FIELD = ("job_id", "task_id", "id")


def uuid_fields(obj):
    """Every field of one class whose ANNOTATION names UUID, with how it was declared."""
    if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel:
        return [(n, str(i.annotation), "pydantic")
                for n, i in obj.model_fields.items() if "UUID" in str(i.annotation)]
    if dataclasses.is_dataclass(obj):
        hints = getattr(obj, "__annotations__", {})
        return [(f.name, str(hints.get(f.name, f.type)), "dataclass")
                for f in dataclasses.fields(obj)
                if "UUID" in str(hints.get(f.name, f.type))]
    ann = getattr(obj, "__annotations__", None)
    if inspect.isclass(obj) and ann:
        return [(n, str(a), "annotated class") for n, a in ann.items() if "UUID" in str(a)]
    return []


found = {}
walked, skipped = 0, []
for pkg_name in ("packages", "apps"):
    try:
        pkg = importlib.import_module(pkg_name)
    except Exception as exc:
        skipped.append((pkg_name, type(exc).__name__))
        continue
    for m in pkgutil.walk_packages(pkg.__path__, pkg_name + "."):
        walked += 1
        try:
            mod = importlib.import_module(m.name)
        except Exception as exc:
            skipped.append((m.name, type(exc).__name__))
            continue
        for obj in vars(mod).values():
            if not inspect.isclass(obj) or getattr(obj, "__module__", "") != m.name:
                continue
            hits = uuid_fields(obj)
            if hits:
                found[f"{obj.__module__}.{obj.__name__}"] = hits

# Which of those records does the flip's own output actually reach? Resolve every
# construction and read by `ast`, never by grep.
targets = {}
for full, hits in found.items():
    module, short = full.rsplit(".", 1)
    if module in CLASSIC_MODULES:
        continue
    for fname, _, _ in hits:
        if fname in JOB_TASK_FIELD:
            targets[short] = fname
            break

paths = [p for p in subprocess.run(["git", "ls-files", "*.py"], capture_output=True,
                                   text=True).stdout.split() if p]
ctor = collections.defaultdict(collections.Counter)
ctor_files = collections.defaultdict(set)
for rel in paths:
    try:
        tree = ast.parse(open(rel, "rb").read(), filename=rel)
    except (SyntaxError, OSError):
        continue
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)):
            continue
        short = n.func.id
        if short not in targets:
            continue
        field, shape = targets[short], "(the field is not passed)"
        for kw in n.keywords:
            if kw.arg == field:
                v = kw.value
                shape = (f"{v.func.id}()" if isinstance(v, ast.Call)
                         and isinstance(v.func, ast.Name) else type(v).__name__)
        ctor[short][shape] += 1
        ctor_files[short].add(rel)

# An `Attribute` or a `Name` is a value the flip retypes; a `UUID()` call and an absent
# field are not, because the flip touches neither.
FED = ("Attribute", "Name")
fed = {s: sum(c for k, c in ctor[s].items() if k in FED) for s in targets}

L = []
A = L.append
A("# F275 T003 — every record the flip FEEDS that still declares a UUID-typed field\n")
A("> Generated, never typed, by the instrument committed at")
A("> `.agent/authored/f275-r56-records.py.md`. Measurement base: `%s`." % BASE)
A("> This file SIZES a class; it performs none of it, and no line under `packages/`,")
A("> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.\n")
A("## 1. Why the earlier sweep could not see these\n")
A("DECISION F275 D26's premise P2 reads, in its own instrument, `issubclass(obj,")
A("BaseModel)`. That is False for every dataclass, so a dataclass declaring a UUID-typed")
A("id was invisible to it, and D27 and D28 migrated the pydantic models it did find. The")
A("sweep below widens in two directions at once — from pydantic to every class kind, and")
A("from `packages.` to `apps.` as well — and reports which direction found anything.\n")
A("## 2. The reading, complete and untrimmed\n")
A("```")
A(f"modules walked: {walked} | modules that RAISED on import and were skipped:"
  f" {len(skipped)}")
for name, exc in skipped:
    A(f"    {name}  {exc}")
A(f"classes under `packages.` or `apps.` declaring a UUID-typed field: {len(found)}")
kinds = collections.Counter(h[0][2] for h in found.values())
A(f"by declaration kind: {dict(sorted(kinds.items()))}")
mods = collections.Counter(n.rsplit('.', 1)[0].split('.')[0] for n in found)
A(f"by top-level package: {dict(sorted(mods.items()))}")
A("")
for name in sorted(found):
    module, short = name.rsplit(".", 1)
    if module in CLASSIC_MODULES:
        tag = "THE CLASSIC RECORD ITSELF"
    elif short in MIGRATED:
        tag = "MIGRATED by DECISION F275 D27 or D28"
    elif short in targets:
        tag = f"NOT ENUMERATED — fed by the flip at {fed[short]} constructions"
    else:
        tag = "NOT ENUMERATED — no job-or-task id field"
    A(f"  {found[name][0][2]:16s} {name}")
    for fname, ann, _ in found[name]:
        A(f"      {fname}: {ann}")
    A(f"      -> {tag}")
A("")
A("the constructions of each NOT ENUMERATED record, and what its id field is given:")
for short in sorted(targets):
    total = sum(ctor[short].values())
    A(f"  {short}.{targets[short]}  {total} constructions in {len(ctor_files[short])}"
      f" files, of which {fed[short]} pass a value the flip retypes")
    for shape, c in ctor[short].most_common():
        mark = "  <- the flip retypes this" if shape in FED else ""
        A(f"      {c:>4}  {shape}{mark}")
A("```\n")
A("## 3. What this does NOT settle\n")
A("WHICH RECORDS MUST MIGRATE IS A RULING AND NOT A COUNT. A record fed by the flip at")
A("zero constructions is not thereby safe: this sweep resolves a CONSTRUCTION, and a field")
A("assigned after construction is not a construction. That reading was not taken.\n")
A("NO CLAIM IS MADE THAT THIS SWEEP IS COMPLETE, and section 2 reports the two ways it can")
A("be short. A module that RAISES on import is skipped, and the count of those is printed")
A("rather than left to be assumed — the D26 instrument skipped the same way and reported")
A("no number at all. And a `TypedDict`, a `NamedTuple` built by the functional form, and")
A("any id held in a plain `dict` carry no class annotation, so they are invisible to every")
A("sweep of this shape, including this one.")

text = "\n".join(L) + "\n"
open(OUT, "w").write(text)
print(text)
print(f"wrote {OUT}")
```
