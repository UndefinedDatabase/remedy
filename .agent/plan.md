# Plan — F312 The scope guard knows orders without file names

## Goal
The scope guard tells three kinds of order apart and refuses a plan only for the kind that drew a
fence; an order that names no file gives a plan, not a failure
(`docs/roadmap/features/T2_F312.md`). F312 owns finding R-1369.

## Current Step
Round 1 (session 1): claim F312, re-head the ledger, DECISIONs F312 D1 and D2, step (2) of
`plan_order_job`'s boundary (`_first_pass_task_plan`), and T001: `do_scope.order_scope_kind`,
the task-plan guard reading the kind of the person's order, and `_step_shape` passing
`scope_order=ctx.order`.

## Next Steps
1. Round 2: T002, the question after two refusals of an open order, under DECISION F312 D3, and
   T003, the three lab order texts as a fixture through the real walk in the `milestones` shape.
2. The closure: the one full suite, the evidence, R-1369's resolution line, STATUS, the PR.

## Risks
- The records of the failed lab job were not read (the data root is not readable here); the
  finding's text and the code are the evidence (DECISION F312 D1).
- `plan_order_job` is a listed function: after the structural step it may not grow.
