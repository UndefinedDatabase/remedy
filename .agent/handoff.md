# Handoff — F280 CLI vocabulary v2, part two
SESSION 5 of feature F280 · round 10 · rounds so far 10

This round booked round 9's independently-reviewed PASS (Gate: F280 R9, no new finding) and landed the first half of DECISION F280 D5's module rename: `flight_plan.py` -> `job_plan.py`, `FlightPlanResult` -> `TaskPlanResult`, and D5's eight named lowercase functions take the `task_plan` spelling. Persisted literals and English-prose nouns unchanged this round.

## Range
Review of `49a43950`..`5100a00a` (commits C0a through C2).

## Commits

### 8b0de034 C0a: F280 R10 C0a: write authored block f280-r10.md (transport carrier)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f280-r10.md` | 158/0 | Block carrier |

### e28f0e84 C0b: F280 R10 C0b: mirror authored block to last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 158/102 | Block carrier mirror |

### 325206a1 C1: F280 R10 C1: append Gate:F280 R9 + R-0940 register, replace plan.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 3304/0 | Append Gate:F280 R9 entry |
| `.agent/plan.md` | 43/47 | Replace with R10 plan |

### 5100a00a C2: F280 R10 C2: apply rename patch (flight_plan -> job_plan, FlightPlanResult -> TaskPlanResult, task_plan spelling)
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/decision.py` | 4/4 | Update task_plan references |
| `apps/cli/commands/do_cmd.py` | 10/10 | Update task_plan references |
| `apps/cli/commands/job.py` | 11/11 | Update task_plan references |
| `apps/cli/commands/job_context_cmd.py` | 3/3 | Update task_plan references |
| `docs/system/vocabulary.md` | 4/4 | Update task_plan references |
| `packages/orchestration/dag_schedule.py` | 1/1 | Update task_plan references |
| `packages/orchestration/decision_inbox.py` | 1/1 | Update task_plan references |
| `packages/orchestration/decision_queue.py` | 1/1 | Update task_plan references |
| `packages/orchestration/dod_compiler.py` | 1/1 | Update task_plan references |
| `packages/orchestration/flight_plan.py => job_plan.py` | 15/15 | Module rename |
| `packages/orchestration/mission_compiler.py` | 2/2 | Update task_plan references |
| `packages/orchestration/orchestrator_loop.py` | 7/7 | Update task_plan references |
| `packages/orchestration/ui_server.py` | 6/6 | Update task_plan references |
| `tests/cli/test_decision_answers.py` | 5/5 | Update task_plan references |
| `tests/cli/test_golden_path.py` | 6/6 | Update task_plan references |
| `tests/cli/test_plan_approval.py` | 23/23 | Update task_plan references |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/1 | Update imports |
| `tests/orchestration/test_bundled_clarification.py` | 1/1 | Update task_plan references |
| `tests/orchestration/test_escalation.py` | 1/1 | Update task_plan references |
| `tests/orchestration/test_flight_plan.py => test_job_plan.py` | 20/20 | Test module rename |
| `tests/orchestration/test_long_run_executor.py` | 1/1 | Update task_plan references |
| `tests/orchestration/test_mission_compiler.py` | 2/2 | Update task_plan references |
| `tests/orchestration/test_plan_prompt_golden.py` | 3/3 | Update task_plan references |
| `tests/orchestration/test_prompt_cache_prefix.py` | 2/2 | Update task_plan references |
| `tests/orchestration/test_prompt_trace.py` | 8/8 | Update task_plan references |
| `tests/schemas/test_flight_plan_schema.py => test_job_plan_schema.py` | 0/0 | Test schema module rename |
| `tests/ui_server/test_command_channel.py` | 4/4 | Update task_plan references |
| `tests/ui_server/test_command_dispatch.py` | 2/2 | Update task_plan references |

Total: 28 files, 145 insertions(+), 145 deletions(-)

## External actions
Push to remote after handoff complete.

## Verification

G1 TRANSPORT: PASS
- `.agent/authored/f280-r10.md` sha256 = `a8099b8b013680cacc20d2161f16971146a97f85bf10862bc78831d9fc3cddd6` ✓
- `.agent/last_block.md` sha256 = `a8099b8b013680cacc20d2161f16971146a97f85bf10862bc78831d9fc3cddd6` ✓
- `.remedy-wt/gate_r9_entry.txt` last 3303 bytes match in live_review.md ✓
- `.remedy-wt/f280-r10-plan.md` matches committed plan.md ✓
- Exit code: 0

G2 THE RECORD (after C1): PASS
- `.agent/live_review.md`: 36 gates, 136 distinct R-ids, 7 Done ids ✓
- `.agent/plan.md`: 42 lines, 1 Goal, 1 Current Step, 1 Next Steps, 1 Risks ✓
- Exit code: 0

G3 THE PATCH (after C2): PASS
- Files changed: 28 (matches expected list exactly) ✓
- Total changes: 145 insertions(+), 145 deletions(-) ✓
- Renames detected: flight_plan.py -> job_plan.py, test_flight_plan.py -> test_job_plan.py, test_flight_plan_schema.py -> test_job_plan_schema.py ✓
- Exit code: 0

G4 THE BOUNDARY (after C2): PASS
- (a) Old identifiers (FlightPlanResult, etc.): 0 occurrences ✓
- (b) Persisted literals unchanged:
  - "flight_plan_approval": 35 occurrences ✓
  - "flight_plan_v1": 36 occurrences ✓
  - FLIGHT_PLAN_SCHEMA_V|_MAX_FLIGHT_PLAN_TASKS: 14 occurrences ✓
- Exit code: 0

G5 TARGETED TESTS (after C2): PASS
- 958 tests passed (exact match) ✓
- Exit code: 0

G6 FULL SUITE (after C2): PASS
- 17654 tests passed, 23 skipped ✓
- No failures (test_vitest_passes not in failed list) ✓
- Exit code: 0

G7 RUFF (after C2): PASS
- Exactly 1 error: UP035 on packages/orchestration/dag_schedule.py:36 ✓
- All other files clean ✓
- Pre-existing baseline confirmed ✓
- Exit code: 1 (expected due to error found)

G8 MUTATION RED-PROOF (disposable worktree): PASS
- Mutated `return approval` to `return None` in task_plan_blocks_execution ✓
- 4 tests failed as expected:
  - tests/cli/test_plan_approval.py::TestApprovalGateEnforcement::test_run_refused_while_pending
  - tests/cli/test_plan_approval.py::TestApprovalGateEnforcement::test_run_refused_while_rejected
  - tests/cli/test_plan_approval.py::TestApprovalGateEnforcement::test_rejected_cli_exit_3
  - tests/cli/test_plan_approval.py::TestApprovalGoldenPathCLI::test_full_approval_sequence
- 53 tests passed during mutation ✓
- Reverted mutation: 57 tests passed ✓
- Worktree removed, git worktree list shows only primary checkout ✓
- Exit code: 0 (after revert)

## Authored-text proofs
Block and source files byte-compared against committed targets: all match ✓

## Deviations & assumptions
None.

## Next
1. Phase 1 rule 1: verify `.agent/STOP` absent.
2. Reviewer verdict on round 10 after independent re-review.
3. Operator moves to next feature or next round (D5's second half) after closure.
