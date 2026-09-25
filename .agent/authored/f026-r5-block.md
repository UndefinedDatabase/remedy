STEP F026 R5 — THE CLOSURE SEQUENCE'S FIRST HALF: book round 4, repair R-1061 and R-1062, write the Built State, consolidate the checklist, run the self-use item and the one full suite

GOAL
Book round 4's PASS and R-1060's resolution, register R-1061 and R-1062 and repair both, append the
Built State to `docs/roadmap/features/T5_F026.md`, run the checklist consolidation pass (it joins
nothing and keeps `docs/agents/planner_reviewer_prompt.md` §3 at 34 items), generate the closure's
self-use item and run it to its approval gate (closure precondition 6), and run this feature's ONE
full suite on the tree that ships, committing its transcript. The evidence bundle, the review
package, the ledger rotation, the STATUS line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue a
verdict, never merge, and never write a `Done:` line: when a repair lands you append ONE line to
`.agent/live_review.md`, `Landed: R-<id> — <one line: what changed, which commit>`. Read first:
`docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3, 6 and 7, `docs/agents/integration_gate.md`,
and `.agent/authored/f025-r9-block.md`'s C4 and C5, which this round's C5 and C6 follow.

THE DIRECTORIES
  `.remedy-wt/f026-r5-payloads/` and `.remedy-wt/f026-r5/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f026-r5-sim/`, `.remedy-wt/f026-r5-drafts/`, `.remedy-wt/f026-r4-dry/`,
  `.remedy-wt/f026-r4-render*/`   The reviewer's; do not touch them.
  `.remedy-wt/f026-r5-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners chained
with `;` or `&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
read `${PIPESTATUS[0]}` when you pipe. Use `git -C <path>`; never `cd` into a worktree. Write any
script holding a dollar-brace or a brace-quote shape to a file under your own directory and run it.
The ONE npm command this round may run is C6's `npm --prefix apps/ui run build`; never `npm install`,
`npm ci` or `npx`. Never `git stash`, never `pkill -f`, never `git worktree prune`.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f026-task-edit-runtime`, `git log --oneline -1` `83c1d0c1`.
3. Measure this block's line count and sha256 (`.remedy-wt/f026-r5/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*'` as found.

PAYLOADS — under `.remedy-wt/f026-r5-payloads/`; verify each one's line count, byte count and sha256
BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| closure_docs.diff | 101 | 7565 | 105c3451d640a6ff15a945218ac6d1e4400d26576f5219d5146e9b78bf83a820 |
| plan.md | 33 | 1231 | 79f48823b6306c769fe19f8ac0713fb3f807c97329b687a849cba8acbc13054a |
| records.diff | 25 | 9514 | 2adb3a46946e517b69edec2677bb3386393a23a8cfe1333bd442db5feb6c9d57 |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `83c1d0c1`)
appends to `.agent/live_review.md` round 4's gate entry, R-1060's `Done:` paragraph and the
registrations of R-1061 and R-1062, and one line to `.agent/prose_slips.md`. `closure_docs.diff`,
generated in the same tree AFTER those records, appends the Built State to
`docs/roadmap/features/T5_F026.md` and replaces, in `docs/agents/planner_reviewer_prompt.md`, the line
`  The next consolidation measures against 34.` with the consolidation paragraph that ends with it
(containment test: TO contains FROM: true — an APPEND; the line occurs once before and once after).

THE SPECIFICATION OF THE TWO REPAIRS
S1 R-1061. In `apps/ui/src/api/taskEditSend.ts`, `describeTaskEditResult(result, jobId = "")` names
   the job's real id in the relaunch sentence for a task edited in the `failed` state — "Relaunch the
   job to run it: remedy job run " followed by the id and a full stop — and, when `jobId` is empty,
   "Relaunch the job to run it." with no command; `sendTaskEdit` passes its target's `jobId`. No
   angle-bracket placeholder remains in the file. `apps/ui/src/api/taskEditSend.test.ts` pins both
   sentences and the flow passing the id.
S2 R-1062. In `edit_task_at_runtime` in `packages/orchestration/task_edit_runtime.py`, the log entry's
   `runtime` object gains `dod_resync_pending`: true when the edit changed the plan task's
   `acceptance` AND the job has a stored DoD — the file named `DOD_FILENAME` of
   `packages/orchestration/dod_gate.py` under `data_paths.job_evidence_dir(job_id, root)` —, false
   otherwise, with a comment naming R-1062 and T5_F026.md's edge case. In
   `tests/orchestration/test_task_edit_runtime.py`, `test_runtime_object_carries_every_key` pins the
   runtime key set EXACTLY and must gain the new key, and new tests pin the three cases: a stored DoD
   and an acceptance edit read true; a stored DoD and a title-only edit read false; no stored DoD and
   an acceptance edit read false.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f026-r5-block.md` := this block and each payload as
   `.agent/authored/f026-r5-<name>`, by `shutil.copyfile`. Subject `F026 R5 C1: copy round 5 block and
   payloads`. Its insertions are this block's line count plus 159.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject
   `F026 R5 C2: book round 4, resolve R-1060, register R-1061 and R-1062`. Expected by
   `git show --numstat`: 8/0 .agent/live_review.md, 13/11 .agent/plan.md, 1/0 .agent/prose_slips.md.
C3 THE REPAIRS: S1 and S2 with their tests and one `Landed:` line each. Subject
   `F026 R5 C3: name the job in the relaunch sentence and note a pending DoD re-sync (R-1061, R-1062)`.
C4 THE BUILT STATE AND THE CONSOLIDATION: `git apply` closure_docs.diff. Subject
   `F026 R5 C4: write the Built State and consolidate the checklist`. Expected: 5/0 docs/agents/planner_reviewer_prompt.md, 77/0 docs/roadmap/features/T5_F026.md.
C5 THE SELF-USE ITEM (closure precondition 6), from a scratch Python file of yours run in the primary
   checkout: (a) `packages.orchestration.self_use_generator.generate_and_append_if_empty()` FIRST, with
   no arguments — the reviewer's dry run in a tree carrying C2's records appended `SU-031`, "Address
   ledger finding R-1057", provenance `generated (self-use-generator tier 1, ledger scan, R-1057)`;
   report what yours does and `next_self_use_item()`'s answer after it. (b) RUN it with
   `packages.orchestration.self_use_runner.run_next_self_use_item`, with `dest_dir` =
   `/home/decodeux/Repos/remedy/.remedy-wt/f026-r5-selfuse` and nothing else, so `max_tasks` stays 1
   and both roles resolve from the `self_use` role configuration; it runs to the approval gate and is
   NEVER applied; a blocked or stopped job is an outcome to record, not a reason to stop. (c) Save
   under `.agent/selfuse_f026/`, mirroring `.agent/selfuse_f025/`'s file names: the item markdown as
   `<id>.md`, `entry_and_job_file.txt`, `execution_config.txt`, `result_state.txt`, `timing.txt`,
   `full_transcript.txt`, and `run_defects.txt` holding every string
   `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the run's own
   `JobPlan`, verbatim, or the literal `NONE`. (d) Then `python3 -m pytest tests/docs/ -q -p
   no:cacheprovider`; red is a STOP. Paths: `scripts/self_use_queue.json` and `.agent/selfuse_f026/**`.
   You register no finding; the reviewer authors every registration from `run_defects.txt`. Subject
   `F026 R5 C5: generate and run the closure's self-use item, record its defects`.
C6 THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C5: (a) `bash -c 'npm
   --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — a failing build is
   a STOP — then `git status --porcelain`, still empty. (b) `python3 -m pytest -n auto -q`, its log at
   `/home/decodeux/remedy-gate-scratch/f026-full-suite.txt`, or under `.remedy-wt/f026-r5-worker/` if
   the sandbox refuses that path, said so; measure its wall time. Write
   `.agent/authored/f026-closure-suite.txt` holding the command, the real exit code, the wall time,
   the summary line and the FULL list of bad node ids (failed plus errors), or the literal `NONE`.
   (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER with
   the transcript. Subject `F026 R5 C6: record the closure suite transcript and rewrite handoff for
   round 5`. Then `git push origin feature/f026-task-edit-runtime`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; `git apply --check` before each `git apply`, exit codes reported.
2. Every commit under 500 insertions by `git show --numstat`; C5's queue and record files included.
3. The round's tracked path set: the `.agent/authored/f026-r5-*` copies,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `apps/ui/src/api/taskEditSend.ts`, `apps/ui/src/api/taskEditSend.test.ts`,
   `packages/orchestration/task_edit_runtime.py`, `tests/orchestration/test_task_edit_runtime.py`,
   `docs/roadmap/features/T5_F026.md`, `docs/agents/planner_reviewer_prompt.md`,
   `scripts/self_use_queue.json`, `.agent/selfuse_f026/**`, `.agent/authored/f026-closure-suite.txt`
   and `.agent/handoff.md`. No edit to `README.md`, `docs/roadmap/STATUS.md`, any `consumed_by`,
   `.agent/decisions.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. A RED full suite in C6 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test or mark anything xfail.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip.
6. The self-use run may leave `remedy/job-*` branches, worktrees or evidence directories behind.
   Report them; delete nothing you did not create as scratch; leave every existing worktree alone.
7. The full suite runs ONCE, in C6, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run before
C6 is written; G6 is C6's suite.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f026-r5-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE RECORDS: `git show <C2>:<path>` and, for the two docs, `git show <C4>:<path>` of each file
   below hashes to the reviewer's simulation (which applied C2's records and then C4's docs, with
   no C3 in between, and C3 touches none of these paths):
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 332093 | 2c346f8b13df89d270edb7cbd7fefccbd2133448f878b671c9b4898785c5c5e4 |
   | C2 | .agent/prose_slips.md | 368264 | de8f696d0fc35480f5f243b33c26690ba5adc2d536bbc7a2ca033d50992e2402 |
   | C2 | .agent/plan.md | 1231 | 79f48823b6306c769fe19f8ac0713fb3f807c97329b687a849cba8acbc13054a |
   | C4 | docs/roadmap/features/T5_F026.md | 10342 | ff218bb577e4066a4aa2e45806896e3aaa78a1f109dcd137bde472cde291439c |
   | C4 | docs/agents/planner_reviewer_prompt.md | 103167 | c104c2cd5291d169c0869c34f6d7337937c36b7ea13b543eebd54717af8ab523 |
   `open_finding_ids` over the ledger reads R-1008, R-1055, R-1057, R-1058, R-1061 and R-1062 at C2;
   the ledger's last two lines at C3 begin `Landed: R-1061 — ` and `Landed: R-1062 — `, in either
   order; and `live_checklist_items` of `packages/orchestration/block_lint.py` over the planner prompt
   reads the same 34 numbers at `83c1d0c1` and at C4.
G3 THE CODE AND THE LINTER: `python3 -m ruff check packages/orchestration/task_edit_runtime.py
   tests/orchestration/test_task_edit_runtime.py` at C3, and `python3 -m apps.cli.main integrity block
   .remedy-wt/f026-r5/block.md` at C4, real exit code 0, whole output.
G4 THE RED PROOFS, at C3, by a tool of yours saved as `.agent/authored/f026-r5-mutations.py` and
   committed IN C3, run in `git worktree add --detach .remedy-wt/f026-r5-mut <C3>` and removed after
   with `git worktree remove --force`: m1 the relaunch sentence goes back to the literal
   `<job id>` (taskEditSend.ts, vitest by the route `.agent/authored/f026-r4-mutations.py` uses);
   m2 `dod_resync_pending` is always false; m3 `dod_resync_pending` is true without a stored DoD
   (task_edit_runtime.py, pytest over the worktree's `tests/orchestration/test_task_edit_runtime.py`
   under `python3 -B` after purging `__pycache__`). Controls first and last; every mutation red; the
   last line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`; its whole output reported.
G5 THE TESTS AND THE TREE, in the primary checkout at C5, serially:
   `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_block_lint.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
   tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py
   tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_test_runner.py
   tests/cli/test_golden_path.py` — exit 0, the vitest node passing, summary line reported; C5's
   readings verbatim, with the self-use job's id, its builder and reviewer names and models — the
   `self_use` role's configured provider, never `fake` — its state, and `run_defects.txt`; then
   `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count` 0; and `git status
   --porcelain` empty with no untracked file (closure precondition 3).
G6 THE INTEGRATION GATE: the UI build's last line and real exit code, `git status --porcelain`
   after it, then the full suite's real exit code, wall time, summary line and every bad node id, all
   in `.agent/authored/f026-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a bad
   node (closure precondition 7).
G7 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip equal
   to `origin/feature/f026-task-edit-runtime`, `git log --oneline -n 8`, `git worktree list`,
   `git branch --list 'remedy/job-*'`, the push's real outcome, and `gh pr list --state open --json
   number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the self-use readings, the full suite's summary line and bad node
ids, the authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate
and per S-item), the deviations, and the next action. Session section: SESSION 1 of feature F026,
round 5, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of
round 5, then the closure's second half — the booking of round 5, the registrations the self-use
defects ask for, any repair the suite requires, the evidence bundle and the review package — and then
the closing round. State the open-findings count as the script reads it at C3, and "Operator
questions open: <the count of `### Q` headings in the file at C2>".
