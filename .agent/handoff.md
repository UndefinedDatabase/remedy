# Handoff — F270 History apply: one commit per task, merge on demand · Round 2

## Session

SESSION 1 of feature F270 · round 2 · rounds so far 2

Context self-assessment: the worker read the block, AGENTS.md, T2_F270.md, DECISION F270 D1 and D2, `job_apply.py` in full, the prototype diff and test, and the helpers it reuses. Every figure below comes from a command run in this round.

## Range

Review of ff9d56a2..HEAD — branch `feature/f270-history-apply`.

## Summary

Round 2 lands T002 with T003 per DECISION F270 D2. `remedy job apply <job> --approve --commit-with-history` runs every existing gate of `apply_job` unchanged and in its present order. It then checks the D2 (2) refusals, checks them again right before the merge, and runs `git merge --no-ff --no-log --no-edit -m <message> <verified tip>` in the target, under the operator's own identity, configuration and hooks. The merge replaces the file copy and nothing else: the post-apply verification and the post-test run after it exactly as they do after a copy. A failed merge (a conflict or a refusing hook) is aborted with `git merge --abort`. HEAD, the status and `MERGE_HEAD` are then proved back where they were, and the refusal names git's unmerged paths or quotes the hook's output. Every refusal is a blocked apply and exits 0, as a blocked apply does today.

- C1 is the bookkeeping: the payload copies, round 1's verdict booked in the ledger, DECISION F270 D2, and the plan.
- C2 is the code: `job_apply.py` (the flag, the refusals, the merge, the abort, the record fields, the summary and the next-step line), the `--commit-with-history` ArgDef on `job.apply`, and the pass-through in `_cmd_job_apply`.
- C3 is the tests: 15 tests in the new `tests/orchestration/test_job_apply_history.py`.
- C4 is this handoff, plus the block's byte copy that C1 missed (see Deviations).

## Commits

### 8b6a6a10 F270 R2 C1: book round 1's verdict, land DECISION F270 D2 and the round 2 plan
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f270-r2-decisions.md` | +50 / -0 | Byte copy of decisions.md |
| `.agent/authored/f270-r2-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f270-r2-plan.md` | +28 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +50 / -0 | `ff9d56a2` bytes + decisions.md (DECISION F270 D2) |
| `.agent/live_review.md` | +2 / -0 | `ff9d56a2` bytes + ledger.md (Gate F270 R1 PASS) |
| `.agent/plan.md` | +9 / -9 | := plan.md |

141 insertions, 9 deletions (`git show --numstat`).

### 2c3f76ec F270 R2 C2: job apply --approve --commit-with-history merges the job branch with --no-ff as the operator, refusing and aborting without changing anything
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +1 / -0 | `--commit-with-history` ArgDef on `job.apply`: what it does and that it needs `--approve` |
| `apps/cli/commands/do_cmd.py` | +8 / -1 | `_cmd_job_apply` parameter, docstring, pass-through, and the `job.apply` handler |
| `packages/orchestration/job_apply.py` | +316 / -7 | D2 (1) to (7); docstrings of the module, `apply_job` and `_apply_from_workspace` |

325 insertions, 8 deletions (`git show --numstat`).

### 17c8c737 F270 R2 C3: tests prove the no-ff merge as the operator, the preview, plain copy unchanged, and every refusal leaving the target byte-identical
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_job_apply_history.py` | +362 / -0 | h1 to h13 (h7 parametrised over a plain directory and a git target) plus one CLI test |

362 insertions, 0 deletions (`git show --numstat`).

### C4 (this commit) F270 R2 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |
| `.agent/authored/f270-r2-block.md` | +102 / -0 | Byte copy of the block (a payload C1 missed) |

Every commit is under 500 inserted lines. The largest is C3, with 362.

## What C2 builds (DECISION F270 D2)

- **Constants and helpers**:
  - `HISTORY_REFUSED = "history_merge_refused"` prefixes every refusal reason.
  - `_history_git(target, *args)` runs every git call of the path with `timeout=HISTORY_GIT_TIMEOUT_SEC` (120) and never raises: a timeout or an OS error returns rc -1.
- **`_history_refusals(job, target, *, skip_blocked, skipped) -> list[str]`**, each entry one sentence, writing nothing. In order:
  - a staging (copy-mode) job, ending the list, whose sentence says nothing was copied and a plain `--approve` copies;
  - a target that is not the top level of a git repository, also ending the list;
  - a detached `HEAD`;
  - `MERGE_HEAD` present;
  - `git status --porcelain --untracked-files=all` not empty, naming the paths (ten at most, then "and N more");
  - `--skip-blocked` given;
  - a file the copy would skip;
  - `_job_branch_refusal`: the branch missing, its tip not `worktree_head`, or the sha256 of `git diff --no-color --no-ext-diff --src-prefix=a/ --dst-prefix=b/ <job_initial_tree> <tip>^{tree}` not `result_diff_sha256`. The diff is read in text mode and re-encoded as UTF-8, exactly as `worktrees.write_tree_diff` wrote `result.diff`.
- **Where the refusals are checked** in `_apply_from_workspace`:
  - First, after the mode-fidelity gate, which is the last existing gate before the preview branch. A real run blocks on the first sentence and puts the rest in `blocked_reasons`. A preview (`--dry-run` or no `--approve`) stays `dry_run` and carries every sentence in `blocked_reasons`; the summary lists them under "With --approve, --commit-with-history would be refused:" and the "To apply" line ends with `--commit-with-history`.
  - Again right before the merge: after the record preflight, the baseline recheck and the durable pre-apply record. A refusal there persists the final record, as the neighbouring post-record failures do.
- **`build_history_merge_message(job, n, target_branch)`**:
  - The first line is `Merge the <n> task commits of Remedy job <first 8 of the id>`, or "task commit" when n is 1.
  - The body sentence is `This merges <remedy/job-id>, the reviewed work of Remedy job <id>, onto <branch> with one commit per applied task.`
  - Next comes the contract line from round 1's `pingpong_job._task_commit_contract_line`, imported rather than copied.
  - Last come the trailers `Remedy-Job: <id>` and `Co-authored-by: Remedy <remedy@local>`, built from `worktrees.REMEDY_JOB_TRAILER` and `REMEDY_COMMIT_NAME/EMAIL`.
- **`_merge_job_branch`**:
  - It records the previous tip, `merged_branch`, `target_branch` and `history_commits` (`rev-list --reverse <worktree_base_commit>..<worktree_head>`), then merges.
  - On success it proves `HEAD^1` is the previous tip and `HEAD^2` is `worktree_head`, and sets `merge_commit`.
  - On failure it collects `git diff --name-only --diff-filter=U` into `merge_conflicts` and runs `git merge --abort` when `MERGE_HEAD` exists. It then re-reads HEAD, the status and `MERGE_HEAD`: if they are not restored it says so and resets nothing. Otherwise it returns the conflict sentence or the quoted git and hook output, with git's own "Not committing merge" advice line dropped. Output is capped at 300 characters.
- **D2 (5)**: after a merge, a failed post-apply verification, a failed post-test and the parent check each add `_merge_undo_sentence` to `blocked_reasons` and to the summary. The sentence gives the merge sha, the previous tip, "nothing was pushed, Remedy undoes nothing itself", and the one command `git reset --keep <previous tip>`. The `Next:` line of a blocked apply that carries a merge commit names the same command. Remedy itself never runs `git reset`.
- **D2 (6)**: the record and JSON export gain `commit_with_history`, `merged_branch`, `target_branch`, `history_commits`, `merge_commit` and `merge_conflicts`. A merged apply's summary reads `Merged <n> task commit(s) of <branch> onto <branch> as merge commit <sha>. Nothing was pushed.` "No commits or pushes were made" stays for an apply without the flag.
- **D2 (7)**: exit codes are unchanged. `_cmd_job_apply` never exits non-zero on a blocked result, and the CLI test measures 0 for both runs.

## External actions

- G4 ran `git worktree add --detach .remedy-wt/f270-r2/mut 17c8c737` and then `git worktree remove --force` on it. `git worktree list` afterwards shows only `/home/decodeux/Repos/remedy  17c8c737 [feature/f270-history-apply]`.
- After this commit: `git push origin feature/f270-history-apply`, never forced. No pull request is opened this round.
- No evidence job and no zip.

## Verification

G1 to G4 ran at C3 (`17c8c737`), before this commit.

- **G1**: `python3 .remedy-wt/f270-r2/g1.py`, exit 0:
  ```
  digest ledger.md True
  digest decisions.md True
  digest plan.md True
  digest block.md True
  plan.md True
  live_review.md True
  decisions.md True
  authored f270-r2-ledger.md True
  authored f270-r2-decisions.md True
  authored f270-r2-plan.md True
  True
  ```
  After the block copy was written for C4, `python3 .remedy-wt/f270-r2/c4_block.py` also exited 0: `block copy sha256 baefec097a18dbb309a1a90b4c049485dcb2efed37c5425e63150b4643b003a1` and `four authored copies equal payloads: True`.
- **G2**: the block's 16-path list, whose first entry is the new file (the only test file this round edited), serial, `python3 -m pytest -q -p no:cacheprovider …`, exit 0: `514 passed in 183.42s (0:03:03)`.
- **G3**: `python3 -m ruff check packages/orchestration/job_apply.py apps/cli/command_catalog.py apps/cli/commands/do_cmd.py tests/orchestration/test_job_apply_history.py`, exit 0: `All checks passed!`
- **G4**: `python3 .remedy-wt/f270-r2/g4.py 17c8c737`, exit 0.
  - It used one disposable worktree `.remedy-wt/f270-r2/mut` at `17c8c737`, purged `__pycache__` before each run, and ran `python3 -B -m pytest -p no:cacheprovider tests/orchestration/test_job_apply_history.py` from the worktree root.
  - Every run's imported module was `/home/decodeux/Repos/remedy/.remedy-wt/f270-r2/mut/packages/orchestration/job_apply.py`.
  - Each FROM matched exactly once. Each mutation was reverted to the original bytes, and the sha256 `4234f6c3…` matched after each revert.
  - All ids below are under `tests/orchestration/test_job_apply_history.py::`.

  | Run | Change | Result | Failing tests |
  |-----|--------|--------|---------------|
  | control | none (unmutated) | exit 0, `15 passed` | none |
  | (a) | `_history_git(target, "merge", "--abort")` → `pass` | exit 1, `2 failed, 13 passed` | `TestRefusals::test_h6_a_git_conflict_is_aborted_naming_the_unmerged_paths`, `TestRefusals::test_h13_a_refusing_pre_merge_commit_hook_is_aborted_and_quoted` |
  | (b) | `elif dirty:` → `elif False:` | exit 1, `3 failed, 12 passed` | `TestTheMerge::test_h3_without_approve_the_flag_previews_and_names_the_refusals`, `TestRefusals::test_h4_a_dirty_tree_is_refused_naming_the_path`, `TestThroughTheCli::test_a_refused_and_a_merging_run_exit_zero_with_their_record_keys` |
  | (c) | `"--no-ff"` removed from the merge call | exit 1, `3 failed, 12 passed` | `TestTheMerge::test_h2_no_ff_even_where_a_fast_forward_was_possible`, `TestRefusals::test_h13_…` (a fast-forward runs no pre-merge-commit hook), `TestThroughTheCli::…` |
  | (d) | `branch_refusal = ""` (no tip or diff-hash check) | exit 1, `2 failed, 13 passed` | `TestRefusals::test_h10_a_moved_branch_tip_is_refused`, `TestRefusals::test_h11_a_deleted_branch_is_refused` |
  | (e) | the `symbolic-ref` check → `if False:` | exit 1, `1 failed, 14 passed` | `TestRefusals::test_h9_a_detached_head_is_refused` |
  | (f) | `commit_with_history = False` at the top of `_apply_from_workspace` (the flag ignored, files copied) | exit 1, `13 failed, 2 passed` | including `TestTheMerge::test_h1_the_merge_lands_both_task_commits_as_the_operator` |

  No mutation stayed green.
- **Full suite**: not run (amend0917-throughput).

## Authored-text proofs

- `.agent/authored/f270-r2-{ledger.md,decisions.md,plan.md}` (C1) and `.agent/authored/f270-r2-block.md` (C4) equal their payloads byte for byte (G1 and `c4_block.py`).
- The block copy's sha256 is `baefec097a18dbb309a1a90b4c049485dcb2efed37c5425e63150b4643b003a1`, the digest the orchestrator named.
- `.agent/live_review.md` and `.agent/decisions.md` are their `ff9d56a2` bytes with ledger.md and decisions.md appended. `.agent/plan.md` is plan.md (G1).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | deviated | `8b6a6a10`; the block copy landed in C4 instead |
| C2 merge path | done | `2c3f76ec` |
| C3 tests h1–h13 + CLI | done | `17c8c737` |
| C4 handoff and push | done | This commit, then the push |
| G1–G4 | done | All exit 0; every mutation red |

## Open findings

`python3 .remedy-wt/f268-r4/count.py` (distinct id) at HEAD reads `registrations 131 done 4 open 127`. This round registers no finding and resolves none.

## Deviations & assumptions

- **Commit sequence**: the order was C1, C2, C3, C4, then the push, with no split of C3. **The block's byte copy was not in C1.** The block lists `block.md` among the payloads, but C1 copied only ledger.md, decisions.md and plan.md, so G1 as run checked three copies. C4 adds `.agent/authored/f270-r2-block.md` and re-checks all four. C1 was not rewritten because C2 and C3 already sat on it.
- **The merge names the verified tip sha, not the branch name**: `git merge … <worktree_head>`. `_job_branch_refusal` has just shown the branch tip equals that sha. Merging the sha means a branch that moves between the check and the merge cannot bring in unreviewed commits. The content is the same as D2 (3)'s merge "of `remedy/job-<job id>`", and the message names the branch.
- **Two refusals D2 (2) does not list**:
  - `MERGE_HEAD` already present. Without this check, the D2 (4) `git merge --abort` could abort the operator's own unfinished merge.
  - A target that is a git repository but not its top level. The copy writes `target/<path>` while a merge writes `<top level>/<path>`, so the post-apply verification would compare the wrong files. I read D2's "not a git repository" as covering it.
- **"1 task commit"**: D2 (3) writes `<n> task commits`. The first line uses the singular when n is 1, so it stays a sentence.
- **Where a preview's refusals live**: a `dry_run` result with the flag carries its refusal sentences, each prefixed `history_merge_refused: `, in the existing `blocked_reasons` list. The alternative was a seventh record field, which D2 (6) does not name. The operator's previous tip for the D2 (5) undo sentence is kept on the result as `history_previous_head`, which is not exported. It reaches the record only inside that sentence in `blocked_reasons`.
- **A hook's output is quoted on one line**: whitespace-collapsed, git's "Not committing merge; use 'git commit'…" advice dropped, capped at 300 characters. Measured on git 2.34.1 in a scratch probe: a failing `pre-merge-commit` hook leaves `MERGE_HEAD` and the job's files staged, and its stdout and stderr both reach git's stderr. For the `pkg` versus `pkg/mod.txt` clash, git 2.34.1 reports `pkg~HEAD` as the only unmerged path, and `git merge --abort` restores the operator's `pkg` file. h6 asserts every reported path appears in the sentence, not the literal `pkg~HEAD`.
- **Observation, not changed**: the merge does not check that `worktree_base_commit` is an ancestor of the operator's `HEAD`. On a branch that does not contain the job's base, the merge also brings in the base's ancestry. D2's list does not name this case, the gates still bind the files, and nothing here would be overwritten.
- **Observation, not changed**: R-0974 (a tracked but ignored file) can make the branch tip's tree differ from `result.diff`. The diff-hash refusal then refuses the merge rather than dropping the file silently. That is the designed outcome of D2 (2), and it was not tested this round.
- **Not changed**: `do`'s `--commit-with-history` stays "not yet available" (T004), as the block orders. No `docs/` page changed. The Built State doc for the flag belongs to the closure sequence in `.agent/plan.md`.
- **Scratch scripts**: `.remedy-wt/f270-r2/probe_git.py`, `c1.py`, `g1.py`, `g4.py` and `c4_block.py` are gitignored. They ran the git probe, did the byte work, and ran G1 and G4.

## Next

Phase 1 rule 1 (`.agent/STOP`), then the review of round 2.

Operator questions open: 5
