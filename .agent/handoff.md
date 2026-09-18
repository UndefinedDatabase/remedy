# Handoff — F270 History apply: one commit per task, merge on demand · Round 1

## Session

SESSION 1 of feature F270 · round 1 · rounds so far 1

Context self-assessment: the worker read the block, AGENTS.md, T2_F270.md, DECISION F270 D1, the prototype, `worktrees.py` in full and every `pingpong_job.py` region it edited once each, and every figure below comes from a command run in this round.

## Range

Review of b7f966c0..HEAD — branch `feature/f270-history-apply`.

## Summary

Round 1 claims F270 and lands T001 per DECISION F270 D1: every applied task of a worktree-mode job lands as one commit on `remedy/job-<job id>`, authored and committed `Remedy <remedy@local>`, unsigned and hook-free, recorded on the task as `worktree_commit` and as the job's `worktree_head`, adopted rather than repeated when HEAD already carries this job's and this task's trailers over a clean worktree, and blocking the job with `task_<id>_worktree_commit_failed` when it fails.

- C1 claimed F270: payload copies, plan, context, the re-headed ledger (Gate F269 R13 PASS, `Done: R-0973`, R-0974 registered, Owner F273), DECISION F270 D1, STATUS `[~]`, and the R-0974 acceptance line in T2_F273.md.
- C2 is the code: `commit_job_worktree`, `read_head_remedy_trailers` and `worktree_matches_head` in `worktrees.py`; the `TaskEntry.worktree_commit` field with its export and import, `build_task_commit_message`, `_commit_applied_task` and the seam in `run_job` in `pingpong_job.py`; the D1 (6) docstring and doc corrections.
- C3 is the tests: seven new tests in `tests/orchestration/test_job_worktree_integration.py`.
- C4 is this handoff.

## Commits

### b58eeb95 F270 R1 C1: claim F270, book F269 round 13 verdict and R-0973 resolution, register R-0974, land DECISION F270 D1
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f270-r1-block.md` | +121 / -0 | Byte copy of the block |
| `.agent/authored/f270-r1-context.md` | +43 / -0 | Byte copy of context.md |
| `.agent/authored/f270-r1-decisions.md` | +53 / -0 | Byte copy of decisions.md |
| `.agent/authored/f270-r1-f273_from.txt` | +4 / -0 | Byte copy of f273_from.txt |
| `.agent/authored/f270-r1-f273_to.txt` | +7 / -0 | Byte copy of f273_to.txt |
| `.agent/authored/f270-r1-ledger.md` | +6 / -0 | Byte copy of ledger.md |
| `.agent/authored/f270-r1-live_review_head.md` | +22 / -0 | Byte copy of live_review_head.md |
| `.agent/authored/f270-r1-plan.md` | +28 / -0 | Byte copy of plan.md |
| `.agent/authored/f270-r1-status_from.txt` | +1 / -0 | Byte copy of status_from.txt |
| `.agent/authored/f270-r1-status_to.txt` | +1 / -0 | Byte copy of status_to.txt |
| `.agent/context.md` | +17 / -15 | := context.md |
| `.agent/decisions.md` | +53 / -0 | `b7f966c0` bytes + decisions.md (DECISION F270 D1) |
| `.agent/live_review.md` | +24 / -20 | live_review_head.md + `b7f966c0` bytes from `## Findings` + ledger.md |
| `.agent/plan.md` | +18 / -15 | := plan.md |
| `docs/roadmap/STATUS.md` | +1 / -1 | F270 line `[ ]` to `[~]` (status_from.txt to status_to.txt) |
| `docs/roadmap/features/T2_F273.md` | +3 / -0 | f273_from.txt replaced by f273_to.txt: the R-0974 acceptance line |

402 insertions, 51 deletions (`git show --numstat`).

### ff323f0e F270 R1 C2: every applied task lands as one Remedy commit on its job worktree branch, adopted on resume, blocking the job on failure
| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/first-fulfilled-job-demo-v0.md` | +5 / -2 | D1 (6): lines 124 and 140 |
| `packages/orchestration/pingpong_job.py` | +119 / -7 | Field, export/import, message builder, adopt-or-commit step, seam, D1 (6) docstrings |
| `packages/orchestration/worktrees.py` | +86 / -6 | Commit helper, trailer reader, clean check, D1 (6) docstrings |

210 insertions, 15 deletions (`git show --numstat`).

### 1da36563 F270 R1 C3: tests prove two Remedy commits for a two-task run, the operator's identity and hooks ignored, adoption, branch refusal, the message, copy mode and the failure block
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_job_worktree_integration.py` | +205 / -0 | Class `TestPerTaskCommitsOnTheJobBranch`, t1 to t7 |

205 insertions, 0 deletions (`git show --numstat`).

### C4 (this commit) F270 R1 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 402.

## What C2 builds (DECISION F270 D1)

- `worktrees.commit_job_worktree(path, message) -> sha` refuses with `WorktreeError`, before anything is written, a checkout whose `rev-parse --abbrev-ref HEAD` does not start with `BRANCH_PREFIX`. Otherwise it runs `git add -A .` and then `git -c core.hooksPath=/dev/null commit --no-verify --no-gpg-sign --allow-empty --quiet -F -`. It sets `GIT_AUTHOR_NAME/EMAIL` and `GIT_COMMITTER_NAME/EMAIL` to `Remedy`/`remedy@local` in the environment. Every git call has a timeout: the two writes use `GIT_COMMIT_TIMEOUT_SEC = 120`, and the branch read and the `rev-parse` use `_git`'s 60 seconds.
- `worktrees.read_head_remedy_trailers(path)` reads HEAD's `Remedy-Job` and `Remedy-Task` through `%(trailers:only,unfold)`. `worktrees.worktree_matches_head(path)` is `status --porcelain --untracked-files=all` empty.
- `pingpong_job.build_task_commit_message(job, task)` writes the first line `task <n>: <title>`, where n is 1 plus the number of other tasks that carry a commit. The title is whitespace-collapsed and cut at a word boundary with `...` to at most 72 characters. The body sentence is `Remedy applied task <id> of job <id>, changing <files, at most ten then ...>.` Then come `contract: <met> of <total> criteria green` (or `contract: none`) and the two trailers.
- `pingpong_job._commit_applied_task` adopts HEAD (via `W.snapshot`) when both trailers match and the worktree is clean. Otherwise it commits. It then sets `task.worktree_commit` and `job.worktree_head`.
- The seam in `run_job` sits after `previous_summaries.append(task.proof_summary)` and before `tasks_run += 1; _persist_job(job)`. It runs only when `isolation_mode == "worktree"`, a handle exists and `worktree_commit` is blank. If the commit fails, the task becomes `TASK_BLOCKED` with error `worktree_commit_failed: <type>: <git error>`, and `_block_job` sets job error `task_<id>_worktree_commit_failed`.

### D1 (6) sentences changed
1. `worktrees.py` `WorktreeHandle.head_commit` comment: "worktree HEAD (== base_commit until committed)" → "worktree HEAD: base_commit until a job task's commit (F270) moves it".
2. `worktrees.py` `retain_for_recovery` docstring: "Keep the worktree — and its uncommitted changes —" and "Nothing is committed and nothing is merged … because the run's changes are uncommitted and the worktree is the only place they exist" → this call commits nothing and merges nothing, and the changes past the branch tip (all of a single run's, and a job task's that never reached its F270 commit) exist only in the worktree.
3. `pingpong_job.py` `_finalize_job_workspace` docstring: "(tree-to-tree — no commit, no merge)" → this step makes no commit and no merge, and the branch already carries one commit per applied task. "KEEP the worktree and its uncommitted changes" → "KEEP the worktree with every change it holds past the branch tip".
4. `pingpong_job.py` `_finalize_job_workspace` retain comment: "the accepted changes are uncommitted and live ONLY in this worktree" → the hand-off lives in this worktree, and any change past the branch tip lives only there.
5. `docs/system/first-fulfilled-job-demo-v0.md` line 124: "Git operations (no commits, branches, or PRs)" → no commit on the operator's branch and no PR; the per-task commits on `remedy/job-<job id>` (F270) are not exercised by the demo.
6. Same file, line 140 (now 142): "No git operations: no commits, no branches, no PRs" → no commit on the operator's branch and no PR; a job's own branch gets one commit per applied task.

## External actions

- `git worktree add --detach .remedy-wt/f270-r1-mut 1da36563` for G4, then `git worktree remove --force` on it. `git worktree list` afterwards: `/home/decodeux/Repos/remedy  1da36563 [feature/f270-history-apply]` alone.
- After this commit: `git push -u origin feature/f270-history-apply`, never forced. No pull request is opened this round.
- No evidence job and no zip.

## Verification

All gates ran at C3 (`1da36563`), before this commit.

- **G1**: `python3 .remedy-wt/f270-r1/g1.py`, exit 0:
  ```
  payload digests match: True
  plan.md equals payload: True
  context.md equals payload: True
  live_review.md equals head + base from ## Findings + ledger: True
  decisions.md equals base + payload: True
  STATUS.md equals base with the pair applied: True
  T2_F273.md equals base with the pair applied: True
  authored copies equal payloads: True 10
  block.md sha256: 86c4ec7a3489d8458103e0bb25d49369df829a8da2549c3fac5375fea735f418
  ```
- **G2**: the block's 31-path list, serial, `python3 -m pytest -q -p no:cacheprovider …`, exit 0: `1035 passed in 217.74s (0:03:37)`. The only test file this round edited, `test_job_worktree_integration.py`, is already first in the list.
- **G3**: `python3 -m ruff check packages/orchestration/worktrees.py packages/orchestration/pingpong_job.py tests/orchestration/test_job_worktree_integration.py`, exit 0: `All checks passed!`
- **G4**: `python3 .remedy-wt/f270-r1/g4.py`, exit 0. It uses one disposable worktree `.remedy-wt/f270-r1-mut` at `1da36563`, `__pycache__` purged before each run, and `python3 -B -m pytest -p no:cacheprovider tests/orchestration/test_job_worktree_integration.py` from the worktree root. Every run's imported module was `/home/decodeux/Repos/remedy/.remedy-wt/f270-r1-mut/packages/orchestration/worktrees.py`. Each mutation was reverted by its exact original bytes, and worktree status was empty after each revert.
  - control (unmutated): exit 0, `20 passed`
  - (a) seam's commit step skipped (`if False and (job.isolation_mode == …`): exit 1, `4 failed, 16 passed`: t1 `test_a_two_task_run_lands_two_remedy_commits_on_the_job_branch`, t2 `test_the_operators_identity_and_hooks_never_reach_the_job_commits`, t3 `test_a_commit_already_made_for_the_task_is_adopted_not_repeated`, t7 `test_a_failed_commit_blocks_the_job`
  - (b) the two `GIT_COMMITTER_*` entries removed from the helper's environment: exit 1, `2 failed, 18 passed`: t1, t2
  - (c) adoption check removed (`adopt = False and (…`): exit 1, `1 failed, 19 passed`: t3
  - (d) branch refusal removed (`if False and not branch.startswith(BRANCH_PREFIX):`): exit 1, `1 failed, 19 passed`: t4 `test_the_commit_helper_refuses_the_operators_checkout`
  - All ids are under `tests/orchestration/test_job_worktree_integration.py::TestPerTaskCommitsOnTheJobBranch::`. No mutation stayed green.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Byte copies are at `.agent/authored/f270-r1-{plan.md,context.md,live_review_head.md,ledger.md,decisions.md,status_from.txt,status_to.txt,f273_from.txt,f273_to.txt,block.md}`. All ten equal their payloads (G1). The block copy's sha256 is `86c4ec7a3489d8458103e0bb25d49369df829a8da2549c3fac5375fea735f418`, the digest the orchestrator named.
- STATUS: TO contains FROM: False. FROM was 1x before and 0x after, and TO 1x after: a rewrite. T2_F273.md: TO contains FROM: True. FROM was 1x before and after, and TO 1x after. C1's diff adds exactly the three TO-only lines, in order: an append.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 claim | done | `b58eeb95` |
| C2 commit on the branch | done | `ff323f0e` |
| C3 tests t1–t7 | done | `1da36563` |
| C4 handoff and push | done | This commit, then the push |
| G1–G4 | done | All exit 0 and every mutation red |

## Open findings

`python3 .remedy-wt/f268-r4/count.py` (distinct id) at HEAD reads `registrations 131 done 4 open 127`. This round registers R-0974 (Owner F273) and books `Done: R-0973`. Neither is F270's.

## Deviations & assumptions

- **Commit sequence**: as ordered (C1, C2, C3, C4, then the push). No split into C2a/C2b: C2 has 210 insertions.
- **A failed commit also marks its task `TASK_BLOCKED`.** D1 (5) names only the job's stop reason and the git error on the task. The task stays `TASK_APPLIED` in no case where its commit is missing. That matches the neighbouring post-apply failure (`target_repo_mutated_after_apply`), and it stops a resume from skipping the task as applied and folding its change into the next task's commit.
- **An empty title**: the first line falls back to `task <n>: untitled task`. D1 does not settle this case. I did not measure whether the parser can produce an empty title.
- **A malformed contract body**: `read_mission_contract` raises, so the commit step fails and the job blocks with `task_<id>_worktree_commit_failed`. This is the same body the job's DoD gate would refuse.
- **Observation, not changed**: in the D1 (4) kill window (after the commit, before the save), `remedy job resume` compares the live head against a checkpoint's recorded `worktree_head` (`apps/cli/commands/job.py` around line 1465) and, per D1's CONTEXT, refuses with exit 3 on a difference. So a checkpoint written before the commit could stop the CLI path before `run_job` can adopt. This was not measured. The adoption is reachable through `resume_job_plan` and `run_job`, which is what t3 drives. Changing the CLI's head check is outside this round's change set.
- **Observation, not changed**: `docs/system/vocabulary.md` line 269 still names the branch `remedy/<job id>` inside the verbatim DECISION amend0905-vocab D10 paragraph. It is a quoted operator decision, not a sentence saying the worktree is never committed on, so D1 (6) does not reach it.
- **Scratch scripts**: `.remedy-wt/f270-r1/build_c1.py`, `g1.py` and `g4.py` (gitignored) did the byte work and ran G1 and G4.

## Next

Phase 1 rule 1 (`.agent/STOP`), then the review of round 1.

Operator questions open: 5
