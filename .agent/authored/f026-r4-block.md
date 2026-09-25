STEP F026 R4 — T003, SECOND HALF: the repair of R-1060, the edit affordance for eligible tasks, and the end-to-end through the CLI and the real door

GOAL
Round 3 passed. Book it, register R-1060, record DECISION F026 D4, repair R-1060 (the secret
detector reads "task-edit-runtime" as a key), and finish T003: an "Edit task" control in the detail
popover for a waiting, paused or failed task only, sent through one new module to `job.edit-task`,
and a live end-to-end — a planned job fails through the CLI, is edited through the real door, is
relaunched through the CLI, and its new trace and its ledger show the edit and the second run.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and never merge, and you never write a `Done:` paragraph: when R-1060's fix lands you
append ONE line to `.agent/live_review.md`, exactly `Landed: R-1060 — <one line: what changed, which
commit>`. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the code and its tests against S1
to S7. Read DECISION F026 D4 (it arrives with C1b) before code; `docs/ui/design_reference/` binds
visuals.

THE DIRECTORIES
  `.remedy-wt/f026-r4-payloads/` and `.remedy-wt/f026-r4/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f026-r4-dry/`, `.remedy-wt/f026-r4-sim/`, `.remedy-wt/f026-r4-drafts/`,
  `.remedy-wt/f026-r4-render/`   The reviewer's; do not touch them.
  `.remedy-wt/f026-r4-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners chained
with `;` or `&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`
and read `${PIPESTATUS[0]}` when you pipe pytest. Use `git -C <path>`; never `cd` into a worktree.
Write any script holding a dollar-brace or a brace-quote shape to a file under your own directory and
run the file. NEVER run npm or npx; G5 names the vitest route.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell is in `/home/decodeux/Repos/remedy`; report `pwd`. `git status --porcelain` empty,
   `git branch --show-current` `feature/f026-task-edit-runtime`, `git log --oneline -1` `753f44bd`.
3. Measure the line count and sha256 of `.remedy-wt/f026-r4/block.md` against the two readings your
   delegation message states (R-0954); stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f026-r4-payloads/`; verify each one's line count, byte count and sha256
BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1169 | d3d2704400c50593d7166f219ddceaa3f2062b283070e1754b54311bbdb08d0b |
| records.diff | 67 | 13331 | d6fe996241624d65508ea6c07522f9f4917db1dabc96264a0208896831293afc |

`plan.md` REWRITES `.agent/plan.md`. `records.diff`, generated with `git diff HEAD` from a tree at
`753f44bd`, appends round 3's gate entry and R-1060's registration to `.agent/live_review.md` and
DECISION F026 D4 to `.agent/decisions.md`.

THE SPECIFICATION
S1 R-1060. In `_SECRET_RE` of `packages/orchestration/redaction_patterns.py` the OpenAI-style
   alternative becomes `(?:(?<![A-Za-z0-9])sk-[a-zA-Z0-9_-]{8,})`, with its comment naming R-1060;
   no other line of that file changes. A NEW FILE at `tests/orchestration/test_redaction_patterns.py`
   pins, through `find_forbidden_surface_tokens`: no finding for `feature/f026-task-edit-runtime`,
   `risk-assessment-notes` or `a desk-organizer here`; a finding for a key of the form
   `sk-` plus sixteen letters and digits placed after a space, after `=`, inside double quotes, after
   `/`, after `-`, and at the very start of the text. The reviewer ran exactly those texts against
   this pattern in a scratch tree and read those answers.
S2 THE PURE VIEW, in `apps/ui/src/api/taskSpecView.ts`: `taskEditAction(dashboard, taskId)` returns
   `null` unless the task's spec exists and its `editState` is `waiting`, `paused` or `failed`, else
   `{taskId, plannedId, specVersion, editState, current}`; and `changedTaskFields(current, draft)`
   takes the current fields and the form's draft (`title`, `goal` and `band` strings, `acceptance`
   and `files` as multi-line strings) and returns an object holding ONLY the backend fields that
   differ — `title`, `goal`, `acceptance` (lines trimmed, blank lines dropped), `est_tokens_band`,
   `files_hint` (the same) — so an unchanged draft returns `{}`.
S3 THE SEND, a NEW FILE at `apps/ui/src/api/taskEditSend.ts`, modelled on `pauseSend.ts` and reusing
   the same helpers (`jobCommandsPath`, `isUsableCommandNonce`, `mintDecisionClientNonce`, the
   `DecisionSendRequest`/`DecisionSendTarget` types): `JOB_EDIT_TASK_COMMAND_ID = "job.edit-task"`;
   `buildTaskEditRequest(target, taskId, fields, expectedVersion, clientNonce)` — `null` when the
   target, the task id, the nonce or the version is unusable or `fields` is empty, else a POST to
   `jobCommandsPath(jobId)` with the bearer and CSRF headers and the body `{command, client_nonce,
   args: {task_id, fields, expected_version}}`; `submitTaskEditRequest`, never throwing;
   `describeTaskEditResult(result)` — accepted: "Saved as v<n>." and, when the body's `state` is
   `failed`, a second sentence "Relaunch the job to run it: remedy job run <job id>."; a 409 whose
   body carries `current_version`: "Not saved: this task changed since you opened it. Close it and
   edit again."; any other 409 with a `detail`: "Not saved: <detail>."; other refusals and
   unreachable exactly as `describePauseSendResult` words its own; and
   `sendTaskEdit(target, taskId, fields, expectedVersion, deps)` with the same injectable
   `mintNonce`, `submit` and `deadline` seams. No component calls `fetch`.
S4 THE FORM, a NEW FILE at `apps/ui/src/components/detail/TaskEditForm.tsx`, taking `target`,
   `jobId` and the `taskEditAction` result: closed, a ghost button "Edit task"; open, a form under
   an `<h3>` "Edit task" with labelled fields — Title (input), Goal (textarea), "Acceptance, one per
   line" (textarea), "Size band" (select of S, M, L, XL), "Files, one per line" (textarea) —
   prefilled from `current`; for the `failed` state the note "Saving puts this task back in the
   queue; relaunch the job to run it."; a primary Save pill (`type="submit"`), disabled while
   `changedTaskFields` is `{}` or a send is in flight, and a ghost Cancel that closes the form; on
   Save it calls `sendTaskEdit` with the action's `specVersion` and shows the returned sentence in a
   `<p aria-live="polite">`. `DetailPopover.tsx` computes `taskEditAction(dashboard, task.id)` and,
   directly after `<TaskVersionList … />`, mounts `<TaskEditForm key={task.id} … />` ONLY when
   `task`, `serverToken` and that action are all present. `DetailPopover.module.css` gains the
   form's rules using only tokens `apps/ui/src/styles/tokens.css` defines — the Save pill filled
   `--remedy-blue` with `--remedy-card` text, 32px high, `--remedy-radius-pill`; Cancel and "Edit
   task" ghost; fields bordered `--remedy-line` on `--remedy-card` with `--remedy-radius-sm`;
   disabled at 45% opacity with a not-allowed cursor (`docs/ui/design_reference/ux_spec.md` §8) —
   and `.popover` gains `max-height: calc(100vh - 120px)` and `overflow-y: auto`, its only change.
   No animation beyond a colour transition on `--remedy-dur-base`.
S5 THE LOG. `docs/ui/design_reference/assumption_log.md` gains one row after round 3's, dated
   2026-09-25, feature F026, citing DECISION F026 D4, for the edit form and the popover's scroll.
S6 THE END-TO-END, a NEW FILE at `tests/ui_server/test_task_edit_e2e_live.py`, marked as
   `tests/ui_server/test_pause_e2e_live.py`'s live classes are and owning its own copies of that
   file's server and POST helpers: an approved two-task plan saved with `repo_path` a fixture repo
   holding `docs/README.md` (each task's `files_hint` names it) and a unique OLD marker in the first
   task's goal and acceptance; `REMEDY_DATA_DIR` under `tmp_path`, passed to every subprocess; run 1
   as `python3 -m apps.cli.main job run <id> --builder-provider fake --reviewer-provider fake
   --max-rounds 1 --repair-rounds 0` from the repository root, after which the job is `blocked`, the
   first task `blocked` and the second `skipped`; a real UI server for the job and a real POST of
   `job.edit-task` with the first task's entry id, a NEW marker in goal and acceptance and
   `expected_version` 1, answering 200 with `spec_version` 2 and the second task in `restored`; run
   2 as `job run <id> --max-rounds 3 --repair-rounds 2`, after which the job is `completed`, both
   tasks `applied_to_job_workspace` and `error` empty; the NEW run's `prompt_trace.jsonl` holding NEW
   and not OLD in every builder entry while the OLD run's holds OLD; and the live server's
   `events-since` frames, paged from cursor 0, holding exactly two `task_run_started` frames whose
   `task_id` is the first task's. The reviewer ran this flow in a scratch tree at `753f44bd` and read
   exactly those outcomes. `apps/ui/src/components/graph/brainReducer.test.ts` gains one test: a
   `task_run_started`, a failed `task_run_completed` and a second `task_run_started` for one task
   leave two builder-run nodes under it, the first `fail`.
S7 SIZE. Every commit under 500 inserted lines; split one that would reach it and say so.

THE TESTS beyond S1 and S6: `apps/ui/src/api/taskSpecView.test.ts` (the action for each of the three
states and `null` for `""` and a missing spec; `changedTaskFields` for no change, each single field,
trimming and blank lines); a NEW FILE at `apps/ui/src/api/taskEditSend.test.ts` (the request's
path, headers and body; `null` for each unusable input and for empty fields; each sentence of
`describeTaskEditResult`; the flow with injected seams); and a NEW FILE at
`tests/ui_contracts/test_task_edit_controls_contract.py` (`TaskEditForm.tsx` and `taskSpecView.ts`
contain no `fetch(`; `taskEditSend.ts` names `"job.edit-task"`; the popover mounts `<TaskEditForm`
with `key={task.id}` inside a condition that names `taskEditAction(dashboard, task.id)`).

BUNDLE — in this order.
C1a — `.agent/authored/f026-r4-block.md` := this block, `.agent/authored/f026-r4-plan.md` :=
  plan.md, `.agent/authored/f026-r4-records.diff` := records.diff, by `shutil.copyfile`.
  Subject: `F026 R4 C1a: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 98. Report the number you measure.
C1b — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F026 R4 C1b: book round 3, register R-1060, record D4`
  Expected by `git show --numstat`: 47/0 .agent/decisions.md, 4/0 .agent/live_review.md, 11/11 .agent/plan.md.
C2 — S1 with its test file and the `Landed: R-1060 — ` line.
  Subject: `F026 R4 C2: the secret detector finds a key only at a token start (R-1060)`
C3 — S2 and S3 with their tests. Subject: `F026 R4 C3: the edit action, the changed fields and the edit request`
C4 — S4 and S5 with the contract test. Subject: `F026 R4 C4: the detail popover offers the edit form for an editable task`
C5 — S6. Subject: `F026 R4 C5: the end-to-end: fail, edit through the door, relaunch, read the trace and the fan`
C6 — the mutation tool as `.agent/authored/f026-r4-mutations.py`. Subject: `F026 R4 C6: the round's red-proof mutation tool`
C7 — `.agent/handoff.md` per `docs/agents/handback_template.md`. Subject: `F026 R4 C7: rewrite handoff for round 4`
  Then `git push origin feature/f026-task-edit-runtime` and report its real outcome.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`; report its exit code.
2. The round's whole tracked path set: the `.agent/authored/f026-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/redaction_patterns.py`, `tests/orchestration/test_redaction_patterns.py`,
   `apps/ui/src/api/taskSpecView.ts`, `apps/ui/src/api/taskSpecView.test.ts`,
   `apps/ui/src/api/taskEditSend.ts`, `apps/ui/src/api/taskEditSend.test.ts`,
   `apps/ui/src/components/detail/TaskEditForm.tsx`, `apps/ui/src/components/detail/DetailPopover.tsx`,
   `apps/ui/src/components/detail/DetailPopover.module.css`,
   `apps/ui/src/components/graph/brainReducer.test.ts`, `docs/ui/design_reference/assumption_log.md`,
   `tests/ui_contracts/test_task_edit_controls_contract.py`, `tests/ui_server/test_task_edit_e2e_live.py`,
   and `.agent/handoff.md`. Report `git diff --name-only 753f44bd` after C7. If a guard outside this
   set goes red, STOP and hand back rather than widen the set. Do NOT touch
   `packages/orchestration/task_edit_runtime.py`, `packages/orchestration/ui_server.py`,
   `packages/orchestration/pingpong_job.py`, `apps/ui/src/api/pauseSend.ts`, `README.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or
   `docs/roadmap/features/T5_F026.md`.
3. A red gate: STOP, commit and push what is verified, hand back honestly under AGENTS.md "If
   Blocked". Do not repair the reviewer's payloads.
4. NOTHING IS MERGED. No `gh pr merge`, `gh pr create`, checkout of `main`, branch deletion,
   force-push or `git stash`.
5. Leave every existing worktree, branch and stash alone. The G5 worktree goes under `.remedy-wt/`,
   is removed as that step's last action, and `git worktree list` is reported afterwards; do not run
   `git worktree prune`.
6. DO NOT run the full suite: amend0917 rule 1 gives F026 exactly one, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the table; each
 `.agent/authored/f026-r4-*` payload copy byte-equal to its source (the block copy against
 `.remedy-wt/f026-r4/block.md`), read back with `git show <C1a>:<path>`.

G2 THE RECORDS — `git show <C1b>:<path>` of each file below hashes to the reviewer's reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 325971 | f99a5029779fa894cb5d31bb818e7f6c5a791d5cfc367ca3cb9c427e951b6246 |
 | .agent/decisions.md | 2139835 | 5d5bf3580408b46cb3b50e214439e4d216fddff52fe669ba9007be2961d51fc4 |
 | .agent/plan.md | 1169 | d3d2704400c50593d7166f219ddceaa3f2062b283070e1754b54311bbdb08d0b |
 and `open_finding_ids` over the ledger's text reads R-1008, R-1055, R-1057 and R-1058 at
 `753f44bd` and those four plus R-1060 at C1b and at C6; the ledger's last line at C2 begins
 `Landed: R-1060 — `.

G3 THE CODE — `python3 -m ruff check` over every `.py` path of constraint 2 at C6.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_redaction_patterns.py tests/ui_contracts/test_task_edit_controls_contract.py tests/ui_server/test_task_edit_e2e_live.py tests/ui_contracts tests/ui_server/test_auth_redaction.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_task_specs.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_prompt_redaction.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the three new test files and the golden path, serially,
 in a tree at `753f44bd` carrying this round's records, and read `1615 passed, 10 skipped` at exit 0. In your run
 the TypeScript node of `tests/ui_server/test_dashboard_contract.py`, the vitest node of
 `tests/orchestration/test_test_runner.py` and the two lint nodes of
 `tests/ui_contracts/test_ui_lint.py` must PASS; the four D3 quarantines and the D12 quarantine stay
 skipped; report what the responsive node reads. `test_no_raw_leaks_in_viewer`, red at `753f44bd`
 in the primary checkout (R-1060), must PASS from C2 on. Report every `SKIPPED` line and account
 for every other difference. Then `python3 -m apps.cli.main integrity check --json`: all six
 checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool takes a worktree path; per mutation it edits the named file INSIDE the
 worktree (asserting its FROM text occurs exactly once), runs the covering tests, restores the bytes,
 and prints label, exit code, failed count and failing ids; controls run first and last; it ends with
 `restored byte-identical: True` per file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
 Python mutations run `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_redaction_patterns.py` and `tests/ui_contracts/test_task_edit_controls_contract.py`
 after purging `__pycache__`; TypeScript mutations run vitest over the worktree's changed `.test.ts`
 files by the route `.agent/authored/f026-r3-mutations.py` uses. The mutations:
  m1 the `sk-` alternative loses its boundary (redaction_patterns.py);
  m2 `taskEditAction` answers an action for an `editState` of `""` (taskSpecView.ts);
  m3 `changedTaskFields` returns every field, changed or not;
  m4 `changedTaskFields` keeps blank lines;
  m5 `buildTaskEditRequest` sends `job.plan-edit-task`;
  m6 `buildTaskEditRequest` omits `expected_version`;
  m7 `describeTaskEditResult` drops the relaunch sentence for a failed task;
  m8 the popover mounts `<TaskEditForm` without the `taskEditAction` condition (DetailPopover.tsx).
 Run: `git worktree add --detach .remedy-wt/f026-r4-mut <C6>`, then
 `python3 -B .agent/authored/f026-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f026-r4-mut`,
 report its whole output; EVERY mutation must be red; one that stays green is reported, you add the
 test that catches it before C7 and re-run. Then `git worktree remove --force .remedy-wt/f026-r4-mut`
 and report `git worktree list`.

G6 TREE AND PUSH — after C7: `git status --porcelain` empty; `git log --oneline -n 9`; `git worktree
 list`; the push's real outcome; `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
 EMPTY. These go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside any this block
expected, every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit, per gate and per S-item), the deviations, and the next
expected action. Your Session section reads SESSION 1 of feature F026, round 4, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
4, then F026's closure sequence. State the open-findings count, 5 (R-1060 stays open until the
reviewer's `Done:`), and the operator-questions count, 4.
