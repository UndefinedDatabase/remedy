# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use consumed round 21, Built
State landed round 22. Round 27 fixed the evidence-packager contract
(R-0792, R-0793) per the operator's ruling of 2026-09-04 and is
independently re-verified (RECORD27, this round). All six closure
preconditions are now satisfied; round 28 rebuilds the evidence job and
review zip against the fixed contract.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 28 rebuilds the F112 closure evidence bundle via
`job_evidence.create_manual_completion_bundle` (the same three scoped
verification commands round 23 used, via `_run_verifications`, now
fixed) and the mandatory review zip
(`scripts/make_review_zip.sh --evidence-dir <path>`), then confirms
`PACKAGE_STATUS=READY_FOR_REVIEW` / `EVIDENCE_AUTHORITATIVE=true` by
reading `.review_zip_manifest.json` from INSIDE the built zip.

## Next Steps

- Round 29: reviewer authors the STATUS `[x]` line from round 28's
  reported job_id/package/hash/path/accepted-HEAD; closure commit
  (STATUS, README capability sync, `self_use_queue` SU-007
  `consumed_by=F112`, final `.agent/` state); PR opened, not merged.
- Round 30: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule;
  hand back the built zip's name and SHA-256 to the operator.

## Risks

- R-0784 (self-use/R-0418 curation gap, OPEN) and R-0767 (model-routing
  seam, OPEN) are both documented pre-existing risks, unrelated to
  F112, carried forward per precondition 1's "Resolved or documented
  risk".
- A PACKAGE_STATUS other than READY_FOR_REVIEW is still a closure
  BLOCKER even after the R-0792/R-0793 fix; round 28 declares rather
  than works around any remaining blocking reason.