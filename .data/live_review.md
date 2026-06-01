# Live Review — Steps 269-276

Reviewer: parallel watcher (independent)
Scope: Steps 269-276 (Merge Gate Closure, Historical Suite Reconciliation, Source Apply Approval Gate)
Status: PASS
Started: 2026-06-01
Completed: 2026-06-01
Branch: feature/steps-247-252-data-honest-contract
Last check: full suite baseline verified

---

## Verdict: PASS

All prior findings resolved. R-3011 (broken test_steps_91_100 calls) fixed with `_make_approved_job()` helper. R-3012 (detector tests) fixed with real `_detect_constitution` integration tests. New approval gate added to `source_apply`. All 13 historical test suites pass (595 tests, 0 failures).

## Findings Resolution

| Finding | Status | Resolution |
|---------|--------|-----------|
| R-3011 (source_apply without job) | **FIXED** | All 6 calls updated with `_make_approved_job()` returning `(job, intent_id)`. 2 new gate tests added. |
| R-3012 (detector test gap) | **FIXED** | 9 new `TestConstitutionDiscoveryIntegration` tests call real `_detect_constitution` with fixture files. |
| R-3013 (stale test count) | **FIXED** | 595 tests verified independently, all pass. |

## New Work (Steps 269-276)

### Step 269 — Fix R-3011: Historical tests pass job= to source_apply
- `_make_permitted_job()` and `_make_approved_job()` helpers in test_steps_91_100.py
- All 6 TestSourceApply calls updated
- 2 new tests: `test_apply_without_intent_blocked`, `test_apply_with_pending_intent_blocked`

### Step 270 — Reconcile historical UI tests with Canvas/Force architecture
- test_steps_91_100.py: `ForceBrainGraph.tsx` checks, legacy path checks
- test_steps_101_110.py: Legacy brain flow, semantic zoom, organic layout paths
- test_steps_111_116.py: Legacy semanticZoom.ts path (3 tests fixed)

### Step 271 — Approval gate on source_apply
- `intent_id` parameter added (required for mutation)
- Gate checks: intent_id provided → intent exists → intent state == "approved"
- Permission check runs first (so job=None/denied tests still work without intent_id)
- test_steps_261_268.py: `_make_approved_job()` with real Job/Artifact models

### Step 272 — Autorun fixture repair for approval gate
- `_create_and_approve_fixture_intent()` creates MagicMock artifact with explanations
- `set_permission(job, Capability.repo_generated_write, allow=True)` at fixture start
- All 3 `apply_structured_patch` call sites in autorun.py pass intent_id=

### Step 273 — Command discovery constitution-level fixtures
- 9 new tests in `TestConstitutionDiscoveryIntegration`
- Tests call real `_detect_constitution` and `discover_commands` with fixture repos
- Shell metacharacters (|, &&, ;, >, <, `, $()) all rejected through real detector

### Step 274 — Legacy dashboard field classification
- 4 fields (`job_name`, `task_count`, `guidance`, `lifecycle`) moved under `"legacy"` key in ui_server.py
- UI reference updated: `dashboard.legacy?.job_name` in remedyApi.ts

### Step 275 — Full historical suite baseline
- 13 suites, 595 tests, 0 failures, 14.79s total

### Step 276 — This review

## Full Test Baseline

| Suite | Tests | Status |
|-------|-------|--------|
| test_steps_91_100.py | 50 | PASS |
| test_steps_101_110.py | 46 | PASS |
| test_steps_111_116.py | 54 | PASS |
| test_steps_172_201.py | 74 | PASS |
| test_steps_208_226.py | 38 | PASS |
| test_steps_247_252.py | 34 | PASS |
| test_steps_253_260.py | 37 | PASS |
| test_steps_261_268.py | 45 | PASS |
| test_command_discovery.py | 92 | PASS |
| test_autonomy_readiness.py | 22 | PASS |
| test_test_runner.py | 43 | PASS |
| test_command_catalog.py | 18 | PASS |
| test_cli_execution_loop_closure.py | 42 | PASS |
| **Total** | **595** | **ALL PASS** |

## Source Apply Approval Proof

```
apply_structured_patch(patch, repo_path, job=job)
  → permission check (is_allowed(job, Capability.repo_generated_write))
  → intent_id required (None → blocked)
  → intent must exist (get_patch_intent(job, intent_id))
  → intent state must be "approved" (not "pending"/"rejected")
  → only then: write to disk
```

Tests proving gate:
- `test_apply_without_intent_blocked` — no intent_id → "approval required: intent_id not provided"
- `test_apply_with_pending_intent_blocked` — pending intent → "state is 'pending', not 'approved'"
- `test_missing_intent_id_blocked` (261-268 suite) — same gate from real Job model

## Merge Readiness

**PASS.** All 595 tests green. All prior findings (R-3011, R-3012, R-3013) resolved. Approval gate enforced on source_apply. Historical test suites reconciled with Canvas/Force architecture. Legacy dashboard fields classified. No shell=True, no 0.0.0.0, no fake state.

---

## Previous Review History

### Steps 261-268: PASS WITH RISKS — findings resolved in 269-276
### Steps 253-260: PASS — findings resolved
### Steps 247-252: PASS WITH RISKS — findings resolved in 253-260
### Steps 227-246: PASS (Canvas Force Brain Graph)
