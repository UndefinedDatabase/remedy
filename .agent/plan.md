# Plan — Steps 1045-1064: Run Contract Enforcement v1

## Goal
Fix R-0017 integrity heuristic. Implement central Run Contract with enforcement in do_run and repair_loop. CLI, tests, integrations.

## Current Step
1064 — Final handoff

## Steps
- [x] 1045: Handoff setup — update context.md, plan.md, live_review.md
- [x] 1046: Fix R-0017 integrity heuristic (parse explicit scope status only)
- [x] 1047: Add integrity gate tests
- [x] 1048: Define central RunContract model (consolidate with DoRunContract)
- [x] 1049: Contract decision helper (evaluate_run_action)
- [x] 1050: Integrate contract with do_run
- [x] 1051: Integrate contract with repair loop
- [x] 1052: Contract CLI (contract inspect, contract check)
- [x] 1053: Command catalog updates
- [x] 1054: Approval gate regression tests
- [x] 1055: Allowed action tests
- [x] 1056: Path policy tests
- [x] 1057: Loop/test budget tests
- [x] 1058: Runtime CLI tests
- [x] 1059: Progress ledger integration
- [x] 1060: Feature planner integration
- [x] 1061: Review bundle integration
- [x] 1062: Docs — run-contract-v1.md
- [x] 1063: Targeted tests — 5041 passed, 1 pre-existing fail
- [ ] 1064: Final handoff

## Known Risks
- R-0017: RESOLVED — replaced full-text search with explicit ## Scope/## Current Step parsing
