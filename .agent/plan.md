# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use item SU-007 run round 21
(RECORD21: VERDICT PASS, booked this round; R-0784 gained a third
occurrence, no new id). Round 22 lands the Built State section
(precondition 4) and re-confirms remaining preconditions before closure.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 22 books RECORD21, then appends a "Built State — what F112
delivered" section to `docs/roadmap/features/T3_F112.md` (precondition
4 — the file has none yet). `remedy integrity_gate.run_integrity_checks()`
already reads all-PASS (precondition 3, reviewer-confirmed pre-round).
No production code touched.

## Next Steps

- Precondition 6's `consumed_by=F112` edit to `scripts/self_use_queue.json`
  lands in the closure commit itself, alongside STATUS/README.
- Evidence job (`job_evidence.create_manual_completion_bundle`), then the
  mandatory fresh review zip, per
  docs/roadmap/STATUS_closure_protocol.md steps 1-2.
- STATUS line authored by the reviewer, applied by the worker; README
  capability sync in the SAME commit (R-0154 pin).
- Final closure commit + PR; merge deferred to the next feature's start.

## Risks

- Split children inherit the parent's full files_hint and re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap" / "proceed-overcap once" options are
  deliberately unbuilt (DECISION F112 D9).
- R-0767 stays OPEN on the model-routing seam this feature's config
  borrows from; unrelated to F112.
- R-0784 (self-use/R-0418 curation gap) is OPEN and belongs to F258, not
  F112 — do not attempt to fix it here.