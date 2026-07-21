# Plan — F018 Budgets & Stop Conditions — Authority & Integration Round

## Goal
Close 14 external review findings. All source fixes applied, 28 new integration
tests pass, existing tests updated (3 tests that pinned unsafe behavior replaced
with fail-closed assertions).

## Status: COMPLETE — Evidence + ZIP delivered

## Completed
- [x] Scope 1: Fail-closed config + durable JobPlan budget persistence
- [x] Scope 2: Canonical RunManifest + Actuals authority
- [x] Scope 3: Stable stop identity, wall clock + Decision Queue
- [x] Scope 4: RunContract reconciliation + honest budget CLI
- [x] Scope 5: 28 integration tests pass, existing tests fixed
- [x] 6 logical commits (d91fd5e → 48b73a2)
- [x] Updated docs: STATUS.md, T0_F018.md, context.md
- [x] Fresh Evidence via create_manual_completion_bundle
- [x] Canonical READY_FOR_REVIEW ZIP
- [x] Mandatory detailed handoff

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].
