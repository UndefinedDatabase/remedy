STEP F028 R2 — BOOK ROUND 1 AND R-1076, RECORD D2, REPAIR R-1076, AND LAND THE FIRST HALF OF T002: the confirmation, the runner's fold at four points, the `plan_add_task` edit kind, and the provenance on the task entry and in the edit log

GOAL
Round 1 passed. Book its gate entry and the registration of R-1076, record DECISION F028 D2 and a
prose slip, repair R-1076, and land the first half of T002: `confirm_task_injection` publishing a
confirmed injection as a second create-only control file, `run_job` folding every confirmed
injection into its own record at four points so the task runs in the same job, the `plan_add_task`
edit kind the fold logs, and the provenance `origin` `human_injected` on the task entry.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Read DECISIONS F028 D1 and D2 in
`.agent/decisions.md` (D2 arrives with C2) before you write code: they are the design. Read
`packages/orchestration/task_edit_runtime.py`'s `edit_task_at_runtime` and
`packages/orchestration/pingpong_job.py`'s `_fold_task_vetoes` whole first: S4 copies the first's
shape and S5 the second's.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/`, `.remedy-wt/f028-r2-sim/`  The reviewer's simulation trees.
  `.remedy-wt/f028-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f028-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f028-task-injection`, and `git log --oneline -1` must read `4b6ccd1d`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 89 | 15410 | eee1df8a3cef7ebbfda08fe8a7f0ba1c2825e2b3af76fbde7ff78309827a198a |
| plan.md | 31 | 1161 | b5dd27102ef67aa1efc7a465d85701cebba375a7f68a62b2d1c04dd465584386 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `4b6ccd1d`. It appends round 1's gate entry and
R-1076's registration to `.agent/live_review.md`, DECISION F028 D2 to `.agent/decisions.md`, and
one line to `.agent/prose_slips.md`.

THE SPECIFICATION
S1 R-1076. `read_injection_draft` in `packages/orchestration/task_injection.py` raises
   `TaskInjectionError` for a record whose `expires_at` is missing, not a `str`, not parseable by
   `datetime.fromisoformat`, or parsed without a time zone; the expiry comparison is otherwise
   unchanged.
S2 THE EDIT KIND. In `packages/orchestration/plan_editing.py`, a function `_add_task(tasks, args)`
   reads `args["task"]` through `PlannedTask.model_validate` (a missing key or a validation error
   is `_refuse_args` with the reason), refuses an id already among `tasks` with `_refuse_args`
   naming it, and answers `[*tasks, task]`. `_EDITS` gains `"plan_add_task": _add_task` as its
   LAST entry. `PLAN_EDIT_COMMANDS` becomes the explicit tuple of the six commands it holds today,
   in today's order, with a comment naming DECISION F028 D2 (5): an add reaches a plan only
   through an injection.
S3 THE CONFIRMATION, in `task_injection.py`. `ORIGIN_HUMAN_INJECTED = "human_injected"` and
   `INJECTED_TASKS_DIRNAME = "injected_tasks"`. `confirmed_injections(job_id, *,
   control_root_path=None) -> tuple[dict, ...]` reads every file of that directory, ordered by
   `(confirmed_at, draft_id)`, `()` when the directory or the job's control directory is absent,
   and raises `TaskInjectionError` for a file that is not a JSON object or lacks a string
   `draft_id` or a dict `task`. `confirm_task_injection(job, confirm_token, *, actor, now=None,
   control_root_path=None) -> dict` NEVER raises for a refusal and answers `{"outcome":
   "refused", "code", "detail"}` from the first of, in order: S4 of round 1's terminal check
   (`job_terminal`); `read_injection_draft(job.job_id, confirm_token, now=now, ...)` refusing
   (its own code); a record whose `job_id` is not the job's (`draft_unknown`); a `status` other
   than `confirmable` (`draft_needs_decision`); a confirmation file for this draft already
   present (`already_confirmed`); a `job.task_plan` round 1's reading of it refuses
   (`no_task_plan`); the draft's task id already an id of the plan or of a confirmed injection the
   record does not hold, or a `depends_on` id in neither set (`draft_stale`, the detail telling
   the operator to draft again); the two sets together at `MAX_PLAN_TASKS` or more (`plan_full`).
   A refusal writes nothing. Otherwise it publishes ONE create-only file in
   `INJECTED_TASKS_DIRNAME`, named as round 1 names a draft file, holding `injected_task_v` 1,
   `job_id`, `draft_id`, `task`, `placement`, `task_rationale`, `text`, `drafted_by` (the draft's
   `actor`), `actor` (this call's, bounded as round 1 bounds it) and `confirmed_at`, through a
   helper `_publish_confirmed_injection(job_id, draft_id, record, *, control_root_path)` written
   as round 1's `_publish_injection_draft` is, a lost publication race answering
   `already_confirmed`; and answers `{"outcome": "confirmed", "job_id", "draft_id", "task_id"`
   (the planned id)`, "placement", "confirmed_at"}`. "A confirmed injection the record does not
   hold" means one whose `draft_id` is not a key of `job.metadata.get("task_injections", {})`.
S4 THE APPLY, in `task_injection.py`: `apply_injection_to_job(job, record, *, now=None) -> dict`
   changes only the in-memory `job`, and raises `TaskInjectionRefused("injection_invalid",
   detail)` leaving `job` untouched when `job.task_plan` does not read as a plan or
   `plan_editing.apply_edit(plan, "plan_add_task", {"task": record["task"]})` raises
   `PlanEditRefused` (its detail carried over). Otherwise, as `edit_task_at_runtime` does:
   `map_task_plan_to_tasks(new_plan)`, `record_llm_task_deliverables(mapped)`, and the one mapped
   entry whose `inputs["plan"]["planned_id"]` is the new id is APPENDED to `job.tasks`, its
   `inputs["plan"]` gaining `origin` (`ORIGIN_HUMAN_INJECTED`), `plan_rationale` (the placement's
   `rationale`), `task_rationale` and `injection_draft_id`; the new body is `new_plan.model_dump()`
   plus the old body's `_`-prefixed keys, its `PLAN_VERSION_KEY` one above `plan_version(body)`,
   its `APPROVED_PLAN_HASH_KEY` re-sealed with `plan_content_hash` exactly when the old body's
   `_approval` is `approved` and carried a hash, and its `EDIT_LOG_KEY` list extended by one entry
   `{"version", "ts", "actor": record["actor"], "command": "plan_add_task", "args": {"task":
   record["task"]}, "before", "after", "injection"}` whose `injection` holds `draft_id`,
   `task_id` (the entry's), `planned_id`, `origin`, `basis` (the placement's), `plan_rationale`,
   `text`, `confirmed_at` and `dod_resync_pending` (`job_dod_path(job.job_id).is_file()`). It
   answers `{"task_id", "planned_id", "folded_at"}`.
S5 THE FOLD, in `pingpong_job.py`: `_fold_task_injections(job, control_root_path) -> bool`, with
   a docstring naming DECISION F028 D2 (3), imports `task_injection` inside its body, reads
   `confirmed_injections` (a `TaskInjectionError` sets `JOB_BLOCKED` and
   `job.error = f"task_injection_control_error: {exc}"`, persists, answers True), and for every
   record whose `draft_id` is not a key of `job.metadata.setdefault("task_injections", {})` calls
   `apply_injection_to_job` and stores under that key `{"task_id", "planned_id", "folded_at"}`,
   or on `TaskInjectionRefused` `{"inert": exc.detail, "folded_at"}`; it persists when anything
   changed and answers False. `run_job` calls it at four points, each as
   `if _fold_task_injections(job, _control): return job`: (a) directly after the veto fold before
   the task loop; (b) directly after the veto fold at the pre-task safe point; (c) as the last
   statement of the loop body, after the post-task safe point's stop check; (d) directly before
   the comment `# F027 D2 (5): THE TERMINAL`, where `len(job.tasks)` is read before the call and
   a larger length after it sets `job.state = JOB_PAUSED`.
S6 THE GUARD LISTS, both in the commit that adds S5: `tests/test_no_orphan_modules.py` loses its
   `ALLOWED_UNWIRED` entry for `packages/orchestration/task_injection.py`, and
   `tests/orchestration/import_reachability_allowlist.txt` gains the line
   `packages.orchestration.task_injection` between `packages.orchestration.task_edit_runtime` and
   `packages.orchestration.task_veto`. The reviewer measured, by wiring the module the same way
   in its simulation tree, that these two guards and no other go red without these edits, and
   that the reachability guard names exactly that one module.

THE TESTS
In `tests/orchestration/test_task_injection.py`: R-1076's four cases; each S3 refusal code, with
no confirmation file written; a confirmed answer whose file reads back through
`confirmed_injections`; `already_confirmed` on the second call; two drafts of one plan, the first
confirmed, the second refused `draft_stale`; `plan_full` counted over confirmed injections;
`confirmed_injections` ordered by `confirmed_at` and raising on a corrupt file; S4 appending one
entry with the four provenance keys, bumping the version, re-sealing an approved plan's hash to
`plan_content_hash` of the new body and leaving an unapproved plan without one, writing the log
entry with its `injection` block, `dod_resync_pending` True with a DoD file present and False
without, `replay_edits(original, edits)` reproducing the new plan's tasks, and a record whose
`depends_on` names a missing task raising `injection_invalid` with the job unchanged. In
`tests/orchestration/test_plan_editing.py`: `plan_add_task` appends; a duplicate id and a missing
`task` are refused; `test_the_six_commands_are_the_feature_files_six` stays as it is. NEW FILE at
`tests/orchestration/test_task_injection_runner.py`, built on the fixtures and fake builders of
`tests/orchestration/test_task_veto_runner.py`: a confirmation published before `run_job` runs
its task in the same run, the job `completed`, the entry carrying `origin` `human_injected`; a
builder that drafts and confirms an injection while the job's LAST task runs, after which the
injected task runs in the same run and the job completes; a wrapper around the real
`_fold_task_injections` that publishes a confirmation just before the call made at point (d),
after which the job is `paused` with the injected task pending and a second `run_job` completes
it; an injection already folded is never folded twice across two runs; a corrupt confirmation
file blocks the job with the `task_injection_control_error:` prefix and dispatches nothing; and
an inert fold records its reason and dispatches nothing new.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — copy this block and the payloads: `.agent/authored/f028-r2-block.md`,
  `.agent/authored/f028-r2-records.diff` and `.agent/authored/f028-r2-plan.md`, by
  `shutil.copyfile`. Subject: `F028 R2 C1: copy round 2 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 120; STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F028 R2 C2: book round 1, register R-1076, record D2 and a prose slip`
  Expected by `git show --numstat`: 60/0 decisions.md, 4/0 live_review.md, 8/8 plan.md, 1/0 prose_slips.md.
C3 — S1 to S4: `packages/orchestration/task_injection.py` and `packages/orchestration/plan_editing.py`.
  Subject: `F028 R2 C3: repair R-1076, confirm an injection, apply it to a job, and add the plan_add_task edit`
C4 — S5 and S6: `packages/orchestration/pingpong_job.py`, `tests/test_no_orphan_modules.py`,
  `tests/orchestration/import_reachability_allowlist.txt`.
  Subject: `F028 R2 C4: fold confirmed injections into run_job at four points`
C5 — THE TESTS: the three test files above. Subject: `F028 R2 C5: test the confirmation, the apply, the edit kind and the runner's fold`
C6 — THE TOOL: `.agent/authored/f028-r2-mutations.py`. Subject: `F028 R2 C6: add the round 2 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F028 R2 C7: rewrite handoff for round 2`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C3 and C5 before you
   commit them: a commit that would reach 500 is split into parts with their own subjects (C3a
   and C3b, C5a and C5b), each part leaving every test of the selection green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `packages/orchestration/task_injection.py`, `packages/orchestration/plan_editing.py`,
   `packages/orchestration/pingpong_job.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/orchestration/test_task_injection.py`, `tests/orchestration/test_plan_editing.py`,
   `tests/orchestration/test_task_injection_runner.py`, and `.agent/handoff.md`. Report the list
   `git diff --name-only 4b6ccd1d` measures after C7. Do NOT touch
   `packages/orchestration/task_veto.py`, `packages/orchestration/task_edit_runtime.py`,
   `packages/orchestration/schemas/models.py`, `packages/orchestration/ui_server.py`, anything
   under `apps/`, `docs/`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C7, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
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
 against the PAYLOADS table; then compare each `.agent/authored/f028-r2-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r2/block.md`), read back with
 `git show <C1>:<path>`. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 313089 | 8cf8fc2a97363c1988bef8eabdf051347b5796605f48f7a9589d3a90b64768f6 |
 | .agent/decisions.md | 2255784 | e2c21f08ff91868b56048a033185ee244e37932b3926b800221b11cb85e580ff |
 | .agent/prose_slips.md | 372463 | eaf83ba1b2cff40b2363f654d4f15e1867c44b209830a730ae401a64e0c17eb1 |
 | .agent/plan.md | 1161 | b5dd27102ef67aa1efc7a465d85701cebba375a7f68a62b2d1c04dd465584386 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at
 `4b6ccd1d` and at C2 (the reviewer read `[]` and `['R-1076']`), and `git diff --name-only <C1>
 <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/task_injection.py
 packages/orchestration/plan_editing.py packages/orchestration/pingpong_job.py
 tests/orchestration/test_task_injection.py tests/orchestration/test_plan_editing.py
 tests/orchestration/test_task_injection_runner.py tests/test_no_orphan_modules.py` at C6, with
 its real exit code. Then quote from the diff the whole of `_fold_task_injections`, its four call
 sites with three lines of context each, `_add_task`, and the refusal ladder of
 `confirm_task_injection`.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py tests/orchestration/test_plan_editing.py tests/orchestration/test_plan_edit_execution.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_manifest.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_worktree_resume_cli.py tests/orchestration/test_job_plan.py tests/orchestration/test_mint_call_sites.py tests/orchestration/test_human_change_one_path.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_unified_store_parity.py tests/orchestration/test_run_manifest_strict_boundaries.py tests/orchestration/test_budget_guard.py tests/orchestration/schemas/test_schemas.py tests/orchestration/test_structured_outputs.py tests/orchestration/test_import_reachability.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the new runner test file, serially, in the primary
 checkout at `4b6ccd1d`, and read `1560 passed, 7 skipped` at real exit code 0; the seven skips
 are the F252 quarantines and stay skipped. Report every `SKIPPED` line, the node counts of the
 three edited test files by `--collect-only -q` at `4b6ccd1d` and at C6, and account for any
 difference from 1560 beyond the nodes the round adds. Then
 `python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f028-r2-mutations.py` takes a worktree path and,
 for each mutation below, edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py
 tests/orchestration/test_plan_editing.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: label, exit
 code, failed count, failing node ids. An unmutated control runs first and last; it ends with
 `restored byte-identical: True` per file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `read_injection_draft` treats a record without `expires_at` as live (task_injection.py);
  m2 `confirm_task_injection` skips the status check (task_injection.py);
  m3 `confirm_task_injection` skips the task-id half of the stale check (task_injection.py);
  m4 `apply_injection_to_job` omits `origin` (task_injection.py);
  m5 `apply_injection_to_job` never re-seals the approval hash (task_injection.py);
  m6 `apply_injection_to_job` leaves the plan version unchanged (task_injection.py);
  m7 `apply_injection_to_job` writes `dod_resync_pending` False always (task_injection.py);
  m8 `_add_task` admits a duplicate id (plan_editing.py);
  m9 fold point (a) is removed (pingpong_job.py);
  m10 fold point (c) is removed (pingpong_job.py);
  m11 fold point (d) no longer sets `JOB_PAUSED` (pingpong_job.py);
  m12 the fold ignores `job.metadata["task_injections"]` and folds every record (pingpong_job.py);
  m13 the fold's `TaskInjectionError` branch answers False without blocking (pingpong_job.py).
 Run it: `git worktree add --detach .remedy-wt/f028-r2-mut <C6>`, then
 `python3 -B .agent/authored/f028-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r2-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, and you then add the test that catches it in C5 before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, empty; `git log --oneline -n 8`, showing
 C7 back to C1 and `4b6ccd1d` in order (more lines if constraint 2 split a commit);
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit, per gate and for R-1076), the deviations, and the next expected action. Name the
commit that lands R-1076's repair; do not write a `Done:` or `Landed:` line into the ledger. Your
Session section reads SESSION 1 of feature F028, round 2, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then the second half of T002 — the shortfall seed's three answers, its labels as a
mapping, and the run-log event with its readers. State the open-findings count, 1 (R-1076, its
repair awaiting review), and the operator-questions count, 0.
