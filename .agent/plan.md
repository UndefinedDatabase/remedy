# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a
complete and green as of round 10.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 11, session 4 — fresh investigation over T003b2b's own call site
(escalation.py's enqueue_task_decision/auto_apply_safe_default, the
piece T003b2a deliberately left untouched) found a second latent
incompatibility beyond DECISION F112 D2/D3's: _record_answer_on_task
reads task.id and task.inputs, fields pingpong JobPlan's TaskEntry has
never carried (only Core Job's Task has them) — calling
auto_apply_safe_default against a live JobPlan would raise
AttributeError (DECISION F112 D4). T003b2b splits into T003b2b1 (this
round: the escalation.py dual-shape fix + a new TaskEntry.inputs field)
and T003b2b2 (deferred: the live call-site wiring, now safe to build).

## Next Steps

- T003b2b2 (own dedicated round(s)): call fit_task_context_to_class_cap
  between _build_task_prompt and task.status = TASK_RUNNING; wire
  compiled_context_paths/candidates/token_budget into run_pingpong; on
  cannot_fit call enqueue_task_decision (options=["split task"] only
  when task_entry_to_planned_task(task) is not None and
  split_one_task on its result returns non-None) then
  auto_apply_safe_default under --yes, reading the answer off the
  returned record directly rather than off task.inputs (same
  dispatch-loop iteration, no resume needed for this path).
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2 is still the highest-risk remaining slice — first-time
  wiring against the live dispatch loop; re-read the call site fresh
  again before authoring it, per DECISION F112 D2/D3/D4.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.