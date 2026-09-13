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

ROUND 87 MEASURES THE FLIP AT ITS OWN BASE AFTER THE SEAM WORK, AND CORRECTS HOW IT CAN LAND.
The committed generator re-derives the flip's input at `bd2a75d5`, the guarded transform flips
a worktree, and a committed instrument classifies the full-suite transcripts the reviewer took
there into the failures the flip alone causes. The round records that F275's one declared
oversize commit was spent in round 73, rules that the flip lands as a series of commits each
under the cap, and asks the operator whether to allow one more oversized commit instead. It
books the round 86 verdict and its prose slips.

## Next Steps

1. THE `UUID(...)` PARSES UNDER `packages/` THAT FEED THE JOB STORE, counted by flow and each
   read for how its caller uses the raw value. The largest residue groups raise at the store's
   path join and at `run_job_fulfill`'s parse. Production code, so a SPLIT round with mutation
   red-proofs.
2. THE FLIP'S DRY RUN AGAIN, at the base that round leaves, read for the groups that remain.
3. THE FLIP, carrying DECISION F275 D48's obligations, as a series of commits each under the
   500-insertion cap inside one round, unless the operator allows one more oversized commit.
   The stale test double at `packages/orchestration/project_registry.py:856` moves with it.
4. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: at `bd2a75d5` it breaks 826 test nodes the unflipped tree passes.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
