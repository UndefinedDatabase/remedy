# Handoff — F288, round 4

## Session

SESSION 1 of feature F288 · round 4 · rounds so far 4. Context remaining at
handback: comfortable — the round's derivations (recording replay, phase
math, geometry fractions) and the probe-tool correction used a moderate
share of the session's budget; a full context window remains for the next
round.

## Range

Review of `55820841`..`HEAD` (`HEAD` is this handback's own commit, `F288 R4
C4`, on `feature/f288-event-stream-completeness`).

## Commits

### 7fd023ce9 F288 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r4-block.md | 191/0 | copy of this round's block |
| .agent/authored/f288-r4-plan.md | 29/0 | copy of the plan payload |
| .agent/authored/f288-r4-records.diff | 54/0 | copy of the records payload |

Measured insertions: 274 (block's own line count 191 + 83), matching the
block's expectation exactly.

### 2c4928452 F288 R4 C2: book round 3's FAIL, record D4 and the round 4 plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 27/0 | DECISION F288 D4 |
| .agent/live_review.md | 2/0 | round 3's Gate entry (VERDICT FAIL) |
| .agent/plan.md | 9/16 | round 4's plan (payload rewrite) |
| .agent/prose_slips.md | 1/0 | the dated round-3 prose-slip line |

Matches the block's expected numstat (27/0, 2/0, 9/16, 1/0) exactly.

### 4ab663659 F288 R4 C3: bring the recording's and the row's four vitest readers to the new recording (R-1075, D4)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r4-probes.py | 162/0 | the G5 tool (first version — see Deviations) |
| apps/ui/src/components/graph/brainLedger.test.ts | 20/6 | `eventFields` widened to the row's two new fields; the GAP SCENARIO's hole/page bounds and length brought to the ten-frame recording |
| apps/ui/src/components/graph/renderers/stateMotion.test.ts | 17/11 | task ids and the seq keys of `EXPECTED` brought to the new recording's repair-round shape |
| apps/ui/src/components/timeline/timelineIndex.test.ts | 14/5 | task ids fixed to the recording's own (a mismatch stalled Finalized forever); loop bound, head and phase-stops brought to seq 9 |
| apps/ui/src/components/timeline/timelineView.test.ts | 40/16 | `DEMO_TASKS` ids fixed; all four failing sub-tests' seq/position moved to the new recording's landmark moments, with the geometry re-derived |

No insertion count was expected by the block for C3; measured 253 total (38
deletions).

### bd45f3eed F288 R4 C3b: correct the probe tool's p2 mutation to a deletion, not a [] literal (DEVIATION — see below)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r4-probes.py | 13/4 | p2's mutation changed from hard-coding `planTaskIds: []` (indistinguishable from the untouched code on this plan-approved-free recording) to deleting the assignment outright, leaving the key `undefined` |

### F288 R4 C4: rewrite handoff for round 4 (this commit — a handoff cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f288-r4-smoketest HEAD` (at `2c4928452`,
  before the fix was committed) — succeeded; used to smoke-test the probe
  tool's mechanics before relying on it for the official gate (DEVIATION —
  see below).
- `python3 .remedy-wt/f288-r4-worker/probes.py .remedy-wt/f288-r4-smoketest` —
  real exit 0 (the tool itself ran cleanly; the worktree's pre-fix test
  files were still red, as expected at that commit).
- `git worktree remove --force .remedy-wt/f288-r4-smoketest` then `git
  worktree prune` — succeeded; count returned to 68.
- `git worktree add --detach .remedy-wt/f288-r4-mut 4ab663659` — succeeded
  (the official G5 worktree, at C3).
- `python3 .remedy-wt/f288-r4-worker/probes.py .remedy-wt/f288-r4-mut` — run
  TWICE against this same worktree: once with the first probe tool (p2 did
  not redden anything, real exit 0 overall — a bug in the probe, not the
  round's code; see Deviations), once after C3b's correction (p2 then
  reddened `brainLedger.test.ts`, real exit 1 overall for that probe). No
  round-owned file needed a second look; only the tool changed.
- `git worktree remove --force .remedy-wt/f288-r4-mut` then `git worktree
  prune` — succeeded; count returned to 68.
- `git push -u origin feature/f288-event-stream-completeness` — reported
  under G6 in this round's reply (run after this file is committed).
- No `gh pr create`, no `gh pr merge`, no branch deletion, no force-push, no
  `git stash`, no `git checkout`/`git switch` in the primary checkout.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table):
- `records.diff`: 54 lines, 11102 bytes, sha256
  `8a9b25a2d01a0e10666c20fc38b6a238361c506117d0f9269dcc23eb9bb8eb6a` — MATCH.
- `plan.md`: 29 lines, 1093 bytes, sha256
  `ce0f362c21212ac8b368107cfdbef283f29d741889cfc756e01663c090d975ab` — MATCH.

Each `.agent/authored/f288-r4-*` copy, read back with `git show
7fd023ce9:<path>`, compared byte-for-byte (Python, not `diff`) with its
source — all three identical: block copy vs `.remedy-wt/f288-r4/block.md`;
`records.diff` copy vs `.remedy-wt/f288-r4-payloads/records.diff`;
`plan.md` copy vs `.remedy-wt/f288-r4-payloads/plan.md`.

### G2 — THE BOOKING
`git show 2c4928452:<path>`, bytes and sha256, each MATCHING the reviewer's
reading exactly:
```
.agent/decisions.md    bytes=2236302  8168fa8db604d7a54439ec6c46653648b1d00ee8ed45f757244beff42180a2b5
.agent/live_review.md  bytes=311964   a3fb95d98d72893287da8a8bd25838fccf890c600ebea818c373a693866f5dcf
.agent/prose_slips.md  bytes=372141   1d186a8dd16460555b690b3ac9ba02b5abc0dbd03b78737d213a17793a917493
.agent/plan.md         bytes=1093     ce0f362c21212ac8b368107cfdbef283f29d741889cfc756e01663c090d975ab
```
Open set (`open_finding_ids` from `scripts/rotate_live_review.py` over
`.agent/live_review.md`'s text at `2c4928452`): `['R-1075']` — matches "the
reviewer read `R-1075` alone".

### G3 — THE REPAIR
`git diff 55820841 4ab663659 -- apps/ui/src` reported whole in this round's
reply. Per-test line (what changed, from -> to):
- `brainLedgerPage > reads rows and cursor...` (brainLedger.test.ts):
  `eventFields` dropped `attemptId`/`planTaskIds` -> keeps them, matching
  `row(...)`'s now-6-field shape.
- `THE GAP SCENARIO > holds the prefix... matches the whole model...`
  (brainLedger.test.ts): held rows `slice(5, 8)` / page `cursor: "8"` /
  `toHaveLength(8)` -> `slice(5, 10)` / `cursor: "10"` / `toHaveLength(10)`,
  covering the recording's true ten frames.
- `the demo recording's state changes > animates every state change...`
  (stateMotion.test.ts): task ids `a7a8f67f1b9a4814`/`1965fb3f26b64fe7` and
  EXPECTED keys `{0,3,4,7}` -> the recording's real ids
  `fe1b5b487fda490f`/`4b3ddac9dba846af` and keys `{0,4,5,9}` (the repair
  rounds at seq 1-3/6-8 birth no transition).
- `the index equals the plain fold... > over the demo recording`
  (timelineIndex.test.ts): seeded ids -> the recording's real ids; loop
  bound `s<=8`, `indexHead` 7, `phaseStops` `[0,1,7]` -> `s<=10`, `9`,
  `[0,1,9]`.
- `at the head: every phase done...` (timelineView.test.ts): `demo(7)`/
  `position:7`, glyph offsets `0,1/6,4/6,5/6` at seq `1,2,5,6`, readout
  `"Event 7 of 7 · +1s"` -> `demo(9)`/`position:9`, offsets `0,2/8,5/8,7/8`
  at seq `1,3,6,8`, readout `"Event 9 of 9 · +1s"`.
- `scrubbed to seq 3: Review half filled...` (timelineView.test.ts): title
  and position `3` -> `4` (the moment task_round_repaired's no-marker left
  open), readout `"Event 3 of 7"` -> `"Event 4 of 9"`; fill/glyph shapes
  unchanged (coincide with the old literals).
- `a glyph exactly at the handle counts as reached` (timelineView.test.ts):
  position `2` -> `3` (the new recording's own heal glyph), fill `2/6` ->
  `3/8`.
- `puts the handle at the end of its event's slot...` (timelineView.test.ts):
  probe seqs `6,7` -> `8,9` (last review event, head), fraction at seq 1
  `(4+1/6)/6` -> `(4+1/8)/6` (review's width moved 6 -> 8); `5/6` and `1`
  landmarks unchanged by construction.

### G4 — THE TESTS
```
$ python3 -m pytest -q -p no:cacheprovider -rs <the ordered selection>
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1825 passed, 5 skipped in 108.96s (0:01:48)
REAL_EXIT=0
```
Matches the block's order exactly: 1825 passed (the reviewer's 1824 passed
at `55820841` plus the one node that was failing there,
`test_vitest_passes`, now passing), 5 skipped (the same five), real exit 0.

```
$ (cd apps/ui && node_modules/.bin/vitest run)
Test Files  74 passed | 1 skipped (75)
     Tests  1439 passed | 5 skipped (1444)
REAL_EXIT=0
```
No failure, either file or test. 1439 = the reviewer's 1431 passed at
`55820841` + the 8 this round's repair turned green; 74 = the reviewer's 70
+ the 4 files this round brought back to fully green.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}
```
All six checks `pass`, `fail_count` 0.

### G5 — THE PROBES
Reported whole in this round's reply (both the buggy-p2 run at `4ab663659`
and the corrected run after C3b, against the same worktree). Summary: p1
stayed green (0 failed) both times — read as it comes; none of the four
files asserts a `repair_run`'s own node state or reads `ignored`, so
flipping the seq-2 outcome from `changed` to `unchanged` has no reader
among them. p3 turned all four files red (6 tests). p2, as first written,
stayed green (a bug: hard-coding `planTaskIds: []` is indistinguishable
from the untouched code on a recording with no `plan_approved` frame); C3b
corrected it to delete the assignment outright, after which p2 turned
`brainLedger.test.ts` red (1 test). Every mutation restored byte-identical;
both controls (before and after, run against the corrected tool) read
green.

## Authored-text proofs

- Block copy (`.agent/authored/f288-r4-block.md`, at `7fd023ce9`) vs
  `.remedy-wt/f288-r4/block.md`: byte-identical (Python comparison).
- `records.diff` copy vs `.remedy-wt/f288-r4-payloads/records.diff`:
  byte-identical.
- `plan.md` copy vs `.remedy-wt/f288-r4-payloads/plan.md`: byte-identical.
- `records.diff` applied via `git apply`: `--check` and the real apply both
  exit 0; the payload was never edited or retyped.
- `.agent/plan.md` after the payload rewrite: sha256
  `ce0f362c21212ac8b368107cfdbef283f29d741889cfc756e01663c090d975ab`,
  matching the payload's own reading exactly.
- `.agent/authored/f288-r4-probes.py` at `HEAD` (after C3b) vs
  `.remedy-wt/f288-r4-worker/probes.py` (the file this round actually ran
  for the reported G5 output): byte-identical, sha256
  `3c61811d35dd6d56ba57ead3ee89b1af637caccf2e786dcff7497264b0a412a0` both
  sides.

## Deviations & assumptions

1. **The probe tool's own p2 mutation was wrong on the first attempt, and I
   corrected it in an unordered commit, C3b.** The block requires p2
   ("`feedRowOf` stops setting `planTaskIds`") and p3 to each turn at least
   one of the four files red. My first version hard-coded
   `planTaskIds: []`, which is indistinguishable from the untouched code:
   this recording has no `plan_approved` frame, so `planTaskIdsOf` already
   returns `[]` for every one of its ten rows, and the mutated run (real
   exit 0, 0 failed) proved it. I corrected the mutation to DELETE the
   assignment entirely — leaving the row's `planTaskIds` key `undefined`
   rather than merely empty — which is what "stops setting" means read
   literally, and re-ran G5 against the SAME `.remedy-wt/f288-r4-mut`
   worktree (unaffected, since only the tool changed, not any round-owned
   file); p2 then reddened `brainLedgerPage`'s test (1 failure), matching
   the block's requirement. The correction is committed as C3b, under the
   `.agent/authored/f288-r4-*` path constraint 3 already lists, and reported
   here per constraint 4.
2. **An extra worktree, not the one G5 orders, added and removed before the
   official gate.** Before trusting the probe tool for the official G5
   run, I smoke-tested its mechanics (mutate/restore/parse) in a throwaway
   worktree at the then-tip (`2c4928452`, before the test-file fixes were
   committed), then removed it and pruned. `git worktree list | wc -l` read
   68 before, during cleanup, and after — the same as step 4's reading —
   and `git status --porcelain` was empty throughout. No round-owned file
   was touched inside it.
3. Every other reading in this handback is real and measured, not expected.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 4 with
R-1075's resolution, then T003 — the prompt node kind, its look, and its
mouse and keyboard reach. Open findings: 1 (R-1075, landed and awaiting the
reviewer's `Done:`). Operator questions: 0.
