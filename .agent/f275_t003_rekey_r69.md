# F275 T003 — the refusal reaches the transform, and the transform reaches the repository

> Measured by the reviewer at `7ac6ec87`, this round's base, with disposable `git worktree`s
> under the gitignored `.remedy-wt/` that the instrument itself creates, uses and removes;
> its last banner reads `git worktree list` and `git status --porcelain` back afterwards.
> THIS FILE RECORDS A MEASUREMENT; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, AS A LIST. Every figure in sections 2 through 6 is re-derived by the committed
> instrument `.agent/authored/f275-r69-instrument.py.md`, which is what this round's gate
> runs, and every indented block below is a verbatim excerpt of that instrument's output.
> NOTHING in this document is a reviewer reading taken outside it. The instrument's LAST
> banner is deliberately not quoted: it prints the branch tip, which moves as this round's
> own commits land, so a quotation of it would age the moment the next commit was written.

## 1. What `R-0879` still owed, measured rather than remembered

Finding `R-0879` has been open since round 58 and asks for two things: RE-KEY the ruled site
set off line numbers, and make the run REFUSE when its set has gone stale, "because the
defect is not that a key drifted — keys drift — but that nothing noticed".

THE FIRST HALF WAS ALREADY DONE, and this round checked that rather than assuming it.

    the re-key stage was landed at round 59: True
    the stage run below is byte-identical to that landed blob: True

DECISION F275 D34 part two ordered the re-key, round 59 built it AND landed it at
`.agent/authored/f275-r59-rekey.py.md`, and the stage this round exercises is byte-identical
to that committed blob. An earlier draft of this round was written on the belief that the
stage lived only in scratch; that belief was wrong and the reading above is why it is not in
this document.

THE SECOND HALF WAS NOT DONE, AND THE REASON IS SHARPER THAN "UNFINISHED". The refusal round
59 built guards the STAGE's output. The finding's own words are "the TRANSFORM refuses to
run", and the transform had no guard at all — so a run that skipped the stage and handed the
committed set straight to the transform reintroduced the defect in full. Round 68 took
exactly that route as a control and measured 54 renames lost with nothing said. And the
transform was in no position to be fixed, because:

    tracked files whose name holds 'flip_transform': []

THE MOST LOAD-BEARING INSTRUMENT OF T003 HAS NEVER BEEN COMMITTED. Every flip dry run from
round 46 to round 68 was taken with a file that exists only in a gitignored scratch
directory. That is not a second finding — it is the reason the second half of `R-0879` could
not be closed — and this round ends it.

## 2. The repair, and the control that makes it a reading

    ruled sites in R                     : 2198
    recovered by (scope, attr, occurrence): 2198
    CONTROL, recovered by (line, col, attr): 2144
    UNRESOLVED                            : 0
    owners carried across                 : 2197
    exit 0
    SET-EQUAL to the set the transform has consumed since round 61: True

TWO THOUSAND ONE HUNDRED AND NINETY-EIGHT AGAINST THE LINE KEY'S 2144. The scope key and the
line key are run over the same two trees in the same pass, so the 54 the line key loses are
measured rather than asserted, and the re-derived set is SET-EQUAL to the one the transform
has consumed since round 61 — which makes that set reproducible from committed inputs.

## 3. The repair's red control — one scope renamed

    occurrences of the target def in packages/orchestration/ui_server.py: 1
    ruled sites in R                     : 2198
    recovered by (scope, attr, occurrence): 2178
    UNRESOLVED                            : 20
    THE PRECONDITION REFUSES. Unresolved ruled sites, by file:
    exit 3
    an output set was written anyway: False
    20  packages/orchestration/ui_server.py

A KEY THAT CARRIES NO LINE NUMBER IS NOT A KEY THAT CANNOT BREAK. Renaming the one scope
enclosing the most ruled sites of any single function — `_handle_command_submission`, which
occurs exactly once in its file, so the mutation names a target rather than describing one —
drives 20 sites to unresolved and the stage to exit 3. It writes NO output set at all, which
is the property that matters: a stale set never reaches the transform rather than reaching
it shortened.

## 4. The refusal, where the set is whole

    PRECONDITION: ruled keys 2198 | resolving at this tree 2198 | NOT resolving 0
    files rewritten: 263 | skipped unparsable: 0
    total rewrites: 6091
    exit 0
    files the run modified in its worktree: 263

The guarded transform differs from the one round 61 ran by ONE function and one call to it,
and nothing else moves. Given the whole set it reports its precondition, proceeds, and lands
the same 6091 rewrites over the same 263 files the unguarded run produced, so the guard
costs the passing case nothing.

## 5. The refusal's red control — the stale set round 68 measured

    PRECONDITION: ruled keys 2198 | resolving at this tree 2144 | NOT resolving 54
    21  packages/orchestration/long_run_executor.py
    12  packages/orchestration/task_runner.py
    11  packages/orchestration/agent_loop.py
    7  packages/orchestration/dag_schedule.py
    3  packages/orchestration/verifier.py
    exit 4
    files the run modified in its worktree: 0
    the discriminator, PASS against REFUSE: 263 modified against 0

TWO HUNDRED AND SIXTY-THREE AGAINST ZERO IS THE WHOLE FINDING. Handed the round 53 committed
set — the exact input round 68 showed under-selects by 54 without complaint — the guarded
transform names all five files with their counts, exits 4, and modifies NOTHING. A refusal
that only printed a warning would read identically on the page; the file count is what tells
the two apart.

## 6. The transform lands, in two parts, because of the insertion cap

    part 1 + part 2 == the transform run in banners 3 and 4: True
    joined source lines: 652

THE FILE IS SPLIT BECAUSE OF A CAP, NOT BECAUSE IT HAS TWO PARTS. At 652 source lines a
single authored blob would be one commit of over 500 insertions, which AGENTS.md DECISION
F104 D1 forbids and whose exemption list names only the five `.agent/` state files — not
`.agent/authored/**`. So the transform travels as two blobs whose fence contents concatenate
byte for byte to the file the measurements above were taken with, and the gate re-derives
that join rather than trusting it. The cut falls at a top-level `def` boundary so each part
reads as a unit. This spends none of the feature's one declared-oversize allowance, which
the flip itself still needs.

## 7. Why this resolves `R-0879`, and what it deliberately does not claim

RESOLVED, on the finding's own terms. It asked for the re-key, which round 59 landed, and for
the transform to refuse a stale set, which this round lands and demonstrates against the case
that must fail. The two guards now stand at DIFFERENT doors — the stage refuses to EMIT a
stale set, the transform refuses to CONSUME one — so skipping the stage can no longer
reintroduce the defect, and that route was not a hypothetical: it is the one round 68 took.

NOT CLAIMED. The guarded transform is an instrument, not production code, and this round adds
no test under `tests/`: nothing in the suite will notice if a later round deletes the guard.
That is a real limit, stated rather than covered — the flip is still unlanded and a guard over
an unlanded change has no production surface to pin a test to; when the flip lands, a test
becomes both possible and owed. `R-0880` stays OPEN with both its obligations unbuilt, and it
is the MIRROR defect: this set reaching too FEW sites is what `R-0879` was, reaching too MANY
is what `R-0880` is, and nothing here touches the second. The id-SHAPE seam DECISION F275 D37
routed into T003's resolver collapse is still production work no round has started.
