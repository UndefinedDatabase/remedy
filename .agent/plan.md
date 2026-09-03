# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001 and T002 complete as of round 4;
T003a (JobPlan.metadata persistence) complete as of round 6.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 6, session 2 — books round 5's verdict, records DECISION F112 D1
(`.agent/decisions.md`) splitting T003 into T003a/T003b after
investigation found the dispatch loop `pingpong_job.py` uses has no
`task_class` on its task objects, never passes compiled-context params to
`run_pingpong`, and its `JobPlan` has no durable `metadata` field at all
— so `enqueue_task_decision`'s write would silently vanish on resume.
This round ships T003a: a `metadata: dict` field on `JobPlan`, exported
and imported like `input_snapshot`, with a persistence round-trip test.

## Next Steps

- T003b: derive a `task_class` for a live `TaskEntry` (no existing
  precedent to reuse — every current caller supplies task_class as a bare
  string; investigate whether a title/body heuristic or a new field is
  right), wire `compiled_context_paths`/`compiled_context_candidates`
  into `pingpong_job.py`'s `run_pingpong(...)` call, then call
  `fit_task_context_to_class_cap` and `enqueue_task_decision` between
  `_build_task_prompt` and `task.status = TASK_RUNNING`
  (`pingpong_job.py`, per-task loop) — before the F006 checkpoint block,
  never after. `safe_default="split task"` via `auto_apply_safe_default`
  when unattended; omit the option when `split_one_task` returns None.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b remains the highest-risk remaining slice — a live dispatch loop
  plus a persistence-format change together. Its own round, call site
  re-read first.
- `R-0767` stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; `python3 -m ruff check <path>` is
  the reliable form, re-measured every round.
