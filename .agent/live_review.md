# Live Review — Steps 2076-2125: Managed Execution Approval + Dogfood Observability Hardening v1.1

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): approval model hardening (expiry/caps/binding); approval validation helper;
session/package/adapter/template binding verification; event ledger/debug bundle hardening;
managed execution CLI hardening; review bundle/progress/cockpit observability; managed execution
integrity checks; small structured logging bridge; docs/tests.
Must NOT: real provider execution; provider SDK; direct repo mutation; auto-apply; auto-approval;
auto-PR/git; hidden browser; arbitrary shell; shell=True; raw transcript/candidate/prompt/log leaks;
secret/env token storage; hardcoded provider monopoly; MemPalace; embeddings/vector DB; UI redesign;
MCP; repo-wide logging refactor.
APPROVAL HARDENING BLOCK — turns managed execution from safe prototype into operator-grade dogfood.
Hard invariants: approval scoped+expiring+bounded+auditable; approval binds session/package/adapter/
template; stale approvals cannot execute; one approval cannot authorize unlimited runs; template kind
must match adapter kind; debug bundle explains failures without raw leaks; builder output remains
untrusted; run output cannot mark repair/mission done; Done ≠ Resolved; reviewer verdict beats
self-report.
Timestamp: 2026-06-16

## Verdict (reviewer-owned)
PENDING — builder commit with all 5 fixes + 19 new/updated tests incoming.
Targeted 102 + CLI 10 passed. Full suite running. Awaiting reviewer re-verdict.

## Changed files (Steps 2076-2125 @ e7bef89)
| File | What changed |
|------|-------------|
| packages/orchestration/managed_builder_execution.py | +380L: ApprovalScope, ExecutionApproval hardened (package_id/adapter_id/adapter_kind/expires_at/max_runs/used_count/max_runtime_seconds/max_output_bytes/approval_scope); validate_execution_approval (11 codes); _increment_approval_used_count; audit_approval_safety (10 codes); 7 new event kinds; debug bundle includes approval_validation/repair_suggestion; structured logging bridge |
| apps/cli/commands/managed_builder_execution_cmd.py | +42L: _cmd_approve passes binding fields; approval-show/validate/list CLI handlers |
| apps/cli/command_catalog.py | +38L: 3 new catalog entries (approval-show/validate/list, all read_only); approve gets binding args |
| packages/orchestration/run_contract.py | +7L: 3 new EXECUTION_APPROVAL_* contract actions |
| packages/orchestration/feature_planner.py | +13L: 2 approval-specific repair rules |
| packages/orchestration/progress_ledger.py | +15L: distinguishes approval-specific blocks in summary |
| packages/orchestration/review_bundle.py | +23L: approval counts in managed_execution_summary |
| packages/orchestration/ui_server.py | +15L: active_approval_count in cockpit |
| tests/orchestration/test_managed_builder_execution.py | +368L: TestApprovalValidation (8 tests), TestApprovalIntegrity (8 tests), TestDebugBundleHardening (2 tests), TestRunnerApprovalEnforcement (5 tests) |
| tests/cli/test_managed_builder_execution_cli.py | +19L: approval-show/validate/list CLI tests |
| tests/orchestration/test_review_bundle.py | no change in this block |
| docs/managed-external-builder-execution-v1-1-hardening.md | NEW: hardening doc |

## Check matrix (Steps 2076-2125 @ e7bef89 + uncommitted WIP)
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Mainline closure | PASS | PR #76 merged → main 1970b7c; fresh branch; zero feature work before closure |
| 2 | Approval model | PARTIAL | Committed: has session_id/package_id/adapter_id/template_id/max_runs/used_count/max_runtime_seconds/max_output_bytes/approval_scope. WIP: default 30-min expires_at added. MISSING in commit: default expiry (R-0106) |
| 3 | Approval validation | PARTIAL | Committed: 11 codes. WIP: session binding via real BuilderSessionRecord. MISSING in commit: session/adapter binding (R-0107) |
| 4 | Managed run binding | PARTIAL | WIP: used_count moved before subprocess. MISSING in commit: failed/timeout consume approval (R-0108) |
| 5 | Event/debug observability | PASS | 7 new event kinds; debug bundle includes approval_validation, repair_suggestion, event timeline; no raw leaks |
| 6 | CLI | PASS | approval-show/validate/list; approve with binding args; JSON-safe; invalid IDs don't traceback |
| 7 | Review Bundle / Progress / Cockpit | PASS | approval counts visible; approval-specific blocks distinguished; cockpit read-only; no mutation |
| 8 | Integrity | PARTIAL | audit_approval_safety covers 10 codes. WIP: missing_expires_at added. MISSING in commit: missing expiry flag (R-0106) |
| 9 | Structured logging bridge | PASS | _log.info in _append_event with safe IDs/summary; no repo-wide refactor |
| 10 | Architecture guards | PASS | No provider SDK; no shell=True; no auto-apply/approve; execution_satisfies_mission=False hardcoded |

## Findings — Steps 2076-2125

### R-0106 — Approval default expiry (Medium, Done)
**Status**: Done. DEFAULT_APPROVAL_EXPIRY_SECONDS=1800 auto-set in approve_managed_execution.
Empty expires_at → approval_expired in validate_execution_approval. missing_expires_at in audit_approval_safety.
4 targeted tests: default future expiry, missing expiry invalid, expired blocks execution, integrity flags.
**Done: R-0106** — awaiting reviewer verdict.

### R-0107 — Real session/package/adapter/template binding (High, Done)
**Status**: Done. _validate_session_binding loads real BuilderSessionRecord via load_builder_session.
Validates package_id/adapter_id/adapter_kind/adapter_enabled against real session + adapter spec.
Graceful when session absent (no binding errors if no session to validate against).
3 targeted tests: missing session no error, package mismatch detected, valid session passes.
**Done: R-0107** — awaiting reviewer verdict.

### R-0108 — used_count counts allowed starts (Medium, Done)
**Status**: Done. _increment_approval_used_count moved before subprocess.run (line 1024).
Approval consumed on allowed start, not on successful exit. Argv failure does NOT consume.
3 targeted tests: failed run consumes, single-run blocks after failed run, argv failure doesn't consume.
**Done: R-0108** — awaiting reviewer verdict.

### R-0109 — Controlled builder execution classification (Medium, Done)
**Status**: Done. action_class changed to "controlled_builder_execution" in command_catalog.py.
2 targeted tests: catalog asserts correct action_class, rejects test_execution.
**Done: R-0109** — awaiting reviewer verdict.

### R-0110 — Dogfood observability and integrity (Low, Done)
**Status**: Done. audit_execution_result_safety extended with events parameter.
4 new violation codes: completed_missing_output_ref, completed_missing_started_event,
completed_missing_completed_event, result_claims_repair_or_mission_done.
Debug bundle includes binding_summary, event_sequence, output_ref_present, next_safe_action.
7 targeted tests: output_ref checks, event sequence checks, repair_done claim, bundle fields.
**Done: R-0110** — awaiting reviewer verdict.

Next id: R-0111.

## Reviewer test run (targeted)
62 passed, 1 failed in 0.14s (test_valid_approval: session_not_found from new binding validation in
builder WIP). Tests run against committed + uncommitted code.

## Reviewer audit log
- Block opened. Check 1 (mainline closure) PASS — PR #76 merged Managed External Builder Execution
  v1 (reviewer PASS @ b3a8182) → main 1970b7c. Fresh branch off merged main; ZERO feature commits
  before closure.
- Prior block 2026-2075 PASS @ b3a8182 (zero open findings) merged via PR #76 → main 1970b7c.
- Commit e7bef89 detected. Full line-level review of committed diff (+1076L, 14 files) + uncommitted
  WIP (+81L in managed_builder_execution.py and command_catalog.py).
- R-0106 (Medium): default expiry missing in committed code. Builder WIP adds DEFAULT_APPROVAL_EXPIRY_SECONDS=1800.
- R-0107 (High): no real session binding in committed code. Builder WIP adds _validate_session_binding.
  Test failing.
- R-0108 (Medium): used_count only on success in committed code. Builder WIP moves before subprocess.
- R-0109 (Medium): action_class="test_execution" in committed code. Builder WIP changes to
  "controlled_builder_execution".
- R-0110 (Low): integrity missing event-sequence and cross-entity checks.
- German scan: zero matches.
- Targeted tests: 62 passed, 1 failed (builder WIP test regression).
- Verdict PENDING: 1 High + 3 Medium + 1 Low open. Awaiting builder commit with fixes + passing tests.
