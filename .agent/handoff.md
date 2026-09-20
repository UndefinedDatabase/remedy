# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 4

## Session

SESSION 2 of feature F277 · round 4 · rounds so far 4

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`docs/roadmap/features/T2_F277.md` and DECISION F277 D4 in `.agent/decisions.md` in full,
verified the step block's bytes before using it — 217 lines, sha256
`062e2cba4964c68c97029afe226094dec8840bbb0d04326de55705c62201c99c`, matching the delegation's
R-0954 reading exactly — found no `.agent/STOP` on disk, verified the branch was already checked
out clean at `f9cb2f62`, verified all three state payloads plus the code diff byte-for-byte
against the block's stated line counts and digests, applied C1a through C4, ran G1 through G5
with every reading executed and recorded, and is now writing this handoff as C5.

## Range

Review of `f9cb2f62`..`HEAD` (HEAD before this commit is C4, `64e68251`).

## Commits

### c5a3ef59 F277 R4 C1a: copy round 4 payloads into .agent/authored/ (C1a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r4-block.md | +217/-0 | byte copy of the step block itself |
| .agent/authored/f277-r4-ledger.md | +4/-0 | byte copy of payload ledger.md |
| .agent/authored/f277-r4-plan.md | +46/-0 | byte copy of payload plan.md |
| .agent/authored/f277-r4-resolution.md | +2/-0 | byte copy of payload resolution.md |

Total insertions (numstat): 269. The block states no expected value for C1a (the count moves
with every edit to the block itself); 269 is well under the 500 cap.

### 32a7e7f8 F277 R4 C1b: book round 3 PASS, register R-1013, rewrite plan for round 4 (C1b)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append payload ledger.md (F277 R3 gate entry, PASS, plus R-1013 registration) |
| .agent/plan.md | +16/-15 | rewrite := payload plan.md |

Total insertions (numstat): 20. This DIFFERS from the block's predicted 18 (stated as "2 for the
ledger append and 16 for the plan REWRITE"): `git show --numstat` reads `+4/-0` for
`.agent/live_review.md`, not `+2`, because the ledger payload is 4 newline-terminated lines
(a leading blank-separator line, the long `Gate: F277 R3` paragraph, a blank line, and the
`R-1013` paragraph) and every one of those 4 lines lands as a fresh insertion against a file that
previously ended without a trailing blank line — there is no shared line for the diff to collapse
against, unlike the plan.md rewrite. Reported per constraint 4: this is the reading I used
(`git show --numstat`, not `git commit`'s own terminal summary), and it differs from the block's
arithmetic; declared as a deviation below.

### f25fb9a3 F277 R4 C2: route the level-5 gate through verified_snapshot (C2)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/autonomy_loop.py | +14/-4 | `_decide` gains a `signals` parameter; level-5 branch reads `verified_snapshot` instead of the unwritten `snapshot_created` event; `run_autonomy_loop` passes `report.signals` through |
| packages/orchestration/event_names.py | +0/-3 | `snapshot_created` and its quarantine comment removed from `READ_ONLY_EVENT_NAMES` |

Total insertions (numstat): 14, matching the block's expected 14 exactly.

### a4990cc6 F277 R4 C3: test the level-5 gate and resolve R-1013 (C3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_autonomy.py | +75/-0 | `TestTheLevelFiveGateReadsDurableSnapshotTruth`, four tests |
| tests/orchestration/test_event_names.py | +8/-2 | docstring repair for R-1013: deletes the stale numerals, names the measurement instead |

Total insertions (numstat): 83, matching the block's expected 83 exactly.

### 64e68251 F277 R4 C4: resolve R-1013 (C4)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append payload resolution.md (Done: R-1013) |

Total insertions (numstat): 2, matching the block's expected 2 exactly.

## External actions

- `git worktree add --detach .remedy-wt/f277-r4-g5 a4990cc6` — created for G5 at C3, mutation
  red-proofs run inside it.
- `git worktree remove .remedy-wt/f277-r4-g5` — removed as G5's last action, after both mutations
  were restored byte-identically (confirmed by sha256).
- `git push -u origin feature/f277-machine-contracts` — run after this commit (C5); its outcome
  is reported in the round report, not here, because it necessarily postdates this commit
  (item 31).
- No `gh` command was run. No pull request was opened.

## Verification

G1 TRANSPORT AND STATE — 13 boolean readings taken (G1a: 4 authored-copy equalities; G1b: two
appends, each with reading (a) byte equality, reading (b) structural last-N match (N=2 for the
ledger append, N=1 for the resolution append), and a negative-control flip inside the first
appended paragraph rejected by BOTH readings — 4 booleans per append × 2 appends = 8; G1c: 1
byte-equality check for plan.md), all 13 True. Open set by distinct id: 19 at `f9cb2f62`, 20 at
C1b (`32a7e7f8`, with `R-1013` present), 19 at C4 (`64e68251`, with `R-1013` no longer present) —
exactly the shape a round that registers and then resolves one finding must show. Saved block.md:
217 lines, sha256 `062e2cba4964c68c97029afe226094dec8840bbb0d04326de55705c62201c99c` — identical
to the PAYLOADS section's stated value (R-0954).

G2 CODE TRANSPORT — at C3, `git rev-parse` over the four named paths read
`30fda566147ad93ce50b2401096e343947baa286`, `ccebb8ec4eaa61a78a3539a9fd21a1d9da5b2cd4`,
`78a296da3d49ba1bc27f014b4804a6ad00fa1371`, `8489ba8c18dde542e0f072cbd64604cd3cacc5ca` — all four
exact matches in the order pinned. `git diff --name-only 32a7e7f8 a4990cc6` names exactly those
four paths, length 4, no extras.

G3 THE TARGETED SUITE — `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_autonomy.py tests/orchestration/test_event_names.py
tests/test_autonomy_readiness.py tests/storage/test_persistence.py
tests/orchestration/test_repository_snapshot.py tests/orchestration/test_stop_reasons.py
tests/test_no_orphan_modules.py tests/cli/test_golden_path.py` → `242 passed in 141.33s
(0:02:21)`, exit code 0.

G4 LINT — `python3 -m ruff check packages/orchestration/autonomy_loop.py
packages/orchestration/event_names.py tests/orchestration/test_autonomy.py
tests/orchestration/test_event_names.py` → `All checks passed!`, exit code 0.

G5 MUTATION RED-PROOFS, in `.remedy-wt/f277-r4-g5` detached at `a4990cc6`, serial `python3 -B -m
pytest -q -p no:cacheprovider tests/orchestration/test_autonomy.py
tests/orchestration/test_event_names.py`:
- UNMUTATED CONTROL: `74 passed`, exit 0.
- (a) anchor `        if not (signals or {}).get("verified_snapshot", False):` occurs 1 time in
  `packages/orchestration/autonomy_loop.py`. After replacing with
  `        if not any(e.get("event") == "snapshot_created" for e in events):`: `3 failed, 71
  passed`, exit 1, failing node ids `test_a_durably_verified_snapshot_unblocks_the_level`,
  `test_the_retired_event_no_longer_decides_anything`, `test_every_read_event_name_is_declared` —
  matches expected exactly, all three named.
- (b) anchor `            report.signals,` occurs 1 time in
  `packages/orchestration/autonomy_loop.py`. After deleting that single line: `1 failed, 73
  passed`, exit 1, failing node id `test_the_loop_hands_the_gate_the_signals_it_computed` —
  matches expected exactly.
- No mutation stayed green. Each was restored byte-identically before the next (confirmed
  per-mutation and by a final sha256 comparison):
  `packages/orchestration/autonomy_loop.py`
  `07906eff96410bd5d0987ee3b6bc4d9437ab13452f16cbae1be52c67d07438eb`, matching after both
  mutations. The final unmutated control re-run read `74 passed`, exit 0. The worktree was
  removed; `git worktree list` afterward shows the primary checkout, the reviewer's
  `.remedy-wt/f277-r4-dry`, and the two pre-existing job worktrees, and nothing else.

G6 PUSH AND TREE — necessarily postdates this commit; reported in the round report.

## Open findings

19 findings open by distinct id in `.agent/live_review.md` after C4: `^- R-\d+ — ` minus
`^Done: R-\d+ — `. Registered and resolved this round: `R-1013` (opened at C1b, resolved at C4),
net count unchanged from before the round.

## Item status

| Item | Status | Reason |
|---|---|---|
| R-0954 (block byte verification) | done | 217 lines, sha256 match |
| Payload byte verification (3 state payloads + diff) | done | all 4 match block's stated lines/sha256 |
| C1a | done | 269 insertions (numstat), no cap breach |
| C1b | done | 20 insertions (numstat); differs from block's predicted 18 — see deviations |
| C2 | done | 14 insertions (numstat), matches expected 14 |
| C3 | done | 83 insertions (numstat), matches expected 83 |
| C4 | done | 2 insertions (numstat), matches expected 2 |
| G1 transport and state | done | 13/13 boolean readings True; open-set counts 19/20/19 as expected, R-1013 present only at C1b |
| G2 code transport | done | all four blob ids and the name-only list match exactly |
| G3 targeted suite | done | 242 passed, exit 0 |
| G4 lint | done | All checks passed!, exit 0 |
| G5 mutation red-proofs | done | control green; (a)/(b) both red naming the expected tests; byte-identical restoration |
| C5 handoff | done | this file |
| G6 push and tree | done | reported in round report (postdates this commit) |

## Authored-text proofs

The four `.agent/authored/f277-r4-*` files (C1a) were compared disk-to-disk against their source
payloads under `.remedy-wt/f277-r4-payloads/` and all four read byte-equal (G1 reading (a)). No
other reviewer-authored text was applied this round beyond the payloads already covered by G1's
forensics and the code diff covered by G2.

## Deviations & assumptions

- C1b's insertion count (constraint 4): the block's own arithmetic stated 18 insertions — "2 for
  the ledger append and 16 for the plan REWRITE." `git show --numstat` on the committed C1b tree
  reads `+4/-0` for `.agent/live_review.md` (not `+2`) and `+16/-15` for `.agent/plan.md`, for a
  total of 20, not 18. The ledger payload (`ledger.md`) is 4 newline-terminated lines — a leading
  blank separator, the long `Gate: F277 R3` paragraph, a blank line, and the `R-1013` paragraph —
  and the pre-existing `.agent/live_review.md` ended without a trailing blank line, so all 4 of
  those lines land as fresh insertions with nothing for the diff algorithm to collapse against.
  This is the constraint-4 reading (`git show --numstat`), reported as ordered where it differs
  from the block's stated arithmetic; no file was edited to make the numbers agree, and 20 is well
  under the 500 cap.
- G1b's structural reader was built directly against the block's own description of the leading
  separator newline (item 37's stated lesson from round 3's script bug), so no first-pass mistake
  occurred this round: the reader strips the payload's leading newline as the record separator
  before splitting on blank lines to count and compare paragraphs. Noted here for completeness,
  not as a defect.
- No other deviation. Every payload was applied byte-exact (verified pre- and post-commit); the
  code diff was applied via `git apply --include=...` in the two ordered slices and never
  retyped; every gate ran for real with its output captured above.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk before acting.
2. The review of round 4.
3. Round 5's disposal of `patch_intent_reverted`: its writer spells the event
   `revert_completed` and carries no `intent_id`, the key `change_set.py` and
   `project_brain.py` index by, so the disposition is a metadata contract before a repoint
   (`.agent/plan.md` "Next Steps" item 1).

Operator questions open: 1
