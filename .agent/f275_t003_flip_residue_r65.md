# F275 T003 — the ruled site set, RE-DERIVED with a receiver in its key

> Measured by the reviewer at `98a67f4f`, this round's base, in one disposable `git
> worktree` under the gitignored `.remedy-wt/`, removed and pruned before this text was
> authored. THIS FILE RECORDS A RE-DERIVATION; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE. Every figure below is re-derived by the committed instrument
> `.agent/authored/f275-r65-rederive.py.md`, which reads the two probe runs and the round 53
> site data and is what this round's gate runs. The re-keyed probe itself is committed at
> `.agent/authored/f275-r65-probe.py.md`. TWO readings are NOT in the instrument's output
> and are the reviewer's own, taken at this base: the two pytest summary lines of section 2,
> which live in the run logs rather than in the probe JSON, and the four receiver-shape
> cases of section 3, which are a separate unit probe. Nothing else in this document is a
> reviewer reading.

## 1. What this round spent

DECISION F275 D38 ruled the route: `f_lasti` plus a disassembly, because this interpreter
has no frame column. This round SPENDS it. The descriptor probe's recorded key gains two
fields, the suite ran under it twice, and the ruled site set was rebuilt with the receiver
joined in. DECISION F275 D36's binding clause — no WRITE until the 39 are resolved or the
set is re-derived with a discriminating key — is discharged by the second of its two routes.

## 2. The two runs

| Run | pytest summary | probe rows |
|---|---|---|
| 1 | `2 failed, 18408 passed, 29 skipped, 1 warning in 1326.55s (0:22:06)` | 2195 |
| 2 | `1 failed, 18415 passed, 23 skipped, 1 warning in 1244.46s (0:20:44)` | 2195 |

    as the ROUND 53 key: run1 2145  run2 2145  symmetric difference 0
    as the ROUND 65 key: run1 2195  run2 2195  symmetric difference 0

THE SITE SET IS THE MEASUREMENT AND IT REPRODUCED UNDER BOTH KEYS. The two summary lines
are not required to agree and are not gated on, for the reason
`.agent/f275_t003_descriptor_sites.md` already gives: a cold worktree fails
`test_vitest_passes` for the gitignored `apps/ui/node_modules`, and the run after it finds
that dependency resolved, which moves tests between skipped and passed. The re-keyed probe
is therefore exactly as reproducible as the one it replaces, which is the precondition for
using it at all.

## 3. What the resolution did, and what it refused

    rows 2195   receiver RESOLVED 2082   REFUSED 113
      refused with direct=False: 2
      refused with direct=True: 111

A refusal is never a guess. Before the suite ran, the resolution was put against four
receiver shapes in a separate unit probe, with the bare name as a CONTROL that must
succeed: `job.id` resolved to `job`, and `outcome.job.id`, `nodes[0].id` and `loader().id`
each returned nothing. A resolution that never refuses is a resolution that guesses, and
the 111 direct refusals are that behaviour at suite scale.

## 4. The ambiguity the old key hid, enumerated

Of the 2145 distinct round 53 keys the run produced, exactly TWELVE cover more than one
resolved receiver — these are the reads where ONE probe proof used to rule two sites:

    tests/orchestration/test_loop_run.py:340 Job.id read -> ['@py_assert4', 'newer']
    tests/orchestration/test_loop_run.py:354 Job.id read -> ['found', 'mine']
    tests/orchestration/test_loop_run.py:384 Job.id read -> ['@py_assert5', 'found']
    tests/orchestration/test_loop_run.py:396 Job.id read -> ['@py_assert5', 'found']
    tests/orchestration/test_mission_state.py:837 Job.id read -> ['job_one', 'job_two']
    tests/test_storage.py:33 Job.id read -> ['job', 'loaded']
    tests/test_storage.py:78 Job.id read -> ['j1', 'j2']
    tests/test_storage.py:34 Job.name read -> ['job', 'loaded']
    tests/orchestration/test_dag_schedule.py:153 Task.id read -> ['c', 'mid']
    tests/orchestration/test_dag_schedule.py:161 Task.id read -> ['independent', 'legacy']
    tests/test_cli_main.py:500 Task.id read -> ['t', 'task']
    tests/test_runner.py:133 Task.id read -> ['@py_assert0', 'existing_task']

TWELVE IS THE NUMBER FINDING `R-0880` WAS RAISED WITH. D36 recorded that the finding "was
raised from a RUN, so it named the 12 located frames the suite reached and called that a
floor", and bounded the class STATICALLY at 39. Both numbers are right and they count
different things: 39 is every at-risk line in the ruled SET, and 12 is the subset a run
can see. The re-keyed probe now separates all twelve by construction.

## 5. The control, which is what makes the rebuild a re-derivation

    round 53 probe rows 2145   its line keys 2145
    rebuilt under the LINE join: 2198   round 53's own R: 2198
    SET-EQUAL to round 53's R: True

The rebuild is fed ROUND 53's OWN probe output and its LINE join, and it reproduces round
53's committed ruled set exactly — not merely in cardinality but as a SET. Without that
reading every number in the next section would be a number about some other join that
happens to resemble the committed one. This control was added because the first attempt at
this rebuild did NOT reproduce it, and the reason turned out to be the input rather than
the logic.

## 6. The re-derivation

    round 65 probe, LINE join     : 2168
    round 65 probe, RECEIVER join : 2116
    line-join drift from round 53's set: 32  (the tree moved between the two commits)
    the RECEIVER join DROPS 52 and ADDS 0

THE ONE-VARIABLE COMPARISON IS 2168 AGAINST 2116, both built from the SAME probe run by the
SAME rebuild, differing only in the join. The drift of 32 from round 53's set is a
different thing entirely and is stated separately so the two cannot be added: this branch
has committed many rounds since round 53 and the reachable set moved with it.

Where the probe REFUSED a receiver on a line, a site on that line keeps its old standing.
A refusal is an absence of evidence, not evidence of absence, and turning one into a strike
is finding `R-0879` arriving from the other side.

## 7. Is every drop justified?

    dropped total                                   : 52
    on one of the 39 at-risk lines D36 bounded      : 31
    the sweep recorded NO receiver for it at all    : 23
    both of the above                               : 5
    NEITHER, so justified by nothing stated so far  : 3

    packages/orchestration/long_run_executor.py:505 col 30 .id  sweep receiver 'entry'
    tests/orchestration/test_loop_run.py:285 col 30 .id         sweep receiver 'job'
    tests/orchestration/test_repair_loop_v1.py:56 col 28 .id    sweep receiver 'art'

FORTY-NINE OF THE FIFTY-TWO ARE ACCOUNTED FOR by D36's own class or by the sweep having no
receiver to match against. THREE ARE NOT, and they are named rather than absorbed. Each is
a site the sweep DID name a receiver for, on a line the probe reached, where the probe
named a different one. That is either a correct drop — the probe proved someone else — or
an under-selection of the kind `R-0879` records, and this artefact does not decide which.
`long_run_executor.py:505` sits one line below the `:504` anomaly
`.agent/f275_t003_flip_residue_r64.md` section 6 reports and does not diagnose, and `art`
is one of the receiver names DECISION F275 D29's P1 exists to decide nothing about.

Against D36's own 39 lines: of their 78 ruled sites, 31 are dropped, 45 remain in the
receiver-join set, and 2 are in neither round 65 set because the tree moved. 38 of the 39
lines were reached by the suite and one was not.

## 8. What this settles, and what it does not

SETTLED: the ruled site set is re-derived with a key that discriminates the receiver, the
re-keyed probe reproduces as a set across two runs, the rebuild reproduces the committed
set under a control, and the twelve run-visible ambiguities are separated. DECISION F275
D36's second escape route is taken.

NOT SETTLED, and stated rather than implied. THE THREE SITES OF SECTION 7 ARE UNRULED and
DECISION F275 D39 holds the write shut until they are. The re-derived set is NOT yet what
the transform consumes — no instrument was pointed at it this round, and the flip's dry run
was not re-run. The `long_run_executor.py:504` disagreement from round 64 is still
undiagnosed. And the 113 refusals are a REFUSAL rather than a resolution: the sites behind
them keep their old standing by design, which is safe for an over-selection and says
nothing about whether any of them should have been ruled at all.
