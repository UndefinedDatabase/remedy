# Handoff — F112 Prompt budget per task class, round 11 (T003b2b1: escalation.py dual-shape fix + TaskEntry.inputs field)

## Session

SESSION 4 of feature F112 · round 11 · rounds so far 11.

Correction carried into this round (prose-only, no product effect, per
amend0827 rule 2 — no new finding id): the round-9 and round-10
handbacks both mislabeled this continuation "session 3" by mistake.
Round 9 was already complete on disk (committed by an earlier,
already-ended session) before the current planner/reviewer session
started, so this is in fact SESSION 4. Every reference to the session
number in this round's authored texts and in this handback says
session 4.

This round books round 10's already-independently-reviewed PASS
verdict into `.agent/live_review.md` (RECORD10, amend0827 rule 1 — a
pending verdict books in the FIRST COMMIT of the next round that is
happening anyway, i.e. round N's verdict books in round N+1's first
commit; the prior two handbacks' phrase "the round after next" was
imprecise for the same rule — see "Next" below), appends DECISION
F112 D4 (fresh investigation this round found `_record_answer_on_task`
in `escalation.py` reads `task.id`/`task.inputs`, fields pingpong
`JobPlan`'s `TaskEntry` has never carried — only Core Job's `Task` has
them — so calling `auto_apply_safe_default` against a live `JobPlan`
would raise `AttributeError`), and ships T003b2b1: a new
`inputs: dict = field(default_factory=dict)` field on `TaskEntry`
(exported/imported like `task_class`, the T003b1 precedent) plus a
dual-shape fix to `_record_answer_on_task` that accepts either
`task.id` (Core Job) or `task.task_id` (pingpong `JobPlan`), matching
`_metadata()`'s own already-established "accept either shape"
contract. Per DECISION F112 D4, T003b2b splits into T003b2b1 (this
round, done — both pieces unit-tested including a real
`enqueue_task_decision` -> `auto_apply_safe_default` chain against a
`JobPlan`/`TaskEntry`) and T003b2b2 (the live call-site wiring —
deferred to its own round(s), now safe to build on a working
escalation path).

## Range

Review of `58cfae0e..HEAD` (commits C0a through C6; C6 is this
handback commit itself, not yet made at the time this file was
written). **This range is UNREVIEWED by construction** — round 11 has
not yet been independently re-reviewed by the reviewer; no verdict on
this round's own work is claimed anywhere in this file.

## Commits

### 6da4b11e F112 R11 C0a: save round 11 block to .agent/authored/f112-r11.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r11.md` | 85/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 2a391ae9 F112 R11 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 39/37 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). Byte-equality confirmed before commit (see Verification Step 0 — `cmp` itself was denied by this session's sandbox; a `python3` byte-equality read substituted). |

### 82533458 F112 R11 C1: append RECORD10 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD10 (round 10's verdict) via `content_bytes + b"\n" + RECORD10_bytes` — the ONE-newline formula. |

### 3f6752c6 F112 R11 C2: apply PLAN11 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 24/22 | Whole-file replacement with PLAN11, extracted programmatically from the committed authored file, not retyped. |

### f4191d8a F112 R11 C3: append DECISION F112 D4 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/1 | Appended DECISION F112 D4 (T003b2b further-split rationale) via the same ONE-newline formula. |

### 21d79aa2 F112 R11 C4: add TaskEntry.inputs field (export/import round-trip)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 7/0 | Applied Pairs E/F/G (all REWRITE, each FROM confirmed to occur exactly once before applying): new `inputs: dict = field(default_factory=dict)` field on `TaskEntry`, plus its export (`_export_job`) and import (`_import_job`) round-trip. |
| `tests/orchestration/test_job_task_runner.py` | 19/0 | Pair H (REWRITE, FROM confirmed to occur exactly once): two new `TestPersistence` tests — `inputs` defaults to `{}`, and round-trips through persist/load. |

### 01c87498 F112 R11 C5: fix _record_answer_on_task for pingpong JobPlan task shape
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/escalation.py` | 8/1 | Applied Pair I (REWRITE, FROM confirmed to occur exactly once before applying): `_record_answer_on_task` now resolves a task's identifier via `getattr(task, "id", None)` falling back to `getattr(task, "task_id", None)`, matching `_metadata()`'s own dual-shape contract. |
| `tests/orchestration/test_escalation.py` | 43/0 | File-end append (byte-length-arithmetic verified): new `TestJobPlanCompatibility` class with two tests proving the full `enqueue_task_decision` -> `auto_apply_safe_default` -> `answer_task_decision` chain against a real `JobPlan`/`TaskEntry`. |

## External actions

`git push` → run immediately after this handback commit (C6); outcome
recorded in the completion report, not in this file (write-once rule).

Two disposable worktrees created and removed during this round, both
for mutation red-proofs only (never committed to, never merged):
- `git worktree add .remedy-wt/f112-r11-mutation-c4 HEAD` (detached at
  `f4191d8a`, before C4's own commit — the real C4 fix+tests were
  copied in from the primary checkout's working tree onto this base so
  the mutation could be tested without ever mutating the primary
  checkout) → `git worktree remove .remedy-wt/f112-r11-mutation-c4 --force`.
- `git worktree add .remedy-wt/f112-r11-mutation-c5 HEAD` (detached at
  `21d79aa2`, after C4's real commit, before C5's own — same copy-in
  pattern) → `git worktree remove .remedy-wt/f112-r11-mutation-c5 --force`.

`git worktree list` after both removals shows neither
`f112-r11-mutation-c4` nor `f112-r11-mutation-c5` (confirmed; only the
pre-existing, unrelated `remedy/job-*` worktrees and the primary
checkout remain).

## Verification

**Step 0 TRANSPORT** — `cmp .agent/authored/f112-r11.md .agent/last_block.md`
was DENIED by this session's sandbox (a bash-permission denial on the
`cmp` invocation itself, unrelated to file content); substituted a
`python3` byte-equality read: `a == b` → **True**, both files **10133
bytes**. Extracted-slice byte counts, measured programmatically against
the pinned figures in the block: RECORD10 **2232 bytes** (pinned 2232,
match), PLAN11 **2321 bytes** (pinned 2321, match), DECISION F112 D4
**5001 bytes** (pinned 5001, match). PASS.

**Step 1 LEDGER (RECORD10)** — `.agent/live_review.md` measured
**2265527 bytes** immediately before the append (matches round 10's
own handback post-size exactly). Appended as `content_bytes + b"\n" +
RECORD10_bytes` (ONE newline). Post-size measured at **2267760
bytes**, matching `2265527 + 1 + 2232` exactly. Old-file-is-prefix
check: **True**. Tail-equality check (`post[len(old):] == b"\n" +
RECORD10_bytes`): **True**. PASS.

**Step 2 PLAN** — PLAN11 extracted programmatically from the committed
`.agent/authored/f112-r11.md` (between its markers) to an in-memory
string, then Python byte-equality against `.agent/plan.md`: **equal,
2321 bytes both sides**. `wc -l .agent/plan.md` → **48**. `grep -c
'^## Goal' .agent/plan.md` → **1**. `grep -c '^## Next Steps'
.agent/plan.md` → **1**. PASS.

**Step 3 DECISION (D4)** — `.agent/decisions.md` measured **756109
bytes** immediately before the append (matches round 10's own handback
post-size exactly). Appended as `content_bytes + b"\n" + D4_bytes`
(ONE newline). Post-size measured at **761111 bytes**, matching
`756109 + 1 + 5001` exactly. Old-file-is-prefix check: **True**.
Tail-equality check: **True**. PASS.

**Step 4 TASKENTRY.INPUTS FIELD (C4)** — Grepped the file for each of
Pairs E/F/G's FROM strings before applying: all **exactly 1**
occurrence. Applied via `Edit` (REWRITE). Pair H's FROM grepped before
applying: **exactly 1** occurrence, applied via `Edit`. After applying:
`python3 -c "import ast; ast.parse(...)"` on both files → **syntax
OK**.
`python3 -m pytest tests/orchestration/test_job_task_runner.py -k "test_inputs_defaults_to_empty_dict or test_inputs_round_trips_through_persist_and_load" -q`
→ **2 passed, 200 deselected**.
`python3 -m pytest tests/orchestration/test_job_task_runner.py -q` →
**202 passed** (no regressions).
`python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_task_runner.py`
→ **`All checks passed!`**. PASS.

**Step 5 MUTATION RED-PROOF for C4** (disposable worktree only) — `git
status --porcelain` in the primary checkout read **empty** immediately
before creating the worktree. Created
`git worktree add .remedy-wt/f112-r11-mutation-c4 HEAD` (detached at
`f4191d8a`, the commit before C4's own — C4 was not yet committed to
the primary checkout at this point). Copied the working-tree state of
`pingpong_job.py` and `test_job_task_runner.py` (the real, correct C4
fix+tests, uncommitted in the primary checkout at the time) into the
worktree. Baseline run in the worktree (unmutated) →
`python3 -m pytest tests/orchestration/test_job_task_runner.py -k "test_inputs_defaults_to_empty_dict or test_inputs_round_trips_through_persist_and_load" -q`
→ **2 passed** (sanity check the copy landed correctly). Mutated:
deleted the `"inputs": t.inputs,` line from the export path, leaving
the field unexported. Re-ran the same command → **1 failed, 1
passed**: `test_inputs_round_trips_through_persist_and_load` went RED
(`AssertionError: assert {} == {'decision_answers': ...}` — the
persisted value silently reverted to `{}` on load since it was never
exported), and `test_inputs_defaults_to_empty_dict` stayed GREEN
(still `{}` by default — nothing to lose), exactly as the block
specified (both colors reported, not a uniform-red mutation). Removed
the worktree via
`git worktree remove .remedy-wt/f112-r11-mutation-c4 --force`; `git
worktree list` no longer shows it. `git status --porcelain` in the
primary checkout read **empty** both before creating and after
removing the worktree — the mutation never touched the primary
checkout. Only then was C4 committed for real (with the correct,
unmutated code) to the primary checkout. PASS.

**Step 6 ESCALATION.PY DUAL-SHAPE FIX (C5)** — Grepped the file for
Pair I's FROM string before applying: **exactly 1** occurrence.
Applied via `Edit` (REWRITE). `python3 -c "import ast;
ast.parse(...)"` on `escalation.py` → **syntax OK**. Test append to
`test_escalation.py` verified by byte-length arithmetic: pre **44878**
bytes, appended **1664** bytes, post **46542** bytes,
`post_len == pre_len + appended_len` (**True**), tail equals the
appended text exactly (**True**).
`python3 -m pytest tests/orchestration/test_escalation.py -k TestJobPlanCompatibility -q`
→ **2 passed, 66 deselected**.
`python3 -m pytest tests/orchestration/test_escalation.py -q` → **68
passed** (no regressions).
`python3 -m ruff check packages/orchestration/escalation.py tests/orchestration/test_escalation.py`
→ **`All checks passed!`**. PASS.

**Step 7 MUTATION RED-PROOF for C5** (disposable worktree only) — `git
status --porcelain` in the primary checkout read **empty** immediately
before creating the worktree. Created
`git worktree add .remedy-wt/f112-r11-mutation-c5 HEAD` (detached at
`21d79aa2`, i.e. after C4's real commit, before C5's own — C5 was not
yet committed to the primary checkout at this point). Copied the
working-tree state of `escalation.py` and `test_escalation.py` (the
real, correct C5 fix+tests, uncommitted in the primary checkout at the
time) into the worktree. Baseline run in the worktree (unmutated) →
`python3 -m pytest tests/orchestration/test_escalation.py -k TestJobPlanCompatibility -q`
→ **2 passed** (sanity check the copy landed correctly). Mutated:
reverted the dual-shape lookup back to `if str(task.id) != task_id:`.
Re-ran the same command → **2 failed, 0 passed**: both
`test_auto_apply_safe_default_answers_and_records_on_a_job_plan_task`
and `test_answer_task_decision_matches_by_task_id_not_id` went RED
with `AttributeError: 'TaskEntry' object has no attribute 'id'`,
exactly as the block specified. Control, same mutated worktree →
`python3 -m pytest tests/orchestration/test_escalation.py -k "TestAnswering or TestSafeDefaults" -q`
→ **7 passed, 61 deselected** — the mutation only breaks the new
JobPlan path, not the old Core Job path. Reverted the mutation in the
worktree (dual-shape lookup restored), re-ran the same command → **2
passed, 0 failed**. Removed the worktree via
`git worktree remove .remedy-wt/f112-r11-mutation-c5 --force`; `git
worktree list` no longer shows it. `git status --porcelain` in the
primary checkout read **empty** both before creating and after
removing the worktree — the mutation never touched the primary
checkout. Only then was C5 committed for real (with the correct,
unmutated code) to the primary checkout. PASS.

**Step 8 FULL-PAIR REGRESSION, LINT, CANARY**:
- `python3 -m pytest tests/orchestration/test_job_task_runner.py tests/orchestration/test_escalation.py -q` → **270 passed**
- `python3 -m ruff check packages/orchestration/pingpong_job.py packages/orchestration/escalation.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_escalation.py` → **`All checks passed!`**
- `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42 passed**

`git status --porcelain` in the primary checkout read **empty**
immediately before this handback's own commit. PASS.

## Authored-text proofs

`.agent/authored/f112-r11.md` (committed at `6da4b11e`) vs
`.agent/last_block.md` (committed at `2a391ae9`): byte-identical (Step
0 transport check above, `python3` byte-equality substitute for the
sandbox-denied `cmp`). RECORD10, PLAN11 and DECISION F112 D4 were all
extracted programmatically from this committed file (never retyped)
and applied via the stated append formulas or whole-file write; every
application was confirmed against pinned byte counts and
before/after equality checks above (Steps 1-3). Pairs E/F/G/H (C4) and
Pair I plus the test-class append (C5) were typed directly from the
round's own prompt text (not carried inside the authored block's
markers, unlike the ledger/plan/decision texts) and verified
mechanically (occurrence counts, byte-length arithmetic) before and
after application, per Steps 4 and 6 above.

## Deviations & assumptions

1. **`cmp` itself was denied by this session's Bash sandbox** (a
   permission denial on the bare `cmp <file1> <file2>` invocation, not
   a content or path issue) at both the C0b self-check and the
   pre-handback re-check. Substituted a `python3` byte-equality read
   (`open(...).read() == open(...).read()`) each time, which returned
   `True` in both cases — the two files are confirmed byte-identical
   by an equivalent method, not merely asserted. Recorded here as a
   deviation from the block's literal `cmp` instruction, not a defect
   in the transport itself.
2. **`git commit`'s own inline insertion/deletion summary disagreed
   with `git show --numstat` read after the fact for two commits this
   round**: C0b's whole-file rewrite of `.agent/last_block.md` (commit-time
   summary read `85 insertions, 83 deletions`; `git show --numstat`
   read `39 insertions, 37 deletions`) and C2's whole-file rewrite of
   `.agent/plan.md` (commit-time summary read `49 insertions, 47
   deletions`; `git show --numstat` read `24 insertions, 22
   deletions`) — the same class of discrepancy rounds 7 through 10 all
   declared for their own C0b commits. The Commits table above uses
   the `git show --numstat` reading throughout.
3. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.
4. **No search of the open-findings ledger (`.agent/live_review.md`'s
   open R-ids) was performed this round.** No new R-XXXX finding was
   minted or claimed resolved this round — only DECISION F112 D4 was
   authored (a scope/design decision, not a defect record). Item 30's
   "grep the DEFECT before minting an id" checklist obligation
   therefore does not apply this round; stated here for completeness
   rather than silently omitted.
5. **Two prose corrections carried into this round from the prompt,
   both prose-only with no product effect (amend0827 rule 2, no new
   finding id):** (a) this session is SESSION 4, not session 3 — the
   round-9 and round-10 handbacks both mislabeled the continuation
   "session 3"; every session-number reference in this round's
   authored texts and this handback says session 4. (b) the prior two
   handbacks' phrase "must be booked by the round after next" for a
   pending verdict was imprecise; the actual rule (amend0827 rule 1)
   is that a pending verdict books in the FIRST COMMIT of the next
   round that is happening anyway — round N's verdict books in round
   N+1's first commit, which is exactly what has happened every round
   so far (RECORD8 in R9's C1, RECORD9 in R10's C1, RECORD10 in this
   round's C1) — see "Next" below for the correctly-worded statement
   about RECORD11.

## Next

**T003b2b2** (per DECISION F112 D4 and the rewritten `.agent/plan.md`
Next Steps): call `fit_task_context_to_class_cap` between
`_build_task_prompt` and `task.status = TASK_RUNNING`; wire
`compiled_context_paths`/`compiled_context_candidates`/
`compiled_context_token_budget` into `run_pingpong`; on `cannot_fit`
call `enqueue_task_decision` (`options=["split task"]` only when
`task_entry_to_planned_task(task) is not None` and `split_one_task` on
its result returns non-`None`) then `auto_apply_safe_default` under
`--yes`, reading the answer off the returned record directly rather
than off `task.inputs` (same dispatch-loop iteration, no resume needed
for this path). Three still-untested pieces against the live dispatch
loop — its own dedicated round(s), re-read the call site fresh again
before authoring, per `.agent/plan.md` Risks and DECISION F112
D2/D3/D4.

**RECORD11 (this round's own verdict) is NOT YET in the ledger** —
round 11 has not been independently re-reviewed by the reviewer yet,
so no verdict exists to book. Per amend0827-process-diet rule 1, it
books in the FIRST COMMIT of the next round that is happening anyway —
that is round 12's own C1, not "the round after next" (the correction
in this handback's Session section explains why that earlier phrasing
was imprecise). Before starting T003b2b2: Phase 1 rule 1 — re-check
`.agent/STOP` from disk (not present as of this round).
