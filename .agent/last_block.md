## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r10.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD9 (append to .agent/live_review.md, one-newline formula — i.e. `content_bytes + b"\n" + RECORD9_bytes`):

Gate: F112 R9 — the round 9 entry. VERDICT PASS, over the range `66401f61abd4aca7e410634019647274ce8ebd08..58cfae0e` (commits C0a through C6), independently reviewed by the reviewer at the start of session 3's round 10 (round 9 ended session 3's own round budget; this booking follows amend0827-process-diet rule 1, the round after next per round 9's own handoff). THE FIELD ADDITION HELD: `git diff 66401f61..58cfae0e -- packages/orchestration/pingpong_job.py` reproduced the exact four-hunk diff C4 describes — TASK_CLASS_DEFAULT constant, the task_class field on TaskEntry, and its export/import round-trip. THE TESTS HELD: `git diff 66401f61..58cfae0e -- tests/orchestration/test_job_task_runner.py` reproduced the exact three new TestPersistence tests C5 describes, and `python3 -m pytest tests/orchestration/test_job_task_runner.py -q` reproduced at 196 passed. THE LEDGER APPENDS HELD BYTE-IDENTICAL: `.agent/authored/f112-r9.md` and `.agent/last_block.md` compare equal; `.agent/plan.md`'s tail matches PLAN9 exactly; `.agent/decisions.md`'s tail matches DECISION F112 D2 exactly, ending "REVERSE by deleting this DECISION and treating T003b as a single unsplit round again."; `.agent/live_review.md`'s tail matches RECORD8 exactly, ending "...rather than spending a round of its own.". DECISION F112 D2's factual claim was re-verified fresh: `split_one_task` (task_granularity.py:213) takes `PlannedTask` (schemas/models.py:136), never `TaskEntry`. THE LINT HELD: `python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_task_runner.py` read "All checks passed!". THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE MUTATION CLEANUP HELD BUT WAS NOT RE-EXECUTED: `git worktree list` showed no `f112-r9-mutation` worktree and `git status --porcelain` read empty in the primary checkout, corroborating the handback's cleanup claim without re-running the mutation itself. `git status --porcelain` also read empty before this reading began.

<<<END RECORD9>>>

PLAN10 (whole-file replacement of .agent/plan.md, no trailing newline, 2166 bytes):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1 complete and
green as of round 9.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 10, session 3 — fresh investigation over T003b2's call site (per
DECISION F112 D2's own instruction to re-read fresh before authoring)
found run_pingpong has no token-budget passthrough: wiring
compiled_context_paths/candidates alone recompiles at
compile_task_context's DEFAULT budget, never the class cap (DECISION
F112 D3). T003b2 splits further into T003b2a (this round: the
TaskEntry->PlannedTask adapter + a compiled_context_token_budget
passthrough on run_pingpong, both unit-tested in isolation) and T003b2b
(deferred: the live call-site wiring).

## Next Steps

- T003b2b (own dedicated round(s)): call fit_task_context_to_class_cap
  between _build_task_prompt and task.status = TASK_RUNNING; pass its
  compiled paths, the job's repo candidate listing, and cap_tokens into
  run_pingpong(compiled_context_paths=..., compiled_context_candidates=...,
  compiled_context_token_budget=...); on cannot_fit call
  enqueue_task_decision (options=["split task"] only when
  task_entry_to_planned_task(task) is not None and split_one_task on its
  result returns non-None) then auto_apply_safe_default under --yes.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b is still the highest-risk remaining slice — first-time wiring
  against the live dispatch loop; re-read the call site fresh again
  before authoring it, per DECISION F112 D2/D3.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.

<<<END PLAN10>>>

DECISION F112 D3 (append to .agent/decisions.md, one-newline formula, 5085 bytes):

## DECISION F112 D3 (2026-09-03, F112 R10) — run_pingpong has no token-budget passthrough; wiring compiled_context_paths/candidates alone would silently ignore the class cap, so T003b2 splits further into T003b2a (this round) and T003b2b (deferred)

CONTEXT. DECISION F112 D2 (F112 R9) split T003b into T003b1 (landed) and T003b2, and named T003b2's own re-read-fresh obligation before authoring: "the fit_task_context_to_class_cap call... wiring its compiled paths into this loop's run_pingpong(compiled_context_paths=..., compiled_context_candidates=...)". Fresh investigation this round (reviewer, read-only, over packages/orchestration/pingpong_loop.py's run_pingpong and packages/orchestration/context_compiler.py's fit_task_context_to_class_cap/compile_task_context) found that wiring, read literally, does not enforce the class cap at all: run_pingpong's use_compiled_context branch calls compile_task_context with no token_budget argument, so it always compiles at compile_task_context's own DEFAULT_CONTEXT_TOKEN_BUDGET regardless of what fit_task_context_to_class_cap resolved for the task's class — the exact silent ballooning T3_F112.md's Goal & Done exists to close.

MEASURED. run_pingpong's signature (pingpong_loop.py:2848) declares compiled_context_paths and compiled_context_candidates (pingpong_loop.py:2863-2864) but no budget parameter of any kind. Its use_compiled_context branch's own call, `compiled = compile_task_context(compiled_root, compiled_context_paths, compiled_context_candidates,)` (pingpong_loop.py:3132-3134), passes only the two positional path lists; compile_task_context's own signature (context_compiler.py:741-748) defaults token_budget to DEFAULT_CONTEXT_TOKEN_BUDGET = 24000 (context_compiler.py:604) whenever the caller omits it. fit_task_context_to_class_cap (context_compiler.py:952-971) resolves a per-class cap_tokens via resolve_task_class_cap and calls compile_task_context ITSELF with that budget, returning a ClassBudgetFit — it never hands run_pingpong anything run_pingpong's own signature accepts. No existing test exercises run_pingpong's use_compiled_context branch at all (grep over tests/orchestration/ for use_compiled_context and COMPILED_CONTEXT_SEGMENT_NAME finds only tests/orchestration/test_context_compiler.py, which never imports run_pingpong) — the branch is reachable dead code today, consistent with DECISION F112 D2's own MEASURED finding that no caller passes either path list yet.

CHOSEN. Add one new keyword parameter to run_pingpong, compiled_context_token_budget: int | None = None (pingpong_loop.py, beside compiled_context_candidates), threaded into the use_compiled_context branch's compile_task_context call only when the caller supplies a value — `compile_kwargs = {"token_budget": compiled_context_token_budget} if compiled_context_token_budget is not None else {}`, then `compile_task_context(..., **compile_kwargs)`. Every existing and hypothetical caller that omits the new parameter keeps today's exact behavior (compile_task_context's own default), so this is additive, not a behavior change to any landed caller. T003b2 splits further: T003b2a (this round) ships the parameter plus its own unit test proving the kwarg reaches compile_task_context, and, independently, the TaskEntry->PlannedTask adapter DECISION F112 D2 already named, with its own unit tests including one round-trip through the real split_one_task. T003b2b (a later round) becomes the live wiring alone: the fit_task_context_to_class_cap call at the dispatch site, the run_pingpong call passing compiled_context_token_budget=fit_result.cap_tokens, and the cannot_fit -> enqueue_task_decision -> auto_apply_safe_default chain — three still-untested pieces against the live loop instead of five, since the two general-purpose building blocks (the parameter, the adapter) are proven in isolation first.

ALTERNATIVE CONSIDERED AND REJECTED. Wire compiled_context_paths/candidates into run_pingpong as plan.md literally named, without a budget passthrough, and treat the cap enforcement gap as a follow-up. Rejected: T3_F112.md's Goal & Done is "no prompt can silently balloon" and "DONE when... an unfittable fixture produces the split decision" — shipping the wiring without the budget means every task that FITS under the class cap (the common case) still compiles at the generic 24000-token default, so the feature's own acceptance criterion would read green while the behavior it certifies is absent from the live path. Deferring that gap silently is worse than the extra parameter.

CONSEQUENCE. .agent/plan.md Next Steps is rewritten to name T003b2a (this round's scope) then T003b2b with the narrowed three-piece list. docs/roadmap/features/T3_F112.md stays unedited this round: its Design section already says "fit(context, cap)" without naming run_pingpong's own parameters, so no sentence there is contradicted by this addition.

REVERSE by deleting this DECISION, removing the compiled_context_token_budget parameter and its call-site kwarg, and treating T003b2 as D2 left it (a single five-piece round).

<<<END D3>>>

===AUTHORED BLOCK END===
