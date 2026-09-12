# F275 T003 — `R-0880`'s second obligation, built at the reach its method actually has

> Measured by the reviewer at `3c59e51b`, this round's base, in a disposable `git worktree`
> under the gitignored `.remedy-wt/` that the instrument itself creates, uses and removes;
> its last banner reads `git worktree list` and `git status --porcelain` back afterwards.
> THIS FILE RECORDS A MEASUREMENT; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, AND IT IS NARROWER THAN THE ONE ROUND 70 WROTE. Every INDENTED line in sections
> 2 through 5 is a verbatim excerpt of the committed instrument
> `.agent/authored/f275-r71-instrument.py.md`, which is what this round's gate runs. The PROSE
> additionally cites figures from `R-0880`'s own registration and from round 70's artefact,
> and names that source in the sentence that uses it — round 70's provenance sentence claimed
> every figure in a range came from its instrument while four of its prose figures came from
> the finding's dry run, which is the slip this wording exists to avoid repeating.

## 1. What the finding asks, and why it cannot be met as written

`R-0880`'s fix clause binds two obligations. The first — bound the over-selection STATICALLY
— was measured at round 70. The second is this: "give the transform the same shape of refusal
`R-0879` gave it, so that a ruled site whose owner verdict CANNOT BE CONFIRMED against the
receiver's own record STOPS the run and is named, rather than being renamed quietly."

TAKEN LITERALLY, THAT OBLIGATION IS UNMEETABLE, and the number that shows it is in section 4.
The static method cannot confirm 999 of the 2198 ruled sites — not because they are wrong,
but because no binding in scope resolves what class their receiver holds. A guard that stops
on every site it cannot confirm stops every run it is ever given. That is a guard that cannot
pass, which is the same defect as a guard that cannot fail wearing the other face, and item
33 of `docs/agents/planner_reviewer_prompt.md` §3 names both.

So this round builds the guard at the reach the method actually has: it stops on a site the
code CONTRADICTS, and it prints the count of what it refuses to decide. DECISION F275 D45
records that narrowing, what it costs, and who inherits the remainder.

## 2. The refuse case — the ruled set as the pipeline holds it

    ruled sites                 : 2198
    live record classes         : 71
    1195  CONFIRMED: the owner verdict matches the receiver's record
    4  CONTRADICTED: the receiver holds another record entirely
    DECIDED                     : 1199
    REFUSED, the stated blind spot: 999
    CONTRADICTED                : 4
    exit 5

    packages/orchestration/mission_state.py:1074 col 36 .id  receiver 'mission' holds Mission  owner verdict Job
    tests/cli/test_repair_request_cli.py:27 col 28 .id  receiver 'fa' holds Artifact  owner verdict Job
    tests/cli/test_repair_v1_cli.py:35 col 28 .id  receiver 'fa' holds Artifact  owner verdict Job
    tests/cli/test_repair_v1_cli.py:129 col 28 .id  receiver 'fa' holds Artifact  owner verdict Job

FOUR SITES STOP THE RUN AND ARE NAMED. `Mission` and `Artifact` are both on `R-0880`'s own
list from its dry run, which recorded `Mission.job_id` at 33 exception lines and
`Artifact.job_id` at 25 — figures from that registration and not from this instrument. The
guard reaches them by a completely different route, which is what a second method is for.

## 3. The pass case — the same stage, the same tree, the cleaned set

    contradicted sites parsed from the report: 4
    ruled set goes from 2198 to 2194
    owner table goes from 2197 to 2193

    ruled sites                 : 2194
    1195  CONFIRMED: the owner verdict matches the receiver's record
    DECIDED                     : 1195
    CONTRADICTED                : 0
    exit 0
    THE DISCRIMINATOR, refuse against pass: exit 5 against exit 0

EXIT 5 AGAINST EXIT 0, OVER THE SAME STAGE AND THE SAME TREE. The pass set is built by the
instrument from the stage's OWN report rather than written by hand, so the two runs cannot
disagree about which four sites the difference is. The confirmed count is 1195 in both,
which is the control on the claim: removing four contradicted sites must not change what the
method confirms, and it does not.

## 4. The blind spot, stated as a count and not as a caveat

    787  REFUSED to decide: receiver's class not statically bound
    113  REFUSED to decide: receiver is not a bare name
    99  REFUSED to decide: annotation carries no class identity
    the guard decides 1199 of 2198 and refuses 999

NINE HUNDRED AND NINETY-NINE SITES ARE UNDECIDED AND THE GUARD IS SILENT ON ALL OF THEM. That
is 45 percent of the ruled set. The largest class by far is a receiver no annotation, no
construction and no loop binding in scope resolves; the smallest is an annotation like `Any`,
which carries no class identity and is the most common annotation on a job parameter in this
repository. The guard is therefore a floor on the over-selection and never a ceiling, exactly
as round 70's bound was, and for the same reason.

Round 70's probe read these three classes at 763, 111 and 99 over the ROUND 53 committed set;
this stage reads 787, 113 and 99 over the RE-KEYED set. The difference is the 54 sites
`R-0879` covered: they did not resolve at all against the stale set and are decidable against
the re-keyed one, so 28 join the confirmed and 26 join the refusals.

## 5. What this settles, and what it does not

SETTLED. The pipeline now carries two refusal stages that guard different properties of the
same set: one refuses to EMIT a set whose keys have gone stale, and this one refuses to EMIT
a set whose owner verdicts the code contradicts. Both are landed as committed authored texts,
both are demonstrated beside the case that must fail, and neither edits anything.

NOT SETTLED, AND `R-0880` STAYS OPEN BECAUSE OF IT. The 999 undecided sites are a real
residual: the defect the finding names can still occur among them and nothing would stop it.
That is not work this round can finish, and pretending otherwise by resolving the finding
would hide the one number that matters. What it becomes instead is a PRECONDITION ON THE FLIP
ROUND, stated in DECISION F275 D45: the flip is one commit that AGENTS.md's declared-oversize
allowance lets this feature land exactly once, so the round that takes it must first either
shrink the refusal set or rule the residual acceptable on the record. The id-SHAPE seam
DECISION F275 D37 routed into T003's resolver collapse is still production work no round has
started.
