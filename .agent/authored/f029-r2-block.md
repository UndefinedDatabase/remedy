STEP F029 R2 — BOOK R1, REPAIR R-1080, AND LAND THE FIRST HALF OF T002: the rerun preparation, the attempt fields, the job's rerun list, and the per-task model

GOAL
Round 1 passed. Book its gate entry and register R-1080, record DECISION F029 D2, repair R-1080,
and land the rerun PREPARATION: `prepare_subtree_rerun` in
`packages/orchestration/subtree_rerun.py` takes a job that is not running, re-acquires its
worktree under its lock, resets the subtree with round 1's `apply_subtree_reset`, and returns the
subtree's tasks to pending with the earlier attempt kept on each task; `run_job` then re-executes
exactly those tasks, passing each rerun task's model override to the builder. No command and no
event yet: that is round 3.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code and tests against S1 to S7 below; only the `.agent/` records travel as payloads. Read
DECISION F029 D2 in the booking diff before you write code: it is the design this implements.
Read, before writing: `packages/orchestration/subtree_rerun.py` whole; in
`packages/orchestration/pingpong_job.py` the `TaskEntry` and `JobPlan` classes, the export and
import of both (search `"spec_version": t.spec_version` and `spec_version=int(`), `_task_stream_dir`,
`_acquire_job_workspace`, `_verify_checkpoints`, `_finalize_job_workspace`, `job_resume_refusal`
and the `run_pingpong(` call inside `run_job`; `create`, `remove`, `release_lock`,
`retain_for_recovery`, `set_checkpoint_ref`, `resolve_checkpoint_ref` and `object_exists` in
`packages/orchestration/worktrees.py`; `plan_edit_lock` in `packages/orchestration/plan_editing.py`;
the reset at step S7 of `edit_task_at_runtime` in `packages/orchestration/task_edit_runtime.py`;
`_bounded_actor` in `packages/orchestration/task_veto.py`; and the harness at the top of
`tests/orchestration/test_job_worktree_integration.py`, whose fake providers drive `run_job`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f029-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f029-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f029-r2-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f029-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f029-r2-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f029-subtree-rerun`, and `git log --oneline -1` must read `0ae9f427`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f029-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f029-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 86 | 14419 | bc5d5bb90d471892243191c339e60935a3b669a7973df0bd8c055e742bf5ef5c |
| plan.md | 34 | 1224 | ffa31d57260b51ece7f6f9c81a91a3fed0071a76f8167481481a60590cd2964d |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer generated
it with `git diff HEAD` from a tree at `0ae9f427`. It appends to `.agent/live_review.md` round 1's
gate entry and R-1080's registration, and to `.agent/decisions.md` DECISION F029 D2.

THE SPECIFICATION
S1 R-1080. Step d of `plan_subtree_reset` refuses `worktree_drift` whenever the live head is "",
   whatever `job.worktree_head` holds, with the same detail as today.
S2 THE FIELDS, in `packages/orchestration/pingpong_job.py`, each exported and imported beside
   `spec_version` with a one-line comment naming DECISION F029 D2, a record without the key
   loading the default: on `TaskEntry`, `attempt: int = 1` (imported as `int(... or 1)`),
   `attempts: list = field(default_factory=list)` (imported as a list of dicts) and
   `model_override: str = ""`; on `JobPlan`, `reruns: list = field(default_factory=list)`.
S3 THE MODEL. The `run_pingpong(` call inside `run_job` passes
   `builder_model=(task.model_override or builder_model)`. Nothing else in `run_job` changes.
S4 THE FOLD, pure, in `subtree_rerun.py`: `fold_subtree_rerun(job, reset, *, rerun_id,
   model_override, actor, now, moved_streams) -> dict`, where `reset` is what
   `apply_subtree_reset` answered and `moved_streams` maps a task id to the evidence-relative
   path its streams were moved to. For each task of `reset["subtree"]`, in plan order: when it
   RAN — its `run_id` or its `worktree_commit` is not "", or its status is not `pending` — one
   dict is appended to its `attempts`: `attempt`, `status`, `final_status`, `reviewer_verdict`,
   `test_passed`, `run_id`, `worktree_commit`, `model_override`, `output_artifact_ids`,
   `stream_evidence` (`moved_streams.get(task_id, "")`), `rerun_id` and `ended_at`
   (`now.isoformat()`), and its `attempt` rises by one. Every subtree task then reads
   `status` `pending`, `model_override` the given override, and every one of `run_id`,
   `final_status`, `final_status_detail`, `reviewer_verdict`, `error`, `task_start_tree`,
   `task_start_tree_ref`, `task_start_recorded_at`, `task_attempt_state`, `worktree_commit` and
   `tripped_limit` "", `safe_diff_files` and `output_artifact_ids` empty, `test_passed`,
   `apply_manifest` and `proof_summary` None, and `repair_rounds_used` 0. Every task OUTSIDE the
   subtree whose status is `skipped` returns to `pending`. The job: `worktree_head` is
   `reset["reset_commit"]`; a `completed` job becomes `paused` with `finished_at` ""; any other
   state is kept; `worktree_cleanup_status` is `retained` and `worktree_cleanup_error` "". One
   record is appended to `job.reruns` and returned: `rerun_id`, `root_task_id`, `subtree`,
   `restored_pending` (the outside ids returned from `skipped`, in plan order), `base_commit`,
   `reset_commit`, `paths`, `exact`, `proof`, `pre_task_tree_equal`, `model` =
   `{"override": model_override, "configured": <the job's execution_config builder_model, "" when
   none>, "reason": HUMAN_OVERRIDE_REASON if model_override else ""}`, `actor`, `at`
   (`now.isoformat()`), `state_before` and `state_after`. `HUMAN_OVERRIDE_REASON =
   "human_override"` is a new constant of `subtree_rerun.py`.
S5 THE PREPARATION. `prepare_subtree_rerun(job_id, root_task_id, *, model_override="",
   actor="operator", now=None) -> dict`, in `subtree_rerun.py`. Inside
   `plan_editing.plan_edit_lock(job_id)` it loads the job with `load_job_plan` and raises
   `SubtreeRerunRefused` from the first of, in order, touching nothing on disk:
   `job_not_found`; `model_invalid` for an override not matching
   `^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,127}$` ("" is no override); state `running` —
   `job_running`, detail `"the job is running; pause or stop it, then rerun"`; a state not in
   `RERUN_ADMITTED_STATES` = `completed`, `blocked`, `paused`, `stopped` — `job_not_rerunnable`,
   detail `f"the job is {state!r}; a rerun needs a job that has completed, blocked, paused or
   stopped"`; S2 of round 1's `unknown_task`; `not_worktree_mode` and `task_not_committed` with
   round 1's details; the job's branch missing by `worktrees._branch_exists` — `job_branch_missing`;
   `job.job_initial_tree` "" or not an object by `worktrees.object_exists` —
   `checkpoint_object_missing`. Then `handle = worktrees.create(job_worktree_id(job_id),
   job.repo_path)`, where `WorktreeLockError` is refused `job_running` with the detail above and
   `WorktreeConflictError` `worktree_conflict` with its message. Then `apply_subtree_reset(job,
   root_task_id, handle.path)`: on `SubtreeRerunRefused` a worktree this call created
   (`handle.created`) is removed with `worktrees.remove(handle, keep_branch=True)`, otherwise the
   lock is released with `worktrees.release_lock(handle)`, and the refusal is re-raised with the
   job file unchanged; on any other exception the worktree is kept with
   `worktrees.retain_for_recovery(handle, <the error>)` and the exception propagates. On success:
   `rerun_id` is `f"rerun-{len(job.reruns) + 1}"`; each subtree task that ran and whose
   `_task_stream_dir(job_id, task_id)` exists has that directory moved with `os.replace` to
   `rerun_attempts/<task_id>/attempt-<its attempt>` under `job_evidence_dir(job_id)` (parents
   created; an existing destination raises), recorded evidence-relative in `moved_streams`; S4
   folds; the `job_initial_tree_ref` is set again with `worktrees.set_checkpoint_ref(repo,
   ref, job.job_initial_tree)` when `resolve_checkpoint_ref` does not answer `job_initial_tree`;
   `save_job_plan(job)` runs once; the lock is released with `worktrees.release_lock(handle)`;
   and it answers S4's record plus `job_id` and `worktree_rematerialized` (`handle.created`).
   `actor` is bounded with `task_veto._bounded_actor`; `now` defaults to the current UTC time.
S6 THE ORPHAN GUARD. `subtree_rerun.py` keeps its `ALLOWED_UNWIRED` entry; round 3's command wires
   it. Change the entry's reason only if its words stop being true, and say so.
S7 NOTHING ELSE. No command, no event, no edit to `apps/`, `worktrees.py`, `checkpoints.py`,
   `dag_schedule.py`, `task_edit_runtime.py` or `plan_editing.py`.

THE TESTS — extend `tests/orchestration/test_subtree_rerun.py`, or add
`tests/orchestration/test_subtree_rerun_prepare.py`, with at least:
R-1080: a job with an empty `worktree_head` planned against a missing path refuses
`worktree_drift`, the detail naming `unknown`. S2: a job with every new field set survives
`save_job_plan` and `load_job_plan` equal, and a record written without the four keys loads
`attempt` 1, `attempts` [], `model_override` "" and `reruns` []. S4 over synthetic entries: the
attempt record's keys and values, `attempt` 2, every cleared field, a never-run pending subtree
task with no attempt record and `attempt` still 1, a `skipped` task outside the subtree restored
while an `applied` one is not, `completed` becoming `paused`, `blocked` staying `blocked`, and the
`model` block with and without an override. THE END TO END, driven by `run_job` with fake
providers as `test_job_worktree_integration.py` drives it, over a three-task job file (each task
depends on its predecessor): run it to `completed` (the worktree is removed, the branch kept); put
a marker file into T002's stream directory; `prepare_subtree_rerun(job_id, "T002",
model_override="rerun-model")` answers subtree `["T002", "T003"]`, `exact` True and
`worktree_rematerialized` True; the reloaded job reads `paused`, T002 and T003 `pending` at
`attempt` 2 each with one attempt record holding the old run id and commit, T001 unchanged, one
`reruns` record whose model block reads `{"override": "rerun-model", "configured": ..., "reason":
"human_override"}`, `worktree_cleanup_status` `retained`, the worktree present on T001's tree, the
lock free, and the marker byte-identical at `rerun_attempts/T002/attempt-1/`; then `run_job`
again completes the job with T001's run id unchanged, new run ids for T002 and T003, the old run
directories still present, the branch holding attempt 1's commits, the reset commit and two new
task commits, and each new run's result recording `builder_configured_model` `rerun-model`.
Refusals, each leaving `job.json` byte-identical and no worktree behind: `job_not_found`,
`model_invalid`, `job_running` for state `running` and for a lock the test itself holds through
`worktrees.create`, `job_not_rerunnable` for `planned`, `task_not_committed`, and a completed job
whose recorded `worktree_head` is wrong, refused `worktree_drift` after the worktree was re-added,
with the re-added worktree removed again.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f029-r2-block.md` := this block; `.agent/authored/f029-r2-booking.diff` and
  `.agent/authored/f029-r2-plan.md` := booking.diff and plan.md. All by `shutil.copyfile`.
  Subject: `F029 R2 C1: copy round 2 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 120. Report the number you measure.
C2 — THE BOOKING, in this order: `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F029 R2 C2: book round 1's PASS, register R-1080, record D2`
  Expected by `git show --numstat`: 66/0 decisions.md, 4/0 live_review.md, 10/9 plan.md.
C3 — S1 and its test. Subject: `F029 R2 C3: R-1080 — refuse a rerun whose worktree head cannot be read`
C4 — S2 and S3. Subject: `F029 R2 C4: carry attempts, a model override and reruns on the job record`
C5 — S4, S5 and every other test. Subject: `F029 R2 C5: prepare a subtree rerun on a job that is not running`
  Split into C5a, C5b, ... under constraint 2 when it would reach 500 insertions.
C6 — your mutation tool (G5) saved as `.agent/authored/f029-r2-mutations.py`, then, as its own
  commit, `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`.
  Subjects: `F029 R2 C6a: add the mutation tool` and `F029 R2 C6b: rewrite handoff for round 2`.
  Then `git push origin feature/f029-subtree-rerun` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`; split a commit that would
   reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f029-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `packages/orchestration/subtree_rerun.py`, `packages/orchestration/pingpong_job.py`,
   `tests/orchestration/test_subtree_rerun.py`, optionally
   `tests/orchestration/test_subtree_rerun_prepare.py`, and `tests/test_no_orphan_modules.py` only
   if S6 requires it. Report `git diff --name-only 0ae9f427` at the tip after C6b.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round wrote that is wrong may be corrected
   before C6b, and the correction is declared. An EXISTING test that goes red is never edited to
   pass; report it and stop.
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
 each `.agent/authored/f029-r2-*` copy read back with `git show <C1>:<path>` compared byte for byte
 with its source (the block copy against `.remedy-wt/f029-r2/block.md`). One reading per copy.
G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2287154 | a0109b36884fa89227762c9af219e2a9d1975f673ef2e2147c4582a79e91416d |
 | .agent/live_review.md | 311765 | a0b8341219b70e3a38debefeeea59c8a98bbf4ca259dde9b4e076e8c1e1d30a7 |
 | .agent/plan.md | 1224 | ffa31d57260b51ece7f6f9c81a91a3fed0071a76f8167481481a60590cd2964d |
 Also the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the file's TEXT at `0ae9f427` (the reviewer read it empty) and at C2 (the reviewer read
 `['R-1080']`).
G3 THE CODE — `python3 -m ruff check` over every Python file the round touched, at the tip before
 C6b, with its real exit code; then quote from the commit that landed it the whole of
 `prepare_subtree_rerun` and the `run_pingpong(` call's `builder_model=` line.
G4 THE TESTS — in the primary checkout at C6a, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_subtree_rerun.py tests/orchestration/test_worktrees.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_job_plan.py tests/orchestration/test_job_plan_state_reads.py tests/orchestration/test_job_run_refs.py tests/orchestration/test_pingpong_job_dod_gate.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_job_evidence.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_checkpoints.py tests/orchestration/test_task_veto.py tests/cli/test_job_commands.py tests/cli/test_job_run_invocation_truth.py tests/cli/test_job_pause.py tests/test_subprocess_timeouts.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 If you add `tests/orchestration/test_subtree_rerun_prepare.py`, put it after the first path.
 The reviewer ran this selection serially in the primary checkout at `0ae9f427` and read
 `1233 passed, 7 skipped` at real exit code 0; the seven skips are the F252 quarantines. Report
 every `SKIPPED` line, the node count the round added by `--collect-only -q` over the test files
 it touched, and account for any difference from 1233 plus that count. Then
 `python3 -m apps.cli.main integrity check --json`: the check `high_blockers_open` reads `pass`
 because R-1080 is Low, and report every check's status and `fail_count`.
G5 THE RED PROOFS — your tool `.agent/authored/f029-r2-mutations.py` takes a worktree path, and for
 each mutation below edits the named module INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the round's subtree-rerun
 test files from the worktree's root after purging its `__pycache__` directories, restores the
 bytes, and prints one line per mutation: its label, the exit code, the failed count and the
 failing node ids. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 step d compares the live head with `job.worktree_head` again, as before S1;
  m2 S4 does not raise `attempt`;
  m3 S4 appends no attempt record;
  m4 S4 keeps `worktree_commit`;
  m5 S4 leaves a `skipped` task outside the subtree as it is;
  m6 S4 leaves a `completed` job `completed`;
  m7 the `run_pingpong(` call passes `builder_model` alone;
  m8 S5 releases the lock on a refusal instead of removing a worktree it created;
  m9 S5 does not set the `job_initial_tree_ref` again;
  m10 S5 moves no stream directory;
  m11 the export drops the `attempts` key;
  m12 S4 leaves `worktree_cleanup_status` as it was.
 Run it: `git worktree add --detach .remedy-wt/f029-r2-mut <C6a>`, then
 `python3 -B .agent/authored/f029-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f029-r2-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, then you add the test that catches it in its own commit before C6a and re-run the tool.
 Then `git worktree remove --force .remedy-wt/f029-r2-mut`, `git worktree prune`, and report
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
expected. Your Session section reads SESSION 1 of feature F029, round 2, and says in one sentence
how much context you had left. Mark R-1080 in the handoff as `Landed: R-1080 — <one line>`; never
write a `Done:` line.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then the second half of T002 — `remedy job rerun-subtree` with the subtree's cost
estimate, the cost preview's confirmation, and the run-log event with its readers. State the
open-findings count, 1 (R-1080, landed and awaiting review), and the operator-questions count, 0.
