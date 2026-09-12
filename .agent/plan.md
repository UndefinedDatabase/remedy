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

ROUND 83 COLLAPSES THE TWO JOB-ID RESOLVERS INTO ONE. `resolve_job_id` now searches both job
stores and `resolve_any_job_id` is an alias of it rather than a second copy, which is the half
of DECISION F275 D37's seam that F260 T004 named. Three tests pin it, and the round red-proves
each against its own mutation. The round also measures how far that carries a ping-pong id
through `job status`; the reviewer's dry run before authoring found it is one step — the
resolver finds the id and the handler then fails loading it from the classic store. The round
82 verdict and its prose slips are booked.

## Next Steps

1. THE HANDLER LAYER, the other half of DECISION F275 D37: the `UUID(...)` parses in
   `apps/cli/` whose argument names a job, and the classic-only load behind them. Production
   code, so a SPLIT round with mutation red-proofs, and likely more than one.
2. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the input
   is re-derived by round 82's committed generator at the flip's own base, and any site fallen
   to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- A RESOLVER THAT FINDS AN ID IS NOT A COMMAND THAT WORKS. `job status`, the one handler
  probed, fails one step later for a ping-pong id with a different message; the other handlers
  that load through the classic store were not probed.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 87 by distinct id at this round's base, with `R-0809` and `R-0880` open. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
