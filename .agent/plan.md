# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 84 GIVES THE JOB-ID RESOLVER A RAISING FORM AND ROUTES THE HANDLERS THAT KEEP THEIR ID.
`lookup_job_id` raises a `ValueError` subclass where `resolve_job_id` exits, so a handler that
guards its parse keeps its own documented path; `resolve_job_id` becomes its wrapper with the
same messages and exit codes. The handler statements that bind a parsed job id are routed
through it. The ones that pass the parse straight into `load_job` are left, because the
reviewer's dry run found `job stop` losing a stop request when one of them was routed without
reading it. The round 83 verdict, its prose slips and one comment round 83 falsified are booked.

## Next Steps

1. THE REMAINING HANDLER PARSES, each `load_job(UUID(...))` read for whether its caller keeps
   using the raw argument as a key, starting with `job stop`'s loader and its caller's
   normalisation. Production code, so a SPLIT round with mutation red-proofs.
2. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the input
   is re-derived by round 82's committed generator at the flip's own base, and any site fallen
   to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- A HANDLER THAT DISCARDS ITS RESOLVED ID CAN KEY ON THE RAW ONE. The dry run caught one such
  site through a test; untested sites of that shape are not seen by any run.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 87 by distinct id at this round's base, with `R-0809` and `R-0880` open. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
