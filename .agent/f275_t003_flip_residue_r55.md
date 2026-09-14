# F275 T003 — the FLIP with all three prerequisites implemented: it is a RETYPE, not a rename

> Measured by the reviewer at `08feacae`, this round's base, in two disposable `git
> worktree`s under the gitignored `.remedy-wt/`, both removed and pruned before this text
> was authored. THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it. It replaces
> neither `.agent/f275_t003_flip_residue.md` nor `.agent/f275_t003_flip_residue_r50.md`,
> which record the runs at `978046fe` and `020b1d57` and stay as written.

## 1. Why this reading was owed

DECISION F275 D29 ruled three prerequisites before the flip and each is now landed: P1,
the type-resolved field rename, at round 53; P2, the surviving `UUID(...)` coercions at
the seam, at rounds 51 and 52 as `R-0877`; P3, the `**` splat class, at round 54. D29's
CONSEQUENCE clause places this dry run after all three. The question it answers is a
measurement and not a prediction: with every prerequisite implemented, does the flip
converge?

IT DOES NOT, AND THE REASON IS NOT A FOURTH MISSING RULE. It is that the classic record
and the unified record disagree about FIELD TYPES as well as about field names, and a
rename carries the name while leaving every reader of the old type standing. Section 6
measures that; sections 3 and 5 are what had to be true before it could be seen.

## 2. The control, and what the two runs are

Both runs were taken at `08feacae` in fresh worktrees, with the same selection and the
same flags, the control first and the flipped tree second, never concurrently.

    $ python3 -B -m pytest tests/ -q --tb=line -p no:randomly -p no:cacheprovider
    CONTROL  1 failed, 18372 passed, 29 skipped, 1 warning in 1342.07s        REAL_EXIT=1
    FLIPPED  1331 failed, 16969 passed, 23 skipped, 1 warning,
             79 errors in 1234.46s                                            REAL_EXIT=1

The control's one failure is
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
which needs the gitignored `apps/ui/node_modules`. Differencing the two node-id sets gives
1331 failures and all 79 errors CAUSED by the flip, and ZERO failures shared between the
runs. THE ZERO IS NOT A FLIP EFFECT AND IS NOT REPORTED AS ONE: that one node passed in
the flipped worktree because the dependency had resolved by the time that run was taken,
which is the same volatility `.agent/f275_t003_descriptor_sites.md` section 3 records for
its two probe runs. The honest comparison against round 50 is therefore 2557 attributed
failures and 106 errors THEN against 1331 and 79 NOW.

## 3. What the transform did, and the two rules that changed

`.remedy-wt/r46_flip_transform.py`, which round 50 re-ran unchanged, with T2 and T3
rewritten and one rule added. Everything else — T1, T4, T5, T6, I1, I2, I3, the five
exclusions and the right-to-left byte-span edit machinery — is unchanged.

P1 REPLACES THE RECEIVER-NAME HEURISTIC WITH THE RULED SITE SET. T2 and T3 no longer ask
whether a receiver's NAME contains a target word; they rename only a site the ruled set R
of `.agent/f275_t003_descriptor_sites.md` holds, and they take the OWNER that decides
`job_id` against `task_id` from three sources in order: the static sweep's verdict where
it proved the class, else the probe's rows for that line where the line names exactly one
owner, else the receiver name restricted to the owners that line names. Of R's 2198 sites
407 resolve by the first, 1734 by the second and 56 by the third; the static sweep and the
probe CONFLICT on none; and exactly one site resolves by no route — `art.id` at
`tests/orchestration/test_repair_loop_v1.py:56`, a receiver the line-granular probe join
swept in beside a job and a task on the same line. It is left alone, which is right.

P3 IMPLEMENTS THE SPLAT CLASS IN EVERY BINDING SHAPE THE REPOSITORY USES. Section 5 is
why that sentence needs the last five words.

| reading | measured |
|---|---:|
| files rewritten | 261 |
| files left unparsable by the edit | 0 |
| files the edit would have broken and were left alone | 0 |
| `git diff --shortstat` insertions | 5185 |
| `git diff --shortstat` deletions | 5051 |
| changed files under `packages/` or `apps/` | 99 |
| changed files under `tests/` | 162 |
| `pytest tests/ -q --co` collected | 18402 |
| collection errors | 0 |

Rewrites by rule, as the instrument counted them: import moved 518, import split 218, T1
type name 1237, T2 job field 1786, T3 task field 411, T4 `description` 247, T4 `id` 107,
T4 `name` 540, T5 seam 779, T6 isoformat 6, S1 splat key 44, S1 splat key DROPPED 25, S2
helper keyword 8, S3 dict-call key 8 — 5934 in all. R50's T2 and T3 read 1896 and 532 from
the heuristic; the ruled set reads 1786 and 411, which is the same difference of verdict
`.agent/f275_t003_descriptor_sites.md` section 1 records, arriving as an edit count.

## 4. What P1 and P3 bought, class by class

Both earlier columns are quoted from the artefacts that measured them —
`.agent/f275_t003_flip_residue.md` section 5 and
`.agent/f275_t003_flip_residue_r50.md` section 4 — and all three columns bucket the
`E   <Exception>: <message>` lines of a `--tb=line` run by exception type and by a message
with quoted spans and digits normalised. This run matched 1364 such lines.

| R46 | R50 | R55 | class |
|---:|---:|---:|---|
| 867 | 867 | 0 | `TypeError: JobPlan.__init__() got an unexpected keyword argument 'X'` |
| 493 | 517 | 127 | `AttributeError: 'X' object has no attribute 'X'` |
| 271 | 368 | 379 | `TypeError: unsupported operand type(s) for /: 'X' and 'X'` |
| 256 | 269 | 194 | `ValueError: badly formed hexadecimal UUID string` |
| 241 | 0 | 0 | `pydantic ValidationError: N validation error for Artifact` |
| 128 | 0 | 0 | `pydantic ValidationError: N validation errors for TaskExecutionContext` |
| 14 | 14 | 25 | `TypeError: TaskEntry.__init__() got an unexpected keyword argument 'X'` |
| — | — | 306 | `SystemExit: N` |

THE CLASS P3 WAS AIMED AT IS NOW ZERO. The `JobPlan` constructor-keyword class, unmoved at
867 across two dry runs and the largest class in both, is gone entirely. What remains of
the constructor-keyword family is 25 lines naming `TaskEntry.acceptance_checks`, which
section 7 rules a different problem, and that figure GREW from 14 because tests that used
to die on `JobPlan.name` now reach further before failing — a class rising while the run
improves is what partial repair looks like, and it is reported rather than smoothed.

`SystemExit` carries no earlier column because neither earlier artefact reported it. No
claim is made that it was absent then; it was not measured, so it is not compared.

## 5. THE THREE DEFECTS THIS DRY RUN FOUND IN ITSELF, each before it found any in the flip

Recorded because each cost a twenty-minute run, and because two of them are defects in the
MODEL of the splat class that DECISION F275 D31 and rule I4 both share.

**D1 — a line DELETION carried as an INDEX is applied after a line SPLICE has moved it.**
D31 rules `permissions` and `description` DROPPED from a `Job` splat rather than renamed,
so the transform removes the whole element. The first implementation recorded the deletion
as a line NUMBER and filtered those numbers at the end, after rule I2 had already SPLICED
mixed imports into two statements — which moves every line below each split. The result
deleted a line four below the one the rule named. IT STILL PARSED AND IT STILL COLLECTED:
the run went green through both of the transform's own guards, and only a reading of the
diff showed blank lines removed that no rule ordered. The fix marks the line in place with
a sentinel and filters sentinels after the splices. THE RULE THIS LEAVES BEHIND: a
mechanical edit that DELETES a line may not name that line by index when any other rule of
the same pass changes the line COUNT, and the audit that catches it is a count of removed
lines by shape, not a parse.

**D2 — a defaults table written `dict(...)` is invisible to an `ast.Dict` sweep.** Rule I4
and D31 both resolve a `Job(**defaults)` site by finding the dict LITERAL assigned to
`defaults`. Nine sites write it `defaults = dict(name=..., ...)`, whose keys are
`keyword.arg` on a `dict` call and not `ast.Dict` keys at all, so round 54's instrument
counted them as carrying no resolvable key. Eight of the nine carry `name=`, and those
eight helper factories produced 1540 of one run's constructor-keyword exception lines.

**D3 — `defaults: dict = {...}` is an `AnnAssign`, not an `Assign`.** Eleven further sites,
found the same way and one run later. Taken together with D2: a sweep for `Assign -> Dict`
sees 16 of the 37 binding sites that feed a target splat, and the enumeration that closed
the class is `Assign` and `AnnAssign` crossed with `Dict` and `dict(...)`, plus the inline
`Job(**{...})` form. One site binds by a list comprehension and is reported unhandled
rather than guessed at:
`tests/ui_contracts/test_graph_architecture.py:725`.

THE RULE D2 AND D3 LEAVE BEHIND, and it is one rule: an instrument that resolves a value
to its BINDING enumerates the binding STATEMENT SHAPES before it reports a count, because
a shape it does not handle is indistinguishable in its output from a site that carries
nothing. Round 54's reading was not wrong about what it measured; it was silent about what
it could not see, and the artefact's own "resolved to NO key at all: 15" line is where
those sites went.

## 6. THE CAUSE: the two records disagree about TYPES, and a rename cannot carry a type

Read by importing the shipped classes at `08feacae` and comparing their declared field
types, never by reading either source:

| concept | classic `Job`/`Task` | unified `JobPlan`/`TaskEntry` |
|---|---|---|
| job id | `uuid.UUID` | `str` |
| task id | `uuid.UUID` | `str` |
| task status | `RunState` | `str` |
| created at | `datetime.datetime` | `str` |
| job state | `RunState` | `RunState` |

EVERY REMAINING CLASS BUT ONE IS THAT TABLE. The transform renames `Job(id=uuid4())` to
`JobPlan(job_id=uuid4())`, and `JobPlan` is a dataclass, which does not coerce and does not
complain: the `UUID` object is stored in a field declared `str` and travels until something
uses it. In the flipped tree 73 target constructions still hand `job_id` a `uuid4()` call
and 6 hand it a `UUID(...)`, and the traceback attributes 342 of the 379 `unsupported
operand` lines to one line, `packages/orchestration/data_paths.py:200`, which is
`jobs_dir(root) / job_id`. The hexadecimal-UUID class is the same value rejected from the
other side. 176 of the 306 `SystemExit` lines are attributed to
`packages/orchestration/data_paths.py:324`, the `no job matches prefix` exit, which is a
record written under one id spelling and looked up under the other.

The reading side of the same table is the `AttributeError` class, and it is now small
enough to enumerate: 46 lines are `str.value` at
`packages/orchestration/project_brain.py:317`, which is `task.status.value` where the
unified `status` is a `str` and no longer an enum; 23 are `str.hex` at
`packages/orchestration/task_runner.py:480`, which is `result.task_id.hex[:8]` where the
unified id is a `str` and no longer a `UUID`; 33 are `Mission.job_id`; 12 are
`Artifact.job_id`.

A SECOND CAUSE IS SMALLER AND IS NOT THE SAME ONE: `JobPlan` is a dataclass and the classic
`Job` is a pydantic model, so `model_dump`, `model_dump_json` and `model_copy` do not exist
on the flipped receiver. That is 13 lines naming `JobPlan.model_dump_json` and a further 12
attributed inside pydantic itself. No rename of a FIELD reaches a METHOD call.

## 7. `TaskEntry.acceptance_checks` is the one class ALREADY RULED, and the ruling holds

25 exception lines, and two production construction sites —
`packages/orchestration/flight_plan.py:523` and
`packages/orchestration/mission_state.py:760`. `dataclasses.fields(TaskEntry)` does not
hold `acceptance_checks`, and `Job`'s companion `Task` declares it as a
`list[AcceptanceCheck]`, so the classic record carries a structured value the unified
record has nowhere to put.

THIS NEEDS NO NEW RULING AND NO NEW ID HERE. DECISION F275 D22 already measured this exact
pair, ruled that the `TaskEntry` widen does NOT carry `acceptance_checks` because
`TaskEntry.acceptance` holds the acceptance text and the mapping is lossy in the direction
the flip travels, and placed the obligation precisely: "the flip round registers the
structured form as a finding naming the feature that owns acceptance criteria", under
operator amendment amend0908-f275-finish rule 4. This dry run CONFIRMS the premise that
ruling rests on and moves nothing: the flip round owes the finding, this round does not,
and no second id is minted for a defect the record already routes — the duplicate rule of
`docs/agents/planner_reviewer_prompt.md` §3 item 30. D22's other two clauses are landed:
`dataclasses.fields(TaskEntry)` holds both `output_artifact_ids` and `budget` at
`08feacae`, which is the widen that decision ordered first.

## 8. The instrument, and exactly which of these figures it reproduces

The two suite runs are not reproducible in a round; the readings that DECIDE this artefact
are, and they are what the instrument takes. It reads the shipped classes by importing
them and resolves every site by `ast` over the files `git ls-files '*.py'` names. Run from
the repository root with `python3 -B`; it writes nothing. Its source is committed verbatim
and fenced at `.agent/authored/f275-r55-instr.py.md`, because a `.py` file anywhere `ruff
check .` scans is counted by `tests/orchestration/test_ci_budgets.py` and turns the
lint-ceiling test red.

WHAT IT REPRODUCES, and the list is exact: section 6's whole field-type table, the
dataclass-against-pydantic reading and the three absent `model_*` methods; section 7's
`TaskEntry` verdict; section 5's binding-shape enumeration, including the sixteen-of-37
figure D2 and D3 turn on and the classic keys those tables carry; and the 73 `uuid4()`
constructions section 6 attributes the largest class to, which it reads at the base as
`Job.id = uuid4()` because the flip renames that keyword without retyping its value.

WHAT IT DOES NOT REPRODUCE, stated rather than left to be discovered: the owner-resolution
split of section 3 — 407, 1734, 56 and 1 — is derived from the ruled site set and the two
round 53 probe runs, which live in the reviewer's gitignored scratch and were never
committed, exactly as `.agent/f275_t003_descriptor_sites.md` section 2 says of its own
enumerations. Reproducing those four figures costs the two twenty-one-minute probe runs
that artefact records. Nor does it reproduce any figure of section 2 or section 4, which
are readings of the two suite runs.

## 9. What this reading does NOT settle

THE RESIDUE IS CLASSIFIED, NOT EXHAUSTED. The classes in section 4 account for 1031 of the
1364 matched E-lines, and 1364 is itself smaller than 1331 failures plus 79 errors, because
a failure whose line the pattern did not match is not counted. That remainder is given NO
numeral beyond the two totals, because none was measured.

THE 79 ERRORS ARE NOT DIAGNOSED HERE beyond the attribution section 6 gives their largest
line. They are consistent with a fixture raising before its test body runs, which is what
the earlier runs also reported, and that reading was not taken again.

WHETHER THE TYPE TABLE EXHAUSTS THE CAUSE IS NOT ESTABLISHED. Section 6 attributes the four
largest classes to it by traceback line and by the shipped field types; nothing here proves
a further cause does not appear once the types are carried, and the honest test of that is
another dry run.

THIS ARTEFACT RULES NOTHING ABOUT THE ROUTE. Whether the retype is a transform rule, a
widening of the unified record, or a decision that the flip is not one commit, is a choice
and belongs in `.agent/decisions.md`, not here.
