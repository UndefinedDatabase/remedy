
## Built State (F270, 2026-09-18)

What exists on disk at the close of F270; every DECISION named lives in `.agent/decisions.md`.
The job worktree branch is `remedy/job-<job id>`, the name the code has used since F047; this file
writes it `remedy/<id>` above.

**T001 — one commit per applied task.** In `run_job` (`packages/orchestration/pingpong_job.py`),
after a task of a git-target job is applied and before it is saved, the worktree's complete state
is committed on the job branch by `commit_job_worktree` in `packages/orchestration/worktrees.py`:
author and committer `Remedy <remedy@local>` whatever the operator's configuration says, no
signing, no hook, and a refusal of any branch that is not Remedy's own. The message is `task <n>:
<title>` within 72 characters, one body sentence, the contract line `contract: <met> of <total>
criteria green` or `contract: none`, and the trailers `Remedy-Job` and `Remedy-Task`. The sha is
the task's `worktree_commit` and the job's `worktree_head`; a commit an interrupted run already
made is adopted by its trailers, never repeated; a failed commit blocks the job (DECISION F270 D1;
`tests/orchestration/test_job_worktree_integration.py`). A copy-mode job commits nothing.

**T002 and T003 — `--commit-with-history`.** `remedy job apply <job> --approve
--commit-with-history` runs every existing apply gate, then, in place of the copy, `git merge
--no-ff --no-log` of the verified job-branch tip onto the operator's current branch under the
operator's identity and hooks, with the message `Merge the <n> task commits of Remedy job <id>`,
the contract line and the trailers `Remedy-Job` and `Co-authored-by: Remedy <remedy@local>`. It
refuses, changing nothing, a staging job, a target that is not a repository's top level, a
detached `HEAD`, the operator's own merge in progress, a dirty tree, `--skip-blocked`, a file the
copy would skip, and a branch that is missing, moved, or whose tree is not the reviewed
`result.diff`; a conflict or a refusing hook is aborted and named. A committed hand edit to a job
file is refused by the baseline gate before git runs (DECISIONs F270 D2 and F263 D-E;
`tests/orchestration/test_job_apply_history.py`).

**T004 — `--commit`, `--commit-auto`, `--push` and the key.** On `job apply`, `--commit
"<message>"` and `--commit-auto` land ONE commit of exactly the copied files on the operator's
branch after the copy verified and the post-test passed, under the operator's identity, with the
contract line and both trailers; `--commit-auto`'s first line starts with an imperative verb and
fits 72 characters. `--push` needs a commit flag, pushes the landed commit to the branch's
configured upstream once, never forced, and is refused before anything is written without an
upstream or while a blocking criterion of the mission is `unmet`; an `open` one is named, not held
(DECISIONs F270 D3 and D4 (6); `tests/orchestration/test_job_apply_commit.py`). `remedy do` takes
the same flags, refuses what it cannot do before any step, chains every job of the walk under a
commit flag so each is cut from its predecessor's commit, and pushes the mission once after its
last job; `apply.push_after_mission` in `packages/orchestration/config.py` makes a `do` run with a
commit flag push as `--push` would (DECISION F270 D4; `tests/cli/test_do_commit_flags.py`,
`docs/guides/do-run-v1.md`). Without a commit flag, `job apply` and `do` commit nothing on the
operator's branch, the key set or not.

**Findings.** R-0975 and R-0976 were raised and resolved inside the feature. R-0974 (a tracked
file `.gitignore` matches never reaches `result.diff`) and R-0977 (`do`'s planner criteria are
never evaluated) were found here and are owned by F273. No finding owned by F270 stays open.
