# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 2 booked round 1's PASS and DECISION F263 D2 (C2), and landed T001's
evidence path (C3): the job's evidence export carries every human change
record, verifies each copy into `human_change_integrity.json`, and a
record that does not verify blocks the final verifier and the review
package's READY gate. BLOCKED at G4: `python3 -m ruff check` over C3's
product paths reads real exit 1 — `tests/orchestration/test_human_change_evidence.py:16`
imports `job_evidence_dir` but never calls it (F401). That file is a
reviewer payload copied verbatim in C3; the worker does not edit or
retype a payload, so the round stopped there per AGENTS.md "If Blocked"
and the block's constraint 4. G5 (the mutation red-proofs) did not run.
T001 is not yet certified done.

## Next Steps

1. Round 3: the reviewer either supplies a corrected
   `test_human_change_evidence.py` (dropping the unused import) or waives
   the ruff gate for this line, then G4 and G5 run to completion.
2. T002, `remedy absorb`: the explicit command over the same `absorb`
   path, with its catalog entry, help text and re-base of the job's state.
3. T003, absorption at every safe point and before every apply, deleting
   the drift error it replaces, with the demo case end to end.
4. The closure sequence, with the one full-suite run.

## Risks

Capturing the target's tree hashes every file once per capture; T003 must
measure that cost at every safe point, as the Acceptance list requires.
