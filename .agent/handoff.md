# Handoff — F112 Prompt budget per task class, round 15 (T003b2b2b1: planned_task_to_task_entry, the reverse of task_entry_to_planned_task)

## Session

SESSION 5 of feature F112 · round 15 · rounds so far 15.

Note: `.agent/handoff.md` inherited from round 14 said "SESSION 4" — a
labeling bug the reviewer found in its own prior block (this round's
prose_slips entry, appended in C4). This is a fresh `/build-remedy-self`
bootstrap, not a continuation of the session that produced rounds 1-14,
so the session number increments: **this is SESSION 5**, not a
continuation of session 4.

This round books round 14's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD14, amend0827 rule 1 — a pending
verdict books in the FIRST COMMIT of the next round that is happening
anyway), registers DECISION F112 D7 (the T003b2b2b → T003b2b2b1/T003b2b2b2
split, following fresh investigation that found five separate unknowns
D6 did not have visibility into), then ships **T003b2b2b1** exactly as
D7's CHOSEN clause specified: `planned_task_to_task_entry`, the reverse
of the already-shipped `task_entry_to_planned_task` — turns one
`split_one_task` child `PlannedTask` back into a dispatchable
`TaskEntry`. Not called from `run_job` this round — a prerequisite
building block only, same "unwired" shape T003c used before T003b2b2a
consumed it.

This round ships production code: two files touched
(`packages/orchestration/pingpong_job.py`,
`tests/orchestration/test_job_task_runner.py`), 102 insertions total —
well under the 500-line cap. DECISION F112 D7 was pre-authored and
registered this round (C3), settling the T003b2b2b scope split the
reviewer's fresh investigation found before delegating.

## Range

Review of `0fba8b0c..70aef315` (commits C0a, C0b, C1, C2, C3, C4, C5,
plus this handback commit C6 itself — seven commits total this round).
**This range is UNREVIEWED by construction** — round 15 has not yet
been independently re-reviewed by the reviewer; no verdict on this
round's own work is claimed anywhere in this file.

## Commits

### 9fda0025 F112 R15 C0a: save round 15 block to .agent/authored/f112-r15.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r15.md` | 89/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). Byte counts of every sub-block re-verified programmatically before commit: RECORD14 2386 bytes, PLAN15 2229 bytes/47 lines/no trailing newline, DECISION D7 5766 bytes, PROSE_SLIP 763 bytes — all matched the block's own pinned figures exactly. |

### c7decc60 F112 R15 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 44/40 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). Verified with `cmp` directly (not denied this round) — exit 0, both files 11987 bytes. |

### cbed7d14 F112 R15 C1: append RECORD14 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD14 (round 14's verdict) via `content_bytes + b"\n" + RECORD14_bytes` — the ONE-newline formula, extracted programmatically from the committed authored file. |

### 5e430b1f F112 R15 C2: apply PLAN15 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 47/49 | Whole-file replacement with PLAN15, extracted programmatically from the committed authored file, not retyped. No trailing newline (per the block). |

### bbf2e2ac F112 R15 C3: append DECISION F112 D7 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/1 | Appended DECISION F112 D7 via `content_bytes + b"\n" + D7_bytes` — the ONE-newline formula. Records the T003b2b2b → T003b2b2b1/T003b2b2b2 split and the five MEASURED unknowns (list-mutation safety, id-collision defense, missing TASK_* status, unbuilt escalation call, loop skip-condition) driving it. |

### 0b271970 F112 R15 C4: append the session-number prose slip to prose_slips.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | 1/0 | Appended the SESSION-4-vs-SESSION-5 labeling slip found in round 14's own block, per the file's append-only one-line-per-entry convention (no blank-line separator, file already ended in its own trailing newline). No R-id spent (amend0827-process-diet rule 2 — reviewer-prose inaccuracy, nothing wrong on disk). |

### 70aef315 F112 R15 C5: add planned_task_to_task_entry, the reverse adapter for split_one_task children (T003b2b2b1)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 26/0 | One REWRITE pair (grep-confirmed exactly one occurrence before applying): inserts `planned_task_to_task_entry` immediately after `task_entry_to_planned_task`, before the `TargetGuard` dataclass. Takes a `PlannedTask`, `task_class` (default `TASK_CLASS_DEFAULT`) and `source_heading_number` (default 0, both keyword-only since `PlannedTask` does not carry either field), returns a `TaskEntry` with `status=TASK_PENDING`. `PlannedTask` used only as a type annotation (already available via the existing `TYPE_CHECKING` import plus `from __future__ import annotations`); no runtime import needed since the function body never constructs one. Not called from `run_job` this round. |
| `tests/orchestration/test_job_task_runner.py` | 76/0 | Part A: one-line REWRITE adding `planned_task_to_task_entry,` to the import list (grep-confirmed exactly one occurrence of the FROM pair before applying). Part B: byte-exact file-end append (verified via ordered-equality — pre-edit blob is an exact PREFIX of the post-edit file, appended bytes are an exact SUFFIX) of `TestPlannedTaskToTaskEntryAdapter`, three tests: basic field mapping, `task_class` defaulting to `TASK_CLASS_DEFAULT`, and a full round trip through `task_entry_to_planned_task` → `split_one_task` → `planned_task_to_task_entry` confirming ids (`T005a/b/c`) and `task_class`/`status` propagate correctly to every child. Append reproduced the file's own 2-blank-line class-separator convention exactly (`...is None\n\n\nclass Test...`, confirmed byte-for-byte before commit). |

## External actions

`git push` → run immediately after this handback commit (C6); outcome
recorded in the completion report, not in this file (write-once rule).

Mutation red-proof disposable worktree `.remedy-wt/f112-r15-mutation`
was created (`git worktree add .remedy-wt/f112-r15-mutation HEAD
--detach`, off commit `70aef315`, after C5 was committed), the mutation
(`task_class=task_class,` → `task_class=TASK_CLASS_DEFAULT,` inside
`planned_task_to_task_entry`) applied there only (never in the primary
checkout), the targeted tests run, and the worktree removed (`git
worktree remove .remedy-wt/f112-r15-mutation --force`) before this
handback (C6) was written. `git worktree list` after removal showed
only the primary checkout and the pre-existing, unrelated `remedy/job-*`
worktrees; no `f112-r15-mutation` entry remained.

## Verification

**Step 0 TRANSPORT** — `cmp .agent/authored/f112-r15.md
.agent/last_block.md` ran directly this round (not denied) → exit 0,
both files **11987 bytes**. Extracted-slice byte counts, measured
programmatically against the pinned figures in the block: RECORD14
**2386 bytes** (pinned 2386, match), PLAN15 **2229 bytes / 47 content
lines, no trailing newline** (pinned 2229/47, match), DECISION D7
**5766 bytes** (pinned 5766, match), PROSE_SLIP **763 bytes** (pinned
763, match). PASS.

**Step 1 LEDGER (RECORD14)** — `.agent/live_review.md` measured
**2272920 bytes** immediately before the append (matches the pinned
pre-append figure exactly). Appended as `content_bytes + b"\n" +
RECORD14_bytes` (ONE newline). Post-size measured at **2275307
bytes**, matching `2272920 + 1 + 2386` exactly (also matching the
block's pinned post-size). Old-file-is-prefix check: **True**.
Tail-equality check (`post[len(old):] == b"\n" + RECORD14_bytes`):
**True**. PASS.

**Step 2 PLAN** — PLAN15 extracted programmatically from the committed
`.agent/authored/f112-r15.md` (between its markers) to an in-memory
byte string, then written as the whole-file replacement and re-read for
confirmation: **equal, 2229 bytes both sides**. `git diff` reviewed in
full before commit; clean whole-file replacement, no unintended
content. PASS.

**Step 3 DECISION (D7)** — `.agent/decisions.md` measured **772449
bytes** immediately before the append (matches the pinned pre-append
figure exactly). Appended as `content_bytes + b"\n" + D7_bytes` (ONE
newline). Post-size measured at **778216 bytes**, matching `772449 + 1
+ 5766` exactly (also matching the block's pinned post-size).
Old-file-is-prefix check: **True**. Tail-equality check: **True**.
PASS.

**Step 3b PROSE_SLIP** — `.agent/prose_slips.md` measured **68405
bytes** immediately before the append (matches the pinned pre-append
figure exactly, file confirmed ending in its own trailing newline
first). Appended as `SLIP_bytes + b"\n"` directly (no blank-line
separator). Post-size measured at **69169 bytes**, matching `68405 +
763 + 1` exactly. Old-file-is-prefix check: **True**. Tail-equality
check: **True**. PASS.

**Step 4 CODE (C5)** — Both FROM strings (the `pingpong_job.py`
REWRITE, and the test file's import REWRITE) grepped to confirm exactly
one occurrence each before applying via `Edit`; `git diff` reviewed in
full before commit and matched the block's TO text exactly, no
unrelated changes. The file-end test append verified via ordered
equality (prefix/suffix check) before commit, matching byte-for-byte.

Targeted: `python3 -m pytest tests/orchestration/test_job_task_runner.py
-k "TestPlannedTaskToTaskEntryAdapter" -q` → **3 passed, 209
deselected**. Full file: `python3 -m pytest
tests/orchestration/test_job_task_runner.py -q` → **212 passed** (209
existing + 3 new, no regressions). Lint: `python3 -m ruff check
packages/orchestration/pingpong_job.py
tests/orchestration/test_job_task_runner.py` → **"All checks
passed!"**. Canary: `python3 -m pytest tests/cli/test_golden_path.py
-q` → **42 passed**. PASS, all as pinned — no deviation from any
expected result this round.

**Step 5 MUTATION RED-PROOF** — in the disposable worktree
`.remedy-wt/f112-r15-mutation` (off commit `70aef315`), changed
`task_class=task_class,` to `task_class=TASK_CLASS_DEFAULT,` inside
`planned_task_to_task_entry` in `packages/orchestration/pingpong_job.py`
(grep-confirmed exactly one occurrence beforehand). No `__pycache__`
directories existed in the fresh worktree (confirmed via `find` before
running), so no cache purge was needed; ran with `python3 -B`
regardless, per the standing cache-purge convention. Ran the targeted
three-test selection from Step 4 there:
`test_basic_field_mapping` and
`test_round_trips_through_split_one_task_with_ids_and_class_preserved`
went **RED** exactly as predicted —
`AssertionError: assert 'standard_build' == 'format'` — because forcing
`task_class` to the default regardless of the caller's argument breaks
both tests' `assert entry.task_class == "format"` (and, in the
round-trip test, `assert e.task_class == "format"` for all three split
children). `test_task_class_defaults_to_standard_build` stayed
**GREEN** (it never passes a non-default `task_class`, so the mutation
changes nothing it asserts). Result: `2 failed, 1 passed`, matching the
block's prediction exactly. `git status --porcelain` in the primary
checkout read **empty** both before the worktree was created and after
it was removed. PASS.

`git status --porcelain` in the primary checkout read **empty**
immediately before this handback's own commit. PASS.

## Authored-text proofs

`.agent/authored/f112-r15.md` (committed at `9fda0025`) vs
`.agent/last_block.md` (committed at `c7decc60`): byte-identical, `cmp`
exit 0, both 11987 bytes (Step 0 transport check above). RECORD14,
PLAN15, DECISION D7 and PROSE_SLIP were all extracted programmatically
from this committed file (never retyped) and applied via the stated
append formula or whole-file write; every application was confirmed
against pinned byte counts and before/after equality checks above
(Steps 1-3b). The code change (C5, the one REWRITE pair in
`pingpong_job.py`, the import REWRITE, and the file-end test append)
was typed/applied directly from the round's own prompt text (not
carried inside the authored block's markers, unlike the
ledger/plan/decision/prose-slip texts) and verified mechanically
(FROM-occurrence counts, a full `git diff` read before commit, the
ordered-equality prefix/suffix proof for the test append, the
targeted/full/lint/canary test runs, and the mutation red-proof) per
Step 4-5 above.

## Deviations & assumptions

**None.** Every verification command in Part 3 of the block ran with
the sandbox permission it needed this round (`cmp`, `find`, `python3 -m
pytest`, `python3 -m ruff check`, `git worktree add/remove`) and
produced exactly the pinned expected result — no substitution, no
disagreement, no repair needed. This round differs from rounds 11-14 in
that respect: `cmp` was denied in some earlier rounds and is not this
round.

1. **This round has seven real commits (C0a, C0b, C1, C2, C3, C4, C5)
   plus this handback as C6** — matching the block's own instructed
   sequence exactly, including the DECISION commit C3. Stated here per
   item 30's "an extra commit, a dropped one, or a reordering is a
   deviation even when correct" instruction — this is the block's own
   instructed shape, not a departure from it.
2. **No search of the open-findings ledger (`.agent/live_review.md`'s
   open R-ids) was performed this round.** No new R-XXXX finding was
   minted or claimed resolved this round — the round is a
   DECISION-authorized implementation slice (T003b2b2b1), not a defect
   record. Item 30's "grep the DEFECT before minting an id" checklist
   obligation therefore does not apply this round; stated here for
   completeness rather than silently omitted.
3. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| RECORD14 booked | done | |
| PLAN15 applied | done | |
| DECISION D7 registered | done | |
| prose slip appended | done | |
| T003b2b2b1 shipped | done | |

## Next

**T003b2b2b2** (per PLAN15's Next Steps, per DECISION F112 D7): the
actual dispatch-loop wiring — a new `TASK_*` status for "replaced by a
split", the `enqueue_task_decision`/`auto_apply_safe_default` calls,
`used_ids` collection from the live `job.tasks` list, safe post-`idx`
insertion, and the loop's own skip condition for the new status.
**Mandatory prerequisite reading before authoring — do NOT assume this
round's investigation (D7's own MEASURED section) is still current by
then; re-read `run_job`'s dispatch loop fresh** (D7's own standing
instruction, the same discipline D2-D6 established and D7 itself just
exercised).

**RECORD15 (this round's own verdict) is NOT YET in the ledger** —
round 15 has not been independently re-reviewed by the reviewer yet, so
no verdict exists to book. Per amend0827-process-diet rule 1, it books
in the FIRST COMMIT of the next round that is happening anyway — that
is round 16's own C1. Before starting T003b2b2b2: Phase 1 rule 1 —
re-check `.agent/STOP` from disk (absent as of this round).
