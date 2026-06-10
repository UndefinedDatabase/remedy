# Live Review — Steps 1065-1084

Reviewer: parallel reviewer
Scope: Run Contract — Persisted, Enforceable Source of Truth
Timestamp: 2026-06-10

## Verdict
PENDING — 3 blockers, 3 high open (baseline gaps for worker to address)

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS
- Steps 1030-1044: PASS WITH RISKS (R-0017 resolved in 1045-1064)
- Steps 1045-1064: PASS — R-0017/R-0018/R-0019/R-0020 all resolved. 126 tests pass.

## Finding Ledger

### R-0021: .environment.py blocked by .env denied path rule

- **Status**: Open
- **Severity**: Blocker
- **Area**: path-policy
- **Details**: `_check_path_policy` at `run_contract.py:297` uses `normalized.startswith(denied)` which causes `.environment.py` to match `.env` because the string `.environment.py` starts with `.env`. This is not segment-aware matching.
- **Evidence**: `evaluate_run_action(c, 'write_metadata', path='.environment.py')` returns `allowed=False, reason="Path '.environment.py' matches denied path '.env'"`.
- **Expected fix**: Make path matching segment-aware. `.env` should only match `.env` exactly or `.env/...` (directory prefix), not `.environment.py`. Use exact+directory-prefix matching only.
- **Fix target**: Step 1074

### R-0022: Contract not persisted — rebuilt fresh on every access

- **Status**: Open
- **Severity**: Blocker
- **Area**: contract-storage
- **Details**: `build_default_run_contract()` creates a new contract every call. No contract is saved to the job or to disk. Four independent contract constructions — no single source of truth.
- **Fix target**: Step 1066

### R-0023: do_run uses private DoRunContract instead of central RunContract

- **Status**: Open
- **Severity**: Blocker
- **Area**: do-flow
- **Details**: `do_run.py` creates its own `DoRunContract` with its own action lists that differ from `RunContract` defaults.
- **Fix target**: Step 1070

### R-0024: repair_loop constructs independent private contract

- **Status**: Open
- **Severity**: High
- **Area**: repair-loop
- **Details**: `repair_loop.py` creates its own `RunContract` inline with hardcoded actions, invisible to CLI and review bundle.
- **Fix target**: Step 1071

### R-0025: No usage ledger — budget enforcement from caller-supplied values only

- **Status**: Open
- **Severity**: High
- **Area**: usage-ledger
- **Details**: No usage tracking persisted. After job reload, usage lost. runtime/token/cost fields exist but never checked.
- **Fix target**: Step 1075

### R-0026: empty allowed_paths permits all path writes

- **Status**: Open
- **Severity**: High
- **Area**: path-policy
- **Details**: When `allowed_paths` is empty (default), all paths not in denied_paths are writable. Document explicitly or change default.
- **Fix target**: Step 1074 (document behavior)

## Baseline Checks (Pre-Worker)

| Check | Status |
|-------|--------|
| Handoff | IN PROGRESS — context.md updated, plan.md updated |
| Contract persistence | FAIL — no persistence, rebuilt every call |
| Canonical actions | WARN — do_run and repair_loop use different action lists |
| Central enforcement | FAIL — 4 independent contract constructions |
| Path policy | FAIL — .environment.py blocked by .env rule |
| Usage ledger | FAIL — no persistence, no measured enforcement |
| CLI runtime | PASS from prior block (6/6 tests) |
| Redaction | PASS from prior block |
