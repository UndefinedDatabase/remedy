# F275 T003 — the third retype rule family, built against nine sites, and the class it closes

> Measured by the reviewer at `5dfeeae6`, this round's base, in two disposable `git
> worktree`s under the gitignored `.remedy-wt/`, both removed and pruned before this text
> was authored. THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it. It replaces
> none of the earlier residue artefacts, which record the runs at `978046fe`, `020b1d57`,
> `08feacae`, `bf5ec6a4` and `bf692757` and stay as written.

## 1. What this round built

DECISION F275 D32 named three retype rule families. The first landed at round 58 and the
`.hex`/`.int` family turned out to be three test sites the flip rewrites anyway. This round
builds the THIRD — a read of `.value` on a status that is a `str` after the flip — against
the nine sites DECISION F275 D35 names, and re-runs the dry run to see whether rewriting
exactly those nine removes exactly the class they were attributed from.

Rule T8 deletes the `.value` suffix and moves nothing else:

    -            status=task.status.value, ref_id=tid,
    +            status=task.status, ref_id=tid,
    -            status_label = task.status.value
    +            status_label = task.status

THE SITE SET IS KEYED BY SCOPE AND NEVER BY LINE NUMBER. Finding `R-0879` is the record of
what a line-keyed set costs, and that lesson binds a set of nine exactly as it binds a set
of 2198. Each site is keyed by `(path, enclosing scope, occurrence index of the chain
inside that scope)` and resolved against the tree the transform is about to run on; a site
that fails to resolve stops the generator.

THE GENERATOR REFUSED ONCE, AND IT WAS RIGHT TO. Its first version keyed on the enclosing
scope and the occurrence of the `.status` ATTRIBUTE. That is ambiguous at
`brain_detail.py:380`, which reads `status=node.status or task.status.value` and holds TWO
`.status` nodes of which only one continues into `.value`; the generator reported
`2 '.status' nodes on that line, expected 1` and exited 3 rather than pick one. The unit
became the CHAIN `<expr>.status.value` instead, and all nine then resolved. A generator
that guesses there is a generator that renames the wrong receiver silently.

## 2. What the transform did

| reading | R59 | R61 |
|---|---:|---:|
| files rewritten | 262 | 263 |
| files left unparsable by the edit | 0 | 0 |
| `T8 status value read` | — | 9 |
| every other rule count | unchanged | unchanged |

The one extra file is `packages/orchestration/trust_report.py`, which no earlier rule
touched. Every other rule count is identical to round 59's run — T2 at 1786, T3 at 411, T7
at 74, 11, 6, 12, 2 and 1 — which is what makes the two runs a difference of ONE variable.

## 3. The run, against its control

    $ python3 -B -m pytest tests/ -q --tb=line -p no:randomly -p no:cacheprovider
    CONTROL  1 failed, 18379 passed, 29 skipped, 1 warning in 1310.48s      REAL_EXIT=1
    FLIPPED  1186 failed, 17152 passed, 29 skipped, 1 warning,
             42 errors in 1285.49s                                          REAL_EXIT=1

THE CONTROL IS ROUND 59'S, REUSED, AND THE REASON IS MEASURED RATHER THAN ASSUMED. A
control run is a property of the PRODUCTION TREE it runs against, and the git object ids of
`packages`, `apps` and `tests` are byte-identical at `bf692757`, where that control ran, and
at `5dfeeae6`, where this flip ran — `2f8a05b5d7c2`, `1dd43398c371` and `509ecf860ffb` at
both. Rounds 59 and 60 moved nothing outside `.agent/`. Re-running it would have spent
twenty-one minutes to reproduce a reading the tree identity already guarantees, and this
paragraph is the justification rather than a shrug.

Differencing the FAILED and ERROR node-id sets:

    shared failures (a worktree artifact, not the flip): 1
         tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes
    CAUSED BY THE FLIP: failures 1185  errors 42
    fixed by the flip (control-only): 0  errors 0

## 4. THE CLASS THE RULE WAS BUILT FOR IS AT ZERO

    `AttributeError: 'str' object has no attribute 'value'`
      at R59, located frames : 61   (project_brain.py 54 · trust_report.py 7)
      at R61, located frames :  0

Not reduced — GONE. Nine rewrites removed sixty-one exception lines, and the two source
frames round 59 attributed them to are the two that DECISION F275 D35 named from the
opposite direction. The prediction and the measurement agree, which is the whole reason
this round existed.

| class, counted over `E <Exc>: <msg>` lines | R58 | R59 | R61 |
|---|---:|---:|---:|
| `TypeError: JobPlan.__init__() got an unexpected keyword argument 'X'` | 0 | 0 | 0 |
| `AttributeError: 'X' object has no attribute 'X'` | 424 | 135 | 78 |
| `TypeError: unsupported operand type(s) for /: 'X' and 'X'` | 90 | 90 | 90 |
| `ValueError: badly formed hexadecimal UUID string` | 223 | 223 | 223 |
| `SystemExit: N` | 337 | 337 | 337 |
| `TypeError: TaskEntry.__init__() got an unexpected keyword argument 'X'` | 25 | 25 | 25 |

Total failures fall from 1240 to 1186. THE FOUR UNCHANGED ROWS ARE THE POINT OF THE TABLE
AS MUCH AS THE CHANGED ONE: this round touched nine `.status.value` reads and nothing else,
and the three largest classes did not move by a single line, which is what a rule family
built against a named site set should look like.

## 5. What is left, and what it is attributed to

    SystemExit                    337   an id SHAPE change, not a rename
    badly formed hex UUID         223   an id SHAPE change, not a rename
    unsupported operand /          90   an id SHAPE change, not a rename
    the `R-0880` over-selection    70   a field renamed on a record the flip does not touch
    TaskEntry.acceptance_checks    25   already placed with the flip round by DECISION F275 D22
    JobPlan pydantic API           18   `model_dump`, `model_dump_json`, `model_copy`

THE `R-0880` CLASS MOVED FROM 66 TO 70 AND THIS ROUND DID NOT ATTRIBUTE THE DIFFERENCE. The
receivers are `Mission.job_id` 33, `Artifact.job_id` 25, `QueueEntry.job_id` 5,
`BrainNode.task_id` 5, `BrainNode.job_id` 1 and `_FakeJob.job_id` 1; of these only
`BrainNode.task_id` moved, from 1 to 5. It is reported as unattributed rather than
explained, and the obvious guess — that T8 unmasked test paths that previously died
earlier — is a guess and is labelled one.

DECISION F275 D32'S THREE RULE FAMILIES ARE NOW ALL ACCOUNTED FOR. The id VALUE family
landed at round 58; the `.hex`/`.int` family was measured at round 58 to be three test
sites the flip rewrites anyway, and the two `str.hex` lines still in this run are those;
this round built the third. No further family of that kind is owed, and what remains is a
different shape of problem.

## 6. What this reading does NOT settle

THE RESIDUE IS CLASSIFIED, NOT EXHAUSTED. The six classes of section 4 account for 753 of
the 1173 matched E-lines, and 1173 is itself smaller than 1185 failures plus 42 errors,
because a failure whose line the pattern did not match is not counted.

THE 42 ERRORS HAVE NOT MOVED FOR THREE RUNS AND ARE STILL NOT DIAGNOSED. They were 42 at
`bf5ec6a4`, 42 at `bf692757` and 42 here. An undiagnosed class that is also a STABLE class
is worth naming as such: whatever causes it is untouched by everything these three rounds
built.

THE THREE LARGEST CLASSES REMAIN UNEXPLAINED BY ANY RULE THIS CHAIN HAS WRITTEN. `SystemExit`
at `data_paths.py:324` is the "no job matches prefix" exit and `unsupported operand` at
`data_paths.py:200` is the `jobs_dir(root) / job_id` join; both are reads of an id whose
SHAPE changed, and neither is a rename. Whether they are a fourth rule family, a consequence
of on-disk records written under the classic shape, or both, is the next question and this
round does not answer it.

NOTHING HERE SAYS THE FLIP IS READY. 1185 failures is not a landable state, and the point of
this run is that one named rule family closed one named class exactly as predicted — not
that the remainder is close.
