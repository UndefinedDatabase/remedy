# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 3 books round 2's FAIL with finding R-1042, repairs it under DECISION
F263 D3 — the unused import dropped, and `.agent/authored` excluded from
ruff — and runs round 2's red proofs, which never ran, so T001 is proved
whole: the record, its evidence path and its READY gate.

## Next Steps

1. T002, `remedy absorb`: the explicit command over the same `absorb`
   path, with its catalog entry, help text and re-base of the job's state.
2. T003, absorption at every safe point and before every apply, deleting
   the drift error it replaces, with the demo case end to end.
3. The closure sequence, with the one full-suite run.

## Risks

Capturing the target's tree hashes every file once per capture; T003 must
measure that cost at every safe point, as the Acceptance list requires.
