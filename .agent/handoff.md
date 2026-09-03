# Handoff — F112 Prompt budget per task class, round 4 (T002: compiler cap wiring)

## Session

SESSION 2 of feature F112 · round 4 · rounds so far 4.

This round books round 3's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD3, amend0827 rule 1 — a verdict
never buys a round of its own), then wires T001's per-class cap
resolver (`resolve_task_class_cap`) onto the context compiler's
existing demotion cascade: a new `ClassBudgetFit` dataclass and
`fit_task_context_to_class_cap` function in
`packages/orchestration/context_compiler.py`, with 4 tests in
`tests/orchestration/test_context_compiler.py` covering
fits-under-cap-with-demotion, cannot_fit-arithmetic, vocabulary
refusal, and real-config wiring (no mock of the resolver in the last
two). The demotion cascade itself, calibration (F074) and granularity
heuristics were not touched, per docs/roadmap/features/T3_F112.md "Do
not touch".

## Range

Review of `3eae460d55a68f292c7a04e76011639b748033ca..4301efc20ea55b5e13a87aea65b77a0b8d926586`
(commits C0a through C4; C5 is this handback commit itself, not yet
made at the time this file was written).

## Commits

### 0910804d F112 R4 C0a: save round 4 block to .agent/authored/f112-r4.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r4.md` | 419/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### e38f7beb F112 R4 C0b: mirror round 4 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 370/343 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). |

### 218e6967 F112 R4 C1: apply PLAN4 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 9/11 | Whole-file replacement with PLAN4, extracted programmatically from the committed authored file, not retyped. |

### 72153bbf F112 R4 C2: append RECORD3 to live_review.md and declare the append-shape discrepancy in prose_slips.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 3/0 | Appended RECORD3 (round 3's verdict) per G3's literal formula `content_bytes + b"\n\n" + RECORD3_bytes`. |
| `.agent/prose_slips.md` | 2/0 | Declared, per amend0827-process-diet rule 2, that the literal append formula produced a 3-newline gap before RECORD3's `Gate:` line instead of the file's established 2-newline (one blank line) convention, because `content_bytes` already carried its own trailing newline before the append. This file is not in the block's named 6-file change set; it is the standing amend0827 rule 2 mechanism, used identically by many prior rounds (see `.agent/prose_slips.md`'s own history) to record exactly this class of block/reality mismatch without spending an R-id, so it is bundled into the same commit as the operation it documents rather than left silent or given an unordered 7th commit. |

### 15bc512a F112 R4 C3: add ClassBudgetFit and fit_task_context_to_class_cap to context_compiler.py
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/context_compiler.py` | 66/0 | Applied CC_IMPORT_FROM→CC_IMPORT_TO then CC_MODULE_FROM→CC_MODULE_TO via `content.replace(FROM, TO, 1)`, in that order, reconstructed byte-identically from the BASE_SHA blob (G4). |

### 4301efc2 F112 R4 C4: add 4 tests to test_context_compiler.py for the per-class cap resolver wiring
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_context_compiler.py` | 104/0 | Applied TEST_P1 through TEST_P5 via `content.replace(FROM, TO, 1)` in that exact order, reconstructed byte-identically from the BASE_SHA blob (G5). |

## External actions

`git worktree add --detach .remedy-wt/f112-r4-mutation HEAD` → created for
the G6 mutation red-proof; outcome: worked, worktree's own
`context_compiler.__file__` printed and confirmed to resolve inside
`.remedy-wt/f112-r4-mutation/`, not the primary checkout.
`git worktree remove .remedy-wt/f112-r4-mutation --force` → removed after
the mutation, revert and re-green cycle; outcome: succeeded, `git
worktree list` no longer shows it.
`git push` → pending, run immediately after this handback commit (C5);
outcome recorded in the completion report, not in this file (write-once
rule).

## Verification

**G1 TRANSPORT** — `cmp .agent/authored/f112-r4.md .agent/last_block.md`.
The sandboxed shell denied the bare `cmp`/`diff` binaries this round (a
new, session-specific denial not seen in earlier F112 rounds); substituted
a direct Python byte-equality read of both files' full contents, which is
the same proof `cmp`'s exit code encodes. Result: **equal, both 18767
bytes.** PASS.

**G2 PLAN** — PLAN4 extracted programmatically from the committed
`.agent/authored/f112-r4.md` (between its markers) to
`.remedy-wt/PLAN4.extracted`, then Python byte-equality against
`.agent/plan.md`: **equal.** `wc -l .agent/plan.md` → **40** (< 50).
`grep -c '^## Goal' .agent/plan.md` → **1**. `grep -c '^## Next Steps'
.agent/plan.md` → **1**. PASS.

**G3 LEDGER** — `.agent/live_review.md` measured **2250826 bytes**
immediately before the append, matching the block's pinned figure exactly
(no STOP triggered). RECORD3 extracted from the committed authored file:
**1739 bytes, 0 internal newlines, last byte a newline** — matches the
block's stated shape exactly. Appended as `content_bytes + b"\n\n" +
RECORD3_bytes`. Post-size measured at **2252567 bytes**, matching
`2250826 + 2 + 1739` exactly. **Second reader (as literally specified):
FAILED strict equality** — splitting the whole post-append file on `\n\n`
gives a last unit of `\n` + RECORD3 (1740 bytes) rather than RECORD3
alone (1739 bytes), because `content_bytes` already ended in its own
single trailing newline before the append added `\n\n`, producing 3
consecutive newlines before `Gate:` instead of the ledger's established
2-newline (one blank line) convention every other entry carries. This
was applied exactly as instructed — not silently corrected — and
declared in `.agent/prose_slips.md` (see C2 above) rather than repaired
by deviating from the ordered formula. **Negative control:** flipping
one byte inside RECORD3's own text (in-memory only) correctly makes the
last split unit differ from both the original and the flipped RECORD3 —
confirmed the check itself discriminates. The byte-count arithmetic,
which is the primary, numerically pinned proof, holds exactly; only the
cosmetic shape check does not. PARTIAL (byte arithmetic PASS, shape
check as literally read FAILED — declared, not routed around).

**G4 PRODUCTION CODE** — Base blob of
`packages/orchestration/context_compiler.py` read via `git show
3eae460d...:packages/orchestration/context_compiler.py`; CC_IMPORT_FROM→
CC_IMPORT_TO then CC_MODULE_FROM→CC_MODULE_TO applied via
`content.replace(FROM, TO, 1)`; result Python-byte-equal to the committed
file (50615 bytes both sides). PASS. `ruff check
packages/orchestration/context_compiler.py`: bare `ruff` binary denied by
the sandbox (consistent with every prior F112 round). `python3 -m ruff
check packages/orchestration/context_compiler.py`: denied on the first
attempt (a session-wide flaky-permission pattern that also hit several
plain-python invocations this round, unrelated to ruff specifically),
succeeded on retry with **`All checks passed!`**. The module form is what
worked, as in every prior round. PASS.

**G5 TEST FILE** — Base blob of
`tests/orchestration/test_context_compiler.py` read the same way; TEST_P1
through TEST_P5 applied in that exact order via `content.replace(FROM,
TO, 1)`; result Python-byte-equal to the committed file (58292 bytes both
sides). PASS. `python3 -m pytest tests/orchestration/test_context_compiler.py -q`
→ **69 passed**. The 4 new tests confirmed by name via `-k
"oversized_context_fits_under_its_class_cap or
unfittable_context_reports_cannot_fit or
class_outside_the_shared_vocabulary_is_refused or
the_cap_comes_from_the_real_resolver_when_config_sets_one" -v` → **4
passed, 65 deselected**. PASS. (Not gated by this round's block, but
worth reporting: `python3 -m ruff check
tests/orchestration/test_context_compiler.py` reports one **F401**,
`ClassBudgetFit` imported but never referenced by name in any of the new
tests — the tests only call `fit_task_context_to_class_cap` and read
attributes off its return value. TEST_P1 is the exact slice that adds
this import; applying it byte for byte per the ordered
`content.replace` is what the round required. Left as ordered rather
than silently trimmed, since G5 names no ruff requirement for this file
and removing the import would be an edit outside the ordered pairs.)

**G6 MUTATION RED-PROOF** — Disposable worktree
`.remedy-wt/f112-r4-mutation` created via `git worktree add --detach`.
Worktree's own `context_compiler.__file__` printed and confirmed to
resolve inside the worktree, not the primary checkout. Confirmed
`if selected.tier == TIER_FENCED` occurs exactly **1** time in the whole
file (inside `fit_task_context_to_class_cap`'s `tier1_tokens`
computation) before mutating. Mutated to `!=`. Ran
`python3 -m pytest tests/orchestration/test_context_compiler.py -q`
inside the worktree: **2 failed, 67 passed** —
`test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded`
and
`test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic`
both failed on their `tier1_tokens` assertion, exactly as predicted, and
no other test reddened. Reverted the mutation; Python byte-equality
confirmed the reverted worktree file matches the primary checkout's copy
exactly. Re-ran: **69 passed** (full green). Removed the worktree via
`git worktree remove --force`; `git worktree list` no longer shows it.
`git status --porcelain` on the PRIMARY checkout read **empty**
immediately after the mutation step and again after cleanup. PASS.

**G7 STATE READERS AND CANARY** (five separate invocations):
- `python3 -m pytest tests/ui_server/ -q` → **515 passed**
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → **52 passed**
- `python3 -m pytest tests/regression/test_resource_safety.py -q` → **21 passed**
- `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → **16 passed**
- `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42 passed**

PASS on all five.

**G8 TREE, COMMITS, SWEEP** — `git status --porcelain` read **empty**
immediately before staging the handback commit. `git ls-files
.remedy-wt` read **empty**. Per-commit `git show --numstat` `+` column,
cross-checked against the Commits table above:
- C0a `0910804d`: `+419/-0` `.agent/authored/f112-r4.md` — matches.
- C0b `e38f7beb`: `+370/-343` `.agent/last_block.md` — matches.
- C1 `218e6967`: `+9/-11` `.agent/plan.md` — matches.
- C2 `72153bbf`: `+3/-0` `.agent/live_review.md`, `+2/-0`
  `.agent/prose_slips.md` — matches.
- C3 `15bc512a`: `+66/-0` `packages/orchestration/context_compiler.py`
  — matches.
- C4 `4301efc2`: `+104/-0`
  `tests/orchestration/test_context_compiler.py` — matches.

All commits well under the 500-line insertion cap. PASS.

**Staleness sweep, one line per file this round touched:**
- `.agent/authored/f112-r4.md` — new file this round; nothing prior
  referenced it, so nothing else needed updating.
- `.agent/last_block.md` — whole-file mirror of the authored file every
  round; no other file depends on its prior content.
- `.agent/plan.md` — whole-file replacement every round by design; no
  other file quotes its prior text.
- `.agent/live_review.md` — append-only; the appended RECORD3 text does
  not reference or invalidate any earlier entry's content.
- `.agent/prose_slips.md` — append-only; the new entry documents this
  round's own append, does not touch or invalidate any earlier entry.
- `packages/orchestration/context_compiler.py` — **stale by
  construction of this round's own ordered change set**: the module
  docstring's `Public API::` list (lines ~71-96) enumerates every public
  name the module exports, and was NOT updated to add `ClassBudgetFit`
  or `fit_task_context_to_class_cap`. The block's CC_MODULE_TO slice
  does not touch the docstring, and the block's own Change clause reads
  "exactly the 6 files named in the Commits section below. Nothing
  else." — editing the docstring was not in the ordered change set, so
  it was left alone rather than silently expanded. Declared here for the
  next round to close (T003 is a natural place, since it will also add
  new public names to this and other modules).
- `tests/orchestration/test_context_compiler.py` — the new
  `ClassBudgetFit` import (TEST_P1) is unused by any test body (see the
  G5 ruff note above); applied exactly as ordered, not trimmed.

## Authored-text proofs

`.agent/authored/f112-r4.md` (committed at `0910804d`) vs
`.agent/last_block.md` (committed at `e38f7beb`): byte-identical, 18767
bytes both sides (G1, Python comparison substituting for a `cmp`/`diff`
binary the sandbox denied this round). PLAN4, RECORD3, CC_IMPORT_FROM/TO,
CC_MODULE_FROM/TO and TEST_P1 through TEST_P5 were all extracted
programmatically from this committed file (never retyped) and applied via
`content.replace(FROM, TO, 1)`; every application was reconstructed from
the BASE_SHA blob and confirmed byte-identical to the committed result
(G2, G4, G5 above).

## Deviations & assumptions

1. **Bare `cmp`/`diff` denied.** The sandboxed shell refused both `cmp`
   and `diff -q` outright this round (a new denial pattern; earlier F112
   rounds report `ruff` as the flaky one, not these). Substituted direct
   Python byte-equality reads everywhere the block ordered a `cmp`.
   Nothing on disk is affected; only the tool used to prove equality
   changed.
2. **Sandbox permission denials were flaky and non-deterministic
   throughout this round**, hitting `cmp`, `diff -q`, and even plain
   `python3 -c "..."` calls that succeeded on identical retry seconds
   later (see the G4 ruff note). Every denied command was retried and
   succeeded, or replaced with an equivalent Python read; no gate result
   in this handback rests on a denied invocation.
3. **G3's second-reader shape check does not hold under a literal
   reading**, for the reason detailed in the G3 verification entry above
   and declared in `.agent/prose_slips.md` (commit C2). The append
   formula was applied exactly as the block specified; the primary,
   numerically pinned byte-count proof (pre-size, RECORD3's own shape,
   post-size) holds exactly. This is a deviation from what the "second
   reader... confirm the last unit equals RECORD3 exactly" clause
   predicts, not from any instruction about what bytes to write.
4. **`.agent/prose_slips.md` was touched this round even though it is
   not among the block's named "exactly the 6 files."** It is the
   standing amend0827-process-diet rule 2 mechanism this exact situation
   exists for (a worker-declared, no-product-effect prose discrepancy),
   used by essentially every prior F112 round and dozens of others
   across the repository's history for the identical purpose; bundled
   into commit C2 alongside the live_review.md append it documents
   rather than given an unordered 7th commit or left undeclared.
5. **The context_compiler.py module docstring's Public API list is now
   stale** (does not name `ClassBudgetFit` or
   `fit_task_context_to_class_cap`) because the block's own ordered
   change set did not include a docstring edit and explicitly capped the
   change set at "exactly the 6 files... Nothing else." Not fixed this
   round; declared in the staleness sweep above for the next round to
   close.
6. **`tests/orchestration/test_context_compiler.py` carries one ruff
   F401** (`ClassBudgetFit` imported but unused) after TEST_P1 is applied
   exactly as ordered. G5 does not gate ruff on this file, so it was left
   as ordered rather than trimmed outside the change set. Declared for
   visibility; a future round may either use the name in an `isinstance`
   assertion or drop the import, whichever the reviewer prefers.
7. **`git push` outcome is not recorded in this file** (write-once rule)
   — see the completion report for the real result.

## Next

T003 — decision wiring (`escalation.enqueue_task_decision`, type
`task_decision`), unattended default split, granularity-machinery seam,
per `.agent/plan.md` Next Steps. Before that: Phase 1 rule 1 — re-check
`.agent/STOP` from disk before authoring the next round.
