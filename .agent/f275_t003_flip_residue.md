# F275 T003 — the FLIP, APPLIED AND RUN: what its residue is

> Measured by the reviewer at `978046fe`, this round's base, in a disposable `git worktree`
> under the gitignored `.remedy-wt/`, removed and pruned before the block was authored.
> THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it.

## 1. Why this reading was owed

`.agent/handoff.md` at `978046fe` names the flip as the next round's work and calls it "a
mechanical transformation with every prerequisite measured". Every clause of that sentence
was earned: DECISION F275 D23 widened in the store capabilities the flip's target lacked,
D24 proved the JOB record pair clean, and D25 ruled the construction mapping and recorded
two mechanical rules. What none of those rounds did is APPLY the flip and RUN the suite.
This file is that run — the fourth artefact of T003 and the first to execute rather than
enumerate.

## 2. The transform

Surgical text edits at `ast`-resolved `(line, column)` spans, right to left within each
line, so comments, blank lines and formatting survive. `ast.unparse` is not used: it
discards every comment, which would destroy this repository's WHY comments and redden the
guards that read source text. Edits are applied IN BYTES, because `ast` reports
`col_offset` as a UTF-8 byte offset — DECISION F275 D25's first mechanical rule. The six
rules already ruled by this chain:

    T1 type names `Job`->`JobPlan`, `Task`->`TaskEntry` · T2 job fields `.id`->`.job_id`,
    `.name`->`.job_title` (D24) · T3 task fields `.id`->`.task_id`,
    `.description`->`.title` (D25) · T4 ctor keywords `name=`, `description=`, `type=`,
    `task_type=`, `id=` · T5 the store seam (D23) · T6
    `<job>.created_at.isoformat()`->`<job>.created_at` (D24)

## 3. THE FOUR RULES THIS DRY RUN ADDED, each learned by failing

Recorded here rather than in DECISION F275 D26 because they are mechanics, not a choice.

**I1 — a type import moves its MODULE PATH, not only its name.** D25's second rule,
restated because implementing it exposed the three below. The unified record lives in
`packages.orchestration.pingpong_job`, so `from packages.core.models import Job` becomes
`from packages.orchestration.pingpong_job import JobPlan`.

**I2 — a MIXED import is SPLIT, never moved.** 358 `ImportFrom` nodes name `Job` or `Task`,
every one from `packages.core.models`, and 176 of those name a target BESIDE a non-target —
`RunState` at 103, `Artifact` and `ArtifactKind` at 29 more, and so on. Moving such a node's
module path wholesale takes the non-targets with it. The node becomes two statements: the
survivors keep the old module, the targets get the new one. Applied: 518 moved, 218 split.

**I3 — the SEAM'S OWN IMPORTS move with the seam.** Rewriting the CALL `save_job(...)` to
`save_job_plan(...)` while leaving `from packages.orchestration.storage import save_job`
standing leaves the new name unbound. The first dry run read exactly that, as `NameError:
name 'save_job_plan' is not defined`, and repairing it moved the suite from 2839 failed and
229 errors to 2714 failed and 106 errors — which is the honest size of this rule's effect
and the reason it is a rule rather than the cause.

**I4 — a construction whose keywords arrive through a `**` splat is INVISIBLE to a keyword
rewrite, and the transform does not yet see it.** `Job(**defaults)` where `defaults` is a
dict literal holding `"id"` keeps the classic key and the unified constructor refuses it. It
is the blindness a text sweep has to an argv-list invocation: the keyword is not a
`keyword.arg`, so no rewrite of `keyword.arg` reaches it. The sites are test helper
factories of the shape `def _make_job(**kw): defaults = {"name": ...}; defaults.update(kw);
return Job(**defaults)`, so the rule must reach the helper's dict literal AND its callers'
keywords — a call-graph pass, not a node rewrite. This class is the largest in the residue
at 867 failures and it is NOT what blocks the flip; see section 6.

## 4. What the applied transform did

| reading | measured |
|---|---:|
| files rewritten | 282 |
| files left unparsable by the edit | 0 |
| `git diff --shortstat` insertions | 5388 |
| `git diff --shortstat` deletions | 5230 |
| changed files under `packages/` or `apps/` | 110 |
| changed files under `tests/` | 172 |
| `pytest tests/ -q --co` collected | 18394 |
| collection errors | 0 |

Rewrites by rule, as the instrument counted them: import moved 518, import split 218, T1
type name 1236, T2 job field 1895, T3 task field 532, T4 `description` 247, T4 `id` 107, T4
`name` 539, T5 seam 779, T6 isoformat 6. Five paths are EXCLUDED because they define or
implement the classic record and its store rather than consume it —
`packages/core/models.py`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/storage.py` and `tests/test_storage.py`, of which four exist.

## 5. What the flipped tree then does

    $ python3 -B -m pytest tests/ -q --tb=line -p no:randomly
    2714 failed, 15551 passed, 23 skipped, 1 warning, 106 errors in 1189.47s (0:19:49)
    REAL_EXIT=1

Classified by bucketing the run's own exception lines — the type, and the message with
quoted spans and digits normalised — over the 2563 lines the pattern matched:

| count | class |
|---:|---|
| 867 | `TypeError: JobPlan.__init__() got an unexpected keyword argument 'X'` |
| 493 | `AttributeError: 'X' object has no attribute 'X'` |
| 271 | `TypeError: unsupported operand type(s) for /: 'X' and 'X'` |
| 256 | `ValueError: badly formed hexadecimal UUID string` |
| 241 | `pydantic ValidationError: N validation error for Artifact` |
| 128 | `pydantic ValidationError: N validation errors for TaskExecutionContext` |
| 14 | `TypeError: TaskEntry.__init__() got an unexpected keyword argument 'X'` |

## 6. THE PREMISES, and the instrument that re-measures them

The four readings DECISION F275 D26 rests on. P1 and P2 read the SHIPPED classes by
importing them, the convention DECISION F275 D22 and D24 set; P3 and P4 resolve a site by
`ast` over the files `git ls-files '*.py'` names, never by grep. Recorded output:

    tracked .py from git ls-files: 993 | instrument reads itself: False
    P1 Job.id <class 'uuid.UUID'> | JobPlan.job_id str
    P1 Task.id <class 'uuid.UUID'> | TaskEntry.task_id str
    P2 pydantic models under `packages.`: 53 | declaring a UUID-typed field: 6
       packages.core.models.Artifact ['id', 'task_id']
       packages.core.models.Job ['id']
       packages.core.models.Task ['id', 'output_artifact_ids']
       packages.orchestration.builder_models.TaskExecutionContext ['job_id', 'task_id']
       packages.orchestration.patch_intent.PatchIntentSet ['task_id', 'artifact_id']
       packages.orchestration.project_registry.RemyProject ['id']
    P3 splat constructions: 51 sites in 30 files, production files 0
    P4 seam imports: 397 sites in 154 files, production files 55

P1 AND P2 ARE WHY THE FLIP IS NOT THE NEXT COMMIT, and P3 is why the largest failure class
is not. A `**` splat is a transform rule: 51 sites, all under `tests/`, and every line they
touch is rewritten by the flip anyway, so nothing is owed to them ahead of it. THE ID SHAPE
IS NOT A RULE. `Job.id` is a `uuid.UUID` and `JobPlan.job_id` is a `str`, and three models
the flip never touches — `Artifact`, `TaskExecutionContext`, `PatchIntentSet` — declare that
type on a field the flip feeds. No rewrite of the classic record can satisfy them, and no
gate over a rename could see them, which is why this reading was owed before the commit and
not after it.

The instrument, so that this artefact is reproducible from itself. Run from the repository
root with `python3 -B`; it writes nothing.

<!-- INSTRUMENT -->
```python
"""F275 R46 — the four premises DECISION F275 D26 rests on, re-measured in one run.

P1 and P2 read the SHIPPED classes by importing them. P3 and P4 resolve a site by `ast`
over the files `git ls-files '*.py'` names, never by grep, so a name inside a comment or
a string is not a site. This probe WRITES NOTHING.
"""
import ast, collections, dataclasses, importlib, inspect, pkgutil, subprocess

CTOR = {"Job", "Task"}
SEAM = {"save_job", "load_job", "load_job_safe", "list_jobs", "list_jobs_safe",
        "resolve_job_id"}

paths = [p for p in subprocess.run(["git", "ls-files", "*.py"], capture_output=True,
                                   text=True).stdout.split() if p]
own = __file__.split("/")[-1]
print(f"tracked .py from git ls-files: {len(paths)} | instrument reads itself: "
      f"{any(p == own or p.endswith('/' + own) for p in paths)}")

from packages.core.models import Job, Task
from packages.orchestration.pingpong_job import JobPlan, TaskEntry
jp = {f.name: str(f.type) for f in dataclasses.fields(JobPlan)}
te = {f.name: str(f.type) for f in dataclasses.fields(TaskEntry)}
print(f"P1 Job.id {Job.model_fields['id'].annotation} | JobPlan.job_id {jp.get('job_id')}")
print(f"P1 Task.id {Task.model_fields['id'].annotation} | "
      f"TaskEntry.task_id {te.get('task_id')}")

from pydantic import BaseModel
import packages
found = {}
for m in pkgutil.walk_packages(packages.__path__, "packages."):
    try:
        mod = importlib.import_module(m.name)
    except Exception:
        continue
    for obj in vars(mod).values():
        if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel:
            found[f"{obj.__module__}.{obj.__name__}"] = obj
hits = {}
for name, obj in found.items():
    u = [f for f, i in obj.model_fields.items() if "UUID" in str(i.annotation)]
    if u:
        hits[name] = u
print(f"P2 pydantic models under `packages.`: {len(found)} | "
      f"declaring a UUID-typed field: {len(hits)}")
for name in sorted(hits):
    print(f"   {name} {hits[name]}")

splats, seam_nodes = [], []
for rel in paths:
    try:
        tree = ast.parse(open(rel, "rb").read(), filename=rel)
    except (SyntaxError, OSError):
        continue
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            called = f.id if isinstance(f, ast.Name) else (
                f.attr if isinstance(f, ast.Attribute) else None)
            if called in CTOR and any(k.arg is None for k in n.keywords):
                splats.append(rel)
        elif isinstance(n, ast.ImportFrom):
            if {a.name for a in n.names} & SEAM:
                seam_nodes.append(rel)
for label, rows in (("P3 splat constructions", splats), ("P4 seam imports", seam_nodes)):
    files = set(rows)
    print(f"{label}: {len(rows)} sites in {len(files)} files, production files "
          f"{len([f for f in files if not f.startswith('tests/')])}")
```

## 7. What this reading does NOT settle

THE RESIDUE IS CLASSIFIED, NOT EXHAUSTED. The classes above account for 2270 of the 2563
exception lines the classifier matched, and 2563 is itself smaller than 2714 failures plus
106 errors, because a failure whose traceback line the pattern did not match is not counted.
That remainder is given NO numeral beyond the two totals, because none was measured.

THE 493 `AttributeError` AND 271 `unsupported operand` CLASSES ARE NOT DIAGNOSED HERE. They
are consistent with the id shape and with a receiver the field rename should not have
touched, and neither reading was taken, so neither is stated. The round that migrates the id
shape re-runs this dry run and reads them against a tree where the shape is no longer a
cause.

THE EXCLUSION LIST IS A CHOICE THIS DRY RUN MADE, NOT A RULING. Excluding
`packages/core/models.py` and `packages/orchestration/storage.py` is what lets the classic
record and its store survive the flip commit, so that DECISION F260 D5's resolver collapse
can delete them in the commit range it names. A later round may rule differently.
