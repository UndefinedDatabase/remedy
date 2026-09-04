# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
Acceptance re-verified round 18, integration gate PASSED round 19
(RECORD19: VERDICT PASS, booked this round, independently re-run by the
reviewer: branch suite 19546 passed / 23 skipped / 0 failed reproduced
directly). Round 20 opens the closure sequence
(docs/roadmap/STATUS_closure_protocol.md).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 20 books RECORD19, then opens closure precondition 6 (the
self-use queue, F257/F258): the queue holds no pending item
(`next_self_use_item()` is None), so this round calls
`self_use_generator.generate_and_append_if_empty` and reports the
result. No self-use job is planned or run this round.

## Next Steps

- New item generated: a later round runs it via `self_use_job` /
  `self_use_runner` to the approval gate, registers any findings
  `self_use_findings.describe_self_use_run_defects` reports, and sets
  `consumed_by` to F112 at closure.
- Generator also answers None: record `self-use NONE (queue exhausted)`
  and proceed without one.
- Either way: evidence job, review zip, STATUS line, PR per
  docs/roadmap/STATUS_closure_protocol.md.

## Risks

- Split children inherit the parent's full files_hint and re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap" / "proceed-overcap once" options are
  deliberately unbuilt (DECISION F112 D9).
- R-0767 stays OPEN on the model-routing seam this feature's config
  borrows from; unrelated to F112.
- `self_use_runner.run_next_self_use_item` refuses an unflagged fake
  provider (R-0767/R-0768 class) — a real provider must resolve first.