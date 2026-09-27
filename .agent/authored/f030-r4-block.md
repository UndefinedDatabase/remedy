STEP F030 R4 — BOOK ROUND 3 AND LAND T003'S END-TO-END PROOF: a note sent through the live write door while a task's build call is in flight reaches that task's next round and the stream, and a note whose task finishes first is reported as not taken in

GOAL
Round 3 passed. Book its gate entry, then prove the feature end to end against a real job run and
the real write door: a note addressed to the running task, posted while its round 1 build call is
held in flight, leaves round 1's prompt untouched, is taken in at round 2 as the
`builder_operator_notes` segment, and reaches the stream as the operator's line before the
acknowledgement and the task's next action; and a note whose task passes in the round it arrived
in is never taken in, never reaches another task, and is listed by the job report and by
`remedy chat show`. The closure sequence follows this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE TEST IS SPECIFIED, NOT SLICED: you write it against S1.
No production file changes in this round. Read, whole: `tests/ui_server/test_pause_e2e_live.py`
(your model: its `_RUNNER`, its process ownership helpers, `_start_ui_server_for_job`, `_post`, and
how it sets the data root around the server), `tests/ui_server/test_steer_task_door.py`,
`tests/orchestration/test_steering_notes.py`'s call-boundary tests, and in
`packages/orchestration/prompt_trace.py` what a trace entry records.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f030-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f030-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f030-r4-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f030-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f030-r4-worker/`    YOURS for logs and scripts; create it if absent. All five are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f030-steering-messages`, and `git log --oneline -1` must read `34f012e3`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f030-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f030-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 10 | 9582 | 355943c47f4ef9f8716cbeddfd0d8cb03e44b8b12754768ffe78f5a2b19bf504 |
| plan.md | 29 | 1033 | 79472ac16f1e8f989d5dcd4409923d4b0be7f7f3e7501879300b142bf738c0fb |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `34f012e3`. It appends round 3's gate entry to
`.agent/live_review.md`.

S1 THE PROOF — a NEW file `tests/ui_server/test_steering_note_e2e_live.py`, marked as the model
is, with its own copies of the model's helpers (the model's header says why). Its runner script is
the model's, with ONE change to the provider: `HandshakeFakeProvider(FakeProvider)`, built with the
pass round each scenario names, whose `build` — on the FIRST build call of the whole runner
process only, kept by a module-level flag because `create_provider` builds a fresh provider for
every task, so that call is the first task's round 1 — writes a file `<tmp>/building` and then
waits, polling every 0.05 s for up to 60 s, until a file `<tmp>/go` exists, before calling
`FakeProvider.build`. Every other call passes straight through. The job is a two-task job markdown file, as the model's is,
tasks T1 and T2 in that order. Both scenarios run the runner as a subprocess against a data root
under `tmp_path`, wait for `building`, start the UI server on that same data root, POST `job.steer`
through `_post` with `task_id` the first task's id and `message` the scenario's note, assert the
answer is 200 with outcome `accepted`, then create `go` and wait for the runner to exit 0 with a
`FINAL:` line. Every child process the test starts is stopped by its own pid.
  SCENARIO A, TAKEN IN — the provider fails round 1 and passes round 2. Assert: the first task's
  run's recorded prompt trace (read from its run directory's `prompt_trace.jsonl`) has builder
  entries for rounds 1 and 2; round 1's `segment_manifest` has no `builder_operator_notes` row and
  its recorded prompt text does not contain the note; round 2's has exactly one such row at rank 5
  and its recorded prompt text contains the note; the second task's builder entries have no such
  row; the consumption marker names the first task and round 2; and in the events the server
  answers through `events-since`, the `steering_message_received` frame's `note` is
  `{"message_id", "text": <the note>, "channel": "cockpit", "task_id": <the first task>}` and its
  `seq` is lower than the `steering_message_consumed` frame's, whose `steering.round_number` is 2,
  and lower than that of at least one later frame of the first task whose kind is not a steering
  kind — the builder's next action. No frame carries a composed reply: no frame's kind other than
  the two steering kinds carries the note's text.
  SCENARIO B, NOT TAKEN IN — the provider passes round 1. Assert: no consumption marker exists; no
  builder trace entry of either task has a `builder_operator_notes` row or contains the note;
  `export_job_report` of the finished job lists, for the first task only, `steering_not_consumed`
  with the note's id and text, and `format_job_report_text` has the line
  `      Steering not consumed: “<the note>”`; and `python3 -m apps.cli.main chat show <job_id>
  --json`, run with the same data root, answers the note's row with `status` `not_taken_in` and
  `addressed_to` the first task.
  If the recorded trace does not record prompt text at all, say so in the handback and assert the
  manifest rows alone; do not change any production file to make it record text.

BUNDLE — the commits are C1 to C5, in this order.
C1 — copy this block and the payloads: `.agent/authored/f030-r4-block.md`,
  `.agent/authored/f030-r4-plan.md`, `.agent/authored/f030-r4-booking.diff`, by
  `shutil.copyfile`. Subject: `F030 R4 C1: copy round 4 block and payloads`
  Its insertions are this block's line count plus 39. Report it; STOP if it is 500 or more.
C2 — THE BOOKING: `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F030 R4 C2: book round 3's PASS`
  Expected by `git show --numstat`: 2/0 live_review.md, 7/8 plan.md.
C3 — S1. Subject: `F030 R4 C3: prove a steering note end to end through the write door`
C4 — your mutation tool (G5) as `.agent/authored/f030-r4-mutations.py`.
  Subject: `F030 R4 C4: add the round 4 mutation tool`
C5 — `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F030 R4 C5: rewrite handoff for round 4`
  Then `git push`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f030-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md` and
   `tests/ui_server/test_steering_note_e2e_live.py`. Report `git diff --name-only 34f012e3` after
   C5. No production file, no existing test and no browser file changes.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test THIS round wrote that is wrong may be corrected
   before C5, and the correction is declared. A red that the code, not the test, causes is
   reported with its evidence, and you stop; you never change a production file.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives it to F030's closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 `.agent/authored/f030-r4-*` payload copy read back with `git show <C1>:<path>` compared byte for
 byte with its source (the block copy against `.remedy-wt/f030-r4/block.md`). One reading each.
G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 317793 | 988cbf32fb2fc9fabb0e7293384b41920b455261ed720b7524649145cfdf3628 |
 | .agent/plan.md | 1033 | 79472ac16f1e8f989d5dcd4409923d4b0be7f7f3e7501879300b142bf738c0fb |
 Also `open_finding_ids` over the ledger's text at C2 (the reviewer read `[]`).
G3 THE CODE — `python3 -m ruff check tests/ui_server/test_steering_note_e2e_live.py` at C4 with
 its real exit code; then quote from the diff the handshake provider and scenario A's ordering
 assertions.
G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes: first the new file
 alone three times, reporting each run's summary line and wall time; then
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_steering_note_e2e_live.py tests/orchestration/test_steering_notes.py tests/orchestration/test_steer_task.py tests/orchestration/test_steering.py tests/orchestration/test_steering_consumption.py tests/cli/test_chat_cmd.py tests/cli/test_job_steer.py tests/ui_server/test_steer_task_door.py tests/ui_server/test_steering_note_frame.py tests/ui_contracts/test_steering_note_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py tests/test_no_orphan_modules.py tests/test_imports.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the new file, serially, in the primary checkout at
 `34f012e3`, and read `567 passed, 1 skipped` at real exit code 0, the skip being the F252
 quarantine in `tests/test_agent_tooling.py`. Report every `SKIPPED` line and the new file's node
 count by `--collect-only -q`, and account for any difference from 567 plus that count. Then
 `python3 -m apps.cli.main integrity check --json`: every check's status and `fail_count`.
G5 THE RED PROOFS — the new test must be able to fail. Your tool
 `.agent/authored/f030-r4-mutations.py` takes a worktree path; for each mutation it replaces the
 quoted line's text INSIDE that worktree (asserting the FROM text occurs exactly once in that
 file), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_server/test_steering_note_e2e_live.py` from the worktree's root after purging its
 `__pycache__`, and restores the bytes; an unmutated control runs first and last; it prints one
 line per mutation (label, exit code, failed count, failing node ids) and ends with
 `restored byte-identical: True` per file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `packages/orchestration/steering.py`: `if addressed_to and addressed_to != str(task_id):`
     becomes `if addressed_to:` — no note is ever taken in;
  m2 `packages/orchestration/pingpong_loop.py`:
     `operator_notes_text = _operator_notes_text_for_round(job_id, task_id)` becomes
     `operator_notes_text = ""`;
  m3 `packages/orchestration/ui_server.py`: `summary["note"] = note` becomes
     `summary.pop("note", None)`;
  m4 `packages/orchestration/pingpong_job.py`: `if task.status in (TASK_PENDING, TASK_RUNNING):`
     becomes `if True:` — the report lists no note.
 Run it: `git worktree add --detach .remedy-wt/f030-r4-mut <C4>`, then
 `python3 -B .agent/authored/f030-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f030-r4-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, and you then strengthen the test before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f030-r4-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5 down to C1 and `34f012e3`; `git worktree list |
 wc -l`, equal to your step 4 reading; the push's real outcome; and `gh pr list --state open
 --json number,headRefName,baseRefName,isDraft`, which must be EMPTY. These readings go in your
 reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, INSIDE `.agent/handoff.md`, with EVERY one of
these sections: the Session section, the range, the per-commit changed-files table with the
insertion count you MEASURED beside the one this block expected (none is expected for C3 and C4),
the external actions, every gate's real output and exit code, the authored-text proofs, the
deviations, the ITEM-STATUS TABLE AGENTS.md requires with one row per commit and one per gate,
and the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F030, round 4, and says in one sentence how much context you
had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then the closure sequence's first round — the Built State, the checklist consolidation,
the self-use item and the one full suite. State the open-findings count, 0, and the
operator-questions count, 0.
