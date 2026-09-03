# Handoff — F112 Prompt budget per task class, round 10 (T003b2a: compiled_context_token_budget passthrough + TaskEntry→PlannedTask adapter)

## Session

SESSION 3 of feature F112 · round 10 · rounds so far 10.

This round books round 9's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD9, amend0827 rule 1 — a verdict
never buys a round of its own), appends DECISION F112 D3 (fresh
investigation this round found `run_pingpong` has no token-budget
passthrough at all: wiring `compiled_context_paths`/`compiled_context_candidates`
alone, as DECISION F112 D2's own plan.md Next Steps literally named,
would silently recompile every task at `compile_task_context`'s
generic `DEFAULT_CONTEXT_TOKEN_BUDGET` rather than the resolved class
cap — the exact silent ballooning T3_F112.md exists to close), and
ships T003b2a: a new `compiled_context_token_budget: int | None = None`
keyword parameter on `run_pingpong` (additive only — every existing
caller that omits it keeps today's exact behavior), plus the
`TaskEntry`→`PlannedTask` adapter DECISION F112 D2 already named
(`task_entry_to_planned_task`). Per DECISION F112 D3, T003b2 splits
further into T003b2a (this round, done — both pieces unit-tested in
isolation) and T003b2b (the live call-site wiring — deferred to its
own round(s)).

## Range

Review of `58cfae0e..HEAD` (commits C0a through C5; C6 is this handback
commit itself, not yet made at the time this file was written). **This
range is UNREVIEWED by construction** — round 10 has not yet been
independently re-reviewed by the reviewer; no verdict on this round's
own work is claimed anywhere in this file.

## Commits

### 50f0c711 F112 R10 C0a: save round 10 block to .agent/authored/f112-r10.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r10.md` | 83/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### d093273d F112 R10 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 37/35 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). `cmp` confirmed byte-identical before commit. |

### 408a983e F112 R10 C1: append RECORD9 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD9 (round 9's verdict) via `content_bytes + b"\n" + RECORD9_bytes` — the ONE-newline formula. |

### e11952be F112 R10 C2: apply PLAN10 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 22/20 | Whole-file replacement with PLAN10, extracted programmatically from the committed authored file, not retyped. |

### b0965a39 F112 R10 C3: append DECISION F112 D3 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/1 | Appended DECISION F112 D3 (T003b2 further-split rationale) via the same ONE-newline formula. |

### c2bbc5f9 F112 R10 C4: add compiled_context_token_budget passthrough to run_pingpong
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_loop.py` | 8/0 | Applied Pair A (APPEND-shaped, TO verified to contain FROM as a literal prefix) and Pair B (REWRITE, FROM confirmed to occur exactly once before applying): new `compiled_context_token_budget: int | None = None` keyword parameter, and `compile_task_context`'s call site now only overrides `token_budget` when the caller supplies one. |
| `tests/orchestration/test_pingpong.py` | 51/0 | File-end append (byte-length-arithmetic verified): `TestCompiledContextTokenBudget` with two tests — the kwarg reaches `compile_task_context` when supplied, and is absent from its kwargs when omitted. |

### 01864da1 F112 R10 C5: add task_entry_to_planned_task adapter
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 37/1 | Applied the insertion pair (REWRITE, FROM confirmed to occur exactly once before applying): new `task_entry_to_planned_task(task: TaskEntry) -> PlannedTask \| None` adapter function, plus (deviation, see below) a `TYPE_CHECKING`-guarded import of `PlannedTask` needed to satisfy `ruff` F821 on the return annotation. |
| `tests/orchestration/test_job_task_runner.py` | 62/0 | Two REWRITE import pairs (Pair C: `TaskEntry`; Pair D: `task_entry_to_planned_task`, both FROM confirmed to occur exactly once before applying) plus a file-end append (byte-length-arithmetic verified): `TestTaskEntryToPlannedTaskAdapter` with four tests — field mapping/newline-splitting, goal-falls-back-to-title, empty-acceptance returns None, and a real round-trip through `task_granularity.split_one_task`. |

## External actions

`git push` → run immediately after this handback commit (C6); outcome
recorded in the completion report, not in this file (write-once rule).

Two disposable worktrees created and removed during this round, both
for mutation red-proofs only (never committed to, never merged):
- `git worktree add .remedy-wt/f112-r10-mutation-c4 HEAD` (detached at
  `b0965a39`, before C4's own commit — the real C4 fix+tests were
  copied in from the primary checkout's working tree onto this base so
  the mutation could be tested without ever mutating the primary
  checkout) → `git worktree remove .remedy-wt/f112-r10-mutation-c4 --force`.
- `git worktree add .remedy-wt/f112-r10-mutation-c5 HEAD` (detached at
  `c2bbc5f9`, after C4's real commit, before C5's own commit — same
  copy-in pattern) → `git worktree remove .remedy-wt/f112-r10-mutation-c5 --force`.

`git worktree list` after both removals shows neither
`f112-r10-mutation-c4` nor `f112-r10-mutation-c5` (confirmed; only the
pre-existing, unrelated `remedy/job-*` worktrees and the primary
checkout remain).

## Verification

**Step 0 TRANSPORT** — `cmp .agent/authored/f112-r10.md .agent/last_block.md`
→ no output, exit 0 (byte-identical). Extracted-slice byte counts,
measured programmatically against the pinned figures in the block:
PLAN10 **2166 bytes** (pinned 2166, match), DECISION F112 D3 **5085
bytes** (pinned 5085, match). RECORD9 was not separately pinned in the
block (no byte count given in its header, unlike PLAN10/D3), measured
at **2019 bytes** for the record. PASS.

**Step 1 LEDGER (RECORD9)** — `.agent/live_review.md` measured
**2263507 bytes** immediately before the append. Appended as
`content_bytes + b"\n" + RECORD9_bytes` (ONE newline). Post-size
measured at **2265527 bytes**, matching `2263507 + 1 + 2019` exactly.
Old-file-is-prefix check: **True**. Tail-equality check
(`post[len(old):] == b"\n" + RECORD9_bytes`): **True**. `git diff`
inspected by eye: exactly one new paragraph line appended after RECORD8,
no other line touched. PASS.

**Step 2 PLAN** — PLAN10 extracted programmatically from the committed
`.agent/authored/f112-r10.md` (between its markers) to an in-memory
string, then Python byte-equality against `.agent/plan.md`: **equal,
2166 bytes both sides**. `wc -l .agent/plan.md` → **46**. `grep -c
'^## Goal' .agent/plan.md` → **1**. `grep -c '^## Next Steps'
.agent/plan.md` → **1**. PASS.

**Step 3 DECISION (D3)** — `.agent/decisions.md` measured **751023
bytes** immediately before the append. Appended as `content_bytes +
b"\n" + D3_bytes` (ONE newline). Post-size measured at **756109
bytes**, matching `751023 + 1 + 5085` exactly. Old-file-is-prefix
check: **True**. Tail-equality check: **True**. `git diff` inspected by
eye: D3 appended immediately after D2's REVERSE line, matching the
established pattern from D2's own append onto D1. PASS.

**Step 4 COMPILED_CONTEXT_TOKEN_BUDGET (C4)** — Grepped the file for
each of Pair A's and Pair B's FROM strings before applying: both
**exactly 1** occurrence. Pair A verified TO contains FROM as a literal
prefix (**True**) before applying via `Edit`. Pair B (REWRITE) applied
via `Edit`. After applying:
`python3 -m pytest tests/orchestration/test_pingpong.py -k TestCompiledContextTokenBudget -q`
→ **2 passed, 34 deselected**.
`python3 -m pytest tests/orchestration/test_pingpong.py -q` → **36
passed** (no regressions).
`python3 -m ruff check packages/orchestration/pingpong_loop.py tests/orchestration/test_pingpong.py`
→ **`All checks passed!`**. PASS.

**Step 5 MUTATION RED-PROOF for C4** (disposable worktree only) — `git
status --porcelain` in the primary checkout read **empty** immediately
before creating the worktree. Created
`git worktree add .remedy-wt/f112-r10-mutation-c4 HEAD` (detached at
`b0965a39`, the commit before C4's own — C4 was not yet committed to
the primary checkout at this point). Copied the working-tree state of
`pingpong_loop.py` and `test_pingpong.py` (the real, correct C4
fix+tests, uncommitted in the primary checkout at the time) into the
worktree. Baseline run in the worktree (unmutated) →
`python3 -m pytest tests/orchestration/test_pingpong.py -k TestCompiledContextTokenBudget -q`
→ **2 passed** (sanity check the copy landed correctly). Mutated: deleted
the `if compiled_context_token_budget is not None:` line and its body,
leaving `compile_kwargs` permanently `{}`. Re-ran the same command →
**1 failed, 1 passed**: `test_token_budget_reaches_compile_task_context`
went RED (`AssertionError: assert None == 777`, i.e. the kwarg no
longer reaches `compile_task_context`), and
`test_no_token_budget_kwarg_when_caller_omits_it` stayed GREEN, exactly
as the block specified (both colors reported, not a uniform-red
mutation). Removed the worktree via
`git worktree remove .remedy-wt/f112-r10-mutation-c4 --force`; `git
worktree list` no longer shows it. `git status --porcelain` in the
primary checkout read **empty** both before creating and after removing
the worktree — the mutation never touched the primary checkout. Only
then was C4 committed for real (with the correct, unmutated code) to
the primary checkout. PASS.

**Step 6 TASK_ENTRY_TO_PLANNED_TASK ADAPTER (C5)** — Grepped the file
for the insertion pair's FROM string before applying: **exactly 1**
occurrence. Applied via `Edit` (REWRITE). `python3 -c "import ast;
ast.parse(...)"` on `pingpong_job.py` → **syntax OK**.
`python3 -m ruff check packages/orchestration/pingpong_job.py` → first
run FAILED: `F821 Undefined name PlannedTask` on the return annotation
(see Deviations item 1 below for the fix and why the block's own claim
about `from __future__ import annotations` did not hold under `ruff`).
After adding a `TYPE_CHECKING`-guarded import (matching this codebase's
own established convention, e.g. `packages/orchestration/approval_queue.py`):
`python3 -m ruff check packages/orchestration/pingpong_job.py
tests/orchestration/test_job_task_runner.py` → **`All checks passed!`**.
Both import pairs (C: `TaskEntry`; D: `task_entry_to_planned_task`)
grepped before applying: each **exactly 1** occurrence. File-end test
append verified by byte-length arithmetic: pre **121206** bytes,
appended **2243** bytes, post **123449** bytes, `post_len == pre_len +
appended_len` (**True**), tail equals the appended text exactly
(**True**).
`python3 -m pytest tests/orchestration/test_job_task_runner.py -k TestTaskEntryToPlannedTaskAdapter -q`
→ **4 passed**.
`python3 -m pytest tests/orchestration/test_job_task_runner.py -q` →
**200 passed** (no regressions). PASS.

**Step 7 MUTATION RED-PROOF for C5** (disposable worktree only) — `git
status --porcelain` in the primary checkout read **empty** immediately
before creating the worktree. Created
`git worktree add .remedy-wt/f112-r10-mutation-c5 HEAD` (detached at
`c2bbc5f9`, i.e. after C4's real commit, before C5's own — C5 was not
yet committed to the primary checkout at this point). Copied the
working-tree state of `pingpong_job.py` and `test_job_task_runner.py`
(the real, correct C5 fix+tests, uncommitted in the primary checkout at
the time) into the worktree. Baseline run in the worktree (unmutated) →
`python3 -m pytest tests/orchestration/test_job_task_runner.py -k TestTaskEntryToPlannedTaskAdapter -q`
→ **4 passed** (sanity check the copy landed correctly). Mutated:
inverted `if not lines: return None` to `if lines: return None`.
Re-ran the same command → **4 failed, 0 passed**, a strict superset of
the block's required both-directions proof:
`test_returns_none_when_acceptance_has_no_non_blank_line` went RED
(acceptance is now empty when the guard fires the WRONG way, and rather
than "wrongly returning a PlannedTask" as the block's prose put it, the
mutated code falls through to `PlannedTask(acceptance=[], ...)`, which
pydantic's own `min_length=1` validator on `PlannedTask.acceptance`
then rejects with `ValidationError: List should have at least 1 item`
— still RED, for the same underlying reason, just surfacing as an
exception rather than a silently-wrong return value).
`test_maps_fields_and_splits_acceptance_on_newlines` went RED
(`assert planned is not None` failed — wrongly returns `None` for a
non-empty acceptance list), exactly as the block specified. The two
tests the block did not name,
`test_goal_falls_back_to_title_when_body_is_empty` and
`test_output_is_accepted_by_split_one_task_and_clusters_one_child_per_line`,
also went RED for the identical structural reason as the second case
(both feed non-blank acceptance, so the inverted guard wrongly returns
`None` for them too) — reported as additional evidence, not a
surprise: with 3 of the 4 tests using non-blank acceptance and only 1
using blank acceptance, this 3-red/1-red split is the only possible
outcome of this specific inversion, and it still cleanly demonstrates
both directions of the guard being reached. Reverted the mutation in
the worktree (`if not lines: return None` restored), re-ran the same
command → **4 passed, 0 failed**. Removed the worktree via
`git worktree remove .remedy-wt/f112-r10-mutation-c5 --force`; `git
worktree list` no longer shows it. `git status --porcelain` in the
primary checkout read **empty** both before creating and after removing
the worktree — the mutation never touched the primary checkout. Only
then was C5 committed for real (with the correct, unmutated code) to
the primary checkout. PASS.

**Step 8 FULL-PAIR REGRESSION, LINT, CANARY**:
- `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_job_task_runner.py -q` → **236 passed**
- `python3 -m ruff check packages/orchestration/pingpong_loop.py packages/orchestration/pingpong_job.py tests/orchestration/test_pingpong.py tests/orchestration/test_job_task_runner.py` → **`All checks passed!`**
- `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42 passed**

`git status --porcelain` in the primary checkout read **empty**
immediately before this handback's own commit. PASS.

## Authored-text proofs

`.agent/authored/f112-r10.md` (committed at `50f0c711`) vs
`.agent/last_block.md` (committed at `d093273d`): byte-identical (Step 0
transport check above, `cmp` clean). RECORD9, PLAN10 and DECISION F112
D3 were all extracted programmatically from this committed file (never
retyped) and applied via the stated append formulas or whole-file
write; every application was confirmed against pinned byte counts (or,
for RECORD9, measured directly since no byte count was pinned for it)
and before/after equality checks above (Steps 1-3). Pair A/Pair B (C4)
and the insertion pair plus Pairs C/D (C5) were typed directly from the
round's own prompt text (not carried inside the authored block's
markers, unlike the ledger/plan/decision texts) and verified
mechanically (occurrence counts, prefix/containment checks) before and
after application, per Steps 4 and 6 above.

## Deviations & assumptions

1. **The block's own claim that `-> PlannedTask | None` is "fine
   unevaluated even without a module-level import" because
   `pingpong_job.py` already has `from __future__ import annotations`
   did not hold under `ruff`.** `python3 -m ruff check
   packages/orchestration/pingpong_job.py` failed with `F821 Undefined
   name PlannedTask` pointing at the return annotation — pyflakes/ruff
   still resolves names used in annotations even when they are deferred
   to strings by PEP 563, because a caller could evaluate them later
   (e.g. via `typing.get_type_hints()`) and hit a real `NameError`.
   Fixed by adding a `TYPE_CHECKING`-guarded import,
   `if TYPE_CHECKING: from packages.orchestration.schemas.models import
   PlannedTask`, immediately after the module's existing imports —
   this is the exact convention already used elsewhere in this
   codebase for the identical situation (e.g.
   `packages/orchestration/approval_queue.py:50-51`, `budget_guard.py:31`,
   `job_fulfillment.py:22`, and seven other files). `from typing import
   Any` became `from typing import TYPE_CHECKING, Any`. The runtime
   `from packages.orchestration.schemas.models import PlannedTask`
   import inside the function body (needed to actually construct
   `PlannedTask` at runtime) was kept exactly as the block specified —
   only the annotation-time name resolution needed the extra guard.
   Confirmed no behavior change: `ruff` clean, all 236 tests across both
   files pass, mutation red-proofs both hold. This is a 4-line addition
   (3 import lines + 1 blank) beyond the block's own diff, well inside
   the 500-line cap.
2. **C4's and C5's mutation worktrees were created from the commit
   BEFORE each change's own commit** (`b0965a39` for C4, `c2bbc5f9` for
   C5), with the real fix+tests copied in from the primary checkout's
   uncommitted working tree, rather than from a commit that already
   contained the change. This was necessary because the block's own
   instruction ("run the mutation red-proof... before committing") logically
   requires the mutation to be exercised before the corresponding
   commit exists, and `git worktree add` needs a base commit to check
   out — the base used was the nearest ancestor, with the working
   tree's real (uncommitted) files copied on top. The primary checkout
   was never mutated at any point; `git status --porcelain` read empty
   there before and after both worktree lifecycles.
3. **`git commit`'s own inline insertion/deletion summary disagreed
   with `git show --numstat` read after the fact for C0b's whole-file
   rewrite of `.agent/last_block.md`** (commit-time summary read `83
   insertions, 81 deletions`; `git show --numstat` read `37 insertions,
   35 deletions`) — the same class of discrepancy rounds 7, 8 and 9 all
   declared for their own C0b commits. The Commits table above uses the
   `git show --numstat` reading throughout.
4. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.
5. **No search of the open-findings ledger (`.agent/live_review.md`'s
   open R-ids) was performed this round.** No new R-XXXX finding was
   minted or claimed resolved this round — only DECISION F112 D3 was
   authored (a scope/design decision, not a defect record). Item 30's
   "grep the DEFECT before minting an id" checklist obligation therefore
   does not apply this round; stated here for completeness rather than
   silently omitted.

## Next

**T003b2b** (per DECISION F112 D3 and the rewritten `.agent/plan.md`
Next Steps): call `fit_task_context_to_class_cap` between
`_build_task_prompt` and `task.status = TASK_RUNNING`; pass its
compiled paths, the job's repo candidate listing, and `cap_tokens` into
`run_pingpong(compiled_context_paths=..., compiled_context_candidates=...,
compiled_context_token_budget=...)`; on `cannot_fit` call
`enqueue_task_decision` (`options=["split task"]` only when
`task_entry_to_planned_task(task) is not None` and `split_one_task` on
its result returns non-`None`) then `auto_apply_safe_default` under
`--yes`. Three still-untested pieces against the live dispatch loop
(narrowed from D2's original five, since the parameter and the adapter
are now both proven in isolation) — its own dedicated round(s),
re-read the call site fresh again before authoring, per
`.agent/plan.md` Risks and DECISION F112 D2/D3.

**RECORD10 (this round's own verdict) is NOT YET in the ledger** —
round 10 has not been independently re-reviewed by the reviewer yet, so
no verdict exists to book. Per amend0827-process-diet rule 1, it must
be booked by the round after next (i.e. not T003b2b's own round, but
the one following it). Before starting T003b2b: Phase 1 rule 1 —
re-check `.agent/STOP` from disk (not present as of this round).
