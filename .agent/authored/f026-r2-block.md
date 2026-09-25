STEP F026 R2 — T002: `job.edit-task` in the catalog, the CLI and the write door, the spec version in `job plan-show`, the trace proof on a fake run, and the repair of R-1059

GOAL
Round 1 passed. Book it, register R-1059, record DECISION F026 D2, then: repair R-1059 (`run_job`
clears the job's stale `error` when a relaunch starts running), close round 1's one unmet test
obligation, and land T002 — the runtime edit reaches the operator as `job.edit-task` through the
catalog, the CLI and the write door with its audit, `job plan-show` shows each task's spec version,
and a fake run proves the next run's prompt trace carries the edit and no remnant of the old spec.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge, and you never write a `Done:` paragraph: when R-1059's fix
lands you append ONE line to `.agent/live_review.md`, exactly
`Landed: R-1059 — <one line: what changed, which commit>`. THE PRODUCTION CHANGE IS SPECIFIED, NOT
SLICED: you write the code and its tests against S1 to S9 below. Only the `.agent/` records travel as
payloads. Read DECISION F026 D1 and D2 in `.agent/decisions.md` (D2 arrives with C1b) before code.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f026-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f026-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f026-r2-dry/`, `.remedy-wt/f026-r2-sim/`, `.remedy-wt/f026-r2-drafts/` and
  `.remedy-wt/f026-r1-drafts/`    The reviewer's; do not touch them.
  `.remedy-wt/f026-r2-worker/`    YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
`for` loops, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture
real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you
pipe pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the file.
Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f026-task-edit-runtime`, and `git log --oneline -1` must read `ee874cb2`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f026-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f026-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1104 | 1de25789543af4d85db2a056ce89a37ec02e7d6b58577f599bc9cf7bfe480a97 |
| records.diff | 69 | 12896 | 0a5a6c6877112c41e880102013eb0ee68f89e77c7d393acadcea461edbe128bd |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `ee874cb2`. It appends to `.agent/live_review.md`
the gate entry of round 1 and the registration of R-1059, and to `.agent/decisions.md` DECISION
F026 D2.

THE SPECIFICATION
S1 R-1059. In `run_job` in `packages/orchestration/pingpong_job.py`, where the job's state becomes
   `JOB_RUNNING` before the dispatch loop and is persisted, the job's `error` becomes `""` in the
   same persist, with a one-line comment naming R-1059. Nothing else in that file changes.
S2 ROUND 1's OBLIGATION. `_assert_refused` in `tests/orchestration/test_task_edit_runtime.py` also
   records, before the call, the sorted names of the files directly in
   `job_evidence_export_dir(job_id, root)` (none when it does not exist) and requires them unchanged
   after it, so a refusal that wrote `plan_v<n>.md` or the edit-log export reds.
S3 THE CATALOG. `apps/cli/command_catalog.py` gains `job.edit-task`: group `job`, subcommand
   `edit-task`, `write_metadata`, exit codes (0, 1, 2, 3), `supports_json`, placed directly after
   `job.plan-edit-task`, and joins `UI_EXPOSED_COMMANDS` with a comment naming DECISION F026 D2. Its
   args, in order: the job id (`_JOB_ID`); a positional `task_id` described EXACTLY as
   "The task: its id in the job, or its id in the job plan"; the option `--spec-version` described
   EXACTLY as "The spec version of the task that `remedy job plan-show` prints; an edit made against
   an older one is refused (required)"; then `--title`, `--goal`, `--acceptance` (repeatable),
   `--band` and `--files-hint` (repeatable) exactly as `job.plan-edit-task` declares them; then
   `_JSON_OPT`. Its description must use the word "run" or "job plan" wherever it uses "task" (the
   vocabulary guard `tests/docs/test_vocabulary.py` requires it of every description naming a task;
   the two arg texts above satisfy it). `docs/guides/exit-codes.md` gains, in its
   `| Command | Exit codes |` table and in that table's own format, the row for `remedy job edit-task`
   with the exit code 3, directly after the row of `remedy job plan-edit-task`.
S4 THE CLI HANDLER, in `apps/cli/commands/job_plan_cmd.py`, registered in its `COMMAND_HANDLERS`
   as `job.edit-task`. It refuses a missing `--spec-version` as `missing_spec_version` and a
   non-integer one as `invalid_spec_version`, both exit 2, before the job is read; loads the job
   with the module's `_load`; resolves the task argument — an argument equal to a task entry's id is
   that entry, otherwise an argument equal to exactly one entry's `inputs["plan"]["planned_id"]` is
   that entry, otherwise the argument passes through unchanged; builds `fields` with
   `_edit_task_args`; calls `edit_task_at_runtime` with actor `CLI_ACTOR`. Refusals: exit 2 for
   `invalid_args`, `unknown_task`, `unknown_command` and `not_a_plan_task`; exit 3 for
   `job_not_found`, `no_task_plan`, `plan_not_editable`, `version_conflict`, `lock_timeout`,
   `job_not_editable`, `task_not_editable` and `spec_archive_conflict`; exit 1 otherwise; every
   refusal carries `current_version`. `--json` success emits `job_id`, `task_id`, `planned_id`,
   `state`, `spec_version`, `plan_version` and `restored`; text success prints one sentence naming
   the planned id, the job and the new spec version, and, for the `failed` state, a second naming the
   relaunch command `remedy job run <job id>`.
S5 `job plan-show` (`_cmd_plan_show` in the same file): each task of the JSON gains `job_task_id`,
   `status` and `spec_version` from the task entry whose planned id matches (`""`, `""` and 1 when
   none does); the text prints, directly under each task's `goal:` line, one line
   `  spec version <n> · <status>`. No existing key or line changes.
S6 THE DOOR, `packages/orchestration/ui_server.py`: a constant `JOB_EDIT_TASK_COMMAND_ID =
   "job.edit-task"`; in `_read_command_payload`, for that command, `args.expected_version` that is
   not a whole number of at least 1 is refused 400 on field `expected_version` with a new constant
   message naming the task's spec version, before the job is read; a public
   `task_edit_refusal(code, detail, current_version)` answering `job_not_editable`,
   `task_not_editable`, `not_a_plan_task` and `spec_archive_conflict` with 409, outcome
   `rejected_state`, and a body holding a new constant message and the backend's `detail`, and
   handing every other code to `plan_edit_refusal`; a new method `_dispatch_edit_task` calling
   `edit_task_at_runtime(job_id, args.get("task_id"), args.get("fields"),
   expected_spec_version=args["expected_version"], actor=token_fingerprint(<the request's token>))`
   and returning the body `command`, `outcome` `accepted`, `task_id`, `state`, `spec_version`,
   `version` (the plan's) and `restored`; and in `_handle_command_submission` a clause for the
   command, placed directly after the plan edits' clause, with exactly that clause's write order,
   refusal handling and audit calls, `task_edit_refusal` in place of `plan_edit_refusal`.
S7 THE GUARDS the door and the catalog widen, each in the commit that widens it:
   `tests/ui_server/test_command_channel.py` — `test_the_set_holds_exactly_the_ruled_ids_and_no_other`
   gains `job.edit-task`; in `test_every_exposed_command_reaches_the_answer_its_effect_gives` the
   plan edits' branch (`command_id.startswith("job.plan-")`) also takes `job.edit-task`, which
   answers 400 on `expected_version`; `TestCommandDoorImportGuard.DOOR_METHODS` gains
   `_dispatch_edit_task` and its `ALLOWED_IMPORTS` gains
   `("packages.orchestration.task_edit_runtime", "edit_task_at_runtime")` with the comment
   `# F026 D2`; `tests/orchestration/import_reachability_allowlist.txt` gains
   `packages.orchestration.task_edit_runtime` in its sorted place; and `tests/test_no_orphan_modules.py`
   loses the `ALLOWED_UNWIRED` entry round 1 added. The reviewer applied exactly these in its
   scratch tree and the door's guard sets `FORBIDDEN_MODULES`, `STORAGE_ALLOWED_NAMES` and
   `ACCEPTED_TRANSITIVE_FORBIDDEN` needed no change.
S8 THE TRACE PROOF — T5_F026.md, verbatim: "Prompt-trace assertion: the next run's evidence must
   contain the v2 content (an automated test greps the trace — the feature's proof)." and "The v2
   prompt-trace grep passes; a v1 remnant in the new trace fails the test." A class in
   `tests/orchestration/test_task_edit_runtime.py`: an approved two-task plan (each task's
   `files_hint` naming a file the repo fixture holds, as `tests/orchestration/test_plan_edit_execution.py`
   builds it, with `repo_path` set) whose first task's goal and acceptance carry a unique OLD marker;
   `run_job` with `FakeProvider(pass_on_round=99)` as builder and reviewer, `max_rounds=1`,
   `repair_rounds=0`, which must end the job `blocked`, the first task `blocked` and the second
   `skipped`; `edit_task_at_runtime` replacing the goal and acceptance with a unique NEW marker; a
   second `run_job` with `FakeProvider(pass_on_round=1, fail_on_round=99)` for both roles,
   `max_rounds=3`, `repair_rounds=0`, which must end `completed` with both tasks
   `applied_to_job_workspace` and the job's `error` `""` (R-1059); then, for the first task's NEW
   run id, `run_dir(run_id) / "prompt_trace.jsonl"`: its builder entries' `prompt_text_redacted`
   contain NEW and do not contain OLD, while the OLD run's trace still contains OLD; and after
   `export_job_evidence(job_id, <tmp dir>)`, the copy under `task_runs/<first task id>/` contains NEW
   and not OLD. The reviewer ran this flow in a scratch tree at `ee874cb2` with S1 applied and read
   exactly those outcomes.
S9 SIZE. Every commit stays under 500 inserted lines; split one that would reach it into parts with
   their own subjects, and say so.

THE TESTS beyond S2 and S8, each in the file named after the source it covers:
`tests/cli/test_job_plan_cmd.py` — `job edit-task` accepted by task entry id and by planned id, with
the JSON body read back and `spec_version` 2 in the record; each refusal class with its exit code
and error (missing and non-integer `--spec-version`, a stale version, a running job, a passed task,
a task without a planned id, an unknown field); the failed state's text naming `remedy job run`;
and `job plan-show`'s three new keys and its new text line, before and after an edit.
`tests/ui_server/test_command_dispatch.py`, a new class beside `TestPlanEditDispatchEffects` and
built the way it is: `job.edit-task` accepted with its body, the edit log's actor the request's
token fingerprint, the audit record `accepted`; a missing `expected_version` 400 on that field with
the job untouched; each runtime refusal 409 `rejected_state` with the detail, audited as such; a
stale version 409 with `current_version`.

BUNDLE — in this order.
C1a — `.agent/authored/f026-r2-block.md` := this block, `.agent/authored/f026-r2-plan.md` :=
  plan.md, `.agent/authored/f026-r2-records.diff` := records.diff, all by `shutil.copyfile`.
  Subject: `F026 R2 C1a: copy round 2 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 100. Report the number you measure.
C1b — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F026 R2 C1b: book round 1, register R-1059, record D2`
  Expected by `git show --numstat`: 49/0 .agent/decisions.md, 4/0 .agent/live_review.md, 9/14 .agent/plan.md.
C2 — S1, and the `Landed: R-1059 — ` line appended to `.agent/live_review.md`.
  Subject: `F026 R2 C2: clear a relaunched job's stale error when it starts running (R-1059)`
C3 — S2. Subject: `F026 R2 C3: a refused runtime edit leaves the export directory unchanged`
C4 — S3, S4 and S5 with their guards from S7 (the exposed set).
  Subject: `F026 R2 C4: job.edit-task in the catalog and the CLI, and the spec version in plan-show`
C5 — S6 with its guards from S7 (the door's methods and imports, the allowlist, the orphan entry).
  Subject: `F026 R2 C5: the door dispatches job.edit-task`
C6 — the tests of S8 and THE TESTS. Subject: `F026 R2 C6: test job.edit-task and prove the next
  run's trace carries the edit`
C7 — your mutation tool (G5) as `.agent/authored/f026-r2-mutations.py`.
  Subject: `F026 R2 C7: the round's red-proof mutation tool`
C8 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F026 R2 C8: rewrite handoff for round 2`
  Then `git push origin feature/f026-task-edit-runtime` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real `git apply`
   and report its exit code.
2. The round's whole tracked path set is: the `.agent/authored/f026-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/pingpong_job.py`, `packages/orchestration/ui_server.py`,
   `apps/cli/command_catalog.py`, `apps/cli/commands/job_plan_cmd.py`,
   `docs/guides/exit-codes.md`, `tests/orchestration/test_task_edit_runtime.py`,
   `tests/cli/test_job_plan_cmd.py`, `tests/ui_server/test_command_dispatch.py`,
   `tests/ui_server/test_command_channel.py`, `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/test_no_orphan_modules.py`, and `.agent/handoff.md`. Report the list
   `git diff --name-only ee874cb2` gives after C8. Do NOT touch
   `packages/orchestration/task_edit_runtime.py`, `packages/orchestration/plan_editing.py`,
   `packages/orchestration/long_run_executor.py`, `apps/ui/`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md` or
   `docs/roadmap/features/T5_F026.md`. If a guard outside this set goes red, STOP and hand back.
3. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
4. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
5. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already listed
   at your step 4, and every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is
   removed as that step's last action, and `git worktree list` is reported afterwards.
6. DO NOT run the full suite: amend0917 rule 1 gives F026 exactly one, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C8 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table; then
 each `.agent/authored/f026-r2-*` payload copy compared byte for byte with its source (the block copy
 against `.remedy-wt/f026-r2/block.md`), read back with `git show <C1a>:<path>`.

G2 THE RECORDS — at C1b, `git show <C1b>:<path>` of each file below hashes to the reviewer's reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 317479 | e6187e0747c474f67f1ea514493bb21a7a5799bebefcbf952337212f8cbfb97e |
 | .agent/decisions.md | 2131684 | 2172168d78f16fe12ef96a865d5445769dc41b67fe4ff7d5914ebd7c8a710510 |
 | .agent/plan.md | 1104 | 1de25789543af4d85db2a056ce89a37ec02e7d6b58577f599bc9cf7bfe480a97 |
 and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text reads R-1008,
 R-1055, R-1057 and R-1058 at `ee874cb2` and those four plus R-1059 at C1b and at C7; the ledger's
 last line at C2 begins `Landed: R-1059 — `.

G3 THE CODE — `python3 -m ruff check` over every `.py` path of constraint 2 at C7; and
 `git diff --numstat ee874cb2 <C7> -- packages/orchestration/pingpong_job.py`, which must read 1 or
 2 insertions and 0 deletions.

G4 THE TESTS — in the primary checkout at C7, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_edit_runtime.py tests/cli/test_job_plan_cmd.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_command_channel.py tests/cli/test_exit_codes.py tests/test_command_catalog.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/cli/test_job_refusal_envelope.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_pause_resume.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_plan_edit_execution.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT `tests/orchestration/test_task_edit_runtime.py` and the
 golden path, serially, in a tree at `ee874cb2` carrying this round's records, and read
 `1467 passed, 2 skipped` at exit 0; the vitest node of `tests/orchestration/test_test_runner.py` skipped there
 and must PASS in your run, and the D12 quarantine in `tests/test_agent_tooling.py` stays skipped.
 Report every `SKIPPED` line, the nodes each test file you changed contributes (`--collect-only -q`
 on it at `ee874cb2` and at C7), and account for every other difference. Then
 `python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool takes a worktree path; for each mutation it edits the named file
 INSIDE that worktree (asserting its FROM text occurs exactly once), purges `__pycache__`, runs
 `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_task_edit_runtime.py`, `tests/cli/test_job_plan_cmd.py` and
 `tests/ui_server/test_command_dispatch.py` from the worktree's root, restores the bytes, and prints
 label, exit code, failed count and failing node ids; an unmutated control runs first and last; it
 ends with `restored byte-identical: True` per file and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations:
  m1 `run_job` leaves `error` as it was when the job starts running (pingpong_job.py);
  m2 the edit no longer updates the entry's `title` (task_edit_runtime.py) — the v1 remnant;
  m3 the reset no longer restores the skipped tasks after the reset task (task_edit_runtime.py);
  m4 the door admits `job.edit-task` without `expected_version`;
  m5 `task_edit_refusal` answers `task_not_editable` with 500;
  m6 the door's dispatcher names the actor `"door"` instead of the token fingerprint;
  m7 the CLI exits 1 for `task_not_editable`;
  m8 the CLI does not resolve a planned id to its task entry;
  m9 the CLI reads a missing `--spec-version` as 1;
  m10 `job plan-show` omits `spec_version`.
 Run: `git worktree add --detach .remedy-wt/f026-r2-mut <C7>`, then
 `python3 -B .agent/authored/f026-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f026-r2-mut`,
 report its whole output; EVERY mutation must be red; one that stays green is reported, and you add
 the test that catches it before C8 and re-run. Then `git worktree remove --force
 .remedy-wt/f026-r2-mut`, `git worktree prune`, and report `git worktree list`.

G6 TREE AND PUSH — after C8: `git status --porcelain` empty; `git log --oneline -n 11`; `git
 worktree list` as at your step 4; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft` EMPTY. These go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside any this block
expected, every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit, per gate and per S-item), the deviations, and the next
expected action. Your Session section reads SESSION 1 of feature F026, round 2, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
2, then T003 — the version chip, the popover's version list, the edit affordance on eligible nodes
only, and the end-to-end. State the open-findings count, 5 (R-1059 stays open until the reviewer's
`Done:`), and the operator-questions count, 4.
