# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a complete and green as
of round 8.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 9, session 3 — fresh investigation over the T003b call site found a
task-type mismatch DECISION F112 D2 records: split_one_task takes
schemas/models.py's PlannedTask, not pingpong_job.py's own TaskEntry.
T003b splits into T003b1 (this round: task_class field on TaskEntry,
defaulted to "standard_build", exported/imported like T003a's metadata)
and T003b2 (the adapter, call-site wiring and decision enqueue, deferred).

## Next Steps

- T003b2 (own dedicated round(s), fresh investigation already done in
  DECISION F112 D2): a TaskEntry->PlannedTask adapter
  (acceptance.splitlines(), empty files_hint — safe per D2's MEASURED),
  the fit_task_context_to_class_cap call between _build_task_prompt and
  task.status = TASK_RUNNING, wiring its compiled paths into this loop's
  run_pingpong(compiled_context_paths=..., compiled_context_candidates=...),
  and on cannot_fit calling enqueue_task_decision (options=["split task"]
  only when split_one_task via the adapter returns non-None) then
  auto_apply_safe_default under --yes.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2 is still the highest-risk remaining slice (five first-time-wired
  pieces per DECISION F112 D2) — re-read the call site fresh again before
  authoring it.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.