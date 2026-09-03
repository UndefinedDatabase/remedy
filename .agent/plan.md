# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green as
of round 17; round 18 re-verifies T3_F112.md's Acceptance clauses
(confirmed met, no new code) and closes session 5 at the integration
gate boundary.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 18, session 5 (closing) — no code this round. Re-ran T3_F112.md's
Acceptance-relevant fixtures fresh: test_class_prompt_budget.py (T001,
24 passed), test_context_compiler.py (T002, 69 passed, including the
oversized/unfittable fixtures by name). Both confirmed unregressed by
rounds 14-17. All three Acceptance clauses (demotion recorded, decision
with correct arithmetic, --yes path splits and completes) are now met
by shipped, tested code — see RECORD17's own ACCEPTANCE
RE-VERIFICATION paragraph for the full citation.

## Next Steps

- SESSION 6 opens here: the integration gate
  (docs/agents/integration_gate.md) — branch run, base-worktree run
  with node_modules/dist parity, comparison, per-id attribution. This
  is its own dedicated round(s); do not fold it into a smaller round.
- Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence
  job, fresh review zip, the STATUS line, the PR.

## Risks

- The integration gate has not run this feature yet — F112's footprint
  (prompt_budget.py, context_compiler.py's fit function, pingpong_job.py's
  dispatch loop, escalation.py's now-exercised JobPlan compatibility) is
  wide enough that a full-suite pass is not yet proven end to end.
- Split children inherit the parent's full files_hint and so re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap for this job" / "proceed-overcap once"
  options are deliberately unbuilt (DECISION F112 D9) — no audit/
  attended-mode seam exists anywhere in this codebase to hook them to.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.