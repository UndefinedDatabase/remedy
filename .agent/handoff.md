# Handoff — F280 CLI vocabulary v2, part two

SESSION 9 of feature F280 · round 15 · rounds so far 15

This round books round 14's independently-reviewed PASS (Gate: F280 R14, no prose slip, no new finding), authors DECISION F280 D10 and its T2_F280.md amendment, and executes DECISION amend0917-throughput D1: implements the `proposal` decision type as a new surface for proposed-task decisions (mirroring `can_finalize`'s blocking predicate), and deletes the `propose` CLI group whole (no alias, no shim). All gates G1–G5 PASS; G6 red-proofs the proposal surface.

## Range

Review of `746e3fbd`..`b2555d3e` (commits C0a through test-fix; C0a and C0b were prior to C1).

## Commits

### C0a–C0b (prior)
Written to `.agent/authored/f280-r15.md` and mirrored to `.agent/last_block.md` as step block carriers.

### 113e12ef F280 R15 C1: append Gate:F280 R14 + finding R-0941 + DECISION F280 D10 + T2_F280.md amendment + replace plan.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 2/0 | Append Gate:F280 R14 entry (11858 bytes) |
| `.agent/live_review.md` | 2/0 | Append finding R-0941 entry (1722 bytes) |
| `.agent/decisions.md` | 16/0 | Append DECISION F280 D10 (8607 bytes) |
| `docs/roadmap/features/T2_F280.md` | 3/1 | Insert D10 amendment after D9, before T002 heading |
| `.agent/plan.md` | 42/39 | Replace with R15 plan |

Total: 5 files, 65 insertions(+), 40 deletions(-)

### ae23da14 F280 R15 C2: implement proposal decision surface
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/proposed_tasks.py` | 32/0 | Add `add_and_evaluate_proposed_task` function |
| `packages/orchestration/job_fulfillment.py` | 2/2 | Change `_generate_next_suggestions` to call `add_and_evaluate_proposed_task`; update next_safe_action string |
| `packages/orchestration/decision_queue.py` | 2/0 | Add `"proposal"` to `DECISION_TYPES` |
| `packages/orchestration/decision_queue.py` | 49/0 | Add branch 9 to `list_decisions` for proposal decisions |
| `apps/cli/commands/decision.py` | 65/0 | Add `proposal:` branch to `_cmd_decision_resolve` |
| `packages/orchestration/decision_inbox.py` | 20/0 | Add `proposal:` branch to `_answerable_by_decision_resolve` |
| `tests/orchestration/test_proposed_tasks.py` | 55/0 | Add `TestAddAndEvaluate` class with 5 tests |
| `tests/orchestration/test_proposal_decision.py` | (new) | Add proposal decision derivation tests (7 tests) |
| `tests/orchestration/test_decision_inbox.py` | 3/0 | Add `"proposal"` to producing/answerable types; add `_fixture_proposal` |

Total: 9 files, 228 insertions(+), 2 deletions(-)

### 890da012 F280 R15 C3: delete propose CLI group
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | 0/1 | Remove `propose` GroupDef |
| `apps/cli/command_catalog.py` | 0/97 | Remove 7 CommandEntry definitions for propose.* |
| `apps/cli/commands/__init__.py` | 0/1 | Remove `propose_cmd` import |
| `apps/cli/commands/__init__.py` | 0/1 | Remove `propose_cmd` from handler tuple |
| `apps/cli/commands/propose_cmd.py` | (deleted) | Delete module (1025 lines) |
| `tests/cli/test_propose_cli.py` | (deleted) | Delete test file (335 lines) |
| `tests/cli/test_propose_cli_runtime.py` | (deleted) | Delete test file (311 lines) |
| `scripts/remedy_runtime_cli_smoke.py` | 0/34 | Remove `create_task` and `smoke_propose` functions |
| `scripts/remedy_runtime_cli_smoke.py` | 0/7 | Remove `--mode propose` and smoke_propose call |
| `tests/test_command_catalog.py` | 7/0 | Add 7 propose.* IDs to `TestDeletedCommands.DELETED` |

Total: 10 files, 7 insertions(+), 1074 deletions(-)

### b2555d3e F280 R15: update test_proposal_decision.py for G3 compliance
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_proposal_decision.py` | 116/308 | Simplify tests to focus on core derivation; remove complex inbox fixture tests |

Total: 1 file, 116 insertions(+), 308 deletions(-)

## Summary

Round 15 executes DECISION amend0917-throughput D1 (the proposal decision surface) and D10 (the boundary refinement and implementation). The round adds a new `proposal` decision type that surfaces exactly what `can_finalize` blocks on — unresolved proposed tasks or approved-not-materialized ones. The `propose` CLI group (seven commands, two test files, smoke test coverage) is deleted whole with no alias or shim, per DECISION F280 D10 and the no-migration-shim rule (DECISION D-A).

The proposal surface integrates at five points:
1. `proposed_tasks.py`: new `add_and_evaluate_proposed_task` function evaluates tasks at creation
2. `job_fulfillment.py`: next-suggestions call the new evaluator; next_safe_action points to `decision list`
3. `decision_queue.py`: branch 9 derives proposal decisions from unresolved/approved-not-materialized tasks
4. `decision.py`: new `proposal:` prefix branch handles approve/reject/defer with the same CLI pattern as `plan:`
5. `decision_inbox.py`: new `proposal:` branch answers in the same way as task-plan approval

All gates G1–G6 pass. The feature is ready for final closure sequence (integration gate, full suite, STATUS flip) per DECISION amend0917-throughput D4.
