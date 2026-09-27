STEP F029 R1 — CLAIM F029 AND LAND T001: the subtree of a task, the walk of the job branch since its commit, the refusals, and the reset as one new commit with its hash proof

GOAL
Pull request 287 is merged; `main` is at `b2863af4` and F029 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F028's round 12 verdict, record DECISION
F029 D1, and land T001: a new module `packages/orchestration/subtree_rerun.py` that computes a
task's subtree, walks the job branch from that task's commit, refuses every unsafe case, and
resets the subtree's files to their state before the task as ONE new commit whose trees prove
it — plus its tests. Nothing in this round changes a task's status or writes `job.json`; that is
T002.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records and the
STATUS line travel as payloads. Read DECISION F029 D1 in the claim diff before you write code: it
is the design this specification implements. Read `packages/orchestration/worktrees.py` from
`_git` through `restore_tree` and `mode_at`, `_commit_applied_task` and
`build_task_commit_message` in `packages/orchestration/pingpong_job.py`, `build_graph` in
`packages/orchestration/dag_schedule.py`, `worktree_drift_message` in
`packages/orchestration/checkpoints.py`, and the fixtures at the top of
`tests/orchestration/test_worktrees.py` before you write anything.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f029-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f029-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f029-r1-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f029-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f029-r1-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `b2863af4`. Report all three. Then
   `git checkout -b feature/f029-subtree-rerun` and report the branch. Do NOT pull: the Open PR
   Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f029-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f029-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 158 | 18109 | 5acca117cdc46dc66d71001b86e1cd9854334748b1156017f710326092beb13d |
| context.md | 37 | 1569 | c2ded9d16a6c91668c61b96cc6e5609be767d782263e183609fde54cbeb52c1b |
| plan.md | 33 | 1208 | 259ad21a932f844e517a04f86d95ef04da23ebe2f349a1c1748a1290f193080d |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`b2863af4` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F028's round 12 gate entry
appended), `docs/roadmap/STATUS.md` (F029's line `[ ]` to `[~]`) and `.agent/decisions.md`
(DECISION F029 D1 appended).

THE SPECIFICATION — all in the new module `packages/orchestration/subtree_rerun.py`, whose
docstring names F029 T001 and DECISION F029 D1 and says in two sentences that a task's commit on
the job branch is its address and that a reset is a new commit, never a rewrite. No
`except Exception` anywhere in it. Every subprocess call carries
`timeout=worktrees.GIT_QUERY_TIMEOUT_SEC`; plain git queries go through `worktrees._git`. The
module never writes `job.json`, never changes a task's status and takes no lock.
S1 CONSTANTS. `RERUN_TRAILER = "Remedy-Rerun"`, `RERUN_FILES_NAMED = 5`, and two exceptions:
   `SubtreeRerunRefused(Exception)` carrying `code`, `detail` and `facts` (a dict, empty by
   default), and `SubtreeRerunError(RuntimeError)` for a reset whose proof fails.
S2 THE SUBTREE. `rerun_subtree_ids(tasks, root_task_id) -> list[str]` answers the root and every
   task that depends on it directly or transitively by `dag_schedule.build_graph`, WHATEVER its
   status, in plan order. A root that is not a task id raises `SubtreeRerunRefused("unknown_task",
   ...)` with the detail `f"there is no task {root_task_id!r} in this job; its tasks are:
   {listing}"`, `listing` joining the first ten ids with `", "` and, when there are more, adding
   `f" and {n} more"`.
S3 THE WALK. `branch_commits_since(worktree_path, base) -> list[dict]` answers, oldest first, one
   dict per commit of `git rev-list --reverse --first-parent {base}..HEAD`:
   `{"sha", "task_id", "rerun_of", "paths"}` — `task_id` the value of its `Remedy-Task` trailer
   and `rerun_of` that of its `Remedy-Rerun` trailer, each "" when absent, read with
   `git log -1 --format=%(trailers:only,unfold) <sha>` as `read_head_remedy_trailers` reads them;
   `paths` the sorted paths of `git diff --name-only --no-renames -z <sha>^ <sha>`.
S4 THE PLAN. `plan_subtree_reset(job, root_task_id, worktree_path) -> dict`, read-only, raises
   `SubtreeRerunRefused` from the first of, in this order:
   a. S2's `unknown_task`;
   b. `job.isolation_mode != "worktree"` — `not_worktree_mode`, detail `"the job ran in a copy of
      the repository, not on a job branch, so no task has a commit to go back to"`;
   c. the root's `worktree_commit` is "" — `task_not_committed`, detail
      `f"task {root} has no commit on the job branch yet, so there is nothing to rerun"`;
   d. `worktrees.head_at(worktree_path)` differs from `job.worktree_head`, an answer of "" counting
      as different — `worktree_drift`, detail EXACTLY
      `checkpoints.worktree_drift_message(job.worktree_head, live or "unknown")`;
   e. `worktrees.worktree_matches_head(worktree_path)` is False — `worktree_dirty`, detail
      `f"the job worktree holds uncommitted changes to {listing}; commit or discard them before a
      rerun"`, `listing` built as in S2 from the paths `git status --porcelain=v1 -z
      --untracked-files=all` names (a rename entry's second path skipped);
   f. the root's commit is not an ancestor of `HEAD` by `worktrees.is_ancestor` —
      `commit_not_on_branch`, detail naming the task and the first twelve characters of its sha;
   g. with `base` = `git rev-parse <root commit>^` and `commits` = S3 over `base`, a task of the
      subtree whose `worktree_commit` is not "" and is not the sha of one of `commits` —
      `subtree_order`, detail `f"task {tid} depends on {root} but its commit {sha[:12]} is not
      after {root}'s on the job branch; rerun from an earlier task"`, the first such task in plan
      order;
   h. INTERLEAVING. A commit is IN the subtree when its `task_id` is a subtree id, and OUTSIDE it
      otherwise, named by its `task_id`, or `f"commit {sha[:12]}"` when that is "". The subtree
      paths are the union of the IN commits' `paths`. Every OUTSIDE commit whose `paths` meet the
      subtree paths gives `{"by": name, "paths": sorted shared paths}`, in branch order; when any
      exists — `interleaved`, detail `f"rerunning {root} would also undo work outside its subtree:
      {parts}; start the rerun at an earlier task whose subtree includes that work"`, `parts`
      joining `f"{by} changed {', '.join(paths)}"` with `"; "`, and `facts` =
      `{"interleaving": [those dicts]}`.
   Otherwise it builds the TARGET TREE in a private index exactly as `worktrees.write_tree_at`
   manages its temporary `GIT_INDEX_FILE`: `git read-tree HEAD`, then for each subtree path in
   sorted order the entry `git ls-tree -z <base> -- <path>` gives, applied with
   `git update-index --add --replace --cacheinfo <mode>,<sha>,<path>`, or, when `base` has no
   entry, `git update-index --force-remove -- <path>`; then `git write-tree`. It answers a
   JSON-serialisable dict: `job_id`, `root_task_id`, `subtree` (S2's list), `base_commit`,
   `head_commit` (the live head), `commits` (S3's dicts, each plus `"in_subtree": bool`), `paths`
   (the sorted subtree paths), `target_tree`, `base_tree` (`git rev-parse <base>^{tree}`),
   `exact` (True when no OUTSIDE commit is in `commits`), and `root_start_tree` (the root task's
   `task_start_tree`, "" when none). When `exact` is True and `target_tree` differs from
   `base_tree` it raises `SubtreeRerunError` naming both.
S5 THE MESSAGE. `build_rerun_commit_message(job, plan) -> str`, with `n = len(plan["subtree"]) -
   1`, answers `f"rerun: reset task {root} and {n} dependent task{'' if n == 1 else 's'}\n\n"`, then
   `f"Remedy reset task {root} of job {job_id} and the tasks depending on it to their state before
   commit {base[:12]}, {changed}.\n\n"`, `changed` being `"changing no file"` when `paths` is empty
   and otherwise `"changing "` plus the first `RERUN_FILES_NAMED` paths joined with `", "`, plus
   `", ..."` when there are more; then `f"{REMEDY_JOB_TRAILER}: {job_id}\n"` and
   `f"{RERUN_TRAILER}: {root}\n"`, the job trailer key imported from `worktrees`.
S6 THE RESET. `apply_subtree_reset(job, root_task_id, worktree_path) -> dict` runs S4, brings the
   worktree to `target_tree` with `worktrees.restore_tree` over a `WorktreeHandle` built from the
   job id, `job.repo_path`, the worktree path and its current branch, and commits with
   `worktrees.commit_job_worktree(worktree_path, build_rerun_commit_message(job, plan))`. THE
   PROOF, after the commit: the new commit's tree equals `target_tree`; for every path of
   `paths` the `git ls-tree` entry (mode and object) at the new commit equals the one at `base`,
   both absent counting as equal; and when `exact`, the new commit's tree equals `base_tree`. A
   failure raises `SubtreeRerunError` naming the check and the path; the commit stays, nothing is
   rewritten. It answers S4's dict plus `reset_commit`, `reset_tree`, `restored` (what
   `restore_tree` returned), `proof` = `{"paths_checked": len(paths), "paths_equal": True,
   "tree_equals_base": exact}`, and `pre_task_tree_equal`: None unless `exact` and
   `root_start_tree` is not "", else whether `reset_tree == root_start_tree`. It does not touch
   `job`; T002's caller records the new head.

THE TESTS — NEW FILE `tests/orchestration/test_subtree_rerun.py`. Each test builds a real git
repository under `tmp_path` whose checked-out branch is `remedy/job-<id>`, makes its base commit
with a fixed identity passed by `-c user.name=... -c user.email=...`, lands every task commit
through `worktrees.commit_job_worktree` with a message ending in the `Remedy-Job` and
`Remedy-Task` trailers, and builds a `JobPlan` with `isolation_mode="worktree"`, its
`worktree_head` the branch tip and `TaskEntry` objects whose `inputs["plan"]` carries
`planned_id` and `depends_on` and whose `worktree_commit` is the task's commit. At least:
S2 over a diamond (T1; T2 and T3 on T1; T4 on T2 and T3) plus an independent T5, the subtree of
T2 being `["T2", "T4"]` and of T1 `["T1", "T2", "T3", "T4"]` with completed statuses included,
tasks without plan inputs chaining to their predecessor, and `unknown_task` over eleven tasks
naming `and 1 more`; the EXACT reset: T1 writes `a.py`, T2 on T1 edits `a.py` and adds
`b.py`, T3 on T2 edits `b.py`, adds `c.py` and deletes a file the base had; the rerun of T2
leaves the branch tip's tree equal to the tree of T1's commit, `c.py` gone, the deleted file
back, an executable bit T2 set cleared, `exact` True, `pre_task_tree_equal` True with the
root's `task_start_tree` set to that tree and None with it "", the reset commit's trailers
`Remedy-Job` and `Remedy-Rerun` read back, and T2's and T3's commits still ancestors of the new
tip; COMPLETED-ELSEWHERE: T4, depending on nothing, applied after T3 and changing only `d.py`,
keeps `d.py` while `a.py`, `b.py` and `c.py` go back, `exact` False and `pre_task_tree_equal`
None; INTERLEAVING: that T4 changing `a.py` instead refuses `interleaved` with `facts` exactly
`{"interleaving": [{"by": "T4", "paths": ["a.py"]}]}`, and a commit with no task trailer changing
`b.py` is named `commit <first twelve>`; every refusal leaves the tip, the tree and
`git status --porcelain` exactly as they were; `worktree_drift` whose detail equals
`worktree_drift_message(...)` exactly, `worktree_drift` for a worktree path that does not
exist, its detail naming `unknown`, `worktree_dirty` naming an untracked file,
`not_worktree_mode`, `task_not_committed`, `commit_not_on_branch` for a commit on another
branch, and `subtree_order` for a dependent whose commit precedes the root's; a SECOND rerun of
T2 after a new T2 commit lands on top of the first reset, with T3's `worktree_commit` cleared as
T002 will clear it, which again restores T1's tree; and
`build_rerun_commit_message` for one and for three dependents and more than five paths.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f029-r1-block.md` := this block, and `.agent/authored/f029-r1-plan.md` and
  `.agent/authored/f029-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F029 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 70. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f029-r1-claim.diff` := claim.diff.
  Subject: `F029 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 158.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F029 R1 C2: claim F029, re-head the live review record, book F028 R12, record D1`
  Expected by `git show --numstat` (insertions and deletions): 15/13 context.md, 74/0
  decisions.md, 24/21 live_review.md, 19/11 plan.md, 1/1 STATUS.md.

C3 — THE CODE: `packages/orchestration/subtree_rerun.py`, and in the same commit one entry in
  `ALLOWED_UNWIRED` of `tests/test_no_orphan_modules.py`, in its alphabetical place,
  `("packages/orchestration/subtree_rerun.py", "F029 T001's subtree reset; T002's rerun command wires it (DECISION F029 D1)")`,
  because the module has no importer until T002 and the orphan guard would otherwise go red.
  Subject: `F029 R1 C3: reset a task's subtree to its state before the task as one proved commit`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_subtree_rerun.py` and your mutation tool
  (G5) saved as `.agent/authored/f029-r1-mutations.py`.
  Subject: `F029 R1 C4: test the subtree reset and add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F029 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f029-subtree-rerun`. Do NOT create a pull request: the
  branch opens one at F029's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so. The
   `ALLOWED_UNWIRED` line lands in the SAME part as the module's first lines.
3. The round's whole tracked path set is: the `.agent/authored/f029-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/subtree_rerun.py`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/test_subtree_rerun.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only b2863af4` at the
   branch tip after C5. Do NOT touch `packages/orchestration/worktrees.py`,
   `packages/orchestration/pingpong_job.py`, `packages/orchestration/checkpoints.py`,
   `packages/orchestration/dag_schedule.py`, anything under `apps/`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md` or
   `docs/roadmap/features/T5_F029.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F029's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f029-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f029-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | docs/roadmap/STATUS.md | 55186 | 0b9fe9b1dd2eb6732d82cddaf83e483b8894ffd497576ba46de23b1246216775 |
 | .agent/live_review.md | 307852 | c63283daaf27049e3f19da677c9f6f6ef3ef5d7aaa58d2e2619fc890a09bfab3 |
 | .agent/decisions.md | 2281119 | 2a107b591a6e9d10d0a259de0380b09fd7f96441ed93ba6c770cca5a8af65157 |
 | .agent/plan.md | 1208 | 259ad21a932f844e517a04f86d95ef04da23ebe2f349a1c1748a1290f193080d |
 | .agent/context.md | 1569 | c2ded9d16a6c91668c61b96cc6e5609be767d782263e183609fde54cbeb52c1b |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `b2863af4` and at C2 (the reviewer read
 it empty at both); at C2 the ledger has exactly one line reading `## Findings` and exactly one
 reading `## Steps`, and its last line begins `Gate: F028 R12 — `; F029's STATUS line at C2 read
 back in full, which must read `- [~] F029 — Subtree rerun`; and `git diff --name-only <C1b> <C2>`,
 which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/subtree_rerun.py
 tests/orchestration/test_subtree_rerun.py tests/test_no_orphan_modules.py` at C4, with its real
 exit code. Then report, quoted from `git show <C3>`, the whole of the refusal ladder of
 `plan_subtree_reset` (steps a to h) and the proof block of `apply_subtree_reset`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_subtree_rerun.py tests/orchestration/test_worktrees.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_checkpoints.py tests/orchestration/test_task_veto.py tests/test_subprocess_timeouts.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less `tests/orchestration/test_subtree_rerun.py`, serially, in
 the primary checkout at `b2863af4` before any change, and read `926 passed, 7 skipped` at real
 exit code 0. The seven skips are the F252 quarantines in `tests/regression/test_named_bugs.py`
 and `tests/test_agent_tooling.py` and stay skipped. Report every `SKIPPED` line the `-rs`
 summary prints, the node count of `tests/orchestration/test_subtree_rerun.py` by
 `--collect-only -q`, and account for any difference from 926 plus that count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f029-r1-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/subtree_rerun.py` INSIDE that worktree
 (asserting its FROM text occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_subtree_rerun.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and
 last and ends with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations, each a real behaviour change:
  m1 S2 answers the direct dependents only, with no transitive walk;
  m2 S2 leaves the root out of the subtree;
  m3 step d reads an unreadable live head ("") as matching;
  m4 step e is skipped;
  m5 a commit carrying no `Remedy-Task` trailer is classed IN the subtree;
  m6 step h is skipped;
  m7 a path `base` has no entry for is left in the target tree instead of removed;
  m8 `base` is the root's commit itself instead of its first parent;
  m9 S6 restores the worktree but makes no commit;
  m10 step g is skipped;
  m11 `exact` is always True;
  m12 S5 leaves out the `Remedy-Rerun` trailer.
 Run it: `git worktree add --detach .remedy-wt/f029-r1-mut <C4>`, then
 `python3 -B .agent/authored/f029-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f029-r1-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f029-r1-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `b2863af4` in that order
 (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal your
 step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F029, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — the rerun command behind the cost preview, the attempt counter and the
subtree's tasks returned to pending, earlier attempts' evidence linked, and the model override
recorded. State the open-findings count, 0, and the operator-questions count, 0.
