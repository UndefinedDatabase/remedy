# Handoff — F273 Findings paydown v1 · Round 12

## Session

SESSION 2 of feature F273 · round 12 · rounds so far 12

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D12, the handback template, round 11's handoff as the template's instance and both code diffs as it applied them. Every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of 4c375fc4..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 12 books round 11's verdict and its five resolutions, registers R-0988, lands DECISION F273 D12, and builds R-0921, R-0917, R-0922, R-0899, R-0910, R-0980, R-0978 and R-0988 as the reviewer's dry run built them.
- C1 books Gate F273 R11 (VERDICT PASS), five `Done:` lines (R-0974, R-0913, R-0890, R-0898, R-0935) and the R-0988 registration. It also lands DECISION F273 D12, rewrites the plan and saves the four payload copies.
- C2 (R-0921, R-0917, R-0922):
  - `_validate_linkage` resolves an intent id through `approval_queue._find_artifact_for_intent`.
  - `verifying_test_run_action` names `remedy test run <job> --intent-id <id> --apply-id <id>`, and `patch apply` prints it as its last line and carries it as `next_safe_action` in its JSON.
  - A new test drives `do run --yes` through the parser to the auto-approval branch.
- C3 (R-0899, R-0910, R-0980, R-0978, R-0988):
  - The smoke script's job check reads `status`, and section 12s is dropped.
  - Tests now hold section 0's words to the catalog's groups, run section 3's check on real `job show` output, and pin 12s's absence.
  - `test_study_run_dispatch_e2e` points `REMEDY_OLLAMA_HOST` at a loopback listener that hangs up, with a 30-second timeout.
  - The `no_model_call` fixture imports `study` first and patches its own binding.
  - The smoke script's direct-run test runs in `tmp_path`.
- C4 is this handoff. R-0916's ruling is DECISION F273 D12 (4), landed in C1; it needs no code.

Landed: R-0921 — `bb31b060` (C2)
Landed: R-0917 — `bb31b060` (C2)
Landed: R-0922 — `bb31b060` (C2)
Landed: R-0899 — `c29ecda7` (C3)
Landed: R-0910 — `c29ecda7` (C3)
Landed: R-0980 — `c29ecda7` (C3)
Landed: R-0978 — `c29ecda7` (C3)
Landed: R-0988 — `c29ecda7` (C3)

## Commits

### 122dbc60 F273 R12 C1: bookkeeping — round 11's verdict and its five resolutions booked, R-0988 registered, DECISION F273 D12 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r12-block.md` | +116 / -0 | Byte copy of the block |
| `.agent/authored/f273-r12-decisions.md` | +41 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r12-ledger.md` | +14 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r12-plan.md` | +28 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +41 / -0 | `4c375fc4` bytes + decisions.md (DECISION F273 D12) |
| `.agent/live_review.md` | +14 / -0 | `4c375fc4` bytes + ledger.md (Gate F273 R11, five `Done:` lines, R-0988) |
| `.agent/plan.md` | +7 / -9 | := plan.md |

261 insertions, 9 deletions (`git show --numstat`).

### bb31b060 F273 R12 C2: R-0921, R-0917, R-0922 — a test run accepts the intent id an apply prints, the apply names its verifying test run, and do run --yes is driven through the parser
All by `git apply .remedy-wt/f273-proto-g2a.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/patch.py` | +9 / -2 | `patch apply` prints `Next: <test run>` and carries `next_safe_action` |
| `packages/orchestration/patch_apply.py` | +14 / -0 | `verifying_test_run_action` |
| `packages/orchestration/test_execution_service.py` | +7 / -6 | Linkage gate resolves the intent via `_find_artifact_for_intent` |
| `tests/cli/test_plan_approval.py` | +32 / -0 | `test_do_run_yes_through_the_parser_reaches_the_auto_approval` |
| `tests/orchestration/test_test_execution_service.py` | +44 / -3 | Intent-linkage pass and refusal tests |
| `tests/test_patch_apply.py` | +28 / -0 | `test_apply_prints_the_test_run_that_carries_the_apply_records_ids` |

134 insertions, 11 deletions.

### c29ecda7 F273 R12 C3: R-0899, R-0910, R-0980, R-0978, R-0988 — the smoke script and its tests read what the product writes, and the study tests reach no model host and no longer depend on order
All by `git apply .remedy-wt/f273-proto-g2b.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `scripts/remedy_smoke.sh` | +3 / -28 | Job check reads `status`; section 12s dropped |
| `tests/cli/test_do_sequence_cli.py` | +5 / -0 | Fixture imports `study` first and patches its binding |
| `tests/cli/test_study_cmd.py` | +43 / -15 | Loopback hang-up listener as model host; timeout 90 -> 30 |
| `tests/test_remedy_smoke_script.py` | +96 / -1 | Sections 0, 3 and 12s tests; direct run in `tmp_path` |

147 insertions, 44 deletions.

### C4 (this commit) F273 R12 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 261.

## External actions

- `git worktree add --detach .remedy-wt/f273-r12-g5wt c29ecda7` for G5 (exit 0), then `git worktree remove --force .remedy-wt/f273-r12-g5wt` (exit 0). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                       c29ecda7 [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g3  d0de8adc (detached HEAD)
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g4  dd23fe6d (detached HEAD)
  ```
  The two `f273-h-*` worktrees belong to research helpers; this round did not touch them.
- After C4: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C3 `c29ecda7` with a clean tree. Every script ran with `cwd` set explicitly and printed its exit code.

- **Transport**, before any write: `sha256sum` of the three payloads, the block and the two diffs matched the block's digests (block.md `b5dd048980559468328708dbd694c8beee5477d7cdb73f994b1853bbe55ee770`).
- **G1**: `python3 .remedy-wt/f273-r12/wk_g1.py`, exit=0:
  ```
  digest plan.md True
  digest ledger.md True
  digest decisions.md True
  digest block.md True
  digest f273-proto-g2a.diff True
  digest f273-proto-g2b.diff True
  plan.md == payload True
  live_review.md == base + ledger True
  decisions.md == base + decisions True
  authored f273-r12-block.md True
  authored f273-r12-plan.md True
  authored f273-r12-ledger.md True
  authored f273-r12-decisions.md True
  C2 paths == g2a numstat True
  C3 paths == g2b numstat True
  ALL True 15
  exit 0
  ```
- **G2**: `git rev-parse c29ecda7:tests c29ecda7:packages c29ecda7:apps c29ecda7:scripts`, exit=0:
  ```
  da037036e587716f4813ee3b76d69d8227c971e9
  f7955a17f3b74dacbd4f4fb4441dd6e0b638d856
  9c53d5b923b407e3cfaa6e26d221905fee69f8ed
  1168aa2c8ca6d3e27b40d1f123d2131a3bfad6c6
  ```
  All four equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial, the block's 20 target files): `python3 .remedy-wt/f273-r12/wk_g3g4.py g3` runs `python3 -m pytest -q -p no:cacheprovider <the 20 files>`, prints the summary line and counts the `R-0803:` lines over the full output. Exit=0:
  ```
  941 passed in 208.36s (0:03:28)
  R-0803 lines: 0
  status porcelain after: ''
  exit 0
  ```
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root (via `wk_g3g4.py g4`), exit=0:
  ```
  All checks passed!
  ```
- **G5** (`python3 .remedy-wt/f273-r12/wk_g5.py`):
  - Setup: one detached worktree at `c29ecda7`, with `python3 -B -m pytest -q -p no:cacheprovider` run from its root.
  - Environment: the env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`.
  - `__pycache__` was purged before every run.
  - Each FROM line was counted with its newline in the named file first, and each file was reverted from its saved bytes.
  ```
  import path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r12-g5wt/packages/orchestration/patch_apply.py
  inside worktree: True
  control (6 files): 439 passed in 30.14s  exit 0
  (a) test_execution_service.py FROM count=1 -> 1 failed, 66 passed  exit 1
      FAILED tests/orchestration/test_test_execution_service.py::TestExecuteTestRunGates::test_an_intent_id_the_job_carries_passes_the_linkage_gate
  (b) patch_apply.py FROM count=1 -> 1 failed, 124 passed  exit 1
      FAILED tests/test_patch_apply.py::TestCLI::test_apply_prints_the_test_run_that_carries_the_apply_records_ids
  (c) do_cmd.py FROM count=1 -> 1 failed, 30 passed  exit 1
      FAILED tests/cli/test_plan_approval.py::TestAutoApproval::test_do_run_yes_through_the_parser_reaches_the_auto_approval[flags1-approved]
  (d) remedy_smoke.sh status->state FROM count=1 -> 1 failed, 160 passed  exit 1
      FAILED tests/test_remedy_smoke_script.py::TestSectionThreeReadsJobShow::test_the_job_check_passes_on_the_job_show_output_of_a_created_job
  (e) remedy_smoke.sh 12s comment FROM count=1 -> 1 failed, 160 passed  exit 1
      FAILED tests/test_remedy_smoke_script.py::TestSectionTwelveSIsDropped::test_no_section_requires_the_token_policy_applied_event
  (f) remedy_smoke.sh grp loop + policy FROM count=1 -> 1 failed, 160 passed  exit 1
      FAILED tests/test_remedy_smoke_script.py::TestSectionZeroGroupsAreCatalogGroups::test_every_word_section_zero_runs_is_a_catalog_group
  (g) test_study_cmd.py host :9 FROM count=1 -> 1 failed, 11 passed  exit 1
      FAILED tests/cli/test_study_cmd.py::TestStudyCommandReachability::test_study_run_dispatch_e2e
  (h) test_do_sequence_cli.py import deleted FROM count=1 -> (do_sequence then study) 6 failed, 49 passed  exit 1
      FAILED tests/cli/test_study_cmd.py::TestStudyRunWritesCards::test_study_run_writes_cards_for_a_fixture_repo
      FAILED tests/cli/test_study_cmd.py::TestStudyRunWritesCards::test_study_run_defaults_path_to_cwd
      FAILED tests/cli/test_study_cmd.py::TestStudyRunWritesCards::test_study_run_resolves_same_project_as_teacher_ask_via_registered_project
      FAILED tests/cli/test_study_cmd.py::TestStudyRunWritesCards::test_study_run_warns_and_falls_back_when_no_project_registered
      FAILED tests/cli/test_study_cmd.py::TestStudyRunRecordsStudyOnce::test_a_registered_project_gets_studied_at_and_studied_head
      FAILED tests/cli/test_study_cmd.py::TestStudyRunRecordsStudyOnce::test_an_unscoped_study_writes_no_project_record
  (i) test_remedy_smoke_script.py cwd removed FROM count=1 -> 1 failed, 160 passed  exit 1
      FAILED tests/test_remedy_smoke_script.py::TestSmokeScriptExecution::test_direct_run_calls_remedy_smoke
  every revert: bytes restored True; worktree status after reverts: ''
  ```
  The control ran over the six named test files together. Every mutation went red; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r12/wk_c1.py` from `git show 4c375fc4:<path>` bytes and the payload bytes. Nothing was hand-edited except this handoff. G1 re-proves every C1 file and every `.agent/authored/f273-r12-*` copy against its payload.
- The code arrived only by `git apply` of the two reviewer-verified diffs, in the block's order. G2's object ids equal the reviewer's dry-run objects.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `122dbc60` |
| C2 R-0921, R-0917, R-0922 | done | `bb31b060` |
| C3 R-0899, R-0910, R-0980, R-0978, R-0988 | done | `c29ecda7` |
| C4 handoff + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r12/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registered in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `122dbc60` (C1 onwards; C2 and C3 do not touch it): **79 open**;
- at `4c375fc4`: 83 open.

C1's five `Done:` lines close five distinct ids (R-0974, R-0913, R-0890, R-0898, R-0935), and it registers one (R-0988): 83 - 5 + 1 = 79. The eight ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C4, then the push. No extra commit.
- **G3 transcript:** `wk_g3g4.py` printed only the lines containing `passed`, `failed` or `error`, plus a count of `R-0803:` lines taken over the full captured output. The summary line and the 0 count are both from that run.
- **G5 worktree removal:** `git worktree remove --force` was used, because mutation (i) makes the smoke script write its log under the worktree's own `.data/smoke/`. That is the behaviour the mutation restores. The worktree was disposable, and its tracked state was clean after the reverts.
- **Payload copies:** the four files listed under PAYLOADS (plan, ledger, decisions, block) went to `.agent/authored/`, as in rounds 2 to 11. The two code diffs are not copied.
- **Scratch:** gitignored under `.remedy-wt/f273-r12/`: `wk_c1.py`, `wk_g1.py`, `wk_g3g4.py`, `wk_g5.py`, `wk_count.py`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 12.

Operator questions open: 5
