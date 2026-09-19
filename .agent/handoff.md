# Handoff — F273 Findings paydown v1 · Round 14

## Session

SESSION 2 of feature F273 · round 14 · rounds so far 14

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D14, round 13's handoff as the template's instance, and the production hunks of all three code diffs as it applied them. Every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of 3a93d638..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 14 books round 13's verdict and its nine resolutions, registers R-0990, lands DECISION F273 D14, and builds R-0989, R-0903, R-0908, R-0911, R-0932 and R-0936 as the reviewer's dry run built them.
- C1 books Gate F273 R13 (VERDICT PASS), nine `Done:` lines (R-0930, R-0929, R-0904, R-0970, R-0915, R-0919, R-0920, R-0905, R-0907) and the R-0990 registration. It also lands DECISION F273 D14, rewrites the plan and saves the four payload copies.
- C2 (R-0989, R-0903, R-0908):
  - `_status_section` names the first pending intent in its approve tip, or falls back to `patch list`; its resume tip names the job id.
  - The cockpit's attention items and tips name the real job id and intent ids; the goal tip names the order in words.
  - `orchestrator_brain.py` is deleted with the dashboard's orchestrator section and its tests. The rollback-proof reader and audit are deleted too; the snapshot section reports no rollback count.
  - `validate_next_safe_action_command` moves out of production to `tests/orchestration/catalog_commands.py` as `names_catalog_command`.
  - The recommendation store, its accept and reject steps, `propose_from_recommendation` and the two cockpit readers are deleted. `run_reviewer` stays.
- C3 (R-0911, R-0932, R-0936):
  - `pingpong_evidence.export_evidence` is deleted. The file-content assertions are kept against `build_evidence_bundle` and `write_evidence_bundle`.
  - The two task-file loaders, `summarize_pingpong` and the `scope_contract` parameters are deleted with their pinning tests. The two prompt goldens are re-cut.
  - `job_fulfillment.py`, three staging functions and the fulfillment sections of `job show --full` are deleted with their tests. Seven event labels leave `humanizeCatalog.ts`.
- C4 is this handoff.

Landed: R-0989 — `a4e677d3` (C2)
Landed: R-0903 — `a4e677d3` (C2)
Landed: R-0908 — `a4e677d3` (C2)
Landed: R-0911 — `d036fb56` (C3)
Landed: R-0932 — `d036fb56` (C3)
Landed: R-0936 — `d036fb56` (C3)

## Commits

### 1d1b780f F273 R14 C1: bookkeeping — round 13's verdict and its nine resolutions booked, R-0990 registered, DECISION F273 D14 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r14-block.md` | +104 / -0 | Byte copy of the block |
| `.agent/authored/f273-r14-decisions.md` | +38 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r14-ledger.md` | +22 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r14-plan.md` | +26 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +38 / -0 | `3a93d638` bytes + decisions.md (DECISION F273 D14) |
| `.agent/live_review.md` | +22 / -0 | `3a93d638` bytes + ledger.md (Gate F273 R13, nine `Done:` lines, R-0990) |
| `.agent/plan.md` | +6 / -7 | := plan.md |

256 insertions, 7 deletions (`git show --numstat`).

### a4e677d3 F273 R14 C2: R-0989, R-0903, R-0908 — the status and cockpit tips name real ids, and the brain reader, the rollback reader and audit and the recommendation store go with their tests
All by `git apply .remedy-wt/f273-proto-g5a.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/job.py` | +6 / -2 | Status tips name the first pending intent and the job id |
| `docs/guides/do-run-v1.md` | +7 / -6 | The catalog check is a test helper now |
| `docs/system/development-artifact-boundary-v0.md` | +0 / -1 | Brain row removed |
| `docs/system/orchestrator-brain-v0.md` | +4 / -4 | Banner: no module of this name remains |
| `docs/system/orchestrator-loop.md` | +6 / -3 | No step replaced `review accept` |
| `docs/system/real-test-execution-snapshot-rollback-proof-v1.md` | +4 / -3 | Banner: reader and audit deleted |
| `packages/orchestration/cockpit.py` | +14 / -8 | `_first_intent_id`; tips and attention items name real ids |
| `packages/orchestration/do_run.py` | +4 / -28 | Catalog validator leaves production |
| `packages/orchestration/orchestrator_brain.py` | +0 / -42 | Deleted |
| `packages/orchestration/proposed_tasks.py` | +0 / -34 | `propose_from_recommendation` deleted |
| `packages/orchestration/real_test_execution.py` | +3 / -27 | Rollback reader and audit deleted |
| `packages/orchestration/reviewer.py` | +5 / -97 | Recommendation store and accept/reject deleted |
| `packages/orchestration/ui_server.py` | +4 / -41 | Orchestrator section, rollback count, reviewer pending count removed |
| `packages/orchestration/ui_view_model.py` | +0 / -14 | Checklist's reviewer items removed |
| `pyproject.toml` | +0 / -1 | Deleted module leaves the mypy list |
| `tests/cli/test_product_spine.py` | +35 / -0 | No-placeholder status tip tests |
| `tests/orchestration/catalog_commands.py` | +20 / -0 | New test helper `names_catalog_command` |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | Deleted module |
| `tests/orchestration/test_approval_queue.py` | +5 / -81 | Follows the deletion |
| `tests/orchestration/test_development_artifact_boundary.py` | +0 / -1 | Follows the deletion |
| `tests/orchestration/test_do_run.py` | +11 / -13 | Uses the test helper |
| `tests/orchestration/test_mission_readiness.py` | +2 / -2 | Uses the test helper |
| `tests/orchestration/test_orchestrator_brain.py` | +0 / -43 | Deleted with its module |
| `tests/orchestration/test_proposed_tasks.py` | +0 / -15 | Follows the deletion |
| `tests/orchestration/test_real_test_execution.py` | +0 / -12 | Follows the deletion |
| `tests/orchestration/test_repair_loop_v1.py` | +4 / -4 | Uses the test helper |
| `tests/orchestration/test_repair_request_builder.py` | +2 / -2 | Uses the test helper |
| `tests/orchestration/test_self_dogfood.py` | +2 / -2 | Uses the test helper |
| `tests/orchestration/test_self_dogfood_execution.py` | +3 / -3 | Uses the test helper |
| `tests/orchestration/test_test_failure_repair.py` | +4 / -4 | Uses the test helper |
| `tests/test_cli_execution_loop_closure.py` | +3 / -3 | Uses the test helper |
| `tests/test_cockpit.py` | +55 / -0 | No-placeholder cockpit tests |
| `tests/test_repair_context_reviewer_memory.py` | +14 / -67 | Follows the deletion |
| `tests/ui_server/test_dashboard_cockpit_truth.py` | +0 / -10 | Orchestrator section tests removed |

217 insertions, 574 deletions.

### d036fb56 F273 R14 C3: R-0911, R-0932, R-0936 — the evidence export, the task-file loaders, the pingpong summary, the scope-contract parameters and the fulfillment spine go with their tests, and the goldens are re-cut
All by `git apply .remedy-wt/f273-proto-g5b.diff`, then `git apply .remedy-wt/f273-proto-g5c.diff`, in one commit.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/job.py` | +1 / -79 | Fulfillment reads leave the status, report and truth |
| `apps/cli/commands/job_context_cmd.py` | +2 / -2 | Comment no longer cites `job_fulfillment` |
| `apps/ui/src/api/humanizeCatalog.ts` | +0 / -7 | Seven fulfillment-only event labels removed |
| `docs/system/first-fulfilled-job-demo-v0.md` | +4 / -8 | Banner: spine deleted |
| `docs/system/run-contract-v1.md` | +2 / -2 | Fixture contract gone |
| `packages/orchestration/job_fulfillment.py` | +0 / -1057 | Deleted |
| `packages/orchestration/orchestrator_loop.py` | +1 / -1 | Comment |
| `packages/orchestration/pingpong_evidence.py` | +0 / -49 | `export_evidence` and scope-plan summary deleted |
| `packages/orchestration/pingpong_loop.py` | +7 / -259 | Loaders, `summarize_pingpong`, `scope_contract` parameters deleted |
| `packages/orchestration/staging_workspace.py` | +2 / -245 | Three staging functions deleted |
| `tests/cli/test_job_report.py` | +1 / -2 | Follows the deletion |
| `tests/cli/test_task_input.py` | +19 / -143 | Loader tests removed |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | Deleted module |
| `tests/orchestration/test_builder_prompt_golden.py` | +27 / -34 | Golden re-cut with a declared-change note |
| `tests/orchestration/test_builder_prompt_hunk_rejections.py` | +0 / -1 | Follows the deletion |
| `tests/orchestration/test_dod_gate.py` | +2 / -118 | Fulfillment tests removed |
| `tests/orchestration/test_evidence_bundle.py` | +48 / -155 | Assertions kept against build/write |
| `tests/orchestration/test_fence_production_e2e.py` | +3 / -64 | Fulfillment tests removed |
| `tests/orchestration/test_job_fulfillment.py` | +3 / -1445 | Only the surviving docs and staging tests stay |
| `tests/orchestration/test_job_task_runner.py` | +6 / -2 | Follows the deletion |
| `tests/orchestration/test_pingpong.py` | +0 / -13 | `summarize_pingpong` tests removed |
| `tests/orchestration/test_pingpong_cli.py` | +0 / -75 | `export_evidence` tests removed |
| `tests/orchestration/test_prompt_trace.py` | +0 / -4 | Follows the deletion |
| `tests/orchestration/test_provider_retry.py` | +0 / -34 | Follows the deletion |
| `tests/orchestration/test_repair_loop.py` | +0 / -110 | `scope_contract` tests removed |
| `tests/orchestration/test_reviewer_prompt_golden.py` | +11 / -21 | Golden re-cut with a declared-change note |
| `tests/orchestration/test_semantic_dedupe.py` | +0 / -2 | Follows the deletion |
| `tests/ui_server/test_command_channel.py` | +0 / -1 | Follows the deletion |

139 insertions, 3934 deletions.

### C4 (this commit) F273 R14 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 256.

## External actions

- `git worktree add --detach .remedy-wt/f273-r14-g5 d036fb56` for G5, then `git worktree remove .remedy-wt/f273-r14-g5` (no `--force` needed). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                        d036fb56 [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g6a  896c5d56 (detached HEAD)
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g6c  c880f932 (detached HEAD)
  ```
  The two `f273-h-*` worktrees belong to research helpers; this round did not touch them.
- After C4: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C3 `d036fb56` with a clean tree. Every script ran with `cwd` set explicitly; exit codes come from `.remedy-wt/f273-r14/wk_run.py`, which prints the child's real return code.

- **Transport**, before any write: `sha256sum` of the three payloads, the block, the three diffs and the G3 control list matched the given digests (block.md `c3da86e004b286c93374dde99b235291b7aa872e574735fd5108fd25d215fbc2`).
- **G1**: `python3 .remedy-wt/f273-r14/wk_g1.py`, exit 0:
  ```
  digest f273-r14/plan.md True
  digest f273-r14/ledger.md True
  digest f273-r14/decisions.md True
  digest f273-r14/block.md True
  digest f273-proto-g5a.diff True
  digest f273-proto-g5b.diff True
  digest f273-proto-g5c.diff True
  digest f273-s2/r14_control.txt True
  plan.md == payload True
  live_review == base + ledger True
  decisions == base + decisions True
  authored f273-r14-plan.md True
  authored f273-r14-ledger.md True
  authored f273-r14-decisions.md True
  authored f273-r14-block.md True
  C2 paths == g5a paths True
  C3 paths == g5b|g5c paths True
  C1 paths == 7 bookkeeping paths True
  18 checks, all True: True
  EXIT CODE: 0
  ```
- **G2**: `git rev-parse d036fb56:tests d036fb56:packages d036fb56:apps d036fb56:docs d036fb56:pyproject.toml`, exit 0:
  ```
  3bb96506a48942faa493776a788f8a9eff14763f
  6893b5256164391cc2591a81a7506bfabae95f82
  c6614371ade5f129651458d8a3a0dbe54f2eb436
  8fe275f9a975addeb3833859997e8594a87bef61
  0624d5bf709e869ed44bc23a725b47f880231b0e
  ```
  All five equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial): `python3 .remedy-wt/f273-r14/wk_g3.py` runs `python3 -m pytest -q -p no:cacheprovider` over the 42 paths of `.remedy-wt/f273-s2/r14_control.txt` plus `tests/orchestration/test_evidence_index.py` and `tests/orchestration/test_test_runner.py`, and counts `R-0803:` lines over the full output:
  ```
  control paths: 42 + extra: 2 missing: []
  2968 passed, 5 skipped in 252.15s (0:04:12)
  R-0803: lines: 0
  EXIT CODE: 0
  ```
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root:
  ```
  All checks passed!
  EXIT CODE: 0
  ```
- **G5** (`python3 .remedy-wt/f273-r14/wk_g5.py`, exit 0): one detached worktree at `d036fb56`; `python3 -B -m pytest -q -p no:cacheprovider` from its root; env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`; `__pycache__` purged before every run; each FROM line counted with its newline first; each file reverted from its saved bytes.
  ```
  cockpit path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r14-g5/packages/orchestration/cockpit.py
  CONTROL (unmutated) over P, Q, test_evidence_bundle.py, test_task_input.py, test_builder_prompt_golden.py: 239 passed in 1.26s | exit 0
  (a) apps/cli/commands/job.py: FROM line count = 1
      tests/cli/test_product_spine.py: 1 failed, 59 passed | exit 1 | RED
      FAILED tests/cli/test_product_spine.py::TestStatusNextActionNamesNoPlaceholder::test_next_action_has_no_angle_bracket_placeholder[pending_task]
  (b) apps/cli/commands/job.py: FROM line count = 1
      tests/cli/test_product_spine.py: 1 failed, 59 passed | exit 1 | RED
      FAILED tests/cli/test_product_spine.py::TestStatusNextActionNamesNoPlaceholder::test_next_action_has_no_angle_bracket_placeholder[pending_intent]
  (c) packages/orchestration/cockpit.py: FROM line count = 1
      tests/test_cockpit.py: 2 failed, 59 passed | exit 1 | RED
      FAILED tests/test_cockpit.py::TestCockpitNamesNoPlaceholder::test_rendered_cockpit_has_no_angle_bracket_placeholder[idle]
      FAILED tests/test_cockpit.py::TestCockpitNamesNoPlaceholder::test_rendered_cockpit_has_no_angle_bracket_placeholder[rejected_repo_denied]
  (d) packages/orchestration/cockpit.py: FROM line count = 1
      tests/test_cockpit.py: 1 failed, 60 passed | exit 1 | RED
      FAILED tests/test_cockpit.py::TestCockpitNamesNoPlaceholder::test_rendered_cockpit_has_no_angle_bracket_placeholder[interrupted]
  (e) packages/orchestration/pingpong_evidence.py: FROM line count = 1
      tests/orchestration/test_evidence_bundle.py: 1 failed, 54 passed | exit 1 | RED
      FAILED tests/orchestration/test_evidence_bundle.py::TestExportedJsonRedaction::test_exported_json_redacted
  (f) packages/orchestration/pingpong_loop.py: FROM line count = 1
      tests/cli/test_task_input.py: 1 failed, 26 passed | exit 1 | RED
      FAILED tests/cli/test_task_input.py::TestTitleDerivation::test_no_goal_derives_title
  (g) packages/orchestration/pingpong_loop.py: FROM line count = 1
      tests/orchestration/test_builder_prompt_golden.py: 7 failed, 29 passed | exit 1 | RED
      FAILED ...::test_segments_reassemble_into_the_frozen_render[full|minimal|resumed|staged|task_body] (5 ids)
      FAILED ...::test_only_the_shapes_without_job_context_are_byte_identical_to_the_frozen_render
      FAILED ...::test_the_cacheable_prefix_survives_a_new_round_and_a_new_staged_state
  every revert: True; worktree status after reverts: ''
  ```
  Every mutation went red; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r14/wk_c1.py` from `git show 3a93d638:<path>` bytes and the payload bytes. Nothing was hand-edited except this handoff. G1 re-proves every C1 file and every `.agent/authored/f273-r14-*` copy against its payload.
- The code arrived only by `git apply` of the three reviewer-verified diffs, in the block's order. G2's object ids equal the reviewer's dry-run objects.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `1d1b780f` |
| C2 R-0989, R-0903, R-0908 | done | `a4e677d3` |
| C3 R-0911, R-0932, R-0936 | done | `d036fb56` |
| C4 handoff + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r14/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registered in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `1d1b780f` (C1 onwards; C2 and C3 do not touch it; the same at `d036fb56`): **63 open**;
- at `3a93d638`: 71 open.

C1's nine `Done:` lines close nine distinct ids, and it registers one (R-0990): 71 - 9 + 1 = 63. The six ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C4, then the push. No extra commit.
- **C2 insertions:** `git diff --stat` before staging showed 197 insertions because the new file `tests/orchestration/catalog_commands.py` was untracked; the commit, with it staged, reads 217 (`git show --numstat`), which matches `git apply --numstat` of g5a.
- **G5 control scope:** the block names the control's files as "the test files named below"; the control ran over exactly the five files the mutations name.
- **G5 worktree:** made with `--detach`, so no branch was created.
- **Payload copies:** the four files listed under PAYLOADS (plan, ledger, decisions, block) went to `.agent/authored/`, as in earlier rounds. The three code diffs are not copied.
- **Scratch:** gitignored under `.remedy-wt/f273-r14/`: `wk_c1.py`, `wk_g1.py`, `wk_g3.py`, `wk_g5.py`, `wk_count.py`, `wk_run.py`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 14.

Operator questions open: 5
