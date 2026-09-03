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

Round 8, session 2 — books round 7's verdict, fixes R-0794 (Medium: a
genuine red test round 6's `JobPlan.metadata` field broke —
`test_jobplan_no_metadata_attr_safe` asserted a state `JobPlan` can no
longer naturally be in; now reconstructs the absence via `del
job.metadata` instead). Branch tip is green across every suite this
session has run. T003a is fully done; T003b is unstarted.

## Next Steps

- T003b (own dedicated round, fresh investigation first — likely a NEW
  SESSION per self-drive session guidance): derive a `task_class` for a
  live `TaskEntry` in `pingpong_job.py` (no existing precedent), wire
  `compiled_context_paths`/`compiled_context_candidates` into that
  file's `run_pingpong(...)` call, then call
  `fit_task_context_to_class_cap` and `enqueue_task_decision` between
  `_build_task_prompt` and `task.status = TASK_RUNNING` in the per-task
  loop — before the F006 checkpoint block, never after.
  `safe_default="split task"` via `auto_apply_safe_default` when
  unattended; omit the option when `split_one_task` returns None. See
  DECISION F112 D1 (`.agent/decisions.md`) for the full investigation.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b is the highest-risk remaining slice — re-read the call site
  fresh before authoring it; do not reuse round-6-era assumptions
  without re-checking them against HEAD.
- `R-0767` stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; `python3 -m ruff check <path>` is
  the reliable form, re-measured every round.