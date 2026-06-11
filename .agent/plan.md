# Plan — Steps 1065-1084: Run Contract SSOT + Budget Ledger

## Goal
Make one persisted RunContract per job the single authority. Add usage ledger with budget enforcement. Fix path policy precision.

## Current Step
1084 — Final handoff

## Steps
- [x] 1065: Reconcile handoff state — update .agent/ files, confirm previous block committed
- [x] 1066: Persist one RunContract per job (load/save/ensure APIs) — 38 tests pass
- [x] 1067: Contract migration for old jobs — lazy via ensure_contract, 43 tests pass
- [x] 1068: Canonical action vocabulary — ContractAction class, ALL_KNOWN_ACTIONS, 53 tests
- [x] 1069: Contract validation — validate_run_contract(), 53 tests
- [x] 1070: Replace DoRunContract — do_run uses central RunContract, 120 tests pass
- [x] 1071: repair_loop uses central contract via ensure_contract, 127 tests pass
- [x] 1072: CLI uses persisted contract via ensure_contract
- [x] 1073: `contract set` CLI command + catalog entry
- [x] 1074: Precise path policy — segment-aware matching, R-0021 fixed, 57 tests
- [x] 1075: Run Usage Ledger — RunUsage, RunBudgetStatus, save/load/check, 68 tests
- [x] 1076: Budget enforcement via usage in evaluate_run_action
- [x] 1077: Record usage in do_run and repair_loop — loops_used incremented
- [x] 1078: Contract decision events — emitted as timeline events
- [x] 1079: Progress ledger — auto-extract contract decisions from events
- [x] 1080: Feature planner — blockers flow through existing rules
- [x] 1081: Review bundle uses active persisted contract
- [x] 1082: Runtime CLI tests
- [x] 1083: Tests and docs update
- [x] 1084: Final handoff with changed files table

## Known Risks
- R-0017: RESOLVED
- Path policy `.env` false positive: Fix target Step 1074
