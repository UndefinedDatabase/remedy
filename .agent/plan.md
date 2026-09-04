# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use item SU-007 generated round 20
(RECORD20: VERDICT PASS, booked this round). Round 21 plans and runs
SU-007 to the normal approval gate (closure precondition 6, F257/F258).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 21 runs `self_use_runner.run_next_self_use_item` against SU-007
(job "Address ledger finding R-0418") through the real builder/reviewer
loop (local `ollama` provider, no external cost), stopping at the normal
approval gate — never promoted. Every string
`self_use_findings.describe_self_use_run_defects` returns for the run's
JobPlan is registered as an R-id finding before close. `consumed_by` is
set to F112 only in the closure commit, not this round.

## Next Steps

- Register any findings the run's own defects surface; repair only if
  small and reviewer-gated as its own round.
- Set SU-007's `consumed_by` to F112 in the closure commit.
- Then: evidence job, review zip, STATUS line, PR per
  docs/roadmap/STATUS_closure_protocol.md.

## Risks

- Split children inherit the parent's full files_hint and re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap" / "proceed-overcap once" options are
  deliberately unbuilt (DECISION F112 D9).
- R-0767 stays OPEN on the model-routing seam this feature's config
  borrows from; unrelated to F112.
- A self-use job can stall mid-run (F110 R16's SU-006 precedent) —
  if so, declare it and resume via `resume_job_plan` next round rather
  than treating it as failed.