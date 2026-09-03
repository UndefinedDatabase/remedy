# Handoff — F112 Prompt budget per task class, round 16 (T003b2b2b2: the dispatch-loop wiring — cannot_fit escalation, split_one_task, TASK_SPLIT)

## Session

SESSION 5 of feature F112 · round 16 · rounds so far 16.

This round books round 15's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD15, amend0827 rule 1 — a pending
verdict books in the FIRST COMMIT of the next round that is happening
anyway), registers DECISION F112 D8 (T003b2b2b2's actual dispatch-loop
wiring, following a fresh re-read of `run_job` and `escalation.py` per
D7's own standing instruction — surfacing a sixth required change
D7 had not seen: `run_job`'s `all_done` completion check did not
include the new status, so a fully-split job would never reach
`JOB_COMPLETED`), then ships **T003b2b2b2**: when a task's
`files_hint` cannot fit its class cap, the dispatch loop now calls
`enqueue_task_decision`/`auto_apply_safe_default`, and on the "split
task" default, `split_one_task`'s children (converted back via
`planned_task_to_task_entry`) replace the parent task in `job.tasks`.
A new `TASK_SPLIT` status was added, wired into the loop's own skip
condition, `select_next_predictable_task`'s mirror of it, and
`run_job`'s `all_done` completion check.

This round ships production code: two files touched
(`packages/orchestration/pingpong_job.py`,
`tests/orchestration/test_job_task_runner.py`), 163 insertions total —
well under the 500-line cap. DECISION F112 D8 was pre-authored and
registered this round (C3), settling T003b2b2b2's actual wiring shape,
including the SIXTH change (the `all_done` fix) D7's own investigation
had not surfaced.

## Range

Review of `dd2135b6..8d6f06df` (commits C0a, C0b, C1, C2, C3, C4, plus
this handback commit C5 itself — seven commits total this round).
**This range is UNREVIEWED by construction** — round 16 has not yet
been independently re-reviewed by the reviewer; no verdict on this
round's own work is claimed anywhere in this file.

## Commits

### e3b6d6af F112 R16 C0a: save round 16 block to .agent/authored/f112-r16.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r16.md` | 82/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). Byte counts of every sub-block re-verified programmatically before commit: RECORD15 2347 bytes, PLAN16 2165 bytes/46 lines/no trailing newline, DECISION D8 8435 bytes — all matched the block's own pinned figures exactly. |

### f5c934f0 F112 R16 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 36/43 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). Verified with `cmp` directly (not denied this round) — exit 0, both files 13591 bytes. |

### 45db8698 F112 R16 C1: append RECORD15 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD15 (round 15's verdict) via `content_bytes + b"\n" + RECORD15_bytes` — the ONE-newline formula, extracted programmatically from the committed authored file. |

### b930d23b F112 R16 C2: apply PLAN16 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 21/22 | Whole-file replacement with PLAN16, extracted programmatically from the committed authored file, not retyped. No trailing newline (per the block). |

### 014d1373 F112 R16 C3: append DECISION F112 D8 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/1 | Appended DECISION F112 D8 via `content_bytes + b"\n" + D8_bytes` — the ONE-newline formula. Records T003b2b2b2's actual dispatch-loop wiring: the new `TASK_SPLIT` status, which of the four `(TASK_APPLIED, TASK_PASSED, TASK_SKIPPED)`-pattern call sites needed it (two did, two didn't, for stated reasons), the sixth change (`all_done`'s own completion check) D7 never read far enough to see, and the accepted redundant-child-re-escalation behavior. |

### 8d6f06df F112 R16 C4: wire cannot_fit -> enqueue_task_decision -> auto_apply_safe_default -> split_one_task into the dispatch loop (T003b2b2b2)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 46/3 | Five REWRITE pairs (each grep-confirmed exactly one occurrence before applying): (1) adds the `TASK_SPLIT = "split"` constant after `TASK_SKIPPED`; (2) adds `TASK_SPLIT` to `select_next_predictable_task`'s skip-condition mirror; (3) adds `TASK_SPLIT` to the main dispatch loop's own skip condition; (4) adds an `else` branch on `fit_result.fits is False` that calls `enqueue_task_decision`/`auto_apply_safe_default`, and on a `"split task"` answer, converts the task via `task_entry_to_planned_task`, splits it via `split_one_task` (with `used_ids` collected from the full `job.tasks`), converts each child back via `planned_task_to_task_entry`, inserts the children at `job.tasks[idx+1:idx+1]`, marks the parent `TASK_SPLIT`, persists, and `continue`s — falling through to the existing uncapped dispatch when unsplittable; (5) adds `TASK_SPLIT` to `run_job`'s `all_done` completion check. The two call sites DECISION D8's MEASURED section named as correctly left untouched (`:3158`'s cosmetic postmortem counter, `:3251`'s `_stop_job` reset) were confirmed unreached — grepped, read, and left alone. |
| `tests/orchestration/test_job_task_runner.py` | 117/0 | Part A: one-line REWRITE adding `TASK_SPLIT,` to the import list (grep-confirmed exactly one occurrence before applying). Part B: one REWRITE pair adding the `_JOB_WITH_FILES_MULTI_ACCEPTANCE` fixture (two acceptance items, so its parent task splits into two children under a tiny cap) right after `_JOB_WITH_FILES`. Part C: byte-exact file-end append (verified via ordered-equality — the file state after Parts A+B is an exact PREFIX of the post-edit file, the appended bytes are an exact SUFFIX, confirmed programmatically) of `TestClassBudgetCannotFitEscalation`, two tests: a splittable task whose children apply and the job reaches `JOB_COMPLETED` (with the three-record redundant-escalation behavior DECISION D8 MEASURED and accepted, explicitly asserted), and an unsplittable task (`_JOB_WITH_FILES`, one acceptance item) falling through to a normal uncapped dispatch exactly as the pre-existing `test_a_files_hint_that_cannot_fit_its_class_cap_falls_through_unchanged` test already covered from the `run_pingpong`-kwargs side (unmodified, still passing — confirmed no conflict, since that test's job is also unsplittable and never inspects `escalation_records`). Append used a 2-blank-line lead-in matching the file's own established class-separator convention (confirmed by reading the file at the `TestPlannedTaskToTaskEntryAdapter` boundary before appending), not the single blank line literally shown in the round's prompt text — see Deviations. |

## External actions

`git push` → run immediately after this handback commit (C5); outcome
recorded in the completion report, not in this file (write-once rule).

Two mutation red-proof disposable worktrees were created and removed,
both off commit `8d6f06df` (after C4 was committed):

- `git worktree add .remedy-wt/f112-r16-mutation1 HEAD --detach` →
  mutation applied (`answered["answer"] == "split task"` →
  `answered["answer"] != "split task"`) → targeted tests run →
  `git worktree remove .remedy-wt/f112-r16-mutation1 --force`.
- `git worktree add .remedy-wt/f112-r16-mutation2 HEAD --detach` →
  mutation applied (`t.status in (TASK_APPLIED, TASK_SKIPPED,
  TASK_SPLIT)` → `t.status in (TASK_APPLIED, TASK_SKIPPED)`) →
  targeted tests run → `git worktree remove
  .remedy-wt/f112-r16-mutation2 --force`.

`git worktree list` after both removals showed only the primary
checkout and the pre-existing, unrelated `remedy/job-*` worktrees; no
`f112-r16-mutation*` entry remained in either case.

## Verification

**Step 0 TRANSPORT** — `cmp .agent/authored/f112-r16.md
.agent/last_block.md` ran directly this round (not denied) → exit 0,
both files **13591 bytes**. Extracted-slice byte counts, measured
programmatically against the pinned figures in the block: RECORD15
**2347 bytes** (pinned 2347, match), PLAN16 **2165 bytes / 46 content
lines, no trailing newline** (pinned 2165/46, match), DECISION D8
**8435 bytes** (pinned 8435, match). PASS.

**Step 1 LEDGER (RECORD15)** — `.agent/live_review.md` measured
**2275307 bytes** immediately before the append (matches the pinned
pre-append figure exactly). Appended as `content_bytes + b"\n" +
RECORD15_bytes` (ONE newline). Post-size measured at **2277655
bytes**, matching `2275307 + 1 + 2347` exactly (also matching the
block's pinned post-size). Old-file-is-prefix check: **True**.
Tail-equality check (`post[len(old):] == b"\n" + RECORD15_bytes`):
**True**. PASS.

**Step 2 PLAN** — PLAN16 extracted programmatically from the committed
`.agent/authored/f112-r16.md` (between its markers) to an in-memory
byte string, then written as the whole-file replacement and re-read for
confirmation: **equal, 2165 bytes both sides**. `git diff` reviewed in
full before commit; clean whole-file replacement, no unintended
content. PASS.

**Step 3 DECISION (D8)** — `.agent/decisions.md` measured **778216
bytes** immediately before the append (matches the pinned pre-append
figure exactly). Appended as `content_bytes + b"\n" + D8_bytes` (ONE
newline). Post-size measured at **786652 bytes**, matching `778216 + 1
+ 8435` exactly (also matching the block's pinned post-size).
Old-file-is-prefix check: **True**. Tail-equality check: **True**.
PASS.

**Step 4 CODE (C4)** — All five `pingpong_job.py` FROM strings and both
test-file FROM strings (import, fixture anchor) grepped to confirm
exactly one occurrence each before applying via `Edit`; `git diff`
reviewed in full before commit and matched the block's TO text exactly
for every pair, no unrelated changes. The file-end test append verified
via ordered equality (prefix/suffix check, computed programmatically
against the reconstructed pre-C4 state) before commit, matching
byte-for-byte with a 2-blank-line lead-in (see Deviations for why 2, not
the 1 literally shown in the prompt).

Targeted: `python3 -m pytest tests/orchestration/test_job_task_runner.py
-k "TestClassBudgetCannotFitEscalation" -q` → **2 passed, 212
deselected**. Full file: `python3 -m pytest
tests/orchestration/test_job_task_runner.py -q` → **214 passed** (212
existing + 2 new, no regressions). Lint: `python3 -m ruff check
packages/orchestration/pingpong_job.py
tests/orchestration/test_job_task_runner.py` → **"All checks
passed!"**. Canary: `python3 -m pytest tests/cli/test_golden_path.py
-q` → **42 passed**. All exactly as pinned.

**Step 5 BROADER REGRESSION** — `python3 -m pytest tests/orchestration/
-q -n auto` → **12743 passed, 10 skipped, 1 warning, 0 failed** in
77.36s. This differs from the block's pinned prediction (**12742
passed, 10 skipped, 1 unrelated failed** —
`TestVitestFrontendTestFoundation::test_vitest_passes`, predicted to
fail in a fresh worktree lacking `node_modules`). Re-run targeted:
`python3 -m pytest tests/orchestration/test_test_runner.py -k
"TestVitestFrontendTestFoundation" -q` → **4 passed, 48 deselected**
(no failure at all). Root cause confirmed: this is the PRIMARY
checkout, not a fresh disposable worktree, and it already has
`node_modules/` present (`ls -d node_modules` succeeded), so the
frontend vitest suite the reviewer's dry-run worktree could not run
here runs and passes. One MORE test passed than predicted, zero
failures instead of one — a favorable, fully explained divergence, not
a regression. See Deviations.

**Step 6 MUTATION RED-PROOF #1** — in disposable worktree
`.remedy-wt/f112-r16-mutation1` (off commit `8d6f06df`), changed
`answered["answer"] == "split task"` to `answered["answer"] != "split
task"` in `packages/orchestration/pingpong_job.py` (grep-confirmed
exactly one occurrence beforehand). Ran the targeted two-test
selection: `test_a_splittable_task_is_replaced_by_its_children` went
**RED** exactly as predicted — `AssertionError: assert ['T001'] ==
['T001', 'T001a', 'T001b']` on the `task_id` list assertion.
`test_an_unsplittable_task_falls_through_uncapped` stayed **GREEN**
(its own split attempt already returns nothing regardless of this
condition). Result: `1 failed, 1 passed`, matching the block's
prediction exactly. `git status --porcelain` in the primary checkout
read **empty** both before the worktree was created and after it was
removed. PASS.

**Step 7 MUTATION RED-PROOF #2** — in disposable worktree
`.remedy-wt/f112-r16-mutation2` (off commit `8d6f06df`), changed
`t.status in (TASK_APPLIED, TASK_SKIPPED, TASK_SPLIT)` to `t.status in
(TASK_APPLIED, TASK_SKIPPED)` inside `run_job`'s `all_done` check
(grep-confirmed exactly one occurrence beforehand). Ran the same
targeted selection: `test_a_splittable_task_is_replaced_by_its_children`
went **RED** exactly as predicted, specifically on `assert result.status
== JOB_COMPLETED` — `AssertionError: assert 'running' == 'completed'`.
`test_an_unsplittable_task_falls_through_uncapped` stayed **GREEN** (it
never produces a `TASK_SPLIT` task). Result: `1 failed, 1 passed`,
matching the block's prediction exactly. `git status --porcelain` read
**empty** before and after. PASS.

`git status --porcelain` in the primary checkout read **empty**
immediately before this handback's own commit. PASS.

## Authored-text proofs

`.agent/authored/f112-r16.md` (committed at `e3b6d6af`) vs
`.agent/last_block.md` (committed at `f5c934f0`): byte-identical, `cmp`
exit 0, both 13591 bytes (Step 0 transport check above). RECORD15,
PLAN16 and DECISION D8 were all extracted programmatically from this
committed file (never retyped) and applied via the stated append
formula or whole-file write; every application was confirmed against
pinned byte counts and before/after equality checks above (Steps 1-3).
The code change (C4, the five REWRITE pairs in `pingpong_job.py`, the
import/fixture REWRITE pairs, and the file-end test append) was
typed/applied directly from the round's own prompt text (not carried
inside the authored block's markers, unlike the
ledger/plan/decision texts) and verified mechanically (FROM-occurrence
counts, a full `git diff` read before commit, the ordered-equality
prefix/suffix proof for the test append, the targeted/full/lint/canary
test runs, the broader regression run, and both mutation red-proofs)
per Step 4-7 above.

## Deviations & assumptions

1. **Broader regression run (Step 5) produced a MORE favorable result
   than pinned, not a matching one**: 12743 passed / 10 skipped / 0
   failed, against a pinned 12742 passed / 10 skipped / 1 (unrelated)
   failed. Investigated and explained: the reviewer's own dry-run
   happened in a disposable worktree without `node_modules`; this
   round's work happened in the primary checkout, which already has
   `node_modules/` installed, so the previously-predicted-failing
   `TestVitestFrontendTestFoundation::test_vitest_passes` (and its
   sibling tests in that class) ran and passed instead of failing.
   Re-verified directly by re-running that test class in isolation (4
   passed, 0 failed) and by confirming `node_modules/` exists at repo
   root. Not suppressed, not worked around — reported here exactly as
   observed, per the block's own instruction to report any disagreement
   rather than force a match. No other test in the 12743 differed from
   the pinned expectation.
2. **The test-file append's (Part C) blank-line lead-in was 2 blank
   lines, not the 1 literally present in the prompt's own code fence.**
   The prompt's parenthetical explicitly stated the appended text
   "already begins with two blank lines to match the file's existing
   2-blank-line class separator convention," but the fenced block as
   delivered contained only one leading blank line before `class
   TestClassBudgetCannotFitEscalation:`. Since Part C carries no pinned
   byte count (unlike Parts C1-C3, which do), and the file's own
   established convention was independently confirmed by reading the
   `TestPlannedTaskToTaskEntryAdapter` boundary (`...is None\n\n\nclass
   Test...`, i.e. two blank lines) immediately before appending, this
   round applied 2 blank lines to match the stated intent and the file's
   real convention, rather than reproducing the fence's literal 1. This
   changes nothing semantically (Python is blank-line-insensitive); the
   ordered-equality proof (Step 4) was re-derived against this actual
   choice, not against the literal fence text, and passed.
3. **This round has six real commits (C0a, C0b, C1, C2, C3, C4) plus
   this handback as C5** — matching the block's own instructed sequence
   exactly. Stated here per item 30's "an extra commit, a dropped one,
   or a reordering is a deviation even when correct" instruction — this
   is the block's own instructed shape, not a departure from it.
4. **No search of the open-findings ledger (`.agent/live_review.md`'s
   open R-ids) was performed this round.** No new R-XXXX finding was
   minted or claimed resolved this round — the round is a
   DECISION-authorized implementation slice (T003b2b2b2), not a defect
   record. Item 30's "grep the DEFECT before minting an id" checklist
   obligation therefore does not apply this round.
5. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| RECORD15 booked | done | |
| PLAN16 applied | done | |
| DECISION D8 registered | done | |
| T003b2b2b2 shipped | done | |

## Next

**Acceptance fixtures per T3_F112.md's own Acceptance section, then the
integration gate** (full suite, twice per feature per
`docs/agents/integration_gate.md`), then closure — per PLAN16's Next
Steps. T003b2b2b is now fully complete across T003b2b2b1 (round 15) and
T003b2b2b2 (this round); T3_F112.md's own T003 description is now true
at the dispatch-loop level.

**RECORD16 (this round's own verdict) is NOT YET in the ledger** —
round 16 has not been independently re-reviewed by the reviewer yet, so
no verdict exists to book. Per amend0827-process-diet rule 1, it books
in the FIRST COMMIT of the next round that is happening anyway — that
is round 17's own C1. Before starting the next round: Phase 1 rule 1 —
re-check `.agent/STOP` from disk (absent as of this round).
