# F275 T003 — the owner check's residual, measured as a RISK and then ruled

> Measured by the reviewer at `f8fbe3b6`, this round's base, in disposable `git worktree`s
> under the gitignored `.remedy-wt/` that the instruments themselves create, use and remove;
> the last banner of each reads `git worktree list` and `git status --porcelain` back
> afterwards. THIS FILE RECORDS A MEASUREMENT; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, STATED AS A SHAPE. EVERY INDENTED LINE IN THIS FILE is a verbatim excerpt of
> the output of one of this round's two committed instruments —
> `.agent/authored/f275-r73-instrument.py.md`, called instrument A below, and
> `.agent/authored/f275-r73-risk.py.md`, called instrument B — which are what this round's
> gates run. Every figure in the PROSE that neither instrument prints is one of exactly two
> kinds, and each names its own source in the sentence that uses it: a CITATION of a named
> decision, finding, round, section, specification, commit or SOURCE LINE; or a figure of
> DECISION F275 D45's own record, which is where the residual was first counted. That list is
> longer than round 72's by the last two entries, because round 72's artefact enumerated four
> kinds and carried six — a commit identifier and a source line were both outside the list
> written to cover them. This clause was checked by running this round's own figure sweep
> against it before emission.

## 1. What DECISION F275 D45 left owed, and which of its two routes is left

D45 forbade the flip round to proceed until one of two things was true on the record: either
the refusal set had been shrunk far enough that the guard's reach fairly approximates the
ruled set, or the residual had been RULED ACCEPTABLE in a dated decision that states the count
it is accepting. Round 72 took the first route and carried the refusal set from 999 to 324.

THIS ROUND ESTABLISHES THAT THE FIRST ROUTE IS SPENT, AND THEN TAKES THE SECOND. Sections 2
through 5 are the evidence that further resolver work no longer finds defects. Sections 6
through 9 measure what the residual actually risks, which is what a ruling has to state.

## 2. The anchor — both stages come out of git

          the COMMITTED round 72 carrier : 19931 bytes, fences 1/1
          its extracted source           : sha256 b0108e5e316af922e411a8ca7be16c892f69e15de8e6b9623ca0078da8e18676
          every class EQUAL to the round 71 figures      : True

Instrument A extracts the round 72 stage from its COMMITTED carrier rather than reading a
scratch copy, so the comparison below is against the artefact round 72 shipped. The same
instrument re-runs the stage's `--narrow` mode and checks it still reproduces the round 71
reader class for class, which keeps the whole three-round chain anchored to one measurement
rather than to a succession of claims.

## 3. What RULE H reaches

                                                              R72      R73    delta
          ruled sites                                        2198     2198       +0
          CONFIRMED                                          1861     1908      +47
          CONTRADICTED                                         13       13       +0
          DECIDED                                            1874     1921      +47
          REFUSED, the stated blind spot                      324      277      -47
            of which: class not statically bound              107      107       +0
            of which: receiver not a bare name / expr         113       66      -47
            of which: annotation carries no class id          104      104       +0

RULES A THROUGH G ALL RESOLVE A NAME. The round 72 stage then refused outright any receiver
that was not a bare name, which left `job.tasks[0].id`, `result.job.id` and `load_job(...).id`
in the blind spot as a CLASS rather than as a difficulty. RULE H walks the receiver expression
instead of demanding it be a name — an attribute against its owner's field annotation, a
subscript against its container's element type, a call against the return table — refusing on
ambiguity like every rule before it and bounding its own recursion at a fixed depth, because a
resolver that never gives up is one whose wrong answers are unbounded too.

## 4. The soundness control, unchanged in form from round 72

          sites the shipped stage DECIDED                  : 1874
          sites this stage DECIDED                         : 1921
          of the shipped stage's decisions, now undecided  : 0
          of the shipped stage's decisions, now DIFFERENT  : 0
          EVERY SITE THE SHIPPED STAGE DECIDED IS UNCHANGED: True
          sites newly decided                              : 47
          newly decided, by verdict                        : {'CONFIRMED': 47}

The per-site decision maps are diffed rather than the counts compared, for the reason round 72
recorded and this round inherits: two banners of totals cannot tell a site that changed its
mind from two sites that swapped.

## 5. The reading that decides the round

          CONTRADICTED, shipped stage                      : 13
          CONTRADICTED, this stage                         : 13
          the contradicted SITE LISTS are identical        : True
          so the widening buys confirmations and no defect : True

ROUND 72'S WIDENING FOUND NINE DEFECTS; THIS ONE FINDS NONE. Forty-seven sites move out of the
blind spot and every one of them is a CONFIRMATION — the contradicted list is identical, site
for site, before and after. That is the shape of a method at the end of its yield: the sites a
better resolver reaches are the ones that were already going to be right. A third resolver
round would be cheap to write and there is no longer a reason to believe it would find
anything, so the remaining route is D45's other one.

## 6. What the residual is, split by the tree it lives in

          refused sites                                    : 324
          of them, in test files                           : 148
          of them, in production files                     : 176
          distinct production files                        : 30

THE RESIDUAL IS NOT THE RISK, and conflating them is what would make a ruling dishonest. The
flip round runs the full suite, and the transform renames `.id` to `.job_id` — a read that
raises `AttributeError` on any receiver that is not a job record, on any line the suite
executes. The record classes are pydantic models and no production class in this repository
defines `__getattr__` or `__getattribute__`, so there is no silent fallback for that read to
land in. So the sites that can hurt are the ones the guard cannot decide AND the suite does
not run. Of the 324, the 148 in test files break the very test that contains them; the 176 in
production files are what sections 7 through 9 measure.

## 7. The control, and the warm-up that had to come first

          warm-up failures: 14
          exit 0
          18416 passed, 23 skipped, 1 warning in 222.78s (0:03:42)
          control failures: 0
          warm-up failures the control no longer reproduces: 14
          control failures the warm-up did not have          : 0

A COLOUR WITH NO BASELINE IS NOT EVIDENCE, AND A FRESH WORKTREE'S FIRST RUN IS NOT A BASELINE.
A worktree carries no `apps/ui/node_modules` and no built dist, so its first suite run fails
the vitest foundation test and a varying subset of the command-channel door tests, and BUILDS
what the next run then finds in place. This instrument was wrong about that before it was
right: two earlier invocations took the first run as the control and got failure sets of ten
and then nine, with different members, which is not a baseline but a coin. So the first run is
now a WARM-UP whose failures are reported and discarded, and the control is the SECOND run.
The control is green — the whole suite at exit 0 — and every one of the warm-up's 14 failures
is gone from it, which is what makes the subtraction in section 9 mean anything.

## 8. Is the residual executed?

          refused production sites EXECUTED by the suite    : 176
          refused production sites NOT executed             : 0
          THE UNEXECUTED SET IS THE RISK SET, and it holds  : 0

EVERY ONE OF THE 176 IS RUN BY THE SUITE. The coverage data comes from the same instrumented
run that produced the control above, so the two readings describe one execution rather than
two, and the set the ruling has to worry about — refused by the guard and never executed — is
empty.

## 9. The probe — what a wrong guess actually costs

          packages/orchestration/ui_view_model.py:292
            before : focus_job_id = str(job.id)
            after  : focus_job_id = str(job.job_id_PROBE)
            failures NOT in the control                   : 46
              tests/cli/test_job_commands.py::TestJobFocusedSingleOrigin::test_child_job_demoted_zoom
            reverted byte-identically                     : True
            THE READING: control exit 0 against mutated exit 1, 46 new failures
          packages/orchestration/autorun.py:320
            before : _emit(data_dir, job.id, "source_context_injected", {
            after  : _emit(data_dir, job.job_id_PROBE, "source_context_injected", {
            failures NOT in the control                   : 2
              tests/orchestration/test_autorun.py::TestFixtureBuilderStructuredPatch::test_fixture_builder_creates_patch
              tests/orchestration/test_diff_parser.py::test_the_huge_diff_parses_inside_the_recorded_perf_budget
            reverted byte-identically                     : True
            THE READING: control exit 0 against mutated exit 1, 2 new failures

"EXECUTED" IS A STATEMENT ABOUT LINES AND A RULING NEEDS ONE ABOUT FAILURES. At two of the
refused production sites, in the same worktree and under the same instrumentation as the
control, the attribute is renamed to one nothing defines — which is what a wrong guess by the
flip looks like — and the suite is run again. The control is green, so each mutated run's exit
1 is the reading and the subtraction only names WHICH tests moved. ATTRIBUTION BY NAME IS THE
EVIDENCE HERE, not the counts: the first site's new failures name the job-focus view model and
the second's name autorun, which are the modules that were mutated.

Of the second site's two new failures only ONE is attributable. The other is the wall-clock
perf budget test, which is load-sensitive under coverage instrumentation and appears in the
warm-up's 14 as well; it is reported rather than filtered, because a probe that quietly drops
the failures it did not expect is a probe that has stopped measuring.

The two sites differ by a margin the ruling should not hide: one rename reddens 46 tests and
the other reddens exactly one. A residual site is caught, but the margin by which it is caught
varies, and a site whose only witness is a single test is one deletion away from unguarded.

## 10. What this settles, and what it does not

SETTLED, AND THIS IS WHAT DECISION F275 D47 RULES. The guard's blind spot is 277 sites after
RULE H. Of the 324 it was before, none lies outside the suite's reach: 148 are in tests that
break themselves and 176 are production lines the suite executes, with the unexecuted set
measured at zero. A wrong rename at such a site is caught, demonstrated rather than argued.
D45's precondition is therefore discharged by its SECOND route, with the count stated, and the
flip round may proceed — carrying one obligation, that the full suite is the backstop and must
run, which the integration gate already requires.

NOT SETTLED. `R-0880` STAYS OPEN: the guard is still silent on 277 sites, and a ruling that the
residual is survivable is not a claim that it is empty. The varying margin of section 9 is
real and is carried as a stated LIMITATION of D47 rather than absorbed into it; it spends no
finding id, because nothing on disk is wrong and amend0827-process-diet rule 2 reserves an id
for a defect with product effect. And nothing here touches the id-SHAPE seam DECISION F275 D37
routed into T003's resolver collapse, which is production work no round has started.
