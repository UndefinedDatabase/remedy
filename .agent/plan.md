# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1/T003c/T003b2b2a complete and green as of round 14; round 15
splits T003b2b2b into T003b2b2b1/T003b2b2b2 (DECISION F112 D7).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 15, session 5 — builds T003b2b2b1 per DECISION F112 D7's CHOSEN
clause: `planned_task_to_task_entry` (the reverse of the existing
`task_entry_to_planned_task`) turns one `split_one_task` child
`PlannedTask` back into a dispatchable `TaskEntry`. Not called from
`run_job` this round — a prerequisite building block only, same shape
T003c used before T003b2b2a wired it.

## Next Steps

- T003b2b2b2 (own round(s)): the actual dispatch-loop wiring — a new
  TASK_* status for "replaced by a split", the enqueue_task_decision /
  auto_apply_safe_default calls, used_ids collection from the live
  job.tasks list, safe post-idx insertion, and the loop's own skip
  condition for the new status. Re-read run_job fresh before authoring
  (D7's own standing instruction) rather than trust this round's reading.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2b2 remains the highest-risk remaining slice, now for five
  separately-named reasons (DECISION F112 D7's MEASURED section) rather
  than one; re-read run_job's dispatch loop fresh before authoring.
- A task with no Files: section, or one whose fenced scope cannot fit its
  class cap, still falls through to build_repo_context uncapped and now
  ALSO never reaches an escalation — accepted default until T003b2b2b2
  lands, not a regression.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.