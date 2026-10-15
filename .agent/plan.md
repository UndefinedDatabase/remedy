# Plan — amend1014c-review-closure-before-merge

## Goal
Operator amendment amend1014c (2026-10-15): repair the four review findings of the old pull request (R1 secret
persistence, R2 Pi timeout floor, R3 call accounting, R4 a 643-insertion commit) and carry them on a clean-history
replacement branch. Not a merge.

## Current Step
Done: R1 to R3 repaired and tested, acceptance A to E passed against the real Pi, the old pull request closed, the
branch `feature/do-golden-path-review-closure` replayed from `main` (tree equal to the old tip), the handoff written.

## Next Steps
1. Operator: review the replacement pull request; do not merge automatically.
2. After a merge decision, F078 resumes on `feature/f078-autonomy-levels`.

## Review Strategy
The old pull request had no review comments on any channel (checked 2026-10-15).

## Risks
- `.agent/STOP` untracked and untouched; the F078 branch untouched.
- Ordinary unrelated dirty content is still hashed by the F263 snapshot (see the handoff); one operator decision.
