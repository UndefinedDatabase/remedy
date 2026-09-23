# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 8 is the closure sequence's evidence half. It books round 7's PASS
and records the self-use run's defect and the one flaky suite node as
recurrences of findings already open, then builds the evidence bundle
against the fork point and the fresh review package.

## Next Steps

1. The closing round: the ledger rotation, the accepted STATUS line with
   the README counters and the self-use item's `consumed_by`, and the pull
   request.

## Risks

A package that does not read READY_FOR_REVIEW blocks the closure; the
round stops and hands back rather than edit an evidence file.
