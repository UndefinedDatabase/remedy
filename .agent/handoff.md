# Handoff — F112 Prompt budget per task class, round 8 (housekeeping: book R7, fix R-0794)

## Session

SESSION 2 of feature F112 · round 8 · rounds so far 8.

This round books round 7's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD7, amend0827 rule 1 — a verdict
never buys a round of its own), including R-0794's registration AND
resolution in the same booking, and fixes R-0794 (Medium): round 7's own
worker found `test_jobplan_no_metadata_attr_safe` in
`tests/orchestration/test_f018_authority_integration.py` RED on the
branch tip — its own premise (`not hasattr(job, "metadata")` on a bare
`JobPlan()`) went permanently false when round 6's own `JobPlan.metadata`
field addition landed. Fixed by reconstructing the metadata-absent state
explicitly via `del job.metadata`, preserving the test's original intent
(list_decisions must not crash when metadata is absent) exactly. Ships NO
new behavior in `packages/`; T003b remains deferred to its own future
round per DECISION F112 D1.

**SESSION-END CANDIDATE FLAGGED — see "Next" below.** This is round 8 of
session 2; the branch tip is now fully green across every suite this
session has touched, with no open findings owed. T003b needs a full
fresh re-read of the dispatch loop per its own "fresh investigation
first" requirement in `.agent/plan.md`, so this is a strong candidate
point to end the session rather than start T003b on round-8 fatigue.

## Range

Review of `e5add7cd1de51b5ebabc7a550e6606d98c269388..HEAD` (commits C0a
through C3; C4 is this handback commit itself, not yet made at the time
this file was written).

## Commits

### 7e58b1d4 F112 R8 C0a: save round 8 block to .agent/authored/f112-r8.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r8.md` | 206/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 0888f593 F112 R8 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 133/111 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). |

### a55e546b F112 R8 C1: apply PLAN8 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 23/22 | Whole-file replacement with PLAN8, extracted programmatically from the committed authored file, not retyped. |

### 1e8dfabf F112 R8 C2: fix R-0794 (stale metadata-absence premise in test_jobplan_no_metadata_attr_safe)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_f018_authority_integration.py` | 6/1 | Applied TEST_FIX_FROM→TEST_FIX_TO via `content.replace(FROM, TO, 1)`, extracted programmatically from the committed authored file. Rewrites the docstring and adds an explicit `del job.metadata` to reconstruct the absent-metadata state a real `JobPlan()` can no longer naturally be in. |

### 00b02a4d F112 R8 C3: append RECORD7 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | Appended RECORD7 (round 7's verdict, including R-0794's registration and resolution) via `content_bytes + b"\n" + RECORD7_bytes` — the ONE-newline formula. |

## External actions

`git push` → run immediately after this handback commit (C4); outcome
recorded in the completion report, not in this file (write-once rule).

## Verification

**G1 TRANSPORT** — Python byte-equality read (via `hashlib.sha256`) of
`.agent/authored/f112-r8.md` and `.agent/last_block.md`. Result:
**equal, both 12928 bytes, identical SHA256.** PASS.

**G2 PLAN** — PLAN8 extracted programmatically from the committed
`.agent/authored/f112-r8.md` (between its markers) to an in-memory
string, then Python byte-equality against `.agent/plan.md`: **equal,
2155 bytes both sides.** `wc -l .agent/plan.md` → **46** (< 50, file has
no trailing newline so the 47th line is uncounted by `wc -l`).
`grep -c '^## Goal' .agent/plan.md` → **1**. `grep -c '^## Next Steps'
.agent/plan.md` → **1**. PASS.

**G3 FIX (R-0794)** — BEFORE the fix commit:
`python3 -m pytest tests/orchestration/test_f018_authority_integration.py -q`
→ **1 failed, 113 passed**, failure named exactly
`TestRealJobPlanDecision::test_jobplan_no_metadata_attr_safe`
(`AssertionError: assert not True`) — reproduces the regression exactly
as the block predicted. Reconstructed the file from
`git show e5add7cd...:tests/orchestration/test_f018_authority_integration.py`
applying TEST_FIX_FROM→TEST_FIX_TO (both extracted programmatically,
never retyped) via `content.replace(FROM, TO, 1)`; byte-compared against
the committed post-fix file: **equal, 71587 bytes both sides.** AFTER
the fix commit, same pytest command → **114 passed, 0 failed.**
`ruff check tests/orchestration/test_f018_authority_integration.py`:
bare `ruff` binary denied as a direct Bash invocation (first tier);
fell back to `python3 -m ruff check <path>` (second tier), which
**worked directly this round** (no third-tier `subprocess.run` fallback
needed) → **`All checks passed!`**. PASS.

**G4 LEDGER (RECORD7)** — `.agent/live_review.md` measured **2259008
bytes** immediately before the append, matching the block's pinned
figure exactly (no STOP triggered). RECORD7 extracted from the
committed authored file using the end-marker-without-leading-newline
form (so the trailing `\n` separating the Gate line from the
`<<<END RECORD7>>>` marker is captured as part of RECORD7 itself, not
stripped): **2711 bytes, 0 internal newlines, last byte a newline** —
matches the block's stated shape and pinned length exactly, with no
manual adjustment needed this round. Appended as `content_bytes +
b"\n" + RECORD7_bytes` (ONE newline). Post-size measured at **2261720
bytes**, matching `2259008 + 1 + 2711` exactly. Second reader: split
the whole post-append file on `\n\n`, last unit == RECORD7 exactly
(**True**). Negative control: flipped one byte inside RECORD7's own
text in memory, re-ran the same comparison against the file's actual
last unit — mismatch confirmed (**False**, correctly rejected). PASS.

**G5 STATE READERS AND CANARY** (five separate invocations):
- `python3 -m pytest tests/ui_server/ -q` → **515 passed**
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → **52 passed**
- `python3 -m pytest tests/regression/test_resource_safety.py -q` → **21 passed**
- `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → **16 passed**
- `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42 passed**

All PASS.

**G6 FULL-FEATURE SPOT CHECK** (five separate invocations, every file
this feature has touched across all rounds):
- `python3 -m pytest tests/orchestration/test_class_prompt_budget.py -q` → **24 passed**
- `python3 -m pytest tests/orchestration/test_context_compiler.py -q` → **69 passed**
- `python3 -m pytest tests/orchestration/test_task_granularity.py -q` → **30 passed**
- `python3 -m pytest tests/orchestration/test_job_task_runner.py -q` → **193 passed**
- `python3 -m pytest tests/orchestration/test_f018_authority_integration.py -q` → **114 passed**

All fully green. PASS.

**G7 TREE, COMMITS, SWEEP** — `git status --porcelain` read **empty**
immediately before staging the handback commit. `git ls-files
.remedy-wt` read **empty**. Per-commit `git show --numstat` `+` column,
cross-checked against the Commits table above:
- C0a `7e58b1d4`: `+206/-0` `.agent/authored/f112-r8.md` — matches.
- C0b `0888f593`: `+133/-111` `.agent/last_block.md` — matches.
- C1 `a55e546b`: `+23/-22` `.agent/plan.md` — matches.
- C2 `1e8dfabf`: `+6/-1` `tests/orchestration/test_f018_authority_integration.py` — matches.
- C3 `00b02a4d`: `+2/-0` `.agent/live_review.md` — matches.

All commits well under the 500-line insertion cap (C0a/C0b exempt
regardless, as whole-file `.agent/**` rewrites, DECISION F104 D1).

**Staleness sweep, one line per file this round touched:**
- `.agent/authored/f112-r8.md` — new file this round; nothing prior
  referenced it, so nothing else needed updating.
- `.agent/last_block.md` — whole-file mirror of the authored file every
  round; no other file depends on its prior content.
- `.agent/plan.md` — whole-file replacement every round by design; no
  other file quotes its prior text.
- `tests/orchestration/test_f018_authority_integration.py` — repo-wide
  search (`grep -rln`, scoped to `packages tests docs`) for the retired
  phrase "JobPlan has no" turned up only the two OTHER, unrelated,
  correctly-untouched hits already identified in round 7
  (`decision_inbox.py:74` re `.tasks`, `decision_queue.py:94` re
  `.artifacts`) and no further instance of the "no `.metadata`" claim
  outside `.agent/live_review.md`'s append-only historical record (left
  untouched by design). A second search for the test's own name
  (`test_jobplan_no_metadata_attr_safe`) found it referenced, as
  expected, only inside this file itself, various `.agent/` state files
  (updated as part of this and prior rounds' normal bookkeeping), and
  archival `.agent/Evidence/f018_repro_closure/**` snapshots from a past
  closure evidence bundle — immutable historical artifacts, correctly
  left untouched.
- `.agent/live_review.md` — append-only; the appended RECORD7 text does
  not reference or invalidate any earlier entry's content.

## Authored-text proofs

`.agent/authored/f112-r8.md` (committed at `7e58b1d4`) vs
`.agent/last_block.md` (committed at `0888f593`): byte-identical, 12928
bytes both sides (G1, Python `hashlib.sha256` comparison). PLAN8,
TEST_FIX_FROM/TEST_FIX_TO and RECORD7 were all extracted programmatically
from this committed file (never retyped) and applied via
`content.replace(FROM, TO, 1)` or the stated append formula; every
application was confirmed against before/after occurrence counts or
byte-equality above (G2, G3, G4).

## Deviations & assumptions

1. **The sandboxed shell denied several individual Bash invocations
   mid-round** (bare `ruff` binary; a `for`-loop-shaped multi-command
   Bash call gathering several `git show --numstat` outputs at once;
   two parallel `grep -rn ... .` calls scanning from the repo root; one
   `python3 -c` append-write to `.agent/live_review.md`; one
   `python3 -c` read computing the G4 second-reader/negative-control
   checks) and accepted the identical command on retry, or an
   equivalent single-command / narrower-scoped form, every time (per
   this round's explicit accepted-equivalent guidance). No gate result
   in this handback rests on a denied invocation; every reported number
   comes from a command that actually ran and printed the quoted
   output. `grep -rln` denied at repo-root scope (`.`) succeeded when
   scoped to specific directories (`packages tests docs`) instead —
   consistent with the environment guidance to search from a specific
   path rather than `/` or an unscoped root.
2. **`git commit`'s own inline insertion/deletion summary disagreed
   with `git show --numstat`/`git show --stat` read after the fact**
   for the C0b whole-file rewrite of `.agent/last_block.md` (commit-time
   summary read `206 insertions(+), 184 deletions(-)`; `git show
   --numstat` and `git show --stat` both read `133 insertions(+), 111
   deletions(-)` post-commit) — same class round 7 declared for its own
   C0b. The Commits table and G7 cross-check above both use the `git
   show --numstat` reading throughout, per the block's own G7 wording.
3. **RECORD7's extraction needed no manual trailing-newline adjustment
   this round**, unlike round 7's RECORD6 (which needed one `\n`
   appended after extraction to reach its pinned byte count): matching
   the end marker WITHOUT a leading `\n` (i.e. `b"<<<END RECORD7>>>"`
   rather than `b"\n<<<END RECORD7>>>"`) captured the block's own
   trailing newline as part of RECORD7 directly, landing on the pinned
   2711-byte figure on the first attempt. Declared for transparency,
   since the two rounds' extraction code differs in this one respect
   and a future round should not assume either form is uniformly
   correct — it depends on whether the block's own trailing newline
   before its END marker is meant to belong to the extracted slice.
4. **`ruff` fell back only one tier this round** (bare binary denied,
   `python3 -m ruff check <path>` worked directly), unlike round 7 where
   both the first two tiers were denied and the third
   (`subprocess.run(...)` inside `python3 -c`) was needed. Declared
   since the block anticipated all three tiers as possibly necessary;
   this round only needed two.
5. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Next

**T003b** — derive a `task_class` for a live `TaskEntry`, wire
`compiled_context_paths`/`compiled_context_candidates` into
`pingpong_job.py`'s `run_pingpong(...)` call, then call
`fit_task_context_to_class_cap` and `enqueue_task_decision` between
`_build_task_prompt` and `task.status = TASK_RUNNING` in the per-task
loop — per `.agent/plan.md` Next Steps and DECISION F112 D1. No open
findings are owed going into this step: R-0794 was registered and
resolved within this same round, and the branch tip is fully green
across every suite this feature has touched (G5/G6 above).

**Strong recommendation: end this session here and start T003b in a NEW
session.** This is round 8 of session 2 — inside the 4-5-round-per-
session default but on the higher side for one session, and T003b
itself demands a "fresh investigation first" per its own plan.md entry
and DECISION F112 D1, which a session boundary serves better than a
9th round tacked onto this one. Before either continuing or ending:
Phase 1 rule 1 — re-check `.agent/STOP` from disk before authoring the
next round (not present as of this round).
