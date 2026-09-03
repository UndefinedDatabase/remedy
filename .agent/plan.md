# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1 complete and green as of round 11.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 12, session 4 — investigation of T003b2b2's call site found
run_pingpong's `use_compiled_context = bool(compiled_context_paths) and
bool(compiled_context_candidates)` requires BOTH lists non-empty, and
job-dispatch TaskEntry has no files_hint source — fenced_paths=[] (the
only value available today) makes the whole wiring a silent no-op,
always falling through to the uncapped build_repo_context path
(DECISION F112 D5). Stronger than D3/D4: not just cannot_fit
unreachable, the capped path never activates at all. T3_F112.md gains
T003c (a "## Files" job-markdown section feeding TaskEntry.files_hint)
as T003b2b2's prerequisite. This round is decision + plan + feature-file
only — no production code, since T003c must land first.

## Next Steps

- T003c (own round(s)): parse "## Files" in job task markdown (mirrors
  the existing "Acceptance:" inline-marker pattern) into a new
  TaskEntry.files_hint: list[str] field, exported/imported like
  inputs/task_class; update task_entry_to_planned_task's mapping.
- T003b2b2 (after T003c): fit_task_context_to_class_cap +
  run_pingpong wiring (now with real fenced_paths) + the cannot_fit
  decision call, now actually reachable.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2 depends on T003c landing first; re-read both call sites
  fresh before authoring either.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.