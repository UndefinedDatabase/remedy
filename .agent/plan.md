# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1/T003c/T003b2b2a/T003b2b2b1 complete and green as of round 15;
round 16 builds T003b2b2b2, the dispatch-loop wiring (DECISION F112 D8).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 16, session 5 — ships T003b2b2b2 per DECISION F112 D8: a cannot_fit
result now calls enqueue_task_decision/auto_apply_safe_default, and on
the "split task" default, split_one_task's children (via
planned_task_to_task_entry) replace the parent task in job.tasks. New
TASK_SPLIT status; the loop's own skip condition and its
select_next_predictable_task mirror both updated; run_job's all_done
completion check now includes TASK_SPLIT (a defect D7 did not surface,
found only by running the round's own test end-to-end). T3_F112.md's own
T003 description is now true at the dispatch-loop level.

## Next Steps

- Acceptance fixtures per T3_F112.md's own Acceptance section.
- The integration gate (full suite, twice per feature per
  docs/agents/integration_gate.md), then closure.

## Risks

- Split children inherit the parent's full files_hint and so re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section);
  accepted, not a defect, but worth knowing before reading an escalation
  ledger for a split job.
- The integration gate has not run this feature yet; F112's own footprint
  (prompt_budget.py, context_compiler.py's fit function, pingpong_job.py's
  dispatch loop) is wide enough that a full-suite pass is not yet proven.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.