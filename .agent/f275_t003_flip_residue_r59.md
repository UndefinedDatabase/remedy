# F275 T003 — the re-keyed site set, its refusal precondition, and what the flip residue looks like once the drift is gone

> Measured by the reviewer at `bf692757`, this round's base, in three disposable `git
> worktree`s under the gitignored `.remedy-wt/`, all removed and pruned before this text was
> authored. THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it. It replaces
> none of `.agent/f275_t003_flip_residue.md`, `_r50.md`, `_r55.md` or `_r58.md`, which record
> the runs at `978046fe`, `020b1d57`, `08feacae` and `bf5ec6a4` and stay as written.

## 1. What this round built

DECISION F275 D34 part two orders two things and this round built both. The ruled site set
of `.agent/f275_t003_descriptor_sites.md` is re-keyed off line numbers, and the transform
gains a precondition that REFUSES to run on a stale set. Finding `R-0879` is the defect
both answer.

The re-key is a stage that sits BETWEEN the measured set and the transform rather than a
change to either. It reads the set at the commit it was measured at, re-expresses each site
by `(path, enclosing scope, attr, occurrence index of that attr inside that scope, in source
order)`, resolves that key against the tree the transform is about to run on, and emits the
set back in the `(path, line, col, attr)` form the transform already consumes. The transform
is therefore UNCHANGED, byte for byte, from the one round 58 ran: the only difference between
that run and this one is which site set it was handed, which is what makes the two runs
comparable at all.

## 2. The re-key, against the line key as its control

    $ python3 -B .remedy-wt/r59_rekey.py <old> <new> r53_R.json r55_owners.json out.json
    ruled sites in R                      : 2198
    recovered by (scope, attr, occurrence): 2198
    CONTROL, recovered by (line, col, attr): 2144
    UNRESOLVED                            : 0
    owners carried across                 : 2197
    REAL_EXIT=0

The old tree is `a815c9a3`, the commit `.agent/f275_t003_descriptor_sites.md` names as its
own base; the new tree is `bf692757`. The line key is run as the control in the same pass
over the same two trees, and it loses exactly the 54 sites round 58's drift measurement
found. That is what makes the first row a reading rather than a hope. One site of the 2198
carries no owner verdict and never did — it is the single `art` receiver round 58's run
also reported — so 2197 owners cross rather than 2198.

## 3. The precondition REFUSES, and that was proved by breaking it on purpose

A guard that has never been seen to fail is not a guard. In a fourth disposable worktree at
`bf692757` one enclosing function was renamed — `test_patch_intent_created_writes_event_with
_count_and_risks` in `tests/test_run_log_cli.py`, chosen because it HOLDS SIX RULED SITES,
which was measured before the mutation rather than assumed:

    recovered by (scope, attr, occurrence): 2192
    UNRESOLVED                            : 6
    THE PRECONDITION REFUSES. Unresolved ruled sites, by file:
          6  tests/test_run_log_cli.py
    REAL_EXIT=3

The first attempt at this control renamed a different function and the stage still exited 0,
correctly: that function held no ruled site, so nothing had gone stale. The control is
reported here as it was finally run, and the first attempt is reported because a mutation
that does not reach the property under proof is the failure mode this control exists to
avoid.

## 4. What the transform did with the re-keyed set

| reading | R58 | R59 |
|---|---:|---:|
| files rewritten | 262 | 262 |
| files left unparsable by the edit | 0 | 0 |
| `git diff --shortstat` insertions | 5182 | 5231 |
| `git diff --shortstat` deletions | 5009 | 5058 |
| changed files under `packages/` or `apps/` | 99 | 99 |
| changed files under `tests/` | 163 | 163 |
| `pytest tests/ -q --co` collected | 18409 | 18409 |
| collection errors | 0 | 0 |

THE TWO RENAME RULES RECOVER EXACTLY WHAT THE DRIFT HAD TAKEN. T2 job field reads 1786 and
T3 task field 411, against 1759 and 384 at round 58 — a gain of 27 on each, 54 together,
which is the drifted site count. Both figures also equal the run at `08feacae`, which is the
last run taken before round 57's migration moved the lines. No other rule count moved.

## 5. The run, against a control at the same commit

    $ python3 -B -m pytest tests/ -q --tb=line -p no:randomly -p no:cacheprovider
    CONTROL  1 failed, 18379 passed, 29 skipped, 1 warning in 1310.48s      REAL_EXIT=1
    FLIPPED  1240 failed, 17098 passed, 29 skipped, 1 warning,
             42 errors in 1299.61s                                          REAL_EXIT=1

Both runs were taken at `bf692757`, the control in a clean worktree and the flip in the
transformed one. Differencing the FAILED and ERROR node-id sets:

    shared failures (a worktree artifact, not the flip): 1
         tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes
    CAUSED BY THE FLIP: failures 1239  errors 42
    fixed by the flip (control-only): 0  errors 0

The one shared failure is the node that needs the gitignored `apps/ui/node_modules`.

| class, counted over `E <Exc>: <msg>` lines | R55 | R58 | R59 |
|---|---:|---:|---:|
| `TypeError: JobPlan.__init__() got an unexpected keyword argument 'X'` | 0 | 0 | 0 |
| `AttributeError: 'X' object has no attribute 'X'` | 127 | 424 | 135 |
| `TypeError: unsupported operand type(s) for /: 'X' and 'X'` | 379 | 90 | 90 |
| `ValueError: badly formed hexadecimal UUID string` | 194 | 223 | 223 |
| `SystemExit: N` | 306 | 337 | 337 |
| `TypeError: TaskEntry.__init__() got an unexpected keyword argument 'X'` | 25 | 25 | 25 |

THE THREE COLUMNS ARE NOT TAKEN AT THE SAME BASE and the table says so rather than implying
otherwise: R55 ran at `08feacae`, R58 at `bf5ec6a4` and R59 at `bf692757`. R58 and R59 differ only
in the site set, so those two columns ARE a difference; the R55 column is offered as
direction only.

## 6. THE DRIFT CLASS IS CLOSED, and that is the whole point of the round

Round 58 recorded 255 attribute-error lines on a `JobPlan` receiver and attributed 235 of
them to three files round 57 had edited. At this run the `JobPlan` receiver appears in that
class 18 times, and every one of the 18 is a pydantic-API read rather than a field read:

    JobPlan.model_dump_json  13
    JobPlan.model_dump        4
    JobPlan.model_copy        1

Those are the `model_dump`, `model_dump_json` and `model_copy` calls DECISION F275 D32's
"WHAT THIS DECISION DOES NOT RULE" paragraph names as a smaller, separate cause. Not one
line of the 255 survives as a field read. Section 6 of `.agent/f275_t003_flip_residue_r58.md`
recorded that re-keying was proved to recover the SITES and that nothing had re-run the
suite against a re-keyed transform; this run is that re-run, and the answer is that the
failures fall by 236 and the errors do not move.

## 7. THE DEFECT THIS RUN FOUND, and it is the mirror image of the last one

**THE RULED SITE SET OVER-SELECTS: IT RULES SITES WHOSE RECEIVER IS NOT A JOB OR TASK RECORD
AT ALL.** Round 58's defect was a set that reached too few sites; this one is the same set
reaching too many. With the drift class gone these are no longer masked, and they are the
second-largest attribute-error class in the run:

    Artifact.job_id    25        BrainNode.task_id   1
    Mission.job_id     33        BrainNode.job_id    1
    QueueEntry.job_id   5        _FakeJob.job_id     1

Sixty-six E-lines, at 13 located frames of which 12 are in this repository and the
thirteenth is pydantic's own `main.py:1042`. The clearest single instance is in
`packages/orchestration/loop_run.py`, where one line carries both a correct rename and an
incorrect one:

    -        link_job_to_mission(project_id, mission.id, str(job.id),
    +        link_job_to_mission(project_id, mission.job_id, str(job.job_id),

THAT LINE IS 285 AT `bf692757` AND 286 IN THE FLIPPED TREE, because rule I5 inserts a
minter import above it, and the traceback frame therefore reads 286 while the base file
reads 285. Both numbers are given rather than one, and this is not a pedantry: a residue
attributed by line number is attributed in the TRANSFORMED tree's coordinates, and reading
those numbers against the base is the same mistake as `R-0879` in the opposite direction.
Every other line number in section 8 below is likewise a frame of the flipped tree.

`job.id` → `job.job_id` is right. `mission.id` → `mission.job_id` is wrong: `Mission` is a
dataclass whose id field is `id`, read off the live class at `bf692757`, and it is not a
record the flip touches. THE CAUSE IS ATTRIBUTED, NOT DIAGNOSED: what is measured is that
the ruled set holds these sites with an owner verdict of `Job` while the runtime receiver is
another record. Whether that came from the static sweep's verdict, from the probe's line, or
from the receiver-name fallback the transform uses third is NOT established here, and the
next round that touches this set owes that reading before it edits anything.

This matters more than its size because the flip is ONE COMMIT that cannot be split. Twelve
wrong renames inside it are twelve defects landing in the one place this feature has no
second chance to correct.

## 8. What the remaining residue is attributed to

Counted over the `<path>:<line>: <Exc>: <msg>` location frames of the same `--tb=line`
report. This is a DIFFERENT reading from the class table in section 5, which counts
`E <Exc>: <msg>` lines, and the two do not agree to the unit — `SystemExit` reads 338 here
against 337 there. Both are reported as what they are.

    SystemExit                    338   data_paths.py:324 193 · brain.py:24 47 · brain.py:122 15
                                        brain.py:288 15 · repo.py:176 12 · brain.py:71 12
    unsupported operand /          96   data_paths.py:200 90
    badly formed hex UUID          87   uuid.py:177 87 (the stdlib frame; the callers are not
                                        resolved here)
    a `.value` read on a `str`     61   project_brain.py:317 54 · trust_report.py:119 7
    TaskEntry.acceptance_checks    25   mission_state.py:760 13 · flight_plan.py:523 12

THE `.status.value` FAMILY IS NOW THE LARGEST CLEANLY-ATTRIBUTED UNBUILT RULE, at 61 lines
over two source lines. It is the third of DECISION F275 D32's three rule families and the
one D34 records as needing its own descriptor-probe round of round 53's shape, because its
76 sites sit on ten receiver names of which five decide nothing by name.

`TaskEntry.acceptance_checks` at 25 is unchanged across all three runs and is not a
regression: DECISION F275 D22 already places it with the flip round as a finding naming the
inheriting feature.

## 9. What this reading does NOT settle

THE RESIDUE IS CLASSIFIED, NOT EXHAUSTED. The six classes of section 5 account for 810 of
the 1229 matched E-lines, and 1229 is itself smaller than 1239 failures plus 42 errors,
because a failure whose line the pattern did not match is not counted. That remainder is
given NO numeral beyond the two totals, because none was measured.

THE 42 ERRORS ARE STILL NOT DIAGNOSED. They did not move from round 58 and this round did
not attribute them either. An undiagnosed class that does not move is reported as
undiagnosed.

THE THREE LARGEST CLASSES ARE UNEXPLAINED BY ANY RULE THIS CHAIN HAS WRITTEN.
`SystemExit` at `data_paths.py:324` is the "no job matches prefix" exit and `unsupported
operand` at `data_paths.py:200` is the `jobs_dir(root) / job_id` join; both are reads of an
id whose SHAPE changed, and neither is a rename. Nothing here rules whether they are a
fourth rule family, a consequence of on-disk records written under the classic shape, or
both.

WHETHER THE OVER-SELECTION OF SECTION 7 IS CONFINED TO THE 12 SITES THE RUN REACHED IS NOT
ESTABLISHED. The run can only show sites the suite executes. A static reading of the ruled
set against the live record classes would bound the class, and this round did not take one.
