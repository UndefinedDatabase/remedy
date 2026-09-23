# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 1 claims F263, re-heads the finding ledger, records DECISION F263 D1,
and lands T001's foundation: `packages/orchestration/human_change.py`, the
target's last known state recorded on every git job behind its own
checkpoint ref, and the certified human change record written before any
re-base, with the tests and their red proofs.

## Next Steps

1. T001's second half: the record joins the job's exported evidence and its
   verification, so a package carries it like any other artifact.
2. T002, `remedy absorb`: the explicit command over the same `absorb` path,
   with its catalog entry, help text and re-base of the job's state.
3. T003, absorption at every safe point and before every apply, deleting
   the drift error it replaces, with the demo case end to end.
4. The closure sequence, with the one full-suite run.

## Risks

Capturing the target's tree hashes every file once per capture; T003 must
measure that cost at every safe point, as the Acceptance list requires.
