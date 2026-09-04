# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green.
Round 26 hit the amend0827 rule 6 soft limit (26 rounds) and filed a
scope report on the review-zip `BLOCKED_EVIDENCE` blocker. The operator
ruled 2026-09-04: the root cause is CONFIRMED (R-0792 output_hash/
stdout_summary contract defect, R-0793 `_scrub_paths` absolute-path gap,
both in shared evidence-packaging infra, neither F112-specific), and
F112's closure continues on its own round budget, no second STATUS line.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 27 fixes the evidence-packager verification-run contract per the
operator's ruling: `output_hash` is always sha256 of the exact stored
`stdout_summary` bytes (`job_evidence.py`'s `_default_verification_runner`
and `_run_verifications`'s normalization loop, `manual_attestation.py`'s
`_vt_run_v11`), and `job_evidence._scrub_paths` delegates to
`packages/common/path_redaction.scrub_paths` for non-repo/non-home
absolute paths. Four red proofs plus one mutation red-proof, all in a
disposable worktree.

## Next Steps

- Round 28: reviewer books round 27's verdict (`Done: R-0792`,
  `Done: R-0793` if PASS), rebuilds F112's closure evidence job and
  review zip, confirms `PACKAGE_STATUS=READY_FOR_REVIEW` /
  `EVIDENCE_AUTHORITATIVE=true` by reading `.review_zip_manifest.json`
  from inside the built zip, not from builder stdout.
- Round 29: closure sequence — STATUS `[x]`, README capability sync,
  `self_use_queue` SU-007 `consumed_by=F112`, final `.agent/` state,
  closure commit, PR opened (not merged that round).
- Round 30: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule.

## Risks

- R-0784, R-0767 (both OPEN, unrelated to F112) carry forward undecided.
- The `scrub_paths` delegation must not regress the R-0790 "+/-"
  non-match guard; the mutation proof below exists to catch exactly that.