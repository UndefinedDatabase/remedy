# Plan

## Goal
Steps 35-37: Run Contract v0, Token Economy v0, Worker Adapter Foundation v0

## Status
COMPLETE — 2165 tests passing, all Steps 35-37 implemented

## Completed

### Step 35 — Run Contract v0
- [x] packages/orchestration/run_contract.py: RunContract dataclass, build_default, export JSON, summarize
- [x] packages/contracts/interfaces.py: RunContractProvider protocol
- [x] test_runner.py: R-0001 fix — assert→raise RuntimeError in execution safety guard
- [x] CLI: remedy run-contract (text + --json) + run_contract_inspected run-log event
- [x] Brain: NT_RUN_CONTRACT node type, ET_HAS_RUN_CONTRACT edge, detail builder

### Step 36 — Token Economy v0
- [x] packages/orchestration/token_policy.py: TokenPolicy dataclass, build_default, export JSON, summarize
- [x] packages/contracts/interfaces.py: TokenPolicyProvider protocol
- [x] CLI: remedy token-policy (text + --json) + token_policy_inspected run-log event
- [x] Brain: NT_TOKEN_POLICY node type, ET_HAS_TOKEN_POLICY edge, detail builder

### Step 37 — Worker Adapter Foundation v0
- [x] packages/orchestration/worker_adapters.py: WorkerProviderSpec, 5 provider specs, list/export/summarize
- [x] CLI: remedy workers (text + --json)
- [x] Brain: NT_WORKER_ADAPTER node type, ET_HAS_WORKER_ADAPTER edge, detail builder

### Tests + Docs
- [x] tests/test_run_contract.py: 27 tests
- [x] tests/test_token_policy.py: 28 tests
- [x] tests/test_worker_adapters.py: 18 tests
- [x] tests/test_execution_foundation.py: 13 tests (brain integration + protocols + R-0001)
- [x] tests/test_remedy_smoke_script.py: 12 new Step 35-37 assertions
- [x] scripts/remedy_smoke.sh: steps 12a-12d (run-contract, token-policy, workers, brain nodes)
- [x] docs/architecture.md: Steps 35-37 sections
- [x] 2165 tests passing

## Next
Commit. Push. Open PR.
