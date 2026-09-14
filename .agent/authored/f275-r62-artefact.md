# F275 T003 — `R-0880` bounded statically, and its cause found in the probe's own key

> Measured by the reviewer at `7910aa7d`, this round's base, from the committed site set
> and its provenance rather than from a run. NO WORKTREE WAS CREATED and no suite was run:
> every figure here is derived from `.agent/f275_t003_descriptor_sites.md`'s own data and
> from the two committed instruments. THIS FILE REWRITES NOTHING. No line under
> `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.

## 1. What was owed

`R-0880` records that the ruled site set OVER-selects: it rules reads whose receiver is not
a job or task record, and the flip would rename them inside the one commit this feature
cannot split. It was raised from a RUN, so it named only what the suite executed — 12
located frames — and the finding itself calls that a floor rather than a count. Its own fix
clause binds two obligations on the round that takes it, and this round takes the FIRST:
bound the class statically, so the over-selected sites are known rather than only the ones
a run happens to reach.

## 2. THE CAUSE, and it is in the key the probe records

The DECISION F272 D7 descriptor probe records a read as `(owner, field, mode, path, LINE,
function)`. IT RECORDS NO COLUMN. Round 53 then matched each probe row against the
attribute nodes of that line to build the ruled site set. Where a line holds TWO attribute
nodes of the same name on DIFFERENT receivers, one proof ruled BOTH — and the second
receiver was never proved to be anything at all.

The instance `R-0880` was raised from is exactly this shape, and the site set says so in
its own data:

    packages/orchestration/loop_run.py:285 col=40 attr=id recv=mission owner=Job static=None
    packages/orchestration/loop_run.py:285 col=56 attr=id recv=job     owner=Job static=None

One line, two `.id` reads, two different receivers, ONE owner verdict, and `static=None` on
both — meaning neither came from the static sweep and both were claimed by the probe. The
probe saw `job.id`. It never saw `mission.id`. Round 53's matcher could not tell them apart
because the only key it had was the line.

THIS IS NOT A FAILURE OF THE PROBE'S METHOD. The probe proves what it proves: that SOME
receiver on that line was a classic `Job`. What was wrong is the inference drawn from it —
that therefore EVERY same-named attribute on that line was one — and that inference is
invisible on any line that holds only one such node, which is 2080 of the 2198 sites' lines.

## 3. THE BOUND

    ruled sites                                                   2198
    distinct (path, line) they occupy                             2080
    lines carrying MORE THAN ONE ruled site                        104
    ruled sites on such a line                                     222
    lines where >1 ruled site shares ONE owner verdict across
      DIFFERENT receiver names — THE AT-RISK CLASS                  39
    ruled sites on those lines                                      78

Every one of the 39 at-risk lines carries exactly TWO ruled sites, so exactly one site per
line is the proved one and exactly one was ruled for free: **39 ruled sites were ruled
without proof, and the class is neither larger nor smaller than that.** The lower and upper
bounds coincide, which is why this is a bound rather than an estimate.

A SHARED LINE IS NOT BY ITSELF A DEFECT, and the arithmetic above turns on that distinction.
Of the 104 lines carrying more than one ruled site, 65 are fine: `job.id` and `task.id` on
one line are two receivers with two DIFFERENT owner verdicts, and each verdict is its own
proof. The defect is only where two different receiver names carry the SAME owner verdict.

By file, the 39 at-risk lines:

    6 test_mission_state.py · 4 test_loop_run.py · 2 test_project_brain.py
    2 test_repair_v1_cli.py · 2 test_watchdog.py · 2 test_repair_request_builder.py
    2 test_dag_schedule.py · and 1 each in test_cli_main.py, test_repair_runtime.py,
    mission_state.py, loop_run.py, test_self_dogfood_execution_cli.py,
    brain_detail.py, long_run_executor.py, test_runner.py, test_repair_request_cli.py

Four are in production modules and the rest are tests.

## 4. THE CROSS-CHECK, and it is what makes this a bound rather than a guess

The previous round's run reached the over-selection at four source frames. All four are
inside the static bound:

    packages/orchestration/loop_run.py:285            in the bound
    packages/orchestration/long_run_executor.py:504   in the bound
    packages/orchestration/brain_detail.py:345        in the bound
    packages/orchestration/mission_state.py:1074      in the bound

The run found the class from one direction and this reading bounds it from the other, and
the two agree. `brain_detail.py:345` is the instance that explains the run's
`BrainNode.task_id` lines: it reads `task = next((t for t in job.tasks if str(t.id) ==
node.id), None)`, where `t.id` is a genuine `Task.id` and `node.id` is a `BrainNode`, both
ruled `Task` from the one proof.

## 5. What this reading does NOT settle

IT DOES NOT SAY WHICH SITE OF EACH PAIR IS THE WRONG ONE. It says exactly one per line is
unproved; it does not say which, because the probe row that proved the line carries no
column to match against. Deciding each pair needs either a probe that records a column or a
per-pair reading of the kind round 60 used on the `.status` family.

IT DOES NOT FIX ANYTHING. No line moved, the site set is unchanged, and the transform still
consumes it as it stands. The second obligation `R-0880`'s fix clause names — the refusal,
so that a site whose owner verdict cannot be confirmed STOPS the run rather than being
renamed quietly — is not built here.

THE REMEDY IS NAMED BUT NOT MEASURED. Adding `col_offset` to the probe's recorded key is a
one-line change to a committed instrument and would make the match exact, at the cost of the
two twenty-one-minute runs a re-derivation needs. Whether the re-derived set differs from
the current one in any way OTHER than these 39 sites is not established, and nothing here
should be read as saying the rest of the set is sound merely because this class is bounded.

THE 39 ARE A BOUND ON THIS SET, NOT ON THE PROBLEM. A site set re-derived at a later commit
would have its own at-risk lines, and this figure describes the artefact measured at
`a815c9a3` and consumed at every commit since.
