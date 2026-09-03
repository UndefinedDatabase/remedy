## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r15.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD14 (append to .agent/live_review.md, one-newline formula — `content_bytes + b"\n" + RECORD14_bytes`, 2386 bytes):

Gate: F112 R14 — the round 14 entry. VERDICT PASS, over the range `5c05e0cb..0fba8b0c` (commits C0a through C5 — seven commits total this round, including DECISION commit C3), independently reviewed by the reviewer at the start of this new session's round 15. THE CODE HELD: `git show 44c517289f0d5` reproduced byte-for-byte the two REWRITE pairs in `packages/orchestration/pingpong_job.py` (the fit_task_context_to_class_cap check, the three new run_pingpong kwargs) and the three new tests appended to `tests/orchestration/test_job_task_runner.py`, matching the authored block exactly. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_job_task_runner.py -q` reproduced at 209 passed. THE LINT HELD: `python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_task_runner.py` reproduced "All checks passed!". THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE TRANSPORT HELD: `.agent/authored/f112-r14.md` and `.agent/last_block.md` compare equal (10458 bytes both). THE LEDGER APPENDS HELD BYTE-IDENTICAL: `.agent/live_review.md` measured 2272920 bytes (2271288 + 1 + 1631, matching RECORD13's own pinned size); `.agent/decisions.md` measured 772449 bytes (766660 + 1 + 5788, matching DECISION D6's own pinned size), tail matches D6's own final sentence exactly; `.agent/plan.md` measured 2394 bytes / 49 content lines, matching PLAN14 exactly. THE MUTATION RED-PROOF HELD: reproduced independently in a fresh disposable worktree (`.remedy-wt/f112-r14-review`, removed after), off commit `0fba8b0c`. Changing `if fit_result.fits:` to `if True:` reproduced exactly the handback's predicted result: `test_a_files_hint_that_cannot_fit_its_class_cap_falls_through_unchanged` went RED (`AssertionError: assert ['src/main.py', 'docs/README.md'] is None`) while the other two targeted tests stayed GREEN, 1 failed / 2 passed. `git status --porcelain` read empty throughout, including after the worktree's removal. ONE REVIEWER-PROCESS SLIP FOUND, NOT A DEFECT ON DISK UNDER packages/apps/tests/docs: the round 14 block inherited the SESSION label "SESSION 4" verbatim from round 13's handback instead of incrementing it — planner_reviewer_prompt.md's own rule states a fresh bootstrap's session is the carried number plus one. Logged in `.agent/prose_slips.md`, corrected from round 15 (SESSION 5) forward.

<<<END RECORD14>>>

PLAN15 (whole-file replacement of .agent/plan.md, no trailing newline, 2229 bytes, 47 content lines):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1/T003c/T003b2b2a complete and green as of round 14; round 15
splits T003b2b2b into T003b2b2b1/T003b2b2b2 (DECISION F112 D7).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 15, session 5 — builds T003b2b2b1 per DECISION F112 D7's CHOSEN
clause: `planned_task_to_task_entry` (the reverse of the existing
`task_entry_to_planned_task`) turns one `split_one_task` child
`PlannedTask` back into a dispatchable `TaskEntry`. Not called from
`run_job` this round — a prerequisite building block only, same shape
T003c used before T003b2b2a wired it.

## Next Steps

- T003b2b2b2 (own round(s)): the actual dispatch-loop wiring — a new
  TASK_* status for "replaced by a split", the enqueue_task_decision /
  auto_apply_safe_default calls, used_ids collection from the live
  job.tasks list, safe post-idx insertion, and the loop's own skip
  condition for the new status. Re-read run_job fresh before authoring
  (D7's own standing instruction) rather than trust this round's reading.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2b2 remains the highest-risk remaining slice, now for five
  separately-named reasons (DECISION F112 D7's MEASURED section) rather
  than one; re-read run_job's dispatch loop fresh before authoring.
- A task with no Files: section, or one whose fenced scope cannot fit its
  class cap, still falls through to build_repo_context uncapped and now
  ALSO never reaches an escalation — accepted default until T003b2b2b2
  lands, not a regression.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.

<<<END PLAN15>>>

DECISION F112 D7 (append to .agent/decisions.md, one-newline formula — `content_bytes + b"\n" + D7_bytes`, 5766 bytes):

## DECISION F112 D7 (2026-09-04, F112 R15) — T003b2b2b splits into T003b2b2b1 (the PlannedTask-to-TaskEntry reverse adapter, unwired) and T003b2b2b2 (the dispatch-loop wiring itself, deferred pending fresh investigation)

CONTEXT. Fresh investigation this round (reviewer, read-only, over run_job's own task-iteration structure, TaskEntry/JobPlan's field shapes, task_granularity.split_one_task's id scheme, and every TASK_* status constant) found that T003b2b2b — as D6 left it, "the cannot_fit -> enqueue_task_decision -> auto_apply_safe_default -> split_one_task chain" — is a substantially bigger unknown than a single round can safely design and ship at once, for reasons D6 did not yet have visibility into.

MEASURED. run_job's dispatch loop (pingpong_job.py:2336, `for idx, task in enumerate(job.tasks):`) iterates the LIVE `job.tasks` list object, so an insertion after the current `idx` is visible to later iterations — ordinary list-iteration semantics, not something this codebase already exercises: grepping every `.tasks.append(`/`.tasks.insert(` call in packages/ found runtime insertion precedent only for the unrelated Core Job model (`packages/core/models.py`'s `Job.tasks`, in `repair_loop.py:914`, `job_fulfillment.py:659,730`, `proposed_tasks.py:670`) — none of it touches `JobPlan`/`TaskEntry`, the pingpong dispatch model this feature builds on. The only existing `JobPlan.tasks.append(...)` call (pingpong_job.py:760) is inside `_import_job`, i.e. deserialization at load time, never a runtime mutation during an active dispatch loop. `split_one_task` produces child ids by suffixing the parent's own id (`task_granularity.py:175-187`, e.g. parent `"T003"` -> children `"T003a"`, `"T003b"`, ...) against a `used_ids` set the CALLER supplies — under-populating that set at the dispatch-loop call site (which would need every existing job.tasks id, not just the parent's) is a real collision risk D6 never considered. No `TASK_*` status constant means "replaced by a split, do not dispatch directly" — the seven existing constants (pingpong_job.py:37-43) are all either normal progress states or `TASK_SKIPPED`, which specifically means "the job blocked and this never ran," a wrong label for a deliberate decomposition. And grepping pingpong_job.py for any existing call into `escalation.py` (`enqueue_task_decision`, `auto_apply_safe_default`, `needs_decision`) found none outside two forward-referencing comments — the dispatch loop has never yet called the escalation machinery at all, so pause-on-open-decision behavior is entirely unbuilt, not merely unwired.

CHOSEN. Split T003b2b2b in two. T003b2b2b1 (this round) ships only the mechanical, fully-specified, zero-risk half: `planned_task_to_task_entry`, the reverse of the already-shipped `task_entry_to_planned_task` (T003b2a) — turns one `split_one_task` child `PlannedTask` back into a dispatchable `TaskEntry`, with `task_class` and `source_heading_number` (fields `PlannedTask` does not carry) passed through by the caller. It is NOT called from `run_job` this round — exactly the same "prerequisite building block, unwired" shape T003c used for `files_hint` before T003b2b2a consumed it (DECISION F112 D5's own precedent). T003b2b2b2 (a future round) designs and ships the actual dispatch-loop wiring — the new `TASK_*` status, the `enqueue_task_decision`/`auto_apply_safe_default` calls, the `used_ids` collection, the safe post-`idx` insertion, and the loop's own skip condition for the new status — once each of those five pieces has been read fresh against the CURRENT state of `run_job` (which by then may itself have shifted), per the standing D2-D7 instruction to re-read the call site before authoring rather than trust an earlier round's reading of it.

ALTERNATIVE CONSIDERED AND REJECTED. Design and ship all of T003b2b2b in one round now, using this round's own investigation as the basis. Rejected: the investigation surfaced five separate genuine unknowns (list-mutation safety margin, id-collision defense, a missing status constant, an unbuilt escalation call, and the loop's own skip-condition change) with no existing precedent for any of them in this model — D2 through D6 have each cost a round precisely when a design was authored against fewer unknowns than the code actually held, and this round's own investigation is exactly the kind of fresh reading that pattern says to act on rather than override. Shipping the adapter alone is real, tested, useful progress with no reachability risk (docs/agents/planner_reviewer_prompt.md §3 item 5); shipping the wiring untested-by-necessity (no dispatch-loop insertion has ever run in this codebase) in the same round would repeat the exact mistake D5 corrected at the file-scope layer, one layer deeper.

CONSEQUENCE. docs/roadmap/features/T3_F112.md gains no new bullet: T003b2b2b1/T003b2b2b2 are DECISION-level sub-slices of the existing T003 bullet, the same status D1-D6 gave every prior sub-slice except T003c. `.agent/plan.md` Next Steps names T003b2b2b2 as the following round's own work, with this round's five MEASURED findings named as its own prerequisite reading. `packages/orchestration/pingpong_job.py` gains `planned_task_to_task_entry`, called from nowhere in production code yet — its own docstring says so, matching `files_hint`'s own T003c-era honesty about being unconsumed until its wiring round lands.

REVERSE by deleting this DECISION, reverting the `planned_task_to_task_entry` addition, and treating T003b2b2b as D6 left it (a single three-piece chain) — which a fresh read of run_job's dispatch loop (no split_one_task call, no escalation call, no status for a split-away task, anywhere in the file) would immediately re-discover unbuildable as one slice.

<<<END DECISION D7>>>

PROSE_SLIP (append to .agent/prose_slips.md, formula — the file currently ends with its own trailing newline, so append `SLIP_bytes + b"\n"` directly, 763 bytes for SLIP):

2026-09-04 · F112 R14 (reviewer) · The round 14 block inherited the SESSION label "SESSION 4" verbatim from round 13's handback instead of incrementing it — planner_reviewer_prompt.md §1 step 3 states a fresh bootstrap's session number is the carried value plus one, and this /build-remedy-self invocation was a fresh bootstrap, not a continuation of the session that produced round 13. THE LESSON: before authoring the first block of any invocation, check whether THIS bootstrap is a continuation or a fresh start, and bump the SESSION NUMBER on a fresh start rather than copying the prior handback's value forward; round 15 corrects the label to SESSION 5. Reviewer-prose tracking slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

<<<END PROSE_SLIP>>>

===AUTHORED BLOCK END===