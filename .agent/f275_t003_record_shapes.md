# F275 T003 — the RECORD SHAPES the flip moves, MEASURED

> Measured at `7f8724c3`, this round's base, over the tracked tree at that commit.
> THIS FILE MEASURES; IT FLIPS NOTHING. No line under `packages/`, `apps/`, `tests/`,
> `docs/` or `scripts/` moved in the round that wrote it.

DECISION F275 D22 compared the two TASK records by IMPORTING both shipped classes and
found them sharing two field names of seven and twenty-three, which disproved DECISION
F272 D15's sentence about them. Nobody had run that reading for the JOB records — the pair
the flip actually moves. This file is that reading, together with the shape readings a
name comparison cannot give, and DECISION F275 D24 carries its ruling.

The instrument's source is embedded below so the measurement is reproducible from this
artefact alone, which is the convention `.agent/f275_t002_flip_inventory.md` set and
`.agent/f275_t003_flip_seam.md` kept. A site is one `(path, line)` pair resolved by `ast`
over the files `git ls-files '*.py'` names, never by grep, so a name inside a comment or a
string is not a site. Every receiver-name filter PRINTS ITS REJECTED RECEIVERS beside the
accepted ones, because a count is only as wide as its predicate and a narrowing nobody can
audit is a narrowing nobody can trust.

No per-SITE list of the type sites is committed, and DECISION F275 D24 records the three
reasons: the figures reproduce DECISION F275 D21's part (c), the transformation there is a
type-NAME rewrite that needs no list, and this artefact regenerates the list in one run.

## The instrument
```python
"""F275 T003 — the flip's last measurements, in one pass.

Produces, at the commit it is run at: the two JOB records compared field by field; the
shape changes on the names they share; the sites that use `created_at` as a DATETIME and
the sites that dereference `budget`; and a re-derivation of the two TYPE-site figures no
committed file holds — DECISION F275 D21's part (c) and the `Task` sites D22 counted.

A site is one `(path, line)` pair resolved by `ast` over the files `git ls-files '*.py'`
names, never by grep. Every receiver-name filter prints its REJECTED receivers beside the
accepted ones, because a count is only as wide as its predicate.
"""
import ast
import collections
import dataclasses
import subprocess
import sys

REPO = "."
sys.path.insert(0, REPO)
JOBISH = ("job", "plan", "record")
SHORT = ("j", "stored")
DT_ONLY = {"isoformat", "strftime", "timestamp", "date", "time", "astimezone",
           "toordinal", "weekday", "utcoffset", "tzname"}


def tracked():
    out = subprocess.run(["git", "ls-files", "*.py"], capture_output=True, text=True,
                         cwd=REPO).stdout
    return [p for p in out.split() if p]


def trees():
    for path in tracked():
        try:
            yield path, ast.parse(open(f"{REPO}/{path}", "rb").read(), filename=path)
        except (SyntaxError, OSError):
            continue


def recv(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call):
        f = node.func
        return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
    return ""


def jobish(name):
    low = name.lower()
    return low in SHORT or any(t in low for t in JOBISH)


def type_sites(name):
    kinds = collections.defaultdict(set)
    for path, tree in trees():
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                f = n.func
                called = f.id if isinstance(f, ast.Name) else (
                    f.attr if isinstance(f, ast.Attribute) else None)
                if called == name:
                    kinds["construction"].add((path, n.lineno))
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                for a in n.names:
                    if a.name == name:
                        kinds["import"].add((path, n.lineno))
            elif isinstance(n, (ast.AnnAssign, ast.arg)):
                if n.annotation is not None:
                    for sub in ast.walk(n.annotation):
                        if (isinstance(sub, ast.Name) and sub.id == name) or \
                           (isinstance(sub, ast.Constant) and sub.value == name):
                            kinds["annotation"].add((path, n.lineno))
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.returns:
                for sub in ast.walk(n.returns):
                    if (isinstance(sub, ast.Name) and sub.id == name) or \
                       (isinstance(sub, ast.Constant) and sub.value == name):
                        kinds["annotation"].add((path, n.lineno))
    return kinds


def report(name, kinds):
    union = set()
    for s in kinds.values():
        union |= s
    files = {p for p, _ in union}
    prod = sorted(f for f in files if not f.startswith("tests/"))
    print(f"\n### `{name}` TYPE sites")
    for k in ("construction", "import", "annotation"):
        print(f"  {k:13s} {len(kinds[k])}")
    print(f"  DISTINCT CHANGED LINES {len(union)} in {len(files)} files — "
          f"{len(prod)} production, {len(files) - len(prod)} test")
    per_file = collections.defaultdict(set)
    for p, ln in union:
        per_file[p].add(ln)
    print(f"  files carrying a site: {len(per_file)}")
    return union


def main():
    from packages.core.models import Job
    from packages.orchestration.pingpong_job import JobPlan

    jf = {n: str(f.annotation) for n, f in Job.model_fields.items()}
    pf = {f.name: str(f.type) for f in dataclasses.fields(JobPlan)}
    shared = sorted(set(jf) & set(pf))
    job_only = sorted(set(jf) - set(pf))
    print("## 1. THE JOB RECORD PAIR, by IMPORTING both shipped classes")
    print(f"  Job fields {len(jf)} | JobPlan fields {len(pf)}")
    print(f"  shared names {len(shared)}: {shared}")
    print(f"  `Job`-only names {len(job_only)}: {job_only}")
    print(f"  ORPHANS (no counterpart, not a known rename): "
          f"{[f for f in job_only if f not in ('id', 'name')]}")

    print("\n## 2. THE ANNOTATIONS ON THE SHARED NAMES, side by side")
    print("  The two reprs differ even where the TYPE does not — pydantic resolves an")
    print("  annotation to its module path and a dataclass keeps the source string — so")
    print("  these are read by MEANING and a string comparison is NOT used.")
    for n in shared:
        print(f"  {n:14s} Job {jf[n]:44s} JobPlan {pf[n]}")

    print("\n## 3. `created_at` USED AS A DATETIME, by receiver")
    acc, rej = [], []
    for path, tree in trees():
        for n in ast.walk(tree):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)):
                continue
            inner = n.func.value
            if not (isinstance(inner, ast.Attribute) and inner.attr == "created_at"):
                continue
            if n.func.attr not in DT_ONLY:
                continue
            r = recv(inner.value)
            (acc if jobish(r) else rej).append((path, n.lineno, r, n.func.attr))
    ap = [r for r in acc if not r[0].startswith("tests/")]
    print(f"  ACCEPTED {len(acc)} — production {len(ap)}, test {len(acc) - len(ap)}")
    for row in sorted(acc):
        print(f"    {row[0]}:{row[1]} receiver {row[2]} .{row[3]}()")
    print(f"  REJECTED {len(rej)}, listed so the filter is auditable:")
    for row in sorted(rej):
        print(f"    {row[0]}:{row[1]} receiver {row[2]} .{row[3]}()")

    print("\n## 4. `budget` DEREFERENCED on a job-ish receiver")
    deref = []
    for path, tree in trees():
        for n in ast.walk(tree):
            if (isinstance(n, ast.Attribute) and isinstance(n.value, ast.Attribute)
                    and n.value.attr == "budget" and jobish(recv(n.value.value))):
                deref.append((path, n.lineno, recv(n.value.value), n.attr))
    dp = [d for d in deref if not d[0].startswith("tests/")]
    print(f"  sites {len(deref)} — production {len(dp)}, test {len(deref) - len(dp)}")
    for row in sorted(deref):
        print(f"    {row[0]}:{row[1]} receiver {row[2]} .budget.{row[3]}")

    print("\n## 5. THE TYPE-SITE FIGURES, re-derived at this commit")
    j = report("Job", type_sites("Job"))
    t = report("Task", type_sites("Task"))
    both = j | t
    print(f"\n## 6. THE TWO TYPE-SITE SETS UNIONED")
    print(f"  union {len(both)} lines in {len({p for p, _ in both})} files; "
          f"overlap {len(j & t)}")


if __name__ == "__main__":
    main()
```

## What it printed

```
## 1. THE JOB RECORD PAIR, by IMPORTING both shipped classes
  Job fields 15 | JobPlan fields 65
  shared names 13: ['artifacts', 'budget', 'budgets', 'created_at', 'fences', 'flight_plan', 'intake', 'metadata', 'mission', 'project_id', 'state', 'tasks', 'user_prompt']
  `Job`-only names 2: ['id', 'name']
  ORPHANS (no counterpart, not a known rename): []

## 2. THE ANNOTATIONS ON THE SHARED NAMES, side by side
  The two reprs differ even where the TYPE does not — pydantic resolves an
  annotation to its module path and a dataclass keeps the source string — so
  these are read by MEANING and a string comparison is NOT used.
  artifacts      Job list[packages.core.models.Artifact]          JobPlan list[Artifact]
  budget         Job <class 'packages.core.models.Budget'>        JobPlan Budget | None
  budgets        Job packages.core.models.JobBudgets | None       JobPlan dict | None
  created_at     Job <class 'datetime.datetime'>                  JobPlan str
  fences         Job packages.core.models.JobFences | None        JobPlan JobFences | None
  flight_plan    Job dict[str, typing.Any] | None                 JobPlan dict | None
  intake         Job dict[str, typing.Any] | None                 JobPlan dict | None
  metadata       Job dict[str, typing.Any]                        JobPlan dict
  mission        Job str | None                                   JobPlan str
  project_id     Job str | None                                   JobPlan str
  state          Job <enum 'RunState'>                            JobPlan RunState
  tasks          Job list[packages.core.models.Task]              JobPlan list[TaskEntry]
  user_prompt    Job str | None                                   JobPlan str

## 3. `created_at` USED AS A DATETIME, by receiver
  ACCEPTED 6 — production 4, test 2
    apps/cli/commands/job.py:149 receiver j .isoformat()
    apps/cli/commands/job.py:160 receiver job .isoformat()
    apps/cli/commands/job.py:170 receiver job .isoformat()
    packages/orchestration/job_fulfillment.py:230 receiver record .isoformat()
    tests/cli/test_loop_cmd.py:179 receiver stored .isoformat()
    tests/cli/test_loop_cmd.py:193 receiver stored .isoformat()
  REJECTED 6, listed so the filter is auditable:
    apps/cli/commands/project.py:51 receiver p .isoformat()
    apps/cli/commands/project.py:62 receiver p .isoformat()
    apps/cli/commands/project.py:71 receiver p .isoformat()
    apps/cli/commands/propose_cmd.py:128 receiver t .isoformat()
    packages/orchestration/project_registry.py:795 receiver project .strftime()
    packages/orchestration/project_registry.py:890 receiver project .isoformat()

## 4. `budget` DEREFERENCED on a job-ish receiver
  sites 1 — production 1, test 0
    packages/orchestration/pingpong_job.py:829 receiver job .budget.model_dump

## 5. THE TYPE-SITE FIGURES, re-derived at this commit

### `Job` TYPE sites
  construction  582
  import        345
  annotation    367
  DISTINCT CHANGED LINES 1294 in 201 files — 46 production, 155 test
  files carrying a site: 201

### `Task` TYPE sites
  construction  246
  import        142
  annotation    40
  DISTINCT CHANGED LINES 428 in 112 files — 15 production, 97 test
  files carrying a site: 112

## 6. THE TWO TYPE-SITE SETS UNIONED
  union 1583 lines in 208 files; overlap 139
```
