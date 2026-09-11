# F275 R55 — `f275_r55_instrument.py`, the readings that decide the flip's residue

> Committed verbatim so `.agent/f275_t003_flip_residue_r55.md` is reproducible from the
> repository itself, in the part of it that IS reproducible: the two suite runs that
> artefact records are not, and its section 8 says exactly which figures this instrument
> does and does not reach. It is a `.md` and not a `.py` because a `.py` file anywhere
> `ruff check .` scans is counted by `tests/orchestration/test_ci_budgets.py`, and a probe
> left at a worktree root turned the lint-ceiling test red — measured, not feared.

```python
"""F275 R55 — the readings that DECIDE the flip's residue, re-measured in one run.

The two suite runs the artefact records are not reproducible inside a round. These are:
the field-type disagreement between the two records, read by IMPORTING the shipped classes;
the binding shapes that feed a `**` splat into a target constructor, resolved by `ast` over
the files `git ls-files '*.py'` names; and the two fields the residue names. This probe
WRITES NOTHING and takes no reading from a source file's text.
"""
import ast
import collections
import dataclasses
import subprocess

from packages.core.models import Job, Task
from packages.orchestration.pingpong_job import JobPlan, TaskEntry

jp = {f.name: str(f.type) for f in dataclasses.fields(JobPlan)}
te = {f.name: str(f.type) for f in dataclasses.fields(TaskEntry)}
print("A. the two records, field by field, by IMPORTING them:")
for label, classic, cfield, unified, ufield in (
        ("job id", Job, "id", jp, "job_id"),
        ("task id", Task, "id", te, "task_id"),
        ("task status", Task, "status", te, "status"),
        ("created at", Job, "created_at", jp, "created_at"),
        ("job state", Job, "state", jp, "state")):
    a = classic.model_fields[cfield].annotation
    print(f"   {label:12s} classic {str(a):28s} unified {unified.get(ufield)}")
print(f"   JobPlan is a dataclass: {dataclasses.is_dataclass(JobPlan)}"
      f" | Job is a pydantic model: {hasattr(Job, 'model_dump')}")
for name in ("model_dump", "model_dump_json", "model_copy"):
    print(f"   JobPlan.{name:16s} exists: {hasattr(JobPlan, name)}")
print(f"   TaskEntry declares acceptance_checks: {'acceptance_checks' in te}")

CTOR = {"Job", "Task"}
CLASSIC = {"name", "id", "description", "type", "task_type", "permissions"}
paths = [p for p in subprocess.run(["git", "ls-files", "*.py"], capture_output=True,
                                   text=True).stdout.split() if p]
shapes, keys, inline, unbound = collections.Counter(), collections.Counter(), 0, 0
for rel in paths:
    try:
        tree = ast.parse(open(rel, "rb").read(), filename=rel)
    except (SyntaxError, OSError):
        continue
    splatted = {}
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id in CTOR):
            continue
        for kw in n.keywords:
            if kw.arg is not None:
                continue
            if isinstance(kw.value, ast.Name):
                splatted[kw.value.id] = n.func.id
            elif isinstance(kw.value, ast.Dict):
                inline += 1
    if not splatted:
        continue
    bound = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(
                n.targets[0], ast.Name):
            name, value = n.targets[0].id, n.value
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            name, value = n.target.id, n.value
        else:
            continue
        if name not in splatted or value is None:
            continue
        bound.add(name)
        kind = type(value).__name__
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
            kind = f"{value.func.id}(...)"
        shapes[f"{type(n).__name__} -> {kind}"] += 1
        items = (value.keys if isinstance(value, ast.Dict)
                 else [k for k in getattr(value, "keywords", [])])
        for item in items:
            k = item.value if isinstance(item, ast.Constant) else getattr(item, "arg", None)
            if isinstance(k, str) and k in CLASSIC:
                keys[f"{splatted[name]}.{k}"] += 1
    unbound += len([n for n in splatted if n not in bound])

print(f"\nB. tracked .py from git ls-files: {len(paths)}")
print("   binding shapes that feed a `**` splat into a target constructor:")
for k, c in shapes.most_common():
    print(f"      {c:>4}  {k}")
print(f"      {inline:>4}  inline Job(**{{...}}) / Task(**{{...}})")
print(f"      {unbound:>4}  splatted name with NO binding statement in its own file")
print(f"   an `Assign -> Dict` sweep alone sees {shapes['Assign -> Dict']} of "
      f"{sum(shapes.values())} binding sites")
print("   classic keys those tables carry:")
for k, c in keys.most_common():
    print(f"      {c:>4}  {k}")

mint = collections.Counter()
for rel in paths:
    try:
        tree = ast.parse(open(rel, "rb").read(), filename=rel)
    except (SyntaxError, OSError):
        continue
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id in CTOR):
            continue
        for kw in n.keywords:
            if kw.arg != "id":
                continue
            v = kw.value
            shape = (f"{v.func.id}()" if isinstance(v, ast.Call)
                     and isinstance(v.func, ast.Name) else type(v).__name__)
            mint[f"{n.func.id}.id = {shape}"] += 1
print("\nC. the VALUE a classic id keyword is constructed with, which the flip renames"
      "\n   and does not retype:")
for k, c in mint.most_common(8):
    print(f"      {c:>4}  {k}")
```
