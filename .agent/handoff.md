# Handoff — F112 Prompt budget per task class, round 14 (T003b2b2a: fit_task_context_to_class_cap + compiled_context_* wiring at the job-dispatch call site)

## Session

SESSION 4 of feature F112 · round 14 · rounds so far 14.

This round books round 13's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD13, amend0827 rule 1 — a pending
verdict books in the FIRST COMMIT of the next round that is happening
anyway, i.e. round N's verdict books in round N+1's first commit), then
ships **T003b2b2a** exactly as DECISION F112 D6's CHOSEN clause
specified: the job-dispatch call site (`pingpong_job.py`'s `run_job`,
its one `run_pingpong(` call) gains a `fit_task_context_to_class_cap`
check and three new `run_pingpong` kwargs
(`compiled_context_paths`, `compiled_context_candidates` set to the
same list, `compiled_context_token_budget`). When `task.files_hint` is
empty or the fit reports `fits=False`, all three stay `None` — today's
exact `build_repo_context` fallback, unchanged. No escalation on
`cannot_fit` this round (that is T003b2b2b, deferred, per D6).

This round ships production code: two files touched
(`packages/orchestration/pingpong_job.py`,
`tests/orchestration/test_job_task_runner.py`), 126 insertions total —
well under the 500-line cap. A DECISION (F112 D6) was pre-authored and
registered this round (C3), since it settles a genuinely new scope
split (T003b2b2 → T003b2b2a/T003b2b2b) the reviewer found before
delegating.

## Range

Review of `5c05e0cb..HEAD` (commits C0a, C0b, C1, C2, C3, C4, plus this
handback commit C5 itself — six commits total this round). **This
range is UNREVIEWED by construction** — round 14 has not yet been
independently re-reviewed by the reviewer; no verdict on this round's
own work is claimed anywhere in this file.

## Commits

### 6db8ea0b F112 R14 C0a: save round 14 block to .agent/authored/f112-r14.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r14.md` | 85/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### dc7bf8e0 F112 R14 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 49/26 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). `cmp` itself was denied by the sandbox this round (documented, recurring property); substituted with a `python3` byte-equality read (`a == b` → True, both **10458 bytes**), the documented equivalent proof. |

### e9d040ee F112 R14 C1: append RECORD13 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD13 (round 13's verdict) via `content_bytes + b"\n" + RECORD13_bytes` — the ONE-newline formula. |

### f5e947bd F112 R14 C2: apply PLAN14 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 25/20 | Whole-file replacement with PLAN14, extracted programmatically from the committed authored file, not retyped. No trailing newline (per the block). |

### 7dd49cbb F112 R14 C3: append DECISION F112 D6 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/1 | Appended DECISION F112 D6 via `content_bytes + b"\n" + D6_bytes` — the ONE-newline formula. Records the T003b2b2 → T003b2b2a/T003b2b2b split and the `compiled_context_candidates` source fix. |

### 44c51728 F112 R14 C4: wire fit_task_context_to_class_cap + compiled_context_* into the job-dispatch run_pingpong call (T003b2b2a)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 21/0 | Pair A (REWRITE, occurred exactly once, grep-confirmed before applying): inserts the `fit_task_context_to_class_cap` gate ahead of the `try:`/`run_pingpong(` call, computing `compiled_context_paths`/`compiled_context_candidates`/`compiled_context_token_budget`, all `None` unless `task.files_hint` is non-empty AND the fit reports `fits=True`. Pair B (REWRITE, occurred exactly once): appends the three new kwargs onto the `run_pingpong(...)` call. `Path` was already imported at module top; `fit_task_context_to_class_cap` is a local import inside the `if task.files_hint:` block, matching `run_pingpong`'s own local-import style for `context_compiler`. |
| `tests/orchestration/test_job_task_runner.py` | 105/0 | Byte-exact file-end append (verified via ordered-equality: pre-edit blob is an exact PREFIX of the post-edit file, appended slice is an exact SUFFIX, `git diff` shows only pure insertions in order) — new `TestClassBudgetCompiledContextWiring` class with three tests: a fitting `files_hint` wires all three kwargs; a `files_hint` that cannot fit its class cap (forced via a monkeypatched `default_cap = 1` config) leaves all three `None`; an empty `files_hint` (two-task job, no `Files:` section) leaves all three `None` across both dispatched tasks. |

## External actions

`git push` → run immediately after this handback commit (C5); outcome
recorded in the completion report, not in this file (write-once rule).

Mutation red-proof worktree `.remedy-wt/f112-r14-mutation` was created
(`git worktree add .remedy-wt/f112-r14-mutation HEAD --detach`, off
commit `44c51728`, after C4 was committed), the mutation
(`if fit_result.fits:` → `if True:`) applied there only (never in the
primary checkout), the targeted tests run, and the worktree removed
(`git worktree remove .remedy-wt/f112-r14-mutation --force`) before
this handback (C5) was written. `git worktree list` after removal
showed only the primary checkout and the pre-existing, unrelated
`remedy/job-*` worktrees; no `f112-r14-mutation` entry remained.

## Verification

**Step 0 TRANSPORT** — `cmp .agent/authored/f112-r14.md
.agent/last_block.md` was DENIED by the sandbox this round (the same
documented, recurring property RECORD12/RECORD13 both name). Substituted
with a `python3` byte-equality read: `a == b` → **True**, both files
**10458 bytes**. Extracted-slice byte counts, measured programmatically
against the pinned figures in the block, both BEFORE saving to disk and
again after re-reading the committed file: RECORD13 **1631 bytes**
(pinned 1631, match), PLAN14 **2394 bytes / 49 content lines** (pinned
2394/49, match), DECISION D6 **5788 bytes** (pinned 5788, match). PASS.

**Step 1 LEDGER (RECORD13)** — `.agent/live_review.md` measured
**2271288 bytes** immediately before the append (matches the pinned
pre-append figure exactly). Appended as `content_bytes + b"\n" +
RECORD13_bytes` (ONE newline). Post-size measured at **2272920
bytes**, matching `2271288 + 1 + 1631` exactly (also matching the
block's pinned post-size). Old-file-is-prefix check: **True**.
Tail-equality check (`post[len(old):] == b"\n" + RECORD13_bytes`):
**True**. PASS.

**Step 2 PLAN** — PLAN14 extracted programmatically from the committed
`.agent/authored/f112-r14.md` (between its markers) to an in-memory
byte string, then written as the whole-file replacement and re-read
for confirmation: **equal, 2394 bytes both sides**. `git diff` reviewed
in full before commit; clean whole-file replacement, no unintended
content. PASS.

**Step 3 DECISION (D6)** — `.agent/decisions.md` measured **766660
bytes** immediately before the append (matches the pinned pre-append
figure exactly). Appended as `content_bytes + b"\n" + D6_bytes` (ONE
newline). Post-size measured at **772449 bytes**, matching `766660 + 1
+ 5788` exactly (also matching the block's pinned post-size).
Old-file-is-prefix check: **True**. Tail-equality check: **True**.
PASS.

**Step 4 CODE (C4)** — Both FROM strings (Pairs A, B — REWRITE) grepped
to confirm exactly one occurrence each before applying via `Edit`;
`git diff` reviewed in full before commit and matched the block's TO
text exactly, no unrelated changes. Additionally cross-checked before
applying: `run_pingpong`'s three `compiled_context_*` kwargs already
exist at `pingpong_loop.py:2863-2865` (confirming the call-site wiring
targets real parameters); `ClassBudgetFit.fits`/`cap_tokens` fields
confirmed at `context_compiler.py:944-949`; `TaskEntry.files_hint`/
`task_class` fields confirmed at `pingpong_job.py:127,137`.

Targeted: `python3 -m pytest tests/orchestration/test_job_task_runner.py
-k "test_a_fitting_files_hint_wires_compiled_context_into_run_pingpong or
test_a_files_hint_that_cannot_fit_its_class_cap_falls_through_unchanged or
test_an_empty_files_hint_leaves_compiled_context_untouched" -q` →
**3 passed, 206 deselected**. Full file: `python3 -m pytest
tests/orchestration/test_job_task_runner.py -q` → **209 passed** (206
existing + 3 new, no regressions). Lint: `python3 -m ruff check
packages/orchestration/pingpong_job.py
tests/orchestration/test_job_task_runner.py` → **"All checks
passed!"**. Canary: `python3 -m pytest tests/cli/test_golden_path.py
-q` → **42 passed** (bare `pytest ...` was denied by the sandbox this
round; `python3 -m pytest ...` is the reliable form — see Deviations).
PASS, all as pinned.

**Step 5 MUTATION RED-PROOF** — in the disposable worktree
`.remedy-wt/f112-r14-mutation` (off commit `44c51728`), changed
`if fit_result.fits:` to `if True:` in
`packages/orchestration/pingpong_job.py` (grep-confirmed exactly one
occurrence beforehand). Ran the same targeted three-test selection from
Step 4 there: `test_a_files_hint_that_cannot_fit_its_class_cap_falls_through_unchanged`
went **RED** exactly as predicted —
`AssertionError: assert ['src/main.py', 'docs/README.md'] is None` —
because forcing the `if True:` branch always wires the three kwargs
regardless of `fits`, so the "cannot fit" fixture's forced `default_cap
= 1` no longer produces the expected `None` fallback. The other two
tests stayed **GREEN**. Result: `1 failed, 2 passed`, matching the
block's prediction exactly. `git status --porcelain` in the primary
checkout read **empty** both before the worktree was created and after
it was removed. PASS.

`git status --porcelain` in the primary checkout read **empty**
immediately before this handback's own commit. PASS.

## Authored-text proofs

`.agent/authored/f112-r14.md` (committed at `6db8ea0b`) vs
`.agent/last_block.md` (committed at `dc7bf8e0`): byte-identical (Step
0 transport check above — `cmp` was denied, substituted with a
`python3` byte-equality read). RECORD13, PLAN14 and DECISION D6 were
all extracted programmatically from this committed file (never
retyped) and applied via the stated append formula or whole-file
write; every application was confirmed against pinned byte counts and
before/after equality checks above (Steps 1-3). The code change (C4,
Pairs A-B plus the file-end test append) was typed directly from the
round's own prompt text (not carried inside the authored block's
markers, unlike the ledger/plan/decision texts) and verified
mechanically (FROM-occurrence counts, a full `git diff` read before
commit, cross-checks against the real `run_pingpong`/`ClassBudgetFit`/
`TaskEntry` signatures, the targeted/full/lint/canary test runs, and
the mutation red-proof) per Step 4-5 above.

## Deviations & assumptions

1. **`cmp` was denied by the sandbox this round** (the same documented,
   recurring property RECORD12/RECORD13 both name — it flips round to
   round and is tracked as a known session property, not a shortcut).
   Substituted with a `python3` byte-equality read in every case the
   block called for `cmp` (Step 0 transport check). This is the
   substitution the block itself pre-authorized ("there is no paste
   relay this session").
2. **Bare `pytest tests/cli/test_golden_path.py -q` (Part 3 step 4) was
   also denied by the sandbox**; `python3 -m pytest
   tests/cli/test_golden_path.py -q` ran cleanly and produced the exact
   pinned result (42 passed). Not a design deviation — same command,
   same result, only the invocation form the sandbox accepted differs.
   `python3 -m ruff check <path>` (already the block's own instructed
   form) was likewise the only lint form that ran.
3. **A `cp` shell command (Part 2, C0b's literal instruction) was
   denied by the sandbox**; substituted by writing the mirror file's
   exact content directly via the Write tool (having just authored that
   same content for `.agent/authored/f112-r14.md`), then verified
   byte-identical via the Step 0 `python3` read. Same outcome (a
   byte-identical mirror file), different tool used to produce it.
4. **No search of the open-findings ledger (`.agent/live_review.md`'s
   open R-ids) was performed this round.** No new R-XXXX finding was
   minted or claimed resolved this round — the round is a
   DECISION-authorized implementation slice (T003b2b2a), not a defect
   record. Item 30's "grep the DEFECT before minting an id" checklist
   obligation therefore does not apply this round; stated here for
   completeness rather than silently omitted.
5. **This round has six real commits (C0a, C0b, C1, C2, C3, C4) plus
   this handback as C5** — matching the block's own instructed
   sequence exactly, including the DECISION commit C3 (present this
   round, unlike round 13 which had none). Stated here per item 30's
   "an extra commit, a dropped one, or a reordering is a deviation even
   when correct" instruction — this is the block's own instructed
   shape, not a departure from it.
6. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| RECORD13 booked | done | |
| PLAN14 applied | done | |
| DECISION D6 registered | done | |
| T003b2b2a shipped | done | |

## Next

**T003b2b2b** (per PLAN14's Next Steps, per DECISION F112 D6): the
`cannot_fit` → `enqueue_task_decision` → `auto_apply_safe_default` →
`split_one_task` chain. **Mandatory prerequisite reading before
authoring** — do NOT attempt to design or build T003b2b2b this round:
`run_job`'s own task-iteration structure (how tasks are consumed from
`job.tasks`, whether a split's children can be inserted back into the
dispatch sequence, or whether the current task can be skipped/replaced
after a split). `split_one_task` is not called anywhere in
`pingpong_job.py` today (confirmed by grep — only a comment references
it), and `run_job`'s dispatch loop (`pingpong_job.py:1761`) has no
existing machinery for this — that shape is unread and undesigned,
per D6's own CHOSEN clause.

**RECORD14 (this round's own verdict) is NOT YET in the ledger** —
round 14 has not been independently re-reviewed by the reviewer yet,
so no verdict exists to book. Per amend0827-process-diet rule 1, it
books in the FIRST COMMIT of the next round that is happening anyway —
that is round 15's own C1. Before starting T003b2b2b: Phase 1 rule 1 —
re-check `.agent/STOP` from disk (not present as of this round).
