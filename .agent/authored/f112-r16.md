## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r16.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD15 (append to .agent/live_review.md, one-newline formula — `content_bytes + b"\n" + RECORD15_bytes`, 2347 bytes):

Gate: F112 R15 — the round 15 entry. VERDICT PASS, over the range `0fba8b0c..dd2135b6` (commits C0a through C6 — seven commits total this round, including DECISION commit C3 and prose-slip commit C4), independently reviewed by the reviewer at the start of this session's round 16. THE CODE HELD: `git show 70aef315` reproduced byte-for-byte the `planned_task_to_task_entry` function added to `packages/orchestration/pingpong_job.py` and the import-block addition plus three new tests appended to `tests/orchestration/test_job_task_runner.py`, matching the authored block exactly. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_job_task_runner.py -q` reproduced at 212 passed. THE LINT HELD: `python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_task_runner.py` reproduced "All checks passed!". THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE TRANSPORT HELD: `.agent/authored/f112-r15.md` and `.agent/last_block.md` compare equal (11987 bytes both). THE LEDGER/DECISION/PLAN/SLIP APPENDS ALL HELD BYTE-IDENTICAL: `.agent/live_review.md` measured 2275307 bytes (2272920 + 1 + 2386, matching RECORD14's own pinned size); `.agent/decisions.md` measured 778216 bytes (772449 + 1 + 5766, matching DECISION D7's own pinned size), tail matches D7's own final sentence; `.agent/plan.md` measured 2229 bytes / 47 content lines, matching PLAN15 exactly; `.agent/prose_slips.md` measured 69169 bytes (68405 + 763 + 1), tail matches the session-number slip exactly, no stray blank line before it. THE SESSION-NUMBER CORRECTION HELD: `.agent/handoff.md` states "SESSION 5" and names the round-14 lapse explicitly. THE MUTATION RED-PROOF HELD: reproduced independently in a fresh disposable worktree (`.remedy-wt/f112-r15-review`, removed after), off commit `dd2135b6`. Changing `task_class=task_class,` to `task_class=TASK_CLASS_DEFAULT,` inside `planned_task_to_task_entry` reproduced exactly the handback's predicted result: `test_basic_field_mapping` and `test_round_trips_through_split_one_task_with_ids_and_class_preserved` went RED (`AssertionError: assert 'standard_build' == 'format'`) while `test_task_class_defaults_to_standard_build` stayed GREEN, 2 failed / 1 passed. `git status --porcelain` read empty throughout, including after the worktree's removal.

<<<END RECORD15>>>

PLAN16 (whole-file replacement of .agent/plan.md, no trailing newline, 2165 bytes, 46 content lines):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1/T003c/T003b2b2a/T003b2b2b1 complete and green as of round 15;
round 16 builds T003b2b2b2, the dispatch-loop wiring (DECISION F112 D8).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 16, session 5 — ships T003b2b2b2 per DECISION F112 D8: a cannot_fit
result now calls enqueue_task_decision/auto_apply_safe_default, and on
the "split task" default, split_one_task's children (via
planned_task_to_task_entry) replace the parent task in job.tasks. New
TASK_SPLIT status; the loop's own skip condition and its
select_next_predictable_task mirror both updated; run_job's all_done
completion check now includes TASK_SPLIT (a defect D7 did not surface,
found only by running the round's own test end-to-end). T3_F112.md's own
T003 description is now true at the dispatch-loop level.

## Next Steps

- Acceptance fixtures per T3_F112.md's own Acceptance section.
- The integration gate (full suite, twice per feature per
  docs/agents/integration_gate.md), then closure.

## Risks

- Split children inherit the parent's full files_hint and so re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section);
  accepted, not a defect, but worth knowing before reading an escalation
  ledger for a split job.
- The integration gate has not run this feature yet; F112's own footprint
  (prompt_budget.py, context_compiler.py's fit function, pingpong_job.py's
  dispatch loop) is wide enough that a full-suite pass is not yet proven.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.

<<<END PLAN16>>>

DECISION F112 D8 (append to .agent/decisions.md, one-newline formula — `content_bytes + b"\n" + D8_bytes`, 8435 bytes):

## DECISION F112 D8 (2026-09-04, F112 R16) — T003b2b2b2's actual dispatch-loop wiring: a new TASK_SPLIT status, two (not four) skip-condition call sites, a completion-check fix D7 did not anticipate, and an accepted redundant-escalation behavior for split children

CONTEXT. This round builds T003b2b2b2 per DECISION F112 D7's CHOSEN clause, after re-reading run_job's dispatch loop and escalation.py fresh (D7's own standing instruction, since D7 explicitly declined to trust its own investigation for this round). The five pieces D7 named — a new TASK_* status, the enqueue_task_decision/auto_apply_safe_default calls, used_ids collection, safe post-idx insertion, and the loop's own skip condition — were confirmed still current (run_job's structure had not shifted since D7, only T003b2b2b1's unwired adapter was added), but the fresh re-read surfaced two things D7's own investigation had not: a SIXTH required change, and a real (harmless) interaction the design has to accept rather than solve.

MEASURED. Grepping every occurrence of the `(TASK_APPLIED, TASK_PASSED, TASK_SKIPPED)` / `(TASK_APPLIED, TASK_SKIPPED)` status-tuple pattern in `pingpong_job.py` found FOUR call sites, not the one D7's own reading implied: the main dispatch loop's skip condition (`pingpong_job.py:2363` at D7's read, `:2368` after this round's edit), `select_next_predictable_task`'s mirror of that same rule (`:1725`/`:1730`, whose own comment says "the SAME pre-fill the loop does" — read and confirmed as a genuine duplicate of the loop's own logic, not a coincidence), a per-event "completed/pending" counter inside a STOP-postmortem log write (`:3158`, unchanged — cosmetic reporting for one log entry, not a correctness path, confirmed by reading its caller), and a task-status reset inside `_stop_job` (`:3251`, unchanged — reads `task.status not in (...)` to decide whether to roll an interrupted task back to PENDING; confirmed unreachable for TASK_SPLIT by construction, since a split task is marked and `continue`s BEFORE `run_pingpong` is ever called, so it can never be "the task that was running" when a stop signal interrupts a live dispatch). Two of the four needed `TASK_SPLIT` added; two did not, for the two different reasons stated. A SIXTH change, found only by reading `run_job`'s own completion determination (`:2653-2654`, unchanged from D7's reading — D7 never read this far): `all_done = all(t.status in (TASK_APPLIED, TASK_SKIPPED) for t in job.tasks)` does not include the new status, so a job whose only unresolved task became `TASK_SPLIT` would never reach `JOB_COMPLETED` — its children could all apply successfully and the job would still read `running` forever. Caught only by writing the round's own test end-to-end and reading `result.status`, not by any earlier static read. Reused as this round's mutation red-proof #2 (removing `TASK_SPLIT` from this tuple reproduces exactly the stuck-`running` symptom). Finally: `_split_task` (task_granularity.py:198-208) has children inherit the parent's FULL `files_hint` whenever a cluster's own file list is empty ("an over-broad hint is less harmful than none"), and `planned_task_to_task_entry` carries that same `files_hint` through — so a split child is dispatched with the SAME fenced scope its parent had, and if the class cap that made the parent `cannot_fit` still applies, the child ALSO fails to fit and ALSO escalates. Measured directly (this round's own test): a two-cluster split under a forced `default_cap=1` produced three escalation records, not one — the parent's (which produced the real split) and one per child (each of which asks, gets the same "split task" default, calls `split_one_task` again, gets `None` back because a single-acceptance-item task cannot usefully split further, and falls through to a normal dispatch) — and the job still reaches `JOB_COMPLETED` correctly, because each child's own fallback is the same safe uncapped-dispatch path a task with no `Files:` section already takes.

CHOSEN. `TASK_SPLIT = "split"` is added among the existing `TASK_*` constants. The main dispatch loop's `else` branch (when `fit_result.fits` is `False`) calls `enqueue_task_decision` with the exact question/options/safe_default `TestJobPlanCompatibility` (`tests/orchestration/test_escalation.py:1120-1143`, DECISION F112 D4's own precedent) already proved against a `JobPlan`/`TaskEntry`, then `auto_apply_safe_default` — unattended by construction, per T3_F112.md's own T003 description ("the decision wiring + unattended default (split)"), since `run_job` has no attended/unattended mode distinction to gate on and inventing one is out of this round's scope. When the answer is `"split task"`, `task_entry_to_planned_task` + `split_one_task` (with `used_ids` collected from the FULL current `job.tasks`, not just the parent's own id, closing D7's own collision-risk note) produce the children, `planned_task_to_task_entry` converts each back, and `job.tasks[idx + 1:idx + 1] = split_entries` inserts them immediately after the parent — the loop's own `enumerate(job.tasks)` iterator sees them on its next step (confirmed by this round's own passing test, not merely asserted). The parent is marked `TASK_SPLIT` and the iteration `continue`s, skipping `run_pingpong` for it entirely — it never dispatches, matching the design's own point (an oversized task is replaced, not run truncated). When `split_one_task` returns `None` (unsplittable) or `task_entry_to_planned_task` returns `None` (no non-blank acceptance), `split_entries` stays empty and the task falls through to today's exact uncapped dispatch — the same honest degrade DECISION F112 D6 already established for a task with no `Files:` section at all. The redundant child re-escalation (MEASURED above) is accepted AS-IS, not engineered around: it is harmless (each child's own fallback is already the safe, tested, existing path), and the only fix available this round — stripping `files_hint` from split children before dispatch — would make a genuinely over-broad hint into no hint at all, contradicting `_split_task`'s own documented reasoning one layer up, for a benefit (fewer redundant ledger rows) this round's own Goal statement does not ask for.

ALTERNATIVE CONSIDERED AND REJECTED. Prevent child re-escalation by clearing `files_hint` on split children inside `planned_task_to_task_entry` or at the call site. Rejected: `_split_task`'s own design (task_granularity.py, unchanged, out of this feature's Do-not-touch scope) already decided that an over-broad `files_hint` on a child is "less harmful than none" — silently discarding it here would second-guess a settled, tested design one layer removed from this round's actual job, for a purely cosmetic benefit (a shorter escalation ledger) against a real cost (a child that legitimately COULD have used its inherited scope for context compilation loses that entirely, for every future task-class-cap tightening, not just this one). The three-record outcome is verbose but correct; verbosity is not this round's problem to solve.

CONSEQUENCE. `packages/orchestration/pingpong_job.py` gains: the `TASK_SPLIT` constant; `TASK_SPLIT` added to the main dispatch loop's skip condition and to `select_next_predictable_task`'s mirror of it; `TASK_SPLIT` added to `run_job`'s `all_done` completion check; the `else` branch on `fit_result.fits` wiring `enqueue_task_decision`/`auto_apply_safe_default`/`split_one_task`/`planned_task_to_task_entry` together at the dispatch site. `docs/roadmap/features/T3_F112.md` gains no new bullet — T003b2b2b2 is the last DECISION-level sub-slice of the existing T003 bullet, and with it T3_F112.md's own T003 description ("the decision wiring + unattended default (split) + an end-to-end where the split resolves the fit + tests") is now literally true at the dispatch-loop level, not only at the escalation-chain level D5's CONSEQUENCE settled for. `.agent/plan.md` Next Steps moves on from T003b2b2b entirely to acceptance fixtures and the integration gate.

REVERSE by deleting this DECISION and reverting every `pingpong_job.py` change it names (the constant, the two skip-condition additions, the `all_done` addition, and the dispatch-site wiring) — which a fresh read of `run_job`'s own `all_done` check (unwatched by D7, watched by this round) would immediately re-discover necessary the moment any split-capable job actually ran to completion.

<<<END DECISION D8>>>

===AUTHORED BLOCK END===