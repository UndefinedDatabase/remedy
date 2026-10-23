# Plan — F133 Provider trust score

## Goal
Make "which model earns which work" a rolling, queryable fact: per model and role, the pass quota,
the repair need, the format-error rate and the cost per pass, each with its window and sample size,
in one trust home; `remedy stats trust` shows it, and routing reads it only as a recommendation.

## Current Step
Round 6, the closure's evidence round: the staging reclaim, the evidence job and the review package.

## Next Steps
1. Round 7: the Built State, the rotation, SU-077's consumed_by, the STATUS line with the README
   sync, and the pull request, left unmerged.

## Risks
- A package that does not read READY_FOR_REVIEW blocks the closure until it does.
