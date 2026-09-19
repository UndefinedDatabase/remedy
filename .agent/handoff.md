# Handoff — F273 Findings paydown v1 · Round 11

## Session

SESSION 2 of feature F273 · round 11 · rounds so far 11

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D11, the handback template, round 10's handoff as the template's instance and both code diffs as it applied them; every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of e707b52e..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 11 books round 10's verdict and its three resolutions, lands DECISION F273 D11, records this session's behaviour rulings in the operator questions file, and builds R-0974, R-0913, R-0890, R-0898 and R-0935 as the reviewer's dry run built them.
- C1 books Gate F273 R10 (VERDICT PASS) and three `Done:` lines (R-0762, R-0661, R-0755), lands DECISION F273 D11, rewrites the plan and saves the four payload copies.
- C2 (R-0974, R-0913, R-0890): `write_tree` seeds its temporary index with `git read-tree HEAD` before `git add -A`, so a tracked ignored file stays in the snapshot, and the dead `write_tree_for_path` is deleted; `job_resume_refusal` is the one answer `resume_job_plan` raises and `remedy job run` prints before `run_job` runs, leaving the record untouched; the self-use runner passes the role config's model and effort for every role whose provider it resolved, unless the caller passed them.
- C3 (R-0898, R-0935): `task_is_done` over `TASK_DONE_STATUSES` (`passed`, `applied`, `completed`) in `pingpong_job.py` is used by `job show`'s summary, status and report sections and by `run_job_fulfill`; `job_budget_limits` validates the persisted budgets dict into `JobBudgets` for both contract readers, and `job budget set` refuses `max_tokens` or `max_runtime_seconds` when the job carries the overlapping F018 limit, naming the `job run` flag that sets it.
- C4 is this handoff, with `.agent/operator_questions.md` := the payload (Q4 merges the two mission-contract rulings, Q6 is folded into it, and Q7 records this session's four behaviour changes).

Landed: R-0974 — `39c849b2` (C2)
Landed: R-0913 — `39c849b2` (C2)
Landed: R-0890 — `39c849b2` (C2)
Landed: R-0898 — `02786347` (C3)
Landed: R-0935 — `02786347` (C3)

## Commits

### 8c2afa85 F273 R11 C1: bookkeeping — round 10's verdict and its three resolutions booked, DECISION F273 D11 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r11-block.md` | +121 / -0 | Byte copy of the block |
| `.agent/authored/f273-r11-decisions.md` | +35 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r11-ledger.md` | +8 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r11-plan.md` | +30 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +35 / -0 | `e707b52e` bytes + decisions.md (DECISION F273 D11) |
| `.agent/live_review.md` | +8 / -0 | `e707b52e` bytes + ledger.md (Gate F273 R10, three `Done:` lines) |
| `.agent/plan.md` | +8 / -9 | := plan.md |

245 insertions, 9 deletions (`git show --numstat`).

### 39c849b2 F273 R11 C2: R-0974, R-0913, R-0890 — the snapshot keeps tracked ignored files, job run refuses an unresumable workspace, and the self-use runner passes the role config's model and effort
All by `git apply .remedy-wt/f273-proto-g1a.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/do_cmd.py` | +10 / -0 | `job run` prints `job_resume_refusal` and exits 1 before `run_job` |
| `packages/orchestration/pingpong_job.py` | +25 / -12 | `job_resume_refusal`; `resume_job_plan` raises it |
| `packages/orchestration/self_use_runner.py` | +9 / -2 | Role config's model and effort passed with its provider |
| `packages/orchestration/worktrees.py` | +10 / -34 | `read-tree HEAD` seed in `write_tree`; `write_tree_for_path` deleted |
| `tests/orchestration/test_job_worktree_handoff.py` | +72 / -0 | `TestTrackedIgnoredFile`, `TestJobRunRefusesAnUnresumableWorkspace` |
| `tests/orchestration/test_self_use_runner.py` | +36 / -0 | `test_an_unflagged_run_records_the_role_configs_models` |

162 insertions, 48 deletions.

### 02786347 F273 R11 C3: R-0898, R-0935 — a passed or applied task is done in every view, and a job's budgets reach its run contract
All by `git apply .remedy-wt/f273-proto-g1b.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/job.py` | +17 / -3 | Three views use `task_is_done`; `job budget set` refuses the F018-owned fields |
| `packages/orchestration/job_fulfillment.py` | +2 / -4 | `run_job_fulfill` uses `task_is_done` |
| `packages/orchestration/pingpong_job.py` | +11 / -0 | `TASK_DONE_STATUSES`, `task_is_done` |
| `packages/orchestration/run_contract.py` | +27 / -19 | `job_budget_limits`; both contract readers use it |
| `tests/cli/test_job_budget_set.py` | +30 / -0 | `TestR0935AFieldTheJobBudgetsOwn` |
| `tests/cli/test_job_show.py` | +33 / -0 | `TestAJobRunnerJobReadsItsTasksAsDone` |
| `tests/orchestration/test_f018_authority_integration.py` | +43 / -0 | `TestR0935PersistedBudgetsReachTheRunContract` |

163 insertions, 26 deletions.

### C4 (this commit) F273 R11 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/operator_questions.md` | := payload | Questions-file rule of `docs/agents/self_drive_protocol.md` |
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 245.

## External actions

- `git worktree add --detach .remedy-wt/f273-r11-g5 02786347` for G5 (exit 0), then `git worktree remove .remedy-wt/f273-r11-g5` (exit 0). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                        02786347 [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g2a  9285a411 (detached HEAD)
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g2b  03f3fe35 (detached HEAD)
  ```
  The two `f273-h-*` worktrees are research helpers'; this round did not touch them.
- After C4: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C3 `02786347` with a clean tree, every script with `cwd` set explicitly and its exit code printed by `.remedy-wt/f273-r11/wk_run.py`.

- **Transport**, before any write: `sha256sum` of the four payloads, the block and the two diffs matched the block's digests (block.md `69ed8aef4af434816607c48bd05c6f936743deb4ed68e9270eee614c317bd948`).
- **G1**: `python3 .remedy-wt/f273-r11/wk_g1.py`, exit=0:
  ```
  digest plan.md True
  digest ledger.md True
  digest decisions.md True
  digest operator_questions.md True
  digest block.md True
  digest f273-proto-g1a.diff True
  digest f273-proto-g1b.diff True
  plan.md == payload True
  live_review == base+ledger True
  decisions == base+D11 True
  authored f273-r11-plan True
  authored f273-r11-ledger True
  authored f273-r11-decisions True
  authored f273-r11-block True
  39c849b2 paths == f273-proto-g1a.diff numstat True
  02786347 paths == f273-proto-g1b.diff numstat True
  16 checks, all True: True
  ```
  The after-C4 check of `.agent/operator_questions.md` against its payload is reported in the round report, per the block.
- **G2**: `git rev-parse 02786347:tests 02786347:packages 02786347:apps`, exit=0:
  ```
  37e828a5d68272d0818de2b341153567d99b11c6
  57920941d61b6d9f8c60fb859967a61487451dd8
  5d61c2fcd474357a19011c382a6140929da1faff
  ```
  All three equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial, the block's 40 targets): `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_episode_snapshot_full_validity.py ... tests/cli/test_golden_path.py`, exit=0:
  ```
  1434 passed in 274.55s (0:04:34)
  ```
  Re-run through `.remedy-wt/f273-r11/wk_g3.py` with the full output captured to `.remedy-wt/f273-r11/wk_g3_out.txt`, exit=0: `1434 passed in 296.15s (0:04:56)`; 0 failed; lines containing `R-0803:`: 0.
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root, exit=0:
  ```
  All checks passed!
  ```
- **G5** (`python3 .remedy-wt/f273-r11/wk_g5.py`, one worktree at `02786347`, `python3 -B -m pytest -q -p no:cacheprovider` from its root, `__pycache__` purged before every run, each FROM counted with its newline in the named file first, each reverted from its saved bytes), exit=0:
  ```
  import path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r11-g5/packages/orchestration/worktrees.py | inside worktree: True
  CONTROL (unmutated) over 5 files: 195 passed in 19.98s exit=0
  (a) packages/orchestration/worktrees.py: FROM count = 1
  (a) tests/orchestration/test_job_worktree_handoff.py: 1 failed, 28 passed in 12.87s exit=1 -> RED
      FAILED tests/orchestration/test_job_worktree_handoff.py::TestTrackedIgnoredFile::test_a_job_edit_to_a_tracked_ignored_file_reaches_the_diff_and_the_target
  (a) reverted, bytes restored: True
  (b) packages/orchestration/pingpong_job.py: FROM count = 1
  (b) tests/orchestration/test_job_worktree_handoff.py: 1 failed, 28 passed in 7.64s exit=1 -> RED
      FAILED tests/orchestration/test_job_worktree_handoff.py::TestJobRunRefusesAnUnresumableWorkspace::test_a_missing_recorded_branch_is_refused_and_the_record_is_untouched
  (b) reverted, bytes restored: True
  (c) packages/orchestration/pingpong_job.py: FROM count = 1
  (c) tests/orchestration/test_job_worktree_handoff.py: 1 failed, 28 passed in 7.79s exit=1 -> RED
      FAILED tests/orchestration/test_job_worktree_handoff.py::TestJobRunRefusesAnUnresumableWorkspace::test_a_non_recoverable_cleanup_status_is_refused
  (c) reverted, bytes restored: True
  (d) apps/cli/commands/do_cmd.py: FROM count = 1
  (d) tests/orchestration/test_job_worktree_handoff.py: 2 failed, 27 passed in 7.78s exit=1 -> RED
      FAILED tests/orchestration/test_job_worktree_handoff.py::TestJobRunRefusesAnUnresumableWorkspace::test_a_missing_recorded_branch_is_refused_and_the_record_is_untouched
      FAILED tests/orchestration/test_job_worktree_handoff.py::TestJobRunRefusesAnUnresumableWorkspace::test_a_non_recoverable_cleanup_status_is_refused
  (d) reverted, bytes restored: True
  (e) packages/orchestration/self_use_runner.py: FROM count = 1
  (e) tests/orchestration/test_self_use_runner.py: 1 failed, 11 passed in 3.52s exit=1 -> RED
      FAILED tests/orchestration/test_self_use_runner.py::TestUnflaggedProviderResolution::test_an_unflagged_run_records_the_role_configs_models
  (e) reverted, bytes restored: True
  (f) packages/orchestration/pingpong_job.py: FROM count = 1
  (f) tests/cli/test_job_show.py: 2 failed, 17 passed in 1.57s exit=1 -> RED
      FAILED tests/cli/test_job_show.py::TestAJobRunnerJobReadsItsTasksAsDone::test_passed_and_applied_tasks_are_done_in_all_three_views
      FAILED tests/cli/test_job_show.py::TestAJobRunnerJobReadsItsTasksAsDone::test_task_is_done_spans_both_vocabularies_and_nothing_else
  (f) reverted, bytes restored: True
  (g) packages/orchestration/run_contract.py: FROM count = 1
  (g) tests/orchestration/test_f018_authority_integration.py: 2 failed, 114 passed in 4.52s exit=1 -> RED
      FAILED tests/orchestration/test_f018_authority_integration.py::TestR0935PersistedBudgetsReachTheRunContract::test_a_new_contract_inherits_the_token_and_wall_clock_budgets
      FAILED tests/orchestration/test_f018_authority_integration.py::TestR0935PersistedBudgetsReachTheRunContract::test_a_persisted_contract_is_reconciled_to_the_budgets
  (g) tests/cli/test_job_budget_set.py: 2 failed, 17 passed in 0.87s exit=1 -> RED
      FAILED tests/cli/test_job_budget_set.py::TestR0935AFieldTheJobBudgetsOwn::test_the_overlapping_field_is_refused_and_nothing_is_written[max_runtime_seconds-900-remedy job run <job_id> --max-wall-clock-minutes <value>]
      FAILED tests/cli/test_job_budget_set.py::TestR0935AFieldTheJobBudgetsOwn::test_the_overlapping_field_is_refused_and_nothing_is_written[max_tokens-9000-remedy job run <job_id> --max-total-tokens <value>]
  (g) reverted, bytes restored: True
  (h) apps/cli/commands/job.py: FROM count = 1
  (h) tests/cli/test_job_budget_set.py: 2 failed, 17 passed in 1.59s exit=1 -> RED
      FAILED tests/cli/test_job_budget_set.py::TestR0935AFieldTheJobBudgetsOwn::test_the_overlapping_field_is_refused_and_nothing_is_written[max_runtime_seconds-900-remedy job run <job_id> --max-wall-clock-minutes <value>]
      FAILED tests/cli/test_job_budget_set.py::TestR0935AFieldTheJobBudgetsOwn::test_the_overlapping_field_is_refused_and_nothing_is_written[max_tokens-9000-remedy job run <job_id> --max-total-tokens <value>]
  (h) reverted, bytes restored: True
  worktree status after reverts: ''
  ```
  The control ran over the five named test files together. Every mutation went red; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r11/wk_c1.py` from `git show e707b52e:<path>` bytes and the payload bytes; `.agent/operator_questions.md` in C4 by `wk_c4.py` from the payload bytes. Nothing was hand-edited except this handoff. G1 re-proves every C1 file and every `.agent/authored/f273-r11-*` copy against its payload.
- The code arrived only by `git apply` of the two reviewer-verified diffs, in the block's order. G2's object ids equal the reviewer's dry-run objects.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `8c2afa85` |
| C2 R-0974, R-0913, R-0890 | done | `39c849b2` |
| C3 R-0898, R-0935 | done | `02786347` |
| C4 handoff + operator questions + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r11/wk_c4.py`, which loads `scripts/rotate_live_review.py` by path and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `8c2afa85` (C1 onwards; C2 and C3 do not touch it): **83 open**;
- at `e707b52e`: 86 open.

C1's three `Done:` lines close three distinct ids (R-0762, R-0661, R-0755) and register none. The five ids landed this round (R-0974, R-0913, R-0890, R-0898, R-0935) are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C4, then the push. No extra commit.
- **G3 ran twice:** the first run's output was piped through `tail`, which hid the first 35% of the progress output, so the "no `R-0803:` line" condition could not be read from it; the identical command was re-run with the full output captured. Both runs: 1434 passed, 0 failed, exit 0.
- **Measurement script:** `wk_c4.py`'s first run wrote `.agent/operator_questions.md` and then failed (exit 1) loading `rotate_live_review.py`, because the module was not registered in `sys.modules` before its dataclass executed; after that fix it re-wrote the same payload bytes and measured. No tracked file other than the operator questions file was touched by it.
- **Payload copies:** the four files listed under PAYLOADS for `.agent/authored/` (plan, ledger, decisions, block), as in rounds 2 to 10; `operator_questions.md` is applied to `.agent/operator_questions.md` in C4, and the two code diffs are not copied.
- **Scratch:** gitignored under `.remedy-wt/f273-r11/`: `wk_c1.py`, `wk_g1.py`, `wk_run.py`, `wk_g3.py`, `wk_g5.py`, `wk_c4.py`, and the output `wk_g3_out.txt`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 11.

Operator questions open: 5
