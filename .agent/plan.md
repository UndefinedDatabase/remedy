# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1/T003c complete and green as of round 13; round 14 splits
T003b2b2 into T003b2b2a/T003b2b2b (DECISION F112 D6) after finding
compiled_context_candidates has no source either.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 14, session 4 — builds T003b2b2a per DECISION F112 D6's CHOSEN
clause: the job-dispatch call site (pingpong_job.py's run_job, its one
run_pingpong( call) gains a fit_task_context_to_class_cap check and three
new run_pingpong kwargs (compiled_context_paths, compiled_context_candidates
set to the same list, compiled_context_token_budget). When task.files_hint
is empty or the fit reports fits=False, all three stay None — today's exact
build_repo_context fallback, unchanged. No escalation on cannot_fit this
round (that is T003b2b2b).

## Next Steps

- T003b2b2b (own round(s)): the cannot_fit -> enqueue_task_decision ->
  auto_apply_safe_default -> split_one_task chain. Prerequisite reading
  before authoring: run_job's own task-iteration structure (how tasks are
  consumed from job.tasks, whether a split's children can be inserted back
  into the sequence) — split_one_task is not called anywhere in
  pingpong_job.py today, confirmed by grep.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2b remains the highest-risk remaining slice; re-read run_job's
  dispatch loop fresh before authoring, same standing instruction as D2-D6.
- A task with no Files: section, or one whose fenced scope cannot fit its
  class cap, still falls through to build_repo_context uncapped — accepted
  default for this round, not a regression; T003b2b2b is what makes
  cannot_fit actionable instead of silently bypassed.
- R-0767 stays OPEN on the model-routing seam this feature's config pattern
  borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.