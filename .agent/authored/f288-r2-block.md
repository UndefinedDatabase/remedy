STEP F288 R2 — THE SECOND HALF OF T001's WRITERS: the run-next path's attempt id, the test service's attempt id, task id and result, and a `plan_approved` event with its block in the stream's envelope

GOAL
Round 1 passed. Book its verdict and one prose slip, record DECISION F288 D2, and land it: the
run-next path in `apps/cli/commands/job.py` mints its attempt id before `task_run_started` and
writes it on every event of the execution; every `test_run_*` event of
`packages/orchestration/test_execution_service.py` carries its test run id as the attempt id, the
request's task id and its result; a new `announce_plan_approval` in
`packages/orchestration/job_plan.py` writes `plan_approved` after every saved approval, human or
unattended; and `_safe_event_summary` carries the attempt id for ten more kinds and a `plan` block
for `plan_approved`, with every reader of the new name.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against the specification S1 to S6 below. Only the
`.agent/` records travel as payloads. Read DECISION F288 D2 in the records diff before you write
code: it is the design this specification implements.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f288-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f288-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f288-r1-dry/`, `.remedy-wt/f288-r1-sim/`, `.remedy-wt/f288-r2-dry/`,
  `.remedy-wt/f288-r2-sim/`       The reviewer's trees; do not touch them.
  `.remedy-wt/f288-r1-drafts/`, `.remedy-wt/f288-r2-drafts/`, `.remedy-wt/f288-review/`
                                  The reviewer's drafts and scripts; do not touch them.
  `.remedy-wt/f288-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f288-event-stream-completeness`, and `git log --oneline -1` must read `c0553449`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f288-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f288-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 87 | 14966 | b11033f96122dd2dbb5251b2019e64450c64399038f528d2bbba2f26d687090d |
| plan.md | 31 | 1145 | 464358ea846b89de5f9237720fe27b1941cf5e7347e636f9e53c8bcf5c8d7a9f |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `c0553449` into which it wrote the edits. It
appends round 1's gate entry to `.agent/live_review.md`, DECISION F288 D2 to `.agent/decisions.md`
and one dated line to `.agent/prose_slips.md`.

THE SPECIFICATION
S1 THE RUN-NEXT PATH. In `_cmd_run_next_task_local`, once `pending_task` is chosen and directly
   before the `log.log("task_run_started", ...)` call, `attempt_id = mint_run_id()` (imported from
   `packages.orchestration.data_paths` inside the function, beside its other local imports), and
   every `log.log(...)` call from `task_run_started` to the function's end, the one inside `_fail`
   included, gains the keyword `attempt_id=attempt_id`. The `task_run_noop` written before any
   task is chosen gains nothing. No outcome and no other keyword changes. In
   `docs/system/architecture.md`, directly before the line `**Terminal-event invariant (v1):**`,
   insert the one-line paragraph below followed by one blank line; it is shown indented by six
   spaces that are NOT part of it, and every other character, backticks included, is literal:
      Every event from `task_run_started` to the terminal event carries `metadata.attempt_id`, the id the execution mints before `task_run_started` (DECISION F288 D2); the pre-execution noop carries none.
S2 THE TEST SERVICE. Every `test_run_*` event `execute_test_run` and its helpers write
   (`test_run_requested`, `test_run_started`, `test_run_completed`, `test_run_timed_out` and every
   `test_run_blocked`) carries, beside every metadata key it carries today: `attempt_id` equal to
   its `test_run_id`; `task_id` equal to the request's task id (`result.linked_task_id`) when that
   is non-empty; and `outcome` `passed` or `failed` for `test_run_completed` (its `status`),
   `timeout` for `test_run_timed_out` and `blocked` for `test_run_blocked`, while
   `test_run_requested` and `test_run_started` carry no `outcome`. Implement it once, inside the
   `_emit` helper or one helper beside it, not per call site; `contract_decision`,
   `run_usage_recorded` and `test_failure_artifact_created` are untouched.
S3 THE PLAN-APPROVED EVENT. In `packages/orchestration/job_plan.py`, directly above
   `resolve_task_plan_approval`, `announce_plan_approval(job: Any, *, mode: str) -> None`, which
   writes, through `timeline.append_run_event` to `data_paths.resolve_data_root()` (both imported
   inside the function), the event `plan_approved` for `str(job.job_id)` with the metadata
   `{"outcome": "approved", "task_ids": [str(t.task_id) for t in job.tasks], "approval_mode": mode}`;
   it catches `OSError`, `ValueError` and `TypeError`, logs one warning naming the job id through
   `logging.getLogger(__name__)`, and returns, so a failed write never undoes a saved approval. Its
   docstring names DECISION F288 D2. `resolve_task_plan_approval` calls it with `mode="human"`
   directly after `save_job_plan(job)` on its APPROVE branch only. The `--yes` branch in
   `packages/orchestration/do_sequence.py` calls it with `mode=AUTO_APPROVAL_MODE` directly after
   the `save_job_plan(job)` that follows `auto_approve_task_plan`, and `_auto_approve_if_gated` in
   `packages/orchestration/orchestrator_loop.py` likewise after its `save_job_plan(job)`.
   `auto_approve_task_plan` itself is unchanged.
S4 THE ENVELOPE. In `packages/orchestration/ui_server.py`, `ATTEMPT_EVENT_KINDS` gains
   `task_run_noop`, `builder_started`, `builder_completed`, `verification_passed`,
   `verification_failed`, `test_run_requested`, `test_run_started`, `test_run_completed`,
   `test_run_timed_out` and `test_run_blocked`, and its comment names DECISION F288 D2 and says the
   long-run executor's repair events are round 3's. For kind `plan_approved` the summary gains the
   key `plan`, placed where the other kind blocks go, whose value is `{"task_ids": [...]}`: the
   string entries of `metadata["task_ids"]` in order when that is a list, and `[]` otherwise. The
   docstring gains one sentence naming DECISION F288 D2's `plan` block and its condition.
S5 THE READERS. `EVENT_NAMES` gains `plan_approved` in its alphabetical place.
   `STREAM_EVENT_CATALOG` gains, in its alphabetical place, the line
   `  "plan_approved": "The plan was approved and its tasks were released.",`.
   `NARRATED_EVENTS` gains, directly after `planning_completed`,
   `"plan_approved": "The plan was approved (mode: {approval_mode})."`.
   `_render_single_event` in `packages/orchestration/timeline.py` renders `plan_approved` as
   `f"  {_OK} Plan approved: {n} task(s), mode {mode}"`, where `n` is the length of
   `metadata["task_ids"]` when it is a list and 0 otherwise, and `mode` is
   `metadata["approval_mode"]` or `?` when absent.
S6 NOTHING ELSE. No other event, module or file changes.

THE TESTS
In `tests/test_run_log_cli.py`, using that file's own harnesses: on the success path every event
from `task_run_started` to `task_run_completed` carries one `attempt_id`, a sixteen-hex string;
`builder_started`, `verification_passed` and `task_run_completed` carry it among them; two runs
of the path carry two different ids; a `_fail` path (permission denied) carries on
`task_run_failed` the id its `task_run_started` carried; and the no-pending noop carries none. In
`tests/orchestration/test_test_execution_service.py`, using that file's own harnesses: a passing
run's `test_run_requested`, `test_run_started` and `test_run_completed` each carry `attempt_id`
equal to the result's `test_run_id`, the completion carries `outcome` `passed` at the top level,
and the first two carry no top-level `outcome`; a request naming a task id puts it at the top level
of all three; and a permission-denied run's `test_run_blocked` carries `outcome` `blocked` and the
attempt id. In `tests/orchestration/test_plan_editing.py`: an approval through
`consume_plan_approval` writes exactly one `plan_approved`, with `outcome` `approved`, `task_ids`
equal to the job's task ids in order and `approval_mode` `human`; a rejection writes none; and with
`append_run_event` made to raise `OSError`, the approval still returns normally and the stored plan
reads approved. In `tests/orchestration/test_orchestrator_loop.py`: `_auto_approve_if_gated` on a
gated job writes one `plan_approved` with `approval_mode` `auto_yes`, and on an ungated job none.
In `tests/orchestration/test_do_run.py`: the `--yes` path writes one `plan_approved` with
`approval_mode` `auto_yes`. In `tests/ui_server/test_sse_stream.py`: round 1's pinned set
becomes the sixteen names of S4 and round 1's `task_run_noop` case moves into the attempt kinds, so
`test_task_run_noop_and_job_stopped_keep_the_base_key_set` is rewritten to pin `job_stopped` and
`plan_approved` without `attempt_id` (this round's decision changes those two round 1 tests; no
other existing assertion may change); `plan_approved`'s key set is the base five plus `plan`, its
`task_ids` keep order and drop non-strings, and an absent or non-list value reads `[]`. In
`tests/orchestration/test_teacher_narration.py`: the pinned sorted list gains `plan_approved`, and
one such event narrates to its exact sentence. In `tests/test_timeline.py`: a `plan_approved`
event renders its exact line, and one with no `task_ids` renders `0 task(s)`. In
`tests/orchestration/test_mint_call_sites.py`: an AST reading of `apps/cli/commands/job.py`
finding exactly one assignment to the name `attempt_id` and that it calls `mint_run_id`.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f288-r2-block.md` := this block, `.agent/authored/f288-r2-records.diff` :=
  records.diff and `.agent/authored/f288-r2-plan.md` := plan.md, all by `shutil.copyfile`.
  Subject: `F288 R2 C1: copy round 2 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 118. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKING AND THE PLAN, in this order: `git apply` records.diff, then rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F288 R2 C2: book round 1's PASS, record D2 and the round 2 plan`
  Expected by `git show --numstat`: 60/0 decisions.md, 2/0 live_review.md, 10/12 plan.md, 1/0 prose_slips.md.

C3 — THE CODE: S1 to S5 — `apps/cli/commands/job.py`, `docs/system/architecture.md`,
  `packages/orchestration/test_execution_service.py`, `packages/orchestration/job_plan.py`,
  `packages/orchestration/do_sequence.py`, `packages/orchestration/orchestrator_loop.py`,
  `packages/orchestration/ui_server.py`, `packages/orchestration/event_names.py`,
  `packages/orchestration/teacher_narration.py`, `packages/orchestration/timeline.py` and
  `apps/ui/src/api/humanizeCatalog.ts`.
  Subject: `F288 R2 C3: carry the attempt id on the run-next path and the test service, and announce plan approvals`

C4 — THE TESTS AND THE TOOL: the test files THE TESTS names, and your mutation tool (G5) saved as
  `.agent/authored/f288-r2-mutations.py`.
  Subject: `F288 R2 C4: test the run-next and test-service attempt ids and the plan-approved event, and add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F288 R2 C5: rewrite handoff for round 2`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f288-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`, the
   files C3 names, the test files THE TESTS names, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only c0553449` at the branch tip after C5. Do NOT touch
   `packages/orchestration/long_run_executor.py`, `packages/orchestration/builder_bridge.py`,
   `packages/orchestration/pingpong_job.py`, `packages/orchestration/pingpong_loop.py`,
   `apps/ui/src/components/`, `apps/ui/src/api/feedRow.ts`, `docs/roadmap/`, `README.md`,
   `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass, the two round 1 tests THE TESTS names
   excepted; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F288's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f288-r2-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f288-r2/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2229214 | c8050e1e5220ff82ee2ea511ada29ad098d177bc1b7747335b4be3c23f6a9c74 |
 | .agent/live_review.md | 301807 | 3259856eb2bd370b84bc3915dc800a4b1e2cf02866272f746584d1c2da8aa187 |
 | .agent/prose_slips.md | 371624 | 703945e4d7105b32ca6859ca5d246bb75ae24a133ca4ae6719bb7f562c4378d5 |
 | .agent/plan.md | 1145 | 464358ea846b89de5f9237720fe27b1941cf5e7347e636f9e53c8bcf5c8d7a9f |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at C2 (the reviewer read it empty), and
 the ledger's last line at C2, which must begin `Gate: F288 R1 — `.

G3 THE CODE — `python3 -m ruff check` over every Python file C3 names and every test file THE
 TESTS names, at C4, with its real exit code. Then quote from `git show <C3>` the whole of
 `announce_plan_approval`, the S2 helper, and the `plan` branch of `_safe_event_summary`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/test_run_log_cli.py tests/orchestration/test_test_execution_service.py tests/orchestration/test_real_test_execution.py tests/test_test_runner.py tests/cli/test_plan_approval.py tests/cli/test_decision_answers.py tests/orchestration/test_plan_editing.py tests/orchestration/test_plan_edit_execution.py tests/orchestration/test_do_run.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_mission_e2e.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_sse_stream.py tests/ui_server/test_budget_tick_envelope.py tests/ui_contracts/test_humanize_catalog.py tests/orchestration/test_event_names.py tests/orchestration/test_event_name_coupling.py tests/orchestration/test_teacher_narration.py tests/test_timeline.py tests/orchestration/test_event_ledger.py tests/orchestration/test_project_brain.py tests/orchestration/test_stop_reasons.py tests/regression/test_named_bugs.py tests/test_remedy_smoke_script.py tests/orchestration/test_mint_call_sites.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/test_imports.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/ui_contracts/test_ui_lint.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this exact selection, serially, in the primary checkout at `c0553449`, and read
 `1883 passed, 7 skipped` at real exit code 0: six D3 quarantines in
 `tests/regression/test_named_bugs.py` and the D12 quarantine in `tests/test_agent_tooling.py`,
 all of which stay skipped. If `tail -15` cuts a `SKIPPED` line off, re-read the summary until you
 have them all. Report every `SKIPPED` line, the number of nodes the round adds and removes
 (`--collect-only -q` on the edited test files at `c0553449` and at C4), and account for any other
 difference from 1883. Then `python3 -m apps.cli.main integrity check --json`, which must read all
 six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f288-r2-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` from the worktree's root after
 purging its `__pycache__` directories, over the worktree's `tests/ui_server/test_sse_stream.py`,
 `tests/orchestration/test_teacher_narration.py`, `tests/test_timeline.py`,
 `tests/orchestration/test_mint_call_sites.py`, `tests/ui_contracts/test_humanize_catalog.py`,
 `tests/test_run_log_cli.py`, `tests/orchestration/test_test_execution_service.py` and the node
 ids of the tests this round added to `tests/orchestration/test_plan_editing.py`,
 `tests/orchestration/test_orchestrator_loop.py` and `tests/orchestration/test_do_run.py`,
 restores the bytes, and prints one line per mutation: its label, the exit code, the failed count
 and the failing node ids. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations, each a real behaviour change:
  m1 the run-next `task_run_started` carries no `attempt_id`;
  m2 `_fail`'s `task_run_failed` carries no `attempt_id`;
  m3 the run-next `task_run_completed` carries a second, freshly minted id;
  m4 the test service's `attempt_id` is omitted from `test_run_started`;
  m5 `test_run_completed` carries no top-level `outcome`;
  m6 `test_run_blocked` carries `outcome` `failed`;
  m7 the request's task id is not lifted onto `test_run_requested`;
  m8 `resolve_task_plan_approval` announces on its reject branch as well;
  m9 `announce_plan_approval` lists the task ids in reverse order;
  m10 `announce_plan_approval` lets an `OSError` propagate;
  m11 `_auto_approve_if_gated` does not announce;
  m12 the `--yes` branch of `do_sequence.py` does not announce;
  m13 the envelope's `plan` block keeps non-string entries;
  m14 `ATTEMPT_EVENT_KINDS` loses `test_run_blocked`;
  m15 `humanizeCatalog.ts` loses its `plan_approved` line.
 Run it: `git worktree add --detach .remedy-wt/f288-r2-mut <C4>`, then
 `python3 -B .agent/authored/f288-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f288-r2-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f288-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `c0553449` in that order (more
 lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal your step 4
 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected (none is expected for C3 and C4 — report what you measure), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F288, round 2, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then the long-run executor's repair events under their own ruling together with T002,
the live graph's reducer. State the open-findings count, 0, and the operator-questions count, 0.
