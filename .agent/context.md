# Context

## Active Branch
feature/steps-2026-2075-managed-external-builder-execution-v1-dogfood-observability (forked from
clean main at 8e7d2e5 after PR #75 merged Main Builder Adapter v0). No drift.

## Mainline reconciliation (Step 2026)
- PR #75 MERGED → main (auto-merge on reviewer PASS per merge-autonomy). Current main commit: 8e7d2e5.
  Main Builder Adapter v0 reviewer verdict PASS @ 786beb9 (zero open findings). Targeted 610 passed;
  full suite 6360 passed.
- Main Builder Adapter v0 (1961-2025) landed: main_builder_adapter.py (models/registry/request packages/
  session lifecycle/fixture builder/recommendation/mission signal/integrity); 10 CLI commands; 6
  run_contract actions; progress/feature/review/cockpit integration; 12 integrity codes.
- Carried risks reconciled below. No feature code before mainline closure.

## Scope
Steps 2026-2075: Managed External Builder Execution v1 + Dogfood Observability — the first managed
execution seam for external builder adapters. Adds bounded command templates, operator approval gate,
managed subprocess runner (argv only, no shell), session tracking, redacted output refs, event/replay/
debug bundles, sandbox intake integration, repair/mission state consumption, and dogfood observability.

## Core principle
Workers execute. Remedy governs. Builder output is UNTRUSTED until sandbox intake, trust/quality
checks, review, apply proof, and re-test gates pass. No provider monopoly — all adapter types
replaceable. Subprocess is allowed ONLY through bounded command templates with sanitized env, argv
list (no shell=True), timeout, and output cap.

## Reused existing infra (DO NOT reinvent)
- main_builder_adapter.py (BuilderAdapterSpec/RequestPackage/SessionRecord, registry, session lifecycle)
- external_builder_sandbox.py (safe ingress, quarantine, intake_provider_repair)
- real_test_execution.py (_argv_is_safe, _SHELL_METACHARS, _FORBIDDEN_TOKENS patterns)
- worker_registry.py, builder_routing.py, token_economy.py, model_route_tournament.py
- candidate_quality.py, repair_loop_v2.py, overnight_mission.py, proof_chain.py
- provider_trust (_scrub_public, _safe_path_label, _SK_PATTERN)
- progress_ledger / feature_planner / review_bundle / ui_server for integration surfaces
- run_contract (ContractAction, _DEFAULT_ALLOWED_ACTIONS) for action gating
- command_catalog (CATALOG, GROUPS, CommandEntry, ArgDef) for CLI registration

## Carried residual risks
- Real rollback RESTORE still NOT implemented (Snapshot/Rollback Proof are honest metadata-only).
- Real adapters are NOT configured yet — all disabled by default, no secrets committed.
- MemPalace remains a FUTURE external adapter / building block, NOT Remedy core.
- No internal long-term memory / embeddings / vector DB.
- Token/cost estimated bands; tournament evidence shared-route granularity.
- Full overnight autonomy still requires safe worker execution + approval/apply gates (future).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser blocker.

## Block constraints (2026-2075)
- May create managed execution module, command templates, approval gate, managed runner (subprocess
  with argv list only), event ledger entries, dogfood debug bundles, CLI surfaces, integrity checks,
  docs, tests.
- Subprocess is allowed ONLY in the managed runner function with: argv list (no shell=True), sanitized
  env (allowlisted vars only), hard timeout, output byte cap, no network/secrets passthrough.
- NO arbitrary shell execution (shell=True FORBIDDEN). NO unconstrained subprocess. NO direct provider
  SDK calls. NO auto-apply/approve/PR/git. NO MemPalace/memory/embeddings. NO UI redesign. NO MCP.
- Builder output is ALWAYS untrusted: goes through External Builder Sandbox / Trust Gate / Candidate
  Quality / review / re-test gates. No direct repo write.
- All real adapters disabled by default. Managed runner disabled by default (needs operator enable).

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh`; full suite once at block end with
  `-k "not test_full_chain_order"`. CLI runtime tests use the approved runner only.

## Changed files (Steps 2026-2075) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/managed_builder_execution.py | NEW core module: CommandTemplate/ExecutionApproval/ExecutionEvent/ManagedExecutionResult + template registry + approval gate + managed runner (shell=False, sanitized env, timeout, output cap) + event ledger + debug bundle + mission signal + integrity | bounded managed execution seam |
| packages/orchestration/run_contract.py | EXECUTION_TEMPLATE_SHOW/CREATE, EXECUTION_APPROVE/RUN/SHOW/DEBUG_BUNDLE (default-allowed) | contract gate |
| apps/cli/commands/managed_builder_execution_cmd.py | NEW handlers: execution template-list/show/create, approve, run, show, list, debug-bundle, integrity | CLI surface |
| apps/cli/commands/__init__.py | register managed_builder_execution_cmd | wire handlers |
| apps/cli/command_catalog.py | 9 execution-group entries (read_only/write_metadata/approval_gate/test_execution) + execution group def | catalog-backed |
| packages/orchestration/overnight_mission.py | _gather_mission_evidence consumes managed_execution_mission_signal (blocked→user decision) | mission consumes execution state |
| packages/orchestration/progress_ledger.py | extract/merge_managed_execution_items (blocked/running/failed/completed) + build wiring | honest progress surface |
| packages/orchestration/feature_planner.py | managed-execution-blocked/failed/completed required-blocker rules | evidence-based required blockers |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 35→36 + _build_managed_execution_summary | safe bundle summary |
| packages/orchestration/ui_server.py | _build_managed_execution_section cockpit (live=bool(running); no mutation) | read-only cockpit |
| tests/orchestration/test_managed_builder_execution.py | NEW unit + arch guards (52 tests) | coverage |
| tests/cli/test_managed_builder_execution_cli.py | NEW CLI tests (7 tests) | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==36 + managed_execution_summary assert | bundle test |
| docs/managed-external-builder-execution-v1.md | NEW architecture doc | document + honesty |
| docs/managed-external-builder-execution-user-guide-v1.md | NEW user guide | user-facing |
| .agent/context.md, .agent/plan.md, .agent/live_review.md | reconciliation + changed-files table | handoff |

## Status
Steps 2026-2075 IN PROGRESS. Mainline closed (PR #75 → main 8e7d2e5). Builder work complete.
Parallel reviewer owns the live_review verdict. Reviewer findings start at R-0106.

## Next block
Ollama Cheap-Task Adapter v0 OR Overnight Autonomy Gate v1 (only after this block PASS).
