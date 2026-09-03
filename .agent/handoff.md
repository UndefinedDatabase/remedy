# Handoff — F112 Prompt budget per task class, round 7 (housekeeping: book R6, fix R-0793)

## Session

SESSION 2 of feature F112 · round 7 · rounds so far 7.

This round books round 6's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD6, amend0827 rule 1 — a verdict
never buys a round of its own), and fixes R-0793 (Low, no functional
effect): a comment in `packages/orchestration/decision_queue.py` and a
prose line in `docs/roadmap/features/T0_F018.md` both still claimed
"JobPlan has no `.metadata`" after round 6's own C4 gave `JobPlan`
exactly that field. Ships NO new behavior; T003b remains deferred to its
own future round per DECISION F112 D1.

**A new, unregistered, currently-FAILING test was found during this
round's staleness sweep — flagged below, NOT fixed (out of this round's
declared change set). See "New finding" under Deviations.**

## Range

Review of `d4cf30549963d0b022c5b50915ebb14a7d534bb3..HEAD` (commits C0a
through C3; C4 is this handback commit itself, not yet made at the time
this file was written).

## Commits

### fd4b958c F112 R7 C0a: save the round 7 block verbatim to .agent/authored/f112-r7.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r7.md` | 184/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 38a1c92b F112 R7 C0b: mirror the round 7 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 120/244 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). |

### 09d538d1 F112 R7 C1: apply PLAN7 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 21/23 | Whole-file replacement with PLAN7, extracted programmatically from the committed authored file, not retyped. |

### 1d2485b3 F112 R7 C2: fix R-0793 (stale JobPlan.metadata comment/doc)
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T0_F018.md` | 1/1 | Applied F018_FROM→F018_TO via `content.replace(FROM, TO, 1)`, extracted programmatically from the committed authored file. Corrects the stale "JobPlan has no `.metadata`" prose. |
| `packages/orchestration/decision_queue.py` | 2/1 | Applied DQ_FROM→DQ_TO via `content.replace(FROM, TO, 1)`. Comment-only; the `getattr(job, "metadata", None) or {}` line itself is untouched. |

### 90b1dd67 F112 R7 C3: append RECORD6 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | Appended RECORD6 (round 6's verdict, including R-0793's registration and resolution) via `content_bytes + b"\n" + RECORD6_bytes` — the ONE-newline formula. |

## External actions

`git push` → run immediately after this handback commit (C4); outcome
recorded in the completion report, not in this file (write-once rule).

## Verification

**G1 TRANSPORT** — Python byte-equality read of
`.agent/authored/f112-r7.md` and `.agent/last_block.md` (bare `cmp` not
attempted; Python read used directly per this session's noted sandbox
flakiness). Result: **equal, both 11342 bytes.** PASS.

**G2 PLAN** — PLAN7 extracted programmatically from the committed
`.agent/authored/f112-r7.md` (between its markers) to an in-memory
string, then Python byte-equality against `.agent/plan.md`: **equal,
2149 bytes both sides.** `wc -l .agent/plan.md` → **46** (< 50).
`grep -c '^## Goal' .agent/plan.md` → **1**. `grep -c '^## Next Steps'
.agent/plan.md` → **1**. PASS.

**G3 FIX (R-0793)** — DQ_FROM and F018_FROM (extracted programmatically
from the committed authored file, never retyped) each confirmed to
occur exactly **1** time in their respective files BEFORE the fix, and
**0** times AFTER, with DQ_TO's first line and F018_TO both occurring
**1** time after. `ruff check packages/orchestration/decision_queue.py`:
bare `ruff` binary denied, `python3 -m ruff check <path>` also denied as
a direct Bash invocation; fell back to `subprocess.run([...])` inside
`python3 -c` (worked). Read **`All checks passed!` both BEFORE the fix**
(checked against a `.remedy-wt/scratch/` copy of the `git show
HEAD:...` blob, i.e. the pre-C2 committed state) **and AFTER** (working
tree post-fix). Comment-only change, as expected. PASS.

**G4 LEDGER (RECORD6)** — `.agent/live_review.md` measured **2256657
bytes** immediately before the append, matching the block's pinned
figure exactly (no STOP triggered). RECORD6 extracted from the
committed authored file: raw extracted text between markers was 2349
bytes with no trailing newline; per the block's own stated shape ("ONE
line ... ending in exactly one trailing newline") and the same
convention round 6 used for RECORD5, one trailing `\n` was appended to
the extracted text to form RECORD6_bytes, giving **2350 bytes, 0
internal newlines, last byte a newline** — matches the block's stated
shape and pinned length exactly. Appended as `content_bytes + b"\n" +
RECORD6_bytes` (ONE newline). Post-size measured at **2259008 bytes**,
matching `2256657 + 1 + 2350` exactly. Second reader: split the whole
post-append file on `\n\n`, last unit == RECORD6 exactly (**True**).
Negative control: flipped one byte inside RECORD6's own text in memory,
re-ran the same comparison against the file's actual last unit —
mismatch confirmed (**False**, correctly rejected). PASS.

**G5 DOCS-ROUND GATE** — `python3 -m pytest tests/docs/ -q` → **295
passed**. `python3 -m pytest tests/orchestration/test_roadmap_index.py
-q` → **30 passed**. PASS.

**G6 STATE READERS AND CANARY** (five separate invocations):
- `python3 -m pytest tests/ui_server/ -q` → **515 passed**
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → **52 passed**
- `python3 -m pytest tests/regression/test_resource_safety.py -q` → **21 passed**
- `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → **16 passed**
- `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42 passed**

All PASS.

**G7 TREE, COMMITS, SWEEP** — `git status --porcelain` read **empty**
immediately before staging the handback commit. `git ls-files
.remedy-wt` read **empty**. Per-commit `git show --numstat` `+` column,
cross-checked against the Commits table above:
- C0a `fd4b958c`: `+184/-0` `.agent/authored/f112-r7.md` — matches.
- C0b `38a1c92b`: `+120/-244` `.agent/last_block.md` — matches.
- C1 `09d538d1`: `+21/-23` `.agent/plan.md` — matches.
- C2 `1d2485b3`: `+1/-1` `docs/roadmap/features/T0_F018.md`, `+2/-1`
  `packages/orchestration/decision_queue.py` — matches.
- C3 `90b1dd67`: `+2/-0` `.agent/live_review.md` — matches.

All commits well under the 500-line insertion cap (C0a/C0b exempt
regardless, as whole-file `.agent/**` rewrites, DECISION F104 D1).

**Staleness sweep, one line per file this round touched:**
- `.agent/authored/f112-r7.md` — new file this round; nothing prior
  referenced it, so nothing else needed updating.
- `.agent/last_block.md` — whole-file mirror of the authored file every
  round; no other file depends on its prior content.
- `.agent/plan.md` — whole-file replacement every round by design; no
  other file quotes its prior text.
- `packages/orchestration/decision_queue.py` /
  `docs/roadmap/features/T0_F018.md` — repo-wide search for the retired
  phrase "JobPlan has no" (via `git grep`, subprocess fallback) turned
  up two OTHER unrelated hits about different attributes
  (`decision_inbox.py:74` and `decision_queue.py:94`, both about
  `.tasks`/`.artifacts`, not `.metadata` — correctly left untouched) and
  **one further, genuinely stale AND currently BROKEN hit**:
  `tests/orchestration/test_f018_authority_integration.py:1044-1050`,
  `TestRealJobPlanDecision::test_jobplan_no_metadata_attr_safe`, whose
  docstring makes the same retired claim and whose body asserts
  `not hasattr(job, "metadata")` — an assertion round 6's own C4 made
  false. Confirmed currently RED: `python3 -m pytest
  tests/orchestration/test_f018_authority_integration.py -q` →
  **1 failed, 113 passed**, the failure being exactly this test
  (`AssertionError: assert not True`). This file predates round 6
  (authored 2026-07-22, per `git blame`) and is NOT in this round's
  declared change set ("exactly the 2 files ... plus state files.
  Nothing else"), so it was deliberately NOT fixed here — see New
  finding below.
- `.agent/live_review.md` — append-only; the appended RECORD6 text does
  not reference or invalidate any earlier entry's content.

## Authored-text proofs

`.agent/authored/f112-r7.md` (committed at `fd4b958c`) vs
`.agent/last_block.md` (committed at `38a1c92b`): byte-identical, 11342
bytes both sides (G1, Python comparison). PLAN7, DQ_FROM/DQ_TO,
F018_FROM/F018_TO and RECORD6 were all extracted programmatically from
this committed file (never retyped) and applied via
`content.replace(FROM, TO, 1)` or the stated append formula; every
application was confirmed against before/after occurrence counts or
byte-equality above (G2, G3, G4).

## Deviations & assumptions

1. **New finding, NOT registered or fixed this round (out of scope):**
   `tests/orchestration/test_f018_authority_integration.py::TestRealJobPlanDecision::test_jobplan_no_metadata_attr_safe`
   is currently FAILING on this branch (confirmed by direct run: `1
   failed, 113 passed`), caused by round 6's own C4
   (`JobPlan.metadata` field addition, commit `d1c4d66e`) — the test's
   own body asserts `not hasattr(job, "metadata")`, which is now false.
   This is a genuine product-affecting regression (test file under
   `tests/`, qualifies for an R-id per amend0827 rule 2), not a prose
   inaccuracy, and it predates R-0793's scope (R-0793 named only
   `decision_queue.py` and `T0_F018.md`). It was NOT caught by round
   6's own gates because those scoped test execution to
   `tests/orchestration/test_job_task_runner.py` only, never this file.
   Checked the open set first (checklist item 30): `git grep -n
   test_jobplan_no_metadata_attr_safe` and a scan of `.agent/live_review.md`
   for existing `R-0` entries found no prior registration. This round's
   own change set is fixed exactly by the block ("exactly the 2 files
   ... Nothing else"), so it was declared here rather than silently
   fixed — the reviewer should register it as its own finding (likely
   Medium: a real test regression, not merely stale prose, though the
   underlying behavior change — `JobPlan` now carrying real metadata —
   is itself intentional per T003a; the test's assumption is what needs
   updating) and schedule its own fix round.
2. **The sandboxed shell denied several individual Bash invocations
   mid-round** (a Python one-liner writing to the repo root instead of
   `.remedy-wt/` scratch, later corrected; `ruff` bare binary; `python3
   -m ruff check <path>` as a direct Bash invocation; `git grep`;
   `python3 -c` running a repo-wide os.walk scan, which also separately
   timed out and was backgrounded rather than denied) and accepted the
   identical or an equivalent command on retry or via the
   `subprocess.run(...)` inside `python3 -c` fallback every time. No
   gate result in this handback rests on a denied invocation; every
   reported number comes from a command that actually ran and printed
   the quoted output. Consistent with prior rounds' noted flakiness.
3. **`/tmp` writes are denied**; used the gitignored `.remedy-wt/`
   scratch directory for all extraction/scratch files instead (one
   scratch file was briefly written to the repo root by mistake before
   this was corrected and the file removed — never committed, `git
   status --porcelain` confirmed empty before every commit).
4. **The bare `ruff` binary AND the `python3 -m ruff check <path>` form
   were both denied** as direct Bash invocations this round (the block
   itself anticipated this three-tier fallback); the third tier,
   `subprocess.run([...])` inside `python3 -c`, worked on first try.
5. **RECORD6's extraction required appending one trailing `\n` to the
   raw text found between the `<<<BEGIN RECORD6>>>`/`<<<END RECORD6>>>`
   markers** (2349 bytes raw, no trailing newline as extracted) to reach
   the block's own pinned 2350-byte figure and its stated shape ("ending
   in exactly one trailing newline") — the same convention used for
   PLAN7 and matching round 6's RECORD5 handling. Declared for
   transparency; not a deviation from the block's own instructions, just
   the marker-stripping mechanics made explicit.
6. **`git commit`'s own inline insertion/deletion summary occasionally
   disagreed with `git show --numstat`/`git diff --stat` read after the
   fact for large single-file rewrites** (same class round 6 declared);
   the Commits table and G7 cross-check above both use the `git show
   --numstat` reading throughout.
7. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Next

Two candidate next actions, in priority order:
1. **Register and fix the newly-found regression** in
   `tests/orchestration/test_f018_authority_integration.py` (see New
   finding above) — likely its own short round, since it is a real red
   test on the branch, not scheduled work.
2. **T003b** — derive a `task_class` for a live `TaskEntry`, wire
   `compiled_context_paths`/`compiled_context_candidates` into
   `pingpong_job.py`'s `run_pingpong(...)` call, then call
   `fit_task_context_to_class_cap` and `enqueue_task_decision` between
   `_build_task_prompt` and `task.status = TASK_RUNNING` in the per-task
   loop — per `.agent/plan.md` Next Steps and DECISION F112 D1. This
   remains the highest-risk remaining slice and is flagged as the likely
   point a NEW SESSION should pick it up fresh, per
   docs/agents/self_drive_protocol.md's session-count guidance (this is
   session 2, round 7 — well inside the 4-5-round-per-session default
   but a natural session boundary given T003b's own "fresh investigation
   first" requirement).

Before either: Phase 1 rule 1 — re-check `.agent/STOP` from disk before
authoring the next round (not present as of this round).
