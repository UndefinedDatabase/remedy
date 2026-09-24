# Handback — F264 Steering channel · Round 7 · THE COCKPIT'S ACTIVITY FEED SHOWS EACH STEERING ACKNOWLEDGEMENT

## Session

SESSION 1 of feature F264 · round 7 · rounds so far 7

This round booked round 6's PASS into `.agent/live_review.md`, recorded
DECISION F264 D7, and landed T003's second half: a new pure module
`apps/ui/src/api/steeringAck.ts` reads the stream's `steering` field on a
`steering_message_consumed` frame, checking every value, and
`feedRowOf` shows that row as "Steering taken in at round <n>:
<restatement>." in the activity feed directly above the steering input.
A Python guard pins the reader's keys and event kind to the server's
stream field. With this round T001 to T003 are built.
A large majority of this session's working-context budget remained at
handback.

## Range

Review of e420be13..87b0ea1f

## Commits

### 13319f60 F264 R7 C1a: copy round 7 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r7-block.md | +229/-0 | copy of this round's block, verbatim |
| .agent/authored/f264-r7-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f264-r7-records.diff | +44/-0 | copy of the records.diff payload |

### 09bcab4c F264 R7 C1b: copy round 7 product and test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r7-mutations.py | +81/-0 | copy of the mutations.py payload |
| .agent/authored/f264-r7-product.diff | +29/-0 | copy of the product.diff payload |
| .agent/authored/f264-r7-steeringAck.test.ts | +41/-0 | copy of the steeringAck.test.ts payload |
| .agent/authored/f264-r7-steeringAck.ts | +50/-0 | copy of the steeringAck.ts payload |
| .agent/authored/f264-r7-tests.diff | +50/-0 | copy of the tests.diff payload |

### 41bc6c4f F264 R7 C2: book round 6's PASS, record DECISION F264 D7 and advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +26/-0 | DECISION F264 D7 |
| .agent/live_review.md | +2/-0 | `Gate: F264 R6 —` PASS entry |
| .agent/plan.md | +11/-8 | rewritten to plan.md payload, advancing to T003's second half |

### a23e3d93 F264 R7 C3: show each steering acknowledgement in the cockpit's activity feed
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/feedRow.ts | +6/-1 | `feedRowOf` renders the acknowledgement row: "Steering taken in at round <n>: <restatement>." directly above the steering input |
| apps/ui/src/api/steeringAck.ts | +50/-0 | new pure module reading the stream's `steering` field on a `steering_message_consumed` frame, checking every value |

### 87b0ea1f F264 R7 C4: test the acknowledgement reader, the feed line and the stream pin
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/feedRow.test.ts | +22/-0 | acknowledgement row rendering, incl. catalog line retained |
| apps/ui/src/api/steeringAck.test.ts | +41/-0 | reader tests: every value checked, round-left-unchecked and wrong-kind rejected |
| tests/ui_contracts/test_steering_send_contract.py | +12/-0 | Python guard pinning the reader's keys and event kind to the server's stream field |

## External actions

- `git worktree add --detach .remedy-wt/f264-r7-mut 87b0ea1f` — succeeded, real exit 0
- `git worktree remove --force .remedy-wt/f264-r7-mut` — succeeded, real exit 0
- `git worktree prune` — succeeded, real exit 0
- `git push origin feature/f264-steering-channel` — reported in the reply (run after this commit; cannot be in this table per the self-reference exception)

No PR created or merged this round (per block constraint 5). `gh pr list` reported in the reply.

## Verification

G1 TRANSPORT — all 7 payloads (records.diff, plan.md, product.diff,
steeringAck.ts, mutations.py, tests.diff, steeringAck.test.ts) measured
line count, byte count and sha256 against the PAYLOADS table: all
matched exactly. All 8 `.agent/authored/f264-r7-*` copies (block + 7
payloads) read back with `git show <commit>:<path>` matched their
sources byte for byte.

G2 THE RECORDS — at C2 (41bc6c4f): `git show 41bc6c4f:.agent/live_review.md`
= 322329 bytes, sha256 5cb85dd31b1011c14bbe2eefc562ae9dad08e677e0d7b04c8ce2c854d25ee075
(match); `.agent/decisions.md` = 1955579 bytes, sha256
0d33643528359dc3417f5a77548e5d9356fbee0aa938ddd35b8a54f730004b4e (match);
`.agent/plan.md` = 1118 bytes, sha256
a16f75fcefaaaaffc52222695f4794ad923ac2b1ced0b8dc68036adcb11d39f3 (match).
Lines added to live_review.md beginning `Gate: F264 R6 — `: 1 (matches
reviewer's reading of 1). `open_finding_ids` (scripts/rotate_live_review.py)
at e420be13 and at 41bc6c4f: both `{R-0499, R-0950, R-1008}`, set
difference empty both directions (matches reviewer's 3 and 3).
`git diff --name-only 09bcab4c 41bc6c4f`: `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md` — exactly the three record
paths.

G3 THE PRODUCT — at C4 (87b0ea1f), all five files read back with
`git show 87b0ea1f:<path>` matched the reviewer's simulated readings
byte for byte: `apps/ui/src/api/steeringAck.ts` (2431 bytes),
`apps/ui/src/api/feedRow.ts` (3281 bytes),
`apps/ui/src/api/steeringAck.test.ts` (1829 bytes),
`apps/ui/src/api/feedRow.test.ts` (3962 bytes),
`tests/ui_contracts/test_steering_send_contract.py` (3531 bytes) — all
sha256 matched. `git diff --name-only 41bc6c4f a23e3d93`: feedRow.ts,
steeringAck.ts (matches C3's two paths). `git diff --name-only a23e3d93
87b0ea1f`: feedRow.test.ts, steeringAck.test.ts,
test_steering_send_contract.py (matches C4's three paths).

G4 THE TESTS — serial pytest run (real exit code):
```
1104 passed, 4 skipped in 81.65s (0:01:21)
REAL_EXIT=0
```
SKIPPED lines (all four, pre-existing D3 quarantine skips, none of them
the four toolchain nodes this round required to pass):
```
tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252)
tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252)
tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252)
tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252)
```
The reviewer's sim (without `tests/cli/test_golden_path.py`, serially in
its own worktree) read `1057 passed, 9 skipped` at exit 0. This primary
checkout carries the UI toolchain a worktree lacks and also ran the
golden path the sim selection excluded; the required four toolchain
nodes — the two `test_ui_lint.py` eslint nodes, the `test_dashboard_contract.py`
typescript node, and the `test_test_runner.py` vitest node — all PASSED
here (none appear in the SKIPPED summary above).
```
python3 -m ruff check tests/ui_contracts/test_steering_send_contract.py
All checks passed!
REAL_EXIT=0
```
```
python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [...all "pass"...], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```

G5 THE RED PROOFS — `.remedy-wt/f264-r7-payloads/mutations.py` against
`.remedy-wt/f264-r7-mut` (detached at 87b0ea1f):
```
control_before: vitest 15 passed, REAL_EXIT=0; pytest 6 passed, REAL_EXIT=0
u1_feed_keeps_the_catalog_line: FROM count 1; vitest 1 failed, 14 passed, REAL_EXIT=1; pytest 6 passed, REAL_EXIT=0; restored byte-identical: True
u2_round_left_unchecked: FROM count 1; vitest 1 failed, 14 passed, REAL_EXIT=1; pytest 6 passed, REAL_EXIT=0; restored byte-identical: True
u3_any_kind_read_as_an_ack: FROM count 1; vitest 1 failed, 14 passed, REAL_EXIT=1; pytest 6 passed, REAL_EXIT=0; restored byte-identical: True
u4_restatement_dropped_from_the_line: FROM count 1; vitest 2 failed, 13 passed, REAL_EXIT=1; pytest 6 passed, REAL_EXIT=0; restored byte-identical: True
p1_reader_key_drifts_from_the_stream: FROM count 1; vitest 2 failed, 13 passed, REAL_EXIT=1; pytest 1 failed, 5 passed, REAL_EXIT=1; restored byte-identical: True
control_after: vitest 15 passed, REAL_EXIT=0; pytest 6 passed, REAL_EXIT=0
```
Exact match to the reviewer's expected readings for all seven mutation
lines. Worktree removed and pruned; `git worktree list` afterward showed
only the primary checkout, the reviewer's `f264-r7-dry`/`f264-r7-sim`,
and the four `job-*` worktrees — nothing else.

## Authored-text proofs

Block (`.agent/authored/f264-r7-block.md`), records.diff, plan.md,
product.diff, steeringAck.ts, mutations.py, tests.diff and
steeringAck.test.ts copies at 13319f60/09bcab4c: each read back with
`git show <commit>:<path>` and compared against the payload table /
this block's own reading — all 8 matched byte for byte. records.diff,
product.diff and tests.diff were applied with `git apply` (never
retyped), each preceded by a real `git apply --check` at exit 0 and
followed by the real `git apply` at exit 0. plan.md, steeringAck.ts and
steeringAck.test.ts were copied whole with `shutil.copyfile`, never
retyped.

## Deviations & assumptions

None. The bundle ran in the block's declared order (C1a, C1b, C2, C3,
C4, C5) with no extra, dropped or reordered commits.

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 7.
Then the closure sequence's first half — the user-facing docs for
`remedy chat`, the feature file's Built State, the checklist
consolidation, the self-use track and the feature's one full suite.
Open findings: 3. Operator questions: 0.
