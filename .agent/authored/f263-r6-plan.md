# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 6 books round 5's PASS, records DECISION F263 D6, and lands T003's
apply half: every apply absorbs before a file is copied, the apply's drift
block is deleted, and a hand edit the job also changed stops the apply
with its name. With it every slice, T001 to T003, has landed.

## Next Steps

1. The closure's first round: the Built State in the feature file, the
   closure's self-use item, and the feature's one full-suite run.
2. The evidence bundle and the review package.
3. The ledger rotation, the accepted STATUS line and the pull request.

## Risks

The cost of the check is recorded per job; the closure reads it from a
real job's record and states it in the Built State.
