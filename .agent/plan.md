# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 7 is the closure sequence's first half. It books round 6's PASS,
adds the guard test that holds the explicit command, the run's safe points
and the apply to one implementation of absorption, writes the feature
file's Built State, generates and runs the closure's self-use item, and
runs the feature's one full suite. Every slice, T001 to T003, has landed.

## Next Steps

1. The registrations the self-use run's defects ask for, and any repair
   the full suite requires.
2. The evidence job and the review package.
3. The ledger rotation, the accepted STATUS line with the README counters,
   and the pull request.

## Risks

The cost of the human-change check is read from the self-use job's own
record, the first real job to run with absorption; a job that stops
before its first safe point would carry no reading.
