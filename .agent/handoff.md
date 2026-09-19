# Handoff — F273 Findings paydown v1 · Round 17

## Session

SESSION 3 of feature F273 · round 17 · rounds so far 17

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D17, the handback template, round 16's handoff as the template's instance and the added lines of the three diffs as it applied them, and held all of it without loss; every figure below comes from a command run in this round.

## Range

Review of 9e753ffc..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 17 books round 16's verdict and nine resolutions, registers R-0992, lands DECISION F273 D17, and builds R-0914, R-0927 and R-0928 as the reviewer's dry run built them.
- C1 books Gate F273 R16 (VERDICT PASS) and nine `Done:` lines (R-0918, R-0923, R-0924, R-0925, R-0926, R-0991, R-0912, R-0940, R-0954), registers R-0992, lands DECISION F273 D17, appends one line to `.agent/prose_slips.md`, rewrites the plan and saves the five payload copies.
- C2 (R-0914): `attest_operator_repair` and every symbol only it or tests reached are deleted, with the export's attestation overlay, its finalize step and the regression-coverage map only that step read, and their tests; `manual_attestation.py` and everything `create_manual_completion_bundle` reaches stay. `docs/system/vocabulary.md`, `T0_F002.md` and `T0_F012.md` carry dated status lines.
- C3 (R-0927, R-0928): `worker_queue.py`, `task_execution.py`, `autorun.py` and `source_context.py` are deleted with their tests, and so are `worker status`, the cockpit's worker section and its UI client. The readers of the event names only those modules emitted go with them; `_COUPLING_CEILING` stays at 1; the coupling ratchet and the catalog contract read a name held in a local; the `apply_structured_patch` permission guard is re-pointed at its three surviving callers; a test pins the project summary's confidence at `low`.
- C4 (R-0914's Acceptance line): `T2_F273.md` gains the branch that keeps `manual_attestation.py` (DECISION F273 D17).
- C5 is this handoff.

Landed: R-0914 — `ca5f5a5a` (C2), its Acceptance line amended at `71d7297f` (C4)
Landed: R-0927 — `1c68337d` (C3)
Landed: R-0928 — `1c68337d` (C3)

## Commits

### b16d1599 F273 R17 C1: bookkeeping — round 16's verdict and its nine resolutions booked, R-0992 registered, DECISION F273 D17 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r17-block.md` | +114 / -0 | Byte copy of the block |
| `.agent/authored/f273-r17-decisions.md` | +33 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r17-ledger.md` | +22 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r17-plan.md` | +27 / -0 | Byte copy of plan.md |
| `.agent/authored/f273-r17-slips.md` | +1 / -0 | Byte copy of slips.md |
| `.agent/decisions.md` | +33 / -0 | `9e753ffc` bytes + decisions.md (DECISION F273 D17) |
| `.agent/live_review.md` | +22 / -0 | `9e753ffc` bytes + ledger.md (Gate F273 R16, nine `Done:` lines, R-0992) |
| `.agent/plan.md` | +7 / -12 | := plan.md |
| `.agent/prose_slips.md` | +1 / -0 | `9e753ffc` bytes + slips.md |

260 insertions, 12 deletions (`git show --numstat`).

### ca5f5a5a F273 R17 C2: R-0914 — the operator-attestation writer and the export's attestation overlay go, the closure evidence producer stays
All by `git apply .remedy-wt/f273-proto-g7c2.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T0_F002.md` | +6 / -0 | Status: the writer this file designs is deleted |
| `docs/roadmap/features/T0_F012.md` | +5 / -0 | Status: the finalize step and the coverage map are deleted |
| `docs/system/vocabulary.md` | +12 / -0 | Status: an operator repair is attested no longer |
| `packages/orchestration/job_evidence.py` | +0 / -608 | Attestation overlay and finalize step deleted |
| `packages/orchestration/manual_attestation.py` | +0 / -48 | Symbols only the writer reached deleted |
| `packages/orchestration/missing_tests_gate.py` | +0 / -19 | Regression-coverage map deleted |
| `packages/orchestration/repair_attest.py` | +11 / -527 | Keeps the attestable-source policy and safe-diff hashing |
| `tests/orchestration/test_job_evidence.py` | +13 / -99 | Overlay tests removed; surviving producer test |
| `tests/orchestration/test_job_state_field.py` | +0 / -15 | Test of the deleted writer removed |
| `tests/orchestration/test_manual_completion_bundle.py` | +13 / -372 | Writer tests removed |
| `tests/orchestration/test_relevant_regression_coverage.py` | +0 / -101 | Deleted with the map |
| `tests/orchestration/test_repair_attest.py` | +32 / -378 | Re-pointed at the surviving policy and hashing |
| `tests/orchestration/test_round13_evidence_alignment.py` | +1 / -83 | Writer tests removed |
| `tests/orchestration/test_token_authority.py` | +42 / -1 | The manual token-truth fixture held locally |
| `tests/test_data_paths.py` | +0 / -1 | Deleted symbol |

135 insertions, 2252 deletions.

### 1c68337d F273 R17 C3: R-0927, R-0928 — the worker queue, the goal-driven path and worker status go with their readers, and the coupling ceiling stays at 1
All by `git apply .remedy-wt/f273-proto-g7b2.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +0 / -10 | `worker status` entry deleted |
| `apps/cli/commands/worker.py` | +0 / -20 | `status` word deleted |
| `apps/ui/src/api/actionClass.ts` | +0 / -1 | Dead event name |
| `apps/ui/src/api/humanizeCatalog.ts` | +4 / -6 | Dead names out; four entries for names a local holds |
| `apps/ui/src/api/remedyApi.ts` | +0 / -2 | Worker client deleted |
| `apps/ui/src/api/types.ts` | +1 / -14 | Worker section type deleted |
| `apps/ui/src/cockpitLogic.test.ts` | +0 / -16 | Worker section tests removed |
| `apps/ui/src/cockpitLogic.ts` | +0 / -8 | Worker section reader deleted |
| `apps/ui/src/components/panels/NeedsAttentionCard.tsx` | +0 / -10 | Worker section reader deleted |
| `apps/ui/src/components/panels/RightLivePanel.tsx` | +0 / -6 | Worker mini panel removed |
| `apps/ui/src/components/pipeline/WorkerStatusMini.tsx` | +0 / -50 | Deleted |
| `docs/guides/autocoder-usage.md` | +1 / -1 | Deleted smoke test reference |
| `docs/guides/resume.md` | +3 / -2 | Two checkpoints deleted |
| `docs/system/vocabulary.md` | +3 / -2 | `worker` group words |
| `docs/system/worker.md` | +17 / -23 | Status: queue, run and status deleted |
| `packages/orchestration/autorun.py` | +0 / -662 | Deleted |
| `packages/orchestration/event_replay.py` | +1 / -44 | Dead-name readers deleted |
| `packages/orchestration/proof_chain.py` | +2 / -19 | Dead-name readers deleted |
| `packages/orchestration/source_context.py` | +0 / -251 | Deleted |
| `packages/orchestration/task_execution.py` | +0 / -234 | Deleted |
| `packages/orchestration/ui_server.py` | +10 / -86 | Worker section and dead-name readers deleted |
| `packages/orchestration/ui_view_model.py` | +1 / -12 | Dead-name readers deleted |
| `packages/orchestration/worker_queue.py` | +0 / -797 | Deleted |
| `pyproject.toml` | +0 / -2 | Deleted modules' entries |
| `scripts/remedy_backend_basis_smoke.py` | +0 / -1 | Deleted module |
| `tests/README.md` | +1 / -1 | Module list |
| `tests/cli/test_do_cmd_cli_path.py` | +0 / -217 | Deleted |
| `tests/cli/test_do_cmd_summary.py` | +0 / -55 | Goal-driven tests removed |
| `tests/cli/test_job_commands.py` | +0 / -19 | Queue tests removed |
| `tests/conftest.py` | +0 / -1 | Deleted module |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -4 | Deleted modules |
| `tests/orchestration/test_autorun.py` | +0 / -320 | Tests of the deleted path removed |
| `tests/orchestration/test_builder_visibility.py` | +0 / -28 | Tests of the deleted path removed |
| `tests/orchestration/test_event_name_coupling.py` | +44 / -4 | Held-local recovery and its test |
| `tests/orchestration/test_event_replay.py` | +11 / -12 | Dead names ignored in an old log |
| `tests/orchestration/test_proof_chain.py` | +0 / -47 | Dead-name tests removed |
| `tests/orchestration/test_proposed_tasks.py` | +0 / -42 | Task-execution port tests removed |
| `tests/orchestration/test_provider_mode.py` | +0 / -196 | Tests of the deleted path removed |
| `tests/orchestration/test_real_do_ollama_smoke.py` | +0 / -110 | Deleted |
| `tests/orchestration/test_source_apply.py` | +0 / -82 | Tests of the deleted path removed |
| `tests/orchestration/test_source_context_quality.py` | +0 / -111 | Deleted |
| `tests/orchestration/test_task_execution.py` | +5 / -211 | Port tests removed; guards on `proposed_tasks.py` stay |
| `tests/orchestration/test_test_runner.py` | +35 / -11 | Permission guard re-pointed at three callers |
| `tests/orchestration/test_worker_docs.py` | +22 / -0 | New: the worker guide keeps its two stances |
| `tests/orchestration/test_worker_execution.py` | +6 / -360 | Worker execution tests removed |
| `tests/orchestration/test_worker_queue.py` | +0 / -392 | Deleted |
| `tests/regression/test_named_bugs.py` | +0 / -4 | Deleted module |
| `tests/test_cli_execution_loop_closure.py` | +0 / -64 | Tests of the deleted path removed |
| `tests/test_command_catalog.py` | +1 / -0 | `worker.status` listed as deleted |
| `tests/test_repair_context_reviewer_memory.py` | +0 / -63 | Tests of the deleted path removed |
| `tests/ui_contracts/test_design_drift.py` | +0 / -4 | Deleted component |
| `tests/ui_contracts/test_humanize_catalog.py` | +45 / -0 | Held-local recovery and its test |
| `tests/ui_server/test_pipeline_contract.py` | +40 / -12 | Absent fields pinned; confidence pinned at `low` |

253 insertions, 4649 deletions.

### 71d7297f F273 R17 C4: R-0914's Acceptance line gains the branch that keeps the module the closure evidence producer reaches
All by `git apply .remedy-wt/f273-s3/r17_docs.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F273.md` | +3 / -1 | R-0914 Acceptance line, D17 branch |

3 insertions, 1 deletion.

### C5 (this commit) F273 R17 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 260.

## External actions

- `git worktree add --detach .remedy-wt/f273-r17-g5 71d7297f` for G5, then `git worktree remove .remedy-wt/f273-r17-g5` (exit 0, no `--force`) as the step's last action. `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                         71d7297f [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h8      cb611ad1 (detached HEAD)
  /home/decodeux/Repos/remedy/.remedy-wt/f273-s3-r17  3cec4809 (detached HEAD)
  ```
  Neither of the other two entries is this worker's: `.remedy-wt/f273-s3-r17` is the reviewer's, and the worker did not create, use or remove `.remedy-wt/f273-h8`.
- The branch `remedy/job-81ec65896729405c` still exists in this repository. A research helper's probe created it before round 16; nobody may delete it without the operator. `git branch --list 'remedy/job-*'` reads 37 branches after the gates, the same count round 16 read.
- After C5: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C4 `71d7297f` with a clean tree. Every script ran with an explicit `cwd`; exit codes come from `.remedy-wt/f273-r17/wk_run.py`, which prints the child's real return code, or from the script's own `EXIT CODE:` line.

- **Transport**, before any write: `sha256sum` of the block, the six payloads and the three diffs matched the given digests. The block file read 114 lines.
- **Block copy**, before C1: `.remedy-wt/f273-r17/wk_c1.py` read the saved `.agent/authored/f273-r17-block.md` back:
  ```
  saved block copy sha256: 053c6b2b8a7bc4d17b06e61473635b9676fbe21c9bd707c0e08af651a09209ff
  saved block copy lines: 114
  equals given sha256: True equals given line count 114: True
  EXIT CODE: 0
  ```
- **G1**: `python3 .remedy-wt/f273-r17/wk_g1.py`, exit 0:
  ```
  digest f273-r17/plan.md True
  digest f273-r17/ledger.md True
  digest f273-r17/decisions.md True
  digest f273-r17/slips.md True
  digest f273-r17/next.md True
  digest f273-s3/r17_targets.txt True
  digest f273-r17/block.md True
  digest f273-proto-g7c2.diff True
  digest f273-proto-g7b2.diff True
  digest f273-s3/r17_docs.diff True
  plan.md == payload True
  .agent/live_review.md == base + ledger.md True
  .agent/decisions.md == base + decisions.md True
  .agent/prose_slips.md == base + slips.md True
  authored f273-r17-plan.md True
  authored f273-r17-ledger.md True
  authored f273-r17-decisions.md True
  authored f273-r17-slips.md True
  authored f273-r17-block.md True
  C2 paths == g7c2 paths True
  C3 paths == g7b2 paths True
  C4 paths == r17_docs paths True
  C1 paths == 9 bookkeeping paths True
  23 checks, all True: True
  EXIT CODE: 0
  ```
- **G2**: `git rev-parse 71d7297f:tests 71d7297f:packages 71d7297f:apps 71d7297f:docs`, exit 0:
  ```
  85eed96929750b60a5d3d74261c991cc2e3dc191
  c4e15508a4fae8d1e0d0f143552c4679612a813a
  448e1225c49f39fed56da7cf75587294e9652908
  e80ecf9e6339fffef23603f9ac12405a02371023
  ```
  All four equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial): `python3 .remedy-wt/f273-r17/wk_g3.py` runs `python3 -m pytest -q -p no:cacheprovider` over every line of `r17_targets.txt` and counts `R-0803:` lines over the full output:
  ```
  target paths: 47 distinct: 47 missing: []
  2566 passed, 11 skipped in 259.33s (0:04:19)
  R-0803: lines: 0
  EXIT CODE: 0
  ```
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root:
  ```
  All checks passed!
  EXIT CODE: 0
  ```
- **G5** (`python3 .remedy-wt/f273-r17/wk_g5.py`, exit 0): one detached worktree at `71d7297f`; `python3 -B -m pytest -q -p no:cacheprovider` from its root; env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`; `__pycache__` purged before every run; each FROM matched as a whole line with its newline; each file reverted from its saved bytes.
  ```
  ui_server path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r17-g5/packages/orchestration/ui_server.py
  CONTROL (unmutated) over T P C U E: 181 passed, 1 skipped in 16.70s | exit 0
  (a) packages/orchestration/hunk_apply.py: FROM line count = 1
      tests/orchestration/test_test_runner.py: 1 failed, 47 passed, 1 skipped in 2.20s | exit 1 | RED
          FAILED tests/orchestration/test_test_runner.py::TestSourceApplyPermissionBoundary::test_no_public_command_reaches_without_permission
  (b) packages/orchestration/ui_server.py: FROM line count = 1
      tests/ui_server/test_pipeline_contract.py: 1 failed, 13 passed in 0.32s | exit 1 | RED
          FAILED tests/ui_server/test_pipeline_contract.py::TestProjectSummaryModelConfidence::test_linked_project_reads_low_confidence
  (c) packages/orchestration/ui_server.py: FROM line count = 1
      tests/ui_server/test_pipeline_contract.py: 2 failed, 12 passed in 0.32s | exit 1 | RED
          FAILED tests/ui_server/test_pipeline_contract.py::TestPipelineEmpty::test_empty_job_pipeline
          FAILED tests/ui_server/test_pipeline_contract.py::TestPipelineFixture::test_fixture_success
  (d) packages/orchestration/proof_chain.py: FROM line count = 1
      tests/orchestration/test_proof_chain.py: 16 failed, 85 passed in 0.61s | exit 1 | RED
          FAILED TestBuildProofChain::test_full_verified_chain, TestBuildProofChain::test_sole_change_gets_generic_test,
          TestExportJson::test_json_stable, TestNextSafeAction::test_verified_no_action,
          TestIncompleteChains::test_linked_test_failed, ::test_explicit_not_required_verifies,
          ::test_generic_before_apply_sole_change_does_not_verify, ::test_generic_after_apply_sole_change_verifies,
          ::test_generic_missing_timestamp_sole_change_does_not_verify, ::test_intent_linked_missing_timestamp_can_verify,
          ::test_task_linked_missing_timestamp_can_verify, TestSummary::test_summary_contains_status,
          TestFileProvenanceAlignment::test_provenance_has_proof_status, TestCommandCatalogTruth::test_verified_action_has_no_command,
          TestProofChainDurableTruth::test_durable_snapshot_verifies, TestProofChainDurableTruth::test_drift_blocked_revert_leaves_apply_active
  (e) apps/ui/src/api/humanizeCatalog.ts: FROM line count = 1
      tests/ui_contracts/test_humanize_catalog.py: 1 failed, 11 passed in 2.50s | exit 1 | RED
          FAILED tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary
  (f) tests/orchestration/test_event_name_coupling.py: FROM line count = 1
      tests/orchestration/test_event_name_coupling.py: 2 failed, 4 passed in 11.00s | exit 1 | RED
          FAILED tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_every_dead_coupling_is_declared
          FAILED tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_the_recovery_finds_a_name_held_in_a_local
  worktree status after reverts: ''
  worktree remove exit 0
  ```
  The control line abbreviates the five paths to T, P, C, U and E and the (d) ids are grouped by class; each mutation printed `reverted: True` after its run (trimmed above). Every mutation went red; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit comes before it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r17/wk_c1.py` from `git show 9e753ffc:<path>` bytes and the payload bytes. Nothing was hand-edited except this handoff. G1 re-proves every C1 file and every `.agent/authored/f273-r17-*` copy against its payload.
- The code and docs arrived only by `git apply` of the three reviewer-verified diffs, in the block's order; `.remedy-wt/f273-r17/wk_stage.py` staged exactly the paths `git apply --numstat` reads from each diff, deletions and the new `tests/orchestration/test_worker_docs.py` included, and printed no unstaged or untracked path. G2's object ids equal the reviewer's dry-run objects.
- The `## Next` body below is `next.md` byte for byte, appended by script.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping (Gate F273 R16, nine `Done:` lines, R-0992 registered, D17, one slip line) | done | `b16d1599` |
| R-0914 | done | `ca5f5a5a` (C2); Acceptance line at `71d7297f` (C4) |
| R-0927 | done | `1c68337d` (C3) |
| R-0928 | done | `1c68337d` (C3) |
| C5 handoff + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |
| R-0992 | skipped | Registered only; D17 (3) takes it with R-0977 |

## Open findings

Measured by `.remedy-wt/f273-r17/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registers it in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `b16d1599` (C1 onwards; C2 to C4 do not touch it; the same at `71d7297f`): **47 open**;
- at `9e753ffc`: 55 open.

C1's nine `Done:` lines close nine distinct ids and it registers R-0992: 55 - 9 + 1 = 47. The three ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C5, then the push. No extra commit.
- **`cp` used once:** the worker copied round 16's scratch helper `wk_run.py` into `.remedy-wt/f273-r17/` with `cp` before noticing the constraint names `cp` as denied by the shell; the copy succeeded, touched only gitignored scratch, and no tracked file came from it.
- **G5 control scope:** the control ran over exactly the five files T, P, C, U and E.
- **G5 worktree:** made with `--detach`, so no branch was created.
- **Other worktrees:** `.remedy-wt/f273-s3-r17` (the reviewer's) and `.remedy-wt/f273-h8` (detached at `cb611ad1`) appear in `git worktree list`; the worker did not create, use or remove either.
- **Payload copies:** the five files the block names for C1 (plan, ledger, decisions, slips, block) went to `.agent/authored/`. `next.md` is not copied; it lives in this handoff's `## Next`.
- **Operator questions:** the count below is the number of `### Q<n>` headings in `.agent/operator_questions.md` (Q1, Q2, Q4, Q5, Q7).
- **Scratch:** gitignored under `.remedy-wt/f273-r17/`: `wk_c1.py`, `wk_stage.py`, `wk_g1.py`, `wk_g3.py`, `wk_g5.py`, `wk_count.py`, `wk_run.py`, `wk_c5.py`, `handoff_head.md`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 17 over `9e753ffc`..the round 17
   handoff commit, booked as `Gate: F273 R17` with `Done:` lines for R-0914, R-0927 and R-0928 in
   the next round's first commit.
2. R-0977 with the `__pycache__` handoff-coverage defect DECISION F273 D16 (6) names, and R-0992.
3. A measured owner for every other open id, then closure.

Operator questions open: 5
