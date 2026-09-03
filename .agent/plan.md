# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a-T003b2b2b2 complete
and green as of round 16; round 17 closes an Acceptance gap the round
16 code left open (DECISION F112 D9): the cannot_fit decision now
carries its arithmetic.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 17, session 5 — per DECISION F112 D9: enqueue_task_decision's call
gains impact=f"tier1_tokens=... cap_tokens=... task_class=..." sourced
from the already-computed fit_result, closing Acceptance's "decision
with correct arithmetic" clause. The Design section's other two options
(raise cap for this job, proceed-overcap once — both "audited", with no
audit/attended-mode seam anywhere in this codebase) stay unbuilt,
explicitly named as an Acceptance-permitted narrowing, not silently
dropped.

## Next Steps

- Re-verify (not re-build) T3_F112.md's remaining Acceptance clauses
  against T002's already-existing fixtures
  (test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded,
  test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic)
  before claiming Acceptance met in full.
- The integration gate (full suite, twice per feature per
  docs/agents/integration_gate.md), then closure.

## Risks

- The integration gate has not run this feature yet; re-confirm before
  closure that nothing outside packages/orchestration regressed.
- Split children inherit the parent's full files_hint and so re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.