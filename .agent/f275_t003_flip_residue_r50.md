# F275 T003 — the FLIP RE-RUN against the migrated id shape: what still blocks it

> Measured by the reviewer at `020b1d57`, this round's base, in two disposable `git worktree`s
> under the gitignored `.remedy-wt/`, both removed and pruned before the block was authored.
> THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it. It does not replace
> `.agent/f275_t003_flip_residue.md`, which records the run at `978046fe` and stays as written.

## 1. Why this reading was owed

DECISION F275 D26 ruled the flip NOT the next commit because a dry run of it at `978046fe`
left 2714 failing tests, and named the ID SHAPE as the largest unruled class. D27 and D28
migrated that shape one assignment-connected component at a time. The question those three
decisions leave is a measurement and not a prediction: with the shape migrated, does the flip
converge?

## 2. THE CONTROL, WHICH THE R46 RUN DID NOT HAVE

R46 reported 2714 failures against no baseline, so it could not tell a flip-caused failure
from a worktree artifact. This run takes both readings at the SAME commit, in two fresh
worktrees, with the same selection and the same flags.

    $ python3 -B -m pytest tests/ -q --tb=line -p no:randomly -p no:cacheprovider
    UNFLIPPED  1 failed, 18366 passed, 29 skipped, 1 warning in 1316.51s       REAL_EXIT=1
    FLIPPED    2558 failed, 15703 passed, 29 skipped, 1 warning,
               106 errors in 1248.09s                                          REAL_EXIT=1

The control's ONE failure is
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
which needs the gitignored `apps/ui/node_modules`, absent from every fresh worktree. It is
the only node id failing in BOTH runs. Differencing the two node-id sets gives 2557 failures
and all 106 errors CAUSED by the flip, against 1 shared failure and 0 errors in the control.
So the honest comparison with R46 is 2714 UNATTRIBUTED against 2557 ATTRIBUTED, and the
migration D26, D27 and D28 performed bought 157 of them.

## 3. What the applied transform did

`.remedy-wt/r46_flip_transform.py` unchanged — the same surgical `ast`-span text edits in
bytes, the same six rules, the same five exclusions. It rewrote 282 files and broke none;
`git diff --shortstat` reads 5390 insertions and 5232 deletions over those 282, of which 110
are under `packages/` or `apps/` and 172 under `tests/`; `pytest tests/ -q --co` then
collected 18396 tests at exit 0 with zero collection errors. Rewrites by rule, as the
instrument counted them: import moved 518, import split 218, T1 type name 1237, T2 job field
1896, T3 task field 532, T4 `description` 247, T4 `id` 107, T4 `name` 540, T5 seam 779, T6
isoformat 6 — 6080 in all.

## 4. The residue by class, the two runs beside each other

Both columns bucket the `E   <Exception>: <message>` lines of a `--tb=line` run by exception
type and by a message with quoted spans and digits normalised. R46's column is quoted from
`.agent/f275_t003_flip_residue.md` section 5; this run matched 2387 such lines.

| R46 | R50 | class |
|---:|---:|---|
| 867 | 867 | `TypeError: JobPlan.__init__() got an unexpected keyword argument 'X'` |
| 493 | 517 | `AttributeError: 'X' object has no attribute 'X'` |
| 271 | 368 | `TypeError: unsupported operand type(s) for /: 'X' and 'X'` |
| 256 | 269 | `ValueError: badly formed hexadecimal UUID string` |
| 241 | 0 | `pydantic ValidationError: N validation error for Artifact` |
| 128 | 0 | `pydantic ValidationError: N validation errors for TaskExecutionContext` |
| 14 | 14 | `TypeError: TaskEntry.__init__() got an unexpected keyword argument 'X'` |

THE MIGRATION DID EXACTLY WHAT IT WAS PERFORMED TO DO AND NOTHING MORE. The two pydantic
classes are gone in full — 369 E-lines to 0 — and the whole run now holds TWO
`ValidationError` lines, `1 validation error for Job` and `1 validation error for Task`, both
against the classic record the flip excludes. Every other class held or GREW, which is why
the total moved by 157 and not by 369: the classes below were never the id shape.

## 5. THE THREE PREREQUISITES THE FLIP STILL HAS, each measured

**P1 — THE FIELD RENAME IS DECIDED BY A RECEIVER-NAME HEURISTIC, and that is the
`AttributeError` class.** The transform renames `.id`, `.name` and `.description` whenever
the receiver's NAME contains `job`, `plan`, `record` or `task`, and never by resolving the
receiver's TYPE. Restricted to the run's `E ` lines, attribute misses total 551 over 22
distinct receiver-and-attribute pairs, and the largest are every one of them a receiver whose
name matched while its type is not `Job` or `Task`:

    191 PlannedTask.task_id · 99 TaskEntry.id · 48 ProposedTask.title ·
    42 TaskOutcome.title · 29 ProposedTask.task_id · 28 _FakeJob.job_id ·
    20 Mission.job_id · 11 _Job.job_id · 7 RemyProject.job_id · 6 PosixPath.job_title

`PosixPath.job_title` is the shape to recognise: a local named `job_dir` or `plan_path` holds
a `Path`, and its `.name` was renamed to `.job_title`. `TaskEntry.id` is the same heuristic
failing from the other side — a receiver the rename SHOULD have reached and did not, because
its name carries no target word. The 551 here and the 517 in section 4 are the same class
read two ways: section 4 splits the `Did you mean:` suffix into its own bucket.

This is not a new discovery. `docs/roadmap/features/T2_F275.md` T002 ALREADY ORDERS the
remedy — the DECISION F272 D7 raising-property probe over every candidate receiver, "giving
the real site set rather than the bound", because `.id` is polymorphic here exactly as
`.status` was. Every dry run of this chain has used the heuristic instead.

**P2 — THE SURVIVING `UUID(...)` COERCIONS, which are the `unsupported operand` and
hexadecimal-UUID classes and are NOT a rename.** The unified record spells a job id as a
16-hex string. `packages/orchestration/timeline.py` normalises with
`jid = job_id if isinstance(job_id, UUID) else UUID(str(job_id))`, which rejects that string,
and `job_dir` in `packages/orchestration/data_paths.py` returns `jobs_dir(root) / job_id`,
joining a `Path` with whatever it is handed — line 200 at `020b1d57`. Of the 368
`unsupported operand` E-lines the traceback attributes 331 to that one line, and of
the 269 hexadecimal-UUID E-lines it attributes 239 to `uuid.py:177`. Resolved by `ast` at
`020b1d57`, over the transform's own file set: `UUID(<job/task argument>)` at 169 sites in 65
files of which 39 are production, `uuid4()` at 637 sites in 144 files of which 34 are
production, and `UUID(<other argument>)` at 49 sites in 21 files of which 14 are production.
No rule of the transform touches a call, so these sites survive the flip verbatim and then
reject the value it produces.

**P3 — THE SPLAT CLASS, unchanged at 867.** Rule I4 of
`.agent/f275_t003_flip_residue.md` section 3. The 881 constructor-keyword E-lines name their
keywords: 778 `JobPlan.name`, 89 `JobPlan.id`, 13 `TaskEntry.acceptance_checks`, 1
`TaskEntry.description`. A keyword arriving through `**defaults` is not a `keyword.arg`, so
no rewrite of `keyword.arg` reaches it; the fix is a call-graph pass over the helper
factories, and `TaskEntry.acceptance_checks` shows those dict literals carry keys the
construction mapping never ruled.

## 6. The instrument, so that this artefact is reproducible from itself

Run from the repository root with `python3 -B`. It resolves every site by `ast` over the
files `git ls-files '*.py'` names, never by grep, and it writes nothing. Its T2 and T3 totals
are the transform's own `T2 job field` and `T3 task field` counts, which is what makes the
heuristic's reach measurable without applying the flip.

<!-- INSTRUMENT -->
```python
"""F275 R50 — the two classes the R46 dry run left undiagnosed, resolved to their sites."""
import ast, collections, subprocess, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "."
JOB_FIELD, TASK_FIELD = {"id", "name"}, {"id", "description"}
JOBISH, TASKISH = ("job", "plan", "record"), ("task",)
EXCLUDE = {"packages/core/models.py", "packages/orchestration/pingpong_job.py",
           "packages/orchestration/storage.py", "tests/test_storage.py",
           "tests/test_models.py"}
recv_name = lambda n: str(getattr(n, "id", None) or getattr(n, "attr", "") or "")
is_jobish = lambda s: s.lower() in ("j", "stored") or any(t in s.lower() for t in JOBISH)
is_taskish = lambda s: s.lower() in ("t", "tk") or any(t in s.lower() for t in TASKISH)

paths = [p for p in subprocess.run(["git", "ls-files", "*.py"], capture_output=True,
                                   text=True, cwd=BASE).stdout.split() if p]
scanned = [p for p in paths if p not in EXCLUDE]
t2, t3 = collections.Counter(), collections.Counter()
uuid_sites, uuid_files = collections.Counter(), collections.defaultdict(set)
for rel in scanned:
    try:
        tree = ast.parse(open(f"{BASE}/{rel}", "rb").read(), filename=rel)
    except (SyntaxError, OSError):
        continue
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute):
            recv = recv_name(n.value)
            if n.attr in JOB_FIELD and is_jobish(recv):
                t2[recv] += 1
            elif n.attr in TASK_FIELD and is_taskish(recv):
                t3[recv] += 1
        elif isinstance(n, ast.Call):
            f = n.func
            called = f.id if isinstance(f, ast.Name) else (
                f.attr if isinstance(f, ast.Attribute) else None)
            if called not in ("UUID", "uuid4", "uuid5", "uuid3"):
                continue
            arg = " ".join(ast.dump(a) for a in n.args).lower() if n.args else ""
            key = called if called != "UUID" else (
                "UUID(job/task arg)" if ("job" in arg or "task" in arg) else "UUID(other arg)")
            uuid_sites[key] += 1
            uuid_files[key].add(rel)

print(f"tracked .py: {len(paths)} | scanned after the transform's exclusions: {len(scanned)}")
print(f"D1 T2 JOB-FIELD edits: {sum(t2.values())} over {len(t2)} distinct receiver names")
for r, c in t2.most_common(10):
    print(f"    {c:>5}  {r or '(expr)'}")
print(f"D1 T3 TASK-FIELD edits: {sum(t3.values())} over {len(t3)} distinct receiver names")
for r, c in t3.most_common(10):
    print(f"    {c:>5}  {r or '(expr)'}")
for k, c in uuid_sites.most_common():
    files = uuid_files[k]
    prod = len([f for f in files if not f.startswith("tests/")])
    print(f"D2 {c:>5}  {k:22s} in {len(files)} files, production {prod}")
```

Its recorded output at `020b1d57`, complete and untrimmed:

    tracked .py: 993 | scanned after the transform's exclusions: 989
    D1 T2 JOB-FIELD edits: 1896 over 19 distinct receiver names
         1802  job
           33  j
            6  parent_job
            6  job_one
            6  plan_less
            5  job_node
            5  _Job
            4  job_stub
            4  cli_job
            4  job_two
    D1 T3 TASK-FIELD edits: 532 over 11 distinct receiver names
          272  task
          235  t
            8  fix_task
            6  pending_task
            3  repair_task
            3  task_node
            1  verify_task
            1  real_task
            1  ptask
            1  awaiting_task
    D2   637  uuid4                  in 144 files, production 34
    D2   169  UUID(job/task arg)     in 65 files, production 39
    D2    49  UUID(other arg)        in 21 files, production 14

## 7. What this reading does NOT settle

THE RESIDUE IS CLASSIFIED, NOT EXHAUSTED. The classes in section 4 account for 2035 of the
2387 matched E-lines, and 2387 is itself smaller than 2557 flip-caused failures plus 106
errors, because a failure whose line the pattern did not match is not counted. That remainder
is given NO numeral beyond the two totals, because none was measured.

THE 106 ERRORS ARE NOT DIAGNOSED HERE. They fall in nine files, the largest being
`tests/orchestration/test_mission_e2e.py` at 24,
`tests/orchestration/test_worktree_resume_cli.py` at 16,
`tests/orchestration/test_feature_mission_adapter.py` at 15 and
`tests/ui_server/test_live_state.py` at 15. They are consistent with a fixture raising before
its test body runs, and that reading was not taken, so it is not stated.

WHETHER P1, P2 AND P3 EXHAUST THE PREREQUISITES IS NOT ESTABLISHED. Each is the diagnosed
cause of a class this run MEASURED; nothing here proves a fourth class does not appear once
they are fixed, and the honest test of that is another dry run.
