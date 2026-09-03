# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a complete as of round 7.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 7, session 2 — books round 6's verdict, fixes R-0793 (Low: a
now-stale "JobPlan has no .metadata" comment/doc pair round 6's own
`JobPlan.metadata` field contradicted — no functional defect). T003a
(config, resolver, compiler wiring, split seam, metadata persistence) is
now fully complete and independently verified across rounds 2-7.

## Next Steps

- T003b (own dedicated round, fresh investigation first): derive a
  `task_class` for a live `TaskEntry` in `pingpong_job.py` (no existing
  precedent — investigate a title/body heuristic vs a new field), wire
  `compiled_context_paths`/`compiled_context_candidates` into that file's
  `run_pingpong(...)` call, then call `fit_task_context_to_class_cap` and
  `enqueue_task_decision` between `_build_task_prompt` and
  `task.status = TASK_RUNNING` in the per-task loop — before the F006
  checkpoint block, never after. `safe_default="split task"` via
  `auto_apply_safe_default` when unattended; omit the option when
  `split_one_task` returns None. See DECISION F112 D1
  (`.agent/decisions.md`) for the full investigation this scoping rests
  on.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b is the highest-risk remaining slice — a live dispatch loop, a
  persistence-format-adjacent change, and a new classification heuristic
  together. Re-read the call site fresh before authoring it.
- `R-0767` stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; `python3 -m ruff check <path>` is
  the reliable form, re-measured every round.
