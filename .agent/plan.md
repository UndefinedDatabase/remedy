# Plan — Steps 1065-1084: Run Contract SSOT + Budget Ledger

## Goal
Make one persisted RunContract per job the single authority. Add usage ledger with budget enforcement. Fix path policy precision.

## Current Step
1070 — Replace DoRunContract as authority in do_run

## Steps
- [x] 1065: Reconcile handoff state — update .agent/ files, confirm previous block committed
- [x] 1066: Persist one RunContract per job (load/save/ensure APIs) — 38 tests pass
- [x] 1067: Contract migration for old jobs — lazy via ensure_contract, 43 tests pass
- [x] 1068: Canonical action vocabulary — ContractAction class, ALL_KNOWN_ACTIONS, 53 tests
- [x] 1069: Contract validation — validate_run_contract(), 53 tests
- [ ] 1070: Replace DoRunContract as authority in do_run
- [ ] 1071: Use same contract in repair_loop (no private contracts)
- [ ] 1072: CLI uses persisted contract
- [ ] 1073: Add `contract set` CLI command
- [ ] 1074: Precise path policy (fix `.env` vs `.environment.py`)
- [ ] 1075: Run Usage Ledger (RunUsage, RunBudgetStatus)
- [ ] 1076: Enforce all budgets via usage ledger
- [ ] 1077: Record usage in do_run and repair_loop
- [ ] 1078: Contract decision events
- [ ] 1079: Progress ledger auto-integration from events
- [ ] 1080: Feature planner auto-integration from blockers
- [ ] 1081: Review bundle uses active persisted contract
- [ ] 1082: Runtime CLI tests
- [ ] 1083: Tests and docs update
- [ ] 1084: Final handoff with changed files table

## Known Risks
- R-0017: RESOLVED
- Path policy `.env` false positive: Fix target Step 1074
