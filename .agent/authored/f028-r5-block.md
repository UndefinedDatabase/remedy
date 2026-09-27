STEP F028 R5 — BOOK ROUND 4 AND REGISTER R-1078, RECORD D5, REPAIR R-1078, AND LAND THE WRITE DOOR'S THREE INJECTION COMMANDS AND THE RUN-LOG EVENT `task_injected` WITH ITS TWO READERS

GOAL
Round 4 passed. Book its gate entry, R-1078's registration and two prose slips, and record
DECISION F028 D5. Repair R-1078. Then let the browser inject: the write door accepts
`job.inject`, `job.inject-confirm` and `job.inject-answer`, checks their arguments before it reads
the job, and runs them through one dispatch method with the door's own actor; and the runner's
fold writes one `task_injected` event per injection it folds, declared in `EVENT_NAMES` and
humanized in `STREAM_EVENT_CATALOG`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests against S1 to S5. Read DECISION F028 D5 in `.agent/decisions.md` (it
arrives with C2) and, whole, the `job.veto-task` branch of `_handle_command_submission`,
`_dispatch_veto_task` and the veto check of `_read_command_payload` in
`packages/orchestration/ui_server.py`, and `TestVetoTaskDispatchEffects` in
`tests/ui_server/test_command_dispatch.py`: S3 and its tests copy their shape.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r5/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/` to `.remedy-wt/f028-r5-sim/`  The reviewer's simulation trees.
  `.remedy-wt/f028-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f028-r5-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx yourself; the vitest node of G4 runs it through pytest.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f028-task-injection`, and `git log --oneline -1` must read `6814c686`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 30 | 1068 | ea6ff390bddb5c46d3030febe9f9ea4ae399426aaf1d04cbe09c118419750265 |
| records.diff | 71 | 13248 | 074a99b06ed1a9a9b18e8f1e4cc924d29a5c45a49e76fb0093f741b749f9e8c2 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; it appends
round 4's gate entry and R-1078's registration to `.agent/live_review.md`, DECISION F028 D5 to
`.agent/decisions.md`, and two lines to `.agent/prose_slips.md`.

THE SPECIFICATION
S1 R-1078, in `apps/cli/commands/job_inject_cmd.py`: `_cmd_inject` under `--yes` over a shortfall
   calls `emit_ok` never; with `--json` it calls only `fail("draft_needs_decision", ...,
   exit_code=EXIT_NOT_READY, job_id=job_id, draft_id=..., decision_seed=..., budget_check=...)`,
   and without `--json` it prints the seed as today and then fails the same way.
S2 THE RESOLVER, in `packages/orchestration/task_injection.py`: `resolve_after_ref(job, ref) ->
   str | None` answers None for None; `ref` when it is a task id of the job's plan; the
   `inputs["plan"]["planned_id"]` of the entry of `job.tasks` whose `task_id` is `ref`, when it
   has one; otherwise `ref` unchanged, which the draft pass then refuses as `unknown_task`.
S3 THE DOOR, in `packages/orchestration/ui_server.py`. Constants `JOB_INJECT_COMMAND_ID =
   "job.inject"`, `JOB_INJECT_CONFIRM_COMMAND_ID = "job.inject-confirm"`,
   `JOB_INJECT_ANSWER_COMMAND_ID = "job.inject-answer"` beside `JOB_VETO_TASK_COMMAND_ID`, and
   `JOB_INJECT_COMMAND_IDS` a `frozenset` of the three. `_read_command_payload`, directly after
   the veto check, refuses with `_command_field_error`: for `job.inject`, an `args["text"]`
   `validate_injection_text` refuses (field `text`, its detail) and an `args["after"]` present and
   not a non-empty `str` (field `after`); for `job.inject-confirm`, an `args["confirm_token"]`
   that is not a non-empty `str` (field `confirm_token`); for `job.inject-answer`, an
   `args["draft_id"]` that is not a non-empty `str` (field `draft_id`) and an `args["option"]`
   outside `SHORTFALL_OPTIONS` (field `option`). `_handle_command_submission` gains, directly
   after the veto branch, one branch for `payload["command"] in JOB_INJECT_COMMAND_IDS`, the veto
   branch's body with `self._dispatch_injection(job, payload)` in place of its dispatch call.
   `_dispatch_injection(self, job, payload) -> dict` imports each name it uses with
   `from packages.orchestration.task_injection import ...`, takes
   `token_fingerprint(self._supplied_bearer_token())` as the actor, and for `job.inject` and
   `job.inject-answer` reads `injection_budget_inputs(job)`, a `TaskInjectionRefused` there
   answering `{"outcome": "refused", "code", "detail"}`; `job.inject` passes
   `resolve_after_ref(job, args.get("after"))` and `call_fn=injection_call_fn()`; each answers
   `{"command": payload["command"], **result}`. `UI_EXPOSED_COMMANDS` in
   `apps/cli/command_catalog.py` gains the three ids after `"job.veto-task"`, under one comment
   naming DECISION F028 D5.
S4 THE DOOR'S GUARDS, in `tests/ui_server/test_command_channel.py`, the ONLY edits this round
   makes to tests it did not write: `test_the_set_holds_exactly_the_ruled_ids_and_no_other`'s
   sorted literal gains the three ids in their sorted places; `TestCommandDoorImportGuard`'s
   `DOOR_METHODS` gains `"_dispatch_injection"` and `ALLOWED_IMPORTS` gains exactly the
   `("packages.orchestration.task_injection", <name>)` pairs the door's two methods import, each
   commented `# F028 D5`; and `test_every_exposed_command_reaches_the_answer_its_effect_gives`
   gains, before its `else`, the branches `job.inject` → 400 on field `text`,
   `job.inject-confirm` → 400 on field `confirm_token`, `job.inject-answer` → 400 on field
   `draft_id`, with one sentence per id added to its docstring. The reviewer wired a door method
   importing eight names of `task_injection` in its simulation tree and read the import guard's
   seven tests green with `DOOR_METHODS` and `ALLOWED_IMPORTS` so extended, so no new module
   reaches the transitive forbidden set.
S5 THE EVENT. `_fold_task_injections` in `packages/orchestration/pingpong_job.py` collects each
   record it folds and, AFTER its `_persist_job`, writes through `RunLogWriter(job.job_id)` one
   `log("task_injected", outcome=..., task_id=..., draft_id=..., planned_id=..., basis=...,
   actor=..., confirmed_unseen=...)` per record: outcome `applied` and `task_id` the new entry's
   id, or outcome `inert` with `task_id` "" and a `reason` keyword carrying the inert detail. A
   comment names DECISION F028 D5 (2) and why the write follows the save. `EVENT_NAMES` in
   `packages/orchestration/event_names.py` gains `"task_injected"` between
   `"task_decision_answered"` and `"task_lesson_written"`, and `STREAM_EVENT_CATALOG` in
   `apps/ui/src/api/humanizeCatalog.ts` gains, between its `task_gate_evaluated` and
   `task_lesson_written` lines, the line
   `  "task_injected": "A task the operator added joined the job's plan.",`.

THE TESTS
In `tests/cli/test_job_inject.py`: `--yes --json` over a shortfall leaves stdout parseable as
exactly one JSON document, an error envelope with code `draft_needs_decision` carrying the draft
id and the seed. In `tests/orchestration/test_task_injection.py`: S2's four answers. In
`tests/orchestration/test_task_injection_runner.py`: a folded injection writes exactly one
`task_injected` event, outcome `applied`, its `task_id` the new entry's; an inert fold writes
one with outcome `inert` and its reason; a second run writes none. A NEW class
`TestInjectionDispatchEffects` in `tests/ui_server/test_command_dispatch.py`, built as
`TestVetoTaskDispatchEffects` is but over a running job with a stored task plan and with
`task_injection.injection_call_fn` and `injection_budget_inputs` monkeypatched: a drafted `job.inject`
answering 200 with `outcome` `drafted`, its `actor` the token's fingerprint and one draft file on
disk; `after` by the entry id reaching the draft's `depends_on` as the planned id; a
`job.inject-confirm` answering 200 `confirmed` with one confirmation file; a second confirm 409
`already_confirmed`; `job.inject-answer` `drop` answering 200 `dropped` over a shortfall draft;
a bad text 400 on field `text` and a bad option 400 on field `option`, with no control file
written by either; and a terminal job 409 `job_terminal`.

BUNDLE — the commits are C1 to C7, in this order.
C1 — copy this block and the payloads: `.agent/authored/f028-r5-block.md`,
  `.agent/authored/f028-r5-records.diff`, `.agent/authored/f028-r5-plan.md`, by
  `shutil.copyfile`. Subject: `F028 R5 C1: copy round 5 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 101; STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F028 R5 C2: book round 4, register R-1078, record D5 and two prose slips`
  Expected by `git show --numstat`: 41/0 decisions.md, 4/0 live_review.md, 9/9 plan.md, 2/0 prose_slips.md.
C3 — S1 and S2: `apps/cli/commands/job_inject_cmd.py`, `packages/orchestration/task_injection.py`.
  Subject: `F028 R5 C3: repair R-1078 and resolve an after reference for the door`
C4 — S3 and S4: `packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
  `tests/ui_server/test_command_channel.py`.
  Subject: `F028 R5 C4: accept job.inject, job.inject-confirm and job.inject-answer at the write door`
C5 — S5: `packages/orchestration/pingpong_job.py`, `packages/orchestration/event_names.py`,
  `apps/ui/src/api/humanizeCatalog.ts`.
  Subject: `F028 R5 C5: write task_injected when the runner folds an injection`
C6 — THE TESTS AND THE TOOL: the four test files of THE TESTS and
  `.agent/authored/f028-r5-mutations.py`. Subject: `F028 R5 C6: test the door's injection commands, the event, the resolver and R-1078`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F028 R5 C7: rewrite handoff for round 5`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C4 and C6 before you
   commit them; a commit that would reach 500 is split into parts with their own subjects, each
   part leaving the selection of G4 green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r5-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`, the
   paths C3, C4 and C5 name, `tests/cli/test_job_inject.py`,
   `tests/orchestration/test_task_injection.py`,
   `tests/orchestration/test_task_injection_runner.py`, `tests/ui_server/test_command_dispatch.py`,
   and `.agent/handoff.md`. Report the list `git diff --name-only 6814c686` measures after C7.
   Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test THIS round
   wrote that is wrong may be corrected before C7, and the correction is declared. An existing
   test goes red and is edited only where S4 orders it; any other is reported, and you stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F028 one full-suite run, at its closure.
8. No `except Exception` in any production line this round writes.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table; then compare each `.agent/authored/f028-r5-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r5/block.md`), read back with
 `git show <C1>:<path>`. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 324718 | 5d5ee90fbaf255e3ee9befcb173084925160b6361d4d9ac13b1e039b8897f653 |
 | .agent/decisions.md | 2266429 | 13170b346f8391108eb1caf8109ad1b578b754818d03de035ff0df3a6e615eaf |
 | .agent/prose_slips.md | 373059 | 004c013e1b9fa07327841c8233ab268e2b3db59f6f48bdbddcac7767240896c4 |
 | .agent/plan.md | 1068 | ea6ff390bddb5c46d3030febe9f9ea4ae399426aaf1d04cbe09c118419750265 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at
 `6814c686` and at C2 (the reviewer read `[]` and `['R-1078']`), and `git diff --name-only <C1>
 <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check apps/cli/commands/job_inject_cmd.py
 packages/orchestration/task_injection.py packages/orchestration/ui_server.py
 apps/cli/command_catalog.py packages/orchestration/pingpong_job.py
 packages/orchestration/event_names.py tests/ui_server/test_command_channel.py
 tests/ui_server/test_command_dispatch.py tests/cli/test_job_inject.py
 tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py` at
 C6, with its real exit code. Then quote from the diff `_dispatch_injection` whole, the new
 branch of `_handle_command_submission`, the new checks of `_read_command_payload`, and the event
 write of `_fold_task_injections`.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py tests/cli/test_job_inject.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_sse_stream.py tests/orchestration/test_event_names.py tests/ui_contracts/test_humanize_catalog.py tests/ui_contracts/test_veto_controls_contract.py tests/orchestration/test_teacher_narration.py tests/ui_contracts/test_phase_mapping.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/test_command_catalog.py tests/orchestration/test_dead_command_check.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `6814c686` and read
 `1500 passed, 7 skipped` at real exit code 0; the seven skips are the F252 quarantines. Report
 every `SKIPPED` line, the node counts of the edited test files by `--collect-only -q` at
 `6814c686` and at C6, and account for any difference from 1500 beyond the nodes the round adds.
 Then `python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f028-r5-mutations.py` takes a worktree path and,
 for each mutation below, edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/cli/test_job_inject.py tests/orchestration/test_task_injection.py
 tests/orchestration/test_task_injection_runner.py tests/ui_server/test_command_dispatch.py
 tests/ui_server/test_command_channel.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: label, exit
 code, failed count, failing node ids. An unmutated control runs first and last; it ends with
 `restored byte-identical: True` per file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `--yes --json` over a shortfall calls `emit_ok` before `fail` again (job_inject_cmd.py);
  m2 `resolve_after_ref` never maps an entry id to its planned id (task_injection.py);
  m3 the door's `job.inject` check never calls `validate_injection_text` (ui_server.py);
  m4 the door's `option` check admits any string (ui_server.py);
  m5 `_dispatch_injection` passes `after` unresolved (ui_server.py);
  m6 `_dispatch_injection` names the actor `"cli"` (ui_server.py);
  m7 the injection branch answers a refusal with 200 (ui_server.py);
  m8 the fold writes no `task_injected` event for an applied record (pingpong_job.py);
  m9 the fold writes the event for an inert record with outcome `applied` (pingpong_job.py).
 Run it: `git worktree add --detach .remedy-wt/f028-r5-mut <C6>`, then
 `python3 -B .agent/authored/f028-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r5-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, and you then add the test that catches it in C6 before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r5-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, empty; `git log --oneline -n 8`, showing
 C7 back to C1 and `6814c686` in order (more lines if constraint 2 split a commit);
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit, per gate and for R-1078), the deviations, and the next expected action. Name the
commit that lands R-1078's repair; write no `Done:` or `Landed:` line into the ledger. Your
Session section reads SESSION 1 of feature F028, round 5, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then the send module, the Add Task sheet and the provenance chip. State the
open-findings count, 1 (R-1078, its repair awaiting review), and the operator-questions count, 0.
