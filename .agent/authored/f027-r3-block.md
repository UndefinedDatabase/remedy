STEP F027 R3 — T001 COMPLETE: a task vetoed while its call runs finishes that call and is then vetoed while the run goes on, the cycle executor withholds a vetoed task and its dependents, and R-1066's repair

GOAL
Book round 2's verdict, resolve R-1065, register R-1066, record DECISION F027 D3, and land it:
`run_job` reads a veto of its in-flight task at the next in-task safe point, so the call already
running finishes, then folds it with the workspace restored and runs on to the next task;
`run_cycles` withholds vetoed tasks and their dependents at every pick and ends `blocked` naming
them; and `worktrees.restore_tree` survives a directory standing where the tree holds a file — with
tests and a mutation tool proving they bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S4 below. Only the `.agent/` records travel as
payloads. Read DECISION F027 D3 in `records.diff` before you write code: it is the design.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-r3-dry/`, `.remedy-wt/f027-r3-drafts/`, `.remedy-wt/f027-review/` and every
                                  older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f027-task-veto`, and `git log --oneline -1` must read `cf6dc546`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 33 | 1256 | c75da9842f99142ba9031bc04063f9434bbacc15938b4d7cd32cd27623a182cc |
| records.diff | 70 | 12143 | 64a471ee1cf66b8a672291ed58326d892a72f2058f5cbb806d173cf7a0a6cddd |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `cf6dc546`. It appends to `.agent/live_review.md`
round 2's gate entry, R-1065's `Done:` paragraph and R-1066's registration, and to
`.agent/decisions.md` DECISION F027 D3.

THE SPECIFICATION
S1 R-1066, in `packages/orchestration/worktrees.py`'s `restore_tree`: before it writes back a
   path the tree holds as a file or a symbolic link, whatever else stands at that path — a
   directory above all — is removed, so the file-to-directory case restores; and every `OSError`
   its own filesystem operations raise is re-raised as `WorktreeError` naming the path, so the
   fold blocks the job with `veto_restore_failed` instead of letting the exception out of
   `run_job`. Nothing else in `worktrees.py` changes.
S2 THE IN-TASK READING, in `packages/orchestration/pingpong_job.py`. Two module constants beside
   the pause's prefixes, `_VETO_REASON_PREFIX` and `_VETO_ERROR_REASON_PREFIX`, and a helper
   `_reason_is_veto(reason)` true for either. In `run_job`'s `_run_stop_check`, after the stop
   check and the in-flight pause reading both answered None: read `task_veto.vetoed_tasks(job.job_id,
   control_root_path=_control)`; when an entry names the in-flight `task`, answer a `_StopSignal`
   with the job id, the entry's `request_id`, the reason `_VETO_REASON_PREFIX` followed by that
   request id, and the source `veto`; when the read raises `TaskVetoError`, answer one with an
   empty request id, the reason `_VETO_ERROR_REASON_PREFIX` followed by the error's text, and the
   source `veto`; otherwise None.
S3 THE HALT, in `run_job`'s `if result.final_status == "stopped":` branch, FIRST, before the pause
   reading: when `_reason_is_veto(result.stop_reason)`, keep the run fields already recorded on
   the task, set `task.reviewer_verdict` from the last round that reached a reviewer as the stop
   path does, and call `_fold_task_vetoes(job, job_handle, _control)`; when it answers True, return
   the job. When the task is `TASK_VETOED` after the fold, close the task log with
   `_log_task_ended(task_log, task, "vetoed")`, persist the budget actuals and the job, and
   `continue` the task loop, so the next task is considered. When it is not — the control area no
   longer names it — block the job with the error
   `veto_fold_failed: task <task id> halted for a veto the control area no longer holds`, persist
   and return. The halt writes no `job_stopped` event, no stop post-mortem and no stop archive, and
   never reaches `_stop_job`.
S4 THE CYCLE EXECUTOR, in `packages/orchestration/long_run_executor.py`. `ready_tasks` gains a
   keyword `vetoed_ids: Collection[str] = ()`: its seeds are the vetoed ids naming a task of the
   plan whose status, read by its string value, is not `completed`, and they join the withheld
   seeds with their transitive dependents exactly as the paused seeds do; its docstring names
   DECISION F027 D3. A helper reads `task_veto.vetoed_tasks` for the job and turns a
   `TaskVetoError` into the loop's own observed-error route, which ends the run `TERMINAL_BLOCKED`
   with the stop reason `task_veto_control_error: <detail>` as the pause-control error route does.
   `run_cycles` reads the vetoed ids at the batch boundary and before every pick, beside the paused
   ids, and passes them to both `ready_tasks` calls there. In the nothing-ready chain, after the
   paused branch and before the generic one: when the vetoed seeds are non-empty and at least one
   seed or one of their dependents is `pending`, the run ends `TERMINAL_BLOCKED` with the stop
   reason `all_remaining_work_vetoed; vetoed=<seed ids>; unreachable=<dependent ids>` — ids in plan
   order joined by commas, `none` for an empty list, the dependents those of
   `blocked_downstream` that are not `completed`. The cycle executor never writes `vetoed` into a
   task's status.

THE TESTS — `tests/orchestration/test_task_veto_runner.py` gains, for `run_job` over a copy job
built as its existing tests build one: a builder provider that records a veto of its own task B
during B's first builder call — B's builder call finished and its reviewer never called, B
`vetoed` with its run id kept, the independent C applied, D skipped, the job `blocked` with the
veto error, the task log's `task_run_failed` event for B carrying outcome `vetoed`, and no
`job_stopped` event in the ledger; the same in a GIT job as its existing git test builds one, where
the builder writes a file before it vetoes — the file gone, `restored` true; and an unreadable veto
area met at the in-task reading — the job `blocked` with `task_veto_control_error`. A NEW FILE at
`tests/orchestration/test_task_veto_cycles.py`, driving `run_cycles` through an injected
`task_step` as `tests/orchestration/test_pause_resume_cycles.py` does, with `ready_tasks` unit tests
over the diamond (veto B: B and D withheld; a veto of a completed task inert) and runs where B is
vetoed before the run — A and C completed, B and D pending, the stop reason exact —, where a step of
A vetoes C during the run — C never picked —, where the only veto names a completed task — the run
green —, and where the veto area is unreadable — `task_veto_control_error`. In
`tests/orchestration/test_worktrees.py`, R-1066's file-to-directory restore and an `OSError` of the
restore surfacing as `WorktreeError`.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads: `.agent/authored/f027-r3-block.md`,
  `.agent/authored/f027-r3-plan.md` and `.agent/authored/f027-r3-records.diff`, by
  `shutil.copyfile`. Subject: `F027 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 103. STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F027 R3 C2: book round 2, resolve R-1065, register R-1066, record D3`
  Expected by `git show --numstat`: 48/0 decisions.md, 6/0 live_review.md, 11/15 plan.md.
C3 — R-1066: S1 and its tests in `tests/orchestration/test_worktrees.py`.
  Subject: `F027 R3 C3: repair R-1066 in worktrees.restore_tree`
C4 — THE CODE: S2 and S3 in `pingpong_job.py`, S4 in `long_run_executor.py`.
  Subject: `F027 R3 C4: veto an in-flight task and withhold vetoed tasks in the cycle executor`
C5 — THE TESTS AND THE MUTATION TOOL: the grown `tests/orchestration/test_task_veto_runner.py`, the
  new `tests/orchestration/test_task_veto_cycles.py`, and `.agent/authored/f027-r3-mutations.py`.
  Subject: `F027 R3 C5: test the in-flight veto and the cycle executor's veto`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, and
  appended to `.agent/live_review.md` a blank line and then exactly one line
  `Landed: R-1066 — <one sentence naming what changed>, at <C3's short SHA>.`, never a `Done:`
  line (docs/agents/planner_reviewer_prompt.md §4 item 4).
  Subject: `F027 R3 C6: rewrite handoff for round 3`. Then `git push`, and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C5a and C5b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/worktrees.py`, `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/long_run_executor.py`, `tests/orchestration/test_worktrees.py`,
   `tests/orchestration/test_task_veto_runner.py`, `tests/orchestration/test_task_veto_cycles.py`,
   and `.agent/handoff.md`. Report the list `git diff --name-only cf6dc546` measures after C6. Do
   NOT touch `packages/orchestration/task_veto.py`, `pause_control.py`, `safe_points.py`,
   `dag_schedule.py`, `pingpong_loop.py`, `run_manifest.py`, `ui_server.py`, `apps/`, `docs/`,
   `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md` or
   `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. If an existing
   test outside your path set goes red because of S1 to S4, report it with its output and stop;
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
 table; then each `.agent/authored/f027-r3-*` payload copy compared byte for byte with its source
 (the block copy against `.remedy-wt/f027-r3/block.md`), read back with `git show <C1>:<path>`.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 300067 | 269de06879d723de4bbe89cea4b57b4c6cbc709715bd3217f97a8fdfce5acc36 |
 | .agent/decisions.md | 2166498 | e63c10eb87613715f57c1560a4c0d8497ec98a6464d396531601d2c3fcd9066b |
 | .agent/plan.md | 1256 | c75da9842f99142ba9031bc04063f9434bbacc15938b4d7cd32cd27623a182cc |
 Also the open set by distinct id, with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's text at C2 (the reviewer read `['R-1066']`), and the ledger's last line, which
 must begin `- R-1066 — `.

G3 THE CODE — `python3 -m ruff check` over every Python file of constraint 3's path set at the
 last code commit, and `git diff --stat <C2> <C3>`, which must name `worktrees.py` and
 `test_worktrees.py` alone.

G4 THE TESTS — in the primary checkout at the last code commit, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_veto_runner.py tests/orchestration/test_task_veto_cycles.py tests/orchestration/test_task_veto.py tests/orchestration/test_worktrees.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_escalation.py tests/orchestration/test_self_healing_cycles.py tests/orchestration/test_resume_kill.py tests/orchestration/test_checkpoints.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_mission_e2e.py tests/orchestration/test_run_report_hook.py tests/orchestration/test_pause_resume.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_run_manifest_zero_call_expectations.py tests/orchestration/test_task_expectation_status_truth.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file and the golden path, serially,
 inside its authoring tree carrying the round's records, and read `1002 passed` at real exit code
 0. Report every `SKIPPED` line, the nodes each new or grown test file contributes
 (`--collect-only -q`), and account for every difference from the reviewer's count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r3-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_task_veto_runner.py`, `tests/orchestration/test_task_veto_cycles.py`
 and `tests/orchestration/test_worktrees.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and last
 and ends with `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations:
  m1 `_run_stop_check` never reads a veto;
  m2 the `stopped` branch lets a veto halt fall through to the stop path;
  m3 the halt sets `TASK_VETOED` itself instead of calling the fold, so nothing is restored;
  m4 the halt returns the job instead of continuing the loop;
  m5 `ready_tasks` ignores `vetoed_ids`;
  m6 `ready_tasks` withholds the vetoed seeds but not their dependents;
  m7 the cycle executor's veto terminal branch is removed;
  m8 the cycle executor swallows a `TaskVetoError` and picks on;
  m9 `ready_tasks` seeds a vetoed task that is `completed`;
  m10 `restore_tree` removes nothing standing where the tree holds a file;
  m11 `restore_tree` lets an `OSError` escape unconverted.
 Run it in `git worktree add --detach .remedy-wt/f027-r3-mut <last code commit>` and report its
 whole output. EVERY mutation must be red; a green one is reported as green, never papered over,
 and you then add the test that catches it before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f027-r3-mut`, `git worktree prune`, `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty; `git log --oneline`
 from `cf6dc546` to the tip; `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected, every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F027, round 3, and says in one sentence how much context you had left. Where S1 to S4
leave a choice open, make it, say so in the deviations, and never widen the path set for it.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T002 — the replan proposal in the decision inbox with its two-option menu and both
options' documented effects. State the open-findings count, 1 (R-1066, landed this round and
awaiting the reviewer's resolution), and the operator-questions count, 5.
