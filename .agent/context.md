# Context

## Active Branch
feature/steps-2076-2125-managed-execution-approval-dogfood-observability-hardening-v1-1
(forked from clean main at 1970b7c after PR #76 merged Managed External Builder Execution v1).

## Mainline reconciliation (Step 2076)
- PR #76 MERGED → main (auto-merge on reviewer PASS per merge-autonomy). Current main: 1970b7c.
  Managed External Builder Execution v1 reviewer verdict PASS @ b3a8182 (zero open findings).
  Targeted 630 passed; full suite 6427 passed.
- v1 landed: managed_builder_execution.py (CommandTemplate/ExecutionApproval/ExecutionEvent/
  ManagedExecutionResult + template registry + approval gate + managed runner + event ledger +
  debug bundle + mission signal + integrity); 9 CLI commands; 6 run_contract actions; progress/
  feature/review/cockpit integration; 52 unit tests + 7 CLI tests.

## Scope
Steps 2076-2125: Managed Execution Approval + Dogfood Observability Hardening v1.1 — hardens the
approval model (expiry, caps, session/package/adapter/template binding), adds approval validation
function (11 codes), extends events/debug bundle, extends integrity checks, adds structured
logging bridge, hardens CLI/review/progress/cockpit surfaces.

## Core principle
Workers execute. Remedy governs. Approval must be scoped, expiring, bounded, auditable. One
approval cannot authorize unlimited runs. Template kind must match adapter kind. Builder output
remains untrusted. Done ≠ Resolved.

## Key gaps in v1 approval (what this block fixes)
1. No expiry (approval lives forever)
2. No per-approval caps (max_runs, max_runtime, max_output)
3. No binding to adapter_id or package_id
4. No one-shot policy (approval reusable indefinitely)
5. No session existence check before approval
6. No adapter_kind matching (approval ignores template.adapter_kind vs session adapter)
7. No used_count tracking
8. No approval_scope enum (single_run vs session_lifetime vs time_bounded)

## Block constraints (2076-2125)
- May modify: managed_builder_execution.py (approval model + validation + runner + events +
  debug bundle + integrity), CLI commands, review bundle, progress ledger, cockpit, docs, tests.
- NO arbitrary shell execution. NO shell=True. NO provider SDK. NO auto-apply/approve/PR/git.
- NO MemPalace/memory/embeddings/MCP. NO UI redesign. NO repo-wide logging refactor.
- Builder output ALWAYS untrusted. execution_satisfies_mission stays hardcoded False.

## Carried residual risks
- Real rollback RESTORE still NOT implemented (metadata-only).
- Real adapters NOT configured — all disabled by default, no secrets committed.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser blocker.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh`; full suite once at block end.
  CLI runtime tests use approved runner only.

## Status
Steps 2076-2125 IN PROGRESS. Mainline closed (PR #76 → main 1970b7c). Implementation starting.
