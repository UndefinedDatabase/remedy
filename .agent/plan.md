# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 5 books round 4's PASS, records DECISION F263 D5, and lands T003's
run half: a git job absorbs a hand edit at every safe point and keeps
running, the two drift blocks are gone for it, each check is counted and
timed, and the demo case runs end to end.

## Next Steps

1. T003's apply half: `job apply` and `do run --apply` absorb before a
   single file is copied, a hand edit that meets the job's own change
   stops the apply and says why, and the second demo case runs.
2. The closure sequence, with the one full-suite run.

## Risks

A hand edit to a file the job also changed is only met at apply; the next
round decides that it stops there rather than overwrite either side.
