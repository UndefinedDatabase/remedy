# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 2, session 1 — T001 part 1: register `prompt_budget.task_class_caps`
and `prompt_budget.default_cap` in `packages/orchestration/config.py`
(mirroring the `model_routing.*` table-key pattern), and ship the new
module `packages/orchestration/prompt_budget.py` — resolver
`resolve_task_class_cap` (configured class cap > configured global default
> shipped fallback, all basis `class_default`) and floor + vocabulary
validator `validate_prompt_budget_config`, both reusing
`model_routing.TASK_CLASS_TIERS` as the one shared class vocabulary. No
tests land this round (round 3, for the 400-line block cap); no compiler
wiring (T002).

## Next Steps

- Round 3: `tests/orchestration/test_class_prompt_budget.py`, gating
  round 2's module, plus the mutation red-proof item 5 forbids ordering
  before a reachable test exists.
- T002: compiler cap enforcement in `context_compiler.py` — `fit(context,
  cap)`, the `cannot_fit` outcome with tier-1/cap/class arithmetic, and
  oversized/unfittable fixtures.
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