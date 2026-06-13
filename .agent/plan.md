# Plan — Steps 1220-1244: Approved Repair Apply Cycle v1

## Goal
Apply an APPROVED repair patch intent through the existing `do continue` path:
approval → snapshot → apply → linked test → proof → truthful stop. On pass:
mark failure repaired + attempt tested_passed (only with snapshot + linked passing
test + proof). On fail: link a new failure, no auto-loop. No bypass apply.

## Current Step
1244 — Final handoff (complete; full suite 5432 green; awaiting reviewer verdict)

## Steps
- [x] 1220: Handoff reconciliation (1193-1219 merged PR #53; scope→1220-1244; new branch)
- [x] 1221: Repair intent classification (repair_kind/expected_effect/original_* IDs)
- [x] 1222: Continue eligibility accepts approved repair intent (verify + tests)
- [x] 1223: Apply repair via existing continue/apply service (no bypass); carry repair IDs
- [x] 1224: Link test run to repair apply (no duplicate usage on retry)
- [x] 1225: RepairAttempt state machine (proposed..tested_passed/failed/superseded)
- [x] 1226: resolve_failure_if_repaired (snapshot+linked passing test+proof only)
- [x] 1227: Proof Chain repair awareness
- [x] 1228: File Provenance repair awareness
- [x] 1229: Progress Ledger repair-apply items
- [x] 1230: Feature Planner repair follow-up
- [x] 1231: Review Bundle repair_cycle_summary
- [x] 1232: Operator Cockpit read-only repair-apply counts (or defer + document)
- [x] 1233: Optional deterministic source fixture repair (only if safe; else docs-only + proof test)
- [x] 1234: Idempotency + crash resume tests
- [x] 1235: CLI runtime E2E (tiny repos)
- [x] 1236: Redaction tests
- [x] 1237: Architecture guards
- [x] 1238: Docs (repair-loop-v1, do-continue-v1, snapshot-rollback-v1)
- [x] 1239: Targeted tests + full pytest once
- [x] 1240: PR strategy draft (whole branch; title reflects full line)
- [x] 1241: Live review (findings/Done/verdict)
- [x] 1242: Merge gate
- [x] 1243: Product readiness update
- [x] 1244: Final handoff

## Hard rules
- No shell=True. No background pytest. scripts/remedy_pytest.sh; full suite once at end.
- Apply ONLY through existing approved continue/apply service. Snapshot mandatory.
  Test Execution Service is the only test path.
- Repair Loop never imports/calls source_apply/patch_apply/test_execution/provider.
- No auto-approve, no auto-revert, no auto repair loop, no multi-cycle.
- No raw stdout/stderr/source/diff/artifact-body/secrets/tracebacks/abs paths anywhere.
- Repair status never "verified" unless linked test passes after repair apply.
- Idempotent: retry no double-apply / no double test budget / no duplicate failure /
  no double-resolve. All next_safe_action commands exist in catalog.
- docs-only repair must NOT be claimed a source fix without test+proof truth.

## Next block
Bounded Overnight Preparation v0 OR Provider-backed Repair Builder.
