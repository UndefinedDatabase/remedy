# F275 T003 — the owner check's refusal set, shrunk and gated by a per-site control

> Measured by the reviewer at `ae84d89c`, this round's base, in a disposable `git worktree`
> under the gitignored `.remedy-wt/` that the instrument itself creates, uses and removes;
> its last banner reads `git worktree list` and `git status --porcelain` back afterwards.
> THIS FILE RECORDS A MEASUREMENT; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, STATED AS A SHAPE. EVERY INDENTED LINE IN THIS FILE is a verbatim excerpt of
> the output of the committed instrument `.agent/authored/f275-r72-instrument.py.md`, which
> is what this round's gate runs. Every figure in the PROSE that the instrument does not
> print is one of exactly two kinds, and each names its own source in the sentence that uses
> it: a CITATION of a named decision, finding, section or specification; or a figure of one
> of the TWO DISCARDED DRAFTS of this round's own stage, which come from the reviewer's dry
> runs and are the subject of that sentence rather than its evidence.

## 1. What DECISION F275 D45 left owed

D45 narrowed `R-0880`'s second obligation from "cannot be confirmed" to "is contradicted",
and made the leftover a PRECONDITION rather than an inheritance: the flip round may not be
taken until the refusal set has been shrunk far enough that the guard's reach fairly
approximates the ruled set, or the residual has been ruled acceptable in a dated decision
that states the count it accepts. D45 also named the route — of the 999 sites it recorded as
refused, 787 were receivers no binding in scope resolved — so the gain was in resolution
power and not in a new rule family. This round takes that route.

## 2. Is the narrow mode really the round 71 method?

          every class EQUAL                              : True
          the contradicted SITE LISTS are identical      : True

THE COMPARISON IS ANCHORED TO THE ARTEFACT ROUND 71 SHIPPED, not to this round's account of
it. Both columns below come from one file run in two modes, which is only meaningful if the
narrow mode is the round 71 reader; so the instrument first runs the COMMITTED round 71
stage beside `--narrow` over the same tree and the same ruled set, and reads the two banners
against each other class for class. They agree in every class and name the same four
contradicted sites. Every figure in the R71 column that follows is therefore the committed
stage's own.

## 3. The two stages over the same tree and the same ruled set

                                                              R71      R72    delta
          ruled sites                                        2198     2198       +0
          CONFIRMED                                          1195     1861     +666
          CONTRADICTED                                          4       13       +9
          DECIDED                                            1199     1874     +675
          REFUSED, the stated blind spot                      999      324     -675
            of which: class not statically bound              787      107     -680
            of which: receiver is not a bare name             113      113       +0
            of which: annotation carries no class id           99      104       +5

SEVEN RESOLUTION RULES ACCOUNT FOR THE DIFFERENCE AND EVERY ONE REFUSES ON AMBIGUITY: a
cross-file table of functions whose return annotation names a live record class; a function
with no return annotation whose every `return` returns one live constructor; container field
element types, so `for t in job.tasks` resolves against `Job.tasks` on the receiver's own
class and never by field name globally; PEP 604 unions and mapping subscripts; `with ... as`
and the walrus; aliases, to a fixed point; and file-wide agreement, which resolves a
receiver no enclosing scope binds only when every scope in the file that binds that name
binds it identically. Wherever a rule can yield two different live record classes for one
name it yields nothing and the site stays refused.

The row that moves the wrong way is the third refusal class, which grows by five. Those are
sites the widening newly BINDS, to something the record-class test then rejects — a receiver
now resolved to `Any` or to a container is a site the method has decided it cannot use, not
a site it lost.

## 4. The control that makes the shrink a reading

          sites the R71 method DECIDED                     : 1199
          sites the R72 method DECIDED                     : 1874
          of R71's decisions, sites R72 no longer decides  : 0
          of R71's decisions, sites R72 decides DIFFERENTLY: 0
          EVERY SITE R71 DECIDED, R72 DECIDES THE SAME WAY : True
          sites R72 decides that R71 refused               : 675
          that count equals the fall in REFUSED            : True

A SMALLER REFUSAL SET IS NOT BY ITSELF A GAIN, and this is the half of the round that says
so. A resolver that binds a receiver wrongly does not announce itself by refusing more; it
announces itself by turning a decided site into a different decision, or into no decision at
all. TWO BANNERS OF COUNTS CANNOT SEE EITHER: a site that changed its mind and two sites
that swapped produce identical totals, and a loss of 327 correct decisions against a gain of
585 reports as "decided grew by exactly what refused lost", which is section 7's second
draft exactly. So the stage carries a `--dump` that writes its PER-SITE decision map, and
the instrument diffs the two maps site by site. Nothing R71 decided is dropped, nothing is
decided differently, and the 675 sites that moved came out of the refusal set alone.

## 5. What the widening found

          NEW contradicted sites                           : 9
            packages/orchestration/long_run_executor.py:503 col 19 .id  receiver 'entry' holds QueueEntry  owner verdict Job
            packages/orchestration/loop_run.py:285 col 40 .id  receiver 'mission' holds Mission  owner verdict Job
            tests/orchestration/test_mission_state.py:420 col 47 .id  receiver 'mission' holds Mission  owner verdict Job
            tests/orchestration/test_mission_state.py:435 col 47 .id  receiver 'mission' holds Mission  owner verdict Job
            tests/orchestration/test_mission_state.py:450 col 47 .id  receiver 'mission' holds Mission  owner verdict Job
            tests/orchestration/test_mission_state.py:735 col 38 .id  receiver 'mission' holds Mission  owner verdict Job
            tests/orchestration/test_mission_state.py:885 col 38 .id  receiver 'mission' holds Mission  owner verdict Job
            tests/orchestration/test_watchdog.py:472 col 40 .id  receiver 'mission' holds Mission  owner verdict Job
            tests/orchestration/test_watchdog.py:890 col 38 .id  receiver 'mission' holds Mission  owner verdict Job
          each was REFUSED by R71, never CONFIRMED         : True

NINE SITES THE NARROW METHOD COULD NOT SEE, AND EVERY ONE IS REAL. Eight are `mission.id`
standing in the MISSION argument of `link_job_to_mission`, whose second parameter is the
mission id and whose third is the job id; the ninth is `entry.id` on a `QueueEntry`, reported
as `entry_id` beside a `job_id` built from a different receiver on the same line. The ruled
set names all nine with the owner verdict `Job`, so the flip would have renamed each to
`job_id` against the code's own reading. That is exactly the defect `R-0880` names, and until
this round the guard was silent on all nine.

## 6. The guard still refuses, and still passes

          contradicted sites parsed from the stage's own report: 13
          ruled set goes from 2198 to 2185
          THE DISCRIMINATOR, refuse against pass: exit 5 against exit 0
          CONFIRMED in the refuse case 1861 ; in the pass case 1861 ; EQUAL: True
          CONTRADICTED in the pass case: 0

The contract is unchanged from round 71: exit 0 means the ruled set may be consumed, exit 5
means it may not. The pass set is built by the instrument from the stage's OWN report rather
than written by hand, so the two runs cannot disagree about which sites the difference is,
and CONFIRMED reads 1861 in both, which is the control on the pair.

## 7. Two drafts that measured better and were wrong

THE FIGURES IN THIS SECTION ALONE ARE THE REVIEWER'S DRY RUNS OF DISCARDED CODE, not the
committed instrument's output, and they are the subject here rather than the evidence.

THE FIRST DRAFT REPORTED A REFUSAL SET OF 297 AND TEN CONTRADICTIONS, and three of those ten
were its own artefacts. It let every scope walk its nested definitions, and because a
module's span covers every line of its file, the module scope republished each function's
locals as file-wide bindings. The clearest artefact was a `for t in job.tasks` at
`packages/orchestration/proposed_tasks.py` resolved against a `for t in
load_proposed_tasks(...)` four hundred lines earlier in a different function, which reported
`ProposedTask` against an owner verdict of `Task` and called the agreement a contradiction.
The round 71 method contains the same leak and is saved from it only by binding too little
for it to matter.

THE SECOND DRAFT REPAIRED THE SCOPING AND REPORTED 741, AND ITS DEFECT IS THE ONE WORTH
KEEPING. Sound scoping cost 327 sites the R71 reader had decided correctly, because a name
bound in one function and used in a sibling function is exactly what the leak had been
connecting. Against 585 newly decided sites the net was +258, and every count-shaped check
passed: DECIDED grew by precisely what REFUSED lost. Only the per-site map diff of section 4
showed that 327 decisions had been destroyed to buy them. Rule G is the answer — unanimity
across a file's binding scopes, which reaches the consistent test file without reaching the
file that contradicts itself, and `proposed_tasks.py` line 721 is REFUSED under it rather
than decided wrongly.

The lesson is not that the drafts were wrong; drafts are. It is that the refusal count is
the number this round exists to reduce, and therefore the number least able to judge its own
reduction. 297 is a better-looking result than 324 by every measure the stage reports about
itself, and it was produced by the least sound of the three.

## 8. What this settles, and what it does not

SETTLED. The owner check's blind spot is 324 sites rather than 999, its decided set is 1874
rather than 1199, and it names nine defects it could not previously reach. The widening is
gated by a per-site property that a wrong resolver breaks, not by the size of its own output.

NOT SETTLED, AND `R-0880` STAYS OPEN BECAUSE OF IT. 324 sites remain undecided and the guard
is still silent on all of them; DECISION F275 D45's precondition is therefore NOT discharged
by this round, and the decision this round records does not rule the residual acceptable.
Its largest surviving class is 113 receivers that are not a bare name at all, which no
binding rule can reach — the route from here is a different method, not a further rule. The
id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse is still production
work no round has started.
