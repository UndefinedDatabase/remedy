STEP F029 R7 — BOOK R6 AND ITS PROSE SLIP, SPACE THE RUN DETAIL'S CONFIRMATION ROW, AND LAND T003's END-TO-END PROOF: a real job run, its middle task rerun with a model override, the subtree run again, both attempts read back

GOAL
Round 6 passed. Book its gate entry and its one prose slip, give the run detail's confirmation row
the space its render showed it lacks, and prove the feature end to end: a three-task job runs through
the real command line, its middle task is rerun with a model override — once through the live write
door behind the cost preview and once through `remedy job rerun-subtree --yes` — the subtree runs
again, the files are back at their state before the task by tree hash, and both attempts are read
back from the job record, git, the run log, the dashboard, the run records and the final report.
The closure sequence follows this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE TEST IS SPECIFIED, NOT SLICED: you write it against S2.
Read, whole: `tests/ui_server/test_task_injection_e2e_live.py` (your model),
`tests/orchestration/test_subtree_rerun_prepare.py` down to its first test class,
`apps/ui/src/components/graph/RunDetailPopover.tsx` with its style sheet, and in
`packages/orchestration/subtree_rerun.py` the functions `fold_subtree_rerun`,
`prepare_subtree_rerun` and `rerun_subtree_command`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f029-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f029-r7/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f029-r7-sim/`       The reviewer's simulation worktree; do not touch it.
  `.remedy-wt/f029-r7-dry/`       The reviewer's dry-run worktree; do not touch or read it.
  `.remedy-wt/f029-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f029-r7-worker/`    YOURS for logs and scripts; create it if absent. Gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx from the shell; vitest runs through the pytest node of G4.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f029-subtree-rerun`, and `git log --oneline -1` must read `cfd779c6`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f029-r7/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f029-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 19 | 10507 | 0b11f442f40785e3bf0b0a794351620fc7c196dd13e44d49cf44d61943f57717 |
| plan.md | 35 | 1369 | 09426a6990397d3192aa3edfa8579d9394ff22dda437a8d26c29dc04886b58b9 |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer generated
it with `git diff HEAD` from a tree at `cfd779c6`. It appends round 6's gate entry to
`.agent/live_review.md` and one line to `.agent/prose_slips.md`.

THE SPECIFICATION
S1 THE SPACING, in `RunDetailPopover.tsx` and `RunDetailPopover.module.css`: the `<div>` that holds
   "Rerun anyway" and "Cancel" (the one rendered when the outcome's kind is `needs_confirmation`)
   takes a NEW class `confirmActions` instead of `actions`, and the style sheet gains, directly
   after the `.actions` rule, `.confirmActions { display: flex; gap: 8px; margin: 8px 0 0; }`
   written as a multi-line rule in the sheet's own layout. The first row of actions keeps `actions`.
   Nothing else in either file changes.
S2 THE PROOF, a NEW file `tests/ui_server/test_subtree_rerun_e2e_live.py`, structured as the model
   file is — `@pytest.mark.subprocess` on one class `TestSubtreeRerunE2ELive`, a real UI server in
   a thread, real POSTs through `HTTPConnection`, real `python -m apps.cli.main` subprocesses with
   `REMEDY_DATA_DIR` and `PYTHONPATH` in their environment — and keeping its OWN copies of the
   model's helpers it uses, per the model's header rule. Its docstring names DECISIONS F029 D1 to D6.
   THE FIXTURE. The repository is a REAL git repository (init, `user.email`, `user.name`,
   `commit.gpgsign false`, one file, one commit): `_create_job_workspace` in `pingpong_job.py`
   chooses worktree mode only for a git repository, and a rerun is refused outside it. The job is an
   APPROVED plan of three tasks saved directly as the model's `_save_approved_two_task_job` saves
   its two: A; B depending on A; C depending on B; each with `est_tokens_band` "S" and `files_hint`
   `["docs/README.md"]` (the CLI's fake builder writes that one file for every task). Run 1 is
   `job run <id> --builder-provider fake --reviewer-provider fake --tasks 0`; it must exit 0 with
   the job `completed`, every task `applied_to_job_workspace`, each on `attempt` 1 with no
   `attempts`.
   TEST (a) `test_the_door_path_reruns_a_middle_task_end_to_end`, in this order:
   1. Keep B's and C's attempt-1 `run_id` and `worktree_commit`, A's too, and a map of the sha256
      of every file under `data_paths.run_dir(<B's run id>, <data dir>)` by relative path.
   2. Set `REMEDY_DATA_DIR` with `monkeypatch.setenv`. Plant one marker file in
      `_task_stream_dir(<job>, <B>)` of `pingpong_job.py`, with a comment saying why: `run_job`
      writes stream evidence only when asked to, and `test_subtree_rerun_prepare.py` plants the
      same kind of marker to prove the move.
   3. Set `REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD` to "0.000001" with `monkeypatch.setenv`, with a
      comment: `resolve_confirm_above_usd` ignores a threshold that is not above zero. Start the
      server. POST `job.rerun-subtree` with `task_id` B and a model M: 200, `outcome`
      `needs_confirmation`, `subtree` equal to `[B, C]`, and the job still `completed` on disk.
   4. POST again with `confirm_cost: true`: 200, `outcome` `prepared`, `root_task_id` B, `subtree`
      `[B, C]`, `exact` true, `pre_task_tree_equal` true, `model` equal to `{"override": M,
      "configured": "", "reason": "human_override"}`, and `run_command` equal to
      `f"remedy job run {job_id}"`.
   5. THE TREE-HASH PROOF, with git on the fixture repository itself: `base_commit` equals
      `git rev-parse <B's attempt-1 commit>^`; `git rev-parse <reset_commit>^{tree}` equals
      `git rev-parse <base_commit>^{tree}`; and `git merge-base --is-ancestor <B's attempt-1
      commit> <the job branch>` exits 0, the branch read from the job record.
   6. The job record: `paused`; one `reruns` entry carrying the same `base_commit` and
      `reset_commit`, `exact` and `pre_task_tree_equal` true, and a `proof` whose `paths_equal`
      and `tree_equals_base` are true; B and C `pending` on `attempt` 2 with one `attempts` record
      each and `model_override` M; B's record carries its attempt-1 `worktree_commit` and `run_id`
      and `stream_evidence` `rerun_attempts/<B>/attempt-1`; A still on `attempt` 1 with no
      `attempts` and its own commit and run id.
   7. The marker now reads the same under `job_evidence_dir(<job>, <data dir>) /
      "rerun_attempts" / <B> / "attempt-1"`, and the old stream directory is gone.
   8. Exactly one `subtree_rerun_prepared` event in the job's run-log files, naming B, whose
      `metadata` has `exact` true and `model_override` M; the dashboard's items for B and C read
      `attempt` 2 with one `attempts` entry and A's reads 1; `events-since` holds exactly one
      `subtree_rerun_prepared` frame.
   9. Run 2, `job run <id> --tasks 0`: exit 0, the job `completed`; A unchanged; B and C
      `applied_to_job_workspace` on `attempt` 2 with one `attempts` record, a NEW `run_id` and a
      NEW `worktree_commit`, and `model_override` M.
   10. THE RUN RECORDS, through `pingpong_loop.load_run`: B's and C's new runs read
      `provider_evidence.builder_configured_model` equal to M; B's attempt-1 run reads it NOT equal
      to M, and the sha256 map of step 1 is unchanged.
   11. THE REPORT, through `job show <id> --full --json` as the model's `_report_markdown` reads it,
      each task line keyed by the first eight characters of its task id: B's and C's lines end with
      `f" — attempt 2, run on {M}"`, and A's line holds no ` — attempt`.
   TEST (b) `test_the_command_line_path_reruns_with_yes`: a second repository and data directory,
   run 1 as above, then in the test's own process, with `REMEDY_DATA_DIR` set by `monkeypatch`,
   `apps.cli.grouped.main(["job", "rerun-subtree", <job>, "B", "--model", M2, "--yes", "--json"])`
   — a `SystemExit` fails the test — whose stdout holds exactly one non-empty line, a JSON envelope
   with `ok` true, `subtree` `[B, C]`, `model.override` M2 and `run_command` as in step 4; the job is
   `paused`; run 2 exits 0 with the job `completed`, B and C on `attempt` 2 with one `attempts`
   record, a new `run_id` and `model_override` M2, and their report lines end with
   `f" — attempt 2, run on {M2}"`.
   M and M2 are two different module constants that `_MODEL_OVERRIDE_RE` accepts. Nothing in S2
   touches a production file.

BUNDLE — the commits are C1 to C6, in this order.
C1 — `.agent/authored/f029-r7-block.md` := this block, `.agent/authored/f029-r7-booking.diff` and
  `.agent/authored/f029-r7-plan.md` := the payloads, by `shutil.copyfile`.
  Subject: `F029 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 54. Report the number you measure.
C2 — `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F029 R7 C2: book round 6 and its prose slip`
  Expected by `git show --numstat`: 2/0 live_review.md, 12/10 plan.md, 1/0 prose_slips.md.
C3 — S1. Subject: `F029 R7 C3: give the run detail's confirmation row its space`
C4 — S2. Subject: `F029 R7 C4: prove a subtree rerun end to end`
C5 — `.agent/authored/f029-r7-mutations.py` (G5). Subject: `F029 R7 C5: add the round 7 mutation tool`
C6 — `.agent/handoff.md` per `docs/agents/handback_template.md`. Subject: `F029 R7 C6: rewrite handoff for round 7`
  Then `git push origin feature/f029-subtree-rerun` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C4 before you commit
   it; if it would reach 500, it becomes C4a (the helpers and test (a)) and C4b (test (b)), each
   leaving the new file's collected tests passing, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f029-r7-*` copies and tool,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`, the two files S1 names, the
   file S2 names, and `.agent/handoff.md`. Report `git diff --name-only cfd779c6` after C6. Touch
   nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test THIS round wrote that is wrong may be corrected
   before C6, and the correction is declared. An existing test that goes red is reported, and you
   stop. A production defect the new test exposes is reported with its evidence, never fixed.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F029 one full-suite run, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table; then
 each `.agent/authored/f029-r7-*` copy read back with `git show <C1>:<path>` compared byte for byte
 with its source (the block copy against `.remedy-wt/f029-r7/block.md`). One reading per copy.
G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 329576 | 7b9e2a2b0a6b5103ad1eafebdf98808ad2f0e2ccf813a9e36ee245ab5ffa230b |
 | .agent/plan.md | 1369 | 09426a6990397d3192aa3edfa8579d9394ff22dda437a8d26c29dc04886b58b9 |
 | .agent/prose_slips.md | 374248 | 16e2ef58281e8cfd5b1d5de8dac99d824a9ad8781d778928d184b6240c67853e |
 Also `open_finding_ids` over the ledger's text at `cfd779c6` and at C2 (the reviewer read `[]` at
 both), and `git diff --name-only <C1> <C2>`, which must name exactly the paths of the table.
G3 THE CODE — `python3 -m ruff check tests/ui_server/test_subtree_rerun_e2e_live.py` at C5 with its
 real exit code; then quote from the diff the whole S1 change (both files) and S2's steps 4, 5 and
 10 as written.
G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_subtree_rerun_e2e_live.py tests/ui_contracts tests/orchestration/test_run_report.py tests/ui_server/test_rerun_subtree_door.py tests/ui_server/test_dashboard_task_attempts.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -16; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection without its first path, serially in the primary checkout at
 `cfd779c6`, and read `1696 passed, 11 skipped` at real exit code 0; the eleven skips are F252
 quarantines. Report every `SKIPPED` line and account for any difference from 1696 beyond the
 nodes the new file adds. Then `python3 -m apps.cli.main integrity check --json`: every check's
 status and `fail_count`.
G5 THE RED PROOFS — your tool `.agent/authored/f029-r7-mutations.py` takes a worktree path. It runs
 `python3 -B -m pytest -q -p no:cacheprovider tests/ui_server/test_subtree_rerun_e2e_live.py` with
 the worktree as working directory and an environment of the tool's own plus `PYTHONPATH` = the
 worktree and `PYTHONDONTWRITEBYTECODE` = "1", after purging every `__pycache__` directory under
 the worktree. It first prints, under that same environment, `__file__` of
 `packages.orchestration.subtree_rerun` and of `packages.orchestration.pingpong_job`, both of which
 must lie inside the worktree. Each mutation replaces ONE whole line of the named file INSIDE the
 worktree, its FROM asserted to occur exactly once, and is restored. Unmutated controls run first
 and last. It prints one line per mutation (label, exit code, failed count, the failing tests'
 names) and ends with `restored byte-identical: True` per file, the PRIMARY checkout's `git status
 --porcelain` (which must be empty) and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `packages/orchestration/pingpong_job.py`: the line holding
     `builder_model=(task.model_override or builder_model),` becomes the same indentation with
     `builder_model=builder_model,` — a run ignores the override;
  m2 `packages/orchestration/ui_server.py`: the line holding `"attempt": int(t.attempt),` becomes
     `"attempt": 1,` — the dashboard forgets the attempt;
  m3 `packages/orchestration/run_report.py`: the line holding `if task.attempt < 2:` becomes
     `if task.attempt < 3:` — the report drops the clause for a second attempt;
  m4 `packages/orchestration/subtree_rerun.py`: the line holding `task.attempt += 1` becomes
     `task.attempt += 0` — the fold does not count the attempt.
 Run it: `git worktree add --detach .remedy-wt/f029-r7-mut <C5>`, then
 `python3 -B .agent/authored/f029-r7-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f029-r7-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, then you strengthen the test that should catch it before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f029-r7-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.
G6 TREE AND PUSH — after C6: `git status --porcelain`, empty; `git log --oneline -n 7`;
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected, every gate's real output and exit code, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per S-item), the deviations, and the next expected action. Your Session section reads SESSION 2
of feature F029, round 7, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 7 with the reviewer's headless render of the confirmation row, then the closure sequence.
State the open-findings count, 0, and the operator-questions count, 0.
