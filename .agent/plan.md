# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1 complete and green as of round 11; round 12 added T003c to
T3_F112.md's Task slicing (no code) as T003b2b2's prerequisite.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 13, session 4 — builds T003c per DECISION F112 D5's CHOSEN clause:
job task markdown gains a "Files:" inline marker (mirrors "Acceptance:"),
parsed into a new TaskEntry.files_hint: list[str] field, exported/
imported like inputs/task_class. task_entry_to_planned_task now passes
task.files_hint through instead of hardcoding [] (T003b2a's own
docstring updated to match).

## Next Steps

- T003b2b2 (own round(s), now unblocked): fit_task_context_to_class_cap
  + run_pingpong wiring at the dispatch site, using a task's real
  files_hint as compiled_context_paths (still [] and falling through to
  build_repo_context for a task with no Files: section — an honest,
  unchanged default, not a regression) + the cannot_fit decision call.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2 remains the highest-risk remaining slice; re-read the call
  site fresh before authoring, same standing instruction as D2-D5.
- A task with no Files: section still cannot engage the capped path
  (use_compiled_context needs both lists non-empty) — worth flagging
  in T003b2b2's own investigation rather than assuming it's solved.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.