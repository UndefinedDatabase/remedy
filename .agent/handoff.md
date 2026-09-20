# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 3

## Session

SESSION 2 of feature F277 · round 3 · rounds so far 3

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`docs/roadmap/features/T2_F277.md` and DECISION F277 D4 in `.agent/decisions.md` in full,
verified the step block's bytes before using it — 212 lines, sha256
`b2fe155dd69657ce441a0772e0ed2fc474245bc39bcbe13770d913411a37e8dc`, matching the delegation's
R-0954 reading exactly — found no `.agent/STOP` on disk, verified the branch was already
checked out clean at `69b7c729`, verified all three state payloads plus the code diff
byte-for-byte against the block's stated line counts and digests, applied C1a through C3, ran
G1 through G5 with every reading executed and recorded, and is now writing this handoff as C4.

## Range

Review of `69b7c729`..`HEAD` (HEAD before this commit is C3, `18079105`).

## Commits

### e259f4db F277 R3 C1a: copy round 3 payloads into .agent/authored/ (C1a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r3-block.md | +212/-0 | byte copy of the step block itself |
| .agent/authored/f277-r3-ledger.md | +2/-0 | byte copy of payload ledger.md |
| .agent/authored/f277-r3-plan.md | +45/-0 | byte copy of payload plan.md |
| .agent/authored/f277-r3-prose_slips.md | +1/-0 | byte copy of payload prose_slips.md |

Total insertions (numstat): 260. The block states no expected value for C1a (the count moves
with every edit to the block itself); 260 is well under the 500 cap.

### 0cc97a66 F277 R3 C1b: book round 2 PASS and rewrite plan for round 3 (C1b)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append payload ledger.md (F277 R2 gate entry, PASS) |
| .agent/plan.md | +20/-22 | rewrite := payload plan.md |
| .agent/prose_slips.md | +1/-0 | append payload prose_slips.md |

Total insertions (numstat): 23, matching the block's expected 23 exactly (2 for the ledger
append, 1 for the prose-slip line, 20 for the plan REWRITE's own numstat, not the payload's 45
lines, because the new plan and the one it replaces share lines). NOTE: `git commit`'s own
terminal summary for this commit read "48 insertions(+), 47 deletions(-)" because it applies
rename detection across the `.agent/plan.md` rewrite; constraint 4 states that summary is NOT
the reading to use. `git show --numstat` on the committed tree reads 20/22 for `.agent/plan.md`
and totals 23 insertions across the three paths, which is reported here.

### 1a26ed8b F277 R3 C2: give command_discovery_completed a writer (C2)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/test_cmds.py | +23/-0 | `_cmd_discover_commands` now emits `command_discovery_completed` via `append_run_event`, non-fatal on `OSError` |
| packages/orchestration/event_names.py | +1/-3 | `command_discovery_completed` moves from `READ_ONLY_EVENT_NAMES` into `EVENT_NAMES`; its quarantine comment is removed |

Total insertions (numstat): 24, matching the block's expected 24 exactly.

### 18079105 F277 R3 C3: add tests for the command_discovery_completed writer (C3)
| Path | +/- | Reason |
|---|---|---|
| tests/test_command_discovery.py | +79/-0 | `TestDiscoveryRecordsItselfInTheRunLedger`, four tests |

Total insertions (numstat): 79, matching the block's expected 79 exactly.

## External actions

- `git worktree add .remedy-wt/f277-r3-g5 HEAD --detach` — created for G5 at C3 (HEAD was
  `18079105`), mutation red-proofs run inside it.
- `git worktree remove .remedy-wt/f277-r3-g5` — removed as G5's last action, after both
  mutations were restored byte-identically (confirmed by sha256).
- `git push -u origin feature/f277-machine-contracts` — run after this commit (C4); its outcome
  is reported in the round report, not here, because it necessarily postdates this commit
  (item 31).
- No `gh` command was run. No pull request was opened.

## Verification

G1 TRANSPORT AND STATE — 10 boolean readings taken (G1a: 4 authored-copy equalities; G1b:
reading (a) byte equality, reading (b) structural last-N=1 match, two negative-control
rejections; G1c: 2 byte-equality checks for plan.md and prose_slips.md), all True. Open set by
distinct id: 19 at `69b7c729` and 19 at C1b (`0cc97a66`) — equal, as expected since this round
registers and resolves nothing. Saved block.md: 212 lines, sha256
`b2fe155dd69657ce441a0772e0ed2fc474245bc39bcbe13770d913411a37e8dc` — identical to the PAYLOADS
section's stated value (R-0954).

G2 CODE TRANSPORT — at C3, `git rev-parse` over the three named paths read
`b0f66911245a5708a679bc6d970e26a59788c749`, `b82893659bfc8ca12cabb93ffebbbec60d41a2ec`,
`4c1ef7d37ceddf3649799f05f0ec4fa68079af91` — all three exact matches in the order pinned.
`git diff --name-only 0cc97a66 18079105` names exactly those three paths, length 3, no extras.

G3 THE TARGETED SUITE — `python3 -m pytest -q -p no:cacheprovider
tests/test_command_discovery.py tests/orchestration/test_event_names.py
tests/test_autonomy_readiness.py tests/test_memory_learn.py tests/test_grouped_cli.py
tests/test_command_catalog.py tests/cli/test_test_run_runtime.py
tests/orchestration/test_test_execution_service.py tests/orchestration/test_command_discovery.py
tests/cli/test_golden_path.py` → `643 passed in 185.58s`, exit code 0.

G4 LINT — `python3 -m ruff check apps/cli/commands/test_cmds.py
packages/orchestration/event_names.py tests/test_command_discovery.py` → `All checks passed!`,
exit code 0.

G5 MUTATION RED-PROOFS, in `.remedy-wt/f277-r3-g5` detached at `18079105`, serial `python3 -B -m
pytest -q -p no:cacheprovider tests/test_command_discovery.py tests/orchestration/test_event_names.py`:
- UNMUTATED CONTROL: `108 passed`, exit 0.
- (a) anchor `            event="command_discovery_completed",` occurs 1 time in
  `apps/cli/commands/test_cmds.py`. After replacing with `            event="agent_loop_inspected",`:
  `4 failed, 104 passed`, exit 1, failing node ids
  `test_the_event_carries_the_keys_memory_learn_reads`, `test_the_json_mode_records_the_same_fact`,
  `test_the_readiness_signal_is_now_reachable`, `test_memory_learn_stores_the_two_entries` —
  matches expected exactly, all four named.
- (b) two edits in `packages/orchestration/event_names.py`, applied as one mutation: the line
  `        "command_discovery_completed",` (deletion anchor, 1 occurrence) and the comment line
  `        # Read by \`autonomy_loop.py\`; the writer spells it` (insertion anchor, 1 occurrence).
  After deleting the first and inserting it above the second: `2 failed, 106 passed`, exit 1,
  failing node ids `test_every_written_event_name_is_declared`,
  `test_a_read_only_name_that_gains_a_writer_leaves_the_quarantine` — matches expected exactly.
- No mutation stayed green. Each was restored byte-identically before the next (confirmed
  per-mutation and by a final sha256 comparison): `apps/cli/commands/test_cmds.py`
  `6b645a50a649f79c02c95ac14d152e331950743df4dc4561956398d83ddb5fc1`,
  `packages/orchestration/event_names.py`
  `b9f564524a6d81d7c19ac319fb398499a0450def793804b25252f212355316c1`, both matching their
  pre-mutation originals. The final unmutated control re-run read `108 passed`, exit 0. The
  worktree was removed; `git worktree list` afterward shows the primary checkout, the reviewer's
  `.remedy-wt/f277-r3-dry`, and the two pre-existing job worktrees, and nothing else.

G6 PUSH AND TREE — necessarily postdates this commit; reported in the round report.

## Open findings

19 findings open by distinct id in `.agent/live_review.md` after C3: `^- R-\d+ — ` minus
`^Done: R-\d+ — `, same count as before the round (this round registers and resolves nothing).

## Item status

| Item | Status | Reason |
|---|---|---|
| R-0954 (block byte verification) | done | 212 lines, sha256 match |
| Payload byte verification (3 state payloads + diff) | done | all 4 match block's stated lines/sha256 |
| C1a | done | 260 insertions (numstat), no cap breach |
| C1b | done | 23 insertions (numstat), matches expected 23; `git commit`'s own summary (48/47) differs due to rename detection, not the constraint-4 reading |
| C2 | done | 24 insertions (numstat), matches expected 24 |
| C3 | done | 79 insertions (numstat), matches expected 79 |
| G1 transport and state | done | 10/10 boolean readings True; open-set counts 19/19 equal as expected |
| G2 code transport | done | all three blob ids and the name-only list match exactly |
| G3 targeted suite | done | 643 passed, exit 0 |
| G4 lint | done | All checks passed!, exit 0 |
| G5 mutation red-proofs | done | control green; (a)/(b) both red naming the expected tests; byte-identical restoration |
| C4 handoff | done | this file |
| G6 push and tree | done | reported in round report (postdates this commit) |

## Authored-text proofs

The four `.agent/authored/f277-r3-*` files (C1a) were compared disk-to-disk against their source
payloads under `.remedy-wt/f277-r3-payloads/` and all four read byte-equal (G1 reading (a)). No
other reviewer-authored text was applied this round beyond the payloads already covered by G1's
forensics and the code diff covered by G2.

## Deviations & assumptions

- G1b's structural reading (item's own script): the payload `ledger.md` begins with a newline
  that the block's prose identifies as "the blank separator its target uses between entries." A
  first pass at the structural paragraph-split reader treated that leading newline as part of the
  payload's own paragraph content rather than as the separator, which made the last-N comparison
  read False even though the byte-equality reading (a) and the negative control both behaved
  correctly. The reader was corrected to strip the payload's leading separator newline before
  counting and comparing paragraphs, consistent with the block's own description of that byte;
  no file on disk was affected by this — it was a bug in the verification script, not in any
  committed content, and is noted here rather than in G1's reported result because the corrected
  reading is what is reported above.
- No other deviation. Every payload was applied byte-exact (verified pre- and post-commit); the
  code diff was applied via `git apply --include=...` in the two ordered slices and never
  retyped; every gate ran for real with its output captured above.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk before acting.
2. The review of round 3.
3. Round 4: dispose of `snapshot_created` (the `autonomy_loop` level-5 gate, routed through
   `build_snapshot_truth` rather than renamed) and the remainder of `patch_intent_reverted`,
   per DECISION F277 D4's "what the remaining rounds take."

Operator questions open: 1
