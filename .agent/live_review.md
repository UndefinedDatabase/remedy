# Live Review — Steps 1065-1084

Reviewer: parallel reviewer
Scope: Run Contract — Persisted, Enforceable Source of Truth
Timestamp: 2026-06-11

## Verdict
PASS WITH RISKS — all blockers/high resolved, 2 low findings remain

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS
- Steps 1030-1044: PASS WITH RISKS (R-0017 resolved in 1045-1064)
- Steps 1045-1064: PASS — R-0017/R-0018/R-0019/R-0020 all resolved. 126 tests pass.

## Finding Ledger

### R-0021: .environment.py blocked by .env denied path rule

- **Status**: Resolved
- **Severity**: Blocker
- **Area**: path-policy
- **Details**: `_check_path_policy` used `normalized.startswith(denied)` causing `.environment.py` to match `.env`.
- **Resolution**: Step 1074 introduced `_path_matches()` at `run_contract.py:564-571` with segment-aware exact+directory-prefix matching. Test at `test_run_contract.py:196-200` confirms `.environment.py` allowed, `.env` blocked, `.env/foo` blocked, `node_modules_backup/` not blocked by `node_modules/`.

### R-0022: Contract not persisted — rebuilt fresh on every access

- **Status**: Resolved
- **Severity**: Blocker
- **Area**: contract-storage
- **Details**: No contract saved to job or disk.
- **Resolution**: Step 1066 added `save_contract()`, `load_contract()`, `ensure_contract()` at `run_contract.py:247-271`. Contract stored in `job.metadata["run_contract"]`. Tests at `test_run_contract.py:322-381` confirm roundtrip, stable contract_id/created_at, JSON survival.

### R-0023: do_run uses private DoRunContract instead of central RunContract

- **Status**: Resolved
- **Severity**: Blocker
- **Area**: do-flow
- **Details**: `do_run.py` created its own `DoRunContract` with different action lists.
- **Resolution**: Step 1070 replaced `DoRunContract` with `ensure_contract(job)` at `do_run.py:229`. `DoRunContract = None` at line 128 (removed class). `_check_contract()` now takes central RunContract directly.

### R-0024: repair_loop constructs independent private contract

- **Status**: Resolved
- **Severity**: High
- **Area**: repair-loop
- **Details**: `repair_loop.py` created inline `RunContract` with hardcoded actions.
- **Resolution**: Step 1071 replaced inline contract with `ensure_contract(job)` at `repair_loop.py:104`. Same persisted contract as do_run and CLI.

### R-0025: No usage ledger — budget enforcement from caller-supplied values only

- **Status**: Resolved
- **Severity**: High
- **Area**: usage-ledger
- **Details**: No usage persistence. Budget values lost after reload.
- **Resolution**: Step 1075 added `RunUsage` dataclass, `save_usage()`/`load_usage()`, `check_budget()` at `run_contract.py:292-391`. Both `do_run.py:419-421` and `repair_loop.py:239-241` record usage. `evaluate_run_action()` accepts `usage` param and checks budgets. Tests at `test_run_contract.py:492-582` confirm persistence, roundtrip, enforcement.

### R-0026: empty allowed_paths permits all path writes

- **Status**: Resolved
- **Severity**: High
- **Area**: path-policy
- **Details**: Empty `allowed_paths` means no path restriction — could be surprising.
- **Resolution**: Documented explicitly at `docs/run-contract-v1.md:35`. Test at `test_run_contract.py:190-194` confirms behavior. Denied paths still enforced. This is intentional for v1.

### R-0027: high_risk_command_execution not in canonical action vocabulary

- **Status**: Open
- **Severity**: Low
- **Area**: canonical-actions
- **Details**: `_DEFAULT_REQUIRES_APPROVAL` at `run_contract.py:178` contains `"high_risk_command_execution"` which is not a `ContractAction` constant and not in `ALL_KNOWN_ACTIONS`. `validate_run_contract()` would flag it as unknown on a default contract. Not breaking — `requires_approval_for` is not checked by `validate_run_contract()` currently. But inconsistent with canonical vocabulary goal.
- **Evidence**: `python3 -c "from packages.orchestration.run_contract import ALL_KNOWN_ACTIONS; print('high_risk_command_execution' in ALL_KNOWN_ACTIONS)"` returns `False`.
- **Expected fix**: Either add `HIGH_RISK_COMMAND = "high_risk_command_execution"` to `ContractAction`, or replace with a canonical name.

### R-0028: docs/run-contract-v1.md stale after Steps 1065-1080

- **Status**: Resolved
- **Severity**: Low
- **Area**: handoff
- **Details**: Three stale claims: DoRunContract reference, "no user-configurable", "no budget enforcement".
- **Resolution**: Commit `ee39c3a` updated both `docs/run-contract-v1.md` and `docs/do-run-v1.md`. Zero `DoRunContract` references remain. Persistence, contract set, and budget enforcement documented.

## Review Cycle Checks

| # | Check | Status | Evidence |
|---|-------|--------|----------|
| 1 | Handoff reconciliation | PASS | context.md, plan.md, live_review match branch feature/steps-1065-1084-run-contract-ssot |
| 2 | Contract persistence | PASS | save/load/ensure roundtrip verified. contract_id stable. created_at stable. JSON survives. |
| 3 | Canonical actions | PASS (low risk) | ALL_KNOWN_ACTIONS=17. Default contract uses only canonical. R-0027 low. |
| 4 | Central enforcement | PASS | do_run, repair_loop, contract CLI, review_bundle all use ensure_contract(). |
| 5 | Path policy | PASS | Segment-aware _path_matches(). .environment.py safe. Traversal/absolute blocked. |
| 6 | Usage ledger | PASS | RunUsage persisted. Loops/tests enforced from usage. Budget check in evaluate_run_action. |
| 7 | Budget enforcement | PASS | check_budget() covers loops, test_runs, runtime, tokens, cost. Exhausted blocks actions. |
| 8 | Contract config CLI | PASS | contract set is metadata-only, validates, limited SETTABLE_FIELDS, no repo mutation. |
| 9 | CLI runtime | PASS | subprocess, timeout=30, no shell=True, JSON parses, missing job safe. |
| 10 | Progress/feature/review | PASS | extract_contract_decisions_from_events. review_bundle uses ensure_contract + load_usage. |
| 11 | Redaction | PASS | No raw source/diff/artifact/stdout/stderr/secrets in new code. |
| 12 | Approval gate | PASS | source_apply not imported in do_run or repair_loop. stop_before_apply enforced. |

## Test Status
- CONFIRMED: 4996 passed, 8 skipped, 1 pre-existing fail (test_project_brain.py::test_full_chain_order — not caused by this block).
- Full suite run on 2026-06-11 post-commit ee39c3a.

## Final Review

| Area | Status |
|------|--------|
| Handoff | PASS |
| Contract persistence | PASS |
| Canonical actions | PASS (R-0027 low) |
| Validation | PASS |
| Central enforcement | PASS |
| Path policy | PASS |
| Usage ledger | PASS |
| Budget enforcement | PASS |
| CLI config/runtime | PASS |
| Progress/feature/review | PASS |
| Redaction | PASS |
| Tests | PASS — 4996 passed, 1 pre-existing fail |
| Remaining findings | 1 (R-0027 low) |
| Merge readiness | PASS WITH RISKS — 1 low naming item (R-0027), carry to next block |
