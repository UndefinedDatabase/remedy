# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001 and T002 complete as of round 4.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 5, session 2 — books round 4's verdict (R-0792, a Low ruff F401
fixed in this same round), then starts T003: `split_one_task` in
`packages/orchestration/task_granularity.py`, a public seam over the
existing `_cluster_acceptance`/`_split_task` clustering for a caller that
already decided (via T002's `cannot_fit`) a task needs to split, without
re-deciding the band/acceptance trigger `normalize_plan` owns.

## Next Steps

- T003 continued: wire `cannot_fit` into `enqueue_task_decision` (type
  `task_decision`, `escalation.py:211`) at the per-task dispatch loop in
  `pingpong_job.py` (~line 2307's `run_pingpong` call, the site with a
  live `Job`/`Task`). Needs: how `task_class` is resolved per task,
  how `compiled_context_paths`/`candidates` reach `run_pingpong` today,
  and a `Task`→`PlannedTask` reconstruction (`flight_plan.py:513-538`
  stashes title/depends_on/band/files_hint on `task.inputs["flight"]`;
  `goal` is not preserved separately — recover it from `task.description`).
- Unattended default `safe_default="split task"`, applied via
  `auto_apply_safe_default` when `unattended=True`
  (`long_run_executor.py:992` `_escalate_task` is the pattern). Omit the
  split option when `split_one_task` returns None (A9: real options only).
- Acceptance fixtures, the integration gate, then closure.

## Risks

- Dispatch-loop wiring is the highest-risk remaining slice — a live loop,
  not a pure function. Gets its own round, call site read in full first.
- `R-0767` stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; `python3 -m ruff check <path>` is
  the reliable form, re-measured every round.
