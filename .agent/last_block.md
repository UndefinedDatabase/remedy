## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r14.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD13 (append to .agent/live_review.md, one-newline formula — `content_bytes + b"\n" + RECORD13_bytes`, 1631 bytes):

Gate: F112 R13 — the round 13 entry. VERDICT PASS, over the range `afb90730..5c05e0cb` (commits C0a through C5 — six commits total this round), independently reviewed by the reviewer at the start of session 4's round 14. THE CODE HELD: `git show ec9ffdd2` reproduced exactly the T003c pairs the handback described in `packages/orchestration/pingpong_job.py` (TaskEntry.files_hint field, the third parser state `_in_files`, export/import round-trip, `task_entry_to_planned_task`'s passthrough) and the four new tests in `tests/orchestration/test_job_task_runner.py`. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_job_task_runner.py -q` reproduced at 206 passed. THE LINT HELD: `python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_task_runner.py` reproduced "All checks passed!". THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE TRANSPORT HELD: `cmp .agent/authored/f112-r13.md .agent/last_block.md` exited 0, both 3859 bytes. THE MUTATION RED-PROOF HELD: reproduced independently in a fresh disposable worktree (`.remedy-wt/f112-r13-review`, removed after), off commit `5c05e0cb`. Deleting the `current_task["_in_files"] = False` line from the "Acceptance:" branch reproduced exactly the handback's predicted result: `test_files_section_extracted` went RED (`AssertionError: assert ['src/main.py', 'docs/README.md', 'done'] == ['src/main.py', 'docs/README.md']`) and `test_no_files_section_leaves_files_hint_empty` stayed GREEN, 1 failed / 1 passed. `git status --porcelain` read empty throughout, including after the worktree's removal.

<<<END RECORD13>>>

PLAN14 (whole-file replacement of .agent/plan.md, no trailing newline, 2394 bytes, 49 content lines):

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

<<<END PLAN14>>>

DECISION F112 D6 (append to .agent/decisions.md, one-newline formula — `content_bytes + b"\n" + D6_bytes`, 5788 bytes):

## DECISION F112 D6 (2026-09-03, F112 R14) — compiled_context_candidates has no source for job-dispatch tasks; T003b2b2 splits into T003b2b2a (fit+wiring, safe fallback on non-fit) and T003b2b2b (the cannot_fit escalation chain, deferred)

CONTEXT. Fresh investigation this round (reviewer, read-only, over run_pingpong's use_compiled_context gate and compile_task_context's own docstring and body) found a second, independent gap from D5's: even with T003c landed (files_hint now populated for a job task that declares a "Files:" section), run_pingpong's gate at pingpong_loop.py:3115 is `bool(compiled_context_paths) and bool(compiled_context_candidates)` — BOTH lists must be non-empty — and no F112 decision or plan.md entry has ever named a source for compiled_context_candidates at the job-dispatch call site (pingpong_job.py:2397). Grepping packages/ for compiled_context_candidates= assignments in production code returns zero hits.

MEASURED. compile_task_context's own docstring (context_compiler.py:752-754) states repo_paths ("the candidate listing the caller walked") feeds ONLY the tier-4 "remaining" omission-disclosure set (context_compiler.py:786: `remaining = set(repo_paths) - fenced - neighbors - distant`). Tier 2 ("direct import neighbors") and tier 3 ("one hop further") are derived from `_import_neighbor_files(root, fenced)` (context_compiler.py:782-784), a real on-disk import-graph walk that does not consult repo_paths at all. Passing repo_paths == fenced_paths — i.e. compiled_context_candidates == task.files_hint, the same list already resolved for compiled_context_paths — therefore satisfies the gate's non-empty requirement on both sides, leaves tier-2/3 neighbor expansion fully intact, and correctly yields an EMPTY tier-4 "remaining" set, which is the honest disclosure for a job-dispatch task whose only declared candidate universe IS its fenced scope, not an omission bug.

CHOSEN. At the job-dispatch call site, compiled_context_candidates is the same list as compiled_context_paths (`list(task.files_hint)`) whenever task.files_hint is non-empty; this closes the candidates gap with no new repo-walk machinery and no change to run_pingpong's own gate. Given that fix, T003b2b2 (as D3/D4 scoped it: (a) the fit_task_context_to_class_cap call, (b) run_pingpong parameter wiring, (c) the cannot_fit -> enqueue_task_decision -> auto_apply_safe_default -> split_one_task chain) is split further, because piece (c) has a genuine, separate unknown D3/D4 did not surface: split_one_task is not called anywhere in pingpong_job.py today (confirmed by grep — only a comment references it), and run_job's own dispatch loop (pingpong_job.py:1761) has no existing machinery to insert a split task's children back into the dispatch sequence or to skip/replace the current task after a split — that shape is unread and undesigned, and authoring it now without investigating run_job's own task-iteration structure first would repeat the mistake D5 corrected (shipping plumbing neither end of which is exercised). T003b2b2a (this round) ships pieces (a) and (b) only, with a specified, tested, safe behavior for the case fit_task_context_to_class_cap reports fits=False: fall through unchanged to the existing build_repo_context default path — the same fallback plan.md's Risks section already names as honest and accepted for a task with no Files: section at all. No escalation is raised this round. T003b2b2b (a future round) designs and ships piece (c) once the dispatch loop's task-queue mechanics are investigated fresh.

ALTERNATIVE CONSIDERED AND REJECTED. Build a repo-wide file listing (mirroring build_repo_context's own os.walk at pingpong_loop.py:745) as compiled_context_candidates, giving job-dispatch tasks a real tier-2/3/4 candidate pool beyond their declared Files: scope. Rejected for this round: it invents new repo-walk machinery for a benefit compile_task_context's own tier-2/3 derivation does not need (that derivation runs off the real import graph regardless of repo_paths) against a real cost — a second, untested code path, and a design question T3_F112.md's own design intent never answered (should job-dispatch tasks see the whole repo as candidates, or only their declared scope?) — that belongs with a feature-file amendment, not this fix. Reusing files_hint is smaller, is proven safe by compile_task_context's own documented behavior (MEASURED above), and does not foreclose building a wider candidate pool later if T3_F112.md's design is amended to want one.

CONSEQUENCE. docs/roadmap/features/T3_F112.md gains no new bullet this round: T003b2b2a/T003b2b2b are DECISION-level sub-slices of the existing T003 bullet, the same status D1-D4 already gave T003a through T003b2b1 — T003c was the one exception, promoted to its own bullet because it was a genuinely new job-markdown-syntax feature, not a wiring slice. .agent/plan.md Next Steps names T003b2b2a as this round's own work and T003b2b2b as the following round, with the run_job task-iteration investigation named as T003b2b2b's own prerequisite reading. packages/orchestration/pingpong_job.py's job-dispatch call site gains the fit_task_context_to_class_cap call and three new run_pingpong kwargs (compiled_context_paths, compiled_context_candidates, compiled_context_token_budget), all three staying None — today's exact default path, build_repo_context — whenever task.files_hint is empty or the fit does not fit under the task's class cap.

REVERSE by deleting this DECISION, reverting the pingpong_job.py call-site change, and treating T003b2b2 as D5 left it (a single three-piece slice) — which a fresh read of run_job's own dispatch loop (no split_one_task call anywhere in the file) would immediately re-discover unbuildable as one slice.

<<<END DECISION D6>>>

===AUTHORED BLOCK END===
