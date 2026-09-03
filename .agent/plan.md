# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001 part 1 landed round 2.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 3, session 1 — fix `R-0791` (two ruff-confirmed defects in
`packages/orchestration/prompt_budget.py`: a redundant-quotes type hint
and a missing trailing newline), then ship
`tests/orchestration/test_class_prompt_budget.py`, completing T001. Still
no compiler wiring — T002.

## Next Steps

- T002: compiler cap enforcement in `context_compiler.py` — `fit(context,
  cap)` over the existing demotion order, the `cannot_fit` outcome with
  tier-1/cap/class arithmetic, and oversized/unfittable fixtures.
- T003: decision wiring (`escalation.enqueue_task_decision`, type
  `task_decision`), unattended default split, granularity-machinery seam.
- Acceptance fixtures, the integration gate, then the closure sequence.

## Risks

- `task_granularity.py`'s split helpers are module-private and built for
  plan-time normalization, not a live dispatched task; T003 may need a
  small public seam addition, never a fork of the heuristics themselves
  (feature file "Do not touch").
- `R-0767` stays OPEN on the model-routing seam this feature's config
  registration pattern borrows from; unrelated to F112, not absorbed.
- ruff availability is INCONSISTENT within this session: the bare `ruff`
  binary is denied but `python3 -m ruff` resolves (measured R2); use the
  module form and re-measure each round rather than trusting a prior
  round's claim.
