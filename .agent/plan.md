# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 4 books round 3's PASS, records DECISION F263 D4, and lands T002:
`remedy absorb`, its catalog entry, help slot and bare form, over
`human_change.absorb_job` — the one path that certifies a hand edit and
re-bases a job's last known state, which the run's safe points will call.

## Next Steps

1. T003, absorption at every safe point and before every apply, deleting
   the drift error it replaces, with the demo case end to end and the
   cost of the check measured.
2. The closure sequence, with the one full-suite run.

## Risks

Capturing the target's tree hashes every file once per capture; T003 must
measure that cost at every safe point, as the Acceptance list requires.
