STEP F029 R4 — BOOK R3 AND LAND T003's SERVER HALF: the shared rerun command, the run-log event, the task item's attempts, and the write door's `job.rerun-subtree`

GOAL
Round 3 passed. Book its gate entry, resolve R-1081, record DECISION F029 D4, and land what the
browser needs from the server: one shared function `rerun_subtree_command` that previews the cost
and prepares a rerun only when confirmed, the run-log event `subtree_rerun_prepared` with its plain
sentence, the dashboard task item's `attempt` and `attempts`, and the write door's command
`job.rerun-subtree`. No browser code beyond the one catalogue sentence: round 5 lands it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code and tests against S1 to S5; only the `.agent/` records travel as payloads. Read DECISION F029
D4 in `.agent/decisions.md` after C2 before you write code. Read, before writing:
`packages/orchestration/subtree_rerun.py` whole; `_write_task_vetoed_event` in
`packages/orchestration/task_veto.py`; `packages/orchestration/event_names.py` and
`tests/orchestration/test_event_names.py`; `apps/ui/src/api/humanizeCatalog.ts` and
`tests/ui_contracts/test_humanize_catalog.py`; in `packages/orchestration/ui_server.py` the task
item of `_build_dashboard` (search `"origin": _task_origin(t)`), the command-id constants
(search `JOB_INJECT_COMMAND_IDS`), the `job.veto-task` and injection branches of
`_handle_command_submission`, `_dispatch_injection`, and the argument checks of
`_read_command_payload`; `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py`; in
`tests/ui_server/test_command_channel.py` the exposed-command loop (search `declined[`), the
exact pin of `UI_EXPOSED_COMMANDS` (search `sorted(UI_EXPOSED_COMMANDS)`) and
`TestCommandDoorImportGuard` with `DOOR_METHODS` and `ALLOWED_IMPORTS`; the injection class of
`tests/ui_server/test_command_dispatch.py`; and `tests/ui_server/test_dashboard_task_origin.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f029-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f029-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f029-r4-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f029-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f029-r4-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f029-subtree-rerun`, and `git log --oneline -1` must read `5d9c8784`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f029-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f029-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 73 | 12137 | 07ed6d77ca9f0a84086c2b7d62e3adf36637bbe7d88340902e0021e3d0ae4b5f |
| plan.md | 35 | 1269 | 1449df68e5a4957b0f60b3efa28cb39fc61493a87fffe09504426c2a6017efd5 |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer generated
it with `git diff HEAD` from a tree at `5d9c8784`. It appends to `.agent/live_review.md` round 3's
gate entry and R-1081's `Done:` line, and to `.agent/decisions.md` DECISION F029 D4.

THE SPECIFICATION
S1 THE FUNCTION, in `subtree_rerun.py`: `rerun_subtree_command(job, task_id, *, model="",
   confirm_cost=False, actor, config=None, confirm_above_usd=None) -> dict`, which never raises
   `SubtreeRerunRefused`. `config` defaults to `resolve_predictive_budget_config(project_root=
   job.repo_path or None)` and `confirm_above_usd` to `resolve_confirm_above_usd()`. In order: a
   `SubtreeRerunRefused` from `rerun_subtree_ids` answers `{"outcome": "refused", "code",
   "detail", "facts"}`; the estimate is `subtree_rerun_cost_estimate`, carried as
   `{"band_usd_low", "band_usd_high", "basis"}`; when `band_usd_high` is None or above
   `confirm_above_usd` and `confirm_cost` is False, the answer is `{"outcome":
   "needs_confirmation", "job_id", "task_id", "subtree", "estimate", "confirm_above_usd"}` and
   nothing is touched; otherwise `prepare_subtree_rerun(job.job_id, task_id,
   model_override=model, actor=actor)` answers `{"outcome": "prepared", **record, "estimate",
   "run_command": f"remedy job run {job.job_id}"}`, and its `SubtreeRerunRefused` answers the
   refused shape above.
S2 THE EVENT. `prepare_subtree_rerun` writes, after `save_job_plan` and inside the guarded block
   R-1081 built, `RunLogWriter(job_id).log("subtree_rerun_prepared", outcome="prepared",
   scope="task", task_id=<root>, rerun_id=..., subtree=[...], restored_pending=[...],
   reset_commit=..., paths=[...], exact=..., model_override=..., actor=..., state_before=...,
   state_after=...)`, the name written inline as a literal. The name joins `EVENT_NAMES` in
   `event_names.py` in its sorted place, and `humanizeCatalog.ts` gains, in its sorted place,
   `"subtree_rerun_prepared": "A task and the tasks that depend on it were reset to run again."`.
   `brainReducer.ts` is not edited (DECISION F029 D4 (3)).
S3 THE DASHBOARD. The task item of `_build_dashboard` gains `"attempt": int(t.attempt)` and
   `"attempts": [dict(a) for a in t.attempts if isinstance(a, dict)]`, directly before `"origin"`,
   which stays the last key.
S4 THE DOOR. `JOB_RERUN_SUBTREE_COMMAND_ID = "job.rerun-subtree"` beside the injection constants;
   the id joins `UI_EXPOSED_COMMANDS` with a comment naming DECISION F029 D4; `_read_command_payload`
   checks its arguments the way it checks the injection commands' — `task_id` a non-empty string
   (required), `model` a string and `confirm_cost` a bool (both optional), anything else refused
   as the other commands refuse it; `_handle_command_submission` gains a branch shaped exactly as
   the injection branch — effect, then 409 `"<code>: <detail>"` for `outcome` `refused`, then the
   audit line, the publication, the accepted event and the 200 for `needs_confirmation` and
   `prepared` — calling a new `_dispatch_rerun_subtree(job, payload)` that imports only
   `rerun_subtree_command` and answers `{"command": command, **rerun_subtree_command(job,
   args["task_id"], model=args.get("model") or "", confirm_cost=bool(args.get("confirm_cost")),
   actor=token_fingerprint(self._supplied_bearer_token()))}`. In `test_command_channel.py`:
   `DOOR_METHODS` gains `_dispatch_rerun_subtree`, `ALLOWED_IMPORTS` gains
   `("packages.orchestration.subtree_rerun", "rerun_subtree_command")` in the form its neighbours
   use, the exact pin gains the id, and the exposed-command loop gains the branch the id needs.
S5 NOTHING ELSE: no edit under `apps/ui/` beyond S2's one line, and none to `pingpong_job.py`,
   `worktrees.py`, `job_rerun_cmd.py` or the catalog entry of `job.rerun-subtree`.

THE TESTS. In `tests/orchestration/test_subtree_rerun_prepare.py`, over round 2's three-task job run
to `completed` (bands written into its tasks' `inputs["plan"]` where a priced estimate is needed):
S1's `refused` for an unknown task; `needs_confirmation` for an unavailable estimate with
`job.json` byte-identical and no worktree re-added; `needs_confirmation` above a threshold; a
priced estimate below the threshold prepares without `confirm_cost`; `confirm_cost=True` prepares
over an unavailable estimate, carrying `run_command` and the model override; a preparation
refusal answers the refused shape with its `facts`. S2: the run log holds exactly one
`subtree_rerun_prepared` line after a preparation, with the fields above, and none after a
refusal. S3, in a NEW file `tests/ui_server/test_dashboard_task_attempts.py` built as
`test_dashboard_task_origin.py` builds its dashboard: after a preparation T002 reads `attempt` 2
with one attempt holding its old run id, T001 reads `attempt` 1 and `attempts` [], and `origin`
is still the last key. S4, in a NEW file `tests/ui_server/test_rerun_subtree_door.py` modelled on
the injection class of `test_command_dispatch.py`: `needs_confirmation` as a 200 changing nothing,
`prepared` as a 200 after `confirm_cost`, a refusal as a 409 reading `unknown_task: ...`, and a
non-bool `confirm_cost` or a missing `task_id` refused before the job is read.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.
C1 — `.agent/authored/f029-r4-block.md` := this block, `.agent/authored/f029-r4-booking.diff` and
  `.agent/authored/f029-r4-plan.md` := the payloads, by `shutil.copyfile`.
  Subject: `F029 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 108. Report the number you measure.
C2 — `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F029 R4 C2: book round 3's PASS, resolve R-1081, record D4`
  Expected by `git show --numstat`: 53/0 decisions.md, 4/0 live_review.md, 12/10 plan.md.
C3 — S1, S2 and their tests. Subject: `F029 R4 C3: one rerun command answers the preview or the preparation, and the preparation writes its event`
C4 — S3 and its test. Subject: `F029 R4 C4: the dashboard's task item carries its attempts`
C5 — S4 and its tests. Subject: `F029 R4 C5: expose job.rerun-subtree through the write door`
  Split any of C3 to C5 under constraint 2 when it would reach 500 insertions.
C6 — `.agent/authored/f029-r4-mutations.py` (G5) as C6a, subject `F029 R4 C6a: add the mutation
  tool`, then `.agent/handoff.md` per `docs/agents/handback_template.md` as C6b, subject
  `F029 R4 C6b: rewrite handoff for round 4`. Then `git push origin feature/f029-subtree-rerun`
  and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`; split a commit that would
   reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f029-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `packages/orchestration/subtree_rerun.py`, `packages/orchestration/event_names.py`,
   `packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
   `apps/ui/src/api/humanizeCatalog.ts`, `tests/orchestration/test_subtree_rerun_prepare.py`,
   `tests/ui_server/test_dashboard_task_attempts.py`, `tests/ui_server/test_rerun_subtree_door.py`
   and `tests/ui_server/test_command_channel.py`. Report `git diff --name-only 5d9c8784` at the
   tip after C6b. A guard outside this set that goes red is reported and stops the round under
   constraint 4; it is never edited.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round wrote that is wrong may be corrected
   before C6b, and the correction is declared. An EXISTING test that goes red is never edited to
   pass unless this block names it; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F029 one full-suite run, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C6b is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table; then
 each `.agent/authored/f029-r4-*` copy read back with `git show <C1>:<path>` compared byte for byte
 with its source (the block copy against `.remedy-wt/f029-r4/block.md`). One reading per copy.
G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2295769 | 3b542a421d20aa63a9640f80af772233c4c95a55083cb64a0e180fe66232493e |
 | .agent/live_review.md | 320687 | 9ea984ea34c730d89b383cd745f3663836c5c97001f72d3a9fba8d99a84802d0 |
 | .agent/plan.md | 1269 | 1449df68e5a4957b0f60b3efa28cb39fc61493a87fffe09504426c2a6017efd5 |
 Also the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the file's TEXT at `5d9c8784` (the reviewer read `['R-1081']`) and at C2 (the reviewer read
 it empty).
G3 THE CODE — `python3 -m ruff check` over every Python file the round touched, at the tip before
 C6b, with its real exit code; then quote from the commit that landed it the whole of
 `rerun_subtree_command`, `_dispatch_rerun_subtree` and the new branch of
 `_handle_command_submission`.
G4 THE TESTS — in the primary checkout at the last commit before C6b, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_rerun_subtree_door.py tests/ui_server/test_dashboard_task_attempts.py tests/orchestration/test_subtree_rerun.py tests/orchestration/test_subtree_rerun_prepare.py tests/cli/test_job_rerun_subtree.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_dashboard_task_origin.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_sse_stream.py tests/ui_contracts tests/orchestration/test_event_names.py tests/test_run_log_cli.py tests/test_command_catalog.py tests/cli/test_exit_codes.py tests/test_subprocess_timeouts.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -16; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the two new files, serially, in the primary checkout at
 `5d9c8784`, and read `2402 passed, 11 skipped` at real exit code 0. Report every `SKIPPED` line
 the `-rs` summary prints and say which of the eleven are not the seven F252 quarantines, the
 node count the round added by `--collect-only -q` over the test files it touched, and account
 for any difference from 2402 plus that count. Then `python3 -m apps.cli.main integrity check
 --json`, every check's status and `fail_count`.
G5 THE RED PROOFS — your tool `.agent/authored/f029-r4-mutations.py` takes a worktree path, and for
 each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_server/test_rerun_subtree_door.py tests/ui_server/test_dashboard_task_attempts.py
 tests/orchestration/test_subtree_rerun_prepare.py tests/ui_server/test_dashboard_task_origin.py`
 from the worktree's root after purging its `__pycache__` directories, restores the bytes, and
 prints one line per mutation: its label, the exit code, the failed count and the failing node
 ids. It runs an unmutated control first and last and ends with `restored byte-identical: True`
 and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 S1 prepares over an unavailable estimate without `confirm_cost`;
  m2 S1 answers `needs_confirmation` even with `confirm_cost`;
  m3 S1 passes no model to the preparation;
  m4 S2 writes no event;
  m5 S3 leaves `attempts` out of the task item;
  m6 S3 places `attempt` after `origin`;
  m7 S4's branch answers a refusal as a 200;
  m8 `_read_command_payload` accepts a `confirm_cost` that is not a bool.
 Run it: `git worktree add --detach .remedy-wt/f029-r4-mut <the last commit before C6b>`, then
 `python3 -B .agent/authored/f029-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f029-r4-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, then you add the test that catches it in its own commit and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f029-r4-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.
G6 TREE AND PUSH — after C6b: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`; `git worktree list | wc -l`, which must equal your step 4 reading; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These go in your reply, since C6b cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected, every gate's real output and exit code, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per S-item), the deviations, and the next expected action. Report what you ran, not what you
expected. Your Session section reads SESSION 1 of feature F029, round 4, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T003's browser half — the send module, the types, the attempt chip, the attempt list
in the task's popover, the Rerun control, and the render proof. State the open-findings count, 0,
and the operator-questions count, 0.
