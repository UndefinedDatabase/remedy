# Handoff — F112 Prompt budget per task class, round 6 (T003a: JobPlan.metadata persistence)

## Session

SESSION 2 of feature F112 · round 6 · rounds so far 6.

This round books round 5's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD5, amend0827 rule 1 — a verdict
never buys a round of its own), then records DECISION F112 D1 into
`.agent/decisions.md`, splitting T003 into T003a/T003b: investigation
found the real dispatch loop (`pingpong_job.py`) has no `task_class` on
its task objects, never activates compiled-context mode, and its
`JobPlan` has no durable `metadata` field at all — so a future
`enqueue_task_decision`'s write would silently vanish on resume. This
round ships T003a only: a durable `metadata: dict` field on `JobPlan`,
exported/imported like `input_snapshot`, plus 2 tests confirming it
round-trips through persist/load and defaults to an empty dict.
`docs/roadmap/features/T3_F112.md` was deliberately NOT touched this
round, per the block's own instruction — the DECISION is the durable
record instead.

## Range

Review of `65ded99998525e3bb96f8b7ee515ea9ac4112e17..HEAD` (commits C0a
through C5; C6 is this handback commit itself, not yet made at the time
this file was written).

## Commits

### e4286123 F112 R6 C0a: save the round 6 block verbatim to .agent/authored/f112-r6.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r6.md` | 308/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### ae79c20c F112 R6 C0b: mirror the round 6 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 208/203 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). |

### e00d8e3d F112 R6 C1: apply PLAN6 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 23/21 | Whole-file replacement with PLAN6, extracted programmatically from the committed authored file, not retyped. |

### 05e64cd6 F112 R6 C2: append RECORD5 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | Appended RECORD5 (round 5's verdict) via `content_bytes + b"\n" + RECORD5_bytes` — the ONE-newline formula this round's block specifically corrected to. |

### a097dbf0 F112 R6 C3: append DECISION F112 D1 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/0 | Appended DECISION F112 D1 (the T003→T003a/T003b split) via the same ONE-newline formula. |

### d1c4d66e F112 R6 C4: add JobPlan.metadata field for T003a persistence
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 7/0 | Applied PPJ_FIELD, PPJ_EXPORT and PPJ_IMPORT pairs in that order via `content.replace(FROM, TO, 1)`, reconstructed byte-identically from the BASE_SHA blob (G5). Adds `JobPlan.metadata: dict`, exported/imported like `input_snapshot`. |

### 01302534 F112 R6 C5: add tests/orchestration/test_job_task_runner.py metadata round-trip tests
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_task_runner.py` | 19/0 | Applied TEST_IMPORT then TEST_APPEND pairs via `content.replace(FROM, TO, 1)` in that order, reconstructed byte-identically from the BASE_SHA blob (G6). Adds 2 tests: round-trip and empty-default. |

## External actions

`git worktree add .remedy-wt/g7-mutation HEAD` → created for the G7
mutation red-proof; outcome: worked, worktree's own
`packages.orchestration.pingpong_job.__file__` printed and confirmed to
resolve inside `.remedy-wt/g7-mutation/`, not the primary checkout.
`git worktree remove .remedy-wt/g7-mutation --force` → removed after the
mutation, revert and re-green cycle; outcome: succeeded, `git worktree
list` no longer shows it (six unrelated pre-existing `job-*` worktrees
from other sessions remain untouched under `.remedy-wt/`, out of this
round's scope).
`git push` → run immediately after this handback commit (C6); outcome
recorded in the completion report, not in this file (write-once rule).

## Verification

**G1 TRANSPORT** — Direct Python byte-equality read of
`.agent/authored/f112-r6.md` and `.agent/last_block.md` (the bare `cmp`
route was not attempted; the sandbox's intermittent Bash denials this
round — see Deviations — made the Python read the reliable choice from
the start). Result: **equal, both 19657 bytes.** PASS.

**G2 PLAN** — PLAN6 extracted programmatically from the committed
`.agent/authored/f112-r6.md` (between its markers) to a scratch file
under `.remedy-wt/`, then Python byte-equality against `.agent/plan.md`:
**equal.** `wc -l .agent/plan.md` → **48** (< 50). `grep -c '^## Goal'
.agent/plan.md` → **1**. `grep -c '^## Next Steps' .agent/plan.md` →
**1**. PASS.

**G3 LEDGER (RECORD5)** — `.agent/live_review.md` measured **2254869
bytes** immediately before the append, matching the block's pinned
figure exactly (no STOP triggered). RECORD5 extracted from the
committed authored file: **1787 bytes, 0 internal newlines, last byte a
newline** — matches the block's stated shape exactly. Appended as
`content_bytes + b"\n" + RECORD5_bytes` (ONE newline, per this round's
corrected formula). Post-size measured at **2256657 bytes**, matching
`2254869 + 1 + 1787` exactly. Second reader: split the whole post-append
file on `\n\n`, last unit == RECORD5 exactly (**True**). Negative
control: flipped one byte inside RECORD5's own text in memory, re-ran
the same comparison against the file's actual last unit — mismatch
confirmed (**False**, correctly rejected). PASS.

**G4 DECISION (DECISION_F112_D1)** — `.agent/decisions.md` measured
**742368 bytes** immediately before the append, matching the block's
pinned figure exactly (no STOP triggered). DECISION_F112_D1 extracted
from the committed authored file: **3737 bytes, ends in exactly one
trailing newline, splits into exactly 7 paragraphs on `\n\n`** — matches
the block's stated shape exactly. Appended as `content_bytes + b"\n" +
DECISION_bytes`. Post-size measured at **746106 bytes**, matching
`742368 + 1 + 3737` exactly. Second reader: split the whole post-append
file on `\n\n`, last 7 units == DECISION_F112_D1's own 7 paragraphs, in
order, exactly (**True**). Negative control: flipped one byte inside the
FIRST of those 7 paragraphs in memory (on a copy), re-compared — mismatch
confirmed (**False**, correctly rejected). PASS.

**G5 PRODUCTION CODE** — Base blob of
`packages/orchestration/pingpong_job.py` read via `git show
65ded999:packages/orchestration/pingpong_job.py`; `PPJ_FIELD_FROM`,
`PPJ_EXPORT_FROM` and `PPJ_IMPORT_FROM` each confirmed to occur exactly
**1** time in that base blob; applied in order
(`PPJ_FIELD→PPJ_EXPORT→PPJ_IMPORT`) via `content.replace(FROM, TO, 1)`;
result Python-byte-equal to the committed file (**True**). PASS.
`python3 -m ruff check packages/orchestration/pingpong_job.py` (the bare
`ruff` binary was tried first and denied by the sandbox; the module form
worked on the first retry — no `subprocess.run` fallback needed):
**`All checks passed!`**. PASS.

**G6 TEST FILE** — Base blob of
`tests/orchestration/test_job_task_runner.py` read the same way;
`TEST_IMPORT_FROM` and `TEST_APPEND_FROM` each confirmed to occur
exactly **1** time; applied in order via `content.replace(FROM, TO, 1)`;
result Python-byte-equal to the committed file (**True**). PASS. `python3
-m pytest tests/orchestration/test_job_task_runner.py -q` → **193
passed** (full file, no regressions — this is a large, widely-used test
file). The 2 new tests confirmed by name via `-k "metadata" -v` → 11
selected (the 2 new tests plus 9 pre-existing tests whose names happen to
contain "metadata": `TestCatalogMetadata` x4, `TestReportRepairMetadata`
x5), **11 passed, 182 deselected**, with
`test_metadata_round_trips_through_persist_and_load` and
`test_metadata_defaults_to_an_empty_dict` both explicitly present and
PASSED in the -v output. PASS.

**G7 MUTATION RED-PROOF** — Disposable worktree `.remedy-wt/g7-mutation`
created via `git worktree add ... HEAD`. Worktree's own
`packages.orchestration.pingpong_job.__file__` printed and confirmed to
resolve inside the worktree, not the primary checkout. Confirmed
`        metadata=dict(data.get("metadata") or {}),` occurs exactly
**1** time in the worktree's copy before mutating. Mutated to
`        metadata={},`. Ran `python3 -m pytest
tests/orchestration/test_job_task_runner.py -q -k metadata` inside the
worktree: **1 failed, 10 passed** —
`test_metadata_round_trips_through_persist_and_load` failed exactly as
predicted (asserted the escalations dict, got `{}`);
`test_metadata_defaults_to_an_empty_dict` still passed, since `{}` is
its own expected result too. Reverted the mutation; Python byte-equality
confirmed the reverted worktree file matches the primary checkout's copy
exactly (**True**). Re-ran: **11 passed** (both metadata tests green
again). Removed the worktree via `git worktree remove --force`; `git
worktree list` no longer shows it. `git status --porcelain` on the
PRIMARY checkout read **empty** immediately after the mutation step and
again after cleanup. PASS.

**G8 FINAL** (four state readers as four separate invocations, plus the
canary):
- `python3 -m pytest tests/ui_server/ -q` → **515 passed**
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → **52 passed**
- `python3 -m pytest tests/regression/test_resource_safety.py -q` → **21 passed**
- `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → **16 passed**
- `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42 passed**

`git status --porcelain` read **empty** immediately before staging the
handback commit. `git ls-files .remedy-wt` read **empty**. Per-commit
`git show --numstat` `+` column, cross-checked against the Commits table
above:
- C0a `e4286123`: `+308/-0` `.agent/authored/f112-r6.md` — matches.
- C0b `ae79c20c`: `+208/-203` `.agent/last_block.md` — matches.
- C1 `e00d8e3d`: `+23/-21` `.agent/plan.md` — matches.
- C2 `05e64cd6`: `+2/-0` `.agent/live_review.md` — matches.
- C3 `a097dbf0`: `+14/-0` `.agent/decisions.md` — matches.
- C4 `d1c4d66e`: `+7/-0` `packages/orchestration/pingpong_job.py` — matches.
- C5 `01302534`: `+19/-0` `tests/orchestration/test_job_task_runner.py` — matches.

All commits well under the 500-line insertion cap (C0a/C0b exempt
regardless, as whole-file `.agent/**` rewrites, DECISION F104 D1). PASS
on all of the above.

**Staleness sweep, one line per file this round touched:**
- `.agent/authored/f112-r6.md` — new file this round; nothing prior
  referenced it, so nothing else needed updating.
- `.agent/last_block.md` — whole-file mirror of the authored file every
  round; no other file depends on its prior content.
- `.agent/plan.md` — whole-file replacement every round by design; no
  other file quotes its prior text.
- `.agent/live_review.md` — append-only; the appended RECORD5 text does
  not reference or invalidate any earlier entry's content.
- `.agent/decisions.md` — append-only; DECISION F112 D1 is new and does
  not contradict any earlier decision. `docs/roadmap/features/T3_F112.md`
  still lists T003 as a single unsplit task ("Task slicing" section) —
  this is the block's INTENDED state this round (the DECISION is the
  durable record instead of a feature-file edit), not staleness.
- `packages/orchestration/pingpong_job.py` — genuine staleness FOUND,
  out of this round's scope to fix: `packages/orchestration/decision_queue.py`
  line 397's comment `# JobPlan has no .metadata attribute; Core Job
  does. Safe for both.` and `docs/roadmap/features/T0_F018.md` line 186's
  prose `getattr fallback for `.metadata` (JobPlan has no `.metadata`)`
  are both now factually stale as of this round's C4 commit — `JobPlan`
  does have `.metadata` now. No functional defect: `getattr(job,
  "metadata", None) or {}` still degrades to `{}` for a job with empty
  metadata, and will now correctly surface real content once T003b
  starts writing decisions there — arguably the intended effect. Neither
  file is in this round's named Change list ("exactly the 4 files...
  Nothing else"), so neither was touched; flagged here for the next
  round or a dedicated cleanup to register/fix.
- `tests/orchestration/test_job_task_runner.py` — the 2 new tests import
  and exercise `JobPlan.metadata`/`save_job_plan` only; no existing
  test's assumptions were changed (confirmed by the full 193-pass run
  above).

## Authored-text proofs

`.agent/authored/f112-r6.md` (committed at `e4286123`) vs
`.agent/last_block.md` (committed at `ae79c20c`): byte-identical, 19657
bytes both sides (G1, Python comparison). PLAN6, RECORD5,
DECISION_F112_D1, PPJ_FIELD/EXPORT/IMPORT and TEST_IMPORT/APPEND were
all extracted programmatically from this committed file (never
retyped) and applied via `content.replace(FROM, TO, 1)`; every
application was reconstructed from the BASE_SHA blob and confirmed
byte-identical to the committed result (G2, G5, G6 above).

## Deviations & assumptions

1. **The sandboxed shell denied a handful of individual Bash
   invocations mid-round** (a Python one-liner writing to `/tmp`, a
   `for` loop running `git show --numstat` across all 7 commits, one
   later retry of a byte-equality read) and accepted the identical or
   equivalent command on retry every time. No gate result in this
   handback rests on a denied invocation; every reported number comes
   from a command that actually ran and printed the quoted output.
   Consistent with round 4/5's noted flakiness.
2. **`/tmp` writes are denied**; used the gitignored `.remedy-wt/`
   scratch directory for all extraction/scratch files instead (per
   standing project convention), never the primary checkout.
3. **The bare `ruff` binary was denied**, as the block itself warned it
   might be; `python3 -m ruff check <path>` worked on the first try for
   both files touched this round — no `subprocess.run` fallback was
   needed.
4. **Two pairs are not literal-prefix ("append-shaped") despite the
   block's general clause**, same pattern round 5 flagged for a
   different pair: `PPJ_IMPORT_FROM`/`PPJ_IMPORT_TO` and
   `TEST_IMPORT_FROM`/`TEST_IMPORT_TO` both insert their new line
   BEFORE the pair's trailing anchor line (`    )` / the next existing
   import name) rather than strictly after `FROM`'s own text, so `TO`
   does not have `FROM` as a strict string prefix even though both
   share their leading lines. This did not affect correctness:
   `content.replace(FROM, TO, 1)` still applies unambiguously because
   each `FROM` occurs exactly once in its file, and G5/G6's
   from-BASE_SHA reconstructions both confirmed byte-identical results.
   Declared because the block's own general clause describing all pairs
   as literal-prefix-shaped was inaccurate for these two; no product
   effect, no R-id.
5. **`git commit`'s own inline "N insertions/deletions" summary printed
   at commit time for C0b and C1 (both large single-file rewrites)
   disagreed with `git show --numstat`/`git diff --stat` read after the
   fact** (e.g. C1 printed "48 insertions(+), 46 deletions(-)" at commit
   time, `git show --numstat` reads `23/21` for the same commit). This
   is a git diff-heuristic rendering difference for near-total-file
   rewrites, not a content discrepancy — G1/G2's independent
   byte-equality checks already prove the actual file content is
   correct regardless of which insertion count is quoted. The Commits
   table and G8 cross-check above both use the `git show --numstat`
   reading, per the block's own G8 instruction.
6. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Next

T003b — derive a `task_class` for a live `TaskEntry`, wire
`compiled_context_paths`/`compiled_context_candidates` into
`pingpong_job.py`'s `run_pingpong(...)` call, then call
`fit_task_context_to_class_cap` and `enqueue_task_decision` between
`_build_task_prompt` and `task.status = TASK_RUNNING` in the per-task
loop — per `.agent/plan.md` Next Steps and DECISION F112 D1. This
remains the highest-risk remaining slice (a live dispatch loop plus a
persistence-format change together) and deserves its own dedicated
round with the call site re-read first. Before that: Phase 1 rule 1 —
re-check `.agent/STOP` from disk before authoring the next round (not
present as of this round).
