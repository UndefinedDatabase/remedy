# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
Acceptance re-verified round 18 (RECORD18: VERDICT PASS, booked this
round). Round 19 opens session 6 at the integration gate.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 19, session 6 — books RECORD18 (round 18, VERDICT PASS) into the
ledger, then runs the integration gate (docs/agents/integration_gate.md):
full-suite branch run, base-worktree run with node_modules/dist parity
restored and mtime-corrected (R-0736), comparison, per-id attribution.
No production code touched. First of the two full-suite runs the
feature owes before closure.

## Next Steps

- If the gate PASSES cleanly: proceed to closure per
  docs/roadmap/STATUS_closure_protocol.md — evidence job, fresh review
  zip, the STATUS line, the PR — in session 6 or session 7.
- If the gate finds a reproducible branch-only regression coupled to
  feature code: STOP, hand back; the fix is its own reviewer-gated
  round, never folded into the gate round.

## Risks

- Split children inherit the parent's full files_hint and so re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap for this job" / "proceed-overcap once"
  options are deliberately unbuilt (DECISION F112 D9) — no audit/
  attended-mode seam exists anywhere in this codebase to hook them to.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- R-0736 (base-worktree mtime staleness) and R-0591 (copytree
  dereferencing symlinks) both bind this round's own base run; both are
  neutralized by constraint, not by code change.