## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r17.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD16 (append to .agent/live_review.md, one-newline formula — `content_bytes + b"\n" + RECORD16_bytes`, 3244 bytes):

Gate: F112 R16 — the round 16 entry. VERDICT PASS, over the range `dd2135b6..b41b2ea7` (commits C0a through C5 — six commits total this round, including DECISION commit C3), independently reviewed by the reviewer at the start of this session's round 17. THE CODE HELD: `git show 8d6f06df` reproduced byte-for-byte all five REWRITE pairs in `packages/orchestration/pingpong_job.py` (the TASK_SPLIT constant, both skip-condition additions, the cannot_fit escalation/split wiring, the all_done fix) and the import/fixture/test-class additions in `tests/orchestration/test_job_task_runner.py`, matching the authored block exactly, including the worker's own correctly-resolved 2-blank-line append convention. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_job_task_runner.py -q` reproduced at 214 passed. THE LINT HELD: `python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_task_runner.py` reproduced "All checks passed!". THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE BROADER SUITE HELD: `python3 -m pytest tests/orchestration/ -q -n auto` reproduced at 12743 passed, 10 skipped, 0 failed in the primary checkout (matching the worker's own reported favorable deviation — this checkout has `node_modules`, so the vitest-dependent test the reviewer's own disposable dry-run had flagged as a known unrelated gap passed here too; no other divergence). THE TRANSPORT HELD: `.agent/authored/f112-r16.md` and `.agent/last_block.md` compare equal (13591 bytes both). THE LEDGER/DECISION/PLAN APPENDS ALL HELD BYTE-IDENTICAL: `.agent/live_review.md` measured 2277655 bytes; `.agent/decisions.md` measured 786652 bytes, tail matches D8's own final sentence; `.agent/plan.md` measured 2165 bytes / 46 content lines, matching PLAN16 exactly. BOTH MUTATION RED-PROOFS HELD: reproduced independently in fresh disposable worktrees (`.remedy-wt/f112-r16-review`, removed after each), off commit `b41b2ea7`. Mutation 1 (`answered["answer"] == "split task"` inverted to `!=`) reproduced exactly: `test_a_splittable_task_is_replaced_by_its_children` RED on the task_id-list assertion, `test_an_unsplittable_task_falls_through_uncapped` GREEN, 1 failed / 1 passed. Mutation 2 (`TASK_SPLIT` removed from the `all_done` tuple) reproduced exactly: the same test RED specifically on `assert result.status == JOB_COMPLETED` (`'running' == 'completed'`), the other test GREEN, 1 failed / 1 passed. `git status --porcelain` read empty throughout, including after both worktrees' removal. A FRESH RE-READ OF T3_F112.md's OWN ACCEPTANCE SECTION (not done since round 12, per the standing D2-D9 instruction) found one real gap this round's own work does not close: the Design section's cannot_fit decision is specified to carry "the arithmetic (tier-1 size, cap, class)" and this round's `enqueue_task_decision` call passes no `impact=` argument at all — Acceptance's own "decision with correct arithmetic" clause is therefore not yet met. Not a defect of round 16's own stated scope (DECISION F112 D8 never claimed to address it), routed to round 17 as DECISION F112 D9 rather than an R-id, per item 30 (this is new-information planning content, not a defect already on disk).

<<<END RECORD16>>>

PLAN17 (whole-file replacement of .agent/plan.md, no trailing newline, 2150 bytes, 47 content lines):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a-T003b2b2b2 complete
and green as of round 16; round 17 closes an Acceptance gap the round
16 code left open (DECISION F112 D9): the cannot_fit decision now
carries its arithmetic.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 17, session 5 — per DECISION F112 D9: enqueue_task_decision's call
gains impact=f"tier1_tokens=... cap_tokens=... task_class=..." sourced
from the already-computed fit_result, closing Acceptance's "decision
with correct arithmetic" clause. The Design section's other two options
(raise cap for this job, proceed-overcap once — both "audited", with no
audit/attended-mode seam anywhere in this codebase) stay unbuilt,
explicitly named as an Acceptance-permitted narrowing, not silently
dropped.

## Next Steps

- Re-verify (not re-build) T3_F112.md's remaining Acceptance clauses
  against T002's already-existing fixtures
  (test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded,
  test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic)
  before claiming Acceptance met in full.
- The integration gate (full suite, twice per feature per
  docs/agents/integration_gate.md), then closure.

## Risks

- The integration gate has not run this feature yet; re-confirm before
  closure that nothing outside packages/orchestration regressed.
- Split children inherit the parent's full files_hint and so re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.

<<<END PLAN17>>>

DECISION F112 D9 (append to .agent/decisions.md, one-newline formula — `content_bytes + b"\n" + D9_bytes`, 5479 bytes):

## DECISION F112 D9 (2026-09-04, F112 R17) — the cannot_fit decision now carries its arithmetic via enqueue_task_decision's impact= parameter; the Design section's other two options (raise cap for this job, proceed-overcap once) stay unbuilt and are named as a deliberate, Acceptance-permitted narrowing

CONTEXT. T3_F112.md's own Acceptance section (re-read fresh at the start of this round — not re-read since round 12, per the standing D2-D8 instruction to re-check the target before authoring) states: "Unfittable fixture: decision with correct arithmetic; --yes path splits and completes." DECISION F112 D8 (round 16) shipped the second half — the split path completes, tested end-to-end — but never added arithmetic to the `enqueue_task_decision` call, because D6/D7/D8 each scoped their own round narrowly around the SPLIT mechanics and none of them re-read Acceptance's own wording against the shipped call site. `enqueue_task_decision`'s signature already carries an `impact: str = ""` parameter (escalation.py:211-219, confirmed unchanged since D4) that round 16's call never passed.

MEASURED. `ClassBudgetFit` (context_compiler.py:933-947, unchanged since T002) already carries every number Acceptance's "arithmetic" phrase names: `tier1_tokens`, `cap_tokens`, `task_class` — all three already computed as `fit_result.tier1_tokens`/`.cap_tokens`/`.task_class` at the exact call site the decision is raised from (pingpong_job.py, the `else` branch on `fit_result.fits`), so no new computation is needed, only passing values already in scope. Separately, T3_F112.md's Design section names THREE options for the decision — "split task ..., raise cap for this job (audited), proceed-overcap once (audited, unattended default NO)" — and D8's own CHOSEN clause built exactly one (`options=["split task"]`). Grepping the whole codebase found no existing "audited" approval/attended-mode machinery anywhere `enqueue_task_decision`/`auto_apply_safe_default` could hook into (the same gap DECISION F112 D8's own CHOSEN clause already noted for "no attended/unattended mode distinction" in `run_job`) — building either of the other two options would mean inventing that machinery from nothing, not merely wiring an existing seam, which no round since D2 has scoped as this feature's job.

CHOSEN. `enqueue_task_decision`'s call gains `impact=f"tier1_tokens={fit_result.tier1_tokens} cap_tokens={fit_result.cap_tokens} task_class={fit_result.task_class}"` — the exact three figures Acceptance names, sourced directly from the already-computed `fit_result`, closing the arithmetic gap with no new computation. The `options=["split task"]` list stays as D8 shipped it: listing "raise cap for this job" or "proceed-overcap once" as answerable options when neither has any code path that acts on that answer would be actively misleading (Code Discoverability Conventions: a deliberate absence is documented where a reader would search for it, not papered over with an unactionable label), so this DECISION states the narrowing explicitly instead. Acceptance's own sentence — "decision with correct arithmetic; --yes path splits and completes" — names neither of the other two options as a DONE condition; only the arithmetic and the split-completes path are, and both are now met.

ALTERNATIVE CONSIDERED AND REJECTED. Build "raise cap for this job (audited)" and/or "proceed-overcap once (audited, unattended default NO)" this round to match the Design section's full three-option list. Rejected: both are explicitly marked "audited" in the feature file's own wording, meaning a human-approval/attended-mode record this codebase has no seam for at all — `run_job` has no attended-mode flag, `escalation.py`'s `auto_apply_safe_default` docstring says plainly "the caller decides whether the run is unattended," and no caller anywhere makes that decision today. Inventing that machinery is a materially larger, separate piece of work than anything D2 through D9 has scoped, it is not required by Acceptance's own DONE bar (quoted above), and T3_F112.md's "Enhanced by: F074 calibrated class caps" line already signals this feature accepts staged completion against its own Design section. Building it speculatively now, un-requested by Acceptance, would be exactly the "while I'm here" scope creep AGENTS.md's Scope Control section forbids.

CONSEQUENCE. `packages/orchestration/pingpong_job.py`'s `enqueue_task_decision` call gains one `impact=` argument; no other production code changes. `tests/orchestration/test_job_task_runner.py`'s `test_a_splittable_task_is_replaced_by_its_children` gains three assertions on `records[0]["impact"]`'s content. `docs/roadmap/features/T3_F112.md` is not amended — this DECISION is the record of a scope narrowing already implicit since D6, made explicit rather than silently assumed, and Acceptance's own two DONE clauses ("decision with correct arithmetic", "--yes path splits and completes") are both now met by shipped, tested code. `.agent/plan.md` Next Steps proceeds to the remaining Acceptance clauses (the oversized/unfittable context-compiler fixtures, already met by T002's own existing tests, confirmed rather than re-verified) and the integration gate.

REVERSE by deleting this DECISION and reverting the `impact=` argument and its three test assertions — which a fresh re-read of T3_F112.md's Acceptance section against the shipped `enqueue_task_decision` call would immediately re-discover incomplete.

<<<END DECISION D9>>>

===AUTHORED BLOCK END===