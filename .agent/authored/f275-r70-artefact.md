# F275 T003 — the round 69 instrument blob repaired, and `R-0880` bounded statically

> Measured by the reviewer at `aa200600`, this round's base, with disposable `git worktree`s
> under the gitignored `.remedy-wt/` that the instruments themselves create, use and remove;
> the last banner reads `git worktree list` and `git status --porcelain` back afterwards.
> THIS FILE RECORDS A MEASUREMENT; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, AS A LIST. Every figure in sections 2 through 4 is re-derived by the committed
> instrument `.agent/authored/f275-r70-instrument.py.md`, which is what this round's gate
> runs, and every indented block below is a verbatim excerpt of that instrument's output.
> NOTHING in this document is a reviewer reading taken outside it. The instrument's LAST
> banner is deliberately not quoted: it prints the branch tip, which moves as this round's
> own commits land.

## 1. What round 69 got wrong, stated plainly

Round 69 landed twelve commits and six of its seven gates passed. G5 went RED and the cause
was the reviewer's, not the worker's: the artefact `.agent/f275_t003_rekey_r69.md` quotes
thirty-four lines of instrument output, and the instrument blob landed beside it at
`.agent/authored/f275-r69-instrument.py.md` cannot produce five of them.

THE MECHANISM IS ORDINARY AND THAT IS THE POINT. The instrument was wrapped into its `.md`
carrier once; two banners were then added to the source; the carrier was never regenerated.
Every check that ran afterwards compared the artefact against the SOURCE's output, which was
correct, and nothing ever compared the CARRIER against the source it was made from. The
artefact was right. The blob was stale. The worker applied both byte for byte as constraint 1
required, reported the red gate rather than repairing a reviewer text to make it green, and
stopped — which is exactly the behaviour the constraint exists to produce.

## 2. The defect, reproduced against the blob round 69 landed

    landed instrument fence: 5887 B, 136 lines
    it runs: exit 0, stderr 0 B
    artefact lines quoted: 34
    lines it CANNOT produce: 5
      the re-key stage was landed at round 59: True
      the stage run below is byte-identical to that landed blob: True
      tracked files whose name holds 'flip_transform': []
      part 1 + part 2 == the transform run in banners 3 and 4: True
      joined source lines: 652
    unmatchable in order   : 5

THE STALE BLOB RUNS CLEANLY AND IS STILL WRONG. It exits 0 with an empty stderr and produces
a perfectly good report — of five banners instead of seven. That is what makes this class
hard to see: nothing fails, and the only symptom is an absence. The five lines are exactly
the two banners the source gained after the carrier was written.

## 3. The repair, against the corrected blob

    corrected fence: 7336 B, 166 lines
    it runs: exit 0, stderr 0 B
    artefact lines quoted: 34
    lines it CANNOT produce: 0
    unmatchable in order   : 0
    matched indices strictly increase: True
    THE DISCRIMINATOR, stale against corrected: 5 absent against 0

FIVE AGAINST ZERO, OVER THE SAME ARTEFACT AND THE SAME SWEEP. The round 69 artefact is not
amended and does not need to be: every line it quotes is real, and the corrected blob
produces all thirty-four in order. What this round changes is the blob, not the record.

One further change is to the source rather than to the process. The instrument previously
carried a literal markdown fence, which is why it could not be re-wrapped without a manual
edit; it now builds that marker from a character code, so the carrier can be regenerated
from the source at any time and the regeneration is what this round's tooling does before
every digest is taken.

## 4. Finding `R-0880`, first obligation — the static bound

`R-0880` says the ruled site set OVER-selects: it rules reads whose receiver is not a job or
a task record at all. Its fix clause binds two things on the round that takes it, and the
first is to bound the class STATICALLY, "because a dry run can only ever show the sites the
suite executes and 12 located frames is a floor rather than a count".

    === 1. LIVE CLASSES CARRYING id / name / description ===
      tracked .py files scanned: 994
      classes found            : 71
      job or task records      : ['Job', 'Task']
      OTHER records, the risk  : 69

    === 2. EVERY RULED SITE, AGAINST THE CLASS ITS RECEIVER HOLDS ===
       1010  agrees: job record, owner Job
        763  receiver's class not statically bound — REFUSED
        157  agrees: task record, owner Task
        111  receiver is not a bare name — REFUSED
         99  receiver annotated with no class identity — REFUSED
         54  site does not resolve at this tree (R-0879's 54)
          4  OVER-SELECTED: receiver is another record entirely
       2198  TOTAL

    === 3. THE BOUND — SITES WHOSE RECEIVER IS NOT THE RECORD THE OWNER CLAIMS ===
         3  Artifact                     defined in packages/core/models.py
         1  Mission                      defined in packages/orchestration/mission_state.py
         4  TOTAL statically confirmed over-selected sites

FOUR CONFIRMED, AND NINE HUNDRED AND SEVENTY-THREE THE METHOD CANNOT DECIDE. The second
number is the honest half of this reading and it is reported first in importance: 763 sites
have a receiver no binding in scope resolves, 111 have a receiver that is not a bare name at
all, and 99 are annotated with something carrying no class identity — `Any` above all, which
is the most common annotation on a job parameter in this repository. So this pass CONFIRMS
the defect statically and does NOT bound it from above. `R-0880` asked for a bound because a
dry run undercounts; a static pass that refuses 44 percent of its input undercounts too, in a
different direction, and saying so is the reading.

    packages/orchestration/mission_state.py:1074 col 36 .id  receiver 'mission' holds Mission  owner verdict Job
    tests/cli/test_repair_request_cli.py:27 col 28 .id  receiver 'fa' holds Artifact  owner verdict Job

THE TWO RECORDS IT NAMES ARE BOTH ON `R-0880`'S OWN LIST. The finding recorded `Mission.job_id`
at 33 exception lines and `Artifact.job_id` at 25 from the dry run; this pass reaches one
Mission site and three Artifact sites by a completely different route, which is the
corroboration a second method is for. It reaches none of the `QueueEntry` or `BrainNode`
sites the dry run found — those receivers are among the 973 it refuses.

This probe's own first run was wrong in two ways and both are recorded here rather than
quietly fixed: it scanned only the files holding ruled sites, so it found neither `Job` nor
`Task` and reported 18 classes instead of 71; and it read the `Any` annotation as a record
class, which produced 99 false positives. Both were caught before this round was authored,
by running the probe rather than by reading it.

## 5. What this settles, and what it does not

SETTLED. The round 69 instrument blob is superseded by one that reproduces the artefact it
was landed beside, and the defect is demonstrated against the stale blob rather than merely
described. `R-0880`'s first obligation has a result: four statically confirmed over-selected
sites, two record classes, both already on the finding's list, and a blind spot of 973 sites
stated as a count rather than as a caveat.

NOT SETTLED. `R-0880` stays OPEN: its SECOND obligation — give the transform a refusal for a
site whose owner verdict cannot be confirmed against the receiver's own record — is unbuilt,
and this round deliberately does not build it, because a refusal keyed on a method that
refuses 973 of 2198 sites would stop every run it is given. That is the next round's problem
and it is now stated in the terms that make it tractable: the refusal needs a decision
procedure with a much smaller refusal set, or it needs to fire only on the sites the static
pass CONFIRMS. The id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse is
still production work no round has started.
