STEP F030 R3 — BOOK ROUND 2 AND LAND T003'S BROWSER HALF: the stream carries a note's text, the feed shows it as the operator's own line, the input addresses the selected task, and the copy promises no conversation

GOAL
Book round 2's PASS, its prose slip and DECISION F030 D3 with its two design-deviation rows, then
land the browser half of T003: a `steering_message_received` frame carries the note, the live
feed renders it as the operator's line with an initial disc, the dashboard's selected task
reaches the feed's input, which sends `job.steer` for it and `chat.send` without one, and every
sentence the input shows promises a note read at the next round and never a reply. The
end-to-end proof is round 4's.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE CHANGE IS SPECIFIED, NOT SLICED: you write the code
and its tests yourself against S1 to S6. Only the `.agent/` records and the assumption-log rows
travel as payloads. Read DECISION F030 D3 in the booking diff first: it is the design. Before you
write anything, read: `_safe_event_summary` and `_steering_ack_summary_payload` in
`packages/orchestration/ui_server.py`; `tests/ui_server/test_sse_stream.py`'s steering tests and
`tests/ui_server/test_brain_demo_recording_live.py`; in `apps/ui/src/api/` `feedRow.ts`,
`steeringAck.ts`, `steeringSend.ts`, `vetoSend.ts`, `humanizeCatalog.ts` and the `.test.ts` beside
each; `components/panels/ActivityFeedCard.tsx`, `ChatInput.tsx`, `RightLivePanel.tsx` and
`RightLivePanel.module.css`; `components/shell/RemedyShell.tsx` from the `selectedNode`
resolution to the `RightLivePanel` mount; `tests/ui_contracts/test_steering_send_contract.py`,
`tests/ui_contracts/test_humanize_catalog.py`, and `TestTheSteeringInputIsHonest` with the mount
pins beside it in `tests/ui_contracts/test_brain_stream_ring.py`; and the feed and input rules of
`docs/ui/design_reference/ux_spec.md` §11 and `component_spec.md`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f030-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f030-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f030-r3-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f030-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f030-r3-worker/`    YOURS for logs, scripts and scratch configs; create it if
                                  absent. All five are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx from the shell; vitest, tsc and eslint run through the pytest nodes of
G4, and G5's tool spawns the primary checkout's own vitest binary as a subprocess.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f030-steering-messages`, and `git log --oneline -1` must read `59e02546`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f030-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f030-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 81 | 17619 | ba547e5dbae5785d75c247e4c1801fbdf97ff1af0ed06ed4edf59e3e8df85c71 |
| plan.md | 30 | 1039 | 1ac082044653f3d73d39318d496b6b813a2b16e92ebdbe98fd2c72abe597e2d5 |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `59e02546`. It appends round 2's gate entry to
`.agent/live_review.md`, DECISION F030 D3 to `.agent/decisions.md`, one line to
`.agent/prose_slips.md`, and two rows naming DECISION F030 D3 to
`docs/ui/design_reference/assumption_log.md`.

THE SPECIFICATION. No `except Exception`; no raw colour (the ratchet counts them) — only
`var(--remedy-*)` tokens already defined; request building stays in `api/`, never in a component.
S1 THE FRAME, in `ui_server.py`. `_steering_note_summary_payload(metadata) -> dict` answers
   exactly `{"message_id": str, "text": str, "channel": str, "task_id": str}`, each read from the
   metadata and `str()`-ed, "" when absent, and nothing else; its docstring gives the
   acknowledgement payload's reason. `_safe_event_summary` adds `summary["note"]` for
   `steering_message_received` only, its `task_id` falling back to the event's top-level
   `task_id` when the metadata has none; every other kind's frame stays byte-identical.
S2 THE ROW. New `apps/ui/src/api/steeringNote.ts`: `STEERING_NOTE_EVENT =
   "steering_message_received"`; `interface SteeringNote { messageId, text, channel, taskId }`;
   `readSteeringNote(envelope)` answering null unless the kind is that event and `note` is an
   object whose four fields are strings with a non-empty `text` after trimming; and
   `steeringFocusTaskId(tasks, nodeId)` answering the `id` of the task whose `nodeId` equals
   `nodeId`, "" for a null `nodeId` or no match. `FeedRow` gains `author?: "operator"`;
   `feedRowOf` gives a note's row `author: "operator"` and its `text` verbatim as the line, and
   gives every other row neither. In `ActivityFeedCard.tsx`'s live rows an operator row draws, in
   place of `GearGlyph`, a disc holding the letter "Y" (a new class in `RightLivePanel.module.css`
   in the role disc's size, `--remedy-*` tokens only) and shows `You` where the kind is shown.
S3 THE FOCUS. `RemedyShell.tsx` computes `steeringFocusTaskId(dashboard.tasks, selectedNode ?
   selectedNode.nodeId : null)` after its prompt resolution and passes it on the ONE existing
   `<RightLivePanel` line as `focusedTaskId`; `RightLivePanel` passes it on the ONE existing
   `<ActivityFeedCard` line; the card takes `focusedTaskId?: string`. Each mount stays one line.
S4 THE SEND, in `steeringSend.ts`. `STEER_TASK_COMMAND = "job.steer"`;
   `buildSteerTaskRequest(target, taskId, message, clientNonce)` shaped exactly as
   `buildVetoTaskRequest` but with `args: { task_id, message }` (the message normalised as
   `buildChatSendRequest` normalises it), null for an empty task id, an unusable nonce or an
   unsendable message; `describeSteerTaskResult` giving one sentence per outcome — 200 `Your note
   was recorded. Task <id> reads it at the start of its next round.`, a 409 naming
   `task_not_steerable`, `job_not_steerable` or `unknown_task` in plain words from the door's
   `"<code>: <detail>"` error, and the 400, 403, 429 and 500 sentences `describeChatSendResult`
   gives; and `sendSteeringNote(target, taskId, message, deps)` shaped as `sendSteeringMessage`.
   The card's `onSend` is exactly
   `onSend={(text) => (focusedTaskId ? sendSteeringNote(target, focusedTaskId, text) : sendSteeringMessage(target, text))}`.
S5 THE COPY. `steeringPlaceholder(taskId)` in `steeringNote.ts` answers
   `Note for task ${taskId} — read at its next round` for a task and `Note for the whole job —
   read at its next round` for "". `ChatInput` gains `placeholder?: string` and `hint?: string`,
   renders `placeholder` in place of "Ask something…" (which no longer occurs in `apps/ui/src`)
   and `hint` as the input's `title`; the card passes `steeringPlaceholder(focusedTaskId ?? "")`
   and `STEERING_REPLY_FRAMING`. `humanizeCatalog.ts` exports, at column 0 and outside
   `STREAM_EVENT_CATALOG`, `STEERING_REPLY_FRAMING = "Remedy never writes a reply to a steering
   note: the builder's next action in this feed is the answer."`.
S6 EXISTING TESTS: exactly one existing assertion changes — in
   `tests/ui_contracts/test_steering_send_contract.py` the pinned `onSend` literal becomes S4's.
   Every other existing test stays as it is; new vitest cases may be ADDED to `feedRow.test.ts`
   and `steeringSend.test.ts` without changing an existing case.

THE TESTS. NEW `tests/ui_server/test_steering_note_frame.py`: a received frame's `note` is exactly
the four keys with the text verbatim and the task id, "" for a job-wide note; a received frame
still carries no `steering` key; an unknown kind's key set is still the base five. NEW
`tests/ui_contracts/test_steering_note_contract.py`: `STEERING_NOTE_EVENT` is in `EVENT_NAMES`;
the `note` fields `steeringNote.ts` reads equal `set(_steering_note_summary_payload({}))`;
`STEER_TASK_COMMAND` is in `UI_EXPOSED_COMMANDS`; `STEERING_REPLY_FRAMING` occurs once at column 0
and holds "never writes a reply"; and a copy audit over every non-test `.ts`/`.tsx` under
`apps/ui/src` finds no "Ask something", "Builder says", "Remedy says" or "replied". NEW
`apps/ui/src/api/steeringNote.test.ts` for `readSteeringNote`, `steeringFocusTaskId` and
`steeringPlaceholder`; ADDED cases in `feedRow.test.ts` (a note's row) and `steeringSend.test.ts`
(the exact `job.steer` request, its null cases, every result sentence, the send flow).

BUNDLE — the commits are C1 to C7, in this order.
C1 — copy this block and the payloads: `.agent/authored/f030-r3-block.md`,
  `.agent/authored/f030-r3-plan.md`, `.agent/authored/f030-r3-booking.diff`, by
  `shutil.copyfile`. Subject: `F030 R3 C1: copy round 3 block and payloads`
  Its insertions are this block's line count plus 111. Report it; STOP if it is 500 or more.
C2 — THE BOOKING: `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F030 R3 C2: book round 2's PASS and record DECISION F030 D3`
  Expected by `git show --numstat`: 44/0 decisions.md, 2/0 live_review.md, 8/7 plan.md, 1/0
  prose_slips.md, 2/0 assumption_log.md.
C3 — THE FRAME: S1 and `tests/ui_server/test_steering_note_frame.py`.
  Subject: `F030 R3 C3: carry a steering note's text on its stream frame`
C4 — THE ROW AND THE FOCUS: S2, S3, `steeringNote.test.ts` and the `feedRow.test.ts` cases.
  Subject: `F030 R3 C4: show a note as the operator's own line and pass the selected task`
C5 — THE SEND AND THE COPY: S4, S5, S6, the `steeringSend.test.ts` cases and
  `tests/ui_contracts/test_steering_note_contract.py`.
  Subject: `F030 R3 C5: address the input's note to the selected task, promising no reply`
C6 — THE TOOL: your mutation tool (G5) as `.agent/authored/f030-r3-mutations.py`.
  Subject: `F030 R3 C6: add the round 3 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F030 R3 C7: rewrite handoff for round 3`
  Then `git push`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f030-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `docs/ui/design_reference/assumption_log.md`, `.agent/handoff.md`,
   `packages/orchestration/ui_server.py`, and under `apps/ui/src/`: `api/steeringNote.ts`,
   `api/steeringNote.test.ts`, `api/feedRow.ts`, `api/feedRow.test.ts`, `api/steeringSend.ts`,
   `api/steeringSend.test.ts`, `api/humanizeCatalog.ts`,
   `components/panels/ActivityFeedCard.tsx`, `components/panels/ChatInput.tsx`,
   `components/panels/RightLivePanel.tsx`, `components/panels/RightLivePanel.module.css`,
   `components/shell/RemedyShell.tsx`; and `tests/ui_server/test_steering_note_frame.py`,
   `tests/ui_contracts/test_steering_note_contract.py`,
   `tests/ui_contracts/test_steering_send_contract.py`. Report `git diff --name-only 59e02546`
   after C7. Touch nothing else — not `steering.py`, not `event_names.py`, nothing under `apps/cli/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test THIS round wrote that is wrong may be corrected
   before C7, and the correction is declared. An existing test that goes red, S6's one assertion
   apart, is reported, and you stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives it to F030's closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 `.agent/authored/f030-r3-*` payload copy read back with `git show <C1>:<path>` compared byte for
 byte with its source (the block copy against `.remedy-wt/f030-r3/block.md`). One reading each.
G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2318512 | d4a3b9066757f4ee5437a2b700f646a400c919495283585e9ef30d48c28640e9 |
 | .agent/live_review.md | 314301 | fff987aee67d2cef8ac4e04dfe459aabed2f599904df779f29708bff4ede2b26 |
 | .agent/plan.md | 1039 | 1ac082044653f3d73d39318d496b6b813a2b16e92ebdbe98fd2c72abe597e2d5 |
 | .agent/prose_slips.md | 374557 | 81ead1202d8dcafb5bf69ee9ee32715bd74d5a7255d02f98e25ff0fdac8a5e2b |
 | docs/ui/design_reference/assumption_log.md | 21917 | ef6dbd9c45dd711ecdcd9427efc6d83ccdea333e4f8f45520ca1751372e74f7e |
 Also `open_finding_ids` over the ledger's text at C2 (the reviewer read `[]`), and
 `git diff --name-only <C1> <C2>`, which must name exactly the paths of the table.
G3 THE CODE — `python3 -m ruff check packages/orchestration/ui_server.py
 tests/ui_server/test_steering_note_frame.py tests/ui_contracts/test_steering_note_contract.py
 tests/ui_contracts/test_steering_send_contract.py` at C6 with its real exit code; then quote
 from the diff `_steering_note_summary_payload`, `readSteeringNote`, the card's operator row and
 its `onSend`, and the shell's `focusedTaskId` line.
G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_steering_note_frame.py tests/ui_server/test_sse_stream.py tests/ui_server/test_brain_demo_recording_live.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/ui_server/test_steer_task_door.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_steering_notes.py tests/orchestration/test_steer_task.py tests/orchestration/test_steering.py tests/orchestration/test_event_names.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -16; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the two new Python test files, serially, in the primary
 checkout at `59e02546`, and read `1840 passed, 11 skipped` at real exit code 0; the eleven
 skips are F252 quarantines. Report every `SKIPPED` line, the node count of each new Python test
 file by `--collect-only -q`, and account for any difference from 1840 plus those counts; the
 vitest cases run inside the one `TestVitestFrontendTestFoundation` selection, so also report the
 vitest totals that node prints or records. Then `python3 -m apps.cli.main integrity check
 --json`: every check's status and `fail_count`.
G5 THE RED PROOFS — your tool `.agent/authored/f030-r3-mutations.py` takes a worktree path. For
 each mutation it edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs the named runner, and restores the bytes. PYTHON: `python3 -B -m pytest -q
 -p no:cacheprovider tests/ui_server/test_steering_note_frame.py tests/ui_server/test_sse_stream.py
 tests/ui_contracts/test_steering_note_contract.py` from the worktree's root after purging its
 `__pycache__`. VITEST: the PRIMARY checkout's `apps/ui/node_modules/.bin/vitest run --config
 <scratch>`, run with the primary's `apps/ui` as its working directory, where `<scratch>` is a
 config the tool writes under `.remedy-wt/f030-r3-worker/` exporting a PLAIN OBJECT with `root`
 the primary's `apps/ui`, `cacheDir` a directory under `.remedy-wt/`, `test.environment`
 `"node"` and `test.include` the worktree's `steeringNote.test.ts`, `feedRow.test.ts` and
 `steeringSend.test.ts` by absolute path. An unmutated control of EACH runner runs first and
 last. It prints one line per mutation (label, runner, exit code, failed count, the failing tests'
 names) and ends with `restored byte-identical: True` per file, the PRIMARY checkout's
 `git status --porcelain` (which must be empty) and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
 <bool>`.
  m1 PYTHON `ui_server.py`: the note payload leaves out `text`;
  m2 PYTHON `ui_server.py`: `note` is added to every kind's frame;
  m3 PYTHON `ui_server.py`: the note payload also copies `record_sha256`;
  m4 VITEST `steeringNote.ts`: `readSteeringNote` accepts a blank text;
  m5 VITEST `steeringNote.ts`: `steeringFocusTaskId` always answers "";
  m6 VITEST `steeringNote.ts`: `steeringPlaceholder` names the whole job for a task;
  m7 VITEST `feedRow.ts`: a note's row keeps the catalog line;
  m8 VITEST `feedRow.ts`: a note's row gets no `author`;
  m9 VITEST `steeringSend.ts`: `buildSteerTaskRequest` sends `chat.send`;
  m10 VITEST `steeringSend.ts`: `buildSteerTaskRequest` leaves out `task_id`;
  m11 VITEST `steeringSend.ts`: a 409 `task_not_steerable` reads as the accepted sentence.
 Run it: `git worktree add --detach .remedy-wt/f030-r3-mut <C6>`, then
 `python3 -B .agent/authored/f030-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f030-r3-mut`
 and report its whole output. EVERY mutation must be red with at least one failing test; one that
 stays green is reported as green, never papered over, and you then add the test that catches it
 before C7 and re-run the tool. Then `git worktree remove --force .remedy-wt/f030-r3-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C7 down to C1 and `59e02546` (more lines if
 constraint 2 split a commit); `git worktree list | wc -l`, equal to your step 4 reading; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, INSIDE `.agent/handoff.md`, with EVERY one of
these sections: the Session section, the range, the per-commit changed-files table with the
insertion count you MEASURED beside the one this block expected (none is expected for C3 to C6),
the external actions, every gate's real output and exit code, the authored-text proofs, the
deviations, the ITEM-STATUS TABLE AGENTS.md requires with one row per commit and one per gate,
and the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F030, round 3, and says in one sentence how much context you
had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003's end-to-end proof — a note sent through the door while a task builds reaches
that task's next round's trace, and the stream shows the note before the task's next action. State
the open-findings count, 0, and the operator-questions count, 0.
