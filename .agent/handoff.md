# Handoff — F273 Findings paydown v1 · Round 18

## Session

SESSION 3 of feature F273 · round 18 · rounds so far 18

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D18, the handback template, round 17's handoff as the template's instance and every hunk of the three diffs as it applied them, and held all of it without loss; every figure below comes from a command run in this round.

## Range

Review of f445a2c0..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 18 books round 17's verdict and three resolutions, registers R-0993, lands DECISION F273 D18 and the third ruling of operator question Q4, and builds R-0993, R-0977 and R-0992 as the reviewer's dry run built them.
- C1 books Gate F273 R17 (VERDICT PASS) and three `Done:` lines (R-0914, R-0927, R-0928), registers R-0993, lands DECISION F273 D18, rewrites the plan and `.agent/operator_questions.md` (Q4's third ruling), and saves the five payload copies.
- C2 (R-0993): `dod_process_exec_policy` sets `PYTHONDONTWRITEBYTECODE=1` on the scrub source, and the pytest check runs with `-p no:cacheprovider`; two new tests prove a check writes nothing into the tree it judges and a gated pytest check in a repository with a passing suite leaves the `do` job completed.
- C3 (R-0977): `do`'s shape step records on each job the milestone its outline came from (or the plan's only milestone) and merges that milestone's slice with `hold_on_milestone=False`; the planner criterion now reads `met` or `unmet`, never `open`, except under `--force-job` on a plan of several milestones. `docs/guides/do-run-v1.md` states both.
- C4 (R-0992): `memory_candidates.py`, the `memory candidates`, `memory approve-candidate` and `memory reject-candidate` words, the cockpit's candidate count and checklist items, the `dev status` key `memory_candidates_ok` and the smoke section 12aq are deleted with their tests; `docs/system/vocabulary.md` carries a dated status paragraph.
- C5 is this handoff.

Landed: R-0993 — `ab9ab436` (C2)
Landed: R-0977 — `77b644be` (C3)
Landed: R-0992 — `d28f2826` (C4)

## Commits

### a02d0477 F273 R18 C1: bookkeeping — round 17's verdict and its three resolutions booked, R-0993 registered, DECISION F273 D18 and Q4's third ruling landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r18-block.md` | +119 / -0 | Byte copy of the block |
| `.agent/authored/f273-r18-decisions.md` | +27 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r18-ledger.md` | +10 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r18-operator_questions.md` | +68 / -0 | Byte copy of operator_questions.md |
| `.agent/authored/f273-r18-plan.md` | +30 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +27 / -0 | `f445a2c0` bytes + decisions.md (DECISION F273 D18) |
| `.agent/live_review.md` | +10 / -0 | `f445a2c0` bytes + ledger.md (Gate F273 R17, three `Done:` lines, R-0993) |
| `.agent/operator_questions.md` | +3 / -1 | := operator_questions.md (Q4 third ruling) |
| `.agent/plan.md` | +13 / -10 | := plan.md |

307 insertions, 11 deletions (`git show --numstat`).

### ab9ab436 F273 R18 C2: R-0993 — a DoD check runs with PYTHONDONTWRITEBYTECODE set and pytest without its cache provider, so it writes nothing into the worktree it judges
All by `git apply .remedy-wt/f273-proto-g8a.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/dod_runners.py` | +2 / -1 | pytest argv gains `-p no:cacheprovider` |
| `packages/orchestration/exec_guard.py` | +7 / -1 | DoD policy env sets `PYTHONDONTWRITEBYTECODE=1` |
| `tests/cli/test_do_sequence_cli.py` | +30 / -0 | `commit_a_passing_suite` helper; job completes under a gated pytest check |
| `tests/orchestration/test_dod_runners.py` | +10 / -0 | A check writes no bytecode and no cache |
| `tests/orchestration/test_exec_guard.py` | +4 / -1 | Policy env pins the set key, and the scrubbed child carries it |

53 insertions, 3 deletions.

### 77b644be F273 R18 C3: R-0977 — each do job records the milestone it serves, and its gate evaluates that milestone's criterion without holding the job on it
All by `git apply .remedy-wt/f273-proto-g8b.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/guides/do-run-v1.md` | +3 / -2 | `shape` row and `--push` paragraph |
| `packages/orchestration/do_sequence.py` | +36 / -16 | Milestone per job order; `record_job_milestone`; `hold_on_milestone=False` |
| `packages/orchestration/mission_contract.py` | +9 / -5 | `hold_on_milestone` keyword on the slice merge |
| `tests/cli/test_do_commit_flags.py` | +12 / -3 | Push tests commit a passing suite; open-criterion test uses `--force-job` on two milestones |
| `tests/cli/test_do_sequence_cli.py` | +83 / -7 | Planner criterion reads `unmet`; two two-milestone tests |

143 insertions, 33 deletions.

### d28f2826 F273 R18 C4: R-0992 — the memory-candidate store, its three memory words, the cockpit readers, the dev status key and the smoke section go with their tests
All by `git apply .remedy-wt/f273-proto-g8c.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +0 / -38 | Three catalog entries deleted |
| `apps/cli/commands/dev.py` | +1 / -11 | `memory_candidates_ok` key and its help line deleted |
| `apps/cli/commands/memory.py` | +0 / -120 | Three handlers deleted |
| `docs/system/vocabulary.md` | +10 / -0 | Status paragraph (R-0992) |
| `packages/orchestration/memory_candidates.py` | +0 / -115 | Deleted |
| `packages/orchestration/ui_server.py` | +0 / -5 | Live-state candidate count deleted |
| `packages/orchestration/ui_view_model.py` | +0 / -17 | Checklist candidate items deleted |
| `scripts/remedy_smoke.sh` | +1 / -37 | Smoke section 12aq and the dev-status key deleted |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | Deleted module |
| `tests/orchestration/test_project_brain.py` | +0 / -79 | Store tests removed |
| `tests/test_cli_execution_loop_closure.py` | +5 / -117 | Word tests removed; absence of the count and key pinned |
| `tests/test_command_catalog.py` | +3 / -0 | Three ids listed as deleted |
| `tests/test_data_paths.py` | +1 / -3 | Routed-handler case re-pointed at `memory learn` |
| `tests/test_repair_context_reviewer_memory.py` | +5 / -85 | Store tests removed; absence of the count pinned |
| `tests/ui_contracts/test_ux_quality.py` | +7 / -8 | A held candidate is not listed |

33 insertions, 636 deletions.

### C5 (this commit) F273 R18 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 307.

## External actions

- `git worktree add --detach .remedy-wt/f273-r18-g5 d28f2826` for G5, then `git worktree remove --force .remedy-wt/f273-r18-g5` as the step's last action (exit 0; the tree was clean, `git status --porcelain` read `''` after the reverts). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                         d28f2826 [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-s3-r18  bd877325 (detached HEAD)
  ```
  `.remedy-wt/f273-s3-r18` is the reviewer's; the worker did not touch it.
- The branch `remedy/job-81ec65896729405c` still exists in this repository. A research helper's probe created it before round 16; nobody may delete it without the operator. `git branch --list 'remedy/job-*'` reads 37 branches after the gates.
- After C5: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C4 `d28f2826` with a clean tree. Every script ran with an explicit `cwd`; a script's exit code is its process's own (the tool reports a non-zero exit as an error, and none was reported).

- **Transport**, before any write: `.remedy-wt/f273-r18/wk_digests.py` printed True for the block, the six payloads and the three diffs. The block file read 119 lines.
- **Block copy**, before C1: `.remedy-wt/f273-r18/wk_c1.py`:
  ```
  saved block lines 119 sha256 b150c3023b578a750b8e0d4170711db2ea055b70f48867dd46b5625e5a4c1540
  given block lines 119 sha256 b150c3023b578a750b8e0d4170711db2ea055b70f48867dd46b5625e5a4c1540
  equal True
  ```
- **G1**: `python3 .remedy-wt/f273-r18/wk_g1.py`, exit 0:
  ```
  True digest .remedy-wt/f273-r18/plan.md
  True digest .remedy-wt/f273-r18/ledger.md
  True digest .remedy-wt/f273-r18/decisions.md
  True digest .remedy-wt/f273-r18/operator_questions.md
  True digest .remedy-wt/f273-r18/next.md
  True digest .remedy-wt/f273-s3/r18_targets.txt
  True digest .remedy-wt/f273-r18/block.md
  True digest .remedy-wt/f273-proto-g8a.diff
  True digest .remedy-wt/f273-proto-g8b.diff
  True digest .remedy-wt/f273-proto-g8c.diff
  True .agent/plan.md == payload
  True .agent/operator_questions.md == payload
  True .agent/live_review.md == base + ledger.md
  True .agent/decisions.md == base + decisions.md
  True .agent/authored/f273-r18-plan.md == payload
  True .agent/authored/f273-r18-ledger.md == payload
  True .agent/authored/f273-r18-decisions.md == payload
  True .agent/authored/f273-r18-operator_questions.md == payload
  True .agent/authored/f273-r18-block.md == payload
  True ab9ab436 paths == numstat of f273-proto-g8a.diff 5
  True 77b644be paths == numstat of f273-proto-g8b.diff 5
  True d28f2826 paths == numstat of f273-proto-g8c.diff 15
  ```
- **G2**: `python3 .remedy-wt/f273-r18/wk_g2.py` (`git rev-parse d28f2826:<sub>`), exit 0:
  ```
  a52f51b4dd93071e87afe8d23dc04a9bff425d99 tests True
  9754f8efaa0572938f7ca34549d377a1c3912407 packages True
  606b88b001ea70d32e9fa6d41e2fc2d64e95a426 apps True
  f10debd13cab12e3de9e9289f6280395cae8e590 docs True
  9dfa0d7d9f2824f65dbf9cc094ec2e1047b93e18 scripts True
  ```
  All five equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial): `python3 .remedy-wt/f273-r18/wk_g3.py` runs `python3 -m pytest -q -p no:cacheprovider` over the 30 lines of `r18_targets.txt`, `env=` without `PYTHONDONTWRITEBYTECODE`, exit 0:
  ```
  targets 30
  summary: 2576 passed, 5 skipped in 357.17s (0:05:57)
  R-0803 lines: 0
  pytest exit 0
  ```
- **G4**: `python3 .remedy-wt/f273-r18/wk_g4.py` (`ruff check . --output-format concise` and `bash -n scripts/remedy_smoke.sh`, both with `cwd` the primary checkout's root), exit 0:
  ```
  All checks passed!
  ruff exit 0
  bash -n exit 0
  ```
- **G5** (`python3 .remedy-wt/f273-r18/wk_g5.py`, exit 0): one detached worktree at `d28f2826`; `python3 -m pytest -q -p no:cacheprovider` over D, R and F from its root; env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` and lacks `PYTHONDONTWRITEBYTECODE`; `__pycache__` purged before every run; each FROM counted as a whole line with its newline; each file reverted from its saved bytes.
  ```
  do_sequence resolves to: /home/decodeux/Repos/remedy/.remedy-wt/f273-r18-g5/packages/orchestration/do_sequence.py
  inside worktree: True
  [control] 119 passed in 94.48s | exit 0
  (a) packages/orchestration/exec_guard.py: FROM count 1; expected red: D and R
      [mut_a] 8 failed, 111 passed in 88.83s | exit 1 | RED
          D ::test_a_gated_pytest_check_in_a_repo_with_a_passing_suite_leaves_the_job_completed
          D ::test_a_two_milestone_do_in_a_repo_with_a_passing_suite_meets_both_planner_criteria
          R ::TestPytestKind::test_a_check_writes_no_bytecode_and_no_cache_into_the_tree_it_judges
          F ::test_push_sends_exactly_one_fast_forward_push_to_the_upstream
          F ::test_the_key_with_a_commit_flag_pushes_once_without_push
          F ::test_a_push_the_remote_refuses_leaves_the_commit_and_fails_the_walk
          F ::test_a_two_job_walk_under_commit_lands_two_linear_commits_and_one_push
          F ::test_the_apply_step_never_passes_push_to_a_job
  (b) packages/orchestration/dod_runners.py: FROM count 1; expected red: R
      [mut_b] 1 failed, 118 passed in 90.10s | exit 1 | RED
          R ::TestPytestKind::test_a_check_writes_no_bytecode_and_no_cache_into_the_tree_it_judges
  (c) packages/orchestration/do_sequence.py: FROM count 1; expected red: D
      [mut_c] 4 failed, 115 passed in 91.80s | exit 1 | RED
          D ::test_contract_cli_tool_gates_the_job_on_its_whole_mission_checks_and_names_the_unmet
          D ::test_a_do_whose_order_proposes_no_template_names_only_criteria_not_met
          D ::test_a_two_milestone_do_ends_with_no_planner_criterion_open
          D ::test_a_two_milestone_do_in_a_repo_with_a_passing_suite_meets_both_planner_criteria
  (d) packages/orchestration/mission_contract.py: FROM count 1; expected red: D and F
      [mut_d] 37 failed, 82 passed in 81.03s | exit 1 | RED  (26 in D, 11 in F)
          D ::test_init_to_study_registers_studies_once_and_records_it
          D ::test_init_writes_every_ignore_entry_into_the_repos_exclude_file
          D ::test_study_to_plan_creates_the_mission_carrying_the_order
          D ::test_plan_to_shape_yields_one_job_linked_to_the_mission_targeting_the_repo
          D ::test_shape_to_run_completes_on_the_named_fake_providers
          D ::test_the_teacher_narrates_the_job_do_ran_without_a_budget
          D ::test_run_to_stop_leaves_the_target_untouched_and_stops_before_apply
          D ::test_job_apply_accepts_the_job_do_ran
          (F, first of 11) ::test_commit_lands_one_commit_with_that_first_line_and_the_trailers
  worktree git status after reverts: ''
  ```
  Each mutation printed `reverted: True`. Every mutation went red; none stayed green. The ids are abbreviated to their file letter; full logs are `.remedy-wt/f273-r18/g5_*.log`.
- **G6** runs after the push and is reported in the round report, because this commit comes before it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r18/wk_c1.py` from `git show f445a2c0:<path>` bytes and the payload bytes, with no hand edit. G1 re-proves every C1 file and every `.agent/authored/f273-r18-*` copy against its payload.
- The code and docs arrived only by `git apply` of the three reviewer-verified diffs, in the block's order; before each commit `git status --porcelain` listed exactly the paths the apply touched, all staged (the deletion of `memory_candidates.py` included), and nothing untracked. G1 proves each commit's path set equals its diff's; G2's object ids equal the reviewer's dry-run objects.
- The `## Next` body below is `next.md` byte for byte, appended by `.remedy-wt/f273-r18/wk_c5.py`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping (Gate F273 R17, three `Done:` lines, R-0993 registered, D18, Q4 third ruling) | done | `a02d0477` |
| R-0993 | done | `ab9ab436` (C2) |
| R-0977 | done | `77b644be` (C3) |
| R-0992 | done | `d28f2826` (C4) |
| G1 to G5 | done | All green / red-proofs red as above |
| C5 handoff + push | done | This commit, then the push |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r18/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registers it in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `a02d0477` (C1 onwards; C2 to C4 do not touch it; the same at `d28f2826`): **45 open**;
- at `f445a2c0`: 47 open.

C1's three `Done:` lines close three distinct ids and it registers R-0993: 47 - 3 + 1 = 45. The three ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C5, then the push. No extra commit.
- **G4 first attempt:** before the scripted G4, the worker ran `python3 -m ruff check /home/decodeux/Repos/remedy --output-format concise` from the session's working directory (the same root, by absolute path rather than `.`); it read `All checks passed!`. The reported G4 is the scripted run with `cwd` the root and the literal `.`.
- **An attempted `$?`:** one Bash call tried `echo "exit=$?"` after G1; the shell refused it before anything ran, and G1 was re-run plainly.
- **G5 extra red:** mutation (a) reddens five tests in F beside the three in D and R the block names; mutation (d) reddens 26 in D and 11 in F. Both are wider than the block states, never narrower.
- **G5 worktree removal:** `worktree remove` was given `--force` as a precaution against ignored bytecode; the tree's `git status --porcelain` was empty beforehand, so nothing tracked was discarded. Made with `--detach`, so no branch was created.
- **G5 interpreter:** `python3 -m pytest` without `-B`, as the block orders; `__pycache__` was purged before every run instead.
- **Payload copies:** the five files the block names for C1 went to `.agent/authored/` as `f273-r18-<name>`. `next.md` is not copied; it lives in this handoff's `## Next`.
- **Operator questions:** the count below is the number of `### Q<n>` headings in `.agent/operator_questions.md` (Q1, Q2, Q4, Q5, Q7).
- **Scratch:** gitignored under `.remedy-wt/f273-r18/`: `wk_digests.py`, `wk_c1.py`, `wk_g1.py`, `wk_g2.py`, `wk_g3.py`, `wk_g4.py`, `wk_g5.py`, `wk_count.py`, `wk_c5.py`, `handoff_head.md`, and the logs `g3.log`, `g5_*.log`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 18 over `f445a2c0`..the round 18
   handoff commit, booked as `Gate: F273 R18` with `Done:` lines for R-0993, R-0977 and R-0992 in
   the next round's first commit.
2. An owner for every open id outside F273's own list (amend0911-feedback rule A), then the
   closure sequence.

Operator questions open: 5
