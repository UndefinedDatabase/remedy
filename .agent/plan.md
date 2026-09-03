# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1 complete and
green as of round 9.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 10, session 3 — fresh investigation over T003b2's call site (per
DECISION F112 D2's own instruction to re-read fresh before authoring)
found run_pingpong has no token-budget passthrough: wiring
compiled_context_paths/candidates alone recompiles at
compile_task_context's DEFAULT budget, never the class cap (DECISION
F112 D3). T003b2 splits further into T003b2a (this round: the
TaskEntry->PlannedTask adapter + a compiled_context_token_budget
passthrough on run_pingpong, both unit-tested in isolation) and T003b2b
(deferred: the live call-site wiring).

## Next Steps

- T003b2b (own dedicated round(s)): call fit_task_context_to_class_cap
  between _build_task_prompt and task.status = TASK_RUNNING; pass its
  compiled paths, the job's repo candidate listing, and cap_tokens into
  run_pingpong(compiled_context_paths=..., compiled_context_candidates=...,
  compiled_context_token_budget=...); on cannot_fit call
  enqueue_task_decision (options=["split task"] only when
  task_entry_to_planned_task(task) is not None and split_one_task on its
  result returns non-None) then auto_apply_safe_default under --yes.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b is still the highest-risk remaining slice — first-time wiring
  against the live dispatch loop; re-read the call site fresh again
  before authoring it, per DECISION F112 D2/D3.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.