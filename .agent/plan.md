# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, cut from `main` after
pull request 233 was merged at the Open PR Gate.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 1, session 1 — claim F112 in the STATUS ledger and set this file and
`.agent/context.md`. Branch already cut. T001 lands over the next two
rounds, split for the 400-line block cap (section 3 item 1): round 2 ships
the config schema (`prompt_budget.task_class_caps` +
`prompt_budget.default_cap`) and the new module
`packages/orchestration/prompt_budget.py` (resolver
`resolve_task_class_cap`, validator `validate_prompt_budget_config`,
reusing `model_routing.TASK_CLASS_TIERS` as the one shared class
vocabulary); round 3 ships that module's tests. No compiler wiring yet —
that is T002.

## Next Steps

- Round 2: `prompt_budget.py` + its config registration.
- Round 3: `tests/orchestration/test_class_prompt_budget.py`, gating
  round 2's module.
- T002: compiler cap enforcement in `context_compiler.py` — `fit(context,
  cap)` over the existing demotion order, plus the `cannot_fit` outcome
  with the tier-1-size/cap/class arithmetic, and oversized/unfittable
  fixtures.
- T003: the decision wiring (`escalation.enqueue_task_decision`, type
  `task_decision`) for "task context exceeds its class cap", unattended
  default split, and the granularity-machinery seam (see Risks).
- Acceptance fixtures, the integration gate, then the closure sequence.

## Risks

- `task_granularity.py`'s split helpers are module-private and built for
  plan-time normalization, not a live dispatched task; T003 may need a
  small public seam addition, never a fork of the heuristics themselves
  (feature file "Do not touch").
- `R-0767` stays OPEN on the model-routing seam this feature's config
  registration pattern borrows from; unrelated to F112, not absorbed.
