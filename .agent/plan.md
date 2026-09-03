# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001 complete as of round 3.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 4, session 2 — T002: `ClassBudgetFit` + `fit_task_context_to_class_cap`
in `packages/orchestration/context_compiler.py`, wiring T001's
`resolve_task_class_cap` onto the existing `compile_task_context` demotion
cascade with no change to that cascade itself. Two fixtures: an oversized
context demoted under its cap (`fits=True`), and an unfittable one
reporting `cannot_fit` arithmetic (`fits=False`, `tier1_tokens` carried).

## Next Steps

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
  binary is denied but `python3 -m ruff` resolves (measured every round so
  far); use the module form and re-measure rather than trusting a prior
  round's claim.
