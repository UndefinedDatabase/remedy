STEP F027 R2 — THE LINEAR RUNNER FOLDS A VETO, AND R-1065'S REPAIR: the fold before the loop and at every pre-task safe point, the vetoed attempt's workspace restored, the unreachable set never dispatched, the terminal that names both sets, and `vetoed` in the manifest's vocabulary

GOAL
Book round 1's verdict, register R-1065, record DECISION F027 D2, and land it: `run_job` reads the
veto control files and folds them into the record, the job workspace is returned to a vetoed
attempt's start tree by a new `worktrees.restore_tree`, independent tasks run on while the
unreachable set is never dispatched, a run whose remaining work is all vetoed or unreachable ends
`blocked` naming both sets, the run manifest accepts `vetoed`, and R-1065 is repaired — with tests
in a new `tests/orchestration/test_task_veto_runner.py` and a mutation tool proving they bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S7 below. Only the `.agent/` records travel as
payloads. Read DECISION F027 D2 in `records.diff` before you write code: it is the design.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-r2-dry/`, `.remedy-wt/f027-r2-drafts/`, `.remedy-wt/f027-review/` and every
                                  older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
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
   `feature/f027-task-veto`, and `git log --oneline -1` must read `25ab44de`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 37 | 1567 | 0cb52ffa8ec84b08caeb9ec2dba6921aeba0e163c5c53bfb6f8084d2c234cb0d |
| records.diff | 89 | 15591 | f9e82396ddfe8ced08b85553cb6e5e5c834f5a8097e305565061684c3ccb0fbb |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `25ab44de`. It appends to `.agent/live_review.md`
round 1's gate entry and R-1065's registration, and to `.agent/decisions.md` DECISION F027 D2.

THE SPECIFICATION
S1 R-1065, in `packages/orchestration/task_veto.py`. Whenever `veto_task_command` is about to
   answer `task_already_vetoed` for a task that has an entry in `vetoed_tasks` — the gate's route
   and the lost-race route alike — it first repairs a missing `task_vetoed` event for that entry
   exactly as S8 of round 1 did, the one write a refusal may make. Both routes then answer ONE shape,
   `{"outcome": "refused", "code": "task_already_vetoed", "detail", "task_id", "request_id"}`, with
   the entry's request id, and the gate's detail for an already vetoed task says the task is
   already vetoed rather than naming its status. A task whose status reads `vetoed` with no entry
   answers the same refusal with `request_id` "" and repairs nothing. Update the docstrings.
S2 THE RESTORE, a NEW function `restore_tree(handle, tree) -> list[str]` in
   `packages/orchestration/worktrees.py`, as D2 (3) rules: for every path
   `changed_files_between(handle, tree, write_tree(handle))` names, a path the tree holds is written
   back with the tree's bytes (`blob_at`) and its mode (`100755` executable, `100644` not), a
   `120000` entry is recreated as that symbolic link, a path the tree lacks is deleted and each
   directory that leaves empty is removed up to the worktree root, and a `160000` entry raises
   `WorktreeError`; then `write_tree(handle)` must equal `tree`, or it raises `WorktreeError`. It
   returns the sorted paths it restored and never runs a git command that writes the index, `HEAD`
   or a ref.
S3 THE FOLD, in `packages/orchestration/pingpong_job.py`, one helper that `run_job` calls
   immediately before its task loop (after the `episode_start` absorb) and at the pre-task safe
   point after `_stop_check(next_task=...)` answered None. It imports `task_veto` inside the
   function, as `run_job` imports `pause_control`, reads `vetoed_tasks(job.job_id,
   control_root_path=_control)`, and folds every entry whose task is not yet `vetoed`, per D2 (2):
   an entry naming no task of the job, or a task whose status is outside `VETOABLE_TASK_STATUSES`,
   is recorded as inert in `job.metadata["task_vetoes"]` with `inert` naming the status (`unknown`
   for no task) and changes no task; otherwise, when `job_handle` is not None and the task's
   attempt is `active` with a `task_start_tree`, `restore_tree(job_handle, task.task_start_tree)`
   runs first; then the task's status becomes `TASK_VETOED` and its `task_attempt_state` `vetoed`,
   `error` is kept, and `job.metadata["task_vetoes"][task_id]` is the entry's `to_json()` plus
   `folded_at`, `restored` (true when `restore_tree` ran) and `unreachable_task_ids` (that task's
   `veto_unreachable` over the tasks, as a list). When the vetoed task's status at the fold was
   `blocked` or `failed`, every task after it in plan order whose status is `skipped` and which is
   not in `veto_unreachable(job.tasks, <every vetoed id>)` goes back to `pending`. The record is
   persisted once, after the entries are folded, only when something changed. A `TaskVetoError`
   blocks the job with the error `task_veto_control_error: <detail>`, and a `WorktreeError` from
   the restore with `veto_restore_failed: <detail>`, each persisted and returned before any further
   task is dispatched, with the task left as it was.
S4 THE LOOP. In `run_job`'s task loop, right after the existing pass over applied, passed, skipped
   and split tasks, a task whose status is `TASK_VETOED` is passed over, and at the pre-task safe
   point, after S3's fold, a task in `veto_unreachable(job.tasks, <every vetoed id>)` is passed
   over without being dispatched. Nothing else in the loop changes.
S5 THE TERMINAL. After the loop, BEFORE the existing `all_done` reading: when at least one task is
   `TASK_VETOED` and every task is applied, passed, skipped, split, vetoed or in the unreachable set
   of every vetoed task, then every unreachable task still `pending` becomes `skipped`, the job
   becomes `JOB_BLOCKED` with `error` exactly `all_remaining_work_vetoed: vetoed <ids>;
   unreachable <ids>` — task ids comma-and-space separated in plan order, `none` for an empty
   set — and `job.metadata["veto_terminal"] = {"vetoed": [...], "unreachable": [...]}`; the DoD
   gate does not run, no run manifest is written, and the record is persisted as the existing
   path does. The task cap's `paused` keeps precedence when a runnable `pending` task remains.
S6 THE MANIFEST'S VOCABULARY, in `packages/orchestration/run_manifest.py`, per D2 (6):
   `"vetoed"` joins `VALID_TASK_STATUSES`; `_TASK_EXPECTATION_ALLOWED_STATUSES` gains `"vetoed"`
   for `EXPECT_SKIPPED`, `EXPECT_EXECUTED`, `EXPECT_PRIOR_EPISODE` and
   `EXPECT_DISPATCHED_NO_CALLS`, and `_COMPLETED_WORKED_STATUSES` does not change; and where the
   expectation of a task that owns no run is derived, a `vetoed` task is `EXPECT_SKIPPED` as a
   `skipped` one is. In `tests/orchestration/test_task_expectation_status_truth.py`, `_ALLOWED`
   gains the same four entries and `test_the_status_vocabulary_matches_the_jobplan` gains
   `PJ.TASK_VETOED`; nothing else in that file changes.
S7 THE WIRING GUARDS. `packages/orchestration/task_veto.py` now has a production importer, so its
   `ALLOWED_UNWIRED` entry in `tests/test_no_orphan_modules.py` is removed, and
   `packages.orchestration.task_veto` joins `tests/orchestration/import_reachability_allowlist.txt`
   in its sorted place — the one line `tests/orchestration/test_import_reachability.py` then asks
   for, and no other.

THE TESTS — a NEW FILE at `tests/orchestration/test_task_veto_runner.py`, with `REMEDY_DATA_DIR`
monkeypatched to `tmp_path`, planned jobs built as `_save_job` in
`tests/orchestration/test_task_edit_runtime.py` builds them (an approved plan, a plain directory as
the repository for a copy job), vetoes recorded through `task_veto.veto_task_command` against the
control root `safe_points.control_root()` resolves under that data root, and runs through `run_job`
with `pingpong_provider.FakeProvider`. It must cover at least: a diamond A, B and C after A, D after
B and C, with B vetoed before the run — A and C applied, B vetoed, D skipped, the job `blocked`
with the exact error, B and D owning no run, and `task_vetoes` holding B's reason verbatim with
`unreachable_task_ids` D; every task vetoed — nothing dispatched and the error naming them all with
`unreachable none`; a job file's tasks without plan metadata, the second of three vetoed — the
first applied, the third skipped; a veto recorded DURING the run by a builder provider that vetoes C
while A runs — C never dispatched; a first run whose failing provider blocks A and skips an
independent task E, A then vetoed, and a relaunch with a passing provider — E back to pending and
applied, A's dependents staying skipped; the task cap (`max_tasks=1`) parking a run after a veto
folded, whose paused manifest validates with the vetoed task as `skipped`; an inert veto of an
applied task; a corrupt veto file blocking the job with `task_veto_control_error` and zero tasks
dispatched; and in a GIT repository as `tests/orchestration/test_job_worktree_integration.py`
builds one, a builder that writes a file and never passes, so the task blocks with that file in the
job workspace, then a veto and a relaunch — the file gone before the next task starts, `restored`
true, and the job `blocked` with the veto error. In `tests/orchestration/test_worktrees.py`, tests
of `restore_tree` for a modified, an added, a deleted, an executable and a symbolic-link path, a
nested directory left empty, and the equality check. In `tests/orchestration/test_task_veto.py`,
R-1065's sequential retry after a failed event write leaving exactly one event, and both
`task_already_vetoed` routes answering the one refused shape with the request id.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads: `.agent/authored/f027-r2-block.md`,
  `.agent/authored/f027-r2-plan.md` and `.agent/authored/f027-r2-records.diff`, by
  `shutil.copyfile`. Subject: `F027 R2 C1: copy round 2 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 126. STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F027 R2 C2: book round 1, register R-1065, record D2`
  Expected by `git show --numstat`: 69/0 decisions.md, 4/0 live_review.md, 11/11 plan.md.
C3 — R-1065 and THE RESTORE: S1 in `task_veto.py`, S2 in `worktrees.py`, and their tests in
  `tests/orchestration/test_task_veto.py` and `tests/orchestration/test_worktrees.py`.
  Subject: `F027 R2 C3: repair R-1065 and add worktrees.restore_tree`
C4 — THE FOLD: S3 to S7 — `pingpong_job.py`, `run_manifest.py`, the status-truth test, the orphan
  entry and the reachability line. Subject: `F027 R2 C4: fold a veto in the linear runner`
C5 — THE RUNNER TESTS AND THE MUTATION TOOL: `tests/orchestration/test_task_veto_runner.py` and
  `.agent/authored/f027-r2-mutations.py`. Subject: `F027 R2 C5: test the runner's fold of a veto`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, and
  appended to `.agent/live_review.md` a blank line and then exactly one line
  `Landed: R-1065 — <one sentence naming what changed>, at <C3's short SHA>.`, never a `Done:`
  line (docs/agents/planner_reviewer_prompt.md §4 item 4).
  Subject: `F027 R2 C6: rewrite handoff for round 2`. Then `git push`, and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/task_veto.py`, `packages/orchestration/worktrees.py`,
   `packages/orchestration/pingpong_job.py`, `packages/orchestration/run_manifest.py`,
   `tests/orchestration/test_task_veto.py`, `tests/orchestration/test_worktrees.py`,
   `tests/orchestration/test_task_expectation_status_truth.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/orchestration/test_task_veto_runner.py`, and `.agent/handoff.md`. Report the list
   `git diff --name-only 25ab44de` measures after C6. Do NOT touch
   `packages/orchestration/long_run_executor.py`, `pause_control.py`, `safe_points.py`,
   `dag_schedule.py`, `pingpong_loop.py`, `ui_server.py`, `apps/`, `docs/`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. If an existing
   test outside your path set goes red because of S1 to S7, report it with its output and stop;
   do not edit it.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every worktree `git worktree list` showed at your step 4, and every stash, alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F027 exactly one, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload the line count, byte count and sha256 you measured against the
 table; then each `.agent/authored/f027-r2-*` payload copy compared byte for byte with its source
 (the block copy against `.remedy-wt/f027-r2/block.md`), read back with `git show <C1>:<path>`.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 295025 | b866146d3419b4856d42e18e56359086df9a469389b13efed6b1a01cd62b3a68 |
 | .agent/decisions.md | 2162102 | e9152eb667c14f8ce4828ffbf12bac2359af2fc4434242dcfb381d8bf0f0e1ab |
 | .agent/plan.md | 1567 | 0cb52ffa8ec84b08caeb9ec2dba6921aeba0e163c5c53bfb6f8084d2c234cb0d |
 Also the open set by distinct id, with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's text at C2 (the reviewer read `['R-1065']`), and the ledger's last line, which
 must begin `- R-1065 — `.

G3 THE CODE — `python3 -m ruff check` over every Python file of constraint 3's path set at the
 last code commit, and `git diff -U0 <C3> <C4> -- tests/orchestration/test_task_expectation_status_truth.py
 tests/test_no_orphan_modules.py tests/orchestration/import_reachability_allowlist.txt`, reported
 whole, which must hold exactly S6's and S7's lines.

G4 THE TESTS — in the primary checkout at the last code commit, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_veto_runner.py tests/orchestration/test_task_veto.py tests/orchestration/test_worktrees.py tests/orchestration/test_task_expectation_status_truth.py tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_zero_call_expectations.py tests/orchestration/test_run_manifest_task_history_chain.py tests/orchestration/test_pause_manifest.py tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_pingpong_job_dod_gate.py tests/cli/test_job_pause.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file and the golden path, serially,
 inside its authoring tree carrying the round's records, and read `688 passed` at real exit code
 0. Report every `SKIPPED` line, the nodes each new or grown test file contributes
 (`--collect-only -q`), and account for every difference from the reviewer's count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r2-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_task_veto_runner.py`, `tests/orchestration/test_task_veto.py` and
 `tests/orchestration/test_worktrees.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and last
 and ends with `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations:
  m1 the pre-task fold is removed, so only the fold before the loop runs;
  m2 the fold never calls `restore_tree`;
  m3 the loop dispatches an unreachable task;
  m4 the fold never sends a skipped task back to pending;
  m5 the fold sends every skipped task after the vetoed one back to pending, unreachable ones too;
  m6 the terminal branch is removed;
  m7 the terminal's error leaves out the unreachable set;
  m8 the fold vetoes a task whose status is outside `VETOABLE_TASK_STATUSES`;
  m9 the fold swallows a `TaskVetoError` and dispatches on;
  m10 `restore_tree` never deletes a path the tree lacks;
  m11 `restore_tree` drops the executable bit;
  m12 `"vetoed"` is left out of `VALID_TASK_STATUSES`;
  m13 the gate's `task_already_vetoed` route repairs no event (R-1065 as it stood);
  m14 the lost race answers `{"outcome": "task_already_vetoed"}` as before.
 Run it in `git worktree add --detach .remedy-wt/f027-r2-mut <last code commit>` and report its
 whole output. EVERY mutation must be red; a green one is reported as green, never papered over,
 and you then add the test that catches it before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f027-r2-mut`, `git worktree prune`, `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty; `git log --oneline`
 from `25ab44de` to the tip; `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected, every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F027, round 2, and says in one sentence how much context you had left. Where S1 to S7
leave a choice open, make it, say so in the deviations, and never widen the path set for it.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then the rest of T001 — a task vetoed while its provider call runs, and the cycle
executor's reading of a veto. State the open-findings count, 1 (R-1065, landed this round and
awaiting the reviewer's resolution), and the operator-questions count, 5.
