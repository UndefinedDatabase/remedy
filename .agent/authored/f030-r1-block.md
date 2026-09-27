STEP F030 R1 — CLAIM F030 AND LAND T001: a steering note addressed to one task, taken in by that task alone at its next round start, carried in one numbered operator-note segment at the steering rank, and listed in the job report when its task finished without it

GOAL
Pull request 288 is merged; `main` is at `15f5d384` and F030 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F029's round 11 verdict, record DECISION
F030 D1, and land T001 on top of F264's steering channel in `packages/orchestration/steering.py`:
an optional task address on a steering message, a drain that lets only the addressed task take a
note in, the `builder_operator_notes` prompt segment, and the job report's listing of notes a
task finished without taking in — plus their tests. No command, no browser code and no event
name is added in this round; that is T002 and T003.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records and the
STATUS line travel as payloads. Read DECISION F030 D1 in the claim diff before you write code: it
is the design this specification implements. Before you write anything, read
`packages/orchestration/steering.py` whole, `compose_builder_prompt`, `_steering_text_for_round`
and SAFE POINT 1 of the round loop of `run_pingpong` (where `_steering_text_for_round` is called
and `builder_compose_args` is built) in `packages/orchestration/pingpong_loop.py`,
`_task_veto_report_map`, `export_job_report` and `format_job_report_text` in
`packages/orchestration/pingpong_job.py`, and `tests/orchestration/test_steering.py`,
`tests/orchestration/test_steering_consumption.py`, `tests/orchestration/test_steering_mission.py`
and the trace-manifest tests of `tests/orchestration/test_builder_prompt_hunk_rejections.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f030-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f030-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f030-r1-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f030-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f030-r1-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `15f5d384`. Report all three. Then
   `git checkout -b feature/f030-steering-messages` and report the branch. Do NOT pull: the Open
   PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f030-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f030-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 141 | 18213 | e3cdb7757158dbc994511a1dbdd9e531323923754f855fc7df4f8993bea20c21 |
| context.md | 36 | 1499 | d9c2c1f100b4c1b38491db60a61ead352a7b0bb207dd1b183fb1f764f8015225 |
| plan.md | 30 | 1059 | 48a396c33275ac0b41c96d8547a928e4e6d8f137e8111e99a6999f6daab6f41e |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`15f5d384` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F029's round 11 gate entry
appended), `docs/roadmap/STATUS.md` (F030's line `[ ]` to `[~]`) and `.agent/decisions.md`
(DECISION F030 D1 appended).

THE SPECIFICATION. No `except Exception` anywhere; every new import of `steering` from
`pingpong_job.py` or `pingpong_loop.py` is function-scoped, as the existing ones are.
S1 THE ADDRESS, in `steering.py`. `record_steering_message(job_id, text, *, job_state, channel,
   task_id="", root=None, now=None)`: a `task_id` that is not a `str` raises
   `SteeringError("the task id must be text")` before anything is written; it is stripped; when
   the stripped value is not "" the record body gains the key `"task_id"` BEFORE its seal is
   computed and the `steering_message_received` event's metadata gains `"task_id"` too; when it
   is "" the body and the metadata are exactly what they are today, key for key. A new
   `note_task_id(record) -> str` answers `str(record.get("task_id", ""))`. The task's status is
   NOT checked here; T002's command does that.
S2 THE DRAIN, in `consume_pending_steering`. A record whose `note_task_id` is not "" and differs
   from `str(task_id)` is skipped: no marker, no event, it stays pending. A record addressed to
   the consuming task gets its marker and its event as today, but its mission is never looked up
   and never amended: its marker's `mission_id` and `amendment_id` are "" and its `understood` is
   `steering_understood(text, task_id, round_number, None)`. The return value is the job-wide
   records alone (`note_task_id` ""), every one of them, oldest first — so `builder_steering`
   never carries a note. The docstring says both in one sentence each and names DECISION F030 D1.
S3 THE NOTES, in `steering.py`. `consumed_task_notes(job_id, task_id, root=None) -> list[dict]`:
   the records addressed to `task_id` that have a consumption marker by
   `list_steering_consumptions`, in the order `list_steering_messages` gives. `OPERATOR_NOTES_HEADING
   = "OPERATOR NOTES (binding):"` and `render_operator_notes_segment(records) -> str`: "" for no
   record, else the heading line, then one line per record `f"{n}. "` plus its text with every
   inner `"\n"` replaced by `"\n   "`, `n` counting from 1, joined with `"\n"`, plus a final
   `"\n"` — the text verbatim, never cut, for the reason `render_steering_segment` gives.
   `unconsumed_task_notes(job_id, task_id, root=None) -> list[dict]`: the records addressed to
   `task_id` with no marker, same order. The module docstring gains one paragraph naming F030
   T001 and DECISION F030 D1.
S4 THE SEGMENT, in `pingpong_loop.py`. `compose_builder_prompt` gains the keyword
   `operator_notes_text: str = ""`; when it is not "" it registers
   `("builder_operator_notes", SegmentStabilityRank.STEERING, [operator_notes_text])` directly
   after the `builder_steering` registration and before `builder_directive`; its docstring gains
   one sentence for it. A new `_operator_notes_text_for_round(job_id, task_id) -> str` answers ""
   when either is "" and otherwise
   `render_operator_notes_segment(consumed_task_notes(job_id, task_id))`. At SAFE POINT 1 it is
   called DIRECTLY AFTER `_steering_text_for_round`, whose call consumes this round's notes, and
   its value reaches `compose_builder_prompt` through `builder_compose_args` as
   `operator_notes_text`. Nothing else in the round loop changes.
S5 THE REPORT, in `pingpong_job.py`. `_task_steering_not_consumed_map(job) -> dict[str, list]`
   reads the job's records and markers ONCE (not per task) and answers, for every task whose
   status is neither `TASK_PENDING` nor `TASK_RUNNING`, the records addressed to it with no
   marker, each as `{"message_id", "text", "received_at"}` in arrival order, omitting a task with
   none; a `SteeringError` from reading them is caught and answers `{}`, with a comment saying
   why, as `_task_veto_report_map` does for its own error. `export_job_report` adds
   `report["steering_not_consumed"]` for a task in that map only, so a job with no such note
   exports the same dict as before. `format_job_report_text` adds, after a task's veto line, one
   line per such note: `"      Steering not consumed: “" + text.replace("\n", "\n        ") + "”"`.
S6 UNCHANGED: `render_steering_segment`, `steering_overview`, `steering_acknowledgements`,
   `normalize_steering_text`, the event names, every existing test, and every file not named in
   constraint 3.

THE TESTS — NEW FILE `tests/orchestration/test_steering_notes.py`, scripted providers only (the
`FakeProvider` pattern of `test_steering_consumption.py`), `REMEDY_DATA_DIR` under `tmp_path`.
At least: a note's record carries `task_id` and passes `verify_steering_record`, and its
received event's metadata carries it; a job-wide record's key set is exactly F264's
(`schema, message_id, job_id, text, channel, received_at, record_sha256`); a task id of `3`
refuses with nothing written; a note to `T2` consumed at a `T1` round writes no marker and no
event and is consumed at the next `T2` round with a marker naming `T2` and that round; the
return value holds a job-wide message and never a note; three notes to one task consumed in one
round render numbered 1 to 3 in arrival order with a two-line note indented, and a second
consume publishes nothing new; a note in a mission's job leaves the contract unamended (the
fixture of `test_steering_mission.py`) with `mission_id` and `amendment_id` ""; the manifest
order `builder_steering, builder_operator_notes, builder_directive` at rank 5 with both texts,
and no `builder_operator_notes` row without one; THE CALL BOUNDARY — a `run_pingpong` with
`job_id` and `task_id` whose provider records a note for that task WHILE round 1's builder call
is in flight: round 1's prompt equals the no-note run's byte for byte, round 2's differs from it
by exactly the segment, and in `result.prompt_traces` the builder entry of round 2 has a
`segment_manifest` row named `builder_operator_notes` at rank 5 and round 1's has none; a note
addressed to another task never appears in any prompt of the run; a note consumed at round 2 is
still in round 3's prompt (a provider that fails rounds 1 and 2); and the report — a `passed`
task with an unconsumed note has `steering_not_consumed` with its id, text and time and the
text report's line, a `pending` task's note and a consumed note give no key, and a job with no
note exports the same keys as before.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f030-r1-block.md` := this block, and `.agent/authored/f030-r1-plan.md` and
  `.agent/authored/f030-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F030 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 66. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f030-r1-claim.diff` := claim.diff.
  Subject: `F030 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 141.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F030 R1 C2: claim F030, re-head the live review record, book F029 R11, record D1`
  Expected by `git show --numstat` (insertions and deletions): 14/15 context.md, 58/0
  decisions.md, 22/22 live_review.md, 16/13 plan.md, 1/1 STATUS.md.

C3 — THE CODE: `packages/orchestration/steering.py`, `packages/orchestration/pingpong_loop.py`
  and `packages/orchestration/pingpong_job.py`.
  Subject: `F030 R1 C3: address a steering note to one task and carry it in that task's rounds`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_steering_notes.py` and your mutation tool
  (G5) saved as `.agent/authored/f030-r1-mutations.py`.
  Subject: `F030 R1 C4: test task-addressed steering notes and add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F030 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f030-steering-messages`. Do NOT create a pull request: the
  branch opens one at F030's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f030-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/steering.py`,
   `packages/orchestration/pingpong_loop.py`, `packages/orchestration/pingpong_job.py`,
   `tests/orchestration/test_steering_notes.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 15f5d384` at the branch tip after C5. Do NOT touch anything
   under `apps/`, `packages/orchestration/ui_server.py`, `packages/orchestration/event_names.py`,
   `apps/cli/command_catalog.py`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md` or `docs/roadmap/features/T5_F030.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F030's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f030-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f030-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | docs/roadmap/STATUS.md | 55545 | 0c5c09c94167969bd49fa368365766da77d8a3656610d738fd31454ec1364975 |
 | .agent/live_review.md | 308465 | 76e75e2e49c270cdf91bc8f9529cfd6e100dd2a61ec987b66b6f7a7a7d10a136 |
 | .agent/decisions.md | 2310781 | 086c7732c203edcf6a428f0ebca886763c91f769f1795e11b02189972a9823ad |
 | .agent/plan.md | 1059 | 48a396c33275ac0b41c96d8547a928e4e6d8f137e8111e99a6999f6daab6f41e |
 | .agent/context.md | 1499 | d9c2c1f100b4c1b38491db60a61ead352a7b0bb207dd1b183fb1f764f8015225 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `15f5d384` and at C2 (the reviewer read
 it empty at both); at C2 the ledger has exactly one line reading `## Findings` and exactly one
 reading `## Steps`, and its last line begins `Gate: F029 R11 — `; F030's STATUS line at C2 read
 back in full, which must read `- [~] F030 — Steering messages`; and `git diff --name-only <C1b>
 <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/steering.py
 packages/orchestration/pingpong_loop.py packages/orchestration/pingpong_job.py
 tests/orchestration/test_steering_notes.py` at C4, with its real exit code. Then report, quoted
 from `git show <C3>`, the whole of the new `consume_pending_steering` loop body, the
 `builder_operator_notes` registration with the two registrations around it, and SAFE POINT 1's
 two calls.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_steering_notes.py tests/orchestration/test_steering.py tests/orchestration/test_steering_consumption.py tests/orchestration/test_steering_mission.py tests/cli/test_chat_cmd.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_builder_prompt_hunk_rejections.py tests/orchestration/test_prompt_trace.py tests/orchestration/test_prompt_cache_prefix.py tests/orchestration/test_prompt_segments.py tests/orchestration/test_semantic_dedupe.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_pause_resume.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_token_ledger.py tests/test_role_override_flags.py tests/ui_server/test_command_channel.py tests/ui_server/test_sse_stream.py tests/ui_contracts/test_steering_send_contract.py tests/orchestration/test_event_names.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py tests/orchestration/test_mint_call_sites.py tests/orchestration/test_manual_completion_bundle.py tests/orchestration/test_run_manifest_strict_boundaries.py tests/orchestration/test_human_change_one_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less `tests/orchestration/test_steering_notes.py`, serially, in
 the primary checkout at `15f5d384` before any change, in two runs over disjoint files, and read
 `1695 passed, 1 skipped` and `37 passed`, both at real exit code 0. The skip is the F252
 quarantine in `tests/test_agent_tooling.py` and stays skipped. Report every `SKIPPED` line the
 `-rs` summary prints, the node count of `tests/orchestration/test_steering_notes.py` by
 `--collect-only -q`, and account for any difference from 1732 plus that count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f030-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_steering_notes.py tests/orchestration/test_steering.py
 tests/orchestration/test_steering_consumption.py tests/orchestration/test_steering_mission.py`
 from the worktree's root after purging its `__pycache__` directories, restores the bytes, and
 prints one line per mutation: its label, the exit code, the failed count and the failing node
 ids. It runs an unmutated control first and last and ends with `restored byte-identical: True`
 and a final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour
 change:
  m1 `steering.py`: the drain consumes a note addressed to another task;
  m2 `steering.py`: the drain returns the notes with the job-wide records;
  m3 `steering.py`: a note amends the mission's contract as a job-wide message does;
  m4 `steering.py`: the notes are numbered from 0;
  m5 `steering.py`: a job-wide record always carries `"task_id": ""`;
  m6 `pingpong_loop.py`: `compose_builder_prompt` never registers `builder_operator_notes`;
  m7 `pingpong_loop.py`: `builder_operator_notes` is registered after `builder_directive`;
  m8 `pingpong_loop.py`: SAFE POINT 1 passes "" as `operator_notes_text`;
  m9 `pingpong_job.py`: the report lists a consumed note;
  m10 `pingpong_job.py`: the report lists a note of a `pending` task;
  m11 `pingpong_job.py`: the text report leaves out the `Steering not consumed:` line.
 Run it: `git worktree add --detach .remedy-wt/f030-r1-mut <C4>`, then
 `python3 -B .agent/authored/f030-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f030-r1-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f030-r1-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `15f5d384` in that order
 (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal your
 step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F030, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — the write door's `job.steer-task` and `remedy job steer` with the task state
gate, the audit and the event. State the open-findings count, 0, and the operator-questions
count, 0.
