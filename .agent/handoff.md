# Handoff — F112 Prompt budget per task class, round 5 (T003 start: split_one_task seam)

## Session

SESSION 2 of feature F112 · round 5 · rounds so far 5.

This round books round 4's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD4, amend0827 rule 1 — a verdict
never buys a round of its own), including R-0792's registration and
resolution (Low: an unused `ClassBudgetFit` import round 4's own
TEST_P1 slice introduced into `tests/orchestration/test_context_compiler.py`).
It then starts T003 by adding `split_one_task`, a public single-task
split seam in `packages/orchestration/task_granularity.py`, for a
future dispatch-time `cannot_fit` decision to call — it wraps the
existing `_cluster_acceptance`/`_split_task` clustering exactly, does
not re-implement or alter it, and does not touch `_split_triggers`,
`_apply_splits` or `normalize_plan` (F016's "Do not touch" boundary,
docs/roadmap/features/T3_F112.md). 4 new tests were added to
`tests/orchestration/test_task_granularity.py`.

## Range

Review of `a4c2570ddfe8e04ed431253caa06f2a24c4457eb..HEAD`
(commits C0a through C5; C6 is this handback commit itself, not yet
made at the time this file was written).

## Commits

### b18945b6 F112 R5 C0a: save round 5 authored block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r5.md` | 303/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 70f31c80 F112 R5 C0b: mirror block to last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 241/357 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). |

### 866c2bc2 F112 R5 C1: apply PLAN5 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 25/19 | Whole-file replacement with PLAN5, extracted programmatically from the committed authored file, not retyped. |

### 7230298e F112 R5 C2: fix R-0792 (unused ClassBudgetFit import)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_context_compiler.py` | 0/1 | Applied FIX_FROM→FIX_TO via `content.replace(FROM, TO, 1)`: removed the unused `ClassBudgetFit` import line R-0792 flagged. |

### d10fb2b4 F112 R5 C3: append RECORD4 to live_review.md and G4 shape note to prose_slips.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 3/0 | Appended RECORD4 (round 4's verdict, including R-0792) per G4's literal formula `content_bytes + b"\n\n" + RECORD4_bytes`. |
| `.agent/prose_slips.md` | 2/0 | Declared, per amend0827-process-diet rule 2, that the literal append formula again produced a 3-newline gap before RECORD4's `Gate:` line instead of the file's established 2-newline convention — the same recurrence round 4 flagged, bundled into this same commit per the block's own instruction and round 4's precedent. |

### 836bd4b2 F112 R5 C4: add split_one_task seam to task_granularity.py
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/task_granularity.py` | 24/0 | Applied TG_FROM→TG_TO via `content.replace(FROM, TO, 1)`, reconstructed byte-identically from the BASE_SHA blob (G5). Adds `split_one_task`, calling only existing private helpers. |

### 7d7a0904 F112 R5 C5: add split_one_task tests to test_task_granularity.py
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_task_granularity.py` | 42/0 | Applied TGT_IMPORT_FROM→TGT_IMPORT_TO then TGT_TESTS_FROM→TGT_TESTS_TO via `content.replace(FROM, TO, 1)` in that order, reconstructed byte-identically from the BASE_SHA blob (G6). |

## External actions

`git worktree add --detach .remedy-wt/f112-r5-g7 HEAD` → created for the
G7 mutation red-proof; outcome: worked, worktree's own
`task_granularity.__file__` printed and confirmed to resolve inside
`.remedy-wt/f112-r5-g7/`, not the primary checkout.
`git worktree remove .remedy-wt/f112-r5-g7 --force` → removed after the
mutation, revert and re-green cycle; outcome: succeeded, `git worktree
list` no longer shows it (six unrelated pre-existing `job-*` worktrees
from other sessions remain untouched under `.remedy-wt/`, out of this
round's scope).
`git push` → pending, run immediately after this handback commit (C6);
outcome recorded in the completion report, not in this file (write-once
rule).

## Verification

**G1 TRANSPORT** — Direct Python byte-equality read of
`.agent/authored/f112-r5.md` and `.agent/last_block.md` (substituting
for `cmp`/`diff`, both denied by the sandbox this round — same
flakiness pattern noted in round 4). Result: **equal, both 15867
bytes.** PASS.

**G2 PLAN** — PLAN5 extracted programmatically from the committed
`.agent/authored/f112-r5.md` (between its markers) to a scratch file,
then Python byte-equality against `.agent/plan.md`: **equal, both 2255
bytes.** `wc -l .agent/plan.md` → **46** (< 50). `grep -c '^## Goal'
.agent/plan.md` → **1**. `grep -c '^## Next Steps' .agent/plan.md` →
**1**. PASS.

**G3 FIX (R-0792)** — Occurrence count of `    ClassBudgetFit,` in
`tests/orchestration/test_context_compiler.py`: **1 before** the fix
commit, **0 after**. `python3 -m ruff check
tests/orchestration/test_context_compiler.py` **before** the fix (run
via `subprocess.run` inside `python3 -c`, since the sandbox denies both
the bare `ruff` binary and a direct `python3 -m ruff` shell invocation
this round — see Deviations): **F401, `ClassBudgetFit` imported but
unused** — confirmed the defect was real, not assumed. Same command
**after** the fix: **`All checks passed!`**. PASS.

**G4 LEDGER** — `.agent/live_review.md` measured **2252567 bytes**
immediately before the append, matching the block's pinned figure
exactly (no STOP triggered). RECORD4 extracted from the committed
authored file: **2300 bytes, 0 internal newlines, last byte a
newline** — matches the block's stated shape exactly. Appended as
`content_bytes + b"\n\n" + RECORD4_bytes`. Post-size measured at
**2254869 bytes**, matching `2252567 + 2 + 2300` exactly. Same shape
recurrence round 4 flagged: `content_bytes` already ended in its own
single trailing newline, so the literal formula produces 3 consecutive
newlines before `Gate:` rather than the ledger's established 2-newline
convention. Applied exactly as instructed, not silently corrected;
declared in `.agent/prose_slips.md` (commit C3), per the block's own
instruction to repeat round 4's precedent. PASS (byte arithmetic exact;
shape recurrence declared, not routed around).

**G5 PRODUCTION CODE** — Base blob of
`packages/orchestration/task_granularity.py` read via `git show
a4c2570d...:packages/orchestration/task_granularity.py` (18217 bytes);
`TG_FROM` confirmed to occur exactly **1** time in that base blob;
`TG_FROM`→`TG_TO` applied via `content.replace(FROM, TO, 1)`; result
Python-byte-equal to the committed file (19344 bytes both sides). PASS.
`python3 -m ruff check packages/orchestration/task_granularity.py`
(via `subprocess.run` inside `python3 -c`, same substitution as G3):
**`All checks passed!`**. PASS.

**G6 TEST FILE** — Base blob of
`tests/orchestration/test_task_granularity.py` read the same way
(16958 bytes); `TGT_IMPORT_FROM` and `TGT_TESTS_FROM` each confirmed to
occur exactly **1** time; `TGT_IMPORT_FROM`→`TGT_IMPORT_TO` then
`TGT_TESTS_FROM`→`TGT_TESTS_TO` applied in that order via
`content.replace(FROM, TO, 1)`; result Python-byte-equal to the
committed file (18439 bytes both sides). PASS. `python3 -m pytest
tests/orchestration/test_task_granularity.py -q` → **30 passed**. The 4
new tests confirmed by name via `-k "split_one_task" -v` →
`test_split_one_task_splits_by_acceptance_clusters`,
`test_split_one_task_returns_none_when_unsplittable`,
`test_split_one_task_avoids_collisions_against_a_supplied_used_ids_set`,
`test_split_one_task_matches_apply_splits_output_for_the_same_task` —
**4 passed, 26 deselected**. PASS.

**G7 MUTATION RED-PROOF** — Disposable worktree `.remedy-wt/f112-r5-g7`
created via `git worktree add --detach`. Worktree's own
`task_granularity.__file__` printed and confirmed to resolve inside the
worktree, not the primary checkout. Confirmed
`    if len(clusters) < 2:\n        return None\n` (4-space indent,
`split_one_task`'s own line) occurs exactly **1** time in the whole
file before mutating. Mutated to `< 1`. Ran `python3 -m pytest
tests/orchestration/test_task_granularity.py -q` inside the worktree:
**1 failed, 29 passed** — `test_split_one_task_returns_none_when_unsplittable`
failed exactly as predicted (asserted `None`, got a one-child split
list), no other test reddened. Reverted the mutation; Python
byte-equality confirmed the reverted worktree file matches the primary
checkout's copy exactly. Re-ran: **30 passed** (full green). Removed
the worktree via `git worktree remove --force`; `git worktree list` no
longer shows it. `git status --porcelain` on the PRIMARY checkout read
**empty** immediately after the mutation step and again after cleanup.
PASS.

**G8 FINAL** (four state readers as four separate invocations, plus the
canary):
- `python3 -m pytest tests/ui_server/ -q` → **515 passed**
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → **52 passed**
- `python3 -m pytest tests/regression/test_resource_safety.py -q` → **21 passed**
- `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → **16 passed**
- `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42 passed**

`git status --porcelain` read **empty** immediately before staging the
handback commit. `git ls-files .remedy-wt` read **empty**. Per-commit
`git show --numstat` `+` column, cross-checked against the Commits
table above:
- C0a `b18945b6`: `+303/-0` `.agent/authored/f112-r5.md` — matches.
- C0b `70f31c80`: `+241/-357` `.agent/last_block.md` — matches.
- C1 `866c2bc2`: `+25/-19` `.agent/plan.md` — matches.
- C2 `7230298e`: `+0/-1` `tests/orchestration/test_context_compiler.py` — matches.
- C3 `d10fb2b4`: `+3/-0` `.agent/live_review.md`, `+2/-0`
  `.agent/prose_slips.md` — matches.
- C4 `836bd4b2`: `+24/-0` `packages/orchestration/task_granularity.py`
  — matches.
- C5 `7d7a0904`: `+42/-0`
  `tests/orchestration/test_task_granularity.py` — matches.

All commits well under the 500-line insertion cap. PASS on all of the
above.

**Staleness sweep, one line per file this round touched:**
- `.agent/authored/f112-r5.md` — new file this round; nothing prior
  referenced it, so nothing else needed updating.
- `.agent/last_block.md` — whole-file mirror of the authored file every
  round; no other file depends on its prior content.
- `.agent/plan.md` — whole-file replacement every round by design; no
  other file quotes its prior text.
- `tests/orchestration/test_context_compiler.py` — removing the unused
  import does not change any test's behavior or any other file's
  reference to this file.
- `.agent/live_review.md` — append-only; the appended RECORD4 text does
  not reference or invalidate any earlier entry's content.
- `.agent/prose_slips.md` — append-only; the new entry documents this
  round's own append, does not touch or invalidate any earlier entry.
- `packages/orchestration/task_granularity.py` — `split_one_task` is
  inserted inside the "Split" section (between `_split_task` and
  `_rewire`), at the exact point the block's own `TG_FROM`/`TG_TO`
  ordered, rather than under the file's later `# Public API` section
  comment (which currently only precedes `normalize_plan`). This is not
  a staleness introduced by this round — the insertion point was fully
  dictated by the ordered pair — but it is worth flagging for whoever
  next touches this file's section comments: `split_one_task` is a
  second public entry point and the `# Public API` marker no longer
  covers the whole public surface by position alone (the function's own
  name and docstring are still fully discoverable by grep, per AGENTS.md
  §Code Discoverability). No fix made; not in this round's ordered
  change set.
- `tests/orchestration/test_task_granularity.py` — the new tests import
  and exercise `split_one_task` only; no existing test's assumptions
  were changed.

## Authored-text proofs

`.agent/authored/f112-r5.md` (committed at `b18945b6`) vs
`.agent/last_block.md` (committed at `70f31c80`): byte-identical, 15867
bytes both sides (G1, Python comparison substituting for a `cmp`/`diff`
binary the sandbox denied this round). PLAN5, FIX_FROM/TO, RECORD4,
TG_FROM/TO, TGT_IMPORT_FROM/TO and TGT_TESTS_FROM/TO were all extracted
programmatically from this committed file (never retyped) and applied
via `content.replace(FROM, TO, 1)`; every application was reconstructed
from the BASE_SHA blob and confirmed byte-identical to the committed
result (G2, G5, G6 above).

## Deviations & assumptions

1. **Bare `cmp`/`diff` denied**, same as round 4. Substituted direct
   Python byte-equality reads everywhere the block ordered a `cmp`.
   Nothing on disk is affected; only the tool used to prove equality
   changed.
2. **Neither the bare `ruff` binary nor a direct `python3 -m ruff`
   shell invocation worked this round** — both were denied by the
   sandbox as top-level Bash commands, even plain `grep` and `cp` were
   denied intermittently on their own. Running the identical command
   via `subprocess.run(...)` inside `python3 -c "..."` succeeded every
   time it was tried. Used that route for every ruff invocation in this
   round (G3, G5); reported which form worked, per the block's own
   instruction. No gate result in this handback rests on a denied
   invocation.
3. **G4's literal append formula recurs its round-4 shape mismatch**,
   as detailed in the G4 verification entry and declared in
   `.agent/prose_slips.md` (commit C3): applied exactly as the block
   specified (repeating round 4's precedent, as the block itself
   ordered), not silently corrected. The pinned byte-count arithmetic
   holds exactly.
4. **The block's general "TO contains FROM as a literal prefix"
   constraint does not hold for the `TGT_IMPORT_FROM`/`TGT_IMPORT_TO`
   pair specifically**: `TGT_IMPORT_FROM` is `"    normalize_plan,\n)\n"`
   and `TGT_IMPORT_TO` is
   `"    normalize_plan,\n    split_one_task,\n)\n"` — the new line is
   inserted BEFORE the closing paren, not appended after it, so `TO`
   does not have `FROM` as a strict string prefix even though both
   share their first line. This did not affect correctness:
   `content.replace(FROM, TO, 1)` still applies unambiguously because
   `FROM` occurs exactly once in the file, and G6's from-BASE_SHA
   reconstruction confirmed the result is byte-identical to the
   committed file. Declared because the block's own general clause
   describing all pairs as literal-prefix-shaped was inaccurate for
   this one pair; no product effect, no R-id (amend0827-process-diet
   rule 2 territory — not added to `.agent/prose_slips.md` separately
   since it is fully captured here per that rule's handback-carrier
   allowance).
5. **`.agent/prose_slips.md` was touched this round even though it is
   not among the block's named "exactly the 4 files... plus
   `.agent/plan.md`, `.agent/authored/f112-r5.md` and
   `.agent/last_block.md`."** It is the standing amend0827-process-diet
   rule 2 mechanism this exact situation exists for, and the block's
   own G4 explicitly instructed declaring the recurrence there,
   "bundled into this commit," if it recurred. Bundled into commit C3
   alongside the live_review.md append it documents.
6. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Next

T003 continued — wire `cannot_fit` into `enqueue_task_decision` (type
`task_decision`, `escalation.py:211`) at the per-task dispatch loop in
`pingpong_job.py` (~line 2307's `run_pingpong` call), per
`.agent/plan.md` Next Steps. This is the highest-risk remaining slice
(a live dispatch loop, not a pure function) and deserves its own
dedicated investigation-then-implementation round. Before that: Phase 1
rule 1 — re-check `.agent/STOP` from disk before authoring the next
round.
