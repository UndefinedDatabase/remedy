# F275 T003 — the three sites rule three different ways, and the re-derived set is NOT safe

> Measured by the reviewer at `4de28049`, this round's base, in one disposable `git
> worktree` under the gitignored `.remedy-wt/`, removed and pruned before this text was
> authored. THIS FILE RECORDS A RULING; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, AS A LIST. Sections 2, 3, 4, 5 and 6 are re-derived in full by the committed
> instrument `.agent/authored/f275-r66-rule.py.md`, which is what this round's gate runs.
> ONE reading is the reviewer's own and is not in that instrument: the paired probe run of
> section 7, which needs a worktree and is quoted there with both its commands. Nothing
> else in this document is a reviewer reading.

## 1. What this round was given

DECISION F275 D39 re-derived the ruled site set with a receiver in its key and held the
write shut on THREE sites it could not justify. This round rules them. They rule three
different ways, and the third way is a systematic defect that reaches 22 of the 52 drops
the re-derivation makes — so the answer to "may the re-derived set be consumed" is NO, on
evidence the re-derivation itself could not see.

## 2. `tests/orchestration/test_repair_loop_v1.py:56` — a CORRECT drop

    source: '    return str(job.id), str(art.id), str(task.id)'
    sweep  col  15 .id           recv 'job'          static 'Job'   RULED True
    sweep  col  28 .id           recv 'art'          static None    RULED True
    sweep  col  41 .id           recv 'task'         static 'Task'  RULED True
    probe  Job.id           lasti  218 recv 'job'            direct True
    probe  Task.id           lasti  234 recv 'task'           direct True

Three `.id` reads on one line with three different receivers. The probe resolves `job` and
`task` and records nothing for `art`, because `art` is an Artifact and the probe installs
descriptors on `Job` and `Task` alone. The site at column 28 was ruled ONLY by sharing a
line with the other two. THIS IS EXACTLY THE OVER-SELECTION FINDING `R-0880` DESCRIBES, and
dropping it is the re-keying working as designed. RULED: the drop stands.

## 3. `packages/orchestration/long_run_executor.py:505` — the site was never ruled

    source: '                     job_id=str(queued_job.id))'
    sweep  col  30 .id           recv 'entry'        static None    RULED False
    probe  Job.id           lasti  408 recv 'queued_job'     direct True
    ast    .id           value Name       node col  32 end col  45

The sweep's site on line 505 carries receiver `entry` and column 30. The source's `.id` on
that line has receiver `queued_job` at column 32, and the probe agrees with the source. The
sweep is wrong about BOTH fields — and the site is `RULED False`, so it is not in round
53's committed set at all. It reached the drop list only because this round's rebuild
recomputes the set from the sweep's raw sites. RULED: not a drop, and not a defect of the
receiver join; a defect of the SWEEP, which section 4 then measures.

## 4. The 504 disagreement round 64 reported, diagnosed

    source: '    return QueuePull(entry_id=entry.id, status=QUEUE_PULL_PLANNED,'
    sweep  col  19 .id           recv 'entry'        static None    RULED True
    sweep  col  40 .id           recv 'queued_job'   static None    RULED True
    ast    .id           value Name       node col  30 end col  38

The instrument prints no `probe` line for that block at all, because the re-keyed run
recorded no row on line 504.

ONE attribute node, at column 30, with receiver `entry`. The sweep placed TWO sites on the
line, at columns 19 and 40, and gave the second of them the receiver `queued_job` — which
belongs to the NEXT line, inside the same multi-line call. So round 64's unexplained
"2 ruled sites against 1 ast node" is the sweep recording positions that do not correspond
to the nodes it was reading, inside a call expression that spans two lines. The `:505`
entry of section 3 is the same defect seen from the other end.

THE REACH OF THAT DEFECT IS MEASURED RATHER THAN GUESSED:

    ruled keys                                        : 2198
    resolving to an ast Attribute at that exact position: 2144
    NOT resolving there                               : 54

FIFTY-FOUR RULED KEYS POINT AT NO ATTRIBUTE NODE. Any consumer that walks the tree and
looks a node up by `(path, line, col, attr)` misses every one of them — silently, because a
lookup that finds nothing is indistinguishable from a site that was never ruled. That is an
UNDER-selection, which is finding `R-0879`'s class, and it is independent of everything the
receiver key does.

## 5. `tests/orchestration/test_loop_run.py:285` — a WRONG drop, with a systematic cause

    source: '    assert link.job_id == str(outcome.job.id)'
    sweep  col  30 .id           recv 'job'          static None    RULED True
    probe  Job.id           lasti   72 recv '@py_assert6'    direct True
    ast    .job_id       value Name       node col  11 end col  22
    ast    .id           value Attribute  node col  30 end col  44
    ast    .job          value Name       node col  30 end col  41

The probe resolved the receiver to `@py_assert6`. No such name exists in the source. PYTEST
REWRITES `assert` STATEMENTS INTO TEMPORARIES BEFORE COMPILING THEM, and the probe reads
the frame of that REWRITTEN code, so the name it recovers by disassembly is one pytest
invented. It can match no sweep receiver, ever. The site is a genuine `Job.id` read and
dropping it is an under-selection. RULED: the drop is WRONG.

## 6. How far the rewriting reaches

    probe rows whose resolved receiver is synthetic: 24
    distinct synthetic names: ['@py_assert0', '@py_assert1', '@py_assert3', '@py_assert4', '@py_assert5', '@py_assert6']
    distinct lines they sit on: 24
    of those lines, beginning with `assert ` in the source: 24

    dropped sites                                  : 52
    of them on a line carrying a SYNTHETIC receiver: 22

EVERY ONE OF THE 24 SITS ON A LINE THAT BEGINS WITH `assert `, which is the mechanism
stated as a measurement rather than as a theory. TWENTY-TWO OF THE FIFTY-TWO DROPS ARE
CAUSED BY THE REWRITING AND NOT BY THE KEY. The re-derived set of DECISION F275 D39 is
therefore not safe to consume: its drop list is 52, of which 22 are under-selections, one
is the never-ruled site of section 3, and the rest are the class it was built to fix.

## 7. The fix, measured on one file

The reviewer ran the SAME committed probe over `tests/test_task_runner.py` twice, once as
round 65 ran it and once with pytest's rewriting disabled:

    $ python3 -B -m pytest tests/test_task_runner.py -p f275_r65_probe -q --tb=no \
          -p no:randomly -p no:cacheprovider
      REAL_EXIT=0   45 passed in 0.20s
      :65 Task.id lasti  50 recv '@py_assert4'      :291 Task.id lasti  36 recv '@py_assert4'
      :293 Task.id lasti 208 recv '@py_assert4'     :295 Task.id lasti 380 recv '@py_assert4'
      synthetic receivers in this run: 4   rows 20   resolved 18

    $ ... the same command with --assert=plain appended
      REAL_EXIT=0   45 passed in 0.18s
      :65 recv None    :291 recv None    :293 recv None    :295 recv None
      synthetic receivers in this run: 0   rows 20   resolved 14

`--assert=plain` DOES NOT RECOVER THE REAL RECEIVER AND IS STILL THE RIGHT FIX. The source
is `assert result.task_id == job.tasks[1].id`, whose receiver is `job.tasks[1]`, a
subscript — so the honest answer is a REFUSAL, and a refusal is what the plain run gives.
The four false names become four Nones, the row count is unchanged at 20, and under the
join a refusal keeps the site's old standing. A wrong name became an honest absence, which
is the direction that cannot cause an under-selection.

## 8. What this settles, and what it does not

SETTLED: the three sites rule as one correct drop, one never-ruled site that indicts the
sweep, and one wrong drop whose cause reaches 22 of the 52. The 504 disagreement is
diagnosed as the sweep recording positions inside a multi-line call that do not correspond
to its nodes, and that defect is measured at 54 ruled keys repo-wide. The re-derived set is
NOT safe to consume and DECISION F275 D40 keeps the write shut.

NOT SETTLED. The paired run of section 7 is ONE FILE and FOUR ROWS; it establishes the
mechanism and the direction of the fix, and it does NOT measure what a whole-suite plain
run would give. The 54 non-resolving keys are measured but not repaired, and no round has
yet asked whether the transform's own consumption of those keys already loses them. Nothing
here re-derives the set — that is the next round, and it needs two more probe runs.
