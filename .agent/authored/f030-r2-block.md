STEP F030 R2 — BOOK ROUND 1 AND LAND T002: `job.steer`, one command on the write door and on the command line that addresses a note to one task, with the task state gate, and `remedy chat show` naming a note's task

GOAL
Book round 1's PASS and record DECISION F030 D2, then land T002 on top of round 1's task address:
`steering.steer_task_command`, the one function both doors call, which refuses an unusable
text, an ended job, an unknown task and a task that will not run again, and records the note
otherwise; `remedy job steer <job_id> --task <task> "<text>"`; the write door's `job.steer`; and
`steering_overview` with `remedy chat show` naming the task a note went to and saying when that
task finished without reading it. No browser code changes in this round; that is T003.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S5 below. Only the `.agent/` records travel
as payloads. Read DECISION F030 D2 in the booking diff before you write code: it is the design
this specification implements. Before you write anything, read `packages/orchestration/steering.py`
whole; `packages/orchestration/task_veto.py`'s `veto_task_command` and `VETOABLE_TASK_STATUSES`;
`apps/cli/commands/chat_cmd.py` and `apps/cli/commands/job_veto_cmd.py` whole; `_resolve_task_arg`
in `apps/cli/commands/job_plan_cmd.py`; the `job.veto-task` and `job.inject` entries, the `chat`
entries and `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py`; in
`packages/orchestration/ui_server.py` the `JOB_VETO_TASK_COMMAND_ID` constant and its comment,
the `job.veto-task` branch of `_handle_command_submission`, `_dispatch_veto_task`, and the
`chat.send` and `job.veto-task` checks of `_read_command_payload`; and in
`tests/ui_server/test_command_channel.py` the exposed-commands loop (the test whose docstring
names `job.rerun-subtree`'s shape error), `TestUiExposedCommands` and `TestCommandDoorImportGuard`
whole. Model the new tests on `tests/cli/test_job_veto.py` and
`tests/ui_server/test_rerun_subtree_door.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f030-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f030-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f030-r2-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f030-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f030-r2-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f030-steering-messages`, and `git log --oneline -1` must read `886b6055`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f030-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f030-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 62 | 11814 | efe75e7d661fea96620f770c8597afadc465bfea367cceebecf6329bef334d60 |
| plan.md | 29 | 950 | a14dcd35f5785c74f8cb8a9ab23c202d18b5c5dc673f233e0960e5dddccdcdbc |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `886b6055` into which it wrote the edits. It
appends round 1's gate entry to `.agent/live_review.md` and DECISION F030 D2 to
`.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere; imports inside the CLI handler and the door
methods are function-scoped, as their neighbours' are.
S1 THE COMMAND, in `steering.py`. `STEERABLE_TASK_STATUSES = frozenset({"pending", "running",
   "blocked", "failed", "skipped"})`, commented as DECISION F030 D2 (3): the statuses of a task
   that can still run, equal to `task_veto.VETOABLE_TASK_STATUSES` and pinned by a test, not
   imported. `steer_task_command(job, task_id, text, *, channel, root=None, now=None) -> dict`
   never raises for a refusal; it answers `{"outcome": "refused", "code", "detail", "task_id"}`
   from the first of, in this order:
   a. `normalize_steering_text(text)` refuses — `invalid_message`, detail `str(exc)`;
   b. `job_is_terminal` of the job's state — `job_not_steerable`, detail
      `f"job {job.job_id} has ended ({state}); no run will read a note"`;
   c. no task of `job.tasks` has the id `task_id` — `unknown_task`, detail
      `f"there is no task {task_id!r} in job {job.job_id}; its tasks are: {listing}"`, `listing`
      joining the first ten task ids with `", "` and, when there are more, adding
      `f" and {n} more"`;
   d. the task's status (a `RunState`'s `.value`, else `str`) is not in
      `STEERABLE_TASK_STATUSES` — `task_not_steerable`, detail
      `f"task {task_id} is {status}; a note reaches only a task that can still run"`.
   Otherwise it calls `record_steering_message(job.job_id, text, job_state=state,
   channel=channel, task_id=task_id, root=root, now=now)` and answers `{"outcome": "accepted",
   "request_id", "message_id", "task_id", "received_at", "record_sha256"}`, both ids being the
   record's `message_id`. A `SteeringWriteError` propagates. Nothing is written on a refusal.
S2 THE OVERVIEW, in `steering.py`. `steering_overview(job_id, job_state, root=None, *,
   task_statuses=None)`: every row gains `"addressed_to": note_task_id(record)`; a row with no
   acknowledgement whose `addressed_to` is a key of `task_statuses` mapping to a status that is
   neither `pending` nor `running` reads `not_taken_in`, whatever the job's state; every other
   row reads exactly as today.
S3 THE COMMAND LINE. A new module `apps/cli/commands/job_steer_cmd.py`, its docstring naming
   F030 T002 and DECISION F030 D2 and its exit codes, with `COMMAND_HANDLERS = {"job.steer": ...}`
   reading `job_id`, `task`, `text` and `json`. It resolves the job id with
   `resolve_job_id_or_fail`, loads the job with `load_job_plan` (None: `fail("job_not_found",
   ..., exit_code=3)`), resolves the task with `job_plan_cmd._resolve_task_arg`, and calls
   `steer_task_command(..., channel="cli")`. A refusal fails with its own code and detail, exit 2
   for `invalid_message` and `unknown_task`, 3 for `job_not_steerable` and `task_not_steerable`;
   a `SteeringWriteError` fails `steering_write_failed` with exit 1. JSON: `emit_ok(job_id=...,
   **result)`. Text: `f"Note {message_id} recorded for task {task_id} of job {job_id}."` then
   `f"Task {task_id} reads it at the start of its next round; nothing interrupts a model call in
   flight."`. The catalog gains `job.steer` directly after `job.veto-task`, `action_class`
   `write_metadata`, args `_JOB_ID`, `ArgDef("text", ...)`, `ArgDef("--task", ..., required=True,
   is_option=True)` and `_JSON_OPT`, `supports_json=True`, `may_mutate_repo=False`,
   `may_execute_commands=False`, `related=("chat.send", "chat.show", "job.veto-task")`,
   `exit_codes=(0, 1, 2, 3)`, its description naming F030. `apps/cli/commands/__init__.py`
   imports and loops the module as it does `job_veto_cmd`; `docs/guides/exit-codes.md` gains
   `| \`remedy job steer\` | 3 |` directly after `remedy job veto-task`'s row; and
   `tests/orchestration/import_reachability_allowlist.txt` gains
   `apps.cli.commands.job_steer_cmd` where the test that generates it places it.
   `chat_cmd._cmd_chat_show` passes `task_statuses` built from the job's tasks; an addressed row's
   first line reads `via {channel} to task {addressed_to}:` in place of `via {channel}:`, and its
   waiting and not-taken-in lines read `waiting — task {T} has not started a round since it
   arrived` and `not taken in — task {T} finished without starting another round`; a job-wide
   row prints exactly as today.
S4 THE WRITE DOOR, in `ui_server.py`. `JOB_STEER_COMMAND_ID = "job.steer"` after
   `JOB_RERUN_SUBTREE_COMMAND_ID`, commented as DECISION F030 D2's twin of `remedy job steer`.
   `_read_command_payload` refuses a `job.steer` whose `args.task_id` is not a non-empty string
   (field `task_id`, `"task_id must be a non-empty string"`) and then one whose `args.message`
   `normalize_steering_text` refuses (field `message`), before the job is read. A new branch of
   `_handle_command_submission`, placed after the `job.veto-task` branch, is that branch's
   shape exactly — a raise audits `rejected_effect` and answers 500, a refusal audits
   `rejected_state` and answers `409` with `f"{code}: {detail}"`, an acceptance audits
   `accepted`, publishes, emits and answers 200. `_dispatch_steer_task(job, payload)` answers
   `{"command": payload["command"], **steer_task_command(job, args["task_id"],
   args["message"], channel="cockpit")}`. `UI_EXPOSED_COMMANDS` gains `"job.steer"` with a
   DECISION F030 D2 comment. In `tests/ui_server/test_command_channel.py`, and nowhere else in
   that file: `DOOR_METHODS` gains `"_dispatch_steer_task"`; `ALLOWED_IMPORTS` gains
   `("packages.orchestration.steering", "steer_task_command")` with `# F030 D2`, plus any other
   name the new door code imports that the set lacks; `TestUiExposedCommands`'s ruled list gains
   `"job.steer"` in its sorted place; and the exposed-commands loop gains a branch for
   `job.steer` answering 400 on field `task_id`, with one sentence in its docstring.
S5 UNCHANGED: `record_steering_message`, the drain, the segment and the report of round 1, the
   event names, every browser file, and every existing test except the four
   `test_command_channel.py` edits S4 names.

THE TESTS. NEW `tests/orchestration/test_steer_task.py`: each refusal code with nothing written;
the refusal order (an ended job naming an unknown task refuses `job_not_steerable`); `unknown_task`
over eleven tasks naming `and 1 more`; acceptance for each of the five steerable statuses with
the record carrying the task id and channel; refusal for `passed`, `applied_to_job_workspace`,
`split` and `vetoed`; `STEERABLE_TASK_STATUSES == frozenset(task_veto.VETOABLE_TASK_STATUSES)`;
the overview's `addressed_to` and its `not_taken_in` for a finished task's note while the job
runs, and a job-wide row unchanged. NEW `tests/cli/test_job_steer.py`: text and JSON acceptance,
a planned id resolving to its task, exit 2 for an unknown task and an empty text, exit 3 for a
`passed` task and an ended job, and `remedy chat show` naming the task in text and
`addressed_to` in JSON. NEW `tests/ui_server/test_steer_task_door.py`: acceptance writes a record
with channel `cockpit` and the task id and an `accepted` audit line; a `passed` task answers 409
whose error begins `task_not_steerable:`, with a `rejected_state` audit line and no record; an
unknown task answers 409 `unknown_task:`; a missing `task_id` and an empty `message` answer 400
on their fields with no record; an ended job answers 409 `job_not_steerable:`.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — copy this block and the payloads: `.agent/authored/f030-r2-block.md`,
  `.agent/authored/f030-r2-plan.md` and `.agent/authored/f030-r2-booking.diff`, all by
  `shutil.copyfile`. Subject: `F030 R2 C1: copy round 2 block and payloads`
  Its insertions are this block's line count plus 91. Report it; STOP if it is 500 or more.
C2 — THE BOOKING: `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F030 R2 C2: book round 1's PASS and record DECISION F030 D2`
  Expected by `git show --numstat`: 44/0 decisions.md, 2/0 live_review.md, 7/8 plan.md.
C3 — THE COMMAND AND ITS TESTS: S1 and S2 in `steering.py`, and
  `tests/orchestration/test_steer_task.py`.
  Subject: `F030 R2 C3: address a note to a task through one shared command`
C4 — THE COMMAND LINE: S3's files and `tests/cli/test_job_steer.py`.
  Subject: `F030 R2 C4: add remedy job steer and name a note's task in chat show`
C5 — THE WRITE DOOR: S4's files and `tests/ui_server/test_steer_task_door.py`.
  Subject: `F030 R2 C5: expose job.steer through the write door`
C6 — THE TOOL: your mutation tool (G5) as `.agent/authored/f030-r2-mutations.py`.
  Subject: `F030 R2 C6: add the round 2 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F030 R2 C7: rewrite handoff for round 2`
  Then `git push`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f030-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `packages/orchestration/steering.py`, `packages/orchestration/ui_server.py`,
   `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`,
   `apps/cli/commands/job_steer_cmd.py`, `apps/cli/commands/chat_cmd.py`,
   `docs/guides/exit-codes.md`, `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/ui_server/test_command_channel.py`, and the three new test files. Report
   `git diff --name-only 886b6055` at the tip after C7. Do NOT touch `apps/ui/`,
   `packages/orchestration/pingpong_loop.py`, `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/event_names.py`, `.agent/context.md`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md` or `docs/roadmap/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round wrote that is wrong may be corrected
   before C7, and the correction is declared. An EXISTING test that goes red is never edited to
   pass, the four S4 edits apart; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives it to F030's closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the lines, bytes and sha256 you measured against the
 PAYLOADS table. Then compare each `.agent/authored/f030-r2-*` payload copy byte for byte with its
 source (the block copy against `.remedy-wt/f030-r2/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2314513 | 1a38d90282c2796588af0c791e1001d4f237896883d38eaefb6a61df47c294b0 |
 | .agent/live_review.md | 311600 | e7463f7d8d71ec17c7c6f5fa90883d6b4b47e704ab04dafc660b725ea1bc155c |
 | .agent/plan.md | 950 | a14dcd35f5785c74f8cb8a9ab23c202d18b5c5dc673f233e0960e5dddccdcdbc |
 Also the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's TEXT at C2 (the reviewer read it empty), and the ledger's last line at C2,
 which must begin `Gate: F030 R1 — `.

G3 THE CODE — `python3 -m ruff check` over every Python file of constraint 3 that is not under
 `.agent/`, at C6, with its real exit code. Then report, quoted from `git show`, the whole of
 `steer_task_command`, the new `_handle_command_submission` branch and `_dispatch_steer_task`.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_steer_task.py tests/cli/test_job_steer.py tests/ui_server/test_steer_task_door.py tests/orchestration/test_steering_notes.py tests/orchestration/test_steering.py tests/orchestration/test_steering_consumption.py tests/orchestration/test_steering_mission.py tests/cli/test_chat_cmd.py tests/orchestration/test_task_veto.py tests/cli/test_job_veto.py tests/cli/test_command_catalog.py tests/cli/test_advertised_commands.py tests/cli/test_exit_codes.py tests/cli/test_cli_ux.py tests/cli/test_json_contract.py tests/cli/test_job_refusal_envelope.py tests/cli/test_list_commands_everywhere.py tests/cli/test_job_commands.py tests/orchestration/test_dead_command_check.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_rerun_subtree_door.py tests/ui_server/test_sse_stream.py tests/ui_server/test_dashboard_contract.py tests/ui_contracts/test_steering_send_contract.py tests/orchestration/test_event_names.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_test_runner.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the three new test files, serially, in the primary
 checkout at `886b6055`, and read `1859 passed, 1 skipped` at real exit code 0, the skip being
 the F252 quarantine in `tests/test_agent_tooling.py`. Report every `SKIPPED` line, the node
 count of each new test file by `--collect-only -q`, and account for any difference from 1859
 plus those counts plus the nodes the S4 edits add to `test_command_channel.py` (report that
 file's count at `886b6055` and at C6). Then `python3 -m apps.cli.main integrity check --json`,
 which must read all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f030-r2-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_steer_task.py tests/cli/test_job_steer.py
 tests/ui_server/test_steer_task_door.py tests/orchestration/test_steering.py
 tests/cli/test_chat_cmd.py` from the worktree's root after purging its `__pycache__`
 directories, restores the bytes, and prints one line per mutation: its label, the exit code, the
 failed count and the failing node ids. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  m1 `steering.py`: `STEERABLE_TASK_STATUSES` also holds `passed`;
  m2 `steering.py`: `STEERABLE_TASK_STATUSES` loses `failed`;
  m3 `steering.py`: `steer_task_command` records the note without its task id;
  m4 `steering.py`: step c is skipped;
  m5 `steering.py`: step b is skipped;
  m6 `steering.py`: `steering_overview` ignores `task_statuses`;
  m7 `job_steer_cmd.py`: `task_not_steerable` exits 1;
  m8 `job_steer_cmd.py`: the task argument is passed on without `_resolve_task_arg`;
  m9 `ui_server.py`: `_dispatch_steer_task` records with channel `cli`;
  m10 `ui_server.py`: `_read_command_payload`'s `job.steer` check on `task_id` is skipped;
  m11 `ui_server.py`: the new branch answers a refusal 200;
  m12 `chat_cmd.py`: `_cmd_chat_show` passes no `task_statuses`.
 Run it: `git worktree add --detach .remedy-wt/f030-r2-mut <C6>`, then
 `python3 -B .agent/authored/f030-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f030-r2-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f030-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C7 down to C1 and `886b6055` (more lines if
 constraint 2 split a commit); `git worktree list | wc -l`, equal to your step 4 reading; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, INSIDE `.agent/handoff.md`, with EVERY one of
these sections: the Session section, the range, the per-commit changed-files table with the
insertion count you MEASURED beside the one this block expected (none is expected for C3 to C6),
the external actions, every gate's real output and exit code, the authored-text proofs, the
deviations, the ITEM-STATUS TABLE AGENTS.md requires with one row per commit and one per gate,
and the next expected action. Round 1's handback left the item-status table out; it is
mandatory. Report what you ran, not what you expected to find. Your Session section reads
SESSION 1 of feature F030, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T003 — the feed shows the operator's own line, the input addresses the focused task
with copy that promises no conversation, and the end-to-end proof. State the open-findings count,
0, and the operator-questions count, 0.
