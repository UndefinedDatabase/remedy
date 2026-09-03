# Handoff — F112 Prompt budget per task class, round 9 (T003b1: task_class field on TaskEntry)

## Session

SESSION 3 of feature F112 · round 9 · rounds so far 9.

This round books round 8's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD8, amend0827 rule 1 — a verdict
never buys a round of its own), appends DECISION F112 D2 (the reviewer's
fresh investigation this round found the granularity-split seam
`split_one_task` takes `schemas/models.py`'s `PlannedTask`, not
`pingpong_job.py`'s own `TaskEntry` — no existing precedent connects
them), and ships T003b1: adds a `task_class: str = TASK_CLASS_DEFAULT`
field to `TaskEntry`, exported/imported like T003a's `metadata` field,
defaulted to the seeded `model_routing.TASK_CLASS_TIERS` key
`"standard_build"`. Per DECISION F112 D2, T003b splits into T003b1 (this
round, done) and T003b2 (the adapter, call-site wiring and decision
enqueue — deferred to its own round(s)).

## Range

Review of `66401f61abd4aca7e410634019647274ce8ebd08..HEAD` (commits C0a
through C5; C6 is this handback commit itself, not yet made at the time
this file was written). **This range is UNREVIEWED by construction** —
round 9 has not yet been independently re-reviewed by the reviewer; no
verdict on this round's own work is claimed anywhere in this file.

## Commits

### d4eea8b1 F112 R9 C0a: save round 9 block to .agent/authored/f112-r9.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r9.md` | 81/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### a0b3f6cd F112 R9 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 57/182 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). |

### 739d08a7 F112 R9 C1: append RECORD8 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | Appended RECORD8 (round 8's verdict) via `content_bytes + b"\n" + RECORD8_bytes` — the ONE-newline formula. |

### 374b4631 F112 R9 C2: apply PLAN9 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 21/23 | Whole-file replacement with PLAN9, extracted programmatically from the committed authored file, not retyped. |

### 0346d142 F112 R9 C3: append DECISION F112 D2 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/0 | Appended DECISION F112 D2 (T003b split rationale) via the same ONE-newline formula. |

### 60aa2f19 F112 R9 C4: add task_class field to TaskEntry (export/import round-trip)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 8/0 | Applied TC_CONST, TC_FIELD, TC_EXPORT, TC_IMPORT (all four REWRITE pairs, each verified TO-does-not-contain-FROM and each FROM confirmed to occur exactly once before applying): new `TASK_CLASS_DEFAULT = "standard_build"` module constant, new `task_class` field on `TaskEntry`, and its export/import round-trip in `_export_job`/`_import_job`. |

### 9d41d14b F112 R9 C5: add task_class persistence tests
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_task_runner.py` | 24/0 | Applied TC_TEST (append-shaped pair, TO verified to contain FROM as a verbatim prefix): three new tests in `TestPersistence` — default value, round-trip through persist/load, and default-is-a-seeded-model-routing-class. |

## External actions

`git push` → run immediately after this handback commit (C6); outcome
recorded in the completion report, not in this file (write-once rule).

## Verification

**Step 0 TRANSPORT** — Python byte-equality of `.agent/authored/f112-r9.md`
and `.agent/last_block.md`: **identical, True**. Extracted-slice byte
counts, measured programmatically against the pinned figures in the
block: RECORD8 **1786 bytes** (pinned 1786, match), PLAN9 **2053 bytes**
(pinned 2053, match), DECISION F112 D2 **4916 bytes** (pinned 4916,
match). PASS.

**Step 1 LEDGER (RECORD8)** — `.agent/live_review.md` measured
**2261720 bytes** immediately before the append, matching the pinned
figure exactly (no STOP triggered), and its tail (last 200 bytes) ended
with `...NO OTHER FINDING IS OWED BY THIS ROUND.\n` (RECORD7),
confirmed before appending. Appended as `content_bytes + b"\n" +
RECORD8_bytes` (ONE newline). Post-size measured at **2263507 bytes**,
matching `2261720 + 1 + 1786` exactly. Second reader: split the whole
post-append file on `\n\n`, last unit == RECORD8 exactly (**True** —
RECORD8 is one paragraph with no internal blank lines, so this check is
meaningful for it). Negative control: flipped one byte inside RECORD8's
own text in memory, re-ran the same comparison — mismatch confirmed
(**False**, correctly rejected). PASS.

**Step 2 PLAN** — PLAN9 extracted programmatically from the committed
`.agent/authored/f112-r9.md` (between its markers) to an in-memory
string, then Python byte-equality against `.agent/plan.md`: **equal,
2053 bytes both sides**. `wc -l .agent/plan.md` → **44** (matches the
block's own stated expectation — the file has 44 embedded newlines, the
45th/last line has no trailing newline so `wc -l` does not count it).
`grep -c '^## Goal' .agent/plan.md` → **1**. `grep -c '^## Next Steps'
.agent/plan.md` → **1**. PASS.

**Step 3 DECISION (D2)** — `.agent/decisions.md` measured **746106
bytes** immediately before the append, matching the pinned figure
exactly (no STOP triggered). Appended as `content_bytes + b"\n" +
D2_bytes` (ONE newline). Post-size measured at **751023 bytes**, matching
`746106 + 1 + 4916` exactly. Second reader (as literally specified —
split the WHOLE FILE on `\n\n`, compare the last unit to D2): reads
**False**, NOT True — see Deviations & assumptions item 1 for why this
is a structural property of D2's own shape (it has 6 internal blank-line
paragraph breaks, unlike RECORD8/RECORD7/RECORD6 which are single
paragraphs), not an append error. A whole-block equality check that is
actually meaningful for a multi-paragraph entry — `post[-len(d2):] ==
d2` and `post[746106:] == b"\n" + d2` — both read **True**, confirming
the append landed byte-exact. Negative control on that meaningful check:
flipped one byte inside D2's own CONTEXT paragraph (its first
paragraph, not its last), re-ran — mismatch confirmed (**False**,
correctly rejected). PASS on substance; the literal split-`\n\n` check
as worded in the block does not apply cleanly to a multi-paragraph
DECISION text (declared, not silently corrected).

**Step 4 TASK_CLASS FIELD** — Before applying, grepped the file for each
of the four FROM strings: TC_CONST **1**, TC_FIELD **1**, TC_EXPORT
**1**, TC_IMPORT **1** — all exactly once. Confirmed mechanically that
TO does NOT contain FROM as a substring for all four (`TO contains FROM:
False` × 4) — all four are REWRITE pairs, applied via `Edit`. After
applying: `TASK_CLASS_DEFAULT` occurs **3** times (definition + field
default + import fallback), `task_class` occurs **3** times (field +
export + import) — both as expected for a field wired into one dataclass
declaration plus its two round-trip sites.
`python3 -m ruff check packages/orchestration/pingpong_job.py` →
**`All checks passed!`**.
`python3 -m pytest tests/orchestration/test_job_task_runner.py -q` →
**193 passed** (code-only commit, no new tests yet — matches the block's
expectation exactly). PASS.

**Step 5 TESTS** — Confirmed `TC_TEST`'s FROM occurs exactly **1** time
in `tests/orchestration/test_job_task_runner.py` (the
`test_metadata_defaults_to_an_empty_dict` method body) before applying,
and that TO contains FROM as a verbatim prefix (**True**). Applied via
`content.replace(FROM, TO, 1)`.
`python3 -m ruff check tests/orchestration/test_job_task_runner.py` →
**`All checks passed!`**.
`python3 -m pytest tests/orchestration/test_job_task_runner.py -q` →
**196 passed** (193 + 3 new, exactly as expected). PASS.

**Step 6 MUTATION RED-PROOF** (disposable worktree only) — `git status
--porcelain` in the primary checkout read **empty** immediately before
creating the worktree. Created `git worktree add .remedy-wt/f112-r9-mutation
HEAD` (detached at `9d41d14b`). Inside the worktree ONLY, mutated
`_export_job`'s `"task_class": t.task_class,` line to `"task_class":
"",`. `python3 -m pytest tests/orchestration/test_job_task_runner.py -q`
in the worktree → **2 failed, 194 passed**, exactly as expected. The two
failing test ids exactly as pytest reported them:
`tests/orchestration/test_job_task_runner.py::TestPersistence::test_task_class_defaults_to_standard_build`
and
`tests/orchestration/test_job_task_runner.py::TestPersistence::test_task_class_round_trips_through_persist_and_load`
(both read a value back through `_export_job`, as predicted). Reverted
the mutation in the worktree (`"task_class": t.task_class,` restored,
`git status --porcelain` in the worktree read empty after revert),
re-ran the same command → **196 passed, 0 failed**. Removed the worktree
via `git worktree remove .remedy-wt/f112-r9-mutation`; `git worktree
list` no longer shows it (confirmed). `git status --porcelain` in the
primary checkout read **empty** both before creating and after removing
the worktree. No commit was made for this step (verification only). PASS.

**Step 7 CANARY AND FULL-FEATURE SPOT CHECK**:
- `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42 passed**
- `python3 -m pytest tests/orchestration/test_class_prompt_budget.py tests/orchestration/test_context_compiler.py tests/orchestration/test_task_granularity.py tests/orchestration/test_f018_authority_integration.py -q` → **237 passed** (24+69+30+114 = 237, exactly as expected)

`git status --porcelain` in the primary checkout read **empty**. PASS.

## Authored-text proofs

`.agent/authored/f112-r9.md` (committed at `d4eea8b1`) vs
`.agent/last_block.md` (committed at `a0b3f6cd`): byte-identical (Step 0
transport check above). RECORD8, PLAN9 and DECISION F112 D2 were all
extracted programmatically from this committed file (never retyped) and
applied via the stated append formulas or whole-file write; every
application was confirmed against pinned byte counts and before/after
equality checks above (Steps 1-3). TC_CONST/TC_FIELD/TC_EXPORT/TC_IMPORT
and TC_TEST were typed directly from the round's own prompt text (not
carried inside the authored block's markers, unlike the ledger/plan/
decision texts) and verified mechanically (occurrence counts,
FROM/TO containment checks) before and after application, per Steps 4-5
above.

## Deviations & assumptions

1. **Step 3's literal second-reader instruction ("split on `\n\n`,
   confirm the last unit equals D2 exactly") reads False, not True, for
   the correctly-appended D2** — reported honestly rather than silently
   reinterpreted or papered over. Root cause: D2, unlike every RECORD
   entry booked into `live_review.md` so far, is a multi-paragraph
   DECISION text with 6 internal blank-line breaks (CONTEXT / MEASURED /
   CHOSEN / ALTERNATIVE CONSIDERED AND REJECTED / CONSEQUENCE / REVERSE).
   Splitting the WHOLE FILE on `\n\n` and taking the last unit yields
   only D2's own final REVERSE paragraph (`"REVERSE by deleting this
   DECISION and treating T003b as a single unsplit round again."`), not
   the whole 4916-byte D2 block — this is a structural fact about D2's
   own shape, not an append defect. The append's correctness is fully
   established by the exact byte arithmetic (`746106 + 1 + 4916 ==
   751023`, measured and matched) and by two whole-block equality checks
   that ARE meaningful for a multi-paragraph text: `post[-len(d2):] ==
   d2` and `post[746106:] == b"\n" + d2`, both **True**, with a negative
   control (one byte flipped inside D2's own CONTEXT paragraph) correctly
   reading **False**. Did not adjust the pinned byte-count arithmetic to
   compensate — that arithmetic was correct and is unaffected by this
   finding, which concerns only which post-hoc equality check is
   meaningful for a multi-paragraph append.
2. **`git commit`'s own inline insertion/deletion summary disagreed with
   `git show --numstat` read after the fact for C0b's whole-file rewrite
   of `.agent/last_block.md`** (commit-time summary read `81 insertions,
   206 deletions`; `git show --numstat` read `57 insertions, 182
   deletions`) — the same class of discrepancy rounds 7 and 8 both
   declared for their own C0b commits. The Commits table above uses the
   `git show --numstat` reading throughout.
3. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Next

**T003b2** (per DECISION F112 D2 and the rewritten `.agent/plan.md` Next
Steps): a `TaskEntry`→`PlannedTask` adapter (`acceptance.splitlines()`,
empty `files_hint` — safe per D2's MEASURED paragraph), the
`fit_task_context_to_class_cap` call between `_build_task_prompt` and
`task.status = TASK_RUNNING`, wiring its compiled paths into this loop's
`run_pingpong(compiled_context_paths=..., compiled_context_candidates=...)`
call, and on `cannot_fit` calling `enqueue_task_decision`
(`options=["split task"]` only when `split_one_task` via the adapter
returns non-`None`) then `auto_apply_safe_default` under `--yes`. Five
still-untested, first-time-wired pieces against the live dispatch loop —
its own dedicated round(s), fresh investigation already done in D2 but
re-read the call site fresh again before authoring, per `.agent/plan.md`
Risks.

**RECORD9 (this round's own verdict) is NOT YET in the ledger** — round 9
has not been independently re-reviewed by the reviewer yet, so no
verdict exists to book. Per amend0827-process-diet rule 1, it must be
booked by the round after next (i.e. not T003b2's own round, but the one
following it). Before starting T003b2: Phase 1 rule 1 — re-check
`.agent/STOP` from disk (not present as of this round).
