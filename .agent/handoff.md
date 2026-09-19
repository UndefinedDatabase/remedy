# Handoff — F273 Findings paydown v1 · Round 19

## Session

SESSION 3 of feature F273 · round 19 · rounds so far 19

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D19, the handback template, round 18's handoff as the template's instance and every hunk of the three diffs as it applied them, and held all of it without loss; every figure below comes from a command run in this round.

## Range

Review of 17c7f169..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 19 books round 18's verdict and three resolutions and the fifteen ids that are moot or already met, lands DECISION F273 D19, and builds the dead residue, the small repairs and the D3 sentences D19 names, as the reviewer's dry run built them.
- C1 books Gate F273 R18 (VERDICT PASS), three `Done:` lines for round 18's ids (R-0993, R-0977, R-0992) and fifteen for the moot or met ids (R-0830, R-0846, R-0849, R-0854, R-0857, R-0868, R-0869, R-0883, R-0840, R-0842, R-0844, R-0845, R-0848, R-0853, R-0865); lands DECISION F273 D19, whose part (4) amends DECISION F260 D3 with the sentences R-0851, R-0852, R-0856 and R-0860 asked of it; rewrites the plan; saves the four payload copies.
- C2 (R-0831, R-0832, R-0850, R-0941, R-0867, R-0863, R-0884): the three route-policy flags in `apps/cli/grouped.py`, the `context_budget_optimized` schema and NowCard entry (the dead-coupling list empties and its ceiling falls to 0), `_job_with_repo`, the test-only functions of `proposed_tasks.py`, `provider_patch_material.py` with its roadmap rule, two `REVIEW_FINDINGS_OPEN` members, and `AcceptanceCheck` with `Verifier` are deleted with their tests.
- C3 (R-0828, R-0826, R-0937): `_stop_job` sets `finished_at`; the self-use reporter answers a stop that never finalized, a run-manifest error and a task that did not pass with a blank error; the smoke script's message names `task_type=`.
- C4 (R-0851, R-0852, R-0856, R-0860): `docs/system/core-product-spine-v0.md` carries a dated status banner and stops listing the deleted command groups.
- C5 is this handoff.

Landed: R-0831 — `9189c0c9` (C2)
Landed: R-0832 — `9189c0c9` (C2)
Landed: R-0850 — `9189c0c9` (C2)
Landed: R-0941 — `9189c0c9` (C2)
Landed: R-0867 — `9189c0c9` (C2)
Landed: R-0863 — `9189c0c9` (C2)
Landed: R-0884 — `9189c0c9` (C2)
Landed: R-0828 — `5108e9d1` (C3)
Landed: R-0826 — `5108e9d1` (C3)
Landed: R-0937 — `5108e9d1` (C3)
Landed: R-0851 — `411f66b3` (C1, D19 (4)) and `1f8ea570` (C4)
Landed: R-0852 — `411f66b3` (C1, D19 (4)) and `1f8ea570` (C4)
Landed: R-0856 — `411f66b3` (C1, D19 (4)) and `1f8ea570` (C4)
Landed: R-0860 — `411f66b3` (C1, D19 (4)) and `1f8ea570` (C4)

## Commits

### 411f66b3 F273 R19 C1: bookkeeping — round 18's verdict and three resolutions booked, the moot and met ids booked, DECISION F273 D19 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r19-block.md` | +112 / -0 | Byte copy of the block |
| `.agent/authored/f273-r19-decisions.md` | +41 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r19-ledger.md` | +38 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r19-plan.md` | +30 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +41 / -0 | `17c7f169` bytes + decisions.md (DECISION F273 D19) |
| `.agent/live_review.md` | +38 / -0 | `17c7f169` bytes + ledger.md (Gate F273 R18, eighteen `Done:` lines) |
| `.agent/plan.md` | +14 / -14 | := plan.md |

314 insertions, 14 deletions (`git show --numstat`).

### 9189c0c9 F273 R19 C2: dead residue — the route-policy flags, the context_budget_optimized readers, _job_with_repo, the test-only proposed-task functions, provider_patch_material, two REVIEW_FINDINGS_OPEN members and AcceptanceCheck with Verifier go with their tests
All by `git apply .remedy-wt/f273-proto-g9a2.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/grouped.py` | +0 / -9 | Three route-policy flags (R-0831) |
| `apps/ui/src/api/actionClass.ts` | +0 / -1 | `context_budget_optimized` bookkeeping kind (R-0832) |
| `docs/system/provider-patch-materialization-v0.md` | +3 / -2 | The module is deleted (R-0867) |
| `packages/contracts/interfaces.py` | +1 / -18 | `Verifier` protocol (R-0884) |
| `packages/core/models.py` | +0 / -7 | `AcceptanceCheck` (R-0884) |
| `packages/orchestration/event_schemas.py` | +0 / -5 | `context_budget_optimized` schema (R-0832) |
| `packages/orchestration/mission_readiness.py` | +0 / -1 | `REVIEW_FINDINGS_OPEN` (R-0863) |
| `packages/orchestration/proposed_tasks.py` | +1 / -342 | Test-only functions and their helpers (R-0941) |
| `packages/orchestration/provider_patch_material.py` | +0 / -547 | Deleted (R-0867) |
| `packages/orchestration/self_dogfood.py` | +0 / -3 | Roadmap rule testing for the deleted file (R-0867) |
| `packages/orchestration/self_dogfood_execution.py` | +0 / -1 | `REVIEW_FINDINGS_OPEN` (R-0863) |
| `pyproject.toml` | +0 / -1 | Deleted module's mypy entry |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | Deleted module |
| `tests/orchestration/test_event_ledger.py` | +0 / -16 | Schema tests of the deleted event |
| `tests/orchestration/test_event_name_coupling.py` | +7 / -8 | Dead-coupling list empty, ceiling 0 |
| `tests/orchestration/test_proposed_tasks.py` | +8 / -206 | Tests of the deleted functions |
| `tests/orchestration/test_provider_patch_material.py` | +0 / -103 | Deleted |
| `tests/orchestration/test_token_economy_integration.py` | +0 / -17 | `_job_with_repo` (R-0850) |
| `tests/orchestration/test_worker_execution.py` | +4 / -20 | Readiness test of the deleted report |
| `tests/test_imports.py` | +3 / -6 | `AcceptanceCheck` and `Verifier` imports |

27 insertions, 1314 deletions.

### 5108e9d1 F273 R19 C3: small repairs — a stopped job records its finish time, the self-use reporter answers an unfinalized stop, a manifest error and a failed task with a blank error, and the smoke messages name keyword arguments
All by `git apply .remedy-wt/f273-proto-g9b2.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/self-use-track-v1.md` | +1 / -1 | Reporter row names what it answers (R-0826) |
| `packages/orchestration/pingpong_job.py` | +1 / -0 | `_stop_job` sets `finished_at` (R-0828) |
| `packages/orchestration/self_use_findings.py` | +21 / -11 | Unfinalized stop, manifest error, non-passing task (R-0826) |
| `scripts/remedy_smoke.sh` | +1 / -1 | Message names `task_type=` (R-0937) |
| `tests/orchestration/test_predictive_budget.py` | +28 / -0 | Budget stop persists `stopped` with a finish time |
| `tests/orchestration/test_self_use_findings.py` | +40 / -0 | Two reporter tests |
| `tests/test_remedy_smoke_script.py` | +6 / -6 | Assertion messages name `task_type=` |

98 insertions, 19 deletions.

### 1f8ea570 F273 R19 C4: the command taxonomy of the core product spine stops listing the deleted command groups, as DECISION F260 D3's amendment in D19 rules
All by `git apply .remedy-wt/f273-proto-g9c2.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/core-product-spine-v0.md` | +5 / -9 | Status banner; deleted groups leave the tables |

5 insertions, 9 deletions.

### C5 (this commit) F273 R19 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 314.

## External actions

- `git worktree add --detach .remedy-wt/f273-r19-g5 1f8ea570` for G5, then `git worktree remove --force .remedy-wt/f273-r19-g5` as the step's last action (exit 0; the tree's `git status --porcelain` read `''` after the reverts). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                         1f8ea570 [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-s3-r19  71dd1f51 (detached HEAD)
  ```
  `.remedy-wt/f273-s3-r19` is the reviewer's; the worker did not touch it.
- The branch `remedy/job-81ec65896729405c` still exists in this repository. A research helper's probe created it before round 16; nobody may delete it without the operator. `git branch --list 'remedy/job-*'` reads 37 branches after the gates.
- After C5: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C4 `1f8ea570` with a clean tree. Every script ran with an explicit `cwd`; exit codes are the process's own, printed as `EXIT_CODE` by `.remedy-wt/f273-r19/wk_run.py` or by the gate script itself.

- **Transport**, before any write: `sha256sum` of the block, the five payloads and the three diffs each equalled the block's digest; the block file read 112 lines.
- **Block copy**, before C1: `.remedy-wt/f273-r19/wk_c1.py`:
  ```
  saved block sha256 cab453471fc37e3d6915b3b4228515e7ec50178802aec1e69344513197929dd4 lines 112
  given block sha256 cab453471fc37e3d6915b3b4228515e7ec50178802aec1e69344513197929dd4 lines 112
  equal True
  ```
- **G1 and G2**: `python3 .remedy-wt/f273-r19/wk_g1g2.py`, EXIT_CODE 0:
  ```
  G1
  digest .remedy-wt/f273-r19/plan.md True
  digest .remedy-wt/f273-r19/ledger.md True
  digest .remedy-wt/f273-r19/decisions.md True
  digest .remedy-wt/f273-r19/next.md True
  digest .remedy-wt/f273-r19/block.md True
  digest .remedy-wt/f273-s3/r19_targets.txt True
  digest .remedy-wt/f273-proto-g9a2.diff True
  digest .remedy-wt/f273-proto-g9b2.diff True
  digest .remedy-wt/f273-proto-g9c2.diff True
  plan.md == payload True
  live_review.md == base + ledger True
  decisions.md == base + decisions True
  authored f273-r19-plan.md True
  authored f273-r19-ledger.md True
  authored f273-r19-decisions.md True
  authored f273-r19-block.md True
  paths 9189c0c9 f273-proto-g9a2.diff 20 True
  paths 5108e9d1 f273-proto-g9b2.diff 7 True
  paths 1f8ea570 f273-proto-g9c2.diff 1 True
  G2
  tests 9e0972ba882e0f07dee9d883474344ccf27eca05
  packages 519a486b77948a2eabf0f3a45248265e56eaf712
  apps 39a6be279a37193ae0ebcf00d97cadb542da960f
  docs 562fdc1bab1c8ed3e18aaa6f6de27116dce0cb86
  scripts 866c1b06bafcedd6f4cca87b588dccae60d37531
  EXIT_CODE 0
  ```
  All five G2 objects equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial): `python3 .remedy-wt/f273-r19/wk_g3.py` runs `python3 -m pytest -q -p no:cacheprovider` over the lines of `r19_targets.txt`, `env=` without `REMEDY_OLLAMA_HOST` and `OLLAMA_HOST`:
  ```
  target paths 24
  R-0803 lines 0
  2228 passed, 4 skipped in 195.06s (0:03:15)
  EXIT_CODE 0
  ```
- **G4**: `ruff` and `bash -n`, each through `wk_run.py` with `cwd` the primary checkout's root:
  ```
  python3 -m ruff check . --output-format concise
  All checks passed!
  EXIT_CODE 0
  bash -n scripts/remedy_smoke.sh
  EXIT_CODE 0
  ```
- **G5** (`python3 .remedy-wt/f273-r19/wk_g5.py`, exit 0): one detached worktree at `1f8ea570`; `python3 -m pytest -q -p no:cacheprovider` from its root; env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`; `__pycache__` purged before every run; each FROM counted as a whole line with its newline; each file reverted from its saved bytes.
  ```
  import path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r19-g5/packages/orchestration/pingpong_job.py
  purged __pycache__ dirs: 2
  control summary: 88 passed in 16.78s
  control EXIT_CODE 0
  (a) packages/orchestration/pingpong_job.py FROM count: 1
  purged __pycache__ dirs: 9
  (a) summary: 1 failed, 75 passed in 3.86s
     FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_provider_call_budget_stop_persists_stopped_with_a_finish_time
  (a) EXIT_CODE 1
  (a) reverted: True
  (b) packages/orchestration/self_use_findings.py FROM count: 1
  purged __pycache__ dirs: 9
  (b) summary: 1 failed, 5 passed in 1.32s
     FAILED tests/orchestration/test_self_use_findings.py::TestDescribeSelfUseRunDefects::test_a_stop_that_never_finalized_surfaces_its_stop_and_its_manifest_error
  (b) EXIT_CODE 1
  (b) reverted: True
  (c) tests/orchestration/test_event_name_coupling.py FROM count: 1
  purged __pycache__ dirs: 7
  (c) summary: 2 failed, 4 passed in 11.81s
     FAILED tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_the_declared_set_only_ever_shrinks
     FAILED tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_no_declared_entry_is_stale
  (c) EXIT_CODE 1
  (c) reverted: True
  worktree status after reverts: ''
  ```
  Every mutation went red in the file the block names; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit comes before it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r19/wk_c1.py` from `git show 17c7f169:<path>` bytes and the payload bytes, with no hand edit. G1 re-proves every C1 file and every `.agent/authored/f273-r19-*` copy against its payload.
- The code and docs arrived only by `git apply` of the three reviewer-verified diffs, in the block's order; before each commit `git status --porcelain` listed exactly the paths the apply touched, all staged (the deletions of `provider_patch_material.py` and its test included), and nothing untracked. G1 proves each commit's path set equals its diff's; G2's object ids equal the reviewer's dry-run objects.
- The `## Next` body below is `next.md` byte for byte, appended by `.remedy-wt/f273-r19/wk_c5.py`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping (Gate F273 R18, eighteen `Done:` lines, D19) | done | `411f66b3` |
| R-0831 | done | `9189c0c9` (C2) |
| R-0832 | done | `9189c0c9` (C2) |
| R-0850 | done | `9189c0c9` (C2) |
| R-0941 | done | `9189c0c9` (C2) |
| R-0867 | done | `9189c0c9` (C2) |
| R-0863 | done | `9189c0c9` (C2) |
| R-0884 | done | `9189c0c9` (C2) |
| R-0828 | done | `5108e9d1` (C3) |
| R-0826 | done | `5108e9d1` (C3) |
| R-0937 | done | `5108e9d1` (C3) |
| R-0851 | done | `411f66b3` (C1, D19 (4)) and `1f8ea570` (C4) |
| R-0852 | done | `411f66b3` (C1, D19 (4)) and `1f8ea570` (C4) |
| R-0856 | done | `411f66b3` (C1, D19 (4)) and `1f8ea570` (C4) |
| R-0860 | done | `411f66b3` (C1, D19 (4)) and `1f8ea570` (C4) |
| G1 to G5 | done | All green / red-proofs red as above |
| C5 handoff + push | done | This commit, then the push |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r19/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registers it in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `411f66b3` (C1 onwards; C2 to C4 do not touch it; the same at `1f8ea570`): **27 open**;
- at `17c7f169`: 45 open.

C1's eighteen `Done:` lines close eighteen distinct ids: 45 - 18 = 27. The fourteen ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C5, then the push. No extra commit.
- **An attempted `$?`:** one Bash call tried `echo "exit=$?"` after the first G1/G2 run; the shell refused the call before anything ran, and G1/G2 were run once through `wk_run.py`, which prints the real exit code.
- **G5 worktree removal:** `worktree remove` was given `--force` as a precaution against ignored bytecode; the tree's `git status --porcelain` was empty beforehand, so nothing tracked was discarded. Made with `--detach`, so no branch was created.
- **G5 control scope:** the control ran B, S and E together (88 passed); each mutation ran only the file the block names for it.
- **Payload copies:** the four files the block names for C1 went to `.agent/authored/` as `f273-r19-<name>`. `next.md` is not copied; it lives in this handoff's `## Next`.
- **Operator questions:** the count below is the number of `### Q<n>` headings in `.agent/operator_questions.md` (Q1, Q2, Q4, Q5, Q7), unchanged this round.
- **Scratch:** gitignored under `.remedy-wt/f273-r19/`: `wk_c1.py`, `wk_run.py`, `wk_g1g2.py`, `wk_g3.py`, `wk_g5.py`, `wk_count.py`, `wk_c5.py`, `handoff_head.md`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 19 over `17c7f169`..the round 19
   handoff commit, booked as `Gate: F273 R19` with `Done:` lines for R-0831, R-0832, R-0850,
   R-0941, R-0867, R-0863, R-0884, R-0828, R-0826, R-0937, R-0851, R-0852, R-0856 and R-0860 in the
   next round's first commit.
2. The closure sequence of `docs/roadmap/STATUS_closure_protocol.md`, with the next paydown's
   registration and the ownership paragraph DECISION F273 D19 (5) leads into.

Operator questions open: 5
