# Handback — F264 Steering channel · Round 6 · THE ACKNOWLEDGEMENT, ON THE STREAM AND IN `remedy chat show`

## Session

SESSION 1 of feature F264 · round 6 · rounds so far 6

This round booked round 5's PASS into `.agent/live_review.md`, recorded
DECISION F264 D6, and landed T003's first half: the consumption event
becomes the acknowledgement, carrying `understood` — a restatement that
quotes the message verbatim with the task round it took effect from,
and for a mission's job also the contract criterion and mission round.
The SSE stream carries exactly that on that event kind alone, and
`remedy chat show <job_id>` lists every message as acknowledged, waiting
or not taken in, read from the same run-log events the stream carries.
A large majority of this session's working-context budget remained at
handback.

## Range

Review of 70664b29..0c57bc87

## Commits

### dddc2268 F264 R6 C1a: copy round 6 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r6-block.md | +222/-0 | copy of this round's block, verbatim |
| .agent/authored/f264-r6-plan.md | +28/-0 | copy of the plan.md payload |
| .agent/authored/f264-r6-records.diff | +49/-0 | copy of the records.diff payload |

### ac89b98d F264 R6 C1b: copy round 6 product and test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r6-mutations.py | +71/-0 | copy of the mutations.py payload |
| .agent/authored/f264-r6-product.diff | +287/-0 | copy of the product.diff payload |
| .agent/authored/f264-r6-tests.diff | +119/-0 | copy of the tests.diff payload |

### e340f38b F264 R6 C2: book round 5's PASS, record DECISION F264 D6 and advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +31/-0 | DECISION F264 D6 |
| .agent/live_review.md | +2/-0 | `Gate: F264 R5 —` PASS entry |
| .agent/plan.md | +7/-9 | rewritten to plan.md payload, advancing to T003's first half |

### 4e27aeda F264 R6 C3: acknowledge a steering message with its restatement and round
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +15/-0 | catalog entry for the acknowledgement surface |
| apps/cli/commands/chat_cmd.py | +49/-1 | `remedy chat show` lists each message acknowledged, waiting or not taken in, from the run-log events |
| docs/guides/exit-codes.md | +1/-0 | doc update for the new/changed surface |
| packages/orchestration/steering.py | +85/-7 | the consumption event gains `understood`: verbatim restatement, task round, and for a mission's job the contract criterion and mission round |
| packages/orchestration/ui_server.py | +19/-0 | SSE stream carries the acknowledgement fields on that event kind alone |

### 0c57bc87 F264 R6 C4: test the acknowledgement on the stream and in remedy chat show
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_chat_cmd.py | +36/-0 | `remedy chat show` acknowledgement listing, incl. ended-job-never-took-in case |
| tests/orchestration/test_steering.py | +25/-0 | consumption event restates message + round; overview names each status |
| tests/orchestration/test_steering_mission.py | +9/-0 | acknowledgement also names the mission criterion and its round |
| tests/ui_server/test_sse_stream.py | +14/-0 | stream carries the acknowledgement's three fields and no other |

## External actions

- `git worktree add --detach .remedy-wt/f264-r6-mut 0c57bc87` — succeeded, real exit 0
- `git worktree remove --force .remedy-wt/f264-r6-mut` — succeeded, real exit 0
- `git worktree prune` — succeeded, real exit 0
- `git push origin feature/f264-steering-channel` — reported in the reply (run after this commit; cannot be in this table per the self-reference exception)

No PR created or merged this round (per block constraint 5). `gh pr list` reported in the reply.

## Verification

G1 TRANSPORT — all 5 payloads (records.diff, plan.md, product.diff,
mutations.py, tests.diff) measured line count, byte count and sha256
against the PAYLOADS table: all matched exactly. All 6
`.agent/authored/f264-r6-*` copies (block + 5 payloads) read back with
`git show <commit>:<path>` matched their sources byte for byte.

G2 THE RECORDS — at C2 (e340f38b): `git show e340f38b:.agent/live_review.md`
= 320467 bytes, sha256 38cee9eec59dc84c44e8d084d94b2810ebad7131212b2ffecc9d97f4691bfe50
(match); `.agent/decisions.md` = 1953336 bytes, sha256
a35641fe23260ab419be247da1444fc3257440aab05e570361d292403bd6d8c7 (match);
`.agent/plan.md` = 980 bytes, sha256
98a6d8e4b283d42a6a2e06038d0baa54037aa6390f9f179278b676366658885a (match).
Lines added to live_review.md beginning `Gate: F264 R5 — `: 1 (matches
reviewer's reading of 1). `open_finding_ids` (scripts/rotate_live_review.py)
at 70664b29 and at e340f38b: both `{R-0499, R-0950, R-1008}`, set
difference empty both directions (matches reviewer's 3 and 3).
`git diff --name-only ac89b98d e340f38b`: `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md` — exactly the three record
paths.

G3 THE PRODUCT — at C4 (0c57bc87), all nine files read back with
`git show 0c57bc87:<path>` matched the reviewer's simulated readings
byte for byte: `apps/cli/command_catalog.py` (113604 bytes),
`apps/cli/commands/chat_cmd.py` (5462 bytes), `docs/guides/exit-codes.md`
(3983 bytes), `packages/orchestration/steering.py` (19122 bytes),
`packages/orchestration/ui_server.py` (152364 bytes),
`tests/cli/test_chat_cmd.py` (5003 bytes),
`tests/orchestration/test_steering.py` (10360 bytes),
`tests/orchestration/test_steering_mission.py` (3982 bytes),
`tests/ui_server/test_sse_stream.py` (28427 bytes) — all sha256 matched.
`git diff --name-only e340f38b 4e27aeda`: command_catalog.py,
chat_cmd.py, exit-codes.md, steering.py, ui_server.py (matches C3's
five paths). `git diff --name-only 4e27aeda 0c57bc87`: test_chat_cmd.py,
test_steering.py, test_steering_mission.py, test_sse_stream.py
(matches C4's four paths).

G4 THE TESTS — serial pytest run (real exit code):
```
1286 passed in 99.39s (0:01:39)
REAL_EXIT=0
```
The reviewer's sim (without `tests/cli/test_golden_path.py`) read
`1243 passed, 1 skipped` at exit 0. This primary checkout carries the
UI toolchain a worktree lacks, so the one skip passed here; the
difference (1286 vs 1243+1) is consistent with the block's own note
that a skip may pass in the primary checkout.
```
python3 -m ruff check packages/orchestration/steering.py packages/orchestration/ui_server.py apps/cli/commands/chat_cmd.py apps/cli/command_catalog.py tests/orchestration/test_steering.py tests/orchestration/test_steering_mission.py tests/cli/test_chat_cmd.py tests/ui_server/test_sse_stream.py
All checks passed!
REAL_EXIT=0
```
```
python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [...all "pass"...], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```

G5 THE RED PROOFS — `.remedy-wt/f264-r6-payloads/mutations.py` against
`.remedy-wt/f264-r6-mut` (detached at 0c57bc87):
```
control_before: 114 passed, REAL_EXIT=0
m1_event_carries_no_restatement: FROM count 1; 2 failed, 112 passed; REAL_EXIT=1; restored byte-identical: True
m2_restatement_names_no_round: FROM count 1; 2 failed, 112 passed; REAL_EXIT=1; restored byte-identical: True
m3_mission_half_unnamed: FROM count 1; 1 failed, 113 passed; REAL_EXIT=1; restored byte-identical: True
m4_ended_job_shown_as_waiting: FROM count 1; 2 failed, 112 passed; REAL_EXIT=1; restored byte-identical: True
m5_stream_drops_the_acknowledgement: FROM count 1; 1 failed, 113 passed; REAL_EXIT=1; restored byte-identical: True
m6_task_read_from_metadata_only: FROM count 1; 2 failed, 112 passed; REAL_EXIT=1; restored byte-identical: True
control_after: 114 passed, REAL_EXIT=0
```
Exact match to the reviewer's expected readings for all eight lines.
Worktree removed and pruned; `git worktree list` afterward showed only
the primary checkout, the reviewer's `f264-r6-dry`/`f264-r6-sim`, and the
four `job-*` worktrees — nothing else.

## Authored-text proofs

Block (`.agent/authored/f264-r6-block.md`), records.diff, plan.md,
product.diff, mutations.py and tests.diff copies at dddc2268/ac89b98d:
each read back with `git show <commit>:<path>` and compared against the
payload table / this block's own reading — all 6 matched byte for byte.
records.diff, product.diff and tests.diff were applied with `git apply`
(never retyped), each preceded by a real `git apply --check` at exit 0
and followed by the real `git apply` at exit 0. plan.md was copied whole
with `shutil.copyfile`, never retyped.

## Deviations & assumptions

None. The bundle ran in the block's declared order (C1a, C1b, C2, C3,
C4, C5) with no extra, dropped or reordered commits.

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 6.
Then T003's second half — the cockpit renders the acknowledgement from
the stream, under the steering input. Open findings: 3. Operator
questions: 0.
