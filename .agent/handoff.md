# Handoff — F112 Prompt budget per task class, round 17 (DECISION F112 D9: enqueue_task_decision carries tier1/cap/class arithmetic)

## Session

SESSION 5 of feature F112 · round 17 · rounds so far 17.

This is a small round, not a new feature slice: it closes an
Acceptance gap the round 16 code (T003b2b2b2) left open. The round 16
verdict (RECORD16, VERDICT PASS) is booked into `.agent/live_review.md`
in this round's first commit (C1), per amend0827 rule 1. RECORD16's own
closing paragraph is what routed this round: a fresh re-read of
T3_F112.md's Acceptance section found that round 16's
`enqueue_task_decision` call passed no `impact=` argument at all, so
Acceptance's "decision with correct arithmetic" clause was not yet met.
DECISION F112 D9 (registered this round, C3) settles the fix:
`enqueue_task_decision`'s existing `impact: str = ""` parameter now
carries `tier1_tokens`/`cap_tokens`/`task_class`, all three already
computed in `fit_result` at the call site — no new computation. D9 also
records, explicitly, that the Design section's other two decision
options ("raise cap for this job", "proceed-overcap once", both marked
"audited") stay unbuilt, because no audited/attended-mode approval
machinery exists anywhere in this codebase to hook them into — a
named, Acceptance-permitted narrowing, not a silent drop.

Production code touched: one file (`packages/orchestration/pingpong_job.py`,
5 insertions — the `impact=` argument), plus one test file
(`tests/orchestration/test_job_task_runner.py`, 3 insertions — three new
assertions inside the already-existing
`test_a_splittable_task_is_replaced_by_its_children`, no new test). Well
under the 500-line cap.

## Range

Review of `b41b2ea7..15afe6d5` (commits C0a, C0b, C1, C2, C3, C4, plus
this handback commit C5 itself — six real commits total this round, C5
not yet made at the time of writing this section header, made
immediately after). **This range is UNREVIEWED by construction** —
round 17 has not yet been independently re-reviewed by the reviewer; no
verdict on this round's own work is claimed anywhere in this file.

## Commits

### a0415ff0 F112 R17 C0a: save round 17 block to .agent/authored/f112-r17.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r17.md` | 83/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). Byte counts of every sub-block re-verified programmatically before commit: RECORD16 3244 bytes, PLAN17 2150 bytes/47 content lines/no trailing newline, DECISION D9 5479 bytes — all matched the block's own pinned figures exactly. |

### ddb40700 F112 R17 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 35/34 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). Verified with `cmp` directly (not denied this round) — exit 0, both files 11517 bytes. |

### df7753cc F112 R17 C1: append RECORD16 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD16 (round 16's verdict, VERDICT PASS) via `content_bytes + b"\n" + RECORD16_bytes` — the ONE-newline formula, extracted programmatically from the committed authored file. |

### 86772afa F112 R17 C2: apply PLAN17 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 20/19 | Whole-file replacement with PLAN17, extracted programmatically from the committed authored file, not retyped. No trailing newline (per the block). |

### c99e7d78 F112 R17 C3: append DECISION F112 D9 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/1 | Appended DECISION F112 D9 via `content_bytes + b"\n" + D9_bytes` — the ONE-newline formula. Records the `impact=` fix, sourced from the already-computed `fit_result`, and the explicit named narrowing on the other two Design-section options. |

### 15afe6d5 F112 R17 C4: enqueue_task_decision carries tier1/cap/class arithmetic (DECISION F112 D9)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 5/0 | One REWRITE pair (grep-confirmed exactly one occurrence before applying): the `enqueue_task_decision` call in the `else` branch of the `fit_result.fits` check gains `impact=f"tier1_tokens={fit_result.tier1_tokens} cap_tokens={fit_result.cap_tokens} task_class={fit_result.task_class}"`. Confirmed `fit_result` is in scope at the call site (computed at line 2434, call site at 2444-2459) before applying. Confirmed `enqueue_task_decision`'s signature (`escalation.py:211-219`) already carries `impact: str = ""` unchanged. |
| `tests/orchestration/test_job_task_runner.py` | 3/0 | One REWRITE pair (grep-confirmed exactly one occurrence before applying): three new assertions appended after the existing `assert all(r["answer_source"] == "default" for r in records)` line inside `test_a_splittable_task_is_replaced_by_its_children`, checking `"tier1_tokens="`, `"cap_tokens=1"` and `"task_class=standard_build"` all appear in `records[0]["impact"]`. No new test added — same test, same count (214 total). |

## External actions

`git push` → run immediately after this handback commit (C5); outcome
recorded in the completion report, not in this file (write-once rule).

One mutation red-proof disposable worktree was created and removed, off
commit `15afe6d5` (after C4 was committed):

- `git worktree add .remedy-wt/f112-r17-mutation HEAD --detach` →
  mutation applied (`f"cap_tokens={fit_result.cap_tokens} "` →
  `f"cap_tokens={fit_result.cap_tokens + 1} "`, grep-confirmed exactly
  one occurrence beforehand) → targeted tests run → `git worktree
  remove .remedy-wt/f112-r17-mutation --force`.

`git worktree list` after removal showed only the primary checkout and
the pre-existing, unrelated `remedy/job-*` worktrees; no
`f112-r17-mutation` entry remained.

## Verification

**Step 0 TRANSPORT** — `cmp .agent/authored/f112-r17.md
.agent/last_block.md` ran directly this round (not denied) → exit 0,
both files **11517 bytes**. Extracted-slice byte counts, measured
programmatically against the pinned figures in the block: RECORD16
**3244 bytes** (pinned 3244, match), PLAN17 **2150 bytes / 47 content
lines, no trailing newline** (pinned 2150/47, match), DECISION D9
**5479 bytes** (pinned 5479, match). PASS.

**Step 1 LEDGER (RECORD16)** — `.agent/live_review.md` measured
**2277655 bytes** immediately before the append (matches the pinned
pre-append figure exactly). Appended as `content_bytes + b"\n" +
RECORD16_bytes` (ONE newline). Post-size measured at **2280900
bytes**, matching `2277655 + 1 + 3244` exactly (also matching the
block's pinned post-size). Old-file-is-prefix check: **True**.
Tail-equality check (`post[len(old):] == b"\n" + RECORD16_bytes`):
**True**. PASS.

**Step 2 PLAN** — PLAN17 extracted programmatically from the committed
`.agent/authored/f112-r17.md` (between its markers) to an in-memory
byte string, then written as the whole-file replacement and re-read for
confirmation: **equal, 2150 bytes both sides**. `git diff` reviewed in
full before commit; clean whole-file replacement, no unintended
content. PASS.

**Step 3 DECISION (D9)** — `.agent/decisions.md` measured **786652
bytes** immediately before the append (matches the pinned pre-append
figure exactly). Appended as `content_bytes + b"\n" + D9_bytes` (ONE
newline). Post-size measured at **792132 bytes**, matching `786652 + 1
+ 5479` exactly (also matching the block's pinned post-size).
Old-file-is-prefix check: **True**. Tail-equality check: **True**.
PASS.

**Step 4 CODE (C4)** — Both FROM strings (the `enqueue_task_decision`
call in `pingpong_job.py`, the `assert all(r["answer_source"] ==
"default" ...)` anchor line in the test file) grepped to confirm
exactly one occurrence each before applying via `Edit`; `git diff`
reviewed in full before commit and matched the block's TO text exactly
for both pairs, no unrelated changes.

Targeted: `python3 -m pytest tests/orchestration/test_job_task_runner.py
-k "TestClassBudgetCannotFitEscalation" -q` → **2 passed, 212
deselected**. Exit 0. Matches pinned expectation exactly (same 2 tests,
3 new assertion lines inside one of them, no test-count change).

Full file: `python3 -m pytest tests/orchestration/test_job_task_runner.py
-q` → **214 passed**. Exit 0. Matches pinned expectation exactly
(unchanged from round 16).

Lint: `python3 -m ruff check packages/orchestration/pingpong_job.py
tests/orchestration/test_job_task_runner.py` → **"All checks
passed!"**. Exit 0. Matches pinned expectation exactly.

Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → **42
passed**. Exit 0. Matches pinned expectation exactly.

**Step 5 MUTATION RED-PROOF** — in disposable worktree
`.remedy-wt/f112-r17-mutation` (off commit `15afe6d5`), changed
`f"cap_tokens={fit_result.cap_tokens} "` to
`f"cap_tokens={fit_result.cap_tokens + 1} "` in
`packages/orchestration/pingpong_job.py` (grep-confirmed exactly one
occurrence beforehand). Ran the targeted two-test selection:
`test_a_splittable_task_is_replaced_by_its_children` went **RED**
exactly as predicted, on `assert "cap_tokens=1" in
records[0]["impact"]` — `AssertionError: assert 'cap_tokens=1' in
'tier1_tokens=10 cap_tokens=2 task_class=standard_build'`. This is the
exact same failing value the reviewer's own dry-run measured
(`'tier1_tokens=10 cap_tokens=2 task_class=standard_build'`), an exact
match, not merely a similar one. `test_an_unsplittable_task_falls_through_uncapped`
stayed **GREEN** (it never reads `impact` at all). Result: `1 failed, 1
passed`, matching the block's prediction exactly. `git status
--porcelain` in the primary checkout read **empty** both before the
worktree was created and after it was removed. PASS.

`git status --porcelain` in the primary checkout read **empty**
immediately before this handback's own commit. PASS.

## Authored-text proofs

`.agent/authored/f112-r17.md` (committed at `a0415ff0`) vs
`.agent/last_block.md` (committed at `ddb40700`): byte-identical, `cmp`
exit 0, both 11517 bytes (Step 0 transport check above). RECORD16,
PLAN17 and DECISION D9 were all extracted programmatically from this
committed file (never retyped) and applied via the stated append
formula or whole-file write; every application was confirmed against
pinned byte counts and before/after equality checks above (Steps 1-3).
The code change (C4, the two REWRITE pairs in `pingpong_job.py` and
the test file) was typed/applied directly from the round's own prompt
text (not carried inside the authored block's markers, unlike the
ledger/plan/decision texts) and verified mechanically (FROM-occurrence
counts, a full `git diff` read before commit, the targeted/full/lint/
canary test runs, and the mutation red-proof) per Step 4-5 above.

## Deviations & assumptions

1. **No broader regression run (`tests/orchestration/ -q -n auto`)
   was ordered or run this round.** The round 17 block's Part 3
   verification list (items 1-6) does not include the broader
   `tests/orchestration/` suite that round 16's block ordered — only
   the targeted selection, the full file, lint, canary, the mutation
   red-proof and a final `git status` check. This is a deliberate
   scope narrowing stated in the block itself ("This is a small
   round... a code pair adding an `impact=` argument... plus three new
   test assertions"), not an omission on this worker's part; not run,
   per instructions.
2. **This round has six real commits (C0a, C0b, C1, C2, C3, C4) plus
   this handback as C5** — matching the block's own instructed sequence
   exactly. Stated here per item 30's "an extra commit, a dropped one,
   or a reordering is a deviation even when correct" instruction — this
   is the block's own instructed shape, not a departure from it.
3. **No search of the open-findings ledger (`.agent/live_review.md`'s
   open R-ids) was performed this round.** No new R-XXXX finding was
   minted or claimed resolved this round — the round is a
   DECISION-authorized implementation slice (closing an Acceptance
   gap), not a defect record. Item 30's "grep the DEFECT before minting
   an id" checklist obligation therefore does not apply this round.
4. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| RECORD16 booked | done | |
| PLAN17 applied | done | |
| DECISION D9 registered | done | |
| impact= wired | done | |

## Next

**Per PLAN17's Next Steps: re-verify (not re-build) T3_F112.md's
remaining Acceptance clauses against T002's already-existing fixtures**
(`test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded`,
`test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic`)
before claiming Acceptance met in full, **then the integration gate**
(full suite, twice per feature per `docs/agents/integration_gate.md`),
then closure.

**RECORD17 (this round's own verdict) is NOT YET in the ledger** —
round 17 has not been independently re-reviewed by the reviewer yet, so
no verdict exists to book. Per amend0827-process-diet rule 1, it books
in the FIRST COMMIT of the next round that is happening anyway — that
is round 18's own C1. Before starting the next round: Phase 1 rule 1 —
re-check `.agent/STOP` from disk (absent as of this round).
