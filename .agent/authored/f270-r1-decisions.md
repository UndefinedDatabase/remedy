
## DECISION F270 D1 (2026-09-18, reviewer, round 1) — one commit per applied task on the job worktree branch
CONTEXT: `docs/roadmap/features/T2_F270.md` T001 and Design ask for a commit on the job worktree
branch after each passed task, authored `Remedy <remedy@local>`, first line `task <n>: <title>` as
a sentence under 72 characters, the contract state as the last body line. Measured at `b7f966c0`:
the branch is `remedy/job-<job id>` (`job_worktree_id` in `packages/orchestration/pingpong_job.py`
prefixes `job-`), not the `remedy/<job id>` the feature file writes, and nothing commits on it;
`run_job` records a task `TASK_APPLIED` and its proof summary before the `_persist_job` call that
saves it; a job's contract criteria change status only in `_gate_job_definition_of_done`, after
its last task; `remedy job resume` refuses with exit 3 when the live worktree `HEAD` differs from
the job's recorded `worktree_head`. A research helper's prototype in a disposable worktree at
`b7f966c0` measured a two-task fake run landing two commits, 0 failures over the worktree, apply
and resume test files, and — with no adoption rule — a second commit of the same task after a
kill between the commit and the save; the reviewer re-ran its two-commit test there, green, and
red at `assert 0 == 2` with the seam disabled.
CHOSEN: (1) WHERE. In `run_job`, after a task is applied and its proof summary is set and before
the `_persist_job` that records it, only when the job's isolation mode is `worktree`; a copy-mode
job commits nothing. The worktree's complete state is committed through its own index (`git add
-A .`), so the branch tip carries exactly what the tasks left in the worktree. (2) IDENTITY.
Author and committer are `Remedy <remedy@local>` whatever the operator's git configuration or
environment says; nothing is signed and no hook runs, because hooks are the operator's gate on the
operator's commits and must not block a job over a branch the operator never checks out. A task
that changed nothing still gets its commit, so one applied task is one commit. The helper that
commits lives in `packages/orchestration/worktrees.py` and refuses, with nothing written, a
checkout whose current branch does not start with `BRANCH_PREFIX`: it can never commit on the
operator's branch. (3) MESSAGE. First line `task <n>: <title>`, n being 1 plus the number of the
job's tasks that already carry a commit (so the branch reads 1, 2, 3 without the gaps a split
parent leaves), the title whitespace-collapsed and cut at a word boundary with `...` so the line
is at most 72 characters; a blank line; one body sentence naming the task id, the job id and the
files the task's apply manifest lists (at most ten, then `...`); a blank line; the line `contract:
<met> of <total> criteria green` over the job's slice (DECISION F269 D3) as recorded when the
commit is made, or `contract: none` when the job belongs to no mission with a contract; a blank
line; the trailers `Remedy-Job: <job id>` and `Remedy-Task: <task id>`. The contract line is the
last body line and the trailers follow as git's trailer paragraph. A job's own gate records its
criteria after its last task, so a per-task line states the criteria as recorded before that
gate — what was recorded, never a forecast. (4) RECORD AND RESUME. The commit's sha is stored on
the task as `worktree_commit` (exported and imported with the job record, "" when none) and
becomes the job's `worktree_head`, so a resumed job's head check matches. A task already carrying
`worktree_commit` is not committed again. A task whose run was interrupted after its commit and
before the save is recognised by the worktree `HEAD` carrying both trailers for this job and this
task while the worktree holds no change against `HEAD`; that commit is adopted, never repeated.
(5) FAILURE. A commit that fails blocks the job with stop reason
`task_<task id>_worktree_commit_failed` and the git error on the task; nothing is retried
silently. (6) Every docstring and doc sentence that says the job worktree is never committed on
is corrected in the same round. The branch tip's tree equals the tree `result.diff` is computed
to, except for a tracked file that `.gitignore` matches, which the branch keeps and the snapshot
drops (R-0974, owned by F273).
ALTERNATIVES: committing only the files the apply manifest lists, rejected because the next task
and `result.diff` both see the whole worktree, so the branch tip would drift from the job's diff;
one commit at the job's end, rejected because T001 asks for one per task; running the operator's
hooks, rejected for the reason (2) gives. REVERSE: remove the seam call, the commit helper and the
task field, restore the docstrings, and delete this paragraph; the branch then carries no commits,
as before.
