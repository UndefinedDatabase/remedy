## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r18.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD17 (append to .agent/live_review.md, one-newline formula — `content_bytes + b"\n" + RECORD17_bytes`, 3250 bytes):

Gate: F112 R17 — the round 17 entry. VERDICT PASS, over the range `b41b2ea7..92f773c6` (commits C0a through C5 — six commits total this round, including DECISION commit C3), independently reviewed by the reviewer at the start of this session's round 18. THE CODE HELD: `git show 15afe6d5` reproduced byte-for-byte the `impact=` addition to the `enqueue_task_decision` call in `packages/orchestration/pingpong_job.py` and the three new assertion lines in `tests/orchestration/test_job_task_runner.py`, matching the authored block exactly. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_job_task_runner.py -q` reproduced at 214 passed. THE LINT HELD: `python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_task_runner.py` reproduced "All checks passed!". THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE TRANSPORT HELD: `.agent/authored/f112-r17.md` and `.agent/last_block.md` compare equal (11517 bytes both). THE LEDGER/DECISION/PLAN APPENDS ALL HELD BYTE-IDENTICAL: `.agent/live_review.md` measured 2280900 bytes; `.agent/decisions.md` measured 792132 bytes, tail matches D9's own final sentence; `.agent/plan.md` measured 2150 bytes / 47 content lines, matching PLAN17 exactly. THE MUTATION RED-PROOF HELD: reproduced independently in a fresh disposable worktree (`.remedy-wt/f112-r17-review`, removed after), off commit `92f773c6`. Changing `cap_tokens={fit_result.cap_tokens}` to `cap_tokens={fit_result.cap_tokens + 1}` reproduced exactly the handback's predicted result: `test_a_splittable_task_is_replaced_by_its_children` went RED on the `"cap_tokens=1" in records[0]["impact"]` assertion, with the exact same failing value the worker itself measured (`'tier1_tokens=10 cap_tokens=2 task_class=standard_build'`), while `test_an_unsplittable_task_falls_through_uncapped` stayed GREEN, 1 failed / 1 passed. `git status --porcelain` read empty throughout, including after the worktree's removal. ACCEPTANCE RE-VERIFICATION (per PLAN17's own Next Steps, DECISION F112 D9's CONSEQUENCE): the reviewer independently re-ran T3_F112.md's own Acceptance-relevant fixtures fresh, none of which any round 14-17 touched — `python3 -m pytest tests/orchestration/test_class_prompt_budget.py -q` (T001) → 24 passed; `python3 -m pytest tests/orchestration/test_context_compiler.py -q` (T002, including `test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded` and `test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic` by name) → 69 passed. Both Acceptance clauses this feature's own Design section names ("Oversized fixture fits under its cap with tier demotions recorded... Unfittable fixture: decision with correct arithmetic; --yes path splits and completes") are now confirmed met by shipped, passing, unregressed tests — the first two by T002's own long-standing fixtures, the third by round 16/17's own end-to-end test. "No mid-file truncation anywhere" has no dedicated guard test under that name; it is `compile_task_context`'s own documented invariant (context_compiler.py:775, unchanged since T002, "Nothing is ever truncated mid-content"), upheld by the same 69 passing tests rather than a separate check.

<<<END RECORD17>>>

PLAN18 (whole-file replacement of .agent/plan.md, no trailing newline, 2375 bytes, 49 content lines):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green as
of round 17; round 18 re-verifies T3_F112.md's Acceptance clauses
(confirmed met, no new code) and closes session 5 at the integration
gate boundary.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 18, session 5 (closing) — no code this round. Re-ran T3_F112.md's
Acceptance-relevant fixtures fresh: test_class_prompt_budget.py (T001,
24 passed), test_context_compiler.py (T002, 69 passed, including the
oversized/unfittable fixtures by name). Both confirmed unregressed by
rounds 14-17. All three Acceptance clauses (demotion recorded, decision
with correct arithmetic, --yes path splits and completes) are now met
by shipped, tested code — see RECORD17's own ACCEPTANCE
RE-VERIFICATION paragraph for the full citation.

## Next Steps

- SESSION 6 opens here: the integration gate
  (docs/agents/integration_gate.md) — branch run, base-worktree run
  with node_modules/dist parity, comparison, per-id attribution. This
  is its own dedicated round(s); do not fold it into a smaller round.
- Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence
  job, fresh review zip, the STATUS line, the PR.

## Risks

- The integration gate has not run this feature yet — F112's footprint
  (prompt_budget.py, context_compiler.py's fit function, pingpong_job.py's
  dispatch loop, escalation.py's now-exercised JobPlan compatibility) is
  wide enough that a full-suite pass is not yet proven end to end.
- Split children inherit the parent's full files_hint and so re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap for this job" / "proceed-overcap once"
  options are deliberately unbuilt (DECISION F112 D9) — no audit/
  attended-mode seam exists anywhere in this codebase to hook them to.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.

<<<END PLAN18>>>

===AUTHORED BLOCK END===
