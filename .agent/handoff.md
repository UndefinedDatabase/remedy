# Handoff — F030, round 2 (book R1, DECISION F030 D2, T002)

## Session

SESSION 1 of feature F030 · round 2 · rounds so far 2. Context remaining at
handback: comfortable — the round read every named source file once, wrote
S1–S4's production change and its three new test files in one pass, hit one
red gate (a vocabulary-page check on the new catalog description) that cost
one small extra commit to repair, then ran every gate green and still has a
healthy context budget left.

## Range

Review of `886b60559`..`HEAD` (`HEAD` is this handback's own commit, `F030
R2 C7`, on `feature/f030-steering-messages`).

## Commits

### 0bb5ddf9e F030 R2 C1: copy round 2 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r2-block.md | 295/0 | verbatim copy of this round's block |
| .agent/authored/f030-r2-booking.diff | 62/0 | verbatim copy of the booking payload |
| .agent/authored/f030-r2-plan.md | 29/0 | verbatim copy of the plan payload |

Measured insertions: 386 (295+62+29). Block expected 295+91=386. Match.

### 286b79727 F030 R2 C2: book round 1's PASS and record DECISION F030 D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 44/0 | DECISION F030 D2 appended (`git apply` of booking.diff) |
| .agent/live_review.md | 2/0 | F030 R1 Gate entry appended (`git apply` of booking.diff) |
| .agent/plan.md | 7/8 | rewritten to plan.md payload |

Measured numstat: 44/0, 2/0, 7/8. Block expected exactly this. Match.

### 31f0f83e2 F030 R2 C3: address a note to a task through one shared command
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/steering.py | 86/6 | S1 `steer_task_command`, `STEERABLE_TASK_STATUSES`; S2 `steering_overview` gains `addressed_to`/`task_statuses` |
| tests/orchestration/test_steer_task.py | 158/0 | new: refusal order, acceptance over the five steerable statuses, refusal over the four non-steerable ones, the pinned-statuses test, the overview's `addressed_to`/`not_taken_in` |

Measured insertions: 244. No insertion count was ordered for this commit.

### 8fec9f4b7 F030 R2 C4: add remedy job steer and name a note's task in chat show
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 25/0 | S3 `job.steer` catalog entry, `UI_EXPOSED_COMMANDS` gains it |
| apps/cli/commands/__init__.py | 2/1 | registers `job_steer_cmd` in the handler-collection import and loop |
| apps/cli/commands/chat_cmd.py | 18/2 | `_cmd_chat_show` builds `task_statuses`, names the addressed task in text and JSON |
| apps/cli/commands/job_steer_cmd.py | 80/0 | new: `remedy job steer` handler |
| docs/guides/exit-codes.md | 1/0 | `remedy job steer` row, directly after `job veto-task`'s |
| tests/cli/test_job_steer.py | 167/0 | new: text/JSON acceptance, planned-id resolution, refusal exit codes, `chat show` naming the task |
| tests/orchestration/import_reachability_allowlist.txt | 1/0 | `apps.cli.commands.job_steer_cmd` in alphabetical place |

Measured insertions: 294. No insertion count was ordered for this commit.

### dfb46b2a2 F030 R2 C5: expose job.steer through the write door
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | 66/0 | S4 `JOB_STEER_COMMAND_ID`, the `job.steer` branch of `_handle_command_submission`, `_dispatch_steer_task`, the `job.steer` shape checks in `_read_command_payload` |
| tests/ui_server/test_command_channel.py | 10/2 | `DOOR_METHODS` gains `_dispatch_steer_task`; `ALLOWED_IMPORTS` gains `steer_task_command`; `TestUiExposedCommands`'s ruled list and the exposed-commands loop gain `job.steer` |
| tests/ui_server/test_steer_task_door.py | 163/0 | new: acceptance with channel `cockpit`, the four refusal/shape-error cases |

Measured insertions: 239. No insertion count was ordered for this commit.

### 1292f743a F030 R2 C6: add the round 2 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r2-mutations.py | 216/0 | G5's red-proof tool, 12 mutations over S1–S4 |

Measured insertions: 216. No insertion count was ordered for this commit.

### 73d3cd0d9 F030 R2 C4 fix: use the vocabulary page's Round meaning fragment for job.steer
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 2/2 | `job.steer`'s description reworded to carry `build`, `docs/system/vocabulary.md`'s meaning fragment for the binding word `Round` |

Measured insertions: 2. Unordered commit — see Deviations below.

Exception (self-reference, per `docs/agents/handback_template.md`): this
handback's own commit, `F030 R2 C7`, is not tabled here.

## External actions

- `git worktree add --detach .remedy-wt/f030-r2-basecount 886b60559` — to
  measure node-count deltas for G4's accounting requirement. Removed with
  `git worktree remove --force .remedy-wt/f030-r2-basecount` and
  `git worktree prune`; `git worktree list | wc -l` read 62 afterward.
- `git worktree add --detach .remedy-wt/f030-r2-mut 73d3cd0d9` — G5's
  red-proof worktree. Removed with
  `git worktree remove --force .remedy-wt/f030-r2-mut` and
  `git worktree prune`; `git worktree list | wc -l` read 62 afterward.
- No push, no PR create/edit/merge yet — those are G6, run after this
  commit; their real readings are in this round's reply, not here.

## Verification

**G1 transport** — payload readings (measured before use):

    booking.diff lines: 62 bytes: 11814 sha256: efe75e7d661fea96620f770c8597afadc465bfea367cceebecf6329bef334d60
    plan.md lines: 29 bytes: 950 sha256: a14dcd35f5785c74f8cb8a9ab23c202d18b5c5dc673f233e0960e5dddccdcdbc

Both equal the PAYLOADS table exactly. Block copy verified before use:
lines 295, sha256 448947e7…5569, equal to the delegation message's two
readings.

Each `.agent/authored/f030-r2-*` copy read back with `git show 0bb5ddf9e:<path>`
equalled its source byte for byte (script output):

    block.md source equal: True  src_sha256: 448947e7…5569  committed_sha256: 448947e7…5569
    plan.md source equal: True   src_sha256: a14dcd35…dcdbc  committed_sha256: a14dcd35…dcdbc
    booking.diff source equal: True  src_sha256: efe75e7d…334d60  committed_sha256: efe75e7d…334d60

`git apply --check .remedy-wt/f030-r2-payloads/booking.diff` → `REAL_EXIT=0`.
`git apply .remedy-wt/f030-r2-payloads/booking.diff` → `REAL_EXIT=0`.

**G2 the booking** — at `286b79727`, `git show <sha>:<path>` read:

    .agent/decisions.md   bytes: 2314513  sha256: 1a38d90282c2796588af0c791e1001d4f237896883d38eaefb6a61df47c294b0
    .agent/live_review.md bytes: 311600   sha256: e7463f7d8d71ec17c7c6f5fa90883d6b4b47e704ab04dafc660b725ea1bc155c
    .agent/plan.md        bytes: 950      sha256: a14dcd35f5785c74f8cb8a9ab23c202d18b5c5dc673f233e0960e5dddccdcdbc

All three equal the reviewer's given readings. `open_finding_ids` (from
`scripts/rotate_live_review.py`, imported and run over the ledger text at
`286b79727`) read `[]` — empty, as the reviewer read it. The ledger's last
line at that commit begins `Gate: F030 R1 — the F030 round`.

**G3 the code** — ruff over every Python file of constraint 3 outside
`.agent/`, run twice (once at C6, re-run at the tip after the C4 fix):

    python3 -m ruff check packages/orchestration/steering.py packages/orchestration/ui_server.py apps/cli/command_catalog.py apps/cli/commands/__init__.py apps/cli/commands/job_steer_cmd.py apps/cli/commands/chat_cmd.py tests/ui_server/test_command_channel.py tests/orchestration/test_steer_task.py tests/cli/test_job_steer.py tests/ui_server/test_steer_task_door.py
    All checks passed!
    REAL_EXIT=0

`steer_task_command`, the new `_handle_command_submission` branch and
`_dispatch_steer_task`, quoted from `git show` at the tip, are in this
round's Verification transcript kept by the worker and match the code
shown in the Commits section's diffs above (S1 and S4 respectively).

**G4 the tests** — first run, at C6 (before the fix), read one failure:
`tests/docs/test_vocabulary.py` — `job.steer`'s description used the
binding word "Round" without one of `docs/system/vocabulary.md`'s meaning
fragments (`build`, `review`, `repair`) for it — `1 failed, 1896 passed, 1
skipped`. Repaired by commit `73d3cd0d9` (reworded the description to
carry `build`), NOT by editing the test. Re-run at the tip:

    SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 ...
    1897 passed, 1 skipped in 120.26s (0:02:00)
    REAL_EXIT=0

Reviewer's base at `886b6055` (selection minus the three new test files):
1859 passed, 1 skipped. Accounting for 1897:
- the three new test files together collect 35 nodes (`--collect-only`):
  `test_steer_task.py` 18, `test_job_steer.py` 11, `test_steer_task_door.py` 6.
- `tests/ui_server/test_command_channel.py` collects 110 nodes at both
  `886b60559` and the tip — the S4 edits changed existing test BODIES
  (a new `DOOR_METHODS`/`ALLOWED_IMPORTS` entry, a new `elif` branch and a
  new list entry) and added no new test function. Delta: 0.
- the catalog-parametrized suites gained 3 nodes from the new `job.steer`
  catalog entry: `tests/cli/test_exit_codes.py` 331→333 (+2),
  `tests/cli/test_json_contract.py` 200→201 (+1). Every other file in that
  group (`test_command_catalog.py`, `test_advertised_commands.py`,
  `test_cli_ux.py`, `test_job_refusal_envelope.py`,
  `test_list_commands_everywhere.py`, `test_job_commands.py`,
  `test_dead_command_check.py`) is unchanged in node count.
- 1859 + 35 + 0 + 3 = 1897. Matches exactly.

`python3 -m apps.cli.main integrity check --json` →

    {"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}
    REAL_EXIT=0

All six checks `pass`.

**G5 the red proofs** — `git worktree add --detach .remedy-wt/f030-r2-mut
73d3cd0d9` (the tip, after the C4 fix — see Deviations), then
`python3 -B .agent/authored/f030-r2-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f030-r2-mut`:

    control (start): exit=0 failed=0 nodes=[]
    m1 STEERABLE_TASK_STATUSES also holds passed: exit=1 failed=5 caught=True restored=True
    m2 STEERABLE_TASK_STATUSES loses failed: exit=1 failed=2 caught=True restored=True
    m3 steer_task_command records the note without its task id: exit=1 failed=12 caught=True restored=True
    m4 step c (the unknown-task check) is skipped: exit=1 failed=4 caught=True restored=True
    m5 step b (the ended-job check) is skipped: exit=1 failed=3 caught=True restored=True
    m6 steering_overview ignores task_statuses: exit=1 failed=2 caught=True restored=True
    m7 task_not_steerable exits 1: exit=1 failed=1 caught=True restored=True
    m8 the task argument is passed on without _resolve_task_arg: exit=1 failed=1 caught=True restored=True
    m9 _dispatch_steer_task records with channel cli: exit=1 failed=1 caught=True restored=True
    m10 _read_command_payload's job.steer check on task_id is skipped: exit=1 failed=1 caught=True restored=True
    m11 the new branch answers a refusal 200: exit=1 failed=3 caught=True restored=True
    m12 _cmd_chat_show passes no task_statuses: exit=1 failed=1 caught=True restored=True
    control (end): exit=0 failed=0 nodes=[]
    restored byte-identical: True
    ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True

Every mutation caught (exit≠0, failed>0, at least one failing node id
printed in full by the tool — trimmed here for length). Worktree removed:
`git worktree remove --force .remedy-wt/f030-r2-mut`, `git worktree prune`;
`git worktree list | wc -l` read 62 afterward, equal to this round's
step-4 reading.

`git diff --name-only 886b6055` at the tip (before C7): exactly the 19
paths constraint 3 lists (the `.agent/authored/f030-r2-*` copies and tool,
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`,
`apps/cli/commands/chat_cmd.py`, `apps/cli/commands/job_steer_cmd.py`,
`docs/guides/exit-codes.md`, `packages/orchestration/steering.py`,
`packages/orchestration/ui_server.py`, `tests/cli/test_job_steer.py`,
`tests/orchestration/import_reachability_allowlist.txt`,
`tests/orchestration/test_steer_task.py`,
`tests/ui_server/test_command_channel.py`,
`tests/ui_server/test_steer_task_door.py`). No path outside that set; none
of the seven forbidden paths (`apps/ui/`, `pingpong_loop.py`,
`pingpong_job.py`, `event_names.py`, `.agent/context.md`,
`.agent/prose_slips.md`, `.agent/candidates.md`,
`.agent/operator_questions.md`, `README.md`, `docs/roadmap/`) touched.

## Authored-text proofs

The three `.agent/authored/f030-r2-*` payload copies (G1, above): each
equals its source byte for byte, read back from `git show 0bb5ddf9e:<path>`
against the file this worker measured from `.remedy-wt/f030-r2/block.md`
and `.remedy-wt/f030-r2-payloads/`. `.agent/authored/f030-r2-mutations.py`
is this worker's own authored tool (G5), not a reviewer payload, so it
carries no fidelity comparison — its correctness is the G5 red-proof run
itself.

## Deviations & assumptions

1. **An 8th, unordered commit** — `73d3cd0d9`, "F030 R2 C4 fix: use the
   vocabulary page's Round meaning fragment for job.steer" — landed between
   C6 and C7. G4's first run (at C6) read one red test,
   `tests/docs/test_vocabulary.py`: `job.steer`'s catalog description used
   the binding word "Round" ("...read at that task's next round...")
   without carrying one of `docs/system/vocabulary.md`'s meaning fragments
   for it (`build`, `review`, `repair`) — DECISION amend0905-vocab D1's
   rule, an EXISTING test correctly catching a real defect in this round's
   own C4 commit. Per constraint 4, an existing test that goes red is never
   edited to pass; the fix instead reworded the description ("...read at
   the start of that task's next build round...") so it carries `build`,
   mirroring `chat.show`'s own existing "build round" phrasing. This is a
   correction to this round's own production text, not a test edit, and it
   is declared here because it departs from the block's exact C1–C7
   sequence (docs/agents/handback_template.md's "ANY DEPARTURE... belongs
   here" rule).
2. Because of (1), G3 (ruff) and G4 (the pytest selection) were each run
   twice: once at C6 (where G4 read the one failure above) and again at the
   tip after the fix, where both read clean. G5's red-proof worktree was
   built at the tip (`73d3cd0d9`), not literally "at C6" as the block's own
   wording says, because red-proving the pre-fix code would have proved
   nothing about what is actually being handed back. All readings reported
   above are the tip's.
3. A disposable worktree, `.remedy-wt/f030-r2-basecount` at `886b60559`,
   was built and removed to measure the base selection's per-file node
   counts for G4's "account for any difference from 1859" requirement —
   the block orders the accounting but does not name a mechanism for it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C4 fix | deviated | unordered commit repairing a red `tests/docs/test_vocabulary.py`, declared above |
| C5 | done | |
| C6 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | run twice; red before the fix is not applicable here, ruff itself was clean both times — the vocabulary failure was a pytest (G4) finding |
| G4 | done | first run at C6 read one failure (`tests/docs/test_vocabulary.py`), repaired by the C4 fix commit, re-run clean |
| G5 | done | all 12 mutations caught, restored byte-identical |

## Next

Per the block's `## Next` order: Phase 1 rule 1 (read `.agent/STOP` from
disk) — checked at this round's step 1, absent. Then the review of round 2.
Then T003 — the feed shows the operator's own line, the input addresses the
focused task with copy that promises no conversation, and the end-to-end
proof. Open findings: 0. Operator questions: 0.
